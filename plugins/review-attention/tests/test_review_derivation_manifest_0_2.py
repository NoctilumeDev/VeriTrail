from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import json
import pickle
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

carrier_test_module = importlib.import_module(  # noqa: E402
    "test_derivation_evidence_manifest_carrier_successor"
)
from veritrail_review import (  # noqa: E402
    _review_derivation_manifest_0_2 as manifest02,
)
from veritrail_review import (  # noqa: E402
    _review_derivation_manifest_0_2_conformance as independent,
)
from veritrail_review.canonical import (  # noqa: E402
    canonical_json_bytes,
    semantic_digest,
)


REPO = ROOT.parents[1]
CORPUS = json.loads(
    (
        REPO
        / "tests"
        / "fixtures"
        / "review-derivation-manifest-0.2"
        / "compatibility-cases.json"
    ).read_text(encoding="utf-8")
)
LEGACY_SCHEMA_SHA256 = (
    "69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91"
)


class ReviewDerivationManifest02Tests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.factory = (
            carrier_test_module.DerivationEvidenceManifestCarrierSuccessorTests()
        )
        self.factory.setUp()

    @staticmethod
    def _failure(call, family):
        with unittest.TestCase().assertRaises(manifest02.Manifest02Error) as caught:
            call()
        unittest.TestCase().assertIs(caught.exception.failure_family, family)

    @staticmethod
    def _conformance_failure(snapshot, family):
        with unittest.TestCase().assertRaises(
            independent.Manifest02ConformanceFailure
        ) as caught:
            independent.validate_review_derivation_manifest_0_2_snapshot(
                snapshot
            )
        unittest.TestCase().assertEqual(caught.exception.family, family)

    def _carrier_snapshot(self, value):
        _, _, admitted = self.factory._admit(value)
        return admitted.claim_future_manifest_consumption()

    def _candidate(self, value):
        return manifest02.build_review_derivation_manifest_0_2_candidate(
            self._carrier_snapshot(value)
        )

    def _admit(self, value):
        candidate = self._candidate(value)
        validation = (
            manifest02.
            independently_validate_review_derivation_manifest_0_2_candidate(
                candidate
            )
        )
        admitted = manifest02.admit_review_derivation_manifest_0_2_candidate(
            candidate, validation
        )
        return candidate, validation, admitted

    def _normal_worlds(self):
        base = self.factory.case.support.relation_helper._inputs()
        complete = self.factory.case.support.relation_helper._with_policy(
            base, lambda policy: policy["slice_policy"].update(max_depth=99)
        )
        branch_empty = self.factory.case.support.relation_helper._with_policy(
            self.factory.case.support.relation_helper._inputs(
                bodies=[(b"pkg/a.py", b"import os\n")]
            ),
            lambda policy: policy["slice_policy"].update(
                anchor_fact_kinds=["CLASS_DECLARATION"]
            ),
        )
        return [
            (
                "NORMAL_CONSISTENT",
                self.factory._normal_value(inputs=complete)[0],
            ),
            (
                "NORMAL_BRANCH_EMPTY",
                self.factory._normal_value(inputs=branch_empty)[0],
            ),
            ("NORMAL_SLICE_PARTIAL", self.factory._normal_value()[0]),
            (
                "NORMAL_RELATION_CONFLICT",
                self.factory._normal_value(conflict=True)[0],
            ),
        ]

    def _all_worlds(self):
        base = self.factory.case.support.relation_helper._inputs()
        complete = self.factory.case.support.relation_helper._with_policy(
            base, lambda policy: policy["slice_policy"].update(max_depth=99)
        )
        branch_empty = self.factory.case.support.relation_helper._with_policy(
            self.factory.case.support.relation_helper._inputs(
                bodies=[(b"pkg/a.py", b"import os\n")]
            ),
            lambda policy: policy["slice_policy"].update(
                anchor_fact_kinds=["CLASS_DECLARATION"]
            ),
        )
        normal_worlds = (
            (
                "NORMAL_CONSISTENT",
                lambda: self.factory._normal_value(inputs=complete)[0],
            ),
            (
                "NORMAL_BRANCH_EMPTY",
                lambda: self.factory._normal_value(inputs=branch_empty)[0],
            ),
            (
                "NORMAL_SLICE_PARTIAL",
                lambda: self.factory._normal_value()[0],
            ),
            (
                "NORMAL_RELATION_CONFLICT",
                lambda: self.factory._normal_value(conflict=True)[0],
            ),
        )
        for label, build in normal_worlds:
            yield label, build()
        for index in range(4):
            label, value, _ = self.factory._negative_value(index)
            yield label, value

    def _validation_snapshot(self, value):
        candidate = self._candidate(value)
        return candidate, candidate._begin_validation()

    @staticmethod
    def _manifest(snapshot):
        return json.loads(snapshot["manifest_bytes"])

    @staticmethod
    def _replace_manifest(snapshot, value):
        snapshot["manifest_bytes"] = canonical_json_bytes(value)

    @staticmethod
    def _rebind_snapshot(snapshot):
        report = snapshot["carrier_validation"]
        report["file_binding_digest"] = semantic_digest(
            independent.CARRIER_FILE_BINDING_DOMAIN,
            list(snapshot["carrier_records"]),
        )
        unsigned = copy.deepcopy(report)
        unsigned.pop("validation_digest", None)
        report["validation_digest"] = semantic_digest(
            independent.CARRIER_VALIDATION_DOMAIN, unsigned
        )
        snapshot["input_snapshot_digest"] = semantic_digest(
            independent.INPUT_SNAPSHOT_DOMAIN,
            {
                "carrier_admission_digest": snapshot[
                    "carrier_admission_digest"
                ],
                "carrier_validation_digest": report["validation_digest"],
                "manifest_raw_sha256": hashlib.sha256(
                    snapshot["manifest_bytes"]
                ).hexdigest(),
                "records": list(snapshot["carrier_records"]),
            },
        )

    def test_all_eight_live_worlds_admit_consume_and_keep_exact_topology(self):
        observed = []
        for label, value in self._all_worlds():
            with self.subTest(world=label):
                candidate, validation, admitted = self._admit(value)
                document = (
                    manifest02.consume_admitted_review_derivation_manifest_0_2(
                        admitted
                    )
                )
                roles = [item["role"] for item in document["files"]]
                expected = (
                    CORPUS["live_relation_conflict_roles"]
                    if label == "NORMAL_RELATION_CONFLICT"
                    else (
                        CORPUS["positive_cases"][0]["expected_roles"]
                        if label.startswith("NORMAL_")
                        else CORPUS["positive_cases"][3]["expected_roles"]
                    )
                )
                self.assertEqual(roles, expected)
                self.assertEqual(document["outcome_kind"], "COVERAGE")
                self.assertEqual(validation.report_copy()["status"], "QUALIFIED")
                self.assertIs(candidate.state, manifest02.CandidateState.ADMITTED)
                staging = {}
                receipt = (
                    manifest02.stage_admitted_review_derivation_manifest_0_2(
                        admitted, staging
                    )
                )
                self.assertEqual(json.loads(staging["manifest.json"]), document)
                self.assertEqual(
                    receipt.receipt_copy()["staging_identity"],
                    manifest02.PRIVATE_STAGING_IDENTITY,
                )
                observed.append(label)
        self.assertEqual(observed, CORPUS["live_worlds"])

    def test_rdmc_000_legacy_bytes_immutable_and_no_0_2_to_0_1_fallback(self):
        legacy_path = REPO / "schemas" / "review-derivation-manifest-0.1.schema.json"
        self.assertEqual(
            hashlib.sha256(legacy_path.read_bytes()).hexdigest(),
            LEGACY_SCHEMA_SHA256,
        )
        legacy = (
            REPO
            / "tests"
            / "fixtures"
            / "review-r1-schema-0.1"
            / "valid-complete"
            / "manifest.json"
        ).read_bytes()
        self.assertIs(
            manifest02.dispatch_review_derivation_manifest_version(legacy),
            manifest02.ManifestSchemaVersion.V0_1,
        )
        value = self._normal_worlds()[0][1]
        _, _, admitted = self._admit(value)
        document = manifest02.consume_admitted_review_derivation_manifest_0_2(
            admitted
        )
        raw = canonical_json_bytes(document)
        self.assertIs(
            manifest02.dispatch_review_derivation_manifest_version(raw),
            manifest02.ManifestSchemaVersion.V0_2,
        )
        rewritten = copy.deepcopy(document)
        rewritten["schema_version"] = "0.1"
        self.assertIs(
            manifest02.dispatch_review_derivation_manifest_version(
                canonical_json_bytes(rewritten)
            ),
            manifest02.ManifestSchemaVersion.V0_1,
        )

    def test_rdmc_001_unknown_version_or_conformance_identity_rejects(self):
        unknown = canonical_json_bytes({"schema_version": "0.2.1"})
        self._failure(
            lambda: manifest02.dispatch_review_derivation_manifest_version(
                unknown
            ),
            manifest02.Manifest02FailureFamily.UNKNOWN_SCHEMA_VERSION,
        )
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        snapshot["conformance_identity"] = "unknown/9.9"
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_COMMON_MODE_OR_AUTHORITY_REJECTED"
        )
        _, snapshot = self._validation_snapshot(value)
        snapshot["producer_identity"] = "foreign-producer/9.9"
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_COMMON_MODE_OR_AUTHORITY_REJECTED"
        )
        _, snapshot = self._validation_snapshot(value)
        snapshot["producer_expected_topology"] = ["foreign"]
        self._conformance_failure(snapshot, "MANIFEST_0_2_SNAPSHOT_REJECTED")

    def test_rdmc_002_coverage_without_ledger_rejects(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        manifest = self._manifest(snapshot)
        manifest["files"] = manifest["files"][:-1]
        self._replace_manifest(snapshot, manifest)
        snapshot["carrier_records"] = snapshot["carrier_records"][:-1]
        snapshot["carrier_bytes_by_role"].pop("COVERAGE_LEDGER")
        self._conformance_failure(snapshot, "MANIFEST_0_2_TOPOLOGY_REJECTED")

    def test_rdmc_003_duplicate_role_or_path_rejects(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        manifest = self._manifest(snapshot)
        manifest["files"][5] = copy.deepcopy(manifest["files"][4])
        self._replace_manifest(snapshot, manifest)
        self._conformance_failure(snapshot, "MANIFEST_0_2_ROLE_PATH_REJECTED")

    def test_rdmc_004_role_path_swap_custom_or_traversal_rejects(self):
        value = self._normal_worlds()[0][1]
        for path in ("relation-set.json", "custom.json", "../source.json"):
            with self.subTest(path=path):
                _, snapshot = self._validation_snapshot(value)
                manifest = self._manifest(snapshot)
                manifest["files"][0]["path"] = path
                self._replace_manifest(snapshot, manifest)
                self._conformance_failure(
                    snapshot, "MANIFEST_0_2_ROLE_PATH_REJECTED"
                )

    def test_rdmc_005_ledger_not_last_rejects(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        manifest = self._manifest(snapshot)
        manifest["files"][-1], manifest["files"][-2] = (
            manifest["files"][-2],
            manifest["files"][-1],
        )
        self._replace_manifest(snapshot, manifest)
        self._conformance_failure(snapshot, "MANIFEST_0_2_TOPOLOGY_REJECTED")

    def test_rdmc_006_absence_or_unknown_placeholder_rejects(self):
        _, negative, _ = self.factory._negative_value(0)
        _, negative_snapshot = self._validation_snapshot(negative)
        normal = self._normal_worlds()[0][1]
        _, normal_snapshot = self._validation_snapshot(normal)
        manifest = self._manifest(negative_snapshot)
        normal_manifest = self._manifest(normal_snapshot)
        manifest["files"].insert(4, copy.deepcopy(normal_manifest["files"][4]))
        self._replace_manifest(negative_snapshot, manifest)
        records = list(negative_snapshot["carrier_records"])
        records.insert(4, copy.deepcopy(normal_snapshot["carrier_records"][4]))
        negative_snapshot["carrier_records"] = tuple(records)
        negative_snapshot["carrier_bytes_by_role"]["FACT_SET"] = (
            normal_snapshot["carrier_bytes_by_role"]["FACT_SET"]
        )
        self._rebind_snapshot(negative_snapshot)
        self._conformance_failure(
            negative_snapshot, "MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED"
        )

    def test_rdmc_007_present_root_without_carrier_rejects(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        manifest = self._manifest(snapshot)
        manifest["files"] = [
            item for item in manifest["files"]
            if item["role"] != "REVIEW_SLICE_SET"
        ]
        self._replace_manifest(snapshot, manifest)
        snapshot["carrier_records"] = tuple(
            item for item in snapshot["carrier_records"]
            if item["role"] != "REVIEW_SLICE_SET"
        )
        snapshot["carrier_bytes_by_role"].pop("REVIEW_SLICE_SET")
        self._rebind_snapshot(snapshot)
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED"
        )

    def test_rdmc_008_set_entry_and_root_artifact_digest_mismatch_rejects(self):
        first = self._normal_worlds()[0][1]
        second = self._normal_worlds()[1][1]
        _, snapshot = self._validation_snapshot(first)
        _, alternative = self._validation_snapshot(second)
        role = "RELATION_SET"
        raw = alternative["carrier_bytes_by_role"][role]
        document = json.loads(raw)
        manifest = self._manifest(snapshot)
        entry = next(item for item in manifest["files"] if item["role"] == role)
        entry.update(
            sha256=hashlib.sha256(raw).hexdigest(),
            size_bytes=len(raw),
            semantic_digest=document["relation_set_digest"],
        )
        self._replace_manifest(snapshot, manifest)
        snapshot["carrier_bytes_by_role"][role] = raw
        records = [copy.deepcopy(item) for item in snapshot["carrier_records"]]
        record = next(item for item in records if item["role"] == role)
        record.update(
            raw_sha256=entry["sha256"],
            size_bytes=entry["size_bytes"],
            semantic_digest=entry["semantic_digest"],
        )
        snapshot["carrier_records"] = tuple(records)
        self._rebind_snapshot(snapshot)
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED"
        )

    def test_rdmc_009_raw_sha256_mismatch_rejects(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        manifest = self._manifest(snapshot)
        manifest["files"][0]["sha256"] = "0" * 64
        self._replace_manifest(snapshot, manifest)
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_CHILD_BINDING_REJECTED"
        )

    def test_rdmc_010_size_bytes_mismatch_rejects(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        manifest = self._manifest(snapshot)
        manifest["files"][0]["size_bytes"] += 1
        self._replace_manifest(snapshot, manifest)
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_CHILD_BINDING_REJECTED"
        )

    def test_rdmc_011_ledger_entry_digest_mismatch_rejects(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        manifest = self._manifest(snapshot)
        manifest["files"][-1]["semantic_digest"] = "f" * 64
        self._replace_manifest(snapshot, manifest)
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_CHILD_BINDING_REJECTED"
        )

    def test_rdmc_012_ledger_prior_conformance_must_be_exact(self):
        value = self._normal_worlds()[0][1]
        _, snapshot = self._validation_snapshot(value)
        snapshot["carrier_validation"]["status"] = "UNQUALIFIED"
        self._conformance_failure(
            snapshot, "MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED"
        )

    def test_rdmc_013_foreign_unsafe_or_interrupted_publication_rejects(self):
        self._failure(
            lambda: manifest02.build_review_derivation_manifest_0_2_candidate(
                {"foreign": True}
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_CARRIER_INPUT_REJECTED,
        )
        self._failure(
            lambda: manifest02.stage_admitted_review_derivation_manifest_0_2(
                {"unsafe": True}, {}
            ),
            manifest02.Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED,
        )

    def test_direct_candidate_construction_cannot_bypass_one_shot_claim(self):
        value = self._normal_worlds()[0][1]
        claim = self._carrier_snapshot(value)
        consumed = claim.input_copy()
        manifest_bytes = manifest02._project_manifest(consumed)
        self._failure(
            lambda: manifest02.ReviewDerivationManifest02Candidate(
                manifest_bytes=manifest_bytes,
                consumed=consumed,
                _token=object(),
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_CARRIER_INPUT_REJECTED,
        )
        candidate = (
            manifest02.build_review_derivation_manifest_0_2_candidate(claim)
        )
        validation = (
            manifest02.
            independently_validate_review_derivation_manifest_0_2_candidate(
                candidate
            )
        )
        manifest02.admit_review_derivation_manifest_0_2_candidate(
            candidate, validation
        )

    def test_construction_and_validation_are_one_shot_under_race(self):
        value = self._normal_worlds()[0][1]
        snapshot = self._carrier_snapshot(value)

        def construct():
            try:
                candidate = (
                    manifest02.build_review_derivation_manifest_0_2_candidate(
                        snapshot
                    )
                )
                return "PASS", candidate
            except manifest02.Manifest02Error as exc:
                return "FAIL", exc.failure_family

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: construct(), range(2)))
        self.assertEqual(sum(item[0] == "PASS" for item in outcomes), 1)
        self.assertEqual(
            [item[1] for item in outcomes if item[0] == "FAIL"],
            [
                manifest02.Manifest02FailureFamily.
                MANIFEST_0_2_CONSTRUCTION_OPPORTUNITY_CONSUMED
            ],
        )
        candidate = next(item[1] for item in outcomes if item[0] == "PASS")

        def validate():
            try:
                result = (
                    manifest02.
                    independently_validate_review_derivation_manifest_0_2_candidate(
                        candidate
                    )
                )
                return "PASS", result
            except manifest02.Manifest02Error as exc:
                return "FAIL", exc.failure_family

        with ThreadPoolExecutor(max_workers=2) as pool:
            validations = list(pool.map(lambda _: validate(), range(2)))
        self.assertEqual(sum(item[0] == "PASS" for item in validations), 1)
        self.assertEqual(
            [item[1] for item in validations if item[0] == "FAIL"],
            [manifest02.Manifest02FailureFamily.MANIFEST_0_2_ALREADY_VALIDATED],
        )

    def test_failed_construction_and_validation_consume_their_opportunity(self):
        value = self._normal_worlds()[0][1]
        snapshot = self._carrier_snapshot(value)
        snapshot._ClaimedFutureManifestCarrierSnapshot__owned_snapshot_seal = (
            "0" * 64
        )
        self._failure(
            lambda: manifest02.build_review_derivation_manifest_0_2_candidate(
                snapshot
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_CARRIER_INPUT_REJECTED,
        )
        self._failure(
            lambda: manifest02.build_review_derivation_manifest_0_2_candidate(
                snapshot
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_CONSTRUCTION_OPPORTUNITY_CONSUMED,
        )

        candidate = self._candidate(self._normal_worlds()[0][1])
        raw_by_role = (
            candidate.
            _ReviewDerivationManifest02Candidate__bytes_by_role
        )
        raw_by_role["SOURCE_SNAPSHOT"] += b" "
        self._failure(
            lambda: (
                manifest02.
                independently_validate_review_derivation_manifest_0_2_candidate(
                    candidate
                )
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_CHILD_BINDING_REJECTED,
        )
        self.assertIs(candidate.state, manifest02.CandidateState.REVOKED)
        self._failure(
            lambda: (
                manifest02.
                independently_validate_review_derivation_manifest_0_2_candidate(
                    candidate
                )
            ),
            manifest02.Manifest02FailureFamily.MANIFEST_0_2_ALREADY_VALIDATED,
        )

    def test_private_staging_failure_and_race_are_one_shot(self):
        _, _, failed = self._admit(self._normal_worlds()[0][1])
        self._failure(
            lambda: manifest02.stage_admitted_review_derivation_manifest_0_2(
                failed, {"manifest.json": b"occupied"}
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_PRIVATE_STAGING_REJECTED,
        )
        self._failure(
            lambda: manifest02.stage_admitted_review_derivation_manifest_0_2(
                failed, {}
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED,
        )

        _, _, admitted = self._admit(self._normal_worlds()[0][1])

        def stage():
            try:
                receipt = (
                    manifest02.stage_admitted_review_derivation_manifest_0_2(
                        admitted, {}
                    )
                )
                return "PASS", receipt.receipt_copy()["receipt_digest"]
            except manifest02.Manifest02Error as exc:
                return "FAIL", exc.failure_family

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: stage(), range(2)))
        self.assertEqual(sum(item[0] == "PASS" for item in outcomes), 1)
        self.assertEqual(
            [item[1] for item in outcomes if item[0] == "FAIL"],
            [
                manifest02.Manifest02FailureFamily.
                MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED
            ],
        )

    def test_snapshot_mutation_replay_copy_and_private_staging_fail_closed(self):
        value = self._normal_worlds()[0][1]
        candidate = self._candidate(value)
        candidate._ReviewDerivationManifest02Candidate__manifest_bytes += b" "
        self._failure(
            lambda: (
                manifest02.
                independently_validate_review_derivation_manifest_0_2_candidate(
                    candidate
                )
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_SNAPSHOT_MUTATION_REJECTED,
        )
        self.assertIs(candidate.state, manifest02.CandidateState.REVOKED)

        _, _, admitted = self._admit(self._normal_worlds()[0][1])
        for operation in (
            lambda: copy.copy(admitted),
            lambda: copy.deepcopy(admitted),
            lambda: pickle.dumps(admitted),
            admitted.to_json,
        ):
            self._failure(
                operation,
                manifest02.Manifest02FailureFamily.
                MANIFEST_0_2_ADMISSION_REJECTED,
            )
        staging = {}
        manifest02.stage_admitted_review_derivation_manifest_0_2(
            admitted, staging
        )
        self._failure(
            lambda: manifest02.stage_admitted_review_derivation_manifest_0_2(
                admitted, {}
            ),
            manifest02.Manifest02FailureFamily.
            MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED,
        )

    def test_independent_conformance_does_not_import_producer_or_read_paths(self):
        conformance_source = (
            REPO
            / "plugins"
            / "review-attention"
            / "src"
            / "veritrail_review"
            / "_review_derivation_manifest_0_2_conformance.py"
        ).read_text(encoding="utf-8")
        syntax = ast.parse(conformance_source)
        imported_names = []
        called_names = []
        for node in ast.walk(syntax):
            if isinstance(node, ast.Import):
                imported_names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported_names.append(node.module or "")
                imported_names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    called_names.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    called_names.append(node.func.attr)
        executable_names = [*imported_names, *called_names]
        self.assertFalse(
            any(
                "_review_derivation_manifest_0_2" in name
                for name in imported_names
            )
        )
        self.assertFalse(
            any("provider" in name.lower() for name in executable_names)
        )
        self.assertNotIn("pathlib", imported_names)
        self.assertTrue(
            {"open", "read_text", "read_bytes"}.isdisjoint(called_names)
        )
        value = self._normal_worlds()[0][1]
        _, validation, _ = self._admit(value)
        self.assertEqual(
            validation.report_copy()["conformance_identity"],
            independent.CONFORMANCE_IDENTITY,
        )


if __name__ == "__main__":
    unittest.main()
