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
from test_execution_cell import _canonical_artifact, _policy_document  # noqa: E402
from veritrail_review import (  # noqa: E402
    DerivationInputRequest,
    DerivationInputRuntime,
    SourceSnapshotRequest,
    SourceSnapshotRuntime,
    SourceSnapshotSpec,
    bind_derivation_inputs,
    create_source_snapshot,
)
from veritrail_review._execution_cell import (  # noqa: E402
    _prepare_closed_test_execution_attempt,
    _run_prepared_closed_test_execution_attempt,
    run_closed_test_execution_cell,
)
from veritrail_review._execution_cell_binding import closed_test_binding  # noqa: E402
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    AttemptEligibilityState,
)
from veritrail_review._execution_cell_values import (  # noqa: E402
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
from veritrail_review._fact_evidence_closure import (  # noqa: E402
    _IntegratedFactEvidenceController,
    _project_final_evidence_for_conformance,
    _validate_final_evidence_projection,
    run_closed_test_fact_evidence_closure,
)
from veritrail_review._fact_evidence_values import (  # noqa: E402
    _DiagnosticClosureEligibility,
    _FactEvidenceClosureError,
    _FactEvidenceClosureFailureCode,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest  # noqa: E402
from veritrail_review.errors import (  # noqa: E402
    DerivationExecutionCellError,
    DerivationExecutionCellFailureCode,
)
from veritrail_review._windows_execution_cell import CellReleaseError  # noqa: E402


class FactEvidenceClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._temporary = tempfile.TemporaryDirectory(prefix="veritrail-r1-fact-")
        cls.root = Path(cls._temporary.name)
        cls.fixture = create_fixture_repository(cls.root / "repository")
        cls.inputs = cls._inputs(name="default")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary.cleanup()

    @classmethod
    def _inputs(
        cls,
        *,
        name: str,
        wall_clock_ms: int = 10_000,
        memory_bytes: int = 268_435_456,
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
        profile_path = root / "derivation-profile.json"
        profile_path.write_bytes((FIXTURE_ROOT / "derivation-profile.json").read_bytes())
        policy_path = root / "review-policy.json"
        policy_path.write_bytes(
            _canonical_artifact(
                _policy_document(
                    snapshot,
                    wall_clock_ms=wall_clock_ms,
                    memory_bytes=memory_bytes,
                )
            )
        )
        return bind_derivation_inputs(
            DerivationInputRequest(
                source_snapshot_path=snapshot_path.resolve(),
                review_policy_path=policy_path.resolve(),
                derivation_profile_path=profile_path.resolve(),
                repository_path=cls.fixture.path.resolve(),
            ),
            runtime=DerivationInputRuntime(git_executable=git_executable()),
        )

    def _run(self, key: str, *, inputs=None, derivation_id: str = "fact-attempt"):
        return run_closed_test_fact_evidence_closure(
            self.inputs if inputs is None else inputs,
            derivation_id=derivation_id,
            binding=closed_test_binding(key),
        )

    def _phase(self, key: str, *, derivation_id: str):
        return run_closed_test_execution_cell(
            self.inputs,
            derivation_id=derivation_id,
            binding=closed_test_binding(key),
        )

    def _run_injected_phase(self, phase):
        binding = closed_test_binding("stable-a")
        prepared = _prepare_closed_test_execution_attempt(
            self.inputs,
            derivation_id=phase.derivation_id,
            binding=binding,
            cancellation_requested=None,
            transport_limits=inspect.signature(
                run_closed_test_fact_evidence_closure
            ).parameters["transport_limits"].default,
        )
        self.assertTrue(prepared.eligibility.admit())

        aligned_phase = replace(
            phase,
            request_provenance_bytes=canonical_json_bytes(
                prepared.request_provenance
            ),
        )

        def return_phase(_prepared):
            if aligned_phase.phase_status is not PhaseStatus.COMPLETED:
                prepared.eligibility.revoke()
            return aligned_phase

        with mock.patch(
            "veritrail_review._fact_evidence_closure._run_prepared_closed_test_execution_attempt",
            side_effect=return_phase,
        ):
            controller = _IntegratedFactEvidenceController(prepared)
            return prepared, controller.run()

    def test_fa001_fa002_completed_results_are_owned_nonpublished_states(self) -> None:
        before = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        one = self._run("stable-a", derivation_id="fa001")
        empty = self._run("empty", derivation_id="fa002")
        after = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))

        self.assertEqual(after, before)
        for result, expected_count in ((one, 1), (empty, 0)):
            self.assertEqual(result.phase_result.phase_status, PhaseStatus.COMPLETED)
            self.assertIsNone(result.evidence_projection)
            self.assertIsNone(result.diagnostic_closure_eligibility)
            state = result.fact_set_construction_state
            self.assertIsNotNone(state)
            document = state.fact_set_document_copy()
            self.assertEqual(len(document["facts"]), expected_count)
            self.assertEqual(document["conflicts"], [])
            self.assertEqual(
                state.canonical_fact_set_artifact_bytes,
                state.fact_set_document_bytes + b"\n",
            )
            self.assertTrue(state.normal_continuation_permitted())

    def test_fa003_byte_identical_duplicate_is_one_member(self) -> None:
        phase = self._phase("stable-a", derivation_id="fa003")
        duplicated = replace(
            phase,
            canonical_fact_bytes=(
                phase.canonical_fact_bytes[0],
                phase.canonical_fact_bytes[0],
            ),
        )
        _prepared, result = self._run_injected_phase(duplicated)
        state = result.fact_set_construction_state
        self.assertIsNotNone(state)
        facts = state.canonical_facts_copy()
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["provenance_refs"], [phase.provider_run_id])

    def test_fa004_identity_or_anchor_drift_rejects_and_revokes(self) -> None:
        base = self._phase("stable-a", derivation_id="fa004")
        original = json.loads(base.canonical_fact_bytes[0])
        mutations = (
            ("source_snapshot_digest", lambda fact: fact.__setitem__("source_snapshot_digest", "0" * 64)),
            ("derivation_profile_digest", lambda fact: fact.__setitem__("derivation_profile_digest", "1" * 64)),
            ("anchor", lambda fact: fact["source_anchor"].__setitem__("end_byte", 0)),
            ("subject", lambda fact: fact.__setitem__("subject_key_digest", "2" * 64)),
            ("fact", lambda fact: fact.__setitem__("fact_id", "3" * 64)),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                fact = copy.deepcopy(original)
                mutate(fact)
                changed = replace(
                    base,
                    canonical_fact_bytes=(canonical_json_bytes(fact),),
                    reported_fact_ids=(fact["fact_id"],),
                )
                binding = closed_test_binding("stable-a")
                prepared = _prepare_closed_test_execution_attempt(
                    self.inputs,
                    derivation_id=base.derivation_id,
                    binding=binding,
                    cancellation_requested=None,
                    transport_limits=inspect.signature(
                        run_closed_test_fact_evidence_closure
                    ).parameters["transport_limits"].default,
                )
                with mock.patch(
                    "veritrail_review._fact_evidence_closure._run_prepared_closed_test_execution_attempt",
                    return_value=changed,
                ):
                    with self.assertRaises(_FactEvidenceClosureError) as raised:
                        _IntegratedFactEvidenceController(prepared).run()
                self.assertEqual(
                    raised.exception.code,
                    _FactEvidenceClosureFailureCode.FACT_ADMISSION_REJECTED,
                )
                self.assertEqual(
                    prepared.eligibility.state, AttemptEligibilityState.REVOKED
                )

    def test_fa005_fa006_reported_ids_close_both_directions(self) -> None:
        base = self._phase("stable-a", derivation_id="fa005-006")
        variants = (
            replace(base, reported_fact_ids=()),
            replace(base, reported_fact_ids=(base.reported_fact_ids[0], "f" * 64)),
        )
        for phase in variants:
            with self.subTest(ids=phase.reported_fact_ids):
                with self.assertRaises(_FactEvidenceClosureError) as raised:
                    self._run_injected_phase(phase)
                self.assertEqual(
                    raised.exception.code,
                    _FactEvidenceClosureFailureCode.FACT_ADMISSION_REJECTED,
                )

    def test_fa007_single_provider_conflict_is_nonconformant_not_conflict(self) -> None:
        result = self._run("bad-candidate", derivation_id="fa007")
        self.assertIsNone(result.fact_set_construction_state)
        evidence = result.evidence_projection.document_copy()
        self.assertEqual(evidence["overall_execution_status"], "FAILED")
        self.assertEqual(
            evidence["diagnostics"][0]["diagnostic_code"],
            "NONCONFORMANT_PROVIDER_OUTPUT",
        )
        self.assertNotIn("conflicts", evidence)

    def test_fa008_owned_values_ignore_mutated_copies(self) -> None:
        result = self._run("stable-a", derivation_id="fa008")
        phase_copy = result.phase_result.canonical_facts_copy()[0]
        state = result.fact_set_construction_state
        fact_set_copy = state.fact_set_document_copy()
        provider_run_copy = state.provider_run_phase_copy()
        phase_copy["semantic_attributes"]["module_key_parts"] = ["mutated"]
        fact_set_copy["facts"].clear()
        provider_run_copy["reported_fact_ids"].clear()
        self.assertIsNone(
            result.phase_result.canonical_facts_copy()[0]["semantic_attributes"][
                "module_key_parts"
            ]
        )
        self.assertEqual(len(state.fact_set_document_copy()["facts"]), 1)
        self.assertEqual(
            state.provider_run_phase_copy()["reported_fact_ids"],
            list(result.phase_result.reported_fact_ids),
        )

    def test_fa009_fa024_no_publication_surface_or_files(self) -> None:
        import veritrail_review

        before = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        self._run("stable-a", derivation_id="fa009-024")
        after = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        self.assertEqual(after, before)
        self.assertNotIn("run_closed_test_fact_evidence_closure", veritrail_review.__all__)
        self.assertFalse(hasattr(veritrail_review, "run_closed_test_fact_evidence_closure"))
        parameters = inspect.signature(run_closed_test_fact_evidence_closure).parameters
        for forbidden in ("output_directory", "publisher", "manifest", "output_path"):
            self.assertNotIn(forbidden, parameters)

    def test_fa010_downstream_failure_uses_new_projection_and_clears_ids(self) -> None:
        phase = self._phase("stable-a", derivation_id="fa010")
        projection = _project_final_evidence_for_conformance(
            phase, terminal_code="EXECUTION_ARTIFACT_BUDGET"
        )
        document = projection.document_copy()
        self.assertEqual(phase.provider_run_status, ProviderRunStatus.COMPLETED)
        self.assertEqual(len(phase.reported_fact_ids), 1)
        self.assertEqual(document["provider_runs"][0]["execution_status"], "COMPLETED")
        self.assertEqual(document["provider_runs"][0]["reported_fact_ids"], [])
        self.assertEqual(document["overall_execution_status"], "INTERRUPTED")

    def test_fa011_to_fa014_nonbudget_terminal_projection_and_one_shot_eligibility(self) -> None:
        keys = {
            "unavailable": ("UNAVAILABLE", "PROVIDER_UNAVAILABLE"),
            "failed": ("FAILED", "PROVIDER_FAILED"),
            "bad-candidate": ("FAILED", "NONCONFORMANT_PROVIDER_OUTPUT"),
            "no-envelope": ("FAILED", "INTERNAL_DERIVATION_ERROR"),
        }
        for key, (status, code) in keys.items():
            with self.subTest(key=key):
                result = self._run(key, derivation_id=f"fa011-014-{key}")
                self.assertIsNone(result.fact_set_construction_state)
                document = result.evidence_projection.document_copy()
                run = document["provider_runs"][0]
                diagnostic = {
                    "diagnostic_code": code,
                    "subject_ref": {
                        "ref_kind": "PROVIDER_RUN",
                        "provider_run_id": run["provider_run_id"],
                    },
                }
                self.assertEqual(document["overall_execution_status"], status)
                self.assertEqual(run["execution_status"], status)
                self.assertEqual(run["diagnostics"], [diagnostic])
                self.assertEqual(document["diagnostics"], [diagnostic])
                eligibility = result.diagnostic_closure_eligibility
                self.assertTrue(eligibility.is_available())
                eligibility.claim()
                self.assertFalse(eligibility.is_available())
                with self.assertRaises(_FactEvidenceClosureError):
                    eligibility.claim()

    def test_fa015_active_stop_projections_never_grant_diagnostic_eligibility(self) -> None:
        base = self._phase("stable-a", derivation_id="fa015")
        for code in (
            "EXECUTION_DEADLINE",
            "EXECUTION_CANCELLED",
            "EXECUTION_MEMORY_BUDGET",
        ):
            with self.subTest(code=code):
                phase = replace(
                    base,
                    provider_run_status=ProviderRunStatus.INTERRUPTED,
                    phase_status=PhaseStatus.INTERRUPTED,
                    diagnostic_code=code,
                    canonical_fact_bytes=(),
                    reported_fact_ids=(),
                )
                projection = _project_final_evidence_for_conformance(phase)
                document = projection.document_copy()
                self.assertEqual(document["provider_runs"][0]["reported_fact_ids"], [])
                self.assertEqual(document["diagnostics"], document["provider_runs"][0]["diagnostics"])
                _prepared, result = self._run_injected_phase(phase)
                self.assertIsNone(result.evidence_projection)
                self.assertIsNone(result.diagnostic_closure_eligibility)

    def test_fa016_artifact_stop_is_top_only_and_has_no_publication_capability(self) -> None:
        phase = self._phase("stable-a", derivation_id="fa016")
        projection = _project_final_evidence_for_conformance(
            phase, terminal_code="EXECUTION_ARTIFACT_BUDGET"
        )
        document = projection.document_copy()
        self.assertEqual(document["provider_runs"][0]["diagnostics"], [])
        self.assertEqual(
            document["diagnostics"],
            [{"diagnostic_code": "EXECUTION_ARTIFACT_BUDGET", "subject_ref": None}],
        )
        self.assertFalse(hasattr(projection, "publish"))
        self.assertFalse(hasattr(projection, "reserve"))

    def test_fa017_release_failure_has_no_closure_result(self) -> None:
        with mock.patch(
            "veritrail_review._execution_cell.run_windows_execution_cell",
            side_effect=CellReleaseError,
        ):
            with self.assertRaises(DerivationExecutionCellError) as raised:
                self._run("empty", derivation_id="fa017")
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.RELEASE_FAILED,
        )

    def test_fa018_fa019_late_stop_or_reservation_prevents_diagnostic_eligibility(self) -> None:
        phase = self._phase("failed", derivation_id="fa018-019")
        for condition in ("stop", "reservation"):
            with self.subTest(condition=condition):
                binding = closed_test_binding("failed")
                prepared = _prepare_closed_test_execution_attempt(
                    self.inputs,
                    derivation_id=phase.derivation_id,
                    binding=binding,
                    cancellation_requested=None,
                    transport_limits=inspect.signature(
                        run_closed_test_fact_evidence_closure
                    ).parameters["transport_limits"].default,
                )
                self.assertTrue(prepared.eligibility.admit())
                prepared.eligibility.revoke()
                if condition == "stop":
                    prepared.context.request_cancellation()
                else:
                    self.assertTrue(prepared.context.reserve_artifact_bytes(b"x"))
                with mock.patch(
                    "veritrail_review._fact_evidence_closure._run_prepared_closed_test_execution_attempt",
                    return_value=replace(
                        phase,
                        request_provenance_bytes=canonical_json_bytes(
                            prepared.request_provenance
                        ),
                    ),
                ), mock.patch(
                    "veritrail_review._fact_evidence_closure._project_final_evidence_for_conformance",
                    side_effect=AssertionError(
                        "projection must not run without diagnostic eligibility"
                    ),
                ):
                    with self.assertRaises(_FactEvidenceClosureError) as raised:
                        _IntegratedFactEvidenceController(prepared).run()
                self.assertEqual(
                    raised.exception.code,
                    _FactEvidenceClosureFailureCode.DIAGNOSTIC_ELIGIBILITY_UNAVAILABLE,
                )

    def test_fa020_noncanonical_diagnostic_placement_is_rejected(self) -> None:
        phase = self._phase("failed", derivation_id="fa020")
        valid = _project_final_evidence_for_conformance(phase).document_copy()
        variants = []
        run_only = copy.deepcopy(valid)
        run_only["diagnostics"] = []
        variants.append(run_only)
        top_only = copy.deepcopy(valid)
        top_only["provider_runs"][0]["diagnostics"] = []
        variants.append(top_only)
        duplicated = copy.deepcopy(valid)
        duplicated["diagnostics"].append(copy.deepcopy(duplicated["diagnostics"][0]))
        duplicated["provider_runs"][0]["diagnostics"].append(
            copy.deepcopy(duplicated["provider_runs"][0]["diagnostics"][0])
        )
        for document in variants + [duplicated]:
            unsigned = {
                key: copy.deepcopy(value)
                for key, value in document.items()
                if key != "derivation_evidence_digest"
            }
            document["derivation_evidence_digest"] = semantic_digest(
                "veritrail.review.derivation-evidence/0.1", unsigned
            )
            with self.assertRaises(_FactEvidenceClosureError):
                _validate_final_evidence_projection(document, phase)

    def test_projection_failure_irreversibly_revokes_diagnostic_eligibility(self) -> None:
        phase = self._phase("failed", derivation_id="projection-failure")
        prepared = _prepare_closed_test_execution_attempt(
            self.inputs,
            derivation_id=phase.derivation_id,
            binding=closed_test_binding("failed"),
            cancellation_requested=None,
            transport_limits=inspect.signature(
                run_closed_test_fact_evidence_closure
            ).parameters["transport_limits"].default,
        )
        self.assertTrue(prepared.eligibility.admit())
        prepared.eligibility.revoke()
        eligibility = _DiagnosticClosureEligibility(
            context=prepared.context,
            attempt_eligibility=prepared.eligibility,
        )
        aligned = replace(
            phase,
            request_provenance_bytes=canonical_json_bytes(
                prepared.request_provenance
            ),
        )
        with mock.patch(
            "veritrail_review._fact_evidence_closure._run_prepared_closed_test_execution_attempt",
            return_value=aligned,
        ), mock.patch(
            "veritrail_review._fact_evidence_closure._diagnostic_eligibility",
            return_value=eligibility,
        ), mock.patch(
            "veritrail_review._fact_evidence_closure._project_final_evidence_for_conformance",
            side_effect=_FactEvidenceClosureError(
                _FactEvidenceClosureFailureCode.EVIDENCE_PROJECTION_REJECTED
            ),
        ):
            with self.assertRaises(_FactEvidenceClosureError):
                _IntegratedFactEvidenceController(prepared).run()
        self.assertFalse(eligibility.is_available())

    def test_fa021_sufficient_budgets_preserve_fact_semantics_not_provenance(self) -> None:
        second_inputs = self._inputs(
            name="larger-budget",
            wall_clock_ms=20_000,
            memory_bytes=402_653_184,
        )
        first = self._run("stable-a", derivation_id="fa021-a")
        second = self._run(
            "stable-a", inputs=second_inputs, derivation_id="fa021-b"
        )
        first_state = first.fact_set_construction_state
        second_state = second.fact_set_construction_state
        first_fact = first_state.canonical_facts_copy()[0]
        second_fact = second_state.canonical_facts_copy()[0]
        self.assertEqual(first_fact["fact_id"], second_fact["fact_id"])
        self.assertEqual(first_fact["subject_key_digest"], second_fact["subject_key_digest"])
        self.assertEqual(first_state.fact_set_digest, second_state.fact_set_digest)
        self.assertNotEqual(first_state.provider_run_id, second_state.provider_run_id)
        self.assertNotEqual(
            first_state.canonical_fact_set_artifact_bytes,
            second_state.canonical_fact_set_artifact_bytes,
        )

    def test_fa022_standalone_phase_cannot_be_resumed_as_integrated_attempt(self) -> None:
        phase = self._phase("stable-a", derivation_id="fa022")
        with self.assertRaises(DerivationExecutionCellError) as raised:
            run_closed_test_fact_evidence_closure(
                phase,
                derivation_id=phase.derivation_id,
                binding=closed_test_binding("stable-a"),
            )
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST,
        )

        prepared = _prepare_closed_test_execution_attempt(
            self.inputs,
            derivation_id="fa022-one-shot",
            binding=closed_test_binding("empty"),
            cancellation_requested=None,
            transport_limits=inspect.signature(
                run_closed_test_fact_evidence_closure
            ).parameters["transport_limits"].default,
        )
        _run_prepared_closed_test_execution_attempt(prepared)
        with self.assertRaises(DerivationExecutionCellError) as repeated:
            _run_prepared_closed_test_execution_attempt(prepared)
        self.assertEqual(
            repeated.exception.code,
            DerivationExecutionCellFailureCode.INVALID_DERIVATION_ATTEMPT_REQUEST,
        )

    def test_non_success_phase_must_match_the_admitted_attempt(self) -> None:
        phase = self._phase("failed", derivation_id="terminal-continuity")
        prepared = _prepare_closed_test_execution_attempt(
            self.inputs,
            derivation_id=phase.derivation_id,
            binding=closed_test_binding("stable-a"),
            cancellation_requested=None,
            transport_limits=inspect.signature(
                run_closed_test_fact_evidence_closure
            ).parameters["transport_limits"].default,
        )
        self.assertTrue(prepared.eligibility.admit())
        prepared.eligibility.revoke()
        injected = replace(
            phase,
            request_provenance_bytes=canonical_json_bytes(
                prepared.request_provenance
            ),
        )
        with mock.patch(
            "veritrail_review._fact_evidence_closure._run_prepared_closed_test_execution_attempt",
            return_value=injected,
        ):
            with self.assertRaises(_FactEvidenceClosureError) as raised:
                _IntegratedFactEvidenceController(prepared).run()
        self.assertEqual(
            raised.exception.code,
            _FactEvidenceClosureFailureCode.EVIDENCE_PROJECTION_REJECTED,
        )

    def test_projection_bytes_and_digests_are_canonical(self) -> None:
        result = self._run("failed", derivation_id="canonical-projection")
        projection = result.evidence_projection
        document = projection.document_copy()
        self.assertEqual(projection.document_bytes, canonical_json_bytes(document))
        unsigned = {
            key: copy.deepcopy(value)
            for key, value in document.items()
            if key != "derivation_evidence_digest"
        }
        self.assertEqual(
            projection.derivation_evidence_digest,
            semantic_digest("veritrail.review.derivation-evidence/0.1", unsigned),
        )


if __name__ == "__main__":
    unittest.main()
