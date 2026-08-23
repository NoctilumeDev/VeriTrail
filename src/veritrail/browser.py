from __future__ import annotations

import asyncio
import importlib.metadata
import math
from collections import Counter
from datetime import datetime, timezone
from time import monotonic
from typing import Any, Callable, Protocol
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from veritrail.canonical import sha256_json
from veritrail.evidence import (
    EvidenceAttachment,
    ImportedEvidence,
    create_attachment,
    import_evidence_document,
)
from veritrail.errors import ValidationError
from veritrail.stop_control import StopRequested, requested_stop_reason

COLLECTOR_VERSION = "browser-playwright/0.1"
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
MAX_NETWORK_EVENTS = 1000
MAX_CONSOLE_EVENTS = 500
MAX_PAGE_ERRORS = 100
MAX_EVENT_TEXT = 4096


class _BrowserLifecycleObserver(Protocol):
    def playwright_started(self, playwright: Any) -> None: ...

    def browser_started(self, browser: Any) -> None: ...

    def checkpoint(self, browser: Any) -> None: ...

    def before_browser_close(self, browser: Any) -> None: ...

    def after_browser_close(self) -> None: ...

    def failed(self, stage: str, error_type: str) -> None: ...


def _settle_playwright_start(playwright: Any) -> None:
    """Finish Playwright's pinned sync-start handshake before ownership hooks run.

    Playwright 1.62 yields its sync API object to the caller before the private
    connection initialization task has returned. If an ownership hook rejects
    the driver at that exact boundary, ``stop()`` can close the owned event loop
    with the task still pending. Draining that already-started task keeps the
    early-failure path deterministic and prevents a later test or Run from
    receiving the previous lifecycle's ``Task was destroyed`` warning.

    The project pins Playwright and already needs its private connection for the
    Windows Job ownership proof. Lightweight test doubles deliberately omit
    those internals, so there is nothing to settle for them.
    """

    sync_wait = getattr(playwright, "_sync", None)
    implementation = getattr(playwright, "_impl_obj", None)
    connection = getattr(implementation, "_connection", None)
    init_task = getattr(connection, "_init_task", None)
    if sync_wait is None or init_task is None or init_task.done():
        return
    sync_wait(asyncio.wait_for(asyncio.shield(init_task), timeout=1.0))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _origin(url: str) -> str | None:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        return None
    if parsed.scheme != "http" or parsed.hostname not in {"localhost", "127.0.0.1"} or port is None:
        return None
    return f"http://{parsed.hostname}:{port}"


def _websocket_origin(url: str) -> str | None:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        return None
    if parsed.scheme != "ws" or parsed.hostname not in {"localhost", "127.0.0.1"} or port is None:
        return None
    return f"ws://{parsed.hostname}:{port}"


def sanitize_url(url: str) -> str:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        return "[INVALID_URL]"
    if parsed.scheme not in {"http", "https"}:
        return f"{parsed.scheme}:[OMITTED]" if parsed.scheme else "[INVALID_URL]"
    if parsed.hostname not in {"localhost", "127.0.0.1"}:
        return "[BLOCKED_NON_LOOPBACK_URL]"
    hostname = parsed.hostname or ""
    netloc = hostname
    if port is not None:
        netloc = f"{hostname}:{port}"
    query = urlencode([(key, "[REDACTED]") for key, _ in parse_qsl(parsed.query, keep_blank_values=True)])
    return urlunsplit((parsed.scheme, netloc, parsed.path or "/", query, ""))


def _declared_browser_observations(plan: dict[str, Any], browser_version: str) -> dict[str, Any]:
    known = {
        "browser_engine": "chromium",
        "browser_headless": plan["browser"]["headless"],
        "browser_version": browser_version,
        "viewport_profile_count": len(plan["browser"]["viewports"]),
    }
    declared = {item["name"] for item in plan["variables"]}
    return {name: value for name, value in known.items() if name in declared}


def _step_entry(viewport: str, step_id: str, action: str) -> dict[str, Any]:
    return {
        "viewport": viewport,
        "step_id": step_id,
        "action": action,
        "started_at": _utc_now(),
        "ended_at": None,
        "elapsed_ms": None,
        "status": "RUNNING",
        "error_type": None,
        "error": None,
    }


def _finish_step(
    entry: dict[str, Any], started: float, *, error: BaseException | None = None
) -> None:
    entry["ended_at"] = _utc_now()
    entry["elapsed_ms"] = round((monotonic() - started) * 1000, 3)
    if error is None:
        entry["status"] = "PASSED"
    else:
        entry["status"] = "FAILED"
        entry["error_type"] = type(error).__name__
        entry["error"] = str(error)


def _execute_step(
    *,
    page: Any,
    step: dict[str, Any],
    viewport_name: str,
    timeout_ms: int,
    screenshot_index: int,
    check_stop: Callable[[], None],
) -> tuple[EvidenceAttachment | None, dict[str, Any] | None]:
    check_stop()
    action = step["action"]
    if action == "goto":
        page.goto(step["url"], wait_until="load", timeout=timeout_ms)
    elif action == "click":
        page.locator(step["selector"]).click(timeout=timeout_ms)
    elif action == "fill":
        page.locator(step["selector"]).fill(step["value"], timeout=timeout_ms)
    elif action == "press":
        page.locator(step["selector"]).press(step["value"], timeout=timeout_ms)
    elif action == "expect_visible":
        page.locator(step["selector"]).wait_for(state="visible", timeout=timeout_ms)
    elif action == "expect_text":
        locator = page.locator(step["selector"])
        locator.wait_for(state="visible", timeout=timeout_ms)
        deadline = monotonic() + timeout_ms / 1000
        while step["value"] not in locator.inner_text(timeout=timeout_ms):
            check_stop()
            if monotonic() >= deadline:
                raise TimeoutError(
                    f"expected text was not observed for step {step['id']!r}"
                )
            page.wait_for_timeout(50)
    elif action == "screenshot":
        content = page.screenshot(full_page=False, type="png", timeout=timeout_ms)
        logical_name = f"{viewport_name}-{step['name']}"
        provisional_path = (
            f"attachments/browser/{viewport_name}/"
            f"{screenshot_index:03d}-{step['name']}.png"
        )
        attachment = create_attachment(
            path=provisional_path,
            content=content,
            media_type="image/png",
            logical_name=logical_name,
        )
        reference = {
            "name": step["name"],
            "viewport": viewport_name,
            "step_id": step["id"],
            "path": attachment.path,
            "sha256": attachment.sha256,
            "size": attachment.size,
            "media_type": attachment.media_type,
        }
        return attachment, reference
    return None, None


def _collect_browser_evidence(
    plan: dict[str, Any],
    *,
    lifecycle_observer: _BrowserLifecycleObserver | None = None,
    cancel_event: object | None = None,
    lifecycle_deadline: float | None = None,
    integrity_check: Callable[[], None] | None = None,
) -> ImportedEvidence:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise ValidationError(
            ["browser-capture requires the 'browser' extra: install VeriTrail[browser]"]
        ) from exc

    policy = plan["browser"]

    def check_stop() -> None:
        reason = requested_stop_reason(cancel_event)
        if reason is not None:
            raise StopRequested(reason)
        if lifecycle_deadline is not None and monotonic() >= lifecycle_deadline:
            raise StopRequested("LIFECYCLE_TIMEOUT")
        if integrity_check is not None:
            integrity_check()

    def operation_timeout_ms() -> int:
        check_stop()
        timeout_ms = int(policy["timeout_ms"])
        if lifecycle_deadline is not None:
            remaining_ms = max(
                1,
                math.ceil((lifecycle_deadline - monotonic()) * 1000),
            )
            timeout_ms = min(timeout_ms, remaining_ms)
        return timeout_ms
    allowed_origins = {
        normalized
        for item in policy["allowed_origins"]
        if (normalized := _origin(item)) is not None
    }
    allowed_websocket_origins = {
        origin.replace("http://", "ws://", 1) for origin in allowed_origins
    }
    started_at = _utc_now()
    steps: list[dict[str, Any]] = []
    console: list[dict[str, Any]] = []
    page_errors: list[dict[str, Any]] = []
    network: list[dict[str, Any]] = []
    screenshots: list[dict[str, Any]] = []
    attachments: list[EvidenceAttachment] = []
    viewport_runs: list[dict[str, Any]] = []
    collection_errors: list[dict[str, str]] = []
    request_records: dict[int, dict[str, Any]] = {}
    browser_version = "unavailable"
    cleanup_complete = True
    browser = None

    def record_collection_error(collector: str, error_type: str) -> None:
        item = {"collector": collector, "error_type": error_type}
        if item not in collection_errors:
            collection_errors.append(item)

    def observe(method: str, *values: Any, required: bool = False) -> None:
        if lifecycle_observer is None:
            return
        try:
            getattr(lifecycle_observer, method)(*values)
        except Exception as exc:
            try:
                lifecycle_observer.failed(method, type(exc).__name__)
            except Exception:
                pass
            if required:
                raise

    check_stop()
    try:
        playwright_context = sync_playwright()
        playwright = playwright_context.start()
        try:
            _settle_playwright_start(playwright)
            # M10 uses this required hook to place the Playwright driver in the
            # owned Job before it is allowed to create Chromium descendants.
            observe("playwright_started", playwright, required=True)
        except Exception:
            try:
                playwright.stop()
            except Exception:
                pass
            raise
        try:
            check_stop()
            browser = playwright.chromium.launch(
                headless=policy["headless"],
                timeout=operation_timeout_ms(),
            )
        except Exception as exc:
            try:
                playwright.stop()
            except Exception:
                pass
            check_stop()
            raise ValidationError(
                [f"Chromium could not be launched ({type(exc).__name__}); install the pinned browser binary"]
            ) from exc
    except StopRequested:
        raise
    except ValidationError:
        raise
    except Exception as exc:
        raise ValidationError([f"Playwright could not start ({type(exc).__name__})"]) from exc

    browser_version = browser.version
    try:
        observe("browser_started", browser)
        check_stop()
        for viewport in policy["viewports"]:
            check_stop()
            viewport_name = viewport["name"]
            viewport_started = _utc_now()
            viewport_steps_start = len(steps)
            viewport_network_start = len(network)
            context = None
            page = None
            viewport_failed = False
            overflow_px = 0
            try:
                context = browser.new_context(
                    viewport={"width": viewport["width"], "height": viewport["height"]},
                    is_mobile=viewport["is_mobile"],
                    service_workers="block",
                )

                def route_request(route: Any, request: Any) -> None:
                    check_stop()
                    if (
                        _origin(request.url) not in allowed_origins
                        or len(network) >= MAX_NETWORK_EVENTS
                    ):
                        route.abort("blockedbyclient")
                    else:
                        route.continue_()

                context.route("**/*", route_request)

                def route_web_socket(route: Any) -> None:
                    check_stop()
                    if _websocket_origin(route.url) not in allowed_websocket_origins:
                        route.close()
                    else:
                        route.connect_to_server()

                context.route_web_socket("**/*", route_web_socket)
                page = context.new_page()

                def reject_unexpected_page(candidate: Any) -> None:
                    nonlocal cleanup_complete
                    if candidate is page:
                        return
                    record_collection_error(
                        f"page-set:{viewport_name}",
                        "UnexpectedPage",
                    )
                    try:
                        candidate.close()
                    except Exception as exc:
                        cleanup_complete = False
                        record_collection_error(
                            f"unexpected-page-close:{viewport_name}",
                            type(exc).__name__,
                        )

                def settle_and_enforce_page_set() -> None:
                    # Page creation is delivered through Playwright's event queue.
                    # Yield briefly at every sealed step boundary, then inspect the
                    # context as a second line of defence against a delayed callback.
                    page.wait_for_timeout(min(10, operation_timeout_ms()))
                    for candidate in list(context.pages):
                        if candidate is not page:
                            reject_unexpected_page(candidate)

                # The frozen browser evidence contract is deliberately single-page.
                # Register after creating the owned primary page so every later popup
                # is rejected at the BrowserContext boundary, before it can silently
                # escape the primary page's console/network/error listeners.
                context.on("page", reject_unexpected_page)
                observe("checkpoint", browser)
                page.set_default_timeout(operation_timeout_ms())
                page.set_default_navigation_timeout(operation_timeout_ms())

                def on_console(message: Any) -> None:
                    if len(console) >= MAX_CONSOLE_EVENTS:
                        record_collection_error("console", "EventLimitExceeded")
                        return
                    message_text = message.text
                    if len(message_text) > MAX_EVENT_TEXT:
                        message_text = message_text[:MAX_EVENT_TEXT] + "[TRUNCATED]"
                        record_collection_error("console", "EventTextTruncated")
                    console.append(
                        {
                            "captured_at": _utc_now(),
                            "viewport": viewport_name,
                            "level": message.type,
                            "text": message_text,
                        }
                    )

                def on_page_error(error: Any) -> None:
                    if len(page_errors) >= MAX_PAGE_ERRORS:
                        record_collection_error("page-errors", "EventLimitExceeded")
                        return
                    message_text = str(error)
                    if len(message_text) > MAX_EVENT_TEXT:
                        message_text = message_text[:MAX_EVENT_TEXT] + "[TRUNCATED]"
                        record_collection_error("page-errors", "EventTextTruncated")
                    page_errors.append(
                        {
                            "captured_at": _utc_now(),
                            "viewport": viewport_name,
                            "error_type": type(error).__name__,
                            "message": message_text,
                        }
                    )

                def on_request(request: Any) -> None:
                    if len(network) >= MAX_NETWORK_EVENTS:
                        record_collection_error("network", "EventLimitExceeded")
                        return
                    record = {
                        "sequence": len(network) + 1,
                        "captured_at": _utc_now(),
                        "viewport": viewport_name,
                        "method": request.method.upper(),
                        "url": sanitize_url(request.url),
                        "resource_type": request.resource_type,
                        "status": None,
                        "finished": False,
                        "failure": None,
                        "redirected_from": sanitize_url(request.redirected_from.url)
                        if request.redirected_from is not None
                        else None,
                    }
                    network.append(record)
                    request_records[id(request)] = record

                def on_response(response: Any) -> None:
                    record = request_records.get(id(response.request))
                    if record is not None:
                        record["status"] = response.status

                def on_request_finished(request: Any) -> None:
                    record = request_records.get(id(request))
                    if record is not None:
                        record["finished"] = True

                def on_request_failed(request: Any) -> None:
                    record = request_records.get(id(request))
                    if record is not None:
                        record["failure"] = str(request.failure or "request failed")

                page.on("console", on_console)
                page.on("pageerror", on_page_error)
                page.on("request", on_request)
                page.on("response", on_response)
                page.on("requestfinished", on_request_finished)
                page.on("requestfailed", on_request_failed)

                initial = _step_entry(viewport_name, "browser-start", "goto")
                steps.append(initial)
                initial_started = monotonic()
                try:
                    page.goto(
                        policy["start_url"],
                        wait_until="load",
                        timeout=operation_timeout_ms(),
                    )
                    check_stop()
                    _finish_step(initial, initial_started)
                except StopRequested as exc:
                    _finish_step(initial, initial_started, error=exc)
                    raise
                except Exception as exc:
                    check_stop()
                    _finish_step(initial, initial_started, error=exc)
                    viewport_failed = True
                finally:
                    observe("checkpoint", browser)

                if not viewport_failed:
                    screenshot_index = 0
                    for declared_step in policy["steps"]:
                        entry = _step_entry(viewport_name, declared_step["id"], declared_step["action"])
                        steps.append(entry)
                        step_started = monotonic()
                        try:
                            check_stop()
                            if declared_step["action"] == "screenshot":
                                screenshot_index += 1
                            attachment, reference = _execute_step(
                                page=page,
                                step=declared_step,
                                viewport_name=viewport_name,
                                timeout_ms=operation_timeout_ms(),
                                screenshot_index=screenshot_index,
                                check_stop=check_stop,
                            )
                            check_stop()
                            if attachment is not None and reference is not None:
                                attachments.append(attachment)
                                screenshots.append(reference)
                            settle_and_enforce_page_set()
                            _finish_step(entry, step_started)
                        except StopRequested as exc:
                            _finish_step(entry, step_started, error=exc)
                            raise
                        except Exception as exc:
                            check_stop()
                            _finish_step(entry, step_started, error=exc)
                            viewport_failed = True
                            break
                        finally:
                            observe("checkpoint", browser)
                if page is not None:
                    check_stop()
                    settle_and_enforce_page_set()
                    overflow_px = max(
                        0,
                        int(
                            page.evaluate(
                                "Math.ceil(document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                            )
                        ),
                    )
            except StopRequested:
                raise
            except Exception as exc:
                viewport_failed = True
                record_collection_error(f"viewport:{viewport_name}", type(exc).__name__)
            finally:
                if context is not None:
                    try:
                        context.close()
                    except Exception as exc:
                        cleanup_complete = False
                        record_collection_error(
                            f"context-close:{viewport_name}", type(exc).__name__
                        )
            viewport_runs.append(
                {
                    "name": viewport_name,
                    "width": viewport["width"],
                    "height": viewport["height"],
                    "is_mobile": viewport["is_mobile"],
                    "started_at": viewport_started,
                    "ended_at": _utc_now(),
                    "status": "FAILED" if viewport_failed else "PASSED",
                    "horizontal_overflow_px": overflow_px,
                    "step_count": len(steps) - viewport_steps_start,
                    "network_request_count": len(network) - viewport_network_start,
                }
            )
    finally:
        observe("before_browser_close", browser)
        try:
            browser.close()
        except Exception as exc:
            cleanup_complete = False
            record_collection_error("browser-close", type(exc).__name__)
        try:
            playwright.stop()
        except Exception as exc:
            cleanup_complete = False
            record_collection_error("playwright-stop", type(exc).__name__)
        observe("after_browser_close")

    failed_requests = [item for item in network if item["failure"] is not None]
    http_errors = [
        item for item in network if isinstance(item["status"], int) and item["status"] >= 400
    ]
    write_counts = Counter(
        (item["viewport"], item["method"], item["url"])
        for item in network
        if item["method"] in WRITE_METHODS
    )
    duplicate_write_groups = [
        {"viewport": key[0], "method": key[1], "url": key[2], "count": count}
        for key, count in sorted(write_counts.items())
        if count > 1
    ]
    all_steps_passed = bool(steps) and all(item["status"] == "PASSED" for item in steps)
    capture_complete = (
        all_steps_passed
        and all(item["status"] == "PASSED" for item in viewport_runs)
        and not collection_errors
        and cleanup_complete
    )
    ended_at = _utc_now()
    facts = {
        "collector_version": COLLECTOR_VERSION,
        "policy_sha256": sha256_json(policy),
        "playwright_version": importlib.metadata.version("playwright"),
        "browser_engine": "chromium",
        "browser_version": browser_version,
        "headless": policy["headless"],
        "start_url": sanitize_url(policy["start_url"]),
        "allowed_origins": sorted(allowed_origins),
        "started_at": started_at,
        "ended_at": ended_at,
        "capture_complete": capture_complete,
        "all_steps_passed": all_steps_passed,
        "cleanup_complete": cleanup_complete,
        "viewport_runs": viewport_runs,
        "viewport_count": len(viewport_runs),
        "steps": steps,
        "console": console,
        "page_errors": page_errors,
        "network": network,
        "screenshots": screenshots,
        "screenshot_count": len(screenshots),
        "unexpected_console_error_count": sum(
            1 for item in console if item["level"] in {"error", "assert"}
        ),
        "page_error_count": len(page_errors),
        "failed_request_count": len(failed_requests),
        "unexpected_http_error_count": len(http_errors),
        "duplicate_write_request_groups": duplicate_write_groups,
        "duplicate_write_request_group_count": len(duplicate_write_groups),
        "horizontal_overflow_viewport_count": sum(
            1 for item in viewport_runs if item["horizontal_overflow_px"] > 0
        ),
        "collection_errors": collection_errors,
    }
    document = {
        "schema_version": "0.1",
        "evidence_type": "browser.session",
        "source": f"VeriTrail {COLLECTOR_VERSION}",
        "captured_at": started_at,
        "facts": facts,
        "observed_variables": _declared_browser_observations(plan, browser_version),
        "metadata": {
            "network_scope": "loopback-only",
            "request_headers_persisted": False,
            "response_headers_persisted": False,
            "request_bodies_persisted": False,
            "response_bodies_persisted": False,
            "query_values_redacted": True,
            "contexts_parallel": False,
            "maximum_live_pages": 1,
            "service_workers": "BLOCKED",
            "websocket_scope": "sealed-loopback-origins-only",
            "screenshot_safety": policy.get(
                "screenshot_safety", "LEGACY_UNACKNOWLEDGED"
            ),
        },
    }
    return import_evidence_document(
        document,
        "generated-browser.json",
        attachments=tuple(attachments),
    )


def collect_browser_evidence(plan: dict[str, Any]) -> ImportedEvidence:
    """Collect the frozen M2 browser.session without M10 resource observation."""

    return _collect_browser_evidence(plan)
