from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock

from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
)
from veritrail_review._execution_cell_values import OwnedExecutionCellPhaseResult
from veritrail_review.budget import BudgetContext, BudgetState


class _FactEvidenceClosureFailureCode(str, Enum):
    FACT_ADMISSION_REJECTED = "FACT_ADMISSION_REJECTED"
    EVIDENCE_PROJECTION_REJECTED = "EVIDENCE_PROJECTION_REJECTED"
    DIAGNOSTIC_ELIGIBILITY_UNAVAILABLE = "DIAGNOSTIC_ELIGIBILITY_UNAVAILABLE"


_FAILURE_MESSAGES = {
    _FactEvidenceClosureFailureCode.FACT_ADMISSION_REJECTED: (
        "the completed Fact phase is not eligible for FactSet admission"
    ),
    _FactEvidenceClosureFailureCode.EVIDENCE_PROJECTION_REJECTED: (
        "the terminal phase cannot form the required Evidence projection"
    ),
    _FactEvidenceClosureFailureCode.DIAGNOSTIC_ELIGIBILITY_UNAVAILABLE: (
        "diagnostic closure eligibility is unavailable"
    ),
}


class _FactEvidenceClosureError(RuntimeError):
    """Private, path-free failure for the non-published closure boundary."""

    def __init__(self, code: _FactEvidenceClosureFailureCode) -> None:
        self.code = code
        self.safe_message = _FAILURE_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")


class _NormalContinuationEligibility:
    """Opaque reference to the same attempt and BudgetContext."""

    def __init__(
        self,
        *,
        context: BudgetContext,
        attempt_eligibility: AttemptEligibility,
    ) -> None:
        self.__context = context
        self.__attempt_eligibility = attempt_eligibility

    def permits_continuation(self) -> bool:
        return (
            self.__attempt_eligibility.state is AttemptEligibilityState.ADMITTED
            and self.__context.checkpoint()
            and self.__context.state is BudgetState.RUNNING
            and self.__context.stop_trigger is None
        )


@dataclass(frozen=True)
class OwnedFactSetConstructionState:
    """Owned canonical FactSet state with no path or publication authority."""

    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    derivation_profile_digest: str
    provider_run_id: str
    provider_run_phase_bytes: bytes
    canonical_fact_bytes: tuple[bytes, ...]
    fact_set_document_bytes: bytes
    canonical_fact_set_artifact_bytes: bytes
    fact_set_digest: str
    _normal_continuation: _NormalContinuationEligibility = field(
        repr=False, compare=False
    )

    def provider_run_phase_copy(self) -> dict[str, object]:
        return _object_copy(self.provider_run_phase_bytes)

    def canonical_facts_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(value) for value in self.canonical_fact_bytes)

    def fact_set_document_copy(self) -> dict[str, object]:
        return _object_copy(self.fact_set_document_bytes)

    def normal_continuation_permitted(self) -> bool:
        return self._normal_continuation.permits_continuation()


@dataclass(frozen=True)
class OwnedDerivationEvidenceProjection:
    """Owned final-outcome value; deliberately not a published Artifact."""

    document_bytes: bytes
    derivation_evidence_digest: str

    def document_copy(self) -> dict[str, object]:
        return _object_copy(self.document_bytes)


@dataclass(frozen=True)
class _DiagnosticClosureClaim:
    """Opaque one-shot claim; it is not an Artifact or Evidence identity."""

    _token: object = field(repr=False, compare=False)


class _DiagnosticClosureEligibility:
    """One-shot future-publication eligibility bound to the original context."""

    def __init__(
        self,
        *,
        context: BudgetContext,
        attempt_eligibility: AttemptEligibility,
    ) -> None:
        self.__context = context
        self.__attempt_eligibility = attempt_eligibility
        self.__lock = Lock()
        self.__consumed = False
        self.__revoked = False

    def is_available(self) -> bool:
        with self.__lock:
            return self.__available_locked()

    def claim(self) -> _DiagnosticClosureClaim:
        with self.__lock:
            if not self.__available_locked():
                self.__revoked = True
                raise _FactEvidenceClosureError(
                    _FactEvidenceClosureFailureCode.DIAGNOSTIC_ELIGIBILITY_UNAVAILABLE
                )
            self.__consumed = True
            return _DiagnosticClosureClaim(object())

    def revoke(self) -> None:
        with self.__lock:
            self.__revoked = True

    def __available_locked(self) -> bool:
        if self.__consumed or self.__revoked:
            return False
        if self.__attempt_eligibility.state is not AttemptEligibilityState.REVOKED:
            return False
        if not self.__context.checkpoint():
            self.__revoked = True
            return False
        available = (
            self.__context.state is BudgetState.RUNNING
            and self.__context.stop_trigger is None
            and self.__context.reserved_artifact_bytes == 0
        )
        if not available:
            self.__revoked = True
        return available


@dataclass(frozen=True)
class OwnedFactEvidenceClosureResult:
    """Private integrated result; exactly one closure branch is populated."""

    phase_result: OwnedExecutionCellPhaseResult
    fact_set_construction_state: OwnedFactSetConstructionState | None
    evidence_projection: OwnedDerivationEvidenceProjection | None
    diagnostic_closure_eligibility: _DiagnosticClosureEligibility | None


def _object_copy(value: bytes) -> dict[str, object]:
    document = json.loads(value)
    if not isinstance(document, dict):
        raise RuntimeError("owned canonical value is not a JSON object")
    return document
