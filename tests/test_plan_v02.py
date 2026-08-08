from __future__ import annotations

import copy
import unittest

from veritrail.errors import ValidationError
from veritrail.plan import seal_plan, validate_plan, verify_sealed_plan

from tests.support import example_plan, preflight_plan


class PlanV02Tests(unittest.TestCase):
    def test_m0_plan_hash_remains_frozen(self) -> None:
        sealed = seal_plan(example_plan())
        self.assertEqual(
            "90235a18c59e9f30cd2aa519d281a4fdb18f04e83bdf2fcc5ff98770dba8a2b8",
            sealed["seal"]["digest"],
        )

    def test_preflight_plan_seals_and_detects_threshold_mutation(self) -> None:
        sealed = seal_plan(preflight_plan())
        verify_sealed_plan(sealed)
        mutated = copy.deepcopy(sealed)
        mutated["preflight"]["available_memory_soft_min_mb"] += 1
        with self.assertRaisesRegex(ValidationError, "seal does not match"):
            verify_sealed_plan(mutated)

    def test_plan_v01_rejects_preflight_field(self) -> None:
        plan = example_plan()
        plan["preflight"] = preflight_plan()["preflight"]
        with self.assertRaisesRegex(ValidationError, "requires schema_version '0.2'"):
            validate_plan(plan)

    def test_plan_v02_requires_preflight_evidence_and_assertion(self) -> None:
        missing_evidence = preflight_plan()
        missing_evidence["required_evidence"] = ["automated.test-summary"]
        with self.assertRaisesRegex(ValidationError, "must require runtime.preflight"):
            validate_plan(missing_evidence)

        missing_assertion = preflight_plan()
        for assertion in missing_assertion["assertions"]:
            assertion["evidence_type"] = "automated.test-summary"
        with self.assertRaisesRegex(ValidationError, "assertion over runtime.preflight"):
            validate_plan(missing_assertion)

    def test_invalid_preflight_policies_are_rejected(self) -> None:
        cases = {
            "soft below hard": lambda policy: policy.update(
                available_memory_soft_min_mb=100,
                available_memory_hard_min_mb=200,
            ),
            "grace beyond sample count": lambda policy: policy.update(
                sample_count=2,
                hard_breach_grace_samples=3,
            ),
            "sampling window too long": lambda policy: policy.update(
                sample_count=20,
                sampling_interval_ms=5000,
            ),
            "too many samples": lambda policy: policy.update(sample_count=21),
            "observer soft above collector hard": lambda policy: policy.update(
                observer_rss_delta_soft_max_mb=513,
                collector_rss_hard_max_mb=512,
            ),
            "duplicate port": lambda policy: policy.update(
                ports=[
                    {"port": 43210, "expected": "FREE"},
                    {"port": 43210, "expected": "LISTENING"},
                ]
            ),
            "out of range port": lambda policy: policy.update(
                ports=[{"port": 70000, "expected": "FREE"}]
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                plan = preflight_plan()
                mutate(plan["preflight"])
                with self.assertRaises(ValidationError):
                    validate_plan(plan)

    def test_plan_v02_rejects_legacy_ambiguous_memory_fields(self) -> None:
        plan = preflight_plan()
        plan["resource_budget"]["memory_soft_mb"] = 512
        with self.assertRaisesRegex(ValidationError, "unsupported fields: memory_soft_mb"):
            validate_plan(plan)


if __name__ == "__main__":
    unittest.main()
