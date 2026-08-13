from __future__ import annotations

import io
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from pathlib import Path

from veritrail.bootstrap_preview import build_bootstrap_preview, resolve_bootstrap
from veritrail.bootstrap_public_run import run_bootstrap_bundle
from veritrail.bootstrap_run import run_observed_bootstrap
from veritrail.catalog import validate_bundle
from veritrail.cli import _bootstrap_interrupt_cancellation, main
from veritrail.comparison import create_comparison_bundle
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile
from veritrail.windows_readiness import probe_owned_http_readiness
from veritrail.windows_service import OwnedServiceSession

from tests.support import bootstrap_plan, bootstrap_profile

ROOT = Path(__file__).resolve().parents[1]


def _free_port(excluded: set[int] | None = None) -> int:
    excluded = set() if excluded is None else excluded
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
            candidate.bind(("127.0.0.1", 0))
            port = int(candidate.getsockname()[1])
        if port not in excluded:
            return port


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(0.2)
        return client.connect_ex(("127.0.0.1", port)) != 0


@unittest.skipUnless(os.name == "nt", "M10 public bootstrap Run is Windows-only")
class BootstrapRunCliTests(unittest.TestCase):
    def _fixture(
        self,
        root: Path,
        *,
        browser_failure: bool = False,
        bootstrap_failure: str | None = None,
    ) -> tuple[Path, Path, Path, Path, dict, list[int]]:
        if bootstrap_failure not in {
            None,
            "dependency-early-exit",
            "application-timeout",
            "dependency-owner-mismatch",
            "application-owner-mismatch",
        }:
            raise ValueError("unsupported bootstrap failure fixture")
        subject = root / "subject"
        watched = subject / "watched"
        watched.mkdir(parents=True)
        (watched / "state.txt").write_text("stable\n", encoding="utf-8")
        shutil.copy2(
            ROOT / "tests" / "fixtures" / "m10_service_helper.py",
            subject / "service.py",
        )

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
        if bootstrap_failure == "dependency-early-exit":
            dependency["arguments"] = [
                {"literal": "service.py"},
                {"literal": "early-exit"},
                {"literal": "17"},
            ]
        elif bootstrap_failure == "dependency-owner-mismatch":
            dependency["arguments"] = [
                {"literal": "service.py"},
                {"literal": "sleep"},
                {"literal": "30"},
            ]
        application = nodes["application"]
        application["port"] = application_port
        application["arguments"] = [
            {"literal": "service.py"},
            {"literal": "browser-application"},
            {"node_port": "application"},
            {"node_origin": "dependency"},
        ]
        if bootstrap_failure == "application-timeout":
            application["arguments"] = [
                {"literal": "service.py"},
                {"literal": "sleep"},
                {"literal": "30"},
            ]
        elif bootstrap_failure == "application-owner-mismatch":
            application["arguments"] = [
                {"literal": "service.py"},
                {"literal": "sleep"},
                {"literal": "30"},
            ]
        for node in nodes.values():
            node["readiness"]["interval_ms"] = 50
            node["readiness"]["total_timeout_ms"] = 3_000
        if bootstrap_failure == "application-timeout":
            application["readiness"]["attempt_timeout_ms"] = 100
            application["readiness"]["total_timeout_ms"] = 500
        profile = seal_project_profile(raw_profile)

        raw_plan = bootstrap_plan(profile)
        raw_plan["preflight"].update(
            {
                "sample_count": 1,
                "sampling_interval_ms": 0,
                "hard_breach_grace_samples": 1,
                "available_memory_soft_min_mb": 1,
                "available_memory_hard_min_mb": 1,
                "disk_free_hard_min_mb": 1,
                "collector_rss_hard_max_mb": 2_048,
                "observer_rss_delta_soft_max_mb": 1_024,
                "ports": [
                    {"port": dependency_port, "expected": "FREE"},
                    {"port": application_port, "expected": "FREE"},
                ],
            }
        )
        application_origin = f"http://127.0.0.1:{application_port}"
        raw_plan["browser"]["start_url"] = f"{application_origin}/"
        raw_plan["browser"]["allowed_origins"] = [application_origin]
        for step in raw_plan["browser"]["steps"]:
            if step["action"] == "goto":
                step["url"] = f"{application_origin}/"
        if browser_failure:
            raw_plan["browser"]["timeout_ms"] = 1_000
            raw_plan["browser"]["steps"][0]["selector"] = (
                "[data-testid='missing']"
            )
        plan = seal_plan(raw_plan, profile)

        plan_path = root / "sealed-plan.json"
        profile_path = root / "sealed-profile.json"
        bindings_path = root / "tool-bindings.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        profile_path.write_text(json.dumps(profile), encoding="utf-8")
        bindings_path.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "bindings": {
                        "python-dependency": {
                            "executable": str(Path(sys.executable).resolve())
                        },
                        "python-application": {
                            "executable": str(Path(sys.executable).resolve())
                        },
                    },
                }
            ),
            encoding="utf-8",
        )
        preview = build_bootstrap_preview(
            plan,
            profile,
            subject_root=subject,
            tool_bindings_path=bindings_path,
        )
        return (
            subject,
            plan_path,
            profile_path,
            bindings_path,
            preview,
            [dependency_port, application_port],
        )

    def _run(
        self,
        *,
        subject: Path,
        plan: Path,
        profile: Path,
        bindings: Path,
        approval: str,
        output: Path,
        run_id: str,
    ) -> tuple[int, dict, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(
                [
                    "run",
                    "--plan",
                    str(plan),
                    "--profile",
                    str(profile),
                    "--subject-root",
                    str(subject),
                    "--tool-bindings",
                    str(bindings),
                    "--approve-bootstrap-preview-sha256",
                    approval,
                    "--output",
                    str(output),
                    "--run-id",
                    run_id,
                ]
            )
        payload = json.loads(stdout.getvalue()) if stdout.getvalue() else {}
        return code, payload, stderr.getvalue()

    def _evidence_document(self, output: Path, evidence_type: str) -> dict:
        manifest = json.loads(
            (output / "evidence-manifest.json").read_text(encoding="utf-8")
        )
        entry = next(
            item
            for item in manifest["artifacts"]
            if item["evidence_type"] == evidence_type
        )
        return json.loads(
            (output / Path(*entry["path"].split("/"))).read_text(encoding="utf-8")
        )

    def test_approved_run_creates_valid_pass_bundle_and_releases_resources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(root)
            output = root / "bundle-pass"

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan,
                profile=profile,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=output,
                run_id="m10-public-pass",
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("PROCEED", payload["resource_decision"])
            self.assertTrue(payload["bootstrap_started"])
            self.assertTrue(payload["services_ready"])
            self.assertTrue(payload["browser_completed"], payload)
            self.assertTrue(payload["browser_capture_complete"], payload)
            self.assertTrue(payload["cleanup_complete"])
            self.assertEqual("NONE", payload["stop_reason"])
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("PASS", payload["verdict"])

            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            evidence_types = {
                item["evidence_type"] for item in report["evidence"]
            }
            self.assertEqual(
                {"runtime.preflight", "runtime.bootstrap", "browser.session"},
                evidence_types,
            )
            self.assertTrue((output / "sealed-profile.json").is_file())
            self.assertEqual(6, len(list((output / "attachments").rglob("*.*"))))
            validated = validate_bundle(output, root)
            self.assertEqual("m10-public-pass", validated.run_id)
            self.assertEqual("PASS", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_same_sealed_authorities_repeat_without_residual_contamination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(root)
            outputs = (root / "bundle-repeat-one", root / "bundle-repeat-two")
            first_manifest: bytes | None = None

            for ordinal, output in enumerate(outputs, start=1):
                code, payload, stderr = self._run(
                    subject=subject,
                    plan=plan,
                    profile=profile,
                    bindings=bindings,
                    approval=preview["preview_sha256"],
                    output=output,
                    run_id=f"m10-public-repeat-{ordinal}",
                )
                self.assertEqual("", stderr)
                self.assertEqual(0, code)
                self.assertEqual("PROCEED", payload["resource_decision"])
                self.assertEqual("COMPLETED", payload["execution_status"])
                self.assertEqual("PASS", payload["verdict"])
                self.assertTrue(payload["cleanup_complete"])
                validated = validate_bundle(output, root)
                self.assertEqual(f"m10-public-repeat-{ordinal}", validated.run_id)
                self.assertEqual("PASS", validated.verdict)
                self.assertEqual([], list(root.glob(".veritrail-*")))
                self.assertTrue(all(_port_is_free(port) for port in ports))
                if ordinal == 1:
                    first_manifest = (output / "bundle-manifest.json").read_bytes()
                else:
                    self.assertEqual(
                        first_manifest,
                        (outputs[0] / "bundle-manifest.json").read_bytes(),
                    )

            first_report = json.loads(
                (outputs[0] / "report.json").read_text(encoding="utf-8")
            )
            second_report = json.loads(
                (outputs[1] / "report.json").read_text(encoding="utf-8")
            )
            self.assertEqual(first_report["plan"], second_report["plan"])
            self.assertEqual(
                (outputs[0] / "sealed-profile.json").read_bytes(),
                (outputs[1] / "sealed-profile.json").read_bytes(),
            )
            first_bootstrap = self._evidence_document(
                outputs[0], "runtime.bootstrap"
            )["facts"]
            second_bootstrap = self._evidence_document(
                outputs[1], "runtime.bootstrap"
            )["facts"]
            self.assertEqual(
                first_bootstrap["preview_sha256"],
                second_bootstrap["preview_sha256"],
            )

            comparison = create_comparison_bundle(
                baseline=outputs[0],
                repeat=outputs[1],
                output=root / "repeat-comparison",
            )
            self.assertTrue(comparison.comparable)
            self.assertEqual("MATCH", comparison.comparison_status)
            self.assertEqual(0, comparison.difference_count)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_browser_business_failure_is_completed_fail_not_contamination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(
                root, browser_failure=True
            )
            output = root / "bundle-fail"

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan,
                profile=profile,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=output,
                run_id="m10-public-fail",
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("BROWSER_HARD_FAILURE", payload["stop_reason"])
            self.assertFalse(payload["browser_capture_complete"])
            self.assertTrue(payload["cleanup_complete"])
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("FAIL", payload["verdict"])
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertNotIn(
                "BROWSER_STATUS_CONFLICT",
                {item["code"] for item in report["contamination"]},
            )
            validated = validate_bundle(output, root)
            self.assertEqual("FAIL", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_dependency_early_exit_creates_completed_fail_bundle_without_browser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(
                root, bootstrap_failure="dependency-early-exit"
            )
            output = root / "bundle-dependency-early-exit"

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan,
                profile=profile,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=output,
                run_id="m10-dependency-early-exit",
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("PROCEED", payload["resource_decision"])
            self.assertTrue(payload["bootstrap_started"])
            self.assertFalse(payload["services_ready"])
            self.assertFalse(payload["browser_started"])
            self.assertFalse(payload["browser_completed"])
            self.assertIsNone(payload["browser_capture_complete"])
            self.assertTrue(payload["cleanup_complete"])
            self.assertEqual("NODE_EARLY_EXIT", payload["stop_reason"])
            self.assertEqual("COMPLETED", payload["execution_status"])
            self.assertEqual("FAIL", payload["verdict"])

            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(
                {"runtime.preflight", "runtime.bootstrap"},
                {item["evidence_type"] for item in report["evidence"]},
            )
            self.assertEqual(["browser.session"], report["missing_evidence"])
            self.assertEqual([], report["contamination"])
            self.assertEqual(
                "FAIL",
                next(
                    item
                    for item in report["assertions"]
                    if item["id"] == "bootstrap-services-ready"
                )["status"],
            )
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual(["dependency"], bootstrap["start_order"]["actual"])
            self.assertEqual(["dependency"], bootstrap["teardown_order"]["attempted"])
            self.assertEqual(["dependency"], bootstrap["teardown_order"]["completed"])
            self.assertFalse(bootstrap["browser_exercise"]["started"])
            self.assertFalse(bootstrap["browser_exercise"]["completed"])
            self.assertTrue(bootstrap["cleanup_complete"])
            self.assertEqual(4, len(list((output / "attachments").rglob("*.*"))))
            validated = validate_bundle(output, root)
            self.assertEqual("COMPLETED", validated.execution_status)
            self.assertEqual("FAIL", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_application_readiness_timeout_creates_aborted_fail_bundle_without_browser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(
                root, bootstrap_failure="application-timeout"
            )
            output = root / "bundle-application-timeout"

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan,
                profile=profile,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=output,
                run_id="m10-application-timeout",
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("PROCEED", payload["resource_decision"])
            self.assertTrue(payload["bootstrap_started"])
            self.assertFalse(payload["services_ready"])
            self.assertFalse(payload["browser_started"])
            self.assertFalse(payload["browser_completed"])
            self.assertIsNone(payload["browser_capture_complete"])
            self.assertTrue(payload["cleanup_complete"])
            self.assertEqual("READINESS_TIMEOUT", payload["stop_reason"])
            self.assertEqual("ABORTED", payload["execution_status"])
            self.assertEqual("FAIL", payload["verdict"])

            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(
                {"runtime.preflight", "runtime.bootstrap"},
                {item["evidence_type"] for item in report["evidence"]},
            )
            self.assertEqual(["browser.session"], report["missing_evidence"])
            self.assertEqual([], report["contamination"])
            self.assertEqual(
                "FAIL",
                next(
                    item
                    for item in report["assertions"]
                    if item["id"] == "bootstrap-services-ready"
                )["status"],
            )
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual(
                ["dependency", "application"], bootstrap["start_order"]["actual"]
            )
            self.assertEqual(
                ["application", "dependency"],
                bootstrap["teardown_order"]["attempted"],
            )
            self.assertEqual(
                ["application", "dependency"],
                bootstrap["teardown_order"]["completed"],
            )
            self.assertFalse(bootstrap["browser_exercise"]["started"])
            self.assertFalse(bootstrap["browser_exercise"]["completed"])
            self.assertTrue(bootstrap["cleanup_complete"])
            self.assertEqual(4, len(list((output / "attachments").rglob("*.*"))))
            validated = validate_bundle(output, root)
            self.assertEqual("ABORTED", validated.execution_status)
            self.assertEqual("FAIL", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_user_cancel_after_services_ready_creates_aborted_pending_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, preview, ports = self._fixture(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            output = root / "bundle-user-cancelled"
            cancellation = threading.Event()

            def cancel_after_application_ready(session, readiness, **kwargs):
                observation = probe_owned_http_readiness(
                    session,
                    readiness,
                    **kwargs,
                )
                if session.node_id == "application" and observation.ready:
                    cancellation.set()
                return observation

            def observed_runner(
                observed_plan,
                observed_profile,
                resolved,
                *,
                output_parent,
                cancel_event,
            ):
                self.assertIs(cancellation, cancel_event)
                return run_observed_bootstrap(
                    observed_plan,
                    observed_profile,
                    resolved,
                    output_parent=output_parent,
                    cancel_event=cancel_event,
                    readiness_probe=cancel_after_application_ready,
                )

            result = run_bootstrap_bundle(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
                approved_preview_sha256=preview["preview_sha256"],
                output=output,
                run_id="m10-user-cancelled",
                cancel_event=cancellation,
                observed_runner=observed_runner,
            )

            self.assertIsNotNone(result.observed)
            lifecycle = result.observed.lifecycle
            self.assertTrue(lifecycle.services_ready)
            self.assertFalse(lifecycle.ready_callback_started)
            self.assertFalse(lifecycle.ready_callback_completed)
            self.assertEqual("USER_CANCELLED", lifecycle.stop_reason)
            self.assertEqual(
                ("application", "dependency"), lifecycle.actual_teardown_order
            )
            self.assertTrue(lifecycle.cleanup_complete)
            self.assertEqual("ABORTED", result.report["execution_status"])
            self.assertEqual("PENDING", result.report["verdict"])
            self.assertEqual([], result.report["contamination"])
            self.assertEqual(["browser.session"], result.report["missing_evidence"])
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertTrue(bootstrap["services_ready"])
            self.assertFalse(bootstrap["browser_exercise"]["started"])
            self.assertFalse(bootstrap["browser_exercise"]["completed"])
            self.assertEqual("USER_CANCELLED", bootstrap["stop"]["reason"])
            self.assertEqual(
                ["application", "dependency"],
                bootstrap["teardown_order"]["completed"],
            )
            self.assertEqual(4, len(list((output / "attachments").rglob("*.*"))))
            validated = validate_bundle(output, root)
            self.assertEqual("ABORTED", validated.execution_status)
            self.assertEqual("PENDING", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_subject_drift_is_preserved_and_makes_public_verdict_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, preview, ports = self._fixture(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            output = root / "bundle-subject-drift"

            def drift_after_application_ready(session, readiness, **kwargs):
                observation = probe_owned_http_readiness(
                    session,
                    readiness,
                    **kwargs,
                )
                if session.node_id == "application" and observation.ready:
                    (subject / "watched" / "state.txt").write_text(
                        "changed\n", encoding="utf-8"
                    )
                return observation

            def observed_runner(
                observed_plan,
                observed_profile,
                resolved,
                *,
                output_parent,
                cancel_event,
            ):
                return run_observed_bootstrap(
                    observed_plan,
                    observed_profile,
                    resolved,
                    output_parent=output_parent,
                    cancel_event=cancel_event,
                    readiness_probe=drift_after_application_ready,
                )

            result = run_bootstrap_bundle(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
                approved_preview_sha256=preview["preview_sha256"],
                output=output,
                run_id="m10-subject-drift",
                observed_runner=observed_runner,
            )

            self.assertIsNotNone(result.observed)
            self.assertTrue(result.observed.subject_observation["changed"])
            self.assertTrue(result.observed.lifecycle.cleanup_complete)
            self.assertEqual("COMPLETED", result.report["execution_status"])
            self.assertEqual("INCONCLUSIVE", result.report["verdict"])
            self.assertEqual(
                {"BOOTSTRAP_SUBJECT_DRIFT"},
                {item["code"] for item in result.report["contamination"]},
            )
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual("SUBJECT_DRIFT", bootstrap["stop"]["reason"])
            self.assertTrue(bootstrap["subject_observation"]["changed"])
            self.assertNotEqual(
                bootstrap["subject_observation"]["before_fingerprint"],
                bootstrap["subject_observation"]["after_fingerprint"],
            )
            self.assertTrue(bootstrap["browser_exercise"]["completed"])
            self.assertTrue(bootstrap["cleanup_complete"])
            self.assertEqual(
                "changed\n",
                (subject / "watched" / "state.txt").read_text(encoding="utf-8"),
            )
            validated = validate_bundle(output, root)
            self.assertEqual("COMPLETED", validated.execution_status)
            self.assertEqual("INCONCLUSIVE", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_port_conflict_after_live_preview_aborts_without_touching_external_owner(self) -> None:
        for contested_index, label in enumerate(("dependency", "application")):
            with self.subTest(node=label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                subject, plan_path, profile_path, bindings, preview, ports = self._fixture(
                    root
                )
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                output = root / f"bundle-{label}-port-conflict"
                external: socket.socket | None = None

                def resolve_then_contest(*args, **kwargs):
                    nonlocal external
                    resolved = resolve_bootstrap(*args, **kwargs)
                    external = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    external.bind(("127.0.0.1", ports[contested_index]))
                    external.listen(socket.SOMAXCONN)
                    return resolved

                def fail_if_called(*_args, **_kwargs):
                    self.fail("port-conflicted preflight invoked the observed runner")

                try:
                    result = run_bootstrap_bundle(
                        plan,
                        profile,
                        subject_root=subject,
                        tool_bindings_path=bindings,
                        approved_preview_sha256=preview["preview_sha256"],
                        output=output,
                        run_id=f"m10-{label}-port-conflict",
                        resolver=resolve_then_contest,
                        observed_runner=fail_if_called,
                    )

                    self.assertIsNone(result.observed)
                    self.assertEqual(
                        "ABORT", result.preflight.document["facts"]["decision"]
                    )
                    conflict = next(
                        item
                        for item in result.preflight.document["facts"]["port_checks"]
                        if item["port"] == ports[contested_index]
                    )
                    self.assertEqual("FREE", conflict["expected"])
                    self.assertEqual("LISTENING", conflict["actual"])
                    self.assertFalse(conflict["matched"])
                    self.assertEqual("ABORTED", result.report["execution_status"])
                    self.assertEqual("PENDING", result.report["verdict"])
                    self.assertEqual([], result.report["contamination"])
                    self.assertEqual(
                        ["runtime.preflight"],
                        [
                            item["evidence_type"]
                            for item in result.report["evidence"]
                        ],
                    )
                    self.assertFalse((output / "attachments").exists())
                    self.assertEqual(
                        1,
                        external.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN),
                    )
                    self.assertFalse(_port_is_free(ports[contested_index]))
                    validated = validate_bundle(output, root)
                    self.assertEqual("ABORTED", validated.execution_status)
                    self.assertEqual("PENDING", validated.verdict)
                    self.assertEqual([], list(root.glob(".veritrail-*")))
                finally:
                    if external is not None:
                        external.close()
                self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_listener_owner_mismatch_aborts_without_killing_external_listener(self) -> None:
        cases = (
            (0, "dependency", "dependency-owner-mismatch"),
            (1, "application", "application-owner-mismatch"),
        )
        for contested_index, label, failure in cases:
            with self.subTest(node=label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                subject, plan_path, profile_path, bindings, preview, ports = self._fixture(
                    root,
                    bootstrap_failure=failure,
                )
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                output = root / f"bundle-{label}-owner-mismatch"
                external: subprocess.Popen[bytes] | None = None

                def observed_runner(
                    observed_plan,
                    observed_profile,
                    resolved,
                    *,
                    output_parent,
                    cancel_event,
                ):
                    nonlocal external
                    external = subprocess.Popen(
                        [
                            sys.executable,
                            "service.py",
                            "serve-for",
                            str(ports[contested_index]),
                            "1.5",
                        ],
                        cwd=subject,
                        env={
                            key: value
                            for key, value in os.environ.items()
                            if key in {"SYSTEMROOT", "WINDIR"}
                        },
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    for _ in range(60):
                        if not _port_is_free(ports[contested_index]):
                            break
                        if external.poll() is not None:
                            self.fail("external listener exited before ownership probing")
                        threading.Event().wait(0.05)
                    else:
                        self.fail("external listener did not become ready")
                    return run_observed_bootstrap(
                        observed_plan,
                        observed_profile,
                        resolved,
                        output_parent=output_parent,
                        cancel_event=cancel_event,
                    )

                try:
                    result = run_bootstrap_bundle(
                        plan,
                        profile,
                        subject_root=subject,
                        tool_bindings_path=bindings,
                        approved_preview_sha256=preview["preview_sha256"],
                        output=output,
                        run_id=f"m10-{label}-owner-mismatch",
                        observed_runner=observed_runner,
                    )

                    self.assertIsNotNone(result.observed)
                    lifecycle = result.observed.lifecycle
                    self.assertFalse(lifecycle.services_ready)
                    self.assertEqual(
                        "LISTENER_OWNERSHIP_MISMATCH", lifecycle.trigger_reason
                    )
                    self.assertEqual(
                        "LISTENER_OWNERSHIP_MISMATCH", lifecycle.stop_reason
                    )
                    expected_started = (
                        ("dependency",)
                        if label == "dependency"
                        else ("dependency", "application")
                    )
                    self.assertEqual(expected_started, lifecycle.actual_start_order)
                    self.assertEqual(
                        tuple(reversed(expected_started)),
                        lifecycle.actual_teardown_order,
                    )
                    self.assertTrue(lifecycle.cleanup_complete)
                    contested = lifecycle.nodes[contested_index]
                    self.assertIsNotNone(contested.readiness)
                    self.assertFalse(contested.readiness.ready)
                    self.assertEqual(
                        "LISTENER_OWNERSHIP_MISMATCH",
                        contested.readiness.error_type,
                    )
                    self.assertTrue(
                        any(
                            attempt.listener_owner_in_job is False
                            for attempt in contested.readiness.attempts
                        )
                    )
                    self.assertEqual(0, external.wait(timeout=3))
                    self.assertEqual("ABORTED", result.report["execution_status"])
                    self.assertEqual("FAIL", result.report["verdict"])
                    self.assertEqual([], result.report["contamination"])
                    self.assertEqual(["browser.session"], result.report["missing_evidence"])
                    bootstrap = self._evidence_document(
                        output, "runtime.bootstrap"
                    )["facts"]
                    self.assertEqual(
                        "LISTENER_OWNERSHIP_MISMATCH", bootstrap["stop"]["reason"]
                    )
                    self.assertFalse(bootstrap["browser_exercise"]["started"])
                    self.assertTrue(bootstrap["cleanup_complete"])
                    self.assertEqual(4, len(list((output / "attachments").rglob("*.*"))))
                    validated = validate_bundle(output, root)
                    self.assertEqual("ABORTED", validated.execution_status)
                    self.assertEqual("FAIL", validated.verdict)
                    self.assertEqual([], list(root.glob(".veritrail-*")))
                finally:
                    if external is not None and external.poll() is None:
                        external.terminate()
                        external.wait(timeout=5)
                self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_cleanup_failure_is_public_and_does_not_skip_remaining_teardown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, preview, ports = self._fixture(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            output = root / "bundle-cleanup-failure"
            actual_termination_order: list[str] = []

            class CleanupFailureProxy:
                def __init__(self, session: OwnedServiceSession) -> None:
                    self._session = session
                    self.node_id = session.node_id
                    self.start_observation = session.start_observation

                def __getattr__(self, name: str):
                    return getattr(self._session, name)

                def terminate(self):
                    actual_termination_order.append(self.node_id)
                    observation = self._session.terminate()
                    if self.node_id != "application":
                        return observation
                    return replace(
                        observation,
                        handles_released=False,
                        error_type="HANDLE_RELEASE_FAILED",
                        cleanup_complete=False,
                    )

            def injected_session_factory(**kwargs):
                return CleanupFailureProxy(OwnedServiceSession.start(**kwargs))

            def observed_runner(
                observed_plan,
                observed_profile,
                resolved,
                *,
                output_parent,
                cancel_event,
            ):
                return run_observed_bootstrap(
                    observed_plan,
                    observed_profile,
                    resolved,
                    output_parent=output_parent,
                    cancel_event=cancel_event,
                    session_factory=injected_session_factory,
                )

            result = run_bootstrap_bundle(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
                approved_preview_sha256=preview["preview_sha256"],
                output=output,
                run_id="m10-cleanup-failure",
                observed_runner=observed_runner,
            )

            self.assertIsNotNone(result.observed)
            lifecycle = result.observed.lifecycle
            self.assertEqual(["application", "dependency"], actual_termination_order)
            self.assertEqual(
                ("application", "dependency"), lifecycle.teardown_attempt_order
            )
            self.assertEqual(
                ("application", "dependency"), lifecycle.actual_teardown_order
            )
            self.assertEqual("NONE", lifecycle.trigger_reason)
            self.assertEqual("CLEANUP_ERROR", lifecycle.stop_reason)
            self.assertFalse(lifecycle.cleanup_complete)
            self.assertEqual("ERROR", result.report["execution_status"])
            self.assertEqual("FAIL", result.report["verdict"])
            self.assertIn(
                "BOOTSTRAP_CLEANUP_INCOMPLETE",
                {item["code"] for item in result.report["contamination"]},
            )
            self.assertEqual(
                "FAIL",
                next(
                    item
                    for item in result.report["assertions"]
                    if item["id"] == "bootstrap-cleanup-complete"
                )["status"],
            )
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual("CLEANUP_ERROR", bootstrap["stop"]["reason"])
            self.assertFalse(bootstrap["cleanup_complete"])
            application = next(
                node for node in bootstrap["nodes"] if node["role"] == "APPLICATION"
            )
            dependency = next(
                node for node in bootstrap["nodes"] if node["role"] == "DEPENDENCY"
            )
            self.assertFalse(application["teardown"]["handles_released"])
            self.assertTrue(dependency["teardown"]["handles_released"])
            self.assertTrue(bootstrap["browser_exercise"]["completed"])
            validated = validate_bundle(output, root)
            self.assertEqual("ERROR", validated.execution_status)
            self.assertEqual("FAIL", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_bootstrap_interrupt_handler_requests_cancel_and_restores_handlers(self) -> None:
        handled = [signal.SIGINT]
        if hasattr(signal, "SIGBREAK"):
            handled.append(signal.SIGBREAK)
        previous = {item: signal.getsignal(item) for item in handled}

        with _bootstrap_interrupt_cancellation() as cancellation:
            self.assertFalse(cancellation.is_set())
            handler = signal.getsignal(signal.SIGINT)
            self.assertTrue(callable(handler))
            handler(signal.SIGINT, None)
            self.assertTrue(cancellation.is_set())

        self.assertEqual(
            previous,
            {item: signal.getsignal(item) for item in handled},
        )

    def test_preview_approval_mismatch_creates_no_bundle_or_process(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(root)
            output = root / "bundle-rejected"
            wrong_approval = "0" * 64
            if wrong_approval == preview["preview_sha256"]:
                wrong_approval = "1" * 64

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan,
                profile=profile,
                bindings=bindings,
                approval=wrong_approval,
                output=output,
                run_id="m10-public-rejected",
            )

            self.assertEqual({}, payload)
            self.assertEqual(2, code)
            self.assertIn("does not match the live BootstrapPreview", stderr)
            self.assertFalse(output.exists())
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_preflight_stop_creates_pending_bundle_without_starting_processes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, _, ports = self._fixture(root)
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan.pop("seal")
            plan["preflight"]["available_memory_soft_min_mb"] = 1_000_000
            plan = seal_plan(plan, profile)
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            preview = build_bootstrap_preview(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
            )
            output = root / "bundle-preflight-stop"

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan_path,
                profile=profile_path,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=output,
                run_id="m10-public-preflight-stop",
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("STOP_ESCALATION", payload["resource_decision"])
            self.assertFalse(payload["bootstrap_started"])
            self.assertIsNone(payload["services_ready"])
            self.assertIsNone(payload["browser_started"])
            self.assertIsNone(payload["browser_completed"])
            self.assertIsNone(payload["browser_capture_complete"])
            self.assertIsNone(payload["stop_reason"])
            self.assertIsNone(payload["cleanup_complete"])
            self.assertEqual("ABORTED", payload["execution_status"])
            self.assertEqual("PENDING", payload["verdict"])
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(
                ["browser.session", "runtime.bootstrap"], report["missing_evidence"]
            )
            self.assertEqual(
                ["runtime.preflight"],
                [item["evidence_type"] for item in report["evidence"]],
            )
            self.assertFalse((output / "attachments").exists())
            validated = validate_bundle(output, root)
            self.assertEqual("ABORTED", validated.execution_status)
            self.assertEqual("PENDING", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_preflight_abort_creates_pending_bundle_without_starting_processes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, _, ports = self._fixture(root)
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan.pop("seal")
            plan["preflight"]["available_memory_soft_min_mb"] = 1_000_000
            plan["preflight"]["available_memory_hard_min_mb"] = 1_000_000
            plan = seal_plan(plan, profile)
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            preview = build_bootstrap_preview(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
            )
            output = root / "bundle-preflight-abort"

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan_path,
                profile=profile_path,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=output,
                run_id="m10-public-preflight-abort",
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("ABORT", payload["resource_decision"])
            self.assertFalse(payload["bootstrap_started"])
            self.assertEqual("ABORTED", payload["execution_status"])
            self.assertEqual("PENDING", payload["verdict"])
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual([], report["contamination"])
            self.assertEqual(
                ["runtime.preflight"],
                [item["evidence_type"] for item in report["evidence"]],
            )
            validated = validate_bundle(output, root)
            self.assertEqual("ABORTED", validated.execution_status)
            self.assertEqual("PENDING", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_stopped_preflight_never_calls_observed_runner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, _, _ = self._fixture(root)
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan.pop("seal")
            plan["preflight"]["available_memory_soft_min_mb"] = 1_000_000
            plan = seal_plan(plan, profile)
            preview = build_bootstrap_preview(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
            )

            def fail_if_called(*_args, **_kwargs):
                self.fail("preflight-stopped run invoked the observed bootstrap runner")

            result = run_bootstrap_bundle(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
                approved_preview_sha256=preview["preview_sha256"],
                output=root / "stopped-direct",
                run_id="m10-stopped-direct",
                observed_runner=fail_if_called,
            )
            self.assertIsNone(result.observed)
            self.assertEqual("ABORTED", result.report["execution_status"])
            self.assertEqual("PENDING", result.report["verdict"])

    def test_invalid_run_id_is_rejected_before_live_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(root)
            output = root / "bundle-invalid-id"

            code, payload, stderr = self._run(
                subject=subject,
                plan=plan,
                profile=profile,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=output,
                run_id="INVALID ID",
            )

            self.assertEqual({}, payload)
            self.assertEqual(2, code)
            self.assertIn("run_id must be a 2-64 character lowercase identifier", stderr)
            self.assertFalse(output.exists())
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))


if __name__ == "__main__":
    unittest.main()
