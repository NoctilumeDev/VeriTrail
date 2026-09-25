from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Mapping

from veritrail_review._review_slice_traversal_assignment_values import (
    OwnedReviewSliceTraversalAssignments,
    _validate_traversal_assignments,
)
from veritrail_review.budget import OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_EMPTY_DOMAIN_CLOSURE_TOKEN = object()
_CLOSED_EMPTY = "CLOSED_EMPTY"


@dataclass(frozen=True)
class OwnedReviewSliceEmptyDomainClosure:
    """Private G-stage empty-domain closure; no SliceSet or Coverage authority."""

    derivation_id: str
    admission_witness_digest: str
    slice_obligation_domain_digest: str
    closure_status: str
    empty_domain_closure_digest: str
    closure_document_bytes: bytes = field(repr=False)
    _assignments: OwnedReviewSliceTraversalAssignments = field(
        repr=False, compare=False
    )
    _committed_phase: OwnedPhaseResult = field(repr=False, compare=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        assignments: OwnedReviewSliceTraversalAssignments,
        closure_document: Mapping[str, object],
        committed_phase: OwnedPhaseResult,
    ) -> "OwnedReviewSliceEmptyDomainClosure":
        document_bytes = canonical_json_bytes(closure_document)
        if (
            type(committed_phase) is not OwnedPhaseResult
            or committed_phase.canonical_bytes != document_bytes
        ):
            raise ValueError
        values = {
            "derivation_id": closure_document["derivation_id"],
            "admission_witness_digest": closure_document[
                "admission_witness_digest"
            ],
            "slice_obligation_domain_digest": closure_document[
                "slice_obligation_domain_digest"
            ],
            "closure_status": closure_document["closure_status"],
            "empty_domain_closure_digest": closure_document[
                "empty_domain_closure_digest"
            ],
            "closure_document_bytes": document_bytes,
            "_assignments": assignments,
            "_committed_phase": committed_phase,
        }
        return cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_EMPTY_DOMAIN_CLOSURE_TOKEN,
        )

    def closure_document_copy(self) -> dict[str, object]:
        return _object(self.closure_document_bytes)

    def _owned_assignments(self) -> OwnedReviewSliceTraversalAssignments:
        return self._assignments


def _validate_empty_domain_closure(
    value: OwnedReviewSliceEmptyDomainClosure,
) -> None:
    if (
        type(value) is not OwnedReviewSliceEmptyDomainClosure
        or value._construction_token is not _EMPTY_DOMAIN_CLOSURE_TOKEN
    ):
        raise ValueError
    assignments = value._owned_assignments()
    _validate_traversal_assignments(assignments)
    gate = assignments._owned_domain_gate()
    obligations = gate.obligations_copy()
    if (
        gate.candidate_composition_status != "CONSISTENT"
        or gate.slice_input_status != "ELIGIBLE"
        or obligations != []
        or assignments.assignment_count != 0
        or assignments.remaining_assignment_count() != 0
    ):
        raise ValueError
    validated = gate._owned_cross_validated_input()
    document = value.closure_document_copy()
    expected_fields = {
        "derivation_id",
        "admission_witness_digest",
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "fact_set_digest",
        "relation_set_digest",
        "slice_obligation_domain_digest",
        "closure_status",
        "assignment_count",
        "traversal_outcomes",
        "normal_slice_candidates",
        "empty_domain_closure_digest",
    }
    if set(document) != expected_fields:
        raise ValueError
    if (
        (
            document["derivation_id"],
            document["admission_witness_digest"],
            document["source_snapshot_digest"],
            document["policy_digest"],
            document["analysis_scope_digest"],
            document["slice_policy_digest"],
            document["derivation_profile_digest"],
            document["fact_set_digest"],
            document["relation_set_digest"],
            document["slice_obligation_domain_digest"],
        )
        != (
            assignments.derivation_id,
            assignments.admission_witness_digest,
            validated.source_snapshot_digest,
            validated.policy_digest,
            validated.analysis_scope_digest,
            validated.slice_policy_digest,
            validated.derivation_profile_digest,
            validated.fact_set_digest,
            validated.relation_set_digest,
            assignments.slice_obligation_domain_digest,
        )
        or document["closure_status"] != _CLOSED_EMPTY
        or document["assignment_count"] != 0
        or document["traversal_outcomes"] != []
        or document["normal_slice_candidates"] != []
    ):
        raise ValueError
    payload = {
        key: copy.deepcopy(item)
        for key, item in document.items()
        if key != "empty_domain_closure_digest"
    }
    if document["empty_domain_closure_digest"] != semantic_digest(
        "veritrail.review.private-slice-empty-domain-closure/0.1", payload
    ):
        raise ValueError
    values = {
        "derivation_id": value.derivation_id,
        "admission_witness_digest": value.admission_witness_digest,
        "slice_obligation_domain_digest": value.slice_obligation_domain_digest,
        "closure_status": value.closure_status,
        "empty_domain_closure_digest": value.empty_domain_closure_digest,
        "closure_document_bytes": value.closure_document_bytes,
        "_assignments": value._assignments,
        "_committed_phase": value._committed_phase,
    }
    if (
        value._state_seal != _private_state_seal(values)
        or canonical_json_bytes(document) != value.closure_document_bytes
        or value._committed_phase.canonical_bytes != value.closure_document_bytes
        or value._committed_phase.phase_status != "COMPLETED_FOR_PHASE"
        or (
            value.derivation_id,
            value.admission_witness_digest,
            value.slice_obligation_domain_digest,
            value.closure_status,
            value.empty_domain_closure_digest,
        )
        != (
            document["derivation_id"],
            document["admission_witness_digest"],
            document["slice_obligation_domain_digest"],
            document["closure_status"],
            document["empty_domain_closure_digest"],
        )
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    raw = values["closure_document_bytes"]
    assignments = values["_assignments"]
    committed = values["_committed_phase"]
    if (
        not isinstance(raw, bytes)
        or type(assignments) is not OwnedReviewSliceTraversalAssignments
        or type(committed) is not OwnedPhaseResult
    ):
        raise ValueError
    payload = {
        key: item
        for key, item in values.items()
        if key not in {"closure_document_bytes", "_assignments", "_committed_phase"}
    }
    payload["closure_document_sha256"] = hashlib.sha256(raw).hexdigest()
    payload["assignments"] = {
        "derivation_id": assignments.derivation_id,
        "admission_witness_digest": assignments.admission_witness_digest,
        "slice_obligation_domain_digest": (
            assignments.slice_obligation_domain_digest
        ),
        "assignment_count": assignments.assignment_count,
    }
    payload["committed_phase"] = {
        "canonical_sha256": hashlib.sha256(committed.canonical_bytes).hexdigest(),
        "phase_status": committed.phase_status,
    }
    return semantic_digest(
        "veritrail.review.private-owned-slice-empty-domain-closure/0.1",
        payload,
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned empty Slice domain closure is not an object")
    return value
