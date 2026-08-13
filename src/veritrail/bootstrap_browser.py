from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from veritrail.browser import _collect_browser_evidence
from veritrail.evidence import ImportedEvidence
from veritrail.errors import SafetyError
from veritrail.resources import MEBIBYTE
from veritrail.windows_job import (
    WAIT_SLICE_MS,
    _WindowsBackend,
    require_windows_command_capability,
)

MAX_BROWSER_PROCESSES = 64
BROWSER_RELEASE_TIMEOUT_MS = 3_000
PROCESS_SYNCHRONIZE = 0x00100000


@dataclass(frozen=True)
class ObservedBrowserEvidence:
    browser: ImportedEvidence
    peak_rss_mb: float | None
    resource_sampling_complete: bool
    process_cleanup_complete: bool


class _ChromiumResourceObserver:
    """Observe only Chromium processes identified by the owned CDP connection."""

    def __init__(self, backend: _WindowsBackend) -> None:
        self._backend = backend
        self._session: Any | None = None
        self._handles: dict[int, Any] = {}
        self._peak_rss_bytes = 0
        self._sample_count = 0
        self._errors: list[str] = []
        self._detached = False
        self._after_close_observed = False
        self._processes_released = False
        self._handles_released = True

    def failed(self, stage: str, error_type: str) -> None:
        code = f"{stage}:{error_type}"
        if code not in self._errors:
            self._errors.append(code)

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
        )
        for process_id in process_ids:
            if process_id not in self._handles:
                self._handles[process_id] = self._backend.win32api.OpenProcess(
                    access, False, process_id
                )

    def _sample(self) -> None:
        last_error: Exception | None = None
        for _ in range(3):
            try:
                before = self._process_ids()
                self._ensure_handles(before)
                total = sum(
                    int(
                        self._backend.win32process.GetProcessMemoryInfo(
                            self._handles[process_id]
                        )["WorkingSetSize"]
                    )
                    for process_id in before
                )
                after = self._process_ids()
                if before != after:
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
        deadline = time.monotonic() + BROWSER_RELEASE_TIMEOUT_MS / 1000
        pending = set(self._handles)
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
        self._processes_released = not pending
        for handle in self._handles.values():
            try:
                self._backend.close_handle(handle)
            except Exception:
                self._handles_released = False
        self._handles.clear()

    def result(self, browser: ImportedEvidence) -> ObservedBrowserEvidence:
        sampling_complete = (
            self._sample_count > 0 and self._detached and not self._errors
        )
        cleanup_complete = (
            self._after_close_observed
            and self._processes_released
            and self._handles_released
        )
        return ObservedBrowserEvidence(
            browser=browser,
            peak_rss_mb=(
                round(self._peak_rss_bytes / MEBIBYTE, 3)
                if self._sample_count > 0
                else None
            ),
            resource_sampling_complete=sampling_complete,
            process_cleanup_complete=cleanup_complete,
        )


def collect_observed_browser_evidence(
    plan: dict[str, Any],
) -> ObservedBrowserEvidence:
    """Collect frozen M2 Evidence plus M10-only Chromium resource ownership facts."""

    require_windows_command_capability()
    observer = _ChromiumResourceObserver(_WindowsBackend())
    browser = _collect_browser_evidence(plan, lifecycle_observer=observer)
    return observer.result(browser)
