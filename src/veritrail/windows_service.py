from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from veritrail.errors import SafetyError
from veritrail.windows_job import (
    FORCED_CLEANUP_TIMEOUT_MS,
    WAIT_SLICE_MS,
    CapturedStream,
    _accounting,
    _build_command_line,
    _CaptureState,
    _create_inheritable_pipe,
    _create_job,
    _read_pipe,
    _validate_runtime_inputs,
    _wait_for_tree_release,
    _WindowsBackend,
    require_windows_command_capability,
)
from veritrail.windows_tcp import list_ipv4_tcp_listeners


@dataclass(frozen=True)
class OwnedServiceStartObservation:
    parent_in_job: bool | None
    process_created: bool
    target_assigned: bool
    target_resumed: bool
    active_process_limit: int
    active_process_limit_enforced: bool
    cleanup_complete: bool
    error_type: str | None
    elapsed_ms: float


@dataclass(frozen=True)
class OwnedServiceTeardownObservation:
    requested: bool
    total_assigned_processes: int
    final_active_processes: int
    forced_termination_requested: bool
    root_signaled: bool
    root_exit_code: int | None
    termination_reason: str
    handles_released: bool
    readers_released: bool
    port_free: bool
    stdout: CapturedStream
    stderr: CapturedStream
    error_type: str | None
    cleanup_complete: bool
    elapsed_ms: float


class OwnedServiceStartError(SafetyError):
    def __init__(
        self, error_type: str, observation: OwnedServiceStartObservation
    ) -> None:
        super().__init__(f"M10 owned service start failed: {error_type}")
        self.error_type = error_type
        self.observation = observation


def _active_process_ids(backend: _WindowsBackend, job: Any) -> frozenset[int]:
    try:
        raw = backend.win32job.QueryInformationJobObject(
            job, backend.win32job.JobObjectBasicProcessIdList
        )
    except Exception as exc:
        raise SafetyError("M10 could not query the owned Job process list") from exc
    if not isinstance(raw, (tuple, list)):
        raise SafetyError("M10 received an invalid owned Job process list")
    try:
        process_ids = tuple(int(value) for value in raw)
    except (TypeError, ValueError) as exc:
        raise SafetyError("M10 received an invalid owned Job process list") from exc
    if any(value <= 0 for value in process_ids) or len(set(process_ids)) != len(process_ids):
        raise SafetyError("M10 received an invalid owned Job process list")
    return frozenset(process_ids)


def _wait_for_port_release(port: int, timeout_ms: int) -> tuple[bool, bool]:
    deadline = time.monotonic() + timeout_ms / 1000
    while True:
        try:
            occupied = any(
                listener.local_port == port for listener in list_ipv4_tcp_listeners()
            )
        except SafetyError:
            return False, False
        if not occupied:
            return True, True
        if time.monotonic() >= deadline:
            return False, True
        time.sleep(WAIT_SLICE_MS / 1000)


class OwnedServiceSession:
    def __init__(
        self,
        *,
        node_id: str,
        backend: _WindowsBackend,
        job: Any,
        process_handle: Any,
        stdout_read: Any,
        stderr_read: Any,
        stdout_thread: threading.Thread,
        stderr_thread: threading.Thread,
        stdout_state: _CaptureState,
        stderr_state: _CaptureState,
        start_observation: OwnedServiceStartObservation,
        port: int,
        process_release_timeout_ms: int,
        port_release_timeout_ms: int,
        reader_shutdown_timeout_ms: int,
    ) -> None:
        self.node_id = node_id
        self._backend = backend
        self._job = job
        self._process_handle = process_handle
        self._stdout_read = stdout_read
        self._stderr_read = stderr_read
        self._stdout_thread = stdout_thread
        self._stderr_thread = stderr_thread
        self._stdout_state = stdout_state
        self._stderr_state = stderr_state
        self.start_observation = start_observation
        self.port = port
        self._process_release_timeout_ms = process_release_timeout_ms
        self._port_release_timeout_ms = port_release_timeout_ms
        self._reader_shutdown_timeout_ms = reader_shutdown_timeout_ms
        self._teardown: OwnedServiceTeardownObservation | None = None

    @classmethod
    def start(
        cls,
        *,
        node_id: str,
        executable: Path,
        arguments: Sequence[str],
        working_directory: Path,
        environment: Mapping[str, str],
        port: int,
        max_stdout_bytes: int,
        max_stderr_bytes: int,
        max_processes: int,
        process_release_timeout_ms: int,
        port_release_timeout_ms: int,
        reader_shutdown_timeout_ms: int,
        _backend: _WindowsBackend | None = None,
    ) -> OwnedServiceSession:
        _validate_runtime_inputs(
            executable,
            arguments,
            working_directory,
            environment,
            timeout_ms=1_000,
            descendant_exit_grace_ms=100,
            max_stdout_bytes=max_stdout_bytes,
            max_stderr_bytes=max_stderr_bytes,
            max_processes=max_processes,
        )
        if not isinstance(node_id, str) or not node_id:
            raise SafetyError("M10 owned service requires a node id")
        if not isinstance(port, int) or isinstance(port, bool) or not 1024 <= port <= 65535:
            raise SafetyError("M10 owned service port is outside the sealed range")
        for name, value in (
            ("process_release_timeout_ms", process_release_timeout_ms),
            ("port_release_timeout_ms", port_release_timeout_ms),
            ("reader_shutdown_timeout_ms", reader_shutdown_timeout_ms),
        ):
            if not isinstance(value, int) or isinstance(value, bool) or not 100 <= value <= 10_000:
                raise SafetyError(f"M10 owned service {name} is outside the sealed range")

        require_windows_command_capability()
        backend = _WindowsBackend() if _backend is None else _backend
        started = time.monotonic()
        try:
            job, parent_in_job, limit_enforced = _create_job(backend, max_processes)
        except Exception as exc:
            observation = OwnedServiceStartObservation(
                parent_in_job=None,
                process_created=False,
                target_assigned=False,
                target_resumed=False,
                active_process_limit=max_processes,
                active_process_limit_enforced=False,
                cleanup_complete=True,
                error_type="JOB_CREATION_FAILED",
                elapsed_ms=round((time.monotonic() - started) * 1000, 3),
            )
            raise OwnedServiceStartError(
                "JOB_CREATION_FAILED", observation
            ) from exc
        process_handle: Any | None = None
        thread_handle: Any | None = None
        stdout_read: Any | None = None
        stdout_write: Any | None = None
        stderr_read: Any | None = None
        stderr_write: Any | None = None
        stdin_read: Any | None = None
        stdin_write: Any | None = None
        stdout_thread: threading.Thread | None = None
        stderr_thread: threading.Thread | None = None
        stdout_state = _CaptureState(max_stdout_bytes, threading.Event())
        stderr_state = _CaptureState(max_stderr_bytes, threading.Event())
        process_created = False
        target_assigned = False
        target_resumed = False
        handles_released = True

        def close(handle: Any | None) -> bool:
            nonlocal handles_released
            if handle is None:
                return True
            try:
                backend.close_handle(handle)
                return True
            except Exception:
                handles_released = False
                return False

        def fail(error_type: str) -> OwnedServiceStartError:
            nonlocal job
            nonlocal process_handle, thread_handle
            nonlocal stdout_read, stdout_write, stderr_read, stderr_write
            nonlocal stdin_read, stdin_write
            close(stdout_write)
            stdout_write = None
            close(stderr_write)
            stderr_write = None
            close(stdin_read)
            stdin_read = None
            close(stdin_write)
            stdin_write = None
            if process_created:
                try:
                    if target_assigned:
                        backend.win32job.TerminateJobObject(job, 1)
                    else:
                        backend.win32process.TerminateProcess(process_handle, 1)
                except Exception:
                    error_type = "START_CLEANUP_TERMINATION_FAILED"
                try:
                    backend.win32event.WaitForSingleObject(
                        process_handle, FORCED_CLEANUP_TIMEOUT_MS
                    )
                except Exception:
                    pass
            close(thread_handle)
            thread_handle = None
            if stdout_thread is not None:
                stdout_thread.join(FORCED_CLEANUP_TIMEOUT_MS / 1000)
                if stdout_thread.is_alive():
                    close(stdout_read)
                    stdout_read = None
                    stdout_thread.join(WAIT_SLICE_MS / 1000)
            else:
                close(stdout_read)
                stdout_read = None
            if stderr_thread is not None:
                stderr_thread.join(FORCED_CLEANUP_TIMEOUT_MS / 1000)
                if stderr_thread.is_alive():
                    close(stderr_read)
                    stderr_read = None
                    stderr_thread.join(WAIT_SLICE_MS / 1000)
            else:
                close(stderr_read)
                stderr_read = None
            close(process_handle)
            process_handle = None
            information = _wait_for_tree_release(
                backend, job, FORCED_CLEANUP_TIMEOUT_MS
            )
            close(job)
            job = None
            readers_released = (
                (stdout_thread is None or not stdout_thread.is_alive())
                and (stderr_thread is None or not stderr_thread.is_alive())
            )
            cleanup_complete = (
                information["ActiveProcesses"] == 0
                and handles_released
                and readers_released
                and stdout_state.error_type is None
                and stderr_state.error_type is None
            )
            return OwnedServiceStartError(
                error_type,
                OwnedServiceStartObservation(
                    parent_in_job=parent_in_job,
                    process_created=process_created,
                    target_assigned=target_assigned,
                    target_resumed=target_resumed,
                    active_process_limit=max_processes,
                    active_process_limit_enforced=limit_enforced,
                    cleanup_complete=cleanup_complete,
                    error_type=error_type,
                    elapsed_ms=round((time.monotonic() - started) * 1000, 3),
                ),
            )

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
            if not close(stdin_write):
                raise fail("PARENT_PIPE_CLOSE_FAILED")
            stdin_write = None

            startup = backend.win32process.STARTUPINFO()
            startup.dwFlags |= backend.win32con.STARTF_USESTDHANDLES
            startup.hStdInput = stdin_read
            startup.hStdOutput = stdout_write
            startup.hStdError = stderr_write
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
                    _build_command_line(executable, arguments),
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
                raise fail("PROCESS_CREATE_FAILED")

            if not close(stdout_write) or not close(stderr_write) or not close(stdin_read):
                raise fail("PARENT_PIPE_CLOSE_FAILED")
            stdout_write = None
            stderr_write = None
            stdin_read = None
            try:
                backend.assign_process_to_job(job, process_handle)
                target_assigned = True
            except Exception:
                raise fail("OWNERSHIP_ASSIGNMENT_FAILED")

            stdout_thread = threading.Thread(
                target=_read_pipe,
                args=(backend, stdout_read, stdout_state),
                name=f"veritrail-bootstrap-{node_id}-stdout",
            )
            stderr_thread = threading.Thread(
                target=_read_pipe,
                args=(backend, stderr_read, stderr_state),
                name=f"veritrail-bootstrap-{node_id}-stderr",
            )
            stdout_thread.start()
            stderr_thread.start()
            try:
                if backend.resume_thread(thread_handle) < 1:
                    raise RuntimeError("unexpected suspend count")
                target_resumed = True
            except Exception:
                raise fail("TARGET_RESUME_FAILED")
            if not close(thread_handle):
                raise fail("THREAD_HANDLE_CLOSE_FAILED")
            thread_handle = None
            observation = OwnedServiceStartObservation(
                parent_in_job=parent_in_job,
                process_created=True,
                target_assigned=True,
                target_resumed=True,
                active_process_limit=max_processes,
                active_process_limit_enforced=limit_enforced,
                cleanup_complete=False,
                error_type=None,
                elapsed_ms=round((time.monotonic() - started) * 1000, 3),
            )
            return cls(
                node_id=node_id,
                backend=backend,
                job=job,
                process_handle=process_handle,
                stdout_read=stdout_read,
                stderr_read=stderr_read,
                stdout_thread=stdout_thread,
                stderr_thread=stderr_thread,
                stdout_state=stdout_state,
                stderr_state=stderr_state,
                start_observation=observation,
                port=port,
                process_release_timeout_ms=process_release_timeout_ms,
                port_release_timeout_ms=port_release_timeout_ms,
                reader_shutdown_timeout_ms=reader_shutdown_timeout_ms,
            )
        except OwnedServiceStartError:
            raise
        except Exception:
            raise fail("SERVICE_START_INTERNAL_ERROR")
        finally:
            if not target_resumed:
                close(stdout_write)
                close(stderr_write)
                close(stdin_read)
                close(stdin_write)

    def active_process_ids(self) -> frozenset[int]:
        if self._teardown is not None:
            return frozenset()
        return _active_process_ids(self._backend, self._job)

    def sample_rss_bytes(self) -> int:
        """Return a race-checked working-set sample for this owned Job tree."""

        if self._teardown is not None:
            return 0
        query_access = (
            self._backend.win32con.PROCESS_QUERY_INFORMATION
            | self._backend.win32con.PROCESS_VM_READ
        )
        for _ in range(2):
            before = self.active_process_ids()
            total = 0
            failed = False
            for process_id in before:
                handle: Any | None = None
                try:
                    handle = self._backend.win32api.OpenProcess(
                        query_access, False, process_id
                    )
                    information = self._backend.win32process.GetProcessMemoryInfo(handle)
                    total += int(information["WorkingSetSize"])
                except Exception:
                    failed = True
                finally:
                    if handle is not None:
                        try:
                            self._backend.close_handle(handle)
                        except Exception:
                            failed = True
            after = self.active_process_ids()
            if before == after and not failed:
                return total
        raise SafetyError("M10 could not obtain a stable owned Job RSS sample")

    def snapshot_streams(self) -> tuple[CapturedStream, CapturedStream]:
        """Copy bounded stream facts before teardown without stopping readers."""

        if self._teardown is not None:
            return self._teardown.stdout, self._teardown.stderr
        return (
            self._stdout_state.result(thread_stopped=False),
            self._stderr_state.result(thread_stopped=False),
        )

    def root_exit_code(self) -> int | None:
        if self._teardown is not None:
            return None
        result = self._backend.win32event.WaitForSingleObject(self._process_handle, 0)
        if result == self._backend.win32event.WAIT_TIMEOUT:
            return None
        if result != self._backend.win32event.WAIT_OBJECT_0:
            raise SafetyError("M10 could not query the owned root process state")
        try:
            return int(self._backend.win32process.GetExitCodeProcess(self._process_handle))
        except Exception as exc:
            raise SafetyError("M10 could not query the owned root process exit code") from exc

    def stream_error_type(self) -> str | None:
        if self._stdout_state.overflowed:
            return "STDOUT_LIMIT_EXCEEDED"
        if self._stderr_state.overflowed:
            return "STDERR_LIMIT_EXCEEDED"
        if self._stdout_state.error_type or self._stderr_state.error_type:
            return "STREAM_CAPTURE_FAILED"
        return None

    def terminate(self) -> OwnedServiceTeardownObservation:
        if self._teardown is not None:
            return self._teardown
        started = time.monotonic()
        handles_released = True
        error_type: str | None = None
        before = _accounting(self._backend, self._job)
        forced = before["ActiveProcesses"] != 0
        if forced:
            try:
                self._backend.win32job.TerminateJobObject(self._job, 1)
            except Exception:
                error_type = "JOB_TERMINATION_FAILED"
        information = _wait_for_tree_release(
            self._backend, self._job, self._process_release_timeout_ms
        )
        if information["ActiveProcesses"] != 0 and error_type is None:
            error_type = "PROCESS_RELEASE_TIMEOUT"

        root_signaled = False
        root_exit_code: int | None = None
        try:
            root_signaled = (
                self._backend.win32event.WaitForSingleObject(
                    self._process_handle, self._process_release_timeout_ms
                )
                == self._backend.win32event.WAIT_OBJECT_0
            )
        except Exception:
            root_signaled = False
        if not root_signaled and error_type is None:
            error_type = "ROOT_PROCESS_NOT_SIGNALED"
        if root_signaled:
            try:
                root_exit_code = int(
                    self._backend.win32process.GetExitCodeProcess(
                        self._process_handle
                    )
                )
            except Exception:
                if error_type is None:
                    error_type = "PROCESS_EXIT_QUERY_FAILED"

        try:
            self._backend.close_handle(self._process_handle)
        except Exception:
            handles_released = False
        self._process_handle = None

        for thread in (self._stdout_thread, self._stderr_thread):
            thread.join(self._reader_shutdown_timeout_ms / 1000)
        if self._stdout_thread.is_alive():
            try:
                self._backend.close_handle(self._stdout_read)
            except Exception:
                handles_released = False
            self._stdout_thread.join(WAIT_SLICE_MS / 1000)
        if self._stderr_thread.is_alive():
            try:
                self._backend.close_handle(self._stderr_read)
            except Exception:
                handles_released = False
            self._stderr_thread.join(WAIT_SLICE_MS / 1000)
        readers_released = (
            not self._stdout_thread.is_alive() and not self._stderr_thread.is_alive()
        )
        if not readers_released and error_type is None:
            error_type = "READER_SHUTDOWN_FAILED"
        stdout = self._stdout_state.result(
            thread_stopped=not self._stdout_thread.is_alive()
        )
        stderr = self._stderr_state.result(
            thread_stopped=not self._stderr_thread.is_alive()
        )
        if (stdout.error_type or stderr.error_type) and error_type is None:
            error_type = "STREAM_CAPTURE_FAILED"

        try:
            self._backend.close_handle(self._job)
        except Exception:
            handles_released = False
        self._job = None
        if not handles_released and error_type is None:
            error_type = "HANDLE_RELEASE_FAILED"

        port_free, port_query_complete = _wait_for_port_release(
            self.port, self._port_release_timeout_ms
        )
        if not port_query_complete and error_type is None:
            error_type = "PORT_RELEASE_QUERY_FAILED"
        elif not port_free and error_type is None:
            error_type = "PORT_RELEASE_TIMEOUT"
        cleanup_complete = (
            information["ActiveProcesses"] == 0
            and root_signaled
            and handles_released
            and readers_released
            and stdout.error_type is None
            and stderr.error_type is None
            and port_free
            and port_query_complete
            and error_type is None
        )
        self._teardown = OwnedServiceTeardownObservation(
            requested=True,
            total_assigned_processes=information["TotalProcesses"],
            final_active_processes=information["ActiveProcesses"],
            forced_termination_requested=forced,
            root_signaled=root_signaled,
            root_exit_code=root_exit_code,
            termination_reason="JOB_TERMINATED" if forced else "ROOT_EXITED",
            handles_released=handles_released,
            readers_released=readers_released,
            port_free=port_free,
            stdout=stdout,
            stderr=stderr,
            error_type=error_type,
            cleanup_complete=cleanup_complete,
            elapsed_ms=round((time.monotonic() - started) * 1000, 3),
        )
        return self._teardown
