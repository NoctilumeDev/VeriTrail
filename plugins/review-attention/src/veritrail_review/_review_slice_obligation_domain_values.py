from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Mapping

from veritrail_review._review_slice_input_cross_validation_values import (
    OwnedCrossValidatedAdmittedGraphSliceInput,
    _validate_cross_validated_input,
)
from veritrail_review.budget import OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_OBLIGATION_DOMAIN_GATE_TOKEN = object()
_ELIGIBLE = "ELIGIBLE"
_BLOCKED_BY_RELATION_CONFLICT = "BLOCKED_BY_RELATION_CONFLICT"


@dataclass(frozen=True)
class OwnedReviewSliceObligationDomainGate:
    """Private C-stage conflict gate and exact denominator; no Slice authority."""

    derivation_id: str
    admission_witness_digest: str
    candidate_composition_status: str
    slice_input_status: str
    slice_obligation_domain_digest: str | None
    obligation_domain_document_bytes: bytes | None = field(repr=False)
    _validated: OwnedCrossValidatedAdmittedGraphSliceInput = field(
        repr=False, compare=False
    )
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        validated: OwnedCrossValidatedAdmittedGraphSliceInput,
        candidate_composition_status: str,
        slice_input_status: str,
        obligation_domain_document: Mapping[str, object] | None,
    ) -> "OwnedReviewSliceObligationDomainGate":
        if obligation_domain_document is None:
            domain_bytes = None
            domain_digest = None
        else:
            domain_bytes = canonical_json_bytes(obligation_domain_document)
            domain_digest = obligation_domain_document[
                "slice_obligation_domain_digest"
            ]
            if not isinstance(domain_digest, str):
                raise ValueError
        values = {
            "derivation_id": validated.derivation_id,
            "admission_witness_digest": validated.admission_witness_digest,
            "candidate_composition_status": candidate_composition_status,
            "slice_input_status": slice_input_status,
            "slice_obligation_domain_digest": domain_digest,
            "obligation_domain_document_bytes": domain_bytes,
            "_validated": validated,
        }
        return cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_OBLIGATION_DOMAIN_GATE_TOKEN,
        )

    def obligation_domain_document_copy(self) -> dict[str, object] | None:
        if self.obligation_domain_document_bytes is None:
            return None
        value = json.loads(self.obligation_domain_document_bytes)
        if not isinstance(value, dict):
            raise RuntimeError("owned Slice obligation domain is not an object")
        return value

    def obligations_copy(self) -> list[dict[str, object]] | None:
        domain = self.obligation_domain_document_copy()
        if domain is None:
            return None
        obligations = domain["obligations"]
        if not isinstance(obligations, list):
            raise RuntimeError("owned Slice obligations are not an array")
        return copy.deepcopy(obligations)

    def continuation_permitted(self) -> bool:
        return (
            self.slice_input_status == _ELIGIBLE
            and self._validated.continuation_permitted()
        )

    def _owned_cross_validated_input(
        self,
    ) -> OwnedCrossValidatedAdmittedGraphSliceInput:
        return self._validated

    def _claim_traversal_assignments(self) -> None:
        self._validated._claim_traversal_assignments()

    def _claim_blocked_input_receipt(self) -> None:
        self._validated._claim_blocked_input_receipt()

    def _try_complete_blocked_input_receipt(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        return self._validated._try_complete_blocked_input_receipt(canonical_bytes)


def _validate_obligation_domain_gate(
    value: OwnedReviewSliceObligationDomainGate,
) -> None:
    if (
        type(value) is not OwnedReviewSliceObligationDomainGate
        or value._construction_token is not _OBLIGATION_DOMAIN_GATE_TOKEN
    ):
        raise ValueError
    _validate_cross_validated_input(value._validated)
    values = {
        field_name: getattr(value, field_name)
        for field_name in (
            "derivation_id",
            "admission_witness_digest",
            "candidate_composition_status",
            "slice_input_status",
            "slice_obligation_domain_digest",
            "obligation_domain_document_bytes",
            "_validated",
        )
    }
    relation_set = value._validated.relation_set_document_copy()
    witness = value._validated.admission_witness_copy()
    claim = witness.get("qualification_claim")
    conflicts = relation_set.get("conflicts")
    if (
        value._state_seal != _private_state_seal(values)
        or value.derivation_id != value._validated.derivation_id
        or value.admission_witness_digest
        != value._validated.admission_witness_digest
        or not isinstance(claim, Mapping)
        or not isinstance(conflicts, list)
        or claim.get("candidate_composition_status")
        != value.candidate_composition_status
    ):
        raise ValueError

    if value.slice_input_status == _BLOCKED_BY_RELATION_CONFLICT:
        if (
            value.candidate_composition_status != "CONFLICTING"
            or not conflicts
            or value.slice_obligation_domain_digest is not None
            or value.obligation_domain_document_bytes is not None
            or value.continuation_permitted()
        ):
            raise ValueError
        return

    if (
        value.slice_input_status != _ELIGIBLE
        or value.candidate_composition_status != "CONSISTENT"
        or conflicts
        or type(value.obligation_domain_document_bytes) is not bytes
        or not isinstance(value.slice_obligation_domain_digest, str)
        or not value.continuation_permitted()
    ):
        raise ValueError
    document = value.obligation_domain_document_copy()
    if document is None:
        raise ValueError
    _validate_domain_document(document, value._validated)
    if (
        canonical_json_bytes(document) != value.obligation_domain_document_bytes
        or document["slice_obligation_domain_digest"]
        != value.slice_obligation_domain_digest
    ):
        raise ValueError


def _validate_domain_document(
    document: Mapping[str, object],
    validated: OwnedCrossValidatedAdmittedGraphSliceInput,
) -> None:
    expected_fields = {
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "fact_set_digest",
        "relation_set_digest",
        "obligations",
        "slice_obligation_domain_digest",
    }
    if set(document) != expected_fields:
        raise ValueError
    coordinates = (
        document["source_snapshot_digest"],
        document["policy_digest"],
        document["analysis_scope_digest"],
        document["slice_policy_digest"],
        document["derivation_profile_digest"],
        document["fact_set_digest"],
        document["relation_set_digest"],
    )
    if coordinates != (
        validated.source_snapshot_digest,
        validated.policy_digest,
        validated.analysis_scope_digest,
        validated.slice_policy_digest,
        validated.derivation_profile_digest,
        validated.fact_set_digest,
        validated.relation_set_digest,
    ):
        raise ValueError
    obligations = document["obligations"]
    if not isinstance(obligations, list):
        raise ValueError
    digests: list[str] = []
    for spec in obligations:
        if not isinstance(spec, Mapping):
            raise ValueError
        _validate_spec(spec, validated)
        digests.append(spec["slice_spec_digest"])  # type: ignore[arg-type]
    if len(digests) != len(set(digests)):
        raise ValueError
    expected_digest = semantic_digest(
        "veritrail.review.slice-obligation-domain/0.1",
        {
            "source_snapshot_digest": document["source_snapshot_digest"],
            "analysis_scope_digest": document["analysis_scope_digest"],
            "slice_policy_digest": document["slice_policy_digest"],
            "derivation_profile_digest": document["derivation_profile_digest"],
            "fact_set_digest": document["fact_set_digest"],
            "relation_set_digest": document["relation_set_digest"],
            "obligations": copy.deepcopy(obligations),
        },
    )
    if document["slice_obligation_domain_digest"] != expected_digest:
        raise ValueError


def _validate_spec(
    spec: Mapping[str, object],
    validated: OwnedCrossValidatedAdmittedGraphSliceInput,
) -> None:
    expected_fields = {
        "source_snapshot_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "fact_set_digest",
        "relation_set_digest",
        "anchor_fact_id",
        "allowed_relations",
        "max_depth",
        "max_symbols",
        "max_files",
        "max_relations",
        "slice_spec_digest",
    }
    if set(spec) != expected_fields:
        raise ValueError
    if (
        spec["source_snapshot_digest"] != validated.source_snapshot_digest
        or spec["analysis_scope_digest"] != validated.analysis_scope_digest
        or spec["slice_policy_digest"] != validated.slice_policy_digest
        or spec["derivation_profile_digest"]
        != validated.derivation_profile_digest
        or spec["fact_set_digest"] != validated.fact_set_digest
        or spec["relation_set_digest"] != validated.relation_set_digest
        or not isinstance(spec["anchor_fact_id"], str)
        or not isinstance(spec["allowed_relations"], list)
    ):
        raise ValueError
    payload = {
        key: copy.deepcopy(item)
        for key, item in spec.items()
        if key != "slice_spec_digest"
    }
    if spec["slice_spec_digest"] != semantic_digest(
        "veritrail.review.slice-spec/0.1", payload
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    payload: dict[str, object] = {}
    for key, item in values.items():
        if isinstance(item, bytes):
            payload[key] = hashlib.sha256(item).hexdigest()
        elif key == "_validated":
            if not isinstance(item, OwnedCrossValidatedAdmittedGraphSliceInput):
                raise ValueError
            payload[key] = {
                "derivation_id": item.derivation_id,
                "qualification_digest": item.qualification_digest,
                "admission_witness_digest": item.admission_witness_digest,
                "relation_set_digest": item.relation_set_digest,
            }
        else:
            payload[key] = item
    return semantic_digest(
        "veritrail.review.private-slice-obligation-domain-gate/0.1", payload
    )
