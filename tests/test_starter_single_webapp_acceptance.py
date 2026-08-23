from __future__ import annotations

import inspect
import tempfile
import unittest
from pathlib import Path

from scripts.starter_single_webapp_acceptance import (
    FIXTURE_ROOT,
    build_answers,
    materialize_subjects,
)
from veritrail.plan import validate_plan
from veritrail.project_profile import project_profile_digest, validate_project_profile
from veritrail_starter.contract import build_documents, normalize_answers


class StarterSingleWebappAcceptanceTests(unittest.TestCase):
    def test_subject_pair_has_one_explicit_business_fact_delta(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pass_root, fail_root = materialize_subjects(Path(temporary))
            pass_files = {
                item.relative_to(pass_root).as_posix(): item.read_bytes()
                for item in pass_root.rglob("*")
                if item.is_file()
            }
            fail_files = {
                item.relative_to(fail_root).as_posix(): item.read_bytes()
                for item in fail_root.rglob("*")
                if item.is_file()
            }
            self.assertEqual(set(pass_files), set(fail_files))
            self.assertEqual(
                [name for name in sorted(pass_files) if pass_files[name] != fail_files[name]],
                ["app/fact.json"],
            )
            self.assertIn(b'"ready"', pass_files["app/fact.json"])
            self.assertIn(b'"blocked"', fail_files["app/fact.json"])

    def test_answers_generate_one_core_valid_unsealed_authority(self) -> None:
        answers = normalize_answers(build_answers(FIXTURE_ROOT, 18789))
        profile, plan, bindings = build_documents(answers)
        self.assertNotIn("seal", profile)
        self.assertNotIn("seal", plan)
        self.assertEqual(plan["resource_budget"]["max_artifact_bytes"], 8 * 1024 * 1024)
        self.assertLessEqual(plan["resource_budget"]["max_artifact_bytes"], 10 * 1024 * 1024)
        self.assertEqual(
            next(
                item
                for item in plan["browser"]["steps"]
                if item["id"] == "starter-ready-fact"
            )["value"],
            "evidence ready: starter-demo",
        )
        self.assertIn(
            "starter-browser-business-steps-passed",
            {item["id"] for item in plan["assertions"]},
        )
        validate_project_profile(profile)
        sealed_profile = dict(profile)
        sealed_profile["seal"] = {
            "algorithm": "sha256",
            "digest": project_profile_digest(profile),
        }
        validate_plan(plan, sealed_profile)
        self.assertEqual(bindings["schema_version"], "0.1")

    def test_acceptance_gate_does_not_depend_on_optimized_away_asserts(self) -> None:
        import scripts.starter_single_webapp_acceptance as acceptance

        source = inspect.getsource(acceptance)
        self.assertNotIn("assert ", source)


if __name__ == "__main__":
    unittest.main()
