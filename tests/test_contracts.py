from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from veritrail.errors import ValidationError
from veritrail.plan import load_json_object, seal_plan, validate_plan, verify_sealed_plan

from tests.support import ROOT, example_plan


class ContractTests(unittest.TestCase):
    def test_public_schemas_are_valid_json_documents(self) -> None:
        for path in sorted((ROOT / "schemas").glob("*.json")):
            with self.subTest(schema=path.name), path.open("r", encoding="utf-8") as handle:
                schema = json.load(handle)
                self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
                self.assertIn("title", schema)

    def test_plan_seal_is_stable_and_detects_mutation(self) -> None:
        first = seal_plan(example_plan())
        second = seal_plan(example_plan())
        self.assertEqual(first["seal"], second["seal"])
        verify_sealed_plan(first)

        mutated = copy.deepcopy(first)
        mutated["assertions"][0]["expected"] = False
        with self.assertRaisesRegex(ValidationError, "seal does not match"):
            verify_sealed_plan(mutated)

    def test_single_variable_plan_rejects_second_primary(self) -> None:
        plan = example_plan()
        plan["variables"][1]["role"] = "PRIMARY"
        with self.assertRaisesRegex(ValidationError, "exactly one PRIMARY"):
            validate_plan(plan)

    def test_ambiguous_concurrency_is_rejected(self) -> None:
        plan = example_plan()
        plan["load_model"] = {"concurrency": 1000}
        with self.assertRaisesRegex(ValidationError, "concurrency is ambiguous"):
            validate_plan(plan)

    def test_l2_scope_requires_consumers(self) -> None:
        plan = example_plan()
        plan["change_scope"]["consumers"] = []
        with self.assertRaisesRegex(ValidationError, "enumerate at least one consumer"):
            validate_plan(plan)

    def test_unknown_nested_contract_field_is_rejected(self) -> None:
        plan = example_plan()
        plan["variables"][0]["surprise"] = True
        with self.assertRaisesRegex(ValidationError, "unsupported fields: surprise"):
            validate_plan(plan)

    def test_personal_path_is_rejected_before_plan_sealing(self) -> None:
        plan = example_plan()
        plan["subject"]["source_ref"] = "C:\\Users\\alice\\project"
        with self.assertRaisesRegex(ValidationError, "personal path"):
            validate_plan(plan)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"schema_version":"0.1","schema_version":"0.2"}', encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "duplicate object key"):
                load_json_object(path)


if __name__ == "__main__":
    unittest.main()
