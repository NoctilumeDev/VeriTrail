from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlsplit

from veritrail_github.errors import CollectionError


NORMALIZATION_SEMANTICS_VERSION = "github-public-render-facts/0.1"

_READ_METHODS = frozenset({"GET", "HEAD"})
_GITHUB_TARGETS = frozenset(
    {
        "GITHUB_REPOSITORY_README",
        "GITHUB_MARKDOWN_FILE",
        "GITHUB_RELEASE",
    }
)
_GITHUB_SUBRESOURCE_WILDCARD_SUFFIXES = (
    "github.com",
    "githubassets.com",
    "githubusercontent.com",
)
_FIXED_SCOPE_SELECTORS = {
    "GITHUB_REPOSITORY_README": "article.markdown-body",
    "GITHUB_MARKDOWN_FILE": "article.markdown-body",
    "GITHUB_RELEASE": "main .markdown-body",
    "GITHUB_PAGES_DEFAULT": "main",
}


class PublicRenderNavigationError(CollectionError):
    """A public URL or navigation fact cannot be represented safely."""


@dataclass(frozen=True)
class NetworkDecision:
    sequence: int
    allowed: bool
    reasons: tuple[str, ...]
    affects_coverage: bool
    safe_url: dict[str, Any] | None


def fixed_scope_selector(target_kind: str) -> str:
    try:
        return _FIXED_SCOPE_SELECTORS[target_kind]
    except KeyError as error:
        raise PublicRenderNavigationError(
            "P2 target kind has no fixed content scope"
        ) from error


def safe_public_url_facts(value: str) -> dict[str, Any]:
    """Retain a public HTTPS coordinate without query values or credentials."""

    if not isinstance(value, str) or not value:
        raise PublicRenderNavigationError("P2 observed URL must be non-empty text")
    if any(
        unicodedata.category(character) in {"Cc", "Cs"} for character in value
    ):
        raise PublicRenderNavigationError(
            "P2 observed URL contains control or non-scalar text"
        )
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as error:
        raise PublicRenderNavigationError(
            "P2 observed URL cannot be parsed safely"
        ) from error
    if parsed.scheme.casefold() != "https":
        raise PublicRenderNavigationError("P2 observed URL must use HTTPS")
    if parsed.username is not None or parsed.password is not None:
        raise PublicRenderNavigationError("P2 observed URL must not contain userinfo")
    host = parsed.hostname.casefold() if parsed.hostname else None
    if host is None:
        raise PublicRenderNavigationError("P2 observed URL must contain a host")
    if port not in {None, 443}:
        raise PublicRenderNavigationError("P2 observed URL must use HTTPS port 443")
    origin = f"https://{host}"
    return {
        "origin": origin,
        "host": host,
        "path": parsed.path or "/",
        "query_present": bool(parsed.query),
        "fragment_present": bool(parsed.fragment),
    }


def normalized_media_type(headers: Mapping[str, str]) -> str | None:
    values = [
        value
        for name, value in headers.items()
        if isinstance(name, str)
        and isinstance(value, str)
        and name.casefold() == "content-type"
    ]
    if not values:
        return None
    if len(values) != 1:
        raise PublicRenderNavigationError(
            "P2 final response has ambiguous Content-Type metadata"
        )
    media_type = values[0].split(";", 1)[0].strip().casefold()
    return media_type or None


class PublicRenderNetworkPolicy:
    """Classify every browser request without retaining secret-bearing URL parts."""

    def __init__(
        self,
        *,
        target_url: str,
        target_kind: str,
        max_requests: int,
        max_redirects: int,
    ) -> None:
        if target_kind not in _FIXED_SCOPE_SELECTORS:
            raise ValueError("target_kind is not a frozen P2 target")
        if (
            isinstance(max_requests, bool)
            or not isinstance(max_requests, int)
            or max_requests < 1
        ):
            raise ValueError("max_requests must be a positive integer")
        if (
            isinstance(max_redirects, bool)
            or not isinstance(max_redirects, int)
            or max_redirects < 0
        ):
            raise ValueError("max_redirects must be a non-negative integer")
        self._target = safe_public_url_facts(target_url)
        self._target_kind = target_kind
        self._max_requests = max_requests
        self._max_redirects = max_redirects
        self._request_count = 0

    @property
    def request_count(self) -> int:
        return self._request_count

    def decide(
        self,
        *,
        method: str,
        url: str,
        main_document: bool,
        redirect_depth: int = 0,
    ) -> NetworkDecision:
        self._request_count += 1
        reasons: list[str] = []
        safe_url: dict[str, Any] | None = None
        try:
            safe_url = safe_public_url_facts(url)
        except PublicRenderNavigationError:
            reasons.append("URL_UNSAFE")

        normalized_method = method.upper() if isinstance(method, str) else ""
        read_request = normalized_method in _READ_METHODS
        if not read_request:
            reasons.append("METHOD_NOT_ALLOWED")
        if self._request_count > self._max_requests:
            reasons.append("REQUEST_LIMIT_EXCEEDED")
        if (
            isinstance(redirect_depth, bool)
            or not isinstance(redirect_depth, int)
            or redirect_depth < 0
        ):
            reasons.append("REDIRECT_DEPTH_INVALID")
        elif main_document and redirect_depth > self._max_redirects:
            reasons.append("REDIRECT_LIMIT_EXCEEDED")
        if safe_url is not None and not self._host_allowed(
            safe_url, main_document=main_document
        ):
            reasons.append("HOST_NOT_ALLOWED")

        allowed = not reasons
        affects_coverage = (
            "REQUEST_LIMIT_EXCEEDED" in reasons
            or "REDIRECT_DEPTH_INVALID" in reasons
            or "REDIRECT_LIMIT_EXCEEDED" in reasons
            or "URL_UNSAFE" in reasons
            or (read_request and "HOST_NOT_ALLOWED" in reasons)
        )
        return NetworkDecision(
            sequence=self._request_count,
            allowed=allowed,
            reasons=tuple(reasons),
            affects_coverage=affects_coverage,
            safe_url=safe_url,
        )

    def reject_websocket(self, url: str) -> NetworkDecision:
        self._request_count += 1
        safe_url = None
        reasons = ["WEBSOCKET_NOT_ALLOWED"]
        try:
            parsed = urlsplit(url)
            if parsed.hostname:
                safe_url = {
                    "scheme_class": parsed.scheme.casefold() or "UNKNOWN",
                    "host": parsed.hostname.casefold(),
                }
        except (TypeError, ValueError):
            reasons.append("URL_UNSAFE")
        if self._request_count > self._max_requests:
            reasons.append("REQUEST_LIMIT_EXCEEDED")
        return NetworkDecision(
            sequence=self._request_count,
            allowed=False,
            reasons=tuple(reasons),
            affects_coverage="REQUEST_LIMIT_EXCEEDED" in reasons,
            safe_url=safe_url,
        )

    def _host_allowed(
        self, safe_url: Mapping[str, Any], *, main_document: bool
    ) -> bool:
        host = safe_url["host"]
        if self._target_kind == "GITHUB_PAGES_DEFAULT":
            return safe_url["origin"] == self._target["origin"]
        if self._target_kind not in _GITHUB_TARGETS:
            return False
        if main_document:
            return host == "github.com"
        return host == "github.com" or any(
            host.endswith(f".{suffix}")
            for suffix in _GITHUB_SUBRESOURCE_WILDCARD_SUFFIXES
        )


def navigation_identity_conflicts(
    *, requested_url: str, final_url: str
) -> list[dict[str, Any]]:
    """Compare safe coordinate identity without claiming content correctness."""

    requested = safe_public_url_facts(requested_url)
    final = safe_public_url_facts(final_url)
    conflicts: list[dict[str, Any]] = []
    if requested["origin"] != final["origin"] or requested["path"] != final["path"]:
        conflicts.append(
            {
                "code": "FINAL_COORDINATE_MISMATCH",
                "requested": requested,
                "observed": final,
            }
        )
    elif final["query_present"] or final["fragment_present"]:
        conflicts.append(
            {
                "code": "FINAL_COORDINATE_DECORATED",
                "requested": requested,
                "observed": final,
            }
        )
    return conflicts
