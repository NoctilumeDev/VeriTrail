from __future__ import annotations

import copy
import http.client
import os
import socket
import tempfile
import threading
import unittest
from pathlib import Path

from veritrail.evidence import import_evidence_document
from veritrail.errors import ValidationError
from veritrail.orchestration import (
    RequestRecorder,
    collect_orchestrated_evidence,
    create_static_server,
    prepare_static_target,
)
from veritrail.plan import seal_plan
from veritrail.resources import collect_preflight_evidence
from veritrail.verdict import evaluate

from tests.support import orchestration_plan
from tests.test_browser_evidence import _browser_artifact


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        return int(server.getsockname()[1])


def _write_site(root: Path) -> Path:
    site = root / "site"
    site.mkdir()
    (site / "index.html").write_text("<!doctype html><title>fixture</title>", encoding="utf-8")
    (site / "data.json").write_text('{"status":"ready"}', encoding="utf-8")
    return site


def _runtime_plan(port: int) -> dict:
    plan = orchestration_plan()
    plan["subject"]["source_ref"] = "site"
    plan["target"]["root"] = "site"
    plan["target"]["port"] = port
    plan["preflight"]["ports"] = [{"port": port, "expected": "FREE"}]
    origin = f"http://127.0.0.1:{port}"
    plan["browser"]["start_url"] = f"{origin}/index.html"
    plan["browser"]["allowed_origins"] = [origin]
    plan["preflight"].update(
        sample_count=1,
        sampling_interval_ms=0,
        hard_breach_grace_samples=1,
        available_memory_soft_min_mb=1,
        available_memory_hard_min_mb=1,
        disk_free_hard_min_mb=1,
        collector_rss_hard_max_mb=512,
        observer_rss_delta_soft_max_mb=512,
    )
    return plan


def _request(
    port: int,
    method: str,
    path: str,
    *,
    headers: dict[str, str] | None = None,
) -> tuple[int, bytes, dict[str, str]]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
    request_headers = {"Host": f"127.0.0.1:{port}", **(headers or {})}
    try:
        connection.request(method, path, headers=request_headers)
        response = connection.getresponse()
        body = response.read()
        return response.status, body, {name.lower(): value for name, value in response.getheaders()}
    finally:
        connection.close()


class OrchestrationTests(unittest.TestCase):
    def test_static_server_is_read_only_sanitized_and_rehashes_before_response(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = _write_site(root)
            port = _free_port()
            plan = _runtime_plan(port)
            snapshot = prepare_static_target(plan, root)
            recorder = RequestRecorder()
            server = create_static_server(snapshot, port, recorder)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                status, body, headers = _request(port, "GET", "/data.json?run=secret-value")
                self.assertEqual(200, status)
                self.assertEqual(b'{"status":"ready"}', body)
                self.assertEqual("no-store", headers["cache-control"])
                self.assertIn("default-src 'self'", headers["content-security-policy"])
                self.assertNotIn("access-control-allow-origin", headers)

                status, body, headers = _request(port, "HEAD", "/index.html")
                self.assertEqual(200, status)
                self.assertEqual(b"", body)
                self.assertGreater(int(headers["content-length"]), 0)
                self.assertEqual(405, _request(port, "POST", "/index.html")[0])
                self.assertEqual(
                    416,
                    _request(port, "GET", "/index.html", headers={"Range": "bytes=0-1"})[0],
                )
                self.assertEqual(
                    400,
                    _request(port, "GET", "/index.html", headers={"Host": "example.test"})[0],
                )
                self.assertEqual(
                    400,
                    _request(
                        port,
                        "GET",
                        "/index.html",
                        headers={"Host": f"localhost:{port}"},
                    )[0],
                )
                self.assertEqual(400, _request(port, "GET", "/%2e%2e/secret.txt")[0])
                self.assertEqual(404, _request(port, "GET", "/missing.txt")[0])

                (site / "data.json").write_text('{"status":"other"}', encoding="utf-8")
                self.assertEqual(409, _request(port, "GET", "/data.json")[0])
            finally:
                server.shutdown()
                server.server_close()
                thread.join(2)
            self.assertFalse(thread.is_alive())
            self.assertFalse(any("?" in item["path"] for item in recorder.requests))
            self.assertFalse(any("secret-value" in item["path"] for item in recorder.requests))

    def test_static_snapshot_rejects_hidden_hardlinked_and_over_limit_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = _write_site(root)
            plan = _runtime_plan(_free_port())

            (site / ".hidden.txt").write_text("hidden", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "hidden"):
                prepare_static_target(plan, root)
            (site / ".hidden.txt").unlink()

            linked = site / "linked.txt"
            os.link(site / "data.json", linked)
            try:
                with self.assertRaisesRegex(ValidationError, "hard link"):
                    prepare_static_target(plan, root)
            finally:
                linked.unlink()

            plan["target"]["max_files"] = 1
            with self.assertRaisesRegex(ValidationError, "file-count"):
                prepare_static_target(plan, root)

    def test_orchestrator_records_complete_lifecycle_and_strict_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write_site(root)
            plan = _runtime_plan(_free_port())
            snapshot = prepare_static_target(plan, root)
            plan["baseline"]["fingerprint"] = snapshot.fingerprint
            result = collect_orchestrated_evidence(
                plan,
                root,
                browser_collector=lambda candidate: _browser_artifact(candidate),
            )
            facts = result.orchestration.document["facts"]
            self.assertEqual("COMPLETED", result.execution_status)
            self.assertTrue(facts["lifecycle_complete"])
            self.assertTrue(facts["cleanup_complete"])
            self.assertTrue(facts["port_released"])
            self.assertEqual(
                ["target-start", "target-ready", "browser-capture", "target-cleanup"],
                [event["stage"] for event in facts["events"]],
            )

            preflight = import_evidence_document(
                collect_preflight_evidence(plan, root), "preflight.json"
            )
            report = evaluate(
                seal_plan(plan),
                [preflight, result.orchestration, result.browser],
                result.execution_status,
            )
            self.assertEqual("PASS", report["verdict"])

            tampered = copy.deepcopy(result.orchestration.document)
            tampered["facts"]["request_count"] += 1
            with self.assertRaisesRegex(ValidationError, "does not match requests"):
                import_evidence_document(tampered, "tampered-orchestration.json")

            tampered_events = copy.deepcopy(result.orchestration.document)
            tampered_events["facts"]["events"] = []
            with self.assertRaisesRegex(ValidationError, "lifecycle state machine"):
                import_evidence_document(tampered_events, "tampered-events.json")

            leaked_query = copy.deepcopy(result.orchestration.document)
            leaked_query["facts"]["requests"][0]["path"] += "?token=secret"
            with self.assertRaisesRegex(ValidationError, "sanitized path"):
                import_evidence_document(leaked_query, "leaked-query.json")

            drifted = copy.deepcopy(result.orchestration.document)
            drifted["facts"]["policy_sha256"] = "f" * 64
            drifted_artifact = import_evidence_document(drifted, "drifted-orchestration.json")
            drifted_report = evaluate(
                seal_plan(plan),
                [preflight, drifted_artifact, result.browser],
                "COMPLETED",
            )
            self.assertEqual("INCONCLUSIVE", drifted_report["verdict"])
            self.assertIn(
                "ORCHESTRATION_POLICY_DRIFT",
                {item["code"] for item in drifted_report["contamination"]},
            )

            fingerprint_drift = copy.deepcopy(result.orchestration.document)
            fingerprint_drift["facts"]["static_root_fingerprint"] = "e" * 64
            fingerprint_artifact = import_evidence_document(
                fingerprint_drift, "fingerprint-drift.json"
            )
            fingerprint_report = evaluate(
                seal_plan(plan),
                [preflight, fingerprint_artifact, result.browser],
                "COMPLETED",
            )
            self.assertEqual("INCONCLUSIVE", fingerprint_report["verdict"])
            self.assertIn(
                "STATIC_ROOT_FINGERPRINT_DRIFT",
                {item["code"] for item in fingerprint_report["contamination"]},
            )

    def test_bind_failure_is_contained_and_does_not_claim_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write_site(root)
            port = _free_port()
            plan = _runtime_plan(port)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as blocker:
                blocker.bind(("127.0.0.1", port))
                blocker.listen(1)
                result = collect_orchestrated_evidence(
                    plan,
                    root,
                    browser_collector=lambda candidate: _browser_artifact(candidate),
                )
            facts = result.orchestration.document["facts"]
            self.assertEqual("ERROR", result.execution_status)
            self.assertFalse(facts["server_started"])
            self.assertFalse(facts["lifecycle_complete"])
            self.assertFalse(facts["port_released"])
            self.assertIn(
                "target-start", {item["stage"] for item in facts["collection_errors"]}
            )


if __name__ == "__main__":
    unittest.main()
