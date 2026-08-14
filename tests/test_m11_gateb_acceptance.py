from __future__ import annotations

import copy
import unittest

from scripts.m11_gateb_acceptance import (
    APPLICATION_PORT,
    EXPECTED_NEGATIVE_PLAN_SHA256,
    EXPECTED_POSITIVE_PLAN_SHA256,
    EXPECTED_PROFILE_SHA256,
    EXPECTED_SUBJECT_REF,
    PAGES,
    raw_browser_negative_plan,
    raw_positive_plan,
    raw_profile,
)
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile


class M11GateBAcceptanceContractTests(unittest.TestCase):
    def test_frozen_profile_uses_exact_single_application_boundary(self) -> None:
        profile = seal_project_profile(raw_profile())

        self.assertEqual(EXPECTED_PROFILE_SHA256, profile["seal"]["digest"])
        self.assertEqual("0.2", profile["schema_version"])
        self.assertEqual("SINGLE_APPLICATION", profile["topology"])
        self.assertEqual("m11-ink-single-app", profile["profile_id"])
        self.assertEqual(["."], profile["subject_watch_roots"])
        self.assertEqual(["application"], profile["start_order"])
        self.assertEqual(["application"], profile["teardown_order"])
        node = profile["nodes"][0]
        self.assertEqual(APPLICATION_PORT, node["port"])
        self.assertEqual(".", node["working_directory"])
        self.assertEqual(65536, node["readiness"]["max_response_bytes"])
        self.assertEqual(
            ["-m", "http.server", "application", "--bind", "127.0.0.1"],
            [
                item.get("literal", item.get("node_port"))
                for item in node["arguments"]
            ],
        )

    def test_positive_plan_freezes_five_pages_two_viewports_and_four_shots(self) -> None:
        profile = seal_project_profile(raw_profile())
        plan = seal_plan(raw_positive_plan(profile["seal"]["digest"]), profile)

        self.assertEqual(EXPECTED_POSITIVE_PLAN_SHA256, plan["seal"]["digest"])
        self.assertEqual("0.7", plan["schema_version"])
        self.assertEqual(2, plan["version"])
        self.assertEqual(EXPECTED_SUBJECT_REF, plan["subject"]["source_ref"])
        self.assertEqual(2, len(plan["browser"]["viewports"]))
        self.assertEqual(4, sum(step["action"] == "screenshot" for step in plan["browser"]["steps"]))
        self.assertEqual(4, sum(step["action"] == "goto" for step in plan["browser"]["steps"]))
        cabin_step = next(
            step
            for step in plan["browser"]["steps"]
            if step["id"] == "scroll-cabin-visible"
        )
        self.assertEqual(
            {"id": "scroll-cabin-visible", "action": "expect_visible", "selector": "#cabin"},
            cabin_step,
        )
        self.assertEqual(PAGES[0][0], plan["browser"]["start_url"].split(str(APPLICATION_PORT), 1)[1])
        screenshot_assertion = next(
            item
            for item in plan["assertions"]
            if item["id"] == "m11-gateb-browser-screenshot-coverage"
        )
        self.assertEqual(8, screenshot_assertion["expected"])

    def test_negative_authority_changes_only_plan_id_and_one_selector(self) -> None:
        profile = seal_project_profile(raw_profile())
        positive = raw_positive_plan(profile["seal"]["digest"])
        negative = raw_browser_negative_plan(profile["seal"]["digest"])

        self.assertEqual(
            EXPECTED_NEGATIVE_PLAN_SHA256,
            seal_plan(negative, profile)["seal"]["digest"],
        )

        self.assertNotEqual(positive["plan_id"], negative["plan_id"])
        positive_without_id = copy.deepcopy(positive)
        negative_without_id = copy.deepcopy(negative)
        positive_without_id.pop("plan_id")
        negative_without_id.pop("plan_id")
        positive_step = next(
            item
            for item in positive_without_id["browser"]["steps"]
            if item["id"] == "su-chapter-visible"
        )
        negative_step = next(
            item
            for item in negative_without_id["browser"]["steps"]
            if item["id"] == "su-chapter-visible"
        )
        self.assertEqual("#chapter11", positive_step.pop("selector"))
        self.assertEqual("#veritrail-m11-missing-selector", negative_step.pop("selector"))
        self.assertEqual(positive_without_id, negative_without_id)


if __name__ == "__main__":
    unittest.main()
