from __future__ import annotations

import json
from dataclasses import dataclass

from veritrail_review._execution_cell_binding import ProviderDescriptor
from veritrail_review._execution_cell_values import (
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)


@dataclass(frozen=True)
class OwnedRelationObservationCellPhaseResult:
    """Copy-owned private 0.2 terminal; it grants no admission authority."""

    derivation_id: str
    request_provenance_bytes: bytes
    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    slice_policy_digest: str
    derivation_profile_digest: str
    fact_set_digest: str
    observation_domain_digest: str
    assigned_observation_item_ids: tuple[str, ...]
    provider_descriptor: ProviderDescriptor
    operands_digest: str
    provider_run_id: str
    attempt_started_at: str
    provider_run_started_at: str
    provider_run_finished_at: str
    phase_finished_at: str
    provider_run_status: ProviderRunStatus
    phase_status: PhaseStatus
    diagnostic_code: str | None
    canonical_relation_bytes: tuple[bytes, ...]
    observation_outcome_bytes: tuple[bytes, ...]
    reported_relation_ids: tuple[str, ...]
    release_outcome: ReleaseOutcome

    def canonical_relations_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object(raw) for raw in self.canonical_relation_bytes)

    def observation_outcomes_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object(raw) for raw in self.observation_outcome_bytes)


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned private value is not an object")
    return value
