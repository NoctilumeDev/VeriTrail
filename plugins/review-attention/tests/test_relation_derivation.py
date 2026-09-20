from __future__ import annotations

import copy
import inspect
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
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
from veritrail_review import _relation_derivation as relation  # noqa: E402
from veritrail_review import _relation_closed_provider as relation_provider  # noqa: E402
from veritrail_review import (  # noqa: E402
    _relation_execution_cell_application as relation_app,
)
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
from veritrail_review._relation_derivation_values import (  # noqa: E402
    _RelationDerivationError,
    _RelationDerivationFailureCode,
)
from veritrail_review._relation_execution_cell_binding import (  # noqa: E402
    closed_test_relation_binding,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402


class RelationDerivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._temporary = tempfile.TemporaryDirectory(prefix="veritrail-r1-relation-")
        cls.root = Path(cls._temporary.name)
        cls.fixture = create_fixture_repository(cls.root / "repository")
        cls.import_fixture = create_fixture_repository(
            cls.root / "import-repository",
            nested_source=b"import pkg.mod\n",
        )
        cls.invalid_fixture = create_fixture_repository(
            cls.root / "invalid-repository",
            nested_source=b"def bad(:\n",
        )
        cls.fact_only_inputs = cls._inputs(
            fixture=cls.fixture,
            name="fact-only",
            include_relation=False,
        )
        cls.relation_inputs = cls._inputs(
            fixture=cls.fixture,
            name="relation",
        )
        cls.import_inputs = cls._inputs(
            fixture=cls.import_fixture,
            name="import",
        )
        cls.invalid_inputs = cls._inputs(
            fixture=cls.invalid_fixture,
            name="invalid",
        )
        cls.advisory_inputs = cls._inputs(
            fixture=cls.fixture,
            name="advisory",
            include_advisory=True,
        )
        cls.short_relation_inputs = cls._inputs(
            fixture=cls.fixture,
            name="short-relation",
            wall_clock_ms=4_000,
        )
        cls.memory_relation_inputs = cls._inputs(
            fixture=cls.fixture,
            name="memory-relation",
            memory_bytes=100_663_296,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary.cleanup()

    @classmethod
    def _inputs(
        cls,
        *,
        fixture,
        name: str,
        include_relation: bool = True,
        include_advisory: bool = False,
        wall_clock_ms: int = 10_000,
        memory_bytes: int = 268_435_456,
    ):
        root = cls.root / name
        root.mkdir()
        publication = create_source_snapshot(
            SourceSnapshotRequest(
                spec=SourceSnapshotSpec(
                    repository_id=f"fixture/{name}",
                    commit_oid=fixture.commit_oid,
                    analysis_root={
                        "path_kind": "GIT_PATH",
                        "git_path_hex": b"pkg".hex(),
                    },
                ),
                repository_path=fixture.path,
                output_directory=root / "snapshot-publication",
            ),
            runtime=SourceSnapshotRuntime(git_executable=git_executable()),
        )
        snapshot_path = root / "source-snapshot.json"
        snapshot_path.write_bytes(publication.snapshot.canonical_bytes)
        snapshot = publication.snapshot.document_copy()
        policy = _policy_document(
            snapshot,
            wall_clock_ms=wall_clock_ms,
            memory_bytes=memory_bytes,
        )
        if include_advisory:
            policy["provider_requirements"].append(
                {
                    "capability_id": "python-ast-advisory",
                    "required": False,
                    "composition_mode": "CUMULATIVE",
                }
            )
        if include_relation:
            policy["provider_requirements"].append(
                {
                    "capability_id": "review-relation-derivation",
                    "required": True,
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
                repository_path=fixture.path.resolve(),
            ),
            runtime=DerivationInputRuntime(git_executable=git_executable()),
        )

    def _run(
        self,
        *,
        inputs=None,
        include_advisory: bool = False,
        derivation_id: str = "relation-derivation",
    ):
        selected = self.relation_inputs if inputs is None else inputs
        return relation.run_closed_test_relation_derivation(
            selected,
            derivation_id=derivation_id,
            bindings=relation.closed_test_relation_derivation_bindings(
                include_advisory=include_advisory
            ),
        )

    @staticmethod
    def _phase_with_module_and_import(prepared, phase):
        request = validate_request_document(
            prepared.request_document,
            launch_key=prepared.binding.launch_key,
        )
        path_hex = sorted(request.supported_paths)[0]
        size = request.source_sizes_by_path_hex[path_hex]
        facts = canonicalize_candidates(
            request,
            [
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
                },
                {
                    "subject_space": "IMPORT_ALIAS",
                    "fact_kind": "IMPORT_DECLARATION",
                    "source_anchor": {
                        "git_path": {
                            "path_kind": "GIT_PATH",
                            "git_path_hex": path_hex,
                        },
                        "start_byte": 0,
                        "end_byte": 14,
                    },
                    "local_ordinal": 0,
                    "semantic_attributes": {
                        "import_form": "IMPORT",
                        "relative_level": 0,
                        "module_parts": ["pkg", "mod"],
                        "imported_name": None,
                        "alias_name": None,
                    },
                },
            ],
        )
        return replace(
            phase,
            canonical_fact_bytes=tuple(canonical_json_bytes(fact) for fact in facts),
            reported_fact_ids=tuple(fact["fact_id"] for fact in facts),
        )

    def _run_with_import_facts(
        self,
        *,
        derivation_id: str,
        relation_launch_key: str = "relation-a",
    ):
        original = relation._run_prepared_closed_test_execution_attempt
        original_build = relation._build_prepared_relation_execution_attempt

        def runner(prepared):
            phase = original(prepared)
            return self._phase_with_module_and_import(prepared, phase)

        def relation_builder(*args, **kwargs):
            prepared = original_build(*args, **kwargs)
            prepared.binding = closed_test_relation_binding(relation_launch_key)
            return prepared

        with mock.patch.object(
            relation,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=runner,
        ), mock.patch.object(
            relation,
            "_build_prepared_relation_execution_attempt",
            side_effect=relation_builder,
        ):
            return self._run(
                inputs=self.import_inputs,
                derivation_id=derivation_id,
            )

    @staticmethod
    def _non_success(phase, status: ProviderRunStatus, code: str):
        phase_status = {
            ProviderRunStatus.FAILED: PhaseStatus.FAILED,
            ProviderRunStatus.UNAVAILABLE: PhaseStatus.UNAVAILABLE,
            ProviderRunStatus.INTERRUPTED: PhaseStatus.INTERRUPTED,
        }[status]
        return replace(
            phase,
            provider_run_status=status,
            phase_status=phase_status,
            diagnostic_code=code,
            canonical_fact_bytes=(),
            reported_fact_ids=(),
            reported_relation_ids=(),
        )

    def test_rd_001_006_017_phase_table_is_sealed_before_execution(self) -> None:
        requirements, fact_bindings, relation_binding = (
            relation._admit_closed_applicability(
                self.relation_inputs,
                derivation_id="phase-table",
                bindings=relation.closed_test_relation_derivation_bindings(),
                cancellation_requested=None,
                transport_limits=relation.DEFAULT_TRANSPORT_LIMITS,
            )
        )
        self.assertEqual(
            requirements,
            {"python-ast": True, "review-relation-derivation": True},
        )
        self.assertEqual(
            [binding.descriptor.provider_id for binding in fact_bindings],
            ["closed-multi-provider-a", "closed-multi-provider-b"],
        )
        self.assertEqual(
            relation_binding.descriptor.capability_id,
            "review-relation-derivation",
        )
        with self.assertRaises(_RelationDerivationError) as missing_requirement:
            relation._admit_closed_applicability(
                self.fact_only_inputs,
                derivation_id="missing-requirement",
                bindings=relation.closed_test_relation_derivation_bindings(),
                cancellation_requested=None,
                transport_limits=relation.DEFAULT_TRANSPORT_LIMITS,
            )
        self.assertEqual(
            missing_requirement.exception.code,
            _RelationDerivationFailureCode.INVALID_DERIVATION_REQUEST,
        )
        with self.assertRaises(_RelationDerivationError) as missing_binding:
            relation._admit_closed_applicability(
                self.relation_inputs,
                derivation_id="missing-binding",
                bindings=relation.closed_test_relation_derivation_bindings()[:-1],
                cancellation_requested=None,
                transport_limits=relation.DEFAULT_TRANSPORT_LIMITS,
            )
        self.assertEqual(
            missing_binding.exception.code,
            _RelationDerivationFailureCode.APPLICABILITY_BINDING_MISMATCH,
        )
        forged = ProviderBinding(
            ProviderDescriptor(
                **{
                    **relation_binding.descriptor.document(),
                    "provider_version": "forged",
                }
            ),
            relation_binding.launch_key,
        )
        with self.assertRaises(_RelationDerivationError):
            relation._admit_closed_applicability(
                self.relation_inputs,
                derivation_id="forged-binding",
                bindings=(*fact_bindings, forged),
                cancellation_requested=None,
                transport_limits=relation.DEFAULT_TRANSPORT_LIMITS,
            )

    def test_rd_002_005_013_relation_operands_v02_have_exact_vector(self) -> None:
        result = self._run(derivation_id="operand-vector")
        descriptor = closed_test_relation_binding().descriptor
        digest = relation_app.relation_provider_operands_digest(
            self.relation_inputs,
            descriptor,
            result.fact_set_digest,
        )
        manual = semantic_digest(
            "veritrail.review.provider-operands/0.2",
            {
                "source_snapshot_digest": self.relation_inputs.source_snapshot_digest,
                "policy_digest": self.relation_inputs.policy_digest,
                "analysis_scope_digest": self.relation_inputs.analysis_scope_digest,
                "slice_policy_digest": self.relation_inputs.slice_policy_digest,
                "derivation_profile_digest": (
                    self.relation_inputs.derivation_profile_digest
                ),
                **descriptor.document(),
                "fact_set_digest": result.fact_set_digest,
            },
        )
        self.assertEqual(
            digest,
            "4218eb9a094ad94287e8ff1628498a26e3189bc4dd3112ec6b4f0b5a57f83406",
        )
        self.assertEqual(digest, manual)
        self.assertEqual(
            result.relation_phase_result.operands_digest,
            digest,
        )
        self.assertNotEqual(
            digest,
            relation_app.relation_provider_operands_digest(
                self.relation_inputs,
                descriptor,
                "0" * 64,
            ),
        )
        other_run = relation_app.provider_run_id(
            "operand-vector-other", descriptor, digest
        )
        self.assertNotEqual(result.relation_phase_result.provider_run_id, other_run)

    def test_exact_fact_set_is_copied_and_recomputed_by_provider(self) -> None:
        result = self._run(derivation_id="request-copy")
        request = relation_app.build_relation_request_document(
            inputs=self.relation_inputs,
            derivation_id="request-copy",
            request_provenance=result.request_provenance_copy(),
            descriptor=closed_test_relation_binding().descriptor,
            fact_set_document=result.fact_set_document_copy(),
        )
        self.assertEqual(request["protocol"], relation_app.PROTOCOL)
        self.assertNotEqual(request["protocol"], "veritrail-review-derivation-cell/0.1")
        self.assertEqual(request["fact_set_digest"], result.fact_set_digest)
        self.assertTrue(
            all("provenance_refs" not in fact for fact in request["fact_set"]["facts"])
        )
        relation_app.validate_relation_request_document(
            request, launch_key="relation-a"
        )
        tampered_digest = copy.deepcopy(request)
        tampered_digest["fact_set_digest"] = "0" * 64
        with self.assertRaises(relation_app.RelationApplicationProtocolError):
            relation_app.validate_relation_request_document(
                tampered_digest, launch_key="relation-a"
            )
        tampered_fact = copy.deepcopy(request)
        tampered_fact["fact_set"]["facts"][0]["fact_id"] = "0" * 64
        with self.assertRaises(relation_app.RelationApplicationProtocolError):
            relation_app.validate_relation_request_document(
                tampered_fact, launch_key="relation-a"
            )

    def test_rd_003_004_012_candidate_belongs_only_to_relation_run(self) -> None:
        result = self._run_with_import_facts(derivation_id="positive-candidate")
        self.assertEqual(result.fact_stage_status, "COMPLETED")
        self.assertEqual(result.relation_start_status, "STARTED")
        self.assertEqual(result.final_phase_status, "COMPLETED")
        relations = result.canonical_relations_copy()
        self.assertEqual(len(relations), 1)
        relation_run = result.relation_provider_run_copy()
        fact_run_ids = {
            run["provider_run_id"] for run in result.fact_provider_runs_copy()
        }
        self.assertEqual(
            relations[0]["provenance_refs"],
            [relation_run["provider_run_id"]],
        )
        self.assertNotIn(relation_run["provider_run_id"], fact_run_ids)
        self.assertEqual(
            relation_run["reported_relation_ids"],
            [relations[0]["relation_id"]],
        )
        self.assertTrue(
            all(
                run["reported_relation_ids"] == []
                for run in result.fact_provider_runs_copy()
            )
        )
        self.assertTrue(
            all(
                run["reported_fact_ids"] == []
                and run["reported_relation_ids"] == []
                for run in result.final_provider_runs_copy()
            )
        )

        request = relation_app.build_relation_request_document(
            inputs=self.import_inputs,
            derivation_id="positive-candidate",
            request_provenance=result.request_provenance_copy(),
            descriptor=closed_test_relation_binding().descriptor,
            fact_set_document=result.fact_set_document_copy(),
        )
        validated = relation_app.validate_relation_request_document(
            request, launch_key="relation-a"
        )
        with mock.patch.object(
            relation_provider,
            "_closed_deterministic_test_parser",
            wraps=relation_provider._closed_deterministic_test_parser,
        ) as parser:
            candidates = relation_provider.run_closed_relation_provider(
                validated, launch_key="relation-a"
            )
        self.assertGreaterEqual(parser.call_count, 1)
        self.assertEqual(len(candidates), 1)

    def test_provider_cannot_mutate_application_fact_set_authority(self) -> None:
        result = self._run_with_import_facts(
            derivation_id="provider-owned-copy",
            relation_launch_key="relation-mutates-owned-input",
        )
        self.assertEqual(result.final_phase_status, "COMPLETED")
        self.assertEqual(len(result.canonical_relations_copy()), 1)
        self.assertGreater(len(result.fact_set_document_copy()["facts"]), 0)

    def test_rd_016_fact_and_relation_cells_share_one_live_budget(self) -> None:
        original_admit = relation.admit_derivation_budget
        original_build = relation._build_prepared_relation_execution_attempt
        original_fact_run = relation._run_prepared_closed_test_execution_attempt
        admitted = []
        relation_contexts = []
        events = []

        def admit(inputs):
            context = original_admit(inputs)
            admitted.append(context)
            return context

        def build(*args, **kwargs):
            events.append("relation-build")
            relation_contexts.append(kwargs["context"])
            return original_build(*args, **kwargs)

        def fact_run(prepared):
            events.append(prepared.binding.descriptor.provider_id)
            return original_fact_run(prepared)

        with mock.patch.object(
            relation, "admit_derivation_budget", side_effect=admit
        ), mock.patch.object(
            relation,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=fact_run,
        ), mock.patch.object(
            relation,
            "_build_prepared_relation_execution_attempt",
            side_effect=build,
        ):
            result = self._run(derivation_id="one-budget")
        self.assertEqual(result.final_phase_status, "COMPLETED")
        self.assertEqual(len(admitted), 1)
        self.assertEqual(relation_contexts, admitted)
        self.assertEqual(
            events,
            [
                "closed-multi-provider-a",
                "closed-multi-provider-b",
                "relation-build",
            ],
        )

    def test_rd_007_conflict_holds_relation_without_fabricated_run(self) -> None:
        original = relation._run_prepared_closed_test_execution_attempt

        def runner(prepared):
            phase = original(prepared)
            if prepared.binding.descriptor.provider_id.endswith("-b"):
                fact = json.loads(phase.canonical_fact_bytes[0])
                fact["semantic_attributes"] = {"module_key_parts": ["conflict"]}
                fact["fact_id"] = semantic_digest(
                    "veritrail.review.code-fact/0.1",
                    {
                        "subject_key_digest": fact["subject_key_digest"],
                        "fact_kind": fact["fact_kind"],
                        "semantic_attributes": fact["semantic_attributes"],
                    },
                )
                return replace(
                    phase,
                    canonical_fact_bytes=(canonical_json_bytes(fact),),
                    reported_fact_ids=(fact["fact_id"],),
                )
            return phase

        with mock.patch.object(
            relation,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=runner,
        ):
            result = self._run(derivation_id="conflict-hold")
        self.assertEqual(result.fact_stage_status, "COMPLETED")
        self.assertEqual(result.relation_start_status, "NOT_STARTED")
        self.assertEqual(result.final_phase_status, "UPSTREAM_HOLD")
        self.assertEqual(result.upstream_reason_codes, ("FACT_CONFLICT",))
        self.assertIsNotNone(result.fact_set_document_copy())
        self.assertEqual(len(result.canonical_conflicts_copy()), 1)
        self.assertIsNone(result.relation_phase_result)
        self.assertIsNone(result.relation_provider_run_copy())

    def test_rd_008_optional_gap_and_conflict_remain_independent(self) -> None:
        original = relation._run_prepared_closed_test_execution_attempt

        def runner(prepared):
            phase = original(prepared)
            provider = prepared.binding.descriptor.provider_id
            if provider == "closed-multi-provider-b":
                fact = json.loads(phase.canonical_fact_bytes[0])
                fact["semantic_attributes"] = {"module_key_parts": ["conflict"]}
                fact["fact_id"] = semantic_digest(
                    "veritrail.review.code-fact/0.1",
                    {
                        "subject_key_digest": fact["subject_key_digest"],
                        "fact_kind": fact["fact_kind"],
                        "semantic_attributes": fact["semantic_attributes"],
                    },
                )
                return replace(
                    phase,
                    canonical_fact_bytes=(canonical_json_bytes(fact),),
                    reported_fact_ids=(fact["fact_id"],),
                )
            if provider == "closed-multi-provider-advisory":
                return self._non_success(
                    phase,
                    ProviderRunStatus.UNAVAILABLE,
                    "PROVIDER_UNAVAILABLE",
                )
            return phase

        with mock.patch.object(
            relation,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=runner,
        ):
            result = self._run(
                inputs=self.advisory_inputs,
                include_advisory=True,
                derivation_id="optional-conflict",
            )
        self.assertEqual(
            result.upstream_reason_codes,
            ("FACT_CONFLICT", "OPTIONAL_SOURCE_GAP"),
        )
        self.assertIsNotNone(result.fact_set_document_copy())
        self.assertIsNone(result.relation_phase_result)

    def test_rd_009_required_failure_has_no_normal_fact_set(self) -> None:
        original = relation._run_prepared_closed_test_execution_attempt

        def runner(prepared):
            phase = original(prepared)
            if prepared.binding.descriptor.provider_id.endswith("-a"):
                return self._non_success(
                    phase, ProviderRunStatus.FAILED, "PROVIDER_FAILED"
                )
            return phase

        with mock.patch.object(
            relation,
            "_run_prepared_closed_test_execution_attempt",
            side_effect=runner,
        ):
            result = self._run(derivation_id="required-failure")
        self.assertEqual(result.fact_stage_status, "FAILED")
        self.assertEqual(result.relation_start_status, "NOT_STARTED")
        self.assertEqual(result.final_phase_status, "UPSTREAM_HOLD")
        self.assertEqual(
            result.upstream_reason_codes, ("REQUIRED_SOURCE_NON_SUCCESS",)
        )
        self.assertIsNone(result.fact_set_document_copy())
        self.assertIsNone(result.relation_phase_result)

    def test_absent_normal_fact_set_holds_relation_without_a_run(self) -> None:
        with mock.patch.object(
            relation,
            "_merge_completed_sources",
            side_effect=relation._FactIdentityCollision,
        ):
            result = self._run(derivation_id="no-normal-fact-set")
        self.assertEqual(result.fact_stage_status, "FAILED")
        self.assertEqual(result.relation_start_status, "NOT_STARTED")
        self.assertEqual(result.final_phase_status, "UPSTREAM_HOLD")
        self.assertEqual(result.upstream_reason_codes, ("NO_NORMAL_FACT_SET",))
        self.assertIsNone(result.fact_set_document_copy())
        self.assertIsNone(result.relation_phase_result)

    def test_rd_010_empty_unavailable_and_interrupted_are_distinct(self) -> None:
        empty = self._run(derivation_id="empty-success")
        self.assertEqual(empty.final_phase_status, "COMPLETED")
        self.assertEqual(empty.canonical_relations_copy(), ())
        self.assertIsNotNone(empty.relation_phase_result)

        original_build = relation._build_prepared_relation_execution_attempt

        def unavailable_build(*args, **kwargs):
            prepared = original_build(*args, **kwargs)
            prepared.binding = closed_test_relation_binding("relation-unavailable")
            return prepared

        with mock.patch.object(
            relation,
            "_build_prepared_relation_execution_attempt",
            side_effect=unavailable_build,
        ):
            unavailable = self._run(derivation_id="unavailable")
        self.assertEqual(unavailable.relation_start_status, "STARTED")
        self.assertEqual(unavailable.final_phase_status, "UNAVAILABLE")
        self.assertIsNotNone(unavailable.relation_provider_run_copy())

        def cancelled_build(*args, **kwargs):
            prepared = original_build(*args, **kwargs)
            prepared.context.request_cancellation()
            return prepared

        with mock.patch.object(
            relation,
            "_build_prepared_relation_execution_attempt",
            side_effect=cancelled_build,
        ):
            interrupted = self._run(derivation_id="interrupted")
        self.assertEqual(interrupted.fact_stage_status, "COMPLETED")
        self.assertEqual(interrupted.final_phase_status, "INTERRUPTED")
        self.assertEqual(interrupted.relation_start_status, "NOT_STARTED")
        self.assertIsNotNone(interrupted.fact_set_document_copy())
        self.assertIsNone(interrupted.relation_provider_run_copy())

    def test_rd_011_015_nonconformant_or_parser_failure_admits_no_candidate(self) -> None:
        original_build = relation._build_prepared_relation_execution_attempt

        def bad_build(*args, **kwargs):
            prepared = original_build(*args, **kwargs)
            prepared.binding = closed_test_relation_binding("relation-bad-candidate")
            return prepared

        with mock.patch.object(
            relation,
            "_build_prepared_relation_execution_attempt",
            side_effect=bad_build,
        ):
            bad = self._run(derivation_id="bad-candidate")
        self.assertEqual(bad.final_phase_status, "FAILED")
        self.assertEqual(bad.canonical_relations_copy(), ())
        self.assertEqual(
            bad.relation_provider_run_copy()["diagnostics"][0]["diagnostic_code"],
            "NONCONFORMANT_PROVIDER_OUTPUT",
        )
        self.assertTrue(
            all(
                run["reported_relation_ids"] == []
                for run in bad.final_provider_runs_copy()
            )
        )

        parser_failure = self._run(
            inputs=self.invalid_inputs,
            derivation_id="parser-failure",
        )
        self.assertEqual(parser_failure.final_phase_status, "FAILED")
        self.assertEqual(parser_failure.canonical_relations_copy(), ())
        self.assertEqual(
            parser_failure.relation_provider_run_copy()["diagnostics"][0][
                "diagnostic_code"
            ],
            "PROVIDER_FAILED",
        )

    def test_rd_011_relation_deadline_retains_no_prefix_candidate(self) -> None:
        original_build = relation._build_prepared_relation_execution_attempt

        def slow_build(*args, **kwargs):
            prepared = original_build(*args, **kwargs)
            prepared.binding = closed_test_relation_binding("relation-slow")
            return prepared

        with mock.patch.object(
            relation,
            "_build_prepared_relation_execution_attempt",
            side_effect=slow_build,
        ):
            result = self._run(
                inputs=self.short_relation_inputs,
                derivation_id="relation-deadline",
            )
        self.assertEqual(result.relation_start_status, "STARTED")
        self.assertEqual(result.final_phase_status, "INTERRUPTED")
        self.assertIsNotNone(result.relation_phase_result)
        self.assertEqual(result.relation_phase_result.canonical_relations_copy(), ())
        self.assertEqual(
            result.relation_provider_run_copy()["reported_relation_ids"], []
        )

    def test_relation_memory_stop_uses_shared_budget_and_keeps_no_candidate(self) -> None:
        original_build = relation._build_prepared_relation_execution_attempt

        def memory_build(*args, **kwargs):
            prepared = original_build(*args, **kwargs)
            prepared.binding = closed_test_relation_binding("relation-memory")
            return prepared

        with mock.patch.object(
            relation,
            "_build_prepared_relation_execution_attempt",
            side_effect=memory_build,
        ):
            result = self._run(
                inputs=self.memory_relation_inputs,
                derivation_id="relation-memory",
            )
        self.assertEqual(result.fact_stage_status, "COMPLETED")
        self.assertEqual(result.relation_start_status, "STARTED")
        self.assertEqual(result.final_phase_status, "INTERRUPTED")
        self.assertIsNotNone(result.relation_phase_result)
        self.assertEqual(
            result.relation_phase_result.diagnostic_code,
            "EXECUTION_MEMORY_BUDGET",
        )
        self.assertEqual(result.canonical_relations_copy(), ())

    def test_private_result_is_copy_owned_unpublished_and_not_exported(self) -> None:
        result = self._run_with_import_facts(derivation_id="private-boundary")
        relation_copy = result.canonical_relations_copy()
        fact_copy = result.fact_set_document_copy()
        relation_copy[0]["target"]["fact_id"] = "0" * 64
        fact_copy["facts"].clear()
        self.assertNotEqual(relation_copy, result.canonical_relations_copy())
        self.assertNotEqual(fact_copy, result.fact_set_document_copy())
        parameters = inspect.signature(
            relation.run_closed_test_relation_derivation
        ).parameters
        self.assertNotIn("output_path", parameters)
        self.assertNotIn("publisher", parameters)
        import veritrail_review

        self.assertFalse(
            hasattr(veritrail_review, "run_closed_test_relation_derivation")
        )
        self.assertNotIn(
            "run_closed_test_relation_derivation", veritrail_review.__all__
        )


if __name__ == "__main__":
    unittest.main()
