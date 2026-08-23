from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable

from veritrail.browser import _collect_browser_evidence
from veritrail.evidence import ImportedEvidence
from veritrail.errors import SafetyError
from veritrail.resources import MEBIBYTE
from veritrail.stop_control import StopRequested
from veritrail.windows_job import (
    WAIT_SLICE_MS,
    _WindowsBackend,
    _create_job,
    require_windows_command_capability,
)

MAX_BROWSER_PROCESSES = 64
BROWSER_RELEASE_TIMEOUT_MS = 3_000
PROCESS_SYNCHRONIZE = 0x00100000
PROCESS_SET_QUOTA = 0x0100
PROCESS_TERMINATE = 0x0001


@dataclass(frozen=True)
class ObservedBrowserEvidence:
    browser: ImportedEvidence
    peak_rss_mb: float | None
    resource_sampling_complete: bool
    process_cleanup_complete: bool
    job_memory_limit_mb: int
    job_memory_limit_enforced: bool


class ObservedBrowserInterrupted(StopRequested):
    def __init__(
        self,
        reason: str,
        *,
        peak_rss_mb: float | None,
        resource_sampling_complete: bool,
        process_cleanup_complete: bool,
        job_memory_limit_mb: int,
        job_memory_limit_enforced: bool,
    ) -> None:
        self.peak_rss_mb = peak_rss_mb
        self.resource_sampling_complete = resource_sampling_complete
        self.process_cleanup_complete = process_cleanup_complete
        self.job_memory_limit_mb = job_memory_limit_mb
        self.job_memory_limit_enforced = job_memory_limit_enforced
        super().__init__(reason)


class ObservedBrowserCollectionError(Exception):
    def __init__(
        self,
        error_type: str,
        *,
        peak_rss_mb: float | None,
        resource_sampling_complete: bool,
        process_cleanup_complete: bool,
        job_memory_limit_mb: int,
        job_memory_limit_enforced: bool,
    ) -> None:
        self.error_type = error_type
        self.peak_rss_mb = peak_rss_mb
        self.resource_sampling_complete = resource_sampling_complete
        self.process_cleanup_complete = process_cleanup_complete
        self.job_memory_limit_mb = job_memory_limit_mb
        self.job_memory_limit_enforced = job_memory_limit_enforced
        super().__init__(error_type)


class _ChromiumResourceObserver:
    """Observe only Chromium processes identified by the owned CDP connection."""

    def __init__(self, backend: _WindowsBackend, max_job_memory_mb: int) -> None:
        self._backend = backend
        self._max_job_memory_mb = max_job_memory_mb
        (
            self._job,
            _,
            self._process_limit_enforced,
            self._memory_limit_enforced,
        ) = _create_job(backend, MAX_BROWSER_PROCESSES, max_job_memory_mb)
        self._session: Any | None = None
        self._handles: dict[int, Any] = {}
        self._peak_rss_bytes = 0
        self._sample_count = 0
        self._errors: list[str] = []
        self._detached = False
        self._after_close_observed = False
        self._processes_released = False
        self._handles_released = True
        self._driver_assigned = False

    def failed(self, stage: str, error_type: str) -> None:
        code = f"{stage}:{error_type}"
        if code not in self._errors:
            self._errors.append(code)

    def playwright_started(self, playwright: Any) -> None:
        try:
            process = playwright._impl_obj._connection._transport._proc
            process_id = process.pid
        except (AttributeError, TypeError) as exc:
            raise SafetyError("M10 Playwright driver identity is unavailable") from exc
        if (
            not isinstance(process_id, int)
            or isinstance(process_id, bool)
            or process_id <= 0
        ):
            raise SafetyError("M10 Playwright driver identity is invalid")
        access = (
            self._backend.win32con.PROCESS_QUERY_INFORMATION
            | self._backend.win32con.PROCESS_VM_READ
            | PROCESS_SYNCHRONIZE
            | PROCESS_SET_QUOTA
            | PROCESS_TERMINATE
        )
        handle = self._backend.win32api.OpenProcess(access, False, process_id)
        try:
            if not self._backend.win32job.IsProcessInJob(handle, self._job):
                self._backend.assign_process_to_job(self._job, handle)
            if not self._backend.win32job.IsProcessInJob(handle, self._job):
                raise SafetyError("M10 Playwright driver Job assignment was not verified")
            self._handles[process_id] = handle
            self._driver_assigned = True
        except Exception:
            self._backend.close_handle(handle)
            raise

    def _process_ids(self) -> frozenset[int]:
        if self._session is None:
            raise SafetyError("M10 Chromium CDP observer is not attached")
        response = self._session.send("SystemInfo.getProcessInfo")
        values = response.get("processInfo") if isinstance(response, dict) else None
        if not isinstance(values, list):
            raise SafetyError("M10 Chromium CDP process response is invalid")
        process_ids: list[int] = []
        for value in values:
            process_id = value.get("id") if isinstance(value, dict) else None
            if (
                not isinstance(process_id, int)
                or isinstance(process_id, bool)
                or process_id <= 0
            ):
                raise SafetyError("M10 Chromium CDP process identity is invalid")
            process_ids.append(process_id)
        if (
            not process_ids
            or len(process_ids) > MAX_BROWSER_PROCESSES
            or len(set(process_ids)) != len(process_ids)
        ):
            raise SafetyError("M10 Chromium CDP process set is outside the bounded policy")
        return frozenset(process_ids)

    def _ensure_handles(self, process_ids: frozenset[int]) -> None:
        access = (
            self._backend.win32con.PROCESS_QUERY_INFORMATION
            | self._backend.win32con.PROCESS_VM_READ
            | PROCESS_SYNCHRONIZE
            | PROCESS_SET_QUOTA
            | PROCESS_TERMINATE
        )
        for process_id in process_ids:
            existing = self._handles.get(process_id)
            if existing is not None:
                if not self._handle_is_signalled(existing):
                    continue
                self._backend.close_handle(existing)
                del self._handles[process_id]
            handle = self._backend.win32api.OpenProcess(access, False, process_id)
            try:
                if not self._backend.win32job.IsProcessInJob(handle, self._job):
                    try:
                        self._backend.assign_process_to_job(self._job, handle)
                    except Exception:
                        # CDP includes short-lived Chromium utility processes. A
                        # process can exit after enumeration but before Job
                        # assignment; a signalled process is already harmless and
                        # must not turn a valid capture into collector failure.
                        # A still-live unassignable process remains a hard failure.
                        if not self._handle_is_signalled(handle):
                            raise
                        self._backend.close_handle(handle)
                        continue
                self._handles[process_id] = handle
            except Exception:
                self._backend.close_handle(handle)
                raise

    def _handle_is_signalled(self, handle: Any) -> bool:
        return (
            self._backend.win32event.WaitForSingleObject(handle, 0)
            == self._backend.win32event.WAIT_OBJECT_0
        )

    def _sample(self) -> None:
        last_error: Exception | None = None
        for _ in range(3):
            try:
                before = self._process_ids()
                self._ensure_handles(before)
                sampled = frozenset(
                    process_id for process_id in before if process_id in self._handles
                )
                total = sum(
                    int(
                        self._backend.win32process.GetProcessMemoryInfo(
                            self._handles[process_id]
                        )["WorkingSetSize"]
                    )
                    for process_id in sampled
                )
                after = self._process_ids()
                if sampled != after:
                    raise SafetyError("M10 Chromium process set changed during RSS sampling")
                self._peak_rss_bytes = max(self._peak_rss_bytes, total)
                self._sample_count += 1
                return
            except Exception as exc:
                last_error = exc
        raise SafetyError("M10 Chromium RSS sampling did not stabilize") from last_error

    def browser_started(self, browser: Any) -> None:
        self._session = browser.new_browser_cdp_session()
        self._sample()

    def checkpoint(self, browser: Any) -> None:
        del browser
        self._sample()

    def before_browser_close(self, browser: Any) -> None:
        del browser
        self._sample()
        if self._session is None:
            raise SafetyError("M10 Chromium CDP observer disappeared before close")
        self._session.detach()
        self._session = None
        self._detached = True

    def after_browser_close(self) -> None:
        self._after_close_observed = True
        pending = self._wait_for_process_release(set(self._handles))
        if pending:
            try:
                self._backend.win32job.TerminateJobObject(self._job, 1)
            except Exception:
                self.failed("browser-job-terminate", "JobTerminationFailed")
            else:
                # A failed page can keep a renderer alive after browser.close().
                # Forced Job termination is an allowed cleanup escalation, but it
                # only counts as complete after every captured process handle is
                # observed signalled.
                pending = self._wait_for_process_release(pending)
        self._processes_released = not pending
        for handle in self._handles.values():
            try:
                self._backend.close_handle(handle)
            except Exception:
                self._handles_released = False
        self._handles.clear()
        try:
            self._backend.close_handle(self._job)
            self._job = None
        except Exception:
            self._handles_released = False

    def _wait_for_process_release(self, pending: set[int]) -> set[int]:
        deadline = time.monotonic() + BROWSER_RELEASE_TIMEOUT_MS / 1000
        while pending and time.monotonic() < deadline:
            released: set[int] = set()
            for process_id in pending:
                try:
                    result = self._backend.win32event.WaitForSingleObject(
                        self._handles[process_id], 0
                    )
                except Exception:
                    continue
                if result == self._backend.win32event.WAIT_OBJECT_0:
                    released.add(process_id)
            pending -= released
            if pending:
                time.sleep(WAIT_SLICE_MS / 1000)
        return pending

    def abort(self) -> None:
        if self._handles:
            try:
                total = sum(
                    int(
                        self._backend.win32process.GetProcessMemoryInfo(handle)[
                            "WorkingSetSize"
                        ]
                    )
                    for handle in self._handles.values()
                    if not self._handle_is_signalled(handle)
                )
                self._peak_rss_bytes = max(self._peak_rss_bytes, total)
                self._sample_count += 1
            except Exception:
                self.failed("browser-abort-sample", "SamplingFailed")
        pending = set(self._handles)
        if self._job is not None:
            if pending:
                try:
                    self._backend.win32job.TerminateJobObject(self._job, 1)
                except Exception:
                    self.failed("browser-abort-job", "JobTerminationFailed")
                else:
                    pending = self._wait_for_process_release(pending)
            try:
                self._backend.close_handle(self._job)
            except Exception:
                self._handles_released = False
            self._job = None
        self._processes_released = not pending
        for handle in self._handles.values():
            try:
                self._backend.close_handle(handle)
            except Exception:
                self._handles_released = False
        self._handles.clear()
        self._after_close_observed = True
        self._detached = self._session is None

    def result(self, browser: ImportedEvidence) -> ObservedBrowserEvidence:
        values = self._result_values()
        return ObservedBrowserEvidence(browser=browser, **values)

    def interrupted(self, reason: str) -> ObservedBrowserInterrupted:
        if not self._driver_assigned:
            self.abort()
            return ObservedBrowserInterrupted(
                reason,
                peak_rss_mb=0.0,
                resource_sampling_complete=True,
                process_cleanup_complete=(
                    self._job is None and not self._handles and self._handles_released
                ),
                job_memory_limit_mb=self._max_job_memory_mb,
                job_memory_limit_enforced=(
                    self._process_limit_enforced and self._memory_limit_enforced
                ),
            )
        if not self._after_close_observed:
            self.abort()
        return ObservedBrowserInterrupted(reason, **self._result_values())

    def collection_error(self, error_type: str) -> ObservedBrowserCollectionError:
        if not self._after_close_observed:
            self.abort()
        values = self._result_values()
        if not self._driver_assigned:
            values.update(
                {
                    "peak_rss_mb": 0.0,
                    "resource_sampling_complete": True,
                    "process_cleanup_complete": (
                        self._job is None and not self._handles and self._handles_released
                    ),
                }
            )
        return ObservedBrowserCollectionError(error_type, **values)

    def _result_values(self) -> dict[str, Any]:
        sampling_complete = (
            self._driver_assigned
            and self._sample_count > 0
            and self._detached
            and not self._errors
        )
        cleanup_complete = (
            self._after_close_observed
            and self._processes_released
            and self._handles_released
        )
        return {
            "peak_rss_mb": (
                round(self._peak_rss_bytes / MEBIBYTE, 3)
                if self._sample_count > 0
                else None
            ),
            "resource_sampling_complete": sampling_complete,
            "process_cleanup_complete": cleanup_complete,
            "job_memory_limit_mb": self._max_job_memory_mb,
            "job_memory_limit_enforced": (
                self._process_limit_enforced and self._memory_limit_enforced
            ),
        }


def collect_observed_browser_evidence(
    plan: dict[str, Any],
    *,
    cancel_event: object | None = None,
    lifecycle_deadline: float | None = None,
    integrity_check: Callable[[], None] | None = None,
) -> ObservedBrowserEvidence:
    """Collect frozen M2 Evidence plus M10-only Chromium resource ownership facts."""

    require_windows_command_capability()
    observer = _ChromiumResourceObserver(
        _WindowsBackend(), plan["browser"]["max_job_memory_mb"]
    )
    try:
        browser = _collect_browser_evidence(
            plan,
            lifecycle_observer=observer,
            cancel_event=cancel_event,
            lifecycle_deadline=lifecycle_deadline,
            integrity_check=integrity_check,
        )
    except StopRequested as exc:
        raise observer.interrupted(exc.reason) from None
    except Exception as exc:
        raise observer.collection_error(type(exc).__name__) from exc
    return observer.result(browser)
