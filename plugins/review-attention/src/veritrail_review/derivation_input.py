from __future__ import annotations

import copy
import json
import os
import shutil
import stat
import time
import unicodedata
from bisect import bisect_right
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Mapping

from veritrail_review.canonical import (
    bounded_canonical_json_bytes,
    bounded_semantic_digest,
    sha256_bytes,
)
from veritrail_review.contracts import (
    build_source_snapshot_document,
    decode_git_path_ref,
    git_oid,
    validate_source_snapshot_document,
)
from veritrail_review.derivation_input_contracts import (
    DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
    DerivationInputRequest,
    DerivationInputRuntime,
    DerivationInputSafetyProfile,
    DerivationInputSet,
    git_acquisition_budget_for_derivation_input,
)
from veritrail_review.errors import (
    DerivationInputError,
    DerivationInputFailureCode,
    SourceSnapshotError,
    SourceSnapshotFailureCode,
)
from veritrail_review.git_objects import acquire_git_snapshot


_SHA256_HEX = frozenset("0123456789abcdef")
_PROFILE_KEYS = frozenset(
    {
        "artifact_kind",
        "schema_version",
        "canonicalization_profile",
        "profile_id",
        "profile_version",
        "language",
        "language_semantics",
        "accepted_source_encodings",
        "supported_entry_kinds",
        "fact_kinds",
        "relation_kinds",
        "normalization_rules",
        "traversal_rules",
        "profile_digest",
    }
)
_POLICY_KEYS = frozenset(
    {
        "artifact_kind",
        "schema_version",
        "canonicalization_profile",
        "policy_id",
        "version",
        "source_snapshot_digest",
        "derivation_profile_digest",
        "scope_decisions",
        "provider_requirements",
        "python_module_mapping",
        "slice_policy",
        "execution_budget",
        "governance",
        "analysis_scope_digest",
        "slice_policy_digest",
        "policy_digest",
        "seal",
    }
)
_FACT_KINDS = (
    "MODULE",
    "CLASS_DECLARATION",
    "FUNCTION_DECLARATION",
    "METHOD_DECLARATION",
    "IMPORT_DECLARATION",
)
_RELATION_KINDS = ("LEXICAL_CONTAINS", "IMPORT_TARGET_LITERAL")
_DIRECTION_RANK = {"OUTBOUND": 0, "INBOUND": 1, "BOTH": 2}
_SUPPORTED_HOST_UNICODE_VERSIONS = frozenset(
    {"13.0.0", "14.0.0", "15.0.0", "15.1.0"}
)
_PYTHON_310_KEYWORDS = frozenset(
    {
        "False", "None", "True", "and", "as", "assert", "async", "await",
        "break", "class", "continue", "def", "del", "elif", "else", "except",
        "finally", "for", "from", "global", "if", "import", "in", "is",
        "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
        "while", "with", "yield",
    }
)

# CPython 3.11--3.13 use newer Unicode databases than the frozen Python 3.10
# language profile.  These are the XID_Start/XID_Continue additions through
# Unicode 15.1, represented as inclusive hexadecimal ranges.  Rejecting them
# after the host lexical check makes the result identical on the supported
# CPython 3.10 and 3.13 matrices without importing or executing reviewed code.
_POST_PYTHON_310_START_RANGES = (
    "870-887,889-88e,8b5,8c8-8c9,c5d,cdd,170d,171f,1b4c,2c2f,2c5f,"
    "9ffd-9fff,a7c0-a7c1,a7d0-a7d1,a7d3,a7d5-a7d9,a7f2-a7f4,"
    "10570-1057a,1057c-1058a,1058c-10592,10594-10595,10597-105a1,"
    "105a3-105b1,105b3-105b9,105bb-105bc,10780-10785,10787-107b0,"
    "107b2-107ba,10f70-10f81,11071-11072,11075,1123f-11240,11740-11746,"
    "11ab0-11abf,11f02,11f04-11f10,11f12-11f33,12f90-12ff0,1342f,"
    "13441-13446,16a70-16abe,1aff0-1aff3,1aff5-1affb,1affd-1affe,"
    "1b11f-1b122,1b132,1b155,1df00-1df1e,1df25-1df2a,1e030-1e06d,"
    "1e290-1e2ad,1e4d0-1e4eb,1e7e0-1e7e6,1e7e8-1e7eb,1e7ed-1e7ee,"
    "1e7f0-1e7fe,2a6de-2a6df,2b735-2b739,2ebf0-2ee5d,31350-323af"
)
_POST_PYTHON_310_CONTINUE_RANGES = (
    "870-887,889-88e,898-89f,8b5,8c8-8d2,c3c,c5d,cdd,cf3,ece,170d,"
    "1715,171f,180f,1ac1-1ace,1b4c,1dfa,200c-200d,2c2f,2c5f,30fb,"
    "9ffd-9fff,a7c0-a7c1,a7d0-a7d1,a7d3,a7d5-a7d9,a7f2-a7f4,ff65,"
    "10570-1057a,1057c-1058a,1058c-10592,10594-10595,10597-105a1,"
    "105a3-105b1,105b3-105b9,105bb-105bc,10780-10785,10787-107b0,"
    "107b2-107ba,10efd-10eff,10f70-10f85,11070-11075,110c2,1123f-11241,"
    "11740-11746,11ab0-11abf,11f00-11f10,11f12-11f3a,11f3e-11f42,"
    "11f50-11f59,12f90-12ff0,1342f,13440-13455,16a70-16abe,16ac0-16ac9,"
    "1aff0-1aff3,1aff5-1affb,1affd-1affe,1b11f-1b122,1b132,1b155,"
    "1cf00-1cf2d,1cf30-1cf46,1df00-1df1e,1df25-1df2a,1e030-1e06d,"
    "1e08f,1e290-1e2ae,1e4d0-1e4f9,1e7e0-1e7e6,1e7e8-1e7eb,"
    "1e7ed-1e7ee,1e7f0-1e7fe,2a6de-2a6df,2b735-2b739,2ebf0-2ee5d,"
    "31350-323af"
)
_PROFILE_CONSTANTS = {
    "artifact_kind": "DERIVATION_PROFILE",
    "schema_version": "0.1",
    "canonicalization_profile": "veritrail-json-c14n/1",
    "profile_id": "veritrail-python-source-3.10",
    "profile_version": "0.1",
    "language": "PYTHON",
    "language_semantics": "PYTHON_3_10",
    "accepted_source_encodings": ["UTF-8", "UTF-8-SIG"],
    "supported_entry_kinds": ["REGULAR_BLOB", "EXECUTABLE_BLOB"],
    "fact_kinds": list(_FACT_KINDS),
    "relation_kinds": list(_RELATION_KINDS),
    "normalization_rules": {
        "path": "git-path-hex/1",
        "anchor": "raw-blob-half-open/1",
        "identifier": "python-3.10-nfkc/1",
        "fact_projection": "r1-python-facts/0.1",
        "import_projection": "r1-python-import-literal/0.1",
    },
    "traversal_rules": {
        "algorithm": "breadth-first/1",
        "budget": "inclusive-atomic-edge/1",
        "tie_break": "r1-relation-rank/0.1",
        "cycle_identity": "fact-and-relation-digest/1",
    },
}


class _DuplicateKey(ValueError):
    pass


class _BindingState:
    def __init__(
        self,
        profile: DerivationInputSafetyProfile,
        *,
        clock: Callable[[], float],
        stage_hook: Callable[[str], None] | None,
    ) -> None:
        self.profile = profile
        self.clock = clock
        self.stage_hook = stage_hook
        self.deadline = clock() + profile.wall_clock_ms / 1000.0

    def checkpoint(self, stage: str) -> None:
        if self.stage_hook is not None:
            self.stage_hook(stage)
        if self.clock() >= self.deadline:
            raise DerivationInputError(
                DerivationInputFailureCode.INPUT_SAFETY_BUDGET_EXHAUSTED
            )


def bind_derivation_inputs(
    request: DerivationInputRequest,
    *,
    runtime: DerivationInputRuntime | None = None,
) -> DerivationInputSet:
    """Import, cross-bind, and locally reproduce the exact R1 derivation inputs."""

    return _bind_derivation_inputs(
        request,
        runtime=runtime or DerivationInputRuntime(),
        safety_profile=DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
        clock=time.monotonic,
        stage_hook=None,
    )


def _bind_derivation_inputs(
    request: DerivationInputRequest,
    *,
    runtime: DerivationInputRuntime,
    safety_profile: DerivationInputSafetyProfile,
    clock: Callable[[], float],
    stage_hook: Callable[[str], None] | None,
) -> DerivationInputSet:
    try:
        _validate_request_and_runtime(request, runtime, safety_profile)
        state = _BindingState(safety_profile, clock=clock, stage_hook=stage_hook)
        repository = _validate_repository(request.repository_path)
        git_executable = _resolve_runtime_git(runtime.git_executable, repository)

        snapshot_bytes = _read_artifact(
            request.source_snapshot_path,
            safety_profile.max_source_snapshot_bytes,
            state,
        )
        policy_bytes = _read_artifact(
            request.review_policy_path,
            safety_profile.max_review_policy_bytes,
            state,
        )
        profile_bytes = _read_artifact(
            request.derivation_profile_path,
            safety_profile.max_derivation_profile_bytes,
            state,
        )

        snapshot = _parse_artifact(
            snapshot_bytes,
            DerivationInputFailureCode.NONCONFORMANT_SOURCE_SNAPSHOT,
            state,
        )
        policy = _parse_artifact(
            policy_bytes,
            DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY,
            state,
        )
        profile = _parse_artifact(
            profile_bytes,
            DerivationInputFailureCode.NONCONFORMANT_DERIVATION_PROFILE,
            state,
        )

        _validate_snapshot(snapshot, snapshot_bytes, state)
        _validate_profile(profile, state)
        _validate_policy(policy, profile, state)
        _validate_cross_artifact_binding(snapshot, policy, profile, state)

        acquisition = _reacquire_snapshot(
            snapshot,
            snapshot_bytes,
            repository,
            git_executable,
            safety_profile,
            state,
        )
        state.checkpoint("owned-copy-start")
        total_blob_bytes = sum(len(value) for value in acquisition.blob_bytes_by_oid.values())
        if total_blob_bytes > safety_profile.max_total_unique_blob_bytes:
            _raise(DerivationInputFailureCode.INPUT_SAFETY_BUDGET_EXHAUSTED)
        result = DerivationInputSet.create(
            source_snapshot_canonical_bytes=snapshot_bytes,
            review_policy_canonical_bytes=policy_bytes,
            derivation_profile_canonical_bytes=profile_bytes,
            verified_blob_bytes_by_object_identity=acquisition.blob_bytes_by_oid,
            source_snapshot_digest=snapshot["source_snapshot_digest"],
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=profile["profile_digest"],
        )
        state.checkpoint("owned-copy-complete")
        return result
    except DerivationInputError:
        raise
    except Exception as exc:
        raise DerivationInputError(
            DerivationInputFailureCode.INTERNAL_INPUT_BINDING_ERROR
        ) from exc


def _validate_request_and_runtime(
    request: DerivationInputRequest,
    runtime: DerivationInputRuntime,
    profile: DerivationInputSafetyProfile,
) -> None:
    if not isinstance(request, DerivationInputRequest) or not isinstance(
        runtime, DerivationInputRuntime
    ):
        _raise(DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST)
    if profile.profile_id != DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE.profile_id:
        _raise(DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST)
    if unicodedata.unidata_version not in _SUPPORTED_HOST_UNICODE_VERSIONS:
        _raise(DerivationInputFailureCode.INPUT_RUNTIME_UNAVAILABLE)
    for item in (
        "wall_clock_ms",
        "max_source_snapshot_bytes",
        "max_review_policy_bytes",
        "max_derivation_profile_bytes",
        "max_total_unique_blob_bytes",
    ):
        value = getattr(profile, item)
        if type(value) is not int or value < 0:
            _raise(DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST)
        if value > getattr(DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE, item):
            _raise(DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST)
    for value in (
        request.source_snapshot_path,
        request.review_policy_path,
        request.derivation_profile_path,
        request.repository_path,
    ):
        if not isinstance(value, Path) or not value.is_absolute():
            _raise(DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST)
    if runtime.git_executable is not None and not runtime.git_executable.is_absolute():
        _raise(DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST)


def _validate_repository(path: Path) -> Path:
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise DerivationInputError(
            DerivationInputFailureCode.INPUT_REPOSITORY_UNAVAILABLE
        ) from exc
    if not resolved.is_dir():
        _raise(DerivationInputFailureCode.INPUT_REPOSITORY_UNAVAILABLE)
    return resolved


def _resolve_runtime_git(explicit: Path | None, repository: Path) -> Path:
    candidate = os.fspath(explicit) if explicit is not None else shutil.which("git")
    if not candidate:
        _raise(DerivationInputFailureCode.INPUT_RUNTIME_UNAVAILABLE)
    try:
        resolved = Path(candidate).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise DerivationInputError(
            DerivationInputFailureCode.INPUT_RUNTIME_UNAVAILABLE
        ) from exc
    if not resolved.is_file() or resolved.is_relative_to(repository):
        _raise(DerivationInputFailureCode.INPUT_RUNTIME_UNAVAILABLE)
    return resolved


def _read_artifact(path: Path, maximum: int, state: _BindingState) -> bytes:
    state.checkpoint("artifact-read-start")
    try:
        before = path.lstat()
    except FileNotFoundError as exc:
        raise DerivationInputError(
            DerivationInputFailureCode.INPUT_ARTIFACT_UNAVAILABLE
        ) from exc
    except OSError as exc:
        raise DerivationInputError(
            DerivationInputFailureCode.INPUT_ARTIFACT_UNAVAILABLE
        ) from exc
    _validate_ordinary_stat(before)
    try:
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            _validate_ordinary_stat(opened)
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                _raise(DerivationInputFailureCode.INPUT_ARTIFACT_UNAVAILABLE)
            value = bytearray()
            while True:
                state.checkpoint("artifact-read-chunk")
                chunk = handle.read(min(65_536, maximum + 1 - len(value)))
                if not chunk:
                    break
                value.extend(chunk)
                if len(value) > maximum:
                    _raise(DerivationInputFailureCode.INPUT_ARTIFACT_TOO_LARGE)
    except DerivationInputError:
        raise
    except (FileNotFoundError, PermissionError, OSError) as exc:
        raise DerivationInputError(
            DerivationInputFailureCode.INPUT_ARTIFACT_UNAVAILABLE
        ) from exc
    state.checkpoint("artifact-read-complete")
    return bytes(value)


def _validate_ordinary_stat(value: os.stat_result) -> None:
    attributes = int(getattr(value, "st_file_attributes", 0))
    reparse_flag = int(getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    if (
        not stat.S_ISREG(value.st_mode)
        or attributes & reparse_flag
        or int(getattr(value, "st_nlink", 1)) != 1
    ):
        _raise(DerivationInputFailureCode.INPUT_ARTIFACT_NOT_ORDINARY_FILE)


def _parse_artifact(
    raw: bytes,
    code: DerivationInputFailureCode,
    state: _BindingState,
) -> dict[str, Any]:
    state.checkpoint("artifact-parse-start")
    try:
        if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
            raise ValueError
        if not raw.endswith(b"\n") or raw.count(b"\n") != 1:
            raise ValueError
        text = raw.decode("utf-8", errors="strict")

        def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise _DuplicateKey
                result[key] = value
            return result

        document = json.loads(text, object_pairs_hook=pairs_hook)
        if not isinstance(document, dict):
            raise ValueError
        if bounded_canonical_json_bytes(
            document,
            max_bytes=len(raw),
            deadline_check=lambda: state.checkpoint("artifact-canonical-validation"),
        ) + b"\n" != raw:
            raise ValueError
    except (UnicodeError, ValueError, TypeError, RecursionError, SourceSnapshotError) as exc:
        raise DerivationInputError(code) from exc
    state.checkpoint("artifact-parse-complete")
    return document


def _validate_snapshot(
    document: Mapping[str, Any], raw: bytes, state: _BindingState
) -> None:
    state.checkpoint("source-snapshot-validation-start")
    try:
        validate_source_snapshot_document(
            document,
            expected_bytes=raw,
            max_canonical_bytes=state.profile.max_source_snapshot_bytes,
            deadline_check=lambda: state.checkpoint("source-snapshot-validation"),
        )
    except SourceSnapshotError as exc:
        if exc.code == SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED:
            raise DerivationInputError(
                DerivationInputFailureCode.INPUT_SAFETY_BUDGET_EXHAUSTED
            ) from exc
        raise DerivationInputError(
            DerivationInputFailureCode.NONCONFORMANT_SOURCE_SNAPSHOT
        ) from exc
    state.checkpoint("source-snapshot-validation-complete")


def _validate_profile(document: Mapping[str, Any], state: _BindingState) -> None:
    code = DerivationInputFailureCode.NONCONFORMANT_DERIVATION_PROFILE
    state.checkpoint("derivation-profile-validation-start")
    try:
        if set(document) != _PROFILE_KEYS:
            raise ValueError
        for key, expected in _PROFILE_CONSTANTS.items():
            if document.get(key) != expected:
                raise ValueError
        _require_digest(document.get("profile_digest"))
        payload = {key: copy.deepcopy(value) for key, value in document.items() if key != "profile_digest"}
        if bounded_semantic_digest(
            "veritrail.review.derivation-profile/0.1",
            payload,
            max_bytes=state.profile.max_derivation_profile_bytes + 1024,
            deadline_check=lambda: state.checkpoint("derivation-profile-digest"),
        ) != document["profile_digest"]:
            raise ValueError
    except (KeyError, TypeError, ValueError, SourceSnapshotError) as exc:
        raise DerivationInputError(code) from exc
    state.checkpoint("derivation-profile-validation-complete")


def _validate_policy(
    document: Mapping[str, Any], profile: Mapping[str, Any], state: _BindingState
) -> None:
    code = DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY
    state.checkpoint("review-policy-validation-start")
    try:
        if set(document) != _POLICY_KEYS:
            raise ValueError
        if document["artifact_kind"] != "REVIEW_POLICY":
            raise ValueError
        if document["schema_version"] != "0.1":
            raise ValueError
        if document["canonicalization_profile"] != "veritrail-json-c14n/1":
            raise ValueError
        _require_text(document["policy_id"])
        _require_positive_integer(document["version"])
        for name in (
            "source_snapshot_digest",
            "derivation_profile_digest",
            "analysis_scope_digest",
            "slice_policy_digest",
            "policy_digest",
        ):
            _require_digest(document[name])
        _validate_scope_decisions(document["scope_decisions"])
        _validate_provider_requirements(document["provider_requirements"])
        _validate_python_module_mapping(document["python_module_mapping"])
        _validate_slice_policy(document["slice_policy"], profile)
        _validate_execution_budget(document["execution_budget"])
        _validate_governance(document["governance"])

        analysis_payload = {
            "source_snapshot_digest": document["source_snapshot_digest"],
            "derivation_profile_digest": document["derivation_profile_digest"],
            "scope_decisions": copy.deepcopy(document["scope_decisions"]),
            "provider_requirements": copy.deepcopy(document["provider_requirements"]),
            "python_module_mapping": copy.deepcopy(document["python_module_mapping"]),
        }
        if bounded_semantic_digest(
            "veritrail.review.analysis-scope/0.1",
            analysis_payload,
            max_bytes=state.profile.max_review_policy_bytes + 1024,
            deadline_check=lambda: state.checkpoint("review-policy-analysis-scope-digest"),
        ) != document["analysis_scope_digest"]:
            raise ValueError
        if bounded_semantic_digest(
            "veritrail.review.slice-policy/0.1",
            {
                "analysis_scope_digest": document["analysis_scope_digest"],
                "slice_policy": copy.deepcopy(document["slice_policy"]),
            },
            max_bytes=state.profile.max_review_policy_bytes + 1024,
            deadline_check=lambda: state.checkpoint("review-policy-slice-digest"),
        ) != document["slice_policy_digest"]:
            raise ValueError
        policy_payload = {
            key: copy.deepcopy(value)
            for key, value in document.items()
            if key not in {"analysis_scope_digest", "slice_policy_digest", "policy_digest", "seal"}
        }
        if bounded_semantic_digest(
            "veritrail.review.review-policy/0.1",
            policy_payload,
            max_bytes=state.profile.max_review_policy_bytes + 1024,
            deadline_check=lambda: state.checkpoint("review-policy-digest"),
        ) != document["policy_digest"]:
            raise ValueError
        seal = document["seal"]
        if not isinstance(seal, Mapping) or set(seal) != {"algorithm", "digest"}:
            raise ValueError
        if seal["algorithm"] != "sha256":
            raise ValueError
        _require_digest(seal["digest"])
        unsealed = {key: copy.deepcopy(value) for key, value in document.items() if key != "seal"}
        if sha256_bytes(
            bounded_canonical_json_bytes(
                unsealed,
                max_bytes=state.profile.max_review_policy_bytes,
                deadline_check=lambda: state.checkpoint("review-policy-seal"),
            )
        ) != seal["digest"]:
            raise ValueError
    except (KeyError, TypeError, ValueError, SourceSnapshotError) as exc:
        raise DerivationInputError(code) from exc
    state.checkpoint("review-policy-validation-complete")


def _validate_scope_decisions(value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError
    paths: list[bytes] = []
    for item in value:
        if not isinstance(item, Mapping) or set(item) != {
            "git_path",
            "disposition",
            "source_class",
            "reason_code",
        }:
            raise ValueError
        paths.append(_decode_policy_path(item["git_path"], allow_root=False))
        if item["source_class"] not in {
            "FIRST_PARTY",
            "GENERATED",
            "VENDORED",
            "UNCLASSIFIED",
        }:
            raise ValueError
        pair = (item["disposition"], item["reason_code"])
        if pair not in {
            ("IN_SCOPE", "POLICY_INCLUDED"),
            ("OUT_OF_SCOPE", "POLICY_EXCLUDED"),
        }:
            raise ValueError
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError


def _validate_provider_requirements(value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError
    identities: list[str] = []
    for item in value:
        if not isinstance(item, Mapping) or set(item) != {
            "capability_id",
            "required",
            "composition_mode",
        }:
            raise ValueError
        _require_text(item["capability_id"])
        if type(item["required"]) is not bool or item["composition_mode"] != "CUMULATIVE":
            raise ValueError
        identities.append(item["capability_id"])
    if identities != sorted(identities) or len(identities) != len(set(identities)):
        raise ValueError


def _validate_python_module_mapping(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != {"module_root", "package_prefix"}:
        raise ValueError
    _decode_policy_path(value["module_root"], allow_root=True)
    prefix = value["package_prefix"]
    if not isinstance(prefix, list) or len(prefix) != len(set(prefix)):
        raise ValueError
    for item in prefix:
        if not _is_python_identifier(item):
            raise ValueError


def _validate_slice_policy(value: Any, profile: Mapping[str, Any]) -> None:
    if not isinstance(value, Mapping) or set(value) != {
        "anchor_fact_kinds",
        "allowed_relations",
        "max_depth",
        "max_symbols",
        "max_files",
        "max_relations",
    }:
        raise ValueError
    anchors = value["anchor_fact_kinds"]
    fact_kinds = profile["fact_kinds"]
    if not isinstance(anchors, list) or not anchors:
        raise ValueError
    if any(item not in fact_kinds for item in anchors):
        raise ValueError
    if anchors != sorted(set(anchors), key=fact_kinds.index):
        raise ValueError
    relations = value["allowed_relations"]
    relation_kinds = profile["relation_kinds"]
    if not isinstance(relations, list):
        raise ValueError
    keys: list[tuple[int, int]] = []
    identities: list[tuple[str, str]] = []
    for item in relations:
        if not isinstance(item, Mapping) or set(item) != {"relation_kind", "direction"}:
            raise ValueError
        if item["relation_kind"] not in relation_kinds or item["direction"] not in _DIRECTION_RANK:
            raise ValueError
        identities.append((item["relation_kind"], item["direction"]))
        keys.append((relation_kinds.index(item["relation_kind"]), _DIRECTION_RANK[item["direction"]]))
    if keys != sorted(keys) or len(identities) != len(set(identities)):
        raise ValueError
    _require_nonnegative_integer(value["max_depth"])
    _require_positive_integer(value["max_symbols"])
    _require_positive_integer(value["max_files"])
    _require_nonnegative_integer(value["max_relations"])


def _validate_execution_budget(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != {
        "wall_clock_ms",
        "memory_bytes",
        "artifact_bytes",
    }:
        raise ValueError
    for item in value.values():
        _require_positive_integer(item)


def _validate_governance(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != {
        "claim_owner_ref",
        "drafter_ref",
        "seal_authority_ref",
        "seal_decision",
    }:
        raise ValueError
    for name in ("claim_owner_ref", "drafter_ref", "seal_authority_ref"):
        _require_text(value[name])
    if value["seal_decision"] != "CONFIRMED":
        raise ValueError


def _validate_cross_artifact_binding(
    snapshot: Mapping[str, Any],
    policy: Mapping[str, Any],
    profile: Mapping[str, Any],
    state: _BindingState,
) -> None:
    state.checkpoint("cross-artifact-validation-start")
    if policy["source_snapshot_digest"] != snapshot["source_snapshot_digest"]:
        _raise(DerivationInputFailureCode.POLICY_SNAPSHOT_MISMATCH)
    if policy["derivation_profile_digest"] != profile["profile_digest"]:
        _raise(DerivationInputFailureCode.POLICY_PROFILE_MISMATCH)
    inventory_paths = [
        _decode_policy_path(item["git_path"], allow_root=False)
        for item in snapshot["inventory"]
    ]
    decision_paths = [
        _decode_policy_path(item["git_path"], allow_root=False)
        for item in policy["scope_decisions"]
    ]
    if inventory_paths != decision_paths:
        _raise(DerivationInputFailureCode.POLICY_SCOPE_MISMATCH)
    analysis_root = _decode_policy_path(
        snapshot["source_coordinate"]["analysis_root"], allow_root=True
    )
    module_root = _decode_policy_path(
        policy["python_module_mapping"]["module_root"], allow_root=True
    )
    if analysis_root and not (
        module_root == analysis_root or module_root.startswith(analysis_root + b"/")
    ):
        _raise(DerivationInputFailureCode.MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT)
    state.checkpoint("cross-artifact-validation-complete")


def _reacquire_snapshot(
    snapshot: Mapping[str, Any],
    imported_bytes: bytes,
    repository: Path,
    git_executable: Path,
    profile: DerivationInputSafetyProfile,
    state: _BindingState,
):
    state.checkpoint("source-reacquisition-start")
    coordinate = snapshot["source_coordinate"]
    commit = coordinate["commit_oid"]
    analysis_root = _decode_policy_path(coordinate["analysis_root"], allow_root=True)
    try:
        acquisition = acquire_git_snapshot(
            repository_path=repository,
            git_executable=git_executable,
            commit_oid=commit["hex"],
            analysis_root=analysis_root,
            budget=git_acquisition_budget_for_derivation_input(profile),
            clock=state.clock,
            stage_hook=state.stage_hook,
            deadline=state.deadline,
        )
        if acquisition.algorithm != commit["algorithm"]:
            _raise(DerivationInputFailureCode.SOURCE_REACQUISITION_MISMATCH)
        regenerated = build_source_snapshot_document(
            repository_id=snapshot["repository_id"],
            commit_oid=git_oid(acquisition.algorithm, acquisition.commit_oid),
            commit_tree_oid=git_oid(acquisition.algorithm, acquisition.commit_tree_oid),
            analysis_tree_oid=git_oid(acquisition.algorithm, acquisition.analysis_tree_oid),
            analysis_root=copy.deepcopy(coordinate["analysis_root"]),
            inventory=[copy.deepcopy(dict(item)) for item in acquisition.inventory],
            max_canonical_bytes=profile.max_source_snapshot_bytes,
            deadline_check=lambda: state.checkpoint("source-reacquisition-canonical"),
        )
        regenerated_bytes = validate_source_snapshot_document(
            regenerated,
            max_canonical_bytes=profile.max_source_snapshot_bytes,
            deadline_check=lambda: state.checkpoint("source-reacquisition-validation"),
        )
        if regenerated_bytes != imported_bytes:
            _raise(DerivationInputFailureCode.SOURCE_REACQUISITION_MISMATCH)
    except DerivationInputError:
        raise
    except SourceSnapshotError as exc:
        if exc.code == SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED:
            raise DerivationInputError(
                DerivationInputFailureCode.INPUT_SAFETY_BUDGET_EXHAUSTED
            ) from exc
        if exc.code == SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE:
            raise DerivationInputError(
                DerivationInputFailureCode.INPUT_REPOSITORY_UNAVAILABLE
            ) from exc
        raise DerivationInputError(
            DerivationInputFailureCode.SOURCE_REACQUISITION_MISMATCH
        ) from exc
    state.checkpoint("source-reacquisition-complete")
    return acquisition


def _decode_policy_path(value: Any, *, allow_root: bool) -> bytes:
    try:
        return decode_git_path_ref(value, allow_repository_root=allow_root)
    except SourceSnapshotError as exc:
        raise ValueError from exc


def _require_digest(value: Any) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(
        char not in _SHA256_HEX for char in value
    ):
        raise ValueError


def _require_text(value: Any) -> None:
    if not isinstance(value, str) or not value or any(
        0xD800 <= ord(char) <= 0xDFFF for char in value
    ):
        raise ValueError


def _require_positive_integer(value: Any) -> None:
    if type(value) is not int or value < 1:
        raise ValueError


def _require_nonnegative_integer(value: Any) -> None:
    if type(value) is not int or value < 0:
        raise ValueError


def _is_python_identifier(value: Any) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or unicodedata.normalize("NFKC", value) != value
        or not value.isidentifier()
        or value in _PYTHON_310_KEYWORDS
    ):
        return False
    if _codepoint_in_ranges(ord(value[0]), _POST_PYTHON_310_START_RANGES):
        return False
    return not any(
        _codepoint_in_ranges(ord(character), _POST_PYTHON_310_CONTINUE_RANGES)
        for character in value[1:]
    )


def _codepoint_in_ranges(codepoint: int, encoded_ranges: str) -> bool:
    lower_bounds, upper_bounds = _decode_codepoint_ranges(encoded_ranges)
    index = bisect_right(lower_bounds, codepoint) - 1
    return index >= 0 and codepoint <= upper_bounds[index]


@lru_cache(maxsize=2)
def _decode_codepoint_ranges(
    encoded_ranges: str,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    lower_bounds: list[int] = []
    upper_bounds: list[int] = []
    for item in encoded_ranges.split(","):
        first, separator, last = item.partition("-")
        lower = int(first, 16)
        upper = int(last, 16) if separator else lower
        lower_bounds.append(lower)
        upper_bounds.append(upper)
    return tuple(lower_bounds), tuple(upper_bounds)


def _raise(code: DerivationInputFailureCode) -> None:
    raise DerivationInputError(code)
