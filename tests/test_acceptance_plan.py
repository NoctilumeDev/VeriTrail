from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from veritrail.acceptance_plan import (
    acceptance_plan_digest,
    load_and_seal_acceptance_plan,
    observation_spec_digest,
    seal_acceptance_plan,
    validate_acceptance_plan,
    verify_sealed_acceptance_plan,
    write_sealed_acceptance_plan,
)
from veritrail.errors import SafetyError, ValidationError
from veritrail.plan import seal_plan, validate_plan

from tests.support import (
    acceptance_plan,
    bootstrap_plan,
    browser_plan,
    command_plan,
    example_plan,
    orchestration_plan,
    preflight_plan,
    sealed_bootstrap_profile,
    sealed_single_bootstrap_profile,
    single_bootstrap_plan,
)


class AcceptancePlanTests(unittest.TestCase):
    def test_seal_is_stable_and_detects_mutation(self) -> None:
        first = seal_acceptance_plan(acceptance_plan())
        second = seal_acceptance_plan(acceptance_plan())
        self.assertEqual(first["seal"], second["seal"])
        verify_sealed_acceptance_plan(first)

        mutated = copy.deepcopy(first)
        mutated["assertions"][0]["right"] = "other"
        with self.assertRaisesRegex(ValidationError, "seal does not match"):
            verify_sealed_acceptance_plan(mutated)

    def test_spec_identity_excludes_plan_prose_governance_and_local_id(self) -> None:
        original = acceptance_plan()
        changed = copy.deepcopy(original)
        changed["question"] = "A different declared question"
        changed["governance"]["drafter_ref"] = "different-drafter"
        changed["observation_specs"][0]["id"] = "renamed-spec"
        changed["evidence_requirements"][0]["observation_spec_id"] = "renamed-spec"

        self.assertNotEqual(acceptance_plan_digest(original), acceptance_plan_digest(changed))
        self.assertEqual(
            observation_spec_digest(original["observation_specs"][0]),
            observation_spec_digest(changed["observation_specs"][0]),
        )

    def test_spec_identity_changes_with_semantic_observation(self) -> None:
        original = acceptance_plan()
        for mutation in ("coordinates", "projections", "contract"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(original)
                if mutation == "coordinates":
                    changed["observation_specs"][0]["coordinates"]["ref"] = "candidate-002"
                elif mutation == "projections":
                    changed["observation_specs"][0]["projections"].append("release_id")
                else:
                    changed["observation_specs"][0]["contract"]["version"] = "0.2"
                self.assertNotEqual(
                    observation_spec_digest(original["observation_specs"][0]),
                    observation_spec_digest(changed["observation_specs"][0]),
                )
                self.assertNotEqual(
                    acceptance_plan_digest(original), acceptance_plan_digest(changed)
                )

    def test_acceptance_and_experiment_plans_do_not_cross_validators(self) -> None:
        with self.assertRaisesRegex(ValidationError, "plan_kind"):
            validate_plan(acceptance_plan())

        missing_kind = acceptance_plan()
        del missing_kind["plan_kind"]
        with self.assertRaisesRegex(ValidationError, "plan_kind must be ACCEPTANCE"):
            validate_acceptance_plan(missing_kind)

        unknown_kind = acceptance_plan()
        unknown_kind["plan_kind"] = "OTHER"
        with self.assertRaisesRegex(ValidationError, "plan_kind must be ACCEPTANCE"):
            validate_acceptance_plan(unknown_kind)

        legacy = example_plan()
        legacy["plan_kind"] = "EXPERIMENT"
        with self.assertRaisesRegex(ValidationError, "plan_kind"):
            validate_plan(legacy)

    def test_causal_fields_float_and_sensitive_paths_are_rejected(self) -> None:
        for field in ("baseline", "variables", "random_seed", "load_model"):
            with self.subTest(field=field):
                plan = acceptance_plan()
                plan[field] = {}
                with self.assertRaisesRegex(ValidationError, "unsupported fields"):
                    validate_acceptance_plan(plan)

        floating = acceptance_plan()
        floating["observation_specs"][0]["coordinates"]["ratio"] = 0.5
        with self.assertRaisesRegex(ValidationError, "floating-point"):
            validate_acceptance_plan(floating)

        sensitive = acceptance_plan()
        sensitive["subject"]["source_ref"] = "C:\\Users\\alice\\project"
        with self.assertRaisesRegex(ValidationError, "personal paths"):
            validate_acceptance_plan(sensitive)

    def test_unknown_but_well_formed_contract_can_be_sealed(self) -> None:
        plan = acceptance_plan()
        plan["observation_specs"][0]["contract"] = {
            "id": "future.unknown-adapter",
            "version": "99.0",
        }
        sealed = seal_acceptance_plan(plan)
        verify_sealed_acceptance_plan(sealed)

    def test_malformed_contract_pointer_and_null_seal_are_rejected(self) -> None:
        missing_contract_version = acceptance_plan()
        del missing_contract_version["observation_specs"][0]["contract"]["version"]
        with self.assertRaisesRegex(ValidationError, "contract.version"):
            validate_acceptance_plan(missing_contract_version)

        malformed_pointer = acceptance_plan()
        malformed_pointer["assertions"][0]["left"]["path"] = "/facts/~2bad"
        with self.assertRaisesRegex(ValidationError, "invalid RFC 6901 escape"):
            validate_acceptance_plan(malformed_pointer)

        null_seal = acceptance_plan()
        null_seal["seal"] = None
        with self.assertRaisesRegex(ValidationError, "seal must contain"):
            validate_acceptance_plan(null_seal)

    def test_legacy_plan_digests_remain_on_the_core_0122_baseline(self) -> None:
        bootstrap_profile = sealed_bootstrap_profile()
        single_profile = sealed_single_bootstrap_profile()
        cases = (
            (example_plan(), None, "90235a18c59e9f30cd2aa519d281a4fdb18f04e83bdf2fcc5ff98770dba8a2b8"),
            (preflight_plan(), None, "df1966bbab8e1f6c0288525747ff96bd5c7d3e26120dbfafea8f27367324f41b"),
            (browser_plan(), None, "2a16769446e4eb617ab4fdd51b7b1eda9c7266654d5a991106416c9488c91fd7"),
            (orchestration_plan(), None, "6cdf3bdf15fe8572d756dee43d7431a81d61a7eb6547af696110e45c24cd120a"),
            (command_plan(), None, "ccae38efe3e6425e50a924634e8e507dced6b1e108a76ed3ca6f563788c9f5d6"),
            (bootstrap_plan(bootstrap_profile), bootstrap_profile, "f853820ac7c54922b7a2aba3c3656412e6bd51456bb80d3c9a882b2e408a9734"),
            (single_bootstrap_plan(single_profile), single_profile, "0196c22d68ca1c0b0c41bb338fd1062f02c6739eada23ef63b29245781d6e65a"),
        )
        for draft, profile, expected in cases:
            with self.subTest(schema_version=draft["schema_version"]):
                self.assertEqual(expected, seal_plan(draft, profile)["seal"]["digest"])

    def test_file_round_trip_is_strict_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.json"
            output = Path(directory) / "sealed.json"
            draft.write_bytes(json.dumps(acceptance_plan()).encode("utf-8"))
            sealed = load_and_seal_acceptance_plan(draft)
            write_sealed_acceptance_plan(output, sealed)
            self.assertEqual(sealed, load_and_seal_acceptance_plan(output))
            with self.assertRaisesRegex(SafetyError, "refusing to overwrite"):
                write_sealed_acceptance_plan(output, sealed)


if __name__ == "__main__":
    unittest.main()
