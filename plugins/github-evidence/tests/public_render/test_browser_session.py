from __future__ import annotations

import unittest
from dataclasses import dataclass

from veritrail_github.public_render_browser import (
    FreshContextRejected,
    PublicRenderBrowserError,
    RenderDeadlineExceeded,
    RenderBrowserSession,
)
from veritrail_github.public_render_contracts import derive_public_render_request
from veritrail_github.public_render_network import PublicRenderNetworkError

from public_render.support import public_render_plan


@dataclass(frozen=True)
class _FakePreflight:
    playwright_version: str = "1.62.0"
    browser_engine: str = "CHROMIUM"
    browser_distribution: str = "BUNDLED_MATCHING"
    browser_version: str = "151.0"


class _FakeResponse:
    def __init__(self, request: object, status: int = 200) -> None:
        self.request = request
        self.status = status

    def all_headers(self) -> dict[str, str]:
        return {"content-type": "text/html; charset=utf-8"}


class _FakeRequest:
    def __init__(
        self,
        url: str,
        frame: object,
        *,
        method: str = "GET",
        navigation: bool = True,
    ) -> None:
        self.url = url
        self.method = method
        self.frame = frame
        self._navigation = navigation
        self.redirected_from = None
        self._response = None

    def is_navigation_request(self) -> bool:
        return self._navigation

    def response(self) -> object:
        return self._response


class _FakeLocator:
    def __init__(self, count: int) -> None:
        self._count = count

    def count(self) -> int:
        return self._count


class _FakePage:
    def __init__(
        self,
        target_url: str,
        scope_count: int,
        scope_wait_error: Exception | None,
    ) -> None:
        self.main_frame = object()
        self.url = target_url
        self._target_url = target_url
        self._scope_count = scope_count
        self._scope_wait_error = scope_wait_error
        self.events: dict[str, object] = {}
        self.goto_calls = 0

    def on(self, event: str, handler: object) -> None:
        self.events[event] = handler

    def goto(self, url: str, **_kwargs: object) -> _FakeResponse:
        self.goto_calls += 1
        self.url = url
        request = _FakeRequest(url, self.main_frame)
        response = _FakeResponse(request)
        request._response = response
        return response

    def wait_for_selector(self, _selector: str, **_kwargs: object) -> None:
        if self._scope_wait_error is not None:
            raise self._scope_wait_error
        if self._scope_count == 0:
            raise TimeoutError("scope absent")

    def locator(self, _selector: str) -> _FakeLocator:
        return _FakeLocator(self._scope_count)


class _FakeCdpSession:
    def __init__(self) -> None:
        self.listeners: dict[str, object] = {}
        self.detached = False

    def send(self, method: str, _params: object = None) -> dict[str, object]:
        if method == "Page.getFrameTree":
            return {"frameTree": {"frame": {"id": "main-frame"}}}
        return {}

    def on(self, event: str, handler: object) -> None:
        self.listeners[event] = handler

    def remove_listener(self, event: str, _handler: object) -> None:
        self.listeners.pop(event, None)

    def detach(self) -> None:
        self.detached = True


class _FakeContext:
    def __init__(
        self,
        target_url: str,
        *,
        initial_state: dict[str, object],
        post_state: dict[str, object],
        scope_count: int,
        scope_wait_error: Exception | None,
    ) -> None:
        self._states = [initial_state, post_state]
        self.page = _FakePage(target_url, scope_count, scope_wait_error)
        self.cdp = _FakeCdpSession()
        self.events: dict[str, object] = {}
        self.routes: list[tuple[str, object]] = []
        self.websocket_routes: list[tuple[str, object]] = []
        self.new_page_calls = 0
        self.closed = False

    def storage_state(self, **_kwargs: object) -> dict[str, object]:
        return self._states.pop(0)

    def route(self, pattern: str, handler: object) -> None:
        self.routes.append((pattern, handler))

    def route_web_socket(self, pattern: str, handler: object) -> None:
        self.websocket_routes.append((pattern, handler))

    def new_page(self) -> _FakePage:
        self.new_page_calls += 1
        return self.page

    def on(self, event: str, handler: object) -> None:
        self.events[event] = handler

    def new_cdp_session(self, _page: object) -> _FakeCdpSession:
        return self.cdp

    def close(self) -> None:
        self.closed = True


class _FakeBrowser:
    version = "151.0"

    def __init__(self, context: _FakeContext) -> None:
        self.context = context
        self.context_options = None
        self.closed = False

    def new_context(self, **options: object) -> _FakeContext:
        self.context_options = options
        return self.context

    def close(self) -> None:
        self.closed = True


class _FakeChromium:
    def __init__(self, browser: _FakeBrowser) -> None:
        self.browser = browser
        self.launch_options = None

    def launch(self, **options: object) -> _FakeBrowser:
        self.launch_options = options
        return self.browser


class _FakePlaywright:
    def __init__(self, browser: _FakeBrowser) -> None:
        self.chromium = _FakeChromium(browser)
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True


class _FakeManager:
    def __init__(self, playwright: _FakePlaywright) -> None:
        self.playwright = playwright

    def start(self) -> _FakePlaywright:
        return self.playwright


class _FakeRoute:
    def __init__(self, url: str = "wss://github.com/socket") -> None:
        self.url = url
        self.continued = False
        self.aborted = False
        self.closed = False

    def continue_(self) -> None:
        self.continued = True

    def abort(self, _reason: str) -> None:
        self.aborted = True

    def close(self) -> None:
        self.closed = True


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def _request() -> dict[str, object]:
    plan = public_render_plan()
    return derive_public_render_request(
        plan, "github-public-render", "browser-session-001"
    )


def _fakes(
    *,
    initial_state: dict[str, object] | None = None,
    post_state: dict[str, object] | None = None,
    scope_count: int = 1,
    scope_wait_error: Exception | None = None,
) -> tuple[_FakeManager, _FakeBrowser, _FakeContext, _FakePlaywright]:
    target_url = "https://github.com/NoctilumeDev/VeriTrail"
    context = _FakeContext(
        target_url,
        initial_state=initial_state or {"cookies": [], "origins": []},
        post_state=post_state
        or {
            "cookies": [
                {
                    "name": "anonymous",
                    "value": "secret",
                    "secure": True,
                    "httpOnly": True,
                    "sameSite": "Lax",
                    "expires": -1,
                }
            ],
            "origins": [],
        },
        scope_count=scope_count,
        scope_wait_error=scope_wait_error,
    )
    browser = _FakeBrowser(context)
    playwright = _FakePlaywright(browser)
    return _FakeManager(playwright), browser, context, playwright


class RenderBrowserSessionTests(unittest.TestCase):
    def test_happy_path_retains_navigation_scope_and_safe_state(self) -> None:
        manager, browser, context, playwright = _fakes()
        with RenderBrowserSession(
            _request(),
            playwright_factory=lambda: manager,
            runtime_preflight=_FakePreflight,
        ) as session:
            navigation = session.navigate()
            scope = session.locate_fixed_scope()
            snapshot = session.snapshot()
            self.assertEqual(navigation.top_level_http_status, 200)
            self.assertEqual(navigation.media_type, "text/html")
            self.assertEqual(scope.count, 1)
            self.assertTrue(scope.usable)
            self.assertEqual(snapshot.initial_state["cookies"], 0)
            self.assertEqual(
                snapshot.post_navigation_state["cookie_count"], 1
            )
            self.assertEqual(snapshot.conflicts, ())
            self.assertEqual(
                snapshot.response_bodies,
                {
                    "total_response_body_bytes": 0,
                    "main_document_response_body_bytes": 0,
                    "delivered_response_body_bytes": 0,
                    "completed_responses": 0,
                    "closed_streams": 0,
                    "active_streams": 0,
                    "request_stage_pauses": 0,
                    "response_error_reason_counts": {},
                    "failure": None,
                },
            )
            self.assertIsNotNone(session.scope_locator)
            self.assertEqual(len(context.routes), 1)
            self.assertEqual(len(context.websocket_routes), 1)
            self.assertEqual(context.new_page_calls, 1)
            self.assertEqual(
                browser.context_options["viewport"],
                {"width": 1365, "height": 768},
            )
            self.assertFalse(browser.context_options["is_mobile"])
            self.assertFalse(browser.context_options["has_touch"])
            self.assertTrue(
                playwright.chromium.launch_options["headless"]
            )
        self.assertTrue(context.cdp.detached)
        self.assertTrue(context.closed)
        self.assertTrue(browser.closed)
        self.assertTrue(playwright.stopped)

    def test_dirty_initial_state_stops_before_page_creation_and_navigation(
        self,
    ) -> None:
        manager, browser, context, playwright = _fakes(
            initial_state={
                "cookies": [{"name": "old", "value": "secret"}],
                "origins": [],
            }
        )
        with self.assertRaises(FreshContextRejected):
            RenderBrowserSession(
                _request(),
                playwright_factory=lambda: manager,
                runtime_preflight=_FakePreflight,
            ).open()
        self.assertEqual(context.routes, [])
        self.assertEqual(context.events, {})
        self.assertEqual(context.new_page_calls, 0)
        self.assertEqual(context.page.goto_calls, 0)
        self.assertTrue(context.closed)
        self.assertTrue(browser.closed)
        self.assertTrue(playwright.stopped)

    def test_scope_count_is_explicit_and_never_falls_back_to_body(self) -> None:
        for count in (0, 2):
            with self.subTest(count=count):
                manager, _browser, _context, _playwright = _fakes(
                    scope_count=count
                )
                with RenderBrowserSession(
                    _request(),
                    playwright_factory=lambda: manager,
                    runtime_preflight=_FakePreflight,
                ) as session:
                    session.navigate()
                    scope = session.locate_fixed_scope()
                    self.assertEqual(scope.count, count)
                    self.assertFalse(scope.usable)
                    self.assertEqual(
                        session.snapshot().conflicts[-1]["code"],
                        "CONTENT_SCOPE_COUNT_MISMATCH",
                    )
                    with self.assertRaises(PublicRenderBrowserError):
                        _ = session.scope_locator

    def test_non_timeout_scope_failure_is_not_flattened_into_absence(self) -> None:
        manager, _browser, _context, _playwright = _fakes(
            scope_wait_error=RuntimeError("synthetic browser failure")
        )
        with RenderBrowserSession(
            _request(),
            playwright_factory=lambda: manager,
            runtime_preflight=_FakePreflight,
        ) as session:
            session.navigate()
            with self.assertRaisesRegex(
                PublicRenderBrowserError, "scope lookup failed"
            ):
                session.locate_fixed_scope()
            self.assertIsNone(session.snapshot().scope)

    def test_deferred_response_failure_cannot_cross_health_barrier(self) -> None:
        manager, _browser, context, _playwright = _fakes()
        with RenderBrowserSession(
            _request(),
            playwright_factory=lambda: manager,
            runtime_preflight=_FakePreflight,
        ) as session:
            context.cdp.listeners["Fetch.requestPaused"]({})
            with self.assertRaises(PublicRenderNetworkError):
                session.assert_healthy()
            self.assertEqual(
                session.snapshot().response_bodies["failure"],
                "PublicRenderNetworkError",
            )

    def test_absolute_deadline_is_not_refreshed_before_navigation(self) -> None:
        manager, _browser, context, _playwright = _fakes()
        clock = _Clock()
        session = RenderBrowserSession(
            _request(),
            playwright_factory=lambda: manager,
            runtime_preflight=_FakePreflight,
            monotonic=clock,
        ).open()
        try:
            clock.now = 46.0
            with self.assertRaises(RenderDeadlineExceeded):
                session.navigate()
            self.assertEqual(context.page.goto_calls, 0)
        finally:
            session.close()

    def test_cleanup_failure_is_recorded_without_stopping_reverse_cleanup(self) -> None:
        manager, browser, context, playwright = _fakes()

        def fail_browser_close() -> None:
            raise RuntimeError("synthetic close failure")

        browser.close = fail_browser_close
        session = RenderBrowserSession(
            _request(),
            playwright_factory=lambda: manager,
            runtime_preflight=_FakePreflight,
        ).open()
        session.navigate()
        session.close()
        snapshot = session.snapshot()
        self.assertEqual(snapshot.cleanup_errors, ("browser:close-failed",))
        self.assertTrue(context.cdp.detached)
        self.assertTrue(context.closed)
        self.assertTrue(playwright.stopped)

    def test_browser_routes_enforce_read_only_and_coverage_semantics(self) -> None:
        manager, _browser, context, _playwright = _fakes()
        with RenderBrowserSession(
            _request(),
            playwright_factory=lambda: manager,
            runtime_preflight=_FakePreflight,
        ) as session:
            handler = context.routes[0][1]

            telemetry_route = _FakeRoute()
            handler(
                telemetry_route,
                _FakeRequest(
                    "https://github.com/_private/telemetry",
                    context.page.main_frame,
                    method="POST",
                    navigation=False,
                ),
            )
            self.assertTrue(telemetry_route.aborted)

            foreign_route = _FakeRoute()
            handler(
                foreign_route,
                _FakeRequest(
                    "https://github.com.attacker.example/pixel",
                    context.page.main_frame,
                    navigation=False,
                ),
            )
            self.assertTrue(foreign_route.aborted)

            asset_route = _FakeRoute()
            handler(
                asset_route,
                _FakeRequest(
                    "https://assets.githubassets.com/app.css",
                    context.page.main_frame,
                    navigation=False,
                ),
            )
            self.assertTrue(asset_route.continued)

            websocket_route = _FakeRoute()
            websocket_handler = context.websocket_routes[0][1]
            websocket_handler(websocket_route)
            self.assertTrue(websocket_route.closed)

            network = session.snapshot().network
            self.assertEqual(network[0]["reasons"], ["METHOD_NOT_ALLOWED"])
            self.assertFalse(network[0]["affects_coverage"])
            self.assertEqual(network[1]["reasons"], ["HOST_NOT_ALLOWED"])
            self.assertTrue(network[1]["affects_coverage"])
            self.assertTrue(network[2]["allowed"])
            self.assertEqual(network[3]["reasons"], ["WEBSOCKET_NOT_ALLOWED"])


if __name__ == "__main__":
    unittest.main()
