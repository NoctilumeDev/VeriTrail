from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Mapping

from veritrail_review._review_slice_traversal_assignment_values import (
    OwnedReviewSliceTraversalBoundary,
    _validate_traversal_boundary,
)
from veritrail_review.budget import OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_TRAVERSAL_OUTCOME_TOKEN = object()
_NORMAL_OUTCOMES = {"NORMAL_COMPLETE", "NORMAL_PARTIAL"}
_FRONTIER_REASONS = (
    "DEPTH_LIMIT",
    "SYMBOL_LIMIT",
    "FILE_LIMIT",
    "RELATION_LIMIT",
)


@dataclass(frozen=True)
class OwnedReviewSliceTraversalOutcome:
    """Private E-stage normal outcome; no SliceSet or Coverage authority."""

    derivation_id: str
    admission_witness_digest: str
    slice_obligation_domain_digest: str
    assignment_ordinal: int
    assignment_digest: str
    slice_spec_digest: str
    outcome_status: str
    traversal_outcome_digest: str
    outcome_document_bytes: bytes = field(repr=False)
    _boundary: OwnedReviewSliceTraversalBoundary = field(
        repr=False, compare=False
    )
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        boundary: OwnedReviewSliceTraversalBoundary,
        outcome_document: Mapping[str, object],
        committed_phase: OwnedPhaseResult,
    ) -> "OwnedReviewSliceTraversalOutcome":
        document_bytes = canonical_json_bytes(outcome_document)
        if (
            type(committed_phase) is not OwnedPhaseResult
            or committed_phase.canonical_bytes != document_bytes
        ):
            raise ValueError
        values = {
            "derivation_id": outcome_document["derivation_id"],
            "admission_witness_digest": outcome_document[
                "admission_witness_digest"
            ],
            "slice_obligation_domain_digest": outcome_document[
                "slice_obligation_domain_digest"
            ],
            "assignment_ordinal": outcome_document["assignment_ordinal"],
            "assignment_digest": outcome_document["assignment_digest"],
            "slice_spec_digest": outcome_document["slice_spec_digest"],
            "outcome_status": outcome_document["outcome_status"],
            "traversal_outcome_digest": outcome_document[
                "traversal_outcome_digest"
            ],
            "outcome_document_bytes": document_bytes,
            "_boundary": boundary,
        }
        return cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_TRAVERSAL_OUTCOME_TOKEN,
        )

    def outcome_document_copy(self) -> dict[str, object]:
        return _object(self.outcome_document_bytes)

    def normal_slice_candidate_copy(self) -> dict[str, object]:
        document = self.outcome_document_copy()
        candidate = document["normal_slice_candidate"]
        if not isinstance(candidate, dict):
            raise RuntimeError("owned traversal outcome lacks a normal Slice")
        return copy.deepcopy(candidate)

    def _owned_boundary(self) -> OwnedReviewSliceTraversalBoundary:
        return self._boundary


def _validate_traversal_outcome(
    value: OwnedReviewSliceTraversalOutcome,
) -> None:
    if (
        type(value) is not OwnedReviewSliceTraversalOutcome
        or value._construction_token is not _TRAVERSAL_OUTCOME_TOKEN
    ):
        raise ValueError
    boundary = value._owned_boundary()
    _validate_traversal_boundary(boundary)
    document = value.outcome_document_copy()
    expected_fields = {
        "derivation_id",
        "admission_witness_digest",
        "slice_obligation_domain_digest",
        "assignment_ordinal",
        "assignment_digest",
        "slice_spec_digest",
        "outcome_status",
        "normal_slice_candidate",
        "traversal_outcome_digest",
    }
    if set(document) != expected_fields:
        raise ValueError
    coordinates = (
        document["derivation_id"],
        document["admission_witness_digest"],
        document["slice_obligation_domain_digest"],
        document["assignment_ordinal"],
        document["assignment_digest"],
        document["slice_spec_digest"],
    )
    if coordinates != (
        boundary.derivation_id,
        boundary.admission_witness_digest,
        boundary.slice_obligation_domain_digest,
        boundary.assignment_ordinal,
        boundary.assignment_digest,
        boundary.slice_spec_digest,
    ):
        raise ValueError
    status = document["outcome_status"]
    candidate = document["normal_slice_candidate"]
    if status not in _NORMAL_OUTCOMES or not isinstance(candidate, Mapping):
        raise ValueError
    _validate_normal_slice(candidate, boundary)
    frontier = candidate["frontier"]
    coverage_status = candidate["coverage_status"]
    if (
        (status == "NORMAL_COMPLETE" and (frontier or coverage_status != "COMPLETE"))
        or (
            status == "NORMAL_PARTIAL"
            and (not frontier or coverage_status != "PARTIAL")
        )
    ):
        raise ValueError
    payload = {
        key: copy.deepcopy(item)
        for key, item in document.items()
        if key != "traversal_outcome_digest"
    }
    if document["traversal_outcome_digest"] != semantic_digest(
        "veritrail.review.private-slice-traversal-outcome/0.1", payload
    ):
        raise ValueError
    values = {
        "derivation_id": value.derivation_id,
        "admission_witness_digest": value.admission_witness_digest,
        "slice_obligation_domain_digest": value.slice_obligation_domain_digest,
        "assignment_ordinal": value.assignment_ordinal,
        "assignment_digest": value.assignment_digest,
        "slice_spec_digest": value.slice_spec_digest,
        "outcome_status": value.outcome_status,
        "traversal_outcome_digest": value.traversal_outcome_digest,
        "outcome_document_bytes": value.outcome_document_bytes,
        "_boundary": value._boundary,
    }
    if (
        value._state_seal != _private_state_seal(values)
        or canonical_json_bytes(document) != value.outcome_document_bytes
        or (
            value.derivation_id,
            value.admission_witness_digest,
            value.slice_obligation_domain_digest,
            value.assignment_ordinal,
            value.assignment_digest,
            value.slice_spec_digest,
            value.outcome_status,
            value.traversal_outcome_digest,
        )
        != (
            *coordinates,
            status,
            document["traversal_outcome_digest"],
        )
    ):
        raise ValueError


def _validate_normal_slice(
    candidate: Mapping[str, object],
    boundary: OwnedReviewSliceTraversalBoundary,
) -> None:
    expected_fields = {
        "slice_id",
        "slice_spec",
        "included_fact_ids",
        "included_relation_ids",
        "frontier",
        "coverage_status",
    }
    if set(candidate) != expected_fields:
        raise ValueError
    request = boundary.traversal_request_copy()
    spec = candidate["slice_spec"]
    facts = candidate["included_fact_ids"]
    relations = candidate["included_relation_ids"]
    frontier = candidate["frontier"]
    if (
        not isinstance(spec, Mapping)
        or canonical_json_bytes(spec)
        != canonical_json_bytes(request["slice_spec"])
        or not isinstance(facts, list)
        or not isinstance(relations, list)
        or not isinstance(frontier, list)
        or facts != sorted(set(facts))
        or relations != sorted(set(relations))
        or spec["anchor_fact_id"] not in facts
    ):
        raise ValueError
    frontier_keys: set[tuple[object, object, object]] = set()
    for item in frontier:
        if not isinstance(item, Mapping) or set(item) != {
            "from_fact_id",
            "relation_id",
            "direction",
            "candidate_fact_id",
            "candidate_depth",
            "reason_codes",
        }:
            raise ValueError
        key = (item["from_fact_id"], item["relation_id"], item["direction"])
        reasons = item["reason_codes"]
        if (
            key in frontier_keys
            or item["direction"] not in {"OUTBOUND", "INBOUND"}
            or type(item["candidate_depth"]) is not int
            or item["candidate_depth"] < 0
            or not isinstance(reasons, list)
            or not reasons
            or reasons
            != [reason for reason in _FRONTIER_REASONS if reason in reasons]
            or len(reasons) != len(set(reasons))
        ):
            raise ValueError
        frontier_keys.add(key)
    expected_slice_id = semantic_digest(
        "veritrail.review.review-slice/0.1",
        {
            "slice_spec_digest": boundary.slice_spec_digest,
            "included_fact_ids": facts,
            "included_relation_ids": relations,
            "frontier": copy.deepcopy(frontier),
        },
    )
    if candidate["slice_id"] != expected_slice_id:
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    raw = values["outcome_document_bytes"]
    boundary = values["_boundary"]
    if not isinstance(raw, bytes) or not isinstance(
        boundary, OwnedReviewSliceTraversalBoundary
    ):
        raise ValueError
    payload = {
        key: item
        for key, item in values.items()
        if key not in {"outcome_document_bytes", "_boundary"}
    }
    payload["outcome_document_sha256"] = hashlib.sha256(raw).hexdigest()
    payload["boundary"] = {
        "derivation_id": boundary.derivation_id,
        "admission_witness_digest": boundary.admission_witness_digest,
        "slice_obligation_domain_digest": (
            boundary.slice_obligation_domain_digest
        ),
        "assignment_digest": boundary.assignment_digest,
    }
    return semantic_digest(
        "veritrail.review.private-owned-slice-traversal-outcome/0.1", payload
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned Slice traversal outcome is not an object")
    return value
