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

import test_fact_fulfillment as fact_support  # noqa: E402
import test_post_terminal_fact_dual_successor as post_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _global_review_composition_authority as global_composition,
)
from veritrail_review import _relation_observation_application as relation_application  # noqa: E402
from veritrail_review import _fact_relation_transition as transition  # noqa: E402
from veritrail_review._fact_fulfillment_binding import closed_fact_bindings  # noqa: E402
from veritrail_review.budget import BudgetContext, ExecutionBudgetLimits  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes  # noqa: E402


class GlobalReviewCompositionAuthorityTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.support = post_support.PostTerminalFactDualSuccessorTests()
        self.support.setUp()

    def _parse(self, inputs):
        with mock.patch.object(
            post_support.parse_support.ParseHelper,
            "_accepted_terminal_for_source",
            side_effect=fact_support.fixture_terminal,
        ):
            _, closure, context, _ = (
                post_support.parse_support.ProductFactConsumerTests()._parse_world(
                    inputs
                )
            )
        return closure, context

    def _owner(
        self,
        inputs,
        *,
        cleanup_obligations=(),
        bindings=None,
        versions=global_composition._VERSION_DOCUMENT,
    ):
        closure, context = self._parse(inputs)
        owner = global_composition.bind_global_review_composition_authority(
            closure,
            exact_inputs=inputs,
            context=context,
            derivation_id="global-review-composition-authority-test",
            bindings=(closed_fact_bindings() if bindings is None else bindings),
            cleanup_obligations=cleanup_obligations,
            versions=versions,
        )
        return owner, context

    def _run(self, owner, *, kind="COMPLETED", conflict=False):
        fact_patch = mock.patch.object(
            global_composition.fact,
            "run_windows_execution_cell",
            side_effect=self.support.fact_helper._cell(kind=kind),
        )
        relation_patch = (
            self._conflict_patch()
            if conflict
            else mock.patch.object(
                transition._source_operation_cell,
                "run_prepared_relation_observation_source_operation_attempt",
                wraps=(
                    transition._source_operation_cell.
                    run_prepared_relation_observation_source_operation_attempt
                ),
            )
        )
        with fact_patch, relation_patch:
            return owner.run()

    def _candidate(self, owner, *, kind="COMPLETED", conflict=False):
        fact_patch = mock.patch.object(
            global_composition.fact,
            "run_windows_execution_cell",
            side_effect=self.support.fact_helper._cell(kind=kind),
        )
        relation_patch = self._conflict_patch() if conflict else mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            wraps=(
                transition._source_operation_cell.
                run_prepared_relation_observation_source_operation_attempt
            ),
        )
        with fact_patch, relation_patch:
            return owner._produce_candidate_for_admission()

    @staticmethod
    def _failure(call, family):
        with unittest.TestCase().assertRaises(
            global_composition.GlobalReviewCompositionError
        ) as caught:
            call()
        unittest.TestCase().assertEqual(caught.exception.failure_family, family)
        return caught.exception

    @staticmethod
    def _reseal(candidate):
        seal = candidate._GlobalCompositionCandidate__snapshot_seal()
        candidate._GlobalCompositionCandidate__seal = seal
        candidate._GlobalCompositionCandidate__bound_seal = seal

    def _normal_inputs(self):
        helper = self.support.relation_helper
        base = helper._inputs()
        complete = helper._with_policy(
            base, lambda policy: policy["slice_policy"].update(max_depth=99)
        )
        branch_empty = helper._with_policy(
            helper._inputs(bodies=[(b"pkg/a.py", b"import os\n")]),
            lambda policy: policy["slice_policy"].update(
                anchor_fact_kinds=["CLASS_DECLARATION"]
            ),
        )
        return complete, branch_empty, base

    def _conflict_patch(self):
        original = (
            transition._source_operation_cell.
            run_prepared_relation_observation_source_operation_attempt
        )

        def conflicting(prepared):
            phase = original(prepared)
            if not prepared.binding.descriptor.provider_id.endswith("provider-b"):
                return phase
            request = relation_application._synthetic_request(
                prepared.request_document, phase.provider_run_id
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
            alternative = (
                relation_application.canonicalize_relation_observation_candidates(
                    request, [candidate]
                )[0]
            )
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

        return mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            side_effect=conflicting,
        )

    def test_gca_000_all_eight_live_worlds_admit_once(self):
        complete, branch_empty, partial = self._normal_inputs()
        normal = (
            ("NORMAL_CONSISTENT", complete, False),
            ("NORMAL_BRANCH_EMPTY", branch_empty, False),
            ("NORMAL_SLICE_PARTIAL", partial, False),
            ("NORMAL_RELATION_CONFLICT", partial, True),
        )
        observed = []
        for expected, inputs, conflict in normal:
            with self.subTest(world=expected):
                owner, context = self._owner(inputs)
                result = self._run(owner, conflict=conflict)
                self.assertEqual(result.world, expected)
                document = result.claim_private_result()
                self.assertEqual(document["world"], expected)
                self.assertEqual(document["selector_route"], "RELATION_HANDOFF")
                self.assertTrue(
                    document["cleanup_outcome"]["all_closed"]
                )
                self.assertEqual(
                    document["context_runtime_identity"], id(context)
                )
                self.assertFalse(
                    document["authority_ceiling"]["core_verdict"]
                )
                observed.append(expected)

        semantic_context = lambda: BudgetContext._admit_for_testing(
            ExecutionBudgetLimits(
                wall_clock_ms=60_000,
                memory_bytes=512 * 1024 * 1024,
                artifact_bytes=64 * 1024 * 1024,
            ),
            clock=lambda: 0.0,
        )
        with mock.patch.object(
            post_support.parse_support.ParseHelper,
            "_context",
            side_effect=semantic_context,
        ):
            for expected, inputs, kind in self.support._negative_worlds():
                with self.subTest(world=expected):
                    owner, _ = self._owner(inputs)
                    result = self._run(owner, kind=kind)
                    document = result.claim_private_result()
                    self.assertEqual(document["world"], expected)
                    self.assertEqual(
                        document["selector_route"],
                        "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2",
                    )
                    self.assertEqual(
                        [item["binding_state"] for item in document["root_topology"]],
                        ["QUALIFIED_ABSENT"] * 3,
                    )
                    observed.append(expected)
        self.assertEqual(
            observed,
            [
                "NORMAL_CONSISTENT",
                "NORMAL_BRANCH_EMPTY",
                "NORMAL_SLICE_PARTIAL",
                "NORMAL_RELATION_CONFLICT",
                "ZERO_PARSE_DENOMINATOR",
                "ALL_PARSE_REJECTED",
                "PROJECTION_BLOCKED",
                "REQUIRED_PROVIDER_NON_SUCCESS",
            ],
        )

    def test_gca_001_version_and_roster_denominator_reject(self):
        inputs = self._normal_inputs()[0]
        bad_versions = dict(global_composition._VERSION_DOCUMENT)
        bad_versions["composition_function"] = "r1-global-review-composition/9.9"
        self._failure(
            lambda: self._owner(inputs, versions=bad_versions),
            global_composition.GlobalCompositionFailureFamily.VERSION_REJECTED,
        )
        expected = closed_fact_bindings()
        self._failure(
            lambda: self._owner(inputs, bindings=expected[:-1]),
            global_composition.GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED,
        )
        self._failure(
            lambda: self._owner(inputs, bindings=(*expected, expected[0])),
            global_composition.GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED,
        )

    def test_gca_002_owner_and_result_are_one_shot_nonserializable(self):
        owner, _ = self._owner(self._normal_inputs()[0])
        result = self._run(owner)
        original = result._GlobalReviewCompositionResult__document_bytes
        result._GlobalReviewCompositionResult__document_bytes = b"{}"
        result._GlobalReviewCompositionResult__bound_document_bytes = b"{}"
        self._failure(
            lambda: result.world,
            global_composition.GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED,
        )
        result._GlobalReviewCompositionResult__document_bytes = original
        result._GlobalReviewCompositionResult__bound_document_bytes = original
        self.assertEqual(result.claim_private_result()["world"], "NORMAL_CONSISTENT")

        owner, _ = self._owner(self._normal_inputs()[0])
        mutated_result = self._run(owner)
        document = json.loads(
            mutated_result._GlobalReviewCompositionResult__document_bytes
        )
        document["world"] = "NORMAL_BRANCH_EMPTY"
        drifted = canonical_json_bytes(document)
        drifted_seal = hashlib.sha256(drifted).hexdigest()
        mutated_result._GlobalReviewCompositionResult__document_bytes = drifted
        mutated_result._GlobalReviewCompositionResult__bound_document_bytes = drifted
        mutated_result._GlobalReviewCompositionResult__document_seal = drifted_seal
        mutated_result._GlobalReviewCompositionResult__bound_document_seal = drifted_seal
        self._failure(
            lambda: mutated_result.world,
            global_composition.GlobalCompositionFailureFamily.ADMISSION_REJECTED,
        )
        self._failure(
            result.claim_private_result,
            global_composition.GlobalCompositionFailureFamily.REPLAY_REJECTED,
        )
        for call, family in (
            (lambda: copy.copy(result), global_composition.GlobalCompositionFailureFamily.ADMISSION_REJECTED),
            (lambda: copy.deepcopy(result), global_composition.GlobalCompositionFailureFamily.ADMISSION_REJECTED),
            (lambda: pickle.dumps(result), global_composition.GlobalCompositionFailureFamily.ADMISSION_REJECTED),
            (result.to_json, global_composition.GlobalCompositionFailureFamily.ADMISSION_REJECTED),
            (owner.run, global_composition.GlobalCompositionFailureFamily.REPLAY_REJECTED),
        ):
            self._failure(call, family)

    def test_gca_003_concurrent_double_consumption_has_one_success(self):
        owner, _ = self._owner(self._normal_inputs()[0])
        with mock.patch.object(
            global_composition.fact,
            "run_windows_execution_cell",
            side_effect=self.support.fact_helper._cell(kind="COMPLETED"),
        ):
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(owner.run) for _ in range(2)]
                outcomes = []
                for future in futures:
                    try:
                        outcomes.append(("PASS", future.result().world))
                    except global_composition.GlobalReviewCompositionError as exc:
                        outcomes.append(("FAIL", exc.failure_family.value))
        self.assertEqual(sum(item[0] == "PASS" for item in outcomes), 1)
        self.assertEqual(sum(item[0] == "FAIL" for item in outcomes), 1)
        self.assertIn(
            (
                "FAIL",
                global_composition.GlobalCompositionFailureFamily.REPLAY_REJECTED.value,
            ),
            outcomes,
        )

    def test_gca_004_cross_world_splice_rejects_independently(self):
        owner, _ = self._owner(self._normal_inputs()[0])
        candidate = self._candidate(owner)
        candidate._GlobalCompositionCandidate__declared_world = "NORMAL_BRANCH_EMPTY"
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.WORLD_SPLICE_REJECTED,
        )

    def test_gca_005_foreign_attempt_and_context_reject(self):
        inputs = self._normal_inputs()[0]
        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        foreign_owner, foreign_context = self._owner(inputs)
        candidate._GlobalCompositionCandidate__owner = foreign_owner
        candidate._GlobalCompositionCandidate__bound_owner = foreign_owner
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.ADMISSION_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        foreign_context_bytes = global_composition._json_bytes(
            global_composition._context_document(foreign_context)
        )
        candidate._GlobalCompositionCandidate__context = foreign_context
        candidate._GlobalCompositionCandidate__bound_context = foreign_context
        candidate._GlobalCompositionCandidate__context_bytes = foreign_context_bytes
        candidate._GlobalCompositionCandidate__bound_context_bytes = foreign_context_bytes
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED,
        )

    def test_gca_006_input_and_roster_mutation_reject(self):
        inputs = self._normal_inputs()[0]
        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        roster = json.loads(candidate._GlobalCompositionCandidate__roster_bytes)
        roster["providers"].pop()
        raw = canonical_json_bytes(roster)
        candidate._GlobalCompositionCandidate__roster_bytes = raw
        candidate._GlobalCompositionCandidate__bound_roster_bytes = raw
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        binding = json.loads(candidate._GlobalCompositionCandidate__input_binding_bytes)
        binding["digests"]["policy_digest"] = "0" * 64
        raw = canonical_json_bytes(binding)
        candidate._GlobalCompositionCandidate__input_binding_bytes = raw
        candidate._GlobalCompositionCandidate__bound_input_binding_bytes = raw
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED,
        )

    def test_gca_007_partial_late_and_unknown_component_reject(self):
        inputs = self._normal_inputs()[0]
        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        receipt = json.loads(candidate._GlobalCompositionCandidate__staging_receipt_bytes)
        receipt["raw_sha256"] = "0" * 64
        candidate._GlobalCompositionCandidate__staging_receipt_bytes = canonical_json_bytes(receipt)
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        continuity_document = json.loads(
            candidate._GlobalCompositionCandidate__continuity_bytes
        )
        continuity_document["continuity_digest"] = "0" * 64
        continuity_raw = canonical_json_bytes(continuity_document)
        candidate._GlobalCompositionCandidate__continuity_bytes = continuity_raw
        candidate._GlobalCompositionCandidate__bound_continuity_bytes = continuity_raw
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.WORLD_SPLICE_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        cleanup = json.loads(candidate._GlobalCompositionCandidate__cleanup_bytes)
        cleanup["cleanup_digest"] = "0" * 64
        candidate._GlobalCompositionCandidate__cleanup_bytes = canonical_json_bytes(
            cleanup
        )
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.RESOURCE_CLEANUP_FAILED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        terminal_phase = candidate._GlobalCompositionCandidate__terminal_phase
        drifted_phase = global_composition.OwnedPhaseResult(
            canonical_bytes=b"{}",
            completed_at_monotonic=terminal_phase.completed_at_monotonic,
        )
        candidate._GlobalCompositionCandidate__terminal_phase = drifted_phase
        candidate._GlobalCompositionCandidate__bound_terminal_phase = drifted_phase
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        carrier_input = candidate._GlobalCompositionCandidate__carrier_input
        carrier_input["consumption_identity"] = "foreign-carrier-consumption/9.9"
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        carrier_input = candidate._GlobalCompositionCandidate__carrier_input
        carrier_input["validation"]["status"] = "UNKNOWN"
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        carrier_input = candidate._GlobalCompositionCandidate__carrier_input
        carrier_input["authority_ceiling"]["core_verdict"] = True
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        carrier_report = json.loads(
            candidate._GlobalCompositionCandidate__carrier_validation_bytes
        )
        carrier_report["file_binding_digest"] = "0" * 64
        candidate._GlobalCompositionCandidate__carrier_validation_bytes = canonical_json_bytes(
            carrier_report
        )
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        manifest_report = json.loads(
            candidate._GlobalCompositionCandidate__manifest_validation_bytes
        )
        manifest_report["root_chain_digest"] = "0" * 64
        candidate._GlobalCompositionCandidate__manifest_validation_bytes = canonical_json_bytes(
            manifest_report
        )
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        candidate._GlobalCompositionCandidate__result_bytes = b"{}"
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        candidate._GlobalCompositionCandidate__carrier_input.pop("files")
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED,
        )

        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        versions = dict(global_composition._VERSION_DOCUMENT)
        versions["admission_function"] = "r1-global-review-composition-admission/9.9"
        raw = canonical_json_bytes(versions)
        candidate._GlobalCompositionCandidate__versions_bytes = raw
        candidate._GlobalCompositionCandidate__bound_versions_bytes = raw
        self._reseal(candidate)
        self._failure(
            lambda: global_composition.independently_admit_global_review_composition(
                candidate
            ),
            global_composition.GlobalCompositionFailureFamily.COMPONENT_VERSION_REJECTED,
        )

    def test_gca_008_manifest_replay_and_cleanup_failure_reject(self):
        inputs = self._normal_inputs()[0]
        owner, _ = self._owner(inputs)
        candidate = self._candidate(owner)
        replay = self._failure(
            candidate._attempt_manifest_staging_replay,
            global_composition.GlobalCompositionFailureFamily.REPLAY_REJECTED,
        )
        self.assertEqual(
            replay.original_reason,
            "MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED",
        )

        owner, _ = self._owner(
            inputs, cleanup_obligations=(lambda: False,)
        )
        failure = self._failure(
            lambda: self._run(owner),
            global_composition.GlobalCompositionFailureFamily.RESOURCE_CLEANUP_FAILED,
        )
        self.assertEqual(failure.original_reason, "CLEANUP_RETURNED_FALSE")
        self.assertFalse(failure.cleanup_outcome_copy()["all_closed"])

    def test_gca_009_earliest_failure_is_retained_through_cleanup(self):
        inputs = self._normal_inputs()[0]
        owner, _ = self._owner(
            inputs, cleanup_obligations=(lambda: False,)
        )
        with mock.patch.object(
            global_composition.fact,
            "execute_product_fact_claim",
            side_effect=RuntimeError("opaque lower failure"),
        ):
            failure = self._failure(
                owner.run,
                global_composition.GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
            )
        self.assertEqual(failure.original_reason, "UNKNOWN")
        self.assertFalse(failure.cleanup_outcome_copy()["all_closed"])


if __name__ == "__main__":
    unittest.main()
