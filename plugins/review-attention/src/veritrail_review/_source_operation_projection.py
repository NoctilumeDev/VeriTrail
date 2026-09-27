from __future__ import annotations

import copy
from typing import Mapping

from veritrail_review._execution_cell_binding import ProviderDescriptor
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
    _validate_language_support_classification,
)
from veritrail_review._relation_execution_cell_application import (
    _validate_fact_set_projection,
    fact_set_semantic_projection,
)
from veritrail_review._source_operation_projection_values import (
    OwnedSourceOperationProjection,
    _PROJECTION_DOMAIN,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_FACT_SET_KEYS = {
    "artifact_kind",
    "schema_version",
    "canonicalization_profile",
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "derivation_profile_digest",
    "facts",
    "conflicts",
    "fact_set_digest",
}
_FACT_KEYS = {
    "source_snapshot_digest",
    "derivation_profile_digest",
    "fact_id",
    "subject_key_digest",
    "subject_space",
    "fact_kind",
    "source_anchor",
    "local_ordinal",
    "semantic_attributes",
    "provenance_refs",
}
_DOMAIN_KEYS = {
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "derivation_profile_digest",
    "fact_set_digest",
    "observation_profile_id",
    "observation_profile_version",
    "observation_profile_digest",
    "capability_id",
    "required",
    "composition_mode",
    "observation_items",
    "provider_responsibilities",
    "observation_domain_digest",
}
_OBSERVATION_ITEM_KEYS = {
    "observation_item_id",
    "source_snapshot_digest",
    "derivation_profile_digest",
    "fact_set_digest",
    "relation_kind",
    "subject_role",
    "subject_fact_id",
}
_RESPONSIBILITY_KEYS = {
    "provider_descriptor",
    "required",
    "assigned_observation_item_ids",
}


def build_fact_derivation_source_operation_projection(
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
) -> OwnedSourceOperationProjection:
    """Project the exact eligible upper bound for one Fact Provider."""

    index = _classification_index(classification)
    return _build_projection(
        classification=classification,
        descriptor=descriptor,
        operation_kind="FACT_DERIVATION",
        fact_set_digest=None,
        observation_domain_digest=None,
        assigned_observation_item_ids=(),
        eligible_subject_ids=index["eligible_subject_ids"],
        operation_subject_ids=index["eligible_subject_ids"],
    )


def build_relation_derivation_source_operation_projection(
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
    fact_set_document: Mapping[str, object],
) -> OwnedSourceOperationProjection:
    """Project only eligible sources referenced by the exact FactSet."""

    index = _classification_index(classification)
    fact_set, facts_by_id = _validated_fact_set(
        classification, index, fact_set_document
    )
    referenced_paths = {
        _fact_path_hex(fact) for fact in facts_by_id.values()
    }
    operation = _subjects_for_paths(index, referenced_paths)
    return _build_projection(
        classification=classification,
        descriptor=descriptor,
        operation_kind="RELATION_DERIVATION",
        fact_set_digest=fact_set["fact_set_digest"],
        observation_domain_digest=None,
        assigned_observation_item_ids=(),
        eligible_subject_ids=index["eligible_subject_ids"],
        operation_subject_ids=operation,
    )


def build_relation_observation_source_operation_projection(
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
    fact_set_document: Mapping[str, object],
    observation_domain: Mapping[str, object],
) -> OwnedSourceOperationProjection:
    """Project sources required by one Provider's exact domain assignment."""

    index = _classification_index(classification)
    fact_set, facts_by_id = _validated_fact_set(
        classification, index, fact_set_document
    )
    domain, assigned_ids, subject_fact_ids = _validated_observation_assignment(
        classification,
        descriptor,
        fact_set,
        facts_by_id,
        observation_domain,
    )
    referenced_paths = {
        _fact_path_hex(facts_by_id[fact_id]) for fact_id in subject_fact_ids
    }
    operation = _subjects_for_paths(index, referenced_paths)
    return _build_projection(
        classification=classification,
        descriptor=descriptor,
        operation_kind="RELATION_OBSERVATION",
        fact_set_digest=fact_set["fact_set_digest"],
        observation_domain_digest=domain["observation_domain_digest"],
        assigned_observation_item_ids=assigned_ids,
        eligible_subject_ids=index["eligible_subject_ids"],
        operation_subject_ids=operation,
    )


def _classification_index(
    classification: OwnedLanguageSupportClassification,
) -> dict[str, object]:
    _validate_language_support_classification(classification)
    ordered_paths: list[str] = []
    eligible_ids: list[str] = []
    identity_by_path: dict[str, str] = {}
    sizes: dict[str, int] = {}
    denominator_paths: set[str] = set()
    eligible_paths: set[str] = set()
    for subject in classification.subjects_copy():
        semantic_input = subject["semantic_input"]
        if not isinstance(semantic_input, Mapping):
            raise ValueError
        inventory = semantic_input["inventory_item"]
        if not isinstance(inventory, Mapping):
            raise ValueError
        git_path = inventory["git_path"]
        content = inventory.get("content")
        if not isinstance(git_path, Mapping):
            raise ValueError
        path_hex = git_path["git_path_hex"]
        identity = subject["subject_identity"]
        if not isinstance(path_hex, str) or not isinstance(identity, str):
            raise ValueError
        ordered_paths.append(path_hex)
        denominator_paths.add(path_hex)
        if subject["disposition"] == "ELIGIBLE":
            if (
                not isinstance(content, Mapping)
                or type(content.get("size_bytes")) is not int
            ):
                raise ValueError
            eligible_paths.add(path_hex)
            eligible_ids.append(identity)
            identity_by_path[path_hex] = identity
            sizes[path_hex] = content["size_bytes"]
    return {
        "ordered_paths": tuple(ordered_paths),
        "eligible_subject_ids": tuple(eligible_ids),
        "identity_by_path": identity_by_path,
        "source_sizes_by_path_hex": sizes,
        "denominator_paths": frozenset(denominator_paths),
        "eligible_paths": frozenset(eligible_paths),
    }


def _validated_fact_set(
    classification: OwnedLanguageSupportClassification,
    index: Mapping[str, object],
    fact_set_document: Mapping[str, object],
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    try:
        document = copy.deepcopy(dict(fact_set_document))
        if (
            set(document) != _FACT_SET_KEYS
            or document["artifact_kind"] != "FACT_SET"
            or document["schema_version"] != "0.1"
            or document["canonicalization_profile"] != "veritrail-json-c14n/1"
            or document["source_snapshot_digest"]
            != classification.source_snapshot_digest
            or document["policy_digest"] != classification.policy_digest
            or document["analysis_scope_digest"]
            != classification.analysis_scope_digest
            or document["derivation_profile_digest"]
            != classification.derivation_profile_digest
        ):
            raise ValueError
        facts = document["facts"]
        if not isinstance(facts, list):
            raise ValueError
        for fact in facts:
            if not isinstance(fact, Mapping) or set(fact) != _FACT_KEYS:
                raise ValueError
            refs = fact["provenance_refs"]
            if (
                not isinstance(refs, list)
                or not refs
                or any(not isinstance(item, str) or not item for item in refs)
                or refs != sorted(set(refs))
            ):
                raise ValueError
        projection = fact_set_semantic_projection(document)
        facts_by_id = _validate_fact_set_projection(
            projection,
            fact_set_digest=document["fact_set_digest"],
            expected_digests={
                "source_snapshot_digest": classification.source_snapshot_digest,
                "analysis_scope_digest": classification.analysis_scope_digest,
                "derivation_profile_digest": classification.derivation_profile_digest,
            },
            source_sizes_by_path_hex=index["source_sizes_by_path_hex"],
            in_scope_paths=index["denominator_paths"],
            supported_paths=index["eligible_paths"],
        )
        return document, facts_by_id
    except Exception as exc:
        raise ValueError(
            "invalid exact FactSet for source operation projection"
        ) from exc


def _validated_observation_assignment(
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
    fact_set: Mapping[str, object],
    facts_by_id: Mapping[str, Mapping[str, object]],
    observation_domain: Mapping[str, object],
) -> tuple[dict[str, object], tuple[str, ...], tuple[str, ...]]:
    try:
        _descriptor_document(descriptor)
        domain = copy.deepcopy(dict(observation_domain))
        if (
            set(domain) != _DOMAIN_KEYS
            or domain["source_snapshot_digest"]
            != classification.source_snapshot_digest
            or domain["policy_digest"] != classification.policy_digest
            or domain["analysis_scope_digest"]
            != classification.analysis_scope_digest
            or domain["derivation_profile_digest"]
            != classification.derivation_profile_digest
            or domain["fact_set_digest"] != fact_set["fact_set_digest"]
        ):
            raise ValueError
        payload = {
            key: copy.deepcopy(item)
            for key, item in domain.items()
            if key not in {"policy_digest", "observation_domain_digest"}
        }
        if domain["observation_domain_digest"] != semantic_digest(
            "veritrail.review.relation-observation-domain/0.1", payload
        ):
            raise ValueError
        items = domain["observation_items"]
        responsibilities = domain["provider_responsibilities"]
        if not isinstance(items, list) or not isinstance(responsibilities, list):
            raise ValueError
        item_by_id: dict[str, dict[str, object]] = {}
        for item in items:
            if not isinstance(item, dict) or set(item) != _OBSERVATION_ITEM_KEYS:
                raise ValueError
            item_id = item["observation_item_id"]
            unsigned = {
                key: copy.deepcopy(value)
                for key, value in item.items()
                if key != "observation_item_id"
            }
            if (
                not isinstance(item_id, str)
                or item_id in item_by_id
                or item_id
                != semantic_digest(
                    "veritrail.review.relation-observation-item/0.1", unsigned
                )
                or item["source_snapshot_digest"]
                != classification.source_snapshot_digest
                or item["derivation_profile_digest"]
                != classification.derivation_profile_digest
                or item["fact_set_digest"] != fact_set["fact_set_digest"]
                or item["subject_fact_id"] not in facts_by_id
            ):
                raise ValueError
            item_by_id[item_id] = item
        target = _descriptor_document(descriptor)
        matches: list[dict[str, object]] = []
        seen_descriptors: set[bytes] = set()
        for responsibility in responsibilities:
            if (
                not isinstance(responsibility, dict)
                or set(responsibility) != _RESPONSIBILITY_KEYS
                or responsibility["required"] is not True
                or not isinstance(responsibility["provider_descriptor"], dict)
            ):
                raise ValueError
            descriptor_bytes = canonical_json_bytes(
                responsibility["provider_descriptor"]
            )
            if descriptor_bytes in seen_descriptors:
                raise ValueError
            seen_descriptors.add(descriptor_bytes)
            assigned = responsibility["assigned_observation_item_ids"]
            if (
                not isinstance(assigned, list)
                or any(not isinstance(item, str) for item in assigned)
                or assigned != sorted(set(assigned))
                or any(item not in item_by_id for item in assigned)
            ):
                raise ValueError
            if responsibility["provider_descriptor"] == target:
                matches.append(responsibility)
        if len(matches) != 1:
            raise ValueError
        assigned_ids = tuple(matches[0]["assigned_observation_item_ids"])
        subject_fact_ids = tuple(
            item_by_id[item_id]["subject_fact_id"] for item_id in assigned_ids
        )
        return domain, assigned_ids, subject_fact_ids  # type: ignore[return-value]
    except Exception as exc:
        raise ValueError(
            "invalid exact observation assignment for source operation projection"
        ) from exc


def _subjects_for_paths(
    index: Mapping[str, object], referenced_paths: set[str]
) -> tuple[str, ...]:
    eligible_paths = index["eligible_paths"]
    if not isinstance(eligible_paths, frozenset) or not referenced_paths.issubset(
        eligible_paths
    ):
        raise ValueError("operation source path is not Language Support eligible")
    ordered_paths = index["ordered_paths"]
    identity_by_path = index["identity_by_path"]
    if not isinstance(ordered_paths, tuple) or not isinstance(identity_by_path, dict):
        raise ValueError
    return tuple(
        identity_by_path[path]
        for path in ordered_paths
        if path in referenced_paths
    )


def _build_projection(
    *,
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
    operation_kind: str,
    fact_set_digest: object,
    observation_domain_digest: object,
    assigned_observation_item_ids: tuple[str, ...],
    eligible_subject_ids: object,
    operation_subject_ids: tuple[str, ...] | object,
) -> OwnedSourceOperationProjection:
    descriptor_document = _descriptor_document(descriptor)
    payload: dict[str, object] = {
        "source_snapshot_digest": classification.source_snapshot_digest,
        "policy_digest": classification.policy_digest,
        "analysis_scope_digest": classification.analysis_scope_digest,
        "derivation_profile_digest": classification.derivation_profile_digest,
        "language_support_function": classification.language_support_function,
        "classification_digest": classification.classification_digest,
        "operation_coordinate": {
            "operation_kind": operation_kind,
            "provider_descriptor": descriptor_document,
            "fact_set_digest": fact_set_digest,
            "observation_domain_digest": observation_domain_digest,
            "assigned_observation_item_ids": list(assigned_observation_item_ids),
        },
        "eligible_subject_ids": list(eligible_subject_ids),
        "operation_subject_ids": list(operation_subject_ids),
    }
    payload["source_operation_projection_digest"] = semantic_digest(
        _PROJECTION_DOMAIN, payload
    )
    return OwnedSourceOperationProjection._create(payload)


def _descriptor_document(descriptor: ProviderDescriptor) -> dict[str, str]:
    if type(descriptor) is not ProviderDescriptor:
        raise ValueError("invalid Provider descriptor")
    document = descriptor.document()
    if any(
        not isinstance(item, str) or not item or item != item.strip()
        for item in document.values()
    ):
        raise ValueError("invalid Provider descriptor")
    return document


def _fact_path_hex(fact: Mapping[str, object]) -> str:
    anchor = fact["source_anchor"]
    if not isinstance(anchor, Mapping):
        raise ValueError
    path = anchor["git_path"]
    if not isinstance(path, Mapping) or not isinstance(path["git_path_hex"], str):
        raise ValueError
    return path["git_path_hex"]
