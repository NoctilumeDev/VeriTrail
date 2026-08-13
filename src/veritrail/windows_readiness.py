from __future__ import annotations

import http.client
import threading
import time
from dataclasses import dataclass
from typing import Any, Mapping

from veritrail.errors import SafetyError
from veritrail.stop_control import requested_stop_reason
from veritrail.windows_service import OwnedServiceSession
from veritrail.windows_tcp import list_ipv4_tcp_listeners


@dataclass(frozen=True)
class ReadinessAttempt:
    ordinal: int
    elapsed_ms: float
    result: str
    http_status: int | None
    response_byte_count: int | None
    listener_owner_in_job: bool
    job_active_process_count: int


@dataclass(frozen=True)
class OwnedReadinessObservation:
    ready: bool
    attempts: tuple[ReadinessAttempt, ...]
    error_type: str | None
    elapsed_ms: float


def _attempt(
    *,
    started: float,
    ordinal: int,
    result: str,
    http_status: int | None = None,
    response_byte_count: int | None = None,
    listener_owner_in_job: bool = False,
    job_active_process_count: int = 0,
) -> ReadinessAttempt:
    return ReadinessAttempt(
        ordinal=ordinal,
        elapsed_ms=round((time.monotonic() - started) * 1000, 3),
        result=result,
        http_status=http_status,
        response_byte_count=response_byte_count,
        listener_owner_in_job=listener_owner_in_job,
        job_active_process_count=job_active_process_count,
    )


def _post_response_ownership(
    session: OwnedServiceSession,
    *,
    expected_owner: int,
    expected_processes: frozenset[int],
) -> tuple[str, int]:
    before = session.active_process_ids()
    listeners = list_ipv4_tcp_listeners()
    after = session.active_process_ids()
    port_rows = [
        listener for listener in listeners if listener.local_port == session.port
    ]
    loopback_rows = [
        listener for listener in port_rows if listener.local_address == "127.0.0.1"
    ]
    if (
        len(port_rows) != 1
        or len(loopback_rows) != 1
        or loopback_rows[0].owning_pid != expected_owner
        or expected_owner not in before
        or expected_owner not in after
    ):
        return "LISTENER_OWNERSHIP_CHANGED", len(after)
    if before != after or before != expected_processes:
        return "JOB_PROCESS_SET_CHANGED", len(after)
    return "STABLE", len(after)


def probe_owned_http_readiness(
    session: OwnedServiceSession,
    readiness: Mapping[str, Any],
    *,
    cancel_event: threading.Event | None = None,
    lifecycle_deadline: float | None = None,
) -> OwnedReadinessObservation:
    started = time.monotonic()
    local_deadline = started + int(readiness["total_timeout_ms"]) / 1000
    deadline = min(local_deadline, lifecycle_deadline) if lifecycle_deadline else local_deadline
    attempts: list[ReadinessAttempt] = []
    consecutive = 0
    ordinal = 0
    terminal_error: str | None = None

    while time.monotonic() < deadline:
        ordinal += 1
        cancellation_reason = requested_stop_reason(cancel_event)
        if cancellation_reason is not None:
            attempts.append(
                _attempt(started=started, ordinal=ordinal, result="CANCELLED")
            )
            terminal_error = cancellation_reason
            break
        stream_error = session.stream_error_type()
        if stream_error is not None:
            attempts.append(
                _attempt(started=started, ordinal=ordinal, result=stream_error)
            )
            terminal_error = stream_error
            break
        try:
            root_exit = session.root_exit_code()
        except SafetyError:
            attempts.append(
                _attempt(started=started, ordinal=ordinal, result="ROOT_QUERY_FAILED")
            )
            terminal_error = "COLLECTOR_ERROR"
            break
        if root_exit is not None:
            attempts.append(
                _attempt(started=started, ordinal=ordinal, result="NODE_EARLY_EXIT")
            )
            terminal_error = "NODE_EARLY_EXIT"
            break

        try:
            before = session.active_process_ids()
            listeners = list_ipv4_tcp_listeners()
            after = session.active_process_ids()
        except SafetyError:
            attempts.append(
                _attempt(started=started, ordinal=ordinal, result="OWNERSHIP_QUERY_FAILED")
            )
            terminal_error = "COLLECTOR_ERROR"
            break
        active_count = len(after)
        port_rows = [
            listener for listener in listeners if listener.local_port == session.port
        ]
        loopback_rows = [
            listener for listener in port_rows if listener.local_address == "127.0.0.1"
        ]
        if port_rows and len(loopback_rows) != len(port_rows):
            attempts.append(
                _attempt(
                    started=started,
                    ordinal=ordinal,
                    result="LISTENER_ADDRESS_MISMATCH",
                    job_active_process_count=active_count,
                )
            )
            terminal_error = "LISTENER_OWNERSHIP_MISMATCH"
            break
        if len(loopback_rows) > 1:
            attempts.append(
                _attempt(
                    started=started,
                    ordinal=ordinal,
                    result="LISTENER_DUPLICATE",
                    job_active_process_count=active_count,
                )
            )
            terminal_error = "LISTENER_OWNERSHIP_MISMATCH"
            break
        if len(loopback_rows) == 0:
            attempts.append(
                _attempt(
                    started=started,
                    ordinal=ordinal,
                    result="LISTENER_NOT_FOUND",
                    job_active_process_count=active_count,
                )
            )
            consecutive = 0
        elif before != after:
            attempts.append(
                _attempt(
                    started=started,
                    ordinal=ordinal,
                    result="JOB_PROCESS_SET_CHANGED",
                    job_active_process_count=active_count,
                )
            )
            consecutive = 0
        else:
            owner = loopback_rows[0].owning_pid
            owned = owner in before and owner in after
            if not owned:
                attempts.append(
                    _attempt(
                        started=started,
                        ordinal=ordinal,
                        result="LISTENER_OWNER_NOT_IN_JOB",
                        job_active_process_count=active_count,
                    )
                )
                terminal_error = "LISTENER_OWNERSHIP_MISMATCH"
                break
            try:
                root_exit = session.root_exit_code()
            except SafetyError:
                attempts.append(
                    _attempt(
                        started=started,
                        ordinal=ordinal,
                        result="ROOT_QUERY_FAILED",
                        listener_owner_in_job=True,
                        job_active_process_count=active_count,
                    )
                )
                terminal_error = "COLLECTOR_ERROR"
                break
            if root_exit is not None:
                attempts.append(
                    _attempt(
                        started=started,
                        ordinal=ordinal,
                        result="NODE_EARLY_EXIT",
                        listener_owner_in_job=True,
                        job_active_process_count=active_count,
                    )
                )
                terminal_error = "NODE_EARLY_EXIT"
                break
            connection = http.client.HTTPConnection(
                "127.0.0.1",
                session.port,
                timeout=int(readiness["attempt_timeout_ms"]) / 1000,
            )
            try:
                connection.request(
                    "GET",
                    str(readiness["path"]),
                    headers={"Connection": "close"},
                )
                response = connection.getresponse()
                content = response.read(int(readiness["max_response_bytes"]) + 1)
                status = int(response.status)
                byte_count = len(content)
                try:
                    ownership, post_active_count = _post_response_ownership(
                        session,
                        expected_owner=owner,
                        expected_processes=after,
                    )
                except SafetyError:
                    attempts.append(
                        _attempt(
                            started=started,
                            ordinal=ordinal,
                            result="OWNERSHIP_QUERY_FAILED",
                            http_status=status,
                            response_byte_count=byte_count,
                            job_active_process_count=active_count,
                        )
                    )
                    terminal_error = "COLLECTOR_ERROR"
                    break
                if ownership == "LISTENER_OWNERSHIP_CHANGED":
                    attempts.append(
                        _attempt(
                            started=started,
                            ordinal=ordinal,
                            result=ownership,
                            http_status=status,
                            response_byte_count=byte_count,
                            job_active_process_count=post_active_count,
                        )
                    )
                    terminal_error = "LISTENER_OWNERSHIP_MISMATCH"
                    break
                if ownership == "JOB_PROCESS_SET_CHANGED":
                    attempts.append(
                        _attempt(
                            started=started,
                            ordinal=ordinal,
                            result=ownership,
                            http_status=status,
                            response_byte_count=byte_count,
                            listener_owner_in_job=True,
                            job_active_process_count=post_active_count,
                        )
                    )
                    consecutive = 0
                else:
                    if byte_count > int(readiness["max_response_bytes"]):
                        result = "HTTP_RESPONSE_TOO_LARGE"
                        consecutive = 0
                    elif status != int(readiness["expected_status"]):
                        result = "HTTP_STATUS_MISMATCH"
                        consecutive = 0
                    else:
                        result = "SUCCESS"
                        consecutive += 1
                    attempts.append(
                        _attempt(
                            started=started,
                            ordinal=ordinal,
                            result=result,
                            http_status=status,
                            response_byte_count=byte_count,
                            listener_owner_in_job=True,
                            job_active_process_count=active_count,
                        )
                    )
                    if consecutive == int(readiness["consecutive_successes"]):
                        return OwnedReadinessObservation(
                            ready=True,
                            attempts=tuple(attempts),
                            error_type=None,
                            elapsed_ms=round((time.monotonic() - started) * 1000, 3),
                        )
            except (OSError, http.client.HTTPException):
                attempts.append(
                    _attempt(
                        started=started,
                        ordinal=ordinal,
                        result="HTTP_REQUEST_FAILED",
                        listener_owner_in_job=True,
                        job_active_process_count=active_count,
                    )
                )
                consecutive = 0
            finally:
                connection.close()

        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(int(readiness["interval_ms"]) / 1000, remaining))

    if terminal_error is None:
        terminal_error = (
            "LIFECYCLE_TIMEOUT"
            if lifecycle_deadline is not None and lifecycle_deadline <= local_deadline
            else "READINESS_TIMEOUT"
        )
    return OwnedReadinessObservation(
        ready=False,
        attempts=tuple(attempts),
        error_type=terminal_error,
        elapsed_ms=round((time.monotonic() - started) * 1000, 3),
    )
