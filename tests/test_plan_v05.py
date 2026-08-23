from __future__ import annotations

import copy
import unittest

from veritrail.errors import ValidationError
from veritrail.plan import seal_plan, validate_plan, verify_sealed_plan

from tests.support import command_plan, orchestration_plan


class PlanV05Tests(unittest.TestCase):
    def test_hardened_plan_v04_hash_is_stable(self) -> None:
        self.assertEqual(
            "6cdf3bdf15fe8572d756dee43d7431a81d61a7eb6547af696110e45c24cd120a",
            seal_plan(orchestration_plan())["seal"]["digest"],
        )

    def test_command_plan_seals_and_detects_policy_mutation(self) -> None:
        sealed = seal_plan(command_plan())
        verify_sealed_plan(sealed)
        mutated = copy.deepcopy(sealed)
        mutated["command"]["timeout_ms"] += 1
        with self.assertRaisesRegex(ValidationError, "seal does not match"):
            verify_sealed_plan(mutated)

    def test_plan_v05_requires_command_evidence_and_decisive_assertion(self) -> None:
        missing_evidence = command_plan()
        missing_evidence["required_evidence"].remove("runtime.command")
        with self.assertRaisesRegex(ValidationError, "must require runtime.command"):
            validate_plan(missing_evidence)

        missing_assertion = command_plan()
        for assertion in missing_assertion["assertions"]:
            if assertion["evidence_type"] == "runtime.command":
                assertion["severity"] = "OBSERVATION"
        with self.assertRaisesRegex(
            ValidationError, "decisive assertion over runtime.command"
        ):
            validate_plan(missing_assertion)

    def test_command_policy_rejects_unsafe_or_ambiguous_values(self) -> None:
        cases = {
            "unsupported adapter": lambda plan: plan["command"].update(adapter="SHELL"),
            "shell entry": lambda plan: plan["command"]["arguments"].append(
                {"literal": "-c"}
            ),
            "ambiguous argument": lambda plan: plan["command"]["arguments"].append(
                {"literal": "tests", "run_work_path": ["results"]}
            ),
            "personal path": lambda plan: plan["command"]["arguments"].append(
                {"literal": "C:\\Users\\example\\secret.txt"}
            ),
            "unsafe workdir": lambda plan: plan["command"].update(
                working_directory="../outside"
            ),
            "reserved workdir": lambda plan: plan["command"].update(
                working_directory="CON"
            ),
            "duplicate environment": lambda plan: plan["command"]["environment"].update(
                inherit=["SYSTEMROOT", "systemroot"]
            ),
            "arbitrary environment": lambda plan: plan["command"]["environment"].update(
                set={"PYTHONPATH": "plugins"}
            ),
            "unsorted exit": lambda plan: plan["command"].update(
                expected_exit_codes=[1, 0]
            ),
            "overlapping roots": lambda plan: plan["command"].update(
                subject_watch_roots=["src", "src/veritrail"]
            ),
            "reserved run path": lambda plan: plan["command"]["arguments"].append(
                {"run_work_path": ["NUL", "result.json"]}
            ),
            "non-string run path": lambda plan: plan["command"]["arguments"].append(
                {"run_work_path": [1]}
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                plan = command_plan()
                mutate(plan)
                with self.assertRaises(ValidationError):
                    validate_plan(plan)

    def test_command_policy_rejects_attached_inline_programs(self) -> None:
        for binding, literal in (
            ("python", "-cprint('bypass')"),
            ("python", "-icprint('cluster bypass')"),
            ("python", "-qcprint('cluster bypass')"),
            ("node", "-econsole.log('bypass')"),
            ("node", "--eval=1+1"),
            ("node", "--loader"),
            ("node", "--experimental-loader"),
        ):
            with self.subTest(binding=binding, literal=literal):
                plan = command_plan()
                plan["command"]["tool_binding"] = binding
                plan["command"]["arguments"].append({"literal": literal})
                with self.assertRaisesRegex(ValidationError, "forbidden inline"):
                    validate_plan(plan)

    def test_typed_run_work_path_is_sealed_without_an_absolute_value(self) -> None:
        plan = command_plan()
        plan["command"]["arguments"].append(
            {"run_work_path": ["results", "summary.json"]}
        )
        sealed = seal_plan(plan)
        self.assertEqual(
            ["results", "summary.json"],
            sealed["command"]["arguments"][-1]["run_work_path"],
        )

    def test_older_plan_rejects_command_contract(self) -> None:
        plan = orchestration_plan()
        plan["command"] = command_plan()["command"]
        with self.assertRaisesRegex(ValidationError, "command requires schema_version '0.5'"):
            validate_plan(plan)


if __name__ == "__main__":
    unittest.main()
