from __future__ import annotations

import copy
import io
import json
import os
import shutil
import socket
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from veritrail.batching import BatchError, _load_source as load_batch_source
from veritrail.bootstrap_evidence import collect_bootstrap_evidence
from veritrail.bootstrap_lifecycle import (
    BootstrapLifecycleEvent,
    BootstrapLifecycleObservation,
    BootstrapNodeObservation,
    materialize_bootstrap_service_specs,
    run_bootstrap_lifecycle,
)
from veritrail.bootstrap_preview import build_bootstrap_preview, resolve_bootstrap
from veritrail.bootstrap_run import _OwnedBootstrapWorkspace
from veritrail.canonical import sha256_json
from veritrail.catalog import validate_bundle
from veritrail.cli import main
from veritrail.comparison import create_comparison_bundle
from veritrail.evidence import (
    import_evidence_document,
    validate_evidence,
    verify_imported_evidence,
)
from veritrail.errors import ValidationError
from veritrail.pairing import PairingError, _load_source as load_pairing_source
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile
from veritrail.reporting import create_bundle
from veritrail.resources import collect_preflight_evidence
from veritrail.windows_job import CapturedStream
from veritrail.windows_readiness import OwnedReadinessObservation, ReadinessAttempt
from veritrail.windows_service import (
    OwnedServiceStartObservation,
    OwnedServiceTeardownObservation,
)

from tests.support import ROOT, single_bootstrap_plan, single_bootstrap_profile
from tests.test_browser_evidence import _browser_artifact


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
        candidate.bind(("127.0.0.1", 0))
        return int(candidate.getsockname()[1])


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(0.2)
        return client.connect_ex(("127.0.0.1", port)) != 0


def _start() -> OwnedServiceStartObservation:
    return OwnedServiceStartObservation(
        parent_in_job=False,
        process_created=True,
        target_assigned=True,
        target_resumed=True,
        active_process_limit=8,
        active_process_limit_enforced=True,
        job_memory_limit_mb=512,
        job_memory_limit_enforced=True,
        cleanup_complete=False,
        error_type=None,
        elapsed_ms=1.0,
    )


def _readiness() -> OwnedReadinessObservation:
    return OwnedReadinessObservation(
        ready=True,
        attempts=(
            ReadinessAttempt(
                ordinal=1,
                elapsed_ms=2.0,
                result="SUCCESS",
                http_status=200,
                response_byte_count=2,
                listener_owner_in_job=True,
                job_active_process_count=1,
            ),
        ),
        error_type=None,
        elapsed_ms=2.0,
    )


def _stream(content: bytes = b"") -> CapturedStream:
    return CapturedStream(
        content=content,
        observed_bytes_lower_bound=len(content),
        stream_complete=True,
        overflowed=False,
        thread_stopped=True,
        error_type=None,
    )


def _teardown() -> OwnedServiceTeardownObservation:
    return OwnedServiceTeardownObservation(
        requested=True,
        total_assigned_processes=1,
        final_active_processes=0,
        forced_termination_requested=True,
        root_signaled=True,
        root_exit_code=1,
        termination_reason="JOB_TERMINATED",
        handles_released=True,
        readers_released=True,
        port_free=True,
        stdout=_stream(b"ready\n"),
        stderr=_stream(),
        error_type=None,
        cleanup_complete=True,
        elapsed_ms=3.0,
    )


def _lifecycle() -> BootstrapLifecycleObservation:
    return BootstrapLifecycleObservation(
        expected_start_order=("application",),
        actual_start_order=("application",),
        expected_teardown_order=("application",),
        actual_teardown_order=("application",),
        teardown_attempt_order=("application",),
        events=(
            BootstrapLifecycleEvent(1, "PREPARED", "ENTERED", 0.1),
            BootstrapLifecycleEvent(2, "EVIDENCE_FINALIZED", "COMPLETE", 5.0),
            BootstrapLifecycleEvent(3, "TEARDOWN_APPLICATION", "COMPLETE", 8.0),
            BootstrapLifecycleEvent(4, "TEARDOWN_COMPLETE", "COMPLETE", 10.0),
        ),
        nodes=(
            BootstrapNodeObservation(
                node_id="application",
                role="APPLICATION",
                start=_start(),
                readiness=_readiness(),
                teardown=_teardown(),
            ),
        ),
        services_ready=True,
        ready_callback_started=True,
        ready_callback_completed=True,
        trigger_reason="NONE",
        stop_reason="NONE",
        cleanup_complete=True,
        elapsed_ms=10.0,
    )


def _resource_observation() -> dict:
    return {
        "core_peak_rss_mb": 32.0,
        "dependency_peak_rss_mb": None,
        "application_peak_rss_mb": 25.0,
        "browser_peak_rss_mb": 64.0,
        "host_available_memory_min_mb": 4096.0,
        "available_memory_soft_min_mb": 1,
        "available_memory_hard_min_mb": 1,
        "hard_breach_grace_samples": 1,
        "max_consecutive_memory_hard_breaches": 0,
        "limit_trigger_reason": None,
        "sampling_complete": True,
    }


def _subject_observation() -> dict:
    return {
        "before_fingerprint": "b" * 64,
        "after_fingerprint": "b" * 64,
        "changed": False,
        "scan_complete": True,
    }


@unittest.skipUnless(os.name == "nt", "M11 single-application bootstrap is Windows-only")
class M11SingleApplicationTests(unittest.TestCase):
    def _fixture(
        self, root: Path, *, port: int | None = None, browser_failure: bool = False
    ) -> tuple[Path, dict, dict, Path, dict, int]:
        selected_port = _free_port() if port is None else port
        subject = root / "subject"
        watched = subject / "watched"
        watched.mkdir(parents=True)
        (watched / "state.txt").write_text("stable\n", encoding="utf-8")
        shutil.copy2(
            ROOT / "examples" / "bootstrap" / "gatea_helper.py",
            subject / "service.py",
        )

        raw_profile = single_bootstrap_profile()
        raw_profile["subject_watch_roots"] = ["watched"]
        raw_profile["lifecycle_timeout_ms"] = 15_000
        application = raw_profile["nodes"][0]
        application["port"] = selected_port
        application["arguments"] = [
            {"literal": "service.py"},
            {"literal": "serve"},
            {"node_port": "application"},
        ]
        application["readiness"].update(
            attempt_timeout_ms=250,
            total_timeout_ms=3_000,
            interval_ms=50,
        )
        profile = seal_project_profile(raw_profile)

        raw_plan = single_bootstrap_plan(profile)
        raw_plan["preflight"].update(
            sample_count=1,
            sampling_interval_ms=0,
            hard_breach_grace_samples=1,
            available_memory_soft_min_mb=1,
            available_memory_hard_min_mb=1,
            disk_free_hard_min_mb=1,
            collector_rss_hard_max_mb=2_048,
            observer_rss_delta_soft_max_mb=1_024,
            ports=[{"port": selected_port, "expected": "FREE"}],
        )
        origin = f"http://127.0.0.1:{selected_port}"
        raw_plan["browser"]["start_url"] = f"{origin}/"
        raw_plan["browser"]["allowed_origins"] = [origin]
        if browser_failure:
            raw_plan["browser"]["timeout_ms"] = 1_000
            raw_plan["browser"]["steps"][0]["selector"] = "[data-testid='missing']"
        plan = seal_plan(raw_plan, profile)

        bindings = root / "tool-bindings.json"
        bindings.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "bindings": {
                        "python-application": {
                            "executable": str(Path(sys.executable).resolve())
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        preview = build_bootstrap_preview(
            plan,
            profile,
            subject_root=subject,
            tool_bindings_path=bindings,
        )
        return subject, plan, profile, bindings, preview, selected_port

    def _bootstrap_artifact(self, plan: dict, profile: dict, preview: dict):
        browser = _browser_artifact(plan)
        bootstrap = collect_bootstrap_evidence(
            plan,
            profile,
            preview,
            _lifecycle(),
            browser_exercise={
                "started": True,
                "completed": True,
                "evidence_sha256": browser.sha256,
                "job_memory_limit_mb": 1024,
                "job_memory_limit_enforced": True,
                "process_cleanup_complete": True,
            },
            resource_observation=_resource_observation(),
            subject_observation=_subject_observation(),
            run_work_released=True,
            staging_released=True,
            captured_at="2026-08-14T00:00:00Z",
        )
        return browser, bootstrap

    def test_preview_materialization_and_real_lifecycle_are_one_node(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, port = self._fixture(root)
            self.assertEqual("0.2", preview["schema_version"])
            self.assertEqual("SINGLE_APPLICATION", preview["topology"])
            self.assertEqual(["application"], preview["start_order"])
            self.assertEqual(["application"], preview["teardown_order"])
            self.assertEqual(1, len(preview["nodes"]))

            resolved = resolve_bootstrap(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
            )
            run_work = root / "run-work"
            run_work.mkdir()
            specs = materialize_bootstrap_service_specs(
                profile, resolved, run_work=run_work
            )
            self.assertEqual(1, len(specs))
            result = run_bootstrap_lifecycle(specs, lifecycle_timeout_ms=15_000)
            self.assertTrue(result.services_ready)
            self.assertEqual(("application",), result.actual_start_order)
            self.assertEqual(("application",), result.teardown_attempt_order)
            self.assertEqual(("application",), result.actual_teardown_order)
            self.assertTrue(result.cleanup_complete)
            self.assertTrue(_port_is_free(port))

    def test_collector_v03_has_one_node_two_streams_and_null_dependency_rss(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, plan, profile, _, preview, _ = self._fixture(Path(directory))
            _, result = self._bootstrap_artifact(plan, profile, preview)
            document = result.bootstrap.document
            self.assertEqual("VeriTrail bootstrap-lifecycle/0.3", document["source"])
            self.assertEqual(1, len(document["facts"]["nodes"]))
            self.assertEqual(2, len(result.bootstrap.attachments))
            self.assertIsNone(
                document["facts"]["resource_observation"]["dependency_peak_rss_mb"]
            )
            self.assertEqual(
                {"project_bootstrap_topology": "veritrail_managed_windows_c1_single_application"},
                document["observed_variables"],
            )
            verify_imported_evidence(result.bootstrap)

            old_collector_claim = copy.deepcopy(document)
            old_collector_claim["source"] = "VeriTrail bootstrap-lifecycle/0.2"
            old_collector_claim["observed_variables"] = {
                "project_bootstrap_mode": "veritrail_managed_windows_c1_two_node_services"
            }
            with self.assertRaises(ValidationError):
                validate_evidence(old_collector_claim, "old-cardinality.json")

    def test_plan_v07_bundle_catalog_comparison_and_analysis_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, plan, profile, _, preview, _ = self._fixture(root)
            browser, bootstrap = self._bootstrap_artifact(plan, profile, preview)
            preflight = import_evidence_document(
                collect_preflight_evidence(plan, root), "preflight.json"
            )
            bundles = []
            for name, run_id in (("first", "m11-unit-positive-a"), ("second", "m11-unit-positive-b")):
                output = root / name
                report = create_bundle(
                    plan=plan,
                    project_profile=profile,
                    evidence_paths=[],
                    output=output,
                    run_id=run_id,
                    execution_status=bootstrap.execution_status,
                    generated_evidence=[preflight, browser, bootstrap.bootstrap],
                )
                self.assertEqual("PASS", report["verdict"])
                validated = validate_bundle(output, root)
                self.assertEqual(profile["seal"]["digest"], validated.profile_sha256)
                bundles.append(output)

            comparison = create_comparison_bundle(
                baseline=bundles[0], repeat=bundles[1], output=root / "comparison"
            )
            self.assertEqual("MATCH", comparison.comparison_status)
            with self.assertRaises(PairingError) as pairing:
                load_pairing_source(bundles[0], "project_bootstrap_topology")
            self.assertEqual("SOURCE_PLAN_VERSION_UNSUPPORTED", pairing.exception.code)
            with self.assertRaises(BatchError) as batching:
                load_batch_source(bundles[0], root, "project_bootstrap_topology")
            self.assertEqual("SOURCE_PLAN_VERSION_UNSUPPORTED", batching.exception.code)

    def test_cli_run_routes_plan_v07_and_stages_record_v02(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, port = self._fixture(root)
            plan_path = root / "sealed-plan.json"
            profile_path = root / "sealed-profile.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            output = root / "bundle"
            staged: list[dict] = []
            original_stage = _OwnedBootstrapWorkspace.stage

            def capture_stage(workspace, document, *, writer=None):
                staged.append(copy.deepcopy(document))
                return original_stage(workspace, document, writer=writer)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with patch.object(_OwnedBootstrapWorkspace, "stage", capture_stage), redirect_stdout(
                stdout
            ), redirect_stderr(stderr):
                code = main(
                    [
                        "run",
                        "--plan",
                        str(plan_path),
                        "--profile",
                        str(profile_path),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings),
                        "--approve-bootstrap-preview-sha256",
                        preview["preview_sha256"],
                        "--output",
                        str(output),
                        "--run-id",
                        "m11-cli-single-positive",
                    ]
                )

            self.assertEqual("", stderr.getvalue())
            self.assertEqual(0, code)
            payload = json.loads(stdout.getvalue())
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("PASS", payload["verdict"])
            self.assertEqual("NONE", payload["stop_reason"])
            self.assertEqual(1, len(staged))
            self.assertEqual("0.2", staged[0]["schema_version"])
            self.assertEqual(["application"], staged[0]["start_order"]["sealed"])
            self.assertEqual(["application"], staged[0]["teardown_order"]["sealed"])
            self.assertEqual(1, len(staged[0]["nodes"]))
            validated = validate_bundle(output, root)
            self.assertEqual("PASS", validated.verdict)
            self.assertTrue(_port_is_free(port))
            self.assertEqual([], list(root.glob(".veritrail-bootstrap-*")))


if __name__ == "__main__":
    unittest.main()
