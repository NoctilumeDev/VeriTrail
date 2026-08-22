from __future__ import annotations

import copy
import unittest

from scripts.m14_inknarratives_acceptance import (
    APPLICATION_PORT,
    EXPECTED_NEGATIVE_PLAN_SHA256,
    EXPECTED_POSITIVE_PLAN_SHA256,
    EXPECTED_PROFILE_SHA256,
    EXPECTED_SUBJECT_REF,
    GALLERY_WORK_IDS,
    POSITIVE_DOCUMENTS_PER_VIEWPORT,
    PUBLIC_PAGES,
    SCREENSHOT_NAMES,
    raw_browser_negative_plan,
    raw_positive_plan,
    raw_profile,
)
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile


class M14InkNarrativesAcceptanceContractTests(unittest.TestCase):
    def test_profile_and_plans_are_digest_frozen(self) -> None:
        profile = seal_project_profile(raw_profile())
        positive = seal_plan(raw_positive_plan(profile["seal"]["digest"]), profile)
        negative = seal_plan(
            raw_browser_negative_plan(profile["seal"]["digest"]), profile
        )

        self.assertEqual(EXPECTED_PROFILE_SHA256, profile["seal"]["digest"])
        self.assertEqual(EXPECTED_POSITIVE_PLAN_SHA256, positive["seal"]["digest"])
        self.assertEqual(EXPECTED_NEGATIVE_PLAN_SHA256, negative["seal"]["digest"])

    def test_profile_is_one_owned_loopback_application(self) -> None:
        profile = raw_profile()
        node = profile["nodes"][0]

        self.assertEqual("SINGLE_APPLICATION", profile["topology"])
        self.assertEqual(APPLICATION_PORT, node["port"])
        self.assertEqual("/index.html", node["readiness"]["path"])
        self.assertEqual(
            ["-m", "http.server", "application", "--bind", "127.0.0.1"],
            [
                item.get("literal", item.get("node_port"))
                for item in node["arguments"]
            ],
        )

    def test_positive_plan_covers_gallery_five_works_and_two_viewports(self) -> None:
        profile = seal_project_profile(raw_profile())
        plan = raw_positive_plan(profile["seal"]["digest"])
        steps = plan["browser"]["steps"]

        self.assertEqual(EXPECTED_SUBJECT_REF, plan["subject"]["source_ref"])
        self.assertEqual(1536, plan["browser"]["max_job_memory_mb"])
        self.assertEqual(2, len(plan["browser"]["viewports"]))
        self.assertEqual(50, len(steps))
        self.assertEqual(4, sum(step["action"] == "screenshot" for step in steps))
        self.assertEqual(
            set(SCREENSHOT_NAMES),
            {step["name"] for step in steps if step["action"] == "screenshot"},
        )
        self.assertEqual(6, len(PUBLIC_PAGES))
        self.assertEqual(10, POSITIVE_DOCUMENTS_PER_VIEWPORT)
        for work_id in GALLERY_WORK_IDS:
            self.assertIn(
                f'[data-work="{work_id}"]',
                {step.get("selector") for step in steps},
            )
            self.assertIn(
                f'[data-work-link="{work_id}"]',
                {step.get("selector") for step in steps},
            )

    def test_negative_authority_changes_only_the_preregistered_selector(self) -> None:
        profile = seal_project_profile(raw_profile())
        positive = raw_positive_plan(profile["seal"]["digest"])
        negative = raw_browser_negative_plan(profile["seal"]["digest"])
        self.assertEqual(
            "#veritrail-m14-missing-gallery",
            next(
                step
                for step in negative["browser"]["steps"]
                if step["id"] == "gallery-works-visible"
            )["selector"],
        )

        normalized_positive = copy.deepcopy(positive)
        normalized_negative = copy.deepcopy(negative)
        normalized_positive["plan_id"] = normalized_negative["plan_id"]
        next(
            step
            for step in normalized_positive["browser"]["steps"]
            if step["id"] == "gallery-works-visible"
        )["selector"] = "#veritrail-m14-missing-gallery"
        self.assertEqual(normalized_positive, normalized_negative)


if __name__ == "__main__":
    unittest.main()
