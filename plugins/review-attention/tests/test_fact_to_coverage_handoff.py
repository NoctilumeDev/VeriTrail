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

import test_fact_fulfillment as fact_tests
from veritrail_review import _fact_fulfillment as fact
from veritrail_review import _fact_to_coverage_handoff as handoff
from veritrail_review._execution_cell_protocol import AttemptEligibilityState
from veritrail_review.budget import BudgetState


class FactToCoverageHandoffTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.helper = fact_tests.FactFulfillmentTests()

    def _normal(self, *, advisory=False):
        parent, context, eligibility, *_ = self.helper._world(advisory=advisory)
        closure = parent.reconcile(self.helper._execute(parent))
        return parent, closure, context, eligibility

    @staticmethod
    def _source(value):
        return value.document_copy()["source"]

    def test_fchc_000_normal_keeps_optional_gap_and_complete_responsibility(self):
        normal, normal_closure, *_ = self._normal(advisory=True)
        normal_doc = self._source(
            handoff.claim_fact_to_coverage_handoff(normal_closure)
        )

        optional, *_ = self.helper._world(advisory=True)
        observations = []
        for claim in optional.claims():
            failed = claim.binding.descriptor.capability_id.endswith("advisory")
            with mock.patch.object(
                fact,
                "run_windows_execution_cell",
                side_effect=self.helper._cell(
                    kind="PROVIDER_FAILED" if failed else "COMPLETED"
                ),
            ):
                observations.append(fact.execute_product_fact_claim(claim))
        optional_closure = optional.reconcile(observations)
        optional_doc = self._source(
            handoff.claim_fact_to_coverage_handoff(optional_closure)
        )

        self.assertEqual(normal_doc["branch"], "NORMAL_FULFILLED")
        self.assertEqual(optional_doc["branch"], "NORMAL_FULFILLED")
        def semantic_facts(document):
            return [
                {key: value for key, value in item.items() if key != "provenance_refs"}
                for item in document["fact_set"]["facts"]
            ]

        self.assertEqual(semantic_facts(normal_doc), semantic_facts(optional_doc))
        self.assertEqual(
            [row["lifecycle"] for row in optional_doc["provider_history"]],
            ["COMPLETED", "COMPLETED", "FAILED"],
        )
        self.assertEqual(
            [row["required"] for row in optional_doc["provider_history"]],
            [True, True, False],
        )

    def test_fchc_001_zero_denominator_and_all_rejected_are_distinct(self):
        documents = []
        for bodies in (
            [(b"a.txt", b"ignored")],
            [(b"a.py", b"def bad(:\n")],
        ):
            parent, *_ = self.helper._world(self.helper._inputs(bodies))
            closure = parent.reconcile(())
            documents.append(
                self._source(handoff.claim_fact_to_coverage_handoff(closure))
            )
        self.assertEqual(
            [value["branch"] for value in documents],
            ["ZERO_PARSE_DENOMINATOR", "ALL_PARSE_REJECTED"],
        )
        self.assertNotEqual(
            documents[0]["parse_partition"], documents[1]["parse_partition"]
        )
        for value in documents:
            self.assertIsNone(value["fact_set"])
            self.assertTrue(
                all(row["lifecycle"] == "NOT_STARTED" for row in value["provider_history"])
            )

    def test_fchc_002_projection_blocked_keeps_full_u_e_and_blocker(self):
        parent, *_ = self.helper._world(
            self.helper._inputs(
                [(b"a.py", "class ｉｆ:\n    pass\ndef later():\n    pass\n".encode())]
            )
        )
        projection = parent.qualification_copy()
        self.assertEqual((len(projection["universe"]), len(projection["expected"])), (3, 2))
        closure = parent.reconcile(())
        source = self._source(handoff.claim_fact_to_coverage_handoff(closure))
        self.assertEqual(source["branch"], "PROJECTION_BLOCKED")
        self.assertEqual(len(source["fact_projection"]["universe"]), 3)
        self.assertEqual(len(source["fact_projection"]["expected"]), 2)
        self.assertEqual(len(source["fact_projection"]["blockers"]), 1)
        self.assertIsNone(source["fact_set"])

    def test_fchc_003_required_non_success_is_a_safe_negative_handoff(self):
        parent, context, eligibility, *_ = self.helper._world()
        closure = parent.reconcile(
            self.helper._execute(parent, kind="PROVIDER_FAILED")
        )
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)
        value = handoff.claim_fact_to_coverage_handoff(closure)
        source = self._source(value)
        self.assertEqual(source["branch"], "REQUIRED_PROVIDER_NON_SUCCESS")
        self.assertTrue(source["fact_projection"]["universe"])
        self.assertTrue(source["fact_projection"]["expected"])
        self.assertIsNone(source["fact_set"])
        self.assertIs(value._context_ref(), context)

    def test_fchc_004_unsafe_partial_prefix_has_no_handoff_claim(self):
        parent, *_ = self.helper._world(advisory=True)
        observations = []
        for claim in parent.claims():
            unsafe = claim.binding.descriptor.capability_id.endswith("advisory")
            with mock.patch.object(
                fact,
                "run_windows_execution_cell",
                side_effect=self.helper._cell(
                    lifecycle={"handles_released": False} if unsafe else None
                ),
            ):
                observations.append(fact.execute_product_fact_claim(claim))
        with self.assertRaises(fact.ProductFactConsumerError):
            parent.reconcile(observations)
        self.assertEqual(
            [value.lifecycle for value in parent.retained_observations()],
            ["COMPLETED", "COMPLETED", "RELEASE_FAILED"],
        )
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            handoff.claim_fact_to_coverage_handoff(parent)  # type: ignore[arg-type]

    def test_fchc_005_serialized_knowledge_is_not_live_authority(self):
        _, closure, *_ = self._normal()
        serialized = closure.document_copy()
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            handoff.claim_fact_to_coverage_handoff(serialized)  # type: ignore[arg-type]

    def test_fchc_006_foreign_equal_world_and_late_stop_do_not_inherit(self):
        _, first, first_context, *_ = self._normal()
        _, second, second_context, *_ = self._normal()
        self.assertIsNot(first_context, second_context)
        first_value = handoff.claim_fact_to_coverage_handoff(first)
        first_semantics = self._source(first_value)
        second_semantics = self._source(
            handoff.claim_fact_to_coverage_handoff(second)
        )
        self.assertNotEqual(
            first_semantics["input_identity"]["fact_consumer_attempt_id"],
            second_semantics["input_identity"]["fact_consumer_attempt_id"],
        )
        first_context.request_cancellation()
        object.__setattr__(first_context, "_state", BudgetState.RUNNING)
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            first_value.document_copy()

        foreign_parent, foreign_closure, _, foreign_eligibility = self._normal()
        _, _, foreign_context, _ = self._normal()
        object.__setattr__(
            foreign_parent,
            "_OwnedProductFactConsumer__context",
            foreign_context,
        )
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            handoff.claim_fact_to_coverage_handoff(foreign_closure)
        self.assertIs(foreign_eligibility.state, AttemptEligibilityState.REVOKED)

    def test_fchc_007_008_legacy_and_handoff_share_one_source_claim(self):
        _, closure, *_ = self._normal()
        closure.claim_continuation()
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            handoff.claim_fact_to_coverage_handoff(closure)

        _, closure, *_ = self._normal()
        handoff.claim_fact_to_coverage_handoff(closure)
        with self.assertRaises(fact.ProductFactConsumerError):
            closure.claim_continuation()

        _, closure, *_ = self._normal()
        barrier = Barrier(2)

        def claim(kind):
            barrier.wait()
            try:
                if kind == "handoff":
                    handoff.claim_fact_to_coverage_handoff(closure)
                else:
                    closure.claim_continuation()
                return True
            except (handoff.FactToCoverageHandoffError, fact.ProductFactConsumerError):
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(pool.map(claim, ("handoff", "legacy"))), 1)

    def test_fchc_009_provider_order_is_canonical_not_completion_order(self):
        parent, *_ = self.helper._world(advisory=True)
        observations = list(self.helper._execute(parent))
        closure = parent.reconcile(tuple(reversed(observations)))
        source = self._source(handoff.claim_fact_to_coverage_handoff(closure))
        self.assertEqual(
            [row["descriptor"]["provider_id"] for row in source["provider_history"]],
            [
                claim.binding.descriptor.provider_id
                for claim in parent.claims()
            ],
        )

    def test_fchc_010_unrepresentable_slot_never_becomes_a_fact_ref(self):
        parent, *_ = self.helper._world(
            self.helper._inputs(
                [(b"a.py", "class ｉｆ:\n    pass\ndef later():\n    pass\n".encode())]
            )
        )
        source = self._source(
            handoff.claim_fact_to_coverage_handoff(parent.reconcile(()))
        )
        blocked = source["fact_projection"]["blockers"][0]
        self.assertIn(blocked["slot"], source["fact_projection"]["universe"])
        self.assertNotIn(
            blocked["slot"]["subject_key_digest"],
            {value["fact_id"] for value in source["fact_projection"]["expected"]},
        )
        raw = json.dumps(source, sort_keys=True)
        for forbidden in ("coverage_status", "CoverageItemRef", "ReviewSliceSet"):
            self.assertNotIn(forbidden, raw)

    def test_fchc_011_copy_owned_value_has_no_coverage_or_execution_authority(self):
        _, closure, context, *_ = self._normal()
        value = handoff.claim_fact_to_coverage_handoff(closure)
        document = value.document_copy()
        document["source"]["fact_projection"]["universe"].clear()
        self.assertTrue(value.document_copy()["source"]["fact_projection"]["universe"])
        self.assertIs(value._context_ref(), context)
        self.assertEqual(
            [name for name in dir(value) if not name.startswith("_")],
            ["document_copy"],
        )
        object.__setattr__(value, "_bytes", bytes(bytearray(value._bytes)))
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            value.document_copy()

    def test_claim_replay_and_source_mutation_fail_closed(self):
        parent, closure, *_ = self._normal()
        handoff.claim_fact_to_coverage_handoff(closure)
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            handoff.claim_fact_to_coverage_handoff(closure)

        parent, closure, _, eligibility = self._normal()
        object.__setattr__(parent, "_OwnedProductFactConsumer__bindings", tuple())
        with self.assertRaises(handoff.FactToCoverageHandoffError):
            handoff.claim_fact_to_coverage_handoff(closure)
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)


if __name__ == "__main__":
    unittest.main()
