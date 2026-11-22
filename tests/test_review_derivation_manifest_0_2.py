from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas"
CORPUS_ROOT = (
    ROOT / "tests" / "fixtures" / "review-derivation-manifest-0.2"
)
LEGACY_SCHEMA_SHA256 = (
    "69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91"
)
ROLE_PATHS = {
    "SOURCE_SNAPSHOT": "source-snapshot.json",
    "REVIEW_POLICY": "review-policy.json",
    "DERIVATION_PROFILE": "derivation-profile.json",
    "DERIVATION_EVIDENCE": "derivation-evidence.json",
    "FACT_SET": "fact-set.json",
    "RELATION_SET": "relation-set.json",
    "REVIEW_SLICE_SET": "review-slices.json",
    "COVERAGE_LEDGER": "coverage-ledger.json",
}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(role: str, ordinal: int) -> dict[str, object]:
    return {
        "role": role,
        "path": ROLE_PATHS[role],
        "sha256": f"{ordinal + 1:064x}",
        "size_bytes": ordinal,
        "semantic_digest": f"{ordinal + 101:064x}",
    }


def manifest(roles: list[str], *, outcome: str = "COVERAGE") -> dict[str, object]:
    return {
        "bundle_kind": "R1_DERIVATION",
        "schema_version": "0.2",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "outcome_kind": outcome,
        "files": [entry(role, index) for index, role in enumerate(roles)],
    }


class ReviewDerivationManifest02SchemaTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load(
            SCHEMA_ROOT / "review-derivation-manifest-0.2.schema.json"
        )
        cls.common = load(SCHEMA_ROOT / "review-r1-common-0.1.schema.json")
        cls.legacy = load(
            SCHEMA_ROOT / "review-derivation-manifest-0.1.schema.json"
        )
        cls.registry = Registry().with_resources(
            [
                (value["$id"], Resource.from_contents(value))
                for value in (cls.schema, cls.common, cls.legacy)
            ]
        )
        cls.validator = Draft202012Validator(
            cls.schema,
            registry=cls.registry,
            format_checker=FormatChecker(),
        )
        cls.legacy_validator = Draft202012Validator(
            cls.legacy,
            registry=cls.registry,
            format_checker=FormatChecker(),
        )
        cls.corpus = load(CORPUS_ROOT / "compatibility-cases.json")

    def assert_rejects(self, value: object) -> None:
        self.assertTrue(list(self.validator.iter_errors(value)))

    def test_schema_is_closed_exact_0_2_and_legacy_bytes_are_immutable(self):
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(
            self.schema["$id"],
            "https://github.com/NoctilumeDev/VeriTrail/"
            "schemas/review-derivation-manifest-0.2.schema.json",
        )
        self.assertEqual(
            hashlib.sha256(
                (
                    SCHEMA_ROOT / "review-derivation-manifest-0.1.schema.json"
                ).read_bytes()
            ).hexdigest(),
            LEGACY_SCHEMA_SHA256,
        )
        value = manifest(
            [
                "SOURCE_SNAPSHOT",
                "REVIEW_POLICY",
                "DERIVATION_PROFILE",
                "DERIVATION_EVIDENCE",
                "COVERAGE_LEDGER",
            ]
        )
        self.validator.validate(value)
        for mutation in (
            {**value, "schema_version": "0.1"},
            {**value, "schema_version": "0.3"},
            {**value, "unexpected": True},
        ):
            self.assert_rejects(mutation)
        legacy_document = load(
            ROOT
            / "tests"
            / "fixtures"
            / "review-r1-schema-0.1"
            / "valid-complete"
            / "manifest.json"
        )
        self.legacy_validator.validate(legacy_document)
        rewritten_as_legacy = copy.deepcopy(value)
        rewritten_as_legacy["schema_version"] = "0.1"
        self.assertTrue(
            list(self.legacy_validator.iter_errors(rewritten_as_legacy))
        )

    def test_all_eight_contract_positive_topologies_validate(self):
        cases = self.corpus["positive_cases"]
        self.assertEqual(len(cases), 8)
        self.assertEqual(
            [case["case_id"] for case in cases],
            [
                "normal",
                "branch-empty",
                "slice-partial",
                "zero-parse-denominator",
                "all-parse-rejected",
                "projection-blocked",
                "required-provider-non-success",
                "qualified-unknown-fact-only",
            ],
        )
        for case in cases:
            with self.subTest(case=case["case_id"]):
                self.validator.validate(manifest(case["expected_roles"]))

    def test_complete_and_diagnostic_0_2_compatibility_branches_validate(self):
        complete_roles = list(ROLE_PATHS)
        diagnostic_roles = complete_roles[:4]
        self.validator.validate(manifest(complete_roles, outcome="COMPLETE"))
        self.validator.validate(
            manifest(diagnostic_roles, outcome="DIAGNOSTIC")
        )
        self.assert_rejects(manifest(diagnostic_roles, outcome="COMPLETE"))
        self.assert_rejects(manifest(complete_roles, outcome="DIAGNOSTIC"))

    def test_role_path_order_count_and_ledger_tail_are_structural(self):
        roles = self.corpus["positive_cases"][0]["expected_roles"]
        value = manifest(roles)
        mutations = []
        missing = copy.deepcopy(value)
        missing["files"].pop()
        mutations.append(missing)
        duplicate = copy.deepcopy(value)
        duplicate["files"][5] = copy.deepcopy(duplicate["files"][4])
        mutations.append(duplicate)
        swapped = copy.deepcopy(value)
        swapped["files"][-1], swapped["files"][-2] = (
            swapped["files"][-2],
            swapped["files"][-1],
        )
        mutations.append(swapped)
        wrong_path = copy.deepcopy(value)
        wrong_path["files"][0]["path"] = "../source-snapshot.json"
        mutations.append(wrong_path)
        extra = copy.deepcopy(value)
        extra["files"][0]["extra"] = True
        mutations.append(extra)
        for mutation in mutations:
            self.assert_rejects(mutation)

    def test_fixture_freezes_falsifier_denominator_and_world_separation(self):
        self.assertEqual(
            [item["id"] for item in self.corpus["falsifiers"]],
            [f"RDMC-{index:03d}" for index in range(14)],
        )
        compatibility = next(
            item
            for item in self.corpus["positive_cases"]
            if item["case_id"] == "qualified-unknown-fact-only"
        )
        self.assertEqual(
            compatibility["expected_roles"],
            [
                "SOURCE_SNAPSHOT",
                "REVIEW_POLICY",
                "DERIVATION_PROFILE",
                "DERIVATION_EVIDENCE",
                "FACT_SET",
                "COVERAGE_LEDGER",
            ],
        )
        self.assertEqual(
            self.corpus["live_relation_conflict_roles"],
            [
                "SOURCE_SNAPSHOT",
                "REVIEW_POLICY",
                "DERIVATION_PROFILE",
                "DERIVATION_EVIDENCE",
                "FACT_SET",
                "RELATION_SET",
                "COVERAGE_LEDGER",
            ],
        )
        self.assertNotEqual(
            compatibility["expected_roles"],
            self.corpus["live_relation_conflict_roles"],
        )


if __name__ == "__main__":
    unittest.main()
