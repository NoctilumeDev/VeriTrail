from __future__ import annotations

import threading


class StopRequested(Exception):
    """A cooperative lifecycle stop with a stable public reason."""

    def __init__(self, reason: str) -> None:
        if not isinstance(reason, str) or not reason:
            raise ValueError("stop reason must be a non-empty string")
        self.reason = reason
        super().__init__(reason)


class StopSignal:
    """Combine an external user event with one first-writer runtime reason."""

    def __init__(self, external_event: threading.Event | None = None) -> None:
        self._external_event = external_event
        self._event = threading.Event()
        self._lock = threading.Lock()
        self._reason: str | None = None

    def request(self, reason: str) -> bool:
        if not isinstance(reason, str) or not reason:
            raise ValueError("stop reason must be a non-empty string")
        with self._lock:
            if (
                self._external_event is not None
                and self._external_event.is_set()
                and reason != "USER_CANCELLED"
            ):
                return False
            if self._reason == "RESOURCE_MEMORY_SOFT_LIMIT" and reason == (
                "RESOURCE_MEMORY_HARD_LIMIT"
            ):
                self._reason = reason
                self._event.set()
                return True
            if reason == "USER_CANCELLED" and self._reason in {
                "RESOURCE_MEMORY_SOFT_LIMIT",
                "RESOURCE_MEMORY_HARD_LIMIT",
            }:
                self._reason = reason
                self._event.set()
                return True
            if self._reason is not None:
                return False
            self._reason = reason
            self._event.set()
            return True

    def is_set(self) -> bool:
        return self._event.is_set() or (
            self._external_event is not None and self._external_event.is_set()
        )

    def reason(self) -> str | None:
        if self._external_event is not None and self._external_event.is_set():
            return "USER_CANCELLED"
        with self._lock:
            reason = self._reason
        if reason is not None:
            return reason
        return None


def requested_stop_reason(signal: object | None) -> str | None:
    if signal is None:
        return None
    reason_reader = getattr(signal, "reason", None)
    if callable(reason_reader):
        reason = reason_reader()
        if reason is not None:
            return str(reason)
    is_set = getattr(signal, "is_set", None)
    if callable(is_set) and is_set():
        return "USER_CANCELLED"
    return None
