from __future__ import annotations

import copy
import io
import os
import sys
from pathlib import Path
from typing import Callable, Mapping

from veritrail_review._execution_cell import (
    _admission_stop_error,
    _internal_failure,
    _map_terminal_kind,
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
    FrameProtocolError,
    encode_frame,
    read_frame,
)
from veritrail_review._execution_cell_values import (
    OwnedExecutionCellPhaseResult,
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
)
from veritrail_review._relation_execution_cell_binding import (
    relation_binding_matches_closed_allow_list,
)
from veritrail_review._relation_execution_cell_values import (
    OwnedRelationExecutionCellPhaseResult,
)
from veritrail_review._relation_observation_binding import (
    relation_observation_binding_matches_allow_list,
)
from veritrail_review._relation_observation_cell_values import (
    OwnedRelationObservationCellPhaseResult,
)
from veritrail_review._source_operation_fact_application import (
    FactSourceOperationProtocolError,
    build_fact_source_operation_request_document,
    validate_fact_source_operation_terminal_document,
)
from veritrail_review._source_operation_gate import (
    ClaimedSourceOperationRequest,
    OwnedSourceOperationAttemptGate,
    OwnedSourceOperationChildClaim,
)
from veritrail_review._source_operation_projection import (
    build_fact_derivation_source_operation_projection,
    build_relation_derivation_source_operation_projection,
    build_relation_observation_source_operation_projection,
)
from veritrail_review._source_operation_projection_values import (
    OwnedSourceOperationProjection,
)
from veritrail_review._source_operation_relation_derivation_application import (
    RelationSourceOperationProtocolError,
    build_relation_source_operation_request_document,
    validate_relation_source_operation_terminal_document,
)
from veritrail_review._source_operation_relation_observation_application import (
    RelationObservationSourceOperationProtocolError,
    build_relation_observation_source_operation_request_document,
    validate_relation_observation_source_operation_terminal_document,
)
from veritrail_review._windows_execution_cell import (
    CellPreparationError,
    CellReleaseError,
    CellRuntimeUnavailableError,
    run_windows_execution_cell,
)
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import canonical_json_bytes
from veritrail_review.derivation_input_contracts import DerivationInputSet
from veritrail_review.errors import (
    BudgetPrimitiveError,
    DerivationExecutionCellError,
    DerivationExecutionCellFailureCode,
)


class _PreparedSourceOperationAttempt:
    """Transport state for one controller-owned, already-bound child claim."""

    def __init__(
        self,
        *,
        inputs: DerivationInputSet,
        derivation_id: str,
        binding: ProviderBinding,
        cancellation_requested: Callable[[], bool] | None,
        transport_limits: ExecutionCellTransportSafetyLimits,
        context: BudgetContext,
        parent_eligibility: AttemptEligibility,
        eligibility: AttemptEligibility,
        request_provenance: Mapping[str, object],
        attempt_started_at: str,
        classification: OwnedLanguageSupportClassification,
        projection: OwnedSourceOperationProjection,
        request_document: Mapping[str, object],
        request_frame: bytes,
        claim: OwnedSourceOperationChildClaim,
    ) -> None:
        self.inputs = inputs
        self.derivation_id = str(derivation_id)
        self.binding = ProviderBinding(binding.descriptor, str(binding.launch_key))
        self.cancellation_requested = cancellation_requested
        self.transport_limits = transport_limits
        self.context = context
        self.parent_eligibility = parent_eligibility
        self.eligibility = eligibility
        self.request_provenance = copy.deepcopy(dict(request_provenance))
        self.attempt_started_at = str(attempt_started_at)
        self.classification = classification
        self.projection = projection
        self.request_document = copy.deepcopy(dict(request_document))
        self.request_frame = memoryview(request_frame).tobytes()
        self.claim = claim


class _PreparedFactSourceOperationAttempt(_PreparedSourceOperationAttempt):
    pass


class _PreparedRelationSourceOperationAttempt(_PreparedSourceOperationAttempt):
    pass


class _PreparedRelationObservationSourceOperationAttempt(
    _PreparedSourceOperationAttempt
):
    pass


def build_prepared_fact_source_operation_attempt(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
    context: BudgetContext,
    parent_eligibility: AttemptEligibility,
    eligibility: AttemptEligibility,
    request_provenance: Mapping[str, object],
    attempt_started_at: str,
    classification: OwnedLanguageSupportClassification,
    source_operation_gate: OwnedSourceOperationAttemptGate,
) -> _PreparedFactSourceOperationAttempt:
    _validate_common_builder_input(
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        binding_allowed=binding_matches_closed_allow_list(binding),
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        parent_eligibility=parent_eligibility,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        classification=classification,
        source_operation_gate=source_operation_gate,
    )
    projection = build_fact_derivation_source_operation_projection(
        classification, binding.descriptor
    )
    request_document = build_fact_source_operation_request_document(
        inputs=inputs,
        derivation_id=derivation_id,
        request_provenance=request_provenance,
        descriptor=binding.descriptor,
        classification=classification,
        projection=projection,
    )
    return _bind_prepared_attempt(
        prepared_type=_PreparedFactSourceOperationAttempt,
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        parent_eligibility=parent_eligibility,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        classification=classification,
        projection=projection,
        request_document=request_document,
        source_operation_gate=source_operation_gate,
    )


def build_prepared_relation_source_operation_attempt(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
    context: BudgetContext,
    parent_eligibility: AttemptEligibility,
    eligibility: AttemptEligibility,
    request_provenance: Mapping[str, object],
    attempt_started_at: str,
    fact_set_document: Mapping[str, object],
    classification: OwnedLanguageSupportClassification,
    source_operation_gate: OwnedSourceOperationAttemptGate,
) -> _PreparedRelationSourceOperationAttempt:
    _validate_common_builder_input(
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        binding_allowed=relation_binding_matches_closed_allow_list(binding),
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        parent_eligibility=parent_eligibility,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        classification=classification,
        source_operation_gate=source_operation_gate,
    )
    projection = build_relation_derivation_source_operation_projection(
        classification, binding.descriptor, fact_set_document
    )
    request_document = build_relation_source_operation_request_document(
        inputs=inputs,
        derivation_id=derivation_id,
        request_provenance=request_provenance,
        descriptor=binding.descriptor,
        fact_set_document=fact_set_document,
        classification=classification,
        projection=projection,
    )
    return _bind_prepared_attempt(
        prepared_type=_PreparedRelationSourceOperationAttempt,
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        parent_eligibility=parent_eligibility,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        classification=classification,
        projection=projection,
        request_document=request_document,
        source_operation_gate=source_operation_gate,
    )


def build_prepared_relation_observation_source_operation_attempt(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
    context: BudgetContext,
    parent_eligibility: AttemptEligibility,
    eligibility: AttemptEligibility,
    request_provenance: Mapping[str, object],
    attempt_started_at: str,
    fact_set_document: Mapping[str, object],
    observation_domain: Mapping[str, object],
    classification: OwnedLanguageSupportClassification,
    source_operation_gate: OwnedSourceOperationAttemptGate,
) -> _PreparedRelationObservationSourceOperationAttempt:
    _validate_common_builder_input(
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        binding_allowed=relation_observation_binding_matches_allow_list(binding),
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        parent_eligibility=parent_eligibility,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        classification=classification,
        source_operation_gate=source_operation_gate,
    )
    projection = build_relation_observation_source_operation_projection(
        classification,
        binding.descriptor,
        fact_set_document,
        observation_domain,
    )
    request_document = build_relation_observation_source_operation_request_document(
        inputs=inputs,
        derivation_id=derivation_id,
        request_provenance=request_provenance,
        descriptor=binding.descriptor,
        fact_set_document=fact_set_document,
        observation_domain=observation_domain,
        classification=classification,
        projection=projection,
    )
    return _bind_prepared_attempt(
        prepared_type=_PreparedRelationObservationSourceOperationAttempt,
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        parent_eligibility=parent_eligibility,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        classification=classification,
        projection=projection,
        request_document=request_document,
        source_operation_gate=source_operation_gate,
    )


def run_prepared_fact_source_operation_attempt(
    prepared: _PreparedFactSourceOperationAttempt,
) -> OwnedExecutionCellPhaseResult:
    terminal, status, started, finished = _run_claimed_attempt(
        prepared,
        worker_name="_source_operation_fact_worker.py",
        terminal_validator=validate_fact_source_operation_terminal_document,
        protocol_errors=(FactSourceOperationProtocolError,),
    )
    facts: tuple[bytes, ...] = ()
    fact_ids: tuple[str, ...] = ()
    if status[1] is PhaseStatus.COMPLETED and terminal is not None:
        facts = tuple(
            canonical_json_bytes(copy.deepcopy(item))
            for item in terminal["canonical_facts"]
        )
        fact_ids = tuple(terminal["reported_fact_ids"])
    request = prepared.request_document
    return OwnedExecutionCellPhaseResult(
        derivation_id=prepared.derivation_id,
        request_provenance_bytes=canonical_json_bytes(prepared.request_provenance),
        source_snapshot_digest=prepared.inputs.source_snapshot_digest,
        policy_digest=prepared.inputs.policy_digest,
        analysis_scope_digest=prepared.inputs.analysis_scope_digest,
        slice_policy_digest=prepared.inputs.slice_policy_digest,
        derivation_profile_digest=prepared.inputs.derivation_profile_digest,
        provider_descriptor=ProviderDescriptor(**request["provider_descriptor"]),
        operands_digest=request["operands_digest"],
        provider_run_id=_provider_run_id(request),
        attempt_started_at=prepared.attempt_started_at,
        provider_run_started_at=started,
        provider_run_finished_at=finished,
        phase_finished_at=_utc_now(),
        provider_run_status=status[0],
        phase_status=status[1],
        diagnostic_code=status[2],
        canonical_fact_bytes=facts,
        reported_fact_ids=fact_ids,
        reported_relation_ids=(),
        release_outcome=ReleaseOutcome.RELEASED,
    )


def run_prepared_relation_source_operation_attempt(
    prepared: _PreparedRelationSourceOperationAttempt,
) -> OwnedRelationExecutionCellPhaseResult:
    terminal, status, started, finished = _run_claimed_attempt(
        prepared,
        worker_name="_source_operation_relation_derivation_worker.py",
        terminal_validator=validate_relation_source_operation_terminal_document,
        protocol_errors=(RelationSourceOperationProtocolError,),
    )
    relations: tuple[bytes, ...] = ()
    relation_ids: tuple[str, ...] = ()
    if status[1] is PhaseStatus.COMPLETED and terminal is not None:
        relations = tuple(
            canonical_json_bytes(copy.deepcopy(item))
            for item in terminal["canonical_relations"]
        )
        relation_ids = tuple(terminal["reported_relation_ids"])
    request = prepared.request_document
    return OwnedRelationExecutionCellPhaseResult(
        derivation_id=prepared.derivation_id,
        request_provenance_bytes=canonical_json_bytes(
            prepared.request_provenance
        ),
        source_snapshot_digest=prepared.inputs.source_snapshot_digest,
        policy_digest=prepared.inputs.policy_digest,
        analysis_scope_digest=prepared.inputs.analysis_scope_digest,
        slice_policy_digest=prepared.inputs.slice_policy_digest,
        derivation_profile_digest=prepared.inputs.derivation_profile_digest,
        fact_set_digest=request["fact_set_digest"],
        provider_descriptor=ProviderDescriptor(**request["provider_descriptor"]),
        operands_digest=request["operands_digest"],
        provider_run_id=_provider_run_id(request),
        attempt_started_at=prepared.attempt_started_at,
        provider_run_started_at=started,
        provider_run_finished_at=finished,
        phase_finished_at=_utc_now(),
        provider_run_status=status[0],
        phase_status=status[1],
        diagnostic_code=status[2],
        canonical_relation_bytes=relations,
        reported_fact_ids=(),
        reported_relation_ids=relation_ids,
        release_outcome=ReleaseOutcome.RELEASED,
    )


def run_prepared_relation_observation_source_operation_attempt(
    prepared: _PreparedRelationObservationSourceOperationAttempt,
) -> OwnedRelationObservationCellPhaseResult:
    terminal, status, started, finished = _run_claimed_attempt(
        prepared,
        worker_name="_source_operation_relation_observation_worker.py",
        terminal_validator=(
            validate_relation_observation_source_operation_terminal_document
        ),
        protocol_errors=(RelationObservationSourceOperationProtocolError,),
    )
    relations: tuple[bytes, ...] = ()
    outcomes: tuple[bytes, ...] = ()
    relation_ids: tuple[str, ...] = ()
    if status[1] is PhaseStatus.COMPLETED and terminal is not None:
        relations = tuple(
            canonical_json_bytes(copy.deepcopy(item))
            for item in terminal["canonical_relations"]
        )
        outcomes = tuple(
            canonical_json_bytes(copy.deepcopy(item))
            for item in terminal["observation_outcomes"]
        )
        relation_ids = tuple(terminal["reported_relation_ids"])
    request = prepared.request_document
    return OwnedRelationObservationCellPhaseResult(
        derivation_id=prepared.derivation_id,
        request_provenance_bytes=canonical_json_bytes(
            prepared.request_provenance
        ),
        source_snapshot_digest=prepared.inputs.source_snapshot_digest,
        policy_digest=prepared.inputs.policy_digest,
        analysis_scope_digest=prepared.inputs.analysis_scope_digest,
        slice_policy_digest=prepared.inputs.slice_policy_digest,
        derivation_profile_digest=prepared.inputs.derivation_profile_digest,
        fact_set_digest=request["fact_set_digest"],
        observation_domain_digest=request["observation_domain_digest"],
        assigned_observation_item_ids=tuple(
            request["assigned_observation_item_ids"]
        ),
        provider_descriptor=ProviderDescriptor(**request["provider_descriptor"]),
        operands_digest=request["operands_digest"],
        provider_run_id=_provider_run_id(request),
        attempt_started_at=prepared.attempt_started_at,
        provider_run_started_at=started,
        provider_run_finished_at=finished,
        phase_finished_at=_utc_now(),
        provider_run_status=status[0],
        phase_status=status[1],
        diagnostic_code=status[2],
        canonical_relation_bytes=relations,
        observation_outcome_bytes=outcomes,
        reported_relation_ids=relation_ids,
        release_outcome=ReleaseOutcome.RELEASED,
    )


def _validate_common_builder_input(
    *,
    inputs: object,
    derivation_id: object,
    binding: object,
    binding_allowed: bool,
    cancellation_requested: object,
    transport_limits: object,
    context: object,
    parent_eligibility: object,
    eligibility: object,
    request_provenance: object,
    attempt_started_at: object,
    classification: object,
    source_operation_gate: object,
) -> None:
    if (
        type(inputs) is not DerivationInputSet
        or not isinstance(derivation_id, str)
        or not derivation_id
        or any(0xD800 <= ord(character) <= 0xDFFF for character in derivation_id)
        or type(binding) is not ProviderBinding
        or not binding_allowed
        or type(context) is not BudgetContext
        or context.state is not BudgetState.RUNNING
        or type(parent_eligibility) is not AttemptEligibility
        or parent_eligibility.state
        not in {AttemptEligibilityState.PROVISIONAL, AttemptEligibilityState.ADMITTED}
        or type(eligibility) is not AttemptEligibility
        or eligibility.state is not AttemptEligibilityState.PROVISIONAL
        or (cancellation_requested is not None and not callable(cancellation_requested))
        or type(transport_limits) is not ExecutionCellTransportSafetyLimits
        or not isinstance(request_provenance, Mapping)
        or not isinstance(attempt_started_at, str)
        or not attempt_started_at
        or type(classification) is not OwnedLanguageSupportClassification
        or type(source_operation_gate) is not OwnedSourceOperationAttemptGate
    ):
        if type(eligibility) is AttemptEligibility:
            eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )


def _bind_prepared_attempt(
    *,
    prepared_type: type[_PreparedSourceOperationAttempt],
    inputs: DerivationInputSet,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
    context: BudgetContext,
    parent_eligibility: AttemptEligibility,
    eligibility: AttemptEligibility,
    request_provenance: Mapping[str, object],
    attempt_started_at: str,
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
    request_document: Mapping[str, object],
    source_operation_gate: OwnedSourceOperationAttemptGate,
) -> _PreparedSourceOperationAttempt:
    try:
        request_frame = encode_frame(
            request_document,
            payload_limit=transport_limits.request_payload_bytes,
        )
        claim = source_operation_gate.bind_child(
            projection=projection,
            request_frame=request_frame,
            transport_limits=transport_limits,
            child_eligibility=eligibility,
        )
    except FrameProtocolError as exc:
        eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.DERIVATION_TRANSPORT_LIMIT_INSUFFICIENT
        ) from exc
    except Exception as exc:
        eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR
        ) from exc
    if cancellation_requested is not None and cancellation_requested():
        context.request_cancellation()
    if not context.checkpoint():
        eligibility.revoke()
        raise _admission_stop_error(context.stop_trigger)
    return prepared_type(
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        parent_eligibility=parent_eligibility,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        classification=classification,
        projection=projection,
        request_document=request_document,
        request_frame=request_frame,
        claim=claim,
    )


def _run_claimed_attempt(
    prepared: _PreparedSourceOperationAttempt,
    *,
    worker_name: str,
    terminal_validator: Callable[..., dict[str, object]],
    protocol_errors: tuple[type[Exception], ...],
) -> tuple[
    dict[str, object] | None,
    tuple[ProviderRunStatus, PhaseStatus, str | None],
    str,
    str,
]:
    if not isinstance(prepared, _PreparedSourceOperationAttempt):
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )
    try:
        claimed = prepared.claim.claim()
        _validate_claimed_identity(prepared, claimed)
        request_frame = claimed._request_frame_copy()
    except Exception as exc:
        prepared.eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR
        ) from exc

    provider_started: list[str] = []
    worker = Path(__file__).with_name(worker_name).resolve()
    arguments = [
        "-I",
        os.fspath(worker),
        prepared.binding.launch_key,
        str(prepared.transport_limits.request_payload_bytes),
        str(prepared.transport_limits.terminal_payload_bytes),
    ]
    try:
        observation = run_windows_execution_cell(
            prepared.context,
            prepared.eligibility,
            executable=Path(sys.executable).resolve(),
            arguments=arguments,
            request_frame=request_frame,
            terminal_payload_limit=prepared.transport_limits.terminal_payload_bytes,
            cancellation_requested=prepared.cancellation_requested,
            on_admitted=lambda: provider_started.append(_utc_now()),
        )
    except CellRuntimeUnavailableError as exc:
        prepared.eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.DERIVATION_RUNTIME_UNAVAILABLE
        ) from exc
    except CellPreparationError as exc:
        prepared.eligibility.revoke()
        if prepared.context.stop_trigger is not None:
            raise _admission_stop_error(prepared.context.stop_trigger) from exc
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR
        ) from exc
    except CellReleaseError as exc:
        prepared.eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.RELEASE_FAILED
        ) from exc

    if not observation.admitted or len(provider_started) != 1:
        prepared.eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR
        )
    started = provider_started[0]
    finished = _utc_now()
    terminal: dict[str, object] | None = None
    if observation.stop_trigger is not None:
        prepared.eligibility.revoke()
        status = (
            ProviderRunStatus.INTERRUPTED,
            PhaseStatus.INTERRUPTED,
            observation.stop_trigger.value,
        )
    elif (
        observation.request_channel_failed
        or observation.result_channel_failed
        or observation.result_transport_exceeded
    ):
        prepared.eligibility.revoke()
        status = _internal_failure()
    else:
        try:
            untrusted = read_frame(
                io.BytesIO(observation.terminal_bytes),
                payload_limit=prepared.transport_limits.terminal_payload_bytes,
            )
            terminal = terminal_validator(
                untrusted, request=prepared.request_document
            )
        except (FrameProtocolError, *protocol_errors):
            prepared.eligibility.revoke()
            status = _internal_failure()
        else:
            status = _map_terminal_kind(terminal["terminal_kind"])
            if status[1] is not PhaseStatus.COMPLETED:
                prepared.eligibility.revoke()

    if status[1] is PhaseStatus.COMPLETED and terminal is not None:
        try:
            committed = (
                prepared.eligibility.permits_phase_commit()
                and prepared.context.try_complete_phase(
                    canonical_json_bytes(terminal),
                    resources_closed=(
                        observation.active_process_zero
                        and observation.handles_released
                        and observation.channel_threads_released
                    ),
                )
                is not None
            )
        except BudgetPrimitiveError:
            committed = False
        if not committed:
            prepared.eligibility.revoke()
            terminal = None
            if prepared.context.stop_trigger is not None:
                status = (
                    ProviderRunStatus.INTERRUPTED,
                    PhaseStatus.INTERRUPTED,
                    prepared.context.stop_trigger.value,
                )
                if prepared.context.state is BudgetState.STOPPING:
                    prepared.context._mark_release(residue_free=True)
            else:
                status = _internal_failure()
    return terminal, status, started, finished


def _validate_claimed_identity(
    prepared: _PreparedSourceOperationAttempt,
    claimed: ClaimedSourceOperationRequest,
) -> None:
    if (
        type(claimed) is not ClaimedSourceOperationRequest
        or claimed._owned_inputs() is not prepared.inputs
        or claimed._owned_classification() is not prepared.classification
        or claimed._owned_projection() is not prepared.projection
        or claimed._context() is not prepared.context
        or claimed._parent_eligibility() is not prepared.parent_eligibility
        or claimed._child_eligibility() is not prepared.eligibility
        or claimed._transport_limits() is not prepared.transport_limits
        or claimed._request_frame_copy() != prepared.request_frame
    ):
        raise ValueError("claimed source operation identity changed")


def _provider_run_id(request: Mapping[str, object]) -> str:
    from veritrail_review._execution_cell_application import provider_run_id

    return provider_run_id(
        request["derivation_id"],
        ProviderDescriptor(**request["provider_descriptor"]),
        request["operands_digest"],
    )
