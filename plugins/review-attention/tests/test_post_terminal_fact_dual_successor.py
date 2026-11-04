from __future__ import annotations

import copy
import json
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_fact_fulfillment as fact_support  # noqa: E402
import test_fact_relation_transition as relation_support  # noqa: E402
import test_fact_to_coverage_exact_input_handoff as carrier_support  # noqa: E402
import test_parse_product_fact_consumer as parse_support  # noqa: E402
from veritrail_review import _fact_relation_transition as relation  # noqa: E402
from veritrail_review import _fact_fulfillment as fact_consumer  # noqa: E402
from veritrail_review import (  # noqa: E402
    _negative_world_coverage_authority_recovery as negative_coverage,
)
from veritrail_review import (  # noqa: E402
    _post_terminal_fact_dual_successor as dual,
)
from veritrail_review._fact_fulfillment_binding import (  # noqa: E402
    closed_fact_bindings,
)
from veritrail_review.budget import BudgetState  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes  # noqa: E402


class PostTerminalFactDualSuccessorTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.relation_helper = relation_support.FactRelationTransitionTests()
        self.fact_helper = fact_support.FactFulfillmentTests()

    def _selector(self, inputs=None, *, kind="COMPLETED"):
        inputs = self.relation_helper._inputs() if inputs is None else inputs
        with mock.patch.object(
            parse_support.ParseHelper,
            "_accepted_terminal_for_source",
            side_effect=fact_support.fixture_terminal,
        ):
            _, parse_closure, context, eligibility = (
                parse_support.ProductFactConsumerTests()._parse_world(inputs)
            )
        selector = dual.create_post_terminal_fact_dual_successor_consumer(
            parse_closure,
            derivation_id="post-terminal-dual-successor-test",
            bindings=closed_fact_bindings(),
        )
        observations = (
            self.fact_helper._execute(selector, kind=kind)
            if selector.claims()
            else ()
        )
        return selector, observations, inputs, context, eligibility

    def _terminal(self, inputs=None, *, kind="COMPLETED"):
        selector, observations, inputs, context, eligibility = self._selector(
            inputs, kind=kind
        )
        closure = selector.reconcile(observations)
        return selector, closure, inputs, context, eligibility

    def _negative_worlds(self):
        empty = carrier_support.FactToCoverageExactInputHandoffTests._empty_inputs()
        empty = self.relation_helper._with_policy(
            empty,
            lambda policy: policy["provider_requirements"].append(
                {
                    "capability_id": "review-relation-derivation",
                    "required": True,
                    "composition_mode": "CUMULATIVE",
                }
            ),
        )
        return (
            (
                "ZERO_PARSE_DENOMINATOR",
                empty,
                "COMPLETED",
            ),
            (
                "ALL_PARSE_REJECTED",
                self.relation_helper._inputs(bodies=[(b"a.py", b"def bad(:\n")]),
                "COMPLETED",
            ),
            (
                "PROJECTION_BLOCKED",
                self.relation_helper._inputs(
                    bodies=[
                        (
                            b"a.py",
                            "class ｉｆ:\n    pass\ndef later():\n    pass\n".encode(),
                        )
                    ]
                ),
                "COMPLETED",
            ),
            (
                "REQUIRED_PROVIDER_NON_SUCCESS",
                self.relation_helper._inputs(),
                "PROVIDER_FAILED",
            ),
        )

    @staticmethod
    def _terminal_values(selector, closure):
        consumer = selector._OwnedPostTerminalFactDualSuccessor__consumer
        slot = selector._OwnedPostTerminalFactDualSuccessor__slot
        return consumer._post_terminal_dual_successor_terminal_source(closure, slot)

    def test_ptds_000_complete_normal_world_has_one_relation_claim(self):
        selector, _, _, _, _ = self._terminal()
        relation_claim = selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.CLAIMED_RELATION)
        self.assertEqual(
            relation_claim.document_copy()["terminal_branch"],
            "NORMAL_FULFILLED",
        )

    def test_ptds_001_all_four_negative_worlds_have_one_exact_input_claim(self):
        for expected, inputs, kind in self._negative_worlds():
            with self.subTest(branch=expected):
                selector, _, _, _, _ = self._terminal(inputs, kind=kind)
                carrier = selector.claim_exact_input()
                identity = carrier.input_identity_copy()
                self.assertEqual(
                    carrier.fact_terminal_source_copy()["branch"], expected
                )
                self.assertEqual(
                    identity["handoff_function"],
                    "r1-fact-to-coverage-exact-input-handoff-successor/0.2",
                )
                self.assertEqual(
                    identity["carrier_identity"],
                    "r1-terminal-validated-original-derivation-input-carrier/0.1",
                )
                self.assertEqual(
                    selector.state, dual.DualSuccessorState.CLAIMED_EXACT_INPUT
                )

    def test_ptds_002_preterminal_claims_reject_and_revoke(self):
        for method_name in ("claim_relation", "claim_exact_input"):
            with self.subTest(route=method_name):
                selector, _, _, _, _ = self._selector()
                self.assertEqual(
                    selector.state, dual.DualSuccessorState.SEALED_NOT_ROUTABLE
                )
                with self.assertRaises(dual.PostTerminalDualSuccessorError) as caught:
                    getattr(selector, method_name)()
                self.assertEqual(
                    caught.exception.failure_family,
                    dual.DualSuccessorFailureFamily.PRE_TERMINAL_CLAIM_REJECTED,
                )
                self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_003_normal_wrong_route_forbids_fallback(self):
        selector, _, _, _, _ = self._terminal()
        with self.assertRaises(dual.PostTerminalDualSuccessorError) as caught:
            selector.claim_exact_input()
        self.assertEqual(
            caught.exception.failure_family,
            dual.DualSuccessorFailureFamily.WRONG_ROUTE_REJECTED,
        )
        with self.assertRaises(dual.PostTerminalDualSuccessorError):
            selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_004_negative_wrong_route_forbids_fallback(self):
        _, inputs, kind = self._negative_worlds()[0]
        selector, _, _, _, _ = self._terminal(inputs, kind=kind)
        with self.assertRaises(dual.PostTerminalDualSuccessorError) as caught:
            selector.claim_relation()
        self.assertEqual(
            caught.exception.failure_family,
            dual.DualSuccessorFailureFamily.WRONG_ROUTE_REJECTED,
        )
        with self.assertRaises(dual.PostTerminalDualSuccessorError):
            selector.claim_exact_input()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_005_correct_claim_then_other_route_revokes_slot(self):
        selector, _, _, _, _ = self._terminal()
        selector.claim_relation()
        with self.assertRaises(dual.PostTerminalDualSuccessorError) as caught:
            selector.claim_exact_input()
        self.assertEqual(
            caught.exception.failure_family,
            dual.DualSuccessorFailureFamily.ALREADY_CONSUMED,
        )
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_006_correct_claim_then_same_route_replay_revokes_slot(self):
        selector, _, _, _, _ = self._terminal()
        selector.claim_relation()
        with self.assertRaises(dual.PostTerminalDualSuccessorError) as caught:
            selector.claim_relation()
        self.assertEqual(
            caught.exception.failure_family,
            dual.DualSuccessorFailureFamily.ALREADY_CONSUMED,
        )
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_007_concurrent_correct_and_wrong_routes_have_at_most_one_winner(self):
        selector, _, _, _, _ = self._terminal()
        barrier = Barrier(2)

        def claim(method_name):
            barrier.wait()
            try:
                getattr(selector, method_name)()
                return method_name
            except dual.PostTerminalDualSuccessorError as exc:
                return exc.failure_family.value

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [
                pool.submit(claim, "claim_relation"),
                pool.submit(claim, "claim_exact_input"),
            ]
            results = [future.result() for future in futures]
        self.assertLessEqual(results.count("claim_relation"), 1)
        self.assertNotIn("claim_exact_input", results)
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_008_equal_copy_objects_do_not_inherit_same_attempt_authority(self):
        selector, _, _, _, _ = self._terminal()
        with self.assertRaises(dual.PostTerminalDualSuccessorError):
            copy.copy(selector)
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

        selector, closure, _, _, _ = self._terminal()
        selector._OwnedPostTerminalFactDualSuccessor__terminal_closure = copy.copy(
            closure
        )
        with self.assertRaises(dual.PostTerminalDualSuccessorError):
            selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

        _, inputs, kind = self._negative_worlds()[1]
        selector, _, _, _, _ = self._terminal(inputs, kind=kind)
        copied_carrier = copy.copy(selector.claim_exact_input())
        with self.assertRaises(Exception):
            copied_carrier.input_identity_copy()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_009_synchronized_terminal_branch_rewrite_is_rejected(self):
        selector, closure, _, _, _ = self._terminal()
        values = self._terminal_values(selector, closure)
        forged = copy.deepcopy(values[0])
        forged["branch"] = "ALL_PARSE_REJECTED"
        forged["fact_projection"]["status"] = "BLOCKED_NO_ACCEPTED_PRODUCTS"
        forged["fact_projection"]["expected"] = []
        forged["fact_set"] = None
        forged["parse_partition"]["accepted"] = []
        consumer = selector._OwnedPostTerminalFactDualSuccessor__consumer
        with mock.patch.object(
            consumer,
            "_post_terminal_dual_successor_terminal_source",
            return_value=(forged, *values[1:]),
        ):
            with self.assertRaises(dual.PostTerminalDualSuccessorError):
                selector.claim_exact_input()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_010_normal_policy_or_fact_denominator_shrink_is_rejected(self):
        selector, _, inputs, _, _ = self._terminal()
        object.__setattr__(inputs, "review_policy_canonical_bytes", b"{}")
        with self.assertRaises(dual.PostTerminalDualSuccessorError) as caught:
            selector.claim_relation()
        self.assertIn(
            caught.exception.failure_family,
            {
                dual.DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
                dual.DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
            },
        )
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

        selector, closure, _, _, _ = self._terminal()
        values = self._terminal_values(selector, closure)
        forged = copy.deepcopy(values[0])
        forged["fact_set"]["facts"] = forged["fact_set"]["facts"][:-1]
        consumer = selector._OwnedPostTerminalFactDualSuccessor__consumer
        with mock.patch.object(
            consumer,
            "_post_terminal_dual_successor_terminal_source",
            return_value=(forged, *values[1:]),
        ):
            with self.assertRaises(dual.PostTerminalDualSuccessorError):
                selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_011_negative_original_blob_or_history_shrink_is_rejected(self):
        _, inputs, kind = self._negative_worlds()[1]
        selector, _, inputs, _, _ = self._terminal(inputs, kind=kind)
        carrier = selector.claim_exact_input()
        object.__setattr__(inputs, "verified_blob_bytes_by_object_identity", {})
        with self.assertRaises(Exception):
            carrier.verified_blob_bytes_copy()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

        _, inputs, kind = self._negative_worlds()[3]
        selector, closure, _, _, _ = self._terminal(inputs, kind=kind)
        values = self._terminal_values(selector, closure)
        forged = copy.deepcopy(values[0])
        forged["provider_history"] = forged["provider_history"][:-1]
        consumer = selector._OwnedPostTerminalFactDualSuccessor__consumer
        with mock.patch.object(
            consumer,
            "_post_terminal_dual_successor_terminal_source",
            return_value=(forged, *values[1:]),
        ):
            with self.assertRaises(dual.PostTerminalDualSuccessorError):
                selector.claim_exact_input()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_012_common_mode_wrong_projectors_still_fail_application(self):
        _, inputs, kind = self._negative_worlds()[1]
        selector, _, _, _, _ = self._terminal(inputs, kind=kind)
        with (
            mock.patch.object(
                dual, "_selector_route_for_source", return_value=dual.RELATION_ROUTE
            ),
            mock.patch.object(dual, "_application_route_matches", return_value=True),
        ):
            with self.assertRaises(dual.PostTerminalDualSuccessorError):
                selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_013_late_stop_or_cleanup_incomplete_has_no_claim(self):
        selector, _, _, context, _ = self._terminal()
        context._state = BudgetState.STOPPING
        with self.assertRaises(dual.PostTerminalDualSuccessorError):
            selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

        selector, closure, _, _, _ = self._terminal()
        values = self._terminal_values(selector, closure)
        forged = copy.deepcopy(values[0])
        forged["provider_history"][0]["lifecycle"] = "RELEASE_FAILED"
        consumer = selector._OwnedPostTerminalFactDualSuccessor__consumer
        with mock.patch.object(
            consumer,
            "_post_terminal_dual_successor_terminal_source",
            return_value=(forged, *values[1:]),
        ):
            with self.assertRaises(dual.PostTerminalDualSuccessorError):
                selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_014_old_domains_cannot_claim_new_domain(self):
        old_relation_closure, _, _, _ = self.relation_helper._fact_closure()
        old_relation_parent = (
            old_relation_closure._OwnedProductFactClosure__parent
        )
        with self.assertRaises(fact_consumer.ProductFactConsumerError):
            old_relation_parent._post_terminal_dual_successor_sealed_state(object())

        legacy_parent, *_ = self.fact_helper._world()
        with self.assertRaises(fact_consumer.ProductFactConsumerError):
            legacy_parent._post_terminal_dual_successor_sealed_state(object())

    def test_ptds_015_unknown_or_malformed_terminal_has_no_route(self):
        selector, closure, _, _, _ = self._terminal()
        values = self._terminal_values(selector, closure)
        forged = copy.deepcopy(values[0])
        forged["branch"] = "SIXTH_BRANCH"
        consumer = selector._OwnedPostTerminalFactDualSuccessor__consumer
        with mock.patch.object(
            consumer,
            "_post_terminal_dual_successor_terminal_source",
            return_value=(forged, *values[1:]),
        ):
            with self.assertRaises(dual.PostTerminalDualSuccessorError):
                selector.claim_relation()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_ptds_016_union_carrier_cannot_enter_either_downstream(self):
        class FakeUnionCarrier:
            def claim_relation(self):
                return self

            def claim_exact_input(self):
                return self

        with self.assertRaises(relation.FactRelationTransitionError):
            relation.run_claimed_fact_handoff_relation_transition(FakeUnionCarrier())

        selector, _, _, _, _ = self._terminal()
        relation_carrier = selector.claim_relation()
        self.assertFalse(hasattr(relation_carrier, "claim_exact_input"))

    def test_ptds_017_authority_ceiling_rejects_coverage_or_global_claim(self):
        selector, _, _, _, _ = self._terminal()
        carrier = selector.claim_relation()
        document = carrier.document_copy()
        document["authority_ceiling"]["coverage_ledger"] = True
        document["authority_ceiling"]["global_composition_admission"] = True
        encoded = canonical_json_bytes(document)
        carrier._ClaimedPostTerminalRelationSource__document_bytes = encoded
        carrier._ClaimedPostTerminalRelationSource__bound_document_bytes = encoded
        with self.assertRaises(dual.PostTerminalDualSuccessorError):
            carrier.document_copy()
        self.assertEqual(selector.state, dual.DualSuccessorState.REVOKED)

    def test_existing_relation_executor_accepts_new_claimed_source(self):
        selector, _, _, _, _ = self._terminal()
        admitted = relation.run_claimed_fact_handoff_relation_transition(
            selector.claim_relation()
        )
        document = admitted.document_copy()
        self.assertEqual(document["admission"]["status"], "QUALIFIED")
        self.assertEqual(document["handoff"]["source_branch"], "NORMAL_FULFILLED")
        self.assertEqual(
            document["relation_set"]["artifact_kind"],
            "PRIVATE_HANDOFF_RELATION_SET",
        )

    def test_existing_negative_producer_accepts_new_exact_input_claim(self):
        _, inputs, kind = self._negative_worlds()[1]
        selector, _, _, _, _ = self._terminal(inputs, kind=kind)
        attempt = negative_coverage.claim_negative_world_coverage_attempt(
            selector.claim_exact_input()
        )
        candidate = negative_coverage.produce_negative_world_coverage_candidate(
            attempt
        )
        validation = (
            negative_coverage.independently_validate_negative_world_coverage_candidate(
                attempt, candidate
            )
        )
        admitted = negative_coverage.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )
        ledger = admitted.coverage_ledger_document_copy()
        self.assertEqual(
            ledger["root_bindings"][0]["terminal_branch"],
            "ALL_PARSE_REJECTED",
        )

    def test_existing_entry_bytes_and_public_exports_remain_independent(self):
        import veritrail_review

        self.assertNotIn("create_post_terminal_fact_dual_successor_consumer", dir(veritrail_review))
        old_closure, _, _, _ = self.relation_helper._fact_closure()
        old = relation.run_fact_handoff_relation_transition(old_closure)
        selector, _, _, _, _ = self._terminal()
        new = relation.run_claimed_fact_handoff_relation_transition(
            selector.claim_relation()
        )
        old_set = old.document_copy()["relation_set"]
        new_set = new.document_copy()["relation_set"]
        self.assertEqual(old_set["relation_set_digest"], new_set["relation_set_digest"])
        self.assertEqual(
            [item["relation_id"] for item in old_set["relations"]],
            [item["relation_id"] for item in new_set["relations"]],
        )


if __name__ == "__main__":
    unittest.main()
