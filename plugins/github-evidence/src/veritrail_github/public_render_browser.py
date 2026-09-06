from __future__ import annotations

import copy
import math
import time
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from veritrail_github.errors import CollectionError
from veritrail_github.public_render_contracts import (
    PUBLIC_RENDER_VIEWPORTS,
    public_render_target_url,
)
from veritrail_github.public_render_navigation import (
    NetworkDecision,
    PublicRenderNetworkPolicy,
    fixed_scope_selector,
    navigation_identity_conflicts,
    normalized_media_type,
    safe_public_url_facts,
)
from veritrail_github.public_render_network import (
    ResponseBodyPolicy,
    ResponseStageBodyController,
)
from veritrail_github.public_render_runtime import preflight_render_runtime


class PublicRenderBrowserError(CollectionError):
    """The bounded P2 browser lifecycle cannot continue safely."""


class FreshContextRejected(PublicRenderBrowserError):
    """A supposedly fresh BrowserContext already contains persistent state."""


class RenderDeadlineExceeded(PublicRenderBrowserError):
    """The single monotonic P2 collection window has expired."""


class RenderNavigationFailed(PublicRenderBrowserError):
    """No trustworthy final main-document response was produced."""


@dataclass(frozen=True)
class BrowserNavigationSnapshot:
    requested_url: dict[str, Any]
    redirect_chain: tuple[dict[str, Any], ...]
    final_url: dict[str, Any]
    top_level_http_status: int
    media_type: str | None


@dataclass(frozen=True)
class FixedScopeSnapshot:
    selector: str
    count: int
    usable: bool


@dataclass(frozen=True)
class BrowserSessionSnapshot:
    runtime: dict[str, Any]
    initial_state: dict[str, Any]
    post_navigation_state: dict[str, Any] | None
    navigation: BrowserNavigationSnapshot | None
    scope: FixedScopeSnapshot | None
    response_bodies: dict[str, Any] | None
    network: tuple[dict[str, Any], ...]
    conflicts: tuple[dict[str, Any], ...]
    cleanup_errors: tuple[str, ...]


def browser_context_options(viewport_profile: str) -> dict[str, Any]:
    """Return the frozen non-persistent, non-mobile P2 context configuration."""

    viewport = PUBLIC_RENDER_VIEWPORTS.get(viewport_profile)
    if viewport is None:
        raise PublicRenderBrowserError("P2 viewport profile is unsupported")
    return {
        "viewport": {
            "width": viewport["width"],
            "height": viewport["height"],
        },
        "device_scale_factor": viewport["device_scale_factor"],
        "is_mobile": False,
        "has_touch": False,
        "locale": "en-US",
        "timezone_id": "UTC",
        "color_scheme": "light",
        "reduced_motion": "reduce",
        "permissions": [],
        "service_workers": "block",
        "accept_downloads": False,
        "java_script_enabled": True,
    }


def validate_fresh_storage_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """Prove the initial context has no cookies or storage-bearing origins."""

    normalized = _storage_state_lists(state)
    if normalized["cookies"] or normalized["origins"]:
        raise FreshContextRejected(
            "P2 BrowserContext initial cookies and origins must both be empty"
        )
    return {
        "kind": "ANONYMOUS_FRESH_CONTEXT",
        "cookies": 0,
        "origins": 0,
    }


def post_navigation_storage_summary(state: Mapping[str, Any]) -> dict[str, Any]:
    """Retain only safe aggregate state; never persist cookie names or values."""

    normalized = _storage_state_lists(state)
    cookies = normalized["cookies"]
    same_site = {"Strict": 0, "Lax": 0, "None": 0, "Unknown": 0}
    secure_count = 0
    http_only_count = 0
    session_cookie_count = 0
    for cookie in cookies:
        if not isinstance(cookie, Mapping):
            raise PublicRenderBrowserError(
                "P2 post-navigation cookie metadata is malformed"
            )
        if cookie.get("secure") is True:
            secure_count += 1
        if cookie.get("httpOnly") is True:
            http_only_count += 1
        expires = cookie.get("expires")
        if isinstance(expires, (int, float)) and not isinstance(expires, bool):
            if expires < 0:
                session_cookie_count += 1
        same_site_value = cookie.get("sameSite")
        key = same_site_value if same_site_value in same_site else "Unknown"
        same_site[key] += 1
    return {
        "cookie_count": len(cookies),
        "origin_count": len(normalized["origins"]),
        "secure_cookie_count": secure_count,
        "http_only_cookie_count": http_only_count,
        "session_cookie_count": session_cookie_count,
        "same_site_counts": same_site,
    }


def _storage_state_lists(state: Mapping[str, Any]) -> dict[str, list[Any]]:
    if not isinstance(state, Mapping):
        raise PublicRenderBrowserError(
            "P2 BrowserContext storage state is not an object"
        )
    candidate = copy.deepcopy(dict(state))
    if set(candidate) != {"cookies", "origins"}:
        raise PublicRenderBrowserError(
            "P2 BrowserContext storage state has an unsupported shape"
        )
    cookies = candidate.get("cookies")
    origins = candidate.get("origins")
    if not isinstance(cookies, list) or not isinstance(origins, list):
        raise PublicRenderBrowserError(
            "P2 BrowserContext storage state lists are malformed"
        )
    return {"cookies": cookies, "origins": origins}


class RenderBrowserSession:
    """Own one bounded Chromium process, context, page and CDP response gate."""

    def __init__(
        self,
        verified_request: Mapping[str, Any],
        *,
        playwright_factory: Any | None = None,
        runtime_preflight: Any = preflight_render_runtime,
        monotonic: Any = time.monotonic,
    ) -> None:
        self._request = copy.deepcopy(dict(verified_request))
        try:
            spec = self._request["observation_spec"]
            self._coordinates = spec["coordinates"]
            self._projections = frozenset(spec["projections"])
            self._policy = self._request["render_policy"]
            self._target_url = public_render_target_url(self._coordinates)
        except (KeyError, TypeError) as error:
            raise PublicRenderBrowserError(
                "P2 browser session requires a validated Render request"
            ) from error
        self._playwright_factory = playwright_factory
        self._runtime_preflight = runtime_preflight
        self._monotonic = monotonic
        self._deadline: float | None = None
        self._playwright_manager = None
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._cdp_session = None
        self._body_controller = None
        self._runtime: dict[str, Any] = {}
        self._initial_state: dict[str, Any] = {}
        self._post_state: dict[str, Any] | None = None
        self._navigation: BrowserNavigationSnapshot | None = None
        self._scope: FixedScopeSnapshot | None = None
        self._scope_locator = None
        self._network_policy: PublicRenderNetworkPolicy | None = None
        self._network_records: list[dict[str, Any]] = []
        self._conflicts: list[dict[str, Any]] = []
        self._cleanup_errors: list[str] = []
        self._opened = False
        self._closed = False

    def __enter__(self) -> RenderBrowserSession:
        return self.open()

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()

    @property
    def page(self) -> Any:
        if self._page is None or not self._opened or self._closed:
            raise PublicRenderBrowserError("P2 browser page is not live")
        return self._page

    @property
    def scope_locator(self) -> Any:
        if self._scope_locator is None or self._scope is None or not self._scope.usable:
            raise PublicRenderBrowserError(
                "P2 fixed content scope is not uniquely usable"
            )
        return self._scope_locator

    def open(self) -> RenderBrowserSession:
        if self._opened or self._closed:
            raise PublicRenderBrowserError("P2 browser session is single-use")
        self._deadline = self._monotonic() + self._policy["max_elapsed_ms"] / 1000
        try:
            preflight = self._runtime_preflight()
            self._runtime = asdict(preflight)
            factory = self._playwright_factory or _default_playwright_factory
            self._playwright_manager = factory()
            self._playwright = self._playwright_manager.start()
            self._browser = self._playwright.chromium.launch(
                headless=self._policy["headless"],
                timeout=self._operation_timeout_ms(
                    self._policy["navigation_timeout_ms"]
                ),
            )
            self._runtime["browser_version"] = self._browser.version
            self._context = self._browser.new_context(
                **browser_context_options(self._coordinates["viewport_profile"])
            )
            initial_storage = self._context.storage_state(indexed_db=True)
            self._initial_state = validate_fresh_storage_state(initial_storage)
            self._install_request_policy()
            self._page = self._context.new_page()
            self._context.on("page", self._reject_unexpected_page)
            self._page.on("download", self._reject_download)
            self._cdp_session = self._context.new_cdp_session(self._page)
            main_frame_id = _main_frame_id(self._cdp_session)
            response_policy = ResponseBodyPolicy(
                max_main_document_response_body_bytes=self._policy[
                    "max_main_document_response_body_bytes"
                ],
                max_total_response_body_bytes=self._policy[
                    "max_total_response_body_bytes"
                ],
                response_body_read_chunk_bytes=self._policy[
                    "response_body_read_chunk_bytes"
                ],
            )
            self._body_controller = ResponseStageBodyController(
                self._cdp_session,
                main_frame_id=main_frame_id,
                policy=response_policy,
            )
            self._body_controller.install()
            self._opened = True
            return self
        except Exception:
            self.close()
            raise

    def navigate(self) -> BrowserNavigationSnapshot:
        if not self._opened or self._closed or self._page is None:
            raise PublicRenderBrowserError("P2 browser session must be opened first")
        if self._navigation is not None:
            raise PublicRenderBrowserError("P2 browser session permits one navigation")
        try:
            response = self._page.goto(
                self._target_url,
                wait_until="domcontentloaded",
                timeout=self._operation_timeout_ms(
                    self._policy["navigation_timeout_ms"]
                ),
            )
        except Exception as error:
            self._raise_body_failure()
            self._check_deadline()
            raise RenderNavigationFailed(
                f"P2 main-document navigation failed: {type(error).__name__}"
            ) from error
        self._raise_body_failure()
        self._check_deadline()
        if response is None:
            raise RenderNavigationFailed(
                "P2 main-document navigation produced no final Response"
            )
        status = response.status
        if isinstance(status, bool) or not isinstance(status, int):
            raise RenderNavigationFailed(
                "P2 final Response omitted its HTTP status"
            )
        final_url = self._page.url
        redirect_chain = _redirect_chain(response)
        headers = response.all_headers()
        if not isinstance(headers, Mapping):
            raise RenderNavigationFailed(
                "P2 final Response headers are not representable"
            )
        media_type = normalized_media_type(headers)
        self._conflicts.extend(
            navigation_identity_conflicts(
                requested_url=self._target_url, final_url=final_url
            )
        )
        self._navigation = BrowserNavigationSnapshot(
            requested_url=safe_public_url_facts(self._target_url),
            redirect_chain=tuple(redirect_chain),
            final_url=safe_public_url_facts(final_url),
            top_level_http_status=status,
            media_type=media_type,
        )
        self._post_state = post_navigation_storage_summary(
            self._context.storage_state(indexed_db=True)
        )
        return self._navigation

    def locate_fixed_scope(self) -> FixedScopeSnapshot | None:
        if self._navigation is None or self._page is None:
            raise PublicRenderBrowserError("P2 navigation must precede scope lookup")
        if self._scope is not None:
            raise PublicRenderBrowserError("P2 fixed scope may be located only once")
        self.assert_healthy()
        if not any(item.startswith("content.") for item in self._projections):
            return None
        selector = fixed_scope_selector(self._coordinates["target_kind"])
        if self._navigation.media_type not in {
            "text/html",
            "application/xhtml+xml",
        }:
            self._conflicts.append(
                {
                    "code": "CONTENT_MEDIA_TYPE_UNSUPPORTED",
                    "media_type": self._navigation.media_type,
                }
            )
            self._scope = FixedScopeSnapshot(selector=selector, count=0, usable=False)
            return self._scope
        try:
            self._page.wait_for_selector(
                selector,
                state="attached",
                timeout=self._operation_timeout_ms(self._policy["scope_timeout_ms"]),
            )
        except Exception as error:
            self._check_deadline()
            if not _is_scope_wait_timeout(error):
                raise PublicRenderBrowserError(
                    "P2 fixed content scope lookup failed"
                ) from error
        locator = self._page.locator(selector)
        count = locator.count()
        usable = count == 1
        self._scope = FixedScopeSnapshot(
            selector=selector,
            count=count,
            usable=usable,
        )
        if usable:
            self._scope_locator = locator
        else:
            self._conflicts.append(
                {
                    "code": "CONTENT_SCOPE_COUNT_MISMATCH",
                    "selector": selector,
                    "observed_count": count,
                    "required_count": 1,
                }
            )
        self.assert_healthy()
        return self._scope

    def assert_healthy(self) -> None:
        """Raise any deferred browser or response-stage failure before acceptance."""

        if not self._opened or self._closed:
            raise PublicRenderBrowserError("P2 browser session is not live")
        self._check_deadline()
        self._raise_body_failure()

    def snapshot(self) -> BrowserSessionSnapshot:
        response_bodies = (
            asdict(self._body_controller.snapshot())
            if self._body_controller is not None
            else None
        )
        return BrowserSessionSnapshot(
            runtime=copy.deepcopy(self._runtime),
            initial_state=copy.deepcopy(self._initial_state),
            post_navigation_state=copy.deepcopy(self._post_state),
            navigation=self._navigation,
            scope=self._scope,
            response_bodies=response_bodies,
            network=tuple(copy.deepcopy(self._network_records)),
            conflicts=tuple(copy.deepcopy(self._conflicts)),
            cleanup_errors=tuple(self._cleanup_errors),
        )

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        resources = (
            ("response-body-controller", self._body_controller, "close"),
            ("cdp-session", self._cdp_session, "detach"),
            ("browser-context", self._context, "close"),
            ("browser", self._browser, "close"),
            ("playwright", self._playwright, "stop"),
        )
        for label, resource, method in resources:
            if resource is None:
                continue
            try:
                getattr(resource, method)()
            except Exception:
                self._cleanup_errors.append(f"{label}:close-failed")

    def _operation_timeout_ms(self, requested_ms: int) -> int:
        self._check_deadline()
        if self._deadline is None:
            raise PublicRenderBrowserError(
                "P2 browser session deadline has not been initialized"
            )
        remaining_ms = max(1, math.ceil((self._deadline - self._monotonic()) * 1000))
        return min(requested_ms, remaining_ms)

    def _check_deadline(self) -> None:
        if self._deadline is not None and self._monotonic() >= self._deadline:
            raise RenderDeadlineExceeded("P2 monotonic collection window expired")

    def _install_request_policy(self) -> None:
        self._network_policy = PublicRenderNetworkPolicy(
            target_url=self._target_url,
            target_kind=self._coordinates["target_kind"],
            max_requests=self._policy["max_requests"],
            max_redirects=self._policy["max_redirects"],
        )
        self._context.route("**/*", self._route_request)
        self._context.route_web_socket("**/*", self._route_websocket)

    def _route_request(self, route: Any, request: Any) -> None:
        try:
            method = request.method
            navigation_request = request.is_navigation_request()
            main_document = (
                navigation_request
                and self._page is not None
                and request.frame == self._page.main_frame
            )
            redirect_depth = _redirect_depth(request) if main_document else 0
            if navigation_request and not main_document:
                decision = self._network_policy.decide(
                    method=method,
                    url=request.url,
                    main_document=False,
                )
                decision = NetworkDecision(
                    sequence=decision.sequence,
                    allowed=False,
                    reasons=tuple((*decision.reasons, "UNEXPECTED_PAGE_NAVIGATION")),
                    affects_coverage=True,
                    safe_url=decision.safe_url,
                )
            else:
                decision = self._network_policy.decide(
                    method=method,
                    url=request.url,
                    main_document=main_document,
                    redirect_depth=redirect_depth,
                )
            self._record_network_decision(method, main_document, decision)
            if decision.allowed:
                route.continue_()
            else:
                route.abort("blockedbyclient")
        except Exception:
            self._conflicts.append({"code": "REQUEST_ROUTE_HANDLER_FAILED"})
            try:
                route.abort("blockedbyclient")
            except Exception:
                pass

    def _route_websocket(self, route: Any) -> None:
        decision = self._network_policy.reject_websocket(route.url)
        self._record_network_decision("WEBSOCKET", False, decision)
        try:
            route.close()
        except Exception:
            self._conflicts.append({"code": "WEBSOCKET_CLOSE_FAILED"})

    def _record_network_decision(
        self, method: str, main_document: bool, decision: NetworkDecision
    ) -> None:
        self._network_records.append(
            {
                "sequence": decision.sequence,
                "method": method.upper() if isinstance(method, str) else "UNKNOWN",
                "main_document": main_document,
                "allowed": decision.allowed,
                "reasons": list(decision.reasons),
                "affects_coverage": decision.affects_coverage,
                "url": copy.deepcopy(decision.safe_url),
            }
        )

    def _reject_unexpected_page(self, page: Any) -> None:
        if page is self._page:
            return
        self._conflicts.append({"code": "UNEXPECTED_PAGE_BLOCKED"})
        try:
            page.close()
        except Exception:
            self._cleanup_errors.append("unexpected-page:close-failed")

    def _reject_download(self, download: Any) -> None:
        self._conflicts.append({"code": "DOWNLOAD_BLOCKED"})
        try:
            download.cancel()
        except Exception:
            self._cleanup_errors.append("download:cancel-failed")

    def _raise_body_failure(self) -> None:
        if self._body_controller is not None:
            self._body_controller.raise_if_failed()


def _default_playwright_factory() -> Any:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise PublicRenderBrowserError(
            "P2 render capability requires the explicit 'render' extra"
        ) from error
    return sync_playwright()


def _main_frame_id(cdp_session: Any) -> str:
    result = cdp_session.send("Page.getFrameTree")
    try:
        frame_id = result["frameTree"]["frame"]["id"]
    except (KeyError, TypeError) as error:
        raise PublicRenderBrowserError(
            "P2 Chromium did not expose a main frame id"
        ) from error
    if not isinstance(frame_id, str) or not frame_id:
        raise PublicRenderBrowserError("P2 Chromium main frame id is invalid")
    return frame_id


def _redirect_depth(request: Any) -> int:
    depth = 0
    current = request.redirected_from
    while current is not None:
        depth += 1
        current = current.redirected_from
    return depth


def _redirect_chain(response: Any) -> list[dict[str, Any]]:
    requests: list[Any] = []
    current = response.request
    while current is not None:
        requests.append(current)
        current = current.redirected_from
    chain: list[dict[str, Any]] = []
    for request in reversed(requests):
        request_response = request.response()
        status = request_response.status if request_response is not None else None
        if status is not None and (
            isinstance(status, bool) or not isinstance(status, int)
        ):
            raise RenderNavigationFailed(
                "P2 redirect response omitted a valid HTTP status"
            )
        chain.append(
            {
                "url": safe_public_url_facts(request.url),
                "http_status": status,
            }
        )
    return chain


def _is_scope_wait_timeout(error: Exception) -> bool:
    if isinstance(error, TimeoutError):
        return True
    error_type = type(error)
    return (
        error_type.__name__ == "TimeoutError"
        and error_type.__module__.startswith("playwright.")
    )
