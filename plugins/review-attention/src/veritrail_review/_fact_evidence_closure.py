from __future__ import annotations

import copy
from typing import Callable, Mapping

from veritrail_review._execution_cell import (
    DEFAULT_TRANSPORT_LIMITS,
    _PreparedExecutionAttempt,
    _prepare_closed_test_execution_attempt,
    _run_prepared_closed_test_execution_attempt,
)
from veritrail_review._execution_cell_application import (
    _validate_fact_projection,
    provider_operands_digest,
    provider_run_id,
)
from veritrail_review._execution_cell_binding import ProviderBinding
from veritrail_review._execution_cell_protocol import (
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._execution_cell_values import (
    OwnedExecutionCellPhaseResult,
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
from veritrail_review._fact_evidence_values import (
    OwnedDerivationEvidenceProjection,
    OwnedFactEvidenceClosureResult,
    OwnedFactSetConstructionState,
    _DiagnosticClosureEligibility,
    _FactEvidenceClosureError,
    _FactEvidenceClosureFailureCode,
    _NormalContinuationEligibility,
)
from veritrail_review.budget import BudgetState
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


_FACT_KEYS = frozenset(
    {
        "fact_id",
        "subject_key_digest",
        "subject_space",
        "fact_kind",
        "source_snapshot_digest",
        "derivation_profile_digest",
        "source_anchor",
        "local_ordinal",
        "semantic_attributes",
        "provenance_refs",
    }
)
_EVIDENCE_KEYS = frozenset(
    {
        "artifact_kind",
        "schema_version",
        "canonicalization_profile",
        "derivation_id",
        "request_provenance",
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "provider_runs",
        "overall_execution_status",
        "started_at",
        "finished_at",
        "diagnostics",
        "derivation_evidence_digest",
    }
)
_RUN_KEYS = frozenset(
    {
        "provider_run_id",
        "capability_id",
        "provider_id",
        "provider_version",
        "parser_id",
        "parser_version",
        "runtime_id",
        "runtime_version",
        "operands_digest",
        "started_at",
        "finished_at",
        "execution_status",
        "reported_fact_ids",
        "reported_relation_ids",
        "diagnostics",
    }
)
_ACTIVE_TERMINAL_STATUS = {
    "PROVIDER_UNAVAILABLE": ("UNAVAILABLE", "UNAVAILABLE"),
    "PROVIDER_FAILED": ("FAILED", "FAILED"),
    "NONCONFORMANT_PROVIDER_OUTPUT": ("FAILED", "FAILED"),
    "INTERNAL_DERIVATION_ERROR": ("FAILED", "FAILED"),
    "EXECUTION_DEADLINE": ("INTERRUPTED", "INTERRUPTED"),
    "EXECUTION_CANCELLED": ("INTERRUPTED", "INTERRUPTED"),
    "EXECUTION_MEMORY_BUDGET": ("INTERRUPTED", "INTERRUPTED"),
}
_DIAGNOSTIC_ELIGIBLE_CODES = frozenset(
    {
        "PROVIDER_UNAVAILABLE",
        "PROVIDER_FAILED",
        "NONCONFORMANT_PROVIDER_OUTPUT",
        "INTERNAL_DERIVATION_ERROR",
    }
)


class _IntegratedFactEvidenceController:
    """Own the one attempt state across execution and non-published closure."""

    def __init__(self, prepared: _PreparedExecutionAttempt) -> None:
        self.__prepared = prepared
        self.__used = False

    def run(self) -> OwnedFactEvidenceClosureResult:
        if self.__used:
            raise _FactEvidenceClosureError(
                _FactEvidenceClosureFailureCode.FACT_ADMISSION_REJECTED
            )
        self.__used = True
        phase = _run_prepared_closed_test_execution_attempt(self.__prepared)
        if phase.phase_status is PhaseStatus.COMPLETED:
            continuation = _NormalContinuationEligibility(
                context=self.__prepared.context,
                attempt_eligibility=self.__prepared.eligibility,
            )
            try:
                fact_set = _admit_completed_fact_phase(
                    self.__prepared.inputs,
                    phase,
                    binding=self.__prepared.binding,
                    request_provenance=self.__prepared.request_provenance,
                    continuation=continuation,
                )
            except Exception:
                self.__prepared.eligibility.revoke()
                raise
            return OwnedFactEvidenceClosureResult(
                phase_result=phase,
                fact_set_construction_state=fact_set,
                evidence_projection=None,
                diagnostic_closure_eligibility=None,
            )

        try:
            _validate_phase_continuity(
                self.__prepared.inputs,
                phase,
                binding=self.__prepared.binding,
                request_provenance=self.__prepared.request_provenance,
            )
        except Exception as exc:
            self.__prepared.eligibility.revoke()
            raise _FactEvidenceClosureError(
                _FactEvidenceClosureFailureCode.EVIDENCE_PROJECTION_REJECTED
            ) from exc

        projection: OwnedDerivationEvidenceProjection | None = None
        diagnostic_eligibility: _DiagnosticClosureEligibility | None = None
        if phase.diagnostic_code in _DIAGNOSTIC_ELIGIBLE_CODES:
            diagnostic_eligibility = _diagnostic_eligibility(
                self.__prepared, phase
            )
            try:
                projection = _project_final_evidence_for_conformance(phase)
            except Exception:
                diagnostic_eligibility.revoke()
                raise
        return OwnedFactEvidenceClosureResult(
            phase_result=phase,
            fact_set_construction_state=None,
            evidence_projection=projection,
            diagnostic_closure_eligibility=diagnostic_eligibility,
        )


def run_closed_test_fact_evidence_closure(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None = None,
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
) -> OwnedFactEvidenceClosureResult:
    """Run the authorized private Fact/Evidence closure without file output."""

    prepared = _prepare_closed_test_execution_attempt(
        inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    return _IntegratedFactEvidenceController(prepared).run()


def _admit_completed_fact_phase(
    inputs: DerivationInputSet,
    phase: OwnedExecutionCellPhaseResult,
    *,
    binding: ProviderBinding,
    request_provenance: Mapping[str, object],
    continuation: _NormalContinuationEligibility,
) -> OwnedFactSetConstructionState:
    try:
        if (
            phase.phase_status is not PhaseStatus.COMPLETED
            or phase.provider_run_status is not ProviderRunStatus.COMPLETED
            or phase.release_outcome is not ReleaseOutcome.RELEASED
            or phase.diagnostic_code is not None
            or phase.reported_relation_ids != ()
            or not continuation.permits_continuation()
        ):
            raise ValueError
        _validate_phase_continuity(
            inputs,
            phase,
            binding=binding,
            request_provenance=request_provenance,
        )

        snapshot = inputs.source_snapshot_document_copy()
        policy = inputs.review_policy_document_copy()
        profile = inputs.derivation_profile_document_copy()
        inventory = {
            item["git_path"]["git_path_hex"]: item
            for item in snapshot["inventory"]
            if isinstance(item, dict)
            and isinstance(item.get("git_path"), dict)
            and item["git_path"].get("path_kind") == "GIT_PATH"
        }
        in_scope = {
            item["git_path"]["git_path_hex"]
            for item in policy["scope_decisions"]
            if item["disposition"] == "IN_SCOPE"
        }
        supported_entry_kinds = set(profile["supported_entry_kinds"])

        facts_by_id: dict[str, tuple[bytes, dict[str, object]]] = {}
        subject_to_fact_id: dict[str, str] = {}
        for raw in phase.canonical_fact_bytes:
            fact = _strict_owned_object(raw)
            if set(fact) != _FACT_KEYS or canonical_json_bytes(fact) != raw:
                raise ValueError
            _validate_admitted_fact(
                fact,
                phase=phase,
                inventory=inventory,
                in_scope=in_scope,
                supported_entry_kinds=supported_entry_kinds,
            )
            fact_id = fact["fact_id"]
            subject = fact["subject_key_digest"]
            if not isinstance(fact_id, str) or not isinstance(subject, str):
                raise ValueError
            previous_subject_fact = subject_to_fact_id.setdefault(subject, fact_id)
            if previous_subject_fact != fact_id:
                raise ValueError
            previous = facts_by_id.get(fact_id)
            if previous is not None and previous[0] != raw:
                raise ValueError
            facts_by_id[fact_id] = (memoryview(raw).tobytes(), copy.deepcopy(fact))

        admitted_ids = tuple(sorted(facts_by_id))
        if phase.reported_fact_ids != admitted_ids:
            raise ValueError
        admitted_facts = [facts_by_id[fact_id][1] for fact_id in admitted_ids]
        digest = semantic_digest(
            "veritrail.review.fact-set/0.1",
            {
                "source_snapshot_digest": inputs.source_snapshot_digest,
                "analysis_scope_digest": inputs.analysis_scope_digest,
                "derivation_profile_digest": inputs.derivation_profile_digest,
                "facts": [
                    {key: copy.deepcopy(value) for key, value in fact.items()
                     if key != "provenance_refs"}
                    for fact in admitted_facts
                ],
                "conflicts": [],
            },
        )
        document = {
            "artifact_kind": "FACT_SET",
            "schema_version": "0.1",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "policy_digest": inputs.policy_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            "facts": admitted_facts,
            "conflicts": [],
            "fact_set_digest": digest,
        }
        document_bytes = canonical_json_bytes(document)
        if not continuation.permits_continuation():
            raise ValueError
        provider_run = _provider_run_document(
            phase,
            execution_status="COMPLETED",
            reported_fact_ids=list(admitted_ids),
            diagnostics=[],
        )
        return OwnedFactSetConstructionState(
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=inputs.policy_digest,
            analysis_scope_digest=inputs.analysis_scope_digest,
            derivation_profile_digest=inputs.derivation_profile_digest,
            provider_run_id=phase.provider_run_id,
            provider_run_phase_bytes=canonical_json_bytes(provider_run),
            canonical_fact_bytes=tuple(
                facts_by_id[fact_id][0] for fact_id in admitted_ids
            ),
            fact_set_document_bytes=document_bytes,
            canonical_fact_set_artifact_bytes=document_bytes + b"\n",
            fact_set_digest=digest,
            _normal_continuation=continuation,
        )
    except _FactEvidenceClosureError:
        raise
    except Exception as exc:
        raise _FactEvidenceClosureError(
            _FactEvidenceClosureFailureCode.FACT_ADMISSION_REJECTED
        ) from exc


def _validate_admitted_fact(
    fact: Mapping[str, object],
    *,
    phase: OwnedExecutionCellPhaseResult,
    inventory: Mapping[str, Mapping[str, object]],
    in_scope: set[str],
    supported_entry_kinds: set[str],
) -> None:
    if (
        fact["source_snapshot_digest"] != phase.source_snapshot_digest
        or fact["derivation_profile_digest"] != phase.derivation_profile_digest
        or fact["provenance_refs"] != [phase.provider_run_id]
    ):
        raise ValueError
    anchor = fact["source_anchor"]
    if not isinstance(anchor, Mapping) or set(anchor) != {
        "git_path",
        "start_byte",
        "end_byte",
    }:
        raise ValueError
    path = anchor["git_path"]
    if (
        not isinstance(path, Mapping)
        or set(path) != {"path_kind", "git_path_hex"}
        or path["path_kind"] != "GIT_PATH"
        or not isinstance(path["git_path_hex"], str)
    ):
        raise ValueError
    path_hex = path["git_path_hex"]
    entry = inventory.get(path_hex)
    if (
        entry is None
        or path_hex not in in_scope
        or entry["entry_kind"] not in supported_entry_kinds
        or not bytes.fromhex(path_hex).endswith(b".py")
        or not isinstance(entry.get("content"), Mapping)
    ):
        raise ValueError
    size = entry["content"]["size_bytes"]
    if type(size) is not int:
        raise ValueError
    _validate_fact_projection(
        subject_space=fact["subject_space"],
        fact_kind=fact["fact_kind"],
        anchor_start=anchor["start_byte"],
        anchor_end=anchor["end_byte"],
        blob_size=size,
        ordinal=fact["local_ordinal"],
        attributes=fact["semantic_attributes"],
    )
    expected_subject = semantic_digest(
        "veritrail.review.fact-subject/0.1",
        {
            "source_snapshot_digest": phase.source_snapshot_digest,
            "derivation_profile_digest": phase.derivation_profile_digest,
            "source_anchor": copy.deepcopy(dict(anchor)),
            "subject_space": fact["subject_space"],
            "local_ordinal": fact["local_ordinal"],
        },
    )
    expected_fact = semantic_digest(
        "veritrail.review.code-fact/0.1",
        {
            "subject_key_digest": expected_subject,
            "fact_kind": fact["fact_kind"],
            "semantic_attributes": copy.deepcopy(fact["semantic_attributes"]),
        },
    )
    if (
        fact["subject_key_digest"] != expected_subject
        or fact["fact_id"] != expected_fact
    ):
        raise ValueError


def _validate_phase_continuity(
    inputs: DerivationInputSet,
    phase: OwnedExecutionCellPhaseResult,
    *,
    binding: ProviderBinding,
    request_provenance: Mapping[str, object],
) -> None:
    if not isinstance(phase, OwnedExecutionCellPhaseResult):
        raise ValueError
    if (
        phase.provider_descriptor != binding.descriptor
        or phase.request_provenance_copy() != dict(request_provenance)
        or phase.source_snapshot_digest != inputs.source_snapshot_digest
        or phase.policy_digest != inputs.policy_digest
        or phase.analysis_scope_digest != inputs.analysis_scope_digest
        or phase.slice_policy_digest != inputs.slice_policy_digest
        or phase.derivation_profile_digest != inputs.derivation_profile_digest
    ):
        raise ValueError
    expected_operands = provider_operands_digest(inputs, binding.descriptor)
    expected_run_id = provider_run_id(
        phase.derivation_id, binding.descriptor, expected_operands
    )
    if (
        phase.operands_digest != expected_operands
        or phase.provider_run_id != expected_run_id
    ):
        raise ValueError


def _project_final_evidence_for_conformance(
    phase: OwnedExecutionCellPhaseResult,
    *,
    terminal_code: str | None = None,
) -> OwnedDerivationEvidenceProjection:
    """Build a non-published projection; this function grants no staging right."""

    try:
        code = phase.diagnostic_code if terminal_code is None else terminal_code
        if phase.release_outcome is not ReleaseOutcome.RELEASED or not isinstance(
            code, str
        ):
            raise ValueError
        if code == "EXECUTION_ARTIFACT_BUDGET":
            if (
                phase.phase_status is not PhaseStatus.COMPLETED
                or phase.provider_run_status is not ProviderRunStatus.COMPLETED
            ):
                raise ValueError
            run_status = "COMPLETED"
            overall_status = "INTERRUPTED"
            run_diagnostics: list[dict[str, object]] = []
            top_diagnostics = [
                {"diagnostic_code": code, "subject_ref": None}
            ]
        else:
            expected = _ACTIVE_TERMINAL_STATUS.get(code)
            if expected is None or terminal_code is not None:
                raise ValueError
            run_status, overall_status = expected
            if (
                phase.provider_run_status.value != run_status
                or phase.phase_status.value != overall_status
            ):
                raise ValueError
            diagnostic = {
                "diagnostic_code": code,
                "subject_ref": {
                    "ref_kind": "PROVIDER_RUN",
                    "provider_run_id": phase.provider_run_id,
                },
            }
            run_diagnostics = [copy.deepcopy(diagnostic)]
            top_diagnostics = [copy.deepcopy(diagnostic)]

        run = _provider_run_document(
            phase,
            execution_status=run_status,
            reported_fact_ids=[],
            diagnostics=run_diagnostics,
        )
        document: dict[str, object] = {
            "artifact_kind": "DERIVATION_EVIDENCE",
            "schema_version": "0.1.1",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "derivation_id": phase.derivation_id,
            "request_provenance": phase.request_provenance_copy(),
            "source_snapshot_digest": phase.source_snapshot_digest,
            "policy_digest": phase.policy_digest,
            "analysis_scope_digest": phase.analysis_scope_digest,
            "slice_policy_digest": phase.slice_policy_digest,
            "derivation_profile_digest": phase.derivation_profile_digest,
            "provider_runs": [run],
            "overall_execution_status": overall_status,
            "started_at": phase.attempt_started_at,
            "finished_at": phase.phase_finished_at,
            "diagnostics": top_diagnostics,
        }
        digest = semantic_digest(
            "veritrail.review.derivation-evidence/0.1", document
        )
        document["derivation_evidence_digest"] = digest
        _validate_final_evidence_projection(document, phase)
        return OwnedDerivationEvidenceProjection(
            document_bytes=canonical_json_bytes(document),
            derivation_evidence_digest=digest,
        )
    except _FactEvidenceClosureError:
        raise
    except Exception as exc:
        raise _FactEvidenceClosureError(
            _FactEvidenceClosureFailureCode.EVIDENCE_PROJECTION_REJECTED
        ) from exc


def _validate_final_evidence_projection(
    document: Mapping[str, object], phase: OwnedExecutionCellPhaseResult
) -> None:
    try:
        if set(document) != _EVIDENCE_KEYS:
            raise ValueError
        if (
            document["artifact_kind"] != "DERIVATION_EVIDENCE"
            or document["schema_version"] != "0.1.1"
            or document["canonicalization_profile"] != "veritrail-json-c14n/1"
            or document["derivation_id"] != phase.derivation_id
            or document["request_provenance"] != phase.request_provenance_copy()
            or document["source_snapshot_digest"] != phase.source_snapshot_digest
            or document["policy_digest"] != phase.policy_digest
            or document["analysis_scope_digest"] != phase.analysis_scope_digest
            or document["slice_policy_digest"] != phase.slice_policy_digest
            or document["derivation_profile_digest"]
            != phase.derivation_profile_digest
            or document["started_at"] != phase.attempt_started_at
            or document["finished_at"] != phase.phase_finished_at
        ):
            raise ValueError
        runs = document["provider_runs"]
        if not isinstance(runs, list) or len(runs) != 1:
            raise ValueError
        run = runs[0]
        if not isinstance(run, Mapping) or set(run) != _RUN_KEYS:
            raise ValueError
        expected_descriptor = phase.provider_descriptor.document()
        if (
            run["provider_run_id"] != phase.provider_run_id
            or any(run[key] != value for key, value in expected_descriptor.items())
            or run["operands_digest"] != phase.operands_digest
            or run["started_at"] != phase.provider_run_started_at
            or run["finished_at"] != phase.provider_run_finished_at
            or run["reported_fact_ids"] != []
            or run["reported_relation_ids"] != []
        ):
            raise ValueError
        top = document["diagnostics"]
        local = run["diagnostics"]
        if not isinstance(top, list) or not isinstance(local, list):
            raise ValueError
        if top == [
            {"diagnostic_code": "EXECUTION_ARTIFACT_BUDGET", "subject_ref": None}
        ]:
            if (
                document["overall_execution_status"] != "INTERRUPTED"
                or run["execution_status"] != "COMPLETED"
                or local != []
                or phase.phase_status is not PhaseStatus.COMPLETED
                or phase.provider_run_status is not ProviderRunStatus.COMPLETED
            ):
                raise ValueError
        else:
            code = phase.diagnostic_code
            expected_status = _ACTIVE_TERMINAL_STATUS.get(code or "")
            expected_diagnostic = {
                "diagnostic_code": code,
                "subject_ref": {
                    "ref_kind": "PROVIDER_RUN",
                    "provider_run_id": phase.provider_run_id,
                },
            }
            if (
                expected_status is None
                or local != [expected_diagnostic]
                or top != [expected_diagnostic]
                or run["execution_status"] != expected_status[0]
                or document["overall_execution_status"] != expected_status[1]
            ):
                raise ValueError
        unsigned = {
            key: copy.deepcopy(value)
            for key, value in document.items()
            if key != "derivation_evidence_digest"
        }
        expected_digest = semantic_digest(
            "veritrail.review.derivation-evidence/0.1", unsigned
        )
        if document["derivation_evidence_digest"] != expected_digest:
            raise ValueError
    except Exception as exc:
        raise _FactEvidenceClosureError(
            _FactEvidenceClosureFailureCode.EVIDENCE_PROJECTION_REJECTED
        ) from exc


def _diagnostic_eligibility(
    prepared: _PreparedExecutionAttempt,
    phase: OwnedExecutionCellPhaseResult,
) -> _DiagnosticClosureEligibility:
    try:
        if (
            phase.diagnostic_code not in _DIAGNOSTIC_ELIGIBLE_CODES
            or phase.release_outcome is not ReleaseOutcome.RELEASED
            or prepared.eligibility.state is not AttemptEligibilityState.REVOKED
            or not prepared.context.checkpoint()
            or prepared.context.state is not BudgetState.RUNNING
            or prepared.context.stop_trigger is not None
            or prepared.context.reserved_artifact_bytes != 0
        ):
            raise ValueError
        result = _DiagnosticClosureEligibility(
            context=prepared.context,
            attempt_eligibility=prepared.eligibility,
        )
        if not result.is_available():
            raise ValueError
        return result
    except Exception as exc:
        raise _FactEvidenceClosureError(
            _FactEvidenceClosureFailureCode.DIAGNOSTIC_ELIGIBILITY_UNAVAILABLE
        ) from exc


def _provider_run_document(
    phase: OwnedExecutionCellPhaseResult,
    *,
    execution_status: str,
    reported_fact_ids: list[str],
    diagnostics: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "provider_run_id": phase.provider_run_id,
        **phase.provider_descriptor.document(),
        "operands_digest": phase.operands_digest,
        "started_at": phase.provider_run_started_at,
        "finished_at": phase.provider_run_finished_at,
        "execution_status": execution_status,
        "reported_fact_ids": copy.deepcopy(reported_fact_ids),
        "reported_relation_ids": [],
        "diagnostics": copy.deepcopy(diagnostics),
    }


def _strict_owned_object(raw: bytes) -> dict[str, object]:
    import json

    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError
    return value
