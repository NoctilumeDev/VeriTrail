from __future__ import annotations

import os
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from veritrail.windows_readiness import probe_owned_http_readiness
from veritrail.windows_service import OwnedServiceSession, OwnedServiceStartError
from veritrail.windows_job import _WindowsBackend

ROOT = Path(__file__).resolve().parents[1]


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
        candidate.bind(("127.0.0.1", 0))
        return int(candidate.getsockname()[1])


def _environment(temp_directory: Path) -> dict[str, str]:
    result = {"PYTHONDONTWRITEBYTECODE": "1"}
    for name in ("SYSTEMROOT", "WINDIR"):
        value = os.environ.get(name)
        if value:
            result[name] = value
    result["TEMP"] = str(temp_directory)
    result["TMP"] = str(temp_directory)
    return result


def _readiness(*, timeout_ms: int = 3_000) -> dict[str, object]:
    return {
        "adapter": "HTTP_GET_LOOPBACK_OWNED_PID",
        "path": "/health",
        "expected_status": 200,
        "attempt_timeout_ms": 250,
        "total_timeout_ms": timeout_ms,
        "interval_ms": 50,
        "consecutive_successes": 2,
        "max_response_bytes": 4096,
    }


@unittest.skipUnless(os.name == "nt", "M10 service lifecycle is Windows-only")
class WindowsServiceTests(unittest.TestCase):
    def _start(
        self,
        directory: Path,
        port: int,
        *arguments: str,
        max_stdout_bytes: int = 65_536,
    ) -> OwnedServiceSession:
        return OwnedServiceSession.start(
            node_id="fixture-node",
            executable=Path(sys.executable),
            arguments=("-m", "tests.fixtures.m10_service_helper", *arguments),
            working_directory=ROOT,
            environment=_environment(directory),
            port=port,
            max_stdout_bytes=max_stdout_bytes,
            max_stderr_bytes=65_536,
            max_processes=4,
            process_release_timeout_ms=3_000,
            port_release_timeout_ms=3_000,
            reader_shutdown_timeout_ms=3_000,
        )

    def test_descendant_listener_becomes_ready_and_job_cleanup_releases_port(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            port = _free_port()
            session = self._start(directory, port, "child-listener", str(port))
            readiness = probe_owned_http_readiness(session, _readiness())
            self.assertTrue(readiness.ready)
            self.assertEqual(2, sum(item.result == "SUCCESS" for item in readiness.attempts))
            self.assertTrue(all(item.listener_owner_in_job for item in readiness.attempts[-2:]))
            teardown = session.terminate()
            self.assertTrue(teardown.cleanup_complete)
            self.assertGreaterEqual(teardown.total_assigned_processes, 2)
            self.assertEqual(0, teardown.final_active_processes)
            self.assertTrue(teardown.port_free)

    def test_early_exit_and_never_ready_are_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            early_port = _free_port()
            early = self._start(directory, early_port, "early-exit", "23")
            early_readiness = probe_owned_http_readiness(early, _readiness())
            self.assertFalse(early_readiness.ready)
            self.assertEqual("NODE_EARLY_EXIT", early_readiness.error_type)
            self.assertTrue(early.terminate().cleanup_complete)

            timeout_port = _free_port()
            sleeping = self._start(directory, timeout_port, "sleep", "30")
            timeout = probe_owned_http_readiness(
                sleeping,
                _readiness(timeout_ms=500),
            )
            self.assertFalse(timeout.ready)
            self.assertEqual("READINESS_TIMEOUT", timeout.error_type)
            self.assertTrue(sleeping.terminate().cleanup_complete)

    def test_wildcard_listener_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            port = _free_port()
            session = self._start(
                directory,
                port,
                "serve",
                str(port),
                "--address",
                "0.0.0.0",
            )
            readiness = probe_owned_http_readiness(session, _readiness())
            self.assertFalse(readiness.ready)
            self.assertEqual("LISTENER_OWNERSHIP_MISMATCH", readiness.error_type)
            self.assertTrue(session.terminate().cleanup_complete)

    def test_external_listener_is_not_terminated_on_owner_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            port = _free_port()
            external = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "tests.fixtures.m10_service_helper",
                    "serve",
                    str(port),
                ],
                cwd=ROOT,
                env=_environment(directory),
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            try:
                for _ in range(60):
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                        if probe.connect_ex(("127.0.0.1", port)) == 0:
                            break
                    threading.Event().wait(0.05)
                else:
                    self.fail("external listener did not start")

                session = self._start(directory, port, "sleep", "30")
                readiness = probe_owned_http_readiness(session, _readiness())
                self.assertFalse(readiness.ready)
                self.assertEqual("LISTENER_OWNERSHIP_MISMATCH", readiness.error_type)
                teardown = session.terminate()
                self.assertFalse(teardown.cleanup_complete)
                self.assertEqual("PORT_RELEASE_TIMEOUT", teardown.error_type)
                self.assertIsNone(external.poll())
            finally:
                external.terminate()
                external.wait(timeout=5)

    def test_output_limit_stops_readiness_and_is_captured(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            port = _free_port()
            session = self._start(
                directory,
                port,
                "spam",
                "stdout",
                "4096",
                max_stdout_bytes=128,
            )
            readiness = probe_owned_http_readiness(session, _readiness())
            self.assertFalse(readiness.ready)
            self.assertEqual("STDOUT_LIMIT_EXCEEDED", readiness.error_type)
            teardown = session.terminate()
            self.assertTrue(teardown.stdout.overflowed)
            self.assertTrue(teardown.cleanup_complete)

    def test_assignment_and_resume_failures_never_execute_suspended_target(self) -> None:
        class FailingAssignmentBackend(_WindowsBackend):
            def assign_process_to_job(self, job: object, process: object) -> None:
                raise RuntimeError("injected assignment failure")

        class FailingResumeBackend(_WindowsBackend):
            def resume_thread(self, thread: object) -> int:
                raise RuntimeError("injected resume failure")

        cases = (
            (FailingAssignmentBackend(), "OWNERSHIP_ASSIGNMENT_FAILED", False),
            (FailingResumeBackend(), "TARGET_RESUME_FAILED", True),
        )
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            for index, (backend, error_type, assigned) in enumerate(cases):
                with self.subTest(error_type=error_type):
                    marker = directory / f"must-not-exist-{index}.txt"
                    with self.assertRaises(OwnedServiceStartError) as caught:
                        OwnedServiceSession.start(
                            node_id="fixture-node",
                            executable=Path(sys.executable),
                            arguments=(
                                str(
                                    ROOT
                                    / "tests"
                                    / "fixtures"
                                    / "m9_process_helper.py"
                                ),
                                "--mode",
                                "marker",
                                "--marker",
                                str(marker),
                            ),
                            working_directory=ROOT,
                            environment=_environment(directory),
                            port=_free_port(),
                            max_stdout_bytes=65_536,
                            max_stderr_bytes=65_536,
                            max_processes=4,
                            process_release_timeout_ms=3_000,
                            port_release_timeout_ms=3_000,
                            reader_shutdown_timeout_ms=3_000,
                            _backend=backend,
                        )
                    observation = caught.exception.observation
                    self.assertEqual(error_type, caught.exception.error_type)
                    self.assertTrue(observation.process_created)
                    self.assertEqual(assigned, observation.target_assigned)
                    self.assertFalse(observation.target_resumed)
                    self.assertTrue(observation.cleanup_complete)
                    self.assertFalse(marker.exists())

    def test_job_creation_failure_is_structured_before_process_creation(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory, mock.patch(
            "veritrail.windows_service._create_job",
            side_effect=RuntimeError("injected Job creation failure"),
        ):
            directory = Path(raw_directory)
            with self.assertRaises(OwnedServiceStartError) as caught:
                self._start(directory, _free_port(), "sleep", "30")
            observation = caught.exception.observation
            self.assertEqual("JOB_CREATION_FAILED", caught.exception.error_type)
            self.assertFalse(observation.process_created)
            self.assertTrue(observation.cleanup_complete)


if __name__ == "__main__":
    unittest.main()
