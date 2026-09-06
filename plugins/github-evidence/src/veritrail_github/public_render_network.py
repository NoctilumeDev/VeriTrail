from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from veritrail_github.errors import CollectionError


DEFAULT_MAIN_DOCUMENT_LIMIT_BYTES = 8 * 1024 * 1024
DEFAULT_TOTAL_RESPONSE_BODY_LIMIT_BYTES = 32 * 1024 * 1024
DEFAULT_READ_CHUNK_BYTES = 64 * 1024


class PublicRenderNetworkError(CollectionError):
    """A bounded response-stage observation cannot continue safely."""


class ResponseBodyBudgetExceeded(PublicRenderNetworkError):
    def __init__(self, *, scope: str, observed_bytes: int, limit_bytes: int) -> None:
        self.scope = scope
        self.observed_bytes = observed_bytes
        self.limit_bytes = limit_bytes
        super().__init__(
            f"P2 {scope} response-body budget exceeded: "
            f"{observed_bytes} > {limit_bytes} bytes"
        )


class ResponseContentEncodingRejected(PublicRenderNetworkError):
    def __init__(self, encoding: str) -> None:
        self.encoding = encoding
        super().__init__(
            "P2 response body requires identity content encoding; "
            f"observed {encoding!r}"
        )


@dataclass(frozen=True)
class ResponseBodyPolicy:
    max_main_document_response_body_bytes: int = DEFAULT_MAIN_DOCUMENT_LIMIT_BYTES
    max_total_response_body_bytes: int = DEFAULT_TOTAL_RESPONSE_BODY_LIMIT_BYTES
    response_body_read_chunk_bytes: int = DEFAULT_READ_CHUNK_BYTES

    def __post_init__(self) -> None:
        values = {
            "max_main_document_response_body_bytes": (
                self.max_main_document_response_body_bytes
            ),
            "max_total_response_body_bytes": self.max_total_response_body_bytes,
            "response_body_read_chunk_bytes": self.response_body_read_chunk_bytes,
        }
        for name, value in values.items():
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if (
            self.max_main_document_response_body_bytes
            > self.max_total_response_body_bytes
        ):
            raise ValueError(
                "main-document response-body budget cannot exceed total budget"
            )
        if self.response_body_read_chunk_bytes > DEFAULT_READ_CHUNK_BYTES:
            raise ValueError("P2 response-body reads cannot exceed 65536 bytes")


@dataclass(frozen=True)
class ResponseBodySnapshot:
    total_response_body_bytes: int
    main_document_response_body_bytes: int
    delivered_response_body_bytes: int
    completed_responses: int
    closed_streams: int
    active_streams: int
    failure: str | None


class ResponseBodyBudget:
    """Own the monotonic, session-wide P2 response-body counters."""

    def __init__(self, policy: ResponseBodyPolicy) -> None:
        self._policy = policy
        self.total_bytes = 0
        self.main_document_bytes = 0

    def consume(self, byte_count: int, *, main_document: bool) -> None:
        if isinstance(byte_count, bool) or not isinstance(byte_count, int):
            raise TypeError("response-body byte count must be an integer")
        if byte_count < 0 or byte_count > self._policy.response_body_read_chunk_bytes:
            raise ValueError("response-body byte count exceeds the frozen read chunk")
        self.total_bytes += byte_count
        if main_document:
            self.main_document_bytes += byte_count
            if (
                self.main_document_bytes
                > self._policy.max_main_document_response_body_bytes
            ):
                raise ResponseBodyBudgetExceeded(
                    scope="main-document",
                    observed_bytes=self.main_document_bytes,
                    limit_bytes=(
                        self._policy.max_main_document_response_body_bytes
                    ),
                )
        if self.total_bytes > self._policy.max_total_response_body_bytes:
            raise ResponseBodyBudgetExceeded(
                scope="total",
                observed_bytes=self.total_bytes,
                limit_bytes=self._policy.max_total_response_body_bytes,
            )


class ResponseStageBodyController:
    """Meter paused CDP response streams before replaying them to Chromium."""

    def __init__(
        self,
        session: Any,
        *,
        main_frame_id: str,
        policy: ResponseBodyPolicy | None = None,
    ) -> None:
        if not isinstance(main_frame_id, str) or not main_frame_id:
            raise ValueError("main_frame_id must be a non-empty CDP frame id")
        self._session = session
        self._main_frame_id = main_frame_id
        self._policy = policy or ResponseBodyPolicy()
        self._budget = ResponseBodyBudget(self._policy)
        self._active_streams: set[str] = set()
        self._failure: PublicRenderNetworkError | None = None
        self._installed = False
        self._delivered_bytes = 0
        self._completed_responses = 0
        self._closed_streams = 0

    def install(self) -> None:
        if self._installed:
            raise RuntimeError("P2 response-stage controller is already installed")
        self._session.send("Network.enable")
        self._session.send(
            "Network.setExtraHTTPHeaders",
            {"headers": {"Accept-Encoding": "identity"}},
        )
        self._session.send(
            "Fetch.enable",
            {
                "patterns": [
                    {"urlPattern": "*", "requestStage": "Response"}
                ]
            },
        )
        self._session.on("Fetch.requestPaused", self._on_request_paused)
        self._installed = True

    def close(self) -> None:
        for handle in tuple(self._active_streams):
            self._close_stream(handle)
        if not self._installed:
            return
        try:
            self._session.remove_listener(
                "Fetch.requestPaused", self._on_request_paused
            )
        except Exception:
            pass
        try:
            self._session.send("Fetch.disable")
        except Exception:
            pass
        self._installed = False

    def raise_if_failed(self) -> None:
        if self._failure is not None:
            raise self._failure

    def snapshot(self) -> ResponseBodySnapshot:
        return ResponseBodySnapshot(
            total_response_body_bytes=self._budget.total_bytes,
            main_document_response_body_bytes=self._budget.main_document_bytes,
            delivered_response_body_bytes=self._delivered_bytes,
            completed_responses=self._completed_responses,
            closed_streams=self._closed_streams,
            active_streams=len(self._active_streams),
            failure=type(self._failure).__name__ if self._failure else None,
        )

    def _on_request_paused(self, params: Mapping[str, Any]) -> None:
        request_id = params.get("requestId")
        if not isinstance(request_id, str) or not request_id:
            self._record_failure(
                PublicRenderNetworkError(
                    "P2 response-stage pause omitted its request id"
                )
            )
            self._stop_loading()
            return
        if self._failure is not None:
            self._fail_request(request_id)
            return
        try:
            self._handle_response(request_id, params)
        except PublicRenderNetworkError as error:
            self._record_failure(error)
            self._fail_request(request_id)
            self._stop_loading()
        except Exception as error:
            self._record_failure(
                PublicRenderNetworkError(
                    "P2 response-stage stream handling failed: "
                    f"{type(error).__name__}"
                )
            )
            self._fail_request(request_id)
            self._stop_loading()

    def _handle_response(
        self, request_id: str, params: Mapping[str, Any]
    ) -> None:
        status = params.get("responseStatusCode")
        if isinstance(status, bool) or not isinstance(status, int):
            raise PublicRenderNetworkError(
                "P2 response-stage pause omitted its HTTP status"
            )
        request = params.get("request")
        method = request.get("method") if isinstance(request, Mapping) else None
        if not isinstance(method, str):
            raise PublicRenderNetworkError(
                "P2 response-stage pause omitted its request method"
            )
        headers = _validated_response_headers(params.get("responseHeaders", []))
        if _has_no_render_body(method, status):
            self._fulfill(
                request_id,
                status,
                headers,
                b"",
                include_content_length=False,
            )
            return

        encoding = _content_encoding(headers)
        if encoding not in (None, "identity"):
            raise ResponseContentEncodingRejected(encoding)

        main_document = (
            params.get("resourceType") == "Document"
            and params.get("frameId") == self._main_frame_id
        )
        result = self._session.send(
            "Fetch.takeResponseBodyAsStream", {"requestId": request_id}
        )
        handle = result.get("stream") if isinstance(result, Mapping) else None
        if not isinstance(handle, str) or not handle:
            raise PublicRenderNetworkError(
                "P2 response-stage pause did not yield a body stream"
            )
        self._active_streams.add(handle)
        chunks: list[bytes] = []
        try:
            while True:
                chunk = self._session.send(
                    "IO.read",
                    {
                        "handle": handle,
                        "size": self._policy.response_body_read_chunk_bytes,
                    },
                )
                data = _decode_io_chunk(chunk)
                self._budget.consume(len(data), main_document=main_document)
                chunks.append(data)
                if chunk.get("eof") is True:
                    break
        finally:
            self._close_stream(handle)

        body = b"".join(chunks)
        self._fulfill(request_id, status, headers, body)

    def _fulfill(
        self,
        request_id: str,
        status: int,
        headers: Sequence[Mapping[str, str]],
        body: bytes,
        *,
        include_content_length: bool = True,
    ) -> None:
        self._session.send(
            "Fetch.fulfillRequest",
            {
                "requestId": request_id,
                "responseCode": status,
                "responseHeaders": _replay_headers(
                    headers,
                    len(body) if include_content_length else None,
                ),
                "body": base64.b64encode(body).decode("ascii"),
            },
        )
        self._delivered_bytes += len(body)
        self._completed_responses += 1

    def _close_stream(self, handle: str) -> None:
        if handle not in self._active_streams:
            return
        try:
            self._session.send("IO.close", {"handle": handle})
        except Exception:
            pass
        self._active_streams.discard(handle)
        self._closed_streams += 1

    def _record_failure(self, error: PublicRenderNetworkError) -> None:
        if self._failure is None:
            self._failure = error

    def _fail_request(self, request_id: str) -> None:
        try:
            self._session.send(
                "Fetch.failRequest",
                {"requestId": request_id, "errorReason": "BlockedByClient"},
            )
        except Exception:
            pass

    def _stop_loading(self) -> None:
        try:
            self._session.send("Page.stopLoading")
        except Exception:
            pass


def _decode_io_chunk(chunk: Any) -> bytes:
    if not isinstance(chunk, Mapping):
        raise PublicRenderNetworkError("P2 body stream returned a non-object chunk")
    data = chunk.get("data")
    if not isinstance(data, str):
        raise PublicRenderNetworkError("P2 body stream omitted chunk data")
    if chunk.get("base64Encoded") is True:
        try:
            return base64.b64decode(data, validate=True)
        except ValueError as error:
            raise PublicRenderNetworkError(
                "P2 body stream returned invalid base64"
            ) from error
    return data.encode("utf-8")


def _validated_response_headers(value: Any) -> tuple[dict[str, str], ...]:
    if not isinstance(value, list):
        raise PublicRenderNetworkError("P2 response headers are not a list")
    normalized: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise PublicRenderNetworkError("P2 response header is not an object")
        name = item.get("name")
        header_value = item.get("value")
        if not isinstance(name, str) or not isinstance(header_value, str):
            raise PublicRenderNetworkError("P2 response header is incomplete")
        normalized.append({"name": name, "value": header_value})
    return tuple(normalized)


def _content_encoding(headers: Sequence[Mapping[str, str]]) -> str | None:
    values = [
        item["value"].strip().casefold()
        for item in headers
        if item["name"].casefold() == "content-encoding"
    ]
    if not values:
        return None
    return ",".join(values)


def _has_no_render_body(method: str, status: int) -> bool:
    return (
        method.casefold() == "head"
        or 100 <= status < 200
        or status in {204, 304}
        or 300 <= status < 400
    )


def _replay_headers(
    headers: Sequence[Mapping[str, str]], body_length: int | None
) -> list[dict[str, str]]:
    connection_tokens: set[str] = set()
    for item in headers:
        if item["name"].casefold() == "connection":
            connection_tokens.update(
                token.strip().casefold()
                for token in item["value"].split(",")
                if token.strip()
            )
    excluded = {
        "connection",
        "content-encoding",
        "content-length",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "proxy-connection",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
        *connection_tokens,
    }
    replay = [
        {"name": item["name"], "value": item["value"]}
        for item in headers
        if item["name"].casefold() not in excluded
    ]
    if body_length is not None:
        replay.append({"name": "Content-Length", "value": str(body_length)})
    return replay
