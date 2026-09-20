from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum

from veritrail_review._execution_cell_values import OwnedExecutionCellPhaseResult
from veritrail_review._relation_execution_cell_values import (
    OwnedRelationExecutionCellPhaseResult,
)


class _RelationDerivationFailureCode(str, Enum):
    INVALID_DERIVATION_REQUEST = "INVALID_DERIVATION_REQUEST"
    APPLICABILITY_BINDING_MISMATCH = "APPLICABILITY_BINDING_MISMATCH"
    DERIVATION_RUNTIME_UNAVAILABLE = "DERIVATION_RUNTIME_UNAVAILABLE"
    PARENT_DERIVATION_REVOKED = "PARENT_DERIVATION_REVOKED"
    DERIVATION_INTEGRITY_FAILURE = "DERIVATION_INTEGRITY_FAILURE"


_FAILURE_MESSAGES = {
    _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST: (
        "the private Relation derivation request is invalid"
    ),
    _RelationDerivationFailureCode.APPLICABILITY_BINDING_MISMATCH: (
        "the submitted bindings do not match the phase-classified closed table"
    ),
    _RelationDerivationFailureCode.DERIVATION_RUNTIME_UNAVAILABLE: (
        "the Relation derivation execution-cell runtime is unavailable"
    ),
    _RelationDerivationFailureCode.PARENT_DERIVATION_REVOKED: (
        "the parent Relation derivation is no longer eligible"
    ),
    _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE: (
        "the private Relation derivation failed integrity validation"
    ),
}


class _RelationDerivationError(RuntimeError):
    def __init__(self, code: _RelationDerivationFailureCode) -> None:
        self.code = code
        self.safe_message = _FAILURE_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")


@dataclass(frozen=True)
class OwnedRelationDerivationResult:
    """Private two-stage history; it grants no RelationSet or publication authority."""

    derivation_id: str
    request_provenance_bytes: bytes
    applicability_descriptor_bytes: tuple[bytes, ...]
    fact_phase_results: tuple[OwnedExecutionCellPhaseResult, ...]
    relation_phase_result: OwnedRelationExecutionCellPhaseResult | None
    fact_provider_run_bytes: tuple[bytes, ...]
    relation_provider_run_bytes: bytes | None
    final_provider_run_bytes: tuple[bytes, ...]
    fact_stage_status: str
    relation_start_status: str
    final_phase_status: str
    upstream_reason_codes: tuple[str, ...]
    canonical_fact_bytes: tuple[bytes, ...]
    canonical_conflict_bytes: tuple[bytes, ...]
    fact_set_document_bytes: bytes | None
    fact_set_digest: str | None
    canonical_relation_bytes: tuple[bytes, ...]

    def request_provenance_copy(self) -> dict[str, object]:
        return _object_copy(self.request_provenance_bytes)

    def applicability_descriptors_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.applicability_descriptor_bytes)

    def fact_provider_runs_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.fact_provider_run_bytes)

    def relation_provider_run_copy(self) -> dict[str, object] | None:
        if self.relation_provider_run_bytes is None:
            return None
        return _object_copy(self.relation_provider_run_bytes)

    def final_provider_runs_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.final_provider_run_bytes)

    def canonical_facts_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.canonical_fact_bytes)

    def canonical_conflicts_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.canonical_conflict_bytes)

    def fact_set_document_copy(self) -> dict[str, object] | None:
        if self.fact_set_document_bytes is None:
            return None
        return _object_copy(self.fact_set_document_bytes)

    def canonical_relations_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.canonical_relation_bytes)


def _object_copy(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned canonical value is not a JSON object")
    return value
