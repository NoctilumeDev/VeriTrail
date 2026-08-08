from __future__ import annotations

import copy
import unittest

from veritrail.errors import ValidationError
from veritrail.plan import seal_plan, validate_plan, verify_sealed_plan

from tests.support import browser_plan, example_plan, preflight_plan


class PlanV03Tests(unittest.TestCase):
    def test_frozen_m0_and_m1_plan_hashes_remain_compatible(self) -> None:
        self.assertEqual(
            "90235a18c59e9f30cd2aa519d281a4fdb18f04e83bdf2fcc5ff98770dba8a2b8",
            seal_plan(example_plan())["seal"]["digest"],
        )
        self.assertEqual(
            "df1966bbab8e1f6c0288525747ff96bd5c7d3e26120dbfafea8f27367324f41b",
            seal_plan(preflight_plan())["seal"]["digest"],
        )

    def test_browser_plan_seals_and_detects_policy_mutation(self) -> None:
        sealed = seal_plan(browser_plan())
        verify_sealed_plan(sealed)
        mutated = copy.deepcopy(sealed)
        mutated["browser"]["timeout_ms"] += 1
        with self.assertRaisesRegex(ValidationError, "seal does not match"):
            verify_sealed_plan(mutated)

    def test_plan_v03_requires_both_evidence_types_and_browser_assertion(self) -> None:
        missing_browser = browser_plan()
        missing_browser["required_evidence"].remove("browser.session")
        with self.assertRaisesRegex(ValidationError, "must require browser.session"):
            validate_plan(missing_browser)

        missing_assertion = browser_plan()
        for assertion in missing_assertion["assertions"]:
            if assertion["evidence_type"] == "browser.session":
                assertion["severity"] = "OBSERVATION"
        with self.assertRaisesRegex(ValidationError, "decisive assertion over browser.session"):
            validate_plan(missing_assertion)

    def test_browser_policy_is_bounded_to_loopback_structured_steps(self) -> None:
        cases = {
            "remote origin": lambda browser: browser.update(
                start_url="https://example.test/", allowed_origins=["https://example.test"]
            ),
            "origin without port": lambda browser: browser.update(
                start_url="http://localhost/index.html", allowed_origins=["http://localhost"]
            ),
            "origin query": lambda browser: browser.update(
                allowed_origins=["http://localhost:18765?token=demo"]
            ),
            "start query": lambda browser: browser.update(
                start_url="http://localhost:18765/index.html?token=demo"
            ),
            "too many viewports": lambda browser: browser.update(
                viewports=browser["viewports"] * 3
            ),
            "duplicate step id": lambda browser: browser["steps"].append(
                copy.deepcopy(browser["steps"][0])
            ),
            "unsupported action": lambda browser: browser["steps"][0].update(
                action="javascript"
            ),
            "action extra field": lambda browser: browser["steps"][1].update(
                value="unexpected"
            ),
            "too many screenshots": lambda browser: browser.update(
                steps=[
                    {"id": f"capture-{index}", "action": "screenshot", "name": f"shot-{index}"}
                    for index in range(5)
                ]
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                plan = browser_plan()
                mutate(plan["browser"])
                with self.assertRaises(ValidationError):
                    validate_plan(plan)

    def test_explicit_ipv4_loopback_is_allowed_but_public_ip_is_not(self) -> None:
        plan = browser_plan()
        plan["browser"]["start_url"] = "http://127.0.0.1:18765/index.html"
        plan["browser"]["allowed_origins"] = ["http://127.0.0.1:18765"]
        validate_plan(plan)

        plan["browser"]["start_url"] = "http://192.0.2.1:18765/index.html"
        plan["browser"]["allowed_origins"] = ["http://192.0.2.1:18765"]
        with self.assertRaises(ValidationError):
            validate_plan(plan)

    def test_older_plans_reject_browser_contract(self) -> None:
        plan_v01 = example_plan()
        plan_v01["browser"] = browser_plan()["browser"]
        with self.assertRaisesRegex(ValidationError, "browser requires schema_version '0.3'"):
            validate_plan(plan_v01)

        plan_v02 = preflight_plan()
        plan_v02["browser"] = browser_plan()["browser"]
        with self.assertRaisesRegex(ValidationError, "browser requires schema_version '0.3'"):
            validate_plan(plan_v02)


if __name__ == "__main__":
    unittest.main()
