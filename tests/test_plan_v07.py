from __future__ import annotations

import copy
import json
import unittest

from veritrail.errors import ValidationError
from veritrail.plan import seal_plan, validate_plan, verify_sealed_plan
from veritrail.project_profile import seal_project_profile, validate_project_profile

from tests.support import (
    ROOT,
    bootstrap_profile,
    sealed_bootstrap_profile,
    sealed_single_bootstrap_profile,
    single_bootstrap_plan,
    single_bootstrap_profile,
)


class PlanV07Tests(unittest.TestCase):
    def test_profile_v02_schema_and_validator_freeze_single_application(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "project-profile-0.2.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("0.2", schema["properties"]["schema_version"]["const"])
        self.assertEqual("SINGLE_APPLICATION", schema["properties"]["topology"]["const"])
        profile = single_bootstrap_profile()
        validate_project_profile(profile)

        cases = {
            "missing topology": lambda value: value.pop("topology"),
            "hidden dependency": lambda value: value["nodes"].append(
                copy.deepcopy(bootstrap_profile()["nodes"][0])
            ),
            "dependency role": lambda value: value["nodes"][0].update(
                role="DEPENDENCY"
            ),
            "depends_on": lambda value: value["nodes"][0].update(
                depends_on=["application"]
            ),
            "two-node order": lambda value: value.update(
                start_order=["application", "other"]
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                candidate = single_bootstrap_profile()
                mutate(candidate)
                with self.assertRaises(ValidationError):
                    validate_project_profile(candidate)

    def test_profile_versions_do_not_accept_each_others_contract(self) -> None:
        old = bootstrap_profile()
        old["topology"] = "SINGLE_APPLICATION"
        with self.assertRaisesRegex(ValidationError, "unsupported fields: topology"):
            validate_project_profile(old)

        new = single_bootstrap_profile()
        new["schema_version"] = "0.1"
        with self.assertRaises(ValidationError):
            validate_project_profile(new)

    def test_plan_v07_binds_only_profile_v02_and_frozen_primary(self) -> None:
        profile = sealed_single_bootstrap_profile()
        plan = single_bootstrap_plan(profile)
        sealed = seal_plan(plan, profile)
        verify_sealed_plan(sealed, profile)

        with self.assertRaisesRegex(ValidationError, "requires a sealed ProjectProfile"):
            validate_plan(plan)
        with self.assertRaisesRegex(ValidationError, "requires ProjectProfile 0.2"):
            validate_plan(plan, sealed_bootstrap_profile())

        wrong_primary = single_bootstrap_plan(profile)
        primary = next(
            item for item in wrong_primary["variables"] if item["role"] == "PRIMARY"
        )
        primary["value"] = "veritrail_managed_windows_c1_two_node_services"
        with self.assertRaisesRegex(ValidationError, "frozen bootstrap topology"):
            validate_plan(wrong_primary, profile)

    def test_plan_v06_rejects_profile_v02_and_v07_rejects_profile_v01(self) -> None:
        old_profile = sealed_bootstrap_profile()
        new_profile = sealed_single_bootstrap_profile()
        old_plan = single_bootstrap_plan(new_profile)
        old_plan["schema_version"] = "0.6"
        primary = next(item for item in old_plan["variables"] if item["role"] == "PRIMARY")
        primary.update(
            name="project_bootstrap_mode",
            value="veritrail_managed_windows_c1_two_node_services",
        )
        with self.assertRaisesRegex(ValidationError, "requires ProjectProfile 0.1"):
            validate_plan(old_plan, new_profile)

        new_plan = single_bootstrap_plan(new_profile)
        new_plan["bootstrap_profile"] = {
            "profile_id": old_profile["profile_id"],
            "profile_version": old_profile["version"],
            "profile_sha256": old_profile["seal"]["digest"],
        }
        with self.assertRaisesRegex(ValidationError, "requires ProjectProfile 0.2"):
            validate_plan(new_plan, old_profile)

    def test_profile_v02_seal_is_stable(self) -> None:
        first = seal_project_profile(single_bootstrap_profile())
        second = seal_project_profile(single_bootstrap_profile())
        self.assertEqual(first["seal"], second["seal"])

    def test_public_gate_a_authority_set_has_stable_one_to_one_bindings(self) -> None:
        root = ROOT / "examples" / "bootstrap"
        base_plan = json.loads((root / "plan-positive.json").read_text(encoding="utf-8"))
        authority_set = json.loads(
            (root / "authority-set.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {
                "positive",
                "browser-negative",
                "early-exit",
                "readiness-timeout",
                "owner-mismatch",
            },
            {item["name"] for item in authority_set["authorities"]},
        )
        for authority in authority_set["authorities"]:
            with self.subTest(authority=authority["name"]):
                profile = seal_project_profile(
                    json.loads(
                        (root / authority["profile"]).read_text(encoding="utf-8")
                    )
                )
                self.assertEqual(
                    authority["profile_sha256"], profile["seal"]["digest"]
                )
                draft = copy.deepcopy(base_plan)
                draft["plan_id"] = authority["plan_id"]
                draft["bootstrap_profile"] = {
                    "profile_id": profile["profile_id"],
                    "profile_version": profile["version"],
                    "profile_sha256": profile["seal"]["digest"],
                }
                missing_selector = authority["browser_missing_selector"]
                if missing_selector is not None:
                    step = next(
                        item
                        for item in draft["browser"]["steps"]
                        if item["id"] == "evidence-list-visible"
                    )
                    step["selector"] = missing_selector
                sealed = seal_plan(draft, profile)
                verify_sealed_plan(sealed, profile)
                self.assertEqual(authority["plan_sha256"], sealed["seal"]["digest"])


if __name__ == "__main__":
    unittest.main()
