from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas"

LEGACY_BYTE_GUARDS = {
    "review-derivation-evidence-0.2.schema.json": (
        "66190e12fad8c3bbec3615c25b1bbaf3cfb1ef723267e0e99185dcf05b8238e6"
    ),
    "review-derivation-manifest-0.1.schema.json": (
        "69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91"
    ),
}


def load(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def semantic_digest(domain: str, payload: object) -> str:
    encoded = json.dumps(
        {"domain": domain, "payload": payload},
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class ReviewR1DerivationEvidence03SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load("review-derivation-evidence-0.3.schema.json")
        cls.common = load("review-r1-common-0.1.schema.json")
        cls.validator = Draft202012Validator(
            cls.schema,
            registry=Registry().with_resources(
                [
                    (value["$id"], Resource.from_contents(value))
                    for value in (cls.schema, cls.common)
                ]
            ),
            format_checker=FormatChecker(),
        )
        cls.normal = {
            "artifact_kind": "DERIVATION_EVIDENCE",
            "schema_version": "0.3",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "derivation_id": "derivation-1",
            "request_provenance": {
                "requested_repository_id": "repo-1",
                "requested_ref": "oid:sha1:" + "1" * 40,
                "resolver_id": "veritrail-r1-owned-snapshot-exact-oid",
                "resolver_version": "0.1",
                "resolved_at": "2026-11-17T00:00:00.000000Z",
            },
            "source_snapshot_digest": "1" * 64,
            "policy_digest": "2" * 64,
            "analysis_scope_digest": "3" * 64,
            "slice_policy_digest": "4" * 64,
            "derivation_profile_digest": "5" * 64,
            "terminal_branch": "NORMAL_FULFILLED",
            "selector_route": "RELATION_HANDOFF",
            "continuity_variant": "NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY",
            "continuity_digest": "6" * 64,
            "application_admission_digest": "7" * 64,
            "coverage_ledger_digest": "8" * 64,
            "root_chain_digest": "9" * 64,
        }
        cls.normal["derivation_evidence_digest"] = semantic_digest(
            "veritrail.review.derivation-evidence/0.3", cls.normal
        )

    def test_schema_is_closed_explicit_and_offline(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        self.assertFalse(self.schema["additionalProperties"])
        self.assertEqual(self.schema["properties"]["schema_version"], {"const": "0.3"})
        self.assertEqual(
            self.schema["$id"],
            "https://github.com/NoctilumeDev/VeriTrail/schemas/review-derivation-evidence-0.3.schema.json",
        )
        self.validator.validate(self.normal)

    def test_normal_and_four_negative_discriminants_are_mutually_bounded(self) -> None:
        for branch in (
            "ZERO_PARSE_DENOMINATOR",
            "ALL_PARSE_REJECTED",
            "PROJECTION_BLOCKED",
            "REQUIRED_PROVIDER_NON_SUCCESS",
        ):
            value = copy.deepcopy(self.normal)
            value["terminal_branch"] = branch
            value["selector_route"] = "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"
            value["continuity_variant"] = "NEGATIVE_WORLD_COVERAGE_CONTINUITY"
            value["derivation_evidence_digest"] = semantic_digest(
                "veritrail.review.derivation-evidence/0.3",
                {
                    key: item
                    for key, item in value.items()
                    if key != "derivation_evidence_digest"
                },
            )
            self.validator.validate(value)
        wrong = copy.deepcopy(self.normal)
        wrong["continuity_variant"] = "NEGATIVE_WORLD_COVERAGE_CONTINUITY"
        self.assertTrue(list(self.validator.iter_errors(wrong)))

    def test_legacy_versions_do_not_validate_as_0_3(self) -> None:
        for version in ("0.1", "0.1.1", "0.2", "9.9"):
            value = copy.deepcopy(self.normal)
            value["schema_version"] = version
            self.assertTrue(list(self.validator.iter_errors(value)))

    def test_legacy_evidence_and_manifest_bytes_remain_exact(self) -> None:
        for name, expected in LEGACY_BYTE_GUARDS.items():
            self.assertEqual(
                hashlib.sha256((SCHEMA_ROOT / name).read_bytes()).hexdigest(),
                expected,
            )


if __name__ == "__main__":
    unittest.main()
