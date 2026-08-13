from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock
from pathlib import Path

from veritrail.windows_job import (
    _PinnedLaunchPaths,
    _WindowsBackend,
    inspect_executable_identity,
    run_owned_process,
)


@unittest.skipUnless(os.name == "nt", "M9 ownership backend is Windows-only")
class WindowsJobTests(unittest.TestCase):
    helper = Path(__file__).parent / "fixtures" / "m9_process_helper.py"

    def _environment(self) -> dict[str, str]:
        return {
            "SYSTEMROOT": os.environ["SYSTEMROOT"],
            "WINDIR": os.environ["WINDIR"],
            "TEMP": tempfile.gettempdir(),
            "TMP": tempfile.gettempdir(),
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def _run(
        self,
        arguments: list[str],
        *,
        timeout_ms: int = 5_000,
        grace_ms: int = 300,
        stdout_limit: int = 1_048_576,
        max_processes: int = 4,
        max_job_memory_mb: int = 1024,
        expected_executable_identity: dict[str, object] | None = None,
        backend: _WindowsBackend | None = None,
        cancel_event: threading.Event | None = None,
    ):
        return run_owned_process(
            executable=Path(sys.executable).resolve(),
            arguments=[str(self.helper.resolve()), *arguments],
            working_directory=Path.cwd().resolve(),
            environment=self._environment(),
            timeout_ms=timeout_ms,
            descendant_exit_grace_ms=grace_ms,
            max_stdout_bytes=stdout_limit,
            max_stderr_bytes=1_048_576,
            max_processes=max_processes,
            max_job_memory_mb=max_job_memory_mb,
            expected_executable_identity=expected_executable_identity,
            subject_root=Path.cwd().resolve(),
            cancel_event=cancel_event,
            _backend=backend,
        )

    def test_suspended_assignment_captures_both_streams_and_releases_tree(self) -> None:
        result = self._run(["--mode", "echo"])

        self.assertTrue(result.process_created)
        self.assertTrue(result.target_assigned)
        self.assertTrue(result.target_resumed)
        self.assertEqual(0, result.exit_code)
        self.assertEqual("EXITED", result.termination_reason)
        self.assertEqual(["stdout-ok"], result.stdout.content.decode().splitlines())
        self.assertEqual(["stderr-ok"], result.stderr.content.decode().splitlines())
        self.assertTrue(result.stdout.stream_complete)
        self.assertTrue(result.stderr.stream_complete)
        self.assertTrue(result.active_process_limit_enforced)
        self.assertEqual(1024, result.job_memory_limit_mb)
        self.assertTrue(result.job_memory_limit_enforced)
        self.assertEqual("NOT_PROVEN", result.process_limit_attempt_observation)
        self.assertFalse(result.forced_termination_requested)
        self.assertEqual(0, result.final_active_processes)
        self.assertTrue(result.cleanup_complete)

    def test_executable_identity_drift_stops_before_resume_and_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "must-not-exist.txt"
            result = self._run(
                ["--mode", "marker", "--marker", str(marker)],
                expected_executable_identity={"sha256": "0" * 64},
            )

            self.assertEqual("LAUNCH_IDENTITY_DRIFT", result.termination_reason)
            self.assertFalse(result.process_created)
            self.assertFalse(marker.exists())
            self.assertTrue(result.job_memory_limit_enforced)
            self.assertTrue(result.cleanup_complete)

    def test_pinned_launch_identity_is_read_from_the_held_handle(self) -> None:
        executable = Path(sys.executable).resolve()
        expected = inspect_executable_identity(executable)
        backend = _WindowsBackend()
        original_create_file = backend.win32file.CreateFile
        executable_opens = 0

        def counted_create_file(path, *args):
            nonlocal executable_opens
            if Path(path) == executable:
                executable_opens += 1
            return original_create_file(path, *args)

        with mock.patch.object(
            backend.win32file, "CreateFile", side_effect=counted_create_file
        ):
            with _PinnedLaunchPaths(
                executable=executable,
                expected_executable_identity=expected,
                working_directory=Path.cwd().resolve(),
                subject_root=Path.cwd().resolve(),
                backend=backend,
            ):
                self.assertEqual(1, executable_opens)

    def test_windows_argv_quoting_preserves_empty_spaces_quotes_and_backslashes(self) -> None:
        values = ["", "two words", 'quote"inside', "trailing\\", "plain"]
        result = self._run(["--mode", "argv", *values])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(values, json.loads(result.stdout.content.decode()))
        self.assertTrue(result.cleanup_complete)

    def test_assignment_failure_terminates_suspended_target_before_marker(self) -> None:
        class FailingAssignmentBackend(_WindowsBackend):
            def assign_process_to_job(self, job, process) -> None:
                raise RuntimeError("synthetic assignment failure")

        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "must-not-exist.txt"
            result = self._run(
                ["--mode", "marker", "--marker", str(marker)],
                backend=FailingAssignmentBackend(),
            )

            self.assertTrue(result.process_created)
            self.assertFalse(result.target_assigned)
            self.assertFalse(result.target_resumed)
            self.assertEqual("OWNERSHIP_ASSIGNMENT_FAILED", result.termination_reason)
            self.assertFalse(marker.exists())
            self.assertTrue(result.forced_termination_requested)
            self.assertEqual(1, result.forced_termination_processes_observed)
            self.assertTrue(result.tree_released)
            self.assertTrue(result.cleanup_complete)

    def test_resume_failure_reaps_assigned_suspended_target_before_marker(self) -> None:
        class FailingResumeBackend(_WindowsBackend):
            def resume_thread(self, thread) -> int:
                raise RuntimeError("synthetic resume failure")

        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "must-not-exist.txt"
            result = self._run(
                ["--mode", "marker", "--marker", str(marker)],
                backend=FailingResumeBackend(),
            )

            self.assertTrue(result.process_created)
            self.assertTrue(result.target_assigned)
            self.assertFalse(result.target_resumed)
            self.assertEqual("TARGET_RESUME_FAILED", result.termination_reason)
            self.assertFalse(marker.exists())
            self.assertTrue(result.forced_termination_requested)
            self.assertGreaterEqual(result.forced_termination_processes_observed, 1)
            self.assertTrue(result.cleanup_complete)

    def test_timeout_terminates_only_the_owned_job(self) -> None:
        result = self._run(["--mode", "sleep", "--seconds", "5"], timeout_ms=1_000)

        self.assertEqual("TIMEOUT", result.termination_reason)
        self.assertTrue(result.target_resumed)
        self.assertTrue(result.forced_termination_requested)
        self.assertGreaterEqual(result.forced_termination_processes_observed, 1)
        self.assertEqual(0, result.final_active_processes)
        self.assertTrue(result.cleanup_complete)

    def test_stdin_is_closed_and_returns_immediate_eof(self) -> None:
        result = self._run(["--mode", "stdin-eof"])

        self.assertEqual("EXITED", result.termination_reason)
        self.assertEqual(["eof"], result.stdout.content.decode().splitlines())
        self.assertTrue(result.cleanup_complete)

    def test_active_process_limit_is_enforced_without_claiming_attempt_observation(self) -> None:
        result = run_owned_process(
            executable=Path(sys._base_executable).resolve(),
            arguments=[
                str(self.helper.resolve()),
                "--mode",
                "spawn-at-limit",
                "--seconds",
                "1",
            ],
            working_directory=Path.cwd().resolve(),
            environment=self._environment(),
            timeout_ms=5_000,
            descendant_exit_grace_ms=300,
            max_stdout_bytes=1_048_576,
            max_stderr_bytes=1_048_576,
            max_processes=1,
        )

        self.assertEqual("EXITED", result.termination_reason)
        self.assertEqual(["spawn-denied"], result.stdout.content.decode().splitlines())
        self.assertGreaterEqual(result.total_assigned_processes, 1)
        self.assertTrue(result.active_process_limit_enforced)
        self.assertEqual("NOT_PROVEN", result.process_limit_attempt_observation)
        self.assertTrue(result.cleanup_complete)

    def test_pre_signalled_cancel_event_terminates_owned_job(self) -> None:
        cancel = threading.Event()
        cancel.set()
        result = self._run(
            ["--mode", "sleep", "--seconds", "5"],
            cancel_event=cancel,
        )

        self.assertEqual("CANCELLED", result.termination_reason)
        self.assertEqual(0, result.final_active_processes)
        self.assertTrue(result.cleanup_complete)

    def test_unrelated_same_executable_process_is_not_terminated(self) -> None:
        external = subprocess.Popen(
            [
                sys._base_executable,
                str(self.helper.resolve()),
                "--mode",
                "sleep",
                "--seconds",
                "10",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        try:
            result = self._run(["--mode", "echo"])

            self.assertEqual("EXITED", result.termination_reason)
            self.assertIsNone(external.poll())
            self.assertTrue(result.cleanup_complete)
        finally:
            if external.poll() is None:
                external.terminate()
            external.wait(timeout=5)

    def test_create_failure_releases_empty_job_and_pipe_handles(self) -> None:
        missing = Path.cwd().resolve() / "missing-veritrail-command.exe"
        result = run_owned_process(
            executable=missing,
            arguments=["--not-run"],
            working_directory=Path.cwd().resolve(),
            environment=self._environment(),
            timeout_ms=1_000,
            descendant_exit_grace_ms=100,
            max_stdout_bytes=1024,
            max_stderr_bytes=1024,
            max_processes=1,
        )

        self.assertFalse(result.process_created)
        self.assertFalse(result.target_resumed)
        self.assertEqual("PROCESS_CREATE_FAILED", result.termination_reason)
        self.assertEqual(0, result.final_active_processes)
        self.assertTrue(result.cleanup_complete)

    def test_long_lived_descendant_is_detected_and_reaped_after_grace(self) -> None:
        result = self._run(
            ["--mode", "spawn-child", "--seconds", "5"],
            timeout_ms=5_000,
            grace_ms=200,
        )

        self.assertEqual("DESCENDANT_GRACE_EXPIRED", result.termination_reason)
        self.assertGreaterEqual(result.total_assigned_processes, 2)
        self.assertEqual(0, result.final_active_processes)
        self.assertTrue(result.cleanup_complete)

    def test_stdout_overflow_terminates_job_and_keeps_bounded_prefix(self) -> None:
        result = self._run(
            ["--mode", "overflow", "--seconds", "5"],
            stdout_limit=1024,
        )

        self.assertEqual("STDOUT_LIMIT_EXCEEDED", result.termination_reason)
        self.assertTrue(result.stdout.overflowed)
        self.assertGreater(result.stdout.observed_bytes_lower_bound, 1024)
        self.assertEqual(1024, len(result.stdout.content))
        self.assertFalse(result.stdout.stream_complete)
        self.assertTrue(result.cleanup_complete)

    def test_descendant_output_overflow_takes_priority_over_grace_expiry(self) -> None:
        result = self._run(
            ["--mode", "spawn-child-overflow", "--seconds", "5"],
            grace_ms=2_000,
            stdout_limit=1024,
        )

        self.assertEqual("STDOUT_LIMIT_EXCEEDED", result.termination_reason)
        self.assertTrue(result.stdout.overflowed)
        self.assertEqual(0, result.final_active_processes)
        self.assertTrue(result.cleanup_complete)


if __name__ == "__main__":
    unittest.main()
