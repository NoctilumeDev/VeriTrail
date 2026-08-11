from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from veritrail.command_execution import collect_command_evidence, sanitize_output
from veritrail.command_preview import resolve_command
from veritrail.evidence import import_evidence_document, verify_imported_evidence
from veritrail.errors import SafetyError, ValidationError
from veritrail.plan import seal_plan
from veritrail.windows_job import CapturedStream, OwnedProcessResult
from veritrail.verdict import evaluate

from tests.support import command_plan


@unittest.skipUnless(sys.platform == "win32", "M9 command execution is Windows-only")
class CommandExecutionTests(unittest.TestCase):
    helper_source = Path(__file__).parent / "fixtures" / "m9_process_helper.py"

    def _fixture(
        self,
        root: Path,
        *,
        arguments: list[dict] | None = None,
        max_watch_files: int = 2000,
    ):
        (root / "src").mkdir()
        (root / "src" / "subject.txt").write_text("stable", encoding="utf-8")
        (root / "tests").mkdir()
        shutil.copy2(self.helper_source, root / "tests" / "helper.py")
        plan = command_plan()
        plan["command"]["arguments"] = arguments or [
            {"literal": "tests/helper.py"},
            {"literal": "--mode"},
            {"literal": "echo"},
        ]
        plan["command"]["max_watch_files"] = max_watch_files
        sealed = seal_plan(plan)
        bindings = root / "tool-bindings.json"
        bindings.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "bindings": {
                        "python": {"executable": str(Path(sys.executable).resolve())}
                    },
                }
            ),
            encoding="utf-8",
        )
        resolved = resolve_command(
            sealed,
            subject_root=root,
            tool_bindings_path=bindings,
        )
        return sealed, bindings, resolved

    def _owned_result(self, reason: str) -> OwnedProcessResult:
        created = reason != "PROCESS_CREATE_FAILED"
        overflowed = reason == "STDOUT_LIMIT_EXCEEDED"
        forced = created and reason != "EXITED"
        empty = CapturedStream(
            content=b"",
            observed_bytes_lower_bound=0,
            stream_complete=created and not overflowed,
            overflowed=False,
            thread_stopped=True,
            error_type=None,
        )
        stdout = (
            CapturedStream(
                content=b"x" * 1024,
                observed_bytes_lower_bound=1025,
                stream_complete=False,
                overflowed=True,
                thread_stopped=True,
                error_type=None,
            )
            if overflowed
            else empty
        )
        return OwnedProcessResult(
            parent_in_job=True,
            process_created=created,
            target_assigned=created,
            target_resumed=created,
            exit_code=0 if reason == "EXITED" else 1 if created else None,
            termination_reason=reason,
            error_type="PROCESS_CREATE_FAILED" if not created else None,
            stdout=stdout,
            stderr=empty,
            active_process_limit=16,
            active_process_limit_enforced=created,
            process_limit_attempt_observation="NOT_PROVEN",
            total_assigned_processes=1 if created else 0,
            final_active_processes=0,
            job_limit_terminated_processes=0,
            forced_termination_requested=forced,
            forced_termination_processes_observed=1 if forced else 0,
            tree_released=True,
            handles_released=True,
            capture_threads_stopped=True,
            cleanup_complete=True,
            elapsed_ms=1.0,
        )

    def test_real_command_produces_strict_redacted_evidence_and_releases_run_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan, bindings, resolved = self._fixture(
                root,
                arguments=[
                    {"literal": "tests/helper.py"},
                    {"literal": "--mode"},
                    {"literal": "canary"},
                ],
            )

            result = collect_command_evidence(
                plan,
                resolved,
                tool_bindings_path=bindings,
                output_parent=root / "artifacts",
            )

            verify_imported_evidence(result.command)
            facts = result.command.document["facts"]
            self.assertEqual("COMPLETED", result.execution_status)
            self.assertTrue(result.continue_pipeline)
            self.assertTrue(facts["exit_expected"])
            self.assertTrue(facts["oneshot_quiescent"])
            self.assertFalse(facts["subject"]["final_state_drift_detected"])
            self.assertTrue(facts["cleanup_complete"])
            self.assertEqual(2, len(result.command.attachments))
            persisted = b"\n".join(
                attachment.content for attachment in result.command.attachments
            ).decode("utf-8")
            self.assertNotIn("ghp_12345678901234567890", persisted)
            self.assertNotIn("alice@example.test", persisted)
            self.assertNotIn("C:\\private", persisted)
            self.assertNotIn("unit-server", persisted)
            self.assertIn("[REDACTED_TOKEN]", persisted)
            self.assertGreater(facts["stdout"]["redaction_count"], 0)
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-run-work-*")))

            document_mutation = copy.deepcopy(result.command)
            document_mutation.document["facts"]["working_directory"] = "C:\\private"
            with self.assertRaisesRegex(ValidationError, "must remain relative"):
                verify_imported_evidence(document_mutation)
            attachment_mutation = copy.deepcopy(result.command)
            object.__setattr__(
                attachment_mutation.attachments[0],
                "content",
                b"\\\\unit-server\\private\\trace\n",
            )
            with self.assertRaisesRegex(ValidationError, "unredacted sensitive text"):
                verify_imported_evidence(attachment_mutation)

            runtime_drift = copy.deepcopy(result.command.document)
            runtime_drift["facts"]["working_directory"] = "src"
            drift_artifact = import_evidence_document(
                runtime_drift,
                "generated-command-drift.json",
                attachments=result.command.attachments,
            )
            verify_imported_evidence(drift_artifact)
            drift_verdict = evaluate(plan, [drift_artifact], "COMPLETED")
            self.assertEqual("INCONCLUSIVE", drift_verdict["verdict"])
            self.assertTrue(
                any(
                    item["code"] == "COMMAND_RUNTIME_POLICY_DRIFT"
                    for item in drift_verdict["contamination"]
                )
            )

    def test_typed_run_work_argument_is_created_then_removed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan, bindings, resolved = self._fixture(
                root,
                arguments=[
                    {"literal": "tests/helper.py"},
                    {"literal": "--mode"},
                    {"literal": "marker"},
                    {"literal": "--marker"},
                    {"run_work_path": ["nested", "result.txt"]},
                ],
            )

            result = collect_command_evidence(
                plan,
                resolved,
                tool_bindings_path=bindings,
                output_parent=root / "artifacts",
            )

            facts = result.command.document["facts"]
            self.assertTrue(result.continue_pipeline)
            self.assertTrue(facts["run_work_created"])
            self.assertTrue(facts["run_work_released"])
            self.assertFalse(facts["subject"]["final_state_drift_detected"])

    def test_cancel_output_limit_and_spawn_failure_keep_typed_statuses_and_cleanup(self) -> None:
        cases = (
            ("cancel", "CANCELLED", "ABORTED"),
            ("overflow", "STDOUT_LIMIT_EXCEEDED", "ABORTED"),
            ("spawn", "PROCESS_CREATE_FAILED", "ERROR"),
        )
        for name, expected_reason, expected_status in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                plan, bindings, resolved = self._fixture(root)
                plan = json.loads(json.dumps(plan))
                plan.pop("seal")
                if name == "overflow":
                    plan["command"]["max_stdout_bytes"] = 1024
                plan = seal_plan(plan)
                resolved = resolve_command(
                    plan,
                    subject_root=root,
                    tool_bindings_path=bindings,
                )
                process_result = self._owned_result(expected_reason)
                result = collect_command_evidence(
                    plan,
                    resolved,
                    tool_bindings_path=bindings,
                    output_parent=root / "artifacts",
                    process_runner=lambda **_: process_result,
                )

                verify_imported_evidence(result.command)
                facts = result.command.document["facts"]
                self.assertEqual(expected_reason, facts["termination_reason"])
                self.assertEqual(expected_status, result.execution_status)
                self.assertFalse(result.continue_pipeline)
                self.assertTrue(facts["cleanup_complete"])
                self.assertEqual([], list((root / "artifacts").glob(".veritrail-run-work-*")))

    def test_subject_final_state_drift_is_preserved_and_blocks_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan, bindings, resolved = self._fixture(
                root,
                arguments=[
                    {"literal": "tests/helper.py"},
                    {"literal": "--mode"},
                    {"literal": "marker"},
                    {"literal": "--marker"},
                    {"literal": "src/changed.txt"},
                ],
            )

            successful = self._owned_result("EXITED")

            def mutate_subject(**_):
                (root / "src" / "changed.txt").write_text("resumed", encoding="utf-8")
                return successful

            result = collect_command_evidence(
                plan,
                resolved,
                tool_bindings_path=bindings,
                output_parent=root / "artifacts",
                process_runner=mutate_subject,
            )

            facts = result.command.document["facts"]
            self.assertEqual("COMPLETED", result.execution_status)
            self.assertFalse(result.continue_pipeline)
            self.assertTrue(facts["subject"]["final_state_drift_detected"])
            self.assertEqual(1, facts["subject"]["diff_counts"]["added"])
            self.assertTrue((root / "src" / "changed.txt").is_file())

    def test_snapshot_limit_failure_never_creates_a_process_or_run_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan, bindings, resolved = self._fixture(root, max_watch_files=1)

            result = collect_command_evidence(
                plan,
                resolved,
                tool_bindings_path=bindings,
                output_parent=root / "artifacts",
            )

            facts = result.command.document["facts"]
            self.assertEqual("ERROR", result.execution_status)
            self.assertFalse(result.continue_pipeline)
            self.assertFalse(facts["process_created"])
            self.assertFalse(facts["run_work_created"])
            self.assertFalse(facts["subject"]["snapshot_complete"])
            self.assertTrue(facts["cleanup_complete"])

    def test_live_binding_drift_is_rejected_before_process_or_run_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan, bindings, resolved = self._fixture(root)
            copied_executable = root / "alternate-python.exe"
            shutil.copy2(Path(sys.executable).resolve(), copied_executable)
            bindings.write_text(
                json.dumps(
                    {
                        "schema_version": "0.1",
                        "bindings": {
                            "python": {"executable": str(copied_executable)}
                        },
                    }
                ),
                encoding="utf-8",
            )
            runner = Mock()

            with self.assertRaisesRegex(SafetyError, "preview drifted"):
                collect_command_evidence(
                    plan,
                    resolved,
                    tool_bindings_path=bindings,
                    output_parent=root / "artifacts",
                    process_runner=runner,
                )

            runner.assert_not_called()
            self.assertFalse((root / "artifacts").exists())

    def test_dual_pass_output_sanitizer_catches_boundary_secret_paths_and_controls(self) -> None:
        secret = b"prefix ghp_12345678901234567890\x00 C:\\private\\item\n"
        sanitized = sanitize_output(
            secret,
            replacements=[],
            chunk_bytes=12,
        )
        text = sanitized.content.decode()

        self.assertNotIn("ghp_12345678901234567890", text)
        self.assertNotIn("C:\\private", text)
        self.assertIn("[REDACTED_TOKEN]", text)
        self.assertIn("[REDACTED_ABSOLUTE_PATH]", text)
        self.assertIn("[CONTROL]", text)
        self.assertGreaterEqual(sanitized.redaction_count, 2)
        expanded = sanitize_output(
            ("1.1.1.1\n" * 100).encode(),
            replacements=[],
            max_persisted_bytes=64,
        )
        self.assertLessEqual(len(expanded.content), 64)
        expanded.content.decode("utf-8", errors="strict")


if __name__ == "__main__":
    unittest.main()
