from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from veritrail.cli import main
from veritrail.errors import ValidationError
from veritrail.resources import collect_preflight_evidence

from tests.support import ROOT, browser_plan


def _write_plan(path: Path, plan: dict) -> None:
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")


class BrowserCliTests(unittest.TestCase):
    def test_older_plans_are_rejected_without_output(self) -> None:
        for relative in (
            Path("examples/minimal/plan.json"),
            Path("examples/preflight/plan-proceed.json"),
        ):
            with self.subTest(plan=relative.name), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "rejected"
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    code = main(
                        [
                            "browser-capture",
                            "--plan",
                            str(ROOT / relative),
                            "--run-id",
                            "m2-old-plan",
                            "--output",
                            str(output),
                        ]
                    )
                self.assertEqual(2, code)
                self.assertIn("schema_version '0.3'", stderr.getvalue())
                self.assertFalse(output.exists())

    def test_stop_escalation_does_not_start_browser(self) -> None:
        plan = browser_plan()
        plan["preflight"].update(
            sample_count=1,
            sampling_interval_ms=0,
            hard_breach_grace_samples=1,
            available_memory_soft_min_mb=1,
            available_memory_hard_min_mb=1,
            disk_free_hard_min_mb=1,
            collector_rss_hard_max_mb=512,
            observer_rss_delta_soft_max_mb=512,
            ports=[],
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path = root / "plan.json"
            output = root / "stopped"
            _write_plan(plan_path, plan)
            evidence = collect_preflight_evidence(plan, root)
            evidence["facts"]["decision"] = "STOP_ESCALATION"
            evidence["facts"]["decision_reasons"] = [
                {"code": "SYNTHETIC_SOFT_STOP", "severity": "SOFT"}
            ]
            with (
                patch("veritrail.cli.collect_preflight_evidence", return_value=evidence),
                patch("veritrail.cli.collect_browser_evidence") as browser_mock,
                redirect_stdout(io.StringIO()) as stdout,
            ):
                code = main(
                    [
                        "browser-capture",
                        "--plan",
                        str(plan_path),
                        "--run-id",
                        "m2-soft-stop",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(0, code)
            browser_mock.assert_not_called()
            result = json.loads(stdout.getvalue())
            self.assertFalse(result["browser_started"])
            self.assertEqual("PENDING", result["verdict"])
            self.assertFalse((output / "attachments").exists())

    def test_missing_browser_dependency_leaves_no_output_or_staging(self) -> None:
        plan = browser_plan()
        plan["preflight"].update(
            sample_count=1,
            sampling_interval_ms=0,
            hard_breach_grace_samples=1,
            available_memory_soft_min_mb=1,
            available_memory_hard_min_mb=1,
            disk_free_hard_min_mb=1,
            collector_rss_hard_max_mb=512,
            observer_rss_delta_soft_max_mb=512,
            ports=[],
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path = root / "plan.json"
            output = root / "missing-browser"
            _write_plan(plan_path, plan)
            with (
                patch(
                    "veritrail.cli.collect_browser_evidence",
                    side_effect=ValidationError(["synthetic missing browser"]),
                ),
                redirect_stderr(io.StringIO()) as stderr,
            ):
                code = main(
                    [
                        "browser-capture",
                        "--plan",
                        str(plan_path),
                        "--run-id",
                        "m2-missing-browser",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(2, code)
            self.assertIn("synthetic missing browser", stderr.getvalue())
            self.assertFalse(output.exists())
            self.assertEqual([], list(root.glob(".veritrail-*")))


if __name__ == "__main__":
    unittest.main()
