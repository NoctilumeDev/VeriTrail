from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from veritrail.cli import main
from veritrail.comparison import ComparisonError, create_comparison_bundle
from veritrail.plan import seal_plan
from veritrail.reporting import create_bundle

from tests.support import ROOT, example_plan, sealed_example_plan


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class ComparisonTests(unittest.TestCase):
    def _bundle(
        self,
        root: Path,
        name: str,
        run_id: str,
        *,
        evidence: str = "evidence-pass.json",
        execution_status: str = "COMPLETED",
        plan: dict[str, object] | None = None,
    ) -> Path:
        output = root / name
        create_bundle(
            plan=plan or sealed_example_plan(),
            evidence_paths=[ROOT / "examples" / "minimal" / evidence],
            output=output,
            run_id=run_id,
            execution_status=execution_status,
        )
        return output

    def test_same_plan_independent_runs_match_without_overwriting_run_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "repeat-baseline")
            repeat = self._bundle(root, "repeat", "repeat-candidate")
            output = root / "comparison"

            result = create_comparison_bundle(
                baseline=baseline, repeat=repeat, output=output
            )
            comparison = _load(output / "comparison.json")

            self.assertEqual("MATCH", result.comparison_status)
            self.assertTrue(result.comparable)
            self.assertEqual([], comparison["differences"])
            self.assertEqual("PASS", comparison["sources"]["baseline"]["verdict"])
            self.assertEqual("PASS", comparison["sources"]["repeat"]["verdict"])
            self.assertEqual(
                "RERUN_SEMANTICS_MATCH", comparison["reasons"][0]["code"]
            )

    def test_pass_to_fail_is_drift_with_specific_semantic_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "drift-baseline")
            repeat = self._bundle(
                root,
                "repeat",
                "drift-repeat",
                evidence="evidence-fail.json",
            )
            output = root / "comparison"

            result = create_comparison_bundle(
                baseline=baseline, repeat=repeat, output=output
            )
            comparison = _load(output / "comparison.json")
            paths = {item["path"] for item in comparison["differences"]}

            self.assertEqual("DRIFT", result.comparison_status)
            self.assertTrue(result.comparable)
            self.assertIn("/verdict", paths)
            self.assertIn("/assertions/suite-completed-successfully/status", paths)
            self.assertIn("/assertions/suite-has-zero-failures/actual", paths)
            self.assertEqual("RERUN_SEMANTIC_DRIFT", comparison["reasons"][0]["code"])

    def test_different_plan_is_retained_as_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "plan-baseline")
            changed = example_plan()
            changed["plan_id"] = "m6-different-plan"
            changed["version"] = 2
            repeat = self._bundle(
                root,
                "repeat",
                "plan-repeat",
                plan=seal_plan(changed),
            )

            result = create_comparison_bundle(
                baseline=baseline, repeat=repeat, output=root / "comparison"
            )
            comparison = _load(root / "comparison" / "comparison.json")

            self.assertEqual("INCONCLUSIVE", result.comparison_status)
            self.assertFalse(result.comparable)
            self.assertIn(
                "PLAN_DIGEST_MISMATCH",
                {reason["code"] for reason in comparison["reasons"]},
            )

    def test_same_run_copy_and_incomplete_run_are_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "same-run")
            copied = root / "copied"
            shutil.copytree(baseline, copied)
            same_output = root / "same-comparison"

            same = create_comparison_bundle(
                baseline=baseline, repeat=copied, output=same_output
            )
            self.assertEqual("INCONCLUSIVE", same.comparison_status)
            self.assertEqual(
                "SAME_RUN_REUSED",
                _load(same_output / "comparison.json")["reasons"][0]["code"],
            )

            incomplete = self._bundle(
                root,
                "incomplete",
                "incomplete-run",
                execution_status="ABORTED",
            )
            incomplete_output = root / "incomplete-comparison"
            result = create_comparison_bundle(
                baseline=baseline, repeat=incomplete, output=incomplete_output
            )
            self.assertEqual("INCONCLUSIVE", result.comparison_status)
            self.assertIn(
                "RUN_NOT_COMPLETED",
                {
                    item["code"]
                    for item in _load(incomplete_output / "comparison.json")["reasons"]
                },
            )

    def test_same_inputs_generate_byte_identical_output_and_refuse_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "stable-baseline")
            repeat = self._bundle(root, "repeat", "stable-repeat")
            first = root / "first"
            second = root / "second"
            create_comparison_bundle(baseline=baseline, repeat=repeat, output=first)
            create_comparison_bundle(baseline=baseline, repeat=repeat, output=second)

            first_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in first.iterdir()
            }
            second_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in second.iterdir()
            }
            self.assertEqual(first_hashes, second_hashes)
            with self.assertRaisesRegex(ComparisonError, "拒绝覆盖"):
                create_comparison_bundle(baseline=baseline, repeat=repeat, output=first)

    def test_tampered_source_is_rejected_without_output_or_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "tamper-baseline")
            repeat = self._bundle(root, "repeat", "tamper-repeat")
            report = repeat / "report.json"
            report.write_bytes(report.read_bytes() + b" ")
            output = root / "comparison"

            with self.assertRaises(ComparisonError) as context:
                create_comparison_bundle(baseline=baseline, repeat=repeat, output=output)
            self.assertEqual("BUNDLE_SIZE_MISMATCH", context.exception.code)
            self.assertFalse(output.exists())
            self.assertFalse(list(root.glob(".veritrail-comparison-*")))

    def test_manifest_has_exactly_two_hashed_files_and_no_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "manifest-baseline")
            repeat = self._bundle(root, "repeat", "manifest-repeat")
            output = root / "comparison"
            create_comparison_bundle(baseline=baseline, repeat=repeat, output=output)

            manifest = _load(output / "comparison-manifest.json")
            self.assertEqual(
                ["comparison.json", "comparison.md"],
                [item["path"] for item in manifest["files"]],
            )
            for item in manifest["files"]:
                path = output / item["path"]
                self.assertEqual(path.stat().st_size, item["size"])
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])
            all_bytes = b"".join(path.read_bytes() for path in output.iterdir())
            self.assertNotIn(str(root).encode("utf-8"), all_bytes)

    def test_cli_success_and_sanitized_failure_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self._bundle(root, "baseline", "cli-baseline")
            repeat = self._bundle(root, "repeat", "cli-repeat")
            output = root / "comparison"
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "compare",
                        "--baseline",
                        str(baseline),
                        "--repeat",
                        str(repeat),
                        "--output",
                        str(output),
                    ]
                )
            payload = json.loads(stdout.getvalue())
            self.assertEqual(0, code)
            self.assertEqual("MATCH", payload["comparison_status"])
            self.assertEqual("comparison", payload["output"])

            stderr = StringIO()
            with redirect_stderr(stderr):
                failure = main(
                    [
                        "compare",
                        "--baseline",
                        str(root / "missing"),
                        "--repeat",
                        str(repeat),
                        "--output",
                        str(root / "never-created"),
                    ]
                )
            error = json.loads(stderr.getvalue())["error"]
            self.assertEqual(2, failure)
            self.assertEqual("SOURCE_BUNDLE_UNREADABLE", error["code"])
            self.assertNotIn(str(root), stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
