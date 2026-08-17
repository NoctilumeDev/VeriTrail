from __future__ import annotations

import argparse
import ctypes
import hashlib
import http.client
import json
import socket
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from veritrail.local_api import create_catalog_server


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATE_B = REPOSITORY_ROOT / "tmp" / "m11-gateb-contract04-20260814-161647"
DEFAULT_BATCH = REPOSITORY_ROOT / "artifacts" / "m8-batch-runtime-v3-20260811" / "analyses" / "supported"
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m12-e-browser-evidence-acceptance"
EXPECTED_RUNS = {
    "m11-gateb-v2-ink-positive-01": ("COMPLETED", "PASS", True),
    "m11-gateb-v2-ink-browser-negative-01": ("COMPLETED", "FAIL", True),
    "m11-gateb-v2-ink-port-conflict-01": ("ABORTED", "PENDING", False),
    "m11-gateb-v2-ink-recovery-positive-02": ("COMPLETED", "PASS", True),
}
BATCH_FILES = (
    "batch-analysis-manifest.json",
    "sealed-batch-plan.json",
    "batch-analysis.json",
    "batch-analysis.md",
)


class MemoryStatusEx(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_ulong),
        ("memory_load", ctypes.c_ulong),
        ("total_physical", ctypes.c_ulonglong),
        ("available_physical", ctypes.c_ulonglong),
        ("total_page_file", ctypes.c_ulonglong),
        ("available_page_file", ctypes.c_ulonglong),
        ("total_virtual", ctypes.c_ulonglong),
        ("available_virtual", ctypes.c_ulonglong),
        ("available_extended_virtual", ctypes.c_ulonglong),
    ]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def available_memory_mb() -> float:
    status = MemoryStatusEx()
    status.length = ctypes.sizeof(MemoryStatusEx)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise OSError("GlobalMemoryStatusEx failed")
    return round(status.available_physical / 1024 / 1024, 3)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: object, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the M12-E production Browser Evidence presentation.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--batch", type=Path, default=DEFAULT_BATCH)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18780)
    return parser.parse_args()


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


def http_request(port: int, method: str, path: str) -> tuple[int, dict[str, str], bytes]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    connection.request(method, path)
    response = connection.getresponse()
    body = response.read()
    result = response.status, {key.lower(): value for key, value in response.getheaders()}, body
    connection.close()
    return result


def response_fact(response: Any) -> dict[str, Any]:
    parsed = urlsplit(response.url)
    origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme != "blob" else "[blob]"
    return {
        "method": response.request.method,
        "origin": origin,
        "path": parsed.path if parsed.scheme != "blob" else "[blob]",
        "resource_type": response.request.resource_type,
        "status": response.status,
    }


def add_page_observers(page: Any, summary: dict[str, Any]) -> None:
    page.on(
        "console",
        lambda message: summary["console_messages"].append(
            {"type": message.type, "text": message.text[:4096]}
        )
        if message.type in {"warning", "error"}
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


def require_no_root_overflow(page: Any, label: str) -> None:
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    offenders = page.locator("*").evaluate_all(
        """nodes => nodes
          .filter(node => node.scrollWidth > node.clientWidth + 1 && getComputedStyle(node).overflowX !== 'visible')
          .map(node => `${node.tagName.toLowerCase()}.${node.className || ''}:${node.scrollWidth - node.clientWidth}`)
          .slice(0, 12)"""
    )
    out_of_view = page.locator("*").evaluate_all(
        """nodes => nodes
          .map(node => {
            const rect = node.getBoundingClientRect();
            return {
              tag: node.tagName.toLowerCase(),
              className: String(node.className || ''),
              left: Math.round(rect.left * 10) / 10,
              right: Math.round(rect.right * 10) / 10,
              width: Math.round(rect.width * 10) / 10,
            };
          })
          .filter(item => item.right > document.documentElement.clientWidth + 0.5)
          .slice(0, 16)"""
    )
    require(
        overflow == 0,
        f"{label} overflowed horizontally by {overflow}px: {offenders}; out_of_view={out_of_view}",
    )


def batch_file_paths(path: Path) -> list[str]:
    return [str(path / name) for name in BATCH_FILES]


def save_screenshot(page: Any, output: Path, summary: dict[str, Any], name: str) -> None:
    path = output / name
    page.screenshot(path=str(path), full_page=False)
    summary["screenshots"].append(
        {"path": name, "sha256": sha256_file(path), "size": path.stat().st_size}
    )


def verify_negative_browser_evidence(page: Any, expect: Any, origin: str) -> None:
    page.goto(f"{origin}?fixture=negative", wait_until="load")
    expect(page.get_by_test_id("status-gate")).to_contain_text("FAIL")
    summary = page.get_by_test_id("browser-summary")
    expect(summary).to_contain_text("浏览器采集摘要")
    expect(summary).to_contain_text("异常事实")
    tabs = page.get_by_role("tab")
    require(tabs.count() == 4, "Browser Evidence did not retain exactly four standard tabs.")
    expect(tabs.nth(0)).to_have_attribute("aria-selected", "true")
    tabs.nth(0).press("ArrowRight")
    expect(tabs.nth(1)).to_be_focused()
    expect(tabs.nth(1)).to_have_attribute("aria-selected", "true")
    expect(page.locator("#panel-console .log--error").first).to_be_visible()
    tabs.nth(1).press("ArrowRight")
    expect(tabs.nth(2)).to_be_focused()
    expect(page.locator("#panel-network .network-row--error").first).to_be_visible()
    tabs.nth(2).press("Home")
    expect(tabs.nth(0)).to_be_focused()
    expect(page.locator("#panel-steps .timeline__entry").first).to_be_visible()
    tabs.nth(0).press("End")
    expect(tabs.nth(3)).to_be_focused()
    trigger = page.get_by_test_id("browser-screenshot-trigger").first
    expect(trigger).to_be_visible()
    trigger.click()
    dialog = page.locator("dialog.screenshot-dialog")
    expect(dialog).to_have_attribute("open", "")
    require(
        len(dialog.locator("code").inner_text()) == 64,
        "Screenshot dialog did not retain the complete SHA-256 evidence identifier.",
    )
    page.keyboard.press("Escape")
    expect(dialog).not_to_have_attribute("open", "")
    require(
        page.evaluate("document.activeElement?.getAttribute('data-testid')") == "browser-screenshot-trigger",
        "Screenshot dialog did not restore focus to its invoking screenshot.",
    )
    require_no_root_overflow(page, "negative Browser Evidence")


def main() -> int:
    args = parse_args()
    gate_b = args.gate_b.resolve()
    catalog = gate_b / "catalog"
    runs = gate_b / "runs"
    dist = args.dist.resolve()
    batch = args.batch.resolve()
    output = args.output.resolve()
    required = [
        catalog / "catalog-manifest.json",
        catalog / "catalog.sqlite3",
        dist / "index.html",
        dist / "fixtures" / "m2-positive" / "evidence-manifest.json",
        dist / "fixtures" / "m2-negative" / "evidence-manifest.json",
        dist / "fixtures" / "m2-invalid" / "report.json",
        *(batch / name for name in BATCH_FILES),
    ]
    if output.exists():
        print("M12-E acceptance refuses to overwrite its output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M12-E acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if any(not path.is_file() for path in required) or not runs.is_dir():
        print("M12-E acceptance requires the frozen M11/M2 inputs, Batch files, and production build.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m12-e-browser-evidence-production",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "checks": [],
        "console_messages": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
        "start_available_memory_mb": available_memory_mb(),
        "gate_b_directory": gate_b.name,
    }
    server = None
    server_thread = None
    server_started = False
    browser = None
    exit_code = 1
    origin = f"http://127.0.0.1:{args.port}"

    try:
        server = create_catalog_server(
            catalog_root=catalog,
            artifact_root=runs,
            web_root=dist,
            port=args.port,
        )
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        server_started = True

        health_status, health_headers, health_body = http_request(args.port, "GET", "/api/v1/health")
        health = json.loads(health_body)
        require(
            health_status == 200 and health["status"] == "READY" and health["read_only"] is True,
            "M12-E server did not report a read-only READY health state.",
        )
        require(health_headers.get("x-content-type-options") == "nosniff", "Health response omitted nosniff.")
        catalog_status, _, catalog_body = http_request(args.port, "GET", "/api/v1/catalog?page=1&page_size=100")
        catalog_response = json.loads(catalog_body)
        require(catalog_status == 200, "M12-E Catalog endpoint did not return HTTP 200.")
        catalog_runs = {item["run_id"]: item for item in catalog_response["runs"]}
        require(set(catalog_runs) == set(EXPECTED_RUNS), "M12-E found an unexpected M11 Run set.")
        for run_id, (execution_status, verdict, _) in EXPECTED_RUNS.items():
            require(catalog_runs[run_id]["execution_status"] == execution_status, f"Execution drifted for {run_id}.")
            require(catalog_runs[run_id]["verdict"] == verdict, f"Verdict drifted for {run_id}.")
        require(http_request(args.port, "HEAD", "/api/v1/catalog")[0] == 200, "Catalog HEAD failed.")
        require(http_request(args.port, "POST", "/api/v1/catalog")[0] == 405, "Catalog accepted a write request.")
        summary["checks"].append("frozen-m11-catalog-read-only")

        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            summary["browser_version"] = browser.version

            desktop = browser.new_context(viewport={"width": 1440, "height": 960})
            page = desktop.new_page()
            add_page_observers(page, summary)
            verify_negative_browser_evidence(page, expect, origin)
            save_screenshot(page, output, summary, "negative-browser-desktop.png")
            summary["checks"].append("desktop-negative-browser-tabs-failures-dialog-focus")

            page.goto(f"{origin}?fixture=invalid", wait_until="load")
            invalid = page.get_by_test_id("error-state")
            expect(invalid).to_have_attribute("data-state-kind", "invalid")
            expect(invalid).to_contain_text("没有据此改写 Run 的 Verdict")
            expect(page.get_by_test_id("run-summary")).not_to_be_visible()
            page.get_by_test_id("retry-positive").click()
            expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
            summary["checks"].append("invalid-bundle-rejected-and-positive-recovery")

            no_browser = catalog_runs["m11-gateb-v2-ink-port-conflict-01"]
            page.goto(f"{origin}?run={no_browser['catalog_run_id']}", wait_until="load")
            expect(page.get_by_test_id("status-gate")).to_contain_text("ABORTED")
            expect(page.get_by_test_id("status-gate")).to_contain_text("PENDING")
            absent = page.get_by_test_id("browser-empty")
            expect(absent).to_have_attribute("data-state-kind", "no-browser")
            expect(absent).to_contain_text("不等于浏览器检查通过")
            require_no_root_overflow(page, "M11 no-browser Run")
            summary["checks"].append("m11-no-browser-is-absence-not-pass")

            page.goto(f"{origin}?run=cr_000000000000000000000000", wait_until="load")
            operational = page.get_by_test_id("error-state")
            expect(operational).to_have_attribute("data-state-kind", "operational")
            expect(operational).to_contain_text("RUN_NOT_FOUND")
            summary["checks"].append("catalog-operational-error-distinct")

            page.goto(f"{origin}?view=batch", wait_until="load")
            input_element = page.get_by_test_id("local-batch-input")
            input_element.set_input_files(batch_file_paths(batch))
            expect(page.get_by_test_id("batch-analysis-view")).to_be_visible()
            page.reload(wait_until="load")
            privacy = page.get_by_test_id("error-state")
            expect(privacy).to_have_attribute("data-state-kind", "privacy")
            expect(privacy).to_contain_text("BATCH_RESELECT_REQUIRED")
            expect(privacy).to_contain_text("为保护隐私")
            expect(page.get_by_test_id("batch-analysis-view")).not_to_be_visible()
            summary["checks"].append("local-file-privacy-reselect-after-refresh")
            desktop.close()

            for width, height in ((390, 844), (360, 800)):
                mobile = browser.new_context(
                    viewport={"width": width, "height": height}, is_mobile=True, reduced_motion="reduce"
                )
                mobile_page = mobile.new_page()
                add_page_observers(mobile_page, summary)
                verify_negative_browser_evidence(mobile_page, expect, origin)
                require(
                    mobile_page.get_by_role("tab").first.evaluate("element => element.offsetHeight >= 44"),
                    f"{width}px Browser tab fell below the 44px target height.",
                )
                save_screenshot(mobile_page, output, summary, f"negative-browser-{width}.png")
                summary["checks"].append(f"mobile-{width}-browser-evidence-no-root-overflow")
                mobile.close()

            forced = browser.new_context(
                viewport={"width": 390, "height": 844}, is_mobile=True, forced_colors="active", reduced_motion="reduce"
            )
            forced_page = forced.new_page()
            add_page_observers(forced_page, summary)
            verify_negative_browser_evidence(forced_page, expect, origin)
            forced_page.get_by_role("tab").nth(3).press("Home")
            expect(forced_page.get_by_role("tab").nth(0)).to_be_focused()
            expect(forced_page.locator("#panel-steps .timeline__entry").first).to_be_visible()
            expect(forced_page.get_by_test_id("browser-summary")).to_contain_text("异常事实")
            require_no_root_overflow(forced_page, "forced-colors Browser Evidence")
            summary["checks"].append("forced-colors-text-boundary-and-focus-contract")
            forced.close()

            browser.close()
            browser = None

        external = [item for item in summary["network"] if item["origin"] not in {origin, "[blob]"}]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        require(not summary["console_messages"], "Production Workbench emitted Console warning/error messages.")
        require(not summary["page_errors"], "Production Workbench emitted a page error.")
        require(not summary["request_failures"], "Production Workbench emitted a request failure.")
        require(not external and not writes and not http_errors, "Production Workbench crossed its read-only network boundary.")
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
        if server is not None:
            if server_started:
                server.shutdown()
            server.server_close()
        if server_thread is not None:
            server_thread.join(timeout=5)
        summary["server_thread_stopped"] = server_thread is None or not server_thread.is_alive()
        summary["ended_at"] = utc_now()
        summary["end_available_memory_mb"] = available_memory_mb()
        summary["network_request_count"] = len(summary["network"])
        (output / "acceptance.json").write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    released = port_is_free(args.port)
    sidecars = list(catalog.glob("catalog.sqlite3-*"))
    if not released or sidecars or not summary["server_thread_stopped"]:
        print("M12-E acceptance left a server thread, port, or SQLite sidecar behind.", file=sys.stderr)
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
                "port_released": released,
                "server_thread_stopped": summary["server_thread_stopped"],
                "sqlite_sidecars": len(sidecars),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
