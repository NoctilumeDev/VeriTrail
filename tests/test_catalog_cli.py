from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from veritrail.cli import main
from veritrail.reporting import create_bundle

from tests.support import ROOT, sealed_example_plan


class CatalogCliTests(unittest.TestCase):
    def test_build_has_structured_sanitized_success_and_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            artifacts = base / "artifacts"
            artifacts.mkdir()
            create_bundle(
                plan=sealed_example_plan(),
                evidence_paths=[ROOT / "examples" / "minimal" / "evidence-pass.json"],
                output=artifacts / "run",
                run_id="cli-catalog-run",
                execution_status="COMPLETED",
            )
            output = base / "catalog"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "catalog-build",
                        "--artifacts",
                        str(artifacts),
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(0, code)
            payload = json.loads(stdout.getvalue())
            self.assertEqual("COMPLETED", payload["status"])
            self.assertEqual(1, payload["run_count"])
            self.assertNotIn(str(base), stdout.getvalue())

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(
                    [
                        "catalog-build",
                        "--artifacts",
                        str(artifacts),
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(2, code)
            error = json.loads(stderr.getvalue())["error"]
            self.assertEqual("CATALOG_OUTPUT_EXISTS", error["code"])
            self.assertNotIn(str(base), stderr.getvalue())

    def test_unexpected_build_error_is_exit_one_without_stack_or_path(self) -> None:
        stderr = io.StringIO()
        with patch("veritrail.cli.build_catalog", side_effect=RuntimeError("private path")):
            with redirect_stderr(stderr):
                code = main(
                    [
                        "catalog-build",
                        "--artifacts",
                        "ignored-artifacts",
                        "--output",
                        "ignored-output",
                    ]
                )
        self.assertEqual(1, code)
        error = json.loads(stderr.getvalue())["error"]
        self.assertEqual("CATALOG_INTERNAL_ERROR", error["code"])
        self.assertNotIn("private path", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
