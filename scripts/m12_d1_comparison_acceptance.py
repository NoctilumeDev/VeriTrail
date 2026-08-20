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
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from veritrail.local_api import create_catalog_server


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATE_B = REPOSITORY_ROOT / "tmp" / "m11-gateb-contract04-20260814-161647"
DEFAULT_DRIFT = REPOSITORY_ROOT / "artifacts" / "m6-comparison-drift-20260809"
DEFAULT_INCONCLUSIVE = REPOSITORY_ROOT / "artifacts" / "m6-comparison-inconclusive-20260809"
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m12-d1-comparison-acceptance"


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


def require_complete_comparison(path: Path, label: str) -> None:
    required = ("comparison-manifest.json", "comparison.json", "comparison.md")
    if not path.is_dir() or any(not (path / name).is_file() for name in required):
        raise ValueError(f"M12-D1 requires a complete {label} Comparison Bundle.")


def require_no_root_overflow(page: Any, label: str) -> None:
    overflow = page.evaluate("Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)")
    require(overflow == 0, f"{label} overflowed horizontally by {overflow}px.")


def open_comparison_view(page: Any, origin: str, expect: Any) -> None:
    page.goto(f"{origin}?view=comparison", wait_until="load")
    expect(page.get_by_test_id("view-comparison-title")).to_be_visible()
    expect(page.get_by_test_id("local-comparison-input")).to_be_visible()


def assert_comparison(
    page: Any,
    expect: Any,
    path: Path,
    status: str,
    label: str,
) -> None:
    page.get_by_test_id("local-comparison-input").set_input_files(str(path))
    expect(page.get_by_test_id("comparison-view")).to_be_visible()
    status_gate = page.get_by_test_id("comparison-status")
    expect(status_gate).to_contain_text(status)
    expected_class = f"comparison-mirror__verdict--{status.lower()}"
    require(
        status_gate.evaluate(
            "(element, className) => element.classList.contains(className)", expected_class
        ),
        f"{label} did not keep its independent ComparisonStatus class.",
    )
    source_ids = page.locator('[data-testid^="comparison-source-"]').evaluate_all(
        "nodes => nodes.map(node => node.getAttribute('data-testid'))"
    )
    require(
        source_ids == ["comparison-source-baseline", "comparison-source-repeat"],
        f"{label} changed the fixed BASELINE -> REPEAT source order.",
    )
    require_no_root_overflow(page, label)
    if status == "MATCH":
        expect(page.get_by_test_id("comparison-no-differences")).to_be_visible()
    elif status == "DRIFT":
        differences = page.get_by_test_id("comparison-differences")
        expect(differences).to_be_visible()
        expect(differences).to_contain_text("BASELINE")
        expect(differences).to_contain_text("REPEAT")
    else:
        expect(status_gate).to_contain_text("可比较")
        expect(status_gate).to_contain_text("否")


def save_screenshot(page: Any, output: Path, summary: dict[str, Any], name: str) -> None:
    path = output / name
    page.screenshot(path=str(path), full_page=False)
    summary["screenshots"].append(
        {"path": name, "sha256": sha256_file(path), "size": path.stat().st_size}
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the M12-D1 Comparison presentation slice.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--drift", type=Path, default=DEFAULT_DRIFT)
    parser.add_argument("--inconclusive", type=Path, default=DEFAULT_INCONCLUSIVE)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18780)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate_b = args.gate_b.resolve()
    match = gate_b / "comparison"
    drift = args.drift.resolve()
    inconclusive = args.inconclusive.resolve()
    catalog = gate_b / "catalog"
    artifacts = gate_b / "runs"
    dist = args.dist.resolve()
    output = args.output.resolve()

    if output.exists():
        print("M12-D1 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M12-D1 acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if not (catalog / "catalog-manifest.json").is_file() or not artifacts.is_dir() or not (dist / "index.html").is_file():
        print("M12-D1 acceptance requires the complete M11 Gate B catalog and production build.", file=sys.stderr)
        return 2
    try:
        require_complete_comparison(match, "M11 MATCH")
        require_complete_comparison(drift, "DRIFT fixture")
        require_complete_comparison(inconclusive, "INCONCLUSIVE fixture")
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m12-d1-comparison-presentation",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "checks": [],
        "console_messages": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
        "m11_match_directory": gate_b.name,
        "fixture_directories": {"drift": drift.name, "inconclusive": inconclusive.name},
    }
    server = None
    server_thread = None
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

        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            summary["browser_version"] = browser.version

            desktop = browser.new_context(viewport={"width": 1440, "height": 960})
            desktop_page = desktop.new_page()
            add_page_observers(desktop_page, summary)
            open_comparison_view(desktop_page, origin, expect)
            desktop_page.get_by_test_id("cross-axis-toggle").click()
            desktop_page.get_by_test_id("cross-axis-runs").click()
            expect(desktop_page.get_by_test_id("run-catalog")).to_be_visible()
            desktop_page.go_back(wait_until="load")
            expect(desktop_page.get_by_test_id("local-comparison-input")).to_be_visible()
            desktop_page.go_forward(wait_until="load")
            expect(desktop_page.get_by_test_id("run-catalog")).to_be_visible()
            desktop_page.go_back(wait_until="load")
            expect(desktop_page.get_by_test_id("local-comparison-input")).to_be_visible()
            summary["checks"].append("desktop-cross-axis-history-keeps-comparison-entry")

            assert_comparison(desktop_page, expect, match, "MATCH", "desktop M11 MATCH")
            sources = desktop_page.get_by_test_id("comparison-sources")
            expect(sources).to_contain_text("m11-gateb-v2-ink-positive-01")
            expect(sources).to_contain_text("m11-gateb-v2-ink-recovery-positive-02")
            save_screenshot(desktop_page, output, summary, "desktop-match.png")
            summary["checks"].append("desktop-real-m11-match-source-axis")

            assert_comparison(desktop_page, expect, drift, "DRIFT", "desktop DRIFT")
            save_screenshot(desktop_page, output, summary, "desktop-drift.png")
            summary["checks"].append("desktop-drift-difference-axis")

            assert_comparison(desktop_page, expect, inconclusive, "INCONCLUSIVE", "desktop INCONCLUSIVE")
            summary["checks"].append("desktop-inconclusive-remains-non-comparable")

            with tempfile.TemporaryDirectory() as temporary_directory:
                corrupted = Path(temporary_directory) / "corrupted-comparison"
                shutil.copytree(match, corrupted)
                changed = corrupted / "comparison.json"
                changed.write_bytes(changed.read_bytes() + b" ")
                desktop_page.get_by_test_id("local-comparison-input").set_input_files(str(corrupted))
                expect(desktop_page.get_by_test_id("error-state")).to_contain_text("COMPARISON_SIZE_MISMATCH")
                require(
                    desktop_page.get_by_test_id("comparison-view").count() == 0,
                    "A corrupted Comparison exposed partial trusted facts.",
                )
                desktop_page.get_by_test_id("local-comparison-input").set_input_files(str(match))
                expect(desktop_page.get_by_test_id("comparison-status")).to_contain_text("MATCH")
            summary["checks"].append("desktop-corruption-contained-and-local-reselection-recovers")
            desktop.close()

            mobile_390 = browser.new_context(
                viewport={"width": 390, "height": 844}, is_mobile=True, reduced_motion="reduce"
            )
            mobile_390_page = mobile_390.new_page()
            add_page_observers(mobile_390_page, summary)
            open_comparison_view(mobile_390_page, origin, expect)
            assert_comparison(mobile_390_page, expect, match, "MATCH", "390px M11 MATCH")
            save_screenshot(mobile_390_page, output, summary, "mobile-390-match.png")
            summary["checks"].append("mobile-390-real-match-no-overflow")
            mobile_390.close()

            mobile_360 = browser.new_context(
                viewport={"width": 360, "height": 800}, is_mobile=True, reduced_motion="reduce"
            )
            mobile_360_page = mobile_360.new_page()
            add_page_observers(mobile_360_page, summary)
            open_comparison_view(mobile_360_page, origin, expect)
            assert_comparison(mobile_360_page, expect, drift, "DRIFT", "360px DRIFT")
            assert_comparison(mobile_360_page, expect, inconclusive, "INCONCLUSIVE", "360px INCONCLUSIVE")
            save_screenshot(mobile_360_page, output, summary, "mobile-360-inconclusive.png")
            summary["checks"].append("mobile-360-drift-and-inconclusive-no-overflow")
            mobile_360.close()

            browser.close()
            browser = None

        external = [item for item in summary["network"] if item["origin"] not in {origin, "[blob]"}]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        if summary["console_messages"] or summary["page_errors"] or summary["request_failures"]:
            raise AssertionError("Workbench emitted an unexpected browser warning or error.")
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
            server.shutdown()
            server.server_close()
        if server_thread is not None:
            server_thread.join(timeout=5)
        summary["ended_at"] = utc_now()
        summary["network_request_count"] = len(summary["network"])
        (output / "acceptance.json").write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    released = port_is_free(args.port)
    if not released:
        print("M12-D1 acceptance did not release its loopback port.", file=sys.stderr)
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
                "port_released": True,
                "output": output.name,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
