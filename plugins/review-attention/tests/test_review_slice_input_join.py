from __future__ import annotations

import copy
import inspect
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
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
from veritrail_review import (  # noqa: E402
    _review_slice_input_cross_validation_values as cross_values,
)
from veritrail_review import (  # noqa: E402
    _review_slice_obligation_domain_values as domain_values,
)
from veritrail_review._execution_cell_binding import ProviderBinding  # noqa: E402
from veritrail_review._review_slice_input_values import (  # noqa: E402
    _ReviewSliceInputError,
    _ReviewSliceInputFailureCode,
)
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


if __name__ == "__main__":
    unittest.main()
