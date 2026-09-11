from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, fields, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping

from veritrail_review.canonical import (
    bounded_canonical_json_bytes,
    bounded_semantic_digest,
    semantic_digest,
)
from veritrail_review.errors import SourceSnapshotError, SourceSnapshotFailureCode


SCHEMA_VERSION = "0.1"
CANONICALIZATION_PROFILE = "veritrail-json-c14n/1"
ACQUISITION_PROFILE_ID = "snapshot-acquisition/windows-reference/0.1"

_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")
_MODE_RE = re.compile(r"^[0-7]{6}$")
_HEX_BYTES_RE = re.compile(r"^(?:[0-9a-f]{2})+$")

_TOP_LEVEL_KEYS = frozenset(
    {
        "artifact_kind",
        "schema_version",
        "canonicalization_profile",
        "repository_id",
        "source_coordinate",
        "inventory",
        "inventory_digest",
        "source_coordinate_digest",
        "source_content_digest",
        "source_snapshot_digest",
    }
)
_COORDINATE_KEYS = frozenset(
    {"commit_oid", "commit_tree_oid", "analysis_tree_oid", "analysis_root"}
)
_INVENTORY_KEYS = frozenset(
    {"git_path", "git_mode", "git_object", "entry_kind", "content"}
)
_GIT_OBJECT_KEYS = frozenset({"algorithm", "hex", "object_type"})
_CONTENT_KEYS = frozenset({"sha256", "size_bytes"})


@dataclass(frozen=True)
class SnapshotAcquisitionBudget:
    profile_id: str = ACQUISITION_PROFILE_ID
    wall_clock_ms: int = 30_000
    max_commit_bytes: int = 8_388_608
    max_tree_depth: int = 128
    max_unique_tree_objects: int = 8_192
    max_expanded_tree_entries: int = 65_536
    max_single_tree_bytes: int = 8_388_608
    max_total_unique_tree_bytes: int = 67_108_864
    max_terminal_inventory_entries: int = 32_768
    max_single_blob_bytes: int = 16_777_216
    max_total_unique_blob_bytes: int = 268_435_456
    max_canonical_artifact_bytes: int = 67_108_864


DEFAULT_ACQUISITION_BUDGET = SnapshotAcquisitionBudget()


def tightened_budget_for_testing(**overrides: int) -> SnapshotAcquisitionBudget:
    """Return a test budget that can only tighten the frozen public profile."""

    valid_names = {item.name for item in fields(SnapshotAcquisitionBudget)} - {"profile_id"}
    if set(overrides) - valid_names:
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    for name, value in overrides.items():
        if type(value) is not int or value < 0:
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
        if value > getattr(DEFAULT_ACQUISITION_BUDGET, name):
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    return replace(DEFAULT_ACQUISITION_BUDGET, **overrides)


@dataclass(frozen=True)
class SourceSnapshotSpec:
    repository_id: str
    commit_oid: str
    analysis_root: Mapping[str, str]

    def __post_init__(self) -> None:
        try:
            owned_root = MappingProxyType(dict(self.analysis_root))
        except (TypeError, ValueError) as exc:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.INVALID_REQUEST
            ) from exc
        object.__setattr__(self, "analysis_root", owned_root)


@dataclass(frozen=True)
class SourceSnapshotRequest:
    spec: SourceSnapshotSpec
    repository_path: Path
    output_directory: Path

    def __post_init__(self) -> None:
        try:
            repository_path = Path(self.repository_path)
            output_directory = Path(self.output_directory)
        except TypeError as exc:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.INVALID_REQUEST
            ) from exc
        object.__setattr__(self, "repository_path", repository_path)
        object.__setattr__(self, "output_directory", output_directory)


@dataclass(frozen=True)
class SourceSnapshotRuntime:
    """Trusted operational configuration; never part of Snapshot identity."""

    git_executable: Path | None = None

    def __post_init__(self) -> None:
        if self.git_executable is not None:
            try:
                executable = Path(self.git_executable)
            except TypeError as exc:
                raise SourceSnapshotError(
                    SourceSnapshotFailureCode.INVALID_REQUEST
                ) from exc
            object.__setattr__(self, "git_executable", executable)


@dataclass(frozen=True)
class OwnedSourceSnapshot:
    """Owned canonical bytes plus immutable blob bytes for a later local consumer."""

    canonical_bytes: bytes
    blob_bytes_by_oid: Mapping[str, bytes]
    _source_snapshot_digest: str

    @classmethod
    def create(
        cls,
        document: Mapping[str, Any],
        canonical_bytes: bytes,
        blob_bytes_by_oid: Mapping[str, bytes],
    ) -> "OwnedSourceSnapshot":
        owned_blobs = {key: bytes(value) for key, value in blob_bytes_by_oid.items()}
        return cls(
            bytes(canonical_bytes),
            MappingProxyType(owned_blobs),
            str(document["source_snapshot_digest"]),
        )

    def document_copy(self) -> dict[str, Any]:
        value = json.loads(self.canonical_bytes)
        if not isinstance(value, dict):
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT
            )
        return value

    @property
    def source_snapshot_digest(self) -> str:
        return self._source_snapshot_digest


def validate_source_snapshot_spec(spec: SourceSnapshotSpec) -> tuple[str, bytes]:
    if not _is_unicode_scalar_text(spec.repository_id) or not spec.repository_id:
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    commit_oid = spec.commit_oid
    if not (_SHA1_RE.fullmatch(commit_oid) or _SHA256_RE.fullmatch(commit_oid)):
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    root_bytes = decode_git_path_ref(spec.analysis_root, allow_repository_root=True)
    return ("SHA1" if len(commit_oid) == 40 else "SHA256", root_bytes)


def decode_git_path_ref(value: Mapping[str, Any], *, allow_repository_root: bool) -> bytes:
    if not isinstance(value, Mapping):
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    kind = value.get("path_kind")
    if kind == "REPOSITORY_ROOT" and allow_repository_root:
        if set(value) != {"path_kind"}:
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
        return b""
    if kind != "GIT_PATH" or set(value) != {"path_kind", "git_path_hex"}:
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    encoded = value.get("git_path_hex")
    if not isinstance(encoded, str) or _HEX_BYTES_RE.fullmatch(encoded) is None:
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    raw = bytes.fromhex(encoded)
    _validate_raw_git_path(raw)
    return raw


def git_path_ref(raw: bytes, *, allow_repository_root: bool = False) -> dict[str, str]:
    if not raw and allow_repository_root:
        return {"path_kind": "REPOSITORY_ROOT"}
    _validate_raw_git_path(raw)
    return {"path_kind": "GIT_PATH", "git_path_hex": raw.hex()}


def git_oid(algorithm: str, oid_hex: str) -> dict[str, str]:
    _validate_oid(algorithm, oid_hex)
    return {"algorithm": algorithm, "hex": oid_hex}


def build_source_snapshot_document(
    *,
    repository_id: str,
    commit_oid: Mapping[str, str],
    commit_tree_oid: Mapping[str, str],
    analysis_tree_oid: Mapping[str, str],
    analysis_root: Mapping[str, str],
    inventory: list[dict[str, Any]],
    max_canonical_bytes: int | None = None,
    deadline_check: Callable[[], None] | None = None,
) -> dict[str, Any]:
    coordinate = {
        "commit_oid": copy.deepcopy(dict(commit_oid)),
        "commit_tree_oid": copy.deepcopy(dict(commit_tree_oid)),
        "analysis_tree_oid": copy.deepcopy(dict(analysis_tree_oid)),
        "analysis_root": copy.deepcopy(dict(analysis_root)),
    }
    owned_inventory = copy.deepcopy(inventory)
    digest = _digest_function(max_canonical_bytes, deadline_check)
    inventory_digest = digest(
        "veritrail.review.source-inventory/0.1", owned_inventory
    )
    coordinate_digest = digest(
        "veritrail.review.source-coordinate/0.1",
        {"repository_id": repository_id, **coordinate},
    )
    content_digest = digest(
        "veritrail.review.source-content/0.1",
        {
            "analysis_tree_oid": coordinate["analysis_tree_oid"],
            "analysis_root": coordinate["analysis_root"],
            "inventory_digest": inventory_digest,
        },
    )
    snapshot_digest = digest(
        "veritrail.review.source-snapshot/0.1",
        {
            "source_coordinate_digest": coordinate_digest,
            "source_content_digest": content_digest,
        },
    )
    return {
        "artifact_kind": "SOURCE_SNAPSHOT",
        "schema_version": SCHEMA_VERSION,
        "canonicalization_profile": CANONICALIZATION_PROFILE,
        "repository_id": repository_id,
        "source_coordinate": coordinate,
        "inventory": owned_inventory,
        "inventory_digest": inventory_digest,
        "source_coordinate_digest": coordinate_digest,
        "source_content_digest": content_digest,
        "source_snapshot_digest": snapshot_digest,
    }


def validate_source_snapshot_document(
    document: Mapping[str, Any],
    *,
    expected_bytes: bytes | None = None,
    max_canonical_bytes: int = DEFAULT_ACQUISITION_BUDGET.max_canonical_artifact_bytes,
    deadline_check: Callable[[], None] | None = None,
) -> bytes:
    try:
        _validate_document_shape(document)
        if deadline_check is not None:
            deadline_check()
        inventory = document["inventory"]
        raw_paths: list[bytes] = []
        algorithm = document["source_coordinate"]["commit_oid"]["algorithm"]
        for entry in inventory:
            raw_paths.append(_validate_inventory_entry(entry, algorithm))
        if raw_paths != sorted(raw_paths) or len(raw_paths) != len(set(raw_paths)):
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
        coordinate = document["source_coordinate"]
        for name in ("commit_oid", "commit_tree_oid", "analysis_tree_oid"):
            _validate_oid_object(coordinate[name], expected_algorithm=algorithm)
        try:
            decode_git_path_ref(coordinate["analysis_root"], allow_repository_root=True)
        except SourceSnapshotError as exc:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT
            ) from exc
        expected = build_source_snapshot_document(
            repository_id=document["repository_id"],
            commit_oid=coordinate["commit_oid"],
            commit_tree_oid=coordinate["commit_tree_oid"],
            analysis_tree_oid=coordinate["analysis_tree_oid"],
            analysis_root=coordinate["analysis_root"],
            inventory=list(inventory),
            max_canonical_bytes=max_canonical_bytes,
            deadline_check=deadline_check,
        )
        if dict(document) != expected:
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
        if deadline_check is not None:
            deadline_check()
        if max_canonical_bytes == 0:
            raise SourceSnapshotError(SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED)
        canonical = bounded_canonical_json_bytes(
            document,
            max_bytes=max_canonical_bytes - 1,
            deadline_check=deadline_check,
        ) + b"\n"
        if expected_bytes is not None and canonical != expected_bytes:
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
        if (
            bounded_canonical_json_bytes(
                copy.deepcopy(dict(document)),
                max_bytes=max_canonical_bytes - 1,
                deadline_check=deadline_check,
            )
            + b"\n"
            != canonical
        ):
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
        if deadline_check is not None:
            deadline_check()
        return canonical
    except SourceSnapshotError:
        raise
    except (KeyError, TypeError, ValueError, UnicodeError) as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT
        ) from exc


def _digest_function(
    max_canonical_bytes: int | None,
    deadline_check: Callable[[], None] | None,
) -> Callable[[str, Any], str]:
    if max_canonical_bytes is None:
        return semantic_digest

    def digest(domain: str, payload: Any) -> str:
        return bounded_semantic_digest(
            domain,
            payload,
            max_bytes=max_canonical_bytes,
            deadline_check=deadline_check,
        )

    return digest


def _validate_document_shape(document: Mapping[str, Any]) -> None:
    if not isinstance(document, Mapping) or set(document) != _TOP_LEVEL_KEYS:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if document["artifact_kind"] != "SOURCE_SNAPSHOT":
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if document["schema_version"] != SCHEMA_VERSION:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if document["canonicalization_profile"] != CANONICALIZATION_PROFILE:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if not _is_unicode_scalar_text(document["repository_id"]) or not document["repository_id"]:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    coordinate = document["source_coordinate"]
    if not isinstance(coordinate, Mapping) or set(coordinate) != _COORDINATE_KEYS:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if not isinstance(document["inventory"], list):
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    for name in (
        "inventory_digest",
        "source_coordinate_digest",
        "source_content_digest",
        "source_snapshot_digest",
    ):
        if not isinstance(document[name], str) or _SHA256_HEX_RE.fullmatch(document[name]) is None:
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)


def _validate_inventory_entry(entry: Mapping[str, Any], algorithm: str) -> bytes:
    if not isinstance(entry, Mapping):
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    keys = set(entry)
    required_keys = {"git_path", "git_mode", "git_object", "entry_kind"}
    if not keys <= _INVENTORY_KEYS or not required_keys <= keys:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    try:
        raw_path = decode_git_path_ref(entry["git_path"], allow_repository_root=False)
    except SourceSnapshotError as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT
        ) from exc
    mode = entry["git_mode"]
    if not isinstance(mode, str) or _MODE_RE.fullmatch(mode) is None:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    obj = entry["git_object"]
    _validate_git_object(obj, expected_algorithm=algorithm)
    object_type = obj["object_type"]
    kind = entry["entry_kind"]
    expected_kind = {
        ("100644", "BLOB"): "REGULAR_BLOB",
        ("100755", "BLOB"): "EXECUTABLE_BLOB",
        ("120000", "BLOB"): "SYMLINK_BLOB",
        ("160000", "COMMIT"): "GITLINK",
    }.get((mode, object_type), "OTHER_TRACKED_ENTRY")
    if kind != expected_kind:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if object_type == "BLOB":
        if keys != _INVENTORY_KEYS:
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
        content = entry["content"]
        if not isinstance(content, Mapping) or set(content) != _CONTENT_KEYS:
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
        if (
            not isinstance(content["sha256"], str)
            or _SHA256_HEX_RE.fullmatch(content["sha256"]) is None
        ):
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
        if type(content["size_bytes"]) is not int or content["size_bytes"] < 0:
            raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    elif "content" in entry:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    return raw_path


def _validate_oid_object(value: Mapping[str, Any], *, expected_algorithm: str) -> None:
    if not isinstance(value, Mapping) or set(value) != {"algorithm", "hex"}:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if value["algorithm"] != expected_algorithm:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    _validate_oid(value["algorithm"], value["hex"])


def _validate_git_object(value: Mapping[str, Any], *, expected_algorithm: str) -> None:
    if not isinstance(value, Mapping) or set(value) != _GIT_OBJECT_KEYS:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if value["object_type"] not in {"BLOB", "COMMIT", "OTHER"}:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    if value["algorithm"] != expected_algorithm:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)
    _validate_oid(value["algorithm"], value["hex"])


def _validate_oid(algorithm: str, oid_hex: str) -> None:
    pattern = _SHA1_RE if algorithm == "SHA1" else _SHA256_RE if algorithm == "SHA256" else None
    if pattern is None or not isinstance(oid_hex, str) or pattern.fullmatch(oid_hex) is None:
        raise SourceSnapshotError(SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT)


def _validate_raw_git_path(raw: bytes) -> None:
    if not raw or b"\x00" in raw or raw.startswith(b"/") or raw.endswith(b"/"):
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    components = raw.split(b"/")
    if any(component in {b"", b".", b".."} for component in components):
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)


def _is_unicode_scalar_text(value: Any) -> bool:
    return isinstance(value, str) and not any(0xD800 <= ord(char) <= 0xDFFF for char in value)
