from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from veritrail.batching import BatchError, _load_source as load_batch_source
from veritrail.bootstrap_evidence import collect_bootstrap_evidence
from veritrail.bootstrap_lifecycle import (
    BootstrapLifecycleEvent,
    BootstrapLifecycleObservation,
    BootstrapNodeObservation,
)
from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.catalog import _CandidateRejected, validate_bundle
from veritrail.comparison import create_comparison_bundle
from veritrail.evidence import (
    import_evidence_document,
    validate_evidence,
    verify_imported_evidence,
)
from veritrail.errors import SafetyError, ValidationError
from veritrail.pairing import PairingError, _load_source as load_pairing_source
from veritrail.plan import seal_plan
from veritrail.reporting import create_bundle
from veritrail.resources import collect_preflight_evidence
from veritrail.verdict import evaluate
from veritrail.windows_job import CapturedStream
from veritrail.windows_readiness import OwnedReadinessObservation, ReadinessAttempt
from veritrail.windows_service import (
    OwnedServiceStartObservation,
    OwnedServiceTeardownObservation,
)

from tests.support import bootstrap_plan, sealed_bootstrap_profile, sealed_example_plan
from tests.test_browser_evidence import _browser_artifact


def _authorities() -> tuple[dict, dict, dict]:
    profile = sealed_bootstrap_profile()
    plan = seal_plan(bootstrap_plan(profile), profile)
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
    return plan, profile, preview


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


def _readiness(ready: bool, error_type: str | None = None) -> OwnedReadinessObservation:
    return OwnedReadinessObservation(
        ready=ready,
        attempts=(
            ReadinessAttempt(
                ordinal=1,
                elapsed_ms=2.0,
                result="SUCCESS" if ready else "NODE_EARLY_EXIT",
                http_status=200 if ready else None,
                response_byte_count=2 if ready else None,
                listener_owner_in_job=ready,
                job_active_process_count=1,
            ),
        ),
        error_type=error_type,
        elapsed_ms=2.0,
    )


def _stream(content: bytes) -> CapturedStream:
    return CapturedStream(
        content=content,
        observed_bytes_lower_bound=len(content),
        stream_complete=True,
        overflowed=False,
        thread_stopped=True,
        error_type=None,
    )


def _teardown(content: bytes = b"") -> OwnedServiceTeardownObservation:
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
        stdout=_stream(content),
        stderr=_stream(b""),
        error_type=None,
        cleanup_complete=True,
        elapsed_ms=3.0,
    )


def _lifecycle(*, early_exit: bool) -> BootstrapLifecycleObservation:
    if early_exit:
        nodes = (
            BootstrapNodeObservation(
                node_id="dependency",
                role="DEPENDENCY",
                start=_start(),
                readiness=_readiness(False, "NODE_EARLY_EXIT"),
                teardown=_teardown(),
            ),
            BootstrapNodeObservation(
                node_id="application",
                role="APPLICATION",
                start=None,
                readiness=None,
                teardown=None,
            ),
        )
        actual_start = ("dependency",)
        actual_teardown = ("dependency",)
        stop_reason = "NODE_EARLY_EXIT"
        services_ready = False
    else:
        nodes = (
            BootstrapNodeObservation(
                node_id="dependency",
                role="DEPENDENCY",
                start=_start(),
                readiness=_readiness(True),
                teardown=_teardown(b"C:\\Users\\example\\private\\dependency.log\n"),
            ),
            BootstrapNodeObservation(
                node_id="application",
                role="APPLICATION",
                start=_start(),
                readiness=_readiness(True),
                teardown=_teardown(b"ready\n"),
            ),
        )
        actual_start = ("dependency", "application")
        actual_teardown = ("application", "dependency")
        stop_reason = "NONE"
        services_ready = True
    return BootstrapLifecycleObservation(
        expected_start_order=("dependency", "application"),
        actual_start_order=actual_start,
        expected_teardown_order=("application", "dependency"),
        actual_teardown_order=actual_teardown,
        teardown_attempt_order=actual_teardown,
        events=(
            BootstrapLifecycleEvent(1, "PREPARED", "ENTERED", 0.1),
            BootstrapLifecycleEvent(2, "EVIDENCE_FINALIZED", "COMPLETE", 5.0),
            BootstrapLifecycleEvent(3, "TEARDOWN_COMPLETE", "COMPLETE", 10.0),
        ),
        nodes=nodes,
        services_ready=services_ready,
        ready_callback_started=not early_exit,
        ready_callback_completed=not early_exit,
        trigger_reason=stop_reason,
        stop_reason=stop_reason,
        cleanup_complete=True,
        elapsed_ms=10.0,
    )


def _observations() -> tuple[dict, dict]:
    return (
        {
            "core_peak_rss_mb": 32.0,
            "dependency_peak_rss_mb": 24.0,
            "application_peak_rss_mb": 25.0,
            "browser_peak_rss_mb": None,
            "sampling_complete": True,
        },
        {
            "before_fingerprint": "b" * 64,
            "after_fingerprint": "b" * 64,
            "changed": False,
            "scan_complete": True,
        },
    )


def _preflight(plan: dict, root: Path, decision: str = "PROCEED"):
    document = collect_preflight_evidence(plan, root)
    facts = document["facts"]
    facts["decision"] = decision
    facts["decision_reasons"] = []
    return import_evidence_document(document, f"preflight-{decision.lower()}.json")


def _write_json(path: Path, value: dict, *, newline: bool) -> None:
    content = canonical_json_bytes(value) + (b"\n" if newline else b"")
    path.write_bytes(content)


def _refresh_bundle_entries(bundle: Path, changed: list[str]) -> None:
    manifest_path = bundle / "bundle-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = {item["path"]: item for item in manifest["files"]}
    for relative in changed:
        content = (bundle / Path(*relative.split("/"))).read_bytes()
        entries[relative]["sha256"] = hashlib.sha256(content).hexdigest()
        entries[relative]["size"] = len(content)
    _write_json(manifest_path, manifest, newline=True)


class BootstrapEvidenceTests(unittest.TestCase):
    def test_only_explicit_staging_failure_can_use_failure_evidence_fallback(self) -> None:
        plan, profile, preview = _authorities()
        resource, subject = _observations()
        lifecycle = _lifecycle(early_exit=False)
        lifecycle = replace(
            lifecycle,
            events=(
                BootstrapLifecycleEvent(1, "PREPARED", "ENTERED", 0.1),
                BootstrapLifecycleEvent(2, "EVIDENCE_FINALIZATION", "FAILED", 5.0),
                BootstrapLifecycleEvent(3, "TEARDOWN_COMPLETE", "COMPLETE", 10.0),
            ),
            trigger_reason="EVIDENCE_ERROR",
            stop_reason="EVIDENCE_ERROR",
        )
        with self.assertRaisesRegex(SafetyError, "explicit failed"):
            collect_bootstrap_evidence(
                plan,
                profile,
                preview,
                lifecycle,
                browser_exercise={
                    "started": True,
                    "completed": True,
                    "evidence_sha256": "d" * 64,
                    "job_memory_limit_mb": 1024,
                    "job_memory_limit_enforced": True,
                },
                resource_observation=resource,
                subject_observation=subject,
                run_work_released=True,
                staging_released=True,
            )

    def test_strict_evidence_has_four_redacted_stream_attachments(self) -> None:
        plan, profile, preview = _authorities()
        resource, subject = _observations()
        result = collect_bootstrap_evidence(
            plan,
            profile,
            preview,
            _lifecycle(early_exit=False),
            browser_exercise={
                "started": True,
                "completed": True,
                "evidence_sha256": "a" * 64,
                "job_memory_limit_mb": 1024,
                "job_memory_limit_enforced": True,
            },
            resource_observation=resource,
            subject_observation=subject,
            run_work_released=True,
            staging_released=True,
            captured_at="2026-08-13T00:00:00Z",
        )
        self.assertEqual("COMPLETED", result.execution_status)
        self.assertTrue(result.continue_pipeline)
        self.assertEqual(4, len(result.bootstrap.attachments))
        verify_imported_evidence(result.bootstrap)
        persisted = b"".join(item.content for item in result.bootstrap.attachments)
        self.assertNotIn(b"Users", persisted)
        self.assertNotIn(b"example", persisted)
        self.assertNotIn(b"private", persisted)
        self.assertNotIn("owning_pid", str(result.bootstrap.document))

        mutated = copy.deepcopy(result.bootstrap.document)
        mutated["facts"]["nodes"][0]["stdout"]["attachment"]["path"] = (
            "attachments/bootstrap/dependency/extra.txt"
        )
        with self.assertRaises(ValidationError):
            validate_evidence(mutated, "mutated-bootstrap.json")

    def test_browser_collector_error_cannot_use_business_failure_exception(self) -> None:
        plan, profile, preview = _authorities()
        healthy = _browser_artifact(plan)
        document = copy.deepcopy(healthy.document)
        document["facts"]["capture_complete"] = False
        document["facts"]["all_steps_passed"] = False
        document["facts"]["collection_errors"] = [
            {"collector": "viewport:desktop", "error_type": "ObserverFailure"}
        ]
        browser = import_evidence_document(
            document,
            "browser-collector-error.json",
            attachments=healthy.attachments,
        )
        resource, subject = _observations()
        resource["browser_peak_rss_mb"] = 16.0
        lifecycle = replace(
            _lifecycle(early_exit=False),
            trigger_reason="BROWSER_HARD_FAILURE",
            stop_reason="BROWSER_HARD_FAILURE",
        )
        bootstrap = collect_bootstrap_evidence(
            plan,
            profile,
            preview,
            lifecycle,
            browser_exercise={
                "started": True,
                "completed": True,
                "evidence_sha256": browser.sha256,
                "job_memory_limit_mb": 1024,
                "job_memory_limit_enforced": True,
            },
            resource_observation=resource,
            subject_observation=subject,
            run_work_released=True,
            staging_released=True,
            captured_at="2026-08-13T00:00:00Z",
        )

        result = evaluate(
            plan,
            [browser, bootstrap.bootstrap],
            bootstrap.execution_status,
        )
        self.assertIn(
            "BROWSER_STATUS_CONFLICT",
            {item["code"] for item in result["contamination"]},
        )

    def test_bundle_catalog_and_comparison_enforce_plan_profile_authorities(self) -> None:
        plan, profile, preview = _authorities()
        resource, subject = _observations()
        bootstrap = collect_bootstrap_evidence(
            plan,
            profile,
            preview,
            _lifecycle(early_exit=True),
            browser_exercise={
                "started": False,
                "completed": False,
                "evidence_sha256": None,
                "job_memory_limit_mb": 1024,
                "job_memory_limit_enforced": False,
            },
            resource_observation=resource,
            subject_observation=subject,
            run_work_released=True,
            staging_released=True,
            captured_at="2026-08-13T00:00:00Z",
        )
        self.assertEqual("COMPLETED", bootstrap.execution_status)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            preflight = _preflight(plan, root)
            first = root / "first"
            second = root / "second"
            for output, run_id in ((first, "m10-source-a"), (second, "m10-source-b")):
                create_bundle(
                    plan=plan,
                    project_profile=profile,
                    evidence_paths=[],
                    output=output,
                    run_id=run_id,
                    execution_status=bootstrap.execution_status,
                    generated_evidence=[preflight, bootstrap.bootstrap],
                )
                validated = validate_bundle(output, root)
                self.assertEqual(profile["seal"]["digest"], validated.profile_sha256)
                manifest_paths = {
                    item.path for item in validated.files
                }
                self.assertIn("sealed-plan.json", manifest_paths)
                self.assertIn("sealed-profile.json", manifest_paths)

            comparison = root / "comparison"
            result = create_comparison_bundle(
                baseline=first, repeat=second, output=comparison
            )
            self.assertTrue(result.comparable)
            self.assertEqual("MATCH", result.comparison_status)

            with self.assertRaises(PairingError) as pairing:
                load_pairing_source(first, "project_bootstrap_mode")
            self.assertEqual("SOURCE_PLAN_VERSION_UNSUPPORTED", pairing.exception.code)
            with self.assertRaises(BatchError) as batching:
                load_batch_source(first, root, "project_bootstrap_mode")
            self.assertEqual("SOURCE_PLAN_VERSION_UNSUPPORTED", batching.exception.code)

            missing_profile = root / "missing-profile-copy"
            shutil.copytree(first, missing_profile)
            (missing_profile / "sealed-profile.json").unlink()
            missing_manifest_path = missing_profile / "bundle-manifest.json"
            missing_manifest = json.loads(missing_manifest_path.read_text(encoding="utf-8"))
            missing_manifest["files"] = [
                item
                for item in missing_manifest["files"]
                if item["path"] != "sealed-profile.json"
            ]
            _write_json(missing_manifest_path, missing_manifest, newline=True)
            with self.assertRaises(_CandidateRejected) as missing:
                validate_bundle(missing_profile, root)
            self.assertEqual("MISSING_SEALED_PROFILE", missing.exception.code)

            authority_drift = root / "authority-drift-copy"
            shutil.copytree(first, authority_drift)
            evidence_manifest_path = authority_drift / "evidence-manifest.json"
            evidence_manifest = json.loads(evidence_manifest_path.read_text(encoding="utf-8"))
            bootstrap_entry = next(
                item
                for item in evidence_manifest["artifacts"]
                if item["evidence_type"] == "runtime.bootstrap"
            )
            evidence_path = authority_drift / Path(*bootstrap_entry["path"].split("/"))
            document = json.loads(evidence_path.read_text(encoding="utf-8"))
            document["facts"]["profile"]["sha256"] = "c" * 64
            _write_json(evidence_path, document, newline=False)
            evidence_content = evidence_path.read_bytes()
            bootstrap_entry["sha256"] = hashlib.sha256(evidence_content).hexdigest()
            bootstrap_entry["size"] = len(evidence_content)
            _write_json(evidence_manifest_path, evidence_manifest, newline=True)
            report_path = authority_drift / "report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["evidence"] = copy.deepcopy(evidence_manifest["artifacts"])
            _write_json(report_path, report, newline=True)
            _refresh_bundle_entries(
                authority_drift,
                [bootstrap_entry["path"], "evidence-manifest.json", "report.json"],
            )
            with self.assertRaises(_CandidateRejected) as drift:
                validate_bundle(authority_drift, root)
            self.assertEqual("BOOTSTRAP_AUTHORITY_MISMATCH", drift.exception.code)

            report_drift = root / "report-drift-copy"
            shutil.copytree(first, report_drift)
            report_path = report_drift / "report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["verdict"] = "PASS" if report["verdict"] != "PASS" else "FAIL"
            _write_json(report_path, report, newline=True)
            _refresh_bundle_entries(report_drift, ["report.json"])
            with self.assertRaises(_CandidateRejected) as report_rejected:
                validate_bundle(report_drift, root)
            self.assertEqual(
                "BOOTSTRAP_REPORT_DERIVATION_MISMATCH",
                report_rejected.exception.code,
            )

            status_drift = root / "status-drift-copy"
            shutil.copytree(first, status_drift)
            report_path = status_drift / "report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["execution_status"] = "ERROR"
            _write_json(report_path, report, newline=True)
            _refresh_bundle_entries(status_drift, ["report.json"])
            with self.assertRaises(_CandidateRejected) as status_rejected:
                validate_bundle(status_drift, root)
            self.assertEqual(
                "BOOTSTRAP_STATUS_CONFLICT", status_rejected.exception.code
            )

            stopped_with_bootstrap = root / "stopped-with-bootstrap-copy"
            shutil.copytree(first, stopped_with_bootstrap)
            evidence_manifest_path = stopped_with_bootstrap / "evidence-manifest.json"
            evidence_manifest = json.loads(evidence_manifest_path.read_text(encoding="utf-8"))
            preflight_entry = next(
                item
                for item in evidence_manifest["artifacts"]
                if item["evidence_type"] == "runtime.preflight"
            )
            preflight_path = stopped_with_bootstrap / Path(*preflight_entry["path"].split("/"))
            preflight_document = json.loads(preflight_path.read_text(encoding="utf-8"))
            preflight_document["facts"]["decision"] = "STOP_ESCALATION"
            preflight_document["facts"]["decision_reasons"] = []
            _write_json(preflight_path, preflight_document, newline=False)
            preflight_content = preflight_path.read_bytes()
            preflight_entry["sha256"] = hashlib.sha256(preflight_content).hexdigest()
            preflight_entry["size"] = len(preflight_content)
            _write_json(evidence_manifest_path, evidence_manifest, newline=True)
            report_path = stopped_with_bootstrap / "report.json"
            stopped_report = json.loads(report_path.read_text(encoding="utf-8"))
            stopped_report["execution_status"] = "ABORTED"
            stopped_report["verdict"] = "PENDING"
            stopped_report["evidence"] = copy.deepcopy(evidence_manifest["artifacts"])
            _write_json(report_path, stopped_report, newline=True)
            _refresh_bundle_entries(
                stopped_with_bootstrap,
                [preflight_entry["path"], "evidence-manifest.json", "report.json"],
            )
            with self.assertRaises(_CandidateRejected) as stopped_extra:
                validate_bundle(stopped_with_bootstrap, root)
            self.assertEqual(
                "BOOTSTRAP_EVIDENCE_CARDINALITY", stopped_extra.exception.code
            )

    def test_preflight_stopped_bundle_applies_only_preflight_evidence(self) -> None:
        plan, profile, preview = _authorities()
        resource, subject = _observations()
        bootstrap = collect_bootstrap_evidence(
            plan,
            profile,
            preview,
            _lifecycle(early_exit=True),
            browser_exercise={
                "started": False,
                "completed": False,
                "evidence_sha256": None,
                "job_memory_limit_mb": 1024,
                "job_memory_limit_enforced": False,
            },
            resource_observation=resource,
            subject_observation=subject,
            run_work_released=True,
            staging_released=True,
            captured_at="2026-08-13T00:00:00Z",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stopped = _preflight(plan, root, "STOP_ESCALATION")
            output = root / "stopped"
            report = create_bundle(
                plan=plan,
                project_profile=profile,
                evidence_paths=[],
                output=output,
                run_id="m10-stopped",
                execution_status="ABORTED",
                generated_evidence=[stopped],
            )
            self.assertEqual("PENDING", report["verdict"])
            self.assertEqual([], report["contamination"])
            self.assertEqual(
                ["browser.session", "runtime.bootstrap"], report["missing_evidence"]
            )
            contaminated = evaluate(
                plan,
                [stopped, bootstrap.bootstrap, _browser_artifact(plan)],
                "ABORTED",
            )
            self.assertNotEqual("PASS", contaminated["verdict"])
            self.assertTrue(
                {"PREFLIGHT_BOOTSTRAP_CONFLICT", "PREFLIGHT_BROWSER_CONFLICT"}
                <= {item["code"] for item in contaminated["contamination"]}
            )
            validated = validate_bundle(output, root)
            self.assertEqual("ABORTED", validated.execution_status)
            self.assertEqual("PENDING", validated.verdict)

            with self.assertRaisesRegex(ValidationError, "must use execution_status ABORTED"):
                create_bundle(
                    plan=plan,
                    project_profile=profile,
                    evidence_paths=[],
                    output=root / "wrong-status",
                    run_id="m10-wrong-status",
                    execution_status="COMPLETED",
                    generated_evidence=[stopped],
                )
            with self.assertRaisesRegex(ValidationError, "must not contain runtime.bootstrap"):
                create_bundle(
                    plan=plan,
                    project_profile=profile,
                    evidence_paths=[],
                    output=root / "extra-bootstrap",
                    run_id="m10-extra-bootstrap",
                    execution_status="ABORTED",
                    generated_evidence=[stopped, bootstrap.bootstrap],
                )
            with self.assertRaisesRegex(ValidationError, "must not contain browser.session"):
                create_bundle(
                    plan=plan,
                    project_profile=profile,
                    evidence_paths=[],
                    output=root / "extra-browser",
                    run_id="m10-extra-browser",
                    execution_status="ABORTED",
                    generated_evidence=[stopped, _browser_artifact(plan)],
                )

            tampered = root / "tampered"
            shutil.copytree(output, tampered)
            report_path = tampered / "report.json"
            tampered_report = json.loads(report_path.read_text(encoding="utf-8"))
            tampered_report["verdict"] = "PASS"
            _write_json(report_path, tampered_report, newline=True)
            _refresh_bundle_entries(tampered, ["report.json"])
            with self.assertRaises(_CandidateRejected) as rejected:
                validate_bundle(tampered, root)
            self.assertEqual(
                "PREFLIGHT_REPORT_DERIVATION_MISMATCH", rejected.exception.code
            )

            status_tampered = root / "status-tampered"
            shutil.copytree(output, status_tampered)
            status_report_path = status_tampered / "report.json"
            status_report = json.loads(status_report_path.read_text(encoding="utf-8"))
            status_report["execution_status"] = "COMPLETED"
            _write_json(status_report_path, status_report, newline=True)
            _refresh_bundle_entries(status_tampered, ["report.json"])
            with self.assertRaises(_CandidateRejected) as status_rejected:
                validate_bundle(status_tampered, root)
            self.assertEqual("PREFLIGHT_STATUS_CONFLICT", status_rejected.exception.code)

            failed_preflight_document = copy.deepcopy(stopped.document)
            failed_preflight_document["facts"]["decision"] = "ABORT"
            failed_preflight_document["facts"]["snapshot_complete"] = False
            failed_preflight_document["facts"]["collection_errors"] = [
                {"collector": "resource_sample", "error_type": "OSError"}
            ]
            failed_preflight = import_evidence_document(
                failed_preflight_document, "failed-preflight.json"
            )
            failed_output = root / "failed-preflight"
            failed_report = create_bundle(
                plan=plan,
                project_profile=profile,
                evidence_paths=[],
                output=failed_output,
                run_id="m10-failed-preflight",
                execution_status="ABORTED",
                generated_evidence=[failed_preflight],
            )
            self.assertEqual("FAIL", failed_report["verdict"])
            failed_validated = validate_bundle(failed_output, root)
            self.assertEqual("FAIL", failed_validated.verdict)

    def test_plan_06_bundle_requires_profile_and_legacy_bundle_rejects_one(self) -> None:
        plan, profile, _ = _authorities()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValidationError, "requires a sealed ProjectProfile"):
                create_bundle(
                    plan=plan,
                    evidence_paths=[],
                    output=root / "missing-profile",
                    run_id="missing-profile",
                    execution_status="ERROR",
                )
            with self.assertRaisesRegex(ValidationError, "accepted only"):
                create_bundle(
                    plan=sealed_example_plan(),
                    project_profile=profile,
                    evidence_paths=[],
                    output=root / "unexpected-profile",
                    run_id="unexpected-profile",
                    execution_status="ERROR",
                )


if __name__ == "__main__":
    unittest.main()
