from __future__ import annotations

import inspect
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_language_support as language_support_tests  # noqa: E402
import test_relation_derivation as relation_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _multi_provider_fact_composition as fact_controller,
)
from veritrail_review import _relation_derivation as relation_controller  # noqa: E402
from veritrail_review import (  # noqa: E402
    _relation_observation_qualification as observation_controller,
)
from veritrail_review._multi_provider_applicability import (  # noqa: E402
    closed_test_multi_provider_bindings,
)
from veritrail_review._relation_observation_qualification_values import (  # noqa: E402
    OwnedRelationCompositionQualificationResult,
)


class SourceOperationControllerIntegrationStageFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        relation_support.RelationDerivationTests.setUpClass()
        cls.relation_inputs = relation_support.RelationDerivationTests.relation_inputs
        helper = language_support_tests.LanguageSupportPrivateClassifierTests()
        cls.denominator_empty_inputs = helper._inputs(
            dispositions={b"pkg/module.py": "OUT_OF_SCOPE"}
        )
        cls.all_unsupported_inputs = helper._inputs(
            [
                (
                    b"pkg/module.py",
                    b"# coding: utf.8\n",
                    "100644",
                    "REGULAR_BLOB",
                )
            ]
        )

        cls.relation_fact_attempts = []
        cls.relation_attempts = []
        fact_run = relation_controller._run_prepared_closed_test_execution_attempt
        relation_run = relation_controller._run_prepared_relation_execution_attempt

        def capture_fact(prepared):
            cls.relation_fact_attempts.append(prepared)
            return fact_run(prepared)

        def capture_relation(prepared):
            cls.relation_attempts.append(prepared)
            return relation_run(prepared)

        with mock.patch.object(
            relation_controller,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=capture_fact,
        ), mock.patch.object(
            relation_controller,
            "_run_prepared_relation_execution_attempt",
            side_effect=capture_relation,
        ):
            cls.relation_result = (
                relation_controller.run_closed_test_relation_derivation(
                    cls.relation_inputs,
                    derivation_id="f-relation-controller",
                    bindings=(
                        relation_controller.closed_test_relation_derivation_bindings()
                    ),
                )
            )

        cls.observation_fact_attempts = []
        cls.observation_attempts = []
        fact_run = (
            observation_controller._run_prepared_closed_test_execution_attempt
        )
        observation_run = (
            observation_controller.run_prepared_relation_observation_attempt
        )

        def capture_observation_fact(prepared):
            cls.observation_fact_attempts.append(prepared)
            return fact_run(prepared)

        def capture_observation(prepared):
            cls.observation_attempts.append(prepared)
            return observation_run(prepared)

        with mock.patch.object(
            observation_controller,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=capture_observation_fact,
        ), mock.patch.object(
            observation_controller,
            "run_prepared_relation_observation_attempt",
            side_effect=capture_observation,
        ):
            cls.observation_result = (
                observation_controller.
                run_closed_test_relation_observation_qualification(
                    cls.relation_inputs,
                    derivation_id="f-observation-controller",
                    bindings=(
                        observation_controller.
                        closed_test_relation_observation_qualification_bindings()
                    ),
                )
            )

        cls.denominator_empty_result, cls.denominator_empty_attempts = (
            cls._run_fact_controller(
                cls.denominator_empty_inputs,
                derivation_id="f-denominator-empty",
            )
        )
        cls.all_unsupported_result, cls.all_unsupported_attempts = (
            cls._run_fact_controller(
                cls.all_unsupported_inputs,
                derivation_id="f-all-unsupported",
            )
        )

        cls.later_empty_fact_attempts = []
        cls.later_empty_relation_attempts = []
        fact_run = relation_controller._run_prepared_closed_test_execution_attempt
        relation_run = relation_controller._run_prepared_relation_execution_attempt

        def empty_fact(prepared):
            cls.later_empty_fact_attempts.append(prepared)
            phase = fact_run(prepared)
            return replace(
                phase,
                canonical_fact_bytes=(),
                reported_fact_ids=(),
            )

        def capture_empty_relation(prepared):
            cls.later_empty_relation_attempts.append(prepared)
            return relation_run(prepared)

        with mock.patch.object(
            relation_controller,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=empty_fact,
        ), mock.patch.object(
            relation_controller,
            "_run_prepared_relation_execution_attempt",
            side_effect=capture_empty_relation,
        ):
            cls.later_empty_result = (
                relation_controller.run_closed_test_relation_derivation(
                    cls.relation_inputs,
                    derivation_id="f-later-empty",
                    bindings=(
                        relation_controller.closed_test_relation_derivation_bindings()
                    ),
                )
            )

    @classmethod
    def _run_fact_controller(cls, inputs, *, derivation_id):
        attempts = []
        original = fact_controller._run_prepared_closed_test_execution_attempt

        def capture(prepared):
            attempts.append(prepared)
            return original(prepared)

        with mock.patch.object(
            fact_controller,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=capture,
        ):
            result = fact_controller.run_closed_test_multi_provider_fact_composition(
                inputs,
                derivation_id=derivation_id,
                bindings=closed_test_multi_provider_bindings(),
            )
        return result, attempts

    def test_f_001_fact_children_use_corrected_wire_and_one_live_attempt(self) -> None:
        attempts = self.relation_fact_attempts
        self.assertEqual(len(attempts), 2)
        self.assertEqual(
            {item.request_document["protocol"] for item in attempts},
            {"veritrail-review-derivation-cell/0.2"},
        )
        self.assertEqual(len({id(item.context) for item in attempts}), 1)
        self.assertEqual(len({id(item.parent_eligibility) for item in attempts}), 1)
        self.assertEqual(len({id(item.classification) for item in attempts}), 1)
        self.assertEqual(len({id(item.eligibility) for item in attempts}), 2)
        self.assertTrue(
            all(
                item.phase_status.value == "COMPLETED"
                for item in self.relation_result.fact_phase_results
            )
        )
        for item in attempts:
            self._assert_exact_provider_source_set(item)

    def test_f_002_relation_controller_continues_same_attempt_on_v03(self) -> None:
        self.assertEqual(len(self.relation_attempts), 1)
        relation_attempt = self.relation_attempts[0]
        fact_attempt = self.relation_fact_attempts[0]
        self.assertEqual(
            relation_attempt.request_document["protocol"],
            "veritrail-review-relation-cell/0.3",
        )
        self.assertIs(relation_attempt.context, fact_attempt.context)
        self.assertIs(
            relation_attempt.parent_eligibility,
            fact_attempt.parent_eligibility,
        )
        self.assertIs(relation_attempt.classification, fact_attempt.classification)
        self.assertEqual(self.relation_result.relation_start_status, "STARTED")
        self.assertEqual(self.relation_result.final_phase_status, "COMPLETED")
        self._assert_exact_provider_source_set(relation_attempt)

    def test_f_003_observation_children_run_on_v04_under_same_attempt(self) -> None:
        self.assertIsInstance(
            self.observation_result,
            OwnedRelationCompositionQualificationResult,
        )
        self.assertEqual(len(self.observation_attempts), 2)
        fact_attempt = self.observation_fact_attempts[0]
        for item in self.observation_attempts:
            self.assertEqual(
                item.request_document["protocol"],
                "veritrail-review-relation-cell/0.4",
            )
            self.assertIs(item.context, fact_attempt.context)
            self.assertIs(item.parent_eligibility, fact_attempt.parent_eligibility)
            self.assertIs(item.classification, fact_attempt.classification)
            self._assert_exact_provider_source_set(item)
        self.assertEqual(
            [
                item["execution_status"]
                for item in self.observation_result.observation_receipts_copy()
            ],
            ["COMPLETED", "COMPLETED"],
        )

    def test_f_004_denominator_empty_and_all_unsupported_remain_distinct(self) -> None:
        first = self.denominator_empty_attempts[0]
        second = self.all_unsupported_attempts[0]
        for result, attempts in (
            (self.denominator_empty_result, self.denominator_empty_attempts),
            (self.all_unsupported_result, self.all_unsupported_attempts),
        ):
            self.assertEqual(result.overall_execution_status, "COMPLETED")
            self.assertEqual(result.canonical_facts_copy(), ())
            self.assertTrue(
                all(item.request_document["source_blobs"] == [] for item in attempts)
            )
            self.assertTrue(
                all(
                    item.phase_status.value == "COMPLETED"
                    for item in result.phase_results
                )
            )
        self.assertNotEqual(
            first.classification.classification_digest,
            second.classification.classification_digest,
        )
        self.assertNotEqual(
            first.projection.source_operation_projection_digest,
            second.projection.source_operation_projection_digest,
        )

    def test_f_005_later_empty_relation_still_runs_applicable_child(self) -> None:
        self.assertEqual(len(self.later_empty_relation_attempts), 1)
        attempt = self.later_empty_relation_attempts[0]
        self.assertGreater(attempt.classification.eligible_count, 0)
        self.assertEqual(attempt.request_document["source_blobs"], [])
        self.assertEqual(attempt.projection.operation_subject_ids, ())
        self.assertEqual(self.later_empty_result.relation_start_status, "STARTED")
        self.assertEqual(self.later_empty_result.final_phase_status, "COMPLETED")
        self.assertIs(
            attempt.context,
            self.later_empty_fact_attempts[0].context,
        )

    def test_f_006_empty_observation_assignment_runs_both_children(self) -> None:
        domain = self.observation_result.observation_domain_copy()
        self.assertEqual(domain["observation_items"], [])
        self.assertGreater(
            self.observation_attempts[0].classification.eligible_count, 0
        )
        for item in self.observation_attempts:
            self.assertEqual(item.projection.assigned_observation_item_ids, ())
            self.assertEqual(item.projection.operation_subject_ids, ())
            self.assertEqual(item.request_document["source_blobs"], [])

    def test_f_007_empty_world_projection_identities_do_not_collapse(self) -> None:
        digests = {
            self.denominator_empty_attempts[0].projection.
            source_operation_projection_digest,
            self.all_unsupported_attempts[0].projection.
            source_operation_projection_digest,
            self.later_empty_relation_attempts[0].projection.
            source_operation_projection_digest,
            self.observation_attempts[0].projection.
            source_operation_projection_digest,
        }
        self.assertEqual(len(digests), 4)

    def test_f_008_integration_remains_private_and_nonpublishing(self) -> None:
        import veritrail_review

        self.assertFalse(
            hasattr(veritrail_review, "run_prepared_fact_source_operation_attempt")
        )
        for function in (
            fact_controller.run_closed_test_multi_provider_fact_composition,
            relation_controller.run_closed_test_relation_derivation,
            observation_controller.
            run_closed_test_relation_observation_qualification,
        ):
            parameters = inspect.signature(function).parameters
            for forbidden in ("output_path", "publisher", "schema", "coverage"):
                self.assertNotIn(forbidden, parameters)

    def _assert_exact_provider_source_set(self, prepared) -> None:
        path_by_subject = {
            item["subject_identity"]: item["semantic_input"]["inventory_item"][
                "git_path"
            ]["git_path_hex"]
            for item in prepared.classification.subjects_copy()
        }
        expected_paths = {
            path_by_subject[item]
            for item in prepared.projection.operation_subject_ids
        }
        actual_paths = {
            item["git_path"]["git_path_hex"]
            for item in prepared.request_document["source_blobs"]
        }
        self.assertEqual(actual_paths, expected_paths)


if __name__ == "__main__":
    unittest.main()
