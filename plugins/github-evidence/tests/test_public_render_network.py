from __future__ import annotations

import base64
import gzip
import threading
import time
import unittest
from collections import defaultdict, deque
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from veritrail_github.public_render_network import (
    DEFAULT_MAIN_DOCUMENT_LIMIT_BYTES,
    DEFAULT_READ_CHUNK_BYTES,
    DEFAULT_TOTAL_RESPONSE_BODY_LIMIT_BYTES,
    PublicRenderNetworkError,
    ResponseBodyBudget,
    ResponseBodyBudgetExceeded,
    ResponseBodyPolicy,
    ResponseContentEncodingRejected,
    ResponseStageBodyController,
)


class _MemoryCdpSession:
    def __init__(self) -> None:
        self.commands: list[tuple[str, dict[str, Any] | None]] = []
        self.listeners: dict[str, Any] = {}
        self.responses: dict[str, deque[dict[str, Any]]] = defaultdict(deque)

    def send(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.commands.append((method, params))
        if self.responses[method]:
            return self.responses[method].popleft()
        return {}

    def queue(self, method: str, response: dict[str, Any]) -> None:
        self.responses[method].append(response)

    def on(self, event: str, listener: Any) -> None:
        self.listeners[event] = listener

    def remove_listener(self, event: str, listener: Any) -> None:
        if self.listeners.get(event) == listener:
            del self.listeners[event]

    def emit(self, event: str, params: dict[str, Any]) -> None:
        self.listeners[event](params)


@dataclass
class _ResponseState:
    expected: int
    sent: int = 0
    completed: bool = False
    disconnected: bool = False
    accept_encoding: str | None = None
    done: threading.Event = field(default_factory=threading.Event)


class _SlowFixture:
    def __init__(
        self,
        responses: dict[str, tuple[bytes, str]],
        *,
        content_encodings: dict[str, str] | None = None,
    ) -> None:
        self.responses = responses
        self.content_encodings = content_encodings or {}
        self.states = {
            path: _ResponseState(expected=len(payload))
            for path, (payload, _media_type) in responses.items()
        }
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.0"

            def do_GET(self) -> None:
                found = fixture.responses.get(self.path)
                if found is None:
                    self.send_error(404)
                    return
                payload, media_type = found
                state = fixture.states[self.path]
                state.accept_encoding = self.headers.get("Accept-Encoding")
                self.send_response(200)
                self.send_header("Content-Type", media_type)
                self.send_header("Content-Length", str(len(payload)))
                content_encoding = fixture.content_encodings.get(self.path)
                if content_encoding is not None:
                    self.send_header("Content-Encoding", content_encoding)
                self.send_header("Connection", "close")
                self.end_headers()
                self.close_connection = True
                try:
                    for offset in range(0, len(payload), DEFAULT_READ_CHUNK_BYTES):
                        chunk = payload[offset : offset + DEFAULT_READ_CHUNK_BYTES]
                        self.wfile.write(chunk)
                        self.wfile.flush()
                        state.sent += len(chunk)
                        time.sleep(0.002)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    state.disconnected = True
                else:
                    state.completed = True
                finally:
                    state.done.set()

            def log_message(self, format: str, *args: Any) -> None:
                del format, args

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def origin(self) -> str:
        host, port = self._server.server_address
        return f"http://{host}:{port}"

    def __enter__(self) -> "_SlowFixture":
        self._thread.start()
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        del exc_type, exc, traceback
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)


class ResponseBodyBudgetTests(unittest.TestCase):
    def test_policy_rejects_expansion_beyond_frozen_chunk(self) -> None:
        with self.assertRaisesRegex(ValueError, "65536"):
            ResponseBodyPolicy(response_body_read_chunk_bytes=65537)

    def test_total_budget_is_shared_across_responses(self) -> None:
        policy = ResponseBodyPolicy(
            max_main_document_response_body_bytes=8,
            max_total_response_body_bytes=10,
            response_body_read_chunk_bytes=8,
        )
        budget = ResponseBodyBudget(policy)
        budget.consume(6, main_document=True)
        budget.consume(4, main_document=False)
        with self.assertRaises(ResponseBodyBudgetExceeded) as raised:
            budget.consume(1, main_document=False)
        self.assertEqual("total", raised.exception.scope)
        self.assertEqual(11, raised.exception.observed_bytes)


class ResponseStageBodyControllerTests(unittest.TestCase):
    def test_base64_cdp_chunk_is_counted_as_decoded_body_bytes(self) -> None:
        session = _MemoryCdpSession()
        raw_body = b"\x00\xffbinary"
        session.queue("Fetch.takeResponseBodyAsStream", {"stream": "stream-1"})
        session.queue(
            "IO.read",
            {
                "data": base64.b64encode(raw_body).decode("ascii"),
                "base64Encoded": True,
                "eof": True,
            },
        )
        controller = ResponseStageBodyController(session, main_frame_id="main")
        controller.install()

        session.emit(
            "Fetch.requestPaused",
            {
                "requestId": "binary-1",
                "frameId": "child",
                "resourceType": "Other",
                "responseStatusCode": 200,
                "request": {"method": "GET"},
                "responseHeaders": [],
            },
        )

        controller.raise_if_failed()
        fulfill = next(
            params
            for method, params in session.commands
            if method == "Fetch.fulfillRequest"
        )
        self.assertEqual(
            base64.b64encode(raw_body).decode("ascii"), fulfill["body"]
        )
        snapshot = controller.snapshot()
        self.assertEqual(len(raw_body), snapshot.total_response_body_bytes)
        self.assertEqual(0, snapshot.main_document_response_body_bytes)
        self.assertEqual(len(raw_body), snapshot.delivered_response_body_bytes)
        self.assertEqual(1, snapshot.closed_streams)
        controller.close()

    def test_redirect_is_replayed_as_an_empty_control_response(self) -> None:
        session = _MemoryCdpSession()
        controller = ResponseStageBodyController(session, main_frame_id="main")
        controller.install()

        session.emit(
            "Fetch.requestPaused",
            {
                "requestId": "redirect-1",
                "frameId": "main",
                "resourceType": "Document",
                "responseStatusCode": 302,
                "request": {"method": "GET"},
                "responseHeaders": [
                    {"name": "Location", "value": "/next"},
                    {"name": "Content-Length", "value": "99"},
                ],
            },
        )

        controller.raise_if_failed()
        methods = [method for method, _params in session.commands]
        self.assertNotIn("Fetch.takeResponseBodyAsStream", methods)
        fulfill = next(
            params
            for method, params in session.commands
            if method == "Fetch.fulfillRequest"
        )
        self.assertEqual("", fulfill["body"])
        self.assertIn(
            {"name": "Location", "value": "/next"},
            fulfill["responseHeaders"],
        )
        self.assertFalse(
            any(
                item["name"].casefold() == "content-length"
                for item in fulfill["responseHeaders"]
            )
        )
        snapshot = controller.snapshot()
        self.assertEqual(1, snapshot.completed_responses)
        self.assertEqual(0, snapshot.total_response_body_bytes)
        controller.close()

    def test_replay_normalizes_transport_headers_and_preserves_duplicates(
        self,
    ) -> None:
        session = _MemoryCdpSession()
        raw_body = b"body"
        session.queue("Fetch.takeResponseBodyAsStream", {"stream": "stream-1"})
        session.queue(
            "IO.read",
            {"data": raw_body.decode("ascii"), "eof": True},
        )
        controller = ResponseStageBodyController(session, main_frame_id="main")
        controller.install()

        session.emit(
            "Fetch.requestPaused",
            {
                "requestId": "headers-1",
                "frameId": "main",
                "resourceType": "Document",
                "responseStatusCode": 200,
                "request": {"method": "GET"},
                "responseHeaders": [
                    {"name": "Connection", "value": "keep-alive, X-Hop"},
                    {"name": "Keep-Alive", "value": "timeout=5"},
                    {"name": "X-Hop", "value": "remove-me"},
                    {"name": "Transfer-Encoding", "value": "chunked"},
                    {"name": "Content-Length", "value": "999"},
                    {"name": "Set-Cookie", "value": "first=1"},
                    {"name": "Set-Cookie", "value": "second=2"},
                ],
            },
        )

        controller.raise_if_failed()
        fulfill = next(
            params
            for method, params in session.commands
            if method == "Fetch.fulfillRequest"
        )
        self.assertEqual(
            [
                {"name": "Set-Cookie", "value": "first=1"},
                {"name": "Set-Cookie", "value": "second=2"},
                {"name": "Content-Length", "value": str(len(raw_body))},
            ],
            fulfill["responseHeaders"],
        )
        controller.close()

    def test_all_control_responses_omit_synthetic_body_length(self) -> None:
        cases = (
            ("HEAD", 200),
            ("GET", 101),
            ("GET", 204),
            ("GET", 304),
            ("GET", 307),
        )
        for index, (method, status) in enumerate(cases):
            with self.subTest(method=method, status=status):
                session = _MemoryCdpSession()
                controller = ResponseStageBodyController(
                    session, main_frame_id="main"
                )
                controller.install()
                session.emit(
                    "Fetch.requestPaused",
                    {
                        "requestId": f"control-{index}",
                        "frameId": "main",
                        "resourceType": "Document",
                        "responseStatusCode": status,
                        "request": {"method": method},
                        "responseHeaders": [
                            {"name": "Content-Length", "value": "999"},
                            {"name": "Transfer-Encoding", "value": "chunked"},
                        ],
                    },
                )
                controller.raise_if_failed()
                fulfill = next(
                    params
                    for command, params in session.commands
                    if command == "Fetch.fulfillRequest"
                )
                self.assertEqual("", fulfill["body"])
                self.assertFalse(
                    any(
                        item["name"].casefold()
                        in {"content-length", "transfer-encoding"}
                        for item in fulfill["responseHeaders"]
                    )
                )
                controller.close()

    def test_exposed_non_identity_header_is_rejected_before_stream_read(self) -> None:
        session = _MemoryCdpSession()
        controller = ResponseStageBodyController(session, main_frame_id="main")
        controller.install()

        session.emit(
            "Fetch.requestPaused",
            {
                "requestId": "request-1",
                "frameId": "main",
                "resourceType": "Document",
                "responseStatusCode": 200,
                "request": {"method": "GET"},
                "responseHeaders": [
                    {"name": "Content-Encoding", "value": "gzip"}
                ],
            },
        )

        with self.assertRaises(ResponseContentEncodingRejected):
            controller.raise_if_failed()
        methods = [method for method, _params in session.commands]
        self.assertNotIn("Fetch.takeResponseBodyAsStream", methods)
        self.assertNotIn("IO.read", methods)
        self.assertIn("Fetch.failRequest", methods)
        self.assertIn("Page.stopLoading", methods)
        controller.close()

    def test_main_document_limit_interrupts_slow_producer_before_completion(
        self,
    ) -> None:
        payload = b"<main>" + b"x" * (12 * 1024 * 1024) + b"</main>"
        with _SlowFixture({"/large": (payload, "text/html; charset=utf-8")}) as fixture:
            error, snapshot = self._navigate_until_budget_failure(
                f"{fixture.origin}/large"
            )
            state = fixture.states["/large"]
            self.assertTrue(state.done.wait(5))

        self.assertEqual("main-document", error.scope)
        self.assertLessEqual(
            error.observed_bytes,
            DEFAULT_MAIN_DOCUMENT_LIMIT_BYTES + DEFAULT_READ_CHUNK_BYTES,
        )
        self.assertEqual(0, snapshot.delivered_response_body_bytes)
        self.assertEqual(0, snapshot.active_streams)
        self.assertFalse(state.completed)
        self.assertTrue(state.disconnected)
        self.assertLess(state.sent, state.expected)
        self.assertEqual("identity", state.accept_encoding)

    def test_total_limit_interrupts_slow_subresource_before_completion(self) -> None:
        document = b'<script src="/large.js"></script><main>after</main>'
        script = b"x" * (40 * 1024 * 1024)
        responses = {
            "/": (document, "text/html; charset=utf-8"),
            "/large.js": (script, "application/javascript"),
        }
        with _SlowFixture(responses) as fixture:
            error, snapshot = self._navigate_until_budget_failure(fixture.origin + "/")
            state = fixture.states["/large.js"]
            self.assertTrue(state.done.wait(5))

        self.assertEqual("total", error.scope)
        self.assertLessEqual(
            error.observed_bytes,
            DEFAULT_TOTAL_RESPONSE_BODY_LIMIT_BYTES + DEFAULT_READ_CHUNK_BYTES,
        )
        self.assertEqual(len(document), snapshot.delivered_response_body_bytes)
        self.assertEqual(0, snapshot.active_streams)
        self.assertFalse(state.completed)
        self.assertTrue(state.disconnected)
        self.assertLess(state.sent, state.expected)
        self.assertEqual("identity", state.accept_encoding)

    def test_non_identity_encoding_fails_before_body_stream_or_delivery(self) -> None:
        payload = gzip.compress(b"x" * (2 * 1024 * 1024))
        with _SlowFixture(
            {"/encoded": (payload, "text/html")},
            content_encodings={"/encoded": "gzip"},
        ) as fixture:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                session = context.new_cdp_session(page)
                main_frame_id = session.send("Page.getFrameTree")["frameTree"][
                    "frame"
                ]["id"]
                controller = ResponseStageBodyController(
                    session, main_frame_id=main_frame_id
                )
                controller.install()
                try:
                    try:
                        page.goto(
                            fixture.origin + "/encoded",
                            wait_until="domcontentloaded",
                            timeout=15000,
                        )
                    except PlaywrightError:
                        pass
                    with self.assertRaises(PublicRenderNetworkError) as raised:
                        controller.raise_if_failed()
                    self.assertNotIsInstance(
                        raised.exception, ResponseBodyBudgetExceeded
                    )
                    snapshot = controller.snapshot()
                finally:
                    controller.close()
                    context.close()
                    browser.close()
            state = fixture.states["/encoded"]
            self.assertTrue(state.done.wait(5))

        self.assertEqual(0, snapshot.total_response_body_bytes)
        self.assertEqual(0, snapshot.delivered_response_body_bytes)
        self.assertEqual(0, snapshot.closed_streams)
        self.assertEqual(0, snapshot.active_streams)
        self.assertEqual("identity", state.accept_encoding)

    def test_bounded_response_is_replayed_byte_for_byte(self) -> None:
        document = b"<main>bounded response</main>"
        with _SlowFixture({"/": (document, "text/html; charset=utf-8")}) as fixture:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                session = context.new_cdp_session(page)
                main_frame_id = session.send("Page.getFrameTree")["frameTree"][
                    "frame"
                ]["id"]
                controller = ResponseStageBodyController(
                    session, main_frame_id=main_frame_id
                )
                controller.install()
                try:
                    response = page.goto(
                        fixture.origin + "/",
                        wait_until="domcontentloaded",
                        timeout=15000,
                    )
                    controller.raise_if_failed()
                    snapshot = controller.snapshot()
                    self.assertIsNotNone(response)
                    self.assertEqual(200, response.status)
                    self.assertEqual(
                        "bounded response", page.locator("main").inner_text()
                    )
                finally:
                    controller.close()
                    context.close()
                    browser.close()

        self.assertEqual(len(document), snapshot.total_response_body_bytes)
        self.assertEqual(len(document), snapshot.main_document_response_body_bytes)
        self.assertEqual(len(document), snapshot.delivered_response_body_bytes)
        self.assertEqual(1, snapshot.completed_responses)
        self.assertEqual(1, snapshot.closed_streams)
        self.assertEqual(0, snapshot.active_streams)

    def _navigate_until_budget_failure(
        self, url: str
    ) -> tuple[ResponseBodyBudgetExceeded, Any]:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            session = context.new_cdp_session(page)
            main_frame_id = session.send("Page.getFrameTree")["frameTree"]["frame"][
                "id"
            ]
            controller = ResponseStageBodyController(
                session, main_frame_id=main_frame_id
            )
            controller.install()
            try:
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                except PlaywrightError:
                    pass
                with self.assertRaises(ResponseBodyBudgetExceeded) as raised:
                    controller.raise_if_failed()
                snapshot = controller.snapshot()
            finally:
                controller.close()
                context.close()
                browser.close()
        return raised.exception, snapshot


if __name__ == "__main__":
    unittest.main()
