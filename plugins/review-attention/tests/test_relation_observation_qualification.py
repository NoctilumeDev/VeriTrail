from __future__ import annotations

import copy
import inspect
import json
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

from support import create_fixture_repository  # noqa: E402
from test_execution_cell import _canonical_artifact, _seal_policy  # noqa: E402
import test_relation_derivation as relation_test_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _relation_observation_application as observation_app,
)
from veritrail_review import (  # noqa: E402
    _relation_observation_provider as observation_provider,
)
from veritrail_review import (  # noqa: E402
    _relation_observation_qualification as qualification,
)
from veritrail_review._execution_cell import _owned_request_provenance  # noqa: E402
from veritrail_review._execution_cell_application import (  # noqa: E402
    canonicalize_candidates,
    validate_request_document,
)
from veritrail_review._execution_cell_binding import (  # noqa: E402
    ProviderBinding,
    ProviderDescriptor,
)
from veritrail_review._execution_cell_values import (  # noqa: E402
    PhaseStatus,
    ProviderRunStatus,
)
from veritrail_review._multi_provider_applicability import (  # noqa: E402
    closed_test_multi_provider_bindings,
)
from veritrail_review._multi_provider_fact_composition import (  # noqa: E402
    _ClosedProviderRun,
    _fact_set_document,
    _merge_completed_sources,
)
from veritrail_review._relation_derivation_values import (  # noqa: E402
    _RelationDerivationError,
    _RelationDerivationFailureCode,
)
from veritrail_review._relation_observation_binding import (  # noqa: E402
    closed_test_relation_observation_bindings,
)
from veritrail_review._relation_observation_domain import (  # noqa: E402
    build_declared_relation_observation_domain,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402
from veritrail_review.derivation_input_contracts import DerivationInputSet  # noqa: E402
from veritrail_review.errors import (  # noqa: E402
    DerivationExecutionCellError,
    DerivationExecutionCellFailureCode,
)


class RelationObservationQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        support = relation_test_support.RelationDerivationTests
        support.setUpClass()
        cls.helper = support()
        cls.inputs = support.import_inputs
        cls.empty_inputs = support.relation_inputs
        cls.two_import_fixture = create_fixture_repository(
            support.root / "two-import-repository",
            nested_source=b"import pkg.mod\nimport other\n",
        )
        cls.two_import_inputs = support._inputs(
            fixture=cls.two_import_fixture,
            name="two-import",
        )
        cls.contexts: list[object] = []
        cls.admitted_contexts: list[object] = []
        cls.positive = cls._run_with_import_facts(
            inputs=cls.inputs,
            derivation_id="rq-positive",
            collect_contexts=True,
        )
        cls.empty = qualification.run_closed_test_relation_observation_qualification(
            cls.empty_inputs,
            derivation_id="rq-empty",
            bindings=qualification.closed_test_relation_observation_qualification_bindings(),
        )
        cls.conflicting = cls._run_with_import_facts(
            inputs=cls.two_import_inputs,
            derivation_id="rq-conflict",
            two_imports=True,
            relation_launch_key="observation-b-conflict",
        )
        cls.a_unavailable = cls._run_with_import_facts(
            inputs=cls.inputs,
            derivation_id="rq-a-unavailable",
            relation_launch_key="observation-a-unavailable",
        )
        cls.fact_set = cls._fact_set_for_result(cls.positive, cls.inputs)

    @classmethod
    def tearDownClass(cls) -> None:
        relation_test_support.RelationDerivationTests.tearDownClass()

    @classmethod
    def _run_with_import_facts(
        cls,
        *,
        inputs,
        derivation_id: str,
        two_imports: bool = False,
        relation_launch_key: str | None = None,
        collect_contexts: bool = False,
    ):
        original_fact_run = qualification._run_prepared_closed_test_execution_attempt
        original_build = qualification.build_prepared_relation_observation_attempt
        original_admit = qualification.admit_derivation_budget

        def fact_run(prepared):
            phase = original_fact_run(prepared)
            if two_imports:
                return cls._phase_with_two_imports(prepared, phase)
            return cls.helper._phase_with_module_and_import(prepared, phase)

        def build(*args, **kwargs):
            binding = kwargs["binding"]
            if collect_contexts:
                cls.contexts.append(kwargs["context"])
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
            if collect_contexts:
                cls.admitted_contexts.append(context)
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
            return qualification.run_closed_test_relation_observation_qualification(
                inputs,
                derivation_id=derivation_id,
                bindings=qualification.closed_test_relation_observation_qualification_bindings(),
            )

    @classmethod
    def _phase_with_two_imports(cls, prepared, phase):
        request = validate_request_document(
            prepared.request_document,
            launch_key=prepared.binding.launch_key,
        )
        path_hex = sorted(request.supported_paths)[0]
        size = request.source_sizes_by_path_hex[path_hex]
        specs = [
            (0, 14, ["pkg", "mod"]),
            (15, 27, ["other"]),
        ]
        candidates = [
            {
                "subject_space": "MODULE_ENTITY",
                "fact_kind": "MODULE",
                "source_anchor": {
                    "git_path": {
                        "path_kind": "GIT_PATH",
                        "git_path_hex": path_hex,
                    },
                    "start_byte": 0,
                    "end_byte": size,
                },
                "local_ordinal": 0,
                "semantic_attributes": {"module_key_parts": None},
            }
        ]
        for start, end, parts in specs:
            candidates.append(
                {
                    "subject_space": "IMPORT_ALIAS",
                    "fact_kind": "IMPORT_DECLARATION",
                    "source_anchor": {
                        "git_path": {
                            "path_kind": "GIT_PATH",
                            "git_path_hex": path_hex,
                        },
                        "start_byte": start,
                        "end_byte": end,
                    },
                    "local_ordinal": 0,
                    "semantic_attributes": {
                        "import_form": "IMPORT",
                        "relative_level": 0,
                        "module_parts": parts,
                        "imported_name": None,
                        "alias_name": None,
                    },
                }
            )
        facts = canonicalize_candidates(request, candidates)
        return replace(
            phase,
            canonical_fact_bytes=tuple(canonical_json_bytes(item) for item in facts),
            reported_fact_ids=tuple(item["fact_id"] for item in facts),
        )

    @staticmethod
    def _fact_set_for_result(result, inputs):
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
        return _fact_set_document(inputs, facts, conflicts)[0]

    def test_rq_001_004_exact_preflight_rejects_missing_extra_drift_and_optional(self) -> None:
        bindings = qualification.closed_test_relation_observation_qualification_bindings()
        requirements, fact_bindings, admitted = (
            qualification._admit_observation_qualification_applicability(
                self.inputs,
                derivation_id="preflight",
                bindings=bindings,
                cancellation_requested=None,
                transport_limits=qualification.DEFAULT_TRANSPORT_LIMITS,
            )
        )
        self.assertEqual(
            requirements,
            {"python-ast": True, "review-relation-derivation": True},
        )
        self.assertEqual(fact_bindings, closed_test_multi_provider_bindings())
        self.assertEqual(admitted, closed_test_relation_observation_bindings())
        for invalid in (
            bindings[:-1],
            (*bindings, bindings[-1]),
            (
                *bindings[:-1],
                ProviderBinding(
                    ProviderDescriptor(
                        **{
                            **bindings[-1].descriptor.document(),
                            "provider_version": "drift",
                        }
                    ),
                    bindings[-1].launch_key,
                ),
            ),
        ):
            with self.assertRaises(_RelationDerivationError) as caught:
                qualification._admit_observation_qualification_applicability(
                    self.inputs,
                    derivation_id="preflight-invalid",
                    bindings=invalid,
                    cancellation_requested=None,
                    transport_limits=qualification.DEFAULT_TRANSPORT_LIMITS,
                )
            self.assertEqual(
                caught.exception.code,
                _RelationDerivationFailureCode.APPLICABILITY_BINDING_MISMATCH,
            )
        policy = self.inputs.review_policy_document_copy()
        policy["provider_requirements"][1]["required"] = False
        _seal_policy(policy)
        optional = DerivationInputSet.create(
            source_snapshot_canonical_bytes=self.inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=self.inputs.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=self.inputs.verified_blob_bytes_by_object_identity,
            source_snapshot_digest=self.inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=self.inputs.derivation_profile_digest,
        )
        with self.assertRaises(_RelationDerivationError):
            qualification._admit_observation_qualification_applicability(
                optional,
                derivation_id="optional",
                bindings=bindings,
                cancellation_requested=None,
                transport_limits=qualification.DEFAULT_TRANSPORT_LIMITS,
            )

    def test_rq_005_006_domain_and_real_complete_empty(self) -> None:
        domain = self.positive.observation_domain_copy()
        self.assertEqual(len(domain["observation_items"]), 2)
        self.assertEqual(
            [
                len(item["assigned_observation_item_ids"])
                for item in domain["provider_responsibilities"]
            ],
            [1, 2],
        )
        self.assertEqual(self.empty.observation_domain_copy()["observation_items"], [])
        self.assertEqual(self.empty.qualification_status, "QUALIFIED")
        self.assertEqual(
            [item["execution_status"] for item in self.empty.observation_receipts_copy()],
            ["COMPLETED", "COMPLETED"],
        )

    def test_rq_007_closed_shape_rejects_unsupported_fact_without_shrinking(self) -> None:
        altered = copy.deepcopy(self.fact_set)
        altered["facts"][1]["fact_kind"] = "FUNCTION_DECLARATION"
        altered["fact_set_digest"] = qualification._fact_set_document(
            self.inputs, altered["facts"], []
        )[1]
        with self.assertRaises(Exception):
            build_declared_relation_observation_domain(
                self.inputs,
                altered,
                closed_test_relation_observation_bindings(),
            )

    def test_rq_008_009_identity_binds_fact_set_domain_and_assignment(self) -> None:
        phase = self.positive.relation_phase_results[0]
        descriptor = phase.provider_descriptor
        assigned = phase.assigned_observation_item_ids
        digest = observation_app.relation_observation_provider_operands_digest(
            self.inputs,
            descriptor,
            self.positive.fact_set_digest,
            self.positive.observation_domain_digest,
            assigned,
        )
        self.assertEqual(digest, phase.operands_digest)
        self.assertNotEqual(
            digest,
            observation_app.relation_observation_provider_operands_digest(
                self.inputs,
                descriptor,
                "0" * 64,
                self.positive.observation_domain_digest,
                assigned,
            ),
        )
        self.assertNotEqual(
            digest,
            observation_app.relation_observation_provider_operands_digest(
                self.inputs,
                descriptor,
                self.positive.fact_set_digest,
                self.positive.observation_domain_digest,
                (*assigned, "f" * 64),
            ),
        )
        domain = self.positive.observation_domain_copy()
        projection = {
            key: copy.deepcopy(value)
            for key, value in domain.items()
            if key not in {"policy_digest", "observation_domain_digest"}
        }
        projection["provider_responsibilities"][0][
            "assigned_observation_item_ids"
        ].append("f" * 64)
        self.assertNotEqual(
            self.positive.observation_domain_digest,
            semantic_digest(
                "veritrail.review.relation-observation-domain/0.1",
                projection,
            ),
        )

    def test_rq_010_011_021_terminal_and_observation_closure_are_independent(self) -> None:
        domain = self.positive.observation_domain_copy()
        descriptor_b = closed_test_relation_observation_bindings()[1].descriptor
        not_started = qualification._observation_receipt(domain, descriptor_b, None)
        self.assertEqual(not_started["execution_status"], "NOT_STARTED")
        self.assertTrue(not_started["missing_observation_item_ids"])
        receipts = self.a_unavailable.observation_receipts_copy()
        self.assertEqual(receipts[0]["execution_status"], "UNAVAILABLE")
        self.assertEqual(receipts[1]["execution_status"], "COMPLETED")
        self.assertEqual(
            self.a_unavailable.required_source_set_terminal_closure, "COMPLETE"
        )
        self.assertEqual(
            self.a_unavailable.required_observation_closure, "INCOMPLETE"
        )
        self.assertEqual(
            self.a_unavailable.candidate_composition_status, "NOT_COMPOSED"
        )

    def test_rq_012_013_completed_empty_or_partial_outcomes_do_not_close(self) -> None:
        domain = self.positive.observation_domain_copy()
        phase = self.positive.relation_phase_results[1]
        empty = replace(
            phase,
            canonical_relation_bytes=(),
            observation_outcome_bytes=(),
            reported_relation_ids=(),
        )
        receipt = qualification._observation_receipt(
            domain, phase.provider_descriptor, empty
        )
        self.assertEqual(receipt["execution_status"], "COMPLETED")
        self.assertEqual(
            receipt["missing_observation_item_ids"],
            list(phase.assigned_observation_item_ids),
        )
        outcomes = phase.observation_outcomes_copy()
        relations = {item["relation_id"]: item for item in phase.canonical_relations_copy()}
        kept = outcomes[:1]
        kept_relations = [relations[item["reported_relation_ids"][0]] for item in kept]
        partial = replace(
            phase,
            canonical_relation_bytes=tuple(canonical_json_bytes(item) for item in kept_relations),
            observation_outcome_bytes=tuple(canonical_json_bytes(item) for item in kept),
            reported_relation_ids=tuple(item["relation_id"] for item in kept_relations),
        )
        partial_receipt = qualification._observation_receipt(
            domain, phase.provider_descriptor, partial
        )
        self.assertEqual(len(partial_receipt["accepted_observation_outcomes"]), 1)
        self.assertEqual(len(partial_receipt["missing_observation_item_ids"]), 1)

    def test_rq_014_017_outcome_accounting_rejects_negative_duplicate_and_mismatch(self) -> None:
        domain = self.positive.observation_domain_copy()
        phase = self.positive.relation_phase_results[1]
        item_id = phase.assigned_observation_item_ids[0]
        negative = observation_app.build_provider_outcome(
            provider_run_id_value=phase.provider_run_id,
            observation_item_id=item_id,
            disposition="NO_CANDIDATE_OBSERVED",
            reported_relation_ids=[],
        )
        invalid_negative = replace(
            phase,
            canonical_relation_bytes=(),
            observation_outcome_bytes=(canonical_json_bytes(negative),),
            reported_relation_ids=(),
        )
        receipt = qualification._observation_receipt(
            domain, phase.provider_descriptor, invalid_negative
        )
        self.assertEqual(receipt["invalid_outcome_ids"], [negative["observation_outcome_id"]])
        original = phase.observation_outcomes_copy()[0]
        duplicate = replace(
            phase,
            observation_outcome_bytes=(
                canonical_json_bytes(original),
                canonical_json_bytes(original),
            ),
        )
        duplicate_receipt = qualification._observation_receipt(
            domain, phase.provider_descriptor, duplicate
        )
        self.assertEqual(
            duplicate_receipt["duplicate_observation_item_ids"],
            [original["observation_item_id"]],
        )
        other_relation = next(
            item
            for item in phase.canonical_relations_copy()
            if item["relation_id"] != original["reported_relation_ids"][0]
        )
        mismatched = observation_app.build_provider_outcome(
            provider_run_id_value=phase.provider_run_id,
            observation_item_id=original["observation_item_id"],
            disposition="CANDIDATE_REPORTED",
            reported_relation_ids=[other_relation["relation_id"]],
        )
        mismatch_phase = replace(
            phase,
            observation_outcome_bytes=(canonical_json_bytes(mismatched),),
        )
        mismatch_receipt = qualification._observation_receipt(
            domain, phase.provider_descriptor, mismatch_phase
        )
        self.assertIn(other_relation["relation_id"], mismatch_receipt["unexpected_relation_ids"])
        self.assertTrue(mismatch_receipt["unreferenced_relation_ids"])

        lexical = next(
            item
            for item in phase.canonical_relations_copy()
            if item["relation_kind"] == "LEXICAL_CONTAINS"
        )
        extra = copy.deepcopy(lexical)
        extra["local_ordinal"] += 10
        extra["relation_subject_digest"] = semantic_digest(
            "veritrail.review.relation-subject/0.1",
            {
                "source_snapshot_digest": phase.source_snapshot_digest,
                "derivation_profile_digest": phase.derivation_profile_digest,
                "relation_space": extra["relation_space"],
                "source_fact_id": extra["source_fact_id"],
                "local_ordinal": extra["local_ordinal"],
            },
        )
        extra["relation_id"] = semantic_digest(
            "veritrail.review.structural-relation/0.1",
            {
                "relation_subject_digest": extra["relation_subject_digest"],
                "relation_kind": extra["relation_kind"],
                "target": extra["target"],
                "semantic_attributes": {},
            },
        )
        lexical_outcome = next(
            item
            for item in phase.observation_outcomes_copy()
            if lexical["relation_id"] in item["reported_relation_ids"]
        )
        two_candidate_outcome = observation_app.build_provider_outcome(
            provider_run_id_value=phase.provider_run_id,
            observation_item_id=lexical_outcome["observation_item_id"],
            disposition="CANDIDATE_REPORTED",
            reported_relation_ids=[lexical["relation_id"], extra["relation_id"]],
        )
        relations = sorted(
            (*phase.canonical_relations_copy(), extra),
            key=lambda item: item["relation_id"],
        )
        outcomes = [
            two_candidate_outcome
            if item["observation_item_id"]
            == lexical_outcome["observation_item_id"]
            else item
            for item in phase.observation_outcomes_copy()
        ]
        outcomes.sort(
            key=lambda item: (
                item["observation_item_id"], item["observation_outcome_id"]
            )
        )
        two_candidates = replace(
            phase,
            canonical_relation_bytes=tuple(
                canonical_json_bytes(item) for item in relations
            ),
            observation_outcome_bytes=tuple(
                canonical_json_bytes(item) for item in outcomes
            ),
            reported_relation_ids=tuple(item["relation_id"] for item in relations),
        )
        cardinality_receipt = qualification._observation_receipt(
            domain, phase.provider_descriptor, two_candidates
        )
        self.assertIn(
            two_candidate_outcome["observation_outcome_id"],
            cardinality_receipt["invalid_outcome_ids"],
        )
        self.assertIn(extra["relation_id"], cardinality_receipt["unreferenced_relation_ids"])

    def test_rq_015_unassigned_outcome_is_unexpected_not_a_smaller_domain(self) -> None:
        domain = self.positive.observation_domain_copy()
        phase = self.positive.relation_phase_results[0]
        unexpected = observation_app.build_provider_outcome(
            provider_run_id_value=phase.provider_run_id,
            observation_item_id="f" * 64,
            disposition="CANDIDATE_REPORTED",
            reported_relation_ids=["e" * 64],
        )
        altered = replace(
            phase,
            canonical_relation_bytes=(),
            observation_outcome_bytes=(canonical_json_bytes(unexpected),),
            reported_relation_ids=(),
        )
        receipt = qualification._observation_receipt(
            domain, phase.provider_descriptor, altered
        )
        self.assertEqual(receipt["unexpected_observation_item_ids"], ["f" * 64])
        self.assertEqual(
            receipt["missing_observation_item_ids"],
            list(phase.assigned_observation_item_ids),
        )

    def test_rq_018_same_id_unions_provenance_without_collapsing_receipts(self) -> None:
        lexical = next(
            item
            for item in self.positive.merged_candidates_copy()
            if item["relation_kind"] == "LEXICAL_CONTAINS"
        )
        self.assertEqual(len(lexical["provenance_refs"]), 2)
        receipts = self.positive.observation_receipts_copy()
        self.assertEqual(len(receipts), 2)
        self.assertEqual(
            sum(
                1
                for receipt in receipts
                for outcome in receipt["accepted_observation_outcomes"]
                if lexical["relation_id"] in outcome["reported_relation_ids"]
            ),
            2,
        )

    def test_rq_019_conflict_can_be_qualified_and_has_no_winner(self) -> None:
        self.assertEqual(self.conflicting.required_observation_closure, "COMPLETE")
        self.assertEqual(self.conflicting.candidate_composition_status, "CONFLICTING")
        self.assertEqual(self.conflicting.qualification_status, "QUALIFIED")
        conflicts = self.conflicting.private_conflicts_copy()
        self.assertGreaterEqual(len(conflicts), 1)
        candidate_ids = {item["relation_id"] for item in self.conflicting.merged_candidates_copy()}
        for conflict in conflicts:
            self.assertTrue(set(conflict["candidate_relation_ids"]).issubset(candidate_ids))

    def test_rq_020_same_id_different_semantics_is_integrity_not_conflict(self) -> None:
        phase_a, phase_b = self.positive.relation_phase_results
        forged = copy.deepcopy(phase_b.canonical_relations_copy()[0])
        forged["relation_id"] = phase_a.canonical_relations_copy()[0]["relation_id"]
        forged["local_ordinal"] += 1
        forged_phase = replace(
            phase_b,
            canonical_relation_bytes=(canonical_json_bytes(forged),),
        )
        with self.assertRaises(qualification._RelationIdentityCollision):
            qualification._compose_candidates((phase_a, forged_phase))

    def test_rq_022_interruption_stops_successor_and_retains_no_prefix_output(self) -> None:
        original = qualification.run_prepared_relation_observation_attempt
        calls: list[str] = []

        def interrupted(prepared):
            phase = original(prepared)
            calls.append(phase.provider_descriptor.provider_id)
            return replace(
                phase,
                provider_run_status=ProviderRunStatus.INTERRUPTED,
                phase_status=PhaseStatus.INTERRUPTED,
                diagnostic_code="EXECUTION_CANCELLED",
                canonical_relation_bytes=(),
                observation_outcome_bytes=(),
                reported_relation_ids=(),
            )

        with mock.patch.object(
            qualification,
            "run_prepared_relation_observation_attempt",
            side_effect=interrupted,
        ):
            result = self._run_with_import_facts(
                inputs=self.inputs,
                derivation_id="rq-interrupted",
            )
        self.assertEqual(calls, ["closed-relation-provider-a"])
        self.assertEqual(len(result.relation_phase_results), 1)
        self.assertEqual(result.candidate_composition_status, "NOT_COMPOSED")
        self.assertEqual(result.qualification_status, "NOT_QUALIFIED")
        self.assertEqual(result.merged_candidates_copy(), ())
        self.assertIn("REQUIRED_SOURCE_INTERRUPTED", result.reason_codes)
        self.assertIn("REQUIRED_SOURCE_NOT_STARTED", result.reason_codes)
        self.assertIn("SHARED_CONTEXT_FAILURE", result.reason_codes)

    def test_rq_022_release_failure_stops_all_successors_and_cannot_qualify(self) -> None:
        calls = 0

        def release_failed(_prepared):
            nonlocal calls
            calls += 1
            raise DerivationExecutionCellError(
                DerivationExecutionCellFailureCode.RELEASE_FAILED
            )

        with mock.patch.object(
            qualification,
            "run_prepared_relation_observation_attempt",
            side_effect=release_failed,
        ):
            result = self._run_with_import_facts(
                inputs=self.inputs,
                derivation_id="rq-release-failed",
            )
        self.assertEqual(calls, 1)
        self.assertEqual(result.relation_phase_results, ())
        self.assertEqual(result.qualification_status, "NOT_QUALIFIED")
        self.assertEqual(result.candidate_composition_status, "NOT_COMPOSED")
        self.assertIn("RELEASE_FAILURE", result.reason_codes)
        self.assertIn("REQUIRED_SOURCE_NOT_STARTED", result.reason_codes)

    def test_rq_023_shared_budget_is_not_refreshed_for_relation_sources(self) -> None:
        self.assertEqual(len(self.admitted_contexts), 1)
        self.assertEqual(len(self.contexts), 2)
        self.assertIs(self.contexts[0], self.admitted_contexts[0])
        self.assertIs(self.contexts[0], self.contexts[1])

    def test_rq_024_025_import_literal_is_conservative_and_parser_is_real(self) -> None:
        relation = next(
            item
            for item in self.positive.merged_candidates_copy()
            if item["relation_kind"] == "IMPORT_TARGET_LITERAL"
        )
        self.assertEqual(relation["target"]["module_parts"], ["pkg", "mod"])
        self.assertEqual(relation["target"]["resolution_status"], "UNRESOLVED")
        self.assertEqual(relation["target"]["topology_status"], "UNKNOWN")
        self.assertEqual(relation["target"]["resolved_fact_ids"], [])
        domain = build_declared_relation_observation_domain(
            self.inputs,
            self.fact_set,
            closed_test_relation_observation_bindings(),
        )
        descriptor = closed_test_relation_observation_bindings()[1].descriptor
        request_document = observation_app.build_relation_observation_request_document(
            inputs=self.inputs,
            derivation_id="parser-proof",
            request_provenance=_owned_request_provenance(self.inputs),
            descriptor=descriptor,
            fact_set_document=self.fact_set,
            observation_domain=domain,
        )
        request = observation_app.validate_relation_observation_request_document(
            request_document, launch_key="observation-b"
        )
        with mock.patch.object(
            observation_provider,
            "_closed_deterministic_test_parser",
            wraps=observation_provider._closed_deterministic_test_parser,
        ) as parser:
            candidates, outcomes = observation_provider.run_closed_relation_observation_provider(
                request, launch_key="observation-b"
            )
        self.assertGreaterEqual(parser.call_count, 1)
        self.assertEqual(len(candidates), 2)
        self.assertEqual(len(outcomes), 2)

    def test_rq_026_027_private_result_is_owned_unpublished_and_unexported(self) -> None:
        domain = self.positive.observation_domain_copy()
        receipts = self.positive.observation_receipts_copy()
        candidates = self.positive.merged_candidates_copy()
        domain["observation_items"].clear()
        receipts[0]["assigned_observation_item_ids"].clear()
        candidates[0]["provenance_refs"].clear()
        self.assertNotEqual(domain, self.positive.observation_domain_copy())
        self.assertNotEqual(receipts, self.positive.observation_receipts_copy())
        self.assertNotEqual(candidates, self.positive.merged_candidates_copy())
        parameters = inspect.signature(
            qualification.run_closed_test_relation_observation_qualification
        ).parameters
        for forbidden in ("output_path", "publisher", "relation_set"):
            self.assertNotIn(forbidden, parameters)
        import veritrail_review

        self.assertFalse(
            hasattr(
                veritrail_review,
                "run_closed_test_relation_observation_qualification",
            )
        )

    def test_rq_028_cross_runtime_golden_identities(self) -> None:
        self.assertEqual(
            self.positive.observation_domain_digest,
            "a4e6d12ad43f789fdfc1e370db77080f3ddf1855507c93b9e88818a9bbeae6b9",
        )
        self.assertEqual(
            self.positive.qualification_digest,
            "8c5fb7b038980920a2fedcf1010c8fc1cb9e8b6103486d308584075b6f173faa",
        )
        self.assertEqual(
            [item["relation_id"] for item in self.positive.merged_candidates_copy()],
            [
                "4e42c7e39960bd9e247da522260afbcd36aa9df49e5d4ac5f9fad6d927df02d2",
                "9872c294f8e9c15128867029ec9fd5845b3ce6cc1220aa8f5cc036605abccdc1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
