from __future__ import annotations

import copy
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_fact_fulfillment as fact_support  # noqa: E402
import test_parse_product_fact_consumer as parse_support  # noqa: E402
from test_execution_cell import _canonical_artifact, _seal_policy  # noqa: E402
from veritrail_review import _fact_fulfillment as fact_consumer  # noqa: E402
from veritrail_review import _fact_relation_transition as transition  # noqa: E402
from veritrail_review import _fact_to_coverage_handoff as coverage_handoff  # noqa: E402
from veritrail_review._execution_cell_binding import (  # noqa: E402
    ProviderBinding,
    ProviderDescriptor,
)
from veritrail_review._fact_fulfillment_binding import (  # noqa: E402
    build_fact_relation_stage_applicability,
    closed_fact_bindings,
)
from veritrail_review._relation_observation_binding import (  # noqa: E402
    corrected_import_form_relation_observation_bindings,
)
from veritrail_review.derivation_input_contracts import DerivationInputSet  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes  # noqa: E402


class FactRelationTransitionTests(unittest.TestCase):
    maxDiff = None

    def _inputs(self, bodies=None, *, advisory=False):
        base = fact_support.FactFulfillmentTests()._inputs(
            bodies=bodies, advisory=advisory
        )
        policy = base.review_policy_document_copy()
        policy["provider_requirements"].append(
            {
                "capability_id": "review-relation-derivation",
                "required": True,
                "composition_mode": "CUMULATIVE",
            }
        )
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=base.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=base.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=(
                base.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=base.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=base.derivation_profile_digest,
        )

    @staticmethod
    def _with_policy(inputs, transform):
        policy = inputs.review_policy_document_copy()
        transform(policy)
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=inputs.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=(
                inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=inputs.derivation_profile_digest,
        )

    def _fact_closure(self, inputs=None, *, advisory=False):
        inputs = self._inputs(advisory=advisory) if inputs is None else inputs
        with mock.patch.object(
            parse_support.ParseHelper,
            "_accepted_terminal_for_source",
            side_effect=fact_support.fixture_terminal,
        ):
            _, parse_closure, context, eligibility = (
                parse_support.ProductFactConsumerTests()._parse_world(inputs)
            )
        parent = fact_consumer.create_product_fact_consumer_for_relation_transition(
            parse_closure,
            derivation_id="fact-relation-transition-test",
            bindings=closed_fact_bindings(include_advisory=advisory),
        )
        observations = fact_support.FactFulfillmentTests()._execute(parent)
        return parent.reconcile(observations), inputs, context, eligibility

    @staticmethod
    def _replace_admission_document(admitted, document):
        document["admission"]["carrier_digest"] = transition._carrier_digest(document)
        document["admission"]["admission_digest"] = transition._admission_digest(
            document
        )
        encoded = canonical_json_bytes(document)
        admitted._OwnedFactRelationTransitionAdmission__bytes = encoded
        admitted._OwnedFactRelationTransitionAdmission__bound_bytes = encoded

    def test_fric_000_018_complete_fact_handoff_qualifies_relation_edge(self):
        closure, inputs, context, _ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        self.assertIs(admitted._inputs_ref(), inputs)
        self.assertIs(admitted._context_ref(), context)
        self.assertEqual(document["admission"]["status"], "QUALIFIED")
        self.assertEqual(
            document["stage_applicability"]["stage_applicability_function"],
            "r1-fact-relation-stage-applicability/0.2",
        )
        self.assertEqual(
            document["fact_set"]["fact_set_digest"],
            document["product_closure"]["fact_set_digest"],
        )
        self.assertEqual(
            len(document["fact_set"]["facts"]), 14
        )
        self.assertEqual(len(document["observation_domain"]["observation_items"]), 10)
        self.assertEqual(len(document["obligation_projection"]["obligations"]), 10)
        self.assertTrue(
            all(
                item["accepted_product_identity"]
                and item["module_fact_id"]
                and item["product_closure_entry_digest"]
                for item in document["obligation_projection"]["obligations"]
            )
        )
        self.assertEqual(len(document["relation_set"]["relations"]), 10)
        self.assertEqual(document["relation_set"]["conflicts"], [])
        self.assertFalse(document["authority_ceiling"]["coverage"])
        self.assertFalse(document["authority_ceiling"]["public_review"])

    def test_fric_multi_path_closure_preserves_complete_truth(self):
        closure, *_ = self._fact_closure(
            self._inputs(
                [
                    (b"pkg/a.py", b"import os\nfrom pkg import value\n"),
                    (b"pkg/b.py", b"from . import sibling\nimport sys, json\n"),
                ]
            )
        )
        document = transition.run_fact_handoff_relation_transition(
            closure
        ).document_copy()
        self.assertEqual(len(document["product_closure"]["products"]), 2)
        self.assertTrue(
            all(
                item["module_fact_id"] in item["fact_ids"]
                for item in document["product_closure"]["products"]
            )
        )
        self.assertEqual(
            set(document["fact_partition"]["all_fact_ids"]),
            set(document["fact_partition"]["structural_anchor_fact_ids"])
            | set(document["fact_partition"]["applicable_subject_fact_ids"])
            | set(document["fact_partition"]["profile_non_applicable_fact_ids"]),
        )

    def test_fric_006_known_empty_executes_both_required_providers(self):
        closure, *_ = self._fact_closure(
            self._inputs([(b"pkg/a.py", b"class C:\n    pass\n")])
        )
        document = transition.run_fact_handoff_relation_transition(
            closure
        ).document_copy()
        self.assertEqual(document["obligation_projection"]["obligations"], [])
        self.assertEqual(len(document["provider_lineage"]), 2)
        self.assertTrue(
            all(
                item["terminal"]["phase_status"] == "COMPLETED"
                and item["terminal"]["provider_run_status"] == "COMPLETED"
                and item["receipt"]["assigned_observation_item_ids"] == []
                for item in document["provider_lineage"]
            )
        )

    def test_fric_003_duplicate_module_fails_product_closure(self):
        closure, *_ = self._fact_closure()
        original = transition._complete_fact_set

        def duplicate_module(source):
            fact_set = original(source)
            module = copy.deepcopy(
                next(item for item in fact_set["facts"] if item["fact_kind"] == "MODULE")
            )
            module["fact_id"] = "f" * 64
            fact_set["facts"].append(module)
            return fact_set

        with mock.patch.object(
            transition, "_complete_fact_set", side_effect=duplicate_module
        ):
            with self.assertRaises(transition.FactRelationTransitionError):
                transition.run_fact_handoff_relation_transition(closure)

    def test_fric_004_foreign_path_fact_fails_product_closure(self):
        closure, *_ = self._fact_closure()
        original = transition._complete_fact_set

        def foreign_path(source):
            fact_set = original(source)
            fact = next(
                item for item in fact_set["facts"] if item["fact_kind"] != "MODULE"
            )
            fact["source_anchor"]["git_path"]["git_path_hex"] = "ff"
            return fact_set

        with mock.patch.object(transition, "_complete_fact_set", side_effect=foreign_path):
            with self.assertRaises(transition.FactRelationTransitionError):
                transition.run_fact_handoff_relation_transition(closure)

    def test_fric_000_filtered_factset_cannot_replace_handoff_truth(self):
        closure, *_ = self._fact_closure()
        original = transition._complete_fact_set

        def filtered(source):
            fact_set = original(source)
            fact_set["facts"] = [
                item
                for item in fact_set["facts"]
                if item["fact_kind"] in {"MODULE", "IMPORT_DECLARATION"}
            ]
            return fact_set

        with mock.patch.object(transition, "_complete_fact_set", side_effect=filtered):
            with self.assertRaises(transition.FactRelationTransitionError):
                transition.run_fact_handoff_relation_transition(closure)

    def test_fric_same_fact_claim_and_transition_continuation_are_one_shot(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        first = admitted.claim_continuation()
        self.assertEqual(first._document_copy()["admission"]["status"], "QUALIFIED")
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.claim_continuation()
        with self.assertRaises(transition.FactRelationTransitionError):
            transition.run_fact_handoff_relation_transition(closure)

    def test_fric_carrier_digest_binds_stage_and_obligation_proof(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        document["stage_applicability"]["stages"][0][
            "applicable_requirements"
        ] = []
        tampered = canonical_json_bytes(document)
        admitted._OwnedFactRelationTransitionAdmission__bytes = tampered
        admitted._OwnedFactRelationTransitionAdmission__bound_bytes = tampered
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()

    def test_fric_cid_007_012_resealed_projection_drift_still_fails(self):
        mutations = (
            lambda document: document["stage_applicability"]["stages"][0].update(
                non_applicable_requirements=[]
            ),
            lambda document: document["stage_applicability"][
                "cross_stage_reconciliation"
            ]["ownership"][0].update(owner="RELATION"),
            lambda document: document["stage_applicability"].update(
                stage_applicability_function="r1-fact-relation-stage-applicability/0.1"
            ),
            lambda document: document["stage_applicability"]["stages"][1][
                "applicable_requirements"
            ][0].update(capability_id="review-fact-derivation"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                closure, *_ = self._fact_closure()
                admitted = transition.run_fact_handoff_relation_transition(closure)
                document = admitted.document_copy()
                mutation(document)
                self._replace_admission_document(admitted, document)
                with self.assertRaises(transition.FactRelationTransitionError):
                    admitted.document_copy()

    def test_fric_admission_links_cannot_drift_under_valid_digests(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        document["admission"]["relation_set_digest"] = "0" * 64
        self._replace_admission_document(admitted, document)
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()

    def test_fric_complete_fact_history_is_copy_owned_by_carrier(self):
        closure, *_ = self._fact_closure()
        document = transition.run_fact_handoff_relation_transition(
            closure
        ).document_copy()
        source = document["fact_handoff_source"]
        self.assertEqual(source["fact_set"], document["fact_set"])
        self.assertIn("parse_partition", source)
        self.assertIn("fact_projection", source)
        self.assertIn("provider_history", source)
        self.assertIn("whole_attempt", source)

    def test_fric_010_equal_world_fresh_attempt_does_not_share_claim(self):
        inputs = self._inputs()
        first, *_ = self._fact_closure(inputs)
        second, *_ = self._fact_closure(inputs)
        first_document = transition.run_fact_handoff_relation_transition(
            first
        ).document_copy()
        second_document = transition.run_fact_handoff_relation_transition(
            second
        ).document_copy()
        self.assertNotEqual(
            first_document["handoff"]["claim_id"],
            second_document["handoff"]["claim_id"],
        )
        self.assertNotEqual(
            first_document["handoff"]["fact_consumer_attempt_id"],
            second_document["handoff"]["fact_consumer_attempt_id"],
        )

    def test_fric_legacy_fact_consumer_still_rejects_combined_policy(self):
        inputs = self._inputs()
        with mock.patch.object(
            parse_support.ParseHelper,
            "_accepted_terminal_for_source",
            side_effect=fact_support.fixture_terminal,
        ):
            _, parse_closure, _, _ = (
                parse_support.ProductFactConsumerTests()._parse_world(inputs)
            )
        with self.assertRaises(fact_consumer.ProductFactConsumerError):
            fact_consumer.create_product_fact_consumer(
                parse_closure,
                derivation_id="legacy-must-fail-closed",
                bindings=closed_fact_bindings(),
            )

    def test_fric_relation_fact_closure_cannot_cross_into_legacy_handoff(self):
        closure, *_ = self._fact_closure()
        with self.assertRaises(Exception):
            coverage_handoff.claim_fact_to_coverage_handoff(closure)

    def test_fric_legacy_fact_closure_cannot_cross_into_relation_transition(self):
        legacy_inputs = fact_support.FactFulfillmentTests()._inputs()
        legacy_parent, *_ = fact_support.FactFulfillmentTests()._world(legacy_inputs)
        legacy_closure = legacy_parent.reconcile(
            fact_support.FactFulfillmentTests()._execute(legacy_parent)
        )
        with self.assertRaises(transition.FactRelationTransitionError):
            transition.run_fact_handoff_relation_transition(legacy_closure)

    def test_fric_cid_positive_optional_advisory_is_fact_owned(self):
        result = build_fact_relation_stage_applicability(self._inputs(advisory=True))
        stages = {item["stage"]: item for item in result["stages"]}
        self.assertEqual(
            [item["capability_id"] for item in stages["FACT"]["applicable_requirements"]],
            ["python-ast", "python-ast-advisory"],
        )
        self.assertEqual(
            [
                item["capability_id"]
                for item in stages["RELATION"]["applicable_requirements"]
            ],
            ["review-relation-derivation"],
        )

    def test_fric_optional_advisory_world_executes_without_policy_narrowing(self):
        closure, *_ = self._fact_closure(advisory=True)
        document = transition.run_fact_handoff_relation_transition(
            closure
        ).document_copy()
        stages = {
            item["stage"]: item
            for item in document["stage_applicability"]["stages"]
        }
        self.assertEqual(
            [
                item["capability_id"]
                for item in stages["FACT"]["applicable_requirements"]
            ],
            ["python-ast", "python-ast-advisory"],
        )
        self.assertEqual(document["admission"]["status"], "QUALIFIED")

    def test_fric_cid_001_rejects_nonexistent_fact_alias(self):
        inputs = self._with_policy(
            self._inputs(),
            lambda policy: policy["provider_requirements"].__setitem__(
                0,
                {
                    "capability_id": "review-fact-derivation",
                    "required": True,
                    "composition_mode": "CUMULATIVE",
                },
            ),
        )
        with self.assertRaises(ValueError):
            build_fact_relation_stage_applicability(inputs)

    def test_fric_cid_002_003_rejects_missing_required_stage(self):
        for capability in ("python-ast", "review-relation-derivation"):
            with self.subTest(capability=capability):
                inputs = self._with_policy(
                    self._inputs(),
                    lambda policy, capability=capability: policy.__setitem__(
                        "provider_requirements",
                        [
                            item
                            for item in policy["provider_requirements"]
                            if item["capability_id"] != capability
                        ],
                    ),
                )
                with self.assertRaises(ValueError):
                    build_fact_relation_stage_applicability(inputs)

    def test_fric_cid_004_005_006_rejects_requiredness_duplicate_unknown(self):
        transforms = (
            lambda policy: policy["provider_requirements"].append(
                {
                    "capability_id": "python-ast-advisory",
                    "required": True,
                    "composition_mode": "CUMULATIVE",
                }
            ),
            lambda policy: policy["provider_requirements"].append(
                copy.deepcopy(policy["provider_requirements"][0])
            ),
            lambda policy: policy["provider_requirements"].append(
                {
                    "capability_id": "unknown-capability",
                    "required": False,
                    "composition_mode": "CUMULATIVE",
                }
            ),
        )
        for index, transform in enumerate(transforms):
            with self.subTest(index=index):
                inputs = self._with_policy(self._inputs(), transform)
                with self.assertRaises(ValueError):
                    build_fact_relation_stage_applicability(inputs)

    def test_fric_cid_009_total_partition_keeps_non_applicable_rows(self):
        result = build_fact_relation_stage_applicability(self._inputs(advisory=True))
        stages = {item["stage"]: item for item in result["stages"]}
        self.assertEqual(
            [
                item["capability_id"]
                for item in stages["RELATION"]["non_applicable_requirements"]
            ],
            ["python-ast", "python-ast-advisory"],
        )
        self.assertTrue(
            result["cross_stage_reconciliation"]["union_complete"]
        )
        self.assertTrue(
            result["cross_stage_reconciliation"]["intersection_empty"]
        )

    def test_fric_cid_010_same_projection_does_not_share_exact_policy(self):
        first_inputs = self._inputs()
        second_inputs = self._with_policy(
            first_inputs,
            lambda policy: policy["execution_budget"].update(
                wall_clock_ms=policy["execution_budget"]["wall_clock_ms"] + 1
            ),
        )
        first = build_fact_relation_stage_applicability(first_inputs)
        second = build_fact_relation_stage_applicability(second_inputs)
        self.assertEqual(first["stages"], second["stages"])
        self.assertEqual(
            first["cross_stage_reconciliation"],
            second["cross_stage_reconciliation"],
        )
        self.assertNotEqual(first["policy_digest"], second["policy_digest"])
        self.assertNotEqual(
            first["policy_canonical_bytes_hex"],
            second["policy_canonical_bytes_hex"],
        )

    def test_fric_binding_family_cannot_be_narrowed_or_drifted(self):
        for bindings in (
            corrected_import_form_relation_observation_bindings()[:-1],
            (
                ProviderBinding(
                    ProviderDescriptor(
                        **{
                            **corrected_import_form_relation_observation_bindings()[0].descriptor.document(),
                            "provider_version": "drift",
                        }
                    ),
                    corrected_import_form_relation_observation_bindings()[0].launch_key,
                ),
                corrected_import_form_relation_observation_bindings()[1],
            ),
        ):
            closure, *_ = self._fact_closure()
            with self.subTest(bindings=bindings):
                with self.assertRaises(transition.FactRelationTransitionError):
                    transition.run_fact_handoff_relation_transition(
                        closure, relation_bindings=bindings
                    )

    def test_fric_missing_emitted_obligation_rejects_completion(self):
        closure, *_ = self._fact_closure()
        original = (
            transition._source_operation_cell.run_prepared_relation_observation_source_operation_attempt
        )

        def missing(prepared):
            phase = original(prepared)
            if prepared.binding.descriptor.provider_id.endswith("provider-b"):
                return replace(
                    phase,
                    observation_outcome_bytes=phase.observation_outcome_bytes[:-1],
                )
            return phase

        with mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            side_effect=missing,
        ):
            with self.assertRaises(transition.FactRelationTransitionError):
                transition.run_fact_handoff_relation_transition(closure)

    def test_fric_duplicate_emitted_obligation_rejects_completion(self):
        closure, *_ = self._fact_closure()
        original = (
            transition._source_operation_cell.run_prepared_relation_observation_source_operation_attempt
        )

        def duplicate(prepared):
            phase = original(prepared)
            if prepared.binding.descriptor.provider_id.endswith("provider-a"):
                return replace(
                    phase,
                    observation_outcome_bytes=(
                        *phase.observation_outcome_bytes,
                        phase.observation_outcome_bytes[0],
                    ),
                )
            return phase

        with mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            side_effect=duplicate,
        ):
            with self.assertRaises(transition.FactRelationTransitionError):
                transition.run_fact_handoff_relation_transition(closure)

    def test_fric_foreign_request_provenance_rejects_completion(self):
        closure, *_ = self._fact_closure()
        original = (
            transition._source_operation_cell.run_prepared_relation_observation_source_operation_attempt
        )

        def foreign(prepared):
            phase = original(prepared)
            return replace(phase, request_provenance_bytes=b"{}")

        with mock.patch.object(
            transition._source_operation_cell,
            "run_prepared_relation_observation_source_operation_attempt",
            side_effect=foreign,
        ):
            with self.assertRaises(transition.FactRelationTransitionError):
                transition.run_fact_handoff_relation_transition(closure)

    def test_fric_resealed_fact_history_drift_fails_bound_source(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        document["fact_handoff_source"]["provider_history"][0][
            "lifecycle"
        ] = "NOT_STARTED"
        document["handoff"]["source_sha256"] = transition.hashlib.sha256(
            canonical_json_bytes(document["fact_handoff_source"])
        ).hexdigest()
        self._replace_admission_document(admitted, document)
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()

    def test_fric_resealed_context_drift_fails_live_context(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        document["transition_attempt"]["started_at_monotonic"] += 1.0
        context_payload = {
            key: document["transition_attempt"][key]
            for key in (
                "budget_limits",
                "started_at_monotonic",
                "execution_deadline_monotonic",
            )
        }
        document["transition_attempt"]["context_identity"] = (
            transition.semantic_digest(
                "veritrail.review.fact-relation-context/0.1", context_payload
            )
        )
        self._replace_admission_document(admitted, document)
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()

    def test_fric_resealed_request_provenance_drift_fails_exact_world(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        lineage = document["provider_lineage"][0]
        lineage["request"]["request_provenance"]["resolved_at"] = (
            "2099-01-01T00:00:00Z"
        )
        lineage["request_sha256"] = transition.hashlib.sha256(
            canonical_json_bytes(lineage["request"])
        ).hexdigest()
        self._replace_admission_document(admitted, document)
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()

    def test_fric_resealed_attempt_identity_drift_fails_external_binding(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        document["handoff"]["claim_id"] = "resealed-foreign-handoff"
        document["transition_attempt"]["attempt_id"] = (
            "resealed-foreign-transition"
        )
        document["transition_attempt"]["attempt_started_at"] = (
            "2099-01-01T00:00:00Z"
        )
        document["admission"]["handoff_claim_id"] = (
            document["handoff"]["claim_id"]
        )
        document["admission"]["transition_attempt_id"] = document[
            "transition_attempt"
        ]["attempt_id"]
        self._replace_admission_document(admitted, document)
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()

    def test_fric_foreign_policy_lineage_cannot_cross_exact_input_world(self):
        first_closure, first_inputs, *_ = self._fact_closure()
        first_admitted = transition.run_fact_handoff_relation_transition(
            first_closure
        )
        first_document = first_admitted.document_copy()
        first_provenance = copy.deepcopy(
            first_document["transition_attempt"]["request_provenance"]
        )

        second_inputs = self._with_policy(
            first_inputs,
            lambda policy: policy["execution_budget"].update(
                wall_clock_ms=policy["execution_budget"]["wall_clock_ms"] + 1
            ),
        )
        second_closure, *_ = self._fact_closure(second_inputs)
        with mock.patch.object(
            transition,
            "_owned_request_provenance",
            return_value=first_provenance,
        ):
            second_document = transition.run_fact_handoff_relation_transition(
                second_closure
            ).document_copy()

        self.assertNotEqual(
            first_document["input_identity"]["policy_digest"],
            second_document["input_identity"]["policy_digest"],
        )
        first_document["provider_lineage"] = copy.deepcopy(
            second_document["provider_lineage"]
        )
        first_document["relation_set"] = copy.deepcopy(
            second_document["relation_set"]
        )
        first_document["relation_set"]["policy_digest"] = first_document[
            "input_identity"
        ]["policy_digest"]
        first_document["admission"]["relation_set_digest"] = first_document[
            "relation_set"
        ]["relation_set_digest"]
        first_document["admission"]["provider_run_ids"] = [
            item["terminal"]["provider_run_id"]
            for item in first_document["provider_lineage"]
        ]
        self._replace_admission_document(first_admitted, first_document)
        with self.assertRaises(transition.FactRelationTransitionError):
            first_admitted.document_copy()

    def test_fric_resealed_terminal_semantic_drift_fails_wire_validation(self):
        closure, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        lineage = next(
            item
            for item in document["provider_lineage"]
            if item["terminal"]["canonical_relations"]
        )
        lineage["terminal"]["canonical_relations"][0]["local_ordinal"] += 1
        lineage["terminal_sha256"] = transition.hashlib.sha256(
            canonical_json_bytes(lineage["terminal"])
        ).hexdigest()
        self._replace_admission_document(admitted, document)
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()

    def test_fric_resealed_relation_set_drift_fails_terminal_recomposition(self):
        closure, inputs, *_ = self._fact_closure()
        admitted = transition.run_fact_handoff_relation_transition(closure)
        document = admitted.document_copy()
        document["relation_set"] = transition._relation_set_document(
            inputs, document["fact_set"], (), ()
        )
        document["admission"]["relation_set_digest"] = document["relation_set"][
            "relation_set_digest"
        ]
        self._replace_admission_document(admitted, document)
        with self.assertRaises(transition.FactRelationTransitionError):
            admitted.document_copy()


if __name__ == "__main__":
    unittest.main()
