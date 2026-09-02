from __future__ import annotations

import copy
import http.client
import io
import os
import shutil
import socket
import sys
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from unittest.mock import patch

from veritrail.bootstrap_browser import (
    ObservedBrowserEvidence,
    collect_observed_browser_evidence,
)
from veritrail.bootstrap_preview import ResolvedBootstrap, ResolvedBootstrapNode
from veritrail.bootstrap_run import _BootstrapResourceMonitor, run_observed_bootstrap
from veritrail.canonical import sha256_json
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile
from veritrail.stop_control import StopSignal
from veritrail.windows_job import inspect_executable_identity
from veritrail.windows_service import OwnedServiceSession

from tests.support import bootstrap_plan, bootstrap_profile
from tests.test_browser_evidence import _browser_artifact

ROOT = Path(__file__).resolve().parents[1]


def _free_port(excluded: set[int] | None = None) -> int:
    excluded = set() if excluded is None else excluded
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
            candidate.bind(("127.0.0.1", 0))
            port = int(candidate.getsockname()[1])
        if port not in excluded:
            return port


def _authorities(
    subject: Path, *, application_mode: str = "application"
) -> tuple[dict, dict, ResolvedBootstrap]:
    dependency_port = _free_port()
    application_port = _free_port({dependency_port})
    raw_profile = bootstrap_profile()
    raw_profile["subject_watch_roots"] = ["watched"]
    raw_profile["lifecycle_timeout_ms"] = 15_000
    nodes = {node["node_id"]: node for node in raw_profile["nodes"]}
    dependency = nodes["dependency"]
    dependency["port"] = dependency_port
    dependency["arguments"] = [
        {"literal": "service.py"},
        {"literal": "serve"},
        {"node_port": "dependency"},
    ]
    dependency["readiness"]["interval_ms"] = 50
    dependency["readiness"]["total_timeout_ms"] = 3_000
    application = nodes["application"]
    application["port"] = application_port
    application["arguments"] = [
        {"literal": "service.py"},
        {"literal": application_mode},
        {"node_port": "application"},
        {"node_origin": "dependency"},
    ]
    application["readiness"]["interval_ms"] = 50
    application["readiness"]["total_timeout_ms"] = 3_000
    profile = seal_project_profile(raw_profile)
    raw_plan = bootstrap_plan(profile)
    raw_plan["preflight"]["ports"] = [
        {"port": dependency_port, "expected": "FREE"},
        {"port": application_port, "expected": "FREE"},
    ]
    application_origin = f"http://127.0.0.1:{application_port}"
    raw_plan["browser"]["start_url"] = f"{application_origin}/"
    raw_plan["browser"]["allowed_origins"] = [application_origin]
    for step in raw_plan["browser"]["steps"]:
        if step["action"] == "goto":
            step["url"] = f"{application_origin}/"
    plan = seal_plan(raw_plan, profile)
    preview = {
        "schema_version": "0.1",
        "plan_sha256": plan["seal"]["digest"],
        "profile_id": profile["profile_id"],
        "profile_version": profile["version"],
        "profile_sha256": profile["seal"]["digest"],
        "platform": profile["platform"],
        "cold_state": profile["cold_state"],
        "start_order": profile["start_order"],
        "teardown_order": profile["teardown_order"],
    }
    preview["preview_sha256"] = sha256_json(preview)
    environment = {
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    for name in ("SYSTEMROOT", "WINDIR"):
        value = os.environ.get(name)
        if value:
            environment[name] = value
    resolved = ResolvedBootstrap(
        preview=preview,
        subject_root=subject,
        nodes=tuple(
            ResolvedBootstrapNode(
                node_id=node_id,
                executable=Path(sys.executable),
                executable_identity=inspect_executable_identity(Path(sys.executable)),
                working_directory=subject,
                inherited_environment={
                    name: value
                    for name, value in environment.items()
                    if name in {"SYSTEMROOT", "WINDIR"}
                },
                explicit_environment={"PYTHONDONTWRITEBYTECODE": "1"},
            )
            for node_id in profile["start_order"]
        ),
    )
    return plan, profile, resolved


def _exercise(plan: dict, port: int) -> ObservedBrowserEvidence:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
    try:
        connection.request("GET", "/")
        response = connection.getresponse()
        content = response.read(4096)
    finally:
        connection.close()
    if response.status != 200 or b'"dependency_status": 200' not in content:
        raise AssertionError("application exercise did not observe its dependency")
    return ObservedBrowserEvidence(
        browser=_browser_artifact(plan),
        peak_rss_mb=8.0,
        resource_sampling_complete=True,
        process_cleanup_complete=True,
        job_memory_limit_mb=plan["browser"]["max_job_memory_mb"],
        job_memory_limit_enforced=True,
    )


def _with_blocking_browser_step(
    plan: dict,
    profile: dict,
    resolved: ResolvedBootstrap,
    *,
    lifecycle_timeout_ms: int,
) -> tuple[dict, dict, ResolvedBootstrap]:
    raw_profile = copy.deepcopy(profile)
    raw_profile.pop("seal")
    raw_profile["lifecycle_timeout_ms"] = lifecycle_timeout_ms
    updated_profile = seal_project_profile(raw_profile)
    raw_plan = copy.deepcopy(plan)
    raw_plan.pop("seal")
    raw_plan["bootstrap_profile"] = {
        "profile_id": updated_profile["profile_id"],
        "profile_version": updated_profile["version"],
        "profile_sha256": updated_profile["seal"]["digest"],
    }
    raw_plan["browser"]["steps"] = [
        {
            "id": "wait-for-unreachable-text",
            "action": "expect_text",
            "selector": "[data-testid='status']",
            "value": "this text is never produced",
        }
    ]
    updated_plan = seal_plan(raw_plan, updated_profile)
    preview = copy.deepcopy(resolved.preview)
    preview.update(
        {
            "plan_sha256": updated_plan["seal"]["digest"],
            "profile_version": updated_profile["version"],
            "profile_sha256": updated_profile["seal"]["digest"],
        }
    )
    preview.pop("preview_sha256")
    preview["preview_sha256"] = sha256_json(preview)
    return (
        updated_plan,
        updated_profile,
        ResolvedBootstrap(
            preview=preview,
            subject_root=resolved.subject_root,
            nodes=resolved.nodes,
        ),
    )


class BootstrapResourceMonitorTests(unittest.TestCase):
    def test_hard_grace_first_triggers_soft_stop_then_upgrades_to_hard(self) -> None:
        samples = iter((50, 50))
        stop_signal = StopSignal()
        monitor = _BootstrapResourceMonitor(
            {
                "available_memory_soft_min_mb": 100,
                "available_memory_hard_min_mb": 100,
                "hard_breach_grace_samples": 2,
            },
            stop_signal,
            host_memory_reader=lambda: (16 * 1024**3, next(samples) * 1024**2),
        )

        monitor._sample()
        self.assertEqual("RESOURCE_MEMORY_SOFT_LIMIT", stop_signal.reason())

        monitor._sample()
        self.assertEqual("RESOURCE_MEMORY_HARD_LIMIT", stop_signal.reason())

    def test_sampling_failure_requests_collector_stop(self) -> None:
        stop_signal = StopSignal()
        monitor = _BootstrapResourceMonitor(
            {
                "available_memory_soft_min_mb": 100,
                "available_memory_hard_min_mb": 50,
                "hard_breach_grace_samples": 2,
            },
            stop_signal,
            host_memory_reader=lambda: (_ for _ in ()).throw(OSError("unavailable")),
        )

        monitor._sample()

        self.assertEqual("COLLECTOR_ERROR", stop_signal.reason())


@unittest.skipUnless(os.name == "nt", "M10 observed bootstrap is Windows-only")
class BootstrapObservedRunTests(unittest.TestCase):
    def _subject(self, root: Path) -> Path:
        subject = root / "subject"
        watched = subject / "watched"
        watched.mkdir(parents=True)
        (watched / "state.txt").write_text("stable\n", encoding="utf-8")
        shutil.copy2(
            ROOT / "tests" / "fixtures" / "m10_service_helper.py",
            subject / "service.py",
        )
        return subject

    def test_owned_staging_survives_teardown_then_builds_strict_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)
            application_port = next(
                node["port"]
                for node in profile["nodes"]
                if node["role"] == "APPLICATION"
            )
            staged: list[bytes] = []

            def writer(path: Path, content: bytes) -> None:
                staged.append(content)
                with path.open("xb") as handle:
                    handle.write(content)
                    handle.flush()
                    os.fsync(handle.fileno())

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                browser_runner=lambda active_plan: _exercise(
                    active_plan, application_port
                ),
                staging_writer=writer,
            )
            self.assertIsNone(result.error_type)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("COMPLETED", result.evidence.execution_status)
            self.assertTrue(result.evidence.continue_pipeline)
            self.assertTrue(result.run_work_released)
            self.assertTrue(result.staging_released)
            self.assertTrue(result.owned_root_released)
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))
            self.assertEqual(1, len(staged))
            self.assertNotIn(str(subject).encode("utf-8"), staged[0])
            self.assertNotIn(b"owning_pid", staged[0])
            self.assertIn(b'"record_type":"bootstrap.pre_teardown"', staged[0])
            self.assertTrue(result.resource_observation["sampling_complete"])
            self.assertGreater(result.resource_observation["core_peak_rss_mb"], 0)
            self.assertGreater(result.resource_observation["dependency_peak_rss_mb"], 0)
            self.assertGreater(result.resource_observation["application_peak_rss_mb"], 0)
            self.assertEqual(False, result.subject_observation["changed"])

    def test_subject_drift_is_observed_without_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)
            application_port = next(
                node["port"] for node in profile["nodes"] if node["role"] == "APPLICATION"
            )

            def exercise_with_drift(active_plan: dict) -> ObservedBrowserEvidence:
                observed = _exercise(active_plan, application_port)
                (subject / "watched" / "state.txt").write_text(
                    "changed\n", encoding="utf-8"
                )
                return observed

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                browser_runner=exercise_with_drift,
            )
            self.assertIsNotNone(result.evidence)
            self.assertEqual(True, result.subject_observation["changed"])
            self.assertEqual(
                "SUBJECT_DRIFT",
                result.evidence.bootstrap.document["facts"]["stop"]["reason"],
            )
            self.assertEqual(
                "changed\n",
                (subject / "watched" / "state.txt").read_text(encoding="utf-8"),
            )
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_staging_failure_still_cleans_both_jobs_and_owned_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)
            application_port = next(
                node["port"] for node in profile["nodes"] if node["role"] == "APPLICATION"
            )

            def fail_staging(path: Path, content: bytes) -> None:
                path.write_bytes(content[:17])
                raise OSError("injected staging failure")

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                browser_runner=lambda active_plan: _exercise(
                    active_plan, application_port
                ),
                staging_writer=fail_staging,
            )
            self.assertIsNotNone(result.evidence)
            self.assertEqual("EVIDENCE_STAGING_FAILED", result.error_type)
            self.assertEqual("EVIDENCE_ERROR", result.lifecycle.stop_reason)
            self.assertEqual("ERROR", result.evidence.execution_status)
            self.assertFalse(result.evidence.continue_pipeline)
            self.assertIn(
                ("EVIDENCE_FINALIZATION", "EVIDENCE_STAGING_FAILED"),
                [(event.stage, event.result) for event in result.lifecycle.events],
            )
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertTrue(result.run_work_released)
            self.assertTrue(result.staging_released)
            self.assertTrue(result.owned_root_released)
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_resource_monitor_stops_before_owned_service_teardown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)
            application_port = next(
                node["port"] for node in profile["nodes"] if node["role"] == "APPLICATION"
            )
            teardown_started = threading.Event()

            class TeardownSamplingGuard:
                def __init__(self, session: OwnedServiceSession) -> None:
                    self._session = session

                def __getattr__(self, name: str):
                    return getattr(self._session, name)

                def sample_rss_bytes(self) -> int:
                    if teardown_started.is_set():
                        raise OSError("resource sampling crossed into teardown")
                    return self._session.sample_rss_bytes()

                def terminate(self):
                    teardown_started.set()
                    time.sleep(0.15)
                    return self._session.terminate()

            def guarded_session_factory(**values):
                return TeardownSamplingGuard(OwnedServiceSession.start(**values))

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                browser_runner=lambda active_plan: _exercise(
                    active_plan, application_port
                ),
                session_factory=guarded_session_factory,
            )

            self.assertTrue(teardown_started.is_set())
            self.assertIsNone(result.error_type)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("COMPLETED", result.evidence.execution_status)
            self.assertTrue(result.resource_observation["sampling_complete"])
            self.assertEqual("NONE", result.lifecycle.stop_reason)
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_browser_observer_failure_is_collector_error_not_business_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)
            application_port = next(
                node["port"] for node in profile["nodes"] if node["role"] == "APPLICATION"
            )

            def incomplete_observer(active_plan: dict) -> ObservedBrowserEvidence:
                observed = _exercise(active_plan, application_port)
                return ObservedBrowserEvidence(
                    browser=observed.browser,
                    peak_rss_mb=observed.peak_rss_mb,
                    resource_sampling_complete=True,
                    process_cleanup_complete=False,
                    job_memory_limit_mb=observed.job_memory_limit_mb,
                    job_memory_limit_enforced=True,
                )

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                browser_runner=incomplete_observer,
            )

            self.assertIsNone(result.error_type)
            self.assertIsNotNone(result.browser)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("COLLECTOR_ERROR", result.lifecycle.stop_reason)
            self.assertEqual("ERROR", result.evidence.execution_status)
            self.assertFalse(result.evidence.continue_pipeline)
            self.assertTrue(result.lifecycle.cleanup_complete)
            bootstrap = result.evidence.bootstrap.document["facts"]
            self.assertEqual("CLEANUP_ERROR", bootstrap["stop"]["reason"])
            self.assertFalse(bootstrap["cleanup_complete"])
            self.assertFalse(
                bootstrap["browser_exercise"]["process_cleanup_complete"]
            )
            self.assertEqual(
                ["application", "dependency"],
                list(result.lifecycle.actual_teardown_order),
            )
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_real_chromium_is_observed_and_linked_before_reverse_teardown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(
                subject, application_mode="browser-application"
            )

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
            )

            self.assertIsNone(result.error_type)
            self.assertIsNotNone(result.browser)
            self.assertIsNotNone(result.evidence)
            browser = result.browser.document["facts"]
            bootstrap = result.evidence.bootstrap.document["facts"]
            self.assertTrue(browser["capture_complete"])
            self.assertTrue(browser["all_steps_passed"])
            self.assertEqual(2, browser["viewport_count"])
            self.assertEqual(2, browser["screenshot_count"])
            self.assertEqual(
                result.browser.sha256,
                bootstrap["browser_exercise"]["evidence_sha256"],
            )
            self.assertTrue(result.resource_observation["sampling_complete"])
            self.assertGreater(result.resource_observation["browser_peak_rss_mb"], 0)
            self.assertEqual(
                ["application", "dependency"],
                list(result.lifecycle.actual_teardown_order),
            )
            self.assertTrue(result.lifecycle.cleanup_complete)
            stages = [event.stage for event in result.lifecycle.events]
            self.assertLess(stages.index("EXERCISED"), stages.index("EVIDENCE_FINALIZED"))
            self.assertLess(
                stages.index("EVIDENCE_FINALIZED"),
                stages.index("TEARDOWN_APPLICATION"),
            )
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_real_browser_popup_is_rejected_and_cannot_claim_complete_capture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(
                subject, application_mode="browser-application"
            )
            raw_plan = copy.deepcopy(plan)
            raw_plan.pop("seal")
            raw_plan["browser"]["steps"] = [
                {
                    "id": "open-unexpected-popup",
                    "action": "click",
                    "selector": "[data-testid='open-popup']",
                }
            ]
            plan = seal_plan(raw_plan, profile)
            preview = copy.deepcopy(resolved.preview)
            preview["plan_sha256"] = plan["seal"]["digest"]
            preview.pop("preview_sha256")
            preview["preview_sha256"] = sha256_json(preview)
            resolved = ResolvedBootstrap(
                preview=preview,
                subject_root=resolved.subject_root,
                nodes=resolved.nodes,
            )

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
            )

            self.assertIsNone(result.error_type)
            self.assertIsNotNone(result.browser)
            browser = result.browser.document["facts"]
            self.assertFalse(browser["capture_complete"])
            self.assertEqual(
                [
                    {"collector": "page-set:desktop", "error_type": "UnexpectedPage"},
                    {"collector": "page-set:mobile", "error_type": "UnexpectedPage"},
                ],
                browser["collection_errors"],
            )
            self.assertEqual("COLLECTOR_ERROR", result.lifecycle.stop_reason)
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_real_browser_hard_failure_keeps_evidence_and_cleans_resources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(
                subject, application_mode="browser-application"
            )
            raw_plan = copy.deepcopy(plan)
            raw_plan.pop("seal")
            raw_plan["browser"]["timeout_ms"] = 1_000
            raw_plan["browser"]["steps"][0]["selector"] = "[data-testid='missing']"
            plan = seal_plan(raw_plan, profile)
            preview = copy.deepcopy(resolved.preview)
            preview["plan_sha256"] = plan["seal"]["digest"]
            preview.pop("preview_sha256")
            preview["preview_sha256"] = sha256_json(preview)
            resolved = ResolvedBootstrap(
                preview=preview,
                subject_root=resolved.subject_root,
                nodes=resolved.nodes,
            )

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
            )

            self.assertIsNone(result.error_type)
            self.assertIsNotNone(result.browser)
            self.assertIsNotNone(result.evidence)
            self.assertFalse(result.browser.document["facts"]["capture_complete"])
            self.assertEqual("BROWSER_HARD_FAILURE", result.lifecycle.stop_reason)
            self.assertIn(
                ("EXERCISED", "BROWSER_HARD_FAILURE"),
                [(event.stage, event.result) for event in result.lifecycle.events],
            )
            self.assertEqual("COMPLETED", result.evidence.execution_status)
            self.assertTrue(result.evidence.continue_pipeline)
            self.assertEqual(
                "BROWSER_HARD_FAILURE",
                result.evidence.bootstrap.document["facts"]["stop"]["reason"],
            )
            self.assertTrue(result.resource_observation["sampling_complete"])
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertEqual(
                ["application", "dependency"],
                list(result.lifecycle.actual_teardown_order),
            )
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_user_cancel_interrupts_active_browser_and_preserves_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(
                subject, application_mode="browser-application"
            )
            plan, profile, resolved = _with_blocking_browser_step(
                plan,
                profile,
                resolved,
                lifecycle_timeout_ms=15_000,
            )
            cancellation = threading.Event()
            browser_entered = threading.Event()
            original = collect_observed_browser_evidence

            def observed_browser(active_plan: dict, **kwargs):
                browser_entered.set()
                return original(active_plan, **kwargs)

            def cancel_during_browser() -> None:
                self.assertTrue(browser_entered.wait(5))
                time.sleep(0.5)
                cancellation.set()

            trigger = threading.Thread(target=cancel_during_browser, daemon=True)
            trigger.start()
            with patch(
                "veritrail.bootstrap_run.collect_observed_browser_evidence",
                side_effect=observed_browser,
            ):
                captured_stderr = io.StringIO()
                with redirect_stderr(captured_stderr):
                    result = run_observed_bootstrap(
                        plan,
                        profile,
                        resolved,
                        output_parent=root / "artifacts",
                        cancel_event=cancellation,
                    )
            trigger.join(2)

            self.assertFalse(trigger.is_alive())
            self.assertNotIn(
                "Error occurred in event listener", captured_stderr.getvalue()
            )
            self.assertEqual("USER_CANCELLED", result.lifecycle.stop_reason)
            self.assertTrue(result.lifecycle.ready_callback_started)
            self.assertFalse(result.lifecycle.ready_callback_completed)
            self.assertIsNone(result.browser)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("ABORTED", result.evidence.execution_status)
            bootstrap = result.evidence.bootstrap.document["facts"]
            self.assertTrue(bootstrap["browser_exercise"]["started"])
            self.assertFalse(bootstrap["browser_exercise"]["completed"])
            self.assertTrue(
                bootstrap["browser_exercise"]["process_cleanup_complete"]
            )
            self.assertEqual(
                ["application", "dependency"],
                list(result.lifecycle.actual_teardown_order),
            )
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_lifecycle_deadline_interrupts_active_browser_before_policy_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(
                subject, application_mode="browser-application"
            )
            plan, profile, resolved = _with_blocking_browser_step(
                plan,
                profile,
                resolved,
                lifecycle_timeout_ms=5_000,
            )
            started = time.monotonic()
            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
            )
            elapsed = time.monotonic() - started

            self.assertEqual("LIFECYCLE_TIMEOUT", result.lifecycle.stop_reason)
            self.assertLess(elapsed, 9.0)
            self.assertIsNone(result.browser)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("ABORTED", result.evidence.execution_status)
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertEqual(
                ["application", "dependency"],
                list(result.lifecycle.actual_teardown_order),
            )
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_runtime_host_memory_hard_limit_aborts_and_cleans_started_node(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)
            low_available = 100 * 1024 * 1024
            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                host_memory_reader=lambda: (16 * 1024**3, low_available),
            )

            self.assertEqual(
                "RESOURCE_MEMORY_HARD_LIMIT", result.lifecycle.stop_reason
            )
            self.assertEqual((), result.lifecycle.actual_start_order)
            self.assertEqual((), result.lifecycle.actual_teardown_order)
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertIsNone(result.browser)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("ABORTED", result.evidence.execution_status)
            resource = result.resource_observation
            self.assertEqual(
                "RESOURCE_MEMORY_HARD_LIMIT", resource["limit_trigger_reason"]
            )
            self.assertGreaterEqual(
                resource["max_consecutive_memory_hard_breaches"],
                resource["hard_breach_grace_samples"],
            )
            self.assertEqual(100.0, resource["host_available_memory_min_mb"])
            self.assertTrue(resource["sampling_complete"])
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_runtime_host_memory_soft_limit_stops_before_process_start(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)
            soft_only_available = 3_000 * 1024 * 1024

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                host_memory_reader=lambda: (16 * 1024**3, soft_only_available),
            )

            self.assertEqual("RESOURCE_MEMORY_SOFT_LIMIT", result.lifecycle.stop_reason)
            self.assertEqual((), result.lifecycle.actual_start_order)
            self.assertEqual((), result.lifecycle.actual_teardown_order)
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertIsNone(result.browser)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("ABORTED", result.evidence.execution_status)
            resource = result.resource_observation
            self.assertEqual(
                "RESOURCE_MEMORY_SOFT_LIMIT", resource["limit_trigger_reason"]
            )
            self.assertEqual(3_000.0, resource["host_available_memory_min_mb"])
            self.assertTrue(resource["sampling_complete"])
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

    def test_runtime_host_memory_sampling_failure_fails_closed_before_process_start(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject = self._subject(root)
            plan, profile, resolved = _authorities(subject)

            result = run_observed_bootstrap(
                plan,
                profile,
                resolved,
                output_parent=root / "artifacts",
                host_memory_reader=lambda: (_ for _ in ()).throw(
                    OSError("unavailable")
                ),
            )

            self.assertEqual("COLLECTOR_ERROR", result.lifecycle.stop_reason)
            self.assertEqual((), result.lifecycle.actual_start_order)
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertIsNotNone(result.evidence)
            self.assertEqual("EVIDENCE_ERROR", result.evidence.bootstrap.document["facts"]["stop"]["reason"])
            self.assertEqual("ERROR", result.evidence.execution_status)
            self.assertFalse(result.resource_observation["sampling_complete"])
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))

if __name__ == "__main__":
    unittest.main()
