from __future__ import annotations

import json
from dataclasses import dataclass

from veritrail_review._execution_cell_values import OwnedExecutionCellPhaseResult
from veritrail_review._relation_observation_cell_values import (
    OwnedRelationObservationCellPhaseResult,
)


@dataclass(frozen=True)
class OwnedRelationCompositionQualificationResult:
    """Private qualification history; never a RelationSet or public Artifact."""

    derivation_id: str
    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    slice_policy_digest: str
    derivation_profile_digest: str
    fact_set_digest: str
    observation_domain_digest: str
    observation_domain_bytes: bytes
    fact_phase_results: tuple[OwnedExecutionCellPhaseResult, ...]
    relation_phase_results: tuple[OwnedRelationObservationCellPhaseResult, ...]
    relation_provider_run_bytes: tuple[bytes, ...]
    observation_receipt_bytes: tuple[bytes, ...]
    required_source_set_terminal_closure: str
    required_observation_closure: str
    candidate_composition_status: str
    qualification_status: str
    merged_candidate_bytes: tuple[bytes, ...]
    private_conflict_bytes: tuple[bytes, ...]
    reason_codes: tuple[str, ...]
    qualification_digest: str

    def observation_domain_copy(self) -> dict[str, object]:
        return _object(self.observation_domain_bytes)

    def relation_provider_runs_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object(raw) for raw in self.relation_provider_run_bytes)

    def observation_receipts_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object(raw) for raw in self.observation_receipt_bytes)

    def merged_candidates_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object(raw) for raw in self.merged_candidate_bytes)

    def private_conflicts_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object(raw) for raw in self.private_conflict_bytes)


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned qualification value is not an object")
    return value
