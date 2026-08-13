from __future__ import annotations

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

from veritrail.bootstrap_preview import build_bootstrap_preview
from veritrail.catalog import validate_bundle
from veritrail.cli import main
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


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(0.2)
        return client.connect_ex(("127.0.0.1", port)) != 0


@unittest.skipUnless(os.name == "nt", "M10 public bootstrap Run is Windows-only")
class BootstrapRunCliTests(unittest.TestCase):
    def _fixture(
        self, root: Path, *, browser_failure: bool = False
    ) -> tuple[Path, Path, Path, Path, dict, list[int]]:
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
        application = nodes["application"]
        application["port"] = application_port
        application["arguments"] = [
            {"literal": "service.py"},
            {"literal": "browser-application"},
            {"node_port": "application"},
            {"node_origin": "dependency"},
        ]
        for node in nodes.values():
            node["readiness"]["interval_ms"] = 50
            node["readiness"]["total_timeout_ms"] = 3_000
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
            self.assertTrue(payload["services_ready"])
            self.assertTrue(payload["browser_completed"])
            self.assertTrue(payload["browser_capture_complete"])
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

    def test_preflight_stop_is_explicitly_rejected_before_process_start(self) -> None:
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

            self.assertEqual({}, payload)
            self.assertEqual(2, code)
            self.assertIn("does not yet emit a preflight-stopped Plan 0.6 Bundle", stderr)
            self.assertFalse(output.exists())
            self.assertEqual([], list(root.glob(".veritrail-*")))
            self.assertTrue(all(_port_is_free(port) for port in ports))

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
