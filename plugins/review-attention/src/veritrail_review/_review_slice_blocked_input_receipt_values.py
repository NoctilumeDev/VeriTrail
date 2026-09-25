from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Mapping

from veritrail_review._review_slice_obligation_domain_values import (
    OwnedReviewSliceObligationDomainGate,
    _validate_obligation_domain_gate,
)
from veritrail_review.budget import OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_BLOCKED_INPUT_RECEIPT_TOKEN = object()
_BLOCKED_BY_RELATION_CONFLICT = "BLOCKED_BY_RELATION_CONFLICT"
_REASON_CODES = ("PROVIDER_CONFLICT", "UPSTREAM_DENOMINATOR_UNKNOWN")


@dataclass(frozen=True)
class OwnedReviewSliceBlockedInputReceipt:
    """Private G-stage blocked receipt; no domain, Slice, or Coverage authority."""

    derivation_id: str
    admission_witness_digest: str
    receipt_status: str
    blocked_input_receipt_digest: str
    receipt_document_bytes: bytes = field(repr=False)
    _gate: OwnedReviewSliceObligationDomainGate = field(repr=False, compare=False)
    _committed_phase: OwnedPhaseResult = field(repr=False, compare=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        gate: OwnedReviewSliceObligationDomainGate,
        receipt_document: Mapping[str, object],
        committed_phase: OwnedPhaseResult,
    ) -> "OwnedReviewSliceBlockedInputReceipt":
        document_bytes = canonical_json_bytes(receipt_document)
        if (
            type(committed_phase) is not OwnedPhaseResult
            or committed_phase.canonical_bytes != document_bytes
        ):
            raise ValueError
        values = {
            "derivation_id": receipt_document["derivation_id"],
            "admission_witness_digest": receipt_document[
                "admission_witness_digest"
            ],
            "receipt_status": receipt_document["slice_input_status"],
            "blocked_input_receipt_digest": receipt_document[
                "blocked_input_receipt_digest"
            ],
            "receipt_document_bytes": document_bytes,
            "_gate": gate,
            "_committed_phase": committed_phase,
        }
        return cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_BLOCKED_INPUT_RECEIPT_TOKEN,
        )

    def receipt_document_copy(self) -> dict[str, object]:
        return _object(self.receipt_document_bytes)

    def reason_codes_copy(self) -> list[str]:
        reasons = self.receipt_document_copy()["reason_codes"]
        if not isinstance(reasons, list) or any(
            not isinstance(item, str) for item in reasons
        ):
            raise RuntimeError("owned blocked receipt lacks reason codes")
        return list(reasons)

    def _owned_domain_gate(self) -> OwnedReviewSliceObligationDomainGate:
        return self._gate


def _validate_blocked_input_receipt(
    value: OwnedReviewSliceBlockedInputReceipt,
) -> None:
    if (
        type(value) is not OwnedReviewSliceBlockedInputReceipt
        or value._construction_token is not _BLOCKED_INPUT_RECEIPT_TOKEN
    ):
        raise ValueError
    gate = value._owned_domain_gate()
    _validate_obligation_domain_gate(gate)
    validated = gate._owned_cross_validated_input()
    relation_set = validated.relation_set_document_copy()
    conflicts = relation_set.get("conflicts")
    if not isinstance(conflicts, list) or not conflicts:
        raise ValueError
    conflict_ids = [item.get("conflict_id") for item in conflicts]
    if any(not isinstance(item, str) for item in conflict_ids):
        raise ValueError

    document = value.receipt_document_copy()
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
        "candidate_composition_status",
        "slice_input_status",
        "slice_obligation_domain_digest",
        "slice_derivation_denominator_status",
        "reason_codes",
        "relation_conflict_ids",
        "normal_slice_candidates",
        "blocked_input_receipt_digest",
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
        )
        != (
            gate.derivation_id,
            gate.admission_witness_digest,
            validated.source_snapshot_digest,
            validated.policy_digest,
            validated.analysis_scope_digest,
            validated.slice_policy_digest,
            validated.derivation_profile_digest,
            validated.fact_set_digest,
            validated.relation_set_digest,
        )
        or document["candidate_composition_status"] != "CONFLICTING"
        or document["slice_input_status"] != _BLOCKED_BY_RELATION_CONFLICT
        or document["slice_obligation_domain_digest"] is not None
        or document["slice_derivation_denominator_status"] != "UNKNOWN"
        or document["reason_codes"] != list(_REASON_CODES)
        or document["relation_conflict_ids"] != conflict_ids
        or document["normal_slice_candidates"] != []
    ):
        raise ValueError
    payload = {
        key: copy.deepcopy(item)
        for key, item in document.items()
        if key != "blocked_input_receipt_digest"
    }
    if document["blocked_input_receipt_digest"] != semantic_digest(
        "veritrail.review.private-slice-blocked-input-receipt/0.1", payload
    ):
        raise ValueError
    values = {
        "derivation_id": value.derivation_id,
        "admission_witness_digest": value.admission_witness_digest,
        "receipt_status": value.receipt_status,
        "blocked_input_receipt_digest": value.blocked_input_receipt_digest,
        "receipt_document_bytes": value.receipt_document_bytes,
        "_gate": value._gate,
        "_committed_phase": value._committed_phase,
    }
    if (
        value._state_seal != _private_state_seal(values)
        or canonical_json_bytes(document) != value.receipt_document_bytes
        or value._committed_phase.canonical_bytes != value.receipt_document_bytes
        or value._committed_phase.phase_status != "COMPLETED_FOR_PHASE"
        or (
            value.derivation_id,
            value.admission_witness_digest,
            value.receipt_status,
            value.blocked_input_receipt_digest,
        )
        != (
            document["derivation_id"],
            document["admission_witness_digest"],
            document["slice_input_status"],
            document["blocked_input_receipt_digest"],
        )
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    raw = values["receipt_document_bytes"]
    gate = values["_gate"]
    committed = values["_committed_phase"]
    if (
        not isinstance(raw, bytes)
        or type(gate) is not OwnedReviewSliceObligationDomainGate
        or type(committed) is not OwnedPhaseResult
    ):
        raise ValueError
    payload = {
        key: item
        for key, item in values.items()
        if key not in {"receipt_document_bytes", "_gate", "_committed_phase"}
    }
    payload["receipt_document_sha256"] = hashlib.sha256(raw).hexdigest()
    payload["gate"] = {
        "derivation_id": gate.derivation_id,
        "admission_witness_digest": gate.admission_witness_digest,
        "candidate_composition_status": gate.candidate_composition_status,
        "slice_input_status": gate.slice_input_status,
    }
    payload["committed_phase"] = {
        "canonical_sha256": hashlib.sha256(committed.canonical_bytes).hexdigest(),
        "phase_status": committed.phase_status,
    }
    return semantic_digest(
        "veritrail.review.private-owned-slice-blocked-input-receipt/0.1",
        payload,
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned blocked Slice input receipt is not an object")
    return value
