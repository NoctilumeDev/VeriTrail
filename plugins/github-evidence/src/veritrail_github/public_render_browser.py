from __future__ import annotations

import copy
from typing import Any, Mapping

from veritrail_github.errors import CollectionError
from veritrail_github.public_render_contracts import PUBLIC_RENDER_VIEWPORTS


class PublicRenderBrowserError(CollectionError):
    """The bounded P2 browser lifecycle cannot continue safely."""


class FreshContextRejected(PublicRenderBrowserError):
    """A supposedly fresh BrowserContext already contains persistent state."""


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
        raise PublicRenderBrowserError("P2 BrowserContext storage state is not an object")
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
