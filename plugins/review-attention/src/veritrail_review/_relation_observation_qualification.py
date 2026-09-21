from __future__ import annotations

import copy
import json
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
from veritrail_review._execution_cell_binding import ProviderBinding, ProviderDescriptor
from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._execution_cell_values import (
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
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
    _RelationDerivationError,
    _RelationDerivationFailureCode,
)
from veritrail_review._relation_observation_binding import (
    closed_test_relation_observation_bindings,
    relation_observation_binding_matches_allow_list,
    relation_observation_descriptor_rank,
)
from veritrail_review._relation_observation_cell import (
    build_prepared_relation_observation_attempt,
    run_prepared_relation_observation_attempt,
)
from veritrail_review._relation_observation_cell_values import (
    OwnedRelationObservationCellPhaseResult,
)
from veritrail_review._relation_observation_domain import (
    build_declared_relation_observation_domain,
    family_rule_for_item,
)
from veritrail_review._relation_observation_qualification_values import (
    OwnedRelationCompositionQualificationResult,
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


_REASON_RANK = {
    code: rank
    for rank, code in enumerate(
        (
            "REQUIRED_SOURCE_NOT_STARTED",
            "REQUIRED_SOURCE_FAILED",
            "REQUIRED_SOURCE_UNAVAILABLE",
            "REQUIRED_SOURCE_INTERRUPTED",
            "OBSERVATION_OUTCOME_MISSING",
            "OBSERVATION_OUTCOME_UNEXPECTED",
            "OBSERVATION_OUTCOME_DUPLICATE",
            "OBSERVATION_OUTCOME_INVALID",
            "OBSERVATION_CANDIDATE_REFERENCE_MISMATCH",
            "UNEXPECTED_RELATION_CANDIDATE",
            "RELATION_IDENTITY_COLLISION",
            "SHARED_CONTEXT_FAILURE",
            "RELEASE_FAILURE",
        )
    )
}


@dataclass(frozen=True)
class _PreparedObservationQualification:
    inputs: DerivationInputSet
    derivation_id: str
    fact_bindings: tuple[ProviderBinding, ...]
    relation_bindings: tuple[ProviderBinding, ...]
    required_by_capability: Mapping[str, bool]
    context: BudgetContext
    parent_eligibility: AttemptEligibility
    fact_child_attempts: tuple[_PreparedExecutionAttempt, ...]
    cancellation_requested: Callable[[], bool] | None
    transport_limits: ExecutionCellTransportSafetyLimits
    request_provenance_bytes: bytes
    attempt_started_at: str


def closed_test_relation_observation_qualification_bindings(
) -> tuple[ProviderBinding, ...]:
    return (
        *closed_test_multi_provider_bindings(),
        *closed_test_relation_observation_bindings(),
    )


def run_closed_test_relation_observation_qualification(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    cancellation_requested: Callable[[], bool] | None = None,
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
) -> OwnedRelationCompositionQualificationResult:
    prepared = _prepare_observation_qualification(
        inputs,
        derivation_id=derivation_id,
        bindings=bindings,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    return _ObservationQualificationController(prepared).run()


def _prepare_observation_qualification(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
) -> _PreparedObservationQualification:
    requirements, fact_bindings, relation_bindings = (
        _admit_observation_qualification_applicability(
            inputs,
            derivation_id=derivation_id,
            bindings=bindings,
            cancellation_requested=cancellation_requested,
            transport_limits=transport_limits,
        )
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
    return _PreparedObservationQualification(
        inputs,
        str(derivation_id),
        fact_bindings,
        relation_bindings,
        copy.deepcopy(requirements),
        context,
        parent,
        tuple(children),
        cancellation_requested,
        transport_limits,
        canonical_json_bytes(request_provenance),
        attempt_started_at,
    )


def _admit_observation_qualification_applicability(
    inputs: object,
    *,
    derivation_id: object,
    bindings: object,
    cancellation_requested: object,
    transport_limits: object,
) -> tuple[
    dict[str, bool], tuple[ProviderBinding, ...], tuple[ProviderBinding, ...]
]:
    if (
        not isinstance(inputs, DerivationInputSet)
        or not isinstance(bindings, Sequence)
        or isinstance(bindings, (str, bytes, bytearray))
    ):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST
        )
    expected_fact = closed_test_multi_provider_bindings()
    expected_relation = closed_test_relation_observation_bindings()
    try:
        submitted = tuple(bindings)
        fact = tuple(
            sorted(
                (
                    binding
                    for binding in submitted
                    if isinstance(binding, ProviderBinding)
                    and binding.descriptor.capability_id == "python-ast"
                ),
                key=lambda item: _descriptor_rank(item.descriptor),
            )
        )
        relation = tuple(
            sorted(
                (
                    binding
                    for binding in submitted
                    if isinstance(binding, ProviderBinding)
                    and binding.descriptor.capability_id
                    == "review-relation-derivation"
                ),
                key=lambda item: relation_observation_descriptor_rank(
                    item.descriptor
                ),
            )
        )
        if (
            len(submitted) != len(expected_fact) + len(expected_relation)
            or fact != expected_fact
            or relation != expected_relation
            or any(
                not relation_observation_binding_matches_allow_list(item)
                for item in relation
            )
        ):
            raise ValueError
        policy = inputs.review_policy_document_copy()
        raw_requirements = policy["provider_requirements"]
        if raw_requirements != [
            {
                "capability_id": "python-ast",
                "required": True,
                "composition_mode": "CUMULATIVE",
            },
            {
                "capability_id": "review-relation-derivation",
                "required": True,
                "composition_mode": "CUMULATIVE",
            },
        ]:
            raise ValueError
        requirements = {
            item["capability_id"]: item["required"]
            for item in raw_requirements
        }
    except Exception as exc:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.APPLICABILITY_BINDING_MISMATCH
        ) from exc
    # The frozen Relation derivation preflight independently validates the
    # remaining request coordinates before any budget or Provider exists.
    if (
        not isinstance(derivation_id, str)
        or not derivation_id
        or any(0xD800 <= ord(character) <= 0xDFFF for character in derivation_id)
        or not isinstance(transport_limits, ExecutionCellTransportSafetyLimits)
        or (cancellation_requested is not None and not callable(cancellation_requested))
    ):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST
        )
    return (
        requirements,
        tuple(
            ProviderBinding(
                ProviderDescriptor(**item.descriptor.document()),
                str(item.launch_key),
            )
            for item in fact
        ),
        tuple(
            ProviderBinding(
                ProviderDescriptor(**item.descriptor.document()),
                str(item.launch_key),
            )
            for item in relation
        ),
    )


class _ObservationQualificationController:
    def __init__(self, prepared: _PreparedObservationQualification) -> None:
        self.__prepared = prepared
        self.__used = False

    def run(self) -> OwnedRelationCompositionQualificationResult:
        if self.__used:
            raise _RelationDerivationError(
                _RelationDerivationFailureCode.PARENT_DERIVATION_REVOKED
            )
        self.__used = True
        base = self.__prepared
        closed_runs: list[_ClosedProviderRun] = []
        for child in base.fact_child_attempts:
            if (
                base.parent_eligibility.state
                is not AttemptEligibilityState.ADMITTED
                or not base.context.checkpoint()
            ):
                base.parent_eligibility.revoke()
                raise _RelationDerivationError(
                    _RelationDerivationFailureCode.PARENT_DERIVATION_REVOKED
                )
            try:
                phase = _run_prepared_closed_test_execution_attempt(child)
                closed = _close_provider_run(
                    base.inputs,
                    phase,
                    binding=child.binding,
                    request_provenance=_owned_object(
                        base.request_provenance_bytes
                    ),
                )
            except Exception as exc:
                base.parent_eligibility.revoke()
                raise _RelationDerivationError(
                    _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
                ) from exc
            closed_runs.append(closed)
        fact_set_document = _close_fact_stage(base, closed_runs)
        observation_domain = build_declared_relation_observation_domain(
            base.inputs,
            fact_set_document,
            self.__prepared.relation_bindings,
        )
        attempts = []
        try:
            for binding in self.__prepared.relation_bindings:
                attempts.append(
                    build_prepared_relation_observation_attempt(
                        base.inputs,
                        derivation_id=base.derivation_id,
                        binding=binding,
                        cancellation_requested=base.cancellation_requested,
                        transport_limits=base.transport_limits,
                        context=base.context,
                        eligibility=AttemptEligibility(),
                        request_provenance=_owned_object(
                            base.request_provenance_bytes
                        ),
                        attempt_started_at=base.attempt_started_at,
                        fact_set_document=fact_set_document,
                        observation_domain=observation_domain,
                    )
                )
        except Exception as exc:
            base.parent_eligibility.revoke()
            for attempt in attempts:
                attempt.eligibility.revoke()
            raise _RelationDerivationError(
                _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
            ) from exc

        phases: list[OwnedRelationObservationCellPhaseResult] = []
        release_failure = False
        shared_failure = False
        for attempt in attempts:
            if (
                base.parent_eligibility.state
                is not AttemptEligibilityState.ADMITTED
                or not base.context.checkpoint()
            ):
                shared_failure = True
                break
            try:
                phase = run_prepared_relation_observation_attempt(attempt)
            except Exception as exc:
                from veritrail_review.errors import (
                    DerivationExecutionCellError,
                    DerivationExecutionCellFailureCode,
                )

                if (
                    isinstance(exc, DerivationExecutionCellError)
                    and exc.code is DerivationExecutionCellFailureCode.RELEASE_FAILED
                ):
                    release_failure = True
                elif base.context.stop_trigger is not None:
                    shared_failure = True
                else:
                    base.parent_eligibility.revoke()
                    raise _RelationDerivationError(
                        _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
                    ) from exc
                break
            phases.append(phase)
            if (
                phase.provider_run_status is ProviderRunStatus.INTERRUPTED
                or base.context.stop_trigger is not None
                or base.context.state is not BudgetState.RUNNING
            ):
                shared_failure = True
                break

        result = _project_qualification(
            base,
            fact_set_document=fact_set_document,
            observation_domain=observation_domain,
            relation_bindings=self.__prepared.relation_bindings,
            fact_phases=tuple(run.phase for run in closed_runs),
            phases=tuple(phases),
            shared_failure=shared_failure,
            release_failure=release_failure,
        )
        commit = canonical_json_bytes(
            {
                "derivation_id": base.derivation_id,
                "phase": "RELATION_OBSERVATION_QUALIFICATION",
                "observation_domain_digest": result.observation_domain_digest,
                "qualification_digest": result.qualification_digest,
                "qualification_status": result.qualification_status,
            }
        )
        if (
            not base.context.checkpoint()
            or base.context.try_complete_phase(commit, resources_closed=True) is None
        ):
            if base.context.state is BudgetState.STOPPING:
                base.context._mark_release(residue_free=True)
            result = _project_qualification(
                base,
                fact_set_document=fact_set_document,
                observation_domain=observation_domain,
                relation_bindings=self.__prepared.relation_bindings,
                fact_phases=tuple(run.phase for run in closed_runs),
                phases=tuple(phases),
                shared_failure=True,
                release_failure=release_failure,
            )
        if result.qualification_status != "QUALIFIED":
            base.parent_eligibility.revoke()
        return result


def _close_fact_stage(
    prepared: _PreparedObservationQualification,
    closed_runs: Sequence[_ClosedProviderRun],
) -> dict[str, object]:
    if len(closed_runs) != len(prepared.fact_bindings):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )
    if any(
        run.phase.provider_run_status is not ProviderRunStatus.COMPLETED
        for run in closed_runs
    ):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST
        )
    try:
        facts, conflicts = _merge_completed_sources(closed_runs)
        if conflicts:
            raise ValueError
        fact_set_document, fact_set_digest = _fact_set_document(
            prepared.inputs, facts, conflicts
        )
    except (_FactIdentityCollision, ValueError) as exc:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST
        ) from exc
    commit = canonical_json_bytes(
        {
            "derivation_id": prepared.derivation_id,
            "phase": "FACT_STAGE_JOIN",
            "fact_stage_status": "COMPLETED",
            "provider_run_ids": [
                run.phase.provider_run_id for run in closed_runs
            ],
            "fact_set_digest": fact_set_digest,
        }
    )
    if (
        not prepared.context.checkpoint()
        or prepared.context.try_complete_phase(commit, resources_closed=True) is None
    ):
        prepared.parent_eligibility.revoke()
        if prepared.context.state is BudgetState.STOPPING:
            prepared.context._mark_release(residue_free=True)
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.PARENT_DERIVATION_REVOKED
        )
    return fact_set_document


def _project_qualification(
    prepared: _PreparedObservationQualification,
    *,
    fact_set_document: Mapping[str, object],
    observation_domain: Mapping[str, object],
    relation_bindings: Sequence[ProviderBinding],
    fact_phases: tuple[object, ...],
    phases: tuple[OwnedRelationObservationCellPhaseResult, ...],
    shared_failure: bool,
    release_failure: bool,
) -> OwnedRelationCompositionQualificationResult:
    phase_by_descriptor = {
        tuple(phase.provider_descriptor.document().items()): phase
        for phase in phases
    }
    receipts: list[dict[str, object]] = []
    provider_runs: list[dict[str, object]] = []
    for binding in relation_bindings:
        key = tuple(binding.descriptor.document().items())
        phase = phase_by_descriptor.get(key)
        receipt = _observation_receipt(
            observation_domain, binding.descriptor, phase
        )
        receipts.append(receipt)
        if phase is not None:
            provider_runs.append(_provider_run_document(phase))
    receipts.sort(
        key=lambda item: relation_observation_descriptor_rank(
            ProviderDescriptor(**item["provider_descriptor"])
        )
    )
    provider_runs.sort(
        key=lambda item: relation_observation_descriptor_rank(
            ProviderDescriptor(
                **{
                    key: item[key]
                    for key in (
                        "capability_id",
                        "provider_id",
                        "provider_version",
                        "parser_id",
                        "parser_version",
                        "runtime_id",
                        "runtime_version",
                    )
                }
            )
        )
    )
    terminal_closure = (
        "COMPLETE"
        if len(provider_runs) == len(relation_bindings)
        else "INCOMPLETE"
    )
    observation_closure = (
        "COMPLETE"
        if all(_receipt_complete(receipt) for receipt in receipts)
        else "INCOMPLETE"
    )
    composition_status = "NOT_COMPOSED"
    merged: tuple[dict[str, object], ...] = ()
    conflicts: tuple[dict[str, object], ...] = ()
    identity_collision = False
    if observation_closure == "COMPLETE" and not shared_failure and not release_failure:
        try:
            merged, conflicts = _compose_candidates(phases)
        except _RelationIdentityCollision:
            composition_status = "INTEGRITY_FAILED"
            identity_collision = True
        else:
            composition_status = "CONFLICTING" if conflicts else "CONSISTENT"

    reasons = _reason_codes(
        receipts,
        identity_collision=identity_collision,
        shared_failure=shared_failure,
        release_failure=release_failure,
    )
    qualification_status = (
        "INTEGRITY_FAILED"
        if identity_collision
        else (
            "QUALIFIED"
            if terminal_closure == "COMPLETE"
            and observation_closure == "COMPLETE"
            and composition_status in {"CONSISTENT", "CONFLICTING"}
            and not shared_failure
            and not release_failure
            else "NOT_QUALIFIED"
        )
    )
    if qualification_status != "QUALIFIED" and composition_status not in {
        "INTEGRITY_FAILED"
    }:
        if shared_failure or release_failure or observation_closure != "COMPLETE":
            composition_status = "NOT_COMPOSED"
            merged = ()
            conflicts = ()
    terminal_projection = [
        {
            "provider_run_id": run["provider_run_id"],
            "execution_status": run["execution_status"],
        }
        for run in provider_runs
    ]
    payload = {
        "observation_domain_digest": observation_domain[
            "observation_domain_digest"
        ],
        "provider_run_terminals": terminal_projection,
        "observation_receipts": copy.deepcopy(receipts),
        "required_source_set_terminal_closure": terminal_closure,
        "required_observation_closure": observation_closure,
        "candidate_composition_status": composition_status,
        "qualification_status": qualification_status,
        "merged_candidate_relation_ids": [
            item["relation_id"] for item in merged
        ],
        "private_conflict_ids": [item["conflict_id"] for item in conflicts],
        "reason_codes": list(reasons),
    }
    qualification_digest = semantic_digest(
        "veritrail.review.relation-composition-qualification/0.1", payload
    )
    return OwnedRelationCompositionQualificationResult(
        derivation_id=prepared.derivation_id,
        source_snapshot_digest=prepared.inputs.source_snapshot_digest,
        policy_digest=prepared.inputs.policy_digest,
        analysis_scope_digest=prepared.inputs.analysis_scope_digest,
        slice_policy_digest=prepared.inputs.slice_policy_digest,
        derivation_profile_digest=prepared.inputs.derivation_profile_digest,
        fact_set_digest=fact_set_document["fact_set_digest"],
        observation_domain_digest=observation_domain[
            "observation_domain_digest"
        ],
        observation_domain_bytes=canonical_json_bytes(observation_domain),
        fact_phase_results=fact_phases,  # type: ignore[arg-type]
        relation_phase_results=phases,
        relation_provider_run_bytes=tuple(
            canonical_json_bytes(item) for item in provider_runs
        ),
        observation_receipt_bytes=tuple(
            canonical_json_bytes(item) for item in receipts
        ),
        required_source_set_terminal_closure=terminal_closure,
        required_observation_closure=observation_closure,
        candidate_composition_status=composition_status,
        qualification_status=qualification_status,
        merged_candidate_bytes=tuple(
            canonical_json_bytes(item) for item in merged
        ),
        private_conflict_bytes=tuple(
            canonical_json_bytes(item) for item in conflicts
        ),
        reason_codes=reasons,
        qualification_digest=qualification_digest,
    )


def _observation_receipt(
    domain: Mapping[str, object],
    descriptor: ProviderDescriptor,
    phase: OwnedRelationObservationCellPhaseResult | None,
) -> dict[str, object]:
    responsibilities = [
        item
        for item in domain["provider_responsibilities"]
        if item["provider_descriptor"] == descriptor.document()
    ]
    if len(responsibilities) != 1:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )
    assigned = list(responsibilities[0]["assigned_observation_item_ids"])
    if phase is None:
        return _receipt_document(
            provider_run_id=None,
            descriptor=descriptor,
            execution_status="NOT_STARTED",
            assigned=assigned,
            accepted=[],
            missing=assigned,
        )
    if (
        phase.provider_descriptor != descriptor
        or phase.source_snapshot_digest != domain["source_snapshot_digest"]
        or phase.policy_digest != domain["policy_digest"]
        or phase.analysis_scope_digest != domain["analysis_scope_digest"]
        or phase.derivation_profile_digest
        != domain["derivation_profile_digest"]
        or phase.fact_set_digest != domain["fact_set_digest"]
        or phase.observation_domain_digest != domain["observation_domain_digest"]
        or list(phase.assigned_observation_item_ids) != assigned
        or phase.release_outcome is not ReleaseOutcome.RELEASED
    ):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )
    _validate_phase_terminal_invariants(phase)
    if phase.provider_run_status is not ProviderRunStatus.COMPLETED:
        return _receipt_document(
            provider_run_id=phase.provider_run_id,
            descriptor=descriptor,
            execution_status=phase.provider_run_status.value,
            assigned=assigned,
            accepted=[],
            missing=assigned,
        )
    outcomes = list(phase.observation_outcomes_copy())
    relations = {
        item["relation_id"]: item for item in phase.canonical_relations_copy()
    }
    items = {
        item["observation_item_id"]: item
        for item in domain["observation_items"]
    }
    by_item: dict[str, list[dict[str, object]]] = {}
    unexpected_items: set[str] = set()
    for outcome in outcomes:
        item_id = outcome.get("observation_item_id")
        if not isinstance(item_id, str):
            continue
        by_item.setdefault(item_id, []).append(outcome)
        if item_id not in assigned:
            unexpected_items.add(item_id)
    duplicate_items = {
        item_id for item_id, values in by_item.items() if len(values) > 1
    }
    accepted: list[dict[str, object]] = []
    invalid_outcomes: set[str] = set()
    unexpected_relation_ids: set[str] = set()
    accepted_relation_ids: set[str] = set()
    for item_id, values in by_item.items():
        for outcome in values:
            outcome_id = outcome.get("observation_outcome_id")
            if not isinstance(outcome_id, str):
                continue
            valid = (
                item_id in assigned
                and item_id not in duplicate_items
                and _valid_outcome_identity(outcome, phase.provider_run_id)
            )
            relation_ids = outcome.get("reported_relation_ids")
            item = items.get(item_id)
            if valid and item is not None:
                rule = family_rule_for_item(
                    item,
                    derivation_profile_digest=phase.derivation_profile_digest,
                )
                if outcome["disposition"] == "CANDIDATE_REPORTED":
                    valid = (
                        isinstance(relation_ids, list)
                        and len(relation_ids) == 1
                        and relation_ids == sorted(set(relation_ids))
                    )
                elif outcome["disposition"] == "NO_CANDIDATE_OBSERVED":
                    valid = bool(rule["negative_outcome_allowed"]) and relation_ids == []
                else:
                    valid = False
            if valid and outcome["disposition"] == "CANDIDATE_REPORTED":
                relation_id = relation_ids[0]
                relation = relations.get(relation_id)
                if relation is None or _relation_item_id(relation, items) != item_id:
                    valid = False
                    unexpected_relation_ids.add(relation_id)
                else:
                    accepted_relation_ids.add(relation_id)
            if valid:
                accepted.append(copy.deepcopy(outcome))
            else:
                invalid_outcomes.add(outcome_id)
    accepted.sort(key=lambda item: item["observation_outcome_id"])
    accepted_items = {item["observation_item_id"] for item in accepted}
    missing = sorted(set(assigned) - accepted_items)
    unreferenced = sorted(set(relations) - accepted_relation_ids)
    for relation_id, relation in relations.items():
        mapped = _relation_item_id(relation, items)
        if mapped not in assigned:
            unexpected_relation_ids.add(relation_id)
    return _receipt_document(
        provider_run_id=phase.provider_run_id,
        descriptor=descriptor,
        execution_status=phase.provider_run_status.value,
        assigned=assigned,
        accepted=accepted,
        missing=missing,
        unexpected_items=sorted(unexpected_items),
        duplicate_items=sorted(duplicate_items),
        unexpected_relation_ids=sorted(unexpected_relation_ids),
        unreferenced_relation_ids=unreferenced,
        invalid_outcome_ids=sorted(invalid_outcomes),
    )


def _receipt_document(
    *,
    provider_run_id: str | None,
    descriptor: ProviderDescriptor,
    execution_status: str,
    assigned: Sequence[str],
    accepted: Sequence[Mapping[str, object]],
    missing: Sequence[str],
    unexpected_items: Sequence[str] = (),
    duplicate_items: Sequence[str] = (),
    unexpected_relation_ids: Sequence[str] = (),
    unreferenced_relation_ids: Sequence[str] = (),
    invalid_outcome_ids: Sequence[str] = (),
) -> dict[str, object]:
    return {
        "provider_run_id": provider_run_id,
        "provider_descriptor": descriptor.document(),
        "required": True,
        "execution_status": execution_status,
        "assigned_observation_item_ids": sorted(set(assigned)),
        "accepted_observation_outcomes": copy.deepcopy(list(accepted)),
        "missing_observation_item_ids": sorted(set(missing)),
        "unexpected_observation_item_ids": sorted(set(unexpected_items)),
        "duplicate_observation_item_ids": sorted(set(duplicate_items)),
        "unexpected_relation_ids": sorted(set(unexpected_relation_ids)),
        "unreferenced_relation_ids": sorted(set(unreferenced_relation_ids)),
        "invalid_outcome_ids": sorted(set(invalid_outcome_ids)),
    }


def _validate_phase_terminal_invariants(
    phase: OwnedRelationObservationCellPhaseResult,
) -> None:
    relations = phase.canonical_relations_copy()
    outcomes = phase.observation_outcomes_copy()
    relation_ids = [item["relation_id"] for item in relations]
    if (
        tuple(relation_ids) != phase.reported_relation_ids
        or relation_ids != sorted(set(relation_ids))
        or list(phase.assigned_observation_item_ids)
        != sorted(set(phase.assigned_observation_item_ids))
        or any(
            relation.get("provenance_refs") != [phase.provider_run_id]
            for relation in relations
        )
        or any(
            canonical_json_bytes(item) != raw
            for item, raw in zip(relations, phase.canonical_relation_bytes)
        )
        or any(
            canonical_json_bytes(item) != raw
            for item, raw in zip(outcomes, phase.observation_outcome_bytes)
        )
    ):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )
    expected_phase = {
        ProviderRunStatus.COMPLETED: PhaseStatus.COMPLETED,
        ProviderRunStatus.FAILED: PhaseStatus.FAILED,
        ProviderRunStatus.UNAVAILABLE: PhaseStatus.UNAVAILABLE,
        ProviderRunStatus.INTERRUPTED: PhaseStatus.INTERRUPTED,
    }[phase.provider_run_status]
    if phase.phase_status is not expected_phase:
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )
    if phase.provider_run_status is ProviderRunStatus.COMPLETED:
        if phase.diagnostic_code is not None:
            raise _RelationDerivationError(
                _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
            )
    elif (
        phase.diagnostic_code is None
        or relations
        or outcomes
        or phase.reported_relation_ids
    ):
        raise _RelationDerivationError(
            _RelationDerivationFailureCode.DERIVATION_INTEGRITY_FAILURE
        )


def _valid_outcome_identity(
    outcome: Mapping[str, object], provider_run_id_value: str
) -> bool:
    try:
        if set(outcome) != {
            "observation_outcome_id",
            "provider_run_id",
            "observation_item_id",
            "disposition",
            "reported_relation_ids",
        }:
            return False
        payload = {
            "provider_run_id": provider_run_id_value,
            "observation_item_id": outcome["observation_item_id"],
            "disposition": outcome["disposition"],
            "reported_relation_ids": copy.deepcopy(
                outcome["reported_relation_ids"]
            ),
        }
        return (
            outcome["provider_run_id"] == provider_run_id_value
            and outcome["observation_outcome_id"]
            == semantic_digest(
                "veritrail.review.relation-observation-outcome/0.1", payload
            )
        )
    except Exception:
        return False


def _relation_item_id(
    relation: Mapping[str, object],
    items: Mapping[str, Mapping[str, object]],
) -> str | None:
    kind = relation.get("relation_kind")
    if kind == "LEXICAL_CONTAINS":
        target = relation.get("target")
        subject_fact_id = target.get("fact_id") if isinstance(target, Mapping) else None
    elif kind == "IMPORT_TARGET_LITERAL":
        subject_fact_id = relation.get("source_fact_id")
    else:
        return None
    matches = [
        item_id
        for item_id, item in items.items()
        if item["relation_kind"] == kind
        and item["subject_fact_id"] == subject_fact_id
    ]
    return matches[0] if len(matches) == 1 else None


def _receipt_complete(receipt: Mapping[str, object]) -> bool:
    return (
        receipt["execution_status"] == "COMPLETED"
        and len(receipt["accepted_observation_outcomes"])
        == len(receipt["assigned_observation_item_ids"])
        and all(
            receipt[key] == []
            for key in (
                "missing_observation_item_ids",
                "unexpected_observation_item_ids",
                "duplicate_observation_item_ids",
                "unexpected_relation_ids",
                "unreferenced_relation_ids",
                "invalid_outcome_ids",
            )
        )
    )


class _RelationIdentityCollision(RuntimeError):
    pass


def _compose_candidates(
    phases: Sequence[OwnedRelationObservationCellPhaseResult],
) -> tuple[tuple[dict[str, object], ...], tuple[dict[str, object], ...]]:
    by_id: dict[str, dict[str, object]] = {}
    semantic_by_id: dict[str, bytes] = {}
    for phase in phases:
        for relation in phase.canonical_relations_copy():
            relation_id = relation["relation_id"]
            semantic = {
                key: copy.deepcopy(value)
                for key, value in relation.items()
                if key != "provenance_refs"
            }
            semantic_bytes = canonical_json_bytes(semantic)
            previous = semantic_by_id.setdefault(relation_id, semantic_bytes)
            if previous != semantic_bytes:
                raise _RelationIdentityCollision
            if relation_id not in by_id:
                by_id[relation_id] = copy.deepcopy(relation)
            provenance = set(by_id[relation_id]["provenance_refs"])
            provenance.update(relation["provenance_refs"])
            by_id[relation_id]["provenance_refs"] = sorted(provenance)
    merged = tuple(by_id[key] for key in sorted(by_id))
    by_subject: dict[str, list[dict[str, object]]] = {}
    for relation in merged:
        by_subject.setdefault(relation["relation_subject_digest"], []).append(
            relation
        )
    conflicts: list[dict[str, object]] = []
    for subject, candidates in by_subject.items():
        ids = sorted({item["relation_id"] for item in candidates})
        if len(ids) < 2:
            continue
        provenance = sorted(
            {
                ref
                for candidate in candidates
                for ref in candidate["provenance_refs"]
            }
        )
        conflicts.append(
            {
                "conflict_id": semantic_digest(
                    "veritrail.review.relation-conflict/0.1",
                    {
                        "relation_subject_digest": subject,
                        "candidate_relation_ids": ids,
                    },
                ),
                "relation_subject_digest": subject,
                "candidate_relation_ids": ids,
                "provenance_refs": provenance,
            }
        )
    conflicts.sort(key=lambda item: item["conflict_id"])
    return merged, tuple(conflicts)


def _reason_codes(
    receipts: Sequence[Mapping[str, object]],
    *,
    identity_collision: bool,
    shared_failure: bool,
    release_failure: bool,
) -> tuple[str, ...]:
    reasons: set[str] = set()
    status_reason = {
        "NOT_STARTED": "REQUIRED_SOURCE_NOT_STARTED",
        "FAILED": "REQUIRED_SOURCE_FAILED",
        "UNAVAILABLE": "REQUIRED_SOURCE_UNAVAILABLE",
        "INTERRUPTED": "REQUIRED_SOURCE_INTERRUPTED",
    }
    for receipt in receipts:
        reason = status_reason.get(receipt["execution_status"])
        if reason:
            reasons.add(reason)
        if receipt["missing_observation_item_ids"]:
            reasons.add("OBSERVATION_OUTCOME_MISSING")
        if receipt["unexpected_observation_item_ids"]:
            reasons.add("OBSERVATION_OUTCOME_UNEXPECTED")
        if receipt["duplicate_observation_item_ids"]:
            reasons.add("OBSERVATION_OUTCOME_DUPLICATE")
        if receipt["invalid_outcome_ids"]:
            reasons.add("OBSERVATION_OUTCOME_INVALID")
        if receipt["unexpected_relation_ids"]:
            reasons.add("OBSERVATION_CANDIDATE_REFERENCE_MISMATCH")
        if receipt["unreferenced_relation_ids"]:
            reasons.add("UNEXPECTED_RELATION_CANDIDATE")
    if identity_collision:
        reasons.add("RELATION_IDENTITY_COLLISION")
    if shared_failure:
        reasons.add("SHARED_CONTEXT_FAILURE")
    if release_failure:
        reasons.add("RELEASE_FAILURE")
    return tuple(sorted(reasons, key=lambda item: _REASON_RANK[item]))


def _provider_run_document(
    phase: OwnedRelationObservationCellPhaseResult,
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


def _owned_object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError
    return value
