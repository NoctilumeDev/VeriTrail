from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from veritrail.catalog import validate_bundle
from veritrail.reporting import create_bundle
from veritrail.verdict import evaluate

from tests.support import artifact, sealed_example_plan


class VerdictTests(unittest.TestCase):
    def test_complete_clean_run_passes(self) -> None:
        result = evaluate(sealed_example_plan(), [artifact()], "COMPLETED")
        self.assertEqual("PASS", result["verdict"])

    def test_hard_failure_fails(self) -> None:
        result = evaluate(
            sealed_example_plan(),
            [artifact(suite_passed=False, failures=1)],
            "COMPLETED",
        )
        self.assertEqual("FAIL", result["verdict"])
        self.assertEqual(2, sum(item["status"] == "FAIL" for item in result["assertions"]))

    def test_variable_contamination_blocks_attribution_of_hard_failure(self) -> None:
        cases = (
            (
                "unknown",
                {
                    "fixture_mode": "passing",
                    "python_major_minor": "3.10",
                    "background_load": "unexpected",
                },
                "UNKNOWN_VARIABLE",
            ),
            (
                "controlled-drift",
                {"fixture_mode": "passing", "python_major_minor": "3.13"},
                "VARIABLE_DRIFT",
            ),
        )
        for name, observations, code in cases:
            with self.subTest(case=name):
                result = evaluate(
                    sealed_example_plan(),
                    [
                        artifact(
                            suite_passed=False,
                            failures=1,
                            observed_variables=observations,
                        )
                    ],
                    "COMPLETED",
                )
                self.assertEqual("INCONCLUSIVE", result["verdict"])
                self.assertIn(code, {item["code"] for item in result["contamination"]})
                self.assertTrue(
                    any(item["status"] == "FAIL" for item in result["assertions"])
                )

    def test_evidence_conflict_blocks_attribution_of_other_hard_failure(self) -> None:
        result = evaluate(
            sealed_example_plan(),
            [
                artifact(suite_passed=False, failures=1),
                artifact(suite_passed=False, failures=2),
            ],
            "COMPLETED",
        )
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        self.assertTrue(any(item["status"] == "FAIL" for item in result["assertions"]))
        self.assertIn(
            "EVIDENCE_CONFLICT",
            {item["code"] for item in result["contamination"]},
        )

    def test_catalog_rederives_contaminated_hard_failure_as_inconclusive(self) -> None:
        plan = sealed_example_plan()
        failed = artifact(
            suite_passed=False,
            failures=1,
            observed_variables={
                "fixture_mode": "passing",
                "python_major_minor": "3.10",
                "background_load": "unexpected",
            },
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "bundle"
            report = create_bundle(
                plan=plan,
                evidence_paths=[],
                output=output,
                run_id="contaminated-hard-failure",
                execution_status="COMPLETED",
                generated_evidence=[failed],
            )
            validated = validate_bundle(output, root)
        self.assertEqual("INCONCLUSIVE", report["verdict"])
        self.assertEqual("INCONCLUSIVE", validated.verdict)

    def test_missing_evidence_is_pending(self) -> None:
        result = evaluate(sealed_example_plan(), [], "COMPLETED")
        self.assertEqual("PENDING", result["verdict"])
        self.assertEqual(["automated.test-summary"], result["missing_evidence"])

    def test_unknown_variable_is_inconclusive(self) -> None:
        observations = {
            "fixture_mode": "passing",
            "python_major_minor": "3.10",
            "background_load": "unexpected",
        }
        result = evaluate(
            sealed_example_plan(),
            [artifact(observed_variables=observations)],
            "COMPLETED",
        )
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        self.assertEqual("UNKNOWN_VARIABLE", result["contamination"][0]["code"])

    def test_controlled_variable_drift_is_inconclusive(self) -> None:
        observations = {"fixture_mode": "passing", "python_major_minor": "3.13"}
        result = evaluate(
            sealed_example_plan(),
            [artifact(observed_variables=observations)],
            "COMPLETED",
        )
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        self.assertEqual("VARIABLE_DRIFT", result["contamination"][0]["code"])

    def test_conflicting_evidence_is_inconclusive(self) -> None:
        result = evaluate(
            sealed_example_plan(),
            [artifact(), artifact(suite_passed=False, failures=0)],
            "COMPLETED",
        )
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        self.assertTrue(any(item["code"] == "EVIDENCE_CONFLICT" for item in result["contamination"]))

    def test_aborted_run_can_preserve_proven_failure(self) -> None:
        failed = evaluate(
            sealed_example_plan(),
            [artifact(suite_passed=False, failures=1)],
            "ABORTED",
        )
        pending = evaluate(sealed_example_plan(), [artifact()], "ABORTED")
        self.assertEqual("FAIL", failed["verdict"])
        self.assertEqual("PENDING", pending["verdict"])
        self.assertEqual("ABORTED", failed["execution_status"])
        self.assertEqual("ABORTED", pending["execution_status"])

    def test_expired_baseline_is_inconclusive(self) -> None:
        plan = copy.deepcopy(sealed_example_plan())
        plan["baseline"]["status"] = "EXPIRED"
        result = evaluate(plan, [artifact()], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", result["verdict"])

    def test_exists_rule_handles_missing_value_in_multiple_artifacts(self) -> None:
        plan = sealed_example_plan()
        plan["assertions"] = [
            {
                "id": "optional-fact-is-absent",
                "severity": "HARD",
                "evidence_type": "automated.test-summary",
                "path": "/facts/not_present",
                "operator": "exists",
                "expected": False,
            }
        ]
        result = evaluate(plan, [artifact(), artifact()], "COMPLETED")
        self.assertEqual("PASS", result["verdict"])


if __name__ == "__main__":
    unittest.main()
