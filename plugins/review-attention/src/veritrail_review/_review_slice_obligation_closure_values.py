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
from veritrail_review._review_slice_traversal_outcome_values import (
    OwnedReviewSliceTraversalOutcome,
    _validate_traversal_outcome,
)
from veritrail_review.budget import OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_OBLIGATION_CLOSURE_TOKEN = object()
_NORMAL_CLOSED = "NORMAL_CLOSED"


@dataclass(frozen=True)
class OwnedReviewSliceObligationClosure:
    """Private F-stage normal closure; no SliceSet or Coverage authority."""

    derivation_id: str
    admission_witness_digest: str
    slice_obligation_domain_digest: str
    closure_status: str
    slice_obligation_closure_digest: str
    closure_document_bytes: bytes = field(repr=False)
    _assignments: OwnedReviewSliceTraversalAssignments = field(
        repr=False, compare=False
    )
    _outcomes: tuple[OwnedReviewSliceTraversalOutcome, ...] = field(
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
        outcomes: tuple[OwnedReviewSliceTraversalOutcome, ...],
        closure_document: Mapping[str, object],
        committed_phase: OwnedPhaseResult,
    ) -> "OwnedReviewSliceObligationClosure":
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
            "slice_obligation_closure_digest": closure_document[
                "slice_obligation_closure_digest"
            ],
            "closure_document_bytes": document_bytes,
            "_assignments": assignments,
            "_outcomes": outcomes,
            "_committed_phase": committed_phase,
        }
        return cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_OBLIGATION_CLOSURE_TOKEN,
        )

    def closure_document_copy(self) -> dict[str, object]:
        return _object(self.closure_document_bytes)

    def normal_slice_candidates_copy(self) -> list[dict[str, object]]:
        document = self.closure_document_copy()
        candidates = document["normal_slice_candidates"]
        if not isinstance(candidates, list):
            raise RuntimeError("owned obligation closure lacks Slice candidates")
        return copy.deepcopy(candidates)

    def traversal_outcomes_copy(self) -> list[dict[str, object]]:
        document = self.closure_document_copy()
        outcomes = document["traversal_outcomes"]
        if not isinstance(outcomes, list):
            raise RuntimeError("owned obligation closure lacks traversal outcomes")
        return copy.deepcopy(outcomes)

    def _owned_assignments(self) -> OwnedReviewSliceTraversalAssignments:
        return self._assignments

    def _owned_outcomes(self) -> tuple[OwnedReviewSliceTraversalOutcome, ...]:
        return self._outcomes


def _validate_slice_obligation_closure(
    value: OwnedReviewSliceObligationClosure,
) -> None:
    if (
        type(value) is not OwnedReviewSliceObligationClosure
        or value._construction_token is not _OBLIGATION_CLOSURE_TOKEN
    ):
        raise ValueError
    assignments = value._owned_assignments()
    outcomes = value._owned_outcomes()
    _validate_traversal_assignments(assignments)
    if (
        type(outcomes) is not tuple
        or not outcomes
        or len(outcomes) != assignments.assignment_count
    ):
        raise ValueError
    for outcome in outcomes:
        _validate_traversal_outcome(outcome)
        boundary = outcome._owned_boundary()
        if boundary._owned_assignments() is not assignments:
            raise ValueError

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
        "traversal_outcomes",
        "normal_slice_candidates",
        "slice_obligation_closure_digest",
    }
    if set(document) != expected_fields:
        raise ValueError
    gate = assignments._owned_domain_gate()
    validated = gate._owned_cross_validated_input()
    coordinates = (
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
    if coordinates != (
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
    ):
        raise ValueError
    outcome_documents = [item.outcome_document_copy() for item in outcomes]
    candidates = [item.normal_slice_candidate_copy() for item in outcomes]
    if (
        document["closure_status"] != _NORMAL_CLOSED
        or document["traversal_outcomes"] != outcome_documents
        or document["normal_slice_candidates"] != candidates
    ):
        raise ValueError
    payload = {
        key: copy.deepcopy(item)
        for key, item in document.items()
        if key != "slice_obligation_closure_digest"
    }
    if document["slice_obligation_closure_digest"] != semantic_digest(
        "veritrail.review.private-slice-obligation-closure/0.1", payload
    ):
        raise ValueError
    values = {
        "derivation_id": value.derivation_id,
        "admission_witness_digest": value.admission_witness_digest,
        "slice_obligation_domain_digest": value.slice_obligation_domain_digest,
        "closure_status": value.closure_status,
        "slice_obligation_closure_digest": (
            value.slice_obligation_closure_digest
        ),
        "closure_document_bytes": value.closure_document_bytes,
        "_assignments": value._assignments,
        "_outcomes": value._outcomes,
        "_committed_phase": value._committed_phase,
    }
    if (
        value._state_seal != _private_state_seal(values)
        or canonical_json_bytes(document) != value.closure_document_bytes
        or value._committed_phase.canonical_bytes
        != value.closure_document_bytes
        or value._committed_phase.phase_status != "COMPLETED_FOR_PHASE"
        or (
            value.derivation_id,
            value.admission_witness_digest,
            value.slice_obligation_domain_digest,
            value.closure_status,
            value.slice_obligation_closure_digest,
        )
        != (
            document["derivation_id"],
            document["admission_witness_digest"],
            document["slice_obligation_domain_digest"],
            document["closure_status"],
            document["slice_obligation_closure_digest"],
        )
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    raw = values["closure_document_bytes"]
    assignments = values["_assignments"]
    outcomes = values["_outcomes"]
    committed = values["_committed_phase"]
    if (
        not isinstance(raw, bytes)
        or not isinstance(assignments, OwnedReviewSliceTraversalAssignments)
        or type(outcomes) is not tuple
        or any(type(item) is not OwnedReviewSliceTraversalOutcome for item in outcomes)
        or type(committed) is not OwnedPhaseResult
    ):
        raise ValueError
    payload = {
        key: item
        for key, item in values.items()
        if key
        not in {
            "closure_document_bytes",
            "_assignments",
            "_outcomes",
            "_committed_phase",
        }
    }
    payload["closure_document_sha256"] = hashlib.sha256(raw).hexdigest()
    payload["assignments"] = {
        "derivation_id": assignments.derivation_id,
        "admission_witness_digest": assignments.admission_witness_digest,
        "slice_obligation_domain_digest": (
            assignments.slice_obligation_domain_digest
        ),
    }
    payload["traversal_outcome_digests"] = [
        item.traversal_outcome_digest for item in outcomes
    ]
    payload["committed_phase"] = {
        "canonical_sha256": hashlib.sha256(committed.canonical_bytes).hexdigest(),
        "phase_status": committed.phase_status,
    }
    return semantic_digest(
        "veritrail.review.private-owned-slice-obligation-closure/0.1", payload
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned Slice obligation closure is not an object")
    return value
