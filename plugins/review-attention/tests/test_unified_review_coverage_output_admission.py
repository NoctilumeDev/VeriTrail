from __future__ import annotations

import copy
import json
import pickle
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from threading import Barrier
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_post_terminal_fact_dual_successor as post_terminal_support  # noqa: E402
from veritrail_review import _fact_relation_transition as transition  # noqa: E402
from veritrail_review import (  # noqa: E402
    _fact_to_coverage_exact_input_handoff as direct_handoff,
)
from veritrail_review import (  # noqa: E402
    _negative_world_coverage_authority_recovery as negative,
)
from veritrail_review import (  # noqa: E402
    _relation_observation_application as relation_application,
)
from veritrail_review import (  # noqa: E402
    _relation_transition_slice_composition as positive,
)
from veritrail_review import (  # noqa: E402
    _unified_review_coverage_output_admission as admission,
)
from veritrail_review.budget import OwnedPhaseResult  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402


class UnifiedReviewCoverageOutputAdmissionTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.support = post_terminal_support.PostTerminalFactDualSuccessorTests()
        self.support.setUp()

    def _normal(self, *, relation_runner=None):
        selector, _, _, context, _ = self.support._terminal()
        claim = selector.claim_relation()
        owner = admission.bind_unified_review_coverage_output_admission(claim)
        run = transition.run_claimed_fact_handoff_relation_transition
        admitted_transition = (
            run(claim) if relation_runner is None else relation_runner(run, claim)
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        return owner, result, claim, selector, context

    def _negative(self, index=0):
        _branch, inputs, kind = self.support._negative_worlds()[index]
        selector, _, _, context, _ = self.support._terminal(inputs, kind=kind)
        claim = selector.claim_exact_input()
        owner = admission.bind_unified_review_coverage_output_admission(claim)
        attempt = negative.claim_negative_world_coverage_attempt(claim)
        candidate = negative.produce_negative_world_coverage_candidate(attempt)
        validation = negative.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        result = negative.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )
        return owner, result, claim, attempt, validation, selector, context

    @staticmethod
    def _rewrite_normal_result(result, mutate):
        document = result.document_copy()
        mutate(document)
        unsigned = copy.deepcopy(document)
        unsigned.pop("composition_digest", None)
        document["composition_digest"] = semantic_digest(
            positive.COMPOSITION_FUNCTION, unsigned
        )
        encoded = canonical_json_bytes(document)
        old_phase = (
            result._OwnedReviewSliceCoverageComposition__committed_phase
        )
        phase = OwnedPhaseResult(
            canonical_bytes=encoded,
            completed_at_monotonic=old_phase.completed_at_monotonic,
        )
        result._OwnedReviewSliceCoverageComposition__bytes = encoded
        result._OwnedReviewSliceCoverageComposition__bound_bytes = encoded
        result._OwnedReviewSliceCoverageComposition__committed_phase = phase
        result._OwnedReviewSliceCoverageComposition__bound_committed_phase = phase

    @staticmethod
    def _failure(call, family):
        with unittest.TestCase().assertRaises(
            admission.UnifiedOutputAdmissionError
        ) as caught:
            call()
        unittest.TestCase().assertEqual(caught.exception.failure_family, family)

    def test_uao_000_normal_route_admits_exact_positive_result_once(self):
        owner, result, claim, _, _ = self._normal()
        admitted = owner.submit(result)
        self.assertEqual(
            owner.state, admission.UnifiedOutputAdmissionState.ADMITTED_NORMAL
        )
        self.assertEqual(admitted.terminal_branch, "NORMAL_FULFILLED")
        self.assertEqual(admitted.selector_route, admission.NORMAL_ROUTE)
        self.assertEqual(admitted.result_kind, admission.NORMAL_RESULT_KIND)
        self.assertIs(admitted.normal_result(), result)
        self.assertIs(
            claim._application_output_admission_coordinates()[0], claim
        )

    def test_uao_001_all_negative_routes_admit_exact_negative_result(self):
        for index, (branch, _inputs, _kind) in enumerate(
            self.support._negative_worlds()
        ):
            with self.subTest(branch=branch):
                owner, result, *_ = self._negative(index)
                admitted = owner.submit(result)
                self.assertEqual(
                    owner.state,
                    admission.UnifiedOutputAdmissionState.ADMITTED_NEGATIVE,
                )
                self.assertEqual(admitted.terminal_branch, branch)
                self.assertEqual(admitted.selector_route, admission.NEGATIVE_ROUTE)
                self.assertIs(admitted.negative_result(), result)

    def test_uao_002_normal_route_rejects_negative_nominal_result(self):
        owner, _, *_ = self._normal()
        _, negative_result, *_ = self._negative(1)
        self._failure(
            lambda: owner.submit(negative_result),
            admission.UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_TYPE_REJECTED,
        )
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_uao_003_negative_route_rejects_positive_nominal_result(self):
        owner, _, *_ = self._negative(0)
        _, positive_result, *_ = self._normal()
        self._failure(
            lambda: owner.submit(positive_result),
            admission.UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_TYPE_REJECTED,
        )

    def test_uao_004_subclass_proxy_and_uninitialized_exact_copy_reject(self):
        class ResultSubclass(positive.OwnedReviewSliceCoverageComposition):
            pass

        class ResultProxy:
            def _application_output_admission_coordinates(self):
                return ()

        for fake in (
            object.__new__(ResultSubclass),
            ResultProxy(),
            object.__new__(positive.OwnedReviewSliceCoverageComposition),
        ):
            with self.subTest(fake=type(fake).__name__):
                owner, _, *_ = self._normal()
                with self.assertRaises(admission.UnifiedOutputAdmissionError):
                    owner.submit(fake)
                self.assertEqual(
                    owner.state, admission.UnifiedOutputAdmissionState.REVOKED
                )

    def test_uao_005_foreign_selector_attempt_result_rejects(self):
        owner, _, *_ = self._normal()
        _, foreign_result, *_ = self._normal()
        self._failure(
            lambda: owner.submit(foreign_result),
            admission.UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED,
        )

    def test_uao_006_equal_terminal_bytes_cannot_replace_live_context(self):
        owner, result, claim, *_ = self._normal()
        _, _, _, _, foreign_context = self._normal()
        original_source = claim._ClaimedPostTerminalRelationSource__source_bytes
        claim._ClaimedPostTerminalRelationSource__context = foreign_context
        self.assertIs(
            claim._ClaimedPostTerminalRelationSource__source_bytes,
            original_source,
        )
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(result)
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_uao_007_claim_id_mismatch_rejects(self):
        owner, result, *_ = self._normal()

        def mutate(document):
            document["bridge_admission"]["request"][
                "handoff_claim_id"
            ] = "foreign-claim"

        self._rewrite_normal_result(result, mutate)
        self._failure(
            lambda: owner.submit(result),
            admission.UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED,
        )

    def test_uao_008_foreign_ledger_swap_fails_independent_reconciliation(self):
        owner, result, *_ = self._normal()
        _, foreign_result, *_ = self._normal()
        foreign_ledger = foreign_result.coverage_ledger_document_copy()

        def mutate(document):
            document["coverage_ledger"] = foreign_ledger
            document["slice_set_admission"]["coverage_ledger_digest"] = (
                foreign_ledger["coverage_ledger_digest"]
            )

        self._rewrite_normal_result(result, mutate)
        with mock.patch.object(
            positive, "validate_review_coverage_ledger", return_value=None
        ):
            self._failure(
                lambda: owner.submit(result),
                admission.UnifiedOutputAdmissionFailureFamily.
                UNIFIED_OUTPUT_LEDGER_RECONCILIATION_REJECTED,
            )

    def test_uao_009_bridge_source_identity_swap_rejects(self):
        owner, result, *_ = self._normal()

        def mutate(document):
            document["bridge_admission"]["request"][
                "fact_consumer_attempt_id"
            ] = "foreign-attempt"

        self._rewrite_normal_result(result, mutate)
        self._failure(
            lambda: owner.submit(result),
            admission.UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED,
        )

    def test_uao_010_negative_attempt_validation_candidate_swap_rejects(self):
        owner, result, *_ = self._negative(1)
        _, foreign, *_ = self._negative(1)
        result._AdmittedNegativeWorldCoverage__attempt = (
            foreign._AdmittedNegativeWorldCoverage__attempt
        )
        result._AdmittedNegativeWorldCoverage__validation = (
            foreign._AdmittedNegativeWorldCoverage__validation
        )
        result._AdmittedNegativeWorldCoverage__phase = (
            foreign._AdmittedNegativeWorldCoverage__phase
        )
        result._AdmittedNegativeWorldCoverage__candidate_bytes = (
            foreign._AdmittedNegativeWorldCoverage__candidate_bytes
        )
        result._AdmittedNegativeWorldCoverage__bound_candidate_bytes = (
            foreign._AdmittedNegativeWorldCoverage__bound_candidate_bytes
        )
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(result)

    def test_uao_011_normal_relation_conflict_is_not_negative(self):
        original = (
            transition._source_operation_cell.
            run_prepared_relation_observation_source_operation_attempt
        )

        def conflicting(prepared):
            phase = original(prepared)
            if not prepared.binding.descriptor.provider_id.endswith("provider-b"):
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
            alternative = relation_application.canonicalize_relation_observation_candidates(
                request, [candidate]
            )[0]
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

        def runner(run, claim):
            with mock.patch.object(
                transition._source_operation_cell,
                "run_prepared_relation_observation_source_operation_attempt",
                side_effect=conflicting,
            ):
                return run(claim)

        owner, result, *_ = self._normal(relation_runner=runner)
        self.assertIsNone(result.document_copy()["review_slice_set"])
        admitted = owner.submit(result)
        self.assertEqual(admitted.result_kind, admission.NORMAL_RESULT_KIND)

    def test_uao_012_successful_result_replay_revokes_attempt(self):
        owner, result, *_ = self._normal()
        admitted = owner.submit(result)
        self._failure(
            lambda: owner.submit(result),
            admission.UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_ALREADY_ADMITTED,
        )
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            _ = admitted.result_kind

    def test_uao_013_failure_cannot_fallback_to_later_result(self):
        owner, result, *_ = self._normal()
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(object())
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(result)
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_uao_014_concurrent_submit_has_at_most_one_admission(self):
        owner, result, *_ = self._normal()
        barrier = Barrier(2)

        def submit():
            barrier.wait()
            try:
                return owner.submit(result)
            except admission.UnifiedOutputAdmissionError as exc:
                return exc.failure_family

        with ThreadPoolExecutor(max_workers=2) as executor:
            values = list(executor.map(lambda _value: submit(), range(2)))
        successes = [
            value
            for value in values
            if type(value) is admission.AdmittedUnifiedReviewCoverageOutput
        ]
        self.assertLessEqual(len(successes), 1)
        self.assertEqual(len(values) - len(successes), 1)
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_uao_015_late_context_stop_prevents_admission(self):
        owner, result, _, _, context = self._normal()
        self.assertTrue(context.request_cancellation())
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(result)
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_uao_016_result_mutation_after_binding_revokes(self):
        owner, result, *_ = self._normal()
        result._OwnedReviewSliceCoverageComposition__bytes = b"{}"
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(result)
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_uao_017_copy_pickle_json_and_public_export_reject(self):
        import veritrail_review

        owner, result, *_ = self._normal()
        admitted = owner.submit(result)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            copy.copy(admitted)
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

        owner, result, *_ = self._normal()
        admitted = owner.submit(result)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            pickle.dumps(admitted)

        owner, result, *_ = self._normal()
        admitted = owner.submit(result)
        with self.assertRaises(TypeError):
            json.dumps(admitted)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            admitted.to_json()
        self.assertNotIn(
            "bind_unified_review_coverage_output_admission", dir(veritrail_review)
        )

    def test_uao_018_authority_ceiling_expansion_rejects(self):
        owner, result, *_ = self._normal()

        def mutate(document):
            document["authority_ceiling"]["manifest"] = True

        self._rewrite_normal_result(result, mutate)
        self._failure(
            lambda: owner.submit(result),
            admission.UnifiedOutputAdmissionFailureFamily.
            UNIFIED_OUTPUT_AUTHORITY_CEILING_REJECTED,
        )

    def test_uao_019_equal_semantic_result_from_foreign_attempt_has_no_authority(self):
        owner, result, *_ = self._negative(0)
        _, foreign, *_ = self._negative(0)
        local_ledger = result.coverage_ledger_document_copy()
        foreign_ledger = foreign.coverage_ledger_document_copy()
        self.assertEqual(
            (
                local_ledger["artifact_kind"],
                local_ledger["schema_version"],
                local_ledger["overall_coverage_status"],
                [item["coverage_status"] for item in local_ledger["stages"]],
            ),
            (
                foreign_ledger["artifact_kind"],
                foreign_ledger["schema_version"],
                foreign_ledger["overall_coverage_status"],
                [item["coverage_status"] for item in foreign_ledger["stages"]],
            ),
        )
        self.assertNotEqual(
            local_ledger["coverage_ledger_digest"],
            foreign_ledger["coverage_ledger_digest"],
        )
        self.assertIs(admission.QUALIFICATION_INHERITANCE_ALLOWED, False)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(foreign)

    def test_uao_020_formal_pass_does_not_claim_problem_solution(self):
        import veritrail_review

        self.assertIs(admission.PROOF_IS_NOT_PROBLEM_SOLVING, True)
        self.assertNotIn(
            "AdmittedUnifiedReviewCoverageOutput", dir(veritrail_review)
        )
        owner, result, *_ = self._normal()
        admitted = owner.submit(result)
        ceiling = admitted.authority_ceiling_copy()
        self.assertFalse(ceiling["manifest"])
        self.assertFalse(ceiling["derivation_evidence"])
        self.assertFalse(ceiling["persistence"])
        self.assertFalse(ceiling["public_review"])
        self.assertFalse(ceiling["core_verdict"])
        self.assertFalse(ceiling["r2_r6"])

    def test_route_claim_can_bind_only_one_application_owner(self):
        selector, _, _, _, _ = self.support._terminal()
        claim = selector.claim_relation()
        first = admission.bind_unified_review_coverage_output_admission(claim)
        self.assertEqual(
            first.state,
            admission.UnifiedOutputAdmissionState.ROUTE_BOUND_NOT_ADMITTED,
        )
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            admission.bind_unified_review_coverage_output_admission(claim)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            first.submit(object())
        self.assertEqual(first.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_wrong_variant_accessor_revokes_existing_admission(self):
        owner, result, *_ = self._normal()
        admitted = owner.submit(result)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            admitted.negative_result()
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_application_owner_cannot_bind_after_downstream_consumption(self):
        selector, _, _, _, _ = self.support._terminal()
        claim = selector.claim_relation()
        transition.run_claimed_fact_handoff_relation_transition(claim)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            admission.bind_unified_review_coverage_output_admission(claim)

        _branch, inputs, kind = self.support._negative_worlds()[0]
        selector, _, _, _, _ = self.support._terminal(inputs, kind=kind)
        claim = selector.claim_exact_input()
        negative.claim_negative_world_coverage_attempt(claim)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            admission.bind_unified_review_coverage_output_admission(claim)

    def test_legacy_direct_carrier_cannot_impersonate_selector_signed_route(self):
        helper = (
            post_terminal_support.carrier_support.
            FactToCoverageExactInputHandoffTests()
        )
        helper.setUp()
        _parent, closure, *_ = helper._closure()
        carrier = direct_handoff.claim_fact_to_coverage_exact_input_handoff(
            closure
        )
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            admission.bind_unified_review_coverage_output_admission(carrier)

    def test_admitted_read_revalidates_result_mutation(self):
        owner, result, *_ = self._normal()
        admitted = owner.submit(result)
        result._OwnedReviewSliceCoverageComposition__bytes = b"{}"
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            _ = admitted.result_kind
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)

    def test_copying_bound_owner_revokes_route_authority(self):
        owner, result, *_ = self._normal()
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            copy.copy(owner)
        self.assertEqual(owner.state, admission.UnifiedOutputAdmissionState.REVOKED)
        with self.assertRaises(admission.UnifiedOutputAdmissionError):
            owner.submit(result)


if __name__ == "__main__":
    unittest.main()
