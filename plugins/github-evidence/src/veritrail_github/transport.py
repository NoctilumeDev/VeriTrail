from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from veritrail_github.errors import TransportError


MAX_RESPONSE_BYTES = 4 * 1024 * 1024


@dataclass(frozen=True)
class TransportResponse:
    status: int
    headers: dict[str, str]
    body: bytes
    final_url: str


class Transport(Protocol):
    def get(
        self,
        *,
        api_origin: str,
        path_and_query: str,
        headers: Mapping[str, str],
        connect_timeout_ms: int,
        read_timeout_ms: int,
        max_redirects: int,
    ) -> TransportResponse: ...


class _SameOriginRedirectHandler(HTTPRedirectHandler):
    def __init__(self, api_origin: str, max_redirects: int) -> None:
        super().__init__()
        self._origin = _origin(api_origin)
        self.max_redirections = max_redirects

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        if _origin(newurl) != self._origin:
            raise TransportError("redirect crossed the frozen GitHub API origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _origin(value: str) -> tuple[str, str, int | None]:
    parsed = urlsplit(value)
    return parsed.scheme.lower(), (parsed.hostname or "").lower(), parsed.port


def _set_read_timeout(response, timeout_ms: int) -> None:  # type: ignore[no-untyped-def]
    """Best-effort split of urllib's connect and body-read timeouts."""

    raw = getattr(getattr(response, "fp", None), "raw", None)
    sock = getattr(raw, "_sock", None)
    if sock is not None:
        try:
            sock.settimeout(timeout_ms / 1000)
        except OSError:
            # The connect timeout remains a stricter safe fallback when an
            # alternative urllib response wrapper hides or closes its socket.
            pass


def _read_bounded(response, read_timeout_ms: int) -> bytes:  # type: ignore[no-untyped-def]
    _set_read_timeout(response, read_timeout_ms)
    body = response.read(MAX_RESPONSE_BYTES + 1)
    if len(body) > MAX_RESPONSE_BYTES:
        raise TransportError("GitHub response exceeded the fixed 4 MiB body limit")
    return body


class UrllibTransport:
    """Stdlib HTTPS transport with same-origin redirects and bounded bodies."""

    def get(
        self,
        *,
        api_origin: str,
        path_and_query: str,
        headers: Mapping[str, str],
        connect_timeout_ms: int,
        read_timeout_ms: int,
        max_redirects: int,
    ) -> TransportResponse:
        if not path_and_query.startswith("/"):
            raise TransportError("request path must be absolute within the API origin")
        url = urljoin(api_origin.rstrip("/") + "/", path_and_query.lstrip("/"))
        if _origin(url) != _origin(api_origin):
            raise TransportError("request crossed the frozen GitHub API origin")
        request = Request(url, method="GET", headers=dict(headers))
        opener = build_opener(_SameOriginRedirectHandler(api_origin, max_redirects))
        timeout_seconds = connect_timeout_ms / 1000
        try:
            with opener.open(request, timeout=timeout_seconds) as response:
                final_url = response.geturl()
                if _origin(final_url) != _origin(api_origin):
                    raise TransportError("final response crossed the GitHub API origin")
                return TransportResponse(
                    status=int(response.status),
                    headers={
                        key.lower(): value for key, value in response.headers.items()
                    },
                    body=_read_bounded(response, read_timeout_ms),
                    final_url=final_url,
                )
        except HTTPError as exc:
            final_url = exc.geturl()
            if _origin(final_url) != _origin(api_origin):
                raise TransportError(
                    "error response crossed the GitHub API origin"
                ) from None
            return TransportResponse(
                status=int(exc.code),
                headers={key.lower(): value for key, value in exc.headers.items()},
                body=_read_bounded(exc, read_timeout_ms),
                final_url=final_url,
            )
        except TransportError:
            raise
        except (URLError, TimeoutError, OSError) as exc:
            raise TransportError("bounded GitHub network request failed") from exc
