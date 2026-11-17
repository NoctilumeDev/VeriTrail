from __future__ import annotations

import copy
import hashlib
import json
import pickle
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_same_attempt_derivation_evidence_continuity as support_module  # noqa: E402
from veritrail_review import (  # noqa: E402
    _derivation_evidence_manifest_carrier_conformance as independent,
)
from veritrail_review import (  # noqa: E402
    _derivation_evidence_manifest_carrier_successor as successor,
)
from veritrail_review import _fact_relation_transition as transition  # noqa: E402
from veritrail_review import (  # noqa: E402
    _relation_observation_application as relation_application,
)
from veritrail_review import (  # noqa: E402
    _relation_transition_slice_composition as positive,
)
from veritrail_review import (  # noqa: E402
    _unified_review_coverage_output_admission as unified,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402


class DerivationEvidenceManifestCarrierSuccessorTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.case = support_module.SameAttemptDerivationEvidenceContinuityTests()
        self.case.setUp()

    @staticmethod
    def _failure(call, family):
        with unittest.TestCase().assertRaises(
            successor.ManifestCarrierSuccessorError
        ) as caught:
            call()
        unittest.TestCase().assertEqual(caught.exception.failure_family, family)

    @staticmethod
    def _admit(value):
        claim = successor.project_manifest_carrier_successor(value)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)
        validation = (
            successor.independently_validate_manifest_carrier_successor_candidate(
                candidate
            )
        )
        carrier = successor.admit_manifest_carrier_successor_candidate(
            candidate, validation
        )
        return candidate, validation, carrier

    def _normal_value(self, *, inputs=None, conflict=False):
        selector, _, exact_inputs, _, _ = self.case.support._terminal(inputs)
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        if conflict:
            original = (
                transition._source_operation_cell.
                run_prepared_relation_observation_source_operation_attempt
            )

            def conflicting(prepared):
                phase = original(prepared)
                if not prepared.binding.descriptor.provider_id.endswith(
                    "provider-b"
                ):
                    return phase
                request = relation_application._synthetic_request(
                    prepared.request_document, phase.provider_run_id
                )
                relations = list(phase.canonical_relations_copy())
                lexical = [
                    item
                    for item in relations
                    if item["relation_kind"] == "LEXICAL_CONTAINS"
                ]
                first = lexical[0]
                second = next(
                    item
                    for item in lexical[1:]
                    if item["source_fact_id"] == first["source_fact_id"]
                    and item["target"] != first["target"]
                )
                candidate = {
                    key: copy.deepcopy(first[key])
                    for key in (
                        "relation_space",
                        "relation_kind",
                        "source_fact_id",
                        "local_ordinal",
                        "target",
                        "semantic_attributes",
                    )
                }
                candidate["target"] = copy.deepcopy(second["target"])
                alternative = (
                    relation_application.canonicalize_relation_observation_candidates(
                        request, [candidate]
                    )[0]
                )
                relations = [
                    item
                    for item in relations
                    if item["relation_id"] != second["relation_id"]
                ]
                relations.append(alternative)
                relations.sort(key=lambda item: item["relation_id"])
                target_item = relation_application.relation_for_observation_item(
                    request, alternative
                )
                outcomes = [json.loads(raw) for raw in phase.observation_outcome_bytes]
                outcome = next(
                    item
                    for item in outcomes
                    if item["observation_item_id"] == target_item
                )
                replacement = relation_application.build_provider_outcome(
                    provider_run_id_value=phase.provider_run_id,
                    observation_item_id=target_item,
                    disposition="CANDIDATE_REPORTED",
                    reported_relation_ids=[alternative["relation_id"]],
                )
                outcomes[outcomes.index(outcome)] = replacement
                outcomes.sort(
                    key=lambda item: (
                        item["observation_item_id"],
                        item["observation_outcome_id"],
                    )
                )
                return replace(
                    phase,
                    canonical_relation_bytes=tuple(
                        canonical_json_bytes(item) for item in relations
                    ),
                    observation_outcome_bytes=tuple(
                        canonical_json_bytes(item) for item in outcomes
                    ),
                    reported_relation_ids=tuple(
                        item["relation_id"] for item in relations
                    ),
                )

            patch = mock.patch.object(
                transition._source_operation_cell,
                "run_prepared_relation_observation_source_operation_attempt",
                side_effect=conflicting,
            )
        else:
            patch = mock.patch.object(
                transition._source_operation_cell,
                "run_prepared_relation_observation_source_operation_attempt",
                wraps=(
                    transition._source_operation_cell.
                    run_prepared_relation_observation_source_operation_attempt
                ),
            )
        with patch:
            admitted_transition = (
                transition.run_claimed_fact_handoff_relation_transition(claim)
            )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        admitted = owner.submit(result)
        return (
            admitted._same_attempt_derivation_evidence_continuity(),
            exact_inputs,
            result.document_copy(),
        )

    def _negative_value(self, index):
        with mock.patch.object(
            support_module.post_terminal_support.parse_support.ParseHelper,
            "_context",
            side_effect=self.case._semantic_context,
        ):
            expected, value, *rest = self.case._negative(index)
        return expected, value, rest

    @staticmethod
    def _candidate_snapshot(value):
        claim = successor.project_manifest_carrier_successor(value)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)
        return candidate, candidate._begin_validation()

    @staticmethod
    def _entry(snapshot, role):
        return next(
            item for item in snapshot["file_entries"] if item["role"] == role
        )

    @staticmethod
    def _replace_entry(snapshot, role, document, *, recompute_digest=True):
        entries = [copy.deepcopy(item) for item in snapshot["file_entries"]]
        entry = next(item for item in entries if item["role"] == role)
        raw = canonical_json_bytes(document)
        entry["bytes"] = raw
        if recompute_digest:
            digest_key = {
                "DERIVATION_EVIDENCE": "derivation_evidence_digest",
                "COVERAGE_LEDGER": "coverage_ledger_digest",
            }[role]
            entry["semantic_digest"] = document[digest_key]
        snapshot["file_entries"] = tuple(entries)
        records = []
        for item in entries:
            records.append(
                {
                    "role": item["role"],
                    "path": item["path"],
                    "raw_sha256": hashlib.sha256(item["bytes"]).hexdigest(),
                    "size_bytes": len(item["bytes"]),
                    "semantic_digest": item["semantic_digest"],
                }
            )
        snapshot["file_records"] = tuple(records)

    @staticmethod
    def _conformance_failure(snapshot, family):
        with unittest.TestCase().assertRaises(
            independent.IndependentCarrierConformanceFailure
        ) as caught:
            independent.validate_manifest_carrier_successor_snapshot(snapshot)
        unittest.TestCase().assertEqual(caught.exception.family, family)

    def test_demc_000_all_eight_live_worlds_admit_exactly_one_carrier(self):
        base = self.case.support.relation_helper._inputs()
        complete = self.case.support.relation_helper._with_policy(
            base, lambda policy: policy["slice_policy"].update(max_depth=99)
        )
        branch_empty = self.case.support.relation_helper._with_policy(
            self.case.support.relation_helper._inputs(
                bodies=[(b"pkg/a.py", b"import os\n")]
            ),
            lambda policy: policy["slice_policy"].update(
                anchor_fact_kinds=["CLASS_DECLARATION"]
            ),
        )
        normal_worlds = [
            ("NORMAL_CONSISTENT", *self._normal_value(inputs=complete)),
            ("NORMAL_BRANCH_EMPTY", *self._normal_value(inputs=branch_empty)),
            ("NORMAL_SLICE_PARTIAL", *self._normal_value()),
            ("NORMAL_RELATION_CONFLICT", *self._normal_value(conflict=True)),
        ]
        observations = []
        for label, value, _inputs, result in normal_worlds:
            with self.subTest(world=label):
                _, validation, carrier = self._admit(value)
                consumed = carrier.claim_future_manifest_consumption().input_copy()
                roles = [item["role"] for item in consumed["files"]]
                roots = {
                    item["stage"]: item
                    for item in result["coverage_ledger"]["root_bindings"]
                }
                self.assertEqual(consumed["validation"]["status"], "QUALIFIED")
                self.assertEqual(roles[:4], [
                    "SOURCE_SNAPSHOT",
                    "REVIEW_POLICY",
                    "DERIVATION_PROFILE",
                    "DERIVATION_EVIDENCE",
                ])
                self.assertEqual(roles[-1], "COVERAGE_LEDGER")
                self.assertIn("FACT_SET", roles)
                self.assertIn("RELATION_SET", roles)
                self.assertEqual(
                    "REVIEW_SLICE_SET" in roles,
                    roots["REVIEW_SLICE_SET"]["binding_state"]
                    == "ARTIFACT_PRESENT",
                )
                self.assertEqual(
                    validation.report_copy()["root_chain_digest"],
                    result["coverage_ledger"]["root_chain_digest"],
                )
                observations.append(label)
        for index in range(4):
            expected, value, _ = self._negative_value(index)
            with self.subTest(world=expected):
                _, _, carrier = self._admit(value)
                consumed = carrier.claim_future_manifest_consumption().input_copy()
                self.assertEqual(
                    [item["role"] for item in consumed["files"]],
                    [
                        "SOURCE_SNAPSHOT",
                        "REVIEW_POLICY",
                        "DERIVATION_PROFILE",
                        "DERIVATION_EVIDENCE",
                        "COVERAGE_LEDGER",
                    ],
                )
                observations.append(expected)
        self.assertEqual(
            observations,
            [
                "NORMAL_CONSISTENT",
                "NORMAL_BRANCH_EMPTY",
                "NORMAL_SLICE_PARTIAL",
                "NORMAL_RELATION_CONFLICT",
                "ZERO_PARSE_DENOMINATOR",
                "ALL_PARSE_REJECTED",
                "PROJECTION_BLOCKED",
                "REQUIRED_PROVIDER_NON_SUCCESS",
            ],
        )

    def test_demc_001_exact_0_3_dispatch_has_no_legacy_fallback(self):
        value, *_ = self._normal_value()
        for version in ("0.2", "9.9"):
            _, snapshot = self._candidate_snapshot(value)
            evidence = json.loads(
                self._entry(snapshot, "DERIVATION_EVIDENCE")["bytes"]
            )
            evidence["schema_version"] = version
            self._replace_entry(
                snapshot, "DERIVATION_EVIDENCE", evidence, recompute_digest=False
            )
            self._conformance_failure(
                snapshot, "MANIFEST_CARRIER_SUCCESSOR_VERSION_REJECTED"
            )

    def test_demc_002_branch_route_variant_are_jointly_discriminated(self):
        for field, value in (
            ("terminal_branch", "ZERO_PARSE_DENOMINATOR"),
            ("selector_route", "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"),
            ("continuity_variant", "NEGATIVE_WORLD_COVERAGE_CONTINUITY"),
        ):
            exact, *_ = self._normal_value()
            _, snapshot = self._candidate_snapshot(exact)
            evidence = json.loads(
                self._entry(snapshot, "DERIVATION_EVIDENCE")["bytes"]
            )
            evidence[field] = value
            evidence["derivation_evidence_digest"] = semantic_digest(
                independent.EVIDENCE_IDENTITY_DOMAIN,
                {
                    key: copy.deepcopy(item)
                    for key, item in evidence.items()
                    if key != "derivation_evidence_digest"
                },
            )
            self._replace_entry(snapshot, "DERIVATION_EVIDENCE", evidence)
            self._conformance_failure(
                snapshot, "MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED"
            )

    def test_demc_003_ledger_and_root_chain_drift_reject(self):
        value, *_ = self._normal_value()
        _, snapshot = self._candidate_snapshot(value)
        ledger = json.loads(self._entry(snapshot, "COVERAGE_LEDGER")["bytes"])
        ledger["root_chain_digest"] = "0" * 64
        self._replace_entry(snapshot, "COVERAGE_LEDGER", ledger)
        self._conformance_failure(
            snapshot, "MANIFEST_CARRIER_LEDGER_CONFORMANCE_REJECTED"
        )

    def test_demc_004_equal_shape_foreign_attempt_rejects(self):
        first, *_ = self._normal_value()
        second, *_ = self._normal_value()
        claim = successor.project_manifest_carrier_successor(first)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)
        candidate._ManifestCarrierSuccessorCandidate__continuity = second
        candidate._ManifestCarrierSuccessorCandidate__bound_continuity = second
        self._failure(
            lambda: successor.independently_validate_manifest_carrier_successor_candidate(
                candidate
            ),
            successor.ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED,
        )

        value, *_ = self._normal_value()
        _, snapshot = self._candidate_snapshot(value)
        binding = json.loads(snapshot["attempt_binding_bytes"])
        binding["application_result_status"] = "COMPLETED"
        snapshot["attempt_binding_bytes"] = canonical_json_bytes(binding)
        self._conformance_failure(
            snapshot, "MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED"
        )

        value, *_ = self._normal_value()
        _, snapshot = self._candidate_snapshot(value)
        binding = json.loads(snapshot["attempt_binding_bytes"])
        binding["context_identity"] = "0" * 64
        snapshot["attempt_binding_bytes"] = canonical_json_bytes(binding)
        self._conformance_failure(
            snapshot, "MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED"
        )

    def test_demc_005_owned_snapshot_mutation_permanently_revokes(self):
        value, *_ = self._normal_value()
        claim = successor.project_manifest_carrier_successor(value)
        claim_entries = claim._ManifestCarrierProjectionClaim__file_entries
        claim_entries[0]["bytes"] = claim_entries[0]["bytes"] + b" "
        self._failure(
            lambda: successor.build_manifest_carrier_successor_candidate(claim),
            successor.ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED,
        )

        value, *_ = self._normal_value()
        claim = successor.project_manifest_carrier_successor(value)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)
        entries = candidate._ManifestCarrierSuccessorCandidate__file_entries
        entries[0]["bytes"] = entries[0]["bytes"] + b" "
        self._failure(
            lambda: successor.independently_validate_manifest_carrier_successor_candidate(
                candidate
            ),
            successor.ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED,
        )
        self.assertEqual(candidate.state, successor.CandidateState.REVOKED)

    def test_demc_006_present_root_without_file_rejects(self):
        value, *_ = self._normal_value()
        _, snapshot = self._candidate_snapshot(value)
        snapshot["file_entries"] = tuple(
            item
            for item in snapshot["file_entries"]
            if item["role"] != "REVIEW_SLICE_SET"
        )
        snapshot["file_records"] = tuple(
            item
            for item in snapshot["file_records"]
            if item["role"] != "REVIEW_SLICE_SET"
        )
        self._conformance_failure(snapshot, "MANIFEST_CARRIER_TOPOLOGY_REJECTED")

    def test_demc_007_absence_cannot_be_placeholder_file(self):
        _, negative_value, _ = self._negative_value(0)
        _, negative_snapshot = self._candidate_snapshot(negative_value)
        normal_value, *_ = self._normal_value()
        _, normal_snapshot = self._candidate_snapshot(normal_value)
        fact_entry = copy.deepcopy(self._entry(normal_snapshot, "FACT_SET"))
        entries = list(negative_snapshot["file_entries"])
        entries.insert(-1, fact_entry)
        negative_snapshot["file_entries"] = tuple(entries)
        records = list(negative_snapshot["file_records"])
        records.insert(
            -1,
            {
                "role": fact_entry["role"],
                "path": fact_entry["path"],
                "raw_sha256": hashlib.sha256(fact_entry["bytes"]).hexdigest(),
                "size_bytes": len(fact_entry["bytes"]),
                "semantic_digest": fact_entry["semantic_digest"],
            },
        )
        negative_snapshot["file_records"] = tuple(records)
        self._conformance_failure(
            negative_snapshot, "MANIFEST_CARRIER_TOPOLOGY_REJECTED"
        )

    def test_demc_008_closed_empty_is_still_present(self):
        branch_empty = self.case.support.relation_helper._with_policy(
            self.case.support.relation_helper._inputs(
                bodies=[(b"pkg/a.py", b"import os\n")]
            ),
            lambda policy: policy["slice_policy"].update(
                anchor_fact_kinds=["CLASS_DECLARATION"]
            ),
        )
        value, _, result = self._normal_value(inputs=branch_empty)
        self.assertEqual(
            result["slice_set_admission"]["terminal_branch"], "CLOSED_EMPTY"
        )
        self.assertEqual(result["review_slice_set"]["slices"], [])
        _, snapshot = self._candidate_snapshot(value)
        snapshot["file_entries"] = tuple(
            item
            for item in snapshot["file_entries"]
            if item["role"] != "REVIEW_SLICE_SET"
        )
        snapshot["file_records"] = tuple(
            item
            for item in snapshot["file_records"]
            if item["role"] != "REVIEW_SLICE_SET"
        )
        self._conformance_failure(snapshot, "MANIFEST_CARRIER_TOPOLOGY_REJECTED")

    def test_demc_009_relation_conflict_keeps_slice_qualified_unknown(self):
        conflict, *_ = self._normal_value(conflict=True)
        _, snapshot = self._candidate_snapshot(conflict)
        normal, *_ = self._normal_value()
        _, normal_snapshot = self._candidate_snapshot(normal)
        slice_entry = copy.deepcopy(
            self._entry(normal_snapshot, "REVIEW_SLICE_SET")
        )
        entries = list(snapshot["file_entries"])
        entries.insert(-1, slice_entry)
        snapshot["file_entries"] = tuple(entries)
        records = list(snapshot["file_records"])
        records.insert(
            -1,
            {
                "role": slice_entry["role"],
                "path": slice_entry["path"],
                "raw_sha256": hashlib.sha256(slice_entry["bytes"]).hexdigest(),
                "size_bytes": len(slice_entry["bytes"]),
                "semantic_digest": slice_entry["semantic_digest"],
            },
        )
        snapshot["file_records"] = tuple(records)
        self._conformance_failure(snapshot, "MANIFEST_CARRIER_TOPOLOGY_REJECTED")

    def test_demc_010_fixture_or_legacy_mapping_has_no_live_alias(self):
        self._failure(
            lambda: successor.project_manifest_carrier_successor(
                {
                    "schema_version": "0.2",
                    "continuity": "fixture-only",
                }
            ),
            successor.ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_LEGACY_ALIAS_REJECTED,
        )

    def test_demc_011_role_path_order_and_ledger_tail_are_frozen(self):
        value, *_ = self._normal_value()
        for mutation in ("path", "order", "duplicate"):
            _, snapshot = self._candidate_snapshot(value)
            entries = [copy.deepcopy(item) for item in snapshot["file_entries"]]
            records = [copy.deepcopy(item) for item in snapshot["file_records"]]
            if mutation == "path":
                entries[0]["path"], entries[1]["path"] = (
                    entries[1]["path"],
                    entries[0]["path"],
                )
                records[0]["path"], records[1]["path"] = (
                    records[1]["path"],
                    records[0]["path"],
                )
            elif mutation == "order":
                entries[-1], entries[-2] = entries[-2], entries[-1]
                records[-1], records[-2] = records[-2], records[-1]
            else:
                entries.insert(1, copy.deepcopy(entries[0]))
                records.insert(1, copy.deepcopy(records[0]))
            snapshot["file_entries"] = tuple(entries)
            snapshot["file_records"] = tuple(records)
            self._conformance_failure(
                snapshot, "MANIFEST_CARRIER_TOPOLOGY_REJECTED"
            )

    def test_demc_012_raw_size_and_semantic_records_are_independently_checked(self):
        value, *_ = self._normal_value()
        for field, replacement in (
            ("raw_sha256", "0" * 64),
            ("size_bytes", 1),
            ("semantic_digest", "f" * 64),
        ):
            _, snapshot = self._candidate_snapshot(value)
            records = [copy.deepcopy(item) for item in snapshot["file_records"]]
            records[0][field] = replacement
            snapshot["file_records"] = tuple(records)
            self._conformance_failure(
                snapshot, "MANIFEST_CARRIER_CHILD_BINDING_REJECTED"
            )

    def test_demc_013_common_mode_projector_state_rejects(self):
        value, *_ = self._normal_value()
        _, snapshot = self._candidate_snapshot(value)
        snapshot["shared_expected_projector_state"] = True
        self._conformance_failure(
            snapshot, "MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED"
        )

    def test_demc_014_validation_does_not_read_paths_or_reinvoke_provider(self):
        value, *_ = self._normal_value()
        claim = successor.project_manifest_carrier_successor(value)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)
        with mock.patch.object(
            Path, "read_bytes", side_effect=AssertionError("path reread")
        ), mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            side_effect=AssertionError("provider reinvoked"),
        ):
            validation = (
                successor.independently_validate_manifest_carrier_successor_candidate(
                    candidate
                )
            )
        self.assertEqual(validation.report_copy()["status"], "QUALIFIED")

    def test_demc_015_late_stop_has_no_admission(self):
        value, _, _, _, _, _, _, _, _, context, _ = self.case._normal()
        claim = successor.project_manifest_carrier_successor(value)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)
        self.assertTrue(context.request_cancellation())
        self._failure(
            lambda: successor.independently_validate_manifest_carrier_successor_candidate(
                candidate
            ),
            successor.ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_CONTEXT_REVOKED,
        )

    def test_demc_016_validation_replay_and_race_have_one_winner(self):
        value, *_ = self._normal_value()
        claim = successor.project_manifest_carrier_successor(value)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)

        def run():
            try:
                result = (
                    successor.independently_validate_manifest_carrier_successor_candidate(
                        candidate
                    )
                )
                return ("PASS", result.report_copy()["status"])
            except successor.ManifestCarrierSuccessorError as exc:
                return ("FAIL", exc.failure_family.value)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: run(), range(2)))
        self.assertEqual(sum(item[0] == "PASS" for item in outcomes), 1)
        self.assertEqual(
            sum(
                item
                == (
                    "FAIL",
                    successor.ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_ALREADY_VALIDATED.value,
                )
                for item in outcomes
            ),
            1,
        )

    def test_demc_017_future_manifest_consumption_is_one_shot_and_racy(self):
        value, *_ = self._normal_value()
        _, _, carrier = self._admit(value)

        def consume():
            try:
                return (
                    "PASS",
                    carrier.claim_future_manifest_consumption().input_copy()[
                        "consumption_identity"
                    ],
                )
            except successor.ManifestCarrierSuccessorError as exc:
                return ("FAIL", exc.failure_family.value)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: consume(), range(2)))
        self.assertEqual(sum(item[0] == "PASS" for item in outcomes), 1)
        self.assertEqual(
            sum(
                item
                == (
                    "FAIL",
                    successor.ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_ALREADY_CONSUMED.value,
                )
                for item in outcomes
            ),
            1,
        )

    def test_demc_018_truth_sufficiency_and_verdict_authority_reject(self):
        value, *_ = self._normal_value()
        for field in ("truth", "sufficiency", "core_verdict"):
            _, snapshot = self._candidate_snapshot(value)
            snapshot["authority_ceiling"][field] = True
            self._conformance_failure(
                snapshot, "MANIFEST_CARRIER_AUTHORITY_CEILING_REJECTED"
            )

    def test_demc_019_legacy_bytes_and_private_values_are_immutable(self):
        guards = {
            "schemas/review-derivation-evidence-0.2.schema.json": (
                "66190e12fad8c3bbec3615c25b1bbaf3cfb1ef723267e0e99185dcf05b8238e6"
            ),
            "schemas/review-derivation-manifest-0.1.schema.json": (
                "69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91"
            ),
        }
        repo = ROOT.parents[1]
        for relative, expected in guards.items():
            self.assertEqual(
                hashlib.sha256((repo / relative).read_bytes()).hexdigest(),
                expected,
            )
        value, *_ = self._normal_value()
        claim = successor.project_manifest_carrier_successor(value)
        candidate = successor.build_manifest_carrier_successor_candidate(claim)
        for operation in (
            lambda: copy.copy(candidate),
            lambda: copy.deepcopy(candidate),
            lambda: pickle.dumps(candidate),
            candidate.to_json,
        ):
            with self.assertRaises(successor.ManifestCarrierSuccessorError):
                operation()


if __name__ == "__main__":
    unittest.main()
