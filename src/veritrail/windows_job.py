from __future__ import annotations

import importlib.metadata
import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from veritrail.errors import SafetyError, ValidationError

EXPECTED_PYWIN32_VERSION = "312"
PIPE_CHUNK_BYTES = 65_536
WAIT_SLICE_MS = 20
FORCED_CLEANUP_TIMEOUT_MS = 5_000
BROKEN_PIPE_ERRORS = {109, 232}


@dataclass(frozen=True)
class CapturedStream:
    content: bytes
    observed_bytes_lower_bound: int
    stream_complete: bool
    overflowed: bool
    thread_stopped: bool
    error_type: str | None


@dataclass(frozen=True)
class OwnedProcessResult:
    parent_in_job: bool
    process_created: bool
    target_assigned: bool
    target_resumed: bool
    exit_code: int | None
    termination_reason: str
    error_type: str | None
    stdout: CapturedStream
    stderr: CapturedStream
    active_process_limit: int
    active_process_limit_enforced: bool
    process_limit_attempt_observation: str
    total_assigned_processes: int
    final_active_processes: int
    job_limit_terminated_processes: int
    forced_termination_requested: bool
    forced_termination_processes_observed: int
    tree_released: bool
    handles_released: bool
    capture_threads_stopped: bool
    cleanup_complete: bool
    elapsed_ms: float


class _CaptureState:
    def __init__(self, limit: int, overflow_event: threading.Event) -> None:
        self.limit = limit
        self.overflow_event = overflow_event
        self.content = bytearray()
        self.observed = 0
        self.complete = False
        self.overflowed = False
        self.error_type: str | None = None

    def add(self, content: bytes) -> None:
        self.observed += len(content)
        remaining = max(0, self.limit - len(self.content))
        if remaining:
            self.content.extend(content[:remaining])
        if self.observed > self.limit:
            self.overflowed = True
            self.overflow_event.set()

    def result(self, *, thread_stopped: bool) -> CapturedStream:
        return CapturedStream(
            content=bytes(self.content),
            observed_bytes_lower_bound=self.observed,
            stream_complete=self.complete,
            overflowed=self.overflowed,
            thread_stopped=thread_stopped,
            error_type=self.error_type,
        )


class _WindowsBackend:
    def __init__(self) -> None:
        try:
            import pywintypes
            import win32api
            import win32con
            import win32event
            import win32file
            import win32job
            import win32pipe
            import win32process
        except ImportError as exc:
            raise SafetyError(
                "M9 command capability is unavailable; install the locked command-windows extra "
                "in the project virtual environment"
            ) from exc
        self.pywintypes = pywintypes
        self.win32api = win32api
        self.win32con = win32con
        self.win32event = win32event
        self.win32file = win32file
        self.win32job = win32job
        self.win32pipe = win32pipe
        self.win32process = win32process

    def close_handle(self, handle: Any) -> None:
        handle.Close()

    def assign_process_to_job(self, job: Any, process: Any) -> None:
        self.win32job.AssignProcessToJobObject(job, process)

    def resume_thread(self, thread: Any) -> int:
        return int(self.win32process.ResumeThread(thread))


def require_windows_command_capability() -> None:
    if os.name != "nt":
        raise SafetyError("M9 command capability is available only on the frozen Windows platform")
    try:
        installed = importlib.metadata.version("pywin32")
    except importlib.metadata.PackageNotFoundError as exc:
        raise SafetyError(
            "M9 command capability is unavailable; install the locked command-windows extra "
            "in the project virtual environment"
        ) from exc
    if installed != EXPECTED_PYWIN32_VERSION:
        raise SafetyError(
            f"M9 command capability requires locked pywin32 {EXPECTED_PYWIN32_VERSION}"
        )
    _WindowsBackend()


def _quote_windows_argument(argument: str) -> str:
    if not argument:
        return '""'
    if not any(character in " \t\n\v\"" for character in argument):
        return argument
    quoted = ['"']
    backslashes = 0
    for character in argument:
        if character == "\\":
            backslashes += 1
            continue
        if character == '"':
            quoted.append("\\" * (backslashes * 2 + 1))
            quoted.append('"')
            backslashes = 0
            continue
        if backslashes:
            quoted.append("\\" * backslashes)
            backslashes = 0
        quoted.append(character)
    if backslashes:
        quoted.append("\\" * (backslashes * 2))
    quoted.append('"')
    return "".join(quoted)


def _build_command_line(executable: Path, arguments: Sequence[str]) -> str:
    values = [str(executable), *arguments]
    command_line = " ".join(_quote_windows_argument(value) for value in values)
    if len(command_line) + 1 > 32_767:
        raise ValidationError(["resolved command line exceeds the Windows length limit"])
    return command_line


def _validate_runtime_inputs(
    executable: Path,
    arguments: Sequence[str],
    working_directory: Path,
    environment: Mapping[str, str],
    *,
    timeout_ms: int,
    descendant_exit_grace_ms: int,
    max_stdout_bytes: int,
    max_stderr_bytes: int,
    max_processes: int,
) -> None:
    errors: list[str] = []
    if not executable.is_absolute() or executable.suffix.casefold() != ".exe":
        errors.append("owned process executable must be an absolute .exe path")
    if not working_directory.is_absolute() or not working_directory.is_dir():
        errors.append("owned process working directory must be an existing absolute directory")
    if not arguments or any(
        not isinstance(argument, str)
        or "\x00" in argument
        or any(ord(character) < 32 for character in argument)
        for argument in arguments
    ):
        errors.append("owned process argument list must contain only control-free strings")
    normalized_environment_names: set[str] = set()
    if not environment or any(
        not isinstance(name, str)
        or not name
        or "=" in name
        or any(ord(character) < 32 for character in name)
        or not isinstance(value, str)
        or any(ord(character) < 32 for character in value)
        for name, value in environment.items()
    ):
        errors.append("owned process environment must contain valid string pairs")
    else:
        for name in environment:
            normalized = name.upper()
            if normalized in normalized_environment_names:
                errors.append(
                    "owned process environment must not contain case-insensitive duplicate names"
                )
                break
            normalized_environment_names.add(normalized)
    ranges = (
        ("timeout_ms", timeout_ms, 1_000, 900_000),
        ("descendant_exit_grace_ms", descendant_exit_grace_ms, 100, 10_000),
        ("max_stdout_bytes", max_stdout_bytes, 1, 1_048_576),
        ("max_stderr_bytes", max_stderr_bytes, 1, 1_048_576),
        ("max_processes", max_processes, 1, 32),
    )
    for name, value, minimum, maximum in ranges:
        if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
            errors.append(f"owned process {name} must be from {minimum} to {maximum}")
    if errors:
        raise ValidationError(errors)


def _create_job(backend: _WindowsBackend, max_processes: int) -> tuple[Any, bool, bool]:
    job = backend.win32job.CreateJobObject(None, "")
    try:
        current_process = backend.win32api.GetCurrentProcess()
        parent_in_job = bool(backend.win32job.IsProcessInJob(current_process, None))
        if backend.win32job.IsProcessInJob(current_process, job):
            raise SafetyError("M9 ownership backend refused a Job that already contains the runner")
        information = backend.win32job.QueryInformationJobObject(
            job, backend.win32job.JobObjectExtendedLimitInformation
        )
        required_flags = (
            backend.win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            | backend.win32job.JOB_OBJECT_LIMIT_ACTIVE_PROCESS
        )
        information["BasicLimitInformation"]["LimitFlags"] = required_flags
        information["BasicLimitInformation"]["ActiveProcessLimit"] = max_processes
        backend.win32job.SetInformationJobObject(
            job,
            backend.win32job.JobObjectExtendedLimitInformation,
            information,
        )
        readback = backend.win32job.QueryInformationJobObject(
            job, backend.win32job.JobObjectExtendedLimitInformation
        )["BasicLimitInformation"]
        enforced = (
            readback["LimitFlags"] & required_flags == required_flags
            and readback["ActiveProcessLimit"] == max_processes
        )
        if not enforced:
            raise SafetyError("M9 ownership backend could not verify the sealed Job limits")
        return job, parent_in_job, enforced
    except Exception:
        backend.close_handle(job)
        raise


def _create_inheritable_pipe(backend: _WindowsBackend) -> tuple[Any, Any]:
    security = backend.pywintypes.SECURITY_ATTRIBUTES()
    security.bInheritHandle = True
    return backend.win32pipe.CreatePipe(security, 0)


def _read_pipe(
    backend: _WindowsBackend,
    handle: Any,
    state: _CaptureState,
) -> None:
    try:
        while not state.overflowed:
            try:
                _, content = backend.win32file.ReadFile(handle, PIPE_CHUNK_BYTES, None)
            except backend.pywintypes.error as exc:
                if getattr(exc, "winerror", None) in BROKEN_PIPE_ERRORS:
                    state.complete = True
                else:
                    state.error_type = "PIPE_READ_FAILED"
                break
            if not content:
                state.complete = True
                break
            state.add(bytes(content))
    except Exception:
        state.error_type = "PIPE_READER_FAILED"
    finally:
        try:
            backend.close_handle(handle)
        except Exception:
            if state.error_type is None:
                state.error_type = "PIPE_HANDLE_CLOSE_FAILED"


def _accounting(backend: _WindowsBackend, job: Any) -> dict[str, int]:
    try:
        information = backend.win32job.QueryInformationJobObject(
            job, backend.win32job.JobObjectBasicAccountingInformation
        )
    except Exception:
        return {
            "TotalProcesses": 0,
            "ActiveProcesses": -1,
            "TotalTerminatedProcesses": 0,
        }
    return {
        "TotalProcesses": int(information["TotalProcesses"]),
        "ActiveProcesses": int(information["ActiveProcesses"]),
        "TotalTerminatedProcesses": int(information["TotalTerminatedProcesses"]),
    }


def _wait_for_tree_release(
    backend: _WindowsBackend,
    job: Any,
    timeout_ms: int,
) -> dict[str, int]:
    deadline = time.monotonic() + timeout_ms / 1000
    information = _accounting(backend, job)
    while information["ActiveProcesses"] != 0 and time.monotonic() < deadline:
        time.sleep(WAIT_SLICE_MS / 1000)
        information = _accounting(backend, job)
    return information


def _empty_stream() -> CapturedStream:
    return CapturedStream(
        content=b"",
        observed_bytes_lower_bound=0,
        stream_complete=False,
        overflowed=False,
        thread_stopped=True,
        error_type=None,
    )


def _pre_resume_failure_result(
    *,
    started: float,
    parent_in_job: bool,
    process_created: bool,
    target_assigned: bool,
    active_process_limit: int,
    active_process_limit_enforced: bool,
    termination_reason: str,
    error_type: str,
    accounting: dict[str, int],
    handles_released: bool,
    target_process_released: bool,
    forced_termination_requested: bool,
    forced_termination_processes_observed: int,
) -> OwnedProcessResult:
    tree_released = accounting["ActiveProcesses"] == 0
    return OwnedProcessResult(
        parent_in_job=parent_in_job,
        process_created=process_created,
        target_assigned=target_assigned,
        target_resumed=False,
        exit_code=None,
        termination_reason=termination_reason,
        error_type=error_type,
        stdout=_empty_stream(),
        stderr=_empty_stream(),
        active_process_limit=active_process_limit,
        active_process_limit_enforced=active_process_limit_enforced,
        process_limit_attempt_observation="NOT_PROVEN",
        total_assigned_processes=accounting["TotalProcesses"],
        final_active_processes=accounting["ActiveProcesses"],
        job_limit_terminated_processes=accounting["TotalTerminatedProcesses"],
        forced_termination_requested=forced_termination_requested,
        forced_termination_processes_observed=forced_termination_processes_observed,
        tree_released=tree_released,
        handles_released=handles_released,
        capture_threads_stopped=True,
        cleanup_complete=tree_released and handles_released and target_process_released,
        elapsed_ms=round((time.monotonic() - started) * 1000, 3),
    )


def run_owned_process(
    *,
    executable: Path,
    arguments: Sequence[str],
    working_directory: Path,
    environment: Mapping[str, str],
    timeout_ms: int,
    descendant_exit_grace_ms: int,
    max_stdout_bytes: int,
    max_stderr_bytes: int,
    max_processes: int,
    cancel_event: threading.Event | None = None,
    _backend: _WindowsBackend | None = None,
) -> OwnedProcessResult:
    _validate_runtime_inputs(
        executable,
        arguments,
        working_directory,
        environment,
        timeout_ms=timeout_ms,
        descendant_exit_grace_ms=descendant_exit_grace_ms,
        max_stdout_bytes=max_stdout_bytes,
        max_stderr_bytes=max_stderr_bytes,
        max_processes=max_processes,
    )
    require_windows_command_capability()
    backend = _WindowsBackend() if _backend is None else _backend
    started = time.monotonic()
    job, parent_in_job, limit_enforced = _create_job(backend, max_processes)
    handles_released = True
    process_handle: Any | None = None
    thread_handle: Any | None = None
    stdout_read: Any | None = None
    stdout_write: Any | None = None
    stderr_read: Any | None = None
    stderr_write: Any | None = None
    stdin_read: Any | None = None
    stdin_write: Any | None = None
    target_assigned = False
    target_resumed = False
    process_created = False
    forced_termination_requested = False
    forced_termination_processes_observed = 0
    stdout_thread: threading.Thread | None = None
    stderr_thread: threading.Thread | None = None
    stdout_overflow = threading.Event()
    stderr_overflow = threading.Event()
    stdout_state = _CaptureState(max_stdout_bytes, stdout_overflow)
    stderr_state = _CaptureState(max_stderr_bytes, stderr_overflow)

    def close(handle: Any | None) -> None:
        nonlocal handles_released
        if handle is None:
            return
        try:
            backend.close_handle(handle)
        except Exception:
            handles_released = False

    def terminate_job() -> None:
        nonlocal forced_termination_requested, forced_termination_processes_observed
        forced_termination_requested = True
        before = _accounting(backend, job)
        forced_termination_processes_observed = max(
            forced_termination_processes_observed,
            max(0, before["ActiveProcesses"]),
        )
        backend.win32job.TerminateJobObject(job, 1)

    try:
        stdout_read, stdout_write = _create_inheritable_pipe(backend)
        stderr_read, stderr_write = _create_inheritable_pipe(backend)
        stdin_read, stdin_write = _create_inheritable_pipe(backend)
        backend.win32api.SetHandleInformation(
            stdout_read, backend.win32con.HANDLE_FLAG_INHERIT, 0
        )
        backend.win32api.SetHandleInformation(
            stderr_read, backend.win32con.HANDLE_FLAG_INHERIT, 0
        )
        backend.win32api.SetHandleInformation(
            stdin_write, backend.win32con.HANDLE_FLAG_INHERIT, 0
        )
        close(stdin_write)
        stdin_write = None

        startup = backend.win32process.STARTUPINFO()
        startup.dwFlags |= backend.win32con.STARTF_USESTDHANDLES
        startup.hStdInput = stdin_read
        startup.hStdOutput = stdout_write
        startup.hStdError = stderr_write
        command_line = _build_command_line(executable, arguments)
        creation_flags = (
            backend.win32process.CREATE_SUSPENDED
            | backend.win32process.CREATE_NO_WINDOW
            | backend.win32process.CREATE_UNICODE_ENVIRONMENT
        )
        normalized_environment = {
            name: environment[name]
            for name in sorted(environment, key=lambda value: value.casefold())
        }
        try:
            process_handle, thread_handle, _, _ = backend.win32process.CreateProcess(
                str(executable),
                command_line,
                None,
                None,
                True,
                creation_flags,
                normalized_environment,
                str(working_directory),
                startup,
            )
            process_created = True
        except Exception:
            close(stdout_write)
            stdout_write = None
            close(stderr_write)
            stderr_write = None
            close(stdin_read)
            stdin_read = None
            close(stdout_read)
            stdout_read = None
            close(stderr_read)
            stderr_read = None
            accounting = _accounting(backend, job)
            close(job)
            job = None
            return _pre_resume_failure_result(
                started=started,
                parent_in_job=parent_in_job,
                process_created=False,
                target_assigned=False,
                active_process_limit=max_processes,
                active_process_limit_enforced=limit_enforced,
                termination_reason="PROCESS_CREATE_FAILED",
                error_type="PROCESS_CREATE_FAILED",
                accounting=accounting,
                handles_released=handles_released,
                target_process_released=True,
                forced_termination_requested=False,
                forced_termination_processes_observed=0,
            )

        close(stdout_write)
        stdout_write = None
        close(stderr_write)
        stderr_write = None
        close(stdin_read)
        stdin_read = None

        suspended_target_termination_requested = False
        suspended_target_released = False
        try:
            backend.assign_process_to_job(job, process_handle)
            target_assigned = True
        except Exception:
            try:
                suspended_target_termination_requested = True
                backend.win32process.TerminateProcess(process_handle, 1)
                suspended_target_released = (
                    backend.win32event.WaitForSingleObject(
                        process_handle, FORCED_CLEANUP_TIMEOUT_MS
                    )
                    == backend.win32event.WAIT_OBJECT_0
                )
            except Exception:
                suspended_target_released = False
            close(thread_handle)
            thread_handle = None
            close(process_handle)
            process_handle = None
            close(stdout_read)
            stdout_read = None
            close(stderr_read)
            stderr_read = None
            accounting = _accounting(backend, job)
            close(job)
            job = None
            return _pre_resume_failure_result(
                started=started,
                parent_in_job=parent_in_job,
                process_created=True,
                target_assigned=False,
                active_process_limit=max_processes,
                active_process_limit_enforced=limit_enforced,
                termination_reason="OWNERSHIP_ASSIGNMENT_FAILED",
                error_type="OWNERSHIP_ASSIGNMENT_FAILED",
                accounting=accounting,
                handles_released=handles_released,
                target_process_released=suspended_target_released,
                forced_termination_requested=suspended_target_termination_requested,
                forced_termination_processes_observed=(
                    1 if suspended_target_termination_requested else 0
                ),
            )

        stdout_thread = threading.Thread(
            target=_read_pipe,
            args=(backend, stdout_read, stdout_state),
            name="veritrail-command-stdout",
        )
        stderr_thread = threading.Thread(
            target=_read_pipe,
            args=(backend, stderr_read, stderr_state),
            name="veritrail-command-stderr",
        )
        stdout_thread.start()
        stderr_thread.start()
        try:
            previous_suspend_count = backend.resume_thread(thread_handle)
            if previous_suspend_count < 1:
                raise RuntimeError("unexpected suspend count")
            target_resumed = True
        except Exception:
            termination_reason = "TARGET_RESUME_FAILED"
            error_type = "TARGET_RESUME_FAILED"
            try:
                terminate_job()
                backend.win32event.WaitForSingleObject(
                    process_handle, FORCED_CLEANUP_TIMEOUT_MS
                )
            except Exception:
                error_type = "JOB_TERMINATION_FAILED"
        finally:
            close(thread_handle)
            thread_handle = None

        if target_resumed:
            deadline = time.monotonic() + timeout_ms / 1000
            termination_reason = "EXITED"
            error_type = None
            while True:
                if cancel_event is not None and cancel_event.is_set():
                    termination_reason = "CANCELLED"
                    break
                if stdout_overflow.is_set():
                    termination_reason = "STDOUT_LIMIT_EXCEEDED"
                    break
                if stderr_overflow.is_set():
                    termination_reason = "STDERR_LIMIT_EXCEEDED"
                    break
                if time.monotonic() >= deadline:
                    termination_reason = "TIMEOUT"
                    break
                wait_result = backend.win32event.WaitForSingleObject(
                    process_handle, WAIT_SLICE_MS
                )
                if wait_result == backend.win32event.WAIT_OBJECT_0:
                    if stdout_overflow.is_set():
                        termination_reason = "STDOUT_LIMIT_EXCEEDED"
                    elif stderr_overflow.is_set():
                        termination_reason = "STDERR_LIMIT_EXCEEDED"
                    break
                if wait_result != backend.win32event.WAIT_TIMEOUT:
                    termination_reason = "PROCESS_WAIT_FAILED"
                    error_type = "PROCESS_WAIT_FAILED"
                    break
            if termination_reason != "EXITED":
                try:
                    terminate_job()
                except Exception:
                    error_type = "JOB_TERMINATION_FAILED"
                backend.win32event.WaitForSingleObject(
                    process_handle, FORCED_CLEANUP_TIMEOUT_MS
                )
            else:
                descendant_deadline = (
                    time.monotonic() + descendant_exit_grace_ms / 1000
                )
                descendants = _accounting(backend, job)
                while (
                    descendants["ActiveProcesses"] != 0
                    and time.monotonic() < descendant_deadline
                ):
                    if cancel_event is not None and cancel_event.is_set():
                        termination_reason = "CANCELLED"
                        break
                    if stdout_overflow.is_set():
                        termination_reason = "STDOUT_LIMIT_EXCEEDED"
                        break
                    if stderr_overflow.is_set():
                        termination_reason = "STDERR_LIMIT_EXCEEDED"
                        break
                    time.sleep(WAIT_SLICE_MS / 1000)
                    descendants = _accounting(backend, job)
                if descendants["ActiveProcesses"] != 0:
                    if termination_reason == "EXITED":
                        termination_reason = "DESCENDANT_GRACE_EXPIRED"
                    try:
                        terminate_job()
                    except Exception:
                        error_type = "JOB_TERMINATION_FAILED"
        exit_code: int | None = None
        try:
            final_wait = backend.win32event.WaitForSingleObject(
                process_handle, FORCED_CLEANUP_TIMEOUT_MS
            )
            if final_wait != backend.win32event.WAIT_OBJECT_0:
                raise TimeoutError("owned root process did not become signaled")
            exit_code = int(backend.win32process.GetExitCodeProcess(process_handle))
        except Exception:
            if error_type is None:
                error_type = "PROCESS_EXIT_QUERY_FAILED"

        accounting = _wait_for_tree_release(
            backend, job, FORCED_CLEANUP_TIMEOUT_MS
        )
        close(process_handle)
        process_handle = None

        for reader in (stdout_thread, stderr_thread):
            if reader is not None:
                reader.join(FORCED_CLEANUP_TIMEOUT_MS / 1000)
        if stdout_thread is not None and stdout_thread.is_alive():
            close(stdout_read)
            stdout_read = None
            stdout_thread.join(WAIT_SLICE_MS / 1000)
        if stderr_thread is not None and stderr_thread.is_alive():
            close(stderr_read)
            stderr_read = None
            stderr_thread.join(WAIT_SLICE_MS / 1000)
        stdout_stopped = stdout_thread is None or not stdout_thread.is_alive()
        stderr_stopped = stderr_thread is None or not stderr_thread.is_alive()
        capture_threads_stopped = stdout_stopped and stderr_stopped
        if termination_reason == "EXITED":
            if stdout_state.overflowed:
                termination_reason = "STDOUT_LIMIT_EXCEEDED"
            elif stderr_state.overflowed:
                termination_reason = "STDERR_LIMIT_EXCEEDED"
        if not capture_threads_stopped and error_type is None:
            error_type = "CAPTURE_THREAD_CLEANUP_FAILED"

        close(job)
        job = None
        tree_released = accounting["ActiveProcesses"] == 0
        stdout_result = stdout_state.result(thread_stopped=stdout_stopped)
        stderr_result = stderr_state.result(thread_stopped=stderr_stopped)
        if (stdout_result.error_type or stderr_result.error_type) and error_type is None:
            error_type = "STREAM_CAPTURE_FAILED"
        cleanup_complete = (
            tree_released
            and handles_released
            and capture_threads_stopped
            and stdout_result.error_type is None
            and stderr_result.error_type is None
        )
        return OwnedProcessResult(
            parent_in_job=parent_in_job,
            process_created=process_created,
            target_assigned=target_assigned,
            target_resumed=target_resumed,
            exit_code=exit_code,
            termination_reason=termination_reason,
            error_type=error_type,
            stdout=stdout_result,
            stderr=stderr_result,
            active_process_limit=max_processes,
            active_process_limit_enforced=limit_enforced,
            process_limit_attempt_observation="NOT_PROVEN",
            total_assigned_processes=accounting["TotalProcesses"],
            final_active_processes=accounting["ActiveProcesses"],
            job_limit_terminated_processes=accounting["TotalTerminatedProcesses"],
            forced_termination_requested=forced_termination_requested,
            forced_termination_processes_observed=forced_termination_processes_observed,
            tree_released=tree_released,
            handles_released=handles_released,
            capture_threads_stopped=capture_threads_stopped,
            cleanup_complete=cleanup_complete,
            elapsed_ms=round((time.monotonic() - started) * 1000, 3),
        )
    finally:
        close(thread_handle)
        close(process_handle)
        close(stdout_write)
        close(stderr_write)
        close(stdin_read)
        close(stdin_write)
        if stdout_thread is None:
            close(stdout_read)
        if stderr_thread is None:
            close(stderr_read)
        close(job)
