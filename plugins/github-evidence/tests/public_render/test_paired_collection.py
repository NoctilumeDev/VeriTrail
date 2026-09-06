from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import fields
from pathlib import Path

from veritrail.acceptance_plan import seal_acceptance_plan

from veritrail_github.collector import GitHubCollector
from veritrail_github.contracts import derive_observation_request
from veritrail_github.errors import ContractError
from veritrail_github.paired_collection import (
    PairedCollectionCoordinator,
    PairedCollectionResult,
)
from veritrail_github.public_render_browser import (
    BrowserNavigationSnapshot,
    BrowserSessionSnapshot,
)
from veritrail_github.public_render_collector import PublicRenderCollector
from veritrail_github.public_render_contracts import derive_public_render_request

from support import TARGET_SHA, base_transport


def _paired_plan() -> dict[str, object]:
    return seal_acceptance_plan(
        {
            "plan_kind": "ACCEPTANCE",
            "schema_version": "0.1",
            "plan_id": "github-paired-fixture",
            "version": 1,
            "subject": {
                "id": "veritrail",
                "version": TARGET_SHA,
                "source_ref": "github:noctilumedev/veritrail",
            },
            "question": (
                "Do the two retained observations satisfy this declared delivery?"
            ),
            "governance": {
                "claim_owner_ref": "human:owner",
                "drafter_ref": "test:paired-fixture",
                "seal_authority_ref": "human:owner",
                "seal_decision": "CONFIRMED",
            },
            "observation_specs": [
                {
                    "id": "github-api",
                    "contract": {
                        "id": "github-observation-request",
                        "version": "0.1",
                    },
                    "evidence_type": "platform.github.api.snapshot",
                    "coordinates": {
                        "owner": "NoctilumeDev",
                        "repository": "VeriTrail",
                        "target_commit_sha": TARGET_SHA,
                        "branch": "main",
                    },
                    "projections": ["commit.identity", "repository.identity"],
                    "canonicalization_profile": "veritrail-json-c14n/1",
                },
                {
                    "id": "github-public-render",
                    "contract": {
                        "id": "github-public-render-request",
                        "version": "0.1",
                    },
                    "evidence_type": "platform.github.public-render",
                    "coordinates": {
                        "owner": "NoctilumeDev",
                        "repository": "VeriTrail",
                        "target_kind": "GITHUB_MARKDOWN_FILE",
                        "target_commit_sha": TARGET_SHA,
                        "repository_path": "README.md",
                        "viewport_profile": "DESKTOP_1365X768",
                    },
                    "projections": ["navigation.identity"],
                    "canonicalization_profile": "veritrail-json-c14n/1",
                },
            ],
            "evidence_requirements": [
                {
                    "id": "github-api-evidence",
                    "observation_spec_id": "github-api",
                    "cardinality": "EXACTLY_ONE",
                },
                {
                    "id": "github-render-evidence",
                    "observation_spec_id": "github-public-render",
                    "cardinality": "EXACTLY_ONE",
                },
            ],
            "sufficiency_rules": [
                {
                    "id": "api-coverage-complete",
                    "left": {
                        "requirement_id": "github-api-evidence",
                        "path": "/metadata/veritrail_observation/coverage",
                    },
                    "operator": "eq",
                    "right": "COMPLETE",
                },
                {
                    "id": "render-coverage-complete",
                    "left": {
                        "requirement_id": "github-render-evidence",
                        "path": "/metadata/veritrail_observation/coverage",
                    },
                    "operator": "eq",
                    "right": "COMPLETE",
                },
            ],
            "integrity_rules": [],
            "assertions": [
                {
                    "id": "api-coordinate-retained",
                    "severity": "HARD",
                    "left": {
                        "requirement_id": "github-api-evidence",
                        "path": "/facts/commit/sha",
                    },
                    "operator": "eq",
                    "right": TARGET_SHA,
                }
            ],
            "resource_budget": {
                "network_requests": 512,
                "max_elapsed_ms": 45000,
            },
            "change_scope": {
                "level": "L3_SYSTEM",
                "owner": "github-evidence-plugin",
                "consumers": ["acceptance-core"],
            },
            "reproduction_steps": ["Run the paired fixture collector."],
            "cleanup_steps": ["Remove both generated Evidence files."],
        }
    )


def _requests(plan):
    return (
        derive_observation_request(plan, "github-api", "paired-api-001"),
        derive_public_render_request(
            plan, "github-public-render", "paired-render-001"
        ),
    )


def _navigation() -> BrowserNavigationSnapshot:
    url = {
        "origin": "https://github.com",
        "host": "github.com",
        "path": f"/NoctilumeDev/VeriTrail/blob/{TARGET_SHA}/README.md",
        "query_present": False,
        "fragment_present": False,
    }
    return BrowserNavigationSnapshot(
        requested_url=url,
        redirect_chain=(),
        final_url=url,
        top_level_http_status=200,
        media_type="text/html",
    )


def _browser_snapshot() -> BrowserSessionSnapshot:
    return BrowserSessionSnapshot(
        runtime={
            "playwright_version": "1.62.0",
            "browser_engine": "CHROMIUM",
            "browser_distribution": "BUNDLED_MATCHING",
            "browser_version": "151.0",
        },
        initial_state={
            "kind": "ANONYMOUS_FRESH_CONTEXT",
            "cookies": 0,
            "origins": 0,
        },
        post_navigation_state={
            "cookie_count": 0,
            "origin_count": 0,
            "secure_cookie_count": 0,
            "http_only_cookie_count": 0,
            "session_cookie_count": 0,
            "same_site_counts": {
                "Strict": 0,
                "Lax": 0,
                "None": 0,
                "Unknown": 0,
            },
        },
        navigation=_navigation(),
        scope=None,
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
        network=(),
        runtime_events={
            "console_categories": {},
            "page_error_count": 0,
            "request_failure_categories": {},
        },
        conflicts=(),
        cleanup_errors=(),
    )


class _FakeBrowserSession:
    def __init__(self, *, events: list[str] | None = None) -> None:
        self._snapshot = _browser_snapshot()
        self._events = events

    def open(self):
        if self._events is not None:
            self._events.append("render-open")
        return self

    def navigate(self):
        return self._snapshot.navigation

    def assert_healthy(self) -> None:
        return None

    def close(self) -> None:
        return None

    def snapshot(self) -> BrowserSessionSnapshot:
        return self._snapshot


class _RecordingCollector:
    def __init__(self, inner, events: list[str], label: str) -> None:
        self._inner = inner
        self._events = events
        self._label = label

    def collect(self, plan, request):
        self._events.append(f"{self._label}-collect")
        return self._inner.collect(plan, request)


class _FailingCollector:
    def collect(self, plan, request):
        raise RuntimeError("raw secret must never be retained")


class PairedCollectionTests(unittest.TestCase):
    def _coordinator(
        self,
        *,
        session_id: str = "paired-session-001",
        session_id_factory=None,
        events: list[str] | None = None,
        api_factory=None,
        render_factory=None,
    ) -> PairedCollectionCoordinator:
        observed = events if events is not None else []

        def default_api_factory(session_factory):
            observed.append("api-factory")
            return _RecordingCollector(
                GitHubCollector(
                    base_transport(), session_id_factory=session_factory
                ),
                observed,
                "api",
            )

        def default_render_factory(session_factory):
            observed.append("render-factory")
            return _RecordingCollector(
                PublicRenderCollector(
                    session_id_factory=session_factory,
                    browser_session_factory=lambda _request: _FakeBrowserSession(
                        events=observed
                    ),
                ),
                observed,
                "render",
            )

        return PairedCollectionCoordinator(
            api_collector_factory=api_factory or default_api_factory,
            render_collector_factory=render_factory or default_render_factory,
            session_id_factory=session_id_factory or (lambda: session_id),
        )

    def test_invalid_requests_create_no_session_collectors_or_outputs(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        api_request["request_id"] = "tampered-api"
        render_request["request_id"] = "tampered-render"
        calls: list[str] = []
        coordinator = PairedCollectionCoordinator(
            api_collector_factory=lambda _session: calls.append("api"),
            render_collector_factory=lambda _session: calls.append("render"),
            session_id_factory=lambda: calls.append("session") or "paired-session",
        )
        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"
            with self.assertRaises(ContractError) as raised:
                coordinator.collect_and_publish(
                    plan,
                    api_request,
                    render_request,
                    api_output_path=api_path,
                    render_output_path=render_path,
                )
            self.assertIn("github-api:", str(raised.exception))
            self.assertIn("github-public-render:", str(raised.exception))
            self.assertEqual(calls, [])
            self.assertFalse(api_path.exists())
            self.assertFalse(render_path.exists())

    def test_output_conflicts_fail_before_session_creation(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        sessions: list[str] = []
        coordinator = self._coordinator(
            session_id_factory=lambda: sessions.append("created") or "x"
        )
        with tempfile.TemporaryDirectory() as temporary:
            shared = Path(temporary) / "shared.json"
            with self.assertRaises(ContractError):
                coordinator.collect_and_publish(
                    plan,
                    api_request,
                    render_request,
                    api_output_path=shared,
                    render_output_path=shared,
                )
            shared.write_text("existing", encoding="utf-8")
            with self.assertRaises(ContractError):
                coordinator.collect_and_publish(
                    plan,
                    api_request,
                    render_request,
                    api_output_path=shared,
                    render_output_path=Path(temporary) / "render.json",
                )
        self.assertEqual(sessions, [])

    def test_invalid_internal_session_stops_before_collector_creation(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        factories: list[str] = []
        coordinator = PairedCollectionCoordinator(
            api_collector_factory=lambda _session: factories.append("api"),
            render_collector_factory=lambda _session: factories.append("render"),
            session_id_factory=lambda: "invalid session",
        )
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ContractError):
                coordinator.collect_and_publish(
                    plan,
                    api_request,
                    render_request,
                    api_output_path=Path(temporary) / "api.json",
                    render_output_path=Path(temporary) / "render.json",
                )
        self.assertEqual(factories, [])

    def test_session_factory_failure_is_safe_and_creates_no_collectors(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        factories: list[str] = []

        def failed_session():
            raise RuntimeError("secret session detail")

        coordinator = PairedCollectionCoordinator(
            api_collector_factory=lambda _session: factories.append("api"),
            render_collector_factory=lambda _session: factories.append("render"),
            session_id_factory=failed_session,
        )
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ContractError) as raised:
                coordinator.collect_and_publish(
                    plan,
                    api_request,
                    render_request,
                    api_output_path=Path(temporary) / "api.json",
                    render_output_path=Path(temporary) / "render.json",
                )
        self.assertNotIn("secret", str(raised.exception))
        self.assertEqual(factories, [])

    def test_fixed_order_publishes_api_before_render_starts(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        events: list[str] = []
        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"

            def render_factory(session_factory):
                events.append("render-factory")
                self.assertTrue(api_path.exists())
                return _RecordingCollector(
                    PublicRenderCollector(
                        session_id_factory=session_factory,
                        browser_session_factory=lambda _request: _FakeBrowserSession(
                            events=events
                        ),
                    ),
                    events,
                    "render",
                )

            result = self._coordinator(
                events=events, render_factory=render_factory
            ).collect_and_publish(
                plan,
                api_request,
                render_request,
                api_output_path=api_path,
                render_output_path=render_path,
            )
            self.assertEqual(
                events,
                [
                    "api-factory",
                    "api-collect",
                    "render-factory",
                    "render-collect",
                    "render-open",
                ],
            )
            self.assertEqual(
                result.collection_order,
                ("github-api", "github-public-render"),
            )
            self.assertEqual(result.api.state, "PUBLISHED")
            self.assertEqual(result.render.state, "PUBLISHED")

    def test_two_artifacts_share_session_but_keep_separate_request_seals(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"
            coordinator = self._coordinator(session_id="paired-shared-session")
            result = coordinator.collect_and_publish(
                plan,
                api_request,
                render_request,
                api_output_path=api_path,
                render_output_path=render_path,
            )
            api_document = json.loads(api_path.read_text(encoding="utf-8"))
            render_document = json.loads(render_path.read_text(encoding="utf-8"))
            api_observation = api_document["metadata"]["veritrail_observation"]
            render_observation = render_document["metadata"]["veritrail_observation"]
            self.assertEqual(
                api_observation["collection_session_id"], "paired-shared-session"
            )
            self.assertEqual(
                render_observation["collection_session_id"], "paired-shared-session"
            )
            self.assertEqual(api_observation["plan_digest"], plan["seal"]["digest"])
            self.assertEqual(
                render_observation["plan_digest"], plan["seal"]["digest"]
            )
            self.assertNotEqual(
                api_observation["request_seal_digest"],
                render_observation["request_seal_digest"],
            )
            self.assertEqual(result.api.artifact_path, api_path)
            self.assertEqual(result.render.artifact_path, render_path)

    def test_api_collection_exception_does_not_prevent_render_publish(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"
            result = self._coordinator(
                api_factory=lambda _session: _FailingCollector()
            ).collect_and_publish(
                plan,
                api_request,
                render_request,
                api_output_path=api_path,
                render_output_path=render_path,
            )
            self.assertEqual(result.api.state, "MISSING")
            self.assertEqual(result.api.error_code, "COLLECTION_ERROR")
            self.assertIsNone(result.api.artifact_path)
            self.assertTrue(render_path.exists())
            self.assertEqual(result.render.state, "PUBLISHED")
            self.assertNotIn("secret", repr(result))

    def test_api_error_evidence_still_allows_render(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)

        def error_api_factory(session_factory):
            return GitHubCollector(
                base_transport(commit_sha="b" * 40),
                session_id_factory=session_factory,
            )

        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"
            result = self._coordinator(
                api_factory=error_api_factory
            ).collect_and_publish(
                plan,
                api_request,
                render_request,
                api_output_path=api_path,
                render_output_path=render_path,
            )
            self.assertEqual(result.api.state, "PUBLISHED")
            self.assertEqual(result.api.coverage, "ERROR")
            self.assertEqual(result.render.state, "PUBLISHED")
            self.assertTrue(api_path.exists())
            self.assertTrue(render_path.exists())

    def test_api_artifact_is_retained_when_render_collection_fails(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"
            result = self._coordinator(
                render_factory=lambda _session: _FailingCollector()
            ).collect_and_publish(
                plan,
                api_request,
                render_request,
                api_output_path=api_path,
                render_output_path=render_path,
            )
            self.assertTrue(api_path.exists())
            self.assertEqual(result.api.state, "PUBLISHED")
            self.assertEqual(result.render.state, "MISSING")
            self.assertEqual(result.render.error_code, "COLLECTION_ERROR")
            self.assertFalse(render_path.exists())

    def test_session_mismatch_rejects_only_the_mismatched_artifact(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)

        def mismatched_api_factory(_session_factory):
            return GitHubCollector(
                base_transport(), session_id_factory=lambda: "different-session"
            )

        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"
            result = self._coordinator(
                api_factory=mismatched_api_factory
            ).collect_and_publish(
                plan,
                api_request,
                render_request,
                api_output_path=api_path,
                render_output_path=render_path,
            )
            self.assertEqual(result.api.error_code, "SESSION_MISMATCH")
            self.assertFalse(api_path.exists())
            self.assertTrue(render_path.exists())

    def test_publish_race_does_not_overwrite_or_prevent_render(self) -> None:
        plan = _paired_plan()
        api_request, render_request = _requests(plan)
        with tempfile.TemporaryDirectory() as temporary:
            api_path = Path(temporary) / "api.json"
            render_path = Path(temporary) / "render.json"

            def racing_api_factory(session_factory):
                inner = GitHubCollector(
                    base_transport(), session_id_factory=session_factory
                )

                class RacingCollector:
                    def collect(self, inner_plan, inner_request):
                        result = inner.collect(inner_plan, inner_request)
                        api_path.write_text("race-winner", encoding="utf-8")
                        return result

                return RacingCollector()

            result = self._coordinator(
                api_factory=racing_api_factory
            ).collect_and_publish(
                plan,
                api_request,
                render_request,
                api_output_path=api_path,
                render_output_path=render_path,
            )
            self.assertEqual(api_path.read_text(encoding="utf-8"), "race-winner")
            self.assertEqual(result.api.state, "COLLECTED_NOT_PUBLISHED")
            self.assertEqual(result.api.error_code, "PUBLISH_ERROR")
            self.assertTrue(render_path.exists())

    def test_result_contract_has_no_joined_facts_match_or_verdict(self) -> None:
        names = {field.name for field in fields(PairedCollectionResult)}
        self.assertEqual(
            names,
            {"collection_session_id", "collection_order", "api", "render"},
        )
        serialized_names = " ".join(sorted(names)).casefold()
        for forbidden in ("facts", "match", "verdict", "acceptance", "core"):
            self.assertNotIn(forbidden, serialized_names)


if __name__ == "__main__":
    unittest.main()
