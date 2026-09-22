from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum


class _RelationSetAdmissionFailureCode(str, Enum):
    QUALIFICATION_REJECTED = "QUALIFICATION_REJECTED"
    RELATION_SET_REJECTED = "RELATION_SET_REJECTED"
    WITNESS_REJECTED = "WITNESS_REJECTED"
    EVIDENCE_PROJECTION_REJECTED = "EVIDENCE_PROJECTION_REJECTED"


_FAILURE_MESSAGES = {
    _RelationSetAdmissionFailureCode.QUALIFICATION_REJECTED: (
        "the owned Relation composition qualification is not admissible"
    ),
    _RelationSetAdmissionFailureCode.RELATION_SET_REJECTED: (
        "the exact qualified Relation membership cannot form a RelationSet"
    ),
    _RelationSetAdmissionFailureCode.WITNESS_REJECTED: (
        "the RelationSet admission witness is nonconformant"
    ),
    _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED: (
        "the admitted value cannot form DerivationEvidence 0.2"
    ),
}


class _RelationSetAdmissionError(RuntimeError):
    """Private, path-free failure for the non-published admission boundary."""

    def __init__(self, code: _RelationSetAdmissionFailureCode) -> None:
        self.code = code
        self.safe_message = _FAILURE_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")


@dataclass(frozen=True)
class OwnedRelationSetAdmissionState:
    """Private admitted value; it grants no staging or publication authority."""

    derivation_id: str
    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    slice_policy_digest: str
    derivation_profile_digest: str
    fact_set_digest: str
    observation_domain_digest: str
    qualification_digest: str
    candidate_composition_status: str
    relation_set_document_bytes: bytes
    canonical_relation_set_artifact_bytes: bytes
    relation_set_digest: str
    admission_witness_bytes: bytes
    admission_witness_digest: str
    request_provenance_bytes: bytes
    provider_run_bytes: tuple[bytes, ...]
    started_at: str
    finished_at: str
    admitted_relation_ids: tuple[str, ...]
    admitted_conflict_ids: tuple[str, ...]
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    def relation_set_document_copy(self) -> dict[str, object]:
        return _object(self.relation_set_document_bytes)

    def admission_witness_copy(self) -> dict[str, object]:
        return _object(self.admission_witness_bytes)

    def request_provenance_copy(self) -> dict[str, object]:
        return _object(self.request_provenance_bytes)

    def provider_runs_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object(raw) for raw in self.provider_run_bytes)


@dataclass(frozen=True)
class OwnedDerivationEvidence02Projection:
    """Private new-copy Evidence 0.2 projection; never a published Artifact."""

    document_bytes: bytes
    derivation_evidence_digest: str

    def document_copy(self) -> dict[str, object]:
        return _object(self.document_bytes)


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned admission value is not an object")
    return value
