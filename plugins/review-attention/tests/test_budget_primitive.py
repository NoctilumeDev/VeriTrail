from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import venv
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from veritrail_review._artifact_budget import _OwnedArtifactStaging
from veritrail_review._windows_budget import _run_owned_process_cell
from veritrail_review.budget import (
    BudgetContext,
    BudgetState,
    BudgetStopTrigger,
    ExecutionBudgetLimits,
    MemoryAttributionState,
    admit_derivation_budget,
)
from veritrail_review.canonical import canonical_json_bytes
from veritrail_review.derivation_input_contracts import DerivationInputSet
from veritrail_review.errors import BudgetPrimitiveError


HELPER = Path(__file__).resolve().parent / "helpers" / "budget_worker.py"
STABLE_BYTES = b'{"value":"stable"}\n'


class _FakeClock:
    def __init__(self, value: float = 100.0) -> None:
        self.value = value
        self._lock = threading.Lock()

    def __call__(self) -> float:
        with self._lock:
            return self.value

    def advance(self, seconds: float) -> None:
        with self._lock:
            self.value += seconds


class _AdvancingClock:
    def __init__(self, value: float = 100.0, step: float = 0.001) -> None:
        self.value = value
        self.step = step

    def __call__(self) -> float:
        current = self.value
        self.value += self.step
        return current


def _context(
    *,
    wall_clock_ms: int = 5_000,
    memory_bytes: int = 256 * 1024 * 1024,
    artifact_bytes: int = 1024,
    clock: _FakeClock | None = None,
) -> BudgetContext:
    return BudgetContext._admit_for_testing(
        ExecutionBudgetLimits(
            wall_clock_ms=wall_clock_ms,
            memory_bytes=memory_bytes,
            artifact_bytes=artifact_bytes,
        ),
        clock=clock or __import__("time").monotonic,
    )


@unittest.skipUnless(os.name == "nt", "Windows reference primitive")
class WindowsBudgetPrimitiveTests(unittest.TestCase):
    def run_cell(
        self,
        context: BudgetContext,
        mode: str,
        root: Path,
        *,
        cancel_after_ms: int | None = None,
    ) -> tuple[object, Path]:
        result = root / "result.json"
        cancel_at = (
            None
            if cancel_after_ms is None
            else context.started_at_monotonic + cancel_after_ms / 1000.0
        )
        observation = _run_owned_process_cell(
            context,
            executable=Path(sys.executable).resolve(strict=True),
            arguments=(os.fspath(HELPER), mode, os.fspath(result)),
            cancellation_requested=(
                None if cancel_at is None else lambda: time.monotonic() >= cancel_at
            ),
        )
        if context.state is BudgetState.STOPPING:
            context._mark_release(
                residue_free=(
                    observation.active_process_zero and observation.handles_released
                )
            )
        return observation, result

    def test_bp_001_sufficient_budget_closes_resources_before_phase_commit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp001-") as name:
            context = _context()
            observation, result = self.run_cell(context, "result", Path(name))
            phase_result = context.try_complete_phase(
                result.read_bytes(),
                resources_closed=(
                    observation.active_process_zero and observation.handles_released
                ),
            )
        self.assertEqual(phase_result.canonical_bytes, STABLE_BYTES)
        self.assertTrue(observation.active_process_zero)
        self.assertTrue(observation.handles_released)
        self.assertIsNone(observation.stop_trigger)
        self.assertEqual(context.state, BudgetState.RUNNING)

    def test_expired_context_never_grants_worker_execution_rights(self) -> None:
        clock = _FakeClock()
        context = _context(wall_clock_ms=1_000, clock=clock)
        clock.advance(1.0)
        with tempfile.TemporaryDirectory(
            prefix="veritrail-r1-expired-process-start-"
        ) as name:
            observation, result = self.run_cell(context, "result", Path(name))
            self.assertFalse(result.exists())
        self.assertFalse(observation.process_created_suspended)
        self.assertFalse(observation.process_resumed)
        self.assertTrue(observation.active_process_zero)
        self.assertTrue(observation.handles_released)
        self.assertEqual(
            observation.stop_trigger, BudgetStopTrigger.EXECUTION_DEADLINE
        )
        self.assertEqual(context.state, BudgetState.RELEASED)

    def test_bp_002_absolute_deadline_rejects_late_result_and_releases_tree(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp002-") as name:
            context = _context(wall_clock_ms=500)
            observation, result = self.run_cell(
                context, "result-then-sleep", Path(name)
            )
            self.assertTrue(result.is_file())
            self.assertIsNone(
                context.try_complete_phase(
                    result.read_bytes(), resources_closed=True
                )
            )
        self.assertEqual(
            observation.stop_trigger, BudgetStopTrigger.EXECUTION_DEADLINE
        )
        self.assertTrue(observation.active_process_zero)
        self.assertEqual(context.state, BudgetState.RELEASED)

    def test_bp_003_caller_cancellation_releases_whole_tree(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp003-") as name:
            context = _context()
            observation, _ = self.run_cell(
                context, "sleep", Path(name), cancel_after_ms=200
            )
        self.assertEqual(
            observation.stop_trigger, BudgetStopTrigger.EXECUTION_CANCELLED
        )
        self.assertTrue(observation.active_process_zero)
        self.assertEqual(context.state, BudgetState.RELEASED)

    def test_bp_004_positive_owned_memory_event_warrants_memory_stop(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp004-") as name:
            observation, _ = self.run_cell(
                _context(wall_clock_ms=10_000, memory_bytes=64 * 1024 * 1024),
                "memory",
                Path(name),
            )
        self.assertTrue(observation.memory_limit_event_observed)
        self.assertEqual(
            observation.memory_attribution,
            MemoryAttributionState.POSITIVELY_OBSERVED,
        )
        self.assertEqual(
            observation.stop_trigger, BudgetStopTrigger.EXECUTION_MEMORY_BUDGET
        )
        self.assertTrue(observation.active_process_zero)

    def test_bp_011_descendant_is_contained_and_whole_tree_reaches_zero(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp011-") as name:
            observation, _ = self.run_cell(
                _context(), "descendant", Path(name), cancel_after_ms=300
            )
        self.assertTrue(observation.job_configured_before_process)
        self.assertTrue(observation.observation_channel_associated_before_process)
        self.assertTrue(observation.process_created_suspended)
        self.assertTrue(observation.process_assigned_before_resume)
        self.assertTrue(observation.process_resumed)
        self.assertTrue(observation.active_process_zero)

    def test_bp_012_sufficient_budgets_do_not_change_helper_output_bytes(self) -> None:
        outputs = []
        for wall_clock_ms in (3_000, 6_000):
            with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp012-") as name:
                context = _context(wall_clock_ms=wall_clock_ms)
                observation, result = self.run_cell(
                    context, "result", Path(name)
                )
                phase_result = context.try_complete_phase(
                    result.read_bytes(),
                    resources_closed=(
                        observation.active_process_zero and observation.handles_released
                    ),
                )
                outputs.append(phase_result.canonical_bytes)
        self.assertEqual(outputs, [STABLE_BYTES, STABLE_BYTES])

    def test_bp_015_result_without_resource_closure_never_becomes_phase_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp015-") as name:
            root = Path(name)
            result = root / "result.json"
            context = _context(wall_clock_ms=1_500)
            holder: list[tuple[object, Path]] = []
            execution = threading.Thread(
                target=lambda: holder.append(
                    self.run_cell(context, "result-then-sleep", root)
                )
            )
            execution.start()
            while (
                not result.is_file()
                and time.monotonic() < context.execution_deadline_monotonic
            ):
                time.sleep(0.005)
            self.assertTrue(result.is_file())
            self.assertIsNone(
                context.try_complete_phase(
                    result.read_bytes(), resources_closed=False
                )
            )
            execution.join(8)
            self.assertFalse(execution.is_alive())
            observation, _ = holder[0]
        self.assertEqual(
            observation.stop_trigger, BudgetStopTrigger.EXECUTION_DEADLINE
        )
        self.assertTrue(observation.active_process_zero)


class DeterministicBudgetPrimitiveTests(unittest.TestCase):
    def test_admission_copy_owns_the_sealed_review_policy_budget(self) -> None:
        policy = {
            "execution_budget": {
                "wall_clock_ms": 1234,
                "memory_bytes": 67_108_864,
                "artifact_bytes": 9876,
            }
        }
        inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=b"{}",
            review_policy_canonical_bytes=canonical_json_bytes(policy),
            derivation_profile_canonical_bytes=b"{}",
            verified_blob_bytes_by_object_identity={},
            source_snapshot_digest="0" * 64,
            policy_digest="1" * 64,
            analysis_scope_digest="2" * 64,
            slice_policy_digest="3" * 64,
            derivation_profile_digest="4" * 64,
        )
        context = admit_derivation_budget(inputs)
        policy["execution_budget"]["wall_clock_ms"] = 9999
        self.assertEqual(context.limits.wall_clock_ms, 1234)
        self.assertEqual(context.limits.memory_bytes, 67_108_864)
        self.assertEqual(context.limits.artifact_bytes, 9876)

    def test_bp_005_active_hard_limit_without_event_never_grants_memory_attribution(self) -> None:
        clock = _FakeClock()
        context = _context(clock=clock)
        self.assertTrue(context.checkpoint())
        self.assertIsNone(context.stop_trigger)
        self.assertEqual(
            context.memory_attribution, MemoryAttributionState.NOT_OBSERVED
        )

    def test_bp_006_same_checkpoint_uses_fixed_rank_and_latches_once(self) -> None:
        clock = _FakeClock()
        context = _context(wall_clock_ms=1_000, clock=clock)
        clock.advance(1.0)
        selected = context._checkpoint_observations(
            now=clock(),
            cancellation_observed=True,
            memory_limit_event_observed=True,
            artifact_over_budget=True,
        )
        self.assertEqual(selected, BudgetStopTrigger.EXECUTION_DEADLINE)
        latched_at = context.stop_latched_at_monotonic
        context._checkpoint_observations(
            now=clock() + 10,
            cancellation_observed=True,
            memory_limit_event_observed=True,
            artifact_over_budget=True,
        )
        self.assertEqual(context.stop_trigger, BudgetStopTrigger.EXECUTION_DEADLINE)
        self.assertEqual(context.stop_latched_at_monotonic, latched_at)

        cancellation_first = _context(clock=_FakeClock())
        winner = cancellation_first._checkpoint_observations(
            now=cancellation_first.started_at_monotonic,
            cancellation_observed=True,
            memory_limit_event_observed=True,
            artifact_over_budget=True,
        )
        self.assertEqual(winner, BudgetStopTrigger.EXECUTION_CANCELLED)

    def test_bp_007_exact_artifact_ceiling_reserves_and_writes_staging(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp007-") as name:
            root = Path(name)
            context = _context(artifact_bytes=9)
            staging = _OwnedArtifactStaging(root, context)
            self.assertTrue(staging.write("a.json", b"1234"))
            self.assertTrue(staging.write("nested/b.json", b"56789"))
            self.assertEqual(context.reserved_artifact_bytes, 9)
            self.assertEqual((staging.path / "nested/b.json").read_bytes(), b"56789")
            staging.cleanup()
            self.assertFalse(staging.path.exists())

    def test_bp_008_one_byte_over_stops_before_target_creation_and_removes_staging(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp008-") as name:
            root = Path(name)
            context = _context(artifact_bytes=8)
            staging = _OwnedArtifactStaging(root, context)
            self.assertTrue(staging.write("a.json", b"1234"))
            self.assertFalse(staging.write("nested/b.json", b"56789"))
            self.assertEqual(
                context.stop_trigger, BudgetStopTrigger.EXECUTION_ARTIFACT_BUDGET
            )
            self.assertEqual(context.reserved_artifact_bytes, 4)
            self.assertFalse(staging.path.exists())
            self.assertEqual(list(root.iterdir()), [])
            self.assertEqual(context.state, BudgetState.STOPPING)
            self.assertEqual(
                context._mark_release(residue_free=True), BudgetState.RELEASED
            )

    def test_artifact_staging_rejects_windows_alias_and_traversal_paths(self) -> None:
        for relative in ("../outside", "nested\\..\\outside", "file.json:stream"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory(
                prefix="veritrail-r1-artifact-path-"
            ) as name:
                staging = _OwnedArtifactStaging(Path(name), _context())
                with self.assertRaises(BudgetPrimitiveError):
                    staging.write(relative, b"x")
                staging.cleanup()

    def test_expired_context_cannot_create_artifact_staging(self) -> None:
        clock = _FakeClock()
        context = _context(wall_clock_ms=1_000, clock=clock)
        clock.advance(1.0)
        with tempfile.TemporaryDirectory(
            prefix="veritrail-r1-expired-staging-"
        ) as name:
            root = Path(name)
            with self.assertRaises(BudgetPrimitiveError):
                _OwnedArtifactStaging(root, context)
            self.assertEqual(list(root.iterdir()), [])
        self.assertEqual(context.stop_trigger, BudgetStopTrigger.EXECUTION_DEADLINE)
        self.assertEqual(context.state, BudgetState.STOPPING)
        self.assertEqual(
            context._mark_release(residue_free=True), BudgetState.RELEASED
        )

    def test_deadline_crossing_during_staging_removes_partial_target(self) -> None:
        clock = _AdvancingClock()
        context = BudgetContext._admit_for_testing(
            ExecutionBudgetLimits(
                wall_clock_ms=4,
                memory_bytes=64 * 1024 * 1024,
                artifact_bytes=65_537,
            ),
            clock=clock,
        )
        with tempfile.TemporaryDirectory(
            prefix="veritrail-r1-staging-deadline-"
        ) as name:
            root = Path(name)
            staging = _OwnedArtifactStaging(root, context)
            self.assertFalse(staging.write("candidate.bin", b"x" * 65_537))
            self.assertEqual(list(root.iterdir()), [])
        self.assertEqual(context.stop_trigger, BudgetStopTrigger.EXECUTION_DEADLINE)
        self.assertEqual(context.state, BudgetState.STOPPING)
        self.assertEqual(context._mark_release(residue_free=True), BudgetState.RELEASED)

    def test_staging_cleanup_cannot_claim_whole_context_release(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="veritrail-r1-staging-release-ownership-"
        ) as name:
            context = _context()
            staging = _OwnedArtifactStaging(Path(name), context)
            self.assertTrue(context.request_cancellation())
            self.assertTrue(staging.cleanup())
            self.assertEqual(context.state, BudgetState.STOPPING)

    def test_bp_009_cleanup_after_deadline_cannot_restore_late_result(self) -> None:
        clock = _FakeClock()
        context = _context(wall_clock_ms=1_000, clock=clock)
        clock.advance(1.1)
        self.assertFalse(context.checkpoint())
        self.assertIsNone(
            context.try_complete_phase(
                STABLE_BYTES,
                resources_closed=True,
                completed_at_monotonic=clock(),
            )
        )
        clock.advance(1.0)
        self.assertEqual(context._mark_release(residue_free=True), BudgetState.RELEASED)
        self.assertIsNone(context.try_complete_phase(STABLE_BYTES, resources_closed=True))

    def test_bp_010_cleanup_escalation_never_refreshes_release_deadline(self) -> None:
        clock = _FakeClock()
        context = _context(clock=clock)
        context.request_cancellation()
        deadline = context.release_deadline_monotonic
        for advance in (0.5, 1.0, 2.0):
            clock.advance(advance)
            context._checkpoint_observations(
                now=clock(), cancellation_observed=True
            )
            self.assertEqual(context.release_deadline_monotonic, deadline)
        self.assertAlmostEqual(context.remaining_release_seconds(), 1.5)

    def test_bp_014_fresh_interpreter_imports_base_without_native_modules(self) -> None:
        script = """
import json
from importlib.util import find_spec
import veritrail_review
try:
    veritrail_review.require_budget_primitive_capability()
except veritrail_review.BudgetPrimitiveError as exc:
    code = exc.code.value
else:
    code = 'NO_ERROR'
print(json.dumps({'win32job': find_spec('win32job'), 'code': code}))
"""
        with tempfile.TemporaryDirectory(prefix="veritrail-r1-bp014-") as name:
            root = Path(name)
            probe_environment = os.environ.copy()
            probe_environment.pop("PYTHONPATH", None)
            wheelhouse = root / "wheelhouse"
            wheelhouse.mkdir()
            package_source = root / "review-attention"
            shutil.copytree(
                PLUGIN_ROOT,
                package_source,
                ignore=shutil.ignore_patterns(
                    "__pycache__", "*.pyc", "build", "*.egg-info"
                ),
            )
            wheel_build = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    "--no-deps",
                    "--wheel-dir",
                    os.fspath(wheelhouse),
                    os.fspath(package_source),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=probe_environment,
            )
            self.assertEqual(
                wheel_build.returncode,
                0,
                f"wheel build failed:\n{wheel_build.stdout}\n{wheel_build.stderr}",
            )
            environment = root / "base-environment"
            venv.EnvBuilder(with_pip=True).create(environment)
            python = environment / "Scripts" / "python.exe"
            wheel = next(wheelhouse.glob("veritrail_review_attention-*.whl"))
            wheel_install = subprocess.run(
                [
                    os.fspath(python),
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    os.fspath(wheel),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=probe_environment,
            )
            self.assertEqual(
                wheel_install.returncode,
                0,
                f"wheel install failed:\n{wheel_install.stdout}\n{wheel_install.stderr}",
            )
            completed = subprocess.run(
                [os.fspath(python), "-I", "-c", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=probe_environment,
            )
            self.assertEqual(
                completed.returncode,
                0,
                "fresh interpreter probe failed:\n"
                f"{completed.stdout}\n{completed.stderr}",
            )
        result = json.loads(completed.stdout)
        self.assertIsNone(result["win32job"])
        self.assertEqual(result["code"], "PLATFORM_CAPABILITY_UNAVAILABLE")

    def test_bp_016_phase_commit_and_stop_share_one_atomic_boundary(self) -> None:
        clock = _FakeClock()
        context = _context(clock=clock)
        lock_held = threading.Event()
        release = threading.Event()
        original_clock = context._clock

        def blocking_clock() -> float:
            lock_held.set()
            release.wait(2)
            return original_clock()

        context._clock = blocking_clock
        result_holder: list[object] = []
        completion = threading.Thread(
            target=lambda: result_holder.append(
                context.try_complete_phase(STABLE_BYTES, resources_closed=True)
            )
        )
        completion.start()
        self.assertTrue(lock_held.wait(1))
        cancellation_result: list[bool] = []
        cancellation = threading.Thread(
            target=lambda: cancellation_result.append(context.request_cancellation())
        )
        cancellation.start()
        release.set()
        completion.join(2)
        cancellation.join(2)
        self.assertFalse(completion.is_alive())
        self.assertFalse(cancellation.is_alive())
        self.assertIsNotNone(result_holder[0])
        self.assertTrue(cancellation_result[0])
        self.assertEqual(
            context.stop_trigger, BudgetStopTrigger.EXECUTION_CANCELLED
        )
        self.assertEqual(result_holder[0].canonical_bytes, STABLE_BYTES)

        stop_first = _context(clock=_FakeClock())
        self.assertTrue(stop_first.request_cancellation())
        self.assertIsNone(
            stop_first.try_complete_phase(STABLE_BYTES, resources_closed=True)
        )


if __name__ == "__main__":
    unittest.main()
