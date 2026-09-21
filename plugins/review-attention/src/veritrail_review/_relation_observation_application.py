from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Mapping, Sequence

from veritrail_review._execution_cell_application import (
    _WorkerValidationState,
    _nonempty_text,
    _validate_source_blobs,
    provider_run_id,
)
from veritrail_review._execution_cell_binding import ProviderDescriptor
from veritrail_review._relation_execution_cell_application import (
    _decode_source_blobs,
    _descriptor_from_document,
    _owned_source_blobs,
    _validate_fact_set_projection,
    _validate_relation_requirement,
    fact_set_semantic_projection,
)
from veritrail_review._relation_observation_binding import (
    closed_test_relation_observation_bindings,
    relation_observation_descriptor_for_launch_key,
)
from veritrail_review._relation_observation_domain import (
    responsibility_for_descriptor,
    validate_declared_relation_observation_domain,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.contracts import validate_source_snapshot_document
from veritrail_review.derivation_input import (
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
)
from veritrail_review.derivation_input_contracts import DerivationInputSet


PROTOCOL = "veritrail-review-relation-cell/0.2"
REQUEST_KIND = "RELATION_OBSERVATION_CELL_REQUEST"
TERMINAL_KIND = "RELATION_OBSERVATION_CELL_TERMINAL"

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
_RELATION_CANDIDATE_KEYS = frozenset(
    {
        "relation_space",
        "relation_kind",
        "source_fact_id",
        "local_ordinal",
        "target",
        "semantic_attributes",
    }
)
_RELATION_KEYS = frozenset(
    {
        "relation_id",
        "relation_subject_digest",
        *_RELATION_CANDIDATE_KEYS,
        "provenance_refs",
    }
)
_OUTCOME_KEYS = frozenset(
    {
        "observation_outcome_id",
        "provider_run_id",
        "observation_item_id",
        "disposition",
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


class RelationObservationApplicationError(ValueError):
    pass


@dataclass(frozen=True)
class ValidatedRelationObservationRequest:
    document: dict[str, object]
    descriptor: ProviderDescriptor
    provider_run_id: str
    facts_by_id: Mapping[str, dict[str, object]]
    observation_items_by_id: Mapping[str, dict[str, object]]
    source_blobs_by_path_hex: Mapping[str, bytes]


def copy_relation_observation_request_for_provider(
    request: ValidatedRelationObservationRequest,
) -> ValidatedRelationObservationRequest:
    return ValidatedRelationObservationRequest(
        document=copy.deepcopy(request.document),
        descriptor=ProviderDescriptor(**request.descriptor.document()),
        provider_run_id=str(request.provider_run_id),
        facts_by_id=copy.deepcopy(dict(request.facts_by_id)),
        observation_items_by_id=copy.deepcopy(
            dict(request.observation_items_by_id)
        ),
        source_blobs_by_path_hex={
            str(path_hex): memoryview(raw).tobytes()
            for path_hex, raw in request.source_blobs_by_path_hex.items()
        },
    )


def relation_observation_provider_operands_digest(
    inputs: DerivationInputSet,
    descriptor: ProviderDescriptor,
    fact_set_digest: str,
    observation_domain_digest: str,
    assigned_observation_item_ids: Sequence[str],
) -> str:
    return semantic_digest(
        "veritrail.review.provider-operands/0.3",
        {
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "policy_digest": inputs.policy_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "slice_policy_digest": inputs.slice_policy_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            **descriptor.document(),
            "fact_set_digest": fact_set_digest,
            "observation_domain_digest": observation_domain_digest,
            "assigned_observation_item_ids": list(
                assigned_observation_item_ids
            ),
        },
    )


def build_relation_observation_request_document(
    *,
    inputs: DerivationInputSet,
    derivation_id: str,
    request_provenance: Mapping[str, object],
    descriptor: ProviderDescriptor,
    fact_set_document: Mapping[str, object],
    observation_domain: Mapping[str, object],
) -> dict[str, object]:
    validated_domain = validate_declared_relation_observation_domain(
        observation_domain,
        inputs=inputs,
        fact_set_document=fact_set_document,
        relation_bindings=closed_test_relation_observation_bindings(),
    )
    responsibility = responsibility_for_descriptor(validated_domain, descriptor)
    assigned = responsibility["assigned_observation_item_ids"]
    snapshot = inputs.source_snapshot_document_copy()
    policy = inputs.review_policy_document_copy()
    profile = inputs.derivation_profile_document_copy()
    projection = fact_set_semantic_projection(fact_set_document)
    fact_set_digest = fact_set_document.get("fact_set_digest")
    if not isinstance(fact_set_digest, str):
        raise RelationObservationApplicationError("invalid FactSet digest")
    if fact_set_digest != semantic_digest(
        "veritrail.review.fact-set/0.1", projection
    ):
        raise RelationObservationApplicationError("FactSet digest mismatch")
    operands = relation_observation_provider_operands_digest(
        inputs,
        descriptor,
        fact_set_digest,
        validated_domain["observation_domain_digest"],
        assigned,
    )
    return {
        "protocol": PROTOCOL,
        "message_kind": REQUEST_KIND,
        "derivation_id": derivation_id,
        "request_provenance": copy.deepcopy(dict(request_provenance)),
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "policy_digest": inputs.policy_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "slice_policy_digest": inputs.slice_policy_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        "provider_descriptor": descriptor.document(),
        "fact_set_digest": fact_set_digest,
        "observation_domain_digest": validated_domain[
            "observation_domain_digest"
        ],
        "assigned_observation_item_ids": copy.deepcopy(assigned),
        "operands_digest": operands,
        "source_snapshot": snapshot,
        "review_policy": policy,
        "derivation_profile": profile,
        "fact_set": projection,
        "observation_domain": validated_domain,
        "source_blobs": _owned_source_blobs(inputs, snapshot),
    }


def validate_relation_observation_request_document(
    document: Mapping[str, object], *, launch_key: str
) -> ValidatedRelationObservationRequest:
    try:
        if set(document) != _REQUEST_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != REQUEST_KIND:
            raise ValueError
        derivation_id = document["derivation_id"]
        if not _nonempty_text(derivation_id):
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
        if not all(isinstance(value, Mapping) for value in (snapshot, policy, profile)):
            raise ValueError
        state = _WorkerValidationState()
        validate_source_snapshot_document(
            snapshot,
            expected_bytes=canonical_json_bytes(snapshot) + b"\n",
            max_canonical_bytes=state.profile.max_source_snapshot_bytes,
        )
        _validate_profile(profile, state)  # type: ignore[arg-type]
        _validate_policy(policy, profile, state)  # type: ignore[arg-type]
        _validate_cross_artifact_binding(snapshot, policy, profile, state)  # type: ignore[arg-type]
        _validate_relation_requirement(policy)
        expected_digests = {
            "source_snapshot_digest": snapshot["source_snapshot_digest"],
            "policy_digest": policy["policy_digest"],
            "analysis_scope_digest": policy["analysis_scope_digest"],
            "slice_policy_digest": policy["slice_policy_digest"],
            "derivation_profile_digest": profile["profile_digest"],
        }
        if any(document[key] != value for key, value in expected_digests.items()):
            raise ValueError
        sizes, supported = _validate_source_blobs(
            document["source_blobs"], snapshot, profile
        )
        source_blobs = _decode_source_blobs(document["source_blobs"])
        in_scope = frozenset(
            item["git_path"]["git_path_hex"]
            for item in policy["scope_decisions"]
            if item["disposition"] == "IN_SCOPE"
        )
        facts_by_id = _validate_fact_set_projection(
            document["fact_set"],
            fact_set_digest=document["fact_set_digest"],
            expected_digests=expected_digests,
            source_sizes_by_path_hex=sizes,
            in_scope_paths=in_scope,
            supported_paths=supported,
        )
        ephemeral_inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=canonical_json_bytes(snapshot) + b"\n",
            review_policy_canonical_bytes=canonical_json_bytes(policy) + b"\n",
            derivation_profile_canonical_bytes=canonical_json_bytes(profile) + b"\n",
            verified_blob_bytes_by_object_identity={},
            **expected_digests,
        )
        fact_set_document = {
            "artifact_kind": "FACT_SET",
            "schema_version": "0.1",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "source_snapshot_digest": document["source_snapshot_digest"],
            "policy_digest": document["policy_digest"],
            "analysis_scope_digest": document["analysis_scope_digest"],
            "derivation_profile_digest": document[
                "derivation_profile_digest"
            ],
            "facts": [
                {
                    **copy.deepcopy(fact),
                    "provenance_refs": [],
                }
                for fact in document["fact_set"]["facts"]
            ],
            "conflicts": [],
            "fact_set_digest": document["fact_set_digest"],
        }
        domain = validate_declared_relation_observation_domain(
            document["observation_domain"],
            inputs=ephemeral_inputs,
            fact_set_document=fact_set_document,
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
        expected_operands = relation_observation_provider_operands_digest(
            ephemeral_inputs,
            descriptor,
            document["fact_set_digest"],
            domain["observation_domain_digest"],
            assigned,
        )
        if document["operands_digest"] != expected_operands:
            raise ValueError
        run_id = provider_run_id(derivation_id, descriptor, expected_operands)
        request_provenance = document["request_provenance"]
        coordinate = snapshot["source_coordinate"]
        commit_oid = coordinate["commit_oid"]
        expected_ref = f"oid:{commit_oid['algorithm'].lower()}:{commit_oid['hex']}"
        if (
            not isinstance(request_provenance, Mapping)
            or set(request_provenance)
            != {
                "requested_repository_id",
                "requested_ref",
                "resolver_id",
                "resolver_version",
                "resolved_at",
            }
            or request_provenance["requested_repository_id"]
            != snapshot["repository_id"]
            or request_provenance["requested_ref"] != expected_ref
            or request_provenance["resolver_id"]
            != "veritrail-r1-owned-snapshot-exact-oid"
            or request_provenance["resolver_version"] != "0.1"
            or not _nonempty_text(request_provenance["resolved_at"])
        ):
            raise ValueError
        items = {
            item["observation_item_id"]: copy.deepcopy(item)
            for item in domain["observation_items"]
        }
        return ValidatedRelationObservationRequest(
            document=copy.deepcopy(dict(document)),
            descriptor=descriptor,
            provider_run_id=run_id,
            facts_by_id=facts_by_id,
            observation_items_by_id=items,
            source_blobs_by_path_hex=source_blobs,
        )
    except Exception as exc:
        if isinstance(exc, RelationObservationApplicationError):
            raise
        raise RelationObservationApplicationError(
            "nonconformant Relation observation request envelope"
        ) from exc


def canonicalize_relation_observation_candidates(
    request: ValidatedRelationObservationRequest, candidates: object
) -> list[dict[str, object]]:
    if not isinstance(candidates, list):
        raise RelationObservationApplicationError("candidates are not a list")
    by_id: dict[str, dict[str, object]] = {}
    for candidate in candidates:
        relation = _canonicalize_candidate(request, candidate)
        relation_id = relation["relation_id"]
        previous = by_id.get(relation_id)
        if previous is not None and previous != relation:
            raise RelationObservationApplicationError("Relation identity collision")
        by_id[relation_id] = relation
    return [by_id[key] for key in sorted(by_id)]


def canonicalize_provider_observation_outcomes(
    request: ValidatedRelationObservationRequest, outcomes: object
) -> list[dict[str, object]]:
    if not isinstance(outcomes, list):
        raise RelationObservationApplicationError("outcomes are not a list")
    result: list[dict[str, object]] = []
    for outcome in outcomes:
        if not isinstance(outcome, Mapping) or set(outcome) != _OUTCOME_KEYS:
            raise RelationObservationApplicationError("invalid outcome shape")
        item_id = outcome["observation_item_id"]
        disposition = outcome["disposition"]
        relation_ids = outcome["reported_relation_ids"]
        if (
            outcome["provider_run_id"] != request.provider_run_id
            or not isinstance(item_id, str)
            or disposition not in {"CANDIDATE_REPORTED", "NO_CANDIDATE_OBSERVED"}
            or not isinstance(relation_ids, list)
            or any(not isinstance(value, str) for value in relation_ids)
            or relation_ids != sorted(set(relation_ids))
            or (disposition == "NO_CANDIDATE_OBSERVED" and relation_ids)
        ):
            raise RelationObservationApplicationError("invalid outcome value")
        payload = {
            "provider_run_id": request.provider_run_id,
            "observation_item_id": item_id,
            "disposition": disposition,
            "reported_relation_ids": copy.deepcopy(relation_ids),
        }
        if outcome["observation_outcome_id"] != semantic_digest(
            "veritrail.review.relation-observation-outcome/0.1", payload
        ):
            raise RelationObservationApplicationError("outcome identity mismatch")
        result.append({"observation_outcome_id": outcome["observation_outcome_id"], **payload})
    result.sort(key=lambda item: (item["observation_item_id"], item["observation_outcome_id"]))
    return result


def relation_observation_terminal_document(
    request: ValidatedRelationObservationRequest,
    *,
    terminal_kind: str,
    canonical_relations: list[dict[str, object]] | None = None,
    observation_outcomes: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    relations = copy.deepcopy(canonical_relations or [])
    outcomes = copy.deepcopy(observation_outcomes or [])
    if terminal_kind not in _TERMINAL_KINDS:
        raise RelationObservationApplicationError("invalid terminal kind")
    if terminal_kind != "COMPLETED" and (relations or outcomes):
        raise RelationObservationApplicationError(
            "non-success terminal retained output"
        )
    return {
        "protocol": PROTOCOL,
        "message_kind": TERMINAL_KIND,
        "derivation_id": request.document["derivation_id"],
        "provider_descriptor": request.descriptor.document(),
        "fact_set_digest": request.document["fact_set_digest"],
        "observation_domain_digest": request.document[
            "observation_domain_digest"
        ],
        "assigned_observation_item_ids": copy.deepcopy(
            request.document["assigned_observation_item_ids"]
        ),
        "operands_digest": request.document["operands_digest"],
        "provider_run_id": request.provider_run_id,
        "terminal_kind": terminal_kind,
        "canonical_relations": relations,
        "observation_outcomes": outcomes,
        "reported_fact_ids": [],
        "reported_relation_ids": [item["relation_id"] for item in relations],
    }


def validate_relation_observation_terminal_document(
    document: Mapping[str, object], *, request: Mapping[str, object]
) -> dict[str, object]:
    try:
        if set(document) != _TERMINAL_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != TERMINAL_KIND:
            raise ValueError
        terminal_kind = document["terminal_kind"]
        if terminal_kind not in _TERMINAL_KINDS:
            raise ValueError
        descriptor = _descriptor_from_document(request["provider_descriptor"])
        run_id = provider_run_id(
            request["derivation_id"], descriptor, request["operands_digest"]
        )
        for key in (
            "derivation_id",
            "provider_descriptor",
            "fact_set_digest",
            "observation_domain_digest",
            "assigned_observation_item_ids",
            "operands_digest",
        ):
            if document[key] != request[key]:
                raise ValueError
        if document["provider_run_id"] != run_id or document["reported_fact_ids"] != []:
            raise ValueError
        relations = document["canonical_relations"]
        outcomes = document["observation_outcomes"]
        reported = document["reported_relation_ids"]
        if not all(isinstance(value, list) for value in (relations, outcomes, reported)):
            raise ValueError
        if terminal_kind != "COMPLETED" and (relations or outcomes or reported):
            raise ValueError
        synthetic = _synthetic_request(request, run_id)
        canonical_relations = canonicalize_relation_observation_candidates(
            synthetic,
            [
                {key: copy.deepcopy(relation[key]) for key in _RELATION_CANDIDATE_KEYS}
                for relation in relations
            ],
        )
        if canonical_relations != relations:
            raise ValueError
        canonical_outcomes = canonicalize_provider_observation_outcomes(
            synthetic, outcomes
        )
        if canonical_outcomes != outcomes:
            raise ValueError
        expected_ids = [item["relation_id"] for item in relations]
        if reported != expected_ids or reported != sorted(set(reported)):
            raise ValueError
        return copy.deepcopy(dict(document))
    except Exception as exc:
        if isinstance(exc, RelationObservationApplicationError):
            raise
        raise RelationObservationApplicationError(
            "nonconformant Relation observation terminal envelope"
        ) from exc


def relation_for_observation_item(
    request: ValidatedRelationObservationRequest,
    relation: Mapping[str, object],
) -> str | None:
    kind = relation["relation_kind"]
    subject_fact_id = (
        relation["target"].get("fact_id")
        if kind == "LEXICAL_CONTAINS"
        else relation["source_fact_id"]
    )
    matches = [
        item_id
        for item_id, item in request.observation_items_by_id.items()
        if item["relation_kind"] == kind
        and item["subject_fact_id"] == subject_fact_id
    ]
    return matches[0] if len(matches) == 1 else None


def _canonicalize_candidate(
    request: ValidatedRelationObservationRequest, candidate: object
) -> dict[str, object]:
    if not isinstance(candidate, Mapping) or set(candidate) != _RELATION_CANDIDATE_KEYS:
        raise RelationObservationApplicationError("nonconformant candidate")
    source_id = candidate["source_fact_id"]
    ordinal = candidate["local_ordinal"]
    target = candidate["target"]
    if (
        not isinstance(source_id, str)
        or source_id not in request.facts_by_id
        or type(ordinal) is not int
        or ordinal < 0
        or candidate["semantic_attributes"] != {}
        or not isinstance(target, Mapping)
    ):
        raise RelationObservationApplicationError("invalid candidate projection")
    source = request.facts_by_id[source_id]
    kind = candidate["relation_kind"]
    space = candidate["relation_space"]
    if kind == "LEXICAL_CONTAINS":
        if (
            space != "CHILD_EDGE"
            or set(target) != {"target_kind", "fact_id"}
            or target["target_kind"] != "FACT"
            or target["fact_id"] not in request.facts_by_id
        ):
            raise RelationObservationApplicationError("invalid lexical target")
        target_fact = request.facts_by_id[target["fact_id"]]
        if (
            source["fact_kind"] != "MODULE"
            or target_fact["fact_kind"] != "IMPORT_DECLARATION"
            or source["source_anchor"]["git_path"]
            != target_fact["source_anchor"]["git_path"]
        ):
            raise RelationObservationApplicationError("invalid lexical endpoints")
    elif kind == "IMPORT_TARGET_LITERAL":
        attributes = source["semantic_attributes"]
        if (
            space != "IMPORT_EDGE"
            or source["fact_kind"] != "IMPORT_DECLARATION"
            or ordinal != 0
            or set(target)
            != {
                "target_kind",
                "relative_level",
                "module_parts",
                "imported_name",
                "resolution_status",
                "topology_status",
                "resolved_fact_ids",
            }
            or target["target_kind"] != "IMPORT_LITERAL"
            or target["relative_level"] != attributes["relative_level"]
            or target["module_parts"] != attributes["module_parts"]
            or target["imported_name"] != attributes["imported_name"]
            or target["resolution_status"] != "UNRESOLVED"
            or target["topology_status"] != "UNKNOWN"
            or target["resolved_fact_ids"] != []
        ):
            raise RelationObservationApplicationError("invalid import target")
    else:
        raise RelationObservationApplicationError("unsupported relation kind")
    owned_target = copy.deepcopy(dict(target))
    subject = semantic_digest(
        "veritrail.review.relation-subject/0.1",
        {
            "source_snapshot_digest": request.document[
                "source_snapshot_digest"
            ],
            "derivation_profile_digest": request.document[
                "derivation_profile_digest"
            ],
            "relation_space": space,
            "source_fact_id": source_id,
            "local_ordinal": ordinal,
        },
    )
    relation_id = semantic_digest(
        "veritrail.review.structural-relation/0.1",
        {
            "relation_subject_digest": subject,
            "relation_kind": kind,
            "target": owned_target,
            "semantic_attributes": {},
        },
    )
    return {
        "relation_id": relation_id,
        "relation_subject_digest": subject,
        "relation_space": space,
        "relation_kind": kind,
        "source_fact_id": source_id,
        "local_ordinal": ordinal,
        "target": owned_target,
        "semantic_attributes": {},
        "provenance_refs": [request.provider_run_id],
    }


def _synthetic_request(
    request: Mapping[str, object], run_id: str
) -> ValidatedRelationObservationRequest:
    facts = request["fact_set"]["facts"]
    items = request["observation_domain"]["observation_items"]
    return ValidatedRelationObservationRequest(
        document=copy.deepcopy(dict(request)),
        descriptor=_descriptor_from_document(request["provider_descriptor"]),
        provider_run_id=run_id,
        facts_by_id={item["fact_id"]: copy.deepcopy(item) for item in facts},
        observation_items_by_id={
            item["observation_item_id"]: copy.deepcopy(item) for item in items
        },
        source_blobs_by_path_hex={},
    )


def build_provider_outcome(
    *,
    provider_run_id_value: str,
    observation_item_id: str,
    disposition: str,
    reported_relation_ids: Sequence[str],
) -> dict[str, object]:
    payload = {
        "provider_run_id": provider_run_id_value,
        "observation_item_id": observation_item_id,
        "disposition": disposition,
        "reported_relation_ids": sorted(set(reported_relation_ids)),
    }
    return {
        "observation_outcome_id": semantic_digest(
            "veritrail.review.relation-observation-outcome/0.1", payload
        ),
        **payload,
    }
