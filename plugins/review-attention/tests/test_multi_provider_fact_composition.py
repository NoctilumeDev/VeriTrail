from __future__ import annotations

import copy
import inspect
import json
import sys
import tempfile
import time
import types
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
SCHEMA_ROOT = REPOSITORY_ROOT / "schemas"
FIXTURE_ROOT = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "review-r1-derivation-input-0.1"
    / "reference-lab"
)
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from support import create_fixture_repository, git_executable  # noqa: E402
from test_execution_cell import (  # noqa: E402
    _canonical_artifact,
    _policy_document,
    _seal_policy,
)
from veritrail_review import (  # noqa: E402
    DerivationInputRequest,
    DerivationInputRuntime,
    SourceSnapshotRequest,
    SourceSnapshotRuntime,
    SourceSnapshotSpec,
    bind_derivation_inputs,
    create_source_snapshot,
)
from veritrail_review._execution_cell_binding import (  # noqa: E402
    ProviderBinding,
    closed_test_binding,
)
from veritrail_review._execution_cell import run_closed_test_execution_cell  # noqa: E402
from veritrail_review.errors import DerivationExecutionCellError  # noqa: E402
from veritrail_review._execution_cell_values import (  # noqa: E402
    PhaseStatus,
    ProviderRunStatus,
)
from veritrail_review import _multi_provider_fact_composition as multi  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402


class MultiProviderFactCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._temporary = tempfile.TemporaryDirectory(prefix="veritrail-r1-multi-")
        cls.root = Path(cls._temporary.name)
        cls.fixture = create_fixture_repository(cls.root / "repository")
        cls.required_inputs = cls._inputs(name="required")
        cls.advisory_inputs = cls._inputs(name="advisory", include_advisory=True)
        schemas = {
            path.name: json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(SCHEMA_ROOT.glob("review-*.schema.json"))
        }
        registry = Registry().with_resources(
            [
                (schema["$id"], Resource.from_contents(schema))
                for schema in schemas.values()
            ]
        )
        cls.fact_set_validator = Draft202012Validator(
            schemas["review-fact-set-0.1.schema.json"],
            registry=registry,
            format_checker=FormatChecker(),
        )
        cls.evidence_validator = Draft202012Validator(
            schemas["review-derivation-evidence-0.1.1.schema.json"],
            registry=registry,
            format_checker=FormatChecker(),
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary.cleanup()

    @classmethod
    def _inputs(
        cls,
        *,
        name: str,
        include_advisory: bool = False,
        wall_clock_ms: int = 10_000,
    ):
        root = cls.root / name
        root.mkdir()
        publication = create_source_snapshot(
            SourceSnapshotRequest(
                spec=SourceSnapshotSpec(
                    repository_id="fixture/repository",
                    commit_oid=cls.fixture.commit_oid,
                    analysis_root={
                        "path_kind": "GIT_PATH",
                        "git_path_hex": b"pkg".hex(),
                    },
                ),
                repository_path=cls.fixture.path,
                output_directory=root / "snapshot-publication",
            ),
            runtime=SourceSnapshotRuntime(git_executable=git_executable()),
        )
        snapshot_path = root / "source-snapshot.json"
        snapshot_path.write_bytes(publication.snapshot.canonical_bytes)
        snapshot = publication.snapshot.document_copy()
        policy = _policy_document(snapshot, wall_clock_ms=wall_clock_ms)
        if include_advisory:
            policy["provider_requirements"].append(
                {
                    "capability_id": "python-ast-advisory",
                    "required": False,
                    "composition_mode": "CUMULATIVE",
                }
            )
            _seal_policy(policy)
        policy_path = root / "review-policy.json"
        policy_path.write_bytes(_canonical_artifact(policy))
        profile_path = root / "derivation-profile.json"
        profile_path.write_bytes((FIXTURE_ROOT / "derivation-profile.json").read_bytes())
        return bind_derivation_inputs(
            DerivationInputRequest(
                source_snapshot_path=snapshot_path.resolve(),
                review_policy_path=policy_path.resolve(),
                derivation_profile_path=profile_path.resolve(),
                repository_path=cls.fixture.path.resolve(),
            ),
            runtime=DerivationInputRuntime(git_executable=git_executable()),
        )

    def _run(
        self,
        *,
        inputs=None,
        bindings=None,
        derivation_id: str = "multi-provider-attempt",
    ):
        selected = self.required_inputs if inputs is None else inputs
        if bindings is None:
            bindings = multi.closed_test_multi_provider_bindings(
                include_advisory=selected is self.advisory_inputs
            )
        return multi.run_closed_test_multi_provider_fact_composition(
            selected,
            derivation_id=derivation_id,
            bindings=bindings,
        )

    def _run_transformed(self, transform, *, inputs=None, derivation_id="transformed"):
        selected = self.required_inputs if inputs is None else inputs
        bindings = multi.closed_test_multi_provider_bindings(
            include_advisory=selected is self.advisory_inputs
        )
        original = multi._run_prepared_closed_test_execution_attempt

        def runner(prepared):
            phase = original(prepared)
            return transform(prepared, phase)

        with mock.patch.object(
            multi,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=runner,
        ):
            return multi.run_closed_test_multi_provider_fact_composition(
                selected,
                derivation_id=derivation_id,
                bindings=bindings,
            )

    @staticmethod
    def _non_success(phase, status: ProviderRunStatus, code: str):
        return replace(
            phase,
            provider_run_status=status,
            phase_status=(
                PhaseStatus.UNAVAILABLE
                if status is ProviderRunStatus.UNAVAILABLE
                else PhaseStatus.FAILED
            ),
            diagnostic_code=code,
            canonical_fact_bytes=(),
            reported_fact_ids=(),
            reported_relation_ids=(),
        )

    @staticmethod
    def _fact_variant(phase, module_part: str) -> dict[str, object]:
        fact = phase.canonical_facts_copy()[0]
        fact["semantic_attributes"] = {"module_key_parts": [module_part]}
        fact["fact_id"] = semantic_digest(
            "veritrail.review.code-fact/0.1",
            {
                "subject_key_digest": fact["subject_key_digest"],
                "fact_kind": fact["fact_kind"],
                "semantic_attributes": copy.deepcopy(fact["semantic_attributes"]),
            },
        )
        return fact

    @staticmethod
    def _phase_with_facts(phase, facts):
        ordered = sorted(facts, key=lambda item: item["fact_id"])
        return replace(
            phase,
            canonical_fact_bytes=tuple(canonical_json_bytes(item) for item in ordered),
            reported_fact_ids=tuple(item["fact_id"] for item in ordered),
        )

    def test_mp_001_002_required_profile_admits_exact_two_bindings(self) -> None:
        result = self._run()
        self.assertEqual(result.overall_execution_status, "COMPLETED")
        self.assertEqual(
            [item["provider_id"] for item in result.applicability_descriptors_copy()],
            ["closed-multi-provider-a", "closed-multi-provider-b"],
        )
        self.assertEqual(len(result.phase_results), 2)

    def test_mp_003_optional_advisory_expands_exact_binding_set(self) -> None:
        result = self._run(inputs=self.advisory_inputs)
        self.assertEqual(result.overall_execution_status, "COMPLETED")
        self.assertEqual(len(result.applicability_descriptors_copy()), 3)
        self.assertEqual(len(result.canonical_conflicts_copy()), 1)

    def test_mp_004_rejects_missing_extra_and_duplicate_bindings_pre_admission(self) -> None:
        exact = multi.closed_test_multi_provider_bindings()
        variants = (
            exact[:1],
            (*exact, closed_test_binding("stable-a")),
            (exact[0], exact[0], exact[1]),
        )
        for bindings in variants:
            with self.subTest(bindings=bindings):
                with self.assertRaises(multi._MultiProviderCompositionError) as raised:
                    self._run(bindings=bindings)
                self.assertEqual(
                    raised.exception.code,
                    multi._MultiProviderCompositionFailureCode.APPLICABILITY_BINDING_MISMATCH,
                )

    def test_mp_005_rejects_descriptor_or_handle_drift_pre_admission(self) -> None:
        exact = multi.closed_test_multi_provider_bindings()
        descriptor_drift = ProviderBinding(
            replace(exact[0].descriptor, provider_version="changed"),
            exact[0].launch_key,
        )
        handle_drift = ProviderBinding(exact[0].descriptor, "stable-a")
        for first in (descriptor_drift, handle_drift):
            with self.subTest(first=first):
                with self.assertRaises(multi._MultiProviderCompositionError):
                    self._run(bindings=(first, exact[1]))

    def test_mp_005_multi_only_binding_cannot_bypass_set_admission(self) -> None:
        with self.assertRaises(DerivationExecutionCellError):
            run_closed_test_execution_cell(
                self.required_inputs,
                derivation_id="forbidden-single-multi-provider",
                binding=closed_test_binding("multi-a"),
            )

    def test_mp_006_ambient_provider_does_not_enter_applicable_set(self) -> None:
        marker = types.ModuleType("ambient_veritrail_provider")
        with mock.patch.dict(sys.modules, {marker.__name__: marker}):
            result = self._run()
        self.assertEqual(len(result.applicability_descriptors_copy()), 2)

    def test_mp_007_023_caller_order_does_not_change_execution_order(self) -> None:
        reverse = tuple(reversed(multi.closed_test_multi_provider_bindings()))
        result = self._run(bindings=reverse)
        self.assertEqual(
            [phase.provider_descriptor.provider_id for phase in result.phase_results],
            ["closed-multi-provider-a", "closed-multi-provider-b"],
        )

    def test_mp_008_all_children_share_one_budget_context_and_deadline(self) -> None:
        observed: list[tuple[int, float]] = []
        original = multi._run_prepared_closed_test_execution_attempt

        def runner(prepared):
            observed.append(
                (id(prepared.context), prepared.context.execution_deadline_monotonic)
            )
            return original(prepared)

        with mock.patch.object(
            multi,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=runner,
        ):
            self._run()
        self.assertEqual(len(observed), 2)
        self.assertEqual(len({item[0] for item in observed}), 1)
        self.assertEqual(len({item[1] for item in observed}), 1)

    def test_mp_009_sufficient_budget_does_not_change_semantic_identity(self) -> None:
        larger = self._inputs(name="larger-budget", wall_clock_ms=20_000)
        first = self._run(derivation_id="budget-a")
        second = self._run(inputs=larger, derivation_id="budget-b")
        self.assertEqual(first.fact_set_digest, second.fact_set_digest)
        first_facts = [
            {key: value for key, value in fact.items() if key != "provenance_refs"}
            for fact in first.canonical_facts_copy()
        ]
        second_facts = [
            {key: value for key, value in fact.items() if key != "provenance_refs"}
            for fact in second.canonical_facts_copy()
        ]
        first_conflicts = [
            {
                key: value
                for key, value in conflict.items()
                if key != "provenance_refs"
            }
            for conflict in first.canonical_conflicts_copy()
        ]
        second_conflicts = [
            {
                key: value
                for key, value in conflict.items()
                if key != "provenance_refs"
            }
            for conflict in second.canonical_conflicts_copy()
        ]
        self.assertEqual(first_facts, second_facts)
        self.assertEqual(first_conflicts, second_conflicts)

    def test_mp_010_required_empty_source_does_not_cancel_other_fact(self) -> None:
        def transform(prepared, phase):
            if prepared.binding.descriptor.provider_id == "closed-multi-provider-a":
                return replace(phase, canonical_fact_bytes=(), reported_fact_ids=())
            return phase

        result = self._run_transformed(transform)
        self.assertEqual(result.overall_execution_status, "COMPLETED")
        self.assertEqual(len(result.canonical_facts_copy()), 1)
        runs = {item["provider_id"]: item for item in result.provider_runs_copy()}
        self.assertEqual(runs["closed-multi-provider-a"]["reported_fact_ids"], [])
        self.assertEqual(len(runs["closed-multi-provider-b"]["reported_fact_ids"]), 1)

    def test_mp_011_same_identity_merges_provenance_bidirectionally(self) -> None:
        result = self._run()
        fact = result.canonical_facts_copy()[0]
        runs = result.provider_runs_copy()
        self.assertEqual(len(fact["provenance_refs"]), 2)
        self.assertEqual(
            set(fact["provenance_refs"]),
            {run["provider_run_id"] for run in runs},
        )
        self.assertTrue(
            all(run["reported_fact_ids"] == [fact["fact_id"]] for run in runs)
        )

    def test_mp_012_same_id_different_semantics_is_integrity_collision(self) -> None:
        prepared = multi._prepare_closed_test_multi_provider_composition(
            self.required_inputs,
            derivation_id="collision-source",
            bindings=multi.closed_test_multi_provider_bindings(),
            cancellation_requested=None,
            transport_limits=multi.DEFAULT_TRANSPORT_LIMITS,
        )
        closed = []
        for child in prepared.child_attempts:
            phase = multi._run_prepared_closed_test_execution_attempt(child)
            closed.append(
                multi._close_provider_run(
                self.required_inputs,
                phase,
                binding=child.binding,
                request_provenance=json.loads(prepared.request_provenance_bytes),
            )
            )
        altered = json.loads(closed[0].canonical_fact_bytes[0])
        altered["semantic_attributes"] = {"module_key_parts": ["collision"]}
        closed[1] = replace(
            closed[1], canonical_fact_bytes=(canonical_json_bytes(altered),)
        )
        with self.assertRaises(multi._FactIdentityCollision):
            multi._merge_completed_sources(closed)
        result = multi._join_closed_runs(prepared, closed)
        self.assertEqual(result.overall_execution_status, "FAILED")
        self.assertIsNone(result.fact_set_document_copy())
        self.assertEqual(
            result.diagnostics_copy(),
            ({"diagnostic_code": "INTERNAL_DERIVATION_ERROR", "subject_ref": None},),
        )
        self.assertTrue(result.diagnostic_closure_available())

    def test_mp_013_015_optional_source_conflict_is_preserved(self) -> None:
        result = self._run(inputs=self.advisory_inputs)
        conflict = result.canonical_conflicts_copy()[0]
        advisory = next(
            run
            for run in result.provider_runs_copy()
            if run["capability_id"] == "python-ast-advisory"
        )
        self.assertEqual(len(conflict["candidate_fact_ids"]), 2)
        self.assertIn(advisory["provider_run_id"], conflict["provenance_refs"])

    def test_mp_014_three_candidates_form_one_sorted_conflict_group(self) -> None:
        def transform(prepared, phase):
            provider = prepared.binding.descriptor.provider_id
            part = {
                "closed-multi-provider-a": "alpha",
                "closed-multi-provider-b": "beta",
                "closed-multi-provider-advisory": "advisory",
            }[provider]
            return self._phase_with_facts(phase, [self._fact_variant(phase, part)])

        result = self._run_transformed(transform, inputs=self.advisory_inputs)
        self.assertEqual(len(result.canonical_conflicts_copy()), 1)
        conflict = result.canonical_conflicts_copy()[0]
        self.assertEqual(
            conflict["candidate_fact_ids"], sorted(conflict["candidate_fact_ids"])
        )
        self.assertEqual(len(conflict["candidate_fact_ids"]), 3)
        self.assertEqual(len(conflict["provenance_refs"]), 3)

    def test_mp_016_single_source_conflict_is_nonconformant_not_fact_conflict(self) -> None:
        def transform(prepared, phase):
            if prepared.binding.descriptor.provider_id == "closed-multi-provider-a":
                return self._phase_with_facts(
                    phase,
                    [
                        self._fact_variant(phase, "one"),
                        self._fact_variant(phase, "two"),
                    ],
                )
            return phase

        result = self._run_transformed(transform)
        self.assertEqual(result.overall_execution_status, "FAILED")
        self.assertEqual(result.canonical_conflicts_copy(), ())
        runs = {run["provider_id"]: run for run in result.provider_runs_copy()}
        self.assertEqual(
            runs["closed-multi-provider-a"]["diagnostics"][0]["diagnostic_code"],
            "NONCONFORMANT_PROVIDER_OUTPUT",
        )

    def test_mp_017_required_failure_does_not_short_circuit_later_source(self) -> None:
        observed: list[str] = []

        def transform(prepared, phase):
            provider = prepared.binding.descriptor.provider_id
            observed.append(provider)
            if provider == "closed-multi-provider-a":
                return self._non_success(
                    phase, ProviderRunStatus.FAILED, "PROVIDER_FAILED"
                )
            return phase

        result = self._run_transformed(transform)
        self.assertEqual(
            observed, ["closed-multi-provider-a", "closed-multi-provider-b"]
        )
        self.assertEqual(result.overall_execution_status, "FAILED")
        self.assertEqual(len(result.provider_runs_copy()), 2)

    def test_mp_018_failed_precedes_unavailable_without_root_cause_claim(self) -> None:
        def transform(prepared, phase):
            if prepared.binding.descriptor.provider_id.endswith("-a"):
                return self._non_success(
                    phase, ProviderRunStatus.FAILED, "PROVIDER_FAILED"
                )
            return self._non_success(
                phase, ProviderRunStatus.UNAVAILABLE, "PROVIDER_UNAVAILABLE"
            )

        result = self._run_transformed(transform)
        self.assertEqual(result.overall_execution_status, "FAILED")
        self.assertEqual(
            {item["diagnostic_code"] for item in result.diagnostics_copy()},
            {"PROVIDER_FAILED", "PROVIDER_UNAVAILABLE"},
        )

    def test_mp_019_021_required_unavailable_clears_all_final_ids(self) -> None:
        def transform(prepared, phase):
            if prepared.binding.descriptor.provider_id.endswith("-b"):
                return self._non_success(
                    phase, ProviderRunStatus.UNAVAILABLE, "PROVIDER_UNAVAILABLE"
                )
            return phase

        result = self._run_transformed(transform)
        self.assertEqual(result.overall_execution_status, "UNAVAILABLE")
        self.assertIsNone(result.fact_set_document_copy())
        self.assertTrue(
            all(run["reported_fact_ids"] == [] for run in result.provider_runs_copy())
        )
        self.assertTrue(result.diagnostic_closure_available())

    def test_mp_020_optional_non_success_is_retained_without_overriding_completed(self) -> None:
        def transform(prepared, phase):
            if prepared.binding.descriptor.capability_id == "python-ast-advisory":
                return self._non_success(
                    phase, ProviderRunStatus.UNAVAILABLE, "PROVIDER_UNAVAILABLE"
                )
            return phase

        result = self._run_transformed(transform, inputs=self.advisory_inputs)
        self.assertEqual(result.overall_execution_status, "COMPLETED")
        advisory = next(
            run
            for run in result.provider_runs_copy()
            if run["capability_id"] == "python-ast-advisory"
        )
        self.assertEqual(advisory["execution_status"], "UNAVAILABLE")
        self.assertEqual(advisory["reported_fact_ids"], [])
        self.assertEqual(len(result.diagnostics_copy()), 1)

    def test_mp_022_bidirectional_provenance_mismatch_is_rejected(self) -> None:
        result = self._run()
        document = result.evidence_projection.document_copy()
        facts = result.canonical_facts_copy()
        document["provider_runs"][0]["reported_fact_ids"] = []
        unsigned = {
            key: copy.deepcopy(value)
            for key, value in document.items()
            if key != "derivation_evidence_digest"
        }
        document["derivation_evidence_digest"] = semantic_digest(
            "veritrail.review.derivation-evidence/0.1", unsigned
        )
        with self.assertRaises(ValueError):
            multi._validate_composed_projection(document, facts=facts)

    def test_frozen_public_schemas_accept_actual_private_composition_projections(self) -> None:
        normal = self._run(derivation_id="schema-normal")
        conflict = self._run(
            inputs=self.advisory_inputs,
            derivation_id="schema-conflict",
        )

        def fail_first(prepared, phase):
            if prepared.binding.descriptor.provider_id.endswith("-a"):
                return self._non_success(
                    phase, ProviderRunStatus.FAILED, "PROVIDER_FAILED"
                )
            return phase

        diagnostic = self._run_transformed(
            fail_first,
            derivation_id="schema-diagnostic",
        )
        for result in (normal, conflict):
            self.fact_set_validator.validate(result.fact_set_document_copy())
            self.evidence_validator.validate(result.evidence_projection.document_copy())
        self.assertIsNone(diagnostic.fact_set_document_copy())
        self.evidence_validator.validate(diagnostic.evidence_projection.document_copy())

    def test_mp_024_stop_before_later_provider_creates_no_fabricated_run(self) -> None:
        original = multi._run_prepared_closed_test_execution_attempt

        def runner(prepared):
            if prepared.binding.descriptor.provider_id.endswith("-b"):
                prepared.context.request_cancellation()
            return original(prepared)

        with mock.patch.object(
            multi,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=runner,
        ):
            result = self._run()
        self.assertEqual(result.overall_execution_status, "INTERRUPTED")
        self.assertEqual(len(result.provider_runs_copy()), 1)
        self.assertIsNone(result.fact_set_document_copy())
        self.assertIsNone(result.evidence_projection)
        self.assertFalse(result.normal_continuation_permitted())
        self.assertFalse(result.diagnostic_closure_available())

    def test_mp_024_later_provider_deadline_and_memory_stop_share_parent_latch(self) -> None:
        scenarios = ("deadline", "memory")
        original = multi._run_prepared_closed_test_execution_attempt
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                inputs = self._inputs(
                    name=f"later-{scenario}",
                    wall_clock_ms=2_500,
                )

                def runner(prepared):
                    if prepared.binding.descriptor.provider_id.endswith("-b"):
                        if scenario == "deadline":
                            remaining = (
                                prepared.context.execution_deadline_monotonic
                                - time.monotonic()
                            )
                            time.sleep(max(0.0, remaining) + 0.05)
                        else:
                            prepared.context._observe_owned_memory_limit()
                    return original(prepared)

                with mock.patch.object(
                    multi,
                    "_run_prepared_closed_test_execution_attempt",
                    side_effect=runner,
                ):
                    result = self._run(
                        inputs=inputs,
                        derivation_id=f"later-{scenario}",
                    )
                self.assertEqual(result.overall_execution_status, "INTERRUPTED")
                self.assertEqual(len(result.provider_runs_copy()), 1)
                self.assertIsNone(result.fact_set_document_copy())
                self.assertIsNone(result.evidence_projection)
                self.assertFalse(result.normal_continuation_permitted())
                self.assertFalse(result.diagnostic_closure_available())

    def test_mp_025_run_local_internal_failure_continues_when_release_is_safe(self) -> None:
        def transform(prepared, phase):
            if prepared.binding.descriptor.provider_id.endswith("-a"):
                return self._non_success(
                    phase, ProviderRunStatus.FAILED, "INTERNAL_DERIVATION_ERROR"
                )
            return phase

        result = self._run_transformed(transform)
        self.assertEqual(len(result.phase_results), 2)
        self.assertEqual(result.overall_execution_status, "FAILED")
        self.assertTrue(result.diagnostic_closure_available())

    def test_mp_025_shared_wire_failure_shapes_continue_after_clean_release(self) -> None:
        for launch_key in (
            "partial-terminal",
            "duplicate-terminal",
            "trailing-terminal",
        ):
            with self.subTest(launch_key=launch_key):
                lower_phase = run_closed_test_execution_cell(
                    self.required_inputs,
                    derivation_id=f"wire-{launch_key}",
                    binding=closed_test_binding(launch_key),
                )
                self.assertEqual(lower_phase.provider_run_status, ProviderRunStatus.FAILED)
                self.assertEqual(lower_phase.phase_status, PhaseStatus.FAILED)
                self.assertEqual(lower_phase.diagnostic_code, "INTERNAL_DERIVATION_ERROR")
                self.assertEqual(lower_phase.canonical_facts_copy(), ())

                def transform(prepared, phase):
                    if prepared.binding.descriptor.provider_id.endswith("-a"):
                        return replace(
                            phase,
                            provider_run_status=lower_phase.provider_run_status,
                            phase_status=lower_phase.phase_status,
                            diagnostic_code=lower_phase.diagnostic_code,
                            canonical_fact_bytes=(),
                            reported_fact_ids=(),
                            reported_relation_ids=(),
                        )
                    return phase

                result = self._run_transformed(
                    transform,
                    derivation_id=f"wire-join-{launch_key}",
                )
                self.assertEqual(len(result.phase_results), 2)
                self.assertEqual(result.overall_execution_status, "FAILED")
                self.assertTrue(result.diagnostic_closure_available())

    def test_mp_026_owned_result_is_unchanged_by_copy_mutation(self) -> None:
        result = self._run(inputs=self.advisory_inputs)
        facts = result.canonical_facts_copy()
        conflicts = result.canonical_conflicts_copy()
        runs = result.provider_runs_copy()
        facts[0]["semantic_attributes"] = {"module_key_parts": ["mutated"]}
        conflicts[0]["candidate_fact_ids"].clear()
        runs[0]["reported_fact_ids"].clear()
        self.assertNotEqual(facts, result.canonical_facts_copy())
        self.assertNotEqual(conflicts, result.canonical_conflicts_copy())
        self.assertNotEqual(runs, result.provider_runs_copy())

    def test_mp_027_private_entry_has_no_publication_probe_and_writes_zero_files(self) -> None:
        parameters = inspect.signature(
            multi.run_closed_test_multi_provider_fact_composition
        ).parameters
        self.assertNotIn("output_path", parameters)
        self.assertNotIn("output_directory", parameters)
        self.assertNotIn("publisher", parameters)
        output = self.root / "forbidden-output"
        output.mkdir()
        self._run(derivation_id="zero-file-check")
        self.assertEqual(list(output.iterdir()), [])

    def test_mp_028_frozen_semantic_vectors_are_runtime_independent(self) -> None:
        required = self._run(derivation_id="vector-required")
        advisory = self._run(
            inputs=self.advisory_inputs,
            derivation_id="vector-advisory",
        )
        vector = {
            "required_fact_set_digest": required.fact_set_digest,
            "required_fact_ids": [
                fact["fact_id"] for fact in required.canonical_facts_copy()
            ],
            "advisory_fact_set_digest": advisory.fact_set_digest,
            "advisory_fact_ids": [
                fact["fact_id"] for fact in advisory.canonical_facts_copy()
            ],
            "advisory_conflict_ids": [
                conflict["conflict_id"]
                for conflict in advisory.canonical_conflicts_copy()
            ],
        }
        self.assertEqual(
            vector,
            {
                "required_fact_set_digest": (
                    "f466d18769a1630cfbaa4bcff01d71193475324b8d4990ceb8e3d535ce47e813"
                ),
                "required_fact_ids": [
                    "bd3fe913ed53476a9362372f88782dbbb4349fa45aa908191f5b83d049db1fc4"
                ],
                "advisory_fact_set_digest": (
                    "dada6a2ad992edc5cec3af2c8d480b0bf494c61e2996f4ae46d1c3d2982bbdbc"
                ),
                "advisory_fact_ids": [
                    "3434c02de4fc0fbc83d9593dddd6ec29bfd1bfa7c5b9235aa90ecc5a6d948c8d",
                    "bd3fe913ed53476a9362372f88782dbbb4349fa45aa908191f5b83d049db1fc4",
                ],
                "advisory_conflict_ids": [
                    "731af487d12164d26754adb241c35b6073a50d5db463ccd0daf2798e01022013"
                ],
            },
        )

    def test_private_capability_is_not_exported(self) -> None:
        import veritrail_review

        self.assertFalse(
            hasattr(
                veritrail_review,
                "run_closed_test_multi_provider_fact_composition",
            )
        )
        self.assertNotIn(
            "run_closed_test_multi_provider_fact_composition",
            veritrail_review.__all__,
        )


if __name__ == "__main__":
    unittest.main()
