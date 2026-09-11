from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping

from veritrail_review.canonical import sha256_bytes
from veritrail_review.contracts import SnapshotAcquisitionBudget, git_path_ref
from veritrail_review.errors import SourceSnapshotError, SourceSnapshotFailureCode


@dataclass(frozen=True)
class GitAcquisition:
    algorithm: str
    commit_oid: str
    commit_tree_oid: str
    analysis_tree_oid: str
    inventory: tuple[dict[str, object], ...]
    blob_bytes_by_oid: Mapping[str, bytes]
    git_executable: Path
    git_version: str


@dataclass(frozen=True)
class _TreeEntry:
    mode: str
    name: bytes
    oid: str


class _BudgetState:
    def __init__(
        self,
        budget: SnapshotAcquisitionBudget,
        *,
        clock: Callable[[], float],
        stage_hook: Callable[[str], None] | None,
        deadline: float,
    ) -> None:
        self.budget = budget
        self._clock = clock
        self._stage_hook = stage_hook
        self.deadline = deadline
        self.unique_tree_oids: set[str] = set()
        self.unique_terminal_oids: set[str] = set()
        self.total_unique_tree_bytes = 0
        self.total_unique_terminal_bytes = 0
        self.expanded_tree_entries = 0
        self.terminal_inventory_entries = 0

    def checkpoint(self, stage: str) -> None:
        if self._stage_hook is not None:
            self._stage_hook(stage)
        if self._clock() >= self.deadline:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED
            )

    def remaining_seconds(self, stage: str) -> float:
        self.checkpoint(stage)
        remaining = self.deadline - self._clock()
        if remaining <= 0:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED
            )
        return remaining

    def admit_commit(self, size: int) -> None:
        self.checkpoint("commit-header")
        if size > self.budget.max_commit_bytes:
            self._exhausted()

    def admit_tree(self, oid: str, size: int) -> None:
        self.checkpoint("tree-header")
        if oid in self.unique_tree_oids:
            return
        if size > self.budget.max_single_tree_bytes:
            self._exhausted()
        if len(self.unique_tree_oids) + 1 > self.budget.max_unique_tree_objects:
            self._exhausted()
        if self.total_unique_tree_bytes + size > self.budget.max_total_unique_tree_bytes:
            self._exhausted()
        self.unique_tree_oids.add(oid)
        self.total_unique_tree_bytes += size

    def admit_terminal_object(self, oid: str, size: int) -> None:
        self.checkpoint("blob-header")
        if oid in self.unique_terminal_oids:
            return
        if size > self.budget.max_single_blob_bytes:
            self._exhausted()
        if self.total_unique_terminal_bytes + size > self.budget.max_total_unique_blob_bytes:
            self._exhausted()
        self.unique_terminal_oids.add(oid)
        self.total_unique_terminal_bytes += size

    def expand_tree_entry(self) -> None:
        self.checkpoint("tree-entry")
        if self.expanded_tree_entries + 1 > self.budget.max_expanded_tree_entries:
            self._exhausted()
        self.expanded_tree_entries += 1

    def add_terminal(self) -> None:
        self.checkpoint("terminal-entry")
        if self.terminal_inventory_entries + 1 > self.budget.max_terminal_inventory_entries:
            self._exhausted()
        self.terminal_inventory_entries += 1

    @staticmethod
    def _exhausted() -> None:
        raise SourceSnapshotError(SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED)


class _GitObjectReader:
    def __init__(
        self,
        repository_path: Path,
        git_executable: Path | None,
        state: _BudgetState,
    ) -> None:
        self._repository_path = _resolve_repository_path(repository_path)
        self._git_executable = _resolve_git_executable(
            git_executable, self._repository_path
        )
        self._state = state
        self._env = _controlled_git_environment()
        self._git_dir, object_format = self._open_repository()
        self.algorithm = {"sha1": "SHA1", "sha256": "SHA256"}.get(object_format, "")
        if not self.algorithm:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.UNSUPPORTED_OBJECT_FORMAT
            )
        self.oid_raw_size = 20 if self.algorithm == "SHA1" else 32
        self._tree_cache: dict[str, bytes] = {}
        self._terminal_cache: dict[str, tuple[str, bytes]] = {}
        self.git_version = self._read_git_version()

    @property
    def git_executable(self) -> Path:
        return self._git_executable

    def read_commit(self, oid: str) -> bytes:
        object_type, size = self._read_header(oid)
        if object_type != "commit":
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SOURCE_OBJECT_TYPE_MISMATCH
            )
        self._state.admit_commit(size)
        return self._read_verified_body(oid, object_type, size)

    def read_tree(self, oid: str) -> bytes:
        cached = self._tree_cache.get(oid)
        if cached is not None:
            self._state.checkpoint("tree-cache")
            return cached
        object_type, size = self._read_header(oid)
        if object_type != "tree":
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SOURCE_OBJECT_TYPE_MISMATCH
            )
        self._state.admit_tree(oid, size)
        body = self._read_verified_body(oid, object_type, size)
        self._tree_cache[oid] = body
        return body

    def read_terminal(self, oid: str) -> tuple[str, bytes]:
        cached = self._terminal_cache.get(oid)
        if cached is not None:
            self._state.checkpoint("blob-cache")
            return cached
        object_type, size = self._read_header(oid)
        self._state.admit_terminal_object(oid, size)
        body = self._read_verified_body(oid, object_type, size)
        result = (object_type, body)
        self._terminal_cache[oid] = result
        return result

    def _open_repository(self) -> tuple[Path, str]:
        try:
            raw_dir = self._run(
                ["-C", os.fspath(self._repository_path), "rev-parse", "--absolute-git-dir"],
                stage="repository-location",
                repository_open=True,
            ).rstrip(b"\r\n")
            if not raw_dir:
                raise ValueError
            git_dir = Path(os.fsdecode(raw_dir)).resolve(strict=True)
            raw_format = self._run(
                [
                    "--no-replace-objects",
                    f"--git-dir={git_dir}",
                    "rev-parse",
                    "--show-object-format",
                ],
                stage="object-format",
                repository_open=True,
            ).strip()
            return git_dir, raw_format.decode("ascii")
        except SourceSnapshotError:
            raise
        except (OSError, UnicodeError, ValueError) as exc:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE
            ) from exc

    def _read_git_version(self) -> str:
        raw = self._run(["--version"], stage="git-version", repository_open=True)
        try:
            return raw.decode("ascii").strip()
        except UnicodeError as exc:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE
            ) from exc

    def _read_header(self, oid: str) -> tuple[str, int]:
        try:
            object_type = self._run_repo(
                ["cat-file", "-t", oid], stage="object-type", object_failure=True
            ).strip().decode("ascii")
            raw_size = self._run_repo(
                ["cat-file", "-s", oid], stage="object-size", object_failure=True
            ).strip()
            if not raw_size or any(byte < 48 or byte > 57 for byte in raw_size):
                raise ValueError
            return object_type, int(raw_size)
        except SourceSnapshotError:
            raise
        except (UnicodeError, ValueError) as exc:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH
            ) from exc

    def _read_verified_body(self, oid: str, object_type: str, declared_size: int) -> bytes:
        try:
            body = self._run_repo(
                ["cat-file", object_type, oid],
                stage=f"{object_type}-body",
                content_failure=True,
            )
        except SourceSnapshotError:
            raise
        verify_git_object_bytes(
            algorithm=self.algorithm,
            object_type=object_type,
            oid=oid,
            declared_size=declared_size,
            body=body,
        )
        self._state.checkpoint(f"{object_type}-verified")
        return bytes(body)

    def _run_repo(
        self,
        args: list[str],
        *,
        stage: str,
        object_failure: bool = False,
        content_failure: bool = False,
    ) -> bytes:
        return self._run(
            ["--no-replace-objects", f"--git-dir={self._git_dir}", *args],
            stage=stage,
            object_failure=object_failure,
            content_failure=content_failure,
        )

    def _run(
        self,
        args: list[str],
        *,
        stage: str,
        repository_open: bool = False,
        object_failure: bool = False,
        content_failure: bool = False,
    ) -> bytes:
        timeout = self._state.remaining_seconds(stage)
        command = [os.fspath(self._git_executable), *args]
        try:
            completed = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self._env,
                shell=False,
                timeout=timeout,
                check=False,
                creationflags=_hidden_process_flags(),
            )
        except subprocess.TimeoutExpired as exc:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED
            ) from exc
        except OSError as exc:
            code = (
                SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE
                if repository_open
                else SourceSnapshotFailureCode.INTERNAL_ACQUISITION_ERROR
            )
            raise SourceSnapshotError(code) from exc
        self._state.checkpoint(f"{stage}-complete")
        if completed.returncode != 0:
            if content_failure:
                code = SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH
            elif object_failure:
                code = SourceSnapshotFailureCode.SOURCE_OBJECT_MISSING
            elif repository_open:
                code = SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE
            else:
                code = SourceSnapshotFailureCode.INTERNAL_ACQUISITION_ERROR
            raise SourceSnapshotError(code)
        return bytes(completed.stdout)


def acquire_git_snapshot(
    *,
    repository_path: Path,
    git_executable: Path | None,
    commit_oid: str,
    analysis_root: bytes,
    budget: SnapshotAcquisitionBudget,
    clock: Callable[[], float] = time.monotonic,
    stage_hook: Callable[[str], None] | None = None,
    deadline: float | None = None,
) -> GitAcquisition:
    fixed_deadline = (
        clock() + (budget.wall_clock_ms / 1000.0)
        if deadline is None
        else deadline
    )
    state = _BudgetState(
        budget,
        clock=clock,
        stage_hook=stage_hook,
        deadline=fixed_deadline,
    )
    reader = _GitObjectReader(repository_path, git_executable, state)
    expected_length = 40 if reader.algorithm == "SHA1" else 64
    if len(commit_oid) != expected_length:
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)

    commit_body = reader.read_commit(commit_oid)
    commit_tree_oid = _parse_commit_tree_oid(
        commit_body, expected_hex_length=expected_length
    )
    root_tree_body = reader.read_tree(commit_tree_oid)
    analysis_tree_oid, analysis_tree_body, analysis_depth = _resolve_analysis_root(
        reader,
        state,
        commit_tree_oid,
        root_tree_body,
        analysis_root,
    )

    inventory: list[dict[str, object]] = []
    _walk_tree(
        reader,
        state,
        analysis_tree_body,
        prefix=analysis_root,
        depth=analysis_depth,
        inventory=inventory,
    )
    state.checkpoint("inventory-sort")
    inventory.sort(key=lambda item: bytes.fromhex(item["git_path"]["git_path_hex"]))
    state.checkpoint("inventory-complete")
    blob_bytes = {
        oid: body
        for oid, (object_type, body) in reader._terminal_cache.items()
        if object_type == "blob"
    }
    return GitAcquisition(
        algorithm=reader.algorithm,
        commit_oid=commit_oid,
        commit_tree_oid=commit_tree_oid,
        analysis_tree_oid=analysis_tree_oid,
        inventory=tuple(inventory),
        blob_bytes_by_oid=blob_bytes,
        git_executable=reader.git_executable,
        git_version=reader.git_version,
    )


def _resolve_analysis_root(
    reader: _GitObjectReader,
    state: _BudgetState,
    commit_tree_oid: str,
    commit_tree_body: bytes,
    analysis_root: bytes,
) -> tuple[str, bytes, int]:
    if not analysis_root:
        return commit_tree_oid, commit_tree_body, 0
    components = analysis_root.split(b"/")
    if len(components) > state.budget.max_tree_depth:
        raise SourceSnapshotError(SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED)
    current_oid = commit_tree_oid
    current_body = commit_tree_body
    for component in components:
        current_entries = _parse_tree(
            current_body,
            reader.oid_raw_size,
            on_entry=state.expand_tree_entry,
        )
        matches = [entry for entry in current_entries if entry.name == component]
        if len(matches) != 1 or matches[0].mode != "040000":
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.ANALYSIS_ROOT_NOT_TREE
            )
        current_oid = matches[0].oid
        try:
            current_body = reader.read_tree(current_oid)
        except SourceSnapshotError as exc:
            if exc.code == SourceSnapshotFailureCode.SOURCE_OBJECT_TYPE_MISMATCH:
                raise SourceSnapshotError(
                    SourceSnapshotFailureCode.ANALYSIS_ROOT_NOT_TREE
                ) from exc
            raise
    return current_oid, current_body, len(components)


def _walk_tree(
    reader: _GitObjectReader,
    state: _BudgetState,
    tree_body: bytes,
    *,
    prefix: bytes,
    depth: int,
    inventory: list[dict[str, object]],
) -> None:
    if depth > state.budget.max_tree_depth:
        raise SourceSnapshotError(SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED)
    entries = _parse_tree(
        tree_body,
        reader.oid_raw_size,
        on_entry=state.expand_tree_entry,
    )
    for entry in entries:
        path = entry.name if not prefix else prefix + b"/" + entry.name
        if entry.mode == "040000":
            child_body = reader.read_tree(entry.oid)
            _walk_tree(
                reader,
                state,
                child_body,
                prefix=path,
                depth=depth + 1,
                inventory=inventory,
            )
            continue
        state.add_terminal()
        oid_record = {
            "algorithm": reader.algorithm,
            "hex": entry.oid,
        }
        if entry.mode == "160000":
            inventory.append(
                {
                    "git_path": git_path_ref(path),
                    "git_mode": entry.mode,
                    "git_object": {**oid_record, "object_type": "COMMIT"},
                    "entry_kind": "GITLINK",
                }
            )
            continue
        actual_type, body = reader.read_terminal(entry.oid)
        object_type = "BLOB" if actual_type == "blob" else "OTHER"
        if entry.mode in {"100644", "100755", "120000"} and object_type != "BLOB":
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SOURCE_OBJECT_TYPE_MISMATCH
            )
        kind = {
            ("100644", "BLOB"): "REGULAR_BLOB",
            ("100755", "BLOB"): "EXECUTABLE_BLOB",
            ("120000", "BLOB"): "SYMLINK_BLOB",
        }.get((entry.mode, object_type), "OTHER_TRACKED_ENTRY")
        item: dict[str, object] = {
            "git_path": git_path_ref(path),
            "git_mode": entry.mode,
            "git_object": {**oid_record, "object_type": object_type},
            "entry_kind": kind,
        }
        if object_type == "BLOB":
            item["content"] = {
                "sha256": sha256_bytes(body),
                "size_bytes": len(body),
            }
        inventory.append(item)


def _parse_commit_tree_oid(body: bytes, *, expected_hex_length: int) -> str:
    header = body.split(b"\n\n", 1)[0]
    values = [line[5:] for line in header.split(b"\n") if line.startswith(b"tree ")]
    if len(values) != 1:
        raise SourceSnapshotError(SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH)
    value = values[0]
    if len(value) != expected_hex_length or any(
        byte not in b"0123456789abcdef" for byte in value
    ):
        raise SourceSnapshotError(SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH)
    return value.decode("ascii")


def verify_git_object_bytes(
    *,
    algorithm: str,
    object_type: str,
    oid: str,
    declared_size: int,
    body: bytes,
) -> None:
    if len(body) != declared_size:
        raise SourceSnapshotError(SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH)
    try:
        encoded_type = object_type.encode("ascii")
    except UnicodeError as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH
        ) from exc
    header = encoded_type + b" " + str(declared_size).encode("ascii") + b"\x00"
    digest_name = {"SHA1": "sha1", "SHA256": "sha256"}.get(algorithm)
    if digest_name is None:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.UNSUPPORTED_OBJECT_FORMAT
        )
    actual_oid = hashlib.new(digest_name, header + body).hexdigest()
    if actual_oid != oid:
        raise SourceSnapshotError(SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH)


def _parse_tree(
    body: bytes,
    oid_raw_size: int,
    *,
    on_entry: Callable[[], None] | None = None,
) -> tuple[_TreeEntry, ...]:
    entries: list[_TreeEntry] = []
    seen_names: set[bytes] = set()
    cursor = 0
    try:
        while cursor < len(body):
            space = body.index(b" ", cursor)
            nul = body.index(b"\x00", space + 1)
            raw_mode = body[cursor:space]
            name = body[space + 1 : nul]
            oid_start = nul + 1
            oid_end = oid_start + oid_raw_size
            if oid_end > len(body):
                raise ValueError
            if not raw_mode or any(byte < 48 or byte > 55 for byte in raw_mode):
                raise ValueError
            mode_value = int(raw_mode, 8)
            if mode_value > 0o777777:
                raise ValueError
            if not name or b"\x00" in name or b"/" in name or name in {b".", b".."}:
                raise ValueError
            if name in seen_names:
                raise ValueError
            seen_names.add(name)
            if on_entry is not None:
                on_entry()
            entries.append(
                _TreeEntry(
                    mode=f"{mode_value:06o}",
                    name=bytes(name),
                    oid=body[oid_start:oid_end].hex(),
                )
            )
            cursor = oid_end
        if cursor != len(body):
            raise ValueError
    except (ValueError, OverflowError) as exc:
        raise SourceSnapshotError(SourceSnapshotFailureCode.MALFORMED_TREE) from exc
    return tuple(entries)


def _resolve_repository_path(repository_path: Path) -> Path:
    try:
        resolved = Path(repository_path).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE
        ) from exc
    if not resolved.is_dir():
        raise SourceSnapshotError(SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE)
    return resolved


def _resolve_git_executable(
    explicit: Path | None, repository_path: Path
) -> Path:
    candidate: str | None
    if explicit is None:
        candidate = shutil.which("git")
    else:
        if not Path(explicit).is_absolute():
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
        candidate = os.fspath(explicit)
    if not candidate:
        raise SourceSnapshotError(SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE)
    try:
        resolved = Path(candidate).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE
        ) from exc
    if not resolved.is_file() or resolved.is_relative_to(repository_path):
        raise SourceSnapshotError(SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE)
    return resolved


def _controlled_git_environment() -> dict[str, str]:
    blocked = {
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_COMMON_DIR",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_NAMESPACE",
        "GIT_INDEX_FILE",
        "GIT_REPLACE_REF_BASE",
        "GIT_CEILING_DIRECTORIES",
        "GIT_DISCOVERY_ACROSS_FILESYSTEM",
    }
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in blocked and not key.startswith("GIT_CONFIG_")
    }
    env.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
        }
    )
    return env


def _hidden_process_flags() -> int:
    if os.name != "nt":
        return 0
    return int(getattr(subprocess, "CREATE_NO_WINDOW", 0))
