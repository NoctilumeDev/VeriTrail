from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any

from veritrail.cli import main
from veritrail.pairing import (
    PairingError,
    create_paired_analysis_bundle,
    seal_pairing_plan,
    validate_pairing_plan,
    write_sealed_pairing_plan,
)
from veritrail.plan import plan_digest, seal_plan
from veritrail.reporting import create_bundle

from tests.support import ROOT, artifact


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _example(name: str) -> dict[str, Any]:
    return _json(ROOT / "examples" / "pairing" / name)


class PairingTests(unittest.TestCase):
    def _create_group(
        self,
        root: Path,
        *,
        treatment_matches_baseline: bool = False,
        negative_has_effect: bool = False,
        treatment_plan: dict[str, Any] | None = None,
        incomplete_role: str | None = None,
    ) -> tuple[Path, dict[str, Path]]:
        plans = {
            "BASELINE": seal_plan(_example("plan-baseline.json")),
            "TREATMENT": treatment_plan or seal_plan(_example("plan-treatment.json")),
            "RESTORED_BASELINE": seal_plan(_example("plan-baseline.json")),
            "NEGATIVE_CONTROL": seal_plan(_example("plan-negative-control.json")),
        }
        evidence = {
            "BASELINE": artifact(
                observed_variables={
                    "experiment_condition": "nominal",
                    "python_major_minor": "3.10",
                }
            ),
            "TREATMENT": artifact(
                suite_passed=treatment_matches_baseline,
                failures=0 if treatment_matches_baseline else 1,
                observed_variables={
                    "experiment_condition": "forced_failure",
                    "python_major_minor": "3.10",
                },
            ),
            "RESTORED_BASELINE": artifact(
                observed_variables={
                    "experiment_condition": "nominal",
                    "python_major_minor": "3.10",
                }
            ),
            "NEGATIVE_CONTROL": artifact(
                suite_passed=not negative_has_effect,
                failures=1 if negative_has_effect else 0,
                observed_variables={
                    "experiment_condition": "negative_control",
                    "python_major_minor": "3.10",
                },
            ),
        }
        runs: dict[str, Path] = {}
        for role in ("BASELINE", "TREATMENT", "RESTORED_BASELINE", "NEGATIVE_CONTROL"):
            output = root / role.lower()
            create_bundle(
                plan=plans[role],
                evidence_paths=[],
                output=output,
                run_id=f"pairing-{role.lower()}",
                execution_status="ABORTED" if role == incomplete_role else "COMPLETED",
                generated_evidence=[evidence[role]],
            )
            runs[role] = output
            time.sleep(0.002)
        pairing = _example("pairing-plan.json")
        pairing["roles"]["TREATMENT"]["plan_sha256"] = plans["TREATMENT"]["seal"]["digest"]
        pairing_path = root / "sealed-pairing.json"
        write_sealed_pairing_plan(pairing_path, seal_pairing_plan(pairing))
        return pairing_path, runs

    def _analyze(self, root: Path, pairing: Path, runs: dict[str, Path], name: str = "analysis"):
        return create_paired_analysis_bundle(
            pairing_plan_path=pairing,
            baseline=runs["BASELINE"],
            treatment=runs["TREATMENT"],
            restored_baseline=runs["RESTORED_BASELINE"],
            negative_control=runs["NEGATIVE_CONTROL"],
            output=root / name,
        )

    def test_pairing_plan_seal_and_role_constraints(self) -> None:
        plan = _example("pairing-plan.json")
        validate_pairing_plan(plan)
        sealed = seal_pairing_plan(plan)
        self.assertEqual(64, len(sealed["seal"]["digest"]))

        broken = copy.deepcopy(plan)
        broken["roles"]["RESTORED_BASELINE"]["primary_value"] = "not-restored"
        with self.assertRaises(PairingError) as context:
            validate_pairing_plan(broken)
        self.assertEqual("PAIRING_PLAN_INVALID", context.exception.code)

        no_effect = copy.deepcopy(plan)
        for outcome in no_effect["outcomes"]:
            outcome["expected_actual"]["TREATMENT"] = outcome["expected_actual"]["BASELINE"]
        with self.assertRaisesRegex(PairingError, "treatment effect"):
            validate_pairing_plan(no_effect)

    def test_supported_four_role_group_preserves_source_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root)
            result = self._analyze(root, pairing, runs)
            analysis = _json(root / "analysis" / "paired-analysis.json")

            self.assertEqual("SUPPORTED", result.analysis_status)
            self.assertTrue(result.attributable)
            self.assertEqual("PAIRED_EFFECT_SUPPORTED", analysis["reasons"][0]["code"])
            self.assertEqual("PASS", analysis["sources"]["BASELINE"]["verdict"])
            self.assertEqual("FAIL", analysis["sources"]["TREATMENT"]["verdict"])
            self.assertEqual("PASS", analysis["sources"]["RESTORED_BASELINE"]["verdict"])
            self.assertEqual("PASS", analysis["sources"]["NEGATIVE_CONTROL"]["verdict"])
            self.assertTrue(
                all(
                    observation["matches"]
                    for outcome in analysis["outcomes"]
                    for observation in outcome["roles"].values()
                )
            )

    def test_treatment_without_effect_is_contradicted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root, treatment_matches_baseline=True)
            result = self._analyze(root, pairing, runs)
            analysis = _json(root / "analysis" / "paired-analysis.json")

            self.assertEqual("CONTRADICTED", result.analysis_status)
            self.assertTrue(result.attributable)
            self.assertEqual("TREATMENT_EFFECT_CONTRADICTED", analysis["reasons"][0]["code"])

    def test_negative_control_effect_and_incomplete_run_are_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root, negative_has_effect=True)
            result = self._analyze(root, pairing, runs, "negative-analysis")
            analysis = _json(root / "negative-analysis" / "paired-analysis.json")
            self.assertEqual("INCONCLUSIVE", result.analysis_status)
            self.assertFalse(result.attributable)
            self.assertIn(
                "NEGATIVE_CONTROL_EFFECT", {item["code"] for item in analysis["reasons"]}
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root, incomplete_role="TREATMENT")
            result = self._analyze(root, pairing, runs)
            self.assertEqual("INCONCLUSIVE", result.analysis_status)
            self.assertIn(
                "RUN_NOT_COMPLETED",
                {item["code"] for item in _json(root / "analysis" / "paired-analysis.json")["reasons"]},
            )

    def test_control_projection_drift_is_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            changed = _example("plan-treatment.json")
            changed["question"] = "A post-registration question change must be rejected."
            sealed_changed = seal_plan(changed)
            pairing, runs = self._create_group(root, treatment_plan=sealed_changed)
            result = self._analyze(root, pairing, runs)
            analysis = _json(root / "analysis" / "paired-analysis.json")
            self.assertEqual("INCONCLUSIVE", result.analysis_status)
            self.assertIn(
                "CONTROL_PROJECTION_MISMATCH",
                {item["code"] for item in analysis["reasons"]},
            )

    def test_reused_role_and_wrong_time_order_are_retained_as_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root)
            reused = dict(runs)
            reused["RESTORED_BASELINE"] = runs["BASELINE"]
            result = self._analyze(root, pairing, reused)
            codes = {
                item["code"]
                for item in _json(root / "analysis" / "paired-analysis.json")["reasons"]
            }
            self.assertEqual("INCONCLUSIVE", result.analysis_status)
            self.assertIn("RUN_ID_REUSED", codes)
            self.assertIn("BUNDLE_REUSED", codes)
            self.assertIn("ROLE_ORDER_MISMATCH", codes)

    def test_same_inputs_are_byte_identical_and_manifest_is_exact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root)
            self._analyze(root, pairing, runs, "first")
            self._analyze(root, pairing, runs, "second")
            first_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (root / "first").iterdir()
            }
            second_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (root / "second").iterdir()
            }
            self.assertEqual(first_hashes, second_hashes)
            manifest = _json(root / "first" / "paired-analysis-manifest.json")
            self.assertEqual(
                [
                    "sealed-pairing-plan.json",
                    "paired-analysis.json",
                    "paired-analysis.md",
                ],
                [item["path"] for item in manifest["files"]],
            )
            all_bytes = b"".join(path.read_bytes() for path in (root / "first").iterdir())
            self.assertNotIn(str(root).encode(), all_bytes)
            with self.assertRaisesRegex(PairingError, "拒绝覆盖"):
                self._analyze(root, pairing, runs, "first")

    def test_tampered_source_and_pairing_plan_are_rejected_without_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root)
            report = runs["TREATMENT"] / "report.json"
            report.write_bytes(report.read_bytes() + b" ")
            with self.assertRaises(PairingError) as context:
                self._analyze(root, pairing, runs)
            self.assertEqual("BUNDLE_SIZE_MISMATCH", context.exception.code)
            self.assertFalse((root / "analysis").exists())
            self.assertFalse(list(root.glob(".veritrail-pairing-*")))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairing, runs = self._create_group(root)
            tampered = _json(pairing)
            tampered["question"] = "Tampered after sealing."
            pairing.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaises(PairingError) as context:
                self._analyze(root, pairing, runs)
            self.assertEqual("PAIRING_PLAN_SEAL_MISMATCH", context.exception.code)

    def test_cli_seal_pair_and_sanitized_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            unsealed = ROOT / "examples" / "pairing" / "pairing-plan.json"
            sealed = root / "sealed.json"
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(
                    ["seal-pairing", "--plan", str(unsealed), "--output", str(sealed)]
                )
            self.assertEqual(0, code)
            self.assertEqual("seal-pairing", json.loads(stdout.getvalue())["command"])

            _, runs = self._create_group(root / "runs")
            output = root / "paired"
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "pair",
                        "--plan",
                        str(sealed),
                        "--baseline",
                        str(runs["BASELINE"]),
                        "--treatment",
                        str(runs["TREATMENT"]),
                        "--restored-baseline",
                        str(runs["RESTORED_BASELINE"]),
                        "--negative-control",
                        str(runs["NEGATIVE_CONTROL"]),
                        "--output",
                        str(output),
                    ]
                )
            payload = json.loads(stdout.getvalue())
            self.assertEqual(0, code)
            self.assertEqual("SUPPORTED", payload["analysis_status"])
            self.assertEqual("paired", payload["output"])

            stderr = StringIO()
            with redirect_stderr(stderr):
                code = main(
                    [
                        "pair",
                        "--plan",
                        str(sealed),
                        "--baseline",
                        str(root / "private-missing-source"),
                        "--treatment",
                        str(runs["TREATMENT"]),
                        "--restored-baseline",
                        str(runs["RESTORED_BASELINE"]),
                        "--negative-control",
                        str(runs["NEGATIVE_CONTROL"]),
                        "--output",
                        str(root / "never-created"),
                    ]
                )
            error = json.loads(stderr.getvalue())["error"]
            self.assertEqual(2, code)
            self.assertEqual("SOURCE_BUNDLE_UNREADABLE", error["code"])
            self.assertNotIn(str(root), stderr.getvalue())

    def test_example_pairing_digests_match_role_plans(self) -> None:
        pairing = _example("pairing-plan.json")
        self.assertEqual(
            plan_digest(_example("plan-baseline.json")),
            pairing["roles"]["BASELINE"]["plan_sha256"],
        )
        self.assertEqual(
            plan_digest(_example("plan-treatment.json")),
            pairing["roles"]["TREATMENT"]["plan_sha256"],
        )
        self.assertEqual(
            plan_digest(_example("plan-negative-control.json")),
            pairing["roles"]["NEGATIVE_CONTROL"]["plan_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
