from __future__ import annotations

import copy
import hashlib
import inspect
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from threading import Barrier
from types import MappingProxyType
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
from veritrail_review import _review_slice_traversal as traversal  # noqa: E402
from veritrail_review import (  # noqa: E402
    _review_slice_input_cross_validation_values as cross_values,
)
from veritrail_review import (  # noqa: E402
    _review_slice_blocked_input_receipt_values as blocked_values,
)
from veritrail_review import (  # noqa: E402
    _review_slice_obligation_domain_values as domain_values,
)
from veritrail_review import (  # noqa: E402
    _review_slice_empty_domain_closure_values as empty_values,
)
from veritrail_review import (  # noqa: E402
    _review_slice_obligation_closure_values as closure_values,
)
from veritrail_review import (  # noqa: E402
    _review_slice_traversal_assignment_values as assignment_values,
)
from veritrail_review import (  # noqa: E402
    _review_slice_traversal_outcome_values as outcome_values,
)
from veritrail_review._execution_cell_binding import ProviderBinding  # noqa: E402
from veritrail_review._review_slice_input_values import (  # noqa: E402
    _ReviewSliceInputError,
    _ReviewSliceInputFailureCode,
)
from veritrail_review.budget import BudgetContext  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402
from veritrail_review.derivation_input_contracts import DerivationInputSet  # noqa: E402
from test_execution_cell import _canonical_artifact, _seal_policy  # noqa: E402


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
        inputs: DerivationInputSet | None = None,
        relation_launch_key: str | None = None,
        two_imports: bool = False,
        capture_context: list[object] | None = None,
    ):
        original_fact_run = qualification._run_prepared_closed_test_execution_attempt
        original_build = qualification.build_prepared_relation_observation_attempt
        original_admit = qualification.admit_derivation_budget

        def fact_run(prepared):
            phase = original_fact_run(prepared)
            if two_imports:
                return self.support._phase_with_two_imports(prepared, phase)
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
            elif (
                relation_launch_key == "observation-b-conflict"
                and binding.descriptor.provider_id
                == "closed-relation-provider-b"
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

        selected_inputs = self.inputs if inputs is None else inputs
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
                selected_inputs,
                derivation_id=derivation_id,
                bindings=(
                    qualification.closed_test_relation_observation_qualification_bindings()
                ),
            )

    def _input_copy(self) -> DerivationInputSet:
        return DerivationInputSet.create(
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

    def _joined(self, derivation_id: str, *, inputs: DerivationInputSet | None = None):
        selected_inputs = self.inputs if inputs is None else inputs
        qualified = self._run(derivation_id, inputs=selected_inputs)
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        joined = slice_input.claim_admitted_graph_slice_input(
            selected_inputs, authority
        )
        return qualified, joined

    def _validated(
        self,
        derivation_id: str,
        *,
        inputs: DerivationInputSet | None = None,
        relation_launch_key: str | None = None,
        two_imports: bool = False,
        capture_context: list[object] | None = None,
    ):
        selected_inputs = self.inputs if inputs is None else inputs
        qualified = self._run(
            derivation_id,
            inputs=selected_inputs,
            relation_launch_key=relation_launch_key,
            two_imports=two_imports,
            capture_context=capture_context,
        )
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        joined = slice_input.claim_admitted_graph_slice_input(
            selected_inputs, authority
        )
        return (
            qualified,
            slice_input.cross_validate_admitted_graph_slice_input(joined),
        )

    @staticmethod
    def _inputs_with_anchor_fact_kinds(
        inputs: DerivationInputSet,
        anchor_fact_kinds: list[str],
    ) -> DerivationInputSet:
        policy = inputs.review_policy_document_copy()
        policy["slice_policy"]["anchor_fact_kinds"] = anchor_fact_kinds
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=(
                inputs.derivation_profile_canonical_bytes
            ),
            verified_blob_bytes_by_object_identity=(
                inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=inputs.derivation_profile_digest,
        )

    @staticmethod
    def _inputs_with_slice_limits(
        inputs: DerivationInputSet,
        **limits: int,
    ) -> DerivationInputSet:
        policy = inputs.review_policy_document_copy()
        policy["slice_policy"].update(limits)
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=(
                inputs.derivation_profile_canonical_bytes
            ),
            verified_blob_bytes_by_object_identity=(
                inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=inputs.derivation_profile_digest,
        )

    @staticmethod
    def _inputs_with_allowed_relations(
        inputs: DerivationInputSet,
        allowed_relations: list[dict[str, str]],
    ) -> DerivationInputSet:
        policy = inputs.review_policy_document_copy()
        policy["slice_policy"]["allowed_relations"] = allowed_relations
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=(
                inputs.derivation_profile_canonical_bytes
            ),
            verified_blob_bytes_by_object_identity=(
                inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=inputs.derivation_profile_digest,
        )

    def _boundary(
        self,
        derivation_id: str,
        *,
        inputs: DerivationInputSet | None = None,
        capture_context: list[object] | None = None,
    ):
        _, validated = self._validated(
            derivation_id,
            inputs=inputs,
            capture_context=capture_context,
        )
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gated
        )
        return slice_input.claim_next_review_slice_traversal(assignments)

    def _assignments(
        self,
        derivation_id: str,
        *,
        inputs: DerivationInputSet | None = None,
        two_imports: bool = False,
        capture_context: list[object] | None = None,
    ):
        _, validated = self._validated(
            derivation_id,
            inputs=inputs,
            two_imports=two_imports,
            capture_context=capture_context,
        )
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        return slice_input.assign_review_slice_obligations_for_traversal(gated)

    @staticmethod
    def _normal_outcomes(assignments):
        outcomes = []
        while assignments.remaining_assignment_count():
            boundary = slice_input.claim_next_review_slice_traversal(assignments)
            outcomes.append(
                slice_input.derive_review_slice_traversal_outcome(boundary)
            )
        return tuple(outcomes)

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

    def test_a_009_cross_attempt_admission_cannot_ride_live_continuation(
        self,
    ) -> None:
        first = self._run("slice-input-a-transplant")
        second = self._run("slice-input-a-transplant")
        foreign_admission = (
            slice_input.admit_relation_set_for_private_closed_proof(
                second.qualification
            )
        )

        self.assertEqual(
            first.qualification.qualification_digest,
            second.qualification.qualification_digest,
        )
        self.assertNotEqual(
            foreign_admission.request_provenance_bytes,
            first.qualification.fact_phase_results[0].request_provenance_bytes,
        )
        with mock.patch.object(
            slice_input,
            "admit_relation_set_for_private_closed_proof",
            return_value=foreign_admission,
        ) as admission_producer:
            self.assertJoinFailure(
                _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED,
                lambda: slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                    first
                ),
            )
        admission_producer.assert_called_once_with(first.qualification)

        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                first
            )
        )
        joined = slice_input.claim_admitted_graph_slice_input(
            self.inputs, authority
        )
        self.assertTrue(joined.continuation_permitted())

    def test_b_001_exact_history_reconstructs_one_private_fact_set(self) -> None:
        qualified, joined = self._joined("slice-input-b-positive")
        validated = slice_input.cross_validate_admitted_graph_slice_input(joined)
        expected_fact_set = self.support._fact_set_for_result(
            qualified.qualification, self.inputs
        )

        self.assertEqual(validated.fact_set_document_copy(), expected_fact_set)
        self.assertEqual(
            validated.fact_set_document_bytes,
            canonical_json_bytes(expected_fact_set),
        )
        self.assertEqual(
            validated.canonical_fact_set_artifact_bytes,
            validated.fact_set_document_bytes + b"\n",
        )
        self.assertEqual(
            validated.source_snapshot_canonical_bytes,
            self.inputs.source_snapshot_canonical_bytes,
        )
        self.assertEqual(
            validated.review_policy_canonical_bytes,
            self.inputs.review_policy_canonical_bytes,
        )
        self.assertEqual(
            validated.derivation_profile_canonical_bytes,
            self.inputs.derivation_profile_canonical_bytes,
        )
        self.assertEqual(
            dict(validated.verified_blob_bytes_by_object_identity),
            dict(self.inputs.verified_blob_bytes_by_object_identity),
        )
        self.assertEqual(
            validated.relation_set_document_copy(),
            joined._owned_admission().relation_set_document_copy(),
        )
        self.assertTrue(validated.continuation_permitted())
        for forbidden in (
            "output_path",
            "output_directory",
            "manifest",
            "review_slice_set",
            "coverage",
        ):
            self.assertFalse(hasattr(validated, forbidden))

    def test_b_002_cross_validation_is_one_shot(self) -> None:
        _, joined = self._joined("slice-input-b-one-shot")
        validated = slice_input.cross_validate_admitted_graph_slice_input(joined)
        self.assertTrue(validated.continuation_permitted())
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(joined),
        )

    def test_b_003_concurrent_cross_validation_has_one_winner(self) -> None:
        _, joined = self._joined("slice-input-b-concurrent")
        barrier = Barrier(2)

        def cross_validate():
            barrier.wait()
            try:
                validated = slice_input.cross_validate_admitted_graph_slice_input(
                    joined
                )
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("VALIDATED", validated)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = [
                future.result()
                for future in (
                    pool.submit(cross_validate),
                    pool.submit(cross_validate),
                )
            ]

        self.assertEqual(
            sorted(item[0] for item in outcomes), ["ERROR", "VALIDATED"]
        )
        failure = next(item for item in outcomes if item[0] == "ERROR")
        success = next(item for item in outcomes if item[0] == "VALIDATED")
        self.assertIs(
            failure[1],
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
        )
        self.assertTrue(success[1].continuation_permitted())

    def test_b_004_failed_cross_validation_consumes_the_claim(self) -> None:
        inputs = self._input_copy()
        original = inputs.review_policy_canonical_bytes
        _, joined = self._joined("slice-input-b-failed-claim", inputs=inputs)
        policy = inputs.review_policy_document_copy()
        policy["governance"]["claim_owner_ref"] = "foreign-owner"
        object.__setattr__(
            inputs,
            "review_policy_canonical_bytes",
            canonical_json_bytes(policy) + b"\n",
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(joined),
        )
        object.__setattr__(inputs, "review_policy_canonical_bytes", original)
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(joined),
        )

    def test_b_005_rs_009_policy_bytes_cannot_ride_matching_digests(self) -> None:
        inputs = self._input_copy()
        _, joined = self._joined("slice-input-b-policy-bytes", inputs=inputs)
        policy = inputs.review_policy_document_copy()
        policy["governance"]["claim_owner_ref"] = "foreign-owner"
        object.__setattr__(
            inputs,
            "review_policy_canonical_bytes",
            canonical_json_bytes(policy) + b"\n",
        )

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(joined),
        )

    def test_b_006_rs_009_profile_bytes_cannot_ride_matching_digest(self) -> None:
        inputs = self._input_copy()
        _, joined = self._joined("slice-input-b-profile-bytes", inputs=inputs)
        profile = inputs.derivation_profile_document_copy()
        profile["profile_id"] = "foreign-profile"
        object.__setattr__(
            inputs,
            "derivation_profile_canonical_bytes",
            canonical_json_bytes(profile) + b"\n",
        )

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(joined),
        )

    def test_b_007_source_snapshot_bytes_are_rechecked(self) -> None:
        snapshot_inputs = self._input_copy()
        _, snapshot_joined = self._joined(
            "slice-input-b-snapshot-bytes", inputs=snapshot_inputs
        )
        snapshot = snapshot_inputs.source_snapshot_document_copy()
        snapshot["repository_id"] = "foreign-repository"
        object.__setattr__(
            snapshot_inputs,
            "source_snapshot_canonical_bytes",
            canonical_json_bytes(snapshot) + b"\n",
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(
                snapshot_joined
            ),
        )

    def test_b_008_verified_blob_bytes_are_rechecked(self) -> None:
        blob_inputs = self._input_copy()
        _, blob_joined = self._joined(
            "slice-input-b-blob-bytes", inputs=blob_inputs
        )
        blobs = dict(blob_inputs.verified_blob_bytes_by_object_identity)
        oid = sorted(blobs)[0]
        blobs[oid] = b"tampered"
        object.__setattr__(
            blob_inputs,
            "verified_blob_bytes_by_object_identity",
            MappingProxyType(blobs),
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(
                blob_joined
            ),
        )

    def test_b_009_fact_history_is_revalidated(self) -> None:
        fact_inputs = self._input_copy()
        _, fact_joined = self._joined(
            "slice-input-b-fact-history", inputs=fact_inputs
        )
        phase = fact_joined._owned_qualification().fact_phase_results[0]
        object.__setattr__(phase, "canonical_fact_bytes", ())
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(
                fact_joined
            ),
        )

    def test_b_010_admission_history_is_revalidated(self) -> None:
        admission_inputs = self._input_copy()
        _, admission_joined = self._joined(
            "slice-input-b-admission-history", inputs=admission_inputs
        )
        object.__setattr__(
            admission_joined._owned_admission(), "policy_digest", "0" * 64
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(
                admission_joined
            ),
        )

    def test_b_011_surface_remains_private_and_nonpublishing(self) -> None:
        import veritrail_review

        name = "cross_validate_admitted_graph_slice_input"
        self.assertFalse(hasattr(veritrail_review, name))
        self.assertNotIn(name, veritrail_review.__all__)
        parameters = inspect.signature(
            slice_input.cross_validate_admitted_graph_slice_input
        ).parameters
        for forbidden in (
            "output_path",
            "output_directory",
            "publisher",
            "manifest",
        ):
            self.assertNotIn(forbidden, parameters)

    def test_b_012_owned_state_seal_detects_post_validation_mutation(self) -> None:
        _, joined = self._joined("slice-input-b-owned-state")
        validated = slice_input.cross_validate_admitted_graph_slice_input(joined)
        cross_values._validate_cross_validated_input(validated)
        object.__setattr__(validated, "fact_set_document_bytes", b"{}")
        with self.assertRaises(ValueError):
            cross_values._validate_cross_validated_input(validated)

    def test_c_001_consistent_graph_builds_exact_private_obligation_domain(
        self,
    ) -> None:
        _, validated = self._validated("slice-input-c-positive")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        domain = gated.obligation_domain_document_copy()

        self.assertEqual(gated.slice_input_status, "ELIGIBLE")
        self.assertEqual(gated.candidate_composition_status, "CONSISTENT")
        self.assertIsNotNone(domain)
        assert domain is not None
        facts = validated.fact_set_document_copy()["facts"]
        anchors = [item for item in facts if item["fact_kind"] == "MODULE"]
        self.assertEqual(len(anchors), 1)
        self.assertEqual(
            [item["anchor_fact_id"] for item in domain["obligations"]],
            [anchors[0]["fact_id"]],
        )
        spec = domain["obligations"][0]
        self.assertEqual(
            spec["slice_spec_digest"],
            semantic_digest(
                "veritrail.review.slice-spec/0.1",
                {
                    key: copy.deepcopy(value)
                    for key, value in spec.items()
                    if key != "slice_spec_digest"
                },
            ),
        )
        self.assertEqual(
            domain["slice_obligation_domain_digest"],
            semantic_digest(
                "veritrail.review.slice-obligation-domain/0.1",
                {
                    key: copy.deepcopy(value)
                    for key, value in domain.items()
                    if key not in {"policy_digest", "slice_obligation_domain_digest"}
                },
            ),
        )
        self.assertTrue(gated.continuation_permitted())

    def test_c_002_domain_claim_is_one_shot(self) -> None:
        _, validated = self._validated("slice-input-c-one-shot")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        self.assertTrue(gated.continuation_permitted())
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED,
            lambda: slice_input.construct_review_slice_obligation_domain(validated),
        )

    def test_c_003_concurrent_domain_claim_has_one_winner(self) -> None:
        _, validated = self._validated("slice-input-c-concurrent")
        barrier = Barrier(2)

        def construct():
            barrier.wait()
            try:
                gated = slice_input.construct_review_slice_obligation_domain(
                    validated
                )
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("DOMAIN", gated)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = [
                future.result()
                for future in (pool.submit(construct), pool.submit(construct))
            ]
        self.assertEqual(sorted(item[0] for item in outcomes), ["DOMAIN", "ERROR"])
        failure = next(item for item in outcomes if item[0] == "ERROR")
        success = next(item for item in outcomes if item[0] == "DOMAIN")
        self.assertIs(
            failure[1], _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED
        )
        self.assertTrue(success[1].continuation_permitted())

    def test_c_004_failed_domain_validation_consumes_claim(self) -> None:
        _, validated = self._validated("slice-input-c-failed-claim")
        original = validated.fact_set_document_bytes
        object.__setattr__(validated, "fact_set_document_bytes", b"{}")
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED,
            lambda: slice_input.construct_review_slice_obligation_domain(validated),
        )
        object.__setattr__(validated, "fact_set_document_bytes", original)
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED,
            lambda: slice_input.construct_review_slice_obligation_domain(validated),
        )

    def test_c_005_rs_006_conflict_blocks_without_empty_domain(self) -> None:
        _, validated = self._validated(
            "slice-input-c-conflict",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
        )
        gated = slice_input.construct_review_slice_obligation_domain(validated)

        self.assertEqual(
            gated.slice_input_status, "BLOCKED_BY_RELATION_CONFLICT"
        )
        self.assertEqual(gated.candidate_composition_status, "CONFLICTING")
        self.assertIsNone(gated.slice_obligation_domain_digest)
        self.assertIsNone(gated.obligation_domain_document_copy())
        self.assertIsNone(gated.obligations_copy())
        self.assertFalse(gated.continuation_permitted())
        self.assertGreater(
            len(validated.relation_set_document_copy()["conflicts"]), 0
        )

    def test_c_006_obligations_follow_profile_kind_rank_then_fact_id(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.support.two_import_inputs,
            ["MODULE", "IMPORT_DECLARATION"],
        )
        _, validated = self._validated(
            "slice-input-c-order",
            inputs=inputs,
            two_imports=True,
        )
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        obligations = gated.obligations_copy()
        self.assertIsNotNone(obligations)
        assert obligations is not None
        facts = validated.fact_set_document_copy()["facts"]
        rank = {
            item: index
            for index, item in enumerate(
                validated.derivation_profile_document_copy()["fact_kinds"]
            )
        }
        expected = sorted(
            [
                item
                for item in facts
                if item["fact_kind"] in {"MODULE", "IMPORT_DECLARATION"}
            ],
            key=lambda item: (rank[item["fact_kind"]], item["fact_id"]),
        )
        self.assertEqual(
            [item["anchor_fact_id"] for item in obligations],
            [item["fact_id"] for item in expected],
        )
        self.assertEqual(
            len({item["slice_spec_digest"] for item in obligations}),
            len(obligations),
        )

    def test_c_007_rs_016_zero_anchor_is_known_empty_domain(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        _, validated = self._validated("slice-input-c-zero-anchor", inputs=inputs)
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        domain = gated.obligation_domain_document_copy()

        self.assertEqual(gated.slice_input_status, "ELIGIBLE")
        self.assertIsNotNone(domain)
        assert domain is not None
        self.assertEqual(domain["obligations"], [])
        self.assertIsNotNone(gated.slice_obligation_domain_digest)
        self.assertTrue(gated.continuation_permitted())
        for forbidden in ("CLOSED_EMPTY", "coverage", "review_slice_set"):
            self.assertNotIn(forbidden, domain)

    def test_c_008_specs_copy_only_exact_sealed_policy_semantics(self) -> None:
        _, validated = self._validated("slice-input-c-policy-copy")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        obligations = gated.obligations_copy()
        self.assertIsNotNone(obligations)
        assert obligations is not None
        slice_policy = validated.review_policy_document_copy()["slice_policy"]
        for spec in obligations:
            for name in (
                "allowed_relations",
                "max_depth",
                "max_symbols",
                "max_files",
                "max_relations",
            ):
                self.assertEqual(spec[name], slice_policy[name])

    def test_c_009_original_budget_stop_rejects_domain(self) -> None:
        contexts: list[object] = []
        _, validated = self._validated(
            "slice-input-c-stopped",
            capture_context=contexts,
        )
        self.assertEqual(len(contexts), 1)
        contexts[0].request_cancellation()
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED,
            lambda: slice_input.construct_review_slice_obligation_domain(validated),
        )

    def test_c_010_surface_remains_private_and_nonpublishing(self) -> None:
        import veritrail_review

        name = "construct_review_slice_obligation_domain"
        self.assertFalse(hasattr(veritrail_review, name))
        self.assertNotIn(name, veritrail_review.__all__)
        parameters = inspect.signature(
            slice_input.construct_review_slice_obligation_domain
        ).parameters
        for forbidden in (
            "output_path",
            "output_directory",
            "publisher",
            "manifest",
            "review_slice_set",
            "coverage",
            "anchor",
        ):
            self.assertNotIn(forbidden, parameters)

    def test_c_011_owned_domain_seal_detects_post_construction_mutation(self) -> None:
        _, validated = self._validated("slice-input-c-owned-state")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        domain_values._validate_obligation_domain_gate(gated)
        object.__setattr__(gated, "obligation_domain_document_bytes", b"{}")
        with self.assertRaises(ValueError):
            domain_values._validate_obligation_domain_gate(gated)

    def test_c_012_same_domain_identity_does_not_share_attempt_authority(self) -> None:
        _, first_validated = self._validated("slice-input-c-identity-one")
        first = slice_input.construct_review_slice_obligation_domain(
            first_validated
        )

        policy = self.inputs.review_policy_document_copy()
        policy["governance"]["claim_owner_ref"] = "alternate-owner"
        _seal_policy(policy)
        second_inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=(
                self.inputs.source_snapshot_canonical_bytes
            ),
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=(
                self.inputs.derivation_profile_canonical_bytes
            ),
            verified_blob_bytes_by_object_identity=(
                self.inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=self.inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=self.inputs.derivation_profile_digest,
        )
        _, second_validated = self._validated(
            "slice-input-c-identity-two",
            inputs=second_inputs,
        )
        second = slice_input.construct_review_slice_obligation_domain(
            second_validated
        )

        self.assertNotEqual(first_validated.policy_digest, second_validated.policy_digest)
        self.assertNotEqual(
            first.admission_witness_digest, second.admission_witness_digest
        )
        self.assertEqual(
            first.slice_obligation_domain_digest,
            second.slice_obligation_domain_digest,
        )
        self.assertEqual(first.obligations_copy(), second.obligations_copy())
        self.assertNotEqual(
            first.obligation_domain_document_bytes,
            second.obligation_domain_document_bytes,
        )

    def test_d_001_exact_domain_forms_private_assignment_and_boundary(self) -> None:
        _, validated = self._validated("slice-input-d-positive")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gated
        )
        boundary = slice_input.claim_next_review_slice_traversal(assignments)
        request = boundary.traversal_request_copy()
        obligations = gated.obligations_copy()

        self.assertIsNotNone(obligations)
        assert obligations is not None
        self.assertEqual(assignments.assignment_count, len(obligations))
        self.assertEqual(assignments.remaining_assignment_count(), 0)
        self.assertEqual(boundary.assignment_ordinal, 0)
        self.assertEqual(
            boundary.slice_spec_digest,
            obligations[0]["slice_spec_digest"],
        )
        self.assertEqual(request["slice_spec"], obligations[0])
        self.assertEqual(
            request["traversal_rules"],
            validated.derivation_profile_document_copy()["traversal_rules"],
        )
        self.assertEqual(request["fact_set"], validated.fact_set_document_copy())
        self.assertEqual(
            request["relation_set"],
            validated.relation_set_document_copy(),
        )
        self.assertTrue(boundary.continuation_permitted())
        for forbidden in (
            "outcome_status",
            "frontier",
            "slice_id",
            "review_slice",
            "review_slice_set",
            "coverage",
        ):
            self.assertNotIn(forbidden, request)

    def test_d_002_assignment_construction_is_one_shot(self) -> None:
        _, validated = self._validated("slice-input-d-one-shot")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gated
        )
        self.assertTrue(assignments.continuation_permitted())
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED,
            lambda: slice_input.assign_review_slice_obligations_for_traversal(
                gated
            ),
        )

    def test_d_003_concurrent_single_assignment_has_one_winner(self) -> None:
        _, validated = self._validated("slice-input-d-concurrent")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gated
        )
        self.assertEqual(assignments.assignment_count, 1)
        barrier = Barrier(2)

        def claim():
            barrier.wait()
            try:
                boundary = slice_input.claim_next_review_slice_traversal(
                    assignments
                )
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("BOUNDARY", boundary)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = [
                future.result()
                for future in (pool.submit(claim), pool.submit(claim))
            ]
        self.assertEqual(
            sorted(item[0] for item in outcomes), ["BOUNDARY", "ERROR"]
        )
        failure = next(item for item in outcomes if item[0] == "ERROR")
        success = next(item for item in outcomes if item[0] == "BOUNDARY")
        self.assertIs(
            failure[1], _ReviewSliceInputFailureCode.TRAVERSAL_BOUNDARY_REJECTED
        )
        self.assertTrue(success[1].continuation_permitted())

    def test_d_004_failed_assignment_validation_consumes_the_claim(self) -> None:
        _, validated = self._validated("slice-input-d-failed-claim")
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        original = gated.obligation_domain_document_bytes
        object.__setattr__(gated, "obligation_domain_document_bytes", b"{}")
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED,
            lambda: slice_input.assign_review_slice_obligations_for_traversal(
                gated
            ),
        )
        object.__setattr__(gated, "obligation_domain_document_bytes", original)
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED,
            lambda: slice_input.assign_review_slice_obligations_for_traversal(
                gated
            ),
        )

    def test_d_005_assignments_follow_complete_domain_order(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.support.two_import_inputs,
            ["MODULE", "IMPORT_DECLARATION"],
        )
        _, validated = self._validated(
            "slice-input-d-order",
            inputs=inputs,
            two_imports=True,
        )
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gated
        )
        obligations = gated.obligations_copy()

        self.assertIsNotNone(obligations)
        assert obligations is not None
        boundaries = [
            slice_input.claim_next_review_slice_traversal(assignments)
            for _ in obligations
        ]
        self.assertEqual(
            [item.assignment_ordinal for item in boundaries],
            list(range(len(obligations))),
        )
        self.assertEqual(
            [item.slice_spec_digest for item in boundaries],
            [item["slice_spec_digest"] for item in obligations],
        )
        self.assertEqual(len(set(assignments.assignment_digests)), len(obligations))
        self.assertEqual(assignments.remaining_assignment_count(), 0)

    def test_d_006_caller_cannot_supply_spec_anchor_or_traversal_result(self) -> None:
        assignment_parameters = inspect.signature(
            slice_input.assign_review_slice_obligations_for_traversal
        ).parameters
        boundary_parameters = inspect.signature(
            slice_input.claim_next_review_slice_traversal
        ).parameters
        self.assertEqual(tuple(assignment_parameters), ("gate",))
        self.assertEqual(tuple(boundary_parameters), ("assignments",))
        for parameters in (assignment_parameters, boundary_parameters):
            for forbidden in (
                "spec",
                "anchor",
                "outcome",
                "frontier",
                "slice",
                "budget",
            ):
                self.assertNotIn(forbidden, parameters)

    def test_d_007_zero_domain_has_no_assignments_or_closed_empty_claim(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        _, validated = self._validated("slice-input-d-zero-domain", inputs=inputs)
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gated
        )

        self.assertEqual(assignments.assignment_count, 0)
        self.assertEqual(assignments.assignment_digests, ())
        self.assertEqual(assignments.remaining_assignment_count(), 0)
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.TRAVERSAL_BOUNDARY_REJECTED,
            lambda: slice_input.claim_next_review_slice_traversal(assignments),
        )
        for value in vars(assignments).values():
            self.assertNotEqual(value, "CLOSED_EMPTY")

    def test_d_008_conflict_gate_cannot_form_assignments(self) -> None:
        _, validated = self._validated(
            "slice-input-d-conflict",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
        )
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        self.assertEqual(
            gated.slice_input_status, "BLOCKED_BY_RELATION_CONFLICT"
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED,
            lambda: slice_input.assign_review_slice_obligations_for_traversal(
                gated
            ),
        )

    def test_d_009_original_budget_stop_rejects_traversal_boundary(self) -> None:
        contexts: list[object] = []
        _, validated = self._validated(
            "slice-input-d-stopped",
            capture_context=contexts,
        )
        gated = slice_input.construct_review_slice_obligation_domain(validated)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gated
        )
        self.assertEqual(len(contexts), 1)
        contexts[0].request_cancellation()
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.TRAVERSAL_BOUNDARY_REJECTED,
            lambda: slice_input.claim_next_review_slice_traversal(assignments),
        )

    def test_d_010_same_domain_does_not_share_assignment_authority(self) -> None:
        _, first_validated = self._validated("slice-input-d-attempt-one")
        first_gate = slice_input.construct_review_slice_obligation_domain(
            first_validated
        )
        first = slice_input.assign_review_slice_obligations_for_traversal(
            first_gate
        )

        _, second_validated = self._validated("slice-input-d-attempt-two")
        second_gate = slice_input.construct_review_slice_obligation_domain(
            second_validated
        )
        second = slice_input.assign_review_slice_obligations_for_traversal(
            second_gate
        )

        self.assertEqual(
            first.slice_obligation_domain_digest,
            second.slice_obligation_domain_digest,
        )
        self.assertNotEqual(first.derivation_id, second.derivation_id)
        self.assertNotEqual(
            first.admission_witness_digest,
            second.admission_witness_digest,
        )
        self.assertNotEqual(first.assignment_digests, second.assignment_digests)

    def test_d_011_owned_state_seals_detect_mutation(self) -> None:
        _, first_validated = self._validated("slice-input-d-assignment-seal")
        first_gate = slice_input.construct_review_slice_obligation_domain(
            first_validated
        )
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            first_gate
        )
        assignment_values._validate_traversal_assignments(assignments)
        object.__setattr__(assignments, "assignment_digests", ("0" * 64,))
        with self.assertRaises(ValueError):
            assignment_values._validate_traversal_assignments(assignments)

        _, second_validated = self._validated("slice-input-d-boundary-seal")
        second_gate = slice_input.construct_review_slice_obligation_domain(
            second_validated
        )
        second_assignments = (
            slice_input.assign_review_slice_obligations_for_traversal(second_gate)
        )
        boundary = slice_input.claim_next_review_slice_traversal(
            second_assignments
        )
        assignment_values._validate_traversal_boundary(boundary)
        object.__setattr__(boundary, "traversal_request_bytes", b"{}")
        with self.assertRaises(ValueError):
            assignment_values._validate_traversal_boundary(boundary)

    def test_d_012_surface_remains_private_and_nonpublishing(self) -> None:
        import veritrail_review

        names = (
            "assign_review_slice_obligations_for_traversal",
            "claim_next_review_slice_traversal",
        )
        for name in names:
            self.assertFalse(hasattr(veritrail_review, name))
            self.assertNotIn(name, veritrail_review.__all__)
        for callback in (
            slice_input.assign_review_slice_obligations_for_traversal,
            slice_input.claim_next_review_slice_traversal,
        ):
            parameters = inspect.signature(callback).parameters
            for forbidden in (
                "output_path",
                "output_directory",
                "publisher",
                "manifest",
                "review_slice_set",
                "coverage",
            ):
                self.assertNotIn(forbidden, parameters)

    def test_e_001_depth_bound_forms_partial_with_structural_frontier(self) -> None:
        boundary = self._boundary("slice-input-e-depth-frontier")
        outcome = slice_input.derive_review_slice_traversal_outcome(boundary)
        candidate = outcome.normal_slice_candidate_copy()
        request = boundary.traversal_request_copy()
        import_relation = next(
            item
            for item in request["relation_set"]["relations"]
            if item["relation_kind"] == "IMPORT_TARGET_LITERAL"
        )

        self.assertEqual(outcome.outcome_status, "NORMAL_PARTIAL")
        self.assertEqual(candidate["coverage_status"], "PARTIAL")
        self.assertEqual(len(candidate["frontier"]), 1)
        self.assertEqual(
            candidate["frontier"][0],
            {
                "from_fact_id": import_relation["source_fact_id"],
                "relation_id": import_relation["relation_id"],
                "direction": "OUTBOUND",
                "candidate_fact_id": None,
                "candidate_depth": 2,
                "reason_codes": ["DEPTH_LIMIT"],
            },
        )
        self.assertNotIn(
            import_relation["relation_id"], candidate["included_relation_ids"]
        )

    def test_e_002_larger_depth_bound_forms_complete_normal_slice(self) -> None:
        inputs = self._inputs_with_slice_limits(self.inputs, max_depth=2)
        boundary = self._boundary("slice-input-e-complete", inputs=inputs)
        outcome = slice_input.derive_review_slice_traversal_outcome(boundary)
        candidate = outcome.normal_slice_candidate_copy()
        request = boundary.traversal_request_copy()

        self.assertEqual(outcome.outcome_status, "NORMAL_COMPLETE")
        self.assertEqual(candidate["coverage_status"], "COMPLETE")
        self.assertEqual(candidate["frontier"], [])
        self.assertEqual(
            candidate["included_fact_ids"],
            sorted(item["fact_id"] for item in request["fact_set"]["facts"]),
        )
        self.assertEqual(
            candidate["included_relation_ids"],
            sorted(
                item["relation_id"]
                for item in request["relation_set"]["relations"]
            ),
        )

    def test_e_003_outcome_claim_is_one_shot_and_concurrent_safe(self) -> None:
        boundary = self._boundary("slice-input-e-concurrent")
        barrier = Barrier(2)

        def derive():
            barrier.wait()
            try:
                value = slice_input.derive_review_slice_traversal_outcome(
                    boundary
                )
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("OUTCOME", value)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = [
                future.result()
                for future in (pool.submit(derive), pool.submit(derive))
            ]
        self.assertEqual(
            sorted(item[0] for item in results), ["ERROR", "OUTCOME"]
        )
        failure = next(item for item in results if item[0] == "ERROR")
        self.assertIs(
            failure[1], _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED
        )

    def test_e_004_failed_boundary_validation_consumes_outcome_claim(self) -> None:
        boundary = self._boundary("slice-input-e-failed-claim")
        original = boundary.traversal_request_bytes
        object.__setattr__(boundary, "traversal_request_bytes", b"{}")
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED,
            lambda: slice_input.derive_review_slice_traversal_outcome(boundary),
        )
        object.__setattr__(boundary, "traversal_request_bytes", original)
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED,
            lambda: slice_input.derive_review_slice_traversal_outcome(boundary),
        )

    def test_e_005_atomic_rejection_records_every_applicable_limit(self) -> None:
        inputs = self._inputs_with_slice_limits(
            self.inputs,
            max_depth=0,
            max_symbols=1,
            max_relations=0,
        )
        boundary = self._boundary("slice-input-e-limit-union", inputs=inputs)
        outcome = slice_input.derive_review_slice_traversal_outcome(boundary)
        candidate = outcome.normal_slice_candidate_copy()
        spec = boundary.traversal_request_copy()["slice_spec"]

        self.assertEqual(candidate["included_fact_ids"], [spec["anchor_fact_id"]])
        self.assertEqual(candidate["included_relation_ids"], [])
        self.assertEqual(len(candidate["frontier"]), 1)
        self.assertEqual(
            candidate["frontier"][0]["reason_codes"],
            ["DEPTH_LIMIT", "SYMBOL_LIMIT", "RELATION_LIMIT"],
        )

    def test_e_006_original_budget_stop_cannot_leave_normal_prefix(self) -> None:
        contexts: list[object] = []
        boundary = self._boundary(
            "slice-input-e-stopped", capture_context=contexts
        )
        self.assertEqual(len(contexts), 1)
        contexts[0].request_cancellation()
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED,
            lambda: slice_input.derive_review_slice_traversal_outcome(boundary),
        )

    def test_e_007_content_can_repeat_but_outcome_authority_cannot(self) -> None:
        first = slice_input.derive_review_slice_traversal_outcome(
            self._boundary("slice-input-e-attempt-one")
        )
        second = slice_input.derive_review_slice_traversal_outcome(
            self._boundary("slice-input-e-attempt-two")
        )

        self.assertEqual(
            first.normal_slice_candidate_copy(),
            second.normal_slice_candidate_copy(),
        )
        self.assertNotEqual(first.derivation_id, second.derivation_id)
        self.assertNotEqual(
            first.admission_witness_digest,
            second.admission_witness_digest,
        )
        self.assertNotEqual(
            first.traversal_outcome_digest,
            second.traversal_outcome_digest,
        )

    def test_e_008_owned_outcome_is_private_sealed_and_nonpublishing(self) -> None:
        import veritrail_review

        boundary = self._boundary("slice-input-e-owned-state")
        outcome = slice_input.derive_review_slice_traversal_outcome(boundary)
        outcome_values._validate_traversal_outcome(outcome)
        object.__setattr__(outcome, "outcome_document_bytes", b"{}")
        with self.assertRaises(ValueError):
            outcome_values._validate_traversal_outcome(outcome)

        name = "derive_review_slice_traversal_outcome"
        self.assertFalse(hasattr(veritrail_review, name))
        self.assertNotIn(name, veritrail_review.__all__)
        parameters = inspect.signature(
            slice_input.derive_review_slice_traversal_outcome
        ).parameters
        self.assertEqual(tuple(parameters), ("boundary",))
        for forbidden in (
            "spec",
            "anchor",
            "outcome",
            "frontier",
            "budget",
            "output_path",
            "publisher",
            "review_slice_set",
            "coverage",
        ):
            self.assertNotIn(forbidden, parameters)

    def test_e_009_disallowed_graph_edges_do_not_expand_or_block(self) -> None:
        inputs = self._inputs_with_allowed_relations(
            self.inputs,
            [
                {
                    "direction": "OUTBOUND",
                    "relation_kind": "LEXICAL_CONTAINS",
                }
            ],
        )
        boundary = self._boundary("slice-input-e-allowed-subset", inputs=inputs)
        outcome = slice_input.derive_review_slice_traversal_outcome(boundary)
        candidate = outcome.normal_slice_candidate_copy()
        relation_set = boundary.traversal_request_copy()["relation_set"]
        lexical = next(
            item
            for item in relation_set["relations"]
            if item["relation_kind"] == "LEXICAL_CONTAINS"
        )

        self.assertEqual(outcome.outcome_status, "NORMAL_COMPLETE")
        self.assertEqual(candidate["frontier"], [])
        self.assertEqual(
            candidate["included_relation_ids"], [lexical["relation_id"]]
        )

    def test_f_001_multi_obligation_outcomes_close_in_domain_order(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.support.two_import_inputs,
            ["MODULE", "IMPORT_DECLARATION"],
        )
        assignments = self._assignments(
            "slice-input-f-positive",
            inputs=inputs,
            two_imports=True,
        )
        self.assertEqual(assignments.assignment_count, 3)
        outcomes = self._normal_outcomes(assignments)

        closure = slice_input.reconcile_review_slice_traversal_outcomes(
            assignments,
            tuple(reversed(outcomes)),
        )
        document = closure.closure_document_copy()

        self.assertEqual(closure.closure_status, "NORMAL_CLOSED")
        self.assertEqual(
            [item["assignment_ordinal"] for item in document["traversal_outcomes"]],
            [0, 1, 2],
        )
        self.assertEqual(
            closure.normal_slice_candidates_copy(),
            [item.normal_slice_candidate_copy() for item in outcomes],
        )
        self.assertEqual(
            closure.slice_obligation_domain_digest,
            assignments.slice_obligation_domain_digest,
        )

    def test_f_002_missing_outcome_rejects_and_consumes_claim(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.support.two_import_inputs,
            ["MODULE", "IMPORT_DECLARATION"],
        )
        assignments = self._assignments(
            "slice-input-f-missing",
            inputs=inputs,
            two_imports=True,
        )
        outcomes = self._normal_outcomes(assignments)

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                assignments, outcomes[:-1]
            ),
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                assignments, outcomes
            ),
        )

    def test_f_003_duplicate_outcome_is_not_two_fulfillments(self) -> None:
        assignments = self._assignments("slice-input-f-duplicate")
        outcomes = self._normal_outcomes(assignments)
        duplicated = (outcomes[0], outcomes[0])

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                assignments, duplicated
            ),
        )

    def test_f_004_cross_attempt_outcome_cannot_close_domain(self) -> None:
        first = self._assignments("slice-input-f-cross-attempt-one")
        second = self._assignments("slice-input-f-cross-attempt-two")
        foreign = self._normal_outcomes(second)

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                first, foreign
            ),
        )

    def test_f_005_dangling_outcome_coordinate_is_rejected(self) -> None:
        assignments = self._assignments("slice-input-f-dangling")
        outcomes = self._normal_outcomes(assignments)
        object.__setattr__(
            outcomes[0],
            "assignment_ordinal",
            assignments.assignment_count,
        )

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                assignments, outcomes
            ),
        )

    def test_f_006_reconciliation_claim_is_one_shot_and_concurrent(self) -> None:
        assignments = self._assignments("slice-input-f-concurrent")
        outcomes = self._normal_outcomes(assignments)
        barrier = Barrier(2)

        def reconcile():
            barrier.wait()
            try:
                value = slice_input.reconcile_review_slice_traversal_outcomes(
                    assignments, outcomes
                )
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("CLOSURE", value)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = [
                future.result()
                for future in (
                    pool.submit(reconcile),
                    pool.submit(reconcile),
                )
            ]
        self.assertEqual(
            sorted(item[0] for item in results), ["CLOSURE", "ERROR"]
        )
        failure = next(item for item in results if item[0] == "ERROR")
        self.assertIs(
            failure[1],
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
        )

    def test_f_007_original_budget_stop_cannot_form_closure(self) -> None:
        contexts: list[object] = []
        assignments = self._assignments(
            "slice-input-f-stopped",
            capture_context=contexts,
        )
        outcomes = self._normal_outcomes(assignments)
        self.assertEqual(len(contexts), 1)
        contexts[0].request_cancellation()

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                assignments, outcomes
            ),
        )

    def test_f_008_zero_domain_does_not_gain_closed_empty_authority(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        assignments = self._assignments(
            "slice-input-f-zero-domain",
            inputs=inputs,
        )
        self.assertEqual(assignments.assignment_count, 0)

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                assignments, ()
            ),
        )
        for value in vars(assignments).values():
            self.assertNotEqual(value, "CLOSED_EMPTY")

    def test_f_009_same_content_does_not_share_closure_authority(self) -> None:
        first_assignments = self._assignments("slice-input-f-attempt-one")
        first = slice_input.reconcile_review_slice_traversal_outcomes(
            first_assignments,
            self._normal_outcomes(first_assignments),
        )
        second_assignments = self._assignments("slice-input-f-attempt-two")
        second = slice_input.reconcile_review_slice_traversal_outcomes(
            second_assignments,
            self._normal_outcomes(second_assignments),
        )

        self.assertEqual(
            first.normal_slice_candidates_copy(),
            second.normal_slice_candidates_copy(),
        )
        self.assertNotEqual(first.derivation_id, second.derivation_id)
        self.assertNotEqual(
            first.admission_witness_digest,
            second.admission_witness_digest,
        )
        self.assertNotEqual(
            first.slice_obligation_closure_digest,
            second.slice_obligation_closure_digest,
        )

    def test_f_010_closure_is_private_sealed_and_nonpublishing(self) -> None:
        import veritrail_review

        assignments = self._assignments("slice-input-f-private")
        closure = slice_input.reconcile_review_slice_traversal_outcomes(
            assignments,
            self._normal_outcomes(assignments),
        )
        closure_values._validate_slice_obligation_closure(closure)
        object.__setattr__(closure, "closure_document_bytes", b"{}")
        with self.assertRaises(ValueError):
            closure_values._validate_slice_obligation_closure(closure)

        name = "reconcile_review_slice_traversal_outcomes"
        self.assertFalse(hasattr(veritrail_review, name))
        self.assertNotIn(name, veritrail_review.__all__)
        parameters = inspect.signature(
            slice_input.reconcile_review_slice_traversal_outcomes
        ).parameters
        self.assertEqual(tuple(parameters), ("assignments", "outcomes"))
        for forbidden in (
            "output_path",
            "publisher",
            "review_slice_set",
            "coverage",
            "manifest",
        ):
            self.assertNotIn(forbidden, parameters)

    def test_g_001_rs_005_exact_zero_anchor_domain_closes_empty(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        assignments = self._assignments(
            "slice-input-g-closed-empty",
            inputs=inputs,
        )

        closure = slice_input.close_empty_review_slice_obligation_domain(
            assignments
        )
        document = closure.closure_document_copy()

        self.assertEqual(closure.closure_status, "CLOSED_EMPTY")
        self.assertEqual(document["traversal_outcomes"], [])
        self.assertEqual(document["normal_slice_candidates"], [])
        self.assertEqual(assignments.assignment_count, 0)
        self.assertEqual(
            closure.slice_obligation_domain_digest,
            assignments.slice_obligation_domain_digest,
        )
        empty_values._validate_empty_domain_closure(closure)
        object.__setattr__(closure, "closure_document_bytes", b"{}")
        with self.assertRaises(ValueError):
            empty_values._validate_empty_domain_closure(closure)

    def test_g_002_nonempty_domain_cannot_use_closed_empty_path(self) -> None:
        assignments = self._assignments("slice-input-g-not-empty")

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED,
            lambda: slice_input.close_empty_review_slice_obligation_domain(
                assignments
            ),
        )
        outcomes = self._normal_outcomes(assignments)
        closure = slice_input.reconcile_review_slice_traversal_outcomes(
            assignments,
            outcomes,
        )
        self.assertEqual(closure.closure_status, "NORMAL_CLOSED")

    def test_g_003_closed_empty_claim_is_one_shot_and_concurrent(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        assignments = self._assignments(
            "slice-input-g-empty-concurrent",
            inputs=inputs,
        )
        barrier = Barrier(2)

        def close():
            barrier.wait()
            try:
                value = slice_input.close_empty_review_slice_obligation_domain(
                    assignments
                )
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("CLOSURE", value)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = [
                future.result()
                for future in (pool.submit(close), pool.submit(close))
            ]
        self.assertEqual(
            sorted(item[0] for item in results), ["CLOSURE", "ERROR"]
        )
        failure = next(item for item in results if item[0] == "ERROR")
        self.assertIs(
            failure[1],
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED,
        )

    def test_g_004_stopped_budget_cannot_form_closed_empty(self) -> None:
        contexts: list[object] = []
        inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        assignments = self._assignments(
            "slice-input-g-empty-stopped",
            inputs=inputs,
            capture_context=contexts,
        )
        self.assertEqual(len(contexts), 1)
        contexts[0].request_cancellation()

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED,
            lambda: slice_input.close_empty_review_slice_obligation_domain(
                assignments
            ),
        )

    def test_g_005_same_empty_domain_does_not_share_attempt_receipt(self) -> None:
        inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        first_assignments = self._assignments(
            "slice-input-g-empty-one",
            inputs=inputs,
        )
        second_assignments = self._assignments(
            "slice-input-g-empty-two",
            inputs=inputs,
        )
        first = slice_input.close_empty_review_slice_obligation_domain(
            first_assignments
        )
        second = slice_input.close_empty_review_slice_obligation_domain(
            second_assignments
        )

        self.assertEqual(
            first.slice_obligation_domain_digest,
            second.slice_obligation_domain_digest,
        )
        self.assertNotEqual(first.derivation_id, second.derivation_id)
        self.assertNotEqual(
            first.admission_witness_digest,
            second.admission_witness_digest,
        )
        self.assertNotEqual(
            first.empty_domain_closure_digest,
            second.empty_domain_closure_digest,
        )

    def test_g_006_conflict_forms_unknown_denominator_receipt(self) -> None:
        _, validated = self._validated(
            "slice-input-g-conflict",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
        )
        gate = slice_input.construct_review_slice_obligation_domain(validated)

        receipt = slice_input.record_blocked_review_slice_input(gate)
        document = receipt.receipt_document_copy()
        relation_set = validated.relation_set_document_copy()

        self.assertEqual(receipt.receipt_status, "BLOCKED_BY_RELATION_CONFLICT")
        self.assertEqual(
            document["slice_derivation_denominator_status"], "UNKNOWN"
        )
        self.assertEqual(
            receipt.reason_codes_copy(),
            ["PROVIDER_CONFLICT", "UPSTREAM_DENOMINATOR_UNKNOWN"],
        )
        self.assertIsNone(document["slice_obligation_domain_digest"])
        self.assertEqual(document["normal_slice_candidates"], [])
        self.assertEqual(
            document["relation_conflict_ids"],
            [item["conflict_id"] for item in relation_set["conflicts"]],
        )
        blocked_values._validate_blocked_input_receipt(receipt)

    def test_g_007_blocked_receipt_claim_is_one_shot_and_concurrent(self) -> None:
        _, validated = self._validated(
            "slice-input-g-conflict-concurrent",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
        )
        gate = slice_input.construct_review_slice_obligation_domain(validated)
        barrier = Barrier(2)

        def close():
            barrier.wait()
            try:
                value = slice_input.record_blocked_review_slice_input(gate)
            except _ReviewSliceInputError as exc:
                return ("ERROR", exc.code)
            return ("RECEIPT", value)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = [
                future.result()
                for future in (pool.submit(close), pool.submit(close))
            ]
        self.assertEqual(sorted(item[0] for item in results), ["ERROR", "RECEIPT"])
        failure = next(item for item in results if item[0] == "ERROR")
        self.assertIs(
            failure[1],
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED,
        )

    def test_g_008_consistent_gate_cannot_claim_blocked_receipt(self) -> None:
        _, validated = self._validated("slice-input-g-not-conflicting")
        gate = slice_input.construct_review_slice_obligation_domain(validated)

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED,
            lambda: slice_input.record_blocked_review_slice_input(gate),
        )
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gate
        )
        closure = slice_input.reconcile_review_slice_traversal_outcomes(
            assignments,
            self._normal_outcomes(assignments),
        )
        self.assertEqual(closure.closure_status, "NORMAL_CLOSED")

    def test_g_009_conflict_cannot_form_assignments_or_closed_empty(self) -> None:
        _, validated = self._validated(
            "slice-input-g-conflict-not-empty",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
        )
        gate = slice_input.construct_review_slice_obligation_domain(validated)

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED,
            lambda: slice_input.assign_review_slice_obligations_for_traversal(gate),
        )
        self.assertIsNone(gate.obligations_copy())
        self.assertIsNone(gate.slice_obligation_domain_digest)

    def test_g_010_blocked_receipt_is_private_sealed_and_nonpublishing(self) -> None:
        import veritrail_review

        _, validated = self._validated(
            "slice-input-g-conflict-private",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
        )
        gate = slice_input.construct_review_slice_obligation_domain(validated)
        receipt = slice_input.record_blocked_review_slice_input(gate)
        blocked_values._validate_blocked_input_receipt(receipt)
        object.__setattr__(receipt, "receipt_document_bytes", b"{}")
        with self.assertRaises(ValueError):
            blocked_values._validate_blocked_input_receipt(receipt)

        for name in (
            "close_empty_review_slice_obligation_domain",
            "record_blocked_review_slice_input",
        ):
            self.assertFalse(hasattr(veritrail_review, name))
            self.assertNotIn(name, veritrail_review.__all__)
        for callback in (
            slice_input.close_empty_review_slice_obligation_domain,
            slice_input.record_blocked_review_slice_input,
        ):
            for forbidden in (
                "output_path",
                "publisher",
                "review_slice_set",
                "coverage",
                "manifest",
            ):
                self.assertNotIn(forbidden, inspect.signature(callback).parameters)

    def test_g_011_same_conflict_content_does_not_share_attempt_receipt(self) -> None:
        receipts = []
        for derivation_id in (
            "slice-input-g-conflict-one",
            "slice-input-g-conflict-two",
        ):
            _, validated = self._validated(
                derivation_id,
                inputs=self.support.two_import_inputs,
                relation_launch_key="observation-b-conflict",
                two_imports=True,
            )
            gate = slice_input.construct_review_slice_obligation_domain(validated)
            receipts.append(slice_input.record_blocked_review_slice_input(gate))

        self.assertEqual(
            receipts[0].receipt_document_copy()["relation_conflict_ids"],
            receipts[1].receipt_document_copy()["relation_conflict_ids"],
        )
        self.assertNotEqual(receipts[0].derivation_id, receipts[1].derivation_id)
        self.assertNotEqual(
            receipts[0].admission_witness_digest,
            receipts[1].admission_witness_digest,
        )
        self.assertNotEqual(
            receipts[0].blocked_input_receipt_digest,
            receipts[1].blocked_input_receipt_digest,
        )

    def test_g_012_not_qualified_world_cannot_enter_slice_negative_path(self) -> None:
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE,
            lambda: self._run(
                "slice-input-g-not-qualified",
                relation_launch_key="observation-a-unavailable",
            ),
        )

    def test_g_013_stopped_budget_cannot_form_blocked_receipt(self) -> None:
        contexts: list[object] = []
        _, validated = self._validated(
            "slice-input-g-conflict-stopped",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
            capture_context=contexts,
        )
        gate = slice_input.construct_review_slice_obligation_domain(validated)
        self.assertEqual(len(contexts), 1)
        contexts[0].request_cancellation()

        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED,
            lambda: slice_input.record_blocked_review_slice_input(gate),
        )

    def test_h_001_rs_010_fresh_budget_with_equal_limits_is_not_same_attempt(
        self,
    ) -> None:
        preclaim_contexts: list[object] = []
        preclaim = self._run(
            "slice-input-h-fresh-budget-preclaim",
            capture_context=preclaim_contexts,
        )
        preclaim_continuation = getattr(
            preclaim,
            "_OwnedRelationQualificationContinuation__continuation",
        )
        preclaim_fresh = BudgetContext._admit_for_testing(
            preclaim_contexts[0].limits
        )
        object.__setattr__(
            preclaim_continuation,
            "_SameAttemptSliceContinuation__context",
            preclaim_fresh,
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED,
            lambda: slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                preclaim
            ),
        )

        contexts: list[object] = []
        qualified = self._run(
            "slice-input-h-fresh-budget",
            capture_context=contexts,
        )
        authority = (
            slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                qualified
            )
        )
        joined = slice_input.claim_admitted_graph_slice_input(
            self.inputs, authority
        )
        self.assertEqual(len(contexts), 1)
        original = contexts[0]
        fresh = BudgetContext._admit_for_testing(original.limits)
        self.assertIsNot(fresh, original)
        self.assertEqual(fresh.limits, original.limits)

        object.__setattr__(
            joined._continuation,
            "_ClaimedSliceContinuation__context",
            fresh,
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED,
            lambda: slice_input.cross_validate_admitted_graph_slice_input(
                joined
            ),
        )

    def test_h_002_rs_008_mid_traversal_stop_leaves_no_normal_prefix(
        self,
    ) -> None:
        contexts: list[object] = []
        boundary = self._boundary(
            "slice-input-h-mid-traversal-stop",
            capture_context=contexts,
        )
        self.assertEqual(len(contexts), 1)
        original = traversal._relation_candidates
        stopped = False

        def stop_after_candidate_discovery(*args, **kwargs):
            nonlocal stopped
            candidates = original(*args, **kwargs)
            if candidates and not stopped:
                stopped = True
                contexts[0].request_cancellation()
            return candidates

        with mock.patch.object(
            traversal,
            "_relation_candidates",
            side_effect=stop_after_candidate_discovery,
        ):
            self.assertJoinFailure(
                _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED,
                lambda: slice_input.derive_review_slice_traversal_outcome(
                    boundary
                ),
            )
        self.assertTrue(stopped)
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED,
            lambda: slice_input.derive_review_slice_traversal_outcome(boundary),
        )

    def test_h_003_rs_013_partial_frontier_cannot_self_report_complete(
        self,
    ) -> None:
        outcome = slice_input.derive_review_slice_traversal_outcome(
            self._boundary("slice-input-h-status-frontier")
        )
        document = outcome.outcome_document_copy()
        self.assertTrue(document["normal_slice_candidate"]["frontier"])
        document["outcome_status"] = "NORMAL_COMPLETE"
        document["traversal_outcome_digest"] = semantic_digest(
            "veritrail.review.private-slice-traversal-outcome/0.1",
            {
                key: copy.deepcopy(value)
                for key, value in document.items()
                if key != "traversal_outcome_digest"
            },
        )
        raw = canonical_json_bytes(document)
        object.__setattr__(outcome, "outcome_status", "NORMAL_COMPLETE")
        object.__setattr__(
            outcome,
            "traversal_outcome_digest",
            document["traversal_outcome_digest"],
        )
        object.__setattr__(outcome, "outcome_document_bytes", raw)
        values = {
            "derivation_id": outcome.derivation_id,
            "admission_witness_digest": outcome.admission_witness_digest,
            "slice_obligation_domain_digest": (
                outcome.slice_obligation_domain_digest
            ),
            "assignment_ordinal": outcome.assignment_ordinal,
            "assignment_digest": outcome.assignment_digest,
            "slice_spec_digest": outcome.slice_spec_digest,
            "outcome_status": outcome.outcome_status,
            "traversal_outcome_digest": outcome.traversal_outcome_digest,
            "outcome_document_bytes": outcome.outcome_document_bytes,
            "_boundary": outcome._boundary,
        }
        object.__setattr__(
            outcome,
            "_state_seal",
            outcome_values._private_state_seal(values),
        )

        with self.assertRaises(ValueError):
            outcome_values._validate_traversal_outcome(outcome)

    def test_h_004_rs_014_graph_external_membership_fails_reconciliation(
        self,
    ) -> None:
        assignments = self._assignments("slice-input-h-membership")
        boundary = slice_input.claim_next_review_slice_traversal(assignments)
        candidate = traversal._derive_normal_review_slice_candidate(boundary)
        graph_external_fact_id = "f" * 64
        self.assertNotIn(
            graph_external_fact_id,
            [
                item["fact_id"]
                for item in boundary.traversal_request_copy()["fact_set"][
                    "facts"
                ]
            ],
        )
        candidate["included_fact_ids"] = sorted(
            candidate["included_fact_ids"] + [graph_external_fact_id]
        )
        candidate["slice_id"] = semantic_digest(
            "veritrail.review.review-slice/0.1",
            {
                "slice_spec_digest": boundary.slice_spec_digest,
                "included_fact_ids": candidate["included_fact_ids"],
                "included_relation_ids": candidate["included_relation_ids"],
                "frontier": copy.deepcopy(candidate["frontier"]),
            },
        )
        with mock.patch.object(
            slice_input,
            "_derive_normal_review_slice_candidate",
            return_value=candidate,
        ):
            outcome = slice_input.derive_review_slice_traversal_outcome(
                boundary
            )
        self.assertIn(
            graph_external_fact_id,
            outcome.normal_slice_candidate_copy()["included_fact_ids"],
        )
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED,
            lambda: slice_input.reconcile_review_slice_traversal_outcomes(
                assignments, (outcome,)
            ),
        )

    def test_h_005_rs_015_closure_receipt_cannot_move_between_attempts(
        self,
    ) -> None:
        first_assignments = self._assignments("slice-input-h-receipt-one")
        first = slice_input.reconcile_review_slice_traversal_outcomes(
            first_assignments,
            self._normal_outcomes(first_assignments),
        )
        second_assignments = self._assignments("slice-input-h-receipt-two")
        second = slice_input.reconcile_review_slice_traversal_outcomes(
            second_assignments,
            self._normal_outcomes(second_assignments),
        )
        self.assertEqual(
            first.normal_slice_candidates_copy(),
            second.normal_slice_candidates_copy(),
        )
        transplanted_values = {
            "derivation_id": first.derivation_id,
            "admission_witness_digest": first.admission_witness_digest,
            "slice_obligation_domain_digest": (
                first.slice_obligation_domain_digest
            ),
            "closure_status": first.closure_status,
            "slice_obligation_closure_digest": (
                first.slice_obligation_closure_digest
            ),
            "closure_document_bytes": first.closure_document_bytes,
            "_assignments": second._assignments,
            "_outcomes": first._outcomes,
            "_committed_phase": first._committed_phase,
        }
        transplanted = replace(
            second,
            **transplanted_values,
            _state_seal=closure_values._private_state_seal(
                transplanted_values
            ),
        )

        with self.assertRaises(ValueError):
            closure_values._validate_slice_obligation_closure(transplanted)

    def test_h_006_rs_016_caller_cannot_supply_empty_denominator(self) -> None:
        _, validated = self._validated("slice-input-h-no-caller-domain")
        self.assertEqual(
            tuple(
                inspect.signature(
                    slice_input.construct_review_slice_obligation_domain
                ).parameters
            ),
            ("validated",),
        )
        gate = slice_input.construct_review_slice_obligation_domain(validated)
        obligations = gate.obligations_copy()
        self.assertIsNotNone(obligations)
        self.assertGreater(len(obligations), 0)
        assignments = slice_input.assign_review_slice_obligations_for_traversal(
            gate
        )
        self.assertGreater(assignments.assignment_count, 0)
        self.assertJoinFailure(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED,
            lambda: slice_input.close_empty_review_slice_obligation_domain(
                assignments
            ),
        )

    def test_h_007_cross_runtime_golden_private_closure_identities(self) -> None:
        def identity(raw: bytes, digest: str) -> dict[str, str]:
            return {
                "semantic_digest": digest,
                "canonical_sha256": hashlib.sha256(raw).hexdigest(),
            }

        partial_assignments = self._assignments(
            "slice-input-h-golden-partial"
        )
        partial_outcomes = self._normal_outcomes(partial_assignments)
        partial_closure = slice_input.reconcile_review_slice_traversal_outcomes(
            partial_assignments,
            partial_outcomes,
        )

        complete_inputs = self._inputs_with_slice_limits(
            self.inputs,
            max_depth=2,
        )
        complete_assignments = self._assignments(
            "slice-input-h-golden-complete",
            inputs=complete_inputs,
        )
        complete_outcomes = self._normal_outcomes(complete_assignments)
        complete_closure = slice_input.reconcile_review_slice_traversal_outcomes(
            complete_assignments,
            complete_outcomes,
        )

        empty_inputs = self._inputs_with_anchor_fact_kinds(
            self.inputs,
            ["CLASS_DECLARATION"],
        )
        empty_assignments = self._assignments(
            "slice-input-h-golden-empty",
            inputs=empty_inputs,
        )
        empty_closure = slice_input.close_empty_review_slice_obligation_domain(
            empty_assignments
        )

        _, conflict_validated = self._validated(
            "slice-input-h-golden-conflict",
            inputs=self.support.two_import_inputs,
            relation_launch_key="observation-b-conflict",
            two_imports=True,
        )
        conflict_gate = slice_input.construct_review_slice_obligation_domain(
            conflict_validated
        )
        blocked = slice_input.record_blocked_review_slice_input(conflict_gate)

        summary = {
            "normal_partial_outcome": identity(
                partial_outcomes[0].outcome_document_bytes,
                partial_outcomes[0].traversal_outcome_digest,
            ),
            "normal_partial_closure": identity(
                partial_closure.closure_document_bytes,
                partial_closure.slice_obligation_closure_digest,
            ),
            "normal_complete_outcome": identity(
                complete_outcomes[0].outcome_document_bytes,
                complete_outcomes[0].traversal_outcome_digest,
            ),
            "normal_complete_closure": identity(
                complete_closure.closure_document_bytes,
                complete_closure.slice_obligation_closure_digest,
            ),
            "closed_empty": identity(
                empty_closure.closure_document_bytes,
                empty_closure.empty_domain_closure_digest,
            ),
            "conflict_blocked": identity(
                blocked.receipt_document_bytes,
                blocked.blocked_input_receipt_digest,
            ),
        }
        self.assertEqual(
            summary,
            {
                "normal_partial_outcome": {
                    "semantic_digest": "75403302066a400158a0070a3c5c133e15dc7e70b4905eb3f78d510b9f4bfdbd",
                    "canonical_sha256": "3d590d36a77bce44a6cf576e4a7461dd8f7fa772e30f0dbb37fe595cd2a2d761",
                },
                "normal_partial_closure": {
                    "semantic_digest": "31bd200a9f135c52d2a17911996489cc092a59943a95e093efadd7cf1416d770",
                    "canonical_sha256": "216b3c4c44d27ed5b56294815356ab6f5be3e0b96e8470fadaed273846796eef",
                },
                "normal_complete_outcome": {
                    "semantic_digest": "468a7195f8a1cbb8daab4e1e05758860321375939258698732dfd3930baf099a",
                    "canonical_sha256": "e43d46b3f46a3d579cfd1808812793e201c3341b764ffb6da830dbf68ec5f208",
                },
                "normal_complete_closure": {
                    "semantic_digest": "9259ca6744511e8f6662d3a00528a1c923a2dfa9ae8b345c4188186d64776bbd",
                    "canonical_sha256": "7a9b7b1358f1c3bde1672506d4d40992218619988e1cf6e5c620859085e97621",
                },
                "closed_empty": {
                    "semantic_digest": "7bbe46ad1b03659052d7c75241b0464101b7dcc7939d6b867c37ca07be58fe7a",
                    "canonical_sha256": "792f655bb17d55392d147b0c138e7f21a4c6c851dc2bed16f903a299db04ca9f",
                },
                "conflict_blocked": {
                    "semantic_digest": "3af34a95a6186c6ae76baa8a5ec37c61967228ad9333dde10247eedb1fcca8ab",
                    "canonical_sha256": "01cae545842dd2b24355f78522df980a17ce8dc8283d0b3d5536819573b900ab",
                },
            },
        )
        self.assertEqual(
            hashlib.sha256(canonical_json_bytes(summary)).hexdigest(),
            "b3f8d2b1848f89996b625abeff43ee97cf689e82878bb9abbeed9a0d58b86a6c",
        )

    def test_h_008_rs_000_007_are_private_precursors_only(self) -> None:
        assignments = self._assignments("slice-input-h-private-precursors")
        closure = slice_input.reconcile_review_slice_traversal_outcomes(
            assignments,
            self._normal_outcomes(assignments),
        )
        document = closure.closure_document_copy()
        self.assertEqual(document["closure_status"], "NORMAL_CLOSED")
        self.assertTrue(
            document["normal_slice_candidates"][0]["frontier"]
        )
        self.assertNotIn("review_slice_set", document)
        self.assertNotIn("coverage_ledger", document)
        self.assertNotIn("coverage_frontier", document)

        import veritrail_review

        for name in (
            "ReviewSliceSet",
            "CoverageLedger",
            "publish_review_slice_set",
            "publish_coverage_ledger",
        ):
            self.assertFalse(hasattr(veritrail_review, name))
            self.assertNotIn(name, veritrail_review.__all__)


if __name__ == "__main__":
    unittest.main()
