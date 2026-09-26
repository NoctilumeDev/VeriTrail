from __future__ import annotations

import copy
import io
import re
import time
from enum import Enum
from typing import Any, Mapping

from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
    _validate_language_support_classification,
)
from veritrail_review.canonical import semantic_digest, sha256_bytes
from veritrail_review.derivation_input import (
    _BindingState,
    _decode_policy_path,
    _parse_artifact,
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
    _validate_snapshot,
)
from veritrail_review.derivation_input_contracts import (
    DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
    DerivationInputSet,
)
from veritrail_review.errors import DerivationInputFailureCode
from veritrail_review.git_objects import verify_git_object_bytes


_FUNCTION_ID = "r1-python-language-support/0.2"
_REASON_RANK = (
    "UNCLASSIFIED_SOURCE",
    "UNSUPPORTED_ENTRY_KIND",
    "UNSUPPORTED_LANGUAGE",
    "UNSUPPORTED_SOURCE_ENCODING",
)
_ACCEPTED_ENCODINGS = frozenset({"UTF-8", "UTF-8-SIG"})
_UTF8_BOM = b"\xef\xbb\xbf"
_COOKIE_RE = re.compile(
    r"^[ \t\f]*#.*?coding[:=][ \t]*([-\w.]+)",
    re.ASCII,
)
_BLANK_RE = re.compile(br"^[ \t\f]*(?:[#\r\n]|$)", re.ASCII)
_UTF8_ALIAS_TARGETS = {
    "cp65001": "utf_8",
    "u8": "utf_8",
    "utf": "utf_8",
    "utf8": "utf_8",
    "utf8_ucs2": "utf_8",
    "utf8_ucs4": "utf_8",
}


class _LanguageSupportFailureCode(str, Enum):
    INPUT_REVALIDATION_REJECTED = "INPUT_REVALIDATION_REJECTED"
    FUNCTION_PROFILE_INCOMPATIBLE = "FUNCTION_PROFILE_INCOMPATIBLE"
    CLASSIFICATION_INTEGRITY_REJECTED = "CLASSIFICATION_INTEGRITY_REJECTED"


_FAILURE_MESSAGES = {
    _LanguageSupportFailureCode.INPUT_REVALIDATION_REJECTED: (
        "the exact Language Support input history failed revalidation"
    ),
    _LanguageSupportFailureCode.FUNCTION_PROFILE_INCOMPATIBLE: (
        "the frozen Profile is incompatible with r1-python-language-support/0.2"
    ),
    _LanguageSupportFailureCode.CLASSIFICATION_INTEGRITY_REJECTED: (
        "the private Language Support classification failed integrity validation"
    ),
}


class _LanguageSupportError(RuntimeError):
    def __init__(self, code: _LanguageSupportFailureCode) -> None:
        self.code = code
        self.safe_message = _FAILURE_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")


class _EncodingRejected(ValueError):
    pass


def classify_language_support(
    inputs: DerivationInputSet,
) -> OwnedLanguageSupportClassification:
    """Recompute the private 0.2 classification without minting authority."""

    snapshot, policy, profile, blobs = _revalidate_exact_inputs(inputs)
    _require_function_profile_compatibility(profile)
    try:
        subjects: list[dict[str, object]] = []
        inventory = snapshot["inventory"]
        decisions = policy["scope_decisions"]
        if not isinstance(inventory, list) or not isinstance(decisions, list):
            raise ValueError
        for item, decision in zip(inventory, decisions, strict=True):
            if not isinstance(item, dict) or not isinstance(decision, dict):
                raise ValueError
            if decision["disposition"] != "IN_SCOPE":
                continue
            subjects.append(
                _classify_subject(
                    item=item,
                    decision=decision,
                    profile=profile,
                    blobs=blobs,
                )
            )
        subjects.sort(key=_subject_raw_path)
        eligible_count = sum(
            item["disposition"] == "ELIGIBLE" for item in subjects
        )
        document: dict[str, object] = {
            "language_support_function": _FUNCTION_ID,
            "subjects": subjects,
            "denominator_count": len(subjects),
            "eligible_count": eligible_count,
            "unsupported_count": len(subjects) - eligible_count,
        }
        document["classification_digest"] = semantic_digest(
            "veritrail.review.private-language-support-classification/0.2",
            document,
        )
        result = OwnedLanguageSupportClassification._create(
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=inputs.policy_digest,
            analysis_scope_digest=inputs.analysis_scope_digest,
            derivation_profile_digest=inputs.derivation_profile_digest,
            classification_document=document,
        )
        _validate_language_support_classification(result)
        return result
    except _LanguageSupportError:
        raise
    except Exception as exc:
        raise _LanguageSupportError(
            _LanguageSupportFailureCode.CLASSIFICATION_INTEGRITY_REJECTED
        ) from exc


def _revalidate_exact_inputs(
    inputs: DerivationInputSet,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, bytes]]:
    try:
        if (
            type(inputs) is not DerivationInputSet
            or type(inputs.source_snapshot_canonical_bytes) is not bytes
            or type(inputs.review_policy_canonical_bytes) is not bytes
            or type(inputs.derivation_profile_canonical_bytes) is not bytes
        ):
            raise ValueError
        state = _BindingState(
            DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
            clock=time.monotonic,
            stage_hook=None,
        )
        snapshot = _parse_artifact(
            inputs.source_snapshot_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_SOURCE_SNAPSHOT,
            state,
        )
        policy = _parse_artifact(
            inputs.review_policy_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY,
            state,
        )
        profile = _parse_artifact(
            inputs.derivation_profile_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_DERIVATION_PROFILE,
            state,
        )
        _validate_snapshot(snapshot, inputs.source_snapshot_canonical_bytes, state)
        _validate_profile(profile, state)
        _validate_policy(policy, profile, state)
        _validate_cross_artifact_binding(snapshot, policy, profile, state)
        if (
            snapshot["source_snapshot_digest"] != inputs.source_snapshot_digest
            or policy["source_snapshot_digest"] != inputs.source_snapshot_digest
            or policy["policy_digest"] != inputs.policy_digest
            or policy["analysis_scope_digest"] != inputs.analysis_scope_digest
            or policy["slice_policy_digest"] != inputs.slice_policy_digest
            or policy["derivation_profile_digest"]
            != inputs.derivation_profile_digest
            or profile["profile_digest"] != inputs.derivation_profile_digest
        ):
            raise ValueError
        blobs = _validate_owned_blob_bytes(inputs, snapshot, state)
        state.checkpoint("language-support-input-revalidation-complete")
        return snapshot, policy, profile, blobs
    except Exception as exc:
        raise _LanguageSupportError(
            _LanguageSupportFailureCode.INPUT_REVALIDATION_REJECTED
        ) from exc


def _validate_owned_blob_bytes(
    inputs: DerivationInputSet,
    snapshot: Mapping[str, object],
    state: _BindingState,
) -> dict[str, bytes]:
    inventory = snapshot["inventory"]
    if not isinstance(inventory, list):
        raise ValueError
    expected: dict[str, tuple[str, int, str]] = {}
    for item in inventory:
        if not isinstance(item, Mapping):
            raise ValueError
        git_object = item["git_object"]
        if not isinstance(git_object, Mapping):
            raise ValueError
        if git_object["object_type"] != "BLOB":
            continue
        content = item.get("content")
        if not isinstance(content, Mapping):
            raise ValueError
        oid = git_object["hex"]
        algorithm = git_object["algorithm"]
        size = content["size_bytes"]
        digest = content["sha256"]
        if (
            not isinstance(oid, str)
            or not isinstance(algorithm, str)
            or type(size) is not int
            or size < 0
            or not isinstance(digest, str)
        ):
            raise ValueError
        identity = (algorithm, size, digest)
        previous = expected.setdefault(oid, identity)
        if previous != identity:
            raise ValueError
    supplied = inputs.verified_blob_bytes_by_object_identity
    if not isinstance(supplied, Mapping) or set(supplied) != set(expected):
        raise ValueError
    owned: dict[str, bytes] = {}
    for oid in sorted(expected):
        state.checkpoint("language-support-blob-validation")
        raw = supplied[oid]
        algorithm, size, digest = expected[oid]
        if (
            type(raw) is not bytes
            or len(raw) != size
            or sha256_bytes(raw) != digest
        ):
            raise ValueError
        verify_git_object_bytes(
            algorithm=algorithm,
            object_type="blob",
            oid=oid,
            declared_size=size,
            body=raw,
        )
        owned[oid] = raw
    return owned


def _require_function_profile_compatibility(profile: Mapping[str, object]) -> None:
    encodings = profile.get("accepted_source_encodings")
    if (
        profile.get("language") != "PYTHON"
        or profile.get("language_semantics") != "PYTHON_3_10"
        or not isinstance(encodings, list)
        or any(not isinstance(item, str) for item in encodings)
        or frozenset(encodings) != _ACCEPTED_ENCODINGS
    ):
        raise _LanguageSupportError(
            _LanguageSupportFailureCode.FUNCTION_PROFILE_INCOMPATIBLE
        )


def _classify_subject(
    *,
    item: dict[str, object],
    decision: dict[str, object],
    profile: dict[str, Any],
    blobs: Mapping[str, bytes],
) -> dict[str, object]:
    raw_path = _decode_policy_path(item["git_path"], allow_root=False)
    source_class_passes = decision["source_class"] in {
        "FIRST_PARTY",
        "GENERATED",
        "VENDORED",
    }
    entry_kind_passes = item["entry_kind"] in profile["supported_entry_kinds"]
    language_path_passes = (
        profile["language"] == "PYTHON" and raw_path.endswith(b".py")
    )
    effective_encoding: str | None = None
    encoding_passes: bool | None = None
    if entry_kind_passes and language_path_passes:
        git_object = item["git_object"]
        if not isinstance(git_object, dict):
            raise ValueError
        raw = blobs[git_object["hex"]]
        effective_encoding = _qualify_source_encoding(raw)
        encoding_passes = effective_encoding is not None
    failed = {
        reason
        for reason, passed in (
            ("UNCLASSIFIED_SOURCE", source_class_passes),
            ("UNSUPPORTED_ENTRY_KIND", entry_kind_passes),
            ("UNSUPPORTED_LANGUAGE", language_path_passes),
            ("UNSUPPORTED_SOURCE_ENCODING", encoding_passes),
        )
        if passed is False
    }
    reasons = [reason for reason in _REASON_RANK if reason in failed]
    semantic_input = {
        "language_support_function": _FUNCTION_ID,
        "inventory_item": copy.deepcopy(item),
        "scope_semantics": {
            "disposition": "IN_SCOPE",
            "source_class": decision["source_class"],
        },
        "profile_support_semantics": {
            "language": profile["language"],
            "language_semantics": profile["language_semantics"],
            "supported_entry_kinds": list(profile["supported_entry_kinds"]),
            "accepted_source_encodings": sorted(
                set(profile["accepted_source_encodings"])
            ),
            "normalization_rules.path": profile["normalization_rules"]["path"],
        },
    }
    return {
        "subject_identity": semantic_digest(
            "veritrail.review.language-support-subject/0.2",
            semantic_input,
        ),
        "semantic_input": semantic_input,
        "disposition": "ELIGIBLE" if not reasons else "UNSUPPORTED",
        "reason_codes": reasons,
        "effective_source_encoding": (
            effective_encoding if not reasons else None
        ),
    }


def _qualify_source_encoding(raw: bytes) -> str | None:
    try:
        stream = io.BytesIO(raw)
        first = stream.readline()
        bom_found = first.startswith(_UTF8_BOM)
        if bom_found:
            first = first[len(_UTF8_BOM) :]
        declaration = _find_cookie(first) if first else None
        if declaration is None and first and _BLANK_RE.match(first):
            second = stream.readline()
            declaration = _find_cookie(second) if second else None
        if bom_found:
            if declaration is not None and _get_normal_name(declaration) != "utf-8":
                return None
            raw[len(_UTF8_BOM) :].decode("utf-8", errors="strict")
            return "UTF-8-SIG"
        if declaration is not None and not _is_accepted_utf8_declaration(declaration):
            return None
        raw.decode("utf-8", errors="strict")
        return "UTF-8"
    except (UnicodeDecodeError, _EncodingRejected):
        return None


def _find_cookie(line: bytes) -> str | None:
    try:
        text = line.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise _EncodingRejected from exc
    match = _COOKIE_RE.match(text)
    if match is None:
        return None
    return _get_normal_name(match.group(1))


def _get_normal_name(original: str) -> str:
    name = original[:12].lower().replace("_", "-")
    if name == "utf-8" or name.startswith("utf-8-"):
        return "utf-8"
    if name in {"latin-1", "iso-8859-1", "iso-latin-1"} or name.startswith(
        ("latin-1-", "iso-8859-1-", "iso-latin-1-")
    ):
        return "iso-8859-1"
    return original


def _normalize_encoding(name: str) -> str:
    characters: list[str] = []
    punctuation = False
    for character in name:
        if character.isascii() and (character.isalnum() or character == "."):
            if punctuation and characters:
                characters.append("_")
            characters.append(character)
            punctuation = False
        else:
            punctuation = True
    return "".join(characters)


def _is_accepted_utf8_declaration(declaration: str) -> bool:
    key = _normalize_encoding(declaration).lower()
    alias_target = _UTF8_ALIAS_TARGETS.get(key) or _UTF8_ALIAS_TARGETS.get(
        key.replace(".", "_")
    )
    resolved_module = alias_target if alias_target is not None else key
    return resolved_module == "utf_8" and "." not in resolved_module


def _subject_raw_path(subject: Mapping[str, object]) -> bytes:
    semantic_input = subject["semantic_input"]
    if not isinstance(semantic_input, Mapping):
        raise ValueError
    inventory_item = semantic_input["inventory_item"]
    if not isinstance(inventory_item, Mapping):
        raise ValueError
    return _decode_policy_path(inventory_item["git_path"], allow_root=False)
