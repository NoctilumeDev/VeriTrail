from __future__ import annotations

import json
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_fact_fulfillment as fact_tests  # noqa: E402
import test_fact_relation_transition as relation_tests  # noqa: E402
import test_language_support as language_tests  # noqa: E402
from test_execution_cell import (  # noqa: E402
    _canonical_artifact,
    _policy_document,
    _seal_policy,
)
from veritrail_review import _fact_fulfillment as fact  # noqa: E402
from veritrail_review import _fact_to_coverage_handoff as legacy  # noqa: E402
from veritrail_review import (  # noqa: E402
    _fact_to_coverage_exact_input_handoff as successor,
)
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    AttemptEligibilityState,
)
from veritrail_review.budget import BudgetContext, BudgetState  # noqa: E402
from veritrail_review.contracts import build_source_snapshot_document  # noqa: E402
from veritrail_review.derivation_input_contracts import (  # noqa: E402
    DerivationInputSet,
)


class FactToCoverageExactInputHandoffTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.helper = fact_tests.FactFulfillmentTests()

    @staticmethod
    def _equal_foreign(inputs: DerivationInputSet) -> DerivationInputSet:
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=inputs.review_policy_canonical_bytes,
            derivation_profile_canonical_bytes=(
                inputs.derivation_profile_canonical_bytes
            ),
            verified_blob_bytes_by_object_identity=(
                inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=inputs.policy_digest,
            analysis_scope_digest=inputs.analysis_scope_digest,
            slice_policy_digest=inputs.slice_policy_digest,
            derivation_profile_digest=inputs.derivation_profile_digest,
        )

    @staticmethod
    def _empty_inputs() -> DerivationInputSet:
        profile_path = (
            REPO_ROOT
            / "tests"
            / "fixtures"
            / "review-r1-derivation-input-0.1"
            / "reference-lab"
            / "derivation-profile.json"
        )
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        snapshot = build_source_snapshot_document(
            repository_id="fixture/fact-coverage-exact-input-empty",
            commit_oid={"algorithm": "SHA1", "hex": "1" * 40},
            commit_tree_oid={"algorithm": "SHA1", "hex": "2" * 40},
            analysis_tree_oid={"algorithm": "SHA1", "hex": "3" * 40},
            analysis_root={"path_kind": "REPOSITORY_ROOT"},
            inventory=[],
        )
        policy = _policy_document(snapshot)
        policy["derivation_profile_digest"] = profile["profile_digest"]
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=_canonical_artifact(snapshot),
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=_canonical_artifact(profile),
            verified_blob_bytes_by_object_identity={},
            source_snapshot_digest=snapshot["source_snapshot_digest"],
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=profile["profile_digest"],
        )

    def _closure(self, inputs=None, *, kind="COMPLETED"):
        inputs = self.helper._inputs() if inputs is None else inputs
        parent, context, eligibility, *_ = self.helper._world(inputs)
        observations = (
            self.helper._execute(parent, kind=kind) if parent.claims() else ()
        )
        return (
            parent,
            parent.reconcile(observations),
            inputs,
            context,
            eligibility,
        )

    def _relation_closure(self):
        closure, _, context, eligibility = (
            relation_tests.FactRelationTransitionTests()._fact_closure()
        )
        return closure, context, eligibility

    def test_fcxi_000_002_binds_original_inputs_after_terminal_validation(self):
        parent, closure, inputs, context, _ = self._closure()
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        identity = value.input_identity_copy()

        self.assertIs(
            value._ClaimedFactToCoverageExactInputHandoff__inputs, inputs
        )
        self.assertIs(
            value._ClaimedFactToCoverageExactInputHandoff__context, context
        )
        self.assertEqual(
            identity["handoff_function"], successor.HANDOFF_FUNCTION
        )
        self.assertEqual(identity["claim_purpose"], successor.CLAIM_PURPOSE)
        self.assertEqual(identity["consumer_identity"], successor.HANDOFF_CONSUMER)
        self.assertEqual(identity["carrier_identity"], successor.CARRIER_IDENTITY)
        self.assertTrue(all(identity["same_object_graph_proof"].values()))
        self.assertEqual(
            value.fact_terminal_source_copy()["branch"], "NORMAL_FULFILLED"
        )
        self.assertIs(parent._inputs_ref(), inputs)

        foreign = self._equal_foreign(inputs)
        self.assertIsNot(foreign, inputs)
        self.assertEqual(
            foreign.source_snapshot_canonical_bytes,
            inputs.source_snapshot_canonical_bytes,
        )
        value._ClaimedFactToCoverageExactInputHandoff__inputs = foreign
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            value.input_identity_copy()

        parent, closure, _, _, eligibility = self._closure()
        with self.assertRaises(fact.ProductFactConsumerError):
            parent._handoff_source_with_original_inputs(closure, _token=object())
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_fcxi_003_006_all_fact_source_claims_share_one_slot(self):
        _, closure, *_ = self._closure()
        closure.claim_continuation()
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            successor.claim_fact_to_coverage_exact_input_handoff(closure)

        _, closure, *_ = self._closure()
        legacy.claim_fact_to_coverage_handoff(closure)
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            successor.claim_fact_to_coverage_exact_input_handoff(closure)

        relation_closure, *_ = self._relation_closure()
        relation_closure._claim_relation_handoff_source()
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            successor.claim_fact_to_coverage_exact_input_handoff(relation_closure)

        _, closure, *_ = self._closure()
        successor.claim_fact_to_coverage_exact_input_handoff(closure)
        with self.assertRaises(fact.ProductFactConsumerError):
            closure.claim_continuation()
        with self.assertRaises(legacy.FactToCoverageHandoffError):
            legacy.claim_fact_to_coverage_handoff(closure)

        _, closure, *_ = self._closure()
        barrier = Barrier(2)

        def claim(kind):
            barrier.wait()
            try:
                if kind == "successor":
                    successor.claim_fact_to_coverage_exact_input_handoff(closure)
                else:
                    legacy.claim_fact_to_coverage_handoff(closure)
                return True
            except (
                successor.FactToCoverageExactInputHandoffError,
                legacy.FactToCoverageHandoffError,
            ):
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(pool.map(claim, ("successor", "legacy"))), 1)

    def test_fcxi_001_013_required_failure_uses_terminal_not_live_authority(self):
        parent, closure, inputs, context, eligibility = self._closure(
            kind="PROVIDER_FAILED"
        )
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)
        with self.assertRaises(fact.ProductFactConsumerError):
            parent._inputs_ref()

        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        self.assertEqual(
            value.fact_terminal_source_copy()["branch"],
            "REQUIRED_PROVIDER_NON_SUCCESS",
        )
        self.assertIs(
            value._ClaimedFactToCoverageExactInputHandoff__inputs, inputs
        )
        self.assertIs(
            value._ClaimedFactToCoverageExactInputHandoff__context, context
        )
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_fcxi_013_all_five_terminal_branches_are_total(self):
        worlds = [
            (None, "COMPLETED", "NORMAL_FULFILLED"),
            (
                self.helper._inputs([(b"a.txt", b"ignored")]),
                "COMPLETED",
                "ZERO_PARSE_DENOMINATOR",
            ),
            (
                self.helper._inputs([(b"a.py", b"def bad(:\n")]),
                "COMPLETED",
                "ALL_PARSE_REJECTED",
            ),
            (
                self.helper._inputs(
                    [
                        (
                            b"a.py",
                            "class ｉｆ:\n    pass\ndef later():\n    pass\n".encode(),
                        )
                    ]
                ),
                "COMPLETED",
                "PROJECTION_BLOCKED",
            ),
            (None, "PROVIDER_FAILED", "REQUIRED_PROVIDER_NON_SUCCESS"),
        ]
        observed = []
        for inputs, kind, expected in worlds:
            _, closure, *_ = self._closure(inputs, kind=kind)
            value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
            observed.append(value.fact_terminal_source_copy()["branch"])
        self.assertEqual(observed, [item[2] for item in worlds])

    def test_fcxi_014_zero_parse_worlds_preserve_distinct_denominators(self):
        unsupported = self.helper._inputs([(b"a.txt", b"ignored")])
        policy_excluded = (
            language_tests.LanguageSupportPrivateClassifierTests()._inputs(
                [(b"pkg/a.py", b"print('hidden')\n", "100644", "REGULAR_BLOB")],
                dispositions={b"pkg/a.py": "OUT_OF_SCOPE"},
            )
        )
        counts = []
        for inputs in (self._empty_inputs(), unsupported, policy_excluded):
            _, closure, *_ = self._closure(inputs)
            value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
            self.assertEqual(
                value.fact_terminal_source_copy()["branch"],
                "ZERO_PARSE_DENOMINATOR",
            )
            snapshot = value.source_snapshot_document_copy()
            policy = value.review_policy_document_copy()
            counts.append(
                (len(snapshot["inventory"]), len(policy["scope_decisions"]))
            )
        self.assertEqual(counts, [(0, 0), (1, 1), (1, 1)])

    def test_fcxi_007_009_late_stop_and_foreign_context_fail_permanently(self):
        _, closure, _, context, eligibility = self._closure()
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        context.request_cancellation()
        object.__setattr__(context, "_state", BudgetState.RUNNING)
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            value.fact_terminal_source_copy()
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            value.input_identity_copy()

        _, closure, _, context, eligibility = self._closure()
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        foreign = BudgetContext._admit_for_testing(context.limits)
        value._ClaimedFactToCoverageExactInputHandoff__context = foreign
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            value.source_snapshot_document_copy()
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_fcxi_008_012_any_input_or_blob_drift_fails_closed(self):
        for field, replacement in (
            ("policy_digest", "0" * 64),
            ("source_snapshot_canonical_bytes", b"{}\n"),
            ("verified_blob_bytes_by_object_identity", {}),
        ):
            _, closure, inputs, _, eligibility = self._closure()
            value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
            object.__setattr__(inputs, field, replacement)
            with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
                value.input_identity_copy()
            self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_fcxi_010_source_or_object_graph_substitution_fails_closed(self):
        _, closure, _, _, eligibility = self._closure()
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        value._ClaimedFactToCoverageExactInputHandoff__source_bytes = bytes(
            bytearray(
                value._ClaimedFactToCoverageExactInputHandoff__source_bytes
            )
        )
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            value.fact_terminal_source_copy()
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

        _, closure, _, _, eligibility = self._closure()
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        _, foreign_closure, *_ = self._closure()
        value._ClaimedFactToCoverageExactInputHandoff__closure = foreign_closure
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            value.fact_terminal_source_copy()
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_fcxi_015_unsafe_or_non_owned_source_is_rejected(self):
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
        with self.assertRaises(successor.FactToCoverageExactInputHandoffError):
            successor.claim_fact_to_coverage_exact_input_handoff(parent)  # type: ignore[arg-type]

    def test_fcxi_016_unknown_or_closest_identity_is_rejected_exactly(self):
        _, closure, *_ = self._closure()
        for keyword, value in (
            ("handoff_function", successor.HANDOFF_FUNCTION.replace("0.2", "0.3")),
            ("claim_purpose", successor.CLAIM_PURPOSE.removesuffix("_0_2")),
            ("consumer_identity", successor.HANDOFF_CONSUMER + "-closest"),
            ("carrier_identity", successor.CARRIER_IDENTITY.replace("0.1", "0.2")),
        ):
            with self.assertRaises(
                successor.FactToCoverageExactInputHandoffError
            ):
                successor.claim_fact_to_coverage_exact_input_handoff(
                    closure, **{keyword: value}
                )
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        self.assertEqual(
            value.input_identity_copy()["handoff_function"],
            successor.HANDOFF_FUNCTION,
        )

    def test_fcxi_017_019_legacy_and_public_surfaces_remain_unchanged(self):
        import veritrail_review

        self.assertEqual(legacy.HANDOFF_FUNCTION, "r1-fact-to-coverage-handoff/0.1")
        self.assertFalse(
            hasattr(veritrail_review, "claim_fact_to_coverage_exact_input_handoff")
        )
        _, closure, *_ = self._closure()
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        public_methods = [name for name in dir(value) if not name.startswith("_")]
        self.assertEqual(
            public_methods,
            [
                "derivation_profile_document_copy",
                "fact_terminal_source_copy",
                "input_identity_copy",
                "review_policy_document_copy",
                "source_snapshot_document_copy",
                "verified_blob_bytes_copy",
            ],
        )

    def test_fcxi_011_018_copies_preserve_truth_without_coverage_authority(self):
        _, closure, *_ = self._closure()
        value = successor.claim_fact_to_coverage_exact_input_handoff(closure)
        source = value.fact_terminal_source_copy()
        snapshot = value.source_snapshot_document_copy()
        policy = value.review_policy_document_copy()
        profile = value.derivation_profile_document_copy()
        blobs = value.verified_blob_bytes_copy()
        identity = value.input_identity_copy()

        source["fact_projection"]["universe"].clear()
        snapshot["inventory"].clear()
        policy["scope_decisions"].clear()
        profile.clear()
        blobs.clear()
        identity["same_object_graph_proof"].clear()
        self.assertTrue(
            value.fact_terminal_source_copy()["fact_projection"]["universe"]
        )
        self.assertTrue(value.source_snapshot_document_copy()["inventory"])
        self.assertTrue(value.review_policy_document_copy()["scope_decisions"])
        self.assertTrue(value.derivation_profile_document_copy())
        self.assertTrue(value.verified_blob_bytes_copy())
        self.assertTrue(value.input_identity_copy()["same_object_graph_proof"])

        raw = json.dumps(
            {
                "source": value.fact_terminal_source_copy(),
                "identity": value.input_identity_copy(),
            },
            sort_keys=True,
        )
        for forbidden in (
            "coverage_status",
            "coverage_obligation",
            "CoverageItemRef",
            "CoverageLedger",
            "ReviewSliceSet",
            "manifest_role",
        ):
            self.assertNotIn(forbidden, raw)


if __name__ == "__main__":
    unittest.main()
