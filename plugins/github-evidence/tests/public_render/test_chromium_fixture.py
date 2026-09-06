from __future__ import annotations

import importlib.util
import unittest
from dataclasses import dataclass

from veritrail_github.public_render_browser import RenderBrowserSession
from veritrail_github.public_render_collector import PublicRenderCollector
from veritrail_github.public_render_contracts import derive_public_render_request

from public_render.support import TARGET_SHA, public_render_plan


@dataclass(frozen=True)
class _FixtureRuntime:
    playwright_version: str = "1.62.0"
    browser_engine: str = "CHROMIUM"
    browser_distribution: str = "BUNDLED_MATCHING"
    browser_version: str = "verified-by-live-session"


class _SyntheticGitHubSession(RenderBrowserSession):
    def __init__(
        self,
        request: dict[str, object],
        html: str,
        *,
        status: int = 200,
        abort_navigation: bool = False,
    ) -> None:
        super().__init__(request, runtime_preflight=lambda: _FixtureRuntime())
        self._fixture_html = html
        self._status = status
        self._abort_navigation = abort_navigation

    def _continue_allowed_request(self, route: object, request: object) -> None:
        if request.is_navigation_request():
            if self._abort_navigation:
                route.abort("failed")
                return
            route.fulfill(
                status=self._status,
                headers={
                    "content-type": "text/html; charset=utf-8",
                    "set-cookie": (
                        "fixture-session=secret-value; Secure; HttpOnly; SameSite=Lax"
                    ),
                },
                body=self._fixture_html,
            )
            return
        route.fulfill(status=204, body="")


@unittest.skipUnless(
    importlib.util.find_spec("playwright") is not None,
    "render extra is not installed",
)
class RealChromiumFixtureTests(unittest.TestCase):
    @staticmethod
    def _navigation_plan() -> dict[str, object]:
        coordinates = {
            "owner": "NoctilumeDev",
            "repository": "VeriTrail",
            "target_kind": "GITHUB_REPOSITORY_README",
            "viewport_profile": "DESKTOP_1365X768",
        }
        return public_render_plan(
            coordinates, projections=["navigation.identity"]
        )

    def test_http_error_statuses_remain_complete_navigation_facts(self) -> None:
        plan = self._navigation_plan()
        for status in (404, 500):
            with self.subTest(status=status):
                request = derive_public_render_request(
                    plan,
                    "github-public-render",
                    f"chromium-status-{status}",
                )
                result = PublicRenderCollector(
                    session_id_factory=lambda status=status: (
                        f"github-render-status-{status}"
                    ),
                    browser_session_factory=lambda verified, status=status: (
                        _SyntheticGitHubSession(
                            verified, "<html></html>", status=status
                        )
                    ),
                ).collect(plan, request)
                document = result.artifact.document

                self.assertEqual(
                    "COMPLETE",
                    document["metadata"]["veritrail_observation"]["coverage"],
                )
                self.assertEqual(
                    status,
                    document["facts"]["navigation"]["top_level_http_status"],
                )

    def test_navigation_without_response_fails_closed_as_error_evidence(self) -> None:
        plan = self._navigation_plan()
        request = derive_public_render_request(
            plan, "github-public-render", "chromium-no-response"
        )
        result = PublicRenderCollector(
            session_id_factory=lambda: "github-render-no-response",
            browser_session_factory=lambda verified: _SyntheticGitHubSession(
                verified, "<html></html>", abort_navigation=True
            ),
        ).collect(plan, request)
        document = result.artifact.document

        self.assertEqual(
            "ERROR", document["metadata"]["veritrail_observation"]["coverage"]
        )
        self.assertIsNone(document["facts"]["navigation"])
        self.assertTrue(
            any(
                item["code"]
                in {
                    "RENDER_NAVIGATION_FAILED",
                    "RESPONSE_BODY_OBSERVATION_FAILED",
                }
                for item in document["metadata"][
                    "github_public_render_collection"
                ]["errors"]
            )
        )

    def test_full_collector_observes_bounded_synthetic_surface(self) -> None:
        projections = sorted(
            [
                "content.headings",
                "content.links",
                "content.literal_markers",
                "content.rendered_text_signature",
                "content.scope",
                "document.identity",
                "navigation.identity",
            ]
        )
        coordinates = {
            "owner": "NoctilumeDev",
            "repository": "VeriTrail",
            "target_kind": "GITHUB_MARKDOWN_FILE",
            "target_commit_sha": TARGET_SHA,
            "repository_path": "README.md",
            "viewport_profile": "DESKTOP_1365X768",
            "literal_markers": ["VeriTrail"],
        }
        plan = public_render_plan(coordinates, projections=projections)
        request = derive_public_render_request(
            plan, "github-public-render", "chromium-fixture-001"
        )
        html = """<!doctype html>
        <html lang="en"><head><title>VeriTrail fixture</title></head>
        <body><article class="markdown-body">
          <h1>VeriTrail fixture</h1>
          <p>VeriTrail keeps evidence <a href="/NoctilumeDev/VeriTrail?token=secret">repository</a>.</p>
          <h2 style="margin-top: 900px">Below the initial viewport</h2>
          <script>
            console.error("synthetic console noise");
            fetch("/_private/telemetry?token=secret", {method: "POST", body: "x"})
              .catch(() => {});
          </script>
        </article></body></html>"""
        result = PublicRenderCollector(
            session_id_factory=lambda: "github-render-chromium-fixture",
            browser_session_factory=lambda verified: _SyntheticGitHubSession(
                verified, html
            ),
        ).collect(plan, request)

        document = result.artifact.document
        observation = document["metadata"]["veritrail_observation"]
        collection = document["metadata"]["github_public_render_collection"]
        facts = document["facts"]
        stable = facts["content"]["window"]["stable_facts"]

        self.assertEqual("COMPLETE", observation["coverage"])
        self.assertEqual(200, facts["navigation"]["top_level_http_status"])
        self.assertEqual("VeriTrail fixture", facts["document"]["title"])
        self.assertEqual(1, facts["content"]["scope"]["observed_count"])
        self.assertTrue(facts["content"]["window"]["samples_stable"])
        self.assertEqual(3, len(facts["content"]["window"]["sample_digests"]))
        self.assertEqual(
            2, stable["literal_markers"][0]["rendered_text_occurrences"]
        )
        headings = stable["headings"]
        self.assertEqual(2, headings["observed_count"])
        self.assertEqual(2, headings["retained_count"])
        self.assertTrue(headings["items"][0]["in_initial_viewport"])
        self.assertFalse(headings["items"][1]["in_initial_viewport"])
        links = stable["links"]
        self.assertEqual(1, links["observed_count"])
        self.assertEqual(1, links["retained_count"])
        self.assertTrue(links["items"][0]["target"]["query_present"])
        self.assertNotIn("token", repr(links["items"][0]))

        network = collection["network_summary"]
        response_bodies = collection["response_body_observation"]
        self.assertGreaterEqual(network["blocked_write_count"], 1)
        self.assertEqual(0, network["affects_coverage_count"])
        self.assertGreater(response_bodies["main_document_response_body_bytes"], 0)
        self.assertEqual(
            response_bodies["total_response_body_bytes"],
            response_bodies["delivered_response_body_bytes"],
        )
        self.assertEqual(0, response_bodies["active_streams"])
        self.assertEqual([], collection["cleanup_errors"])
        self.assertGreaterEqual(
            collection["runtime_events"]["console_categories"].get("error", 0),
            1,
        )
        self.assertNotIn("secret-value", repr(document))
        self.assertNotIn("token=secret", repr(document))


if __name__ == "__main__":
    unittest.main()
