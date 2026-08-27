from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from veritrail.atomic_publish import publish_staged_directory
from veritrail.catalog import (
    CatalogError,
    _build_catalog_for_staged_parent_publish,
    build_catalog,
    load_catalog_manifest,
)
from veritrail.cli import main
from veritrail.demo import create_first_run_demo
from veritrail.errors import SafetyError
from veritrail.local_api import CatalogApplication


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

            web = root / "web"
            web.mkdir()
            (web / "index.html").write_text(
                "<!doctype html><title>Workbench</title>", encoding="utf-8"
            )
            application = CatalogApplication(
                output / "catalog", output / "artifacts", web
            )
            try:
                self.assertEqual("READY", application.health()["status"])
                payload = application.catalog(page=1, page_size=10)
                self.assertEqual(2, payload["catalog"]["run_count"])
                self.assertEqual(0, payload["catalog"]["issue_count"])
                self.assertEqual(
                    ["demo-fail", "demo-pass"],
                    sorted(run["run_id"] for run in payload["runs"]),
                )
            finally:
                application.close()

            control_output = root / "control-catalog"
            control = build_catalog(output / "artifacts", control_output)
            control_manifest = load_catalog_manifest(control_output)
            self.assertEqual(catalog["catalog_id"], control.catalog_id)
            self.assertEqual(
                catalog["bundle_set_sha256"], control.bundle_set_sha256
            )
            self.assertEqual(
                catalog["database"]["logical_sha256"],
                control_manifest["database"]["logical_sha256"],
            )

            root_text = str(root)
            root_bytes = root_text.encode("utf-8")
            for path in output.rglob("*"):
                if path.is_file():
                    self.assertNotIn(root_bytes, path.read_bytes())
                    if path.suffix in {".json", ".md"}:
                        self.assertNotIn(root_text, path.read_text(encoding="utf-8"))

            with self.assertRaisesRegex(SafetyError, "refusing to overwrite"):
                create_first_run_demo(output)

            moved = root / "moved-demo"
            output.rename(moved)
            with self.assertRaises(CatalogError) as raised:
                CatalogApplication(
                    moved / "catalog", moved / "artifacts", web
                )
            self.assertEqual("ARTIFACT_ROOT_MISMATCH", raised.exception.code)

    def test_demo_staging_catalog_only_accepts_the_planned_final_artifact_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "first-run"
            web = root / "web"
            web.mkdir()
            (web / "index.html").write_text(
                "<!doctype html><title>Workbench</title>", encoding="utf-8"
            )
            observed_codes: list[str] = []

            def inspect_then_publish(stage: Path, target: Path) -> None:
                with self.assertRaises(CatalogError) as raised:
                    CatalogApplication(
                        stage / "catalog", stage / "artifacts", web
                    )
                observed_codes.append(raised.exception.code)
                publish_staged_directory(stage, target)

            with patch(
                "veritrail.demo.publish_staged_directory",
                side_effect=inspect_then_publish,
            ):
                create_first_run_demo(output)

            self.assertEqual(["ARTIFACT_ROOT_MISMATCH"], observed_codes)
            application = CatalogApplication(
                output / "catalog", output / "artifacts", web
            )
            try:
                self.assertEqual("READY", application.health()["status"])
            finally:
                application.close()

    def test_staged_catalog_producer_rejects_unrelated_or_existing_targets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = root / ".stage"
            artifacts = stage / "artifacts"
            artifacts.mkdir(parents=True)

            with self.assertRaises(CatalogError) as wrong_layout:
                _build_catalog_for_staged_parent_publish(
                    artifacts,
                    stage / "not-catalog",
                    stage_root=stage,
                    published_root=root / "final",
                )
            self.assertEqual(
                "CATALOG_STAGED_PUBLISH_INVALID", wrong_layout.exception.code
            )

            other_parent = root / "other"
            other_parent.mkdir()
            with self.assertRaises(CatalogError) as unrelated_target:
                _build_catalog_for_staged_parent_publish(
                    artifacts,
                    stage / "catalog",
                    stage_root=stage,
                    published_root=other_parent / "final",
                )
            self.assertEqual(
                "CATALOG_STAGED_PUBLISH_INVALID", unrelated_target.exception.code
            )

            existing_target = root / "existing"
            existing_target.mkdir()
            with self.assertRaises(CatalogError) as target_exists:
                _build_catalog_for_staged_parent_publish(
                    artifacts,
                    stage / "catalog",
                    stage_root=stage,
                    published_root=existing_target,
                )
            self.assertEqual(
                "CATALOG_STAGED_PUBLISH_TARGET_EXISTS", target_exists.exception.code
            )

    @unittest.skipUnless(os.name == "nt", "Win32 path normalization is Windows-only")
    def test_demo_rejects_final_names_that_win32_would_rewrite(self) -> None:
        for suffix in (".", " "):
            with self.subTest(suffix=repr(suffix)):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    with self.assertRaises(CatalogError) as raised:
                        create_first_run_demo(root / f"first-run{suffix}")

                    self.assertEqual(
                        "CATALOG_STAGED_PUBLISH_INVALID", raised.exception.code
                    )
                    self.assertFalse((root / "first-run").exists())
                    self.assertFalse(list(root.glob(".veritrail-demo-*")))
                    self.assertFalse(list(root.rglob(".veritrail-catalog-*")))

    def test_demo_failure_is_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "failed-demo"
            with patch(
                "veritrail.demo._build_catalog_for_staged_parent_publish",
                side_effect=RuntimeError("failure"),
            ):
                with self.assertRaisesRegex(RuntimeError, "failure"):
                    create_first_run_demo(output)
            self.assertFalse(output.exists())
            self.assertFalse(list(root.glob(".veritrail-demo-*")))

    def test_demo_outer_publication_failure_removes_both_staging_levels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "failed-publication"
            with patch(
                "veritrail.demo.publish_staged_directory",
                side_effect=RuntimeError("outer publication failed"),
            ):
                with self.assertRaisesRegex(RuntimeError, "outer publication failed"):
                    create_first_run_demo(output)
            self.assertFalse(output.exists())
            self.assertFalse(list(root.glob(".veritrail-demo-*")))
            self.assertFalse(list(root.rglob(".veritrail-catalog-*")))

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

    def test_demo_cli_sanitizes_unexpected_internal_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "final-demo"
            staging = root / ".veritrail-demo-private"
            failure = PermissionError(
                5,
                "rename blocked",
                str(staging),
                str(output),
            )
            stderr = StringIO()

            with patch(
                "veritrail.cli.create_first_run_demo", side_effect=failure
            ), redirect_stderr(stderr):
                result = main(["demo", "--output", str(output)])

            payload = json.loads(stderr.getvalue())
            self.assertEqual(1, result)
            self.assertEqual(
                {
                    "error": {
                        "code": "DEMO_INTERNAL_ERROR",
                        "message": "Demo generation encountered an unexpected internal error.",
                    }
                },
                payload,
            )
            self.assertNotIn(str(root), stderr.getvalue())
            self.assertNotIn(".veritrail-demo-", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
