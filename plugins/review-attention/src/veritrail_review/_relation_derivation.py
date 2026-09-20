from __future__ import annotations

import copy
from dataclasses import dataclass
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
    ProviderDescriptor,
    binding_matches_closed_allow_list,
)
from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._execution_cell_values import ProviderRunStatus
from veritrail_review._multi_provider_applicability import (
    _descriptor_rank,
    closed_test_multi_provider_bindings,
)
from veritrail_review._multi_provider_fact_composition import (
    _ClosedProviderRun,
    _FactIdentityCollision,
    _close_provider_run,
    _fact_set_document,
    _merge_completed_sources,
    _provider_diagnostic,
)
from veritrail_review._relation_derivation_values import (
    OwnedRelationDerivationResult,
    _RelationDerivationError,
    _RelationDerivationFailureCode,
)
from veritrail_review._relation_execution_cell import (
    _PreparedRelationExecutionAttempt,
    _build_prepared_relation_execution_attempt,
    _run_prepared_relation_execution_attempt,
)
from veritrail_review._relation_execution_cell_binding import (
    closed_test_relation_binding,
    relation_binding_matches_closed_allow_list,
)
from veritrail_review._relation_execution_cell_values import (
    OwnedRelationExecutionCellPhaseResult,
)
from veritrail_review._windows_budget import require_budget_primitive_capability
from veritrail_review.budget import BudgetContext, BudgetState, admit_derivation_budget
from veritrail_review.canonical import canonical_json_bytes
from veritrail_review.derivation_input_contracts import DerivationInputSet
from veritrail_review.errors import BudgetPrimitiveError


_ALLOWED_REQUIREMENTS = {
    "python-ast": True,
    "python-ast-advisory": False,
    "review-relation-derivation": True,
}


@dataclass(frozen=True)
class _PreparedRelationDerivation:
    inputs: DerivationInputSet
    derivation_id: str
    fact_bindings: tuple[ProviderBinding, ...]
    relation_binding: ProviderBinding
    required_by_capability: Mapping[str, bool]
    context: BudgetContext
    parent_eligibility: AttemptEligibility
    fact_child_attempts: tuple[_PreparedExecutionAttempt, ...]
    cancellation_requested: Callable[[], bool] | None
    transport_limits: ExecutionCellTransportSafetyLimits
    request_provenance_bytes: bytes
    attempt_started_at: str


def closed_test_relation_derivation_bindings(
    *, include_advisory: bool = False
) -> tuple[ProviderBinding, ...]:
    """Return the fixed private phase-classified binding table."""

    return (
        *closed_test_multi_provider_bindings(include_advisory=include_advisory),
        closed_test_relation_binding(),
    )


def run_closed_test_relation_derivation(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    cancellation_requested: Callable[[], bool] | None = None,
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
) -> OwnedRelationDerivationResult:
    prepared = _prepare_closed_test_relation_derivation(
        inputs,
        derivation_id=derivation_id,
        bindings=bindings,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    return _RelationDerivationController(prepared).run()


def _prepare_closed_test_relation_derivation(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
) -> _PreparedRelationDerivation:
    requirements, fact_bindings, relation_binding = _admit_closed_applicability(
        inputs,
        derivation_id=derivation_id,
        bindings=bindings,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    try:
        require_budget_primitive_capability()
    except BudgetPrimitiveError as exc:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_RUNTIME_UNAVAILABLE
        ) from exc
    try:
        context = admit_derivation_budget(inputs)
    except BudgetPrimitiveError as exc:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST
        ) from exc
    request_provenance = _owned_request_provenance(inputs)
    attempt_started_at = _utc_now()
    parent = AttemptEligibility()
    children: list[_PreparedExecutionAttempt] = []
    try:
        for binding in fact_bindings:
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
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.PARENT_DERIVATION_REVOKED
        ) from exc
    return _PreparedRelationDerivation(
        inputs=inputs,
        derivation_id=str(derivation_id),
        fact_bindings=fact_bindings,
        relation_binding=relation_binding,
        required_by_capability=copy.deepcopy(requirements),
        context=context,
        parent_eligibility=parent,
        fact_child_attempts=tuple(children),
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        request_provenance_bytes=canonical_json_bytes(request_provenance),
        attempt_started_at=attempt_started_at,
    )


class _RelationDerivationController:
    def __init__(self, prepared: _PreparedRelationDerivation) -> None:
        self.__prepared = prepared
        self.__used = False

    def run(self) -> OwnedRelationDerivationResult:
        if self.__used:
            raise _RelationDerivationError(
                _RelationDerivationFailureCode.PARENT_DERIVATION_REVOKED
            )
        self.__used = True
        prepared = self.__prepared
        closed_runs: list[_ClosedProviderRun] = []
        for child in prepared.fact_child_attempts:
            if (
                prepared.parent_eligibility.state
                is not AttemptEligibilityState.ADMITTED
                or not prepared.context.checkpoint()
            ):
                prepared.parent_eligibility.revoke()
                return _interrupted_result(prepared, closed_runs)
            try:
                phase = _run_prepared_closed_test_execution_attempt(child)
                closed = _close_provider_run(
                    prepared.inputs,
                    phase,
                    binding=child.binding,
                    request_provenance=_owned_object(
                        prepared.request_provenance_bytes
                    ),
                )
            except Exception as exc:
                prepared.parent_eligibility.revoke()
                if prepared.context.stop_trigger is not None:
                    if prepared.context.state is BudgetState.STOPPING:
                        prepared.context._mark_release(residue_free=True)
                    return _interrupted_result(prepared, closed_runs)
                raise _RelationDerivationError(
                    _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
                ) from exc
            closed_runs.append(closed)

        return _join_fact_stage_and_continue(prepared, closed_runs)


def _join_fact_stage_and_continue(
    prepared: _PreparedRelationDerivation,
    closed_runs: Sequence[_ClosedProviderRun],
) -> OwnedRelationDerivationResult:
    if len(closed_runs) != len(prepared.fact_bindings):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )
    required = [
        run
        for run in closed_runs
        if prepared.required_by_capability[run.binding.descriptor.capability_id]
    ]
    if any(run.phase.provider_run_status is ProviderRunStatus.FAILED for run in required):
        fact_status = "FAILED"
    elif any(
        run.phase.provider_run_status is ProviderRunStatus.UNAVAILABLE
        for run in required
    ):
        fact_status = "UNAVAILABLE"
    else:
        fact_status = "COMPLETED"

    facts: tuple[dict[str, object], ...] = ()
    conflicts: tuple[dict[str, object], ...] = ()
    fact_set_document: dict[str, object] | None = None
    fact_set_digest: str | None = None
    normal_fact_set_failed = False
    if fact_status == "COMPLETED":
        try:
            facts, conflicts = _merge_completed_sources(closed_runs)
            fact_set_document, fact_set_digest = _fact_set_document(
                prepared.inputs, facts, conflicts
            )
        except _FactIdentityCollision:
            fact_status = "FAILED"
            normal_fact_set_failed = True
            facts = ()
            conflicts = ()

    fact_commit = canonical_json_bytes(
        {
            "derivation_id": prepared.derivation_id,
            "phase": "FACT_STAGE_JOIN",
            "fact_stage_status": fact_status,
            "provider_run_ids": [
                run.phase.provider_run_id for run in closed_runs
            ],
            "fact_set_digest": fact_set_digest,
        }
    )
    if (
        not prepared.context.checkpoint()
        or prepared.context.try_complete_phase(
            fact_commit, resources_closed=True
        )
        is None
    ):
        prepared.parent_eligibility.revoke()
        if prepared.context.state is BudgetState.STOPPING:
            prepared.context._mark_release(residue_free=True)
        return _interrupted_result(prepared, closed_runs)

    reasons: list[str] = []
    if fact_set_document is None:
        reasons.append(
            "NO_NORMAL_FACT_SET"
            if normal_fact_set_failed
            else "REQUIRED_SOURCE_NON_SUCCESS"
        )
    if conflicts:
        reasons.append("FACT_CONFLICT")
    optional_gap = any(
        not prepared.required_by_capability[run.binding.descriptor.capability_id]
        and run.phase.provider_run_status is not ProviderRunStatus.COMPLETED
        for run in closed_runs
    )
    if optional_gap:
        reasons.append("OPTIONAL_SOURCE_GAP")
    if reasons:
        prepared.parent_eligibility.revoke()
        return _owned_result(
            prepared,
            closed_runs=closed_runs,
            relation_phase=None,
            relation_run=None,
            fact_stage_status=fact_status,
            relation_start_status="NOT_STARTED",
            final_phase_status="UPSTREAM_HOLD",
            upstream_reason_codes=tuple(reasons),
            facts=facts,
            conflicts=conflicts,
            fact_set_document=fact_set_document,
            fact_set_digest=fact_set_digest,
            relations=(),
        )
    if fact_set_document is None:
        prepared.parent_eligibility.revoke()
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )
    try:
        relation_attempt = _build_prepared_relation_execution_attempt(
            prepared.inputs,
            derivation_id=prepared.derivation_id,
            binding=prepared.relation_binding,
            cancellation_requested=prepared.cancellation_requested,
            transport_limits=prepared.transport_limits,
            context=prepared.context,
            eligibility=AttemptEligibility(),
            request_provenance=_owned_object(prepared.request_provenance_bytes),
            attempt_started_at=prepared.attempt_started_at,
            fact_set_document=fact_set_document,
        )
        relation_phase = _run_prepared_relation_execution_attempt(relation_attempt)
        relation_run = _relation_provider_run_document(relation_phase)
        _validate_relation_run_closure(relation_phase, relation_run)
    except Exception as exc:
        prepared.parent_eligibility.revoke()
        if prepared.context.stop_trigger is not None:
            if prepared.context.state is BudgetState.STOPPING:
                prepared.context._mark_release(residue_free=True)
            return _interrupted_result(
                prepared,
                closed_runs,
                fact_stage_status=fact_status,
                facts=facts,
                conflicts=conflicts,
                fact_set_document=fact_set_document,
                fact_set_digest=fact_set_digest,
            )
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        ) from exc

    final_status = relation_phase.provider_run_status.value
    relations = relation_phase.canonical_relations_copy()
    final_commit = canonical_json_bytes(
        {
            "derivation_id": prepared.derivation_id,
            "phase": "PRIVATE_FINAL_JOIN",
            "fact_set_digest": fact_set_digest,
            "relation_provider_run_id": relation_phase.provider_run_id,
            "relation_phase_status": final_status,
            "candidate_relation_ids": list(
                relation_phase.reported_relation_ids
            ),
            "final_reported_ids": [],
        }
    )
    if (
        not prepared.context.checkpoint()
        or prepared.context.try_complete_phase(
            final_commit, resources_closed=True
        )
        is None
    ):
        prepared.parent_eligibility.revoke()
        if prepared.context.state is BudgetState.STOPPING:
            prepared.context._mark_release(residue_free=True)
        final_status = "INTERRUPTED"
    elif final_status != "COMPLETED":
        prepared.parent_eligibility.revoke()
    return _owned_result(
        prepared,
        closed_runs=closed_runs,
        relation_phase=relation_phase,
        relation_run=relation_run,
        fact_stage_status=fact_status,
        relation_start_status="STARTED",
        final_phase_status=final_status,
        upstream_reason_codes=(),
        facts=facts,
        conflicts=conflicts,
        fact_set_document=fact_set_document,
        fact_set_digest=fact_set_digest,
        relations=relations,
    )


def _admit_closed_applicability(
    inputs: object,
    *,
    derivation_id: object,
    bindings: object,
    cancellation_requested: object,
    transport_limits: object,
) -> tuple[dict[str, bool], tuple[ProviderBinding, ...], ProviderBinding]:
    valid_id = (
        isinstance(derivation_id, str)
        and bool(derivation_id)
        and all(not 0xD800 <= ord(character) <= 0xDFFF for character in derivation_id)
    )
    if (
        not isinstance(inputs, DerivationInputSet)
        or not valid_id
        or not isinstance(bindings, Sequence)
        or isinstance(bindings, (str, bytes, bytearray))
        or not isinstance(transport_limits, ExecutionCellTransportSafetyLimits)
        or (cancellation_requested is not None and not callable(cancellation_requested))
    ):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST
        )
    try:
        raw_requirements = inputs.review_policy_document_copy()["provider_requirements"]
        requirements: dict[str, bool] = {}
        for item in raw_requirements:
            capability = item["capability_id"]
            if (
                capability not in _ALLOWED_REQUIREMENTS
                or item["required"] is not _ALLOWED_REQUIREMENTS[capability]
                or item["composition_mode"] != "CUMULATIVE"
                or capability in requirements
            ):
                raise ValueError
            requirements[capability] = item["required"]
        if "python-ast" not in requirements or "review-relation-derivation" not in requirements:
            raise ValueError
        if set(requirements) not in (
            {"python-ast", "review-relation-derivation"},
            {"python-ast", "python-ast-advisory", "review-relation-derivation"},
        ):
            raise ValueError
    except Exception as exc:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST
        ) from exc
    expected_fact = closed_test_multi_provider_bindings(
        include_advisory="python-ast-advisory" in requirements
    )
    expected_relation = closed_test_relation_binding()
    try:
        submitted = tuple(bindings)
        fact_bindings = tuple(
            sorted(
                (
                    binding
                    for binding in submitted
                    if isinstance(binding, ProviderBinding)
                    and binding.descriptor.capability_id
                    in {"python-ast", "python-ast-advisory"}
                ),
                key=lambda item: _descriptor_rank(item.descriptor),
            )
        )
        relation_bindings = tuple(
            binding
            for binding in submitted
            if isinstance(binding, ProviderBinding)
            and binding.descriptor.capability_id == "review-relation-derivation"
        )
        if (
            len(submitted) != len(expected_fact) + 1
            or fact_bindings != expected_fact
            or len(relation_bindings) != 1
            or relation_bindings[0] != expected_relation
            or any(
                not binding_matches_closed_allow_list(binding)
                for binding in fact_bindings
            )
            or not relation_binding_matches_closed_allow_list(relation_bindings[0])
        ):
            raise ValueError
    except Exception as exc:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.APPLICABILITY_BINDING_MISMATCH
        ) from exc
    return (
        requirements,
        tuple(
            ProviderBinding(
                ProviderDescriptor(**binding.descriptor.document()),
                str(binding.launch_key),
            )
            for binding in fact_bindings
        ),
        ProviderBinding(
            ProviderDescriptor(**expected_relation.descriptor.document()),
            str(expected_relation.launch_key),
        ),
    )


def _relation_provider_run_document(
    phase: OwnedRelationExecutionCellPhaseResult,
) -> dict[str, object]:
    diagnostics: list[dict[str, object]] = []
    if phase.diagnostic_code is not None:
        diagnostics.append(
            _provider_diagnostic(phase.diagnostic_code, phase.provider_run_id)
        )
    return {
        "provider_run_id": phase.provider_run_id,
        **phase.provider_descriptor.document(),
        "operands_digest": phase.operands_digest,
        "started_at": phase.provider_run_started_at,
        "finished_at": phase.provider_run_finished_at,
        "execution_status": phase.provider_run_status.value,
        "reported_fact_ids": [],
        "reported_relation_ids": list(phase.reported_relation_ids),
        "diagnostics": diagnostics,
    }


def _validate_relation_run_closure(
    phase: OwnedRelationExecutionCellPhaseResult,
    run: Mapping[str, object],
) -> None:
    relations = phase.canonical_relations_copy()
    relation_ids = [relation["relation_id"] for relation in relations]
    if (
        phase.fact_set_digest == ""
        or phase.reported_fact_ids != ()
        or relation_ids != list(phase.reported_relation_ids)
        or relation_ids != sorted(set(relation_ids))
        or run["provider_run_id"] != phase.provider_run_id
        or run["reported_fact_ids"] != []
        or run["reported_relation_ids"] != relation_ids
        or any(
            relation["provenance_refs"] != [phase.provider_run_id]
            for relation in relations
        )
    ):
        raise ValueError
    if phase.provider_run_status is not ProviderRunStatus.COMPLETED and relations:
        raise ValueError


def _owned_result(
    prepared: _PreparedRelationDerivation,
    *,
    closed_runs: Sequence[_ClosedProviderRun],
    relation_phase: OwnedRelationExecutionCellPhaseResult | None,
    relation_run: Mapping[str, object] | None,
    fact_stage_status: str,
    relation_start_status: str,
    final_phase_status: str,
    upstream_reason_codes: tuple[str, ...],
    facts: Sequence[Mapping[str, object]],
    conflicts: Sequence[Mapping[str, object]],
    fact_set_document: Mapping[str, object] | None,
    fact_set_digest: str | None,
    relations: Sequence[Mapping[str, object]],
) -> OwnedRelationDerivationResult:
    fact_runs = [copy.deepcopy(run.provider_run_document) for run in closed_runs]
    final_runs = [copy.deepcopy(run) for run in fact_runs]
    if relation_run is not None:
        final_runs.append(copy.deepcopy(dict(relation_run)))
    for run in final_runs:
        run["reported_fact_ids"] = []
        run["reported_relation_ids"] = []
    final_runs.sort(key=lambda item: item["provider_run_id"])
    fact_document_bytes = (
        None
        if fact_set_document is None
        else canonical_json_bytes(fact_set_document)
    )
    descriptors: list[dict[str, object]] = []
    for binding in prepared.fact_bindings:
        descriptors.append(
            {
                "stage": "FACT",
                "required": prepared.required_by_capability[
                    binding.descriptor.capability_id
                ],
                "provider_descriptor": binding.descriptor.document(),
            }
        )
    descriptors.append(
        {
            "stage": "RELATION",
            "required": True,
            "provider_descriptor": prepared.relation_binding.descriptor.document(),
        }
    )
    return OwnedRelationDerivationResult(
        derivation_id=prepared.derivation_id,
        request_provenance_bytes=memoryview(
            prepared.request_provenance_bytes
        ).tobytes(),
        applicability_descriptor_bytes=tuple(
            canonical_json_bytes(item) for item in descriptors
        ),
        fact_phase_results=tuple(run.phase for run in closed_runs),
        relation_phase_result=relation_phase,
        fact_provider_run_bytes=tuple(
            canonical_json_bytes(run) for run in fact_runs
        ),
        relation_provider_run_bytes=(
            None if relation_run is None else canonical_json_bytes(relation_run)
        ),
        final_provider_run_bytes=tuple(
            canonical_json_bytes(run) for run in final_runs
        ),
        fact_stage_status=fact_stage_status,
        relation_start_status=relation_start_status,
        final_phase_status=final_phase_status,
        upstream_reason_codes=tuple(upstream_reason_codes),
        canonical_fact_bytes=tuple(canonical_json_bytes(fact) for fact in facts),
        canonical_conflict_bytes=tuple(
            canonical_json_bytes(conflict) for conflict in conflicts
        ),
        fact_set_document_bytes=fact_document_bytes,
        fact_set_digest=fact_set_digest,
        canonical_relation_bytes=tuple(
            canonical_json_bytes(relation) for relation in relations
        ),
    )


def _interrupted_result(
    prepared: _PreparedRelationDerivation,
    closed_runs: Sequence[_ClosedProviderRun],
    *,
    fact_stage_status: str = "INTERRUPTED",
    facts: Sequence[Mapping[str, object]] = (),
    conflicts: Sequence[Mapping[str, object]] = (),
    fact_set_document: Mapping[str, object] | None = None,
    fact_set_digest: str | None = None,
) -> OwnedRelationDerivationResult:
    return _owned_result(
        prepared,
        closed_runs=closed_runs,
        relation_phase=None,
        relation_run=None,
        fact_stage_status=fact_stage_status,
        relation_start_status="NOT_STARTED",
        final_phase_status="INTERRUPTED",
        upstream_reason_codes=("SHARED_BUDGET_STOP",),
        facts=facts,
        conflicts=conflicts,
        fact_set_document=fact_set_document,
        fact_set_digest=fact_set_digest,
        relations=(),
    )


def _owned_object(raw: bytes) -> dict[str, object]:
    import json

    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError
    return value
