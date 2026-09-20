from __future__ import annotations

import copy
import io
import os
import sys
from pathlib import Path
from threading import Lock
from typing import Callable, Mapping

from veritrail_review._execution_cell import (
    _admission_stop_error,
    _internal_failure,
    _map_terminal_kind,
    _utc_now,
)
from veritrail_review._execution_cell_binding import ProviderBinding
from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    FrameProtocolError,
    encode_frame,
    read_frame,
)
from veritrail_review._execution_cell_values import (
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
from veritrail_review._relation_execution_cell_application import (
    RelationApplicationProtocolError,
    build_relation_request_document,
    validate_relation_terminal_document,
)
from veritrail_review._relation_execution_cell_binding import (
    relation_binding_matches_closed_allow_list,
)
from veritrail_review._relation_execution_cell_values import (
    OwnedRelationExecutionCellPhaseResult,
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


class _PreparedRelationExecutionAttempt:
    """One Relation attempt bound to its caller-owned derivation context."""

    def __init__(
        self,
        *,
        inputs: DerivationInputSet,
        derivation_id: str,
        binding: ProviderBinding,
        cancellation_requested: Callable[[], bool] | None,
        transport_limits: ExecutionCellTransportSafetyLimits,
        context: BudgetContext,
        eligibility: AttemptEligibility,
        request_provenance: Mapping[str, object],
        attempt_started_at: str,
        fact_set_document: Mapping[str, object],
        request_document: Mapping[str, object],
        request_frame: bytes,
    ) -> None:
        self.inputs = inputs
        self.derivation_id = str(derivation_id)
        self.binding = ProviderBinding(binding.descriptor, str(binding.launch_key))
        self.cancellation_requested = cancellation_requested
        self.transport_limits = transport_limits
        self.context = context
        self.eligibility = eligibility
        self.request_provenance = copy.deepcopy(dict(request_provenance))
        self.attempt_started_at = str(attempt_started_at)
        self.fact_set_document = copy.deepcopy(dict(fact_set_document))
        self.request_document = copy.deepcopy(dict(request_document))
        self.request_frame = memoryview(request_frame).tobytes()
        self._lock = Lock()
        self._consumed = False

    def claim_for_execution(self) -> None:
        with self._lock:
            if self._consumed:
                raise DerivationExecutionCellError(
                    DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
                )
            self._consumed = True


def _build_prepared_relation_execution_attempt(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
    context: BudgetContext,
    eligibility: AttemptEligibility,
    request_provenance: Mapping[str, object],
    attempt_started_at: str,
    fact_set_document: Mapping[str, object],
) -> _PreparedRelationExecutionAttempt:
    if (
        not isinstance(inputs, DerivationInputSet)
        or not isinstance(derivation_id, str)
        or not derivation_id
        or any(0xD800 <= ord(character) <= 0xDFFF for character in derivation_id)
        or not relation_binding_matches_closed_allow_list(binding)
        or not isinstance(context, BudgetContext)
        or context.state is not BudgetState.RUNNING
        or not isinstance(eligibility, AttemptEligibility)
        or eligibility.state is not AttemptEligibilityState.PROVISIONAL
        or (cancellation_requested is not None and not callable(cancellation_requested))
        or not isinstance(transport_limits, ExecutionCellTransportSafetyLimits)
        or not isinstance(request_provenance, Mapping)
        or not isinstance(attempt_started_at, str)
        or not attempt_started_at
        or not isinstance(fact_set_document, Mapping)
    ):
        if isinstance(eligibility, AttemptEligibility):
            eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )
    try:
        request_document = build_relation_request_document(
            inputs=inputs,
            derivation_id=derivation_id,
            request_provenance=request_provenance,
            descriptor=binding.descriptor,
            fact_set_document=fact_set_document,
        )
        request_frame = encode_frame(
            request_document,
            payload_limit=transport_limits.request_payload_bytes,
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
    return _PreparedRelationExecutionAttempt(
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        fact_set_document=fact_set_document,
        request_document=request_document,
        request_frame=request_frame,
    )


def _run_prepared_relation_execution_attempt(
    prepared: _PreparedRelationExecutionAttempt,
) -> OwnedRelationExecutionCellPhaseResult:
    if not isinstance(prepared, _PreparedRelationExecutionAttempt):
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )
    prepared.claim_for_execution()
    context = prepared.context
    eligibility = prepared.eligibility
    request_document = copy.deepcopy(prepared.request_document)
    provider_started: list[str] = []
    worker = Path(__file__).with_name("_relation_execution_cell_worker.py").resolve()
    arguments = [
        "-I",
        os.fspath(worker),
        prepared.binding.launch_key,
        str(prepared.transport_limits.request_payload_bytes),
        str(prepared.transport_limits.terminal_payload_bytes),
    ]
    try:
        observation = run_windows_execution_cell(
            context,
            eligibility,
            executable=Path(sys.executable).resolve(),
            arguments=arguments,
            request_frame=prepared.request_frame,
            terminal_payload_limit=prepared.transport_limits.terminal_payload_bytes,
            cancellation_requested=prepared.cancellation_requested,
            on_admitted=lambda: provider_started.append(_utc_now()),
        )
    except CellRuntimeUnavailableError as exc:
        eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.DERIVATION_RUNTIME_UNAVAILABLE
        ) from exc
    except CellPreparationError as exc:
        eligibility.revoke()
        if context.stop_trigger is not None:
            raise _admission_stop_error(context.stop_trigger) from exc
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR
        ) from exc
    except CellReleaseError as exc:
        eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.RELEASE_FAILED
        ) from exc

    if not observation.admitted or len(provider_started) != 1:
        eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR
        )
    provider_started_at = provider_started[0]
    provider_finished_at = _utc_now()
    expected_run_id = _expected_provider_run_id(request_document)

    terminal: dict[str, object] | None = None
    if observation.stop_trigger is not None:
        eligibility.revoke()
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
        eligibility.revoke()
        status = _internal_failure()
    else:
        try:
            untrusted_terminal = read_frame(
                io.BytesIO(observation.terminal_bytes),
                payload_limit=prepared.transport_limits.terminal_payload_bytes,
            )
            terminal = validate_relation_terminal_document(
                untrusted_terminal, request=request_document
            )
        except (FrameProtocolError, RelationApplicationProtocolError):
            eligibility.revoke()
            status = _internal_failure()
        else:
            status = _map_terminal_kind(terminal["terminal_kind"])
            if status[1] is not PhaseStatus.COMPLETED:
                eligibility.revoke()

    relation_bytes: tuple[bytes, ...] = ()
    relation_ids: tuple[str, ...] = ()
    if status[1] is PhaseStatus.COMPLETED and terminal is not None:
        try:
            committed = (
                eligibility.permits_phase_commit()
                and context.try_complete_phase(
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
            eligibility.revoke()
            if context.stop_trigger is not None:
                status = (
                    ProviderRunStatus.INTERRUPTED,
                    PhaseStatus.INTERRUPTED,
                    context.stop_trigger.value,
                )
                if context.state is BudgetState.STOPPING:
                    context._mark_release(residue_free=True)
            else:
                status = _internal_failure()
        else:
            relation_bytes = tuple(
                canonical_json_bytes(copy.deepcopy(relation))
                for relation in terminal["canonical_relations"]
            )
            relation_ids = tuple(terminal["reported_relation_ids"])

    if status[1] is not PhaseStatus.COMPLETED:
        relation_bytes = ()
        relation_ids = ()
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
        fact_set_digest=request_document["fact_set_digest"],
        provider_descriptor=prepared.binding.descriptor,
        operands_digest=request_document["operands_digest"],
        provider_run_id=expected_run_id,
        attempt_started_at=prepared.attempt_started_at,
        provider_run_started_at=provider_started_at,
        provider_run_finished_at=provider_finished_at,
        phase_finished_at=_utc_now(),
        provider_run_status=status[0],
        phase_status=status[1],
        diagnostic_code=status[2],
        canonical_relation_bytes=relation_bytes,
        reported_fact_ids=(),
        reported_relation_ids=relation_ids,
        release_outcome=ReleaseOutcome.RELEASED,
    )


def _expected_provider_run_id(request: Mapping[str, object]) -> str:
    from veritrail_review._execution_cell_application import provider_run_id
    from veritrail_review._execution_cell_binding import ProviderDescriptor

    descriptor = ProviderDescriptor(**request["provider_descriptor"])
    return provider_run_id(
        request["derivation_id"], descriptor, request["operands_digest"]
    )
