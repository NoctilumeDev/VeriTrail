from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from veritrail.acceptance_plan import seal_acceptance_plan
from veritrail.acceptance_reporting import create_acceptance_bundle
from veritrail.canonical import canonical_json_bytes
from veritrail.catalog import build_catalog, load_catalog_snapshot
from veritrail.cli import main
from veritrail.errors import SafetyError

from tests.support import acceptance_artifact, acceptance_plan


class AcceptanceReportingTests(unittest.TestCase):
    def _write_inputs(self, root: Path) -> tuple[Path, list[Path]]:
        plan = seal_acceptance_plan(acceptance_plan())
        plan_path = root / "acceptance-plan.json"
        plan_path.write_bytes(canonical_json_bytes(plan) + b"\n")
        evidence = [
            acceptance_artifact(
                plan, "api-spec", facts={"commit_sha": "candidate-001"}
            ),
            acceptance_artifact(
                plan, "render-spec", facts={"commit_sha": "candidate-001"}
            ),
        ]
        evidence_paths: list[Path] = []
        for index, artifact in enumerate(evidence, start=1):
            path = root / f"evidence-{index}.json"
            path.write_bytes(canonical_json_bytes(artifact.document) + b"\n")
            evidence_paths.append(path)
        return plan_path, evidence_paths

    def test_bundle_is_independent_hashed_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, evidence_paths = self._write_inputs(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            output = root / "acceptance-output"
            report = create_acceptance_bundle(
                plan=plan,
                evidence_paths=evidence_paths,
                output=output,
                acceptance_id="acceptance-001",
                execution_status="COMPLETED",
            )
            self.assertEqual("PASS", report["verdict"])
            self.assertEqual("ACCEPTANCE", report["report_kind"])
            self.assertTrue((output / "sealed-acceptance-plan.json").is_file())
            self.assertTrue((output / "acceptance-report.json").is_file())
            self.assertTrue((output / "acceptance-report.md").is_file())
            self.assertTrue((output / "acceptance-evidence-manifest.json").is_file())
            self.assertFalse((output / "report.json").exists())
            self.assertFalse((output / "bundle-manifest.json").exists())

            manifest = json.loads(
                (output / "acceptance-bundle-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual("ACCEPTANCE", manifest["bundle_kind"])
            for entry in manifest["files"]:
                content = (output / Path(entry["path"])).read_bytes()
                self.assertEqual(entry["size"], len(content))
                self.assertEqual(entry["sha256"], hashlib.sha256(content).hexdigest())

            markdown = (output / "acceptance-report.md").read_text(encoding="utf-8")
            self.assertIn("Verdict: `PASS`", markdown)
            self.assertIn("same\\-visible\\-commit", markdown)
            self.assertNotIn("Primary variable", markdown)
            self.assertNotIn("Baseline:", markdown)

            with self.assertRaisesRegex(SafetyError, "refusing to overwrite"):
                create_acceptance_bundle(
                    plan=plan,
                    evidence_paths=evidence_paths,
                    output=output,
                    acceptance_id="acceptance-002",
                    execution_status="COMPLETED",
                )

    def test_explicit_cli_round_trip_and_legacy_cli_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.json"
            sealed = root / "sealed.json"
            draft.write_bytes(canonical_json_bytes(acceptance_plan()) + b"\n")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(
                    [
                        "acceptance-seal",
                        "--plan",
                        str(draft),
                        "--output",
                        str(sealed),
                    ]
                )
            self.assertEqual(0, code)
            self.assertEqual("acceptance-seal", json.loads(stdout.getvalue())["command"])

            plan = json.loads(sealed.read_text(encoding="utf-8"))
            evidence_paths = []
            for spec_id in ("api-spec", "render-spec"):
                artifact = acceptance_artifact(
                    plan, spec_id, facts={"commit_sha": "candidate-001"}
                )
                path = root / f"{spec_id}.json"
                path.write_bytes(canonical_json_bytes(artifact.document) + b"\n")
                evidence_paths.append(path)
            output = root / "bundle"
            argv = [
                "acceptance-evaluate",
                "--plan",
                str(sealed),
                "--output",
                str(output),
                "--acceptance-id",
                "acceptance-cli",
            ]
            for path in evidence_paths:
                argv.extend(["--evidence", str(path)])
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(argv)
            self.assertEqual(0, code)
            self.assertEqual("PASS", json.loads(stdout.getvalue())["verdict"])

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = main(
                    ["seal", "--plan", str(draft), "--output", str(root / "legacy.json")]
                )
            self.assertEqual(2, code)
            self.assertIn("plan_kind", stderr.getvalue())

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = main(
                    [
                        "evaluate",
                        "--plan",
                        str(sealed),
                        "--output",
                        str(root / "legacy-bundle"),
                        "--run-id",
                        "legacy-acceptance",
                    ]
                )
            self.assertEqual(2, code)
            self.assertIn("plan_kind", stderr.getvalue())

    def test_manifest_does_not_retain_malformed_optional_digests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = seal_acceptance_plan(acceptance_plan())
            artifact = acceptance_artifact(
                plan, "api-spec", facts={"commit_sha": "candidate-001"}
            )
            document = json.loads(canonical_json_bytes(artifact.document))
            document["metadata"]["veritrail_observation"]["facts_digest"] = "not-a-digest"
            path = root / "malformed-metadata.json"
            path.write_bytes(canonical_json_bytes(document) + b"\n")

            report = create_acceptance_bundle(
                plan=plan,
                evidence_paths=[path],
                output=root / "bundle",
                acceptance_id="acceptance-malformed-metadata",
                execution_status="COMPLETED",
            )
            self.assertEqual("INCONCLUSIVE", report["verdict"])
            self.assertIsNone(report["evidence"][0]["facts_digest"])

    def test_legacy_catalog_marks_acceptance_directory_unsupported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, evidence_paths = self._write_inputs(root)
            bundle = root / "artifacts" / "acceptance-only"
            bundle.parent.mkdir()
            create_acceptance_bundle(
                plan=json.loads(plan_path.read_text(encoding="utf-8")),
                evidence_paths=evidence_paths,
                output=bundle,
                acceptance_id="acceptance-catalog",
                execution_status="COMPLETED",
            )
            catalog_root = root / "catalog"
            result = build_catalog(bundle.parent, catalog_root)
            self.assertEqual(0, result.run_count)
            self.assertEqual(1, result.issue_count)
            manifest, database = load_catalog_snapshot(catalog_root)
            self.assertEqual("COMPLETED_WITH_ISSUES", manifest["build_status"])
            self.assertGreater(len(database), 0)


if __name__ == "__main__":
    unittest.main()
