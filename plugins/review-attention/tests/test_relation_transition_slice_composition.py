from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_fact_relation_transition as transition_support  # noqa: E402
from veritrail_review import _fact_relation_transition as transition  # noqa: E402
from veritrail_review import _relation_transition_slice_composition as composition  # noqa: E402
from veritrail_review import _relation_observation_application as relation_application  # noqa: E402
from veritrail_review import _review_slice_input as legacy_slice_input  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402


class RelationTransitionSliceCompositionTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.support = transition_support.FactRelationTransitionTests()

    def _admission(self, inputs=None):
        closure, inputs, context, eligibility = self.support._fact_closure(inputs)
        admitted = transition.run_fact_handoff_relation_transition(closure)
        return admitted, inputs, context, eligibility

    def _bridge(self, inputs=None):
        admitted, inputs, context, eligibility = self._admission(inputs)
        claimed = admitted.claim_continuation()
        bridge = composition.admit_relation_transition_for_slice_composition(claimed)
        return admitted, claimed, bridge, inputs, context, eligibility

    def _result(self, inputs=None):
        admitted, claimed, bridge, inputs, context, eligibility = self._bridge(inputs)
        result = composition.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        )
        return result, admitted, claimed, bridge, inputs, context, eligibility

    def test_rsc_001_exact_transition_composes_complete_slice_and_coverage_world(self):
        result, admitted, _, bridge, inputs, context, eligibility = self._result()
        document = result.document_copy()
        source = admitted.document_copy()
        slice_set = document["review_slice_set"]
        ledger = document["coverage_ledger"]

        self.assertIsNotNone(slice_set)
        self.assertEqual(document["slice_set_admission"]["terminal_branch"], "NORMAL_PARTIAL")
        self.assertEqual(len(source["fact_set"]["facts"]), 14)
        self.assertEqual(len(source["relation_set"]["relations"]), 10)
        self.assertEqual(len(document["slice_obligation_domain"]["obligations"]), 1)
        self.assertEqual(len(slice_set["slices"]), 1)
        self.assertEqual(ledger["overall_coverage_status"], "PARTIAL")
        self.assertEqual(
            [(item["stage"], item["coverage_status"]) for item in ledger["stages"]],
            [
                ("SNAPSHOT_INVENTORY", "COMPLETE"),
                ("POLICY_SCOPE", "COMPLETE"),
                ("LANGUAGE_SUPPORT", "COMPLETE"),
                ("PARSE", "COMPLETE"),
                ("FACT_DERIVATION", "COMPLETE"),
                ("RELATION_DERIVATION", "COMPLETE"),
                ("SLICE_DERIVATION", "PARTIAL"),
            ],
        )
        roots = {item["stage"]: item for item in ledger["root_bindings"]}
        self.assertEqual(set(roots), {"FACT_SET", "RELATION_SET", "REVIEW_SLICE_SET"})
        self.assertEqual(roots["FACT_SET"]["artifact_digest"], source["fact_set"]["fact_set_digest"])
        self.assertEqual(roots["RELATION_SET"]["artifact_digest"], source["relation_set"]["relation_set_digest"])
        self.assertEqual(roots["REVIEW_SLICE_SET"]["artifact_digest"], slice_set["slice_set_digest"])
        self.assertIs(admitted._inputs_ref(), inputs)
        self.assertIs(admitted._context_ref(), context)
        self.assertIs(bridge._coordinates()[3], admitted._eligibility_ref())
        self.assertFalse(document["authority_ceiling"]["manifest"])
        self.assertFalse(document["authority_ceiling"]["persistence"])
        self.assertFalse(document["authority_ceiling"]["public_review"])
        self.assertEqual(bridge.document_copy()["admission"]["status"], "QUALIFIED")

    def test_rsc_002_multi_path_preserves_per_path_module_closure(self):
        inputs = self.support._inputs(
            [
                (b"pkg/a.py", b"import os\nfrom pkg import value\n"),
                (b"pkg/b.py", b"from . import sibling\nimport sys, json\n"),
            ]
        )
        result, admitted, *_ = self._result(inputs)
        source = admitted.document_copy()
        document = result.document_copy()
        module_ids = {
            item["fact_id"]
            for item in source["fact_set"]["facts"]
            if item["fact_kind"] == "MODULE"
        }
        obligations = document["slice_obligation_domain"]["obligations"]
        slices = document["review_slice_set"]["slices"]

        self.assertEqual(len(source["product_closure"]["products"]), 2)
        self.assertEqual({item["anchor_fact_id"] for item in obligations}, module_ids)
        self.assertEqual(
            {item["slice_spec"]["anchor_fact_id"] for item in slices}, module_ids
        )
        self.assertEqual(len(obligations), len(slices))

    def test_rsc_003_valid_zero_anchor_domain_closes_empty_without_inventing_members(self):
        inputs = self.support._with_policy(
            self.support._inputs([(b"pkg/a.py", b"import os\n")]),
            lambda policy: policy["slice_policy"].update(
                anchor_fact_kinds=["CLASS_DECLARATION"]
            ),
        )
        result, *_ = self._result(inputs)
        document = result.document_copy()

        self.assertEqual(document["slice_obligation_domain"]["obligations"], [])
        self.assertEqual(document["review_slice_set"]["slices"], [])
        self.assertEqual(document["slice_set_admission"]["terminal_branch"], "CLOSED_EMPTY")
        slice_root = next(
            item
            for item in document["coverage_ledger"]["root_bindings"]
            if item["stage"] == "REVIEW_SLICE_SET"
        )
        self.assertEqual(slice_root["terminal_branch"], "CLOSED_EMPTY")

    def test_rsc_004_relation_conflict_preserves_unknown_slice_and_partial_coverage(self):
        closure, *_ = self.support._fact_closure()
        original = (
            transition._source_operation_cell.
            run_prepared_relation_observation_source_operation_attempt
        )

        def conflicting(prepared):
            phase = original(prepared)
            if not prepared.binding.descriptor.provider_id.endswith("provider-b"):
                return phase
            request = relation_application._synthetic_request(
                prepared.request_document,
                phase.provider_run_id,
            )
            relations = list(phase.canonical_relations_copy())
            lexical = [
                item for item in relations if item["relation_kind"] == "LEXICAL_CONTAINS"
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
            alternative = relation_application.canonicalize_relation_observation_candidates(
                request, [candidate]
            )[0]
            self.assertEqual(
                alternative["relation_subject_digest"], first["relation_subject_digest"]
            )
            self.assertNotEqual(alternative["relation_id"], first["relation_id"])
            relations = [
                item for item in relations if item["relation_id"] != second["relation_id"]
            ]
            relations.append(alternative)
            relations.sort(key=lambda item: item["relation_id"])

            target_item = relation_application.relation_for_observation_item(
                request, alternative
            )
            outcomes = [json.loads(raw) for raw in phase.observation_outcome_bytes]
            outcome = next(
                item for item in outcomes if item["observation_item_id"] == target_item
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
                    item["observation_item_id"], item["observation_outcome_id"]
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

        with mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            side_effect=conflicting,
        ):
            admitted = transition.run_fact_handoff_relation_transition(closure)
        bridge = composition.admit_relation_transition_for_slice_composition(
            admitted.claim_continuation()
        )
        document = composition.compose_review_slice_set_and_coverage(
            bridge.claim_continuation()
        ).document_copy()

        self.assertTrue(document["bridge_admission"])
        self.assertIsNone(document["slice_obligation_domain"])
        self.assertIsNone(document["review_slice_set"])
        self.assertEqual(
            document["slice_set_admission"]["terminal_branch"],
            "PREDECESSOR_UNKNOWN",
        )
        self.assertEqual(document["coverage_ledger"]["overall_coverage_status"], "UNKNOWN")
        stages = {item["stage"]: item for item in document["coverage_ledger"]["stages"]}
        self.assertEqual(stages["RELATION_DERIVATION"]["coverage_status"], "PARTIAL")
        self.assertEqual(stages["SLICE_DERIVATION"]["coverage_status"], "UNKNOWN")

    def test_rsc_005_transition_and_bridge_claims_are_one_shot(self):
        _, claimed, bridge, *_ = self._bridge()
        with self.assertRaises(composition.RelationTransitionSliceCompositionError) as second:
            composition.admit_relation_transition_for_slice_composition(claimed)
        self.assertEqual(
            second.exception.code,
            composition.RelationTransitionSliceCompositionFailureCode.BRIDGE_ALREADY_CONSUMED,
        )

        continuation = bridge.claim_continuation()
        with self.assertRaises(composition.RelationTransitionSliceCompositionError) as reused:
            bridge.claim_continuation()
        self.assertEqual(
            reused.exception.code,
            composition.RelationTransitionSliceCompositionFailureCode.BRIDGE_ALREADY_CONSUMED,
        )
        result = composition.compose_review_slice_set_and_coverage(continuation)
        self.assertEqual(result.document_copy()["slice_set_admission"]["status"], "QUALIFIED")

    def test_rsc_006_foreign_digest_only_and_legacy_authorities_fail_closed(self):
        with self.assertRaises(composition.RelationTransitionSliceCompositionError) as foreign:
            composition.admit_relation_transition_for_slice_composition(object())
        self.assertEqual(
            foreign.exception.code,
            composition.RelationTransitionSliceCompositionFailureCode.BRIDGE_INPUT_REJECTED,
        )
        with self.assertRaises(composition.RelationTransitionSliceCompositionError):
            composition.ClaimedRelationTransitionSliceBridgeContinuation(
                object(), _token=object()
            )

        admitted, _, _, _ = self._admission()
        claimed = admitted.claim_continuation()
        with self.assertRaises(Exception):
            legacy_slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                claimed
            )
        bridge = composition.admit_relation_transition_for_slice_composition(claimed)
        with self.assertRaises(Exception):
            legacy_slice_input.admit_relation_set_for_slice_input_private_closed_proof(
                bridge
            )

    def test_rsc_007_common_mode_denominator_omission_is_independently_rejected(self):
        _, _, bridge, *_ = self._bridge()
        original = composition._build_review_slice_obligation_domain

        def narrowed(view):
            domain = original(view)
            domain["obligations"] = []
            domain["slice_obligation_domain_digest"] = semantic_digest(
                "veritrail.review.slice-obligation-domain/0.1",
                {
                    key: copy.deepcopy(value)
                    for key, value in domain.items()
                    if key not in {"policy_digest", "slice_obligation_domain_digest"}
                },
            )
            return domain

        with mock.patch.object(
            composition,
            "_build_review_slice_obligation_domain",
            side_effect=narrowed,
        ):
            with self.assertRaises(composition.RelationTransitionSliceCompositionError) as caught:
                composition.compose_review_slice_set_and_coverage(
                    bridge.claim_continuation()
                )
        self.assertEqual(
            caught.exception.code,
            composition.RelationTransitionSliceCompositionFailureCode.COMPOSITION_RECONCILIATION_REJECTED,
        )

    def test_rsc_008_mutated_slice_candidate_cannot_enter_the_set(self):
        _, _, bridge, *_ = self._bridge()
        original = composition._derive_normal_review_slice_candidate

        def duplicated(boundary):
            candidate = original(boundary)
            candidate["included_fact_ids"].append(candidate["included_fact_ids"][0])
            return candidate

        with mock.patch.object(
            composition,
            "_derive_normal_review_slice_candidate",
            side_effect=duplicated,
        ):
            with self.assertRaises(composition.RelationTransitionSliceCompositionError) as caught:
                composition.compose_review_slice_set_and_coverage(
                    bridge.claim_continuation()
                )
        self.assertEqual(
            caught.exception.code,
            composition.RelationTransitionSliceCompositionFailureCode.COMPOSITION_RECONCILIATION_REJECTED,
        )

    def test_rsc_009_resealed_transition_history_drift_cannot_cross_bridge(self):
        admitted, _, _, _ = self._admission()
        claimed = admitted.claim_continuation()
        document = admitted.document_copy()
        document["relation_set"]["relations"] = document["relation_set"]["relations"][1:]
        document["relation_set"]["relation_set_digest"] = semantic_digest(
            transition.RELATION_SET_FUNCTION,
            {
                key: copy.deepcopy(value)
                for key, value in document["relation_set"].items()
                if key != "relation_set_digest"
            },
        )
        self.support._replace_admission_document(admitted, document)

        with self.assertRaises(composition.RelationTransitionSliceCompositionError):
            composition.admit_relation_transition_for_slice_composition(claimed)

    def test_rsc_010_legacy_slice_bytes_remain_exact(self):
        expected = {
            "_review_slice_input.py": "185ab7adb57b13ffc29a14bf20411702c316000b0c6733a45f7135f8db3ca307",
            "_review_slice_input_values.py": "21a58d679018bc45131d8e4a3909d1f14a7491085106f422e18d64d9f5048bb3",
            "_review_slice_traversal.py": "263bfc8adeac96a1181afdbaa526aac3452523a240f699d23f2a948529a6b784",
        }
        source = ROOT / "src" / "veritrail_review"
        self.assertEqual(
            {
                name: hashlib.sha256((source / name).read_bytes()).hexdigest()
                for name in expected
            },
            expected,
        )


if __name__ == "__main__":
    unittest.main()
