from __future__ import annotations

import math
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from veritrail_review.derivation_input_contracts import DerivationInputSet
from veritrail_review.errors import BudgetPrimitiveError, BudgetPrimitiveFailureCode


RELEASE_ENVELOPE_MS = 5_000
_ADMISSION_TOKEN = object()


class BudgetState(str, Enum):
    ADMITTED = "ADMITTED"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    RELEASED = "RELEASED"
    RELEASE_FAILED = "RELEASE_FAILED"


class BudgetStopTrigger(str, Enum):
    EXECUTION_DEADLINE = "EXECUTION_DEADLINE"
    EXECUTION_CANCELLED = "EXECUTION_CANCELLED"
    EXECUTION_MEMORY_BUDGET = "EXECUTION_MEMORY_BUDGET"
    EXECUTION_ARTIFACT_BUDGET = "EXECUTION_ARTIFACT_BUDGET"


class MemoryAttributionState(str, Enum):
    NOT_OBSERVED = "MEMORY_ATTRIBUTION_NOT_OBSERVED"
    POSITIVELY_OBSERVED = "MEMORY_ATTRIBUTION_POSITIVELY_OBSERVED"


@dataclass(frozen=True)
class ExecutionBudgetLimits:
    wall_clock_ms: int
    memory_bytes: int
    artifact_bytes: int


@dataclass(frozen=True)
class OwnedPhaseResult:
    canonical_bytes: bytes
    completed_at_monotonic: float
    phase_status: str = "COMPLETED_FOR_PHASE"


class BudgetContext:
    """One copy-owned execution budget and its atomic stop/commit boundary."""

    def __init__(
        self,
        limits: ExecutionBudgetLimits,
        *,
        _admission_token: object,
        _clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if _admission_token is not _ADMISSION_TOKEN:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            )
        _validate_limits(limits)
        self._clock = _clock
        self._lock = threading.Lock()
        self._limits = ExecutionBudgetLimits(
            wall_clock_ms=limits.wall_clock_ms,
            memory_bytes=limits.memory_bytes,
            artifact_bytes=limits.artifact_bytes,
        )
        self._state = BudgetState.ADMITTED
        try:
            self._started_at = float(self._clock())
            self._execution_deadline = (
                self._started_at + self._limits.wall_clock_ms / 1000.0
            )
        except (OverflowError, TypeError, ValueError) as exc:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            ) from exc
        if not math.isfinite(self._started_at) or not math.isfinite(
            self._execution_deadline
        ):
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            )
        self._stop_trigger: BudgetStopTrigger | None = None
        self._stop_latched_at: float | None = None
        self._release_deadline: float | None = None
        self._reserved_artifact_bytes = 0
        self._memory_attribution = MemoryAttributionState.NOT_OBSERVED
        self._state = BudgetState.RUNNING

    @classmethod
    def _admit_for_testing(
        cls,
        limits: ExecutionBudgetLimits,
        *,
        clock: Callable[[], float] = time.monotonic,
    ) -> "BudgetContext":
        return cls(limits, _admission_token=_ADMISSION_TOKEN, _clock=clock)

    @property
    def limits(self) -> ExecutionBudgetLimits:
        return self._limits

    @property
    def state(self) -> BudgetState:
        with self._lock:
            return self._state

    @property
    def started_at_monotonic(self) -> float:
        return self._started_at

    @property
    def execution_deadline_monotonic(self) -> float:
        return self._execution_deadline

    @property
    def stop_trigger(self) -> BudgetStopTrigger | None:
        with self._lock:
            return self._stop_trigger

    @property
    def stop_latched_at_monotonic(self) -> float | None:
        with self._lock:
            return self._stop_latched_at

    @property
    def release_deadline_monotonic(self) -> float | None:
        with self._lock:
            return self._release_deadline

    @property
    def reserved_artifact_bytes(self) -> int:
        with self._lock:
            return self._reserved_artifact_bytes

    @property
    def memory_attribution(self) -> MemoryAttributionState:
        with self._lock:
            return self._memory_attribution

    def checkpoint(self) -> bool:
        """Return execution eligibility after applying the absolute deadline."""

        with self._lock:
            self._checkpoint_locked(now=float(self._clock()))
            return self._state is BudgetState.RUNNING

    def request_cancellation(self) -> bool:
        """Submit caller cancellation to the one terminal-stop latch."""

        with self._lock:
            before = self._stop_trigger
            self._checkpoint_locked(
                now=float(self._clock()), cancellation_observed=True
            )
            return (
                before is None
                and self._stop_trigger is BudgetStopTrigger.EXECUTION_CANCELLED
            )

    def reserve_artifact_bytes(self, exact_bytes: bytes) -> bool:
        """Atomically reserve application-owned bytes before a create-new write."""

        try:
            byte_count = len(memoryview(exact_bytes))
        except TypeError as exc:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            ) from exc
        with self._lock:
            now = float(self._clock())
            self._checkpoint_locked(now=now)
            if self._state is not BudgetState.RUNNING:
                return False
            projected = self._reserved_artifact_bytes + byte_count
            if projected > self._limits.artifact_bytes:
                self._checkpoint_locked(now=now, artifact_over_budget=True)
                return False
            self._reserved_artifact_bytes = projected
            return True

    def try_complete_phase(
        self,
        canonical_bytes: bytes,
        *,
        resources_closed: bool,
        completed_at_monotonic: float | None = None,
    ) -> OwnedPhaseResult | None:
        """Commit one phase result through the same lock used by terminal stops."""

        if type(resources_closed) is not bool:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            )
        try:
            owned_bytes = memoryview(canonical_bytes).tobytes()
        except TypeError as exc:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            ) from exc
        with self._lock:
            now = float(self._clock())
            completed_at = now if completed_at_monotonic is None else float(
                completed_at_monotonic
            )
            if (
                not math.isfinite(completed_at)
                or completed_at < self._started_at
            ):
                raise BudgetPrimitiveError(
                    BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
                )
            self._checkpoint_locked(now=now)
            if (
                self._state is not BudgetState.RUNNING
                or not resources_closed
                or completed_at > self._execution_deadline
                or now >= self._execution_deadline
            ):
                return None
            return OwnedPhaseResult(
                canonical_bytes=owned_bytes,
                completed_at_monotonic=completed_at,
            )

    def remaining_release_seconds(self) -> float:
        with self._lock:
            if self._state is not BudgetState.STOPPING:
                return 0.0
            assert self._release_deadline is not None
            return max(0.0, self._release_deadline - float(self._clock()))

    def _observe_owned_memory_limit(self) -> bool:
        """Internal backend entry: ownership must be proven before this call."""

        with self._lock:
            self._memory_attribution = MemoryAttributionState.POSITIVELY_OBSERVED
            before = self._stop_trigger
            self._checkpoint_locked(
                now=float(self._clock()), memory_limit_event_observed=True
            )
            return (
                before is None
                and self._stop_trigger is BudgetStopTrigger.EXECUTION_MEMORY_BUDGET
            )

    def _checkpoint_observations(
        self,
        *,
        now: float,
        cancellation_observed: bool = False,
        memory_limit_event_observed: bool = False,
        artifact_over_budget: bool = False,
    ) -> BudgetStopTrigger | None:
        """Internal deterministic checkpoint used by the conformance harness."""

        if not math.isfinite(now):
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            )
        with self._lock:
            if memory_limit_event_observed:
                self._memory_attribution = MemoryAttributionState.POSITIVELY_OBSERVED
            self._checkpoint_locked(
                now=now,
                cancellation_observed=cancellation_observed,
                memory_limit_event_observed=memory_limit_event_observed,
                artifact_over_budget=artifact_over_budget,
            )
            return self._stop_trigger

    def _mark_release(self, *, residue_free: bool) -> BudgetState:
        with self._lock:
            if self._state is not BudgetState.STOPPING:
                raise BudgetPrimitiveError(
                    BudgetPrimitiveFailureCode.BUDGET_CONTEXT_NOT_RUNNING
                )
            within_envelope = (
                self._release_deadline is not None
                and float(self._clock()) <= self._release_deadline
            )
            self._state = (
                BudgetState.RELEASED
                if residue_free and within_envelope
                else BudgetState.RELEASE_FAILED
            )
            return self._state

    def _checkpoint_locked(
        self,
        *,
        now: float,
        cancellation_observed: bool = False,
        memory_limit_event_observed: bool = False,
        artifact_over_budget: bool = False,
    ) -> None:
        if self._state is not BudgetState.RUNNING:
            return
        selected: BudgetStopTrigger | None = None
        if now >= self._execution_deadline:
            selected = BudgetStopTrigger.EXECUTION_DEADLINE
        elif cancellation_observed:
            selected = BudgetStopTrigger.EXECUTION_CANCELLED
        elif memory_limit_event_observed:
            selected = BudgetStopTrigger.EXECUTION_MEMORY_BUDGET
        elif artifact_over_budget:
            selected = BudgetStopTrigger.EXECUTION_ARTIFACT_BUDGET
        if selected is None:
            return
        self._stop_trigger = selected
        self._stop_latched_at = now
        self._release_deadline = now + RELEASE_ENVELOPE_MS / 1000.0
        self._state = BudgetState.STOPPING


def admit_derivation_budget(inputs: DerivationInputSet) -> BudgetContext:
    """Copy the sealed ReviewPolicy budget into one owned runtime context."""

    if not isinstance(inputs, DerivationInputSet):
        raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT)
    try:
        value = inputs.review_policy_document_copy()["execution_budget"]
        if not isinstance(value, dict) or set(value) != {
            "wall_clock_ms",
            "memory_bytes",
            "artifact_bytes",
        }:
            raise ValueError
        limits = ExecutionBudgetLimits(
            wall_clock_ms=value["wall_clock_ms"],
            memory_bytes=value["memory_bytes"],
            artifact_bytes=value["artifact_bytes"],
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise BudgetPrimitiveError(
            BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
        ) from exc
    return BudgetContext(limits, _admission_token=_ADMISSION_TOKEN)


def _validate_limits(limits: ExecutionBudgetLimits) -> None:
    if not isinstance(limits, ExecutionBudgetLimits) or any(
        type(value) is not int or value <= 0
        for value in (
            limits.wall_clock_ms,
            limits.memory_bytes,
            limits.artifact_bytes,
        )
    ):
        raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT)
