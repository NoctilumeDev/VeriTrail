from __future__ import annotations

import argparse
import hashlib
import json
import socket
import sys
import threading
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_LOCAL_BUNDLE = REPOSITORY_ROOT / "artifacts" / "m2-freeze-pass"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m3-workbench-acceptance"


class QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return

    def _serve_empty_catalog(self, *, include_body: bool) -> None:
        payload = json.dumps(
            {
                "schema_version": "0.1",
                "catalog": {
                    "catalog_id": "cat_000000000000000000000000",
                    "build_status": "COMPLETED",
                    "read_only": True,
                    "run_count": 0,
                    "issue_count": 0,
                    "duplicate_count": 0,
                },
                "pagination": {
                    "page": 1,
                    "page_size": 100,
                    "total_items": 0,
                    "total_pages": 0,
                },
                "runs": [],
                "issues": [],
                "issues_truncated": False,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if include_body:
            self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/api/v1/catalog":
            self._serve_empty_catalog(include_body=True)
            return
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802
        if self.path == "/api/v1/catalog":
            self._serve_empty_catalog(include_body=False)
            return
        super().do_HEAD()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def response_fact(response: Any) -> dict[str, Any]:
    parsed = urlsplit(response.url)
    return {
        "method": response.request.method,
        "path": "[blob]" if parsed.scheme == "blob" else parsed.path,
        "resource_type": response.request.resource_type,
        "status": response.status,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded M3 Workbench browser acceptance.")
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--local-bundle", type=Path, default=DEFAULT_LOCAL_BUNDLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18766)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dist = args.dist.resolve()
    local_bundle = args.local_bundle.resolve()
    output = args.output.resolve()
    if not dist.is_dir() or not (dist / "index.html").is_file():
        print("M3 acceptance requires an existing web/dist production build.", file=sys.stderr)
        return 2
    if not local_bundle.is_dir() or not (local_bundle / "bundle-manifest.json").is_file():
        print("M3 acceptance requires a local VeriTrail evidence bundle.", file=sys.stderr)
        return 2
    if output.exists():
        print("M3 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535:
        print("M3 acceptance port must be between 1024 and 65535.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    handler = partial(QuietStaticHandler, directory=str(dist))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m3-workbench",
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "execution_status": "RUNNING",
        "checks": [],
        "console_errors": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
    }
    browser = None
    exit_code = 1
    try:
        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            summary["playwright_version"] = "1.62.0"
            summary["browser_version"] = browser.version
            desktop = browser.new_context(viewport={"width": 1280, "height": 720})
            page = desktop.new_page()
            page.on(
                "console",
                lambda message: summary["console_errors"].append(
                    {"type": message.type, "text": message.text[:4096]}
                )
                if message.type == "error"
                else None,
            )
            page.on(
                "pageerror",
                lambda error: summary["page_errors"].append(
                    {"name": error.name, "message": error.message[:4096]}
                ),
            )
            page.on(
                "requestfailed",
                lambda request: summary["request_failures"].append(
                    {
                        "method": request.method,
                        "path": urlsplit(request.url).path,
                        "failure": request.failure,
                    }
                ),
            )
            page.on("response", lambda response: summary["network"].append(response_fact(response)))

            origin = f"http://127.0.0.1:{args.port}"
            page.goto(f"{origin}/?fixture=positive", wait_until="load")
            expect(page.locator('[aria-label="运行状态：COMPLETED"]')).to_be_visible()
            expect(page.locator('[aria-label="验收结论：PASS"]')).to_be_visible()
            expect(page.get_by_test_id("integrity-status")).to_contain_text("8 个文件")
            desktop_overflow = page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth"
            )
            assert desktop_overflow == 0, f"desktop horizontal overflow: {desktop_overflow}px"
            summary["checks"].append("desktop-positive")

            page.get_by_test_id("fixture-negative").click()
            expect(page.locator('[aria-label="验收结论：FAIL"]')).to_be_visible()
            page.get_by_test_id("filter-fail").click()
            assert page.locator(".assertion--fail").count() == 3
            page.get_by_role("tab", name="Console 4").click()
            expect(page.locator('[aria-labelledby="tab-console"]')).to_contain_text(
                "synthetic console failure"
            )
            page.get_by_role("tab", name="Network 4").click()
            expect(page.locator('[aria-labelledby="tab-network"]')).to_contain_text("/missing.json")
            page.get_by_role("tab", name="截图 2").click()
            page.locator(".screenshot-card").first.click()
            expect(page.locator("dialog[open]")).to_be_visible()
            page.keyboard.press("Escape")
            summary["checks"].append("desktop-negative-evidence")

            page.get_by_test_id("fixture-invalid").click()
            expect(page.get_by_test_id("error-state")).to_contain_text("MISSING_ROOT_FILE")
            assert page.get_by_test_id("status-gate").count() == 0
            page.get_by_test_id("retry-positive").click()
            expect(page.locator('[aria-label="验收结论：PASS"]')).to_be_visible()
            page.go_back(wait_until="load")
            expect(page.get_by_test_id("error-state")).to_be_visible()
            page.go_forward(wait_until="load")
            expect(page.locator('[aria-label="验收结论：PASS"]')).to_be_visible()
            summary["checks"].append("invalid-contained-retry-history")

            requests_before_local = len(summary["network"])
            page.get_by_test_id("local-bundle-input").set_input_files(str(local_bundle))
            expect(page.get_by_test_id("run-summary")).to_contain_text("m2-freeze-pass")
            expect(page.get_by_test_id("run-summary")).to_contain_text("本地目录 · 仅内存读取")
            assert len(summary["network"]) == requests_before_local
            summary["checks"].append("desktop-local-directory-no-upload")

            desktop_screenshot = output / "desktop.png"
            page.screenshot(path=str(desktop_screenshot), full_page=False)
            summary["screenshots"].append(
                {
                    "path": "desktop.png",
                    "sha256": sha256_file(desktop_screenshot),
                    "size": desktop_screenshot.stat().st_size,
                }
            )
            desktop.close()

            mobile = browser.new_context(
                viewport={"width": 390, "height": 844},
                is_mobile=True,
                reduced_motion="reduce",
            )
            mobile_page = mobile.new_page()
            mobile_page.on(
                "console",
                lambda message: summary["console_errors"].append(
                    {"type": message.type, "text": message.text[:4096]}
                )
                if message.type == "error"
                else None,
            )
            mobile_page.on(
                "pageerror",
                lambda error: summary["page_errors"].append(
                    {"name": error.name, "message": error.message[:4096]}
                ),
            )
            mobile_page.on(
                "requestfailed",
                lambda request: summary["request_failures"].append(
                    {
                        "method": request.method,
                        "path": urlsplit(request.url).path,
                        "failure": request.failure,
                    }
                ),
            )
            mobile_page.on("response", lambda response: summary["network"].append(response_fact(response)))
            mobile_page.goto(f"{origin}/?fixture=positive", wait_until="load")
            expect(mobile_page.locator('[aria-label="验收结论：PASS"]')).to_be_visible()
            mobile_overflow = mobile_page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth"
            )
            assert mobile_overflow == 0, f"mobile horizontal overflow: {mobile_overflow}px"
            mobile_page.get_by_test_id("fixture-negative").click()
            expect(mobile_page.locator('[aria-label="验收结论：FAIL"]')).to_be_visible()
            mobile_screenshot = output / "mobile.png"
            mobile_page.screenshot(path=str(mobile_screenshot), full_page=False)
            summary["screenshots"].append(
                {
                    "path": "mobile.png",
                    "sha256": sha256_file(mobile_screenshot),
                    "size": mobile_screenshot.stat().st_size,
                }
            )
            summary["checks"].append("mobile-positive-negative-no-overflow-reduced-motion")
            mobile.close()
            browser.close()
            browser = None

        http_errors = [entry for entry in summary["network"] if entry["status"] >= 400]
        if summary["console_errors"] or summary["page_errors"] or summary["request_failures"]:
            raise AssertionError("Workbench emitted unexpected runtime errors.")
        if http_errors:
            raise AssertionError("Workbench made an unexpected HTTP 4xx/5xx request.")
        if any(
            entry["path"] != "[blob]" and not entry["path"].startswith("/")
            for entry in summary["network"]
        ):
            raise AssertionError("Workbench network evidence contains a malformed path.")
        summary["network_request_count"] = len(summary["network"])
        summary["http_error_count"] = 0
        summary["execution_status"] = "COMPLETED"
        summary["verdict"] = "PASS"
        exit_code = 0
    except Exception as error:
        summary["execution_status"] = "ERROR"
        summary["verdict"] = "FAIL"
        summary["failure_type"] = type(error).__name__
        summary["failure_message"] = str(error)[:4096]
    finally:
        if browser is not None:
            try:
                browser.close()
            except Exception:
                # The Playwright context may already be stopped while unwinding an assertion.
                pass
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=5)
        summary["ended_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        summary["network_request_count"] = len(summary["network"])
        summary["http_error_count"] = len(
            [entry for entry in summary["network"] if entry["status"] >= 400]
        )
        with (output / "acceptance.json").open("w", encoding="utf-8", newline="\n") as stream:
            json.dump(summary, stream, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            stream.write("\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        port_released = probe.connect_ex(("127.0.0.1", args.port)) != 0
    if not port_released:
        print("M3 acceptance server port was not released.", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "execution_status": summary["execution_status"],
                "verdict": summary["verdict"],
                "checks": len(summary["checks"]),
                "network_request_count": summary.get("network_request_count", 0),
                "http_error_count": summary.get("http_error_count", 0),
                "output": output.name,
                "port_released": True,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
