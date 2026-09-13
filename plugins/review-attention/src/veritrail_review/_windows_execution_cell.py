from __future__ import annotations

import ctypes
import os
import subprocess
import threading
import time
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

from veritrail_review._execution_cell_protocol import AttemptEligibility
from veritrail_review._windows_budget import (
    _COMPLETION_KEY,
    _ERROR_TIMEOUT,
    _JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO,
    _JOB_OBJECT_MSG_JOB_MEMORY_LIMIT,
    _WAIT_SLICE_MS,
    _JobCompletionPortAssociation,
    _WindowsBindings,
    require_budget_primitive_capability,
)
from veritrail_review.budget import BudgetContext, BudgetState, BudgetStopTrigger
from veritrail_review.errors import BudgetPrimitiveError


_ERROR_BROKEN_PIPE = 109
_ERROR_NO_DATA = 232


class CellPreparationError(RuntimeError):
    pass


class CellRuntimeUnavailableError(RuntimeError):
    pass


class CellReleaseError(RuntimeError):
    pass


@dataclass(frozen=True)
class WindowsExecutionCellObservation:
    admitted: bool
    process_created_suspended: bool
    process_assigned_before_resume: bool
    process_resumed: bool
    active_process_zero: bool
    handles_released: bool
    channel_threads_released: bool
    memory_limit_event_observed: bool
    stop_trigger: BudgetStopTrigger | None
    terminal_bytes: bytes
    request_channel_failed: bool
    result_channel_failed: bool
    result_transport_exceeded: bool
    root_exit_code: int | None


def run_windows_execution_cell(
    context: BudgetContext,
    eligibility: AttemptEligibility,
    *,
    executable: Path,
    arguments: Sequence[str],
    request_frame: bytes,
    terminal_payload_limit: int,
    cancellation_requested: Callable[[], bool] | None,
    on_admitted: Callable[[], None],
) -> WindowsExecutionCellObservation:
    if (
        not isinstance(context, BudgetContext)
        or context.state is not BudgetState.RUNNING
        or not isinstance(eligibility, AttemptEligibility)
        or not isinstance(executable, Path)
        or not executable.is_absolute()
        or not isinstance(request_frame, bytes)
        or type(terminal_payload_limit) is not int
        or terminal_payload_limit <= 0
        or any(not isinstance(value, str) or "\x00" in value for value in arguments)
        or (cancellation_requested is not None and not callable(cancellation_requested))
        or not callable(on_admitted)
    ):
        raise CellPreparationError

    try:
        require_budget_primitive_capability()
        bindings = _WindowsBindings()
        import pywintypes
        import win32con
        import win32file
        import win32pipe
        import win32process
    except (BudgetPrimitiveError, ImportError) as exc:
        raise CellRuntimeUnavailableError from exc

    job: Any | None = None
    port: Any | None = None
    process: Any | None = None
    primary_thread: Any | None = None
    request_read: Any | None = None
    request_write: Any | None = None
    result_read: Any | None = None
    result_write: Any | None = None
    stderr_sink: Any | None = None
    process_created = False
    assigned = False
    resumed = False
    active_process_zero = False
    handles_released = False
    admitted = False
    memory_event = False
    forced_termination = False
    request_failed = False
    result_failed = False
    result_exceeded = False
    result_chunks = bytearray()
    root_exit_code: int | None = None
    writer: threading.Thread | None = None
    reader: threading.Thread | None = None

    def close_handle(name: str) -> bool:
        nonlocal job, port, process, primary_thread
        nonlocal request_read, request_write, result_read, result_write, stderr_sink
        value = locals_for_handles()[name]
        if value is None:
            return True
        try:
            bindings.close(value)
        except Exception:
            return False
        if name == "job":
            job = None
        elif name == "port":
            port = None
        elif name == "process":
            process = None
        elif name == "primary_thread":
            primary_thread = None
        elif name == "request_read":
            request_read = None
        elif name == "request_write":
            request_write = None
        elif name == "result_read":
            result_read = None
        elif name == "result_write":
            result_write = None
        elif name == "stderr_sink":
            stderr_sink = None
        return True

    def locals_for_handles() -> dict[str, Any | None]:
        return {
            "job": job,
            "port": port,
            "process": process,
            "primary_thread": primary_thread,
            "request_read": request_read,
            "request_write": request_write,
            "result_read": result_read,
            "result_write": result_write,
            "stderr_sink": stderr_sink,
        }

    def close_all_handles() -> bool:
        failures = 0
        for name in (
            "primary_thread",
            "request_read",
            "request_write",
            "result_read",
            "result_write",
            "stderr_sink",
            "process",
            "port",
            "job",
        ):
            if not close_handle(name):
                failures += 1
        return failures == 0

    def terminate_and_release() -> bool:
        """Cleanup-only path; never restores attempt eligibility."""

        nonlocal active_process_zero, forced_termination
        if job is not None:
            try:
                bindings.win32job.TerminateJobObject(job, 74)
                forced_termination = True
            except Exception:
                pass
        if process is not None and not assigned:
            try:
                bindings.win32process.TerminateProcess(process, 74)
            except Exception:
                pass
        release_deadline = context.release_deadline_monotonic
        if release_deadline is None:
            release_deadline = time.monotonic() + 5.0
        while job is not None and time.monotonic() <= release_deadline:
            try:
                job_empty = query_active_processes() == 0
                root_stopped = (
                    process is None
                    or bindings.win32event.WaitForSingleObject(process, 0)
                    == bindings.win32event.WAIT_OBJECT_0
                )
                if job_empty and root_stopped:
                    active_process_zero = True
                    break
            except Exception:
                break
            time.sleep(0.01)
        close_handle("request_write")
        close_handle("result_read")
        if writer is not None:
            writer.join(max(0.0, release_deadline - time.monotonic()))
        if reader is not None:
            reader.join(max(0.0, release_deadline - time.monotonic()))
        channels_released = (
            active_process_zero
            and (writer is None or not writer.is_alive())
            and (reader is None or not reader.is_alive())
        )
        handles_closed = close_all_handles()
        released = channels_released and handles_closed
        if context.state is BudgetState.STOPPING:
            released = (
                context._mark_release(residue_free=released) is BudgetState.RELEASED
            )
        return released

    def query_active_processes() -> int:
        if job is None:
            return 0
        information = bindings.win32job.QueryInformationJobObject(
            job, bindings.win32job.JobObjectBasicAccountingInformation
        )
        return int(information["ActiveProcesses"])

    def receive_packet(wait_ms: int) -> tuple[int, int] | None:
        if port is None:
            return None
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

    def checkpoint_preparation() -> bool:
        return context._checkpoint_observations(
            now=time.monotonic(),
            cancellation_observed=bool(
                cancellation_requested is not None and cancellation_requested()
            ),
        ) is None

    def write_request() -> None:
        nonlocal request_failed, request_write
        try:
            offset = 0
            while offset < len(request_frame):
                _, written = win32file.WriteFile(
                    request_write, request_frame[offset : offset + 65_536]
                )
                if type(written) is not int or written <= 0:
                    raise OSError
                offset += written
        except Exception:
            request_failed = True
        finally:
            close_handle("request_write")

    def read_result() -> None:
        nonlocal result_failed, result_exceeded, result_read
        maximum = 8 + terminal_payload_limit + 1
        try:
            while True:
                try:
                    _, chunk = win32file.ReadFile(result_read, 65_536)
                except pywintypes.error as exc:
                    if exc.winerror in {_ERROR_BROKEN_PIPE, _ERROR_NO_DATA}:
                        break
                    raise
                if not chunk:
                    break
                remaining = maximum - len(result_chunks)
                if remaining <= 0:
                    result_exceeded = True
                    break
                result_chunks.extend(chunk[:remaining])
                if len(chunk) > remaining or len(result_chunks) >= maximum:
                    result_exceeded = True
                    break
        except Exception:
            result_failed = True
        finally:
            close_handle("result_read")

    try:
        if not checkpoint_preparation():
            raise CellPreparationError
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
            raise CellPreparationError
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
            raise CellPreparationError
        if not checkpoint_preparation():
            raise CellPreparationError

        inheritable = pywintypes.SECURITY_ATTRIBUTES()
        inheritable.bInheritHandle = True
        request_read, request_write = win32pipe.CreatePipe(inheritable, 0)
        result_read, result_write = win32pipe.CreatePipe(inheritable, 0)
        bindings.win32api.SetHandleInformation(
            request_write, win32con.HANDLE_FLAG_INHERIT, 0
        )
        bindings.win32api.SetHandleInformation(
            result_read, win32con.HANDLE_FLAG_INHERIT, 0
        )
        stderr_sink = win32file.CreateFile(
            "NUL",
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            inheritable,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None,
        )
        if not checkpoint_preparation():
            raise CellPreparationError

        startup = win32process.STARTUPINFO()
        startup.dwFlags |= win32process.STARTF_USESTDHANDLES
        startup.hStdInput = request_read
        startup.hStdOutput = result_write
        startup.hStdError = stderr_sink
        command_line = subprocess.list2cmdline([os.fspath(executable), *arguments])
        process, primary_thread, _, _ = win32process.CreateProcess(
            os.fspath(executable),
            command_line,
            None,
            None,
            True,
            win32process.CREATE_SUSPENDED
            | win32process.CREATE_NO_WINDOW
            | win32process.CREATE_UNICODE_ENVIRONMENT,
            None,
            None,
            startup,
        )
        process_created = True
        bindings.win32job.AssignProcessToJobObject(job, process)
        assigned = True
        close_handle("request_read")
        close_handle("result_write")
        close_handle("stderr_sink")

        if not checkpoint_preparation() or not assigned:
            raise CellPreparationError
        if not eligibility.admit():
            raise CellPreparationError
        admitted = True
        on_admitted()
        win32process.ResumeThread(primary_thread)
        resumed = True
        close_handle("primary_thread")

        writer = threading.Thread(target=write_request, name="r1-cell-request")
        reader = threading.Thread(target=read_result, name="r1-cell-result")
        writer.start()
        reader.start()

        while True:
            packet = receive_packet(_WAIT_SLICE_MS)
            memory_this_checkpoint = False
            if packet is not None:
                message, completion_key = packet
                if completion_key == _COMPLETION_KEY:
                    if message == _JOB_OBJECT_MSG_JOB_MEMORY_LIMIT:
                        memory_event = True
                        memory_this_checkpoint = True
                    elif message == _JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO:
                        active_process_zero = True
            context._checkpoint_observations(
                now=time.monotonic(),
                cancellation_observed=bool(
                    cancellation_requested is not None and cancellation_requested()
                ),
                memory_limit_event_observed=memory_this_checkpoint,
            )
            if context.state is BudgetState.STOPPING and not forced_termination:
                bindings.win32job.TerminateJobObject(job, 73)
                forced_termination = True

            root_signaled = (
                bindings.win32event.WaitForSingleObject(process, 0)
                == bindings.win32event.WAIT_OBJECT_0
            )
            if root_signaled and root_exit_code is None:
                root_exit_code = int(bindings.win32process.GetExitCodeProcess(process))
            if root_signaled:
                active_process_zero = active_process_zero or query_active_processes() == 0

            if active_process_zero:
                writer.join(0.25)
                reader.join(0.25)
                if not writer.is_alive() and not reader.is_alive():
                    break
            if context.state is BudgetState.STOPPING and context.remaining_release_seconds() <= 0:
                eligibility.revoke()
                close_all_handles()
                context._mark_release(residue_free=False)
                raise CellReleaseError

        handles_released = close_all_handles()
        channel_threads_released = not writer.is_alive() and not reader.is_alive()
        if not handles_released or not channel_threads_released:
            eligibility.revoke()
            if context.state is BudgetState.STOPPING:
                context._mark_release(residue_free=False)
            raise CellReleaseError
        if context.state is BudgetState.STOPPING:
            eligibility.revoke()
            if context._mark_release(residue_free=True) is not BudgetState.RELEASED:
                raise CellReleaseError
        return WindowsExecutionCellObservation(
            admitted=admitted,
            process_created_suspended=process_created,
            process_assigned_before_resume=assigned,
            process_resumed=resumed,
            active_process_zero=active_process_zero,
            handles_released=handles_released,
            channel_threads_released=channel_threads_released,
            memory_limit_event_observed=memory_event,
            stop_trigger=context.stop_trigger,
            terminal_bytes=bytes(result_chunks),
            request_channel_failed=request_failed,
            result_channel_failed=result_failed,
            result_transport_exceeded=result_exceeded,
            root_exit_code=root_exit_code,
        )
    except CellReleaseError:
        raise
    except Exception as exc:
        eligibility.revoke()
        released = terminate_and_release()
        if not released and process_created:
            raise CellReleaseError from exc
        if admitted:
            return WindowsExecutionCellObservation(
                admitted=True,
                process_created_suspended=process_created,
                process_assigned_before_resume=assigned,
                process_resumed=resumed,
                active_process_zero=active_process_zero,
                handles_released=released,
                channel_threads_released=bool(
                    (writer is None or not writer.is_alive())
                    and (reader is None or not reader.is_alive())
                ),
                memory_limit_event_observed=memory_event,
                stop_trigger=context.stop_trigger,
                terminal_bytes=bytes(result_chunks),
                request_channel_failed=True,
                result_channel_failed=True,
                result_transport_exceeded=result_exceeded,
                root_exit_code=root_exit_code,
            )
        raise CellPreparationError from exc
    finally:
        if any(value is not None for value in locals_for_handles().values()):
            if job is not None:
                try:
                    bindings.win32job.TerminateJobObject(job, 75)
                except Exception:
                    pass
            close_all_handles()
