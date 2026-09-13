from __future__ import annotations

import copy
import json
import sys
import tempfile
import time
import unittest
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
    run_closed_test_execution_cell,
)
from veritrail_review._execution_cell_application import (  # noqa: E402
    ApplicationProtocolError,
)
from veritrail_review._execution_cell_binding import (  # noqa: E402
    ProviderBinding,
    ProviderDescriptor,
    closed_test_binding,
)
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    encode_frame,
)
from veritrail_review._execution_cell_values import (  # noqa: E402
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
from veritrail_review.canonical import (  # noqa: E402
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from veritrail_review.errors import (  # noqa: E402
    BudgetPrimitiveError,
    BudgetPrimitiveFailureCode,
    DerivationExecutionCellError,
    DerivationExecutionCellFailureCode,
)
from veritrail_review._windows_budget import _WindowsBindings  # noqa: E402
from veritrail_review._windows_execution_cell import CellReleaseError  # noqa: E402


def _canonical_artifact(document: dict[str, object]) -> bytes:
    return canonical_json_bytes(document) + b"\n"


def _seal_policy(document: dict[str, object]) -> dict[str, object]:
    document["analysis_scope_digest"] = semantic_digest(
        "veritrail.review.analysis-scope/0.1",
        {
            key: copy.deepcopy(document[key])
            for key in (
                "source_snapshot_digest",
                "derivation_profile_digest",
                "scope_decisions",
                "provider_requirements",
                "python_module_mapping",
            )
        },
    )
    document["slice_policy_digest"] = semantic_digest(
        "veritrail.review.slice-policy/0.1",
        {
            "analysis_scope_digest": document["analysis_scope_digest"],
            "slice_policy": copy.deepcopy(document["slice_policy"]),
        },
    )
    document["policy_digest"] = semantic_digest(
        "veritrail.review.review-policy/0.1",
        {
            key: copy.deepcopy(value)
            for key, value in document.items()
            if key
            not in {
                "analysis_scope_digest",
                "slice_policy_digest",
                "policy_digest",
                "seal",
            }
        },
    )
    document.pop("seal", None)
    document["seal"] = {
        "algorithm": "sha256",
        "digest": sha256_bytes(canonical_json_bytes(document)),
    }
    return document


def _policy_document(
    snapshot: dict[str, object],
    *,
    wall_clock_ms: int = 10_000,
    memory_bytes: int = 268_435_456,
) -> dict[str, object]:
    profile = json.loads((FIXTURE_ROOT / "derivation-profile.json").read_bytes())
    return _seal_policy(
        {
            "artifact_kind": "REVIEW_POLICY",
            "schema_version": "0.1",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "policy_id": "execution-cell-test-policy",
            "version": 1,
            "source_snapshot_digest": snapshot["source_snapshot_digest"],
            "derivation_profile_digest": profile["profile_digest"],
            "scope_decisions": [
                {
                    "git_path": copy.deepcopy(item["git_path"]),
                    "disposition": "IN_SCOPE",
                    "source_class": "FIRST_PARTY",
                    "reason_code": "POLICY_INCLUDED",
                }
                for item in snapshot["inventory"]
            ],
            "provider_requirements": [
                {
                    "capability_id": "python-ast",
                    "required": True,
                    "composition_mode": "CUMULATIVE",
                }
            ],
            "python_module_mapping": {
                "module_root": copy.deepcopy(
                    snapshot["source_coordinate"]["analysis_root"]
                ),
                "package_prefix": ["pkg"],
            },
            "slice_policy": {
                "anchor_fact_kinds": ["MODULE"],
                "allowed_relations": [
                    {"relation_kind": "LEXICAL_CONTAINS", "direction": "OUTBOUND"},
                    {
                        "relation_kind": "IMPORT_TARGET_LITERAL",
                        "direction": "OUTBOUND",
                    },
                ],
                "max_depth": 1,
                "max_symbols": 128,
                "max_files": 32,
                "max_relations": 256,
            },
            "execution_budget": {
                "wall_clock_ms": wall_clock_ms,
                "memory_bytes": memory_bytes,
                "artifact_bytes": 16_777_216,
            },
            "governance": {
                "claim_owner_ref": "fixture-human",
                "drafter_ref": "fixture-drafter",
                "seal_authority_ref": "fixture-human",
                "seal_decision": "CONFIRMED",
            },
        }
    )


class ExecutionCellTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="veritrail-r1-cell-")
        self.root = Path(self._temporary.name)
        self.fixture = create_fixture_repository(self.root / "repository")
        self.inputs = self._inputs(name="default")

    def tearDown(self) -> None:
        self._temporary.cleanup()

    def _inputs(
        self,
        *,
        name: str,
        wall_clock_ms: int = 10_000,
        memory_bytes: int = 268_435_456,
    ):
        root = self.root / name
        root.mkdir()
        publication = create_source_snapshot(
            SourceSnapshotRequest(
                spec=SourceSnapshotSpec(
                    repository_id="fixture/repository",
                    commit_oid=self.fixture.commit_oid,
                    analysis_root={"path_kind": "GIT_PATH", "git_path_hex": b"pkg".hex()},
                ),
                repository_path=self.fixture.path,
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
                repository_path=self.fixture.path.resolve(),
            ),
            runtime=DerivationInputRuntime(git_executable=git_executable()),
        )

    def _run(self, key: str, *, derivation_id: str = "cell-attempt-1", **kwargs):
        return run_closed_test_execution_cell(
            self.inputs,
            derivation_id=derivation_id,
            binding=closed_test_binding(key),
            **kwargs,
        )

    def test_stable_provider_returns_one_nonpublished_owned_fact(self) -> None:
        before = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        result = self._run("stable-a")
        after = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        self.assertEqual(after, before)
        self.assertEqual(result.provider_run_status, ProviderRunStatus.COMPLETED)
        self.assertEqual(result.phase_status, PhaseStatus.COMPLETED)
        self.assertEqual(result.release_outcome, ReleaseOutcome.RELEASED)
        self.assertIsNone(result.diagnostic_code)
        facts = result.canonical_facts_copy()
        self.assertEqual(len(facts), 1)
        self.assertEqual(result.reported_fact_ids, (facts[0]["fact_id"],))
        self.assertEqual(facts[0]["provenance_refs"], [result.provider_run_id])
        self.assertNotIn("artifact_kind", facts[0])

        facts[0]["semantic_attributes"]["module_key_parts"] = ["mutated"]
        self.assertIsNone(
            result.canonical_facts_copy()[0]["semantic_attributes"]["module_key_parts"]
        )

    def test_replaceable_providers_preserve_fact_identity_not_run_identity(self) -> None:
        first = self._run("stable-a", derivation_id="cell-attempt-a")
        second = self._run("stable-b", derivation_id="cell-attempt-b")
        first_fact = first.canonical_facts_copy()[0]
        second_fact = second.canonical_facts_copy()[0]
        self.assertEqual(first_fact["fact_id"], second_fact["fact_id"])
        self.assertEqual(
            first_fact["subject_key_digest"], second_fact["subject_key_digest"]
        )
        self.assertNotEqual(first.provider_run_id, second.provider_run_id)
        self.assertNotEqual(
            first_fact["provenance_refs"], second_fact["provenance_refs"]
        )

    def test_successful_empty_provider_is_not_missing_execution(self) -> None:
        result = self._run("empty")
        self.assertEqual(result.phase_status, PhaseStatus.COMPLETED)
        self.assertEqual(result.canonical_facts_copy(), ())
        self.assertEqual(result.reported_fact_ids, ())

    def test_positive_provider_failures_keep_facts_empty(self) -> None:
        expected = {
            "failed": (PhaseStatus.FAILED, "PROVIDER_FAILED"),
            "unavailable": (PhaseStatus.UNAVAILABLE, "PROVIDER_UNAVAILABLE"),
            "bad-candidate": (
                PhaseStatus.FAILED,
                "NONCONFORMANT_PROVIDER_OUTPUT",
            ),
        }
        for key, (status, diagnostic) in expected.items():
            with self.subTest(key=key):
                result = self._run(key, derivation_id=f"attempt-{key}")
                self.assertEqual(result.phase_status, status)
                self.assertEqual(result.diagnostic_code, diagnostic)
                self.assertEqual(result.canonical_facts_copy(), ())
                self.assertEqual(result.reported_fact_ids, ())

    def test_missing_abnormal_and_bad_terminal_use_epistemic_fallback(self) -> None:
        for key in (
            "no-envelope",
            "abnormal-exit",
            "trailing-terminal",
            "partial-terminal",
            "duplicate-terminal",
            "facts-on-failure",
        ):
            with self.subTest(key=key):
                result = self._run(key, derivation_id=f"attempt-{key}")
                self.assertEqual(result.provider_run_status, ProviderRunStatus.FAILED)
                self.assertEqual(result.phase_status, PhaseStatus.FAILED)
                self.assertEqual(result.diagnostic_code, "INTERNAL_DERIVATION_ERROR")
                self.assertEqual(result.canonical_facts_copy(), ())

    def test_rejected_terminal_cannot_supply_provider_run_identity(self) -> None:
        spoofed_run_id = "0" * 64

        def reject_terminal(document, *, request):
            document["provider_run_id"] = spoofed_run_id
            raise ApplicationProtocolError("deterministic rejected terminal")

        with mock.patch(
            "veritrail_review._execution_cell.validate_terminal_document",
            side_effect=reject_terminal,
        ):
            result = self._run("stable-a", derivation_id="rejected-terminal")
        self.assertEqual(result.phase_status, PhaseStatus.FAILED)
        self.assertEqual(result.diagnostic_code, "INTERNAL_DERIVATION_ERROR")
        self.assertNotEqual(result.provider_run_id, spoofed_run_id)
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_partial_request_after_admission_cannot_produce_a_fact(self) -> None:
        def truncate_request(document, *, payload_limit):
            return encode_frame(document, payload_limit=payload_limit)[:-1]

        with mock.patch(
            "veritrail_review._execution_cell.encode_frame",
            side_effect=truncate_request,
        ):
            result = self._run("stable-a", derivation_id="partial-request")
        self.assertEqual(result.phase_status, PhaseStatus.FAILED)
        self.assertEqual(result.diagnostic_code, "INTERNAL_DERIVATION_ERROR")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_provider_cannot_self_report_fact_or_execution_identity(self) -> None:
        result = self._run("self-reporting-candidate")
        self.assertEqual(result.phase_status, PhaseStatus.FAILED)
        self.assertEqual(result.diagnostic_code, "NONCONFORMANT_PROVIDER_OUTPUT")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_tiny_request_transport_fails_before_provider_run(self) -> None:
        with self.assertRaises(DerivationExecutionCellError) as raised:
            self._run(
                "empty",
                transport_limits=ExecutionCellTransportSafetyLimits(1, 1024),
            )
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.DERIVATION_TRANSPORT_LIMIT_INSUFFICIENT,
        )

    def test_binding_mismatch_fails_before_execution(self) -> None:
        expected = closed_test_binding("stable-a")
        mismatched = ProviderBinding(
            ProviderDescriptor(
                **{
                    **expected.descriptor.document(),
                    "provider_version": "changed",
                }
            ),
            expected.launch_key,
        )
        with self.assertRaises(DerivationExecutionCellError) as raised:
            run_closed_test_execution_cell(
                self.inputs,
                derivation_id="mismatch",
                binding=mismatched,
            )
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.PROVIDER_BINDING_MISMATCH,
        )

    def test_unassigned_suspended_worker_is_terminated_without_admission(self) -> None:
        bindings = _WindowsBindings()
        original = bindings.win32job
        calls: list[int] = []

        class FailingAssignment:
            def __getattr__(self, name: str):
                return getattr(original, name)

            def AssignProcessToJobObject(self, job, process) -> None:
                calls.append(int(bindings.win32process.GetProcessId(process)))
                raise OSError("deterministic assignment failure")

        bindings.win32job = FailingAssignment()
        with mock.patch(
            "veritrail_review._windows_execution_cell._WindowsBindings",
            return_value=bindings,
        ):
            with self.assertRaises(DerivationExecutionCellError) as raised:
                self._run("empty", derivation_id="assignment-failure")
        self.assertEqual(len(calls), 1)
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.INTERNAL_DERIVATION_ADMISSION_ERROR,
        )

    def test_resume_failure_is_an_admitted_internal_result_not_no_attempt(self) -> None:
        bindings = _WindowsBindings()
        calls: list[bool] = []

        def fail_resume(_thread) -> None:
            calls.append(True)
            raise OSError("deterministic resume failure")

        with mock.patch.object(
            bindings.win32process, "ResumeThread", side_effect=fail_resume
        ):
            result = self._run("empty", derivation_id="resume-failure")
        self.assertEqual(calls, [True])
        self.assertEqual(result.provider_run_status, ProviderRunStatus.FAILED)
        self.assertEqual(result.phase_status, PhaseStatus.FAILED)
        self.assertEqual(result.diagnostic_code, "INTERNAL_DERIVATION_ERROR")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_runtime_loss_during_cell_preparation_is_typed_and_preadmission(self) -> None:
        failure = BudgetPrimitiveError(
            BudgetPrimitiveFailureCode.PLATFORM_CAPABILITY_UNAVAILABLE
        )
        with mock.patch(
            "veritrail_review._windows_execution_cell.require_budget_primitive_capability",
            side_effect=failure,
        ):
            with self.assertRaises(DerivationExecutionCellError) as raised:
                self._run("empty", derivation_id="runtime-loss")
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.DERIVATION_RUNTIME_UNAVAILABLE,
        )

    def test_release_failure_is_not_returned_as_a_phase_result(self) -> None:
        with mock.patch(
            "veritrail_review._execution_cell.run_windows_execution_cell",
            side_effect=CellReleaseError,
        ):
            with self.assertRaises(DerivationExecutionCellError) as raised:
                self._run("empty", derivation_id="release-failure")
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.RELEASE_FAILED,
        )

    def test_pre_admission_cancellation_is_not_a_phase_result(self) -> None:
        with self.assertRaises(DerivationExecutionCellError) as raised:
            self._run("empty", cancellation_requested=lambda: True)
        self.assertEqual(
            raised.exception.code,
            DerivationExecutionCellFailureCode.DERIVATION_ADMISSION_CANCELLED,
        )

    def test_deadline_interrupts_slow_provider_without_partial_fact(self) -> None:
        self.inputs = self._inputs(name="deadline", wall_clock_ms=500)
        result = self._run("slow", derivation_id="deadline-attempt")
        self.assertEqual(result.provider_run_status, ProviderRunStatus.INTERRUPTED)
        self.assertEqual(result.phase_status, PhaseStatus.INTERRUPTED)
        self.assertEqual(result.diagnostic_code, "EXECUTION_DEADLINE")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_terminal_arrival_does_not_commit_before_worker_release(self) -> None:
        self.inputs = self._inputs(name="terminal-sleep", wall_clock_ms=500)
        result = self._run(
            "terminal-then-sleep", derivation_id="terminal-sleep-attempt"
        )
        self.assertEqual(result.provider_run_status, ProviderRunStatus.INTERRUPTED)
        self.assertEqual(result.phase_status, PhaseStatus.INTERRUPTED)
        self.assertEqual(result.diagnostic_code, "EXECUTION_DEADLINE")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_late_cancellation_beats_an_early_terminal_envelope(self) -> None:
        started = time.monotonic()
        result = self._run(
            "terminal-then-sleep",
            derivation_id="terminal-cancel-attempt",
            cancellation_requested=lambda: time.monotonic() - started >= 0.1,
        )
        self.assertEqual(result.provider_run_status, ProviderRunStatus.INTERRUPTED)
        self.assertEqual(result.phase_status, PhaseStatus.INTERRUPTED)
        self.assertEqual(result.diagnostic_code, "EXECUTION_CANCELLED")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_positive_job_memory_event_is_the_only_memory_attribution(self) -> None:
        self.inputs = self._inputs(
            name="memory", wall_clock_ms=10_000, memory_bytes=100_663_296
        )
        result = self._run("memory", derivation_id="memory-attempt")
        self.assertEqual(result.provider_run_status, ProviderRunStatus.INTERRUPTED)
        self.assertEqual(result.phase_status, PhaseStatus.INTERRUPTED)
        self.assertEqual(result.diagnostic_code, "EXECUTION_MEMORY_BUDGET")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_sufficient_transport_and_budget_changes_do_not_enter_fact_identity(self) -> None:
        first = self._run("stable-a", derivation_id="safety-default")
        second = self._run(
            "stable-a",
            derivation_id="safety-tight",
            transport_limits=ExecutionCellTransportSafetyLimits(
                1_048_576, 1_048_576
            ),
        )
        third_inputs = self._inputs(name="budget-wide", wall_clock_ms=20_000)
        third = run_closed_test_execution_cell(
            third_inputs,
            derivation_id="budget-wide",
            binding=closed_test_binding("stable-a"),
        )
        facts = [
            item.canonical_facts_copy()[0]
            for item in (first, second, third)
        ]
        self.assertEqual({item["fact_id"] for item in facts}, {facts[0]["fact_id"]})
        self.assertEqual(
            {item["subject_key_digest"] for item in facts},
            {facts[0]["subject_key_digest"]},
        )
        self.assertEqual(len({item.provider_run_id for item in (first, second, third)}), 3)

    def test_primitive_commit_failure_revokes_attempt_and_cannot_leak_fact(self) -> None:
        created: list[AttemptEligibility] = []

        class TrackingEligibility(AttemptEligibility):
            def __init__(self) -> None:
                super().__init__()
                created.append(self)

        failure = BudgetPrimitiveError(
            BudgetPrimitiveFailureCode.BUDGET_CONTEXT_NOT_RUNNING
        )
        with mock.patch(
            "veritrail_review._execution_cell.AttemptEligibility",
            TrackingEligibility,
        ), mock.patch(
            "veritrail_review.budget.BudgetContext.try_complete_phase",
            side_effect=failure,
        ):
            result = self._run("stable-a", derivation_id="primitive-failure")
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].state, AttemptEligibilityState.REVOKED)
        self.assertEqual(result.phase_status, PhaseStatus.FAILED)
        self.assertEqual(result.diagnostic_code, "INTERNAL_DERIVATION_ERROR")
        self.assertEqual(result.canonical_facts_copy(), ())

    def test_retry_is_a_new_attempt_not_hidden_resume(self) -> None:
        first = self._run("stable-a", derivation_id="retry-1")
        second = self._run("stable-a", derivation_id="retry-2")
        self.assertNotEqual(first.provider_run_id, second.provider_run_id)
        self.assertEqual(
            first.canonical_facts_copy()[0]["fact_id"],
            second.canonical_facts_copy()[0]["fact_id"],
        )
        self.assertLessEqual(first.attempt_started_at, first.provider_run_started_at)
        self.assertLessEqual(first.provider_run_started_at, first.provider_run_finished_at)
        self.assertLessEqual(first.provider_run_finished_at, first.phase_finished_at)


if __name__ == "__main__":
    unittest.main()
