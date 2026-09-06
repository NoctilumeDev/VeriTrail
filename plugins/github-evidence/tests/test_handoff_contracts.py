from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes

from veritrail_github.errors import ContractError
from veritrail_github.handoff_contracts import (
    handoff_manifest_digest,
    validate_handoff_manifest,
)


FIXTURE = (
    Path(__file__).parent / "fixtures" / "github-evidence-handoff-0.1.json"
)


def handoff_fixture() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class HandoffManifestContractTests(unittest.TestCase):
    def test_frozen_positive_vector_and_canonical_identity(self) -> None:
        manifest = handoff_fixture()
        self.assertEqual(validate_handoff_manifest(manifest), manifest)
        self.assertEqual(
            canonical_json_bytes(manifest),
            canonical_json_bytes(validate_handoff_manifest(manifest)),
        )
        self.assertEqual(
            handoff_manifest_digest(manifest),
            "5fc2018b4b28946fe37673b85d27baf2b779ce25cc92a3f01b18519ec6253b89",
        )

    def test_top_level_and_side_contract_are_closed(self) -> None:
        for path, field in (((), "plan_digest"), (("sides", 0), "coverage")):
            with self.subTest(path=path, field=field):
                manifest = handoff_fixture()
                target: Any = manifest
                for segment in path:
                    target = target[segment]
                target[field] = "must-not-enter-handoff"
                with self.assertRaisesRegex(ContractError, "unsupported fields"):
                    validate_handoff_manifest(manifest)

        non_string_key = handoff_fixture()
        non_string_key[1] = "not-a-json-object-key"
        with self.assertRaisesRegex(ContractError, "unsupported fields"):
            validate_handoff_manifest(non_string_key)

    def test_roles_are_complete_distinct_and_ordered(self) -> None:
        mutations = []

        missing = handoff_fixture()
        missing["sides"] = missing["sides"][:1]
        mutations.append(missing)

        duplicate = handoff_fixture()
        duplicate["sides"][1]["collector_role"] = "github-api"
        mutations.append(duplicate)

        reversed_sides = handoff_fixture()
        reversed_sides["sides"].reverse()
        mutations.append(reversed_sides)

        wrong_order = handoff_fixture()
        wrong_order["collection_order"].reverse()
        mutations.append(wrong_order)

        for manifest in mutations:
            with self.subTest(manifest=manifest):
                with self.assertRaises(ContractError):
                    validate_handoff_manifest(manifest)

    def test_unsafe_or_ambiguous_evidence_paths_are_rejected(self) -> None:
        invalid_paths = (
            "",
            ".",
            "..",
            "../evidence.json",
            "nested/evidence.json",
            "nested\\evidence.json",
            "/absolute.json",
            "C:\\absolute.json",
            "evidence.json.",
            "CON.json",
        )
        for value in invalid_paths:
            with self.subTest(value=value):
                manifest = handoff_fixture()
                manifest["sides"][0]["evidence_path"] = value
                with self.assertRaisesRegex(ContractError, "evidence_path"):
                    validate_handoff_manifest(manifest)

    def test_state_field_combinations_are_closed(self) -> None:
        valid = handoff_fixture()
        valid["sides"][0] = {
            "collector_role": "github-api",
            "state": "COLLECTED_NOT_PUBLISHED",
            "evidence_path": None,
            "evidence_sha256": "c" * 64,
            "error_code": "PUBLISH_ERROR",
        }
        valid["sides"][1] = {
            "collector_role": "github-public-render",
            "state": "MISSING",
            "evidence_path": None,
            "evidence_sha256": None,
            "error_code": "COLLECTION_ERROR",
        }
        self.assertEqual(validate_handoff_manifest(valid), valid)

        invalid = []
        for field, value in (
            ("evidence_path", None),
            ("evidence_sha256", None),
            ("error_code", "COLLECTION_ERROR"),
        ):
            manifest = handoff_fixture()
            manifest["sides"][0][field] = value
            invalid.append(manifest)

        missing_with_digest = copy.deepcopy(valid)
        missing_with_digest["sides"][1]["evidence_sha256"] = "d" * 64
        invalid.append(missing_with_digest)

        for manifest in invalid:
            with self.subTest(manifest=manifest):
                with self.assertRaises(ContractError):
                    validate_handoff_manifest(manifest)

    def test_digest_requires_lowercase_sha256_and_finite_json(self) -> None:
        uppercase = handoff_fixture()
        uppercase["sides"][0]["evidence_sha256"] = "A" * 64
        with self.assertRaisesRegex(ContractError, "lowercase SHA-256"):
            handoff_manifest_digest(uppercase)

        floating = handoff_fixture()
        floating["unexpected"] = 1.0
        with self.assertRaises(ContractError):
            handoff_manifest_digest(floating)


if __name__ == "__main__":
    unittest.main()
