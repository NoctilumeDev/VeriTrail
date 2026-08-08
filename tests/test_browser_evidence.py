from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from veritrail.browser import sanitize_url
from veritrail.canonical import sha256_json
from veritrail.evidence import (
    EvidenceAttachment,
    create_attachment,
    import_evidence_document,
    import_evidence_files,
    verify_imported_evidence,
)
from veritrail.errors import ValidationError
from veritrail.plan import seal_plan
from veritrail.reporting import create_bundle
from veritrail.resources import collect_preflight_evidence
from veritrail.verdict import evaluate

from tests.support import browser_plan


PNG_BYTES = b"\x89PNG\r\n\x1a\nsynthetic-test-png"


def _safe_runtime_plan() -> dict:
    plan = browser_plan()
    plan["preflight"].update(
        sample_count=1,
        sampling_interval_ms=0,
        hard_breach_grace_samples=1,
        available_memory_soft_min_mb=1,
        available_memory_hard_min_mb=1,
        disk_free_hard_min_mb=1,
        collector_rss_hard_max_mb=512,
        observer_rss_delta_soft_max_mb=512,
        ports=[],
    )
    return plan


def _browser_artifact(plan: dict, *, console_error: bool = False):
    attachments = []
    screenshots = []
    viewport_runs = []
    steps = []
    network = []
    for index, viewport in enumerate(plan["browser"]["viewports"], start=1):
        path = f"attachments/browser/{viewport['name']}/001-ready.png"
        attachment = create_attachment(
            path=path,
            content=PNG_BYTES + bytes([index]),
            media_type="image/png",
            logical_name=f"{viewport['name']}-ready",
        )
        attachments.append(attachment)
        screenshots.append(
            {
                "name": "ready",
                "viewport": viewport["name"],
                "step_id": "capture-ready",
                "path": attachment.path,
                "sha256": attachment.sha256,
                "size": attachment.size,
                "media_type": attachment.media_type,
            }
        )
        viewport_runs.append(
            {
                "name": viewport["name"],
                "width": viewport["width"],
                "height": viewport["height"],
                "is_mobile": viewport["is_mobile"],
                "started_at": "2026-08-09T00:00:00Z",
                "ended_at": "2026-08-09T00:00:01Z",
                "status": "PASSED",
                "horizontal_overflow_px": 0,
                "step_count": 1,
                "network_request_count": 1,
            }
        )
        steps.append(
            {
                "viewport": viewport["name"],
                "step_id": "capture-ready",
                "action": "screenshot",
                "started_at": "2026-08-09T00:00:00Z",
                "ended_at": "2026-08-09T00:00:01Z",
                "elapsed_ms": 1.0,
                "status": "PASSED",
                "error_type": None,
                "error": None,
            }
        )
        network.append(
            {
                "sequence": index,
                "captured_at": "2026-08-09T00:00:00Z",
                "viewport": viewport["name"],
                "method": "GET",
                "url": "http://localhost:18765/data.json?run=%5BREDACTED%5D",
                "resource_type": "fetch",
                "status": 200,
                "finished": True,
                "failure": None,
                "redirected_from": None,
            }
        )
    console = (
        [
            {
                "captured_at": "2026-08-09T00:00:00Z",
                "viewport": "desktop",
                "level": "error",
                "text": "synthetic failure",
            }
        ]
        if console_error
        else []
    )
    facts = {
        "collector_version": "browser-playwright/0.1",
        "policy_sha256": sha256_json(plan["browser"]),
        "playwright_version": "1.62.0",
        "browser_engine": "chromium",
        "browser_version": "145.0.0.0",
        "headless": plan["browser"]["headless"],
        "start_url": plan["browser"]["start_url"],
        "allowed_origins": plan["browser"]["allowed_origins"],
        "started_at": "2026-08-09T00:00:00Z",
        "ended_at": "2026-08-09T00:00:02Z",
        "capture_complete": True,
        "all_steps_passed": True,
        "cleanup_complete": True,
        "viewport_runs": viewport_runs,
        "viewport_count": len(viewport_runs),
        "steps": steps,
        "console": console,
        "page_errors": [],
        "network": network,
        "screenshots": screenshots,
        "screenshot_count": len(screenshots),
        "unexpected_console_error_count": len(console),
        "page_error_count": 0,
        "failed_request_count": 0,
        "unexpected_http_error_count": 0,
        "duplicate_write_request_groups": [],
        "duplicate_write_request_group_count": 0,
        "horizontal_overflow_viewport_count": 0,
        "collection_errors": [],
    }
    document = {
        "schema_version": "0.1",
        "evidence_type": "browser.session",
        "source": "browser-unit-test",
        "captured_at": "2026-08-09T00:00:00Z",
        "facts": facts,
        "observed_variables": {
            "browser_engine": "chromium",
            "browser_headless": plan["browser"]["headless"],
            "viewport_profile_count": len(viewport_runs),
        },
        "metadata": {
            "network_scope": "loopback-only",
            "request_headers_persisted": False,
            "response_headers_persisted": False,
            "request_bodies_persisted": False,
            "response_bodies_persisted": False,
            "query_values_redacted": True,
            "contexts_parallel": False,
            "maximum_live_pages": 1,
        },
    }
    return import_evidence_document(
        document, "browser.json", attachments=tuple(attachments)
    )


class BrowserEvidenceTests(unittest.TestCase):
    def test_url_sanitizer_removes_query_values_userinfo_and_loopback_ip(self) -> None:
        value = sanitize_url(
            "http://demo:secret@127.0.0.1:18765/data.json?token=secret&mode=test#part"
        )
        self.assertEqual(
            "http://localhost:18765/data.json?token=%5BREDACTED%5D&mode=%5BREDACTED%5D",
            value,
        )
        self.assertNotIn("secret", value)
        self.assertNotIn("demo", value)

    def test_browser_attachment_is_hashed_written_and_manifested(self) -> None:
        plan = _safe_runtime_plan()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            preflight = import_evidence_document(
                collect_preflight_evidence(plan, root), "preflight.json"
            )
            browser = _browser_artifact(plan)
            output = root / "bundle"
            report = create_bundle(
                plan=seal_plan(plan),
                evidence_paths=[],
                output=output,
                run_id="m2-browser-bundle",
                execution_status="COMPLETED",
                generated_evidence=[preflight, browser],
            )
            self.assertEqual("PASS", report["verdict"])
            browser_entry = next(
                item for item in report["evidence"] if item["evidence_type"] == "browser.session"
            )
            self.assertEqual(2, len(browser_entry["attachments"]))
            for item in browser_entry["attachments"]:
                path = output / Path(item["path"])
                self.assertTrue(path.is_file())
                self.assertEqual(item["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            manifest = json.loads((output / "bundle-manifest.json").read_text(encoding="utf-8"))
            manifest_paths = {item["path"] for item in manifest["files"]}
            self.assertTrue({item["path"] for item in browser_entry["attachments"]} <= manifest_paths)

    def test_attachment_mutation_and_path_traversal_are_rejected(self) -> None:
        plan = _safe_runtime_plan()
        artifact = _browser_artifact(plan)
        original = artifact.attachments[0]
        mutated = EvidenceAttachment(
            path=original.path,
            content=original.content + b"changed",
            sha256=original.sha256,
            size=original.size,
            media_type=original.media_type,
            logical_name=original.logical_name,
        )
        object.__setattr__(artifact, "attachments", (mutated, *artifact.attachments[1:]))
        with self.assertRaisesRegex(ValidationError, "changed after hashing"):
            verify_imported_evidence(artifact)

        with self.assertRaisesRegex(ValidationError, "stay under attachments"):
            create_attachment(
                path="attachments/../escape.png",
                content=PNG_BYTES,
                media_type="image/png",
                logical_name="escape",
            )

    def test_external_browser_json_cannot_claim_missing_screenshots_or_network_bodies(self) -> None:
        plan = _safe_runtime_plan()
        artifact = _browser_artifact(plan)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "browser.json"
            path.write_text(
                json.dumps(artifact.document, ensure_ascii=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValidationError, "references do not match"):
                import_evidence_files([path], 5_242_880)

        unsafe_document = copy.deepcopy(artifact.document)
        unsafe_document["facts"]["network"][0]["response_body"] = "must not persist"
        with self.assertRaisesRegex(ValidationError, "exact supported fields"):
            import_evidence_document(unsafe_document, "unsafe-browser.json")

    def test_browser_policy_drift_is_inconclusive_and_console_error_fails(self) -> None:
        plan = _safe_runtime_plan()
        with tempfile.TemporaryDirectory() as directory:
            preflight = import_evidence_document(
                collect_preflight_evidence(plan, Path(directory)), "preflight.json"
            )
        clean = _browser_artifact(plan)
        self.assertEqual(
            "PASS", evaluate(seal_plan(plan), [preflight, clean], "COMPLETED")["verdict"]
        )

        drifted_document = copy.deepcopy(clean.document)
        drifted_document["facts"]["policy_sha256"] = "f" * 64
        drifted = import_evidence_document(
            drifted_document,
            "drifted-browser.json",
            attachments=clean.attachments,
        )
        drifted_result = evaluate(seal_plan(plan), [preflight, drifted], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", drifted_result["verdict"])
        self.assertIn("BROWSER_POLICY_DRIFT", {item["code"] for item in drifted_result["contamination"]})

        failed = _browser_artifact(plan, console_error=True)
        self.assertEqual(
            "FAIL", evaluate(seal_plan(plan), [preflight, failed], "COMPLETED")["verdict"]
        )


if __name__ == "__main__":
    unittest.main()
