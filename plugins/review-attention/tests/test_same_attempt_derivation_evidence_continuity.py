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

import test_post_terminal_fact_dual_successor as post_terminal_support  # noqa: E402
from veritrail_review import _fact_relation_transition as transition  # noqa: E402
from veritrail_review import (  # noqa: E402
    _negative_world_coverage_authority_recovery as negative,
)
from veritrail_review import _relation_set_admission as legacy  # noqa: E402
from veritrail_review import (  # noqa: E402
    _relation_observation_application as relation_application,
)
from veritrail_review import (  # noqa: E402
    _relation_transition_slice_composition as positive,
)
from veritrail_review import (  # noqa: E402
    _same_attempt_derivation_evidence_continuity as continuity,
)
from veritrail_review import (  # noqa: E402
    _unified_review_coverage_output_admission as unified,
)
from veritrail_review.canonical import canonical_json_bytes  # noqa: E402


class SameAttemptDerivationEvidenceContinuityTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.support = post_terminal_support.PostTerminalFactDualSuccessorTests()
        self.support.setUp()

    def _normal(self):
        selector, closure, inputs, context, eligibility = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        admitted_transition = transition.run_claimed_fact_handoff_relation_transition(
            claim
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        admitted = owner.submit(result)
        value = admitted._same_attempt_derivation_evidence_continuity()
        return (
            value,
            admitted,
            owner,
            result,
            admitted_transition,
            claim,
            selector,
            closure,
            inputs,
            context,
            eligibility,
        )

    def _negative(self, index: int):
        expected, inputs, kind = self.support._negative_worlds()[index]
        selector, closure, exact_inputs, context, eligibility = self.support._terminal(
            inputs, kind=kind
        )
        claim = selector.claim_exact_input()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        attempt = negative.claim_negative_world_coverage_attempt(claim)
        candidate = negative.produce_negative_world_coverage_candidate(attempt)
        validation = negative.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        result = negative.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )
        admitted = owner.submit(result)
        value = admitted._same_attempt_derivation_evidence_continuity()
        return (
            expected,
            value,
            admitted,
            owner,
            result,
            claim,
            selector,
            closure,
            exact_inputs,
            context,
            eligibility,
        )

    def _negative_uncommitted(self, index: int):
        expected, inputs, kind = self.support._negative_worlds()[index]
        selector, closure, exact_inputs, context, eligibility = self.support._terminal(
            inputs, kind=kind
        )
        claim = selector.claim_exact_input()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        attempt = negative.claim_negative_world_coverage_attempt(claim)
        candidate = negative.produce_negative_world_coverage_candidate(attempt)
        validation = negative.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        result = negative.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )
        return (
            expected,
            selector,
            claim,
            owner,
            result,
            closure,
            exact_inputs,
            context,
            eligibility,
        )

    @staticmethod
    def _failure(call, family):
        with unittest.TestCase().assertRaises(
            continuity.SameAttemptDerivationEvidenceContinuityError
        ) as caught:
            call()
        unittest.TestCase().assertEqual(caught.exception.failure_family, family)

    def test_dec_000_normal_world_commits_exact_private_continuity(self):
        value, admitted, _, result, transition_value, claim, *_ = self._normal()
        document = value._document_copy()
        self.assertEqual(value.continuity_variant, continuity.NORMAL_VARIANT)
        self.assertEqual(value.terminal_branch, "NORMAL_FULFILLED")
        self.assertEqual(value.selector_route, continuity.NORMAL_ROUTE)
        self.assertIs(value.normal_result(), result)
        self.assertIs(admitted.normal_result(), result)
        self.assertEqual(
            document["selector_claim_id"], claim.document_copy()["claim_id"]
        )
        self.assertEqual(
            document["transition_admission_sha256"],
            hashlib.sha256(
                canonical_json_bytes(transition_value.document_copy())
            ).hexdigest(),
        )
        fact = document["fact_controller_capture"]
        relation = document["relation_controller_capture"]
        self.assertLessEqual(fact["attempt_started_at"], fact["phase_finished_at"])
        self.assertLessEqual(fact["phase_finished_at"], relation["phase_finished_at"])
        self.assertEqual(document["reconciliation"]["status"], "RECONCILED")

    def test_dec_001_all_four_negative_worlds_commit_without_placeholders(self):
        branches = []
        for index in range(4):
            with self.subTest(index=index):
                expected, value, admitted, _, result, claim, *_ = self._negative(index)
                document = value._document_copy()
                branches.append(value.terminal_branch)
                self.assertEqual(value.terminal_branch, expected)
                self.assertEqual(value.continuity_variant, continuity.NEGATIVE_VARIANT)
                self.assertIs(value.negative_result(), result)
                self.assertIs(admitted.negative_result(), result)
                self.assertIsNone(document["relation_controller_capture"])
                self.assertIsNone(document["transition_admission_sha256"])
                source = claim.fact_terminal_source_copy()
                self.assertIsNone(source["fact_set"])
                self.assertFalse(result.authority_ceiling_copy()["relation_set"])
                self.assertFalse(result.authority_ceiling_copy()["review_slice_set"])
        self.assertEqual(
            branches,
            [
                "ZERO_PARSE_DENOMINATOR",
                "ALL_PARSE_REJECTED",
                "PROJECTION_BLOCKED",
                "REQUIRED_PROVIDER_NON_SUCCESS",
            ],
        )

    def test_dec_002_003_016_017_foreign_equal_shape_cannot_cross_attempts(self):
        selector_a, *_ = self.support._terminal()
        claim_a = selector_a.claim_relation()
        owner_a = unified.bind_unified_review_coverage_output_admission(claim_a)
        selector_b, *_ = self.support._terminal()
        claim_b = selector_b.claim_relation()
        unified.bind_unified_review_coverage_output_admission(claim_b)
        transition_b = transition.run_claimed_fact_handoff_relation_transition(claim_b)
        bridge_b = positive.admit_relation_transition_for_slice_composition(
            transition_b.claim_continuation()
        )
        result_b = positive.compose_review_slice_set_and_coverage(
            bridge_b.claim_continuation()
        )
        with self.assertRaises(unified.UnifiedOutputAdmissionError):
            owner_a.submit(result_b)

    def test_dec_004_006_controller_timing_is_owned_and_missing_capture_revokes(self):
        selector, *_ = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        admitted_transition = transition.run_claimed_fact_handoff_relation_transition(
            claim
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        runs = slot._SameAttemptContinuityCaptureSlot__fact_runs
        first = next(iter(runs.values()))
        first["finished_at"] = None
        self._failure(
            lambda: owner.submit(result),
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING,
        )
        self.assertEqual(slot.state, continuity.EvidenceContinuityState.REVOKED)

    def test_dec_004_provider_reported_controller_timing_is_rejected(self):
        original_execute = self.support.fact_helper._execute

        def provider_claims_controller_time(terminal, _request):
            terminal["controller_timing"] = {
                "attempt_started_at": "1900-01-01T00:00:00Z",
                "phase_finished_at": "2999-01-01T00:00:00Z",
            }

        with mock.patch.object(
            self.support.fact_helper,
            "_execute",
            side_effect=lambda parent, **kwargs: original_execute(
                parent,
                kind=kwargs.get("kind", "COMPLETED"),
                transform=provider_claims_controller_time,
            ),
        ):
            selector, _, _, _, _ = self.support._terminal()
        claim = selector.claim_exact_input()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        attempt = negative.claim_negative_world_coverage_attempt(claim)
        candidate = negative.produce_negative_world_coverage_candidate(attempt)
        validation = negative.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        result = negative.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )
        admitted = owner.submit(result)
        value = admitted._same_attempt_derivation_evidence_continuity()
        document = value._document_copy()

        self.assertEqual(value.terminal_branch, "REQUIRED_PROVIDER_NON_SUCCESS")
        self.assertEqual(value.continuity_variant, continuity.NEGATIVE_VARIANT)
        self.assertTrue(
            all(
                item["lifecycle"] == "FAILED"
                for item in document["fact_controller_capture"]["provider_runs"]
            )
        )
        self.assertNotEqual(
            document["fact_controller_capture"]["attempt_started_at"],
            "1900-01-01T00:00:00.000000Z",
        )
        self.assertNotEqual(
            document["fact_controller_capture"]["phase_finished_at"],
            "2999-01-01T00:00:00.000000Z",
        )

    def test_dec_005_007_008_009_late_or_missing_transition_never_recovers(self):
        selector, *_ = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        original_capture = claim._capture_same_attempt_continuity_transition
        with mock.patch.object(
            claim, "_capture_same_attempt_continuity_transition", return_value=None
        ):
            admitted_transition = (
                transition.run_claimed_fact_handoff_relation_transition(claim)
            )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        self._failure(
            lambda: original_capture(admitted_transition),
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED,
        )
        with self.assertRaises((
            continuity.SameAttemptDerivationEvidenceContinuityError,
            unified.UnifiedOutputAdmissionError,
        )):
            owner.submit(result)

    def test_dec_009_missing_relation_provider_run_revokes(self):
        selector, *_ = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        admitted_transition = transition.run_claimed_fact_handoff_relation_transition(
            claim
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        transition_capture = slot._SameAttemptContinuityCaptureSlot__transition
        capture = json.loads(transition_capture["capture_bytes"])
        capture["provider_runs"].pop()
        transition_capture["capture_bytes"] = canonical_json_bytes(capture)

        self._failure(
            lambda: owner.submit(result),
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED,
        )
        self.assertEqual(slot.state, continuity.EvidenceContinuityState.REVOKED)

    def test_dec_010_011_012_negative_not_started_and_started_are_disjoint(self):
        _, zero, *_ = self._negative(0)
        zero_runs = zero._document_copy()["fact_controller_capture"]["provider_runs"]
        self.assertEqual(zero_runs, [])

        _, failed, *_ = self._negative(3)
        failed_runs = failed._document_copy()["fact_controller_capture"][
            "provider_runs"
        ]
        self.assertTrue(failed_runs)
        self.assertTrue(
            all(
                item[name] is not None
                for item in failed_runs
                for name in ("started_at", "finished_at", "phase_finished_at")
            )
        )

    def test_dec_010_fabricated_not_started_timing_rejects(self):
        _, selector, _, owner, result, *_ = self._negative_uncommitted(0)
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        attempt_started_at = (
            slot._SameAttemptContinuityCaptureSlot__attempt_started_at
        )
        slot._SameAttemptContinuityCaptureSlot__fact_runs[object()] = {
            "claim": object(),
            "started_at": attempt_started_at,
            "finished_at": attempt_started_at,
            "phase_finished_at": attempt_started_at,
            "lifecycle": "NOT_STARTED",
        }
        self._failure(
            lambda: owner.submit(result),
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING,
        )

    def test_dec_011_started_negative_provider_requires_controller_finish(self):
        _, selector, _, owner, result, *_ = self._negative_uncommitted(3)
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        run = next(iter(slot._SameAttemptContinuityCaptureSlot__fact_runs.values()))
        run["finished_at"] = None
        self._failure(
            lambda: owner.submit(result),
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING,
        )

    def test_dec_012_negative_placeholder_injection_rejects(self):
        _, inputs, kind = self.support._negative_worlds()[0]
        selector, *_ = self.support._terminal(inputs, kind=kind)
        claim = selector.claim_exact_input()
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        source = json.loads(
            slot._SameAttemptContinuityCaptureSlot__terminal_source_bytes
        )
        source["fact_set"] = {"fabricated": True}
        slot._SameAttemptContinuityCaptureSlot__terminal_source_bytes = (
            canonical_json_bytes(source)
        )
        with self.assertRaises(unified.UnifiedOutputAdmissionError) as caught:
            unified.bind_unified_review_coverage_output_admission(claim)
        self.assertEqual(
            caught.exception.failure_family,
            unified.UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED,
        )
        self.assertEqual(
            slot.state,
            continuity.EvidenceContinuityState.REVOKED,
        )

    def test_dec_013_relation_conflict_stays_normal_qualified_unknown(self):
        selector, _, _, _, _ = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        original = (
            transition._source_operation_cell.
            run_prepared_relation_observation_source_operation_attempt
        )

        def conflicting(prepared):
            phase = original(prepared)
            if not prepared.binding.descriptor.provider_id.endswith("provider-b"):
                return phase
            request = relation_application._synthetic_request(
                prepared.request_document,
                phase.provider_run_id,
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
            self.assertEqual(
                alternative["relation_subject_digest"],
                first["relation_subject_digest"],
            )
            self.assertNotEqual(alternative["relation_id"], first["relation_id"])
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

        with mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            side_effect=conflicting,
        ):
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
        value = admitted._same_attempt_derivation_evidence_continuity()
        result_document = result.document_copy()
        continuity_document = value._document_copy()

        self.assertEqual(value.continuity_variant, continuity.NORMAL_VARIANT)
        self.assertEqual(value.terminal_branch, "NORMAL_FULFILLED")
        self.assertEqual(value.selector_route, continuity.NORMAL_ROUTE)
        self.assertIs(value.normal_result(), result)
        self.assertIsNone(result_document["review_slice_set"])
        self.assertEqual(
            result_document["slice_set_admission"]["terminal_branch"],
            "PREDECESSOR_UNKNOWN",
        )
        self.assertEqual(
            result_document["coverage_ledger"]["overall_coverage_status"],
            "UNKNOWN",
        )
        self.assertEqual(
            continuity_document["reconciliation"]["continuity_variant"],
            continuity.NORMAL_VARIANT,
        )

    def test_dec_014_015_wrong_variant_and_unknown_branch_revoke(self):
        _, value, *_ = self._negative(0)
        self._failure(
            value.normal_result,
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED,
        )
        self._failure(
            lambda: continuity._route_for_branch("UNKNOWN_BRANCH"),
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED,
        )

    def test_dec_014_wrong_route_result_submission_revokes(self):
        selector, *_ = self.support._terminal()
        claim = selector.claim_relation()
        normal_owner = unified.bind_unified_review_coverage_output_admission(claim)
        _, _, _, _, negative_result, *_ = (
            self._negative_uncommitted(0)
        )
        with self.assertRaises(unified.UnifiedOutputAdmissionError):
            normal_owner.submit(negative_result)
        normal_slot = (
            selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        )
        self.assertEqual(
            normal_slot.state,
            continuity.EvidenceContinuityState.REVOKED,
        )

        normal_selector, *_ = self.support._terminal()
        normal_claim = normal_selector.claim_relation()
        unified.bind_unified_review_coverage_output_admission(normal_claim)
        admitted_transition = (
            transition.run_claimed_fact_handoff_relation_transition(normal_claim)
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        normal_result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        _, _, _, negative_owner, _, *_ = self._negative_uncommitted(0)
        with self.assertRaises(unified.UnifiedOutputAdmissionError):
            negative_owner.submit(normal_result)

    def test_dec_015_unknown_bound_branch_revokes_instead_of_catch_all(self):
        selector, *_ = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        admitted_transition = transition.run_claimed_fact_handoff_relation_transition(
            claim
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        slot._SameAttemptContinuityCaptureSlot__branch = "UNKNOWN_BRANCH"
        with self.assertRaises(
            continuity.SameAttemptDerivationEvidenceContinuityError
        ):
            owner.submit(result)
        self.assertEqual(slot.state, continuity.EvidenceContinuityState.REVOKED)

    def test_dec_018_019_legacy_projector_cannot_alias_qualified_negative(self):
        _, value, admitted, *_ = self._negative(1)
        with self.assertRaises(Exception):
            legacy.project_private_derivation_evidence_0_2(value)
        self.assertEqual(admitted.result_kind, "NEGATIVE_WORLD_COVERAGE")
        self.assertEqual(value.continuity_variant, continuity.NEGATIVE_VARIANT)

    def test_dec_019_negative_semantic_rewrite_revokes(self):
        _, value, _, _, result, *_ = self._negative(1)
        rewritten = result.coverage_ledger_document_copy()
        rewritten["overall_coverage_status"] = "FAILED"
        rewritten_bytes = canonical_json_bytes(rewritten)
        result._AdmittedNegativeWorldCoverage__candidate_bytes = rewritten_bytes
        result._AdmittedNegativeWorldCoverage__bound_candidate_bytes = (
            rewritten_bytes
        )
        with self.assertRaises(
            continuity.SameAttemptDerivationEvidenceContinuityError
        ):
            value.negative_result()

    def test_dec_020_027_authority_ceiling_remains_private_and_narrow(self):
        value, *_ = self._normal()
        ceiling = value.authority_ceiling_copy()
        self.assertTrue(ceiling["private_same_attempt_continuity"])
        for key in (
            "legacy_evidence_0_2",
            "public_evidence_schema",
            "manifest",
            "persistence",
            "public_review",
            "core_verdict",
            "global_composition_authority",
            "r2_r6",
        ):
            self.assertFalse(ceiling[key])
        import veritrail_review

        self.assertNotIn(
            "CommittedSameAttemptDerivationEvidenceContinuity",
            dir(veritrail_review),
        )

    def test_dec_021_022_context_stop_or_cleanup_failure_has_no_commit(self):
        selector, _, _, context, _ = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        admitted_transition = transition.run_claimed_fact_handoff_relation_transition(
            claim
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        context.request_cancellation()
        with self.assertRaises(unified.UnifiedOutputAdmissionError):
            owner.submit(result)

        cleanup_selector, cleanup_closure, *_ = self.support._terminal()
        values = self.support._terminal_values(
            cleanup_selector,
            cleanup_closure,
        )
        forged = copy.deepcopy(values[0])
        forged["provider_history"][0]["lifecycle"] = "RELEASE_FAILED"
        consumer = (
            cleanup_selector._OwnedPostTerminalFactDualSuccessor__consumer
        )
        with mock.patch.object(
            consumer,
            "_post_terminal_dual_successor_terminal_source",
            return_value=(forged, *values[1:]),
        ):
            with self.assertRaises(Exception):
                cleanup_selector.claim_relation()
        cleanup_slot = (
            cleanup_selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        )
        self.assertNotEqual(
            cleanup_slot.state,
            continuity.EvidenceContinuityState.COMMITTED,
        )

    def test_dec_023_bound_value_mutation_revokes_permanently(self):
        value, *_ = self._normal()
        value._CommittedSameAttemptDerivationEvidenceContinuity__encoded = b"{}"
        self._failure(
            lambda: value.continuity_variant,
            continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED,
        )

    def test_dec_023_fact_capture_mutation_revokes_permanently(self):
        value, _, _, _, _, _, selector, *_ = self._normal()
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        run = next(iter(slot._SameAttemptContinuityCaptureSlot__fact_runs.values()))
        run["lifecycle"] = "FABRICATED"
        with self.assertRaises(
            continuity.SameAttemptDerivationEvidenceContinuityError
        ):
            value.terminal_branch
        self.assertEqual(slot.state, continuity.EvidenceContinuityState.REVOKED)

    def test_dec_023_input_mutation_revokes_permanently(self):
        value, _, _, _, _, _, selector, _, inputs, *_ = self._normal()
        object.__setattr__(inputs, "policy_digest", "0" * 64)
        with self.assertRaises(
            continuity.SameAttemptDerivationEvidenceContinuityError
        ):
            value.terminal_branch
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        self.assertEqual(slot.state, continuity.EvidenceContinuityState.REVOKED)

    def test_dec_023_result_mutation_revokes_permanently(self):
        value, _, _, result, _, _, selector, *_ = self._normal()
        result._OwnedReviewSliceCoverageComposition__bytes = b"{}"
        with self.assertRaises(
            continuity.SameAttemptDerivationEvidenceContinuityError
        ):
            value.terminal_branch
        slot = selector._OwnedPostTerminalFactDualSuccessor__continuity_capture_slot
        self.assertEqual(slot.state, continuity.EvidenceContinuityState.REVOKED)

    def test_dec_024_025_replay_and_concurrent_second_submit_are_rejected(self):
        selector, *_ = self.support._terminal()
        claim = selector.claim_relation()
        owner = unified.bind_unified_review_coverage_output_admission(claim)
        admitted_transition = transition.run_claimed_fact_handoff_relation_transition(
            claim
        )
        bridge = positive.admit_relation_transition_for_slice_composition(
            admitted_transition.claim_continuation()
        )
        result = positive.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )

        def submit():
            try:
                return owner.submit(result)
            except Exception as exc:
                return exc

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: submit(), range(2)))
        self.assertEqual(
            sum(isinstance(value, unified.AdmittedUnifiedReviewCoverageOutput) for value in outcomes),
            1,
        )
        self.assertEqual(sum(isinstance(value, Exception) for value in outcomes), 1)

    def test_dec_026_copy_pickle_and_json_cannot_restore_private_value(self):
        _, value, *_ = self._negative(2)
        for operation in (
            lambda: copy.copy(value),
            lambda: pickle.dumps(value),
            value.to_json,
        ):
            with self.subTest(operation=operation):
                with self.assertRaises(
                    continuity.SameAttemptDerivationEvidenceContinuityError
                ):
                    operation()

    def test_dec_028_029_qualification_does_not_inherit_or_claim_global_solution(self):
        self.assertIs(continuity.PROOF_IS_NOT_PROBLEM_SOLVING, True)
        self.assertIs(continuity.QUALIFICATION_INHERITANCE_ALLOWED, False)
        self.assertIs(continuity.LOCAL_NOT_GLOBAL, True)
        self.assertIs(continuity.POST_R1_GLOBAL_CHECK_REQUIRED, True)
        self.assertEqual(
            continuity.CONTRACT_FUNCTION,
            "r1-same-attempt-derivation-evidence-continuity/0.1",
        )


if __name__ == "__main__":
    unittest.main()
