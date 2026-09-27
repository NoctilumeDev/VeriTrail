from __future__ import annotations

import inspect
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_language_support as language_support_tests  # noqa: E402
import test_source_operation_projection as projection_support  # noqa: E402
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import _source_operation_gate as gate  # noqa: E402
from veritrail_review import _source_operation_projection as projection  # noqa: E402
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    encode_frame,
)
from veritrail_review.budget import (  # noqa: E402
    BudgetContext,
    ExecutionBudgetLimits,
)
from veritrail_review.derivation_input_contracts import (  # noqa: E402
    DerivationInputSet,
)


class SourceOperationSameAttemptGateStageBTests(unittest.TestCase):
    def setUp(self) -> None:
        support = projection_support.SourceOperationProjectionStageATests(
            "test_a_001_fact_projection_is_exact_eligible_upper_bound"
        )
        support.setUp()
        self.support = support
        self.inputs = support.inputs
        self.classification = support.classification
        self.projection = (
            projection.build_fact_derivation_source_operation_projection(
                self.classification,
                support.fact_descriptor,
            )
        )
        self.limits = ExecutionCellTransportSafetyLimits(
            request_payload_bytes=4096,
            terminal_payload_bytes=4096,
        )
        self.frame = self._frame("fact-a")
        self.context = self._context()
        self.parent = AttemptEligibility()
        self.gate = gate.create_source_operation_attempt_gate(
            self.inputs,
            self.context,
            self.parent,
            self.classification,
        )

    def test_b_001_exact_parent_and_child_bind_one_live_claim(self) -> None:
        child = AttemptEligibility()
        claim = self._bind(child=child)
        self.gate.admit_parent()

        claimed = claim.claim()

        self.assertIs(self.parent.state, AttemptEligibilityState.ADMITTED)
        self.assertIs(child.state, AttemptEligibilityState.PROVISIONAL)
        self.assertIs(claimed._owned_inputs(), self.inputs)
        self.assertIs(claimed._owned_classification(), self.classification)
        self.assertIs(claimed._context(), self.context)
        self.assertIs(claimed._parent_eligibility(), self.parent)
        self.assertIs(claimed._owned_projection(), self.projection)
        self.assertEqual(claimed._request_frame_copy(), self.frame)
        self.assertIs(claimed._transport_limits(), self.limits)
        self.assertIs(claimed._child_eligibility(), child)

    def test_b_002_each_child_claim_is_one_shot(self) -> None:
        child = AttemptEligibility()
        claim = self._bind(child=child)
        self.gate.admit_parent()

        first = claim.claim()
        with self.assertRaises(gate._SourceOperationGateError):
            claim.claim()

        self.assertIs(first._child_eligibility(), child)
        self.assertIs(child.state, AttemptEligibilityState.PROVISIONAL)

    def test_b_003_concurrent_claim_has_one_winner(self) -> None:
        claim = self._bind()
        self.gate.admit_parent()
        barrier = Barrier(2)

        def compete() -> object:
            barrier.wait()
            try:
                return claim.claim()
            except gate._SourceOperationGateError as exc:
                return exc

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = tuple(pool.map(lambda _item: compete(), range(2)))

        winners = [
            item
            for item in results
            if isinstance(item, gate.ClaimedSourceOperationRequest)
        ]
        failures = [
            item for item in results if isinstance(item, gate._SourceOperationGateError)
        ]
        self.assertEqual(len(winners), 1)
        self.assertEqual(len(failures), 1)
        self.assertIs(
            winners[0]._child_eligibility().state,
            AttemptEligibilityState.PROVISIONAL,
        )

    def test_b_004_failed_claim_validation_consumes_the_claim(self) -> None:
        child = AttemptEligibility()
        claim = self._bind(child=child)
        self.gate.admit_parent()
        object.__setattr__(
            claim,
            "_OwnedSourceOperationChildClaim__request_frame",
            self._frame("changed"),
        )

        with self.assertRaises(gate._SourceOperationGateError):
            claim.claim()
        with self.assertRaises(gate._SourceOperationGateError):
            claim.claim()

        self.assertIs(child.state, AttemptEligibilityState.REVOKED)
        self.assertIs(self.parent.state, AttemptEligibilityState.REVOKED)

    def test_b_005_same_limits_fresh_context_cannot_replace_original(self) -> None:
        child = AttemptEligibility()
        claim = self._bind(child=child)
        self.gate.admit_parent()
        fresh = self._context()
        self.assertEqual(fresh.limits, self.context.limits)
        object.__setattr__(
            self.gate,
            "_OwnedSourceOperationAttemptGate__context",
            fresh,
        )

        with self.assertRaises(gate._SourceOperationGateError):
            claim.claim()

        self.assertIs(self.parent.state, AttemptEligibilityState.REVOKED)
        self.assertIs(child.state, AttemptEligibilityState.REVOKED)

    def test_b_006_parent_or_child_eligibility_cannot_be_swapped(self) -> None:
        with self.subTest(identity="parent"):
            child = AttemptEligibility()
            claim = self._bind(child=child)
            self.gate.admit_parent()
            object.__setattr__(
                self.gate,
                "_OwnedSourceOperationAttemptGate__parent_eligibility",
                AttemptEligibility(),
            )
            with self.assertRaises(gate._SourceOperationGateError):
                claim.claim()
            self.assertIs(child.state, AttemptEligibilityState.REVOKED)

        self.setUp()
        with self.subTest(identity="child"):
            child = AttemptEligibility()
            claim = self._bind(child=child)
            self.gate.admit_parent()
            object.__setattr__(
                claim,
                "_OwnedSourceOperationChildClaim__child_eligibility",
                AttemptEligibility(),
            )
            with self.assertRaises(gate._SourceOperationGateError):
                claim.claim()
            self.assertIs(child.state, AttemptEligibilityState.REVOKED)
            self.assertIs(self.parent.state, AttemptEligibilityState.REVOKED)

    def test_b_007_projection_or_frame_cannot_be_swapped(self) -> None:
        for identity in ("projection", "frame"):
            with self.subTest(identity=identity):
                self.setUp()
                child = AttemptEligibility()
                claim = self._bind(child=child)
                self.gate.admit_parent()
                if identity == "projection":
                    changed = (
                        projection.build_fact_derivation_source_operation_projection(
                            self.classification,
                            self.support.other_fact_descriptor,
                        )
                    )
                    object.__setattr__(
                        claim,
                        "_OwnedSourceOperationChildClaim__projection",
                        changed,
                    )
                else:
                    object.__setattr__(
                        claim,
                        "_OwnedSourceOperationChildClaim__request_frame",
                        self._frame("fact-b"),
                    )
                with self.assertRaises(gate._SourceOperationGateError):
                    claim.claim()
                self.assertIs(child.state, AttemptEligibilityState.REVOKED)

    def test_b_008_parent_or_context_stop_invalidates_all_children(self) -> None:
        first_child = AttemptEligibility()
        second_child = AttemptEligibility()
        first = self._bind(child=first_child)
        second = self._bind(child=second_child)
        self.gate.admit_parent()
        self.assertTrue(self.context.request_cancellation())

        for claim in (first, second):
            with self.assertRaises(gate._SourceOperationGateError):
                claim.claim()

        self.assertIs(self.parent.state, AttemptEligibilityState.REVOKED)
        self.assertIs(first_child.state, AttemptEligibilityState.REVOKED)
        self.assertIs(second_child.state, AttemptEligibilityState.REVOKED)

    def test_b_009_equal_semantics_do_not_share_claim_authority(self) -> None:
        first_child = AttemptEligibility()
        second_child = AttemptEligibility()
        first = self._bind(child=first_child)
        second = self._bind(child=second_child)
        self.gate.admit_parent()

        first_claimed = first.claim()
        second_claimed = second.claim()

        self.assertIs(first_claimed._owned_projection(), self.projection)
        self.assertIs(second_claimed._owned_projection(), self.projection)
        self.assertIsNot(first_claimed, second_claimed)
        self.assertIsNot(first_child, second_child)

    def test_b_010_classification_must_match_the_exact_input_world(self) -> None:
        helper = language_support_tests.LanguageSupportPrivateClassifierTests()
        other_inputs = helper._inputs(
            [(b"different.py", b"print('different')\n", "100644", "REGULAR_BLOB")]
        )
        other = language_support.classify_language_support(other_inputs)

        with self.assertRaises(gate._SourceOperationGateError):
            gate.create_source_operation_attempt_gate(
                self.inputs,
                self._context(),
                AttemptEligibility(),
                other,
            )

    def test_b_011_parent_admission_is_one_way_but_later_child_binding_is_legal(
        self,
    ) -> None:
        first = self._bind()
        self.gate.admit_parent()
        with self.assertRaises(gate._SourceOperationGateError):
            self.gate.admit_parent()

        self.setUp()
        first = self._bind()
        self.gate.admit_parent()
        later = self._bind(frame=self._frame("later"))
        self.assertIsInstance(first.claim(), gate.ClaimedSourceOperationRequest)
        self.assertIsInstance(later.claim(), gate.ClaimedSourceOperationRequest)

    def test_b_012_malformed_or_over_limit_frame_fails_before_admission(self) -> None:
        for frame, limits in (
            (b"{}", self.limits),
            (
                self.frame,
                ExecutionCellTransportSafetyLimits(
                    request_payload_bytes=1,
                    terminal_payload_bytes=4096,
                ),
            ),
        ):
            with self.subTest(frame=frame, limits=limits):
                self.setUp()
                child = AttemptEligibility()
                with self.assertRaises(gate._SourceOperationGateError):
                    self._bind(child=child, frame=frame, limits=limits)
                self.assertIs(child.state, AttemptEligibilityState.REVOKED)
                self.assertIs(self.parent.state, AttemptEligibilityState.REVOKED)

    def test_b_013_claimed_request_rechecks_parent_before_use(self) -> None:
        child = AttemptEligibility()
        claim = self._bind(child=child)
        self.gate.admit_parent()
        claimed = claim.claim()
        self.parent.revoke()

        with self.assertRaises(gate._SourceOperationGateError):
            claimed._request_frame_copy()

        self.assertIs(child.state, AttemptEligibilityState.REVOKED)

    def test_b_014_gate_is_private_and_direct_construction_is_rejected(self) -> None:
        import veritrail_review

        self.assertFalse(hasattr(veritrail_review, "OwnedSourceOperationAttemptGate"))
        self.assertFalse(hasattr(veritrail_review, "ClaimedSourceOperationRequest"))
        self.assertNotIn("path", inspect.signature(self._bind).parameters)
        with self.assertRaises(gate._SourceOperationGateError):
            gate.OwnedSourceOperationAttemptGate(
                inputs=self.inputs,
                context=self.context,
                parent_eligibility=self.parent,
                classification=self.classification,
                _construction_token=object(),
            )

    def test_b_015_equal_input_or_classification_cannot_replace_identity(self) -> None:
        for identity in ("inputs", "classification"):
            with self.subTest(identity=identity):
                self.setUp()
                child = AttemptEligibility()
                claim = self._bind(child=child)
                self.gate.admit_parent()
                if identity == "inputs":
                    replacement = DerivationInputSet.create(
                        source_snapshot_canonical_bytes=(
                            self.inputs.source_snapshot_canonical_bytes
                        ),
                        review_policy_canonical_bytes=(
                            self.inputs.review_policy_canonical_bytes
                        ),
                        derivation_profile_canonical_bytes=(
                            self.inputs.derivation_profile_canonical_bytes
                        ),
                        verified_blob_bytes_by_object_identity=(
                            self.inputs.verified_blob_bytes_by_object_identity
                        ),
                        source_snapshot_digest=self.inputs.source_snapshot_digest,
                        policy_digest=self.inputs.policy_digest,
                        analysis_scope_digest=self.inputs.analysis_scope_digest,
                        slice_policy_digest=self.inputs.slice_policy_digest,
                        derivation_profile_digest=(
                            self.inputs.derivation_profile_digest
                        ),
                    )
                    self.assertIsNot(replacement, self.inputs)
                    object.__setattr__(
                        self.gate,
                        "_OwnedSourceOperationAttemptGate__inputs",
                        replacement,
                    )
                else:
                    replacement = language_support.classify_language_support(
                        self.inputs
                    )
                    self.assertEqual(
                        replacement.classification_document_bytes,
                        self.classification.classification_document_bytes,
                    )
                    self.assertIsNot(replacement, self.classification)
                    object.__setattr__(
                        self.gate,
                        "_OwnedSourceOperationAttemptGate__classification",
                        replacement,
                    )
                with self.assertRaises(gate._SourceOperationGateError):
                    claim.claim()
                self.assertIs(self.parent.state, AttemptEligibilityState.REVOKED)
                self.assertIs(child.state, AttemptEligibilityState.REVOKED)

    def test_b_016_one_child_eligibility_cannot_back_two_claims(self) -> None:
        child = AttemptEligibility()
        first = self._bind(child=child)

        with self.assertRaises(gate._SourceOperationGateError):
            self._bind(child=child, frame=self._frame("duplicate"))

        self.assertIsInstance(first, gate.OwnedSourceOperationChildClaim)
        self.assertIs(self.parent.state, AttemptEligibilityState.REVOKED)
        self.assertIs(child.state, AttemptEligibilityState.REVOKED)

    def _bind(
        self,
        *,
        child: AttemptEligibility | None = None,
        frame: bytes | None = None,
        limits: ExecutionCellTransportSafetyLimits | None = None,
    ) -> gate.OwnedSourceOperationChildClaim:
        return self.gate.bind_child(
            projection=self.projection,
            request_frame=self.frame if frame is None else frame,
            transport_limits=self.limits if limits is None else limits,
            child_eligibility=AttemptEligibility() if child is None else child,
        )

    @staticmethod
    def _frame(name: str) -> bytes:
        return encode_frame({"prepared_request": name}, payload_limit=4096)

    @staticmethod
    def _context() -> BudgetContext:
        return BudgetContext._admit_for_testing(
            ExecutionBudgetLimits(
                wall_clock_ms=60_000,
                memory_bytes=64 * 1024 * 1024,
                artifact_bytes=16 * 1024 * 1024,
            )
        )


if __name__ == "__main__":
    unittest.main()
