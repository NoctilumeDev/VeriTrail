from __future__ import annotations

import copy
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = ROOT / "plugins" / "review-attention" / "src"
TEST_ROOT = ROOT / "plugins" / "review-attention" / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    sys.path.insert(0, str(location))

import test_fact_fulfillment as fact_support  # noqa: E402
from veritrail_review import _fact_to_coverage_handoff as fact_handoff  # noqa: E402
from veritrail_review import _relation_import_form_provider as provider  # noqa: E402
from veritrail_review import _relation_observation_qualification as qualification  # noqa: E402
from veritrail_review import _source_operation_fact_application as fact_app  # noqa: E402
from veritrail_review import (  # noqa: E402
    _source_operation_relation_observation_application as observation_app,
)
from veritrail_review._execution_cell import _owned_request_provenance  # noqa: E402
from veritrail_review._multi_provider_applicability import (  # noqa: E402
    closed_test_multi_provider_bindings,
)
from veritrail_review._multi_provider_fact_composition import (  # noqa: E402
    _ClosedProviderRun,
    _fact_set_document,
    _merge_completed_sources,
)
from veritrail_review._relation_observation_binding import (  # noqa: E402
    closed_test_relation_observation_bindings,
    corrected_import_form_relation_observation_bindings,
)
from veritrail_review._relation_set_admission import (  # noqa: E402
    admit_relation_set_for_private_closed_proof,
)
from veritrail_review._source_operation_projection import (  # noqa: E402
    build_relation_observation_source_operation_projection,
)
from veritrail_review._language_support import classify_language_support  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes  # noqa: E402
from veritrail_review.derivation_input_contracts import (  # noqa: E402
    DerivationInputSet,
)


_IDENTITY_KEYS = {
    "source_snapshot_digest",
    "derivation_profile_digest",
    "subject_key_digest",
    "fact_id",
    "provenance_refs",
}


class RelationImportFormProviderTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.helper = fact_support.FactFulfillmentTests()
        cls.legacy = cls._world(
            [(b"pkg/a.py", b"pass\nimport os\n")],
            derivation_id="rpif-legacy",
            successor=True,
        )
        cls.legacy_old = cls._world(
            [(b"pkg/a.py", b"pass\nimport os\n")],
            derivation_id="rpif-legacy-old",
            successor=False,
        )
        cls.expanded = cls._world(
            [
                (
                    b"pkg/a.py",
                    b"import os, sys as system\n"
                    b"from pkg import first, second as other\n"
                    b"from ..base import value as alias\n"
                    b"from . import *\n"
                    b"if flag:\n"
                    b"    import json\n"
                    b"def f():\n"
                    b"    from nested import item\n",
                )
            ],
            derivation_id="rpif-expanded",
            successor=True,
        )
        cls.multi_path = cls._world(
            [
                (b"pkg/a.py", b"import os\nfrom pkg import value\n"),
                (b"pkg/b.py", b"from . import sibling\nimport sys, json\n"),
            ],
            derivation_id="rpif-multi-path",
            successor=True,
        )
        cls.utf8_sig = cls._world(
            [(b"pkg/bom.py", b"\xef\xbb\xbfimport os\n")],
            derivation_id="rpif-utf8-sig",
            successor=True,
        )

    @classmethod
    def _world(cls, bodies, *, derivation_id: str, successor: bool):
        fact_inputs = cls.helper._inputs(bodies)
        parent, *_ = cls.helper._world(fact_inputs)
        closure = parent.reconcile(cls.helper._execute(parent))
        source = fact_handoff.claim_fact_to_coverage_handoff(
            closure
        ).document_copy()["source"]
        if source["branch"] != "NORMAL_FULFILLED":
            raise AssertionError("Fact fixture did not produce complete truth")
        semantic_candidates = [
            {
                key: copy.deepcopy(value)
                for key, value in fact.items()
                if key not in _IDENTITY_KEYS
            }
            for fact in source["fact_set"]["facts"]
        ]

        policy = fact_inputs.review_policy_document_copy()
        policy["provider_requirements"].append(
            {
                "capability_id": "review-relation-derivation",
                "required": True,
                "composition_mode": "CUMULATIVE",
            }
        )
        fact_support._seal_policy(policy)
        inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=fact_inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=canonical_json_bytes(policy) + b"\n",
            derivation_profile_canonical_bytes=fact_inputs.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=(
                fact_inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=fact_inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=fact_inputs.derivation_profile_digest,
        )
        original_run = qualification._run_prepared_closed_test_execution_attempt

        def exact_fact_run(prepared):
            phase = original_run(prepared)
            request = fact_app.validate_fact_source_operation_request_document(
                prepared.request_document, launch_key=prepared.binding.launch_key
            )
            facts = fact_app.canonicalize_fact_candidates(
                request, semantic_candidates
            )
            return replace(
                phase,
                canonical_fact_bytes=tuple(
                    canonical_json_bytes(fact) for fact in facts
                ),
                reported_fact_ids=tuple(fact["fact_id"] for fact in facts),
            )

        bindings = (
            qualification.corrected_import_form_relation_observation_qualification_bindings()
            if successor
            else qualification.closed_test_relation_observation_qualification_bindings()
        )
        with mock.patch.object(
            qualification,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=exact_fact_run,
        ):
            result = qualification.run_closed_test_relation_observation_qualification(
                inputs, derivation_id=derivation_id, bindings=bindings
            )

        closed = []
        for binding, phase in zip(
            closed_test_multi_provider_bindings(), result.fact_phase_results
        ):
            closed.append(
                _ClosedProviderRun(
                    binding=binding,
                    phase=phase,
                    canonical_fact_bytes=phase.canonical_fact_bytes,
                    provider_run_document={},
                )
            )
        facts, conflicts = _merge_completed_sources(closed)
        fact_set = _fact_set_document(inputs, facts, conflicts)[0]
        domain = result.observation_domain_copy()
        relation_bindings = (
            corrected_import_form_relation_observation_bindings()
            if successor
            else closed_test_relation_observation_bindings()
        )
        classification = classify_language_support(inputs)
        requests = {}
        for binding in relation_bindings:
            projection = build_relation_observation_source_operation_projection(
                classification, binding.descriptor, fact_set, domain
            )
            document = (
                observation_app.build_relation_observation_source_operation_request_document(
                    inputs=inputs,
                    derivation_id=derivation_id,
                    request_provenance=_owned_request_provenance(inputs),
                    descriptor=binding.descriptor,
                    fact_set_document=fact_set,
                    observation_domain=domain,
                    classification=classification,
                    projection=projection,
                )
            )
            requests[binding.launch_key] = (
                observation_app.validate_relation_observation_source_operation_request_document(
                    document, launch_key=binding.launch_key
                )
            )
        return SimpleNamespace(
            inputs=inputs,
            result=result,
            fact_set=fact_set,
            domain=domain,
            requests=requests,
        )

    def test_rpif_000_legacy_semantics_are_preserved(self) -> None:
        successor = [
            {key: value for key, value in relation.items() if key != "provenance_refs"}
            for relation in self.legacy.result.merged_candidates_copy()
        ]
        historical = [
            {key: value for key, value in relation.items() if key != "provenance_refs"}
            for relation in self.legacy_old.result.merged_candidates_copy()
        ]
        self.assertEqual(
            canonical_json_bytes(successor), canonical_json_bytes(historical)
        )
        successor_receipts = self.legacy.result.observation_receipts_copy()
        historical_receipts = self.legacy_old.result.observation_receipts_copy()
        self.assertEqual(
            sorted(
                [
                (outcome["disposition"], outcome["reported_relation_ids"])
                for receipt in successor_receipts
                for outcome in receipt["accepted_observation_outcomes"]
                ],
                key=lambda item: (item[0], item[1]),
            ),
            sorted(
                [
                (outcome["disposition"], outcome["reported_relation_ids"])
                for receipt in historical_receipts
                for outcome in receipt["accepted_observation_outcomes"]
                ],
                key=lambda item: (item[0], item[1]),
            ),
        )
        successor_request = self.legacy.requests["import-form-observation-b"]
        historical_request = self.legacy_old.requests["observation-b"]
        self.assertEqual(historical_request.document["protocol"], observation_app.PROTOCOL)
        self.assertEqual(
            successor_request.document["protocol"],
            observation_app.IMPORT_FORM_PROTOCOL,
        )
        self.assertNotEqual(
            successor_request.document["operands_digest"],
            historical_request.document["operands_digest"],
        )
        with self.assertRaises(
            observation_app.RelationObservationSourceOperationProtocolError
        ):
            observation_app.validate_relation_observation_source_operation_request_document(
                successor_request.document, launch_key="observation-b"
            )
        with self.assertRaises(
            observation_app.RelationObservationSourceOperationProtocolError
        ):
            observation_app.validate_relation_observation_source_operation_request_document(
                historical_request.document, launch_key="import-form-observation-b"
            )

    def test_rpif_001_legacy_body_ordinal_is_not_compacted(self) -> None:
        lexical = next(
            item
            for item in self.legacy.result.merged_candidates_copy()
            if item["relation_kind"] == "LEXICAL_CONTAINS"
        )
        self.assertEqual(lexical["local_ordinal"], 1)

    def test_rpif_002_multi_alias_import_has_one_fact_per_alias(self) -> None:
        facts = [
            item
            for item in self.expanded.fact_set["facts"]
            if item["fact_kind"] == "IMPORT_DECLARATION"
            and item["semantic_attributes"]["import_form"] == "IMPORT"
            and item["source_anchor"]["start_byte"] == 0
        ]
        self.assertEqual([item["local_ordinal"] for item in facts], [0, 1])
        self._assert_each_import_has_two_relations(self.expanded, facts)

    def test_rpif_003_multi_alias_from_import_keeps_name_semantics(self) -> None:
        facts = [
            item
            for item in self.expanded.fact_set["facts"]
            if item["fact_kind"] == "IMPORT_DECLARATION"
            and item["semantic_attributes"]["module_parts"] == ["pkg"]
        ]
        self.assertEqual(
            [
                (
                    item["semantic_attributes"]["imported_name"],
                    item["semantic_attributes"]["alias_name"],
                    item["local_ordinal"],
                )
                for item in facts
            ],
            [("first", None, 0), ("second", "other", 1)],
        )
        self._assert_each_import_has_two_relations(self.expanded, facts)

    def test_rpif_004_relative_and_star_imports_keep_full_target(self) -> None:
        targets = {
            (
                item["target"]["relative_level"],
                tuple(item["target"]["module_parts"]),
                item["target"]["imported_name"],
            )
            for item in self.expanded.result.merged_candidates_copy()
            if item["relation_kind"] == "IMPORT_TARGET_LITERAL"
        }
        self.assertIn((2, ("base",), "value"), targets)
        self.assertIn((1, (), "*"), targets)

    def test_rpif_005_nested_imports_use_extension_ordinals(self) -> None:
        raw = next(iter(self.expanded.requests.values())).source_blobs_by_path_hex
        occurrences = provider.import_alias_occurrences(next(iter(raw.values())))
        nested = [item for item in occurrences if item["start_byte"] > 100]
        self.assertTrue(nested)
        self.assertTrue(all(item["lexical_child_ordinal"] >= 6 for item in nested))

    def test_rpif_006_multi_path_parents_never_cross_paths(self) -> None:
        facts = {item["fact_id"]: item for item in self.multi_path.fact_set["facts"]}
        for relation in self.multi_path.result.merged_candidates_copy():
            if relation["relation_kind"] != "LEXICAL_CONTAINS":
                continue
            self.assertEqual(
                facts[relation["source_fact_id"]]["source_anchor"]["git_path"],
                facts[relation["target"]["fact_id"]]["source_anchor"]["git_path"],
            )

    def test_rpif_007_missing_fact_rejects_unmatched_occurrence(self) -> None:
        request = self._provider_request(self.expanded)
        facts = dict(request.facts_by_id)
        removed = next(
            key for key, fact in facts.items() if fact["fact_kind"] == "IMPORT_DECLARATION"
        )
        del facts[removed]
        with self.assertRaises(provider.RelationImportFormProviderFailed):
            provider._bind_import_facts(facts, request.source_blobs_by_path_hex)

    def test_rpif_008_duplicate_fact_rejects_shared_occurrence(self) -> None:
        request = self._provider_request(self.expanded)
        facts = dict(request.facts_by_id)
        duplicate = copy.deepcopy(
            next(fact for fact in facts.values() if fact["fact_kind"] == "IMPORT_DECLARATION")
        )
        facts["f" * 64] = duplicate
        with self.assertRaises(provider.RelationImportFormProviderFailed):
            provider._bind_import_facts(facts, request.source_blobs_by_path_hex)

    def test_rpif_009_single_field_semantic_drift_is_rejected(self) -> None:
        request = self._provider_request(self.expanded)
        facts = copy.deepcopy(request.facts_by_id)
        target = next(
            fact for fact in facts.values() if fact["fact_kind"] == "IMPORT_DECLARATION"
        )
        target["semantic_attributes"]["alias_name"] = "foreign"
        with self.assertRaises(provider.RelationImportFormProviderFailed):
            provider._bind_import_facts(facts, request.source_blobs_by_path_hex)

    def test_rpif_010_partial_assignment_cannot_shrink_denominator(self) -> None:
        request = self._provider_request(self.expanded)
        damaged = self._request_copy(request)
        damaged.document["assigned_observation_item_ids"] = damaged.document[
            "assigned_observation_item_ids"
        ][:-1]
        with self.assertRaises(provider.RelationImportFormProviderFailed):
            provider.run_relation_import_form_provider(
                damaged, launch_key="import-form-observation-b"
            )

    def test_rpif_011_duplicate_assignment_is_not_complete(self) -> None:
        request = self._provider_request(self.expanded)
        damaged = self._request_copy(request)
        damaged.document["assigned_observation_item_ids"].append(
            damaged.document["assigned_observation_item_ids"][0]
        )
        with self.assertRaises(provider.RelationImportFormProviderFailed):
            provider.run_relation_import_form_provider(
                damaged, launch_key="import-form-observation-b"
            )

    def test_rpif_012_terminal_partition_rejects_missing_duplicate_and_foreign(self) -> None:
        request = self._provider_request(self.expanded)
        candidates, outcomes = provider.run_relation_import_form_provider(
            request, launch_key="import-form-observation-b"
        )
        relations = observation_app.canonicalize_relation_observation_source_operation_candidates(
            request, candidates
        )
        admitted = observation_app.canonicalize_relation_observation_source_operation_outcomes(
            request, outcomes
        )
        terminal = observation_app.relation_observation_source_operation_terminal_document(
            request,
            terminal_kind="COMPLETED",
            canonical_relations=relations,
            observation_outcomes=admitted,
        )
        phase = self.expanded.result.relation_phase_results[1]
        partial = replace(
            phase,
            observation_outcome_bytes=phase.observation_outcome_bytes[:-1],
        )
        partial_receipt = qualification._observation_receipt(
            self.expanded.domain, phase.provider_descriptor, partial
        )
        self.assertEqual(len(partial_receipt["missing_observation_item_ids"]), 1)
        original = phase.observation_outcomes_copy()[0]
        duplicate = replace(
            phase,
            observation_outcome_bytes=(
                canonical_json_bytes(original),
                canonical_json_bytes(original),
            ),
        )
        duplicate_receipt = qualification._observation_receipt(
            self.expanded.domain, phase.provider_descriptor, duplicate
        )
        self.assertEqual(
            duplicate_receipt["duplicate_observation_item_ids"],
            [original["observation_item_id"]],
        )
        foreign = copy.deepcopy(terminal)
        foreign["observation_outcomes"][0]["provider_run_id"] = "f" * 64
        with self.assertRaises(
            observation_app.RelationObservationSourceOperationProtocolError
        ):
            observation_app.validate_relation_observation_source_operation_terminal_document(
                foreign, request=request.document
            )

    def test_rpif_013_parser_is_explicitly_pinned_to_python_310(self) -> None:
        raw = (
            b"match value:\n"
            b"    case _:\n"
            b"        import os, sys as system\n"
            b"        from ..pkg import value, other as alias\n"
        )
        with mock.patch.object(
            provider.ast, "parse", wraps=provider.ast.parse
        ) as parse:
            occurrences = provider.import_alias_occurrences(raw)
        self.assertEqual(parse.call_args.kwargs["feature_version"], (3, 10))
        self.assertEqual(
            occurrences,
            (
                {
                    "start_byte": 33,
                    "end_byte": 57,
                    "alias_ordinal": 0,
                    "lexical_child_ordinal": 1,
                    "attributes": {
                        "import_form": "IMPORT",
                        "relative_level": 0,
                        "module_parts": ["os"],
                        "imported_name": None,
                        "alias_name": None,
                    },
                },
                {
                    "start_byte": 33,
                    "end_byte": 57,
                    "alias_ordinal": 1,
                    "lexical_child_ordinal": 2,
                    "attributes": {
                        "import_form": "IMPORT",
                        "relative_level": 0,
                        "module_parts": ["sys"],
                        "imported_name": None,
                        "alias_name": "system",
                    },
                },
                {
                    "start_byte": 66,
                    "end_byte": 105,
                    "alias_ordinal": 0,
                    "lexical_child_ordinal": 3,
                    "attributes": {
                        "import_form": "FROM_IMPORT",
                        "relative_level": 2,
                        "module_parts": ["pkg"],
                        "imported_name": "value",
                        "alias_name": None,
                    },
                },
                {
                    "start_byte": 66,
                    "end_byte": 105,
                    "alias_ordinal": 1,
                    "lexical_child_ordinal": 4,
                    "attributes": {
                        "import_form": "FROM_IMPORT",
                        "relative_level": 2,
                        "module_parts": ["pkg"],
                        "imported_name": "other",
                        "alias_name": "alias",
                    },
                },
            ),
        )

    def test_rpif_014_extension_rank_collision_fails_closed(self) -> None:
        raw = b"import os, sys\n"
        with mock.patch.object(
            provider, "_extension_rank", return_value=(0, 0, "IMPORT", 0, b"x")
        ):
            with self.assertRaises(provider.RelationImportFormProviderFailed):
                provider.import_alias_occurrences(raw)

    def test_rpif_015_equal_bytes_do_not_reuse_provider_run_identity(self) -> None:
        first = self._provider_request(self.expanded)
        binding = corrected_import_form_relation_observation_bindings()[1]
        classification = classify_language_support(self.expanded.inputs)
        projection = build_relation_observation_source_operation_projection(
            classification,
            binding.descriptor,
            self.expanded.fact_set,
            self.expanded.domain,
        )
        second_document = (
            observation_app.build_relation_observation_source_operation_request_document(
                inputs=self.expanded.inputs,
                derivation_id="rpif-different-attempt",
                request_provenance=_owned_request_provenance(self.expanded.inputs),
                descriptor=binding.descriptor,
                fact_set_document=self.expanded.fact_set,
                observation_domain=self.expanded.domain,
                classification=classification,
                projection=projection,
            )
        )
        second = observation_app.validate_relation_observation_source_operation_request_document(
            second_document, launch_key=binding.launch_key
        )
        self.assertEqual(first.source_blobs_by_path_hex, second.source_blobs_by_path_hex)
        self.assertEqual(first.document["fact_set_digest"], second.document["fact_set_digest"])
        self.assertNotEqual(first.provider_run_id, second.provider_run_id)

    def test_utf8_sig_source_offsets_bind_to_authoritative_facts(self) -> None:
        facts = [
            item
            for item in self.utf8_sig.fact_set["facts"]
            if item["fact_kind"] == "IMPORT_DECLARATION"
        ]
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["source_anchor"]["start_byte"], 3)
        lexical = next(
            item
            for item in self.utf8_sig.result.merged_candidates_copy()
            if item["relation_kind"] == "LEXICAL_CONTAINS"
        )
        self.assertEqual(lexical["target"]["fact_id"], facts[0]["fact_id"])

    def test_successor_reuses_private_qualification_and_admission(self) -> None:
        self.assertEqual(self.expanded.result.qualification_status, "QUALIFIED")
        self.assertEqual(
            self.expanded.result.candidate_composition_status, "CONSISTENT"
        )
        admitted = admit_relation_set_for_private_closed_proof(self.expanded.result)
        self.assertEqual(
            admitted.admitted_relation_ids,
            tuple(
                item["relation_id"]
                for item in self.expanded.result.merged_candidates_copy()
            ),
        )

    @staticmethod
    def _provider_request(world):
        return world.requests["import-form-observation-b"]

    @staticmethod
    def _request_copy(request):
        return SimpleNamespace(
            document=copy.deepcopy(request.document),
            descriptor=request.descriptor,
            provider_run_id=request.provider_run_id,
            facts_by_id=copy.deepcopy(request.facts_by_id),
            observation_items_by_id=copy.deepcopy(request.observation_items_by_id),
            source_blobs_by_path_hex=copy.deepcopy(request.source_blobs_by_path_hex),
        )

    def _assert_each_import_has_two_relations(self, world, facts) -> None:
        by_fact = {fact["fact_id"]: set() for fact in facts}
        for relation in world.result.merged_candidates_copy():
            if relation["relation_kind"] == "LEXICAL_CONTAINS":
                fact_id = relation["target"]["fact_id"]
            else:
                fact_id = relation["source_fact_id"]
            if fact_id in by_fact:
                by_fact[fact_id].add(relation["relation_kind"])
        self.assertEqual(
            {frozenset(value) for value in by_fact.values()},
            {frozenset({"LEXICAL_CONTAINS", "IMPORT_TARGET_LITERAL"})},
        )


if __name__ == "__main__":
    unittest.main()
