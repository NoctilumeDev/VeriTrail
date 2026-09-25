from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from threading import Lock
from typing import Mapping

from veritrail_review._review_slice_obligation_domain_values import (
    OwnedReviewSliceObligationDomainGate,
    _validate_obligation_domain_gate,
)
from veritrail_review.budget import OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_ASSIGNMENT_SET_TOKEN = object()
_TRAVERSAL_BOUNDARY_TOKEN = object()
_CLAIM_STATE_TOKEN = object()
_OUTCOME_CLAIM_STATE_TOKEN = object()


class _TraversalAssignmentClaimState:
    __slots__ = ("__cursor", "__lock")

    def __init__(self, *, _construction_token: object) -> None:
        if _construction_token is not _CLAIM_STATE_TOKEN:
            raise ValueError
        self.__lock = Lock()
        self.__cursor = 0

    def claim_next(self, assignment_count: int) -> int:
        with self.__lock:
            if self.__cursor >= assignment_count:
                raise ValueError
            ordinal = self.__cursor
            self.__cursor += 1
            return ordinal

    def remaining(self, assignment_count: int) -> int:
        with self.__lock:
            return assignment_count - self.__cursor


class _TraversalOutcomeClaimState:
    __slots__ = ("__claimed", "__lock")

    def __init__(self, *, _construction_token: object) -> None:
        if _construction_token is not _OUTCOME_CLAIM_STATE_TOKEN:
            raise ValueError
        self.__lock = Lock()
        self.__claimed = False

    def claim(self) -> None:
        with self.__lock:
            if self.__claimed:
                raise ValueError
            self.__claimed = True


@dataclass(frozen=True)
class OwnedReviewSliceTraversalAssignments:
    """Private D-stage exact assignments; no traversal result or Slice authority."""

    derivation_id: str
    admission_witness_digest: str
    slice_obligation_domain_digest: str
    assignment_digests: tuple[str, ...]
    _slice_spec_bytes: tuple[bytes, ...] = field(repr=False, compare=False)
    _gate: OwnedReviewSliceObligationDomainGate = field(repr=False, compare=False)
    _claim_state: _TraversalAssignmentClaimState = field(repr=False, compare=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        gate: OwnedReviewSliceObligationDomainGate,
        obligations: list[dict[str, object]],
    ) -> "OwnedReviewSliceTraversalAssignments":
        domain_digest = gate.slice_obligation_domain_digest
        if not isinstance(domain_digest, str):
            raise ValueError
        spec_bytes = tuple(canonical_json_bytes(item) for item in obligations)
        assignment_digests = tuple(
            _assignment_digest(
                derivation_id=gate.derivation_id,
                admission_witness_digest=gate.admission_witness_digest,
                slice_obligation_domain_digest=domain_digest,
                assignment_ordinal=ordinal,
                slice_spec_digest=spec["slice_spec_digest"],
            )
            for ordinal, spec in enumerate(obligations)
        )
        values = {
            "derivation_id": gate.derivation_id,
            "admission_witness_digest": gate.admission_witness_digest,
            "slice_obligation_domain_digest": domain_digest,
            "assignment_digests": assignment_digests,
            "_slice_spec_bytes": spec_bytes,
            "_gate": gate,
        }
        return cls(
            **values,
            _claim_state=_TraversalAssignmentClaimState(
                _construction_token=_CLAIM_STATE_TOKEN
            ),
            _state_seal=_assignment_set_state_seal(values),
            _construction_token=_ASSIGNMENT_SET_TOKEN,
        )

    @property
    def assignment_count(self) -> int:
        return len(self.assignment_digests)

    def remaining_assignment_count(self) -> int:
        return self._claim_state.remaining(self.assignment_count)

    def continuation_permitted(self) -> bool:
        return self._gate.continuation_permitted()

    def _claim_next(self) -> tuple[int, str, bytes]:
        ordinal = self._claim_state.claim_next(self.assignment_count)
        return (
            ordinal,
            self.assignment_digests[ordinal],
            self._slice_spec_bytes[ordinal],
        )

    def _owned_domain_gate(self) -> OwnedReviewSliceObligationDomainGate:
        return self._gate

    def _claim_normal_reconciliation(self) -> None:
        validated = self._gate._owned_cross_validated_input()
        validated._owned_joined_input()._claim_normal_reconciliation()

    def _try_complete_obligation_closure(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        validated = self._gate._owned_cross_validated_input()
        return validated._owned_joined_input()._try_complete_obligation_closure(
            canonical_bytes
        )

    def _claim_closed_empty_reconciliation(self) -> None:
        validated = self._gate._owned_cross_validated_input()
        validated._owned_joined_input()._claim_closed_empty_reconciliation()

    def _try_complete_closed_empty_obligation_closure(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        validated = self._gate._owned_cross_validated_input()
        return (
            validated._owned_joined_input()
            ._try_complete_closed_empty_obligation_closure(canonical_bytes)
        )


@dataclass(frozen=True)
class OwnedReviewSliceTraversalBoundary:
    """Private D-stage traversal input; no outcome, frontier, or Slice authority."""

    derivation_id: str
    admission_witness_digest: str
    slice_obligation_domain_digest: str
    assignment_ordinal: int
    assignment_digest: str
    slice_spec_digest: str
    traversal_algorithm: str
    traversal_request_bytes: bytes = field(repr=False)
    _assignments: OwnedReviewSliceTraversalAssignments = field(
        repr=False, compare=False
    )
    _outcome_claim_state: _TraversalOutcomeClaimState = field(
        repr=False, compare=False
    )
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        assignments: OwnedReviewSliceTraversalAssignments,
        assignment_ordinal: int,
        assignment_digest: str,
        slice_spec_bytes: bytes,
    ) -> "OwnedReviewSliceTraversalBoundary":
        gate = assignments._owned_domain_gate()
        validated = gate._owned_cross_validated_input()
        spec = _object(slice_spec_bytes)
        profile = validated.derivation_profile_document_copy()
        traversal_rules = profile.get("traversal_rules")
        if not isinstance(traversal_rules, Mapping):
            raise ValueError
        traversal_algorithm = traversal_rules.get("algorithm")
        if traversal_algorithm != "breadth-first/1":
            raise ValueError
        request = {
            "request_kind": "REVIEW_SLICE_TRAVERSAL",
            "protocol_version": "0.1",
            "derivation_id": assignments.derivation_id,
            "admission_witness_digest": assignments.admission_witness_digest,
            "slice_obligation_domain_digest": (
                assignments.slice_obligation_domain_digest
            ),
            "assignment_ordinal": assignment_ordinal,
            "assignment_digest": assignment_digest,
            "slice_spec": spec,
            "traversal_rules": copy.deepcopy(dict(traversal_rules)),
            "fact_set": validated.fact_set_document_copy(),
            "relation_set": validated.relation_set_document_copy(),
        }
        request_bytes = canonical_json_bytes(request)
        values = {
            "derivation_id": assignments.derivation_id,
            "admission_witness_digest": assignments.admission_witness_digest,
            "slice_obligation_domain_digest": (
                assignments.slice_obligation_domain_digest
            ),
            "assignment_ordinal": assignment_ordinal,
            "assignment_digest": assignment_digest,
            "slice_spec_digest": spec["slice_spec_digest"],
            "traversal_algorithm": traversal_algorithm,
            "traversal_request_bytes": request_bytes,
            "_assignments": assignments,
        }
        return cls(
            **values,
            _outcome_claim_state=_TraversalOutcomeClaimState(
                _construction_token=_OUTCOME_CLAIM_STATE_TOKEN
            ),
            _state_seal=_traversal_boundary_state_seal(values),
            _construction_token=_TRAVERSAL_BOUNDARY_TOKEN,
        )

    def traversal_request_copy(self) -> dict[str, object]:
        return _object(self.traversal_request_bytes)

    def continuation_permitted(self) -> bool:
        return self._assignments.continuation_permitted()

    def _owned_assignments(self) -> OwnedReviewSliceTraversalAssignments:
        return self._assignments

    def _claim_outcome(self) -> None:
        self._outcome_claim_state.claim()

    def _try_complete_outcome(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        gate = self._assignments._owned_domain_gate()
        validated = gate._owned_cross_validated_input()
        joined = validated._owned_joined_input()
        return joined._try_complete_traversal_outcome(canonical_bytes)


def _validate_traversal_assignments(
    value: OwnedReviewSliceTraversalAssignments,
) -> None:
    if (
        type(value) is not OwnedReviewSliceTraversalAssignments
        or value._construction_token is not _ASSIGNMENT_SET_TOKEN
    ):
        raise ValueError
    gate = value._owned_domain_gate()
    _validate_obligation_domain_gate(gate)
    obligations = gate.obligations_copy()
    if (
        obligations is None
        or not gate.continuation_permitted()
        or value.derivation_id != gate.derivation_id
        or value.admission_witness_digest != gate.admission_witness_digest
        or value.slice_obligation_domain_digest
        != gate.slice_obligation_domain_digest
    ):
        raise ValueError
    expected_spec_bytes = tuple(canonical_json_bytes(item) for item in obligations)
    expected_digests = tuple(
        _assignment_digest(
            derivation_id=value.derivation_id,
            admission_witness_digest=value.admission_witness_digest,
            slice_obligation_domain_digest=value.slice_obligation_domain_digest,
            assignment_ordinal=ordinal,
            slice_spec_digest=spec["slice_spec_digest"],
        )
        for ordinal, spec in enumerate(obligations)
    )
    values = {
        "derivation_id": value.derivation_id,
        "admission_witness_digest": value.admission_witness_digest,
        "slice_obligation_domain_digest": value.slice_obligation_domain_digest,
        "assignment_digests": value.assignment_digests,
        "_slice_spec_bytes": value._slice_spec_bytes,
        "_gate": value._gate,
    }
    if (
        value._state_seal != _assignment_set_state_seal(values)
        or value._slice_spec_bytes != expected_spec_bytes
        or value.assignment_digests != expected_digests
        or len(value.assignment_digests) != len(set(value.assignment_digests))
    ):
        raise ValueError


def _validate_traversal_boundary(
    value: OwnedReviewSliceTraversalBoundary,
) -> None:
    if (
        type(value) is not OwnedReviewSliceTraversalBoundary
        or value._construction_token is not _TRAVERSAL_BOUNDARY_TOKEN
        or type(value._outcome_claim_state) is not _TraversalOutcomeClaimState
    ):
        raise ValueError
    assignments = value._owned_assignments()
    _validate_traversal_assignments(assignments)
    if (
        not value.continuation_permitted()
        or value.assignment_ordinal < 0
        or value.assignment_ordinal >= assignments.assignment_count
        or value.assignment_digest
        != assignments.assignment_digests[value.assignment_ordinal]
    ):
        raise ValueError
    request = value.traversal_request_copy()
    gate = assignments._owned_domain_gate()
    validated = gate._owned_cross_validated_input()
    profile = validated.derivation_profile_document_copy()
    slice_spec = request.get("slice_spec")
    if not isinstance(slice_spec, Mapping):
        raise ValueError
    expected_fields = {
        "request_kind",
        "protocol_version",
        "derivation_id",
        "admission_witness_digest",
        "slice_obligation_domain_digest",
        "assignment_ordinal",
        "assignment_digest",
        "slice_spec",
        "traversal_rules",
        "fact_set",
        "relation_set",
    }
    if (
        set(request) != expected_fields
        or request["request_kind"] != "REVIEW_SLICE_TRAVERSAL"
        or request["protocol_version"] != "0.1"
        or request["derivation_id"] != value.derivation_id
        or request["admission_witness_digest"]
        != value.admission_witness_digest
        or request["slice_obligation_domain_digest"]
        != value.slice_obligation_domain_digest
        or request["assignment_ordinal"] != value.assignment_ordinal
        or request["assignment_digest"] != value.assignment_digest
        or canonical_json_bytes(slice_spec)
        != assignments._slice_spec_bytes[value.assignment_ordinal]
        or request["traversal_rules"] != profile["traversal_rules"]
        or request["fact_set"] != validated.fact_set_document_copy()
        or request["relation_set"] != validated.relation_set_document_copy()
        or slice_spec.get("slice_spec_digest")
        != value.slice_spec_digest
        or value.traversal_algorithm != "breadth-first/1"
    ):
        raise ValueError
    values = {
        "derivation_id": value.derivation_id,
        "admission_witness_digest": value.admission_witness_digest,
        "slice_obligation_domain_digest": value.slice_obligation_domain_digest,
        "assignment_ordinal": value.assignment_ordinal,
        "assignment_digest": value.assignment_digest,
        "slice_spec_digest": value.slice_spec_digest,
        "traversal_algorithm": value.traversal_algorithm,
        "traversal_request_bytes": value.traversal_request_bytes,
        "_assignments": value._assignments,
    }
    if (
        value._state_seal != _traversal_boundary_state_seal(values)
        or canonical_json_bytes(request) != value.traversal_request_bytes
    ):
        raise ValueError


def _assignment_digest(
    *,
    derivation_id: str,
    admission_witness_digest: str,
    slice_obligation_domain_digest: str,
    assignment_ordinal: int,
    slice_spec_digest: object,
) -> str:
    if not isinstance(slice_spec_digest, str):
        raise ValueError
    return semantic_digest(
        "veritrail.review.private-slice-obligation-assignment/0.1",
        {
            "derivation_id": derivation_id,
            "admission_witness_digest": admission_witness_digest,
            "slice_obligation_domain_digest": slice_obligation_domain_digest,
            "assignment_ordinal": assignment_ordinal,
            "slice_spec_digest": slice_spec_digest,
        },
    )


def _assignment_set_state_seal(values: Mapping[str, object]) -> str:
    spec_bytes = values["_slice_spec_bytes"]
    gate = values["_gate"]
    if (
        not isinstance(spec_bytes, tuple)
        or any(type(item) is not bytes for item in spec_bytes)
        or not isinstance(gate, OwnedReviewSliceObligationDomainGate)
    ):
        raise ValueError
    payload = {
        key: item
        for key, item in values.items()
        if key not in {"_slice_spec_bytes", "_gate"}
    }
    payload["slice_spec_byte_digests"] = [
        hashlib.sha256(item).hexdigest() for item in spec_bytes
    ]
    payload["gate"] = {
        "derivation_id": gate.derivation_id,
        "admission_witness_digest": gate.admission_witness_digest,
        "slice_obligation_domain_digest": gate.slice_obligation_domain_digest,
    }
    return semantic_digest(
        "veritrail.review.private-slice-traversal-assignments/0.1", payload
    )


def _traversal_boundary_state_seal(values: Mapping[str, object]) -> str:
    request_bytes = values["traversal_request_bytes"]
    assignments = values["_assignments"]
    if not isinstance(request_bytes, bytes) or not isinstance(
        assignments, OwnedReviewSliceTraversalAssignments
    ):
        raise ValueError
    payload = {
        key: item
        for key, item in values.items()
        if key not in {"traversal_request_bytes", "_assignments"}
    }
    payload["traversal_request_sha256"] = hashlib.sha256(
        request_bytes
    ).hexdigest()
    payload["assignments"] = {
        "derivation_id": assignments.derivation_id,
        "admission_witness_digest": assignments.admission_witness_digest,
        "slice_obligation_domain_digest": (
            assignments.slice_obligation_domain_digest
        ),
    }
    return semantic_digest(
        "veritrail.review.private-slice-traversal-boundary/0.1", payload
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned Slice traversal value is not an object")
    return value
