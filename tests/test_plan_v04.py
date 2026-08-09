from __future__ import annotations

import copy
import unittest

from veritrail.errors import ValidationError
from veritrail.plan import seal_plan, validate_plan, verify_sealed_plan

from tests.support import browser_plan, orchestration_plan


class PlanV04Tests(unittest.TestCase):
    def test_frozen_plan_v03_hash_remains_compatible(self) -> None:
        self.assertEqual(
            "2a16769446e4eb617ab4fdd51b7b1eda9c7266654d5a991106416c9488c91fd7",
            seal_plan(browser_plan())["seal"]["digest"],
        )

    def test_orchestration_plan_seals_and_detects_target_mutation(self) -> None:
        sealed = seal_plan(orchestration_plan())
        verify_sealed_plan(sealed)
        mutated = copy.deepcopy(sealed)
        mutated["target"]["startup_timeout_ms"] += 1
        with self.assertRaisesRegex(ValidationError, "seal does not match"):
            verify_sealed_plan(mutated)

    def test_plan_v04_requires_orchestration_evidence_and_decisive_assertion(self) -> None:
        missing_evidence = orchestration_plan()
        missing_evidence["required_evidence"].remove("runtime.orchestration")
        with self.assertRaisesRegex(ValidationError, "must require runtime.orchestration"):
            validate_plan(missing_evidence)

        missing_assertion = orchestration_plan()
        for assertion in missing_assertion["assertions"]:
            if assertion["evidence_type"] == "runtime.orchestration":
                assertion["severity"] = "OBSERVATION"
        with self.assertRaisesRegex(
            ValidationError, "decisive assertion over runtime.orchestration"
        ):
            validate_plan(missing_assertion)

    def test_static_target_policy_is_bounded_and_cross_checked(self) -> None:
        cases = {
            "unsafe root": lambda plan: plan["target"].update(root="../site"),
            "backslash root": lambda plan: plan["target"].update(root="examples\\site"),
            "unsupported adapter": lambda plan: plan["target"].update(adapter="SHELL"),
            "privileged port": lambda plan: plan["target"].update(port=80),
            "port not free": lambda plan: plan["preflight"]["ports"][0].update(
                expected="LISTENING"
            ),
            "browser port mismatch": lambda plan: plan["browser"].update(
                start_url="http://localhost:18768/index.html",
                allowed_origins=["http://localhost:18768"],
            ),
            "ready query": lambda plan: plan["target"].update(
                ready_path="/index.html?secret=value"
            ),
            "ready empty segment": lambda plan: plan["target"].update(
                ready_path="/assets//index.html"
            ),
            "ready control character": lambda plan: plan["target"].update(
                ready_path="/index.html\n"
            ),
            "file above total": lambda plan: plan["target"].update(
                max_file_bytes=2, max_total_bytes=1
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                plan = orchestration_plan()
                mutate(plan)
                with self.assertRaises(ValidationError):
                    validate_plan(plan)

    def test_malformed_cross_fields_are_validation_errors_not_crashes(self) -> None:
        for field, value in (
            ("ports", None),
            ("ports", {}),
        ):
            with self.subTest(preflight_field=field, value=value):
                plan = orchestration_plan()
                plan["preflight"][field] = value
                with self.assertRaises(ValidationError):
                    validate_plan(plan)

        for field, value in (("allowed_origins", None), ("steps", {})):
            with self.subTest(browser_field=field, value=value):
                plan = orchestration_plan()
                plan["browser"][field] = value
                with self.assertRaises(ValidationError):
                    validate_plan(plan)

        plan = orchestration_plan()
        plan["browser"]["allowed_origins"] = ["http://[invalid"]
        with self.assertRaises(ValidationError):
            validate_plan(plan)

    def test_older_plan_rejects_target_contract(self) -> None:
        plan = browser_plan()
        plan["target"] = orchestration_plan()["target"]
        with self.assertRaisesRegex(ValidationError, "target requires schema_version '0.4'"):
            validate_plan(plan)


if __name__ == "__main__":
    unittest.main()
