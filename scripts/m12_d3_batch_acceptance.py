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
DEFAULT_ANALYSES = REPOSITORY_ROOT / "artifacts" / "m8-batch-runtime-v3-20260811" / "analyses"
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m12-d3-batch-acceptance"
BATCH_FILES = (
    "batch-analysis-manifest.json",
    "sealed-batch-plan.json",
    "batch-analysis.json",
    "batch-analysis.md",
)
EXPECTED_STATES = {
    "SUPPORTED": ("COMPLETE", "SUPPORTED"),
    "CONTRADICTED": ("COMPLETE", "CONTRADICTED"),
    "INCOMPLETE": ("INCOMPLETE", "INCONCLUSIVE"),
    "INCONCLUSIVE": ("INCONCLUSIVE", "INCONCLUSIVE"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: object, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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


def batch_files(path: Path) -> list[str]:
    return [str(path / name) for name in BATCH_FILES]


def require_complete_batch(path: Path, label: str) -> None:
    require(path.is_dir(), f"M12-D3 requires the {label} analysis directory.")
    missing = [name for name in BATCH_FILES if not (path / name).is_file()]
    require(not missing, f"M12-D3 {label} analysis is missing: {', '.join(missing)}.")


def read_batch_order(path: Path) -> tuple[list[str], list[str]]:
    analysis = json.loads((path / "batch-analysis.json").read_text(encoding="utf-8"))
    profiles = [str(profile["id"]) for profile in analysis["profiles"]]
    slots = [str(slot["slot_id"]) for slot in analysis["slots"]]
    return profiles, slots


def response_fact(response: Any) -> dict[str, Any]:
    parsed = urlsplit(response.url)
    return {
        "method": response.request.method,
        "origin": f"{parsed.scheme}://{parsed.netloc}",
        "path": parsed.path,
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
    overflow = page.evaluate("Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)")
    require(overflow == 0, f"{label} overflowed horizontally by {overflow}px.")


def dom_order(page: Any, selector: str, attribute: str) -> list[str]:
    return page.locator(selector).evaluate_all(
        "(nodes, attribute) => nodes.map(node => node.getAttribute(attribute))", attribute
    )


def save_screenshot(page: Any, output: Path, summary: dict[str, Any], name: str) -> None:
    path = output / name
    page.screenshot(path=str(path), full_page=False)
    summary["screenshots"].append(
        {"path": name, "sha256": sha256_file(path), "size": path.stat().st_size}
    )


def open_batch_view(page: Any, origin: str, expect: Any) -> None:
    page.goto(f"{origin}?view=batch", wait_until="load")
    expect(page.get_by_test_id("view-batch-title")).to_be_visible()
    expect(page.get_by_test_id("local-batch-input")).to_be_visible()


def import_and_verify_batch(
    page: Any,
    expect: Any,
    path: Path,
    label: str,
    status: str,
    require_matrix_focus: bool,
) -> None:
    coverage, hypothesis = EXPECTED_STATES[status]
    expected_profiles, expected_slots = read_batch_order(path)
    page.get_by_test_id("local-batch-input").set_input_files(batch_files(path))
    expect(page.get_by_test_id("batch-analysis-view")).to_be_visible()
    coverage_gate = page.get_by_test_id("batch-coverage-status")
    hypothesis_gate = page.get_by_test_id("batch-hypothesis-status")
    expect(coverage_gate).to_contain_text(coverage)
    expect(hypothesis_gate).to_contain_text(hypothesis)
    require(
        coverage_gate.evaluate(
            "(element, className) => element.classList.contains(className)",
            f"batch-analysis-status--{coverage.lower()}",
        ),
        f"{label} lost its independent CoverageStatus class.",
    )
    require(
        hypothesis_gate.evaluate(
            "(element, className) => element.classList.contains(className)",
            f"batch-analysis-status--{hypothesis.lower()}",
        ),
        f"{label} lost its independent HypothesisStatus class.",
    )
    require(
        dom_order(page, '[data-testid="batch-profile-matrix"] tbody tr', "data-batch-profile")
        == expected_profiles,
        f"{label} changed the sealed Profile matrix order.",
    )
    require(
        dom_order(page, '[data-testid="batch-wave-list"] [data-batch-slot]', "data-batch-slot")
        == expected_slots,
        f"{label} changed the sealed slot order.",
    )
    matrix = page.locator('[aria-label="全因子 Profile 矩阵"]')
    require(matrix.get_attribute("role") == "region", f"{label} lost the named matrix region.")
    require(matrix.get_attribute("tabindex") == "0", f"{label} lost the matrix keyboard target.")
    require(
        page.locator('[data-testid="batch-wave-list"] details').count() > 0
        and page.locator('[data-testid="batch-wave-list"] details').first.evaluate(
            "node => node instanceof HTMLDetailsElement"
        ),
        f"{label} replaced native outcome details.",
    )
    expect(page.get_by_test_id("batch-boundary")).to_contain_text("不证明真实并行")
    require_no_root_overflow(page, label)

    if status == "SUPPORTED":
        expect(page.get_by_test_id("batch-wave-list")).to_contain_text("FAIL")
    elif status == "CONTRADICTED":
        expect(page.get_by_test_id("batch-reasons")).to_contain_text("BATCH_HYPOTHESIS_CONTRADICTED")
        expect(page.get_by_test_id("batch-profile-matrix")).to_contain_text("2")
    elif status == "INCOMPLETE":
        expect(page.get_by_test_id("batch-wave-list")).to_contain_text("MISSING")
        expect(page.get_by_test_id("batch-wave-list")).to_contain_text("来源 Run 未提供")
    else:
        expect(page.get_by_test_id("batch-reasons")).to_contain_text("WAVE_ORDER_MISMATCH")

    if require_matrix_focus:
        view_title = page.get_by_test_id("view-batch-title")
        view_title.focus()
        view_title.press("Tab")
        require(
            page.evaluate("document.activeElement?.getAttribute('aria-label')") == "全因子 Profile 矩阵",
            f"{label} did not advance from its stable view title to the matrix region by keyboard.",
        )


def require_local_matrix_scroll(page: Any, label: str) -> None:
    metrics = page.locator(".batch-matrix-scroll").evaluate(
        """element => {
          const before = element.scrollLeft;
          element.scrollLeft = Math.max(1, Math.floor(element.scrollWidth - element.clientWidth));
          return { before, after: element.scrollLeft, clientWidth: element.clientWidth, scrollWidth: element.scrollWidth };
        }"""
    )
    require(
        metrics["scrollWidth"] > metrics["clientWidth"] and metrics["after"] > metrics["before"],
        f"{label} did not preserve a usable local matrix scroll region.",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the M12-D3 Batch presentation slice.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--analyses", type=Path, default=DEFAULT_ANALYSES)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18786)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate_b = args.gate_b.resolve()
    analyses_root = args.analyses.resolve()
    analyses = {name: analyses_root / name.lower() for name in EXPECTED_STATES}
    catalog = gate_b / "catalog"
    artifacts = gate_b / "runs"
    dist = args.dist.resolve()
    output = args.output.resolve()
    sidecars = (catalog / "catalog.sqlite3-wal", catalog / "catalog.sqlite3-shm")

    if output.exists():
        print("M12-D3 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M12-D3 acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if not (catalog / "catalog-manifest.json").is_file() or not artifacts.is_dir() or not (dist / "index.html").is_file():
        print("M12-D3 acceptance requires the complete M11 Gate B catalog and production build.", file=sys.stderr)
        return 2
    if any(path.exists() for path in sidecars):
        print("M12-D3 acceptance requires a clean read-only Catalog without SQLite sidecars.", file=sys.stderr)
        return 2
    try:
        for label, path in analyses.items():
            require_complete_batch(path, label)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m12-d3-batch-presentation",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "verdict": "PENDING",
        "checks": [],
        "console_messages": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
        "m11_gate_b_directory": gate_b.name,
        "fixture_directories": {label.lower(): path.name for label, path in analyses.items()},
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
            open_batch_view(desktop_page, origin, expect)
            desktop_page.get_by_test_id("cross-axis-runs").click()
            expect(desktop_page.get_by_test_id("run-catalog")).to_be_visible()
            desktop_page.go_back(wait_until="load")
            expect(desktop_page.get_by_test_id("local-batch-input")).to_be_visible()
            desktop_page.go_forward(wait_until="load")
            expect(desktop_page.get_by_test_id("run-catalog")).to_be_visible()
            desktop_page.go_back(wait_until="load")
            expect(desktop_page.get_by_test_id("local-batch-input")).to_be_visible()
            summary["checks"].append("desktop-fixed-navigation-history-keeps-batch-entry")

            for status in ("SUPPORTED", "CONTRADICTED", "INCOMPLETE", "INCONCLUSIVE"):
                open_batch_view(desktop_page, origin, expect)
                import_and_verify_batch(
                    desktop_page,
                    expect,
                    analyses[status],
                    f"desktop {status}",
                    status,
                    status == "SUPPORTED",
                )
                summary["checks"].append(f"desktop-{status.lower()}-status-order-and-boundary")
            open_batch_view(desktop_page, origin, expect)
            desktop_page.get_by_test_id("local-batch-input").set_input_files(batch_files(analyses["CONTRADICTED"]))
            save_screenshot(desktop_page, output, summary, "desktop-contradicted.png")

            with tempfile.TemporaryDirectory() as temporary_directory:
                corrupted = Path(temporary_directory) / "corrupted-batch"
                shutil.copytree(analyses["SUPPORTED"], corrupted)
                changed = corrupted / "batch-analysis.json"
                changed.write_bytes(changed.read_bytes() + b" ")
                open_batch_view(desktop_page, origin, expect)
                desktop_page.get_by_test_id("local-batch-input").set_input_files(batch_files(corrupted))
                expect(desktop_page.get_by_test_id("error-state")).to_contain_text("BATCH_SIZE_MISMATCH")
                require(
                    desktop_page.get_by_test_id("batch-analysis-view").count() == 0,
                    "A corrupted BatchAnalysis exposed partial trusted facts.",
                )
                desktop_page.get_by_test_id("local-batch-input").set_input_files(batch_files(analyses["SUPPORTED"]))
                expect(desktop_page.get_by_test_id("batch-hypothesis-status")).to_contain_text("SUPPORTED")
            summary["checks"].append("desktop-corruption-contained-and-explicit-reselection-recovers")

            desktop_page.reload(wait_until="load")
            expect(desktop_page.get_by_test_id("error-state")).to_contain_text("BATCH_RESELECT_REQUIRED")
            require(
                desktop_page.get_by_test_id("batch-analysis-view").count() == 0,
                "A refreshed page retained private local BatchAnalysis facts.",
            )
            summary["checks"].append("desktop-refresh-requires-local-batch-reselection")
            desktop.close()

            mobile_390 = browser.new_context(
                viewport={"width": 390, "height": 844}, is_mobile=True, reduced_motion="reduce"
            )
            mobile_390_page = mobile_390.new_page()
            add_page_observers(mobile_390_page, summary)
            open_batch_view(mobile_390_page, origin, expect)
            import_and_verify_batch(
                mobile_390_page, expect, analyses["SUPPORTED"], "390px SUPPORTED", "SUPPORTED", False
            )
            require_local_matrix_scroll(mobile_390_page, "390px SUPPORTED")
            save_screenshot(mobile_390_page, output, summary, "mobile-390-supported.png")
            summary["checks"].append("mobile-390-supported-local-matrix-scroll-no-root-overflow")
            mobile_390.close()

            mobile_360 = browser.new_context(
                viewport={"width": 360, "height": 800}, is_mobile=True, reduced_motion="reduce"
            )
            mobile_360_page = mobile_360.new_page()
            add_page_observers(mobile_360_page, summary)
            open_batch_view(mobile_360_page, origin, expect)
            import_and_verify_batch(
                mobile_360_page, expect, analyses["INCOMPLETE"], "360px INCOMPLETE", "INCOMPLETE", False
            )
            require_local_matrix_scroll(mobile_360_page, "360px INCOMPLETE")
            open_batch_view(mobile_360_page, origin, expect)
            import_and_verify_batch(
                mobile_360_page, expect, analyses["INCONCLUSIVE"], "360px INCONCLUSIVE", "INCONCLUSIVE", False
            )
            save_screenshot(mobile_360_page, output, summary, "mobile-360-inconclusive.png")
            summary["checks"].append("mobile-360-incomplete-and-inconclusive-local-scroll-no-root-overflow")
            mobile_360.close()

            browser.close()
            browser = None

        external = [item for item in summary["network"] if item["origin"] != origin]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        require(not summary["console_messages"], "Workbench emitted an unexpected browser warning or error.")
        require(not summary["page_errors"], "Workbench emitted an unexpected page error.")
        require(not summary["request_failures"], "Workbench emitted an unexpected failed request.")
        require(not external and not writes and not http_errors, "Workbench crossed the same-origin read-only network boundary.")
        require(
            any(item["path"] == "/api/v1/catalog" for item in summary["network"]),
            "Production browser run did not observe the Catalog API.",
        )
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
        summary["port_released"] = port_is_free(args.port)
        summary["server_thread_stopped"] = server_thread is None or not server_thread.is_alive()
        summary["sqlite_sidecars_absent"] = not any(path.exists() for path in sidecars)
        (output / "acceptance.json").write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    if not summary["port_released"]:
        print("M12-D3 acceptance did not release its loopback port.", file=sys.stderr)
        return 1
    if not summary["server_thread_stopped"] or not summary["sqlite_sidecars_absent"]:
        print("M12-D3 acceptance did not leave its read-only service boundary clean.", file=sys.stderr)
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
                "port_released": summary["port_released"],
                "server_thread_stopped": summary["server_thread_stopped"],
                "sqlite_sidecars_absent": summary["sqlite_sidecars_absent"],
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
