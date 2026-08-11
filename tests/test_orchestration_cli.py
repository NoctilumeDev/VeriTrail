from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from veritrail.catalog import build_catalog
from veritrail.cli import main
from veritrail.command_preview import build_command_preview
from veritrail.evidence import import_evidence_document
from veritrail.local_api import CatalogApplication
from veritrail.orchestration import collect_orchestrated_evidence, prepare_static_target
from veritrail.plan import seal_plan
from veritrail.resources import collect_preflight_evidence

from tests.support import ROOT, command_plan
from tests.test_browser_evidence import _browser_artifact
from tests.test_orchestration import _free_port, _runtime_plan, _write_site


def _write_plan(path: Path, plan: dict) -> None:
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")


class OrchestrationCliTests(unittest.TestCase):
    def _command_fixture(self, root: Path, *, mode: str = "echo") -> tuple[Path, Path, str]:
        _write_site(root)
        (root / "tests").mkdir()
        shutil.copy2(
            ROOT / "tests" / "fixtures" / "m9_process_helper.py",
            root / "tests" / "helper.py",
        )
        port = _free_port()
        runtime = _runtime_plan(port)
        plan = command_plan()
        for field in ("subject", "target", "preflight", "browser"):
            plan[field] = runtime[field]
        plan["command"]["subject_watch_roots"] = ["tests"]
        helper_mode = "marker" if mode == "drift" else mode
        plan["command"]["arguments"] = [
            {"literal": "tests/helper.py"},
            {"literal": "--mode"},
            {"literal": helper_mode},
        ]
        if mode == "sleep":
            plan["command"]["arguments"].extend(
                [{"literal": "--seconds"}, {"literal": "5"}]
            )
            plan["command"]["timeout_ms"] = 1000
            command_assertion = next(
                item for item in plan["assertions"] if item["evidence_type"] == "runtime.command"
            )
            command_assertion["path"] = "/facts/shell_used"
            command_assertion["expected"] = False
        elif mode == "drift":
            plan["command"]["arguments"].extend(
                [{"literal": "--marker"}, {"literal": "tests/changed.txt"}]
            )
        elif mode == "exit-code":
            plan["command"]["arguments"].extend(
                [{"literal": "--code"}, {"literal": "7"}]
            )
        elif mode == "overflow":
            plan["command"]["max_stdout_bytes"] = 1024
            command_assertion = next(
                item for item in plan["assertions"] if item["evidence_type"] == "runtime.command"
            )
            command_assertion["path"] = "/facts/shell_used"
            command_assertion["expected"] = False
        plan["baseline"]["fingerprint"] = prepare_static_target(plan, root).fingerprint
        sealed = seal_plan(plan)
        plan_path = root / "plan.json"
        _write_plan(plan_path, sealed)
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
        preview = build_command_preview(
            sealed,
            subject_root=root,
            tool_bindings_path=bindings,
        )
        return plan_path, bindings, preview["preview_sha256"]

    def test_older_plan_is_rejected_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "rejected"
            with redirect_stderr(io.StringIO()) as stderr:
                code = main(
                    [
                        "run",
                        "--plan",
                        str(ROOT / "examples" / "browser" / "plan.json"),
                        "--subject-root",
                        str(ROOT),
                        "--run-id",
                        "m5-old-plan",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(2, code)
            self.assertIn("schema_version '0.4'", stderr.getvalue())
            self.assertFalse(output.exists())

    def test_proceed_runs_target_and_stdout_does_not_persist_subject_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write_site(root)
            plan = _runtime_plan(_free_port())
            plan["baseline"]["fingerprint"] = prepare_static_target(plan, root).fingerprint
            plan_path = root / "plan.json"
            output = root / "bundle"
            _write_plan(plan_path, plan)

            def orchestrate(candidate: dict, subject_root: Path):
                return collect_orchestrated_evidence(
                    candidate,
                    subject_root,
                    browser_collector=lambda item: _browser_artifact(item),
                )

            with (
                patch("veritrail.cli.collect_orchestrated_evidence", side_effect=orchestrate),
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--run-id",
                        "m5-cli-pass",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(0, code)
            payload = json.loads(stdout.getvalue())
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("PASS", payload["verdict"])
            self.assertTrue(payload["cleanup_complete"])
            self.assertEqual("bundle", payload["output"])
            self.assertNotIn(str(root), stdout.getvalue())
            self.assertTrue((output / "bundle-manifest.json").is_file())

    def test_preflight_abort_and_stop_never_start_target(self) -> None:
        for decision, expected_status in (("ABORT", "ABORTED"), ("STOP_ESCALATION", "COMPLETED")):
            with self.subTest(decision=decision), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                _write_site(root)
                plan = _runtime_plan(_free_port())
                plan_path = root / "plan.json"
                output = root / "bundle"
                _write_plan(plan_path, plan)
                evidence = collect_preflight_evidence(plan, root)
                evidence["facts"]["decision"] = decision
                evidence["facts"]["decision_reasons"] = [
                    {
                        "code": "SYNTHETIC_RESOURCE_CONTROL",
                        "severity": "HARD" if decision == "ABORT" else "SOFT",
                    }
                ]
                with (
                    patch("veritrail.cli.collect_preflight_evidence", return_value=evidence),
                    patch("veritrail.cli.collect_orchestrated_evidence") as orchestrator,
                    redirect_stdout(io.StringIO()) as stdout,
                ):
                    code = main(
                        [
                            "run",
                            "--plan",
                            str(plan_path),
                            "--subject-root",
                            str(root),
                            "--run-id",
                            f"m5-{decision.lower()}",
                            "--output",
                            str(output),
                        ]
                    )
                self.assertEqual(0, code)
                orchestrator.assert_not_called()
                payload = json.loads(stdout.getvalue())
                self.assertEqual(expected_status, payload["execution_status"])
                self.assertEqual("PENDING", payload["verdict"])
                self.assertFalse(payload["target_started"])
                self.assertIsNone(payload["cleanup_complete"])

    def test_plan_v05_runs_approved_command_then_existing_target_bundle_chain(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, bindings, approval = self._command_fixture(root)
            artifacts = root / "artifacts"
            output = artifacts / "bundle"

            def orchestrate(candidate: dict, subject_root: Path):
                return collect_orchestrated_evidence(
                    candidate,
                    subject_root,
                    browser_collector=lambda item: _browser_artifact(item),
                )

            with (
                patch("veritrail.cli.collect_orchestrated_evidence", side_effect=orchestrate),
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-command",
                        approval,
                        "--run-id",
                        "m9-cli-pass",
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(0, code)
            payload = json.loads(stdout.getvalue())
            self.assertTrue(payload["command_started"])
            self.assertTrue(payload["command_cleanup_complete"])
            self.assertEqual("EXITED", payload["command_termination_reason"])
            self.assertTrue(payload["target_started"])
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("PASS", payload["verdict"])
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(
                [
                    "browser.session",
                    "runtime.command",
                    "runtime.orchestration",
                    "runtime.preflight",
                ],
                sorted(item["evidence_type"] for item in report["evidence"]),
            )
            self.assertTrue((output / "attachments" / "command" / "stdout.txt").is_file())
            encoded_bundle = "".join(
                path.read_text(encoding="utf-8", errors="ignore")
                for path in output.rglob("*")
                if path.is_file() and path.suffix != ".png"
            )
            self.assertNotIn(str(root), encoded_bundle)
            catalog = build_catalog(artifacts, root / "catalog")
            self.assertEqual("COMPLETED", catalog.status)
            self.assertEqual(1, catalog.run_count)
            self.assertEqual(0, catalog.issue_count)
            web = root / "web"
            web.mkdir()
            (web / "index.html").write_text("<!doctype html>", encoding="utf-8")
            application = CatalogApplication(root / "catalog", artifacts, web)
            catalog_run_id = application.catalog(1, 50)["runs"][0]["catalog_run_id"]
            _, _, _, content_type = application.bundle_file(
                catalog_run_id,
                "attachments/command/stdout.txt",
            )
            self.assertEqual("text/plain; charset=utf-8", content_type)

    def test_plan_v05_approval_mismatch_rejects_before_process_and_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, bindings, _ = self._command_fixture(root)
            output = root / "bundle"
            with (
                patch("veritrail.cli.collect_command_evidence") as command_collector,
                redirect_stderr(io.StringIO()) as stderr,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-command",
                        "0" * 64,
                        "--run-id",
                        "m9-approval-rejected",
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(2, code)
            command_collector.assert_not_called()
            self.assertIn("approved command digest", stderr.getvalue())
            self.assertFalse(output.exists())

    def test_plan_v05_timeout_is_aborted_pending_and_does_not_start_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, bindings, approval = self._command_fixture(root, mode="sleep")
            output = root / "bundle"
            with (
                patch("veritrail.cli.collect_orchestrated_evidence") as orchestrator,
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-command",
                        approval,
                        "--run-id",
                        "m9-timeout",
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(0, code)
            orchestrator.assert_not_called()
            payload = json.loads(stdout.getvalue())
            self.assertEqual("ABORTED", payload["execution_status"])
            self.assertEqual("PENDING", payload["verdict"])
            self.assertEqual("TIMEOUT", payload["command_termination_reason"])
            self.assertTrue(payload["command_cleanup_complete"])
            self.assertFalse(payload["target_started"])
            self.assertEqual([], list(root.glob(".veritrail-run-work-*")))

    def test_plan_v05_subject_drift_is_inconclusive_without_rollback_or_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, bindings, approval = self._command_fixture(root, mode="drift")
            output = root / "bundle"
            with (
                patch("veritrail.cli.collect_orchestrated_evidence") as orchestrator,
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-command",
                        approval,
                        "--run-id",
                        "m9-subject-drift",
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(0, code)
            orchestrator.assert_not_called()
            payload = json.loads(stdout.getvalue())
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("INCONCLUSIVE", payload["verdict"])
            self.assertFalse(payload["target_started"])
            self.assertTrue((root / "tests" / "changed.txt").is_file())
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertTrue(
                any(
                    item["code"] == "COMMAND_SUBJECT_FINAL_STATE_DRIFT"
                    for item in report["contamination"]
                )
            )

    def test_plan_v05_preflight_abort_never_resolves_or_runs_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, bindings, approval = self._command_fixture(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            evidence = collect_preflight_evidence(plan, root)
            evidence["facts"]["decision"] = "ABORT"
            evidence["facts"]["decision_reasons"] = [
                {"code": "SYNTHETIC_RESOURCE_CONTROL", "severity": "HARD"}
            ]
            output = root / "bundle"
            with (
                patch("veritrail.cli.collect_preflight_evidence", return_value=evidence),
                patch("veritrail.cli.resolve_command") as resolver,
                patch("veritrail.cli.collect_command_evidence") as command_collector,
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-command",
                        approval,
                        "--run-id",
                        "m9-preflight-abort",
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(0, code)
            resolver.assert_not_called()
            command_collector.assert_not_called()
            payload = json.loads(stdout.getvalue())
            self.assertEqual("ABORTED", payload["execution_status"])
            self.assertEqual("PENDING", payload["verdict"])
            self.assertFalse(payload["command_started"])
            evidence_types = {
                item["evidence_type"]
                for item in json.loads((output / "report.json").read_text(encoding="utf-8"))[
                    "evidence"
                ]
            }
            self.assertNotIn("runtime.command", evidence_types)

    def test_plan_v05_unexpected_exit_can_be_completed_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, bindings, approval = self._command_fixture(root, mode="exit-code")
            output = root / "bundle"
            with (
                patch("veritrail.cli.collect_orchestrated_evidence") as orchestrator,
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-command",
                        approval,
                        "--run-id",
                        "m9-unexpected-exit",
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(0, code)
            orchestrator.assert_not_called()
            payload = json.loads(stdout.getvalue())
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("FAIL", payload["verdict"])
            self.assertEqual("EXITED", payload["command_termination_reason"])
            self.assertFalse(payload["target_started"])

    def test_plan_v05_output_overflow_is_aborted_pending(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, bindings, approval = self._command_fixture(root, mode="overflow")
            output = root / "bundle"
            with (
                patch("veritrail.cli.collect_orchestrated_evidence") as orchestrator,
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(root),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-command",
                        approval,
                        "--run-id",
                        "m9-output-overflow",
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(0, code)
            orchestrator.assert_not_called()
            payload = json.loads(stdout.getvalue())
            self.assertEqual("ABORTED", payload["execution_status"])
            self.assertEqual("PENDING", payload["verdict"])
            self.assertEqual("STDOUT_LIMIT_EXCEEDED", payload["command_termination_reason"])
            self.assertTrue(payload["command_cleanup_complete"])


if __name__ == "__main__":
    unittest.main()
