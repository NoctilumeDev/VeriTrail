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
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m11-gateb-workbench-acceptance"
EXPECTED_RUNS = {
    "m11-gateb-v2-ink-positive-01": ("COMPLETED", "PASS", True),
    "m11-gateb-v2-ink-browser-negative-01": ("COMPLETED", "FAIL", True),
    "m11-gateb-v2-ink-port-conflict-01": ("ABORTED", "PENDING", False),
    "m11-gateb-v2-ink-recovery-positive-02": ("COMPLETED", "PASS", True),
}


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the M11 Gate B production Workbench.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18778)
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
        lambda message: summary["console_errors"].append(
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


def require(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    args = parse_args()
    gate_b = args.gate_b.resolve()
    catalog = gate_b / "catalog"
    artifacts = gate_b / "runs"
    comparison = gate_b / "comparison"
    dist = args.dist.resolve()
    output = args.output.resolve()
    acceptance_path = gate_b / "acceptance.json"

    if output.exists():
        print("M11 Workbench acceptance refuses to overwrite its output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M11 Workbench acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    required = [
        acceptance_path,
        catalog / "catalog-manifest.json",
        catalog / "catalog.sqlite3",
        comparison / "comparison-manifest.json",
        comparison / "comparison.json",
        comparison / "comparison.md",
        dist / "index.html",
    ]
    if any(not path.is_file() for path in required) or not artifacts.is_dir():
        print("M11 Workbench acceptance requires the complete Gate B output and production build.", file=sys.stderr)
        return 2

    authority = json.loads(acceptance_path.read_text(encoding="utf-8"))
    expected_plan_sha256 = {
        item["run_id"]: authority["authorities"][item["authority"]]["plan_sha256"]
        for item in authority["runs"]
    }
    if set(expected_plan_sha256) != set(EXPECTED_RUNS):
        print("M11 Workbench acceptance found an unexpected Gate B Run set.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m11-gate-b-production-workbench",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "checks": [],
        "console_errors": [],
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
            artifact_root=artifacts,
            web_root=dist,
            port=args.port,
        )
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        server_started = True

        status, headers, body = http_request(args.port, "GET", "/api/v1/health")
        health = json.loads(body)
        require(
            status == 200
            and health["status"] == "READY"
            and health["read_only"] is True,
            "Workbench health endpoint did not report a read-only READY service.",
        )
        require(
            headers.get("x-content-type-options") == "nosniff",
            "Workbench health endpoint omitted the nosniff response header.",
        )

        status, _, body = http_request(args.port, "GET", "/api/v1/catalog?page=1&page_size=100")
        catalog_response = json.loads(body)
        require(status == 200, "Workbench catalog endpoint did not return HTTP 200.")
        require(
            catalog_response["catalog"]["run_count"] == 4,
            "Workbench catalog did not report exactly four valid Runs.",
        )
        require(
            catalog_response["catalog"]["issue_count"] == 1,
            "Workbench catalog did not report exactly one isolated issue.",
        )
        require(
            len(catalog_response["runs"]) == 4,
            "Workbench catalog response did not contain exactly four Runs.",
        )
        require(
            len(catalog_response["issues"]) == 1,
            "Workbench catalog response did not contain exactly one isolated issue.",
        )
        catalog_runs = {item["run_id"]: item for item in catalog_response["runs"]}
        require(
            set(catalog_runs) == set(EXPECTED_RUNS),
            "Workbench catalog returned an unexpected Run set.",
        )
        for run_id, (execution_status, verdict, _) in EXPECTED_RUNS.items():
            require(
                catalog_runs[run_id]["execution_status"] == execution_status,
                f"Workbench catalog execution status drifted for {run_id}.",
            )
            require(
                catalog_runs[run_id]["verdict"] == verdict,
                f"Workbench catalog Verdict drifted for {run_id}.",
            )
            require(
                catalog_runs[run_id]["plan"]["sha256"] == expected_plan_sha256[run_id],
                f"Workbench catalog Plan authority drifted for {run_id}.",
            )
        summary["checks"].append("http-catalog-four-runs-one-isolated-issue")

        require(
            http_request(args.port, "HEAD", "/api/v1/catalog")[0] == 200,
            "Workbench catalog HEAD contract failed.",
        )
        require(
            http_request(args.port, "POST", "/api/v1/catalog")[0] == 405,
            "Workbench catalog accepted a write request.",
        )
        require(
            http_request(args.port, "GET", "/api/v1/catalog?unknown=1")[0] == 400,
            "Workbench catalog accepted an unknown query parameter.",
        )
        summary["checks"].append("http-readonly-negative-contract")

        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            summary["browser_version"] = browser.version

            desktop = browser.new_context(viewport={"width": 1440, "height": 960})
            page = desktop.new_page()
            add_page_observers(page, summary)
            page.goto(origin, wait_until="load")
            expect(page.get_by_test_id("run-catalog")).to_be_visible()
            expect(page.get_by_test_id("run-catalog")).to_contain_text("4 Runs")
            expect(page.get_by_test_id("catalog-issues")).to_contain_text("目录问题 1 项")
            catalog_columns = page.get_by_test_id("catalog-columns")
            expect(catalog_columns).to_contain_text("Run / 时间")
            expect(catalog_columns).to_contain_text("运行状态")
            expect(catalog_columns).to_contain_text("验收结论")
            expect(catalog_columns).to_contain_text("Plan / 目录事实")
            for run_id, (execution_status, verdict, _) in EXPECTED_RUNS.items():
                item = catalog_runs[run_id]
                catalog_row = page.locator(
                    f'[data-catalog-run-id="{item["catalog_run_id"]}"]'
                )
                expect(catalog_row.locator(".catalog-run__identity")).to_contain_text(run_id)
                expect(catalog_row.locator(".catalog-run__execution")).to_contain_text(
                    execution_status
                )
                expect(catalog_row.locator(".catalog-run__verdict")).to_contain_text(verdict)
                expect(catalog_row.locator(".catalog-run__facts")).to_contain_text(
                    item["plan"]["id"]
                )
            summary["checks"].append("desktop-catalog-stable-columns-and-separated-statuses")
            catalog_desktop_shot = output / "catalog-desktop.png"
            page.screenshot(path=str(catalog_desktop_shot), full_page=False)
            summary["screenshots"].append(
                {
                    "path": "catalog-desktop.png",
                    "sha256": sha256_file(catalog_desktop_shot),
                    "size": catalog_desktop_shot.stat().st_size,
                }
            )

            cross_axis = page.get_by_test_id("cross-axis-toggle")
            expect(cross_axis).to_have_attribute("aria-expanded", "false")
            cross_axis.click()
            expect(page.get_by_test_id("cross-axis-runs")).to_be_visible()
            page.get_by_test_id("cross-axis-runs").press("ArrowRight")
            require(
                page.evaluate("document.activeElement?.getAttribute('data-testid')")
                == "cross-axis-batch",
                "Workbench cross-axis ArrowRight did not follow its declared geometry.",
            )
            page.get_by_test_id("cross-axis-comparison").click()
            expect(page.get_by_test_id("view-comparison-title")).to_be_focused()
            expect(page.get_by_test_id("local-comparison-input")).to_be_visible()
            expect(page.get_by_test_id("comparison-empty")).to_be_visible()
            expect(page.get_by_test_id("run-catalog")).not_to_be_visible()
            require(
                page.url.endswith("?view=comparison"),
                "Workbench cross-axis Comparison URL did not preserve the public view.",
            )
            cross_axis.click()
            page.get_by_test_id("cross-axis-pairing").click()
            expect(page.get_by_test_id("view-pairing-title")).to_be_focused()
            expect(page.get_by_test_id("local-pairing-input")).to_be_visible()
            expect(page.get_by_test_id("run-catalog")).not_to_be_visible()
            cross_axis.click()
            page.get_by_test_id("cross-axis-batch").click()
            expect(page.get_by_test_id("view-batch-title")).to_be_focused()
            expect(page.get_by_test_id("local-batch-input")).to_be_visible()
            expect(page.get_by_test_id("run-catalog")).not_to_be_visible()
            cross_axis.click()
            page.get_by_test_id("cross-axis-runs").click()
            expect(page.get_by_test_id("view-runs-title")).to_be_focused()
            expect(page.get_by_test_id("run-catalog")).to_be_visible()
            summary["checks"].append("desktop-cross-axis-four-public-views-and-focus")

            for run_id, (execution_status, verdict, browser_applicable) in EXPECTED_RUNS.items():
                item = catalog_runs[run_id]
                button = page.locator(f'[data-catalog-run-id="{item["catalog_run_id"]}"]')
                expect(button).to_contain_text(run_id)
                expect(button.locator(".catalog-run__execution")).to_contain_text(execution_status)
                expect(button.locator(".catalog-run__verdict")).to_contain_text(verdict)
                button.click()
                expect(page.get_by_test_id("run-summary")).to_contain_text(run_id)
                expect(page.get_by_test_id("status-gate")).to_contain_text(execution_status)
                expect(page.get_by_test_id("status-gate")).to_contain_text(verdict)
                expect(page.get_by_test_id("integrity-status")).to_contain_text("Core 裁决")
                expect(page.get_by_test_id("integrity-status")).to_contain_text("已核验")
                require(
                    page.get_by_test_id("run-summary").locator("code").get_attribute("title")
                    == expected_plan_sha256[run_id],
                    f"Workbench detail Plan authority drifted for {run_id}.",
                )
                require(
                    len(expected_plan_sha256[run_id]) == 64,
                    f"Workbench detail Plan hash was not a full SHA-256 for {run_id}.",
                )
                ledger = page.get_by_test_id("evidence-ledger")
                expect(ledger).to_contain_text("runtime.preflight")
                if browser_applicable:
                    expect(ledger).to_contain_text("runtime.bootstrap")
                    expect(page.get_by_test_id("browser-evidence")).to_be_visible()
                else:
                    expect(page.get_by_test_id("browser-empty")).to_be_visible()
                require(
                    page.evaluate(
                        "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                    )
                    == 0,
                    f"Workbench desktop detail overflowed for {run_id}.",
                )
                page.get_by_test_id("catalog-return").click()
                require(
                    page.evaluate(
                        "document.activeElement?.getAttribute('data-catalog-run-id')"
                    )
                    == item["catalog_run_id"],
                    f"Workbench did not restore catalog focus for {run_id}.",
                )
                summary["checks"].append(f"desktop-{run_id}-verified")

            recovery_id = "m11-gateb-v2-ink-recovery-positive-02"
            recovery_catalog_id = catalog_runs[recovery_id]["catalog_run_id"]
            page.locator(f'[data-catalog-run-id="{recovery_catalog_id}"]').click()
            page.go_back(wait_until="load")
            expect(page.get_by_test_id("run-catalog")).to_be_visible()
            page.go_forward(wait_until="load")
            expect(page.get_by_test_id("run-summary")).to_contain_text(recovery_id)
            summary["checks"].append("desktop-catalog-history")

            page.get_by_test_id("cross-axis-toggle").click()
            page.get_by_test_id("cross-axis-comparison").click()
            expect(page.get_by_test_id("local-comparison-input")).to_be_visible()
            comparison_input = page.get_by_test_id("local-comparison-input")
            comparison_input.set_input_files(str(comparison))
            expect(page.get_by_test_id("comparison-view")).to_be_visible()
            expect(page.get_by_test_id("comparison-status")).to_contain_text("MATCH")
            expect(page.get_by_test_id("comparison-no-differences")).to_be_visible()
            sources = page.get_by_test_id("comparison-sources")
            expect(sources).to_contain_text("m11-gateb-v2-ink-positive-01")
            expect(sources).to_contain_text("m11-gateb-v2-ink-recovery-positive-02")
            require(
                page.evaluate(
                    "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                )
                == 0,
                "Workbench desktop Comparison overflowed horizontally.",
            )
            summary["checks"].append("desktop-real-comparison-match")

            desktop_shot = output / "desktop.png"
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
            add_page_observers(mobile_page, summary)
            mobile_page.goto(origin, wait_until="load")
            expect(mobile_page.get_by_test_id("run-catalog")).to_be_visible()
            require(
                mobile_page.get_by_test_id("catalog-columns").evaluate(
                    "element => getComputedStyle(element).display"
                )
                == "none",
                "Workbench mobile Catalog did not collapse visual column labels.",
            )
            aborted_id = "m11-gateb-v2-ink-port-conflict-01"
            aborted_catalog_id = catalog_runs[aborted_id]["catalog_run_id"]
            aborted_row = mobile_page.locator(
                f'[data-catalog-run-id="{aborted_catalog_id}"]'
            )
            expect(aborted_row.locator(".catalog-run__execution")).to_contain_text("ABORTED")
            expect(aborted_row.locator(".catalog-run__verdict")).to_contain_text("PENDING")
            require(
                mobile_page.evaluate(
                    "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                )
                == 0,
                "Workbench mobile Catalog overflowed horizontally.",
            )
            catalog_mobile_shot = output / "catalog-mobile.png"
            mobile_page.screenshot(path=str(catalog_mobile_shot), full_page=False)
            summary["screenshots"].append(
                {
                    "path": "catalog-mobile.png",
                    "sha256": sha256_file(catalog_mobile_shot),
                    "size": catalog_mobile_shot.stat().st_size,
                }
            )
            mobile_page.get_by_test_id("cross-axis-toggle").click()
            require(
                mobile_page.evaluate(
                    "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                )
                == 0,
                "Workbench mobile expanded cross-axis overflowed horizontally.",
            )
            mobile_page.get_by_test_id("cross-axis-runs").click()
            negative_id = "m11-gateb-v2-ink-browser-negative-01"
            negative_catalog_id = catalog_runs[negative_id]["catalog_run_id"]
            mobile_page.locator(f'[data-catalog-run-id="{negative_catalog_id}"]').click()
            expect(mobile_page.get_by_test_id("status-gate")).to_contain_text("COMPLETED")
            expect(mobile_page.get_by_test_id("status-gate")).to_contain_text("FAIL")
            require(
                mobile_page.evaluate(
                    "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                )
                == 0,
                "Workbench mobile negative detail overflowed horizontally.",
            )
            mobile_page.get_by_test_id("cross-axis-toggle").click()
            mobile_page.get_by_test_id("cross-axis-comparison").click()
            expect(mobile_page.get_by_test_id("local-comparison-input")).to_be_visible()
            mobile_page.get_by_test_id("local-comparison-input").set_input_files(str(comparison))
            expect(mobile_page.get_by_test_id("comparison-status")).to_contain_text("MATCH")
            require(
                mobile_page.evaluate(
                    "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                )
                == 0,
                "Workbench mobile Comparison overflowed horizontally.",
            )
            mobile_shot = output / "mobile.png"
            mobile_page.screenshot(path=str(mobile_shot), full_page=False)
            summary["screenshots"].append(
                {
                    "path": "mobile.png",
                    "sha256": sha256_file(mobile_shot),
                    "size": mobile_shot.stat().st_size,
                }
            )
            summary["checks"].append("mobile-catalog-negative-and-comparison-no-overflow")
            mobile.close()
            browser.close()
            browser = None

        external = [item for item in summary["network"] if item["origin"] not in {origin, "[blob]"}]
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
        if server is not None:
            if server_started:
                server.shutdown()
            server.server_close()
        if server_thread is not None:
            server_thread.join(timeout=5)
        summary["server_thread_stopped"] = (
            server_thread is None or not server_thread.is_alive()
        )
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
        print(
            "M11 Workbench acceptance left a server thread, port, or SQLite sidecar behind.",
            file=sys.stderr,
        )
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
