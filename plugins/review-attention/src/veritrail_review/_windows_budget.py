from __future__ import annotations

import ctypes
import importlib.metadata
import os
import subprocess
import time
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

from veritrail_review.budget import (
    BudgetContext,
    BudgetState,
    BudgetStopTrigger,
    MemoryAttributionState,
)
from veritrail_review.errors import BudgetPrimitiveError, BudgetPrimitiveFailureCode


EXPECTED_PYWIN32_VERSION = "312"
_COMPLETION_KEY = 0x525631
_WAIT_SLICE_MS = 10
_ERROR_TIMEOUT = 258
_JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO = 4
_JOB_OBJECT_MSG_JOB_MEMORY_LIMIT = 10


class _JobCompletionPortAssociation(ctypes.Structure):
    _fields_ = [
        ("completion_key", wintypes.LPVOID),
        ("completion_port", wintypes.HANDLE),
    ]


@dataclass(frozen=True)
class WindowsExecutionObservation:
    process_created_suspended: bool
    job_configured_before_process: bool
    observation_channel_associated_before_process: bool
    process_assigned_before_resume: bool
    process_resumed: bool
    memory_limit_event_observed: bool
    memory_attribution: MemoryAttributionState
    stop_trigger: BudgetStopTrigger | None
    active_process_zero: bool
    handles_released: bool
    forced_termination_requested: bool
    elapsed_ms: float


class _WindowsBindings:
    def __init__(self) -> None:
        try:
            import win32api
            import win32event
            import win32file
            import win32job
            import win32process
        except ImportError as exc:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.PLATFORM_CAPABILITY_UNAVAILABLE
            ) from exc
        self.win32api = win32api
        self.win32event = win32event
        self.win32file = win32file
        self.win32job = win32job
        self.win32process = win32process

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.set_job_information = kernel32.SetInformationJobObject
        self.set_job_information.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            wintypes.LPVOID,
            wintypes.DWORD,
        ]
        self.set_job_information.restype = wintypes.BOOL
        self.get_completion = kernel32.GetQueuedCompletionStatus
        self.get_completion.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(ctypes.c_size_t),
            ctypes.POINTER(ctypes.c_void_p),
            wintypes.DWORD,
        ]
        self.get_completion.restype = wintypes.BOOL

    def close(self, handle: Any | None) -> None:
        if handle is None:
            return
        closer = getattr(handle, "Close", None)
        if closer is not None:
            closer()
        else:
            self.win32api.CloseHandle(handle)


def require_budget_primitive_capability() -> None:
    """Fail closed unless the frozen Windows native binding is available."""

    if os.name != "nt":
        raise BudgetPrimitiveError(
            BudgetPrimitiveFailureCode.PLATFORM_CAPABILITY_UNAVAILABLE
        )
    try:
        installed = importlib.metadata.version("pywin32")
    except importlib.metadata.PackageNotFoundError as exc:
        raise BudgetPrimitiveError(
            BudgetPrimitiveFailureCode.PLATFORM_CAPABILITY_UNAVAILABLE
        ) from exc
    if installed != EXPECTED_PYWIN32_VERSION:
        raise BudgetPrimitiveError(
            BudgetPrimitiveFailureCode.PLATFORM_CAPABILITY_UNAVAILABLE
        )
    _WindowsBindings()


def _run_owned_process_cell(
    context: BudgetContext,
    *,
    executable: Path,
    arguments: Sequence[str],
    cancellation_requested: Callable[[], bool] | None = None,
) -> WindowsExecutionObservation:
    """Run one internal process cell without interpreting its result transport."""

    if (
        not isinstance(context, BudgetContext)
        or context.state is not BudgetState.RUNNING
        or not isinstance(executable, Path)
        or not executable.is_absolute()
        or any(not isinstance(value, str) or "\x00" in value for value in arguments)
        or (cancellation_requested is not None and not callable(cancellation_requested))
    ):
        raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT)

    require_budget_primitive_capability()
    bindings = _WindowsBindings()
    started = time.monotonic()
    job: Any | None = None
    port: Any | None = None
    process: Any | None = None
    primary_thread: Any | None = None
    job_configured = False
    port_associated = False
    process_created = False
    assigned = False
    resumed = False
    memory_event_observed = False
    active_process_zero = False
    handles_released = False
    forced_termination = False

    def close_all() -> None:
        nonlocal job, port, process, primary_thread, handles_released
        failures = 0
        handles = (primary_thread, process, port, job)
        primary_thread = process = port = job = None
        for handle in handles:
            if handle is not None:
                try:
                    bindings.close(handle)
                except Exception:
                    failures += 1
        handles_released = failures == 0

    def query_active_processes() -> int:
        if job is None:
            return 0
        information = bindings.win32job.QueryInformationJobObject(
            job, bindings.win32job.JobObjectBasicAccountingInformation
        )
        return int(information["ActiveProcesses"])

    def observation() -> WindowsExecutionObservation:
        return WindowsExecutionObservation(
            process_created_suspended=process_created,
            job_configured_before_process=job_configured,
            observation_channel_associated_before_process=port_associated,
            process_assigned_before_resume=assigned,
            process_resumed=resumed,
            memory_limit_event_observed=memory_event_observed,
            memory_attribution=context.memory_attribution,
            stop_trigger=context.stop_trigger,
            active_process_zero=active_process_zero,
            handles_released=handles_released,
            forced_termination_requested=forced_termination,
            elapsed_ms=round((time.monotonic() - started) * 1000, 3),
        )

    def receive_packet(wait_ms: int) -> tuple[int, int] | None:
        assert port is not None
        transferred = wintypes.DWORD()
        key = ctypes.c_size_t()
        overlapped = ctypes.c_void_p()
        completed = bindings.get_completion(
            wintypes.HANDLE(int(port)),
            ctypes.byref(transferred),
            ctypes.byref(key),
            ctypes.byref(overlapped),
            wait_ms,
        )
        if completed:
            return int(transferred.value), int(key.value)
        error = ctypes.get_last_error()
        if error == _ERROR_TIMEOUT:
            return None
        raise ctypes.WinError(error)

    try:
        if not context.checkpoint():
            active_process_zero = True
            close_all()
            return observation()

        job = bindings.win32job.CreateJobObject(None, "")
        limits = bindings.win32job.QueryInformationJobObject(
            job, bindings.win32job.JobObjectExtendedLimitInformation
        )
        required_flags = (
            bindings.win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            | bindings.win32job.JOB_OBJECT_LIMIT_JOB_MEMORY
        )
        limits["BasicLimitInformation"]["LimitFlags"] = required_flags
        limits["JobMemoryLimit"] = context.limits.memory_bytes
        bindings.win32job.SetInformationJobObject(
            job, bindings.win32job.JobObjectExtendedLimitInformation, limits
        )
        readback = bindings.win32job.QueryInformationJobObject(
            job, bindings.win32job.JobObjectExtendedLimitInformation
        )
        if (
            readback["BasicLimitInformation"]["LimitFlags"] & required_flags
            != required_flags
            or int(readback["JobMemoryLimit"]) != context.limits.memory_bytes
        ):
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.PLATFORM_CONTAINMENT_FAILED
            )
        job_configured = True

        port = bindings.win32file.CreateIoCompletionPort(-1, 0, 0, 1)
        association = _JobCompletionPortAssociation(
            ctypes.c_void_p(_COMPLETION_KEY), ctypes.c_void_p(int(port))
        )
        if not bindings.set_job_information(
            wintypes.HANDLE(int(job)),
            bindings.win32job.JobObjectAssociateCompletionPortInformation,
            ctypes.byref(association),
            ctypes.sizeof(association),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        port_associated = True

        if not context.checkpoint():
            active_process_zero = query_active_processes() == 0
            close_all()
            return observation()

        command_line = subprocess.list2cmdline([os.fspath(executable), *arguments])
        startup = bindings.win32process.STARTUPINFO()
        process, primary_thread, _, _ = bindings.win32process.CreateProcess(
            os.fspath(executable),
            command_line,
            None,
            None,
            False,
            bindings.win32process.CREATE_SUSPENDED
            | bindings.win32process.CREATE_NO_WINDOW
            | bindings.win32process.CREATE_UNICODE_ENVIRONMENT,
            None,
            None,
            startup,
        )
        process_created = True
        bindings.win32job.AssignProcessToJobObject(job, process)
        assigned = True
        if context.checkpoint():
            bindings.win32process.ResumeThread(primary_thread)
            resumed = True
        bindings.close(primary_thread)
        primary_thread = None

        while True:
            packet = receive_packet(_WAIT_SLICE_MS)
            memory_observed_this_checkpoint = False
            if packet is not None:
                message, completion_key = packet
                if completion_key == _COMPLETION_KEY:
                    if message == _JOB_OBJECT_MSG_JOB_MEMORY_LIMIT:
                        memory_event_observed = True
                        memory_observed_this_checkpoint = True
                    elif message == _JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO:
                        active_process_zero = True

            now = time.monotonic()
            cancellation_observed = bool(
                cancellation_requested is not None and cancellation_requested()
            )
            context._checkpoint_observations(
                now=now,
                cancellation_observed=cancellation_observed,
                memory_limit_event_observed=memory_observed_this_checkpoint,
            )
            if context.state is BudgetState.STOPPING and not forced_termination:
                bindings.win32job.TerminateJobObject(job, 73)
                forced_termination = True

            root_signaled = (
                bindings.win32event.WaitForSingleObject(process, 0)
                == bindings.win32event.WAIT_OBJECT_0
            )
            if root_signaled:
                memory_observed_during_drain = False
                while True:
                    packet = receive_packet(0)
                    if packet is None:
                        break
                    message, completion_key = packet
                    if completion_key != _COMPLETION_KEY:
                        continue
                    if message == _JOB_OBJECT_MSG_JOB_MEMORY_LIMIT:
                        memory_event_observed = True
                        memory_observed_during_drain = True
                    elif message == _JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO:
                        active_process_zero = True
                context._checkpoint_observations(
                    now=time.monotonic(),
                    cancellation_observed=bool(
                        cancellation_requested is not None
                        and cancellation_requested()
                    ),
                    memory_limit_event_observed=memory_observed_during_drain,
                )
                active_process_zero = active_process_zero or query_active_processes() == 0

            if context.state is BudgetState.RUNNING and root_signaled and active_process_zero:
                close_all()
                if not handles_released:
                    raise BudgetPrimitiveError(
                        BudgetPrimitiveFailureCode.PLATFORM_CONTAINMENT_FAILED
                    )
                return observation()

            if context.state is BudgetState.STOPPING:
                if active_process_zero or query_active_processes() == 0:
                    active_process_zero = True
                    close_all()
                    return observation()
                if context.remaining_release_seconds() <= 0:
                    close_all()
                    context._mark_release(residue_free=False)
                    raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.RELEASE_FAILED)
    except BudgetPrimitiveError:
        raise
    except Exception as exc:
        raise BudgetPrimitiveError(
            BudgetPrimitiveFailureCode.PLATFORM_CONTAINMENT_FAILED
        ) from exc
    finally:
        if job is not None:
            try:
                bindings.win32job.TerminateJobObject(job, 74)
            except Exception:
                pass
        if any(value is not None for value in (job, port, process, primary_thread)):
            close_all()
