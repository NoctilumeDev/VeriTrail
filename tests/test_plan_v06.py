from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from veritrail.cli import main
from veritrail.errors import ValidationError
from veritrail.plan import seal_plan, validate_plan, verify_sealed_plan

from tests.support import (
    ROOT,
    bootstrap_plan,
    command_plan,
    orchestration_plan,
    sealed_bootstrap_profile,
)


class PlanV06Tests(unittest.TestCase):
    def test_plan_v06_schema_has_the_frozen_exact_top_level_contract(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "experiment-plan-0.6.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            {
                "schema_version",
                "plan_id",
                "version",
                "subject",
                "question",
                "baseline",
                "experiment_type",
                "variables",
                "required_evidence",
                "assertions",
                "random_seed",
                "resource_budget",
                "preflight",
                "browser",
                "bootstrap_profile",
                "load_model",
                "change_scope",
                "reproduction_steps",
                "cleanup_steps",
            },
            set(schema["required"]),
        )

    def test_hardened_plan_v04_and_v05_hashes_are_stable(self) -> None:
        self.assertEqual(
            "6cdf3bdf15fe8572d756dee43d7431a81d61a7eb6547af696110e45c24cd120a",
            seal_plan(orchestration_plan())["seal"]["digest"],
        )
        self.assertEqual(
            "ccae38efe3e6425e50a924634e8e507dced6b1e108a76ed3ca6f563788c9f5d6",
            seal_plan(command_plan())["seal"]["digest"],
        )

    def test_plan_v06_requires_and_binds_sealed_profile(self) -> None:
        profile = sealed_bootstrap_profile()
        plan = bootstrap_plan(profile)
        sealed = seal_plan(plan, profile)
        verify_sealed_plan(sealed, profile)
        with self.assertRaisesRegex(ValidationError, "requires a sealed ProjectProfile"):
            validate_plan(plan)

        mismatched = copy.deepcopy(profile)
        mismatched["version"] = 2
        mismatched.pop("seal")
        from veritrail.project_profile import seal_project_profile

        mismatched = seal_project_profile(mismatched)
        with self.assertRaisesRegex(ValidationError, "does not match"):
            validate_plan(plan, mismatched)

    def test_plan_v06_frozen_primary_evidence_and_contract_boundaries(self) -> None:
        profile = sealed_bootstrap_profile()

        def weaken_bootstrap_assertions(plan: dict) -> None:
            for assertion in plan["assertions"]:
                if assertion["evidence_type"] == "runtime.bootstrap":
                    assertion["severity"] = "OBSERVATION"

        cases = {
            "primary name": lambda plan: next(
                item for item in plan["variables"] if item["role"] == "PRIMARY"
            ).update(name="other_mode"),
            "primary value": lambda plan: next(
                item for item in plan["variables"] if item["role"] == "PRIMARY"
            ).update(value="other"),
            "missing bootstrap evidence": lambda plan: plan["required_evidence"].remove(
                "runtime.bootstrap"
            ),
            "legacy evidence": lambda plan: plan["required_evidence"].append(
                "runtime.command"
            ),
            "weak bootstrap assertion": weaken_bootstrap_assertions,
            "legacy assertion": lambda plan: plan["assertions"].append(
                {
                    "id": "legacy-command",
                    "severity": "OBSERVATION",
                    "evidence_type": "runtime.command",
                    "path": "/facts/exit_expected",
                    "operator": "eq",
                    "expected": True,
                }
            ),
            "legacy target": lambda plan: plan.update(
                target=orchestration_plan()["target"]
            ),
            "legacy command": lambda plan: plan.update(command=command_plan()["command"]),
            "missing screenshot acknowledgement": lambda plan: plan["browser"].pop(
                "screenshot_safety"
            ),
            "missing browser memory limit": lambda plan: plan["browser"].pop(
                "max_job_memory_mb"
            ),
            "oversized browser memory limit": lambda plan: plan["browser"].update(
                max_job_memory_mb=4096
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                plan = bootstrap_plan(profile)
                mutate(plan)
                with self.assertRaises(ValidationError):
                    validate_plan(plan, profile)

    def test_plan_v06_cross_checks_ports_and_browser_origin(self) -> None:
        profile = sealed_bootstrap_profile()
        wrong_port = bootstrap_plan(profile)
        wrong_port["preflight"]["ports"][1]["port"] = 18773
        with self.assertRaisesRegex(ValidationError, "each ProjectProfile node port"):
            validate_plan(wrong_port, profile)

        wrong_origin = bootstrap_plan(profile)
        wrong_origin["browser"]["allowed_origins"] = ["http://127.0.0.1:18773"]
        with self.assertRaisesRegex(ValidationError, "application origin"):
            validate_plan(wrong_origin, profile)

    def test_older_plan_rejects_bootstrap_profile(self) -> None:
        plan = orchestration_plan()
        plan["bootstrap_profile"] = bootstrap_plan()["bootstrap_profile"]
        with self.assertRaisesRegex(ValidationError, "requires schema_version '0.6'"):
            validate_plan(plan)

    def test_seal_cli_requires_exact_profile_only_for_plan_v06(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = sealed_bootstrap_profile()
            profile_path = root / "sealed-profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(bootstrap_plan(profile)), encoding="utf-8")
            output = root / "sealed-plan.json"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "seal",
                        "--plan",
                        str(plan_path),
                        "--profile",
                        str(profile_path),
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(0, code)
            self.assertEqual("", stderr.getvalue())
            verify_sealed_plan(json.loads(output.read_text(encoding="utf-8")), profile)

            old_plan = root / "old-plan.json"
            old_plan.write_text(json.dumps(orchestration_plan()), encoding="utf-8")
            with redirect_stdout(io.StringIO()), redirect_stderr(stderr := io.StringIO()):
                code = main(
                    [
                        "seal",
                        "--plan",
                        str(old_plan),
                        "--profile",
                        str(profile_path),
                        "--output",
                        str(root / "must-not-exist.json"),
                    ]
                )
            self.assertEqual(2, code)
            self.assertIn("accepted only", stderr.getvalue())
            self.assertFalse((root / "must-not-exist.json").exists())


if __name__ == "__main__":
    unittest.main()
