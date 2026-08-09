from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from veritrail.cli import main
from veritrail.evidence import import_evidence_document
from veritrail.orchestration import collect_orchestrated_evidence, prepare_static_target
from veritrail.resources import collect_preflight_evidence

from tests.support import ROOT
from tests.test_browser_evidence import _browser_artifact
from tests.test_orchestration import _free_port, _runtime_plan, _write_site


def _write_plan(path: Path, plan: dict) -> None:
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")


class OrchestrationCliTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
