from __future__ import annotations

import copy
import hashlib
import inspect
import sys
import unittest
from dataclasses import replace
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_relation_observation_qualification as qualification_test_support  # noqa: E402
from veritrail_review import _relation_set_admission as admission  # noqa: E402
from veritrail_review._relation_set_admission_values import (  # noqa: E402
    _RelationSetAdmissionError,
    _RelationSetAdmissionFailureCode,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402


class RelationSetAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        support = qualification_test_support.RelationObservationQualificationTests
        support.setUpClass()
        cls.support = support
        cls.positive = support.positive
        cls.conflicting = support.conflicting
        cls.not_qualified = support.a_unavailable
        cls.admitted = admission.admit_relation_set_for_private_closed_proof(
            cls.positive
        )
        cls.projected = admission.project_private_derivation_evidence_0_2(
            cls.admitted
        )
        cls.second_qualification = support._run_with_import_facts(
            inputs=support.inputs,
            derivation_id="rae-independent-attempt",
        )
        cls.second_admitted = admission.admit_relation_set_for_private_closed_proof(
            cls.second_qualification
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.support.tearDownClass()

    def assertAdmissionFailure(self, code, callback) -> None:  # noqa: N802
        with self.assertRaises(_RelationSetAdmissionError) as caught:
            callback()
        self.assertIs(caught.exception.code, code)

    def test_rae_000_not_qualified_stops_before_relation_set_or_witness(self) -> None:
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.QUALIFICATION_REJECTED,
            lambda: admission.admit_relation_set_for_private_closed_proof(
                self.not_qualified
            ),
        )

    def test_rae_001_exact_qualified_membership_forms_private_state(self) -> None:
        relation_set = self.admitted.relation_set_document_copy()
        witness = self.admitted.admission_witness_copy()
        self.assertEqual(relation_set["artifact_kind"], "RELATION_SET")
        self.assertEqual(relation_set["schema_version"], "0.1")
        self.assertEqual(
            [item["relation_id"] for item in relation_set["relations"]],
            list(self.admitted.admitted_relation_ids),
        )
        self.assertEqual(
            witness["admission_claim"]["relation_set_digest"],
            self.admitted.relation_set_digest,
        )
        self.assertFalse(hasattr(self.admitted, "output_path"))
        self.assertFalse(hasattr(self.admitted, "manifest"))

    def test_rae_002_digest_alone_is_not_an_admission_input(self) -> None:
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.QUALIFICATION_REJECTED,
            lambda: admission.admit_relation_set_for_private_closed_proof(
                self.positive.qualification_digest
            ),
        )

    def test_rae_003_relation_set_semantic_tamper_is_rejected(self) -> None:
        relation_set = self.admitted.relation_set_document_copy()
        relation_set["relations"][1]["target"]["module_parts"] = ["forged"]
        forged = replace(
            self.admitted,
            relation_set_document_bytes=canonical_json_bytes(relation_set),
            canonical_relation_set_artifact_bytes=(
                canonical_json_bytes(relation_set) + b"\n"
            ),
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(forged),
        )

    def test_rae_004_provenance_and_reverse_run_closure_are_revalidated(self) -> None:
        relation_set = self.admitted.relation_set_document_copy()
        relation_set["relations"][0]["provenance_refs"] = ["0" * 64]
        forged_relation_set = replace(
            self.admitted,
            relation_set_document_bytes=canonical_json_bytes(relation_set),
            canonical_relation_set_artifact_bytes=(
                canonical_json_bytes(relation_set) + b"\n"
            ),
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(
                forged_relation_set
            ),
        )
        missing_run = replace(
            self.admitted,
            provider_run_bytes=self.admitted.provider_run_bytes[:-1],
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(missing_run),
        )

    def test_relation_target_is_revalidated_against_the_exact_fact(self) -> None:
        phases = list(self.positive.relation_phase_results)
        phase = phases[1]
        relations = list(phase.canonical_relations_copy())
        target_relation = next(
            item
            for item in relations
            if item["relation_kind"] == "IMPORT_TARGET_LITERAL"
        )
        old_relation_id = target_relation["relation_id"]
        target_relation["target"]["module_parts"] = ["forged"]
        target_relation["relation_id"] = semantic_digest(
            "veritrail.review.structural-relation/0.1",
            {
                "relation_subject_digest": target_relation[
                    "relation_subject_digest"
                ],
                "relation_kind": target_relation["relation_kind"],
                "target": target_relation["target"],
                "semantic_attributes": target_relation["semantic_attributes"],
            },
        )
        new_relation_id = target_relation["relation_id"]

        outcomes = list(phase.observation_outcomes_copy())
        for outcome in outcomes:
            if old_relation_id not in outcome["reported_relation_ids"]:
                continue
            outcome["reported_relation_ids"] = [new_relation_id]
            outcome["observation_outcome_id"] = semantic_digest(
                "veritrail.review.relation-observation-outcome/0.1",
                {
                    "provider_run_id": outcome["provider_run_id"],
                    "observation_item_id": outcome["observation_item_id"],
                    "disposition": outcome["disposition"],
                    "reported_relation_ids": outcome["reported_relation_ids"],
                },
            )
        phase = replace(
            phase,
            canonical_relation_bytes=tuple(
                canonical_json_bytes(item) for item in relations
            ),
            observation_outcome_bytes=tuple(
                canonical_json_bytes(item) for item in outcomes
            ),
            reported_relation_ids=tuple(
                sorted(
                    new_relation_id if item == old_relation_id else item
                    for item in phase.reported_relation_ids
                )
            ),
        )
        phases[1] = phase

        domain = self.positive.observation_domain_copy()
        relation_runs = [
            admission._relation_provider_run_document(item) for item in phases
        ]
        receipts = [
            admission._observation_receipt(
                domain, item.provider_descriptor, item
            )
            for item in phases
        ]
        merged, conflicts = admission._compose_candidates(phases)
        claim = admission._qualification_claim(
            self.positive,
            relation_runs,
            receipts,
            merged,
            conflicts,
        )
        forged = replace(
            self.positive,
            relation_phase_results=tuple(phases),
            relation_provider_run_bytes=tuple(
                canonical_json_bytes(item) for item in relation_runs
            ),
            observation_receipt_bytes=tuple(
                canonical_json_bytes(item) for item in receipts
            ),
            merged_candidate_bytes=tuple(
                canonical_json_bytes(item) for item in merged
            ),
            private_conflict_bytes=tuple(
                canonical_json_bytes(item) for item in conflicts
            ),
            qualification_digest=claim["qualification_digest"],
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.QUALIFICATION_REJECTED,
            lambda: admission.admit_relation_set_for_private_closed_proof(forged),
        )

    def test_rae_005_conflicting_qualification_is_admitted_without_winner(self) -> None:
        state = admission.admit_relation_set_for_private_closed_proof(
            self.conflicting
        )
        relation_set = state.relation_set_document_copy()
        self.assertEqual(state.candidate_composition_status, "CONFLICTING")
        self.assertEqual(
            [item["relation_id"] for item in relation_set["relations"]],
            [
                item["relation_id"]
                for item in self.conflicting.merged_candidates_copy()
            ],
        )
        self.assertEqual(
            [item["conflict_id"] for item in relation_set["conflicts"]],
            [item["conflict_id"] for item in self.conflicting.private_conflicts_copy()],
        )
        self.assertNotIn("winner", canonical_json_bytes(relation_set).decode())
        for forbidden in ("slice", "coverage", "attention"):
            self.assertNotIn(forbidden, relation_set)

    def test_rae_009_same_semantics_has_distinct_attempt_witness(self) -> None:
        self.assertEqual(
            self.admitted.relation_set_digest, self.second_admitted.relation_set_digest
        )
        self.assertNotEqual(
            self.admitted.relation_set_document_bytes,
            self.second_admitted.relation_set_document_bytes,
        )
        self.assertNotEqual(
            self.admitted.admission_witness_bytes,
            self.second_admitted.admission_witness_bytes,
        )
        self.assertNotEqual(
            self.projected.document_bytes,
            admission.project_private_derivation_evidence_0_2(
                self.second_admitted
            ).document_bytes,
        )

    def test_rae_011_relation_set_has_no_self_admission_field(self) -> None:
        relation_set = self.admitted.relation_set_document_copy()
        self.assertNotIn("admission_status", relation_set)
        self.assertNotIn("admission_witness_digest", relation_set)

    def test_rae_012_projection_has_no_raw_witness_construction_entry(self) -> None:
        parameters = inspect.signature(
            admission.project_private_derivation_evidence_0_2
        ).parameters
        self.assertEqual(tuple(parameters), ("admitted",))
        fake = replace(self.admitted, _construction_token=object())
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(fake),
        )
        import veritrail_review

        self.assertFalse(
            hasattr(veritrail_review, "project_private_derivation_evidence_0_2")
        )

    def test_rae_013_witness_cannot_move_between_same_semantic_attempts(self) -> None:
        transplanted = replace(
            self.second_admitted,
            admission_witness_bytes=self.admitted.admission_witness_bytes,
            admission_witness_digest=self.admitted.admission_witness_digest,
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(transplanted),
        )

    def test_rae_014_changed_qualification_claim_is_rejected(self) -> None:
        witness = self.admitted.admission_witness_copy()
        outcomes = witness["qualification_claim"]["observation_receipts"][0][
            "accepted_observation_outcomes"
        ]
        outcomes[0]["outcome"] = "NEGATIVE"
        forged = replace(
            self.admitted,
            admission_witness_bytes=canonical_json_bytes(witness),
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(forged),
        )

    def test_rae_015_conflicting_membership_cannot_shrink_or_select_winner(self) -> None:
        state = admission.admit_relation_set_for_private_closed_proof(
            self.conflicting
        )
        relation_set = state.relation_set_document_copy()
        relation_set["relations"].pop()
        shrunk = replace(
            state,
            relation_set_document_bytes=canonical_json_bytes(relation_set),
            canonical_relation_set_artifact_bytes=canonical_json_bytes(relation_set) + b"\n",
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(shrunk),
        )
        relation_set = state.relation_set_document_copy()
        relation_set["winner_relation_id"] = relation_set["relations"][0]["relation_id"]
        winner = replace(
            state,
            relation_set_document_bytes=canonical_json_bytes(relation_set),
            canonical_relation_set_artifact_bytes=canonical_json_bytes(relation_set) + b"\n",
        )
        self.assertAdmissionFailure(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED,
            lambda: admission.project_private_derivation_evidence_0_2(winner),
        )

    def test_private_projection_is_owned_and_contains_no_identity_cycle(self) -> None:
        document = self.projected.document_copy()
        witness = document["relation_admission"]
        self.assertEqual(document["schema_version"], "0.2")
        self.assertEqual(document["overall_execution_status"], "COMPLETED")
        self.assertNotIn("derivation_evidence_digest", canonical_json_bytes(witness).decode())
        copied = self.projected.document_copy()
        copied["relation_admission"]["admission_claim"]["derivation_id"] = "forged"
        self.assertNotEqual(copied, self.projected.document_copy())

    def test_cross_runtime_golden_admission_identities(self) -> None:
        self.assertEqual(
            self.admitted.relation_set_digest,
            "9be261a89ffa32d328357590567cdc1050b9158979b81f2a24f2c3fe6c5c4749",
        )
        self.assertEqual(
            self.admitted.admission_witness_digest,
            "029865c7abb407a6c6eb147892ce686bcc1d085cdd6c4b9d4a430bec100b3bc3",
        )
        self.assertEqual(
            hashlib.sha256(
                self.admitted.canonical_relation_set_artifact_bytes
            ).hexdigest(),
            "8ee1ab118ac2add04e9ce8e55cb1f070df0ad3f8f6cec2a22a9c64a7f3a080d1",
        )


if __name__ == "__main__":
    unittest.main()
