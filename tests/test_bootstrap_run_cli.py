from __future__ import annotations

import copy
import io
import json
import os
import shutil
import signal
import socket
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from veritrail.bootstrap_preview import build_bootstrap_preview, resolve_bootstrap
from veritrail.bootstrap_browser import (
    ObservedBrowserCollectionError,
    ObservedBrowserEvidence,
    collect_observed_browser_evidence,
)
from veritrail.bootstrap_public_run import BootstrapPublicRunResult, run_bootstrap_bundle
from veritrail.bootstrap_run import run_observed_bootstrap
from veritrail.catalog import build_catalog, validate_bundle
from veritrail.cli import _bootstrap_interrupt_cancellation, main
from veritrail.comparison import create_comparison_bundle
from veritrail.evidence import import_evidence_document
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile
from veritrail.windows_readiness import probe_owned_http_readiness
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


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(0.2)
        return client.connect_ex(("127.0.0.1", port)) != 0


def _subject_drift_failure_diagnostic(
    *, report: dict, browser: dict, bootstrap: dict
) -> dict:
    """Project bounded first-failure facts without changing product semantics."""

    failed_network = []
    for item in browser.get("network", []):
        status = item.get("status")
        if (
            item.get("finished") is not True
            or item.get("failure") is not None
            or status is None
            or (isinstance(status, int) and status >= 400)
        ):
            failed_network.append(
                {
                    key: item.get(key)
                    for key in (
                        "sequence",
                        "viewport",
                        "method",
                        "url",
                        "resource_type",
                        "status",
                        "finished",
                        "failure",
                    )
                }
            )
    return {
        "report": {
            "execution_status": report.get("execution_status"),
            "verdict": report.get("verdict"),
            "contamination_codes": [
                item.get("code") for item in report.get("contamination", [])
            ],
        },
        "browser": {
            "capture_complete": browser.get("capture_complete"),
            "all_steps_passed": browser.get("all_steps_passed"),
            "cleanup_complete": browser.get("cleanup_complete"),
            "collection_errors": browser.get("collection_errors"),
            "failed_request_count": browser.get("failed_request_count"),
            "failed_network": failed_network,
            "viewport_statuses": [
                {
                    "name": item.get("name"),
                    "status": item.get("status"),
                    "is_mobile": item.get("is_mobile"),
                }
                for item in browser.get("viewport_runs", [])
            ],
            "step_statuses": [
                {
                    key: item.get(key)
                    for key in (
                        "viewport",
                        "step_id",
                        "action",
                        "status",
                        "error_type",
                        "error",
                    )
                }
                for item in browser.get("steps", [])
            ],
        },
        "bootstrap": {
            "stop": bootstrap.get("stop"),
            "subject_observation": bootstrap.get("subject_observation"),
            "browser_exercise": bootstrap.get("browser_exercise"),
            "cleanup": bootstrap.get("cleanup"),
            "cleanup_complete": bootstrap.get("cleanup_complete"),
            "lifecycle_events": bootstrap.get("lifecycle_events"),
        },
    }


_MAX_ATTEMPT_EVENTS = 64
_MAX_ATTEMPT_NODES = 16
_MAX_BROWSER_RECORDS = 64
_MAX_DIAGNOSTIC_BYTES = 65_536
_MAX_DIAGNOSTIC_TEXT = 1_024


def _bounded_sequence(value: object, *, label: str, limit: int) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise AssertionError(f"{label} must be a list or tuple")
    if len(value) > limit:
        raise AssertionError(f"{label} exceeds the diagnostic bound {limit}")
    return tuple(value)


def _bounded_text(value: object, *, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise AssertionError(f"{label} must be text or None")
    if len(value) > _MAX_DIAGNOSTIC_TEXT:
        raise AssertionError(f"{label} exceeds the diagnostic text bound")
    return value


def _bounded_mapping_projection(
    value: object, *, label: str, keys: tuple[str, ...]
) -> dict[str, object]:
    if not isinstance(value, dict):
        raise AssertionError(f"{label} must be a mapping")
    return {key: value.get(key) for key in keys}


def _bootstrap_node_projection(node: object) -> dict[str, object]:
    start = getattr(node, "start")
    readiness = getattr(node, "readiness")
    teardown = getattr(node, "teardown")
    readiness_attempts = ()
    if readiness is not None:
        readiness_attempts = _bounded_sequence(
            getattr(readiness, "attempts"),
            label="readiness attempts",
            limit=_MAX_BROWSER_RECORDS,
        )
    return {
        "node_id": _bounded_text(getattr(node, "node_id"), label="node id"),
        "role": _bounded_text(getattr(node, "role"), label="node role"),
        "start": None
        if start is None
        else {
            "error_type": _bounded_text(start.error_type, label="start error type"),
            "cleanup_complete": start.cleanup_complete,
            "process_created": start.process_created,
            "target_assigned": start.target_assigned,
            "target_resumed": start.target_resumed,
        },
        "readiness": None
        if readiness is None
        else {
            "ready": readiness.ready,
            "error_type": _bounded_text(
                readiness.error_type, label="readiness error type"
            ),
            "attempt_count": len(readiness_attempts),
        },
        "teardown": None
        if teardown is None
        else {
            "error_type": _bounded_text(
                teardown.error_type, label="teardown error type"
            ),
            "termination_reason": _bounded_text(
                teardown.termination_reason, label="termination reason"
            ),
            "cleanup_complete": teardown.cleanup_complete,
            "port_free": teardown.port_free,
            "handles_released": teardown.handles_released,
            "readers_released": teardown.readers_released,
        },
    }


def _bootstrap_attempt_projection(
    result: BootstrapPublicRunResult,
) -> dict[str, object]:
    report = result.report
    if not isinstance(report, dict):
        raise AssertionError("bootstrap report must be a mapping")
    projection: dict[str, object] = {
        "report": {
            "execution_status": report.get("execution_status"),
            "verdict": report.get("verdict"),
        },
        "observed": None,
    }
    observed = result.observed
    if observed is None:
        return projection

    lifecycle = observed.lifecycle
    events = _bounded_sequence(
        lifecycle.events,
        label="lifecycle events",
        limit=_MAX_ATTEMPT_EVENTS,
    )
    nodes = _bounded_sequence(
        lifecycle.nodes,
        label="lifecycle nodes",
        limit=_MAX_ATTEMPT_NODES,
    )
    browser_facts = None
    if observed.browser is not None:
        document = observed.browser.document
        if not isinstance(document, dict) or not isinstance(document.get("facts"), dict):
            raise AssertionError("browser Evidence facts must be a mapping")
        browser_facts = document["facts"]

    browser_projection = None
    if browser_facts is not None:
        failed_network = []
        for item in _bounded_sequence(
            browser_facts.get("network", []),
            label="browser network facts",
            limit=_MAX_BROWSER_RECORDS,
        ):
            if not isinstance(item, dict):
                raise AssertionError("browser network fact must be a mapping")
            status = item.get("status")
            if (
                item.get("finished") is not True
                or item.get("failure") is not None
                or status is None
                or (isinstance(status, int) and status >= 400)
            ):
                failed_network.append(
                    {
                        key: item.get(key)
                        for key in (
                            "sequence",
                            "viewport",
                            "method",
                            "url",
                            "resource_type",
                            "status",
                            "finished",
                            "failure",
                        )
                    }
                )
        collection_errors = []
        for item in _bounded_sequence(
            browser_facts.get("collection_errors", []),
            label="browser collection errors",
            limit=_MAX_BROWSER_RECORDS,
        ):
            if not isinstance(item, dict):
                raise AssertionError("browser collection error must be a mapping")
            collection_errors.append(
                {
                    "collector": item.get("collector"),
                    "error_type": item.get("error_type"),
                }
            )
        browser_projection = {
            "capture_complete": browser_facts.get("capture_complete"),
            "all_steps_passed": browser_facts.get("all_steps_passed"),
            "cleanup_complete": browser_facts.get("cleanup_complete"),
            "collection_errors": collection_errors,
            "failed_request_count": browser_facts.get("failed_request_count"),
            "failed_network": failed_network,
        }

    projection["observed"] = {
        "events": [
            {
                "ordinal": event.ordinal,
                "stage": _bounded_text(event.stage, label="lifecycle stage"),
                "result": _bounded_text(event.result, label="lifecycle result"),
            }
            for event in events
        ],
        "nodes": [_bootstrap_node_projection(node) for node in nodes],
        "services_ready": lifecycle.services_ready,
        "ready_callback_started": lifecycle.ready_callback_started,
        "ready_callback_completed": lifecycle.ready_callback_completed,
        "trigger_reason": _bounded_text(
            lifecycle.trigger_reason, label="lifecycle trigger reason"
        ),
        "stop_reason": _bounded_text(
            lifecycle.stop_reason, label="lifecycle stop reason"
        ),
        "cleanup_complete": lifecycle.cleanup_complete,
        "error_type": _bounded_text(observed.error_type, label="observed error type"),
        "resource_observation": _bounded_mapping_projection(
            observed.resource_observation,
            label="resource observation",
            keys=(
                "core_peak_rss_mb",
                "dependency_peak_rss_mb",
                "application_peak_rss_mb",
                "browser_peak_rss_mb",
                "host_available_memory_min_mb",
                "limit_trigger_reason",
                "sampling_complete",
            ),
        ),
        "subject_observation": _bounded_mapping_projection(
            observed.subject_observation,
            label="subject observation",
            keys=("changed", "scan_complete"),
        ),
        "run_work_released": observed.run_work_released,
        "staging_released": observed.staging_released,
        "owned_root_released": observed.owned_root_released,
        "browser_present": observed.browser is not None,
        "browser": browser_projection,
    }
    return projection


class _BootstrapAttemptObserver:
    """Capture one same-attempt diagnostic without changing product control flow."""

    def __init__(self, original=run_bootstrap_bundle, *, projector=None) -> None:
        self._original = original
        self._projector = projector or _bootstrap_attempt_projection
        self._call_count = 0
        self._result: object | None = None
        self._exception: BaseException | None = None
        self._projection: dict[str, object] | None = None
        self._diagnostic_error: BaseException | None = None

    def __call__(self, *args, **kwargs):
        if self._call_count != 0:
            raise AssertionError("bootstrap attempt observer must wrap exactly one call")
        self._call_count = 1
        try:
            result = self._original(*args, **kwargs)
        except Exception as exc:
            self._exception = exc
            try:
                self._projection = {
                    "exception": {
                        "type": type(exc).__name__,
                        "message": _bounded_text(
                            str(exc), label="bootstrap exception message"
                        ),
                    }
                }
            except Exception as diagnostic_exc:
                self._diagnostic_error = diagnostic_exc
            raise

        self._result = result
        if not isinstance(result, BootstrapPublicRunResult):
            self._diagnostic_error = AssertionError(
                "bootstrap attempt returned a foreign result type"
            )
            return result
        try:
            self._projection = {"result": self._projector(result)}
        except Exception as diagnostic_exc:
            self._diagnostic_error = diagnostic_exc
        return result

    def diagnostic(self, *, returned: object | None = None) -> dict[str, object]:
        if self._call_count != 1:
            raise AssertionError("bootstrap attempt observer did not wrap exactly one call")
        captured = self._exception if self._exception is not None else self._result
        if returned is not None and returned is not captured:
            raise AssertionError("bootstrap attempt observer detected result replacement")
        if self._diagnostic_error is not None:
            raise AssertionError("bootstrap attempt diagnostic failed") from self._diagnostic_error
        if self._projection is None:
            raise AssertionError("bootstrap attempt diagnostic is missing")
        try:
            encoded = json.dumps(
                self._projection,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        except Exception as exc:
            raise AssertionError("bootstrap attempt diagnostic is not JSON-safe") from exc
        if len(encoded) > _MAX_DIAGNOSTIC_BYTES:
            raise AssertionError("bootstrap attempt diagnostic exceeds its byte bound")
        return self._projection


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
        # Positive functional paths inherit the canonical bounded fail-safe.
        # Dedicated lifecycle tests own deadline and cancellation timing.
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

    def test_shared_positive_fixture_keeps_canonical_lifecycle_budget(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, _, profile_path, _, _, ports = self._fixture(root)
            profile = json.loads(profile_path.read_text(encoding="utf-8"))

            self.assertEqual(120_000, bootstrap_profile()["lifecycle_timeout_ms"])
            self.assertEqual(
                bootstrap_profile()["lifecycle_timeout_ms"],
                profile["lifecycle_timeout_ms"],
            )
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

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

    def _run_with_browser_error_trace(
        self,
        *,
        subject: Path,
        plan: Path,
        profile: Path,
        bindings: Path,
        approval: str,
        output: Path,
        run_id: str,
        browser_collector=collect_observed_browser_evidence,
    ) -> tuple[int, dict, str, tuple[str, ...]]:
        error_types: list[str] = []

        def traced_browser_collector(*args, **kwargs):
            try:
                return browser_collector(*args, **kwargs)
            except ObservedBrowserCollectionError as exc:
                error_types.append(exc.error_type)
                raise

        with patch(
            "veritrail.bootstrap_run.collect_observed_browser_evidence",
            side_effect=traced_browser_collector,
        ):
            code, payload, stderr = self._run(
                subject=subject,
                plan=plan,
                profile=profile,
                bindings=bindings,
                approval=approval,
                output=output,
                run_id=run_id,
            )
        return code, payload, stderr, tuple(error_types)

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

    def test_catalog_accepts_public_m10_outcomes_and_isolates_a_corrupt_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            fixture = base / "fixture"
            fixture.mkdir()
            artifacts = base / "artifacts"
            artifacts.mkdir()
            subject, plan_path, profile_path, bindings, preview, ports = self._fixture(
                fixture
            )

            pass_output = artifacts / "pass"
            code, payload, stderr = self._run(
                subject=subject,
                plan=plan_path,
                profile=profile_path,
                bindings=bindings,
                approval=preview["preview_sha256"],
                output=pass_output,
                run_id="m10-catalog-pass",
            )
            self.assertEqual((0, "", "PASS"), (code, stderr, payload["verdict"]))

            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            stopped_plan = json.loads(plan_path.read_text(encoding="utf-8"))
            stopped_plan.pop("seal")
            stopped_plan["preflight"]["available_memory_soft_min_mb"] = 1_000_000
            stopped_plan = seal_plan(stopped_plan, profile)
            stopped_plan_path = fixture / "sealed-plan-stopped.json"
            stopped_plan_path.write_text(json.dumps(stopped_plan), encoding="utf-8")
            stopped_preview = build_bootstrap_preview(
                stopped_plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
            )
            stopped_output = artifacts / "stopped"
            code, payload, stderr = self._run(
                subject=subject,
                plan=stopped_plan_path,
                profile=profile_path,
                bindings=bindings,
                approval=stopped_preview["preview_sha256"],
                output=stopped_output,
                run_id="m10-catalog-stopped",
            )
            self.assertEqual(
                (0, "", "ABORTED", "PENDING"),
                (code, stderr, payload["execution_status"], payload["verdict"]),
            )

            corrupt_output = artifacts / "corrupt-copy"
            shutil.copytree(pass_output, corrupt_output)
            report_path = corrupt_output / "report.json"
            report_path.write_bytes(report_path.read_bytes() + b" ")

            catalog_output = base / "catalog"
            catalog = build_catalog(artifacts, catalog_output)
            self.assertEqual("COMPLETED_WITH_ISSUES", catalog.status)
            self.assertEqual(2, catalog.run_count)
            self.assertEqual(1, catalog.issue_count)
            connection = sqlite3.connect(catalog_output / "catalog.sqlite3")
            try:
                runs = connection.execute(
                    "SELECT run_id, execution_status, verdict "
                    "FROM catalog_runs ORDER BY run_id"
                ).fetchall()
                issues = connection.execute(
                    "SELECT code FROM catalog_issues ORDER BY issue_id"
                ).fetchall()
            finally:
                connection.close()
            self.assertEqual(
                [
                    ("m10-catalog-pass", "COMPLETED", "PASS"),
                    ("m10-catalog-stopped", "ABORTED", "PENDING"),
                ],
                runs,
            )
            self.assertEqual([("BUNDLE_SIZE_MISMATCH",)], issues)
            self.assertEqual([], list(base.glob(".veritrail-catalog-*")))
            self.assertEqual([], list(fixture.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_same_attempt_failure_observer_is_bounded_and_fail_closed(self) -> None:
        def controlled_result(
            *,
            execution_status: str = "COMPLETED",
            verdict: str = "PASS",
            browser_facts: dict | None = None,
            resource_sampling_complete: bool = True,
        ) -> BootstrapPublicRunResult:
            lifecycle = SimpleNamespace(
                events=(
                    SimpleNamespace(
                        ordinal=1,
                        stage="EXERCISED",
                        result=(
                            "COMPLETE"
                            if execution_status == "COMPLETED"
                            else "COLLECTOR_ERROR"
                        ),
                    ),
                ),
                nodes=(),
                services_ready=True,
                ready_callback_started=True,
                ready_callback_completed=execution_status == "COMPLETED",
                trigger_reason="NONE",
                stop_reason=(
                    "NONE"
                    if execution_status == "COMPLETED"
                    else "COLLECTOR_ERROR"
                ),
                cleanup_complete=True,
            )
            browser = (
                None
                if browser_facts is None
                else SimpleNamespace(document={"facts": browser_facts})
            )
            observed = SimpleNamespace(
                lifecycle=lifecycle,
                evidence=object(),
                browser=browser,
                resource_observation={
                    "core_peak_rss_mb": 1.0,
                    "dependency_peak_rss_mb": 1.0,
                    "application_peak_rss_mb": 1.0,
                    "browser_peak_rss_mb": 1.0,
                    "host_available_memory_min_mb": 1_024.0,
                    "limit_trigger_reason": None,
                    "sampling_complete": resource_sampling_complete,
                },
                subject_observation={"changed": False, "scan_complete": True},
                run_work_released=True,
                staging_released=True,
                owned_root_released=True,
                staged_sha256="0" * 64,
                error_type=(
                    None if execution_status == "COMPLETED" else "BROWSER_INCOMPLETE"
                ),
            )
            return BootstrapPublicRunResult(
                report={"execution_status": execution_status, "verdict": verdict},
                preflight=None,
                observed=observed,
                preview_sha256="1" * 64,
            )

        success = controlled_result()
        success_observer = _BootstrapAttemptObserver(lambda: success)
        returned = success_observer()
        self.assertIs(success, returned)
        success_diagnostic = success_observer.diagnostic(returned=returned)
        self.assertEqual(
            ("COMPLETED", "PASS"),
            (
                success_diagnostic["result"]["report"]["execution_status"],
                success_diagnostic["result"]["report"]["verdict"],
            ),
        )

        browser_exception = ObservedBrowserCollectionError(
            "DiagnosticSentinel",
            peak_rss_mb=0.0,
            resource_sampling_complete=True,
            process_cleanup_complete=True,
            job_memory_limit_mb=1,
            job_memory_limit_enforced=True,
        )

        def raise_browser_exception():
            raise browser_exception

        exception_observer = _BootstrapAttemptObserver(raise_browser_exception)
        with self.assertRaises(ObservedBrowserCollectionError) as caught:
            exception_observer()
        self.assertIs(browser_exception, caught.exception)
        self.assertEqual(
            "ObservedBrowserCollectionError",
            exception_observer.diagnostic(returned=caught.exception)["exception"][
                "type"
            ],
        )

        formed_failure = controlled_result(
            execution_status="ERROR",
            verdict="PENDING",
            browser_facts={
                "capture_complete": False,
                "all_steps_passed": False,
                "cleanup_complete": True,
                "collection_errors": [
                    {
                        "collector": "network:desktop",
                        "error_type": "HostSocketNoBufferSpace",
                    }
                ],
                "failed_request_count": 1,
                "network": [
                    {
                        "sequence": 1,
                        "viewport": "desktop",
                        "method": "GET",
                        "url": "http://127.0.0.1/",
                        "resource_type": "document",
                        "status": None,
                        "finished": False,
                        "failure": "net::ERR_NO_BUFFER_SPACE",
                    }
                ],
            },
        )
        formed_observer = _BootstrapAttemptObserver(lambda: formed_failure)
        self.assertIs(formed_failure, formed_observer())
        formed_projection = formed_observer.diagnostic()["result"]["observed"]
        self.assertEqual(
            "net::ERR_NO_BUFFER_SPACE",
            formed_projection["browser"]["failed_network"][0]["failure"],
        )

        incomplete_resource = controlled_result(resource_sampling_complete=False)
        resource_observer = _BootstrapAttemptObserver(lambda: incomplete_resource)
        self.assertIs(incomplete_resource, resource_observer())
        self.assertFalse(
            resource_observer.diagnostic()["result"]["observed"][
                "resource_observation"
            ]["sampling_complete"]
        )

        call_count = 0

        def counted_result():
            nonlocal call_count
            call_count += 1
            return success

        duplicate_observer = _BootstrapAttemptObserver(counted_result)
        self.assertIs(success, duplicate_observer())
        with self.assertRaises(AssertionError):
            duplicate_observer()
        self.assertEqual(1, call_count)

        foreign = object()
        foreign_observer = _BootstrapAttemptObserver(lambda: foreign)
        self.assertIs(foreign, foreign_observer())
        with self.assertRaises(AssertionError):
            foreign_observer.diagnostic()

        replacement_observer = _BootstrapAttemptObserver(lambda: success)
        self.assertIs(success, replacement_observer())
        with self.assertRaises(AssertionError):
            replacement_observer.diagnostic(returned=object())

        unbounded = controlled_result()
        unbounded.observed.lifecycle.events = tuple(
            SimpleNamespace(ordinal=index, stage="EXERCISED", result="COMPLETE")
            for index in range(_MAX_ATTEMPT_EVENTS + 1)
        )
        unbounded_observer = _BootstrapAttemptObserver(lambda: unbounded)
        self.assertIs(unbounded, unbounded_observer())
        with self.assertRaises(AssertionError):
            unbounded_observer.diagnostic()

        def fail_diagnostic(_result):
            raise RuntimeError("diagnostic sentinel")

        diagnostic_failure_observer = _BootstrapAttemptObserver(
            lambda: success,
            projector=fail_diagnostic,
        )
        self.assertIs(success, diagnostic_failure_observer())
        with self.assertRaises(AssertionError):
            diagnostic_failure_observer.diagnostic()

    def test_same_sealed_authorities_repeat_without_residual_contamination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(root)
            outputs = (root / "bundle-repeat-one", root / "bundle-repeat-two")
            first_manifest: bytes | None = None

            for ordinal, output in enumerate(outputs, start=1):
                attempt_observer = _BootstrapAttemptObserver()
                with patch(
                    "veritrail.cli.run_bootstrap_bundle",
                    side_effect=attempt_observer,
                ):
                    code, payload, stderr, browser_error_types = (
                        self._run_with_browser_error_trace(
                            subject=subject,
                            plan=plan,
                            profile=profile,
                            bindings=bindings,
                            approval=preview["preview_sha256"],
                            output=output,
                            run_id=f"m10-public-repeat-{ordinal}",
                        )
                    )
                diagnostic = {
                    "payload": payload,
                    "browser_error_types": browser_error_types,
                    "same_attempt": attempt_observer.diagnostic(),
                }
                self.assertEqual("", stderr)
                self.assertEqual(0, code)
                self.assertEqual("PROCEED", payload["resource_decision"])
                self.assertEqual(
                    "COMPLETED", payload["execution_status"], msg=diagnostic
                )
                self.assertEqual("PASS", payload["verdict"], msg=diagnostic)
                self.assertTrue(payload["cleanup_complete"], msg=diagnostic)
                self.assertEqual((), browser_error_types, msg=diagnostic)
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

            code, payload, stderr, browser_error_types = (
                self._run_with_browser_error_trace(
                    subject=subject,
                    plan=plan,
                    profile=profile,
                    bindings=bindings,
                    approval=preview["preview_sha256"],
                    output=output,
                    run_id="m10-public-fail",
                )
            )
            diagnostic = {
                "payload": payload,
                "browser_error_types": browser_error_types,
            }

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual(
                "BROWSER_HARD_FAILURE", payload["stop_reason"], msg=diagnostic
            )
            self.assertFalse(payload["browser_capture_complete"], msg=diagnostic)
            self.assertTrue(payload["cleanup_complete"], msg=diagnostic)
            self.assertEqual(
                "COMPLETED", payload["execution_status"], msg=diagnostic
            )
            self.assertEqual("FAIL", payload["verdict"], msg=diagnostic)
            self.assertEqual((), browser_error_types, msg=diagnostic)
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertNotIn(
                "BROWSER_STATUS_CONFLICT",
                {item["code"] for item in report["contamination"]},
            )
            validated = validate_bundle(output, root)
            self.assertEqual("FAIL", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_host_socket_failure_is_collector_error_with_raw_network_fact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(root)
            output = root / "bundle-host-socket-collector-error"

            def host_socket_failure(
                active_plan: dict, **_kwargs
            ) -> ObservedBrowserEvidence:
                original = _browser_artifact(active_plan)
                document = copy.deepcopy(original.document)
                facts = document["facts"]
                raw_failure_text = "net::ERR_NO_BUFFER_SPACE"
                facts["network"][0].update(
                    {
                        "status": None,
                        "finished": False,
                        "failure": raw_failure_text,
                    }
                )
                facts["failed_request_count"] = 1
                facts["capture_complete"] = False
                facts["all_steps_passed"] = False
                facts["viewport_runs"][0]["status"] = "FAILED"
                facts["collection_errors"] = [
                    {
                        "collector": "network:desktop",
                        "error_type": "HostSocketNoBufferSpace",
                    }
                ]
                return ObservedBrowserEvidence(
                    browser=import_evidence_document(
                        document,
                        "browser-host-socket-failure.json",
                        attachments=original.attachments,
                    ),
                    peak_rss_mb=8.0,
                    resource_sampling_complete=True,
                    process_cleanup_complete=True,
                    job_memory_limit_mb=active_plan["browser"][
                        "max_job_memory_mb"
                    ],
                    job_memory_limit_enforced=True,
                )

            code, payload, stderr, browser_error_types = (
                self._run_with_browser_error_trace(
                    subject=subject,
                    plan=plan,
                    profile=profile,
                    bindings=bindings,
                    approval=preview["preview_sha256"],
                    output=output,
                    run_id="m10-host-socket-collector-error",
                    browser_collector=host_socket_failure,
                )
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("COLLECTOR_ERROR", payload["stop_reason"])
            self.assertFalse(payload["browser_capture_complete"])
            self.assertTrue(payload["cleanup_complete"])
            self.assertEqual("ERROR", payload["execution_status"])
            self.assertEqual("PENDING", payload["verdict"])
            self.assertEqual((), browser_error_types)

            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            browser_assertions = [
                item
                for item in report["assertions"]
                if item["evidence_type"] == "browser.session"
            ]
            self.assertTrue(browser_assertions)
            self.assertEqual(
                {"NOT_EVALUATED"}, {item["status"] for item in browser_assertions}
            )
            self.assertEqual([], report["contamination"])

            browser = self._evidence_document(output, "browser.session")["facts"]
            self.assertEqual(
                "net::ERR_NO_BUFFER_SPACE", browser["network"][0]["failure"]
            )
            self.assertEqual(
                [
                    {
                        "collector": "network:desktop",
                        "error_type": "HostSocketNoBufferSpace",
                    }
                ],
                browser["collection_errors"],
            )
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual("COLLECTOR_ERROR", bootstrap["stop"]["reason"])
            self.assertTrue(bootstrap["cleanup_complete"])
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_browser_process_cleanup_failure_is_public_error_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, preview, ports = self._fixture(
                root
            )
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            output = root / "bundle-browser-cleanup-failure"

            def incomplete_browser(active_plan: dict) -> ObservedBrowserEvidence:
                observed = collect_observed_browser_evidence(active_plan)
                return replace(observed, process_cleanup_complete=False)

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
                    browser_runner=incomplete_browser,
                )

            result = run_bootstrap_bundle(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
                approved_preview_sha256=preview["preview_sha256"],
                output=output,
                run_id="m10-browser-cleanup-failure",
                observed_runner=observed_runner,
            )

            self.assertIsNotNone(result.observed)
            self.assertEqual("ERROR", result.report["execution_status"])
            self.assertEqual("FAIL", result.report["verdict"])
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual("CLEANUP_ERROR", bootstrap["stop"]["reason"])
            self.assertFalse(bootstrap["cleanup_complete"])
            self.assertFalse(
                bootstrap["browser_exercise"]["process_cleanup_complete"]
            )
            validated = validate_bundle(output, root)
            self.assertEqual("ERROR", validated.execution_status)
            self.assertEqual("FAIL", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_runtime_resource_stops_and_sampling_failure_preserve_pending_verdict(
        self,
    ) -> None:
        scenarios = (
            (
                "soft",
                lambda: (16 * 1024**3, 1_536 * 1024**2),
                "RESOURCE_MEMORY_SOFT_LIMIT",
                "ABORTED",
            ),
            (
                "hard",
                lambda: (16 * 1024**3, 0),
                "RESOURCE_MEMORY_HARD_LIMIT",
                "ABORTED",
            ),
            (
                "sampling-error",
                lambda: (_ for _ in ()).throw(OSError("unavailable")),
                "EVIDENCE_ERROR",
                "ERROR",
            ),
        )
        for name, memory_reader, expected_reason, expected_status in scenarios:
            with self.subTest(scenario=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                subject, plan_path, profile_path, bindings, preview, ports = self._fixture(
                    root
                )
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                plan.pop("seal")
                plan["preflight"].update(
                    {
                        "sample_count": 2,
                        "available_memory_soft_min_mb": 2_048,
                        "available_memory_hard_min_mb": 1_024,
                        "hard_breach_grace_samples": 2,
                    }
                )
                plan = seal_plan(plan, profile)
                preview = build_bootstrap_preview(
                    plan,
                    profile,
                    subject_root=subject,
                    tool_bindings_path=bindings,
                )
                output = root / f"bundle-runtime-{name}"

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
                        host_memory_reader=memory_reader,
                    )

                result = run_bootstrap_bundle(
                    plan,
                    profile,
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    approved_preview_sha256=preview["preview_sha256"],
                    output=output,
                    run_id=f"m10-runtime-{name}",
                    observed_runner=observed_runner,
                )

                self.assertIsNotNone(result.observed)
                self.assertEqual(expected_status, result.report["execution_status"])
                self.assertEqual("PENDING", result.report["verdict"])
                self.assertEqual(
                    "NOT_EVALUATED",
                    next(
                        item
                        for item in result.report["assertions"]
                        if item["id"] == "bootstrap-services-ready"
                    )["status"],
                )
                bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
                self.assertEqual(expected_reason, bootstrap["stop"]["reason"])
                self.assertTrue(bootstrap["cleanup_complete"])
                validated = validate_bundle(output, root)
                self.assertEqual(expected_status, validated.execution_status)
                self.assertEqual("PENDING", validated.verdict)
                self.assertEqual([], list(root.glob(".veritrail-*")))
                self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_user_cancel_during_browser_creates_public_pending_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, _, ports = self._fixture(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            plan.pop("seal")
            plan["browser"]["steps"] = [
                {
                    "id": "wait-for-unreachable-text",
                    "action": "expect_text",
                    "selector": "[data-testid='status']",
                    "value": "this text is never produced",
                }
            ]
            plan = seal_plan(plan, profile)
            preview = build_bootstrap_preview(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
            )
            output = root / "bundle-browser-user-cancelled"
            cancellation = threading.Event()
            browser_entered = threading.Event()
            original = collect_observed_browser_evidence

            def observed_browser(active_plan: dict, **kwargs):
                browser_entered.set()
                return original(active_plan, **kwargs)

            def cancel_during_browser() -> None:
                if not browser_entered.wait(5):
                    return
                time.sleep(0.5)
                cancellation.set()

            trigger = threading.Thread(target=cancel_during_browser, daemon=True)
            trigger.start()
            with patch(
                "veritrail.bootstrap_run.collect_observed_browser_evidence",
                side_effect=observed_browser,
            ):
                result = run_bootstrap_bundle(
                    plan,
                    profile,
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    approved_preview_sha256=preview["preview_sha256"],
                    output=output,
                    run_id="m10-browser-user-cancelled",
                    cancel_event=cancellation,
                )
            trigger.join(2)

            self.assertFalse(trigger.is_alive())
            self.assertIsNotNone(result.observed)
            self.assertEqual("ABORTED", result.report["execution_status"])
            self.assertEqual("PENDING", result.report["verdict"])
            self.assertEqual(["browser.session"], result.report["missing_evidence"])
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual("USER_CANCELLED", bootstrap["stop"]["reason"])
            self.assertTrue(bootstrap["services_ready"])
            self.assertTrue(bootstrap["browser_exercise"]["started"])
            self.assertFalse(bootstrap["browser_exercise"]["completed"])
            self.assertTrue(
                bootstrap["browser_exercise"]["process_cleanup_complete"]
            )
            self.assertTrue(bootstrap["cleanup_complete"])
            validated = validate_bundle(output, root)
            self.assertEqual("ABORTED", validated.execution_status)
            self.assertEqual("PENDING", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_browser_collector_error_creates_public_error_pending_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, preview, ports = self._fixture(
                root
            )
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            output = root / "bundle-browser-collector-error"

            def fail_browser(active_plan: dict) -> ObservedBrowserEvidence:
                raise ObservedBrowserCollectionError(
                    "SafetyError",
                    peak_rss_mb=0.0,
                    resource_sampling_complete=True,
                    process_cleanup_complete=True,
                    job_memory_limit_mb=active_plan["browser"]["max_job_memory_mb"],
                    job_memory_limit_enforced=True,
                )

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
                    browser_runner=fail_browser,
                )

            result = run_bootstrap_bundle(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
                approved_preview_sha256=preview["preview_sha256"],
                output=output,
                run_id="m10-browser-collector-error",
                observed_runner=observed_runner,
            )

            self.assertIsNotNone(result.observed)
            self.assertEqual("ERROR", result.report["execution_status"])
            self.assertEqual("PENDING", result.report["verdict"])
            self.assertEqual(["browser.session"], result.report["missing_evidence"])
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual("COLLECTOR_ERROR", bootstrap["stop"]["reason"])
            self.assertTrue(bootstrap["browser_exercise"]["started"])
            self.assertFalse(bootstrap["browser_exercise"]["completed"])
            self.assertTrue(
                bootstrap["browser_exercise"]["process_cleanup_complete"]
            )
            self.assertTrue(bootstrap["cleanup_complete"])
            validated = validate_bundle(output, root)
            self.assertEqual("ERROR", validated.execution_status)
            self.assertEqual("PENDING", validated.verdict)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_browser_collector_error_trace_keeps_the_exact_private_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(root)
            output = root / "bundle-browser-collector-error-trace"

            def fail_browser(active_plan: dict, **_kwargs) -> ObservedBrowserEvidence:
                raise ObservedBrowserCollectionError(
                    "DiagnosticSentinel",
                    peak_rss_mb=0.0,
                    resource_sampling_complete=True,
                    process_cleanup_complete=True,
                    job_memory_limit_mb=active_plan["browser"]["max_job_memory_mb"],
                    job_memory_limit_enforced=True,
                )

            code, payload, stderr, browser_error_types = (
                self._run_with_browser_error_trace(
                    subject=subject,
                    plan=plan,
                    profile=profile,
                    bindings=bindings,
                    approval=preview["preview_sha256"],
                    output=output,
                    run_id="m10-browser-collector-error-trace",
                    browser_collector=fail_browser,
                )
            )

            self.assertEqual("", stderr)
            self.assertEqual(0, code)
            self.assertEqual("ERROR", payload["execution_status"])
            self.assertTrue(payload["cleanup_complete"])
            self.assertEqual(("DiagnosticSentinel",), browser_error_types)
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

    def test_dependency_early_exit_creates_completed_fail_bundle_without_browser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings, preview, ports = self._fixture(
                root, bootstrap_failure="dependency-early-exit"
            )
            output = root / "bundle-dependency-early-exit"

            optimization_flag = (
                ["-" + ("O" * sys.flags.optimize)] if sys.flags.optimize else []
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    *optimization_flag,
                    "-X",
                    "faulthandler",
                    "-m",
                    "veritrail",
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
                    preview["preview_sha256"],
                    "--output",
                    str(output),
                    "--run-id",
                    "m10-dependency-early-exit",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            diagnostic = {
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }

            self.assertEqual("", completed.stderr, msg=diagnostic)
            self.assertEqual(0, completed.returncode, msg=diagnostic)
            payload = json.loads(completed.stdout)
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

    def test_subject_drift_failure_diagnostic_retains_browser_cause_facts(self) -> None:
        # Proof-facility witness only; the real Chromium test below remains authoritative.
        browser = copy.deepcopy(_browser_artifact(bootstrap_plan()).document["facts"])
        browser["capture_complete"] = False
        browser["all_steps_passed"] = False
        browser["cleanup_complete"] = True
        browser["failed_request_count"] = 1
        browser["viewport_runs"][0]["status"] = "FAILED"
        browser["steps"][0].update(
            status="FAILED",
            error_type="TimeoutError",
            error="selector timeout",
        )
        browser["network"][0].update(
            status=None,
            finished=False,
            failure="net::ERR_NO_BUFFER_SPACE",
        )
        browser["collection_errors"] = [
            {
                "collector": "network:desktop",
                "error_type": "HostSocketNoBufferSpace",
            }
        ]
        bootstrap = {
            "stop": {"reason": "SUBJECT_DRIFT", "stage": "subject"},
            "subject_observation": {"changed": True},
            "browser_exercise": {
                "started": True,
                "completed": True,
                "process_cleanup_complete": True,
            },
            "cleanup": {"run_work_released": True, "staging_released": True},
            "cleanup_complete": True,
            "lifecycle_events": [
                {"ordinal": 1, "stage": "browser", "result": "COMPLETED"}
            ],
        }
        report = {
            "execution_status": "COMPLETED",
            "verdict": "INCONCLUSIVE",
            "contamination": [
                {"code": "BOOTSTRAP_SUBJECT_DRIFT"},
                {"code": "BROWSER_STATUS_CONFLICT"},
            ],
        }

        diagnostic = _subject_drift_failure_diagnostic(
            report=report,
            browser=browser,
            bootstrap=bootstrap,
        )

        self.assertEqual(
            ["BOOTSTRAP_SUBJECT_DRIFT", "BROWSER_STATUS_CONFLICT"],
            diagnostic["report"]["contamination_codes"],
        )
        self.assertFalse(diagnostic["browser"]["capture_complete"])
        self.assertEqual("FAILED", diagnostic["browser"]["viewport_statuses"][0]["status"])
        self.assertEqual("TimeoutError", diagnostic["browser"]["step_statuses"][0]["error_type"])
        self.assertEqual(
            "net::ERR_NO_BUFFER_SPACE",
            diagnostic["browser"]["failed_network"][0]["failure"],
        )
        self.assertEqual(
            [{"collector": "network:desktop", "error_type": "HostSocketNoBufferSpace"}],
            diagnostic["browser"]["collection_errors"],
        )
        self.assertTrue(diagnostic["bootstrap"]["subject_observation"]["changed"])
        self.assertTrue(diagnostic["bootstrap"]["cleanup_complete"])

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
            browser = self._evidence_document(output, "browser.session")["facts"]
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            diagnostic = _subject_drift_failure_diagnostic(
                report=result.report,
                browser=browser,
                bootstrap=bootstrap,
            )
            diagnostic_message = json.dumps(
                diagnostic,
                ensure_ascii=True,
                sort_keys=True,
            )
            self.assertEqual(
                {"BOOTSTRAP_SUBJECT_DRIFT"},
                {item["code"] for item in result.report["contamination"]},
                msg=diagnostic_message,
            )
            self.assertTrue(browser["capture_complete"], msg=diagnostic_message)
            self.assertTrue(browser["all_steps_passed"], msg=diagnostic_message)
            self.assertTrue(browser["cleanup_complete"], msg=diagnostic_message)
            self.assertEqual([], browser["collection_errors"], msg=diagnostic_message)
            self.assertEqual([], diagnostic["browser"]["failed_network"], msg=diagnostic_message)
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
                    def mismatch_readiness_probe(session, readiness, **kwargs):
                        nonlocal external
                        if session.port == ports[contested_index]:
                            self.assertIsNone(external)
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
                                creationflags=getattr(
                                    subprocess, "CREATE_NO_WINDOW", 0
                                ),
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                            )
                            for _ in range(60):
                                if not _port_is_free(ports[contested_index]):
                                    break
                                if external.poll() is not None:
                                    self.fail(
                                        "external listener exited before ownership probing"
                                    )
                                threading.Event().wait(0.05)
                            else:
                                self.fail("external listener did not become ready")
                        return probe_owned_http_readiness(
                            session, readiness, **kwargs
                        )

                    return run_observed_bootstrap(
                        observed_plan,
                        observed_profile,
                        resolved,
                        output_parent=output_parent,
                        cancel_event=cancel_event,
                        readiness_probe=mismatch_readiness_probe,
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

    def test_staging_failure_creates_public_error_bundle_after_reverse_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile_path, bindings, preview, ports = self._fixture(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            output = root / "bundle-staging-failure"

            def fail_staging(path: Path, content: bytes) -> None:
                path.write_bytes(content[:17])
                raise OSError("injected staging failure")

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
                    staging_writer=fail_staging,
                )

            result = run_bootstrap_bundle(
                plan,
                profile,
                subject_root=subject,
                tool_bindings_path=bindings,
                approved_preview_sha256=preview["preview_sha256"],
                output=output,
                run_id="m10-staging-failure",
                observed_runner=observed_runner,
            )

            self.assertIsNotNone(result.observed)
            self.assertEqual("EVIDENCE_STAGING_FAILED", result.observed.error_type)
            lifecycle = result.observed.lifecycle
            self.assertEqual("EVIDENCE_ERROR", lifecycle.trigger_reason)
            self.assertEqual("EVIDENCE_ERROR", lifecycle.stop_reason)
            self.assertEqual(
                ("application", "dependency"), lifecycle.actual_teardown_order
            )
            self.assertTrue(lifecycle.cleanup_complete)
            failed_index = next(
                index
                for index, event in enumerate(lifecycle.events)
                if event.stage == "EVIDENCE_FINALIZATION"
                and event.result == "EVIDENCE_STAGING_FAILED"
            )
            first_teardown = next(
                index
                for index, event in enumerate(lifecycle.events)
                if event.stage.startswith("TEARDOWN_")
            )
            self.assertLess(failed_index, first_teardown)
            self.assertEqual("ERROR", result.report["execution_status"])
            self.assertEqual("PENDING", result.report["verdict"])
            self.assertEqual([], result.report["contamination"])
            self.assertEqual([], result.report["missing_evidence"])
            bootstrap = self._evidence_document(output, "runtime.bootstrap")["facts"]
            self.assertEqual("EVIDENCE_ERROR", bootstrap["stop"]["reason"])
            self.assertTrue(bootstrap["services_ready"])
            self.assertTrue(bootstrap["browser_exercise"]["completed"])
            self.assertTrue(bootstrap["cleanup_complete"])
            self.assertEqual(6, len(list((output / "attachments").rglob("*.*"))))
            validated = validate_bundle(output, root)
            self.assertEqual("ERROR", validated.execution_status)
            self.assertEqual("PENDING", validated.verdict)
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
