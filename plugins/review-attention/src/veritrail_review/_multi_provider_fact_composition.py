from __future__ import annotations

import copy
from dataclasses import dataclass, replace
from typing import Callable, Mapping, Sequence

from veritrail_review._execution_cell import (
    DEFAULT_TRANSPORT_LIMITS,
    _PreparedExecutionAttempt,
    _build_prepared_closed_test_execution_attempt,
    _owned_request_provenance,
    _run_prepared_closed_test_execution_attempt,
    _utc_now,
)
from veritrail_review._execution_cell_binding import (
    ProviderBinding,
)
from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._execution_cell_values import (
    OwnedExecutionCellPhaseResult,
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
from veritrail_review._fact_evidence_closure import (
    _ACTIVE_TERMINAL_STATUS,
    _FACT_KEYS,
    _provider_run_document,
    _strict_owned_object,
    _validate_admitted_fact,
    _validate_phase_continuity,
)
from veritrail_review._multi_provider_applicability import (
    _admit_closed_applicability,
    closed_test_multi_provider_bindings,
)
from veritrail_review._multi_provider_values import (
    OwnedMultiProviderFactCompositionResult,
    _MultiProviderCompositionError,
    _MultiProviderCompositionFailureCode,
    _object_copy,
)
from veritrail_review._fact_evidence_values import (
    OwnedDerivationEvidenceProjection,
    _DiagnosticClosureEligibility,
    _NormalContinuationEligibility,
)
from veritrail_review._windows_budget import require_budget_primitive_capability
from veritrail_review.budget import (
    BudgetContext,
    BudgetState,
    admit_derivation_budget,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet
from veritrail_review.errors import BudgetPrimitiveError


@dataclass(frozen=True)
class _PreparedMultiProviderComposition:
    inputs: DerivationInputSet
    derivation_id: str
    bindings: tuple[ProviderBinding, ...]
    required_by_capability: Mapping[str, bool]
    context: BudgetContext
    parent_eligibility: AttemptEligibility
    child_attempts: tuple[_PreparedExecutionAttempt, ...]
    request_provenance_bytes: bytes
    attempt_started_at: str


@dataclass(frozen=True)
class _ClosedProviderRun:
    binding: ProviderBinding
    phase: OwnedExecutionCellPhaseResult
    canonical_fact_bytes: tuple[bytes, ...]
    provider_run_document: dict[str, object]


def run_closed_test_multi_provider_fact_composition(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    cancellation_requested: Callable[[], bool] | None = None,
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
) -> OwnedMultiProviderFactCompositionResult:
    """Run the frozen private multi-Provider slice without file output."""

    prepared = _prepare_closed_test_multi_provider_composition(
        inputs,
        derivation_id=derivation_id,
        bindings=bindings,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    return _MultiProviderCompositionController(prepared).run()


def _prepare_closed_test_multi_provider_composition(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
) -> _PreparedMultiProviderComposition:
    requirements, normalized = _admit_closed_applicability(
        inputs,
        derivation_id=derivation_id,
        bindings=bindings,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    try:
        require_budget_primitive_capability()
    except BudgetPrimitiveError as exc:
        raise _MultiProviderCompositionError(
            _MultiProviderCompositionFailureCode.DERIVATION_RUNTIME_UNAVAILABLE
        ) from exc
    try:
        context = admit_derivation_budget(inputs)
    except BudgetPrimitiveError as exc:
        raise _MultiProviderCompositionError(
            _MultiProviderCompositionFailureCode.INVALID_COMPOSITION_REQUEST
        ) from exc

    request_provenance = _owned_request_provenance(inputs)
    attempt_started_at = _utc_now()
    parent = AttemptEligibility()
    children: list[_PreparedExecutionAttempt] = []
    try:
        for binding in normalized:
            children.append(
                _build_prepared_closed_test_execution_attempt(
                    inputs,
                    derivation_id=derivation_id,
                    binding=binding,
                    cancellation_requested=cancellation_requested,
                    transport_limits=transport_limits,
                    context=context,
                    eligibility=AttemptEligibility(),
                    request_provenance=request_provenance,
                    attempt_started_at=attempt_started_at,
                )
            )
        if not parent.admit() or not context.checkpoint():
            raise ValueError
    except Exception as exc:
        parent.revoke()
        for child in children:
            child.eligibility.revoke()
        if isinstance(exc, _MultiProviderCompositionError):
            raise
        raise _MultiProviderCompositionError(
            _MultiProviderCompositionFailureCode.PARENT_COMPOSITION_REVOKED
        ) from exc

    return _PreparedMultiProviderComposition(
        inputs=inputs,
        derivation_id=str(derivation_id),
        bindings=normalized,
        required_by_capability=copy.deepcopy(requirements),
        context=context,
        parent_eligibility=parent,
        child_attempts=tuple(children),
        request_provenance_bytes=canonical_json_bytes(request_provenance),
        attempt_started_at=attempt_started_at,
    )


class _MultiProviderCompositionController:
    def __init__(self, prepared: _PreparedMultiProviderComposition) -> None:
        self.__prepared = prepared
        self.__used = False

    def run(self) -> OwnedMultiProviderFactCompositionResult:
        if self.__used:
            raise _MultiProviderCompositionError(
                _MultiProviderCompositionFailureCode.PARENT_COMPOSITION_REVOKED
            )
        self.__used = True
        prepared = self.__prepared
        closed_runs: list[_ClosedProviderRun] = []

        for child in prepared.child_attempts:
            if (
                prepared.parent_eligibility.state
                is not AttemptEligibilityState.ADMITTED
                or not prepared.context.checkpoint()
            ):
                prepared.parent_eligibility.revoke()
                raise _MultiProviderCompositionError(
                    _MultiProviderCompositionFailureCode.PARENT_COMPOSITION_REVOKED
                )
            try:
                phase = _run_prepared_closed_test_execution_attempt(child)
                closed = _close_provider_run(
                    prepared.inputs,
                    phase,
                    binding=child.binding,
                    request_provenance=_object_copy(
                        prepared.request_provenance_bytes
                    ),
                )
            except Exception as exc:
                prepared.parent_eligibility.revoke()
                if prepared.context.stop_trigger is not None:
                    if prepared.context.state is BudgetState.STOPPING:
                        prepared.context._mark_release(residue_free=True)
                    return _stopped_result(prepared, closed_runs)
                raise _MultiProviderCompositionError(
                    _MultiProviderCompositionFailureCode.COMPOSITION_INTEGRITY_FAILURE
                ) from exc
            closed_runs.append(closed)
            if (
                closed.phase.provider_run_status is ProviderRunStatus.INTERRUPTED
                or prepared.context.stop_trigger is not None
                or prepared.context.state is not BudgetState.RUNNING
            ):
                prepared.parent_eligibility.revoke()
                return _stopped_result(prepared, closed_runs)

        return _join_closed_runs(prepared, closed_runs)


def _close_provider_run(
    inputs: DerivationInputSet,
    phase: OwnedExecutionCellPhaseResult,
    *,
    binding: ProviderBinding,
    request_provenance: Mapping[str, object],
) -> _ClosedProviderRun:
    _validate_phase_continuity(
        inputs,
        phase,
        binding=binding,
        request_provenance=request_provenance,
    )
    if phase.release_outcome is not ReleaseOutcome.RELEASED:
        raise ValueError
    if phase.phase_status is PhaseStatus.COMPLETED:
        try:
            facts = _admit_run_local_facts(inputs, phase)
        except Exception:
            failed = replace(
                phase,
                provider_run_status=ProviderRunStatus.FAILED,
                phase_status=PhaseStatus.FAILED,
                diagnostic_code="NONCONFORMANT_PROVIDER_OUTPUT",
                canonical_fact_bytes=(),
                reported_fact_ids=(),
                reported_relation_ids=(),
            )
            return _closed_non_success_run(binding, failed)
        run = _provider_run_document(
            phase,
            execution_status="COMPLETED",
            reported_fact_ids=[
                _strict_owned_object(raw)["fact_id"] for raw in facts
            ],
            diagnostics=[],
        )
        return _ClosedProviderRun(binding, phase, facts, run)
    return _closed_non_success_run(binding, phase)


def _admit_run_local_facts(
    inputs: DerivationInputSet, phase: OwnedExecutionCellPhaseResult
) -> tuple[bytes, ...]:
    if (
        phase.provider_run_status is not ProviderRunStatus.COMPLETED
        or phase.diagnostic_code is not None
        or phase.reported_relation_ids != ()
    ):
        raise ValueError
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
    by_id: dict[str, tuple[bytes, dict[str, object]]] = {}
    subjects: dict[str, str] = {}
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
        previous_subject = subjects.setdefault(subject, fact_id)
        if previous_subject != fact_id:
            raise ValueError
        previous = by_id.get(fact_id)
        if previous is not None and previous[0] != raw:
            raise ValueError
        by_id[fact_id] = (memoryview(raw).tobytes(), copy.deepcopy(fact))
    admitted_ids = tuple(sorted(by_id))
    if phase.reported_fact_ids != admitted_ids:
        raise ValueError
    return tuple(by_id[fact_id][0] for fact_id in admitted_ids)


def _closed_non_success_run(
    binding: ProviderBinding, phase: OwnedExecutionCellPhaseResult
) -> _ClosedProviderRun:
    code = phase.diagnostic_code
    expected = _ACTIVE_TERMINAL_STATUS.get(code or "")
    if (
        expected is None
        or phase.provider_run_status.value != expected[0]
        or phase.phase_status.value != expected[1]
        or phase.canonical_fact_bytes != ()
        or phase.reported_fact_ids != ()
        or phase.reported_relation_ids != ()
    ):
        raise ValueError
    diagnostic = _provider_diagnostic(code, phase.provider_run_id)
    run = _provider_run_document(
        phase,
        execution_status=expected[0],
        reported_fact_ids=[],
        diagnostics=[diagnostic],
    )
    return _ClosedProviderRun(binding, phase, (), run)


def _join_closed_runs(
    prepared: _PreparedMultiProviderComposition,
    closed_runs: Sequence[_ClosedProviderRun],
) -> OwnedMultiProviderFactCompositionResult:
    if len(closed_runs) != len(prepared.bindings):
        raise _MultiProviderCompositionError(
            _MultiProviderCompositionFailureCode.COMPOSITION_INTEGRITY_FAILURE
        )
    required = [
        run
        for run in closed_runs
        if prepared.required_by_capability[run.binding.descriptor.capability_id]
    ]
    if any(run.phase.provider_run_status is ProviderRunStatus.FAILED for run in required):
        overall = "FAILED"
    elif any(
        run.phase.provider_run_status is ProviderRunStatus.UNAVAILABLE
        for run in required
    ):
        overall = "UNAVAILABLE"
    else:
        overall = "COMPLETED"

    facts: tuple[dict[str, object], ...] = ()
    conflicts: tuple[dict[str, object], ...] = ()
    composition_diagnostics: list[dict[str, object]] = []
    if overall == "COMPLETED":
        try:
            facts, conflicts = _merge_completed_sources(closed_runs)
        except _FactIdentityCollision:
            overall = "FAILED"
            composition_diagnostics.append(
                {"diagnostic_code": "INTERNAL_DERIVATION_ERROR", "subject_ref": None}
            )

    if overall != "COMPLETED":
        prepared.parent_eligibility.revoke()
        facts = ()
        conflicts = ()

    fact_set_document: dict[str, object] | None = None
    fact_set_digest: str | None = None
    if overall == "COMPLETED":
        fact_set_document, fact_set_digest = _fact_set_document(
            prepared.inputs, facts, conflicts
        )

    diagnostics = _sorted_unique_diagnostics(
        [
            diagnostic
            for run in closed_runs
            for diagnostic in run.provider_run_document["diagnostics"]
        ]
        + composition_diagnostics
    )
    provider_runs = _final_provider_runs(closed_runs, overall=overall)
    evidence = _evidence_projection(
        prepared,
        provider_runs=provider_runs,
        overall=overall,
        diagnostics=diagnostics,
        facts=facts,
    )
    commit_bytes = canonical_json_bytes(
        {
            "derivation_id": prepared.derivation_id,
            "overall_execution_status": overall,
            "provider_run_ids": [run["provider_run_id"] for run in provider_runs],
            "fact_set_digest": fact_set_digest,
            "derivation_evidence_digest": evidence.derivation_evidence_digest,
        }
    )
    if (
        not prepared.context.checkpoint()
        or prepared.context.try_complete_phase(
            commit_bytes,
            resources_closed=True,
        )
        is None
    ):
        prepared.parent_eligibility.revoke()
        if prepared.context.state is BudgetState.STOPPING:
            prepared.context._mark_release(residue_free=True)
        return _stopped_result(prepared, closed_runs)

    normal: _NormalContinuationEligibility | None = None
    diagnostic: _DiagnosticClosureEligibility | None = None
    if overall == "COMPLETED":
        normal = _NormalContinuationEligibility(
            context=prepared.context,
            attempt_eligibility=prepared.parent_eligibility,
        )
        if not normal.permits_continuation():
            prepared.parent_eligibility.revoke()
            raise _MultiProviderCompositionError(
                _MultiProviderCompositionFailureCode.PARENT_COMPOSITION_REVOKED
            )
    else:
        diagnostic = _DiagnosticClosureEligibility(
            context=prepared.context,
            attempt_eligibility=prepared.parent_eligibility,
        )
        if not diagnostic.is_available():
            raise _MultiProviderCompositionError(
                _MultiProviderCompositionFailureCode.PARENT_COMPOSITION_REVOKED
            )

    return _owned_result(
        prepared,
        closed_runs=closed_runs,
        provider_runs=provider_runs,
        overall=overall,
        diagnostics=diagnostics,
        facts=facts,
        conflicts=conflicts,
        fact_set_document=fact_set_document,
        fact_set_digest=fact_set_digest,
        evidence=evidence,
        normal=normal,
        diagnostic=diagnostic,
    )


class _FactIdentityCollision(RuntimeError):
    pass


def _merge_completed_sources(
    closed_runs: Sequence[_ClosedProviderRun],
) -> tuple[tuple[dict[str, object], ...], tuple[dict[str, object], ...]]:
    by_id: dict[str, dict[str, object]] = {}
    semantic_by_id: dict[str, bytes] = {}
    for run in closed_runs:
        if run.phase.provider_run_status is not ProviderRunStatus.COMPLETED:
            continue
        for raw in run.canonical_fact_bytes:
            fact = _strict_owned_object(raw)
            fact_id = fact["fact_id"]
            semantic = {
                key: copy.deepcopy(value)
                for key, value in fact.items()
                if key != "provenance_refs"
            }
            semantic_bytes = canonical_json_bytes(semantic)
            previous = semantic_by_id.setdefault(fact_id, semantic_bytes)
            if previous != semantic_bytes:
                raise _FactIdentityCollision
            if fact_id not in by_id:
                by_id[fact_id] = copy.deepcopy(fact)
            refs = set(by_id[fact_id]["provenance_refs"])
            refs.update(fact["provenance_refs"])
            by_id[fact_id]["provenance_refs"] = sorted(refs)

    facts = tuple(by_id[fact_id] for fact_id in sorted(by_id))
    by_subject: dict[str, list[dict[str, object]]] = {}
    for fact in facts:
        by_subject.setdefault(fact["subject_key_digest"], []).append(fact)
    conflicts: list[dict[str, object]] = []
    for subject, candidates in by_subject.items():
        candidate_ids = sorted({fact["fact_id"] for fact in candidates})
        if len(candidate_ids) < 2:
            continue
        provenance = sorted(
            {
                ref
                for fact in candidates
                for ref in fact["provenance_refs"]
            }
        )
        conflict_id = semantic_digest(
            "veritrail.review.fact-conflict/0.1",
            {
                "subject_key_digest": subject,
                "candidate_fact_ids": candidate_ids,
            },
        )
        conflicts.append(
            {
                "conflict_id": conflict_id,
                "subject_key_digest": subject,
                "candidate_fact_ids": candidate_ids,
                "provenance_refs": provenance,
            }
        )
    conflicts.sort(key=lambda item: item["conflict_id"])
    return facts, tuple(conflicts)


def _fact_set_document(
    inputs: DerivationInputSet,
    facts: Sequence[Mapping[str, object]],
    conflicts: Sequence[Mapping[str, object]],
) -> tuple[dict[str, object], str]:
    semantic_facts = [
        {key: copy.deepcopy(value) for key, value in fact.items() if key != "provenance_refs"}
        for fact in facts
    ]
    semantic_conflicts = [
        {
            key: copy.deepcopy(value)
            for key, value in conflict.items()
            if key != "provenance_refs"
        }
        for conflict in conflicts
    ]
    digest = semantic_digest(
        "veritrail.review.fact-set/0.1",
        {
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            "facts": semantic_facts,
            "conflicts": semantic_conflicts,
        },
    )
    return (
        {
            "artifact_kind": "FACT_SET",
            "schema_version": "0.1",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "policy_digest": inputs.policy_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            "facts": copy.deepcopy(list(facts)),
            "conflicts": copy.deepcopy(list(conflicts)),
            "fact_set_digest": digest,
        },
        digest,
    )


def _final_provider_runs(
    closed_runs: Sequence[_ClosedProviderRun], *, overall: str
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for closed in closed_runs:
        run = copy.deepcopy(closed.provider_run_document)
        if overall != "COMPLETED":
            run["reported_fact_ids"] = []
            run["reported_relation_ids"] = []
        result.append(run)
    result.sort(key=lambda item: item["provider_run_id"])
    return result


def _evidence_projection(
    prepared: _PreparedMultiProviderComposition,
    *,
    provider_runs: list[dict[str, object]],
    overall: str,
    diagnostics: Sequence[Mapping[str, object]],
    facts: Sequence[Mapping[str, object]],
) -> OwnedDerivationEvidenceProjection:
    document: dict[str, object] = {
        "artifact_kind": "DERIVATION_EVIDENCE",
        "schema_version": "0.1.1",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "derivation_id": prepared.derivation_id,
        "request_provenance": _object_copy(prepared.request_provenance_bytes),
        "source_snapshot_digest": prepared.inputs.source_snapshot_digest,
        "policy_digest": prepared.inputs.policy_digest,
        "analysis_scope_digest": prepared.inputs.analysis_scope_digest,
        "slice_policy_digest": prepared.inputs.slice_policy_digest,
        "derivation_profile_digest": prepared.inputs.derivation_profile_digest,
        "provider_runs": copy.deepcopy(provider_runs),
        "overall_execution_status": overall,
        "started_at": prepared.attempt_started_at,
        "finished_at": _utc_now(),
        "diagnostics": copy.deepcopy(list(diagnostics)),
    }
    digest = semantic_digest("veritrail.review.derivation-evidence/0.1", document)
    document["derivation_evidence_digest"] = digest
    _validate_composed_projection(document, facts=facts)
    return OwnedDerivationEvidenceProjection(
        document_bytes=canonical_json_bytes(document),
        derivation_evidence_digest=digest,
    )


def _validate_composed_projection(
    document: Mapping[str, object],
    *,
    facts: Sequence[Mapping[str, object]] = (),
) -> None:
    runs = document.get("provider_runs")
    diagnostics = document.get("diagnostics")
    if not isinstance(runs, list) or not isinstance(diagnostics, list):
        raise ValueError
    run_ids = [run["provider_run_id"] for run in runs]
    if run_ids != sorted(set(run_ids)):
        raise ValueError
    if diagnostics != _sorted_unique_diagnostics(diagnostics):
        raise ValueError
    overall = document["overall_execution_status"]
    if overall != "COMPLETED" and any(
        run["reported_fact_ids"] or run["reported_relation_ids"] for run in runs
    ):
        raise ValueError
    facts_by_run: dict[str, set[str]] = {
        run["provider_run_id"]: set(run["reported_fact_ids"])
        for run in runs
    }
    if any(run["reported_relation_ids"] for run in runs):
        raise ValueError
    unsigned = {
        key: copy.deepcopy(value)
        for key, value in document.items()
        if key != "derivation_evidence_digest"
    }
    if document["derivation_evidence_digest"] != semantic_digest(
        "veritrail.review.derivation-evidence/0.1", unsigned
    ):
        raise ValueError
    if len(facts_by_run) != len(runs):
        raise ValueError
    fact_by_id: dict[str, Mapping[str, object]] = {}
    for fact in facts:
        fact_id = fact.get("fact_id")
        refs = fact.get("provenance_refs")
        if (
            not isinstance(fact_id, str)
            or not isinstance(refs, list)
            or refs != sorted(set(refs))
            or any(ref not in facts_by_run for ref in refs)
            or fact_id in fact_by_id
        ):
            raise ValueError
        fact_by_id[fact_id] = fact
        if any(fact_id not in facts_by_run[ref] for ref in refs):
            raise ValueError
    for run_id, reported in facts_by_run.items():
        if any(
            fact_id not in fact_by_id
            or run_id not in fact_by_id[fact_id]["provenance_refs"]
            for fact_id in reported
        ):
            raise ValueError
    if overall == "COMPLETED":
        if set(fact_by_id) != {
            fact_id for reported in facts_by_run.values() for fact_id in reported
        }:
            raise ValueError
    elif fact_by_id:
        raise ValueError

    run_diagnostics = [
        diagnostic for run in runs for diagnostic in run["diagnostics"]
    ]
    for run in runs:
        expected_subject = {
            "ref_kind": "PROVIDER_RUN",
            "provider_run_id": run["provider_run_id"],
        }
        if any(
            diagnostic.get("subject_ref") != expected_subject
            for diagnostic in run["diagnostics"]
        ):
            raise ValueError
    top_bytes = {canonical_json_bytes(item) for item in diagnostics}
    if any(canonical_json_bytes(item) not in top_bytes for item in run_diagnostics):
        raise ValueError


def _owned_result(
    prepared: _PreparedMultiProviderComposition,
    *,
    closed_runs: Sequence[_ClosedProviderRun],
    provider_runs: Sequence[Mapping[str, object]],
    overall: str,
    diagnostics: Sequence[Mapping[str, object]],
    facts: Sequence[Mapping[str, object]],
    conflicts: Sequence[Mapping[str, object]],
    fact_set_document: Mapping[str, object] | None,
    fact_set_digest: str | None,
    evidence: OwnedDerivationEvidenceProjection | None,
    normal: _NormalContinuationEligibility | None,
    diagnostic: _DiagnosticClosureEligibility | None,
) -> OwnedMultiProviderFactCompositionResult:
    document_bytes = (
        None if fact_set_document is None else canonical_json_bytes(fact_set_document)
    )
    return OwnedMultiProviderFactCompositionResult(
        derivation_id=prepared.derivation_id,
        request_provenance_bytes=memoryview(
            prepared.request_provenance_bytes
        ).tobytes(),
        applicability_descriptor_bytes=tuple(
            canonical_json_bytes(binding.descriptor.document())
            for binding in prepared.bindings
        ),
        phase_results=tuple(closed.phase for closed in closed_runs),
        provider_run_bytes=tuple(canonical_json_bytes(run) for run in provider_runs),
        overall_execution_status=overall,
        diagnostic_bytes=tuple(canonical_json_bytes(item) for item in diagnostics),
        canonical_fact_bytes=tuple(canonical_json_bytes(fact) for fact in facts),
        canonical_conflict_bytes=tuple(
            canonical_json_bytes(conflict) for conflict in conflicts
        ),
        fact_set_document_bytes=document_bytes,
        canonical_fact_set_artifact_bytes=(
            None if document_bytes is None else document_bytes + b"\n"
        ),
        fact_set_digest=fact_set_digest,
        evidence_projection=evidence,
        _normal_continuation=normal,
        _diagnostic_closure=diagnostic,
    )


def _stopped_result(
    prepared: _PreparedMultiProviderComposition,
    closed_runs: Sequence[_ClosedProviderRun],
) -> OwnedMultiProviderFactCompositionResult:
    diagnostics = _sorted_unique_diagnostics(
        [
            diagnostic
            for run in closed_runs
            for diagnostic in run.provider_run_document["diagnostics"]
        ]
    )
    runs = _final_provider_runs(closed_runs, overall="INTERRUPTED")
    return _owned_result(
        prepared,
        closed_runs=closed_runs,
        provider_runs=runs,
        overall="INTERRUPTED",
        diagnostics=diagnostics,
        facts=(),
        conflicts=(),
        fact_set_document=None,
        fact_set_digest=None,
        evidence=None,
        normal=None,
        diagnostic=None,
    )


def _provider_diagnostic(code: str, provider_run_id: str) -> dict[str, object]:
    return {
        "diagnostic_code": code,
        "subject_ref": {
            "ref_kind": "PROVIDER_RUN",
            "provider_run_id": provider_run_id,
        },
    }


def _sorted_unique_diagnostics(
    diagnostics: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    by_bytes: dict[bytes, dict[str, object]] = {}
    for diagnostic in diagnostics:
        owned = copy.deepcopy(dict(diagnostic))
        by_bytes[canonical_json_bytes(owned)] = owned
    return sorted(
        by_bytes.values(),
        key=lambda item: (
            item["diagnostic_code"],
            canonical_json_bytes(item["subject_ref"]),
        ),
    )
