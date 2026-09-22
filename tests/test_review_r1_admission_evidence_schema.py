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
CORPUS_ROOT = ROOT / "tests" / "fixtures" / "review-r1-derivation-evidence-0.2"
IDENTITY_DOMAIN = "veritrail.review.derivation-evidence/0.2"

HISTORICAL_BYTE_GUARDS = {
    "schemas/review-derivation-evidence-0.1.schema.json": "2efbd1d4f73f20fb045c2110136e7f3089e07408b9d496f59c30492a2c3666e7",
    "schemas/review-derivation-evidence-0.1.1.schema.json": "a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045",
    "schemas/review-relation-set-0.1.schema.json": "397124031139d69f664445bd341be0139d0bed953487eb0cad796779ca8b4744",
    "schemas/review-derivation-manifest-0.1.schema.json": "69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91",
    "tests/fixtures/review-r1-derivation-evidence-0.1.1/README.md": "16168eeab31757daa5a8b8b66165a2a00916b78517b6fa630938b9e33f5878ef",
    "tests/fixtures/review-r1-derivation-evidence-0.1.1/compatibility-cases.json": "b202f0063b1d94a6edc7bf5c9e8aa30e24a76ff6584638bf416c7739ce1283df",
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


def semantic_digest(domain: str, payload: object) -> str:
    return hashlib.sha256(
        canonical_json_bytes({"domain": domain, "payload": payload})
    ).hexdigest()


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


def _without(value: dict[str, object], *keys: str) -> dict[str, object]:
    return {key: copy.deepcopy(item) for key, item in value.items() if key not in keys}


def validate_admission_conformance(
    evidence: dict[str, object],
    relation_set: dict[str, object] | None,
) -> None:
    evidence_payload = _without(evidence, "derivation_evidence_digest")
    if evidence["derivation_evidence_digest"] != semantic_digest(
        IDENTITY_DOMAIN, evidence_payload
    ):
        raise ValueError("Evidence identity mismatch")

    if evidence["overall_execution_status"] != "COMPLETED":
        if evidence["relation_admission"] is not None or relation_set is not None:
            raise ValueError("non-completed Evidence cannot carry admission")
        if any(
            run["reported_fact_ids"] or run["reported_relation_ids"]
            for run in evidence["provider_runs"]
        ):
            raise ValueError("non-completed Evidence cannot report final identities")
        return

    if relation_set is None or evidence["relation_admission"] is None:
        raise ValueError("completed admission-capable Evidence needs both objects")
    witness = evidence["relation_admission"]
    domain = witness["observation_domain"]
    qualification = witness["qualification_claim"]
    claim = witness["admission_claim"]

    relation_payload = {
        "source_snapshot_digest": relation_set["source_snapshot_digest"],
        "analysis_scope_digest": relation_set["analysis_scope_digest"],
        "derivation_profile_digest": relation_set["derivation_profile_digest"],
        "fact_set_digest": relation_set["fact_set_digest"],
        "relations": [_without(item, "provenance_refs") for item in relation_set["relations"]],
        "conflicts": [_without(item, "provenance_refs") for item in relation_set["conflicts"]],
    }
    if relation_set["relation_set_digest"] != semantic_digest(
        "veritrail.review.relation-set/0.1", relation_payload
    ):
        raise ValueError("RelationSet identity mismatch")
    if domain["observation_domain_digest"] != semantic_digest(
        "veritrail.review.relation-observation-domain/0.1",
        _without(domain, "policy_digest", "observation_domain_digest"),
    ):
        raise ValueError("observation domain identity mismatch")
    if qualification["qualification_digest"] != semantic_digest(
        "veritrail.review.relation-composition-qualification/0.1",
        _without(qualification, "qualification_digest"),
    ):
        raise ValueError("qualification identity mismatch")
    if claim["admission_witness_digest"] != semantic_digest(
        "veritrail.review.relation-set-admission-witness/0.1",
        _without(claim, "admission_witness_digest"),
    ):
        raise ValueError("admission witness identity mismatch")

    coordinate_pairs = (
        ("derivation_id", evidence, claim),
        ("source_snapshot_digest", evidence, relation_set),
        ("source_snapshot_digest", evidence, domain),
        ("source_snapshot_digest", evidence, claim),
        ("policy_digest", evidence, relation_set),
        ("policy_digest", evidence, domain),
        ("policy_digest", evidence, claim),
        ("analysis_scope_digest", evidence, relation_set),
        ("analysis_scope_digest", evidence, domain),
        ("analysis_scope_digest", evidence, claim),
        ("derivation_profile_digest", evidence, relation_set),
        ("derivation_profile_digest", evidence, domain),
        ("derivation_profile_digest", evidence, claim),
        ("fact_set_digest", relation_set, domain),
        ("fact_set_digest", relation_set, claim),
        ("observation_domain_digest", domain, qualification),
        ("observation_domain_digest", domain, claim),
        ("qualification_digest", qualification, claim),
        ("relation_set_digest", relation_set, claim),
    )
    if any(left[key] != right[key] for key, left, right in coordinate_pairs):
        raise ValueError("cross-object coordinate mismatch")

    relation_ids = [item["relation_id"] for item in relation_set["relations"]]
    conflict_ids = [item["conflict_id"] for item in relation_set["conflicts"]]
    if (
        claim["admitted_relation_ids"] != relation_ids
        or qualification["merged_candidate_relation_ids"] != relation_ids
        or claim["admitted_conflict_ids"] != conflict_ids
        or qualification["private_conflict_ids"] != conflict_ids
    ):
        raise ValueError("admitted membership mismatch")

    relation_runs = [
        run for run in evidence["provider_runs"]
        if run["capability_id"] == "review-relation-derivation"
    ]
    relation_run_ids = [run["provider_run_id"] for run in relation_runs]
    if claim["relation_provider_run_ids"] != relation_run_ids:
        raise ValueError("admission run closure mismatch")
    if qualification["provider_run_terminals"] != [
        {"provider_run_id": run["provider_run_id"], "execution_status": run["execution_status"]}
        for run in relation_runs
    ]:
        raise ValueError("qualification terminal mismatch")

    accepted_by_relation: dict[str, set[str]] = {}
    for receipt in qualification["observation_receipts"]:
        run_id = receipt["provider_run_id"]
        if run_id not in relation_run_ids:
            raise ValueError("receipt references an unknown Relation run")
        for outcome in receipt["accepted_observation_outcomes"]:
            if outcome["provider_run_id"] != run_id:
                raise ValueError("outcome and receipt run mismatch")
            for relation_id in outcome["reported_relation_ids"]:
                accepted_by_relation.setdefault(relation_id, set()).add(run_id)
    if set(accepted_by_relation) != set(relation_ids):
        raise ValueError("outcomes do not close admitted membership")
    for relation in relation_set["relations"]:
        if set(relation["provenance_refs"]) != accepted_by_relation[relation["relation_id"]]:
            raise ValueError("Relation provenance does not close over outcomes")
    for run in relation_runs:
        expected = sorted(
            relation_id for relation_id, refs in accepted_by_relation.items()
            if run["provider_run_id"] in refs
        )
        if run["reported_relation_ids"] != expected:
            raise ValueError("ProviderRun reverse relation closure mismatch")


class ReviewR1AdmissionEvidenceSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_ROOT / "review-derivation-evidence-0.2.schema.json")
        cls.common_schema = load_json(SCHEMA_ROOT / "review-r1-common-0.1.schema.json")
        cls.relation_schema = load_json(SCHEMA_ROOT / "review-relation-set-0.1.schema.json")
        cls.registry = Registry().with_resources(
            [
                (schema["$id"], Resource.from_contents(schema))
                for schema in (cls.schema, cls.common_schema, cls.relation_schema)
            ]
        )
        cls.evidence_validator = Draft202012Validator(
            cls.schema, registry=cls.registry, format_checker=FormatChecker()
        )
        cls.relation_validator = Draft202012Validator(
            cls.relation_schema, registry=cls.registry, format_checker=FormatChecker()
        )
        cls.corpus = load_json(CORPUS_ROOT / "compatibility-cases.json")
        cls.positive = {
            case["case_id"]: {
                "evidence": load_json(CORPUS_ROOT / case["evidence"]),
                "relation_set": (
                    load_json(CORPUS_ROOT / case["relation_set"])
                    if case["relation_set"] is not None else None
                ),
            }
            for case in cls.corpus["positive_cases"]
        }

    def test_schema_is_additive_closed_and_self_describing(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(self.schema["properties"]["schema_version"], {"const": "0.2"})
        self.assertIn("relation_admission", self.schema["required"])
        self.assertFalse(self.schema["additionalProperties"])
        self.assertEqual(
            self.schema["$id"],
            "https://github.com/NoctilumeDev/VeriTrail/schemas/review-derivation-evidence-0.2.schema.json",
        )

    def test_historical_schemas_corpus_relation_set_and_manifest_are_unchanged(self) -> None:
        for relative_path, expected in HISTORICAL_BYTE_GUARDS.items():
            with self.subTest(path=relative_path):
                actual = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
                self.assertEqual(actual, expected)

    def test_positive_corpus_validates_and_recomputes_cross_object_closure(self) -> None:
        self.assertEqual(
            list(self.positive),
            ["R1-RAE-CV-001", "R1-RAE-CV-002", "R1-RAE-CV-003"],
        )
        for case_id, specimen in self.positive.items():
            with self.subTest(case=case_id):
                evidence = specimen["evidence"]
                relation_set = specimen["relation_set"]
                self.evidence_validator.validate(evidence)
                if relation_set is not None:
                    self.relation_validator.validate(relation_set)
                validate_admission_conformance(evidence, relation_set)

    def test_rae_006_historical_evidence_cannot_masquerade_as_0_2(self) -> None:
        historical_0_1 = load_json(
            ROOT
            / "tests/fixtures/review-r1-schema-0.1/valid-complete/derivation-evidence.json"
        )
        historical_0_1_1 = load_json(
            ROOT
            / "tests/fixtures/review-r1-derivation-evidence-0.1.1/compatibility-cases.json"
        )["cases"][0]["document"]
        self.assertTrue(list(self.evidence_validator.iter_errors(historical_0_1)))
        self.assertTrue(list(self.evidence_validator.iter_errors(historical_0_1_1)))

    def test_rae_007_008_noncompleted_is_null_and_completed_needs_witness(self) -> None:
        interrupted = self.positive["R1-RAE-CV-003"]["evidence"]
        self.assertIsNone(interrupted["relation_admission"])
        self.assertTrue(
            all(
                not run["reported_fact_ids"] and not run["reported_relation_ids"]
                for run in interrupted["provider_runs"]
            )
        )
        completed_without_witness = copy.deepcopy(
            self.positive["R1-RAE-CV-001"]["evidence"]
        )
        completed_without_witness["relation_admission"] = None
        self.assertTrue(
            list(self.evidence_validator.iter_errors(completed_without_witness))
        )

    def test_rae_010_manifest_binding_cannot_repair_an_invalid_witness(self) -> None:
        specimen = copy.deepcopy(self.positive["R1-RAE-CV-001"])
        evidence = specimen["evidence"]
        evidence["relation_admission"]["qualification_claim"][
            "observation_receipts"
        ][0]["accepted_observation_outcomes"][0]["disposition"] = "NEGATIVE"
        evidence["derivation_evidence_digest"] = semantic_digest(
            IDENTITY_DOMAIN, _without(evidence, "derivation_evidence_digest")
        )
        self.evidence_validator.validate(evidence)
        with self.assertRaises(ValueError):
            validate_admission_conformance(evidence, specimen["relation_set"])
        self.assertEqual(
            hashlib.sha256(
                (SCHEMA_ROOT / "review-derivation-manifest-0.1.schema.json").read_bytes()
            ).hexdigest(),
            HISTORICAL_BYTE_GUARDS[
                "schemas/review-derivation-manifest-0.1.schema.json"
            ],
        )

    def test_identity_vectors_freeze_exact_0_2_bytes_and_semantics(self) -> None:
        vectors = load_json(CORPUS_ROOT / "identity-vectors.json")
        self.assertEqual(vectors["identity_domain"], IDENTITY_DOMAIN)
        for vector, specimen in zip(vectors["vectors"], self.positive.values()):
            evidence = specimen["evidence"]
            artifact_bytes = canonical_json_bytes(evidence) + b"\n"
            self.assertEqual(
                vector["canonical_artifact_sha256"],
                hashlib.sha256(artifact_bytes).hexdigest(),
            )
            self.assertEqual(
                vector["derivation_evidence_digest"],
                semantic_digest(IDENTITY_DOMAIN, _without(evidence, "derivation_evidence_digest")),
            )
            if specimen["relation_set"] is not None:
                self.assertEqual(
                    vector["relation_set_digest"],
                    specimen["relation_set"]["relation_set_digest"],
                )
                self.assertEqual(
                    vector["admission_witness_digest"],
                    evidence["relation_admission"]["admission_claim"]["admission_witness_digest"],
                )

    def test_negative_vectors_are_schema_or_conformance_rejected(self) -> None:
        for vector in self.corpus["negative_cases"]:
            with self.subTest(case=vector["case_id"]):
                specimen = copy.deepcopy(self.positive[vector["base_case_id"]])
                target = specimen[vector["target"]]
                source = vector.get("value_from_case")
                if source is None:
                    value = vector["value"]
                else:
                    source_case, pointer = source.split(":", 1)
                    value = get_json_pointer(
                        self.positive[source_case]["evidence"], pointer
                    )
                set_json_pointer(target, vector["path"], value)
                if vector.get("recompute_evidence_digest"):
                    evidence = specimen["evidence"]
                    evidence["derivation_evidence_digest"] = semantic_digest(
                        IDENTITY_DOMAIN, _without(evidence, "derivation_evidence_digest")
                    )
                validator = (
                    self.evidence_validator
                    if vector["target"] == "evidence"
                    else self.relation_validator
                )
                errors = list(validator.iter_errors(target))
                if vector["expected"] == "SCHEMA_REJECT":
                    self.assertTrue(errors, "Schema unexpectedly accepted vector")
                else:
                    self.assertFalse(errors, errors)
                    with self.assertRaises(ValueError):
                        validate_admission_conformance(
                            specimen["evidence"], specimen["relation_set"]
                        )

    def test_rae_016_017_identity_is_acyclic_and_manifest_topology_is_unchanged(self) -> None:
        evidence = copy.deepcopy(self.positive["R1-RAE-CV-001"]["evidence"])
        witness = evidence["relation_admission"]
        self.assertNotIn("derivation_evidence_digest", canonical_json_bytes(witness).decode())
        witness["admission_claim"]["derivation_evidence_digest"] = evidence[
            "derivation_evidence_digest"
        ]
        self.assertTrue(list(self.evidence_validator.iter_errors(evidence)))
        manifest_schemas = sorted(
            path.name
            for path in SCHEMA_ROOT.glob("review-derivation-manifest-*.schema.json")
        )
        self.assertEqual(
            manifest_schemas, ["review-derivation-manifest-0.1.schema.json"]
        )


if __name__ == "__main__":
    unittest.main()
