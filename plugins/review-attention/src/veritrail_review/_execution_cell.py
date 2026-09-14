from __future__ import annotations

import copy
import io
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Callable

from veritrail_review._execution_cell_application import (
    ApplicationProtocolError,
    build_request_document,
    validate_terminal_document,
)
from veritrail_review._execution_cell_binding import (
    ProviderBinding,
    ProviderDescriptor,
    binding_is_multi_provider_only,
    binding_matches_closed_allow_list,
)
from veritrail_review._execution_cell_protocol import (
    MAX_REQUEST_PAYLOAD_BYTES,
    MAX_TERMINAL_PAYLOAD_BYTES,
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
from veritrail_review._windows_budget import require_budget_primitive_capability
from veritrail_review._windows_execution_cell import (
    CellPreparationError,
    CellReleaseError,
    CellRuntimeUnavailableError,
    run_windows_execution_cell,
)
from veritrail_review.budget import (
    BudgetContext,
    BudgetState,
    BudgetStopTrigger,
    admit_derivation_budget,
)
from veritrail_review.canonical import canonical_json_bytes
from veritrail_review.derivation_input_contracts import DerivationInputSet
from veritrail_review.errors import (
    BudgetPrimitiveError,
    DerivationExecutionCellError,
    DerivationExecutionCellFailureCode,
)


DEFAULT_TRANSPORT_LIMITS = ExecutionCellTransportSafetyLimits(
    request_payload_bytes=MAX_REQUEST_PAYLOAD_BYTES,
    terminal_payload_bytes=MAX_TERMINAL_PAYLOAD_BYTES,
)


class _PreparedExecutionAttempt:
    """One controller-owned attempt state; it may enter the cell exactly once."""

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
        request_provenance: dict[str, object],
        attempt_started_at: str,
        request_document: dict[str, object],
        request_frame: bytes,
    ) -> None:
        self.inputs = inputs
        self.derivation_id = derivation_id
        self.binding = binding
        self.cancellation_requested = cancellation_requested
        self.transport_limits = transport_limits
        self.context = context
        self.eligibility = eligibility
        self.request_provenance = copy.deepcopy(request_provenance)
        self.attempt_started_at = attempt_started_at
        self.request_document = copy.deepcopy(request_document)
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


def run_closed_test_execution_cell(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None = None,
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
) -> OwnedExecutionCellPhaseResult:
    """Run the frozen closed-provider phase without publishing any Artifact."""

    prepared = _prepare_closed_test_execution_attempt(
        inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    return _run_prepared_closed_test_execution_attempt(prepared)


def _prepare_closed_test_execution_attempt(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
) -> _PreparedExecutionAttempt:
    """Create the one private state shared by the cell and later R1 phases."""

    _validate_attempt_request(
        inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
    )
    if (
        not binding_matches_closed_allow_list(binding)
        or binding_is_multi_provider_only(binding)
    ):
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.PROVIDER_BINDING_MISMATCH
        )
    try:
        require_budget_primitive_capability()
    except BudgetPrimitiveError as exc:
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.DERIVATION_RUNTIME_UNAVAILABLE
        ) from exc

    request_provenance = _owned_request_provenance(inputs)
    attempt_started_at = _utc_now()
    try:
        context = admit_derivation_budget(inputs)
    except BudgetPrimitiveError as exc:
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        ) from exc
    return _build_prepared_closed_test_execution_attempt(
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


def _build_prepared_closed_test_execution_attempt(
    inputs: DerivationInputSet,
    *,
    derivation_id: str,
    binding: ProviderBinding,
    cancellation_requested: Callable[[], bool] | None,
    transport_limits: ExecutionCellTransportSafetyLimits,
    context: BudgetContext,
    eligibility: AttemptEligibility,
    request_provenance: dict[str, object],
    attempt_started_at: str,
) -> _PreparedExecutionAttempt:
    """Build one child cell against caller-owned parent attempt state."""

    if (
        not isinstance(inputs, DerivationInputSet)
        or not isinstance(binding, ProviderBinding)
        or not isinstance(binding.descriptor, ProviderDescriptor)
        or not binding_matches_closed_allow_list(binding)
        or not isinstance(context, BudgetContext)
        or context.state is not BudgetState.RUNNING
        or not isinstance(eligibility, AttemptEligibility)
        or eligibility.state is not AttemptEligibilityState.PROVISIONAL
        or not isinstance(request_provenance, dict)
        or not isinstance(attempt_started_at, str)
        or not attempt_started_at
    ):
        if isinstance(eligibility, AttemptEligibility):
            eligibility.revoke()
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )
    try:
        request_document = build_request_document(
            inputs=inputs,
            derivation_id=derivation_id,
            request_provenance=request_provenance,
            descriptor=binding.descriptor,
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

    return _PreparedExecutionAttempt(
        inputs=inputs,
        derivation_id=derivation_id,
        binding=binding,
        cancellation_requested=cancellation_requested,
        transport_limits=transport_limits,
        context=context,
        eligibility=eligibility,
        request_provenance=request_provenance,
        attempt_started_at=attempt_started_at,
        request_document=request_document,
        request_frame=request_frame,
    )


def _owned_request_provenance(
    inputs: DerivationInputSet,
) -> dict[str, object]:
    snapshot = inputs.source_snapshot_document_copy()
    coordinate = snapshot["source_coordinate"]
    commit_oid = coordinate["commit_oid"]
    return {
        "requested_repository_id": snapshot["repository_id"],
        "requested_ref": f"oid:{commit_oid['algorithm'].lower()}:{commit_oid['hex']}",
        "resolver_id": "veritrail-r1-owned-snapshot-exact-oid",
        "resolver_version": "0.1",
        "resolved_at": _utc_now(),
    }


def _run_prepared_closed_test_execution_attempt(
    prepared: _PreparedExecutionAttempt,
) -> OwnedExecutionCellPhaseResult:
    """Consume an already-owned attempt without rebuilding its budget or inputs."""

    if not isinstance(prepared, _PreparedExecutionAttempt):
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )
    prepared.claim_for_execution()
    inputs = prepared.inputs
    binding = prepared.binding
    cancellation_requested = prepared.cancellation_requested
    transport_limits = prepared.transport_limits
    context = prepared.context
    eligibility = prepared.eligibility
    request_document = copy.deepcopy(prepared.request_document)
    request_provenance = copy.deepcopy(prepared.request_provenance)
    attempt_started_at = prepared.attempt_started_at
    request_frame = memoryview(prepared.request_frame).tobytes()

    provider_started: list[str] = []
    worker = Path(__file__).with_name("_execution_cell_worker.py").resolve()
    arguments = [
        "-I",
        os.fspath(worker),
        binding.launch_key,
        str(transport_limits.request_payload_bytes),
        str(transport_limits.terminal_payload_bytes),
    ]
    try:
        observation = run_windows_execution_cell(
            context,
            eligibility,
            executable=Path(sys.executable).resolve(),
            arguments=arguments,
            request_frame=request_frame,
            terminal_payload_limit=transport_limits.terminal_payload_bytes,
            cancellation_requested=cancellation_requested,
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
    provider_run_started_at = provider_started[0]
    provider_run_finished_at = _utc_now()
    expected_provider_run_id = _expected_provider_run_id(request_document)

    status: tuple[ProviderRunStatus, PhaseStatus, str | None]
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
                payload_limit=transport_limits.terminal_payload_bytes,
            )
            terminal = validate_terminal_document(
                untrusted_terminal, request=request_document
            )
        except (FrameProtocolError, ApplicationProtocolError):
            eligibility.revoke()
            status = _internal_failure()
        else:
            status = _map_terminal_kind(terminal["terminal_kind"])
            if status[1] is not PhaseStatus.COMPLETED:
                eligibility.revoke()

    facts: tuple[bytes, ...] = ()
    fact_ids: tuple[str, ...] = ()
    if status[1] is PhaseStatus.COMPLETED and terminal is not None:
        commit_candidate = canonical_json_bytes(terminal)
        try:
            committed = (
                eligibility.permits_phase_commit()
                and context.try_complete_phase(
                    commit_candidate,
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
            facts = tuple(
                canonical_json_bytes(copy.deepcopy(fact))
                for fact in terminal["canonical_facts"]
            )
            fact_ids = tuple(terminal["reported_fact_ids"])

    if status[1] is not PhaseStatus.COMPLETED:
        facts = ()
        fact_ids = ()
    phase_finished_at = _utc_now()
    return OwnedExecutionCellPhaseResult(
        derivation_id=str(prepared.derivation_id),
        request_provenance_bytes=canonical_json_bytes(request_provenance),
        source_snapshot_digest=inputs.source_snapshot_digest,
        policy_digest=inputs.policy_digest,
        analysis_scope_digest=inputs.analysis_scope_digest,
        slice_policy_digest=inputs.slice_policy_digest,
        derivation_profile_digest=inputs.derivation_profile_digest,
        provider_descriptor=binding.descriptor,
        operands_digest=request_document["operands_digest"],
        provider_run_id=expected_provider_run_id,
        attempt_started_at=attempt_started_at,
        provider_run_started_at=provider_run_started_at,
        provider_run_finished_at=provider_run_finished_at,
        phase_finished_at=phase_finished_at,
        provider_run_status=status[0],
        phase_status=status[1],
        diagnostic_code=status[2],
        canonical_fact_bytes=facts,
        reported_fact_ids=fact_ids,
        reported_relation_ids=(),
        release_outcome=ReleaseOutcome.RELEASED,
    )


def _validate_attempt_request(
    inputs: object,
    *,
    derivation_id: object,
    binding: object,
    cancellation_requested: object,
    transport_limits: object,
) -> None:
    valid_text = (
        isinstance(derivation_id, str)
        and bool(derivation_id)
        and all(not 0xD800 <= ord(character) <= 0xDFFF for character in derivation_id)
    )
    valid_binding_shape = isinstance(binding, ProviderBinding) and isinstance(
        binding.descriptor, ProviderDescriptor
    )
    if valid_binding_shape:
        descriptor_values = binding.descriptor.document().values()
        valid_binding_shape = (
            binding.descriptor.capability_id == "python-ast"
            and isinstance(binding.launch_key, str)
            and bool(binding.launch_key)
            and all(
                isinstance(value, str)
                and bool(value)
                and all(not 0xD800 <= ord(ch) <= 0xDFFF for ch in value)
                for value in descriptor_values
            )
        )
    if (
        not isinstance(inputs, DerivationInputSet)
        or not valid_text
        or not valid_binding_shape
        or not isinstance(transport_limits, ExecutionCellTransportSafetyLimits)
        or (cancellation_requested is not None and not callable(cancellation_requested))
    ):
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )
    try:
        requirements = inputs.review_policy_document_copy()["provider_requirements"]
    except Exception as exc:
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        ) from exc
    if requirements != [
        {
            "capability_id": "python-ast",
            "required": True,
            "composition_mode": "CUMULATIVE",
        }
    ]:
        raise DerivationExecutionCellError(
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST
        )


def _admission_stop_error(
    trigger: BudgetStopTrigger | None,
) -> DerivationExecutionCellError:
    if trigger is BudgetStopTrigger.EXECUTION_CANCELLED:
        code = DerivationExecutionCellFailureCode.DERIVATION_ADMISSION_CANCELLED
    elif trigger is BudgetStopTrigger.EXECUTION_DEADLINE:
        code = DerivationExecutionCellFailureCode.DERIVATION_ADMISSION_DEADLINE
    else:
        code = DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR
    return DerivationExecutionCellError(code)


def _map_terminal_kind(
    value: object,
) -> tuple[ProviderRunStatus, PhaseStatus, str | None]:
    mapping = {
        "COMPLETED": (
            ProviderRunStatus.COMPLETED,
            PhaseStatus.COMPLETED,
            None,
        ),
        "PROVIDER_UNAVAILABLE": (
            ProviderRunStatus.UNAVAILABLE,
            PhaseStatus.UNAVAILABLE,
            "PROVIDER_UNAVAILABLE",
        ),
        "PROVIDER_FAILED": (
            ProviderRunStatus.FAILED,
            PhaseStatus.FAILED,
            "PROVIDER_FAILED",
        ),
        "NONCONFORMANT_PROVIDER_OUTPUT": (
            ProviderRunStatus.FAILED,
            PhaseStatus.FAILED,
            "NONCONFORMANT_PROVIDER_OUTPUT",
        ),
        "INTERNAL_DERIVATION_ERROR": _internal_failure(),
    }
    return mapping[value]


def _internal_failure() -> tuple[ProviderRunStatus, PhaseStatus, str]:
    return (
        ProviderRunStatus.FAILED,
        PhaseStatus.FAILED,
        "INTERNAL_DERIVATION_ERROR",
    )


def _expected_provider_run_id(request: dict[str, object]) -> str:
    from veritrail_review._execution_cell_application import provider_run_id

    descriptor = ProviderDescriptor(**request["provider_descriptor"])
    return provider_run_id(
        request["derivation_id"], descriptor, request["operands_digest"]
    )


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )
