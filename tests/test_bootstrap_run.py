from __future__ import annotations

import http.client
import os
import shutil
import socket
import sys
import tempfile
import unittest
from pathlib import Path

from veritrail.bootstrap_preview import ResolvedBootstrap, ResolvedBootstrapNode
from veritrail.bootstrap_run import (
    BootstrapBrowserObservation,
    run_observed_bootstrap,
)
from veritrail.canonical import sha256_json
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile

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


def _authorities(subject: Path) -> tuple[dict, dict, ResolvedBootstrap]:
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
        {"literal": "application"},
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
                executable_identity={"sha256": "a" * 64},
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


def _exercise(port: int) -> BootstrapBrowserObservation:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
    try:
        connection.request("GET", "/")
        response = connection.getresponse()
        content = response.read(4096)
    finally:
        connection.close()
    if response.status != 200 or b'"dependency_status": 200' not in content:
        raise AssertionError("application exercise did not observe its dependency")
    return BootstrapBrowserObservation(evidence_sha256="b" * 64, peak_rss_mb=8.0)


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
                node["port"] for node in profile["nodes"] if node["role"] == "APPLICATION"
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
                browser_runner=lambda: _exercise(application_port),
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

            def exercise_with_drift() -> BootstrapBrowserObservation:
                observed = _exercise(application_port)
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
                browser_runner=lambda: _exercise(application_port),
                staging_writer=fail_staging,
            )
            self.assertIsNone(result.evidence)
            self.assertEqual("EVIDENCE_STAGING_VERIFY_FAILED", result.error_type)
            self.assertEqual("EVIDENCE_ERROR", result.lifecycle.stop_reason)
            self.assertTrue(result.lifecycle.cleanup_complete)
            self.assertTrue(result.run_work_released)
            self.assertTrue(result.staging_released)
            self.assertTrue(result.owned_root_released)
            self.assertEqual([], list((root / "artifacts").glob(".veritrail-*")))


if __name__ == "__main__":
    unittest.main()
