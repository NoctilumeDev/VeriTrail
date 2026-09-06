from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from veritrail.bootstrap_browser import (
    ObservedBrowserCollectionError,
    ObservedBrowserInterrupted,
    _ChromiumResourceObserver,
)
from veritrail.errors import SafetyError


class _DriverBackend:
    def __init__(
        self,
        *,
        assignment_fails: bool = False,
        signal_after_terminate: bool = True,
    ) -> None:
        self.win32con = SimpleNamespace(
            PROCESS_QUERY_INFORMATION=0x0400,
            PROCESS_VM_READ=0x0010,
        )
        self.win32api = SimpleNamespace(OpenProcess=self.open_process)
        self.win32job = SimpleNamespace(
            IsProcessInJob=self.is_process_in_job,
            TerminateJobObject=self.terminate_job,
        )
        self.win32event = SimpleNamespace(
            WAIT_OBJECT_0=0,
            WaitForSingleObject=self.wait_for_single_object,
        )
        self.assignment_fails = assignment_fails
        self.signal_after_terminate = signal_after_terminate
        self.assigned = False
        self.closed: list[object] = []
        self.terminated: list[tuple[object, int]] = []

    def open_process(self, access: int, inherit: bool, process_id: int) -> object:
        self.opened = (access, inherit, process_id)
        return object()

    def is_process_in_job(self, handle: object, job: object) -> bool:
        del handle, job
        return self.assigned

    def assign_process_to_job(self, job: object, handle: object) -> None:
        del job, handle
        if self.assignment_fails:
            raise RuntimeError("synthetic assignment failure")
        self.assigned = True

    def close_handle(self, handle: object) -> None:
        self.closed.append(handle)

    def terminate_job(self, job: object, exit_code: int) -> None:
        self.terminated.append((job, exit_code))

    def wait_for_single_object(self, handle: object, timeout_ms: int) -> int:
        del handle, timeout_ms
        if self.signal_after_terminate and self.terminated:
            return self.win32event.WAIT_OBJECT_0
        return 258


class _FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += seconds


def _playwright_with_driver(process_id: int) -> SimpleNamespace:
    process = SimpleNamespace(pid=process_id)
    transport = SimpleNamespace(_proc=process)
    connection = SimpleNamespace(_transport=transport)
    implementation = SimpleNamespace(_connection=connection)
    return SimpleNamespace(_impl_obj=implementation)


class ChromiumResourceObserverTests(unittest.TestCase):
    def test_driver_is_assigned_before_browser_descendants_can_start(self) -> None:
        backend = _DriverBackend()
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]

        observer.playwright_started(_playwright_with_driver(3210))

        self.assertEqual((0x0400 | 0x0010 | 0x00100000 | 0x0100 | 0x0001, False, 3210), backend.opened)
        self.assertTrue(backend.assigned)
        self.assertTrue(observer._driver_assigned)
        self.assertIn(3210, observer._handles)

    def test_live_unassignable_driver_fails_closed_and_releases_handle(self) -> None:
        backend = _DriverBackend(assignment_fails=True)
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]

        with self.assertRaisesRegex(RuntimeError, "synthetic assignment failure"):
            observer.playwright_started(_playwright_with_driver(3211))

        self.assertFalse(observer._driver_assigned)
        self.assertNotIn(3211, observer._handles)
        self.assertEqual(1, len(backend.closed))

    def test_missing_driver_identity_is_rejected_before_browser_launch(self) -> None:
        backend = _DriverBackend()
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]

        with self.assertRaisesRegex(SafetyError, "driver identity is unavailable"):
            observer.playwright_started(SimpleNamespace())

        self.assertFalse(backend.assigned)

    def test_abort_releases_job_and_all_captured_process_handles(self) -> None:
        backend = _DriverBackend()
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]
        first = object()
        second = object()
        observer._handles = {1: first, 2: second}

        observer.abort()

        self.assertIsNone(observer._job)
        self.assertEqual({}, observer._handles)
        self.assertEqual(["owned-job", first, second], backend.closed)

    def test_interrupt_before_driver_assignment_releases_empty_job(self) -> None:
        backend = _DriverBackend()
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]

        interruption = observer.interrupted("USER_CANCELLED")

        self.assertIsInstance(interruption, ObservedBrowserInterrupted)
        self.assertEqual("USER_CANCELLED", interruption.reason)
        self.assertEqual(0.0, interruption.peak_rss_mb)
        self.assertTrue(interruption.resource_sampling_complete)
        self.assertTrue(interruption.process_cleanup_complete)
        self.assertIsNone(observer._job)
        self.assertEqual(["owned-job"], backend.closed)

    def test_collection_error_before_driver_assignment_releases_empty_job(self) -> None:
        backend = _DriverBackend()
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]

        failure = observer.collection_error("SafetyError")

        self.assertIsInstance(failure, ObservedBrowserCollectionError)
        self.assertEqual("SafetyError", failure.error_type)
        self.assertEqual(0.0, failure.peak_rss_mb)
        self.assertTrue(failure.resource_sampling_complete)
        self.assertTrue(failure.process_cleanup_complete)
        self.assertIsNone(observer._job)
        self.assertEqual(["owned-job"], backend.closed)

    def test_browser_release_escalation_shares_one_cleanup_deadline(self) -> None:
        backend = _DriverBackend(signal_after_terminate=False)
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]
        observer._handles = {1: object()}
        observer._session = SimpleNamespace(detach=lambda: None)
        clock = _FakeClock()

        with (
            patch(
                "veritrail.bootstrap_browser.time.monotonic",
                side_effect=clock.monotonic,
            ),
            patch(
                "veritrail.bootstrap_browser.time.sleep",
                side_effect=clock.sleep,
            ),
        ):
            observer.after_browser_close()

        self.assertLessEqual(clock.now, 3.05)
        self.assertEqual([("owned-job", 1)], backend.terminated)
        self.assertFalse(observer._processes_released)

    def test_browser_release_escalation_observes_terminated_processes(self) -> None:
        backend = _DriverBackend(signal_after_terminate=True)
        with patch(
            "veritrail.bootstrap_browser._create_job",
            return_value=("owned-job", False, True, True),
        ):
            observer = _ChromiumResourceObserver(backend, 512)  # type: ignore[arg-type]
        observer._handles = {1: object()}
        observer._session = SimpleNamespace(detach=lambda: None)
        clock = _FakeClock()

        with (
            patch(
                "veritrail.bootstrap_browser.time.monotonic",
                side_effect=clock.monotonic,
            ),
            patch(
                "veritrail.bootstrap_browser.time.sleep",
                side_effect=clock.sleep,
            ),
        ):
            observer.after_browser_close()

        self.assertLessEqual(clock.now, 0.1)
        self.assertEqual([("owned-job", 1)], backend.terminated)
        self.assertTrue(observer._processes_released)


if __name__ == "__main__":
    unittest.main()
