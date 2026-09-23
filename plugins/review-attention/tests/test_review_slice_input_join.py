from __future__ import annotations

import inspect
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_relation_observation_qualification as qualification_support  # noqa: E402
from veritrail_review import _relation_observation_qualification as qualification  # noqa: E402
from veritrail_review import _review_slice_input as slice_input  # noqa: E402
from veritrail_review._execution_cell_binding import ProviderBinding  # noqa: E402
from veritrail_review._review_slice_input_values import (  # noqa: E402
    _ReviewSliceInputError,
    _ReviewSliceInputFailureCode,
)
from veritrail_review.derivation_input_contracts import DerivationInputSet  # noqa: E402


class ReviewSliceInputJoinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        support = qualification_support.RelationObservationQualificationTests
        support.setUpClass()
        cls.support = support
        cls.inputs = support.inputs

    @classmethod
    def tearDownClass(cls) -> None:
        cls.support.tearDownClass()

    def assertJoinFailure(self, code, callback) -> None:  # noqa: N802
        with self.assertRaises(_ReviewSliceInputError) as caught:
            callback()
        self.assertIs(caught.exception.code, code)

    def _run(
        self,
        derivation_id: str,
        *,
        relation_launch_key: str | None = None,
        capture_context: list[object] | None = None,
    ):
        original_fact_run = qualification._run_prepared_closed_test_execution_attempt
        original_build = qualification.build_prepared_relation_observation_attempt
        original_admit = qualification.admit_derivation_budget

        def fact_run(prepared):
            phase = original_fact_run(prepared)
            return self.support.helper._phase_with_module_and_import(
                prepared, phase
            )

        def build(*args, **kwargs):
            binding = kwargs["binding"]
            if (
                relation_launch_key == "observation-a-unavailable"
                and binding.descriptor.provider_id
                == "closed-relation-provider-a"
            ):
                kwargs["binding"] = ProviderBinding(
                    binding.descriptor, relation_launch_key
                )
            return original_build(*args, **kwargs)

        def admit(inputs):
            context = original_admit(inputs)
            if capture_context is not None:
                capture_context.append(context)
            return context

        with mock.patch.object(
            qualification,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=fact_run,
        ), mock.patch.object(
            qualification,
            "build_prepared_relation_observation_attempt",
            side_effect=build,
        ), mock.patch.object(
            qualification,
            "admit_derivation_budget",
            side_effect=admit,
        ):
            return qualification.run_closed_test_relation_observation_qualification_for_slice_input(
                self.inputs,
                derivation_id=derivation_id,
                bindings=(
                    qualification.closed_test_relation_observation_qualification_bindings()
                ),
            )

    def test_a_001_exact_live_attempt_forms_one_private_input_join(self) -> None:
        qualified = self._run("slice-input-a-positive")
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        joined = slice_input.claim_admitted_graph_slice_input(
            self.inputs, authority
        )

        self.assertEqual(joined.derivation_id, "slice-input-a-positive")
        self.assertEqual(
            joined.qualification_digest,
            qualified.qualification.qualification_digest,
        )
        self.assertEqual(
            joined.relation_set_digest,
            joined._owned_admission().relation_set_digest,
        )
        self.assertIs(joined._owned_inputs(), self.inputs)
        self.assertIs(joined._owned_qualification(), qualified.qualification)
        self.assertTrue(joined.continuation_permitted())
        for forbidden in (
            "output_path",
            "output_directory",
            "manifest",
            "review_slice_set",
            "coverage",
        ):
            self.assertFalse(hasattr(joined, forbidden))

    def test_a_002_raw_qualification_or_admission_has_no_join_authority(self) -> None:
        qualified = self._run("slice-input-a-raw")
        admitted = slice_input.admit_relation_set_for_private_closed_proof(
            qualified.qualification
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED,
            lambda: slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified.qualification
            ),
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED,
            lambda: slice_input.claim_admitted_graph_slice_input(
                self.inputs, admitted
            ),
        )

    def test_a_003_admission_binding_and_input_claim_are_each_one_shot(self) -> None:
        qualified = self._run("slice-input-a-one-shot")
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED,
            lambda: slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            ),
        )
        joined = slice_input.claim_admitted_graph_slice_input(
            self.inputs, authority
        )
        self.assertTrue(joined.continuation_permitted())
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED,
            lambda: slice_input.claim_admitted_graph_slice_input(
                self.inputs, authority
            ),
        )

    def test_a_004_equal_bytes_in_a_new_input_object_do_not_inherit_attempt(self) -> None:
        qualified = self._run("slice-input-a-reconstructed")
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        reconstructed = DerivationInputSet.create(
            source_snapshot_canonical_bytes=(
                self.inputs.source_snapshot_canonical_bytes
            ),
            review_policy_canonical_bytes=self.inputs.review_policy_canonical_bytes,
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
            derivation_profile_digest=self.inputs.derivation_profile_digest,
        )
        self.assertIsNot(reconstructed, self.inputs)
        self.assertEqual(
            reconstructed.source_snapshot_canonical_bytes,
            self.inputs.source_snapshot_canonical_bytes,
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED,
            lambda: slice_input.claim_admitted_graph_slice_input(
                reconstructed, authority
            ),
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED,
            lambda: slice_input.claim_admitted_graph_slice_input(
                self.inputs, authority
            ),
        )

    def test_a_005_stopped_original_budget_cannot_be_replaced_or_claimed(self) -> None:
        contexts: list[object] = []
        qualified = self._run(
            "slice-input-a-stopped", capture_context=contexts
        )
        self.assertEqual(len(contexts), 1)
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        contexts[0].request_cancellation()
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED,
            lambda: slice_input.claim_admitted_graph_slice_input(
                self.inputs, authority
            ),
        )

    def test_a_006_not_qualified_history_cannot_export_continuation(self) -> None:
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE,
            lambda: self._run(
                "slice-input-a-not-qualified",
                relation_launch_key="observation-a-unavailable",
            ),
        )

    def test_a_007_new_surfaces_are_private_and_nonpublishing(self) -> None:
        import veritrail_review

        for name in (
            "run_closed_test_relation_observation_qualification_for_slice_input",
            "admit_relation_set_for_slice_input_private_closed_proof",
            "claim_admitted_graph_slice_input",
        ):
            self.assertFalse(hasattr(veritrail_review, name))
            self.assertNotIn(name, veritrail_review.__all__)

        for callback in (
            qualification.run_closed_test_relation_observation_qualification_for_slice_input,
            slice_input.admit_relation_set_for_slice_input_private_closed_proof,
            slice_input.claim_admitted_graph_slice_input,
        ):
            parameters = inspect.signature(callback).parameters
            for forbidden in (
                "output_path",
                "output_directory",
                "publisher",
                "manifest",
            ):
                self.assertNotIn(forbidden, parameters)

    def test_a_008_concurrent_claim_has_exactly_one_winner(self) -> None:
        qualified = self._run("slice-input-a-concurrent")
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        barrier = Barrier(2)

        def claim():
            barrier.wait()
            try:
                joined = slice_input.claim_admitted_graph_slice_input(
                    self.inputs, authority
                )
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("JOINED", joined)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = [future.result() for future in (pool.submit(claim), pool.submit(claim))]

        self.assertEqual(
            sorted(item[0] for item in outcomes), ["ERROR", "JOINED"]
        )
        failure = next(item for item in outcomes if item[0] == "ERROR")
        success = next(item for item in outcomes if item[0] == "JOINED")
        self.assertIs(
            failure[1], _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED
        )
        self.assertTrue(success[1].continuation_permitted())


if __name__ == "__main__":
    unittest.main()
