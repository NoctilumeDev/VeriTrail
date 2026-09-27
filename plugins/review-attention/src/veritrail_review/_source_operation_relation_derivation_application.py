from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Mapping

from veritrail_review._execution_cell_application import provider_run_id
from veritrail_review._execution_cell_binding import ProviderDescriptor
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
)
from veritrail_review._relation_execution_cell_application import (
    RelationApplicationProtocolError as HistoricalRelationProtocolError,
    _descriptor_from_document,
    _validate_canonical_relation,
    _validate_fact_set_projection,
    _validate_relation_requirement,
    canonicalize_relation_candidates as _canonicalize_relation_candidates,
    fact_set_semantic_projection,
)
from veritrail_review._relation_execution_cell_binding import (
    relation_descriptor_for_launch_key,
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
    build_relation_derivation_source_operation_projection,
)
from veritrail_review._source_operation_projection_values import (
    OwnedSourceOperationProjection,
    _validate_source_operation_projection,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


PROTOCOL = "veritrail-review-relation-cell/0.3"
REQUEST_KIND = "RELATION_CELL_REQUEST"
TERMINAL_KIND = "RELATION_CELL_TERMINAL"
OPERANDS_DOMAIN = "veritrail.review.provider-operands/0.5"

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
        "operands_digest",
        "source_snapshot",
        "review_policy",
        "derivation_profile",
        "fact_set",
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
        "operands_digest",
        "provider_run_id",
        "terminal_kind",
        "canonical_relations",
        "reported_fact_ids",
        "reported_relation_ids",
    }
)
_TERMINAL_KINDS = frozenset(
    {
        "COMPLETED",
        "PROVIDER_UNAVAILABLE",
        "PROVIDER_FAILED",
        "NONCONFORMANT_PROVIDER_OUTPUT",
        "INTERNAL_DERIVATION_ERROR",
    }
)


class RelationSourceOperationProtocolError(ValueError):
    """The private corrected Relation derivation wire failed validation."""


@dataclass(frozen=True)
class ValidatedRelationSourceOperationRequest:
    document: dict[str, object]
    descriptor: ProviderDescriptor
    provider_run_id: str
    facts_by_id: dict[str, dict[str, object]]
    source_blobs_by_path_hex: dict[str, bytes]


def copy_relation_source_operation_request_for_provider(
    request: ValidatedRelationSourceOperationRequest,
) -> ValidatedRelationSourceOperationRequest:
    """Give Provider code an owned copy without omitted source bodies."""

    return ValidatedRelationSourceOperationRequest(
        document=copy.deepcopy(request.document),
        descriptor=ProviderDescriptor(**request.descriptor.document()),
        provider_run_id=str(request.provider_run_id),
        facts_by_id=copy.deepcopy(request.facts_by_id),
        source_blobs_by_path_hex={
            str(path_hex): memoryview(raw).tobytes()
            for path_hex, raw in request.source_blobs_by_path_hex.items()
        },
    )


def relation_source_operation_operands_digest(
    inputs: DerivationInputSet,
    descriptor: ProviderDescriptor,
    fact_set_digest: str,
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> str:
    """Bind the historical Relation operands plus exact gate semantics."""

    return _operands_digest_from_parts(
        source_snapshot_digest=inputs.source_snapshot_digest,
        policy_digest=inputs.policy_digest,
        analysis_scope_digest=inputs.analysis_scope_digest,
        slice_policy_digest=inputs.slice_policy_digest,
        derivation_profile_digest=inputs.derivation_profile_digest,
        descriptor=descriptor,
        fact_set_digest=fact_set_digest,
        language_support_function=classification.language_support_function,
        classification_digest=classification.classification_digest,
        source_operation_projection_digest=(
            projection.source_operation_projection_digest
        ),
    )


def build_relation_source_operation_request_document(
    *,
    inputs: DerivationInputSet,
    derivation_id: str,
    request_provenance: Mapping[str, object],
    descriptor: ProviderDescriptor,
    fact_set_document: Mapping[str, object],
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> dict[str, object]:
    """Build corrected Relation input without integrating a controller."""

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
    expected_projection = build_relation_derivation_source_operation_projection(
        classification, descriptor, owned_fact_set
    )
    if (
        projection.projection_document_copy()
        != expected_projection.projection_document_copy()
    ):
        raise RelationSourceOperationProtocolError(
            "Relation source operation projection mismatch"
        )
    fact_set = fact_set_semantic_projection(owned_fact_set)
    fact_set_digest = owned_fact_set.get("fact_set_digest")
    if not isinstance(fact_set_digest, str):
        raise RelationSourceOperationProtocolError("invalid FactSet digest")
    source_blobs, _, _ = _owned_operation_source_blobs(
        inputs, classification, projection
    )
    operands_digest = relation_source_operation_operands_digest(
        inputs,
        descriptor,
        fact_set_digest,
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
        "operands_digest": operands_digest,
        "source_snapshot": snapshot,
        "review_policy": policy,
        "derivation_profile": profile,
        "fact_set": fact_set,
        "language_support_classification": (
            classification.classification_document_copy()
        ),
        "source_operation_projection": projection.projection_document_copy(),
        "source_blobs": source_blobs,
    }


def validate_relation_source_operation_request_document(
    document: Mapping[str, object], *, launch_key: str
) -> ValidatedRelationSourceOperationRequest:
    """Validate the 0.3 request without reacquiring omitted bodies."""

    try:
        if set(document) != _REQUEST_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != REQUEST_KIND:
            raise ValueError
        derivation_id = document["derivation_id"]
        if not isinstance(derivation_id, str) or not derivation_id:
            raise ValueError
        descriptor = _descriptor_from_document(document["provider_descriptor"])
        expected_descriptor = relation_descriptor_for_launch_key(launch_key)
        if expected_descriptor is None or descriptor != expected_descriptor:
            raise ValueError
        request_provenance = document["request_provenance"]
        if not isinstance(request_provenance, Mapping) or set(request_provenance) != {
            "requested_repository_id",
            "requested_ref",
            "resolver_id",
            "resolver_version",
            "resolved_at",
        }:
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
        _validate_relation_projection(
            projection,
            classification=classification,
            descriptor=descriptor,
            fact_set_digest=document["fact_set_digest"],
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
            language_support_function=classification.language_support_function,
            classification_digest=classification.classification_digest,
            source_operation_projection_digest=(
                projection.source_operation_projection_digest
            ),
        )
        if document["operands_digest"] != expected_operands:
            raise ValueError
        run_id = provider_run_id(derivation_id, descriptor, expected_operands)
        _validate_request_provenance(request_provenance, snapshot)
        return ValidatedRelationSourceOperationRequest(
            document=copy.deepcopy(dict(document)),
            descriptor=descriptor,
            provider_run_id=run_id,
            facts_by_id=copy.deepcopy(facts_by_id),
            source_blobs_by_path_hex=source_blobs,
        )
    except Exception as exc:
        if isinstance(exc, RelationSourceOperationProtocolError):
            raise
        raise RelationSourceOperationProtocolError(
            "nonconformant corrected Relation derivation request envelope"
        ) from exc


def canonicalize_relation_source_operation_candidates(
    request: ValidatedRelationSourceOperationRequest, candidates: object
) -> list[dict[str, object]]:
    try:
        return _canonicalize_relation_candidates(  # type: ignore[arg-type]
            request, candidates
        )
    except HistoricalRelationProtocolError as exc:
        raise RelationSourceOperationProtocolError(
            "nonconformant Relation candidates"
        ) from exc


def relation_source_operation_terminal_document(
    request: ValidatedRelationSourceOperationRequest,
    *,
    terminal_kind: str,
    canonical_relations: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    relations = copy.deepcopy(canonical_relations or [])
    if terminal_kind not in _TERMINAL_KINDS:
        raise RelationSourceOperationProtocolError("invalid terminal kind")
    if terminal_kind != "COMPLETED" and relations:
        raise RelationSourceOperationProtocolError(
            "non-success terminal retained candidates"
        )
    return {
        "protocol": PROTOCOL,
        "message_kind": TERMINAL_KIND,
        "derivation_id": request.document["derivation_id"],
        "provider_descriptor": request.descriptor.document(),
        "fact_set_digest": request.document["fact_set_digest"],
        "operands_digest": request.document["operands_digest"],
        "provider_run_id": request.provider_run_id,
        "terminal_kind": terminal_kind,
        "canonical_relations": relations,
        "reported_fact_ids": [],
        "reported_relation_ids": [
            relation["relation_id"] for relation in relations
        ],
    }


def validate_relation_source_operation_terminal_document(
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
        terminal_kind = document["terminal_kind"]
        if terminal_kind not in _TERMINAL_KINDS:
            raise ValueError
        descriptor = _descriptor_from_document(request["provider_descriptor"])
        run_id = provider_run_id(
            request["derivation_id"], descriptor, request["operands_digest"]
        )
        if (
            document["derivation_id"] != request["derivation_id"]
            or document["provider_descriptor"] != request["provider_descriptor"]
            or document["fact_set_digest"] != request["fact_set_digest"]
            or document["operands_digest"] != request["operands_digest"]
            or document["provider_run_id"] != run_id
            or document["reported_fact_ids"] != []
        ):
            raise ValueError
        relations = document["canonical_relations"]
        reported = document["reported_relation_ids"]
        if not isinstance(relations, list) or not isinstance(reported, list):
            raise ValueError
        if terminal_kind != "COMPLETED" and (relations or reported):
            raise ValueError
        facts = request["fact_set"]["facts"]
        facts_by_id = {fact["fact_id"]: copy.deepcopy(fact) for fact in facts}
        previous_id: str | None = None
        subjects: set[str] = set()
        for relation in relations:
            _validate_canonical_relation(
                relation, run_id=run_id, request=request, facts_by_id=facts_by_id
            )
            relation_id = relation["relation_id"]
            if previous_id is not None and relation_id <= previous_id:
                raise ValueError
            previous_id = relation_id
            subject = relation["relation_subject_digest"]
            if subject in subjects:
                raise ValueError
            subjects.add(subject)
        expected_ids = [relation["relation_id"] for relation in relations]
        if reported != expected_ids or reported != sorted(set(reported)):
            raise ValueError
        return copy.deepcopy(dict(document))
    except Exception as exc:
        raise RelationSourceOperationProtocolError(
            "nonconformant corrected Relation derivation terminal envelope"
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
        semantic_input = subject["semantic_input"]
        inventory = semantic_input["inventory_item"]
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


def _validate_relation_projection(
    projection: OwnedSourceOperationProjection,
    *,
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
    fact_set_digest: object,
    facts_by_id: Mapping[str, Mapping[str, object]],
    expected_digests: Mapping[str, str],
    index: Mapping[str, object],
) -> None:
    _validate_source_operation_projection(projection)
    referenced_paths = {
        fact["source_anchor"]["git_path"]["git_path_hex"]
        for fact in facts_by_id.values()
    }
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
        or projection.operation_kind != "RELATION_DERIVATION"
        or projection.provider_descriptor_copy() != descriptor.document()
        or projection.fact_set_digest != fact_set_digest
        or projection.observation_domain_digest is not None
        or projection.assigned_observation_item_ids != ()
        or projection.eligible_subject_ids != index["eligible_subject_ids"]
        or projection.operation_subject_ids != operation_ids
    ):
        raise ValueError
