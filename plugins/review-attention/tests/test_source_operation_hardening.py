from __future__ import annotations

import base64
import copy
import hashlib
import inspect
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from threading import Barrier


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_language_support as language_support_tests  # noqa: E402
import test_relation_observation_qualification as obs_support  # noqa: E402
import test_source_operation_controller_integration as f_support  # noqa: E402
import test_source_operation_fact_wire as fact_wire_support  # noqa: E402
import test_source_operation_gate as gate_support  # noqa: E402
import test_source_operation_relation_observation_wire as obs_wire_support  # noqa: E402
from veritrail_review import _execution_cell_application as old_fact  # noqa: E402
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _multi_provider_fact_composition as fact_controller,
)
from veritrail_review import _source_operation_fact_application as fact  # noqa: E402
from veritrail_review import _source_operation_gate as gate  # noqa: E402
from veritrail_review import _source_operation_projection as projection  # noqa: E402
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    FrameProtocolError,
    encode_frame,
)
from veritrail_review._multi_provider_applicability import (  # noqa: E402
    closed_test_multi_provider_bindings,
)
from veritrail_review._relation_observation_binding import (  # noqa: E402
    closed_test_relation_observation_bindings,
)
from veritrail_review._relation_set_admission import (  # noqa: E402
    admit_relation_set_for_private_closed_proof,
)
from veritrail_review.canonical import (  # noqa: E402
    canonical_json_bytes,
    semantic_digest,
)


class SourceOperationHardeningStageGTests(unittest.TestCase):
    """Direct LSPC-000..018 falsifiers plus one canonical report."""

    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        f_support.SourceOperationControllerIntegrationStageFTests.setUpClass()
        cls.f = f_support.SourceOperationControllerIntegrationStageFTests
        helper = language_support_tests.LanguageSupportPrivateClassifierTests()
        cls.mixed_inputs = helper._inputs(
            [
                (b"pkg/good.py", b"print('good')\n", "100644", "REGULAR_BLOB"),
                (
                    b"pkg/bad.py",
                    b"# coding: utf.8\n",
                    "100644",
                    "REGULAR_BLOB",
                ),
            ]
        )
        cls.mixed_result, cls.mixed_attempts = cls.f._run_fact_controller(
            cls.mixed_inputs,
            derivation_id="g-mixed",
        )
        cls.out_inputs = helper._inputs(
            [
                (b"pkg/good.py", b"print('good')\n", "100644", "REGULAR_BLOB"),
                (b"pkg/out.py", b"print('out')\n", "100644", "REGULAR_BLOB"),
            ],
            dispositions={b"pkg/out.py": "OUT_OF_SCOPE"},
        )
        cls.out_result, cls.out_attempts = cls.f._run_fact_controller(
            cls.out_inputs,
            derivation_id="g-out-of-scope",
        )
        cls.large_inputs = helper._inputs(
            [
                (b"pkg/good.py", b"print('good')\n", "100644", "REGULAR_BLOB"),
                (
                    b"pkg/omitted.py",
                    b"x = 1\n" * 40_000,
                    "100644",
                    "REGULAR_BLOB",
                ),
            ],
            dispositions={b"pkg/omitted.py": "OUT_OF_SCOPE"},
        )
        cls.large_attempts = []
        original = fact_controller._run_prepared_closed_test_execution_attempt

        def capture(prepared):
            cls.large_attempts.append(prepared)
            return original(prepared)

        cls.small_limits = ExecutionCellTransportSafetyLimits(
            request_payload_bytes=64 * 1024,
            terminal_payload_bytes=16 * 1024 * 1024,
        )
        from unittest import mock

        with mock.patch.object(
            fact_controller,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=capture,
        ):
            cls.large_result = (
                fact_controller.run_closed_test_multi_provider_fact_composition(
                    cls.large_inputs,
                    derivation_id="g-filter-before-encode",
                    bindings=closed_test_multi_provider_bindings(),
                    transport_limits=cls.small_limits,
                )
            )

        obs_support.RelationObservationQualificationTests.setUpClass()
        cls.failed_observation = (
            obs_support.RelationObservationQualificationTests.a_unavailable
        )
        cls.splice_first = obs_support.RelationObservationQualificationTests.positive
        cls.splice_second = (
            obs_support.RelationObservationQualificationTests.
            _run_with_import_facts(
                inputs=obs_support.RelationObservationQualificationTests.inputs,
                derivation_id="g-cross-attempt-second",
            )
        )

    def test_g_001_lspc_000_terminal_success_cannot_authorize_rejected_input(
        self,
    ) -> None:
        self.assertEqual(self.mixed_result.overall_execution_status, "COMPLETED")
        classification = self.mixed_attempts[0].classification
        dispositions = {
            bytes.fromhex(
                item["semantic_input"]["inventory_item"]["git_path"][
                    "git_path_hex"
                ]
            ): item["disposition"]
            for item in classification.subjects_copy()
        }
        self.assertEqual(dispositions[b"pkg/bad.py"], "UNSUPPORTED")
        self.assertEqual(self._request_paths(self.mixed_attempts[0]), {b"pkg/good.py"})

    def test_g_002_lspc_001_all_unsupported_never_reaches_provider_body(
        self,
    ) -> None:
        for attempt in self.f.all_unsupported_attempts:
            self.assertEqual(attempt.request_document["source_blobs"], [])
        self.assertEqual(
            self.f.all_unsupported_result.overall_execution_status,
            "COMPLETED",
        )

    def test_g_003_lspc_002_out_of_scope_rejection_precedes_exposure(self) -> None:
        self.assertEqual(self.out_result.overall_execution_status, "COMPLETED")
        for attempt in self.out_attempts:
            self.assertEqual(self._request_paths(attempt), {b"pkg/good.py"})

    def test_g_004_lspc_003_fact_required_subject_omission_is_rejected(self) -> None:
        support = fact_wire_support.SourceOperationFactWireStageCTests()
        support.setUp()
        changed = copy.deepcopy(support.request)
        projection_document = changed["source_operation_projection"]
        projection_document["operation_subject_ids"] = projection_document[
            "operation_subject_ids"
        ][:-1]
        projection_document["source_operation_projection_digest"] = semantic_digest(
            "veritrail.review.private-source-operation-projection/0.1",
            {
                key: value
                for key, value in projection_document.items()
                if key != "source_operation_projection_digest"
            },
        )
        changed["source_blobs"] = changed["source_blobs"][:-1]
        changed["operands_digest"] = self._fact_operands(
            changed,
            support.descriptor,
        )
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_request_document(
                changed,
                launch_key="stable-a",
            )

    def test_g_005_lspc_004_relation_rejects_eligible_but_unneeded_body(self) -> None:
        prepared = self.f.relation_attempts[0]
        changed = copy.deepcopy(prepared.request_document)
        actual = self._request_paths(prepared)
        eligible = self._eligible_paths(prepared.classification)
        extra = sorted(eligible - actual)[0]
        changed["source_blobs"].append(self._blob_for_path(prepared.inputs, extra))
        from veritrail_review import (
            _source_operation_relation_derivation_application as relation_app,
        )

        with self.assertRaises(relation_app.RelationSourceOperationProtocolError):
            relation_app.validate_relation_source_operation_request_document(
                changed,
                launch_key=prepared.binding.launch_key,
            )

    def test_g_006_lspc_005_observer_rejects_body_outside_assignment(self) -> None:
        support = obs_wire_support.SourceOperationRelationObservationWireStageETests()
        support.setUpClass()
        changed = copy.deepcopy(support.request)
        assigned = self._document_paths(changed)
        donor = sorted(self._eligible_paths(support.classification) - assigned)[0]
        changed["source_blobs"].append(
            self._blob_for_path(support.inputs, donor)
        )
        from veritrail_review import (
            _source_operation_relation_observation_application as obs_app,
        )

        with self.assertRaises(
            obs_app.RelationObservationSourceOperationProtocolError
        ):
            obs_app.validate_relation_observation_source_operation_request_document(
                changed,
                launch_key=support.binding.launch_key,
            )

    def test_g_007_lspc_006_equal_classification_has_new_attempt_authority(
        self,
    ) -> None:
        first = gate_support.SourceOperationSameAttemptGateStageBTests()
        second = gate_support.SourceOperationSameAttemptGateStageBTests()
        first.setUp()
        second.setUp()
        self.assertEqual(
            first.classification.classification_document_bytes,
            second.classification.classification_document_bytes,
        )
        self.assertIsNot(first.context, second.context)
        first_claim = first._bind()
        second_claim = second._bind()
        first.gate.admit_parent()
        second.gate.admit_parent()
        self.assertIsNot(first_claim.claim(), second_claim.claim())

    def test_g_008_lspc_007_equal_limits_do_not_replace_budget_identity(self) -> None:
        support = gate_support.SourceOperationSameAttemptGateStageBTests()
        support.setUp()
        child = AttemptEligibility()
        claim = support._bind(child=child)
        support.gate.admit_parent()
        fresh = support._context()
        self.assertEqual(fresh.limits, support.context.limits)
        object.__setattr__(
            support.gate,
            "_OwnedSourceOperationAttemptGate__context",
            fresh,
        )
        with self.assertRaises(gate._SourceOperationGateError):
            claim.claim()
        self.assertIs(child.state, AttemptEligibilityState.REVOKED)

    def test_g_009_lspc_008_callers_cannot_assert_projection_authority(self) -> None:
        parameters = inspect.signature(
            projection.build_fact_derivation_source_operation_projection
        ).parameters
        self.assertEqual(tuple(parameters), ("classification", "descriptor"))
        for forbidden in ("paths", "digest", "eligible", "complete"):
            self.assertNotIn(forbidden, parameters)

    def test_g_010_lspc_009_gate_change_invalidates_old_operands(self) -> None:
        support = fact_wire_support.SourceOperationFactWireStageCTests()
        support.setUp()
        changed = copy.deepcopy(support.request)
        changed["language_support_classification"][
            "language_support_function"
        ] = "foreign-function/9.9"
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_request_document(
                changed,
                launch_key="stable-a",
            )

    def test_g_011_lspc_010_corrected_wire_rejects_historical_shape(self) -> None:
        support = fact_wire_support.SourceOperationFactWireStageCTests()
        support.setUp()
        old_request = old_fact.build_request_document(
            inputs=support.inputs,
            derivation_id="g-old-wire",
            request_provenance=support.provenance,
            descriptor=support.descriptor,
        )
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_request_document(
                old_request,
                launch_key="stable-a",
            )

    def test_g_012_lspc_011_one_claim_has_one_concurrent_winner(self) -> None:
        support = gate_support.SourceOperationSameAttemptGateStageBTests()
        support.setUp()
        claim = support._bind()
        support.gate.admit_parent()
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
        self.assertEqual(len(winners), 1)

    def test_g_013_lspc_012_cancelled_parent_rejects_stale_frame(self) -> None:
        support = gate_support.SourceOperationSameAttemptGateStageBTests()
        support.setUp()
        child = AttemptEligibility()
        claim = support._bind(child=child)
        support.gate.admit_parent()
        self.assertTrue(support.context.request_cancellation())
        with self.assertRaises(gate._SourceOperationGateError):
            claim.claim()
        self.assertIs(child.state, AttemptEligibilityState.REVOKED)

    def test_g_014_lspc_013_filter_happens_before_frame_encoding(self) -> None:
        prepared = self.large_attempts[0]
        self.assertEqual(self.large_result.overall_execution_status, "COMPLETED")
        self.assertLessEqual(
            len(prepared.request_frame) - 8,
            self.small_limits.request_payload_bytes,
        )
        self.assertEqual(self._request_paths(prepared), {b"pkg/good.py"})
        full = copy.deepcopy(prepared.request_document)
        full["source_blobs"].append(
            self._blob_for_path(prepared.inputs, b"pkg/omitted.py")
        )
        with self.assertRaises(FrameProtocolError):
            encode_frame(
                full,
                payload_limit=self.small_limits.request_payload_bytes,
            )

    def test_g_015_lspc_014_empty_worlds_keep_distinct_closure_identity(self) -> None:
        digests = {
            self.f.denominator_empty_attempts[0].projection.
            source_operation_projection_digest,
            self.f.all_unsupported_attempts[0].projection.
            source_operation_projection_digest,
            self.f.later_empty_relation_attempts[0].projection.
            source_operation_projection_digest,
            self.f.observation_attempts[0].projection.
            source_operation_projection_digest,
        }
        self.assertEqual(len(digests), 4)

    def test_g_016_lspc_015_worker_rejects_digest_consistent_wrong_bytes(self) -> None:
        support = fact_wire_support.SourceOperationFactWireStageCTests()
        support.setUp()
        changed = copy.deepcopy(support.request)
        raw = b"print('tampered')\n"
        changed["source_blobs"][0]["content_base64"] = base64.b64encode(raw).decode(
            "ascii"
        )
        changed["source_blobs"][0]["size_bytes"] = len(raw)
        changed["source_blobs"][0]["content_sha256"] = hashlib.sha256(raw).hexdigest()
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_request_document(
                changed,
                launch_key="stable-a",
            )

    def test_g_017_lspc_016_worker_has_no_omitted_body_side_channel(self) -> None:
        prepared = self.out_attempts[0]
        frame = prepared.request_frame
        omitted = self.out_inputs.verified_blob_bytes_by_object_identity[
            self._oid_for_path(self.out_inputs, b"pkg/out.py")
        ]
        self.assertNotIn(base64.b64encode(omitted), frame)
        from veritrail_review import _source_operation_fact_worker as worker

        source = inspect.getsource(worker)
        self.assertNotIn("DerivationInputSet", source)
        self.assertNotIn("verified_blob_bytes_by_object_identity", source)

    def test_g_018_lspc_017_cross_attempt_result_splice_is_rejected(self) -> None:
        failed_receipts = self.failed_observation.observation_receipts_copy()
        self.assertEqual(failed_receipts[0]["execution_status"], "UNAVAILABLE")
        self.assertEqual(self.failed_observation.qualification_status, "NOT_QUALIFIED")
        first = self.splice_first
        second = self.splice_second
        self.assertEqual(first.source_snapshot_digest, second.source_snapshot_digest)
        self.assertEqual(first.fact_set_digest, second.fact_set_digest)
        spliced = replace(
            first,
            relation_phase_results=second.relation_phase_results,
            relation_provider_run_bytes=second.relation_provider_run_bytes,
            observation_receipt_bytes=second.observation_receipt_bytes,
            _relation_source_operation_projections=(
                second._relation_source_operation_projections
            ),
        )
        with self.assertRaises(Exception) as caught:
            admit_relation_set_for_private_closed_proof(spliced)
        self.assertEqual(type(caught.exception).__name__, "_RelationSetAdmissionError")

    def test_g_019_lspc_018_projection_does_not_mint_fulfillment(self) -> None:
        value = self.f.relation_attempts[0].projection
        forbidden = {
            "parse",
            "fulfillment",
            "coverage",
            "evidence",
            "verdict",
            "publication",
        }
        fields = {name.lower() for name in value.__dataclass_fields__}
        self.assertTrue(forbidden.isdisjoint(fields))
        import veritrail_review

        for name in (
            "OwnedSourceOperationProjection",
            "classify_language_support",
            "run_closed_test_multi_provider_fact_composition",
        ):
            self.assertFalse(hasattr(veritrail_review, name))

    def test_g_020_hardening_report_has_stable_canonical_bytes(self) -> None:
        report = {
            "contract": "r1-language-support-eligible-operation-projection/0.1",
            "falsifiers": [f"LSPC-{index:03d}:REJECTED" for index in range(19)],
            "protocols": {
                "fact": "veritrail-review-derivation-cell/0.2",
                "relation": "veritrail-review-relation-cell/0.3",
                "observation": "veritrail-review-relation-cell/0.4",
            },
            "empty_projection_digests": sorted(
                {
                    self.f.denominator_empty_attempts[0].projection.
                    source_operation_projection_digest,
                    self.f.all_unsupported_attempts[0].projection.
                    source_operation_projection_digest,
                    self.f.later_empty_relation_attempts[0].projection.
                    source_operation_projection_digest,
                    self.f.observation_attempts[0].projection.
                    source_operation_projection_digest,
                }
            ),
        }
        raw = canonical_json_bytes(report)
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            "dc6ef339570c83af99e7882c3de703ea51e9df91c5b0fd9265bc1b65cbc9ca22",
        )

    @staticmethod
    def _request_paths(prepared) -> set[bytes]:
        return SourceOperationHardeningStageGTests._document_paths(
            prepared.request_document
        )

    @staticmethod
    def _document_paths(document) -> set[bytes]:
        return {
            bytes.fromhex(item["git_path"]["git_path_hex"])
            for item in document["source_blobs"]
        }

    @staticmethod
    def _eligible_paths(classification) -> set[bytes]:
        return {
            bytes.fromhex(
                item["semantic_input"]["inventory_item"]["git_path"][
                    "git_path_hex"
                ]
            )
            for item in classification.subjects_copy()
            if item["disposition"] == "ELIGIBLE"
        }

    @staticmethod
    def _blob_for_path(inputs, path: bytes) -> dict[str, object]:
        for item in inputs.source_snapshot_document_copy()["inventory"]:
            if bytes.fromhex(item["git_path"]["git_path_hex"]) != path:
                continue
            raw = inputs.verified_blob_bytes_by_object_identity[
                item["git_object"]["hex"]
            ]
            return {
                "git_path": copy.deepcopy(item["git_path"]),
                "size_bytes": len(raw),
                "content_sha256": item["content"]["sha256"],
                "content_base64": base64.b64encode(raw).decode("ascii"),
            }
        raise KeyError(path)

    @staticmethod
    def _oid_for_path(inputs, path: bytes) -> str:
        for item in inputs.source_snapshot_document_copy()["inventory"]:
            if bytes.fromhex(item["git_path"]["git_path_hex"]) == path:
                return item["git_object"]["hex"]
        raise KeyError(path)

    @staticmethod
    def _fact_operands(document, descriptor) -> str:
        classification = document["language_support_classification"]
        projection_document = document["source_operation_projection"]
        return semantic_digest(
            fact.OPERANDS_DOMAIN,
            {
                "source_snapshot_digest": document["source_snapshot_digest"],
                "policy_digest": document["policy_digest"],
                "analysis_scope_digest": document["analysis_scope_digest"],
                "slice_policy_digest": document["slice_policy_digest"],
                "derivation_profile_digest": document[
                    "derivation_profile_digest"
                ],
                **descriptor.document(),
                "language_support_function": classification[
                    "language_support_function"
                ],
                "classification_digest": classification["classification_digest"],
                "source_operation_projection_digest": projection_document[
                    "source_operation_projection_digest"
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
