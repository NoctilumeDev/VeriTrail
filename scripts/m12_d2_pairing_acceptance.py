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
DEFAULT_SUPPORTED = REPOSITORY_ROOT / "artifacts" / "m7-paired-supported-20260809"
DEFAULT_CONTRADICTED = REPOSITORY_ROOT / "artifacts" / "m7-paired-contradicted-20260809"
DEFAULT_INCONCLUSIVE = REPOSITORY_ROOT / "artifacts" / "m7-paired-inconclusive-20260809"
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m12-d2-pairing-acceptance"
PAIRING_FILES = (
    "paired-analysis-manifest.json",
    "sealed-pairing-plan.json",
    "paired-analysis.json",
    "paired-analysis.md",
)
ROLES = ("BASELINE", "TREATMENT", "RESTORED_BASELINE", "NEGATIVE_CONTROL")


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


def pairing_files(path: Path) -> list[str]:
    return [str(path / name) for name in PAIRING_FILES]


def require_complete_pairing(path: Path, label: str) -> None:
    if not path.is_dir() or any(not (path / name).is_file() for name in PAIRING_FILES):
        raise ValueError(f"M12-D2 requires a complete {label} PairedAnalysis.")


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
    overflow = page.evaluate("Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)")
    require(overflow == 0, f"{label} overflowed horizontally by {overflow}px.")


def role_order(page: Any, selector: str) -> list[str]:
    return page.locator(f"{selector} [data-pairing-role]").evaluate_all(
        "nodes => nodes.map(node => node.getAttribute('data-pairing-role'))"
    )


def outcome_role_orders(page: Any) -> list[list[str]]:
    return page.locator('[data-testid="paired-outcomes"] > article').evaluate_all(
        """nodes => nodes.map(outcome => [...outcome.querySelectorAll('[data-pairing-role]')]
          .map(node => node.getAttribute('data-pairing-role')))"""
    )


def outcome_role_is_mismatch(page: Any, role: str) -> bool:
    return page.get_by_test_id("paired-outcomes").locator(
        f'[data-pairing-role="{role}"]'
    ).evaluate_all(
        "nodes => nodes.length > 0 && nodes.every(node => "
        "node.classList.contains('is-mismatch') && node.textContent.includes('不符'))"
    )


def open_pairing_view(page: Any, origin: str, expect: Any) -> None:
    page.goto(f"{origin}?view=pairing", wait_until="load")
    expect(page.get_by_test_id("view-pairing-title")).to_be_visible()
    expect(page.get_by_test_id("local-pairing-input")).to_be_visible()


def pairing_input(page: Any) -> Any:
    input_element = page.get_by_test_id("local-pairing-input")
    if input_element.count() == 0:
        input_element = page.get_by_label("重新选择本地 VeriTrail PairedAnalysis 四个文件")
    return input_element


def assert_pairing(page: Any, expect: Any, path: Path, status: str, label: str) -> None:
    input_element = pairing_input(page)
    require(input_element.count() == 1, f"{label} lost its explicit local PairedAnalysis selector.")
    input_element.set_input_files(pairing_files(path))
    expect(page.get_by_test_id("paired-analysis-view")).to_be_visible()
    status_gate = page.get_by_test_id("paired-analysis-status")
    expect(status_gate).to_contain_text(status)
    expect(status_gate).to_have_attribute("aria-label", f"配对分析：{status}")
    analysis_view = page.get_by_test_id("paired-analysis-view")
    expected_class = f"pairing-page--{status.lower()}"
    require(
        analysis_view.evaluate(
            "(element, className) => element.classList.contains(className)", expected_class
        ),
        f"{label} did not expose its independent AnalysisStatus presentation state.",
    )
    require(
        role_order(page, '[data-testid="paired-sequence"]') == list(ROLES),
        f"{label} changed the sealed sequence order.",
    )
    require_no_root_overflow(page, label)


def save_screenshot(page: Any, output: Path, summary: dict[str, Any], name: str) -> None:
    path = output / name
    page.screenshot(path=str(path), full_page=False)
    summary["screenshots"].append(
        {"path": name, "sha256": sha256_file(path), "size": path.stat().st_size}
    )


def verify_status_specific_facts(page: Any, expect: Any, status: str) -> None:
    page.get_by_test_id("pairing-open-sources").click()
    expect(page.get_by_test_id("paired-sources")).to_be_visible()
    require(
        role_order(page, '[data-testid="paired-sources"]') == list(ROLES),
        f"{status} changed the source-ledger order.",
    )
    if status == "SUPPORTED":
        expect(
            page.get_by_test_id("paired-sources").locator('[data-pairing-role="TREATMENT"]')
        ).to_contain_text("FAIL")
    elif status == "CONTRADICTED":
        expect(
            page.get_by_test_id("paired-sources").locator('[data-pairing-role="TREATMENT"]')
        ).to_contain_text("PASS")
    else:
        expect(
            page.get_by_test_id("paired-sources").locator('[data-pairing-role="NEGATIVE_CONTROL"]')
        ).to_contain_text("FAIL")
    require_no_root_overflow(page, f"{status} Pairing source ledger")
    page.get_by_test_id("pairing-panel-return").click()
    expect(page.get_by_test_id("paired-analysis-status")).to_be_visible()

    page.get_by_test_id("pairing-open-outcomes").click()
    expect(page.get_by_test_id("paired-outcomes")).to_be_visible()
    orders = outcome_role_orders(page)
    require(
        orders and all(order == list(ROLES) for order in orders),
        f"{status} changed a preregistered outcome order.",
    )
    if status == "CONTRADICTED":
        require(
            outcome_role_is_mismatch(page, "TREATMENT"),
            "CONTRADICTED TREATMENT did not remain visibly mismatched in every outcome.",
        )
    elif status == "INCONCLUSIVE":
        require(
            outcome_role_is_mismatch(page, "NEGATIVE_CONTROL"),
            "INCONCLUSIVE NEGATIVE_CONTROL did not remain visibly mismatched in every outcome.",
        )
    require_no_root_overflow(page, f"{status} Pairing outcome ledger")
    page.get_by_test_id("pairing-panel-return").click()
    expect(page.get_by_test_id("paired-analysis-status")).to_be_visible()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the M12-D2 Pairing presentation slice.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--supported", type=Path, default=DEFAULT_SUPPORTED)
    parser.add_argument("--contradicted", type=Path, default=DEFAULT_CONTRADICTED)
    parser.add_argument("--inconclusive", type=Path, default=DEFAULT_INCONCLUSIVE)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18785)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate_b = args.gate_b.resolve()
    supported = args.supported.resolve()
    contradicted = args.contradicted.resolve()
    inconclusive = args.inconclusive.resolve()
    catalog = gate_b / "catalog"
    artifacts = gate_b / "runs"
    dist = args.dist.resolve()
    output = args.output.resolve()
    sidecars = (catalog / "catalog.sqlite3-wal", catalog / "catalog.sqlite3-shm")

    if output.exists():
        print("M12-D2 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M12-D2 acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if not (catalog / "catalog-manifest.json").is_file() or not artifacts.is_dir() or not (dist / "index.html").is_file():
        print("M12-D2 acceptance requires the complete M11 Gate B catalog and production build.", file=sys.stderr)
        return 2
    if any(path.exists() for path in sidecars):
        print("M12-D2 acceptance requires a clean read-only Catalog without SQLite sidecars.", file=sys.stderr)
        return 2
    try:
        require_complete_pairing(supported, "SUPPORTED")
        require_complete_pairing(contradicted, "CONTRADICTED")
        require_complete_pairing(inconclusive, "INCONCLUSIVE")
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m12-d2-pairing-presentation",
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
        "fixture_directories": {
            "supported": supported.name,
            "contradicted": contradicted.name,
            "inconclusive": inconclusive.name,
        },
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
            open_pairing_view(desktop_page, origin, expect)
            desktop_page.get_by_test_id("cross-axis-runs").click()
            expect(desktop_page.get_by_test_id("run-catalog")).to_be_visible()
            desktop_page.go_back(wait_until="load")
            expect(desktop_page.get_by_test_id("local-pairing-input")).to_be_visible()
            desktop_page.go_forward(wait_until="load")
            expect(desktop_page.get_by_test_id("run-catalog")).to_be_visible()
            desktop_page.go_back(wait_until="load")
            expect(desktop_page.get_by_test_id("local-pairing-input")).to_be_visible()
            summary["checks"].append("desktop-fixed-navigation-history-keeps-pairing-entry")

            assert_pairing(desktop_page, expect, supported, "SUPPORTED", "desktop SUPPORTED")
            verify_status_specific_facts(desktop_page, expect, "SUPPORTED")
            save_screenshot(desktop_page, output, summary, "desktop-supported.png")
            summary["checks"].append("desktop-supported-status-source-and-sequence-separation")

            assert_pairing(desktop_page, expect, contradicted, "CONTRADICTED", "desktop CONTRADICTED")
            verify_status_specific_facts(desktop_page, expect, "CONTRADICTED")
            save_screenshot(desktop_page, output, summary, "desktop-contradicted.png")
            summary["checks"].append("desktop-contradicted-treatment-mismatch-remains-distinct")

            assert_pairing(desktop_page, expect, inconclusive, "INCONCLUSIVE", "desktop INCONCLUSIVE")
            verify_status_specific_facts(desktop_page, expect, "INCONCLUSIVE")
            summary["checks"].append("desktop-inconclusive-negative-control-mismatch-remains-distinct")

            with tempfile.TemporaryDirectory() as temporary_directory:
                corrupted = Path(temporary_directory) / "corrupted-pairing"
                shutil.copytree(supported, corrupted)
                changed = corrupted / "paired-analysis.json"
                changed.write_bytes(changed.read_bytes() + b" ")
                pairing_input(desktop_page).set_input_files(pairing_files(corrupted))
                expect(desktop_page.get_by_test_id("error-state")).to_contain_text("PAIRING_SIZE_MISMATCH")
                require(
                    desktop_page.get_by_test_id("paired-analysis-view").count() == 0,
                    "A corrupted Pairing exposed partial trusted facts.",
                )
                pairing_input(desktop_page).set_input_files(pairing_files(supported))
                expect(desktop_page.get_by_test_id("paired-analysis-status")).to_contain_text("SUPPORTED")
            summary["checks"].append("desktop-corruption-contained-and-explicit-reselection-recovers")

            desktop_page.reload(wait_until="load")
            expect(desktop_page.get_by_test_id("error-state")).to_contain_text("PAIRING_RESELECT_REQUIRED")
            require(
                desktop_page.get_by_test_id("paired-analysis-view").count() == 0,
                "A refreshed page retained private local Pairing facts.",
            )
            summary["checks"].append("desktop-refresh-requires-local-pairing-reselection")
            desktop.close()

            mobile_390 = browser.new_context(
                viewport={"width": 390, "height": 844}, is_mobile=True, reduced_motion="reduce"
            )
            mobile_390_page = mobile_390.new_page()
            add_page_observers(mobile_390_page, summary)
            open_pairing_view(mobile_390_page, origin, expect)
            assert_pairing(mobile_390_page, expect, supported, "SUPPORTED", "390px SUPPORTED")
            verify_status_specific_facts(mobile_390_page, expect, "SUPPORTED")
            save_screenshot(mobile_390_page, output, summary, "mobile-390-supported.png")
            summary["checks"].append("mobile-390-supported-four-role-sequence-and-no-overflow")
            mobile_390.close()

            mobile_360 = browser.new_context(
                viewport={"width": 360, "height": 800}, is_mobile=True, reduced_motion="reduce"
            )
            mobile_360_page = mobile_360.new_page()
            add_page_observers(mobile_360_page, summary)
            open_pairing_view(mobile_360_page, origin, expect)
            assert_pairing(mobile_360_page, expect, contradicted, "CONTRADICTED", "360px CONTRADICTED")
            verify_status_specific_facts(mobile_360_page, expect, "CONTRADICTED")
            assert_pairing(mobile_360_page, expect, inconclusive, "INCONCLUSIVE", "360px INCONCLUSIVE")
            verify_status_specific_facts(mobile_360_page, expect, "INCONCLUSIVE")
            save_screenshot(mobile_360_page, output, summary, "mobile-360-inconclusive.png")
            summary["checks"].append("mobile-360-contradicted-and-inconclusive-no-overflow")
            mobile_360.close()

            browser.close()
            browser = None

        external = [item for item in summary["network"] if item["origin"] not in {origin, "[blob]"}]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        require(not summary["console_messages"], "Workbench emitted an unexpected browser warning or error.")
        require(not summary["page_errors"], "Workbench emitted an unexpected page error.")
        require(not summary["request_failures"], "Workbench emitted an unexpected failed request.")
        require(not external and not writes and not http_errors, "Workbench crossed the same-origin read-only network boundary.")
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
        print("M12-D2 acceptance did not release its loopback port.", file=sys.stderr)
        return 1
    if not summary["server_thread_stopped"] or not summary["sqlite_sidecars_absent"]:
        print("M12-D2 acceptance did not leave its read-only service boundary clean.", file=sys.stderr)
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
