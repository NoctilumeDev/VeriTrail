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
CORPUS_ROOT = ROOT / "tests" / "fixtures" / "review-r1-derivation-evidence-0.1.1"
OLD_CORPUS_ROOT = ROOT / "tests" / "fixtures" / "review-r1-schema-0.1"
IDENTITY_DOMAIN = "veritrail.review.derivation-evidence/0.1"

FROZEN_0_1_SHA256 = {
    "schemas/review-coverage-ledger-0.1.schema.json": "e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545",
    "schemas/review-derivation-evidence-0.1.schema.json": "2efbd1d4f73f20fb045c2110136e7f3089e07408b9d496f59c30492a2c3666e7",
    "schemas/review-derivation-manifest-0.1.schema.json": "69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91",
    "schemas/review-derivation-profile-0.1.schema.json": "cd2995c30ce2529ae60a2673c366411d91cb08e0753a6a19a89f74cca6159dce",
    "schemas/review-fact-set-0.1.schema.json": "e33be9db7cae98d7ccdfc23bc95b71c81ad6921729c1ec1a81d708d590c288c1",
    "schemas/review-policy-0.1.schema.json": "101aed88a4155d5ae907bb43a822bd925e8a2f9b52df02a2366cb93ff7cecf4f",
    "schemas/review-r1-common-0.1.schema.json": "e36f0d4ba494645bc991736b780c2c5354be13789466ab82d72b4963c674da4a",
    "schemas/review-relation-set-0.1.schema.json": "397124031139d69f664445bd341be0139d0bed953487eb0cad796779ca8b4744",
    "schemas/review-slice-set-0.1.schema.json": "7d9eaba8978776d679e785ed3246a155bd7f78e3f5442219879fb3f80d80b851",
    "schemas/review-source-snapshot-0.1.schema.json": "f806e52d1f38d850003a85644d1380c00c8129a76720b9d4e96310d06a236518",
    "tests/fixtures/review-r1-schema-0.1/README.md": "3990bc0664461d049e5684dee8b32c1342901d4fafbb345aa8d7c802fd968e89",
    "tests/fixtures/review-r1-schema-0.1/compatibility-cases.json": "5cb46458ddf23673fcf0a2fef197637074e7dda16a538bace0b4d95b5d1bb696",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-00-07.json": "00b0cdfaf2754da5bed506fd215d52e27f3a8a1bfbd6cc0811d85208b7effca8",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-08-14.json": "c4acb39a568b50c49b2910b68a2815afd0f7a5eecdb6980ac71baf9bb16def42",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-15-22.json": "d23078ad43183bc237f0c4b8a5a77f4fb2ef870d94498b08c7878b9e0b81940b",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-23-29.json": "9d3712f44a074fdb9b6570e096aac035afcc0e987c394ca924a74c2645a1e2d5",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-30.json": "4449f0b43ec38ca3abfcdfbe8b6969c5b7e265fbfabc471356a97a16aa194e34",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-31.json": "a5f66942a218870d7b4a236244e768ae234a00c5b3cb4c1c1ae3810395cecd48",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-conflicts.json": "664469a017a128b1a6a24c13c0a83227b89070456cc50cdbf2b467d691b58fef",
    "tests/fixtures/review-r1-schema-0.1/identity-vectors/raw-sha256-vectors.json": "bfebba3823d4afbaa1d1805ad9f25109787c4352b212d877f49b0e072d0320a1",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/coverage-ledger.json": "256b529b0aaf1405c5020c5f3ffc5296ca769d95c1d6c85854369e79edae3a0a",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/derivation-evidence.json": "563664e5675cb861c7c22d4017c97d186a7e370bca4851dbf7bb09df49afb555",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/derivation-profile.json": "29ed3bed4caf4bd2d7dbae0d54166796fac2148eb483067809700aa953df95e2",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/fact-set.json": "63c77b77b31eb4e4f127f8bd5eeb77a4aa50d4791f556f1f325da9c32fb355e5",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/manifest.json": "ddccc2f4ed298f93c242a7004d361ca9af2d81574350a4035684aeb29bf2efe1",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/relation-set.json": "739e2f1eac4844346779a0953add1c1e09b3adcefbacd657c8716d89f00ab67c",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/review-policy.json": "b97bbbb7b41addcaf728fb5361aab33d9e801661f7c50c6a07c6228ae8872bc2",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/review-slices.json": "81e1aa631a9817c56b57dfe24a9a4ce8d38e11080fa4d6cc6e85f6825f9cb4a4",
    "tests/fixtures/review-r1-schema-0.1/valid-complete/source-snapshot.json": "ef07cdd90aa89dc630e9d21f7cc18ed65888f0a989b8b06eb61cbdda25045fce",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def semantic_digest(document: dict[str, object]) -> tuple[bytes, str]:
    payload = copy.deepcopy(document)
    payload.pop("derivation_evidence_digest")
    identity_bytes = canonical_json_bytes({"domain": IDENTITY_DOMAIN, "payload": payload})
    return identity_bytes, hashlib.sha256(identity_bytes).hexdigest()


def set_json_pointer(document: object, pointer: str, value: object) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    current = document
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    leaf = parts[-1]
    if isinstance(current, list):
        current[int(leaf)] = copy.deepcopy(value)
    else:
        current[leaf] = copy.deepcopy(value)


def get_json_pointer(document: object, pointer: str) -> object:
    current = document
    for part in pointer.split("/")[1:]:
        key = part.replace("~1", "/").replace("~0", "~")
        current = current[int(key)] if isinstance(current, list) else current[key]
    return copy.deepcopy(current)


def validate_correction_conformance(document: dict[str, object]) -> None:
    runs = {run["provider_run_id"]: run for run in document["provider_runs"]}
    top_diagnostics = document["diagnostics"]

    if document["overall_execution_status"] != "COMPLETED":
        for run in runs.values():
            if run["reported_fact_ids"] or run["reported_relation_ids"]:
                raise ValueError("non-completed Evidence cannot report canonical identities")

    for run_id, run in runs.items():
        if run["execution_status"] != "COMPLETED" and (
            run["reported_fact_ids"] or run["reported_relation_ids"]
        ):
            raise ValueError("non-completed run cannot report canonical identities")
        for diagnostic in run["diagnostics"]:
            code = diagnostic["diagnostic_code"]
            if code == "EXECUTION_ARTIFACT_BUDGET":
                raise ValueError("artifact budget is an Evidence-level stop")
            if code == "EXECUTION_MEMORY_BUDGET":
                subject = diagnostic["subject_ref"]
                if run["execution_status"] != "INTERRUPTED" or subject["provider_run_id"] != run_id:
                    raise ValueError("memory budget must identify its interrupted run")
                if diagnostic not in top_diagnostics:
                    raise ValueError("memory budget tuple must also be retained at Evidence level")

    for diagnostic in top_diagnostics:
        code = diagnostic["diagnostic_code"]
        if code not in {"EXECUTION_MEMORY_BUDGET", "EXECUTION_ARTIFACT_BUDGET"}:
            continue
        if document["overall_execution_status"] != "INTERRUPTED":
            raise ValueError("budget stop requires interrupted Evidence")
        if code == "EXECUTION_ARTIFACT_BUDGET":
            if diagnostic["subject_ref"] is not None:
                raise ValueError("artifact budget has no run-local subject")
            continue
        subject = diagnostic["subject_ref"]
        run = runs.get(subject["provider_run_id"])
        if run is None or diagnostic not in run["diagnostics"]:
            raise ValueError("memory budget tuple must bind the same ProviderRun")


class ReviewR1DerivationEvidenceSchemaCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_ROOT / "review-derivation-evidence-0.1.1.schema.json")
        cls.old_schema = load_json(SCHEMA_ROOT / "review-derivation-evidence-0.1.schema.json")
        cls.common_schema = load_json(SCHEMA_ROOT / "review-r1-common-0.1.schema.json")
        cls.manifest_schema = load_json(SCHEMA_ROOT / "review-derivation-manifest-0.1.schema.json")
        cls.registry = Registry().with_resources(
            [
                (schema["$id"], Resource.from_contents(schema))
                for schema in [cls.schema, cls.old_schema, cls.common_schema, cls.manifest_schema]
            ]
        )
        cls.validator = Draft202012Validator(
            cls.schema,
            registry=cls.registry,
            format_checker=FormatChecker(),
        )
        cls.manifest_validator = Draft202012Validator(
            cls.manifest_schema,
            registry=cls.registry,
            format_checker=FormatChecker(),
        )
        cls.corpus = load_json(CORPUS_ROOT / "compatibility-cases.json")
        cls.cases = {case["case_id"]: case for case in cls.corpus["cases"]}

    def test_schema_resource_is_additive_and_self_describing(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(
            self.schema["$id"],
            "https://github.com/NoctilumeDev/VeriTrail/schemas/review-derivation-evidence-0.1.1.schema.json",
        )
        self.assertEqual(self.schema["title"], "VeriTrail Review DerivationEvidence 0.1.1")
        self.assertEqual(self.schema["properties"]["schema_version"], {"const": "0.1.1"})
        self.assertEqual(self.schema["required"], self.old_schema["required"])
        self.assertEqual(set(self.schema["properties"]), set(self.old_schema["properties"]))
        self.assertEqual(self.schema["$defs"]["RequestProvenance"], self.old_schema["$defs"]["RequestProvenance"])
        self.assertEqual(
            set(self.schema["$defs"]) - set(self.old_schema["$defs"]),
            {"ProviderRunDiagnostic"},
        )
        for definition in set(self.old_schema["$defs"]) - {"Diagnostic", "ProviderRun"}:
            with self.subTest(definition=definition):
                self.assertEqual(self.schema["$defs"][definition], self.old_schema["$defs"][definition])
        old_codes = set(self.old_schema["$defs"]["Diagnostic"]["properties"]["diagnostic_code"]["enum"])
        new_codes = set(self.schema["$defs"]["Diagnostic"]["properties"]["diagnostic_code"]["enum"])
        self.assertEqual(new_codes - old_codes, {"EXECUTION_MEMORY_BUDGET", "EXECUTION_ARTIFACT_BUDGET"})
        self.assertEqual(old_codes - new_codes, set())

    def test_all_twenty_nine_frozen_0_1_files_remain_byte_identical(self) -> None:
        expected_corpus_paths = {
            path for path in FROZEN_0_1_SHA256 if path.startswith("tests/fixtures/review-r1-schema-0.1/")
        }
        actual_corpus_paths = {
            path.relative_to(ROOT).as_posix()
            for path in OLD_CORPUS_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(len(FROZEN_0_1_SHA256), 29)
        self.assertEqual(actual_corpus_paths, expected_corpus_paths)
        for relative_path, expected in FROZEN_0_1_SHA256.items():
            with self.subTest(path=relative_path):
                self.assertEqual(hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest(), expected)

    def test_positive_vectors_validate_and_recompute_exact_identity(self) -> None:
        self.assertEqual(self.corpus["identity_domain"], IDENTITY_DOMAIN)
        self.assertEqual(list(self.cases), [f"R1-DE-CV-{index:03d}" for index in range(1, 11)])
        for case_id in ["R1-DE-CV-001", "R1-DE-CV-002", "R1-DE-CV-003"]:
            case = self.cases[case_id]
            with self.subTest(case=case_id):
                document = case["document"]
                self.validator.validate(document)
                validate_correction_conformance(document)
                identity_bytes, digest = semantic_digest(document)
                self.assertEqual(identity_bytes, bytes.fromhex(case["expected_identity_canonical_utf8_hex"]))
                self.assertEqual(digest, case["expected_derivation_evidence_digest"])
                self.assertEqual(document["derivation_evidence_digest"], digest)

    def test_negative_vectors_change_one_semantic_variable_and_are_rejected(self) -> None:
        for case_id in [f"R1-DE-CV-{index:03d}" for index in range(4, 11)]:
            case = self.cases[case_id]
            vectors = case.get("vectors")
            if vectors is None:
                vectors = [{"vector_id": "default", "mutation": case["mutation"]}]
            base = self.cases[case["base_case_id"]]["document"]
            for vector in vectors:
                with self.subTest(case=case_id, vector=vector["vector_id"]):
                    mutation = vector["mutation"]
                    original_value = get_json_pointer(base, mutation["path"])
                    mutated = copy.deepcopy(base)
                    set_json_pointer(mutated, mutation["path"], mutation["value"])
                    restored = copy.deepcopy(mutated)
                    set_json_pointer(restored, mutation["path"], original_value)
                    self.assertEqual(restored, base)
                    errors = list(self.validator.iter_errors(mutated))
                    expected = vector.get("expected")
                    if expected is None:
                        expected = case["expected"]
                    if expected == "SCHEMA_REJECT":
                        self.assertTrue(errors, "Schema unexpectedly accepted the negative vector")
                    else:
                        self.assertEqual(expected, "CONFORMANCE_REJECT")
                        self.assertFalse(errors, errors)
                        with self.assertRaises(ValueError):
                            validate_correction_conformance(mutated)

    def test_diagnostic_manifest_binds_corrected_evidence_bytes(self) -> None:
        specimen = self.corpus["diagnostic_manifest_specimen"]
        manifest = specimen["manifest"]
        evidence_case = self.cases[specimen["evidence_case_id"]]
        evidence_bytes = canonical_json_bytes(evidence_case["document"]) + b"\n"
        self.manifest_validator.validate(manifest)
        self.assertEqual(manifest["schema_version"], "0.1")
        self.assertEqual(manifest["outcome_kind"], "DIAGNOSTIC")
        self.assertEqual(len(manifest["files"]), 4)
        evidence_entry = manifest["files"][3]
        self.assertEqual(evidence_entry["role"], "DERIVATION_EVIDENCE")
        self.assertEqual(evidence_entry["size_bytes"], len(evidence_bytes))
        self.assertEqual(evidence_entry["sha256"], hashlib.sha256(evidence_bytes).hexdigest())
        self.assertEqual(
            evidence_entry["semantic_digest"],
            evidence_case["expected_derivation_evidence_digest"],
        )


if __name__ == "__main__":
    unittest.main()
