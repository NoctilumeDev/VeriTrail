from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Mapping

from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_LANGUAGE_SUPPORT_RESULT_TOKEN = object()
_FUNCTION_ID = "r1-python-language-support/0.2"
_REASON_RANK = (
    "UNCLASSIFIED_SOURCE",
    "UNSUPPORTED_ENTRY_KIND",
    "UNSUPPORTED_LANGUAGE",
    "UNSUPPORTED_SOURCE_ENCODING",
)
_ELIGIBLE = "ELIGIBLE"
_UNSUPPORTED = "UNSUPPORTED"


@dataclass(frozen=True)
class OwnedLanguageSupportClassification:
    """Private deterministic classification; no attempt or Parse authority."""

    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    derivation_profile_digest: str
    language_support_function: str
    classification_digest: str
    denominator_count: int
    eligible_count: int
    unsupported_count: int
    classification_document_bytes: bytes = field(repr=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        source_snapshot_digest: str,
        policy_digest: str,
        analysis_scope_digest: str,
        derivation_profile_digest: str,
        classification_document: Mapping[str, object],
    ) -> "OwnedLanguageSupportClassification":
        document = dict(classification_document)
        document_bytes = canonical_json_bytes(document)
        subjects = document.get("subjects")
        if not isinstance(subjects, list):
            raise ValueError
        values = {
            "source_snapshot_digest": source_snapshot_digest,
            "policy_digest": policy_digest,
            "analysis_scope_digest": analysis_scope_digest,
            "derivation_profile_digest": derivation_profile_digest,
            "language_support_function": document["language_support_function"],
            "classification_digest": document["classification_digest"],
            "denominator_count": document["denominator_count"],
            "eligible_count": document["eligible_count"],
            "unsupported_count": document["unsupported_count"],
            "classification_document_bytes": document_bytes,
        }
        value = cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_LANGUAGE_SUPPORT_RESULT_TOKEN,
        )
        _validate_language_support_classification(value)
        return value

    def classification_document_copy(self) -> dict[str, object]:
        _validate_language_support_classification(self)
        return _object(self.classification_document_bytes)

    def subjects_copy(self) -> tuple[dict[str, object], ...]:
        document = self.classification_document_copy()
        subjects = document["subjects"]
        if not isinstance(subjects, list):
            raise RuntimeError("owned Language Support subjects are unavailable")
        return tuple(dict(item) for item in subjects if isinstance(item, dict))


def _validate_language_support_classification(
    value: OwnedLanguageSupportClassification,
) -> None:
    if (
        type(value) is not OwnedLanguageSupportClassification
        or value._construction_token is not _LANGUAGE_SUPPORT_RESULT_TOKEN
    ):
        raise ValueError
    document = _object(value.classification_document_bytes)
    if set(document) != {
        "language_support_function",
        "subjects",
        "denominator_count",
        "eligible_count",
        "unsupported_count",
        "classification_digest",
    }:
        raise ValueError
    subjects = document["subjects"]
    if not isinstance(subjects, list):
        raise ValueError
    path_order: list[bytes] = []
    identities: list[str] = []
    eligible = 0
    unsupported = 0
    for subject in subjects:
        if not isinstance(subject, dict) or set(subject) != {
            "subject_identity",
            "semantic_input",
            "disposition",
            "reason_codes",
            "effective_source_encoding",
        }:
            raise ValueError
        semantic_input = subject["semantic_input"]
        if not isinstance(semantic_input, dict) or set(semantic_input) != {
            "language_support_function",
            "inventory_item",
            "scope_semantics",
            "profile_support_semantics",
        }:
            raise ValueError
        scope_semantics = semantic_input["scope_semantics"]
        profile_semantics = semantic_input["profile_support_semantics"]
        supported_entry_kinds = (
            profile_semantics.get("supported_entry_kinds")
            if isinstance(profile_semantics, dict)
            else None
        )
        if (
            semantic_input["language_support_function"] != _FUNCTION_ID
            or not isinstance(scope_semantics, dict)
            or set(scope_semantics) != {"disposition", "source_class"}
            or scope_semantics["disposition"] != "IN_SCOPE"
            or scope_semantics["source_class"]
            not in {"FIRST_PARTY", "GENERATED", "VENDORED", "UNCLASSIFIED"}
            or not isinstance(profile_semantics, dict)
            or set(profile_semantics)
            != {
                "language",
                "language_semantics",
                "supported_entry_kinds",
                "accepted_source_encodings",
                "normalization_rules.path",
            }
            or profile_semantics["language"] != "PYTHON"
            or profile_semantics["language_semantics"] != "PYTHON_3_10"
            or not isinstance(supported_entry_kinds, list)
            or any(not isinstance(item, str) for item in supported_entry_kinds)
            or len(supported_entry_kinds) != len(set(supported_entry_kinds))
            or profile_semantics["accepted_source_encodings"]
            != ["UTF-8", "UTF-8-SIG"]
            or not isinstance(profile_semantics["normalization_rules.path"], str)
        ):
            raise ValueError
        inventory_item = semantic_input["inventory_item"]
        if not isinstance(inventory_item, dict):
            raise ValueError
        path = inventory_item.get("git_path")
        if not isinstance(path, dict) or set(path) != {"path_kind", "git_path_hex"}:
            raise ValueError
        path_hex = path.get("git_path_hex")
        if path.get("path_kind") != "GIT_PATH" or not isinstance(path_hex, str):
            raise ValueError
        try:
            raw_path = bytes.fromhex(path_hex)
        except ValueError as exc:
            raise ValueError from exc
        path_order.append(raw_path)
        identity = subject["subject_identity"]
        if (
            not isinstance(identity, str)
            or identity
            != semantic_digest(
                "veritrail.review.language-support-subject/0.2",
                semantic_input,
            )
        ):
            raise ValueError
        identities.append(identity)
        reasons = subject["reason_codes"]
        if (
            not isinstance(reasons, list)
            or any(reason not in _REASON_RANK for reason in reasons)
            or reasons != [reason for reason in _REASON_RANK if reason in reasons]
            or len(reasons) != len(set(reasons))
        ):
            raise ValueError
        disposition = subject["disposition"]
        encoding = subject["effective_source_encoding"]
        if disposition == _ELIGIBLE:
            if reasons or encoding not in {"UTF-8", "UTF-8-SIG"}:
                raise ValueError
            eligible += 1
        elif disposition == _UNSUPPORTED:
            if not reasons or encoding is not None:
                raise ValueError
            unsupported += 1
        else:
            raise ValueError
    if (
        path_order != sorted(path_order)
        or len(path_order) != len(set(path_order))
        or len(identities) != len(set(identities))
        or document["language_support_function"] != _FUNCTION_ID
        or type(document["denominator_count"]) is not int
        or type(document["eligible_count"]) is not int
        or type(document["unsupported_count"]) is not int
        or document["denominator_count"] != len(subjects)
        or document["eligible_count"] != eligible
        or document["unsupported_count"] != unsupported
        or eligible + unsupported != len(subjects)
    ):
        raise ValueError
    payload = {
        key: item
        for key, item in document.items()
        if key != "classification_digest"
    }
    if document["classification_digest"] != semantic_digest(
        "veritrail.review.private-language-support-classification/0.2",
        payload,
    ):
        raise ValueError
    values = {
        "source_snapshot_digest": value.source_snapshot_digest,
        "policy_digest": value.policy_digest,
        "analysis_scope_digest": value.analysis_scope_digest,
        "derivation_profile_digest": value.derivation_profile_digest,
        "language_support_function": value.language_support_function,
        "classification_digest": value.classification_digest,
        "denominator_count": value.denominator_count,
        "eligible_count": value.eligible_count,
        "unsupported_count": value.unsupported_count,
        "classification_document_bytes": value.classification_document_bytes,
    }
    if (
        value._state_seal != _private_state_seal(values)
        or canonical_json_bytes(document) != value.classification_document_bytes
        or (
            value.language_support_function,
            value.classification_digest,
            value.denominator_count,
            value.eligible_count,
            value.unsupported_count,
        )
        != (
            document["language_support_function"],
            document["classification_digest"],
            document["denominator_count"],
            document["eligible_count"],
            document["unsupported_count"],
        )
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    raw = values.get("classification_document_bytes")
    if not isinstance(raw, bytes):
        raise ValueError
    payload = {
        key: item
        for key, item in values.items()
        if key != "classification_document_bytes"
    }
    payload["classification_document_sha256"] = hashlib.sha256(raw).hexdigest()
    return semantic_digest(
        "veritrail.review.private-owned-language-support-classification/0.2",
        payload,
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned Language Support classification is not an object")
    return value
