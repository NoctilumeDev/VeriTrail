from __future__ import annotations

import argparse
import hashlib
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
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m12-r2-runs-acceptance"
EXPECTED_RUNS = {
    "m11-gateb-v2-ink-positive-01": ("COMPLETED", "PASS"),
    "m11-gateb-v2-ink-browser-negative-01": ("COMPLETED", "FAIL"),
    "m11-gateb-v2-ink-port-conflict-01": ("ABORTED", "PENDING"),
    "m11-gateb-v2-ink-recovery-positive-02": ("COMPLETED", "PASS"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


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


def require(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def response_fact(response: Any) -> dict[str, Any]:
    parsed = urlsplit(response.url)
    origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme != "blob" else "[blob]"
    return {
        "method": response.request.method,
        "origin": origin,
        "path": parsed.path if parsed.scheme != "blob" else "[blob]",
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


def root_overflow(page: Any) -> int:
    return page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


def save_screenshot(page: Any, output: Path, summary: dict[str, Any], name: str) -> None:
    path = output / name
    page.screenshot(path=str(path), full_page=False)
    summary["screenshots"].append(
        {"path": name, "sha256": sha256_file(path), "size": path.stat().st_size}
    )


def catalog_rows(page: Any) -> list[dict[str, Any]]:
    return page.locator("[data-catalog-run-id]").evaluate_all(
        """nodes => nodes.map(node => {
          const execution = node.querySelector('.catalog-run__execution .status-badge')
          const verdict = node.querySelector('.catalog-run__verdict .status-badge')
          const executionStyle = getComputedStyle(execution)
          const verdictStyle = getComputedStyle(verdict)
          return {
            runId: node.querySelector('.catalog-run__identity strong')?.textContent?.trim(),
            execution: node.querySelector('.catalog-run__execution')?.textContent?.trim(),
            verdict: node.querySelector('.catalog-run__verdict')?.textContent?.trim(),
            children: [...node.children].map(child => child.className),
            executionShape: {
              left: executionStyle.borderLeftWidth,
              right: executionStyle.borderRightWidth,
              top: executionStyle.borderTopWidth,
            },
            verdictShape: {
              left: verdictStyle.borderLeftWidth,
              right: verdictStyle.borderRightWidth,
              top: verdictStyle.borderTopWidth,
            },
          }
        })"""
    )


def verify_catalog_facts(page: Any, expect: Any, summary: dict[str, Any]) -> list[dict[str, Any]]:
    expect(page.get_by_test_id("run-catalog")).to_be_visible()
    expect(page.get_by_test_id("catalog-runs")).to_be_visible()
    expect(page.get_by_test_id("catalog-columns")).to_contain_text("Run / 时间")
    expect(page.get_by_test_id("catalog-columns")).to_contain_text("运行状态")
    expect(page.get_by_test_id("catalog-columns")).to_contain_text("验收结论")
    expect(page.get_by_test_id("catalog-columns")).to_contain_text("Plan / 目录事实")
    rows = catalog_rows(page)
    require(len(rows) == len(EXPECTED_RUNS), "R2 Catalog did not expose the four M11 Gate B Runs.")
    expected_children = [
        "catalog-run__identity",
        "catalog-run__execution",
        "catalog-run__verdict",
        "catalog-run__facts",
    ]
    for row in rows:
        run_id = row["runId"]
        require(run_id in EXPECTED_RUNS, f"R2 Catalog exposed an unexpected Run: {run_id}")
        execution, verdict = EXPECTED_RUNS[run_id]
        require(execution in row["execution"], f"R2 Catalog lost execution fact for {run_id}")
        require(verdict in row["verdict"], f"R2 Catalog lost verdict fact for {run_id}")
        require(row["children"] == expected_children, f"R2 Catalog changed column order for {run_id}")
        require(row["executionShape"]["left"] == "1px", f"R2 execution badge lost its framed grammar for {run_id}")
        require(row["verdictShape"]["left"] == "3px", f"R2 verdict badge lost its left-plaque grammar for {run_id}")
        require(row["verdictShape"]["right"] == "0px", f"R2 verdict badge became a second framed button for {run_id}")
    require(root_overflow(page) == 0, "R2 desktop Catalog overflowed horizontally.")
    summary["desktop_catalog_rows"] = rows
    return rows


def verify_source_tools(page: Any, expect: Any, summary: dict[str, Any]) -> None:
    toolstrip = page.get_by_test_id("runs-toolstrip")
    expect(toolstrip).to_be_visible()
    fixtures = page.get_by_role("group", name="示例证据")
    expect(fixtures).to_be_visible()
    for test_id, label in (
        ("fixture-positive", "正向证据"),
        ("fixture-negative", "负向证据"),
        ("fixture-invalid", "校验损坏包"),
    ):
        expect(page.get_by_test_id(test_id)).to_have_text(label)
    local_input = page.get_by_test_id("local-bundle-input")
    expect(local_input).to_be_visible()
    require(
        local_input.evaluate("element => element.parentElement?.tagName") == "LABEL",
        "R2 local evidence input is no longer owned by its labelled native control.",
    )
    summary["source_tool_labels"] = ["示例证据", "正向证据", "负向证据", "校验损坏包", "选择本地证据包"]


def verify_desktop(page: Any, expect: Any, gate_b: Path, output: Path, summary: dict[str, Any]) -> None:
    page.goto(summary["origin"], wait_until="load")
    verify_source_tools(page, expect, summary)
    rows = verify_catalog_facts(page, expect, summary)
    save_screenshot(page, output, summary, "desktop-catalog.png")

    negative = page.get_by_test_id("fixture-negative")
    negative.click()
    expect(page.get_by_test_id("status-gate")).to_contain_text("FAIL")
    page.get_by_test_id("fixture-positive").click()
    expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
    summary["checks"].append("desktop-demo-source-selection-keeps-status-facts")

    first_row = page.locator("[data-catalog-run-id]").first
    catalog_run_id = first_row.get_attribute("data-catalog-run-id")
    require(catalog_run_id is not None, "R2 first Catalog row lost its return-focus identifier.")
    first_row.click()
    expect(page.get_by_test_id("run-summary")).to_be_visible()
    page.get_by_test_id("catalog-return").click()
    require(
        page.evaluate("document.activeElement?.getAttribute('data-catalog-run-id')") == catalog_run_id,
        "R2 Catalog return did not restore focus to its originating native Run button.",
    )
    summary["checks"].append("desktop-catalog-return-focus")

    local_input = page.get_by_test_id("local-bundle-input")
    local_positive = gate_b / "runs" / "m11-gateb-v2-ink-positive-01"
    local_input.set_input_files(str(local_positive))
    expect(page.get_by_test_id("run-summary")).to_contain_text("m11-gateb-v2-ink-positive-01")
    require(page.url.endswith("?fixture=local"), "R2 local bundle did not preserve its local-source URL state.")
    summary["checks"].append("desktop-local-bundle-load")

    corrupted = gate_b / "runs" / "m11-gateb-v2-corrupted-copy"
    local_input.set_input_files(str(corrupted))
    expect(page.get_by_test_id("error-state")).to_be_visible()
    page.get_by_test_id("retry-positive").click()
    expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
    summary["checks"].append("desktop-corrupted-local-bundle-recovery")

    require(root_overflow(page) == 0, "R2 desktop detail after local recovery overflowed horizontally.")
    summary["desktop_catalog_run_count"] = len(rows)


def verify_mobile(
    browser: Any,
    expect: Any,
    output: Path,
    summary: dict[str, Any],
    width: int,
    height: int,
) -> None:
    context = browser.new_context(
        viewport={"width": width, "height": height},
        is_mobile=True,
        reduced_motion="reduce",
    )
    page = context.new_page()
    add_page_observers(page, summary)
    try:
        page.goto(summary["origin"], wait_until="load")
        verify_source_tools(page, expect, summary)
        expect(page.get_by_test_id("run-catalog")).to_be_visible()
        expect(page.get_by_test_id("catalog-columns")).to_be_hidden()
        aborted = page.get_by_role("button", name="Run m11-gateb-v2-ink-port-conflict-01")
        expect(aborted).to_contain_text("ABORTED")
        expect(aborted).to_contain_text("PENDING")
        require(root_overflow(page) == 0, f"R2 {width}px Catalog overflowed horizontally.")
        save_screenshot(page, output, summary, f"mobile-{width}-catalog.png")
        summary["checks"].append(f"mobile-{width}-source-tools-catalog-and-no-overflow")
    finally:
        context.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate M12 R2 Runs presentation.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18784)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate_b = args.gate_b.resolve()
    catalog = gate_b / "catalog"
    artifacts = gate_b / "runs"
    dist = args.dist.resolve()
    output = args.output.resolve()
    port = args.port
    if output.exists():
        print("M12 R2 acceptance refuses to overwrite its output directory.", file=sys.stderr)
        return 2
    if not 1024 <= port <= 65535 or not port_is_free(port):
        print("M12 R2 acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if not (catalog / "catalog.sqlite3").is_file() or not artifacts.is_dir() or not (dist / "index.html").is_file():
        print("M12 R2 acceptance requires the complete M11 Gate B catalog and production build.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m12-r2-runs-presentation",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "verdict": "PENDING",
        "origin": f"http://127.0.0.1:{port}",
        "checks": [],
        "console_messages": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
        "gate_b_directory": gate_b.name,
    }
    server = None
    server_thread = None
    browser = None
    exit_code = 1
    try:
        server = create_catalog_server(
            catalog_root=catalog,
            artifact_root=artifacts,
            web_root=dist,
            port=port,
        )
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                summary["browser_version"] = browser.version
                desktop = browser.new_context(viewport={"width": 1440, "height": 960})
                page = desktop.new_page()
                add_page_observers(page, summary)
                verify_desktop(page, expect, gate_b, output, summary)
                desktop.close()
                verify_mobile(browser, expect, output, summary, 390, 844)
                verify_mobile(browser, expect, output, summary, 360, 800)
            finally:
                browser.close()
                browser = None

        external = [item for item in summary["network"] if item["origin"] not in {summary["origin"], "[blob]"}]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        require(not summary["console_messages"], "M12 R2 emitted Console warnings or errors.")
        require(not summary["page_errors"], "M12 R2 emitted page errors.")
        require(not summary["request_failures"], "M12 R2 emitted failed network requests.")
        require(not external and not writes and not http_errors, "M12 R2 crossed its same-origin read-only network boundary.")
        summary["network_request_count"] = len(summary["network"])
        summary["execution_status"] = "COMPLETED"
        summary["verdict"] = "PASS"
        exit_code = 0
    except Exception as error:
        summary["execution_status"] = "ERROR"
        summary["verdict"] = "PENDING"
        summary["error"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        if browser is not None:
            browser.close()
        if server is not None:
            server.shutdown()
            server.server_close()
        if server_thread is not None:
            server_thread.join(timeout=5)
        summary["port_released"] = port_is_free(port)
        summary["server_thread_stopped"] = server_thread is None or not server_thread.is_alive()
        summary["finished_at"] = utc_now()
        (output / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(
        json.dumps(
            {
                key: summary[key]
                for key in ("checks", "execution_status", "verdict", "port_released", "server_thread_stopped")
            },
            ensure_ascii=False,
        )
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
