from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum

from veritrail_review._execution_cell_values import OwnedExecutionCellPhaseResult
from veritrail_review._fact_evidence_values import (
    OwnedDerivationEvidenceProjection,
    _DiagnosticClosureEligibility,
    _NormalContinuationEligibility,
)


class _MultiProviderCompositionFailureCode(str, Enum):
    INVALID_COMPOSITION_REQUEST = "INVALID_COMPOSITION_REQUEST"
    APPLICABILITY_BINDING_MISMATCH = "APPLICABILITY_BINDING_MISMATCH"
    DERIVATION_RUNTIME_UNAVAILABLE = "DERIVATION_RUNTIME_UNAVAILABLE"
    PARENT_COMPOSITION_REVOKED = "PARENT_COMPOSITION_REVOKED"
    COMPOSITION_INTEGRITY_FAILURE = "COMPOSITION_INTEGRITY_FAILURE"


_FAILURE_MESSAGES = {
    _MultiProviderCompositionFailureCode.INVALID_COMPOSITION_REQUEST: (
        "the private multi-Provider composition request is invalid"
    ),
    _MultiProviderCompositionFailureCode.APPLICABILITY_BINDING_MISMATCH: (
        "the submitted bindings do not match the closed applicability table"
    ),
    _MultiProviderCompositionFailureCode.DERIVATION_RUNTIME_UNAVAILABLE: (
        "the derivation execution-cell runtime is unavailable"
    ),
    _MultiProviderCompositionFailureCode.PARENT_COMPOSITION_REVOKED: (
        "the parent composition attempt is no longer eligible"
    ),
    _MultiProviderCompositionFailureCode.COMPOSITION_INTEGRITY_FAILURE: (
        "the private multi-Provider composition failed integrity validation"
    ),
}


class _MultiProviderCompositionError(RuntimeError):
    """Private, path-free failure for the closed conformance boundary."""

    def __init__(self, code: _MultiProviderCompositionFailureCode) -> None:
        self.code = code
        self.safe_message = _FAILURE_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")


@dataclass(frozen=True)
class OwnedMultiProviderFactCompositionResult:
    """Copy-owned private result with no path, writer, or Manifest authority."""

    derivation_id: str
    request_provenance_bytes: bytes
    applicability_descriptor_bytes: tuple[bytes, ...]
    phase_results: tuple[OwnedExecutionCellPhaseResult, ...]
    provider_run_bytes: tuple[bytes, ...]
    overall_execution_status: str
    diagnostic_bytes: tuple[bytes, ...]
    canonical_fact_bytes: tuple[bytes, ...]
    canonical_conflict_bytes: tuple[bytes, ...]
    fact_set_document_bytes: bytes | None
    canonical_fact_set_artifact_bytes: bytes | None
    fact_set_digest: str | None
    evidence_projection: OwnedDerivationEvidenceProjection | None
    _normal_continuation: _NormalContinuationEligibility | None = field(
        repr=False, compare=False
    )
    _diagnostic_closure: _DiagnosticClosureEligibility | None = field(
        repr=False, compare=False
    )

    def request_provenance_copy(self) -> dict[str, object]:
        return _object_copy(self.request_provenance_bytes)

    def applicability_descriptors_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.applicability_descriptor_bytes)

    def provider_runs_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.provider_run_bytes)

    def diagnostics_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.diagnostic_bytes)

    def canonical_facts_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.canonical_fact_bytes)

    def canonical_conflicts_copy(self) -> tuple[dict[str, object], ...]:
        return tuple(_object_copy(raw) for raw in self.canonical_conflict_bytes)

    def fact_set_document_copy(self) -> dict[str, object] | None:
        if self.fact_set_document_bytes is None:
            return None
        return _object_copy(self.fact_set_document_bytes)

    def normal_continuation_permitted(self) -> bool:
        return (
            self._normal_continuation is not None
            and self._normal_continuation.permits_continuation()
        )

    def diagnostic_closure_available(self) -> bool:
        return (
            self._diagnostic_closure is not None
            and self._diagnostic_closure.is_available()
        )


def _object_copy(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned canonical value is not a JSON object")
    return value
