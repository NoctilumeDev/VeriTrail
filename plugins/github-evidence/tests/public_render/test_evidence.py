from __future__ import annotations

import copy
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from veritrail.evidence import import_evidence_document
from veritrail_github.errors import CollectionError, ContractError
from veritrail_github.public_render_browser import (
    BrowserNavigationSnapshot,
    BrowserSessionSnapshot,
    FixedScopeSnapshot,
)
from veritrail_github.public_render_collector import (
    PublicRenderCollector,
    assemble_public_render_artifact,
)
from veritrail_github.public_render_conformance import (
    verify_public_render_evidence,
)
from veritrail_github.public_render_content import ContentSample, ContentWindow
from veritrail_github.public_render_contracts import (
    DEFAULT_RENDER_POLICY,
    derive_public_render_request,
)
from veritrail_github.publisher import publish_evidence

from public_render.support import public_render_plan


def _navigation(status: int = 200) -> BrowserNavigationSnapshot:
    coordinate = {
        "origin": "https://github.com",
        "host": "github.com",
        "path": "/NoctilumeDev/VeriTrail/blob/" + "a" * 40 + "/README.md",
        "query_present": False,
        "fragment_present": False,
    }
    return BrowserNavigationSnapshot(
        requested_url=coordinate,
        redirect_chain=(),
        final_url=coordinate,
        top_level_http_status=status,
        media_type="text/html",
    )


def _snapshot(
    *,
    status: int = 200,
    scope_count: int = 1,
    browser_version: str = "151.0",
    network: tuple[dict[str, object], ...] = (),
    cleanup_errors: tuple[str, ...] = (),
) -> BrowserSessionSnapshot:
    return BrowserSessionSnapshot(
        runtime={
            "playwright_version": "1.62.0",
            "browser_engine": "CHROMIUM",
            "browser_distribution": "BUNDLED_MATCHING",
            "browser_version": browser_version,
        },
        initial_state={
            "kind": "ANONYMOUS_FRESH_CONTEXT",
            "cookies": 0,
            "origins": 0,
        },
        post_navigation_state={
            "cookie_count": 1,
            "origin_count": 0,
            "secure_cookie_count": 1,
            "http_only_cookie_count": 1,
            "session_cookie_count": 1,
            "same_site_counts": {
                "Strict": 0,
                "Lax": 1,
                "None": 0,
                "Unknown": 0,
            },
        },
        navigation=_navigation(status),
        scope=FixedScopeSnapshot(
            selector="article.markdown-body",
            count=scope_count,
            usable=scope_count == 1,
        ),
        response_bodies={
            "total_response_body_bytes": 100,
            "main_document_response_body_bytes": 100,
            "delivered_response_body_bytes": 100,
            "completed_responses": 1,
            "closed_streams": 1,
            "active_streams": 0,
            "request_stage_pauses": 1,
            "response_error_reason_counts": {},
            "failure": None,
        },
        main_frame_responses=(),
        network=network,
        runtime_events={
            "console_categories": {"error": 2},
            "page_error_count": 0,
            "request_failure_categories": {"ERR_BLOCKED_BY_CLIENT": 2},
        },
        conflicts=(),
        cleanup_errors=cleanup_errors,
    )


def _content_window(*, stable: bool = True) -> ContentWindow:
    digests = ("b" * 64,) * 3 if stable else ("b" * 64, "c" * 64, "b" * 64)
    samples = tuple(
        ContentSample(
            digest=digest,
            facts={
                "rendered_text_signature": {
                    "sha256": "d" * 64,
                    "utf8_byte_length": 12,
                    "line_count": 1,
                }
            },
            truncations=(),
            conflicts=(),
        )
        for digest in digests
    )
    return ContentWindow(
        samples_stable=stable,
        sample_digests=digests,
        samples=samples,
        navigation_conflicts=(),
    )


class _FakeBrowserSession:
    def __init__(self, snapshot: BrowserSessionSnapshot) -> None:
        self._snapshot = snapshot
        self.calls: list[str] = []

    def open(self):
        self.calls.append("open")
        return self

    def navigate(self):
        self.calls.append("navigate")
        return self._snapshot.navigation

    def assert_healthy(self) -> None:
        self.calls.append("assert_healthy")

    def close(self) -> None:
        self.calls.append("close")

    def snapshot(self) -> BrowserSessionSnapshot:
        self.calls.append("snapshot")
        return self._snapshot


def _assemble(
    *,
    request_id: str = "render-request-001",
    session_id: str = "render-session-001",
    status: int = 200,
    stable: bool = True,
    network: tuple[dict[str, object], ...] = (),
    cleanup_errors: tuple[str, ...] = (),
):
    plan = public_render_plan()
    request = derive_public_render_request(
        plan, "github-public-render", request_id
    )
    artifact = assemble_public_render_artifact(
        plan,
        request,
        session_id=session_id,
        started_at="2026-09-06T00:00:00Z",
        completed_at="2026-09-06T00:00:01Z",
        elapsed_ms=1000,
        browser_snapshot=_snapshot(
            status=status, network=network, cleanup_errors=cleanup_errors
        ),
        document=None,
        content_window=_content_window(stable=stable),
        phase_observations=[
            {
                "sequence": 1,
                "phase": "open",
                "outcome": "OBSERVED",
                "elapsed_ms_monotonic": 1,
            },
            {
                "sequence": 2,
                "phase": "navigation",
                "outcome": "OBSERVED",
                "elapsed_ms_monotonic": 2,
            },
            {
                "sequence": 3,
                "phase": "cleanup",
                "outcome": "OBSERVED",
                "elapsed_ms_monotonic": 1,
            },
        ],
        errors=[],
    )
    return plan, request, artifact


class PublicRenderEvidenceTests(unittest.TestCase):
    def test_complete_evidence_separates_fact_and_artifact_identity(self) -> None:
        plan, request, first = _assemble()
        _plan, _request, second = _assemble(
            request_id="render-request-002", session_id="render-session-002"
        )
        first_observation = first.document["metadata"]["veritrail_observation"]
        second_observation = second.document["metadata"]["veritrail_observation"]

        self.assertEqual(first_observation["coverage"], "COMPLETE")
        self.assertEqual(
            first_observation["facts_digest"], second_observation["facts_digest"]
        )
        self.assertNotEqual(first.sha256, second.sha256)
        verify_public_render_evidence(plan, request, first)

    def test_policy_and_browser_versions_do_not_pollute_fact_identity(self) -> None:
        plan = public_render_plan()
        first_request = derive_public_render_request(
            plan, "github-public-render", "render-policy-001"
        )
        policy = dict(DEFAULT_RENDER_POLICY)
        policy["max_requests"] = 256
        second_request = derive_public_render_request(
            plan,
            "github-public-render",
            "render-policy-002",
            render_policy=policy,
        )
        arguments = {
            "started_at": "2026-09-06T00:00:00Z",
            "completed_at": "2026-09-06T00:00:01Z",
            "elapsed_ms": 1000,
            "document": None,
            "content_window": _content_window(),
            "phase_observations": [
                {
                    "sequence": 1,
                    "phase": "open",
                    "outcome": "OBSERVED",
                    "elapsed_ms_monotonic": 1,
                },
                {
                    "sequence": 2,
                    "phase": "navigation",
                    "outcome": "OBSERVED",
                    "elapsed_ms_monotonic": 1,
                },
                {
                    "sequence": 3,
                    "phase": "cleanup",
                    "outcome": "OBSERVED",
                    "elapsed_ms_monotonic": 1,
                },
            ],
            "errors": [],
        }
        first = assemble_public_render_artifact(
            plan,
            first_request,
            session_id="render-policy-session-001",
            browser_snapshot=_snapshot(browser_version="151.0"),
            **arguments,
        )
        second = assemble_public_render_artifact(
            plan,
            second_request,
            session_id="render-policy-session-002",
            browser_snapshot=_snapshot(browser_version="152.0"),
            **arguments,
        )

        first_observation = first.document["metadata"]["veritrail_observation"]
        second_observation = second.document["metadata"]["veritrail_observation"]
        self.assertEqual(
            first_observation["facts_digest"], second_observation["facts_digest"]
        )
        self.assertNotEqual(first.sha256, second.sha256)

    def test_http_500_is_a_complete_navigation_fact_not_a_verdict(self) -> None:
        plan = public_render_plan(projections=["navigation.identity"])
        request = derive_public_render_request(
            plan, "github-public-render", "render-http-500"
        )
        artifact = assemble_public_render_artifact(
            plan,
            request,
            session_id="render-session-http-500",
            started_at="2026-09-06T00:00:00Z",
            completed_at="2026-09-06T00:00:01Z",
            elapsed_ms=1000,
            browser_snapshot=_snapshot(status=500, scope_count=0),
            document=None,
            content_window=None,
            phase_observations=[
                {
                    "sequence": 1,
                    "phase": "open",
                    "outcome": "OBSERVED",
                    "elapsed_ms_monotonic": 1,
                },
                {
                    "sequence": 2,
                    "phase": "navigation",
                    "outcome": "OBSERVED",
                    "elapsed_ms_monotonic": 1,
                },
                {
                    "sequence": 3,
                    "phase": "cleanup",
                    "outcome": "OBSERVED",
                    "elapsed_ms_monotonic": 1,
                }
            ],
            errors=[],
        )

        self.assertEqual(
            artifact.document["metadata"]["veritrail_observation"]["coverage"],
            "COMPLETE",
        )
        self.assertEqual(artifact.document["facts"]["navigation"]["top_level_http_status"], 500)
        self.assertNotIn("passed", repr(artifact.document).casefold())

    def test_unstable_content_is_partial_without_selecting_a_sample(self) -> None:
        _plan, _request, artifact = _assemble(stable=False)
        observation = artifact.document["metadata"]["veritrail_observation"]
        window = artifact.document["facts"]["content"]["window"]

        self.assertEqual(observation["coverage"], "PARTIAL")
        self.assertFalse(window["samples_stable"])
        self.assertIsNone(window["stable_facts"])
        self.assertEqual(len(window["sample_digests"]), 3)

    def test_unexpected_read_host_is_partial_but_telemetry_write_is_not(self) -> None:
        write = {
            "sequence": 1,
            "method": "POST",
            "main_document": False,
            "allowed": False,
            "reasons": ["METHOD_NOT_ALLOWED"],
            "affects_coverage": False,
            "url": {"host": "github.com"},
        }
        read = {
            "sequence": 2,
            "method": "GET",
            "main_document": False,
            "allowed": False,
            "reasons": ["HOST_NOT_ALLOWED"],
            "affects_coverage": True,
            "url": {"host": "example.com"},
        }
        _plan, _request, write_only = _assemble(network=(write,))
        _plan, _request, with_read = _assemble(network=(write, read))

        self.assertEqual(
            write_only.document["metadata"]["veritrail_observation"]["coverage"],
            "COMPLETE",
        )
        self.assertEqual(
            with_read.document["metadata"]["veritrail_observation"]["coverage"],
            "PARTIAL",
        )

    def test_cleanup_failure_forces_error_without_erasing_facts(self) -> None:
        _plan, _request, artifact = _assemble(
            cleanup_errors=("browser:close-failed",)
        )
        observation = artifact.document["metadata"]["veritrail_observation"]

        self.assertEqual(observation["coverage"], "ERROR")
        self.assertIsNotNone(artifact.document["facts"]["navigation"])

    def test_conformance_rejects_forged_coverage(self) -> None:
        plan, request, artifact = _assemble(stable=False)
        document = copy.deepcopy(artifact.document)
        document["metadata"]["veritrail_observation"]["coverage"] = "COMPLETE"
        forged = import_evidence_document(document, artifact.input_name)

        with self.assertRaisesRegex(ContractError, "coverage"):
            verify_public_render_evidence(plan, request, forged)

    def test_standard_publisher_is_create_new_for_p2_evidence(self) -> None:
        _plan, _request, artifact = _assemble()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "render-evidence.json"
            publish_evidence(output, artifact)
            retained = output.read_bytes()

            self.assertTrue(retained.endswith(b"\n"))
            with self.assertRaisesRegex(CollectionError, "refusing to overwrite"):
                publish_evidence(output, artifact)

    def test_invalid_request_never_creates_browser_session(self) -> None:
        plan = public_render_plan()
        request = derive_public_render_request(
            plan, "github-public-render", "render-invalid"
        )
        request["render_policy"] = dict(DEFAULT_RENDER_POLICY)
        request["render_policy"]["max_requests"] = 1
        created: list[object] = []
        collector = PublicRenderCollector(
            browser_session_factory=lambda value: created.append(value)
        )

        with self.assertRaises(ContractError):
            collector.collect(plan, request)

        self.assertEqual(created, [])

    def test_runtime_failure_produces_error_evidence_without_raw_message(self) -> None:
        plan = public_render_plan()
        request = derive_public_render_request(
            plan, "github-public-render", "render-runtime-error"
        )
        collector = PublicRenderCollector(
            clock=lambda: datetime(2026, 9, 6, tzinfo=timezone.utc),
            session_id_factory=lambda: "render-session-runtime-error",
            browser_session_factory=lambda _request: (_ for _ in ()).throw(
                RuntimeError("secret machine path")
            ),
        )

        result = collector.collect(plan, request)
        observation = result.artifact.document["metadata"]["veritrail_observation"]

        self.assertEqual(observation["coverage"], "ERROR")
        self.assertNotIn("secret machine path", repr(result.artifact.document))

    def test_collector_runs_one_serial_navigation_session(self) -> None:
        plan = public_render_plan(projections=["navigation.identity"])
        request = derive_public_render_request(
            plan, "github-public-render", "render-serial"
        )
        session = _FakeBrowserSession(_snapshot())
        collector = PublicRenderCollector(
            clock=lambda: datetime(2026, 9, 6, tzinfo=timezone.utc),
            session_id_factory=lambda: "render-session-serial",
            browser_session_factory=lambda _request: session,
        )

        result = collector.collect(plan, request)

        self.assertEqual(
            session.calls,
            ["open", "navigate", "assert_healthy", "close", "snapshot"],
        )
        self.assertEqual(
            result.artifact.document["metadata"]["veritrail_observation"][
                "coverage"
            ],
            "COMPLETE",
        )


if __name__ == "__main__":
    unittest.main()
