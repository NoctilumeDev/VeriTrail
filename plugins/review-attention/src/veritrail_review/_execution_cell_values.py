from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum

from veritrail_review._execution_cell_binding import ProviderDescriptor


class ProviderRunStatus(str, Enum):
    COMPLETED = "COMPLETED"
    INTERRUPTED = "INTERRUPTED"
    FAILED = "FAILED"
    UNAVAILABLE = "UNAVAILABLE"


class PhaseStatus(str, Enum):
    COMPLETED = "COMPLETED"
    INTERRUPTED = "INTERRUPTED"
    FAILED = "FAILED"
    UNAVAILABLE = "UNAVAILABLE"


class ReleaseOutcome(str, Enum):
    RELEASED = "RELEASED"
    RELEASE_FAILED = "RELEASE_FAILED"


@dataclass(frozen=True)
class OwnedExecutionCellPhaseResult:
    """Copy-owned phase value; intentionally not a public R1 Artifact."""

    derivation_id: str
    request_provenance_bytes: bytes
    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    slice_policy_digest: str
    derivation_profile_digest: str
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
    canonical_fact_bytes: tuple[bytes, ...]
    reported_fact_ids: tuple[str, ...]
    reported_relation_ids: tuple[str, ...]
    release_outcome: ReleaseOutcome

    def request_provenance_copy(self) -> dict[str, object]:
        value = json.loads(self.request_provenance_bytes)
        if not isinstance(value, dict):
            raise RuntimeError("owned request provenance is not an object")
        return value

    def canonical_facts_copy(self) -> tuple[dict[str, object], ...]:
        result: list[dict[str, object]] = []
        for raw in self.canonical_fact_bytes:
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise RuntimeError("owned canonical Fact is not an object")
            result.append(value)
        return tuple(result)
