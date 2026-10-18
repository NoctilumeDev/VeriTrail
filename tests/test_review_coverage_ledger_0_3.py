from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SRC = ROOT / "plugins" / "review-attention" / "src"
if str(PLUGIN_SRC) not in sys.path:
    sys.path.insert(0, str(PLUGIN_SRC))

from veritrail_review._review_coverage_ledger_conformance import (  # noqa: E402
    LEDGER_DIGEST_DOMAIN,
    ROOT_CHAIN_DOMAIN,
    CoverageLedgerConformanceError,
    CoverageLedgerConformanceFailureCode,
    bind_coverage_ledger_conformance_source,
    validate_review_coverage_ledger,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402


SCHEMA_ROOT = ROOT / "schemas"
CORPUS_ROOT = ROOT / "tests" / "fixtures" / "review-coverage-ledger-0.3"
OLD_CORPUS_ROOT = ROOT / "tests" / "fixtures" / "review-r1-schema-0.1"
FROZEN_FILES = {
    "schemas/review-coverage-ledger-0.1.schema.json": "e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545",
    "schemas/review-r1-common-0.1.schema.json": "e36f0d4ba494645bc991736b780c2c5354be13789466ab82d72b4963c674da4a",
    "schemas/review-derivation-manifest-0.1.schema.json": "69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91",
}
OLD_CORPUS_BYTE_MANIFEST = "3b892301545fbe4ab77e52749c79f80881bb5d8da3cdb52c7e181a530381be9e"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def old_corpus_byte_manifest() -> str:
    digest = hashlib.sha256()
    files = sorted(path for path in OLD_CORPUS_ROOT.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(OLD_CORPUS_ROOT).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def source_for(case: dict[str, object], *, stages=None, projections=None, safe=True):
    source = case["source"]
    return bind_coverage_ledger_conformance_source(
        fact_handoff_source_digest=source["fact_handoff_source_digest"],
        root_binding_projections=(
            projections if projections is not None else source["root_binding_projections"]
        ),
        stage_projections=stages if stages is not None else source["stage_projections"],
        authority_safe=safe,
    )


def refresh_ledger_digest(document: dict[str, object]) -> None:
    unsigned = copy.deepcopy(document)
    unsigned.pop("coverage_ledger_digest", None)
    document["coverage_ledger_digest"] = semantic_digest(LEDGER_DIGEST_DOMAIN, unsigned)


def refresh_root_chain_digest(document: dict[str, object]) -> None:
    payload = {
        "root_binding_function": document["root_binding_function"],
        "root_chain_domain": document["root_chain_domain"],
        "root_bindings": document["root_bindings"],
    }
    document["root_chain_digest"] = semantic_digest(ROOT_CHAIN_DOMAIN, payload)
    refresh_ledger_digest(document)


class ReviewCoverageLedger03Tests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_ROOT / "review-coverage-ledger-0.3.schema.json")
        cls.old_schema = load_json(SCHEMA_ROOT / "review-coverage-ledger-0.1.schema.json")
        cls.common_schema = load_json(SCHEMA_ROOT / "review-r1-common-0.1.schema.json")
        cls.manifest_schema = load_json(SCHEMA_ROOT / "review-derivation-manifest-0.1.schema.json")
        cls.registry = Registry().with_resources(
            [
                (schema["$id"], Resource.from_contents(schema))
                for schema in (cls.schema, cls.old_schema, cls.common_schema, cls.manifest_schema)
            ]
        )
        cls.validator = Draft202012Validator(
            cls.schema, registry=cls.registry, format_checker=FormatChecker()
        )
        cls.old_validator = Draft202012Validator(
            cls.old_schema, registry=cls.registry, format_checker=FormatChecker()
        )
        cls.manifest_validator = Draft202012Validator(
            cls.manifest_schema, registry=cls.registry, format_checker=FormatChecker()
        )
        cls.corpus = load_json(CORPUS_ROOT / "compatibility-cases.json")
        cls.cases = {case["case_id"]: case for case in cls.corpus["positive_cases"]}

    def assert_schema_rejects(self, document: dict[str, object]) -> None:
        self.assertTrue(list(self.validator.iter_errors(document)))

    def assert_conformance_rejects(
        self,
        document: dict[str, object],
        source,
        code: CoverageLedgerConformanceFailureCode | None = None,
    ) -> None:
        with self.assertRaises(CoverageLedgerConformanceError) as caught:
            validate_review_coverage_ledger(document, source)
        if code is not None:
            self.assertIs(caught.exception.code, code)

    def test_schema_is_closed_exact_0_3_child(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(
            self.schema["$id"],
            "https://github.com/NoctilumeDev/VeriTrail/schemas/review-coverage-ledger-0.3.schema.json",
        )
        self.assertEqual(self.schema["properties"]["schema_version"], {"const": "0.3"})
        self.assertFalse(self.schema["additionalProperties"])
        for old_root in ("fact_set_digest", "relation_set_digest", "slice_set_digest"):
            self.assertNotIn(old_root, self.schema["properties"])
        self.assertEqual(
            self.schema["$defs"]["CoverageReason"]["enum"][-1],
            "UNREPRESENTABLE_EXPECTED_FACT",
        )

    def test_positive_worlds_validate_and_recompute_exact_identities(self) -> None:
        self.assertEqual(
            list(self.cases),
            [
                "normal",
                "branch_empty",
                "slice_partial",
                "zero_parse_denominator",
                "all_parse_rejected",
                "projection_blocked",
                "required_provider_non_success",
                "qualified_unknown",
            ],
        )
        identities = set()
        for name, case in self.cases.items():
            with self.subTest(world=name):
                document = case["document"]
                self.validator.validate(document)
                validate_review_coverage_ledger(document, source_for(case))
                unsigned = copy.deepcopy(document)
                unsigned.pop("coverage_ledger_digest")
                self.assertEqual(
                    document["coverage_ledger_digest"],
                    semantic_digest(LEDGER_DIGEST_DOMAIN, unsigned),
                )
                self.assertEqual(
                    document["coverage_ledger_digest"],
                    case["expected_coverage_ledger_digest"],
                )
                identities.add(document["root_chain_digest"])
        self.assertEqual(len(identities), len(self.cases))

    def test_rscsc_000_and_full_historical_bytes_are_guarded(self) -> None:
        for relative, expected in FROZEN_FILES.items():
            with self.subTest(path=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)
        self.assertEqual(len([p for p in OLD_CORPUS_ROOT.rglob("*") if p.is_file()]), 19)
        self.assertEqual(old_corpus_byte_manifest(), OLD_CORPUS_BYTE_MANIFEST)

    def test_rscsc_001_to_004_shape_falsifiers(self) -> None:
        base = self.cases["projection_blocked"]["document"]
        vectors = {}
        value = copy.deepcopy(base)
        del value["stages"][4]["blocked"]
        vectors["RSCSC-001"] = value
        value = copy.deepcopy(base)
        del value["stages"][4]["blocked"][0]["disposition_family"]
        vectors["RSCSC-002"] = value
        value = copy.deepcopy(base)
        value["stages"][4]["blocked"][0]["reason_codes"] = ["DERIVATION_ERROR"]
        vectors["RSCSC-003"] = value
        value = copy.deepcopy(base)
        value["stages"][5]["blocked"] = copy.deepcopy(value["stages"][4]["blocked"])
        vectors["RSCSC-004"] = value
        for falsifier_id, document in vectors.items():
            with self.subTest(falsifier=falsifier_id):
                self.assert_schema_rejects(document)

    def test_rscsc_005_to_011_cross_field_falsifiers(self) -> None:
        base = self.cases["projection_blocked"]
        vectors: dict[str, dict[str, object]] = {}

        value = copy.deepcopy(base["document"])
        value["stages"][4]["blocked"][0]["item_ref"]["item_id"] = "f" * 64
        vectors["RSCSC-005"] = value
        value = copy.deepcopy(base["document"])
        value["stages"][4]["completed"].append(
            copy.deepcopy(value["stages"][4]["blocked"][0]["item_ref"])
        )
        value["stages"][4]["completed"].sort(key=lambda item: item["item_id"])
        vectors["RSCSC-006"] = value
        value = copy.deepcopy(base["document"])
        value["stages"][4]["blocked"].append(copy.deepcopy(value["stages"][4]["blocked"][0]))
        vectors["RSCSC-007"] = value
        value = copy.deepcopy(base["document"])
        value["stages"][4]["coverage_status"] = "COMPLETE"
        vectors["RSCSC-008"] = value
        value = copy.deepcopy(base["document"])
        value["stages"][5]["coverage_status"] = "COMPLETE"
        vectors["RSCSC-009"] = value
        value = copy.deepcopy(base["document"])
        value["stages"][4]["reason_codes"] = []
        vectors["RSCSC-010"] = value
        value = copy.deepcopy(self.cases["required_provider_non_success"]["document"])
        value["stages"][4]["execution_failed"].reverse()
        vectors["RSCSC-011"] = value
        for falsifier_id, document in vectors.items():
            with self.subTest(falsifier=falsifier_id):
                refresh_ledger_digest(document)
                stages = document["stages"]
                source = source_for(base, stages=stages)
                if falsifier_id == "RSCSC-007":
                    self.assert_schema_rejects(document)
                else:
                    self.validator.validate(document)
                    self.assert_conformance_rejects(document, source)

    def test_rscsc_012_old_digest_domain_is_rejected(self) -> None:
        case = self.cases["normal"]
        value = copy.deepcopy(case["document"])
        unsigned = copy.deepcopy(value)
        unsigned.pop("coverage_ledger_digest")
        value["coverage_ledger_digest"] = semantic_digest(
            "veritrail.review.coverage-ledger/0.1", unsigned
        )
        self.validator.validate(value)
        self.assert_conformance_rejects(
            value,
            source_for(case),
            CoverageLedgerConformanceFailureCode.INVALID_LEDGER_DIGEST,
        )

    def test_rscsc_013_014_and_h_exact_version_dispatch(self) -> None:
        case = self.cases["normal"]
        for falsifier_id, version in (
            ("RSCSC-013", "0.4"),
            ("RSCSC-014", "0.2"),
        ):
            value = copy.deepcopy(case["document"])
            value["schema_version"] = version
            with self.subTest(falsifier=falsifier_id):
                self.assert_conformance_rejects(
                    value,
                    source_for(case),
                    CoverageLedgerConformanceFailureCode.UNKNOWN_CHILD_VERSION,
                )
        self.assertTrue(list(self.old_validator.iter_errors(case["document"])))

    def test_rscsc_015_foreign_attempt_provenance_is_rejected(self) -> None:
        case = self.cases["normal"]
        projections = copy.deepcopy(case["source"]["root_binding_projections"])
        projections[1]["terminal_history_projection"]["same_attempt_source"] = "f" * 64
        self.assert_conformance_rejects(
            case["document"],
            source_for(case, projections=projections),
            CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE,
        )

    def test_terminal_history_members_must_be_canonical(self) -> None:
        case = self.cases["qualified_unknown"]
        projections = copy.deepcopy(case["source"]["root_binding_projections"])
        projections[1]["terminal_history_projection"]["history"].reverse()
        self.assert_conformance_rejects(
            case["document"],
            source_for(case, projections=projections),
            CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE,
        )

    def test_terminal_history_cannot_omit_an_applicable_member(self) -> None:
        case = self.cases["projection_blocked"]
        projections = copy.deepcopy(case["source"]["root_binding_projections"])
        projections[0]["terminal_history_projection"]["history"] = [
            member
            for member in projections[0]["terminal_history_projection"]["history"]
            if member["name"] != "blockers"
        ]
        self.assert_conformance_rejects(
            case["document"],
            source_for(case, projections=projections),
            CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE,
        )

    def test_terminal_history_predecessor_is_recomputed_not_self_reported(self) -> None:
        case = self.cases["normal"]
        projections = copy.deepcopy(case["source"]["root_binding_projections"])
        history = projections[1]["terminal_history_projection"]["history"]
        next(member for member in history if member["name"] == "predecessor_binding")[
            "value"
        ] = "f" * 64
        self.assert_conformance_rejects(
            case["document"],
            source_for(case, projections=projections),
            CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE,
        )

    def test_unknown_stage_observations_cannot_escape_known_prefix(self) -> None:
        case = self.cases["qualified_unknown"]
        stages = copy.deepcopy(case["source"]["stage_projections"])
        stages[5]["eligible"] = [
            {"item_id": "f" * 64, "item_kind": "RELATION"}
        ]
        stages[5]["completed"] = copy.deepcopy(stages[5]["eligible"])
        value = copy.deepcopy(case["document"])
        value["stages"] = stages
        refresh_ledger_digest(value)
        self.validator.validate(value)
        self.assert_conformance_rejects(
            value,
            source_for(case, stages=stages),
            CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION,
        )

    def test_rscsc_016_schema_witness_does_not_replace_conformance(self) -> None:
        case = self.cases["projection_blocked"]
        value = copy.deepcopy(case["document"])
        value["stages"][4]["coverage_status"] = "COMPLETE"
        refresh_ledger_digest(value)
        self.validator.validate(value)
        self.assert_conformance_rejects(
            value,
            source_for(case, stages=value["stages"]),
            CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION,
        )

    def test_rbcc_000_state_artifact_contradiction_is_schema_rejected(self) -> None:
        value = copy.deepcopy(self.cases["normal"]["document"])
        value["root_bindings"][0]["binding_state"] = "QUALIFIED_ABSENT"
        self.assert_schema_rejects(value)

    def test_rbcc_001_002_negative_world_identities_remain_distinct(self) -> None:
        self.assertNotEqual(
            self.cases["zero_parse_denominator"]["document"]["root_chain_digest"],
            self.cases["all_parse_rejected"]["document"]["root_chain_digest"],
        )
        self.assertNotEqual(
            self.cases["projection_blocked"]["document"]["root_chain_digest"],
            self.cases["required_provider_non_success"]["document"]["root_chain_digest"],
        )

    def test_rbcc_003_foreign_relation_and_slice_transplant_is_rejected(self) -> None:
        case = self.cases["projection_blocked"]
        value = copy.deepcopy(case["document"])
        value["root_bindings"][1:] = copy.deepcopy(
            self.cases["normal"]["document"]["root_bindings"][1:]
        )
        refresh_root_chain_digest(value)
        self.validator.validate(value)
        self.assert_conformance_rejects(
            value,
            source_for(case),
            CoverageLedgerConformanceFailureCode.INVALID_ROOT_CHAIN,
        )

    def test_rbcc_004_branch_empty_is_present_not_absent(self) -> None:
        case = self.cases["branch_empty"]
        self.assertEqual(case["document"]["root_bindings"][2]["binding_state"], "ARTIFACT_PRESENT")
        value = copy.deepcopy(case["document"])
        value["root_bindings"][2]["binding_state"] = "QUALIFIED_ABSENT"
        self.assert_schema_rejects(value)

    def test_rbcc_005_unknown_cannot_be_promoted(self) -> None:
        case = self.cases["qualified_unknown"]
        value = copy.deepcopy(case["document"])
        value["root_bindings"][2] = copy.deepcopy(
            self.cases["zero_parse_denominator"]["document"]["root_bindings"][2]
        )
        refresh_root_chain_digest(value)
        self.validator.validate(value)
        self.assert_conformance_rejects(value, source_for(case))

    def test_rbcc_006_007_semantic_bytes_do_not_grant_live_authority(self) -> None:
        case = self.cases["normal"]
        self.assert_conformance_rejects(
            case["document"],
            source_for(case, safe=False),
            CoverageLedgerConformanceFailureCode.UNSAFE_AUTHORITY_SOURCE,
        )
        source = source_for(case)
        self.assertEqual(
            [name for name in dir(source) if not name.startswith("_")],
            ["document_copy"],
        )

    def test_rbcc_008_rejects_closest_version_fallback(self) -> None:
        case = self.cases["normal"]
        value = copy.deepcopy(case["document"])
        value["schema_version"] = "0.2"
        self.assert_conformance_rejects(
            value,
            source_for(case),
            CoverageLedgerConformanceFailureCode.UNKNOWN_CHILD_VERSION,
        )

    def test_rbcc_009_manifest_0_1_does_not_publish_negative_child(self) -> None:
        manifest = load_json(OLD_CORPUS_ROOT / "valid-complete" / "manifest.json")
        coverage = next(item for item in manifest["files"] if item["role"] == "COVERAGE_LEDGER")
        negative = self.cases["projection_blocked"]["document"]
        raw = canonical_json_bytes(negative) + b"\n"
        coverage = copy.deepcopy(coverage)
        coverage["sha256"] = hashlib.sha256(raw).hexdigest()
        coverage["size_bytes"] = len(raw)
        coverage["semantic_digest"] = negative["coverage_ledger_digest"]
        manifest["files"] = [
            item
            for item in manifest["files"]
            if item["role"] in {
                "SOURCE_SNAPSHOT",
                "REVIEW_POLICY",
                "DERIVATION_PROFILE",
                "DERIVATION_EVIDENCE",
            }
        ] + [coverage]
        self.assertTrue(list(self.manifest_validator.iter_errors(manifest)))

    def test_rbcc_010_binding_order_or_predecessor_change_is_rejected(self) -> None:
        case = self.cases["normal"]
        for mutation in ("swap", "predecessor"):
            value = copy.deepcopy(case["document"])
            if mutation == "swap":
                value["root_bindings"][1], value["root_bindings"][2] = (
                    value["root_bindings"][2],
                    value["root_bindings"][1],
                )
            else:
                value["root_bindings"][1]["predecessor_binding_digest"] = "f" * 64
            refresh_root_chain_digest(value)
            with self.subTest(mutation=mutation):
                if mutation == "swap":
                    self.assert_schema_rejects(value)
                else:
                    self.validator.validate(value)
                    self.assert_conformance_rejects(value, source_for(case))

    def test_rbcc_011_root_chain_does_not_own_coverage_status(self) -> None:
        case = self.cases["normal"]
        value = copy.deepcopy(case["document"])
        original_root = copy.deepcopy(value["root_bindings"])
        value["stages"][6]["coverage_status"] = "PARTIAL"
        refresh_ledger_digest(value)
        self.assertEqual(value["root_bindings"], original_root)
        self.validator.validate(value)
        self.assert_conformance_rejects(
            value,
            source_for(case, stages=value["stages"]),
            CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION,
        )

    def test_all_normative_falsifier_ids_are_directly_accounted_for(self) -> None:
        expected = {
            *[f"RSCSC-{index:03d}" for index in range(17)],
            *[f"RBCC-{index:03d}" for index in range(12)],
        }
        self.assertEqual(set(self.corpus["falsifier_ids"]), expected)


if __name__ == "__main__":
    unittest.main()
