from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Mapping, Sequence

from veritrail_review._execution_cell_application import provider_run_id
from veritrail_review._execution_cell_binding import ProviderDescriptor
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
)
from veritrail_review._relation_execution_cell_application import (
    _descriptor_from_document,
    _validate_fact_set_projection,
    _validate_relation_requirement,
    fact_set_semantic_projection,
)
from veritrail_review._relation_observation_application import (
    RelationObservationApplicationError as HistoricalObservationProtocolError,
    canonicalize_provider_observation_outcomes as _canonicalize_outcomes,
    canonicalize_relation_observation_candidates as _canonicalize_candidates,
    relation_observation_terminal_document as _historical_terminal_document,
    validate_relation_observation_terminal_document as _validate_historical_terminal,
)
from veritrail_review._relation_observation_binding import (
    closed_test_relation_observation_bindings,
    relation_observation_descriptor_for_launch_key,
)
from veritrail_review._relation_observation_domain import (
    responsibility_for_descriptor,
    validate_declared_relation_observation_domain,
)
from veritrail_review._source_operation_fact_application import (
    _expected_digests,
    _owned_operation_source_blobs,
    _require_input_digests,
    _validate_classification_metadata,
    _validate_frozen_documents,
    _validate_operation_source_blobs,
    _validate_request_provenance,
)
from veritrail_review._source_operation_projection import (
    build_relation_observation_source_operation_projection,
)
from veritrail_review._source_operation_projection_values import (
    OwnedSourceOperationProjection,
    _validate_source_operation_projection,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


PROTOCOL = "veritrail-review-relation-cell/0.4"
REQUEST_KIND = "RELATION_OBSERVATION_CELL_REQUEST"
TERMINAL_KIND = "RELATION_OBSERVATION_CELL_TERMINAL"
OPERANDS_DOMAIN = "veritrail.review.provider-operands/0.6"

_REQUEST_KEYS = frozenset(
    {
        "protocol",
        "message_kind",
        "derivation_id",
        "request_provenance",
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "provider_descriptor",
        "fact_set_digest",
        "observation_domain_digest",
        "assigned_observation_item_ids",
        "operands_digest",
        "source_snapshot",
        "review_policy",
        "derivation_profile",
        "fact_set",
        "observation_domain",
        "language_support_classification",
        "source_operation_projection",
        "source_blobs",
    }
)
_TERMINAL_KEYS = frozenset(
    {
        "protocol",
        "message_kind",
        "derivation_id",
        "provider_descriptor",
        "fact_set_digest",
        "observation_domain_digest",
        "assigned_observation_item_ids",
        "operands_digest",
        "provider_run_id",
        "terminal_kind",
        "canonical_relations",
        "observation_outcomes",
        "reported_fact_ids",
        "reported_relation_ids",
    }
)


class RelationObservationSourceOperationProtocolError(ValueError):
    """The private corrected Relation observation wire failed validation."""


@dataclass(frozen=True)
class ValidatedRelationObservationSourceOperationRequest:
    document: dict[str, object]
    descriptor: ProviderDescriptor
    provider_run_id: str
    facts_by_id: dict[str, dict[str, object]]
    observation_items_by_id: dict[str, dict[str, object]]
    source_blobs_by_path_hex: dict[str, bytes]


def copy_relation_observation_source_operation_request_for_provider(
    request: ValidatedRelationObservationSourceOperationRequest,
) -> ValidatedRelationObservationSourceOperationRequest:
    """Give Provider code an owned view containing only operation source paths."""

    operation_paths = frozenset(request.source_blobs_by_path_hex)
    provider_facts = {
        fact_id: copy.deepcopy(fact)
        for fact_id, fact in request.facts_by_id.items()
        if fact["source_anchor"]["git_path"]["git_path_hex"] in operation_paths
    }
    return ValidatedRelationObservationSourceOperationRequest(
        document=copy.deepcopy(request.document),
        descriptor=ProviderDescriptor(**request.descriptor.document()),
        provider_run_id=str(request.provider_run_id),
        facts_by_id=provider_facts,
        observation_items_by_id=copy.deepcopy(request.observation_items_by_id),
        source_blobs_by_path_hex={
            str(path_hex): memoryview(raw).tobytes()
            for path_hex, raw in request.source_blobs_by_path_hex.items()
        },
    )


def relation_observation_source_operation_operands_digest(
    inputs: DerivationInputSet,
    descriptor: ProviderDescriptor,
    fact_set_digest: str,
    observation_domain_digest: str,
    assigned_observation_item_ids: Sequence[str],
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> str:
    """Bind the historical observation operands plus exact gate semantics."""

    return _operands_digest_from_parts(
        source_snapshot_digest=inputs.source_snapshot_digest,
        policy_digest=inputs.policy_digest,
        analysis_scope_digest=inputs.analysis_scope_digest,
        slice_policy_digest=inputs.slice_policy_digest,
        derivation_profile_digest=inputs.derivation_profile_digest,
        descriptor=descriptor,
        fact_set_digest=fact_set_digest,
        observation_domain_digest=observation_domain_digest,
        assigned_observation_item_ids=assigned_observation_item_ids,
        language_support_function=classification.language_support_function,
        classification_digest=classification.classification_digest,
        source_operation_projection_digest=(
            projection.source_operation_projection_digest
        ),
    )


def build_relation_observation_source_operation_request_document(
    *,
    inputs: DerivationInputSet,
    derivation_id: str,
    request_provenance: Mapping[str, object],
    descriptor: ProviderDescriptor,
    fact_set_document: Mapping[str, object],
    observation_domain: Mapping[str, object],
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> dict[str, object]:
    """Build corrected observation input without integrating a controller."""

    snapshot = inputs.source_snapshot_document_copy()
    policy = inputs.review_policy_document_copy()
    profile = inputs.derivation_profile_document_copy()
    _validate_frozen_documents(snapshot, policy, profile)
    _validate_relation_requirement(policy)
    expected_digests = _expected_digests(snapshot, policy, profile)
    _require_input_digests(inputs, expected_digests)
    _validate_classification_metadata(
        classification, snapshot=snapshot, policy=policy, profile=profile
    )
    owned_fact_set = copy.deepcopy(dict(fact_set_document))
    validated_domain = validate_declared_relation_observation_domain(
        observation_domain,
        inputs=inputs,
        fact_set_document=owned_fact_set,
        relation_bindings=closed_test_relation_observation_bindings(),
    )
    responsibility = responsibility_for_descriptor(validated_domain, descriptor)
    assigned = responsibility["assigned_observation_item_ids"]
    expected_projection = build_relation_observation_source_operation_projection(
        classification,
        descriptor,
        owned_fact_set,
        validated_domain,
    )
    if (
        projection.projection_document_copy()
        != expected_projection.projection_document_copy()
    ):
        raise RelationObservationSourceOperationProtocolError(
            "Relation observation source operation projection mismatch"
        )
    fact_set = fact_set_semantic_projection(owned_fact_set)
    fact_set_digest = owned_fact_set.get("fact_set_digest")
    domain_digest = validated_domain["observation_domain_digest"]
    if not isinstance(fact_set_digest, str) or not isinstance(domain_digest, str):
        raise RelationObservationSourceOperationProtocolError(
            "invalid observation semantic digest"
        )
    source_blobs, _, _ = _owned_operation_source_blobs(
        inputs, classification, projection
    )
    operands_digest = relation_observation_source_operation_operands_digest(
        inputs,
        descriptor,
        fact_set_digest,
        domain_digest,
        assigned,
        classification,
        projection,
    )
    return {
        "protocol": PROTOCOL,
        "message_kind": REQUEST_KIND,
        "derivation_id": derivation_id,
        "request_provenance": copy.deepcopy(dict(request_provenance)),
        **expected_digests,
        "provider_descriptor": descriptor.document(),
        "fact_set_digest": fact_set_digest,
        "observation_domain_digest": domain_digest,
        "assigned_observation_item_ids": copy.deepcopy(assigned),
        "operands_digest": operands_digest,
        "source_snapshot": snapshot,
        "review_policy": policy,
        "derivation_profile": profile,
        "fact_set": fact_set,
        "observation_domain": validated_domain,
        "language_support_classification": (
            classification.classification_document_copy()
        ),
        "source_operation_projection": projection.projection_document_copy(),
        "source_blobs": source_blobs,
    }


def validate_relation_observation_source_operation_request_document(
    document: Mapping[str, object], *, launch_key: str
) -> ValidatedRelationObservationSourceOperationRequest:
    """Validate the 0.4 request without reacquiring omitted bodies."""

    try:
        if set(document) != _REQUEST_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != REQUEST_KIND:
            raise ValueError
        derivation_id = document["derivation_id"]
        if not isinstance(derivation_id, str) or not derivation_id:
            raise ValueError
        descriptor = _descriptor_from_document(document["provider_descriptor"])
        expected_descriptor = relation_observation_descriptor_for_launch_key(
            launch_key
        )
        if expected_descriptor is None or descriptor != expected_descriptor:
            raise ValueError
        snapshot = document["source_snapshot"]
        policy = document["review_policy"]
        profile = document["derivation_profile"]
        classification_document = document["language_support_classification"]
        projection_document = document["source_operation_projection"]
        fact_set = document["fact_set"]
        if not all(
            isinstance(value, Mapping)
            for value in (
                snapshot,
                policy,
                profile,
                classification_document,
                projection_document,
                fact_set,
            )
        ):
            raise ValueError
        _validate_frozen_documents(snapshot, policy, profile)
        _validate_relation_requirement(policy)
        expected_digests = _expected_digests(snapshot, policy, profile)
        for key, expected_digest in expected_digests.items():
            if document[key] != expected_digest:
                raise ValueError
        classification = OwnedLanguageSupportClassification._create(
            source_snapshot_digest=expected_digests["source_snapshot_digest"],
            policy_digest=expected_digests["policy_digest"],
            analysis_scope_digest=expected_digests["analysis_scope_digest"],
            derivation_profile_digest=expected_digests[
                "derivation_profile_digest"
            ],
            classification_document=classification_document,
        )
        _validate_classification_metadata(
            classification, snapshot=snapshot, policy=policy, profile=profile
        )
        projection = OwnedSourceOperationProjection._create(projection_document)
        index = _classification_index(classification)
        facts_by_id = _validate_fact_set_projection(
            fact_set,
            fact_set_digest=document["fact_set_digest"],
            expected_digests=expected_digests,
            source_sizes_by_path_hex=index["source_sizes_by_path_hex"],
            in_scope_paths=index["denominator_paths"],
            supported_paths=index["eligible_paths"],
        )
        semantic_fact_set = _fact_set_with_empty_provenance(document, fact_set)
        ephemeral_inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=canonical_json_bytes(snapshot) + b"\n",
            review_policy_canonical_bytes=canonical_json_bytes(policy) + b"\n",
            derivation_profile_canonical_bytes=canonical_json_bytes(profile) + b"\n",
            verified_blob_bytes_by_object_identity={},
            **expected_digests,
        )
        domain = validate_declared_relation_observation_domain(
            document["observation_domain"],
            inputs=ephemeral_inputs,
            fact_set_document=semantic_fact_set,
            relation_bindings=closed_test_relation_observation_bindings(),
        )
        responsibility = responsibility_for_descriptor(domain, descriptor)
        assigned = responsibility["assigned_observation_item_ids"]
        if (
            document["observation_domain_digest"]
            != domain["observation_domain_digest"]
            or document["assigned_observation_item_ids"] != assigned
            or assigned != sorted(set(assigned))
        ):
            raise ValueError
        _validate_observation_projection(
            projection,
            classification=classification,
            descriptor=descriptor,
            fact_set_digest=document["fact_set_digest"],
            domain=domain,
            assigned=assigned,
            facts_by_id=facts_by_id,
            expected_digests=expected_digests,
            index=index,
        )
        _, source_blobs = _validate_operation_source_blobs(
            document["source_blobs"], classification, projection
        )
        expected_operands = _operands_digest_from_parts(
            **expected_digests,
            descriptor=descriptor,
            fact_set_digest=document["fact_set_digest"],
            observation_domain_digest=domain["observation_domain_digest"],
            assigned_observation_item_ids=assigned,
            language_support_function=classification.language_support_function,
            classification_digest=classification.classification_digest,
            source_operation_projection_digest=(
                projection.source_operation_projection_digest
            ),
        )
        if document["operands_digest"] != expected_operands:
            raise ValueError
        _validate_request_provenance(document["request_provenance"], snapshot)
        run_id = provider_run_id(derivation_id, descriptor, expected_operands)
        items = {
            item["observation_item_id"]: copy.deepcopy(item)
            for item in domain["observation_items"]
        }
        return ValidatedRelationObservationSourceOperationRequest(
            document=copy.deepcopy(dict(document)),
            descriptor=descriptor,
            provider_run_id=run_id,
            facts_by_id=copy.deepcopy(facts_by_id),
            observation_items_by_id=items,
            source_blobs_by_path_hex=source_blobs,
        )
    except Exception as exc:
        if isinstance(exc, RelationObservationSourceOperationProtocolError):
            raise
        raise RelationObservationSourceOperationProtocolError(
            "nonconformant corrected Relation observation request envelope"
        ) from exc


def canonicalize_relation_observation_source_operation_candidates(
    request: ValidatedRelationObservationSourceOperationRequest,
    candidates: object,
) -> list[dict[str, object]]:
    try:
        return _canonicalize_candidates(request, candidates)  # type: ignore[arg-type]
    except HistoricalObservationProtocolError as exc:
        raise RelationObservationSourceOperationProtocolError(
            "nonconformant Relation observation candidates"
        ) from exc


def canonicalize_relation_observation_source_operation_outcomes(
    request: ValidatedRelationObservationSourceOperationRequest,
    outcomes: object,
) -> list[dict[str, object]]:
    try:
        return _canonicalize_outcomes(request, outcomes)  # type: ignore[arg-type]
    except HistoricalObservationProtocolError as exc:
        raise RelationObservationSourceOperationProtocolError(
            "nonconformant Relation observation outcomes"
        ) from exc


def relation_observation_source_operation_terminal_document(
    request: ValidatedRelationObservationSourceOperationRequest,
    *,
    terminal_kind: str,
    canonical_relations: list[dict[str, object]] | None = None,
    observation_outcomes: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    try:
        document = _historical_terminal_document(
            request,  # type: ignore[arg-type]
            terminal_kind=terminal_kind,
            canonical_relations=canonical_relations,
            observation_outcomes=observation_outcomes,
        )
    except HistoricalObservationProtocolError as exc:
        raise RelationObservationSourceOperationProtocolError(
            "invalid corrected Relation observation terminal"
        ) from exc
    document["protocol"] = PROTOCOL
    return document


def validate_relation_observation_source_operation_terminal_document(
    document: Mapping[str, object], *, request: Mapping[str, object]
) -> dict[str, object]:
    try:
        if set(document) != _TERMINAL_KEYS:
            raise ValueError
        if (
            document["protocol"] != PROTOCOL
            or document["message_kind"] != TERMINAL_KIND
        ):
            raise ValueError
        historical = copy.deepcopy(dict(document))
        historical["protocol"] = "veritrail-review-relation-cell/0.2"
        _validate_historical_terminal(historical, request=request)
        return copy.deepcopy(dict(document))
    except Exception as exc:
        raise RelationObservationSourceOperationProtocolError(
            "nonconformant corrected Relation observation terminal envelope"
        ) from exc


def _operands_digest_from_parts(
    *,
    source_snapshot_digest: str,
    policy_digest: str,
    analysis_scope_digest: str,
    slice_policy_digest: str,
    derivation_profile_digest: str,
    descriptor: ProviderDescriptor,
    fact_set_digest: str,
    observation_domain_digest: str,
    assigned_observation_item_ids: Sequence[str],
    language_support_function: str,
    classification_digest: str,
    source_operation_projection_digest: str,
) -> str:
    return semantic_digest(
        OPERANDS_DOMAIN,
        {
            "source_snapshot_digest": source_snapshot_digest,
            "policy_digest": policy_digest,
            "analysis_scope_digest": analysis_scope_digest,
            "slice_policy_digest": slice_policy_digest,
            "derivation_profile_digest": derivation_profile_digest,
            **descriptor.document(),
            "fact_set_digest": fact_set_digest,
            "observation_domain_digest": observation_domain_digest,
            "assigned_observation_item_ids": list(
                assigned_observation_item_ids
            ),
            "language_support_function": language_support_function,
            "classification_digest": classification_digest,
            "source_operation_projection_digest": (
                source_operation_projection_digest
            ),
        },
    )


def _classification_index(
    classification: OwnedLanguageSupportClassification,
) -> dict[str, object]:
    eligible_ids: list[str] = []
    eligible_paths: set[str] = set()
    denominator_paths: set[str] = set()
    identity_by_path: dict[str, str] = {}
    source_sizes: dict[str, int] = {}
    ordered_paths: list[str] = []
    for subject in classification.subjects_copy():
        inventory = subject["semantic_input"]["inventory_item"]
        path_hex = inventory["git_path"]["git_path_hex"]
        identity = subject["subject_identity"]
        if (
            not isinstance(path_hex, str)
            or not isinstance(identity, str)
            or path_hex in denominator_paths
        ):
            raise ValueError
        denominator_paths.add(path_hex)
        ordered_paths.append(path_hex)
        if subject["disposition"] == "ELIGIBLE":
            size = inventory["content"]["size_bytes"]
            if type(size) is not int:
                raise ValueError
            eligible_ids.append(identity)
            eligible_paths.add(path_hex)
            identity_by_path[path_hex] = identity
            source_sizes[path_hex] = size
    if ordered_paths != sorted(ordered_paths, key=bytes.fromhex):
        raise ValueError
    return {
        "eligible_subject_ids": tuple(eligible_ids),
        "eligible_paths": frozenset(eligible_paths),
        "denominator_paths": frozenset(denominator_paths),
        "identity_by_path": identity_by_path,
        "source_sizes_by_path_hex": source_sizes,
        "ordered_paths": tuple(ordered_paths),
    }


def _fact_set_with_empty_provenance(
    request: Mapping[str, object], fact_set: Mapping[str, object]
) -> dict[str, object]:
    return {
        "artifact_kind": "FACT_SET",
        "schema_version": "0.1",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "source_snapshot_digest": request["source_snapshot_digest"],
        "policy_digest": request["policy_digest"],
        "analysis_scope_digest": request["analysis_scope_digest"],
        "derivation_profile_digest": request["derivation_profile_digest"],
        "facts": [
            {**copy.deepcopy(fact), "provenance_refs": []}
            for fact in fact_set["facts"]
        ],
        "conflicts": [],
        "fact_set_digest": request["fact_set_digest"],
    }


def _validate_observation_projection(
    projection: OwnedSourceOperationProjection,
    *,
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
    fact_set_digest: object,
    domain: Mapping[str, object],
    assigned: Sequence[str],
    facts_by_id: Mapping[str, Mapping[str, object]],
    expected_digests: Mapping[str, str],
    index: Mapping[str, object],
) -> None:
    _validate_source_operation_projection(projection)
    items_by_id = {
        item["observation_item_id"]: item
        for item in domain["observation_items"]
    }
    referenced_paths: set[str] = set()
    for item_id in assigned:
        item = items_by_id[item_id]
        fact = facts_by_id.get(item["subject_fact_id"])
        if fact is None:
            raise ValueError
        referenced_paths.add(fact["source_anchor"]["git_path"]["git_path_hex"])
    eligible_paths = index["eligible_paths"]
    if not isinstance(eligible_paths, frozenset) or not referenced_paths.issubset(
        eligible_paths
    ):
        raise ValueError
    identity_by_path = index["identity_by_path"]
    ordered_paths = index["ordered_paths"]
    if not isinstance(identity_by_path, dict) or not isinstance(ordered_paths, tuple):
        raise ValueError
    operation_ids = tuple(
        identity_by_path[path]
        for path in ordered_paths
        if path in referenced_paths
    )
    if (
        projection.source_snapshot_digest
        != expected_digests["source_snapshot_digest"]
        or projection.policy_digest != expected_digests["policy_digest"]
        or projection.analysis_scope_digest
        != expected_digests["analysis_scope_digest"]
        or projection.derivation_profile_digest
        != expected_digests["derivation_profile_digest"]
        or projection.language_support_function
        != classification.language_support_function
        or projection.classification_digest
        != classification.classification_digest
        or projection.operation_kind != "RELATION_OBSERVATION"
        or projection.provider_descriptor_copy() != descriptor.document()
        or projection.fact_set_digest != fact_set_digest
        or projection.observation_domain_digest
        != domain["observation_domain_digest"]
        or projection.assigned_observation_item_ids != tuple(assigned)
        or projection.eligible_subject_ids != index["eligible_subject_ids"]
        or projection.operation_subject_ids != operation_ids
    ):
        raise ValueError
