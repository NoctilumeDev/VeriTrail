from __future__ import annotations

import ast
import copy
from datetime import datetime
import hashlib
import io
import json
import keyword
from pathlib import Path
import tokenize
import unicodedata
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas"
CORPUS_ROOT = ROOT / "tests" / "fixtures" / "review-r1-schema-0.1"
VALID_ROOT = CORPUS_ROOT / "valid-complete"

SCHEMA_BY_ARTIFACT = {
    "manifest.json": "review-derivation-manifest-0.1.schema.json",
    "source-snapshot.json": "review-source-snapshot-0.1.schema.json",
    "review-policy.json": "review-policy-0.1.schema.json",
    "derivation-profile.json": "review-derivation-profile-0.1.schema.json",
    "derivation-evidence.json": "review-derivation-evidence-0.1.schema.json",
    "fact-set.json": "review-fact-set-0.1.schema.json",
    "relation-set.json": "review-relation-set-0.1.schema.json",
    "review-slices.json": "review-slice-set-0.1.schema.json",
    "coverage-ledger.json": "review-coverage-ledger-0.1.schema.json",
}

EXPECTED_SCHEMA_FILES = {
    "review-r1-common-0.1.schema.json",
    *SCHEMA_BY_ARTIFACT.values(),
}

FROZEN_IDENTITY_DOMAINS = {
    "veritrail.review.source-coordinate/0.1",
    "veritrail.review.source-inventory/0.1",
    "veritrail.review.source-content/0.1",
    "veritrail.review.source-snapshot/0.1",
    "veritrail.review.derivation-profile/0.1",
    "veritrail.review.analysis-scope/0.1",
    "veritrail.review.slice-policy/0.1",
    "veritrail.review.review-policy/0.1",
    "veritrail.review.fact-subject/0.1",
    "veritrail.review.code-fact/0.1",
    "veritrail.review.fact-set/0.1",
    "veritrail.review.fact-conflict/0.1",
    "veritrail.review.relation-subject/0.1",
    "veritrail.review.structural-relation/0.1",
    "veritrail.review.relation-set/0.1",
    "veritrail.review.relation-conflict/0.1",
    "veritrail.review.slice-spec/0.1",
    "veritrail.review.review-slice/0.1",
    "veritrail.review.slice-set/0.1",
    "veritrail.review.coverage-denominator/0.1",
    "veritrail.review.coverage-ledger/0.1",
    "veritrail.review.provider-operands/0.1",
    "veritrail.review.provider-run/0.1",
    "veritrail.review.derivation-evidence/0.1",
}

STAGE_ORDER = [
    "SNAPSHOT_INVENTORY",
    "POLICY_SCOPE",
    "LANGUAGE_SUPPORT",
    "PARSE",
    "FACT_DERIVATION",
    "RELATION_DERIVATION",
    "SLICE_DERIVATION",
]

ROLE_TO_ARTIFACT = {
    "SOURCE_SNAPSHOT": ("source-snapshot.json", "source_snapshot_digest"),
    "REVIEW_POLICY": ("review-policy.json", "policy_digest"),
    "DERIVATION_PROFILE": ("derivation-profile.json", "profile_digest"),
    "DERIVATION_EVIDENCE": ("derivation-evidence.json", "derivation_evidence_digest"),
    "FACT_SET": ("fact-set.json", "fact_set_digest"),
    "RELATION_SET": ("relation-set.json", "relation_set_digest"),
    "REVIEW_SLICE_SET": ("review-slices.json", "slice_set_digest"),
    "COVERAGE_LEDGER": ("coverage-ledger.json", "coverage_ledger_digest"),
}


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def semantic_digest(domain: str, payload: object) -> str:
    envelope = {"domain": domain, "payload": payload}
    return hashlib.sha256(canonical_json_bytes(envelope)).hexdigest()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_refs(value: object) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref":
                refs.append(child)
            refs.extend(collect_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(collect_refs(child))
    return refs


def collect_shape_placeholders(value: object, path: str = "") -> set[str]:
    placeholders: set[str] = set()
    if isinstance(value, dict):
        if value.get("type") == "object" and not ({"additionalProperties", "maxProperties"} & value.keys()):
            placeholders.add(f"OPEN_OBJECT:{path}")
        if value.get("type") == "array" and not ({"items", "prefixItems"} & value.keys()):
            placeholders.add(f"OPEN_ARRAY:{path}")
        for key, child in value.items():
            placeholders.update(collect_shape_placeholders(child, f"{path}/{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            placeholders.update(collect_shape_placeholders(child, f"{path}/{index}"))
    return placeholders


def validate_git_path_hex(value: str) -> bytes:
    if not value or len(value) % 2 or value.lower() != value:
        raise ValueError("Git path hex must be non-empty, lower-case, and even length")
    try:
        raw = bytes.fromhex(value)
    except ValueError as exc:
        raise ValueError("Git path is not hexadecimal") from exc
    if not raw or b"\x00" in raw or raw.startswith(b"/") or raw.endswith(b"/"):
        raise ValueError("Git path has a forbidden root, terminator, or empty boundary")
    parts = raw.split(b"/")
    if any(part in {b"", b".", b".."} for part in parts):
        raise ValueError("Git path contains a forbidden component")
    return raw


def status_join(statuses: list[str]) -> str:
    if "UNKNOWN" in statuses:
        return "UNKNOWN"
    if "PARTIAL" in statuses:
        return "PARTIAL"
    return "COMPLETE"


def is_python_310_identifier(value: object) -> bool:
    return (
        isinstance(value, str)
        and value == unicodedata.normalize("NFKC", value)
        and value.isidentifier()
        and not keyword.iskeyword(value)
    )


def coverage_item_key(value: dict[str, object]) -> bytes:
    return canonical_json_bytes(value)


def stage_partition_is_conformant(stage: dict[str, object]) -> bool:
    denominator = stage["denominator"]
    if denominator["state"] != "KNOWN":
        return stage["coverage_status"] == "UNKNOWN"

    eligible = {coverage_item_key(item) for item in stage["eligible"]}
    outer_items = [
        item["item_ref"]
        for field in ("out_of_scope", "unsupported")
        for item in stage[field]
    ]
    inner_items = [
        item["item_ref"]
        for field in (
            "unresolved", "conflicts", "parse_failed", "execution_failed", "truncated"
        )
        for item in stage[field]
    ] + list(stage["completed"])
    outer = [coverage_item_key(item) for item in outer_items]
    inner = [coverage_item_key(item) for item in inner_items]
    denominator_items = [coverage_item_key(item) for item in denominator["item_refs"]]
    if len(outer) != len(set(outer)) or len(inner) != len(set(inner)):
        return False
    if set(outer) & eligible:
        return False
    if set(inner) != eligible:
        return False
    if set(denominator_items) != eligible | set(outer):
        return False

    has_gap = bool(
        outer_items
        or any(
            stage[field]
            for field in (
                "unresolved", "conflicts", "parse_failed", "execution_failed", "truncated"
            )
        )
        or stage["frontier"]
    )
    expected_status = "PARTIAL" if has_gap else "COMPLETE"
    return stage["coverage_status"] == expected_status


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")


class ReviewR1SchemaPayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            path.name: load_json(path)
            for path in sorted(SCHEMA_ROOT.glob("review-*.schema.json"))
        }
        cls.registry = Registry().with_resources(
            [
                (schema["$id"], Resource.from_contents(schema))
                for schema in cls.schemas.values()
            ]
        )
        cls.validators = {
            artifact: Draft202012Validator(
                cls.schemas[schema_name],
                registry=cls.registry,
                format_checker=FormatChecker(),
            )
            for artifact, schema_name in SCHEMA_BY_ARTIFACT.items()
        }
        cls.artifacts = {
            name: load_json(VALID_ROOT / name)
            for name in SCHEMA_BY_ARTIFACT
        }
        cls.compatibility = load_json(CORPUS_ROOT / "compatibility-cases.json")
        cls.cases = {
            case["case_id"]: case for case in cls.compatibility["cases"]
        }
        cls.identity_vectors = []
        cls.raw_vectors = []
        for path in sorted((CORPUS_ROOT / "identity-vectors").glob("*.json")):
            document = load_json(path)
            cls.identity_vectors.extend(document.get("vectors", []))
            cls.raw_vectors.extend(document.get("raw_sha256_vectors", []))

    def assert_schema_rejects(self, artifact: str, document: object) -> None:
        errors = list(self.validators[artifact].iter_errors(document))
        self.assertTrue(errors, f"{artifact} unexpectedly accepted a negative vector")

    def test_schema_file_set_is_exact_and_offline(self) -> None:
        self.assertEqual(set(self.schemas), EXPECTED_SCHEMA_FILES)
        for name, schema in self.schemas.items():
            Draft202012Validator.check_schema(schema)
            self.assertEqual(
                schema["$id"],
                f"https://github.com/NoctilumeDev/VeriTrail/schemas/{name}",
            )
            for ref in collect_refs(schema):
                self.assertTrue(
                    ref.startswith("#/")
                    or ref.startswith("review-r1-common-0.1.schema.json#/"),
                    f"network or non-common cross-schema reference: {name}: {ref}",
                )

    def test_only_discriminated_shape_placeholders_remain_open(self) -> None:
        actual = {
            f"{name}:{placeholder}"
            for name, schema in self.schemas.items()
            for placeholder in collect_shape_placeholders(schema)
        }
        self.assertEqual(
            actual,
            {
                "review-derivation-manifest-0.1.schema.json:OPEN_ARRAY:/properties/files",
                "review-fact-set-0.1.schema.json:OPEN_OBJECT:/$defs/Fact/properties/semantic_attributes",
                "review-relation-set-0.1.schema.json:OPEN_OBJECT:/$defs/Relation/properties/target",
            },
        )

    def test_valid_complete_bundle_matches_all_root_schemas(self) -> None:
        for artifact, validator in self.validators.items():
            with self.subTest(artifact=artifact):
                validator.validate(self.artifacts[artifact])

    def test_valid_artifact_files_are_exact_canonical_bytes(self) -> None:
        for name, document in self.artifacts.items():
            with self.subTest(name=name):
                actual = (VALID_ROOT / name).read_bytes()
                self.assertEqual(actual, canonical_json_bytes(document) + b"\n")
                self.assertFalse(actual.startswith(b"\xef\xbb\xbf"))
                self.assertNotIn(b"\r", actual)
                self.assertFalse(actual.endswith(b"\n\n"))

    def test_manifest_binds_exact_file_and_semantic_identities(self) -> None:
        manifest = self.artifacts["manifest.json"]
        self.assertEqual(manifest["outcome_kind"], "COMPLETE")
        self.assertEqual([entry["role"] for entry in manifest["files"]], list(ROLE_TO_ARTIFACT))
        for entry in manifest["files"]:
            name, digest_field = ROLE_TO_ARTIFACT[entry["role"]]
            exact_bytes = (VALID_ROOT / name).read_bytes()
            self.assertEqual(entry["path"], name)
            self.assertEqual(entry["size_bytes"], len(exact_bytes))
            self.assertEqual(entry["sha256"], hashlib.sha256(exact_bytes).hexdigest())
            self.assertEqual(entry["semantic_digest"], self.artifacts[name][digest_field])

    def test_all_frozen_identity_domains_have_recomputable_vectors(self) -> None:
        domains = {vector["identity_envelope"]["domain"] for vector in self.identity_vectors}
        self.assertEqual(domains, FROZEN_IDENTITY_DOMAINS)
        self.assertEqual(len(self.identity_vectors), 34)
        self.assertEqual(len(self.raw_vectors), 1)
        self.assertEqual(len({vector["vector_id"] for vector in self.identity_vectors}), len(self.identity_vectors))
        for vector in self.identity_vectors:
            with self.subTest(vector=vector["vector_id"]):
                actual = canonical_json_bytes(vector["identity_envelope"])
                self.assertEqual(actual, bytes.fromhex(vector["expected_canonical_utf8_hex"]))
                self.assertEqual(hashlib.sha256(actual).hexdigest(), vector["expected_digest"])
        for vector in self.raw_vectors:
            with self.subTest(vector=vector["vector_id"]):
                actual = canonical_json_bytes(vector["value"])
                self.assertEqual(actual, bytes.fromhex(vector["expected_canonical_utf8_hex"]))
                self.assertEqual(hashlib.sha256(actual).hexdigest(), vector["expected_digest"])

    def test_domain_is_part_of_semantic_identity(self) -> None:
        payload = {"same": "payload"}
        first = semantic_digest("veritrail.review.code-fact/0.1", payload)
        second = semantic_digest("veritrail.review.structural-relation/0.1", payload)
        self.assertNotEqual(first, second)

    def test_compatibility_matrix_has_twenty_stable_coordinates(self) -> None:
        self.assertEqual(list(self.cases), [f"R1-CV-{index:03d}" for index in range(1, 21)])
        self.assertEqual(len(self.cases), 20)

    def test_git_path_vectors_preserve_raw_bytes_and_reject_forbidden_forms(self) -> None:
        accepted = self.cases["R1-CV-002"]["vectors"]
        decoded = [validate_git_path_hex(vector["git_path_hex"]) for vector in accepted]
        self.assertEqual(len(decoded), len(set(decoded)))
        self.assertEqual([value.hex() for value in decoded], [item["git_path_hex"] for item in accepted])
        for value in self.cases["R1-CV-003"]["vectors"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_git_path_hex(value)

    def test_coordinate_and_content_identities_are_separate(self) -> None:
        case = self.cases["R1-CV-004"]
        root = {"path_kind": "REPOSITORY_ROOT"}
        tree = {"algorithm": "SHA1", "hex": case["tree_oid"]}
        inventory_digest = "4" * 64
        content_payload = {
            "analysis_tree_oid": tree,
            "analysis_root": root,
            "inventory_digest": inventory_digest,
        }
        content_digests = []
        coordinate_digests = []
        snapshot_digests = []
        for commit in case["commit_oids"]:
            coordinate = semantic_digest(
                "veritrail.review.source-coordinate/0.1",
                {
                    "repository_id": "fixture/repository",
                    "commit_oid": {"algorithm": "SHA1", "hex": commit},
                    "commit_tree_oid": tree,
                    "analysis_tree_oid": tree,
                    "analysis_root": root,
                },
            )
            content = semantic_digest("veritrail.review.source-content/0.1", content_payload)
            snapshot = semantic_digest(
                "veritrail.review.source-snapshot/0.1",
                {"source_coordinate_digest": coordinate, "source_content_digest": content},
            )
            coordinate_digests.append(coordinate)
            content_digests.append(content)
            snapshot_digests.append(snapshot)
        self.assertEqual(len(set(content_digests)), 1)
        self.assertEqual(len(set(coordinate_digests)), 2)
        self.assertEqual(len(set(snapshot_digests)), 2)

    def test_friendly_ref_and_replaced_path_do_not_rewrite_owned_snapshot(self) -> None:
        ref_case = self.cases["R1-CV-005"]
        self.assertEqual(ref_case["expected_snapshot_commit"], ref_case["resolved_commit_before"])
        self.assertNotEqual(ref_case["expected_snapshot_commit"], ref_case["resolved_commit_after"])
        byte_case = self.cases["R1-CV-006"]
        verified = bytes.fromhex(byte_case["verified_bytes_hex"])
        replaced = bytes.fromhex(byte_case["replacement_bytes_hex"])
        self.assertNotEqual(hashlib.sha256(verified).digest(), hashlib.sha256(replaced).digest())
        self.assertEqual(byte_case["expected"], "CONSUME_VERIFIED_BYTES_OR_FAIL")

    def test_encoding_anchor_syntax_and_import_vectors_are_explicit(self) -> None:
        for vector in self.cases["R1-CV-007"]["vectors"]:
            raw = bytes.fromhex(vector["source_hex"])
            self.assertLessEqual(vector["start_byte"], vector["end_byte"])
            self.assertLessEqual(vector["end_byte"], len(raw))
            self.assertEqual(raw[vector["start_byte"] : vector["end_byte"]].decode("utf-8"), "import α")

        non_utf = bytes.fromhex(self.cases["R1-CV-008"]["source_hex"])
        encoding, _ = tokenize.detect_encoding(io.BytesIO(non_utf).readline)
        self.assertEqual(encoding, "iso-8859-1")
        self.assertEqual(self.cases["R1-CV-008"]["expected_reason"], "UNSUPPORTED_SOURCE_ENCODING")

        syntax_case = self.cases["R1-CV-009"]
        with self.assertRaises(SyntaxError):
            ast.parse(syntax_case["source_utf8"], feature_version=(3, 10))

        import_case = self.cases["R1-CV-010"]
        node = ast.parse(import_case["source_utf8"], feature_version=(3, 10)).body[0]
        actual = [
            {
                "module_parts": alias.name.split("."),
                "alias_name": alias.asname,
                "local_ordinal": index,
            }
            for index, alias in enumerate(node.names)
        ]
        self.assertEqual(actual, import_case["expected_aliases"])

    def test_provider_layering_conflict_bfs_budget_and_overlap_vectors(self) -> None:
        for vector in self.cases["R1-CV-011"]["vectors"]:
            combined = sorted(set(vector["source_a"]) | set(vector["source_b"]))
            self.assertEqual(combined, vector["expected"])

        conflict = self.cases["R1-CV-012"]
        self.assertEqual(conflict["expected"], "CONFLICT")
        self.assertEqual(len(conflict["candidate_ids"]), 2)
        self.assertEqual(len(set(conflict["candidate_ids"])), 2)

        graph_case = self.cases["R1-CV-013"]
        adjacency: dict[str, list[tuple[str, str]]] = {}
        for source, target, relation in graph_case["edges"]:
            adjacency.setdefault(source, []).append((target, relation))
        queue = [graph_case["anchor"]]
        visited = set()
        order = []
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            order.append(current)
            queue.extend(target for target, _ in sorted(adjacency.get(current, [])))
        self.assertEqual(order, graph_case["expected_fact_order"])

        reasons = [vector["expected_reason"] for vector in self.cases["R1-CV-014"]["vectors"]]
        self.assertEqual(reasons, ["DEPTH_LIMIT", "SYMBOL_LIMIT", "FILE_LIMIT", "RELATION_LIMIT"])

        overlap = self.cases["R1-CV-015"]
        unique = sorted({fact for slice_ids in overlap["slice_fact_ids"] for fact in slice_ids})
        self.assertEqual(unique, overlap["expected_unique_fact_ids"])

    def test_typed_gaps_diagnostic_boundary_and_reference_lab_remain_explicit(self) -> None:
        gaps = self.cases["R1-CV-016"]["vectors"]
        self.assertEqual(len({item.get("disposition", item.get("denominator")) for item in gaps}), 4)
        self.assertEqual(len({item["reason"] for item in gaps}), 4)

        interrupted = self.cases["R1-CV-017"]
        self.assertEqual(interrupted["allowed_manifest_outcome"], "DIAGNOSTIC")
        self.assertEqual(interrupted["allowed_roles"], list(ROLE_TO_ARTIFACT)[:4])

        mutations = self.cases["R1-CV-018"]["mutations"]
        self.assertEqual(len(mutations), 8)
        self.assertEqual(len(set(mutations)), 8)

        self.assertEqual(
            self.cases["R1-CV-019"]["runners"],
            ["CPYTHON_3_10_NORMAL", "CPYTHON_3_10_OPTIMIZED", "CPYTHON_3_13_NORMAL", "CPYTHON_3_13_OPTIMIZED"],
        )

        lab = self.cases["R1-CV-020"]
        self.assertEqual(lab["repository"], "NoctilumeDev/VeriTrail")
        self.assertEqual(lab["commit"], "9ab64121350b69ce81e6be79961ad426026bbc39")
        self.assertEqual(lab["analysis_root"], "plugins/github-evidence/src/veritrail_github")
        self.assertEqual((lab["tracked_ordinary_python_blobs"], lab["total_blob_bytes"]), (22, 259553))

    def test_cross_artifact_references_order_and_coverage_equations(self) -> None:
        snapshot = self.artifacts["source-snapshot.json"]
        policy = self.artifacts["review-policy.json"]
        profile = self.artifacts["derivation-profile.json"]
        evidence = self.artifacts["derivation-evidence.json"]
        facts = self.artifacts["fact-set.json"]
        relations = self.artifacts["relation-set.json"]
        slices = self.artifacts["review-slices.json"]
        ledger = self.artifacts["coverage-ledger.json"]

        for artifact in [policy, evidence, facts, relations, slices, ledger]:
            self.assertEqual(artifact["source_snapshot_digest"], snapshot["source_snapshot_digest"])
        for artifact in [policy, evidence, facts, relations, slices, ledger]:
            self.assertEqual(artifact["derivation_profile_digest"], profile["profile_digest"])
        for artifact in [evidence, facts, relations, slices, ledger]:
            self.assertEqual(artifact["policy_digest"], policy["policy_digest"])

        self.assertEqual(facts["facts"], sorted(facts["facts"], key=lambda item: item["fact_id"]))
        self.assertEqual(relations["relations"], sorted(relations["relations"], key=lambda item: item["relation_id"]))
        self.assertEqual(slices["slices"], sorted(slices["slices"], key=lambda item: item["slice_id"]))

        run_ids = {run["provider_run_id"] for run in evidence["provider_runs"]}
        for fact in facts["facts"]:
            self.assertEqual(fact["provenance_refs"], sorted(set(fact["provenance_refs"])))
            self.assertTrue(set(fact["provenance_refs"]).issubset(run_ids))
        for relation in relations["relations"]:
            self.assertEqual(relation["provenance_refs"], sorted(set(relation["provenance_refs"])))
            self.assertTrue(set(relation["provenance_refs"]).issubset(run_ids))

        self.assertEqual([stage["stage"] for stage in ledger["stages"]], STAGE_ORDER)
        for stage in ledger["stages"]:
            denominator = stage["denominator"]
            self.assertEqual(denominator["state"], "KNOWN")
            self.assertEqual(denominator["item_refs"], stage["eligible"])
            expected_denominator = semantic_digest(
                "veritrail.review.coverage-denominator/0.1",
                {"stage": stage["stage"], "item_refs": denominator["item_refs"]},
            )
            self.assertEqual(denominator["source_digest"], expected_denominator)
            denominator_set = {canonical_json_bytes(item) for item in denominator["item_refs"]}
            eligible_set = {canonical_json_bytes(item) for item in stage["eligible"]}
            outer_terminal = {
                canonical_json_bytes(item["item_ref"])
                for field in ("out_of_scope", "unsupported")
                for item in stage[field]
            }
            inner_terminal = {
                canonical_json_bytes(item["item_ref"])
                for field in (
                    "unresolved", "conflicts", "parse_failed", "execution_failed", "truncated"
                )
                for item in stage[field]
            } | {canonical_json_bytes(item) for item in stage["completed"]}
            self.assertEqual(denominator_set, eligible_set | outer_terminal)
            self.assertEqual(eligible_set, inner_terminal)
            self.assertEqual(stage["coverage_status"], "COMPLETE")
        self.assertEqual(
            ledger["overall_coverage_status"],
            status_join([stage["coverage_status"] for stage in ledger["stages"]]),
        )

    def test_policy_ordering_and_python_identifier_rules_are_conformant(self) -> None:
        snapshot = self.artifacts["source-snapshot.json"]
        policy = self.artifacts["review-policy.json"]
        profile = self.artifacts["derivation-profile.json"]
        facts = self.artifacts["fact-set.json"]

        inventory_paths = [entry["git_path"]["git_path_hex"] for entry in snapshot["inventory"]]
        scope_paths = [decision["git_path"]["git_path_hex"] for decision in policy["scope_decisions"]]
        self.assertEqual(scope_paths, sorted(set(scope_paths), key=bytes.fromhex))
        self.assertEqual(scope_paths, inventory_paths)

        capability_ids = [item["capability_id"] for item in policy["provider_requirements"]]
        self.assertEqual(capability_ids, sorted(set(capability_ids)))

        identifiers = list(policy["python_module_mapping"]["package_prefix"])
        for fact in facts["facts"]:
            attributes = fact["semantic_attributes"]
            identifiers.extend(attributes.get("module_key_parts") or [])
            identifiers.extend(attributes.get("module_parts") or [])
            identifiers.extend(
                value
                for value in (attributes.get("declared_name"), attributes.get("imported_name"), attributes.get("alias_name"))
                if value not in {None, "*"}
            )
        self.assertTrue(all(is_python_310_identifier(value) for value in identifiers))

        fact_rank = {kind: index for index, kind in enumerate(profile["fact_kinds"])}
        anchor_kinds = policy["slice_policy"]["anchor_fact_kinds"]
        self.assertEqual(anchor_kinds, sorted(set(anchor_kinds), key=fact_rank.__getitem__))
        relation_rank = {kind: index for index, kind in enumerate(profile["relation_kinds"])}
        direction_rank = {"OUTBOUND": 0, "INBOUND": 1, "BOTH": 2}
        expected_relations = sorted(
            policy["slice_policy"]["allowed_relations"],
            key=lambda item: (relation_rank[item["relation_kind"]], direction_rank[item["direction"]]),
        )
        self.assertEqual(policy["slice_policy"]["allowed_relations"], expected_relations)
        self.assertEqual(
            len(expected_relations),
            len({(item["relation_kind"], item["direction"]) for item in expected_relations}),
        )
        for review_slice in self.artifacts["review-slices.json"]["slices"]:
            self.assertEqual(review_slice["slice_spec"]["allowed_relations"], expected_relations)

        schema_valid_keyword = copy.deepcopy(facts)
        module = next(item for item in schema_valid_keyword["facts"] if item["fact_kind"] == "MODULE")
        module["semantic_attributes"]["module_key_parts"] = ["class"]
        self.validators["fact-set.json"].validate(schema_valid_keyword)
        self.assertFalse(is_python_310_identifier("class"))

        schema_valid_non_normalized = copy.deepcopy(facts)
        module = next(item for item in schema_valid_non_normalized["facts"] if item["fact_kind"] == "MODULE")
        module["semantic_attributes"]["module_key_parts"] = ["\u212a"]
        self.validators["fact-set.json"].validate(schema_valid_non_normalized)
        self.assertFalse(is_python_310_identifier("\u212a"))

    def test_anchor_bounds_and_import_literal_alignment_are_conformant(self) -> None:
        snapshot = self.artifacts["source-snapshot.json"]
        facts = self.artifacts["fact-set.json"]
        relations = self.artifacts["relation-set.json"]
        blob_sizes = {
            entry["git_path"]["git_path_hex"]: entry["content"]["size_bytes"]
            for entry in snapshot["inventory"]
            if entry["entry_kind"] in {"REGULAR_BLOB", "EXECUTABLE_BLOB"}
        }
        facts_by_id = {fact["fact_id"]: fact for fact in facts["facts"]}
        for fact in facts["facts"]:
            anchor = fact["source_anchor"]
            size = blob_sizes[anchor["git_path"]["git_path_hex"]]
            self.assertLessEqual(0, anchor["start_byte"])
            self.assertLessEqual(anchor["start_byte"], anchor["end_byte"])
            self.assertLessEqual(anchor["end_byte"], size)

        out_of_bounds = copy.deepcopy(facts)
        out_of_bounds["facts"][0]["source_anchor"]["end_byte"] = next(iter(blob_sizes.values())) + 1
        self.validators["fact-set.json"].validate(out_of_bounds)
        anchor = out_of_bounds["facts"][0]["source_anchor"]
        self.assertGreater(anchor["end_byte"], blob_sizes[anchor["git_path"]["git_path_hex"]])

        for relation in relations["relations"]:
            if relation["relation_kind"] != "IMPORT_TARGET_LITERAL":
                continue
            source = facts_by_id[relation["source_fact_id"]]
            self.assertEqual(source["fact_kind"], "IMPORT_DECLARATION")
            for field in ("relative_level", "module_parts", "imported_name"):
                self.assertEqual(relation["target"][field], source["semantic_attributes"][field])

        mismatched = copy.deepcopy(relations)
        imported = next(item for item in mismatched["relations"] if item["relation_kind"] == "IMPORT_TARGET_LITERAL")
        imported["target"]["module_parts"] = ["other"]
        self.validators["relation-set.json"].validate(mismatched)
        source = facts_by_id[imported["source_fact_id"]]
        self.assertNotEqual(imported["target"]["module_parts"], source["semantic_attributes"]["module_parts"])

    def test_coverage_partition_and_status_are_semantic_not_shape_only(self) -> None:
        ledger = self.artifacts["coverage-ledger.json"]
        self.assertTrue(all(stage_partition_is_conformant(stage) for stage in ledger["stages"]))

        duplicate_terminal = copy.deepcopy(ledger)
        stage = duplicate_terminal["stages"][3]
        stage["parse_failed"] = [
            {"item_ref": copy.deepcopy(stage["completed"][0]), "reason_codes": ["PARSE_ERROR"]}
        ]
        self.validators["coverage-ledger.json"].validate(duplicate_terminal)
        self.assertFalse(stage_partition_is_conformant(stage))

        slices = self.artifacts["review-slices.json"]
        self.assertTrue(all(not item["frontier"] and item["coverage_status"] == "COMPLETE" for item in slices["slices"]))
        stale_status = copy.deepcopy(slices)
        review_slice = stale_status["slices"][0]
        relation = self.artifacts["relation-set.json"]["relations"][0]
        review_slice["frontier"] = [
            {
                "from_fact_id": relation["source_fact_id"],
                "relation_id": relation["relation_id"],
                "direction": "OUTBOUND",
                "candidate_fact_id": None,
                "candidate_depth": 1,
                "reason_codes": ["RELATION_LIMIT"],
            }
        ]
        self.validators["review-slices.json"].validate(stale_status)
        self.assertEqual(review_slice["coverage_status"], "COMPLETE")
        self.assertTrue(review_slice["frontier"])

    def test_execution_time_and_manifest_outcome_require_cross_artifact_conformance(self) -> None:
        evidence = self.artifacts["derivation-evidence.json"]
        resolved = parse_utc(evidence["request_provenance"]["resolved_at"])
        started = parse_utc(evidence["started_at"])
        finished = parse_utc(evidence["finished_at"])
        self.assertLessEqual(resolved, started)
        self.assertLessEqual(started, finished)
        for run in evidence["provider_runs"]:
            self.assertLessEqual(started, parse_utc(run["started_at"]))
            self.assertLessEqual(parse_utc(run["started_at"]), parse_utc(run["finished_at"]))
            self.assertLessEqual(parse_utc(run["finished_at"]), finished)

        reversed_time = copy.deepcopy(evidence)
        reversed_time["provider_runs"][0]["finished_at"] = "2026-09-10T00:00:04Z"
        self.validators["derivation-evidence.json"].validate(reversed_time)
        self.assertGreater(
            parse_utc(reversed_time["provider_runs"][0]["finished_at"]),
            parse_utc(reversed_time["finished_at"]),
        )

        interrupted = copy.deepcopy(evidence)
        interrupted["overall_execution_status"] = "INTERRUPTED"
        interrupted["provider_runs"][0]["execution_status"] = "INTERRUPTED"
        self.validators["derivation-evidence.json"].validate(interrupted)
        self.validators["manifest.json"].validate(self.artifacts["manifest.json"])
        self.assertFalse(
            self.artifacts["manifest.json"]["outcome_kind"] == "COMPLETE"
            and interrupted["overall_execution_status"] == "COMPLETED"
        )

    def test_all_artifact_semantic_digests_recompute_from_frozen_projections(self) -> None:
        snapshot = self.artifacts["source-snapshot.json"]
        policy = self.artifacts["review-policy.json"]
        profile = self.artifacts["derivation-profile.json"]
        evidence = self.artifacts["derivation-evidence.json"]
        fact_set = self.artifacts["fact-set.json"]
        relation_set = self.artifacts["relation-set.json"]
        slice_set = self.artifacts["review-slices.json"]
        ledger = self.artifacts["coverage-ledger.json"]

        inventory_digest = semantic_digest(
            "veritrail.review.source-inventory/0.1", snapshot["inventory"]
        )
        self.assertEqual(snapshot["inventory_digest"], inventory_digest)
        coordinate_payload = {"repository_id": snapshot["repository_id"], **snapshot["source_coordinate"]}
        coordinate_digest = semantic_digest(
            "veritrail.review.source-coordinate/0.1", coordinate_payload
        )
        self.assertEqual(snapshot["source_coordinate_digest"], coordinate_digest)
        content_digest = semantic_digest(
            "veritrail.review.source-content/0.1",
            {
                "analysis_tree_oid": snapshot["source_coordinate"]["analysis_tree_oid"],
                "analysis_root": snapshot["source_coordinate"]["analysis_root"],
                "inventory_digest": inventory_digest,
            },
        )
        self.assertEqual(snapshot["source_content_digest"], content_digest)
        self.assertEqual(
            snapshot["source_snapshot_digest"],
            semantic_digest(
                "veritrail.review.source-snapshot/0.1",
                {
                    "source_coordinate_digest": coordinate_digest,
                    "source_content_digest": content_digest,
                },
            ),
        )

        profile_payload = {key: value for key, value in profile.items() if key != "profile_digest"}
        self.assertEqual(
            profile["profile_digest"],
            semantic_digest("veritrail.review.derivation-profile/0.1", profile_payload),
        )
        analysis_scope_payload = {
            key: policy[key]
            for key in (
                "source_snapshot_digest",
                "derivation_profile_digest",
                "scope_decisions",
                "provider_requirements",
                "python_module_mapping",
            )
        }
        self.assertEqual(
            policy["analysis_scope_digest"],
            semantic_digest("veritrail.review.analysis-scope/0.1", analysis_scope_payload),
        )
        self.assertEqual(
            policy["slice_policy_digest"],
            semantic_digest(
                "veritrail.review.slice-policy/0.1",
                {
                    "analysis_scope_digest": policy["analysis_scope_digest"],
                    "slice_policy": policy["slice_policy"],
                },
            ),
        )
        policy_payload = {
            key: value
            for key, value in policy.items()
            if key not in {"analysis_scope_digest", "slice_policy_digest", "policy_digest", "seal"}
        }
        self.assertEqual(
            policy["policy_digest"],
            semantic_digest("veritrail.review.review-policy/0.1", policy_payload),
        )
        policy_without_seal = {key: value for key, value in policy.items() if key != "seal"}
        self.assertEqual(
            policy["seal"]["digest"], hashlib.sha256(canonical_json_bytes(policy_without_seal)).hexdigest()
        )

        for fact in fact_set["facts"]:
            subject_payload = {
                key: fact[key]
                for key in (
                    "source_snapshot_digest",
                    "derivation_profile_digest",
                    "source_anchor",
                    "subject_space",
                    "local_ordinal",
                )
            }
            self.assertEqual(
                fact["subject_key_digest"],
                semantic_digest("veritrail.review.fact-subject/0.1", subject_payload),
            )
            self.assertEqual(
                fact["fact_id"],
                semantic_digest(
                    "veritrail.review.code-fact/0.1",
                    {
                        "subject_key_digest": fact["subject_key_digest"],
                        "fact_kind": fact["fact_kind"],
                        "semantic_attributes": fact["semantic_attributes"],
                    },
                ),
            )
        fact_set_payload = {
            "source_snapshot_digest": fact_set["source_snapshot_digest"],
            "analysis_scope_digest": fact_set["analysis_scope_digest"],
            "derivation_profile_digest": fact_set["derivation_profile_digest"],
            "facts": [
                {key: value for key, value in fact.items() if key != "provenance_refs"}
                for fact in fact_set["facts"]
            ],
            "conflicts": [
                {key: value for key, value in conflict.items() if key != "provenance_refs"}
                for conflict in fact_set["conflicts"]
            ],
        }
        self.assertEqual(
            fact_set["fact_set_digest"],
            semantic_digest("veritrail.review.fact-set/0.1", fact_set_payload),
        )

        for relation in relation_set["relations"]:
            subject_payload = {
                "source_snapshot_digest": relation_set["source_snapshot_digest"],
                "derivation_profile_digest": relation_set["derivation_profile_digest"],
                "relation_space": relation["relation_space"],
                "source_fact_id": relation["source_fact_id"],
                "local_ordinal": relation["local_ordinal"],
            }
            self.assertEqual(
                relation["relation_subject_digest"],
                semantic_digest("veritrail.review.relation-subject/0.1", subject_payload),
            )
            self.assertEqual(
                relation["relation_id"],
                semantic_digest(
                    "veritrail.review.structural-relation/0.1",
                    {
                        "relation_subject_digest": relation["relation_subject_digest"],
                        "relation_kind": relation["relation_kind"],
                        "target": relation["target"],
                        "semantic_attributes": relation["semantic_attributes"],
                    },
                ),
            )
        relation_set_payload = {
            "source_snapshot_digest": relation_set["source_snapshot_digest"],
            "analysis_scope_digest": relation_set["analysis_scope_digest"],
            "derivation_profile_digest": relation_set["derivation_profile_digest"],
            "fact_set_digest": relation_set["fact_set_digest"],
            "relations": [
                {key: value for key, value in relation.items() if key != "provenance_refs"}
                for relation in relation_set["relations"]
            ],
            "conflicts": [
                {key: value for key, value in conflict.items() if key != "provenance_refs"}
                for conflict in relation_set["conflicts"]
            ],
        }
        self.assertEqual(
            relation_set["relation_set_digest"],
            semantic_digest("veritrail.review.relation-set/0.1", relation_set_payload),
        )

        for review_slice in slice_set["slices"]:
            spec = review_slice["slice_spec"]
            spec_payload = {key: value for key, value in spec.items() if key != "slice_spec_digest"}
            self.assertEqual(
                spec["slice_spec_digest"],
                semantic_digest("veritrail.review.slice-spec/0.1", spec_payload),
            )
            self.assertEqual(
                review_slice["slice_id"],
                semantic_digest(
                    "veritrail.review.review-slice/0.1",
                    {
                        "slice_spec_digest": spec["slice_spec_digest"],
                        "included_fact_ids": review_slice["included_fact_ids"],
                        "included_relation_ids": review_slice["included_relation_ids"],
                        "frontier": review_slice["frontier"],
                    },
                ),
            )
        slice_set_payload = {
            key: slice_set[key]
            for key in (
                "source_snapshot_digest",
                "analysis_scope_digest",
                "slice_policy_digest",
                "derivation_profile_digest",
                "fact_set_digest",
                "relation_set_digest",
                "slices",
            )
        }
        self.assertEqual(
            slice_set["slice_set_digest"],
            semantic_digest("veritrail.review.slice-set/0.1", slice_set_payload),
        )
        ledger_payload = {
            key: value for key, value in ledger.items() if key != "coverage_ledger_digest"
        }
        self.assertEqual(
            ledger["coverage_ledger_digest"],
            semantic_digest("veritrail.review.coverage-ledger/0.1", ledger_payload),
        )

        for run in evidence["provider_runs"]:
            operands_payload = {
                "source_snapshot_digest": evidence["source_snapshot_digest"],
                "policy_digest": evidence["policy_digest"],
                "analysis_scope_digest": evidence["analysis_scope_digest"],
                "slice_policy_digest": evidence["slice_policy_digest"],
                "derivation_profile_digest": evidence["derivation_profile_digest"],
                **{
                    key: run[key]
                    for key in (
                        "capability_id", "provider_id", "provider_version", "parser_id",
                        "parser_version", "runtime_id", "runtime_version"
                    )
                },
            }
            self.assertEqual(
                run["operands_digest"],
                semantic_digest("veritrail.review.provider-operands/0.1", operands_payload),
            )
            self.assertEqual(
                run["provider_run_id"],
                semantic_digest(
                    "veritrail.review.provider-run/0.1",
                    {
                        "derivation_id": evidence["derivation_id"],
                        "capability_id": run["capability_id"],
                        "provider_id": run["provider_id"],
                        "operands_digest": run["operands_digest"],
                    },
                ),
            )
        evidence_payload = {
            key: value for key, value in evidence.items() if key != "derivation_evidence_digest"
        }
        self.assertEqual(
            evidence["derivation_evidence_digest"],
            semantic_digest("veritrail.review.derivation-evidence/0.1", evidence_payload),
        )

    def test_discriminators_and_closed_objects_reject_shape_drift(self) -> None:
        snapshot = copy.deepcopy(self.artifacts["source-snapshot.json"])
        snapshot["unexpected"] = True
        self.assert_schema_rejects("source-snapshot.json", snapshot)

        snapshot = copy.deepcopy(self.artifacts["source-snapshot.json"])
        del snapshot["inventory"][0]["content"]
        self.assert_schema_rejects("source-snapshot.json", snapshot)

        snapshot = copy.deepcopy(self.artifacts["source-snapshot.json"])
        snapshot["inventory"][0]["entry_kind"] = "EXECUTABLE_BLOB"
        self.assert_schema_rejects("source-snapshot.json", snapshot)

        profile = copy.deepcopy(self.artifacts["derivation-profile.json"])
        profile["fact_kinds"].reverse()
        self.assert_schema_rejects("derivation-profile.json", profile)

        evidence = copy.deepcopy(self.artifacts["derivation-evidence.json"])
        evidence["started_at"] = "2026-09-10T08:00:00+08:00"
        self.assert_schema_rejects("derivation-evidence.json", evidence)

        facts = copy.deepcopy(self.artifacts["fact-set.json"])
        import_fact = next(item for item in facts["facts"] if item["fact_kind"] == "IMPORT_DECLARATION")
        import_fact["semantic_attributes"]["imported_name"] = "*"
        self.assert_schema_rejects("fact-set.json", facts)

        relations = copy.deepcopy(self.artifacts["relation-set.json"])
        lexical = next(item for item in relations["relations"] if item["relation_kind"] == "LEXICAL_CONTAINS")
        lexical["relation_space"] = "IMPORT_EDGE"
        self.assert_schema_rejects("relation-set.json", relations)

        relations = copy.deepcopy(self.artifacts["relation-set.json"])
        imported = next(item for item in relations["relations"] if item["relation_kind"] == "IMPORT_TARGET_LITERAL")
        imported["local_ordinal"] = 1
        self.assert_schema_rejects("relation-set.json", relations)

        ledger = copy.deepcopy(self.artifacts["coverage-ledger.json"])
        ledger["stages"][0]["frontier"] = [
            {
                "slice_id": "1" * 64,
                "frontier_item": {
                    "from_fact_id": "2" * 64,
                    "relation_id": "3" * 64,
                    "direction": "OUTBOUND",
                    "candidate_fact_id": None,
                    "candidate_depth": 1,
                    "reason_codes": ["DEPTH_LIMIT"],
                },
            }
        ]
        self.assert_schema_rejects("coverage-ledger.json", ledger)

        ledger = copy.deepcopy(self.artifacts["coverage-ledger.json"])
        ledger["stages"][6]["denominator"] = {
            "state": "UNKNOWN",
            "source_digest": None,
            "known_item_refs": [],
            "reason_codes": ["PROVIDER_CONFLICT"],
        }
        self.assert_schema_rejects("coverage-ledger.json", ledger)

        manifest = copy.deepcopy(self.artifacts["manifest.json"])
        manifest["files"][0]["path"] = "other.json"
        self.assert_schema_rejects("manifest.json", manifest)

    def test_diagnostic_manifest_shape_is_distinct_from_complete(self) -> None:
        manifest = copy.deepcopy(self.artifacts["manifest.json"])
        manifest["outcome_kind"] = "DIAGNOSTIC"
        manifest["files"] = manifest["files"][:4]
        self.validators["manifest.json"].validate(manifest)
        complete_with_four = copy.deepcopy(manifest)
        complete_with_four["outcome_kind"] = "COMPLETE"
        self.assert_schema_rejects("manifest.json", complete_with_four)


if __name__ == "__main__":
    unittest.main()
