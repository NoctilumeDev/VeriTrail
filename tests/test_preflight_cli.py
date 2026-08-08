from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from veritrail.cli import main

from tests.support import ROOT


class PreflightCliTests(unittest.TestCase):
    def test_plan_v01_is_rejected_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "rejected"
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(
                    [
                        "preflight",
                        "--plan",
                        str(ROOT / "examples" / "minimal" / "plan.json"),
                        "--run-id",
                        "m1-v01-rejected",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(2, code)
            self.assertIn("schema_version '0.2'", stderr.getvalue())
            self.assertFalse(output.exists())

    def test_hard_preflight_creates_aborted_pending_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "hard-abort"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "preflight",
                        "--plan",
                        str(ROOT / "examples" / "preflight" / "plan-abort.json"),
                        "--run-id",
                        "m1-hard-abort",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(0, code)
            command_result = json.loads(stdout.getvalue())
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            markdown = (output / "report.md").read_text(encoding="utf-8")
            self.assertEqual("ABORT", command_result["resource_decision"])
            self.assertEqual("ABORTED", report["execution_status"])
            self.assertEqual("PENDING", report["verdict"])
            self.assertEqual("ABORT", report["evidence"][0]["summary"]["resource_decision"])
            self.assertIn("decision: ABORT", markdown)

    def test_existing_output_is_rejected_before_collection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "existing"
            output.mkdir()
            marker = output / "keep.txt"
            marker.write_text("preserve", encoding="utf-8")
            with redirect_stderr(io.StringIO()):
                code = main(
                    [
                        "preflight",
                        "--plan",
                        str(ROOT / "examples" / "preflight" / "plan-proceed.json"),
                        "--run-id",
                        "m1-existing-output",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(2, code)
            self.assertEqual("preserve", marker.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
