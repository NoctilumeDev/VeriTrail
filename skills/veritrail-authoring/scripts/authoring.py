from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


PROTOCOL_VERSION = "0.1"
SUPPORTED_STARTER_VERSIONS = frozenset({"0.1.0.dev0"})
ALLOWED_STARTER_COMMANDS = frozenset({"doctor", "init", "validate", "review"})
MAX_INTAKE_BYTES = 256 * 1024
MAX_SCAN_ENTRIES = 2048
MAX_SCAN_DEPTH = 4
MAX_PUBLIC_FILES = 128
TRANSIENT_PREFIX = ".veritrail-authoring-"
TRANSIENT_SUFFIX = ".answers.json"
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)

INTAKE_FIELDS = frozenset({"schema_version", "repository_root", "topology", "answers"})
TOPOLOGY_FIELDS = frozenset(
    {
        "managed_nodes",
        "uses_shell",
        "uses_container_or_vm",
        "uses_remote_dependency",
        "requires_secret",
        "loopback_only",
    }
)
REQUIRED_POINTERS = (
    "/schema_version",
    "/repository_root",
    "/topology/managed_nodes",
    "/topology/uses_shell",
    "/topology/uses_container_or_vm",
    "/topology/uses_remote_dependency",
    "/topology/requires_secret",
    "/topology/loopback_only",
    "/answers/schema_version",
    "/answers/preset",
    "/answers/workspace_id",
    "/answers/question",
    "/answers/subject/root",
    "/answers/subject/id",
    "/answers/subject/version",
    "/answers/subject/source_ref",
    "/answers/subject/working_directory",
    "/answers/subject/watch_roots",
    "/answers/application/executable",
    "/answers/application/arguments",
    "/answers/application/port",
    "/answers/application/health_path",
    "/answers/application/expected_status",
    "/answers/browser/start_url",
    "/answers/browser/allowed_origin",
    "/answers/browser/headless",
    "/answers/browser/timeout_ms",
    "/answers/browser/viewports",
    "/answers/browser/steps",
    "/answers/browser/screenshot_safety",
    "/answers/budgets/max_artifact_bytes",
    "/answers/budgets/max_watch_files",
    "/answers/budgets/max_watch_total_bytes",
    "/answers/budgets/lifecycle_timeout_ms",
    "/answers/budgets/max_stdout_bytes",
    "/answers/budgets/max_stderr_bytes",
    "/answers/budgets/max_processes",
    "/answers/budgets/application_memory_mb",
    "/answers/budgets/browser_memory_mb",
    "/answers/timeouts/readiness_attempt_ms",
    "/answers/timeouts/readiness_total_ms",
    "/answers/timeouts/readiness_interval_ms",
    "/answers/timeouts/shutdown_process_ms",
    "/answers/timeouts/shutdown_port_ms",
    "/answers/timeouts/shutdown_reader_ms",
    "/answers/random_seed",
)

SECRET_KEY = re.compile(
    r"(?i)(?:^|[-_])(password|passwd|token|secret|api[-_]?key|authorization|cookie|credential|private[-_]?key)(?:$|[-_])"
)
SECRET_KEY_COMPACT = re.compile(
    r"(?i)(?:password|passwd|token|secret|apikey|authorization|cookie|credential|privatekey)"
)
SECRET_VALUE = re.compile(
    r"(?i)(?:Bearer\s+[A-Za-z0-9._~+/=-]+|github_pat_[A-Za-z0-9_]{20,}|gh[opsu]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
SECRET_FILE = re.compile(
    r"(?i)^(?:\.env(?:\..*)?|\.git-credentials|cookies?(?:\.sqlite)?|login data|web data|.*\.(?:pem|key|pfx|p12))$"
)
PUBLIC_FILE = re.compile(
    r"(?i)^(?:readme(?:\..+)?|pyproject\.toml|package\.json|package-lock\.json|pnpm-lock\.yaml|yarn\.lock|requirements(?:-[a-z0-9_.-]+)?\.txt|poetry\.lock|pdm\.lock|uv\.lock|cargo\.toml|cargo\.lock|go\.mod|go\.sum|pom\.xml|build\.gradle(?:\.kts)?|gradle\.properties|.*\.(?:sln|csproj|fsproj|vbproj))$"
)
UNSUPPORTED_MARKER = re.compile(
    r"(?i)^(?:docker-compose(?:\..+)?\.ya?ml|compose(?:\..+)?\.ya?ml|dockerfile(?:\..+)?|devcontainer\.json)$"
)
SKIP_DIRECTORIES = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".veritrail",
        "__pycache__",
        "artifacts",
        "build",
        "dist",
        "node_modules",
        "target",
        "vendor",
        ".venv",
        "venv",
        "user data",
        "profiles",
    }
)

NOT_PROVEN = (
    "the application has not been started by this Skill",
    "no ProjectProfile or ExperimentPlan has been sealed",
    "no Preview digest has been approved",
    "no browser evidence, Bundle, ExecutionStatus, or Verdict exists",
)
BOUNDARY = {
    "authoring_role": "AUTHORING_ASSISTANT",
    "seal_state": "NOT_SEALED",
    "execution_state": "NOT_RUN",
    "verdict_state": "NO_VERDICT",
}


class AuthoringFailure(Exception):
    def __init__(self, state: str, code: str, messages: Iterable[str]) -> None:
        self.state = state
        self.code = code
        self.messages = tuple(messages)
        super().__init__("; ".join(self.messages))


class _JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        del message
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "COMMAND_LINE_INVALID",
            ("command line arguments are invalid",),
        )


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(_canonical_bytes(value))


def _metadata_is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def _is_reparse(path: Path) -> bool:
    metadata = os.lstat(path)
    return stat.S_ISLNK(metadata.st_mode) or _metadata_is_reparse(metadata)


def _ordinary_directory(raw: Any) -> Path:
    if not isinstance(raw, str) or not raw or not Path(raw).is_absolute():
        raise AuthoringFailure(
            "NO_MATCHING_PRESET",
            "REPOSITORY_UNAVAILABLE",
            ("repository root must be an explicit absolute path",),
        )
    path = Path(raw)
    try:
        if not path.exists() or not path.is_dir() or _is_reparse(path):
            raise OSError("unsafe directory")
        return path.resolve(strict=True)
    except OSError as exc:
        raise AuthoringFailure(
            "NO_MATCHING_PRESET",
            "REPOSITORY_UNAVAILABLE",
            ("repository root must be an existing ordinary directory",),
        ) from exc


def _ordinary_intake(path: Path) -> bytes:
    if not path.is_absolute() or path.suffix.casefold() != ".json" or SECRET_FILE.fullmatch(path.name):
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "INTAKE_UNAVAILABLE",
            ("intake must be an explicit ordinary JSON file",),
        )
    identity = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_nlink")
    try:
        before = os.lstat(path)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or _metadata_is_reparse(before)
            or before.st_size > MAX_INTAKE_BYTES
        ):
            raise OSError("unsafe intake")
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            data = handle.read(MAX_INTAKE_BYTES + 1)
        after = os.lstat(path)
        if (
            _metadata_is_reparse(opened)
            or _metadata_is_reparse(after)
            or not stat.S_ISREG(opened.st_mode)
            or not stat.S_ISREG(after.st_mode)
            or opened.st_nlink != 1
            or after.st_nlink != 1
            or opened.st_size > MAX_INTAKE_BYTES
            or len(data) > MAX_INTAKE_BYTES
            or any(getattr(before, field) != getattr(opened, field) for field in identity)
            or any(getattr(opened, field) != getattr(after, field) for field in identity)
            or len(data) != opened.st_size
        ):
            raise OSError("intake changed")
        return data
    except OSError as exc:
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "INTAKE_UNAVAILABLE",
            ("intake could not be read as one bounded ordinary file",),
        ) from exc


def _load_json_bytes(data: bytes) -> dict[str, Any]:
    if len(data) > MAX_INTAKE_BYTES:
        raise AuthoringFailure(
            "NEEDS_USER_INPUT", "INTAKE_TOO_LARGE", ("intake exceeds 256 KiB",)
        )
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuthoringFailure(
            "NEEDS_USER_INPUT", "INTAKE_INVALID", ("intake must be one UTF-8 JSON object",)
        ) from exc
    if not isinstance(value, dict):
        raise AuthoringFailure(
            "NEEDS_USER_INPUT", "INTAKE_INVALID", ("intake must be one JSON object",)
        )
    return value


def _load_intake(args: argparse.Namespace) -> dict[str, Any]:
    if args.stdin:
        return _load_json_bytes(sys.stdin.buffer.read(MAX_INTAKE_BYTES + 1))
    return _load_json_bytes(_ordinary_intake(args.intake))


def _has_pointer(value: dict[str, Any], pointer: str) -> bool:
    current: Any = value
    for segment in pointer.lstrip("/").split("/"):
        if not isinstance(current, dict) or segment not in current or current[segment] is None:
            return False
        current = current[segment]
    return True


def _contains_secret(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            if key_text == "requires_secret" and isinstance(item, bool):
                continue
            if (
                SECRET_KEY.search(key_text) is not None
                or SECRET_KEY_COMPACT.search(re.sub(r"[^A-Za-z0-9]", "", key_text))
                is not None
                or _contains_secret(item)
            ):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_secret(item) for item in value)
    return isinstance(value, str) and SECRET_VALUE.search(value) is not None


def _safe_scan(root: Path) -> dict[str, Any]:
    public_files: list[str] = []
    unsupported_markers: list[str] = []
    secret_entries_ignored = 0
    reparse_entries_ignored = 0
    entries_examined = 0
    truncated = False
    stack: list[tuple[Path, int]] = [(root, 0)]

    while stack and entries_examined < MAX_SCAN_ENTRIES:
        directory, depth = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name.casefold())
        except OSError:
            continue
        for entry in entries:
            if entries_examined >= MAX_SCAN_ENTRIES:
                truncated = True
                break
            entries_examined += 1
            name = entry.name
            relative = Path(entry.path).relative_to(root).as_posix()
            if SECRET_FILE.fullmatch(name):
                secret_entries_ignored += 1
                continue
            try:
                entry_path = Path(entry.path)
                if entry.is_symlink() or _is_reparse(entry_path):
                    reparse_entries_ignored += 1
                    continue
                if entry.is_dir(follow_symlinks=False):
                    folded = name.casefold()
                    if (
                        depth < MAX_SCAN_DEPTH
                        and folded not in SKIP_DIRECTORIES
                        and (not name.startswith(".") or name == ".github")
                    ):
                        stack.append((entry_path, depth + 1))
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
            except OSError:
                continue
            if PUBLIC_FILE.fullmatch(name) or UNSUPPORTED_MARKER.fullmatch(name):
                if len(public_files) < MAX_PUBLIC_FILES:
                    public_files.append(relative)
            if UNSUPPORTED_MARKER.fullmatch(name) and len(unsupported_markers) < MAX_PUBLIC_FILES:
                unsupported_markers.append(relative)

    return {
        "entries_examined": entries_examined,
        "public_files": sorted(set(public_files), key=str.casefold),
        "secret_entries_ignored": secret_entries_ignored,
        "reparse_entries_ignored": reparse_entries_ignored,
        "scan_truncated": truncated,
        "unsupported_markers_requiring_confirmation": sorted(
            set(unsupported_markers), key=str.casefold
        ),
    }


def inspect_repository(root_raw: str) -> dict[str, Any]:
    root = _ordinary_directory(root_raw)
    scan = _safe_scan(root)
    return {
        "schema_version": PROTOCOL_VERSION,
        "operation": "inspect",
        "state": "NEEDS_USER_INPUT",
        "preset_candidate": "single-webapp",
        "repository": {"root": str(root), **scan},
        "provenance": {
            "OBSERVED": [
                "repository root is an ordinary directory",
                "only bounded public filenames and filesystem metadata were inspected",
            ],
            "USER_SUPPLIED": ["repository_root"],
            "INFERRED": ["single-webapp remains only a candidate until topology is confirmed"],
            "NOT_PROVEN": list(NOT_PROVEN),
        },
        "questions": [
            "Confirm exactly one Starter-managed application node.",
            "Confirm no shell, container/VM, remote dependency, or secret is required.",
            "Confirm the trusted executable, structured arguments, fixed loopback port, and health path.",
            "Confirm every browser check, budget, timeout, and screenshot safety choice.",
        ],
        "boundary": BOUNDARY,
    }


def _starter_contract() -> tuple[str, Any, type[Exception]]:
    try:
        from veritrail_starter import __version__ as starter_version
        from veritrail_starter.contract import normalize_answers
        from veritrail_starter.errors import StarterError
    except ImportError as exc:
        raise AuthoringFailure(
            "STARTER_VERSION_UNSUPPORTED",
            "STARTER_NOT_AVAILABLE",
            ("VeriTrail Starter 0.1 is not importable",),
        ) from exc
    if starter_version not in SUPPORTED_STARTER_VERSIONS:
        raise AuthoringFailure(
            "STARTER_VERSION_UNSUPPORTED",
            "STARTER_VERSION_UNSUPPORTED",
            ("the installed Starter version is outside the frozen Skill 0.1 range",),
        )
    return starter_version, normalize_answers, StarterError


def _validate_intake(document: dict[str, Any]) -> dict[str, Any]:
    unknown = sorted(set(document) - INTAKE_FIELDS)
    if unknown:
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "INTAKE_INVALID",
            ("intake has unsupported top-level fields",),
        )
    if _contains_secret(document):
        return {
            "schema_version": PROTOCOL_VERSION,
            "operation": "candidate",
            "state": "NO_MATCHING_PRESET",
            "preset_candidate": None,
            "reasons": [{"code": "SECRET_REQUIRED_OR_PRESENT"}],
            "boundary": BOUNDARY,
        }
    missing = [pointer for pointer in REQUIRED_POINTERS if not _has_pointer(document, pointer)]
    if missing:
        return {
            "schema_version": PROTOCOL_VERSION,
            "operation": "candidate",
            "state": "NEEDS_USER_INPUT",
            "preset_candidate": "single-webapp",
            "missing_fields": missing,
            "boundary": BOUNDARY,
        }
    if document.get("schema_version") != PROTOCOL_VERSION:
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "INTAKE_VERSION_UNSUPPORTED",
            ("intake schema_version must be 0.1",),
        )
    topology = document.get("topology")
    if not isinstance(topology, dict) or set(topology) != TOPOLOGY_FIELDS:
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "TOPOLOGY_CONFIRMATION_INVALID",
            ("topology confirmation must contain exactly the frozen fields",),
        )
    if not isinstance(topology["managed_nodes"], int) or isinstance(
        topology["managed_nodes"], bool
    ):
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "TOPOLOGY_CONFIRMATION_INVALID",
            ("managed_nodes must be an explicit integer",),
        )
    boolean_fields = TOPOLOGY_FIELDS - {"managed_nodes"}
    if any(not isinstance(topology[field], bool) for field in boolean_fields):
        raise AuthoringFailure(
            "NEEDS_USER_INPUT",
            "TOPOLOGY_CONFIRMATION_INVALID",
            ("all topology flags must be explicit booleans",),
        )
    unsupported: list[dict[str, str]] = []
    if topology["managed_nodes"] != 1:
        unsupported.append({"code": "MULTI_NODE_TOPOLOGY"})
    if topology["uses_shell"]:
        unsupported.append({"code": "SHELL_REQUIRED"})
    if topology["uses_container_or_vm"]:
        unsupported.append({"code": "CONTAINER_OR_VM_REQUIRED"})
    if topology["uses_remote_dependency"]:
        unsupported.append({"code": "REMOTE_DEPENDENCY_REQUIRED"})
    if topology["requires_secret"]:
        unsupported.append({"code": "SECRET_REQUIRED"})
    if not topology["loopback_only"]:
        unsupported.append({"code": "NON_LOOPBACK_REQUIRED"})
    if unsupported:
        return {
            "schema_version": PROTOCOL_VERSION,
            "operation": "candidate",
            "state": "NO_MATCHING_PRESET",
            "preset_candidate": None,
            "reasons": unsupported,
            "boundary": BOUNDARY,
        }

    root = _ordinary_directory(document["repository_root"])
    answers = document.get("answers")
    if not isinstance(answers, dict):
        raise AuthoringFailure(
            "NEEDS_USER_INPUT", "ANSWERS_INVALID", ("answers must be one JSON object",)
        )
    answer_root = answers.get("subject", {}).get("root") if isinstance(answers.get("subject"), dict) else None
    try:
        normalized_answer_root = os.path.normcase(str(_ordinary_directory(answer_root)))
        normalized_repository_root = os.path.normcase(str(root))
        if normalized_answer_root != normalized_repository_root:
            raise AuthoringFailure(
                "STARTER_VALIDATION_FAILED",
                "INVALID_INPUT",
                ("answers.subject.root must equal repository_root",),
            )
    except AuthoringFailure as exc:
        if exc.code == "REPOSITORY_UNAVAILABLE":
            raise AuthoringFailure(
                "STARTER_VALIDATION_FAILED",
                "INVALID_INPUT",
                ("answers.subject.root must equal repository_root",),
            ) from exc
        raise

    starter_version, normalize_answers, StarterError = _starter_contract()
    try:
        normalized = normalize_answers(copy.deepcopy(answers))
    except StarterError as exc:
        return {
            "schema_version": PROTOCOL_VERSION,
            "operation": "candidate",
            "state": "STARTER_VALIDATION_FAILED",
            "preset_candidate": "single-webapp",
            "starter_error": {"code": exc.code, "messages": list(exc.messages)},
            "boundary": BOUNDARY,
        }
    scan = _safe_scan(root)
    return {
        "schema_version": PROTOCOL_VERSION,
        "operation": "candidate",
        "state": "CANDIDATE_READY",
        "preset_candidate": "single-webapp",
        "starter_version": starter_version,
        "answers_sha256": hashlib.sha256(_canonical_bytes(normalized)).hexdigest(),
        "answers": normalized,
        "provenance": {
            "OBSERVED": {
                "public_files": scan["public_files"],
                "secret_entries_ignored": scan["secret_entries_ignored"],
                "reparse_entries_ignored": scan["reparse_entries_ignored"],
            },
            "USER_SUPPLIED": ["topology confirmations", "all Answers 0.1 fields"],
            "INFERRED": ["single-webapp preset candidate"],
            "NOT_PROVEN": list(NOT_PROVEN),
        },
        "boundary": BOUNDARY,
    }


def candidate(document: dict[str, Any]) -> dict[str, Any]:
    return _validate_intake(document)


def _invoke_starter(command: str, arguments: list[str]) -> dict[str, Any]:
    if command not in ALLOWED_STARTER_COMMANDS:
        raise AuthoringFailure(
            "STARTER_VERSION_UNSUPPORTED",
            "STARTER_COMMAND_FORBIDDEN",
            ("the requested Starter command is outside the Skill allowlist",),
        )
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "veritrail_starter.cli", command, *arguments],
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AuthoringFailure(
            "STARTER_VALIDATION_FAILED",
            "STARTER_INVOCATION_FAILED",
            ("Starter did not return one bounded result",),
        ) from exc
    try:
        lines = completed.stdout.decode("utf-8").splitlines()
        if len(lines) != 1:
            raise ValueError("unexpected stdout")
        result = json.loads(lines[0])
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise AuthoringFailure(
            "STARTER_VERSION_UNSUPPORTED",
            "STARTER_PROTOCOL_UNSUPPORTED",
            ("Starter did not return the frozen single-JSON protocol",),
        ) from exc
    if (
        not isinstance(result, dict)
        or result.get("schema_version") != PROTOCOL_VERSION
        or result.get("command") != command
        or result.get("outcome") not in {"OK", "ERROR"}
    ):
        raise AuthoringFailure(
            "STARTER_VERSION_UNSUPPORTED",
            "STARTER_PROTOCOL_UNSUPPORTED",
            ("Starter returned an unknown protocol shape",),
        )
    return result


def _failure_from_starter(operation: str, result: dict[str, Any]) -> dict[str, Any]:
    error = result.get("error") if isinstance(result.get("error"), dict) else {}
    code = error.get("code", "UNKNOWN_STARTER_ERROR")
    messages = error.get("messages", [])
    if code == "CORE_INCOMPATIBLE":
        state = "STARTER_VERSION_UNSUPPORTED"
    elif code in {"NEEDS_INPUT", "ENVIRONMENT_NOT_READY"}:
        state = "NEEDS_USER_INPUT"
    else:
        state = "STARTER_VALIDATION_FAILED"
    return {
        "schema_version": PROTOCOL_VERSION,
        "operation": operation,
        "state": state,
        "starter_error": {"code": code, "messages": messages},
        "boundary": BOUNDARY,
    }


def _transient_answers(root: Path, answers: dict[str, Any]) -> Path:
    descriptor, raw_path = tempfile.mkstemp(
        prefix=TRANSIENT_PREFIX, suffix=TRANSIENT_SUFFIX, dir=root
    )
    path = Path(raw_path)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(_canonical_bytes(answers))
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
        raise
    return path


def _remove_transient(path: Path, root: Path) -> None:
    try:
        metadata = os.lstat(path)
        if (
            path.parent.resolve(strict=True) == root
            and path.name.startswith(TRANSIENT_PREFIX)
            and path.name.endswith(TRANSIENT_SUFFIX)
            and stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not _is_reparse(path)
        ):
            path.unlink()
    except OSError:
        return


def create_draft(document: dict[str, Any]) -> dict[str, Any]:
    prepared = candidate(document)
    if prepared["state"] != "CANDIDATE_READY":
        return {**prepared, "operation": "draft"}
    root = _ordinary_directory(document["repository_root"])
    transient = _transient_answers(root, prepared["answers"])
    try:
        doctor = _invoke_starter("doctor", ["--answers", str(transient)])
        if doctor["outcome"] == "ERROR":
            return _failure_from_starter("draft", doctor)
        if doctor.get("status") != "READY":
            state = "NO_MATCHING_PRESET" if doctor.get("status") == "UNSUPPORTED" else "NEEDS_USER_INPUT"
            return {
                "schema_version": PROTOCOL_VERSION,
                "operation": "draft",
                "state": state,
                "doctor": doctor,
                "boundary": BOUNDARY,
            }
        initialized = _invoke_starter(
            "init", ["--preset", "single-webapp", "--answers", str(transient)]
        )
        if initialized["outcome"] == "ERROR":
            return _failure_from_starter("draft", initialized)
        workspace = root / ".veritrail"
        validated = _invoke_starter("validate", ["--workspace", str(workspace)])
        if validated["outcome"] == "ERROR":
            return _failure_from_starter("draft", validated)
        reviewed = _invoke_starter("review", ["--workspace", str(workspace)])
        if reviewed["outcome"] == "ERROR":
            return _failure_from_starter("draft", reviewed)
        return {
            "schema_version": PROTOCOL_VERSION,
            "operation": "draft",
            "state": "DRAFT_READY_FOR_HUMAN_REVIEW",
            "workspace": ".veritrail",
            "review_file": ".veritrail/REVIEW.md",
            "starter": {
                "doctor": doctor,
                "init": initialized,
                "validate": validated,
                "review": reviewed,
            },
            "provenance": prepared["provenance"],
            "boundary": BOUNDARY,
        }
    finally:
        _remove_transient(transient, root)


def review_draft(workspace: Path) -> dict[str, Any]:
    _starter_contract()
    validated = _invoke_starter("validate", ["--workspace", str(workspace)])
    if validated["outcome"] == "ERROR":
        return _failure_from_starter("review-draft", validated)
    reviewed = _invoke_starter("review", ["--workspace", str(workspace)])
    if reviewed["outcome"] == "ERROR":
        return _failure_from_starter("review-draft", reviewed)
    return {
        "schema_version": PROTOCOL_VERSION,
        "operation": "review-draft",
        "state": "DRAFT_READY_FOR_HUMAN_REVIEW",
        "workspace": str(workspace),
        "starter": {"validate": validated, "review": reviewed},
        "boundary": BOUNDARY,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = _JsonArgumentParser(
        prog="veritrail-authoring",
        description="Prepare a fail-closed VeriTrail Starter DRAFT candidate.",
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)
    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--repository", required=True)
    for name in ("candidate", "draft"):
        command = subparsers.add_parser(name)
        source = command.add_mutually_exclusive_group(required=True)
        source.add_argument("--intake", type=Path)
        source.add_argument("--stdin", action="store_true")
    review_parser = subparsers.add_parser("review-draft")
    review_parser.add_argument("--workspace", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    argument_list = list(sys.argv[1:] if argv is None else argv)
    operation = next(
        (
            item
            for item in argument_list
            if item in {"inspect", "candidate", "draft", "review-draft"}
        ),
        "authoring",
    )
    try:
        args = build_parser().parse_args(argument_list)
        operation = args.operation
        if operation == "inspect":
            result = inspect_repository(args.repository)
        elif operation == "candidate":
            result = candidate(_load_intake(args))
        elif operation == "draft":
            result = create_draft(_load_intake(args))
        else:
            result = review_draft(args.workspace)
        _emit(result)
        return 0
    except AuthoringFailure as exc:
        _emit(
            {
                "schema_version": PROTOCOL_VERSION,
                "operation": operation,
                "state": exc.state,
                "error": {"code": exc.code, "messages": list(exc.messages)},
                "boundary": BOUNDARY,
            }
        )
        return 2
    except Exception:
        _emit(
            {
                "schema_version": PROTOCOL_VERSION,
                "operation": operation,
                "state": "STARTER_VALIDATION_FAILED",
                "error": {
                    "code": "AUTHORING_INTERNAL_ERROR",
                    "messages": ["operation failed closed without changing authority"],
                },
                "boundary": BOUNDARY,
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
