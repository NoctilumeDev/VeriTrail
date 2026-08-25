from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from veritrail.catalog import load_catalog_manifest
from veritrail.cli import main
from veritrail.demo import create_first_run_demo
from veritrail.errors import SafetyError


class FirstRunDemoTests(unittest.TestCase):
    def test_demo_creates_pass_fail_and_catalog_without_repository_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "first-run"
            summary = create_first_run_demo(output)

            self.assertEqual("PASS", summary["runs"]["pass"]["verdict"])
            self.assertEqual("FAIL", summary["runs"]["fail"]["verdict"])
            self.assertEqual("SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE", summary["boundary"])
            self.assertEqual(
                summary["plan_sha256"],
                json.loads(
                    (output / "artifacts" / "demo-pass" / "report.json").read_text(
                        encoding="utf-8"
                    )
                )["plan"]["sha256"],
            )
            self.assertEqual(
                summary["plan_sha256"],
                json.loads(
                    (output / "artifacts" / "demo-fail" / "report.json").read_text(
                        encoding="utf-8"
                    )
                )["plan"]["sha256"],
            )
            catalog = load_catalog_manifest(output / "catalog")
            self.assertEqual(2, catalog["run_count"])
            self.assertEqual(0, catalog["issue_count"])

            root_text = str(root)
            root_bytes = root_text.encode("utf-8")
            for path in output.rglob("*"):
                if path.is_file():
                    self.assertNotIn(root_bytes, path.read_bytes())
                    if path.suffix in {".json", ".md"}:
                        self.assertNotIn(root_text, path.read_text(encoding="utf-8"))

            with self.assertRaisesRegex(SafetyError, "refusing to overwrite"):
                create_first_run_demo(output)

    def test_demo_failure_is_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "failed-demo"
            with patch("veritrail.demo.build_catalog", side_effect=RuntimeError("failure")):
                with self.assertRaisesRegex(RuntimeError, "failure"):
                    create_first_run_demo(output)
            self.assertFalse(output.exists())
            self.assertFalse(list(root.glob(".veritrail-demo-*")))

    def test_demo_cli_reports_verdicts_catalog_and_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "cli-demo"
            stdout = StringIO()
            with redirect_stdout(stdout):
                result = main(["demo", "--output", str(output)])
            payload = json.loads(stdout.getvalue())
            self.assertEqual(0, result)
            self.assertEqual("demo", payload["command"])
            self.assertEqual("PASS", payload["pass_verdict"])
            self.assertEqual("FAIL", payload["fail_verdict"])
            self.assertEqual(2, payload["catalog_run_count"])
            self.assertEqual("SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE", payload["boundary"])
            self.assertTrue((output / "demo-summary.json").is_file())


if __name__ == "__main__":
    unittest.main()
