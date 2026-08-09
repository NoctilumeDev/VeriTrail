from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import socket
import sys
import tempfile
import threading
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m6-comparison-acceptance"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded M6 Comparison Workbench acceptance.")
    parser.add_argument("--match", type=Path, required=True, help="verified MATCH Comparison Bundle")
    parser.add_argument("--drift", type=Path, required=True, help="verified DRIFT Comparison Bundle")
    parser.add_argument(
        "--inconclusive",
        type=Path,
        required=True,
        help="verified INCONCLUSIVE Comparison Bundle",
    )
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18769)
    return parser.parse_args()


class WorkbenchHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if urlsplit(self.path).path.startswith("/api/"):
            self.path = "/index.html"
        super().do_GET()

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def response_fact(response: Any) -> dict[str, Any]:
    parsed = urlsplit(response.url)
    return {
        "method": response.request.method,
        "origin": f"{parsed.scheme}://{parsed.netloc}",
        "path": parsed.path,
        "resource_type": response.request.resource_type,
        "status": response.status,
    }


def port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
        if exclusive is not None:
            probe.setsockopt(socket.SOL_SOCKET, exclusive, 1)
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True


def main() -> int:
    args = parse_args()
    dist = args.dist.resolve()
    output = args.output.resolve()
    comparisons = {
        "MATCH": args.match.resolve(),
        "DRIFT": args.drift.resolve(),
        "INCONCLUSIVE": args.inconclusive.resolve(),
    }
    if output.exists():
        print("M6 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M6 acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if not (dist / "index.html").is_file():
        print("M6 acceptance requires an existing Workbench production build.", file=sys.stderr)
        return 2
    for status, path in comparisons.items():
        if not all((path / name).is_file() for name in (
            "comparison-manifest.json",
            "comparison.json",
            "comparison.md",
        )):
            print(f"M6 acceptance requires a complete {status} Comparison Bundle.", file=sys.stderr)
            return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m6-deterministic-rerun-comparison",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "checks": [],
        "console_errors": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
    }
    handler = partial(WorkbenchHandler, directory=str(dist))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    browser = None
    exit_code = 1
    origin = f"http://127.0.0.1:{args.port}"
    try:
        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            summary["browser_version"] = browser.version
            desktop = browser.new_context(viewport={"width": 1280, "height": 800})
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
                    {"method": request.method, "path": urlsplit(request.url).path}
                ),
            )
            page.on("response", lambda response: summary["network"].append(response_fact(response)))
            page.goto(origin, wait_until="load")
            comparison_input = page.get_by_test_id("local-comparison-input")
            comparison_input.focus()
            assert page.evaluate("document.activeElement?.dataset.testid") == "local-comparison-input"

            for expected_status in ("MATCH", "DRIFT", "INCONCLUSIVE"):
                comparison_input.set_input_files(str(comparisons[expected_status]))
                expect(page.get_by_test_id("comparison-view")).to_be_visible()
                expect(page.get_by_test_id("comparison-status")).to_contain_text(expected_status)
                expect(page.get_by_test_id("comparison-sources")).to_contain_text("BASELINE")
                expect(page.get_by_test_id("comparison-sources")).to_contain_text("REPEAT")
                assert page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                ) == 0
                summary["checks"].append(f"desktop-{expected_status.lower()}-verified")

            with tempfile.TemporaryDirectory() as directory:
                corrupted = Path(directory) / "corrupted-comparison"
                shutil.copytree(comparisons["MATCH"], corrupted)
                changed = corrupted / "comparison.json"
                changed.write_bytes(changed.read_bytes() + b" ")
                comparison_input.set_input_files(str(corrupted))
                expect(page.get_by_test_id("error-state")).to_contain_text("COMPARISON_SIZE_MISMATCH")
                assert page.get_by_test_id("comparison-view").count() == 0
                page.get_by_test_id("retry-positive").click()
                expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
                summary["checks"].append("desktop-corruption-contained-and-recovered")

            comparison_input = page.get_by_test_id("local-comparison-input")
            comparison_input.set_input_files(str(comparisons["MATCH"]))
            expect(page.get_by_test_id("comparison-status")).to_contain_text("MATCH")
            page.reload(wait_until="load")
            expect(page.get_by_test_id("error-state")).to_contain_text("COMPARISON_RESELECT_REQUIRED")
            page.go_back(wait_until="load")
            expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
            summary["checks"].append("desktop-history-privacy-boundary")

            desktop_shot = output / "desktop.png"
            comparison_input = page.get_by_test_id("local-comparison-input")
            comparison_input.set_input_files(str(comparisons["DRIFT"]))
            expect(page.get_by_test_id("comparison-status")).to_contain_text("DRIFT")
            page.screenshot(path=str(desktop_shot), full_page=False)
            summary["screenshots"].append(
                {
                    "path": "desktop.png",
                    "sha256": sha256_file(desktop_shot),
                    "size": desktop_shot.stat().st_size,
                }
            )
            desktop.close()

            mobile = browser.new_context(
                viewport={"width": 390, "height": 844}, is_mobile=True, reduced_motion="reduce"
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
                    {"method": request.method, "path": urlsplit(request.url).path}
                ),
            )
            mobile_page.on(
                "response", lambda response: summary["network"].append(response_fact(response))
            )
            mobile_page.goto(origin, wait_until="load")
            mobile_page.get_by_test_id("local-comparison-input").set_input_files(
                str(comparisons["MATCH"])
            )
            expect(mobile_page.get_by_test_id("comparison-status")).to_contain_text("MATCH")
            assert mobile_page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth"
            ) == 0
            mobile_shot = output / "mobile.png"
            mobile_page.screenshot(path=str(mobile_shot), full_page=False)
            summary["screenshots"].append(
                {
                    "path": "mobile.png",
                    "sha256": sha256_file(mobile_shot),
                    "size": mobile_shot.stat().st_size,
                }
            )
            summary["checks"].append("mobile-match-no-overflow")
            mobile.close()
            browser.close()
            browser = None

        external = [item for item in summary["network"] if item["origin"] != origin]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        if summary["console_errors"] or summary["page_errors"] or summary["request_failures"]:
            raise AssertionError("Workbench emitted unexpected browser errors.")
        if external or writes or http_errors:
            raise AssertionError("Workbench crossed the same-origin read-only network boundary.")
        summary["network_request_count"] = len(summary["network"])
        summary["external_request_count"] = len(external)
        summary["write_request_count"] = len(writes)
        summary["http_error_count"] = len(http_errors)
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
                pass
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=5)
        summary["ended_at"] = utc_now()
        summary["network_request_count"] = len(summary["network"])
        (output / "acceptance.json").write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    released = port_is_free(args.port)
    if not released:
        print("M6 acceptance did not release its loopback port.", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "execution_status": summary["execution_status"],
                "verdict": summary["verdict"],
                "checks": len(summary["checks"]),
                "network_request_count": summary.get("network_request_count", 0),
                "http_error_count": summary.get("http_error_count", 0),
                "external_request_count": summary.get("external_request_count", 0),
                "write_request_count": summary.get("write_request_count", 0),
                "output": output.name,
                "port_released": True,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
