from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Mapping

from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_SOURCE_OPERATION_PROJECTION_TOKEN = object()
_PROJECTION_DOMAIN = "veritrail.review.private-source-operation-projection/0.1"
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_OPERATION_KINDS = {
    "FACT_DERIVATION",
    "RELATION_DERIVATION",
    "RELATION_OBSERVATION",
}
_DESCRIPTOR_KEYS = {
    "capability_id",
    "provider_id",
    "provider_version",
    "parser_id",
    "parser_version",
    "runtime_id",
    "runtime_version",
}


@dataclass(frozen=True)
class OwnedSourceOperationProjection:
    """Private canonical body-authority projection; never live authority."""

    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    derivation_profile_digest: str
    language_support_function: str
    classification_digest: str
    operation_kind: str
    provider_descriptor_bytes: bytes = field(repr=False)
    fact_set_digest: str | None
    observation_domain_digest: str | None
    assigned_observation_item_ids: tuple[str, ...]
    eligible_subject_ids: tuple[str, ...]
    operation_subject_ids: tuple[str, ...]
    source_operation_projection_digest: str
    projection_document_bytes: bytes = field(repr=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls, document: Mapping[str, object]
    ) -> "OwnedSourceOperationProjection":
        owned = dict(document)
        coordinate = owned.get("operation_coordinate")
        if not isinstance(coordinate, Mapping):
            raise ValueError
        descriptor = coordinate.get("provider_descriptor")
        eligible = owned.get("eligible_subject_ids")
        operation = owned.get("operation_subject_ids")
        assigned = coordinate.get("assigned_observation_item_ids")
        if (
            not isinstance(descriptor, Mapping)
            or not isinstance(eligible, list)
            or not isinstance(operation, list)
            or not isinstance(assigned, list)
        ):
            raise ValueError
        document_bytes = canonical_json_bytes(owned)
        values = {
            "source_snapshot_digest": owned["source_snapshot_digest"],
            "policy_digest": owned["policy_digest"],
            "analysis_scope_digest": owned["analysis_scope_digest"],
            "derivation_profile_digest": owned["derivation_profile_digest"],
            "language_support_function": owned["language_support_function"],
            "classification_digest": owned["classification_digest"],
            "operation_kind": coordinate["operation_kind"],
            "provider_descriptor_bytes": canonical_json_bytes(descriptor),
            "fact_set_digest": coordinate["fact_set_digest"],
            "observation_domain_digest": coordinate["observation_domain_digest"],
            "assigned_observation_item_ids": tuple(assigned),
            "eligible_subject_ids": tuple(eligible),
            "operation_subject_ids": tuple(operation),
            "source_operation_projection_digest": owned[
                "source_operation_projection_digest"
            ],
            "projection_document_bytes": document_bytes,
        }
        value = cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_SOURCE_OPERATION_PROJECTION_TOKEN,
        )
        _validate_source_operation_projection(value)
        return value

    def projection_document_copy(self) -> dict[str, object]:
        _validate_source_operation_projection(self)
        return _object(self.projection_document_bytes)

    def provider_descriptor_copy(self) -> dict[str, str]:
        _validate_source_operation_projection(self)
        descriptor = _object(self.provider_descriptor_bytes)
        return {str(key): str(item) for key, item in descriptor.items()}


def _validate_source_operation_projection(
    value: OwnedSourceOperationProjection,
) -> None:
    if (
        type(value) is not OwnedSourceOperationProjection
        or value._construction_token is not _SOURCE_OPERATION_PROJECTION_TOKEN
    ):
        raise ValueError
    document = _object(value.projection_document_bytes)
    if set(document) != {
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "derivation_profile_digest",
        "language_support_function",
        "classification_digest",
        "operation_coordinate",
        "eligible_subject_ids",
        "operation_subject_ids",
        "source_operation_projection_digest",
    }:
        raise ValueError
    coordinate = document["operation_coordinate"]
    if not isinstance(coordinate, dict) or set(coordinate) != {
        "operation_kind",
        "provider_descriptor",
        "fact_set_digest",
        "observation_domain_digest",
        "assigned_observation_item_ids",
    }:
        raise ValueError
    descriptor = coordinate["provider_descriptor"]
    if (
        not isinstance(descriptor, dict)
        or set(descriptor) != _DESCRIPTOR_KEYS
        or any(not _nonempty_text(item) for item in descriptor.values())
    ):
        raise ValueError
    operation_kind = coordinate["operation_kind"]
    fact_set_digest = coordinate["fact_set_digest"]
    observation_domain_digest = coordinate["observation_domain_digest"]
    assigned = coordinate["assigned_observation_item_ids"]
    if operation_kind not in _OPERATION_KINDS or not _string_list(assigned):
        raise ValueError
    if operation_kind == "FACT_DERIVATION":
        if (
            fact_set_digest is not None
            or observation_domain_digest is not None
            or assigned != []
        ):
            raise ValueError
    elif operation_kind == "RELATION_DERIVATION":
        if (
            not _digest(fact_set_digest)
            or observation_domain_digest is not None
            or assigned != []
        ):
            raise ValueError
    elif not (
        _digest(fact_set_digest)
        and _digest(observation_domain_digest)
        and len(assigned) == len(set(assigned))
    ):
        raise ValueError
    eligible = document["eligible_subject_ids"]
    operation = document["operation_subject_ids"]
    if (
        not _string_list(eligible)
        or not _string_list(operation)
        or len(eligible) != len(set(eligible))
        or len(operation) != len(set(operation))
        or not set(operation).issubset(eligible)
        or any(not _digest(item) for item in (*eligible, *operation))
    ):
        raise ValueError
    for key in (
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "derivation_profile_digest",
        "classification_digest",
        "source_operation_projection_digest",
    ):
        if not _digest(document[key]):
            raise ValueError
    if not _nonempty_text(document["language_support_function"]):
        raise ValueError
    payload = {
        key: item
        for key, item in document.items()
        if key != "source_operation_projection_digest"
    }
    if document["source_operation_projection_digest"] != semantic_digest(
        _PROJECTION_DOMAIN, payload
    ):
        raise ValueError
    values = {
        "source_snapshot_digest": value.source_snapshot_digest,
        "policy_digest": value.policy_digest,
        "analysis_scope_digest": value.analysis_scope_digest,
        "derivation_profile_digest": value.derivation_profile_digest,
        "language_support_function": value.language_support_function,
        "classification_digest": value.classification_digest,
        "operation_kind": value.operation_kind,
        "provider_descriptor_bytes": value.provider_descriptor_bytes,
        "fact_set_digest": value.fact_set_digest,
        "observation_domain_digest": value.observation_domain_digest,
        "assigned_observation_item_ids": value.assigned_observation_item_ids,
        "eligible_subject_ids": value.eligible_subject_ids,
        "operation_subject_ids": value.operation_subject_ids,
        "source_operation_projection_digest": (
            value.source_operation_projection_digest
        ),
        "projection_document_bytes": value.projection_document_bytes,
    }
    if (
        value._state_seal != _private_state_seal(values)
        or canonical_json_bytes(document) != value.projection_document_bytes
        or canonical_json_bytes(descriptor) != value.provider_descriptor_bytes
        or (
            value.source_snapshot_digest,
            value.policy_digest,
            value.analysis_scope_digest,
            value.derivation_profile_digest,
            value.language_support_function,
            value.classification_digest,
            value.operation_kind,
            value.fact_set_digest,
            value.observation_domain_digest,
            value.assigned_observation_item_ids,
            value.eligible_subject_ids,
            value.operation_subject_ids,
            value.source_operation_projection_digest,
        )
        != (
            document["source_snapshot_digest"],
            document["policy_digest"],
            document["analysis_scope_digest"],
            document["derivation_profile_digest"],
            document["language_support_function"],
            document["classification_digest"],
            coordinate["operation_kind"],
            coordinate["fact_set_digest"],
            coordinate["observation_domain_digest"],
            tuple(assigned),
            tuple(eligible),
            tuple(operation),
            document["source_operation_projection_digest"],
        )
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    payload: dict[str, object] = {}
    for key, item in values.items():
        if key.endswith("_bytes"):
            if not isinstance(item, bytes):
                raise ValueError
            payload[f"{key}_sha256"] = hashlib.sha256(item).hexdigest()
        elif isinstance(item, tuple):
            payload[key] = list(item)
        else:
            payload[key] = item
    return semantic_digest(
        "veritrail.review.private-owned-source-operation-projection/0.1",
        payload,
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned source operation projection is not an object")
    return value


def _digest(value: object) -> bool:
    return isinstance(value, str) and _HEX_64.fullmatch(value) is not None


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value) and value == value.strip()


def _string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)
