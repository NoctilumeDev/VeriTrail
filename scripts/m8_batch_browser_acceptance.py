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

from veritrail.catalog import build_catalog
from veritrail.local_api import create_catalog_server


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m8-batch-browser-acceptance"
BATCH_FILES = (
    "batch-analysis-manifest.json",
    "sealed-batch-plan.json",
    "batch-analysis.json",
    "batch-analysis.md",
)


def batch_files(path: Path) -> list[str]:
    return [str(path / name) for name in BATCH_FILES]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run bounded M8 BatchAnalysis production-browser acceptance."
    )
    parser.add_argument("--supported", type=Path, required=True)
    parser.add_argument("--contradicted", type=Path, required=True)
    parser.add_argument("--incomplete", type=Path, required=True)
    parser.add_argument("--inconclusive", type=Path, required=True)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18771)
    return parser.parse_args()


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


def attach_observers(page: Any, summary: dict[str, Any]) -> None:
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


def screenshot_fact(path: Path) -> dict[str, Any]:
    return {
        "path": path.name,
        "sha256": sha256_file(path),
        "size": path.stat().st_size,
    }


def main() -> int:
    args = parse_args()
    dist = args.dist.resolve()
    output = args.output.resolve()
    analyses = {
        "SUPPORTED": args.supported.resolve(),
        "CONTRADICTED": args.contradicted.resolve(),
        "INCOMPLETE": args.incomplete.resolve(),
        "INCONCLUSIVE": args.inconclusive.resolve(),
    }
    if output.exists():
        print("M8 browser acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M8 browser acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if not (dist / "index.html").is_file():
        print("M8 browser acceptance requires an existing Workbench production build.", file=sys.stderr)
        return 2
    for status, path in analyses.items():
        if not all((path / name).is_file() for name in BATCH_FILES):
            print(
                f"M8 browser acceptance requires a complete {status} BatchAnalysis.",
                file=sys.stderr,
            )
            return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m8-preregistered-full-factorial-batch-workbench",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "verdict": "INCONCLUSIVE",
        "checks": [],
        "console_errors": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
    }
    server = None
    server_thread = None
    browser = None
    exit_code = 1
    origin = f"http://127.0.0.1:{args.port}"
    try:
        from playwright.sync_api import expect, sync_playwright

        with tempfile.TemporaryDirectory() as directory:
            runtime_root = Path(directory)
            empty_artifacts = runtime_root / "empty-artifacts"
            empty_artifacts.mkdir()
            catalog_root = runtime_root / "catalog"
            catalog = build_catalog(empty_artifacts, catalog_root)
            if catalog.run_count != 0:
                raise AssertionError("browser acceptance Catalog must be an empty valid snapshot")
            server = create_catalog_server(
                catalog_root=catalog_root,
                artifact_root=empty_artifacts,
                web_root=dist,
                port=args.port,
            )
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()

            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                summary["browser_version"] = browser.version
                desktop = browser.new_context(viewport={"width": 1280, "height": 800})
                page = desktop.new_page()
                attach_observers(page, summary)
                page.goto(origin, wait_until="load")
                expect(page.get_by_test_id("run-catalog")).to_contain_text("0 Runs")
                batch_input = page.get_by_test_id("local-batch-input")
                batch_input.focus()
                if page.evaluate("document.activeElement?.dataset.testid") != "local-batch-input":
                    raise AssertionError("BatchAnalysis input did not receive keyboard focus")

                expected_states = {
                    "SUPPORTED": ("COMPLETE", "SUPPORTED"),
                    "CONTRADICTED": ("COMPLETE", "CONTRADICTED"),
                    "INCOMPLETE": ("INCOMPLETE", "INCONCLUSIVE"),
                    "INCONCLUSIVE": ("INCONCLUSIVE", "INCONCLUSIVE"),
                }
                for name, (coverage, hypothesis) in expected_states.items():
                    batch_input = page.get_by_test_id("local-batch-input")
                    batch_input.set_input_files(batch_files(analyses[name]))
                    expect(page.get_by_test_id("batch-analysis-view")).to_be_visible()
                    expect(page.get_by_test_id("batch-coverage-status")).to_contain_text(coverage)
                    expect(page.get_by_test_id("batch-hypothesis-status")).to_contain_text(
                        hypothesis
                    )
                    expect(page.get_by_test_id("batch-profile-matrix")).to_contain_text(
                        "combined"
                    )
                    expect(page.get_by_test_id("batch-wave-list")).to_contain_text("FAIL")
                    expect(page.get_by_test_id("batch-boundary")).to_contain_text(
                        "不证明真实并行"
                    )
                    if name == "SUPPORTED":
                        batch_input.focus()
                        batch_input.press("Tab")
                        if page.evaluate(
                            "document.activeElement?.getAttribute('aria-label')"
                        ) != "全因子 Profile 矩阵":
                            raise AssertionError(
                                "BatchAnalysis keyboard focus order is not deterministic"
                            )
                        summary["checks"].append("desktop-keyboard-focus-order")
                    if page.evaluate(
                        "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                    ) != 0:
                        raise AssertionError(f"desktop {name} produced document overflow")
                    if name == "INCOMPLETE":
                        expect(page.get_by_text("来源 Run 未提供", exact=True)).to_be_visible()
                    if name == "INCONCLUSIVE":
                        expect(page.get_by_test_id("batch-reasons")).to_contain_text(
                            "WAVE_ORDER_MISMATCH"
                        )
                    summary["checks"].append(f"desktop-{name.lower()}-verified")

                corrupted = runtime_root / "corrupted-analysis"
                shutil.copytree(analyses["SUPPORTED"], corrupted)
                changed = corrupted / "batch-analysis.json"
                changed.write_bytes(changed.read_bytes() + b" ")
                page.get_by_test_id("local-batch-input").set_input_files(batch_files(corrupted))
                expect(page.get_by_test_id("error-state")).to_contain_text(
                    "BATCH_SIZE_MISMATCH"
                )
                if page.get_by_test_id("batch-analysis-view").count() != 0:
                    raise AssertionError("corrupt BatchAnalysis leaked a partially trusted view")
                page.get_by_test_id("retry-positive").click()
                expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
                summary["checks"].append("desktop-corruption-contained-and-recovered")

                page.get_by_test_id("local-batch-input").set_input_files(
                    batch_files(analyses["SUPPORTED"])
                )
                expect(page.get_by_test_id("batch-hypothesis-status")).to_contain_text(
                    "SUPPORTED"
                )
                page.reload(wait_until="load")
                expect(page.get_by_test_id("error-state")).to_contain_text(
                    "BATCH_RESELECT_REQUIRED"
                )
                if page.get_by_test_id("batch-analysis-view").count() != 0:
                    raise AssertionError("reload retained private local BatchAnalysis files")
                page.go_back(wait_until="load")
                expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
                summary["checks"].append("desktop-history-privacy-boundary")

                page.get_by_test_id("local-batch-input").set_input_files(
                    batch_files(analyses["CONTRADICTED"])
                )
                expect(page.get_by_test_id("batch-hypothesis-status")).to_contain_text(
                    "CONTRADICTED"
                )
                page.get_by_test_id("batch-analysis-view").scroll_into_view_if_needed()
                desktop_shot = output / "desktop.png"
                page.screenshot(path=str(desktop_shot), full_page=False)
                summary["screenshots"].append(screenshot_fact(desktop_shot))
                desktop.close()

                mobile = browser.new_context(
                    viewport={"width": 390, "height": 844},
                    is_mobile=True,
                    reduced_motion="reduce",
                )
                mobile_page = mobile.new_page()
                attach_observers(mobile_page, summary)
                mobile_page.goto(origin, wait_until="load")
                mobile_page.get_by_test_id("local-batch-input").set_input_files(
                    batch_files(analyses["SUPPORTED"])
                )
                expect(mobile_page.get_by_test_id("batch-coverage-status")).to_contain_text(
                    "COMPLETE"
                )
                expect(mobile_page.get_by_test_id("batch-hypothesis-status")).to_contain_text(
                    "SUPPORTED"
                )
                expect(mobile_page.get_by_test_id("batch-wave-list")).to_contain_text("FAIL")
                if mobile_page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                ) != 0:
                    raise AssertionError("mobile BatchAnalysis produced document overflow")
                matrix_size = mobile_page.locator(".batch-matrix-scroll").evaluate(
                    "element => ({clientWidth: element.clientWidth, scrollWidth: element.scrollWidth})"
                )
                if matrix_size["scrollWidth"] <= matrix_size["clientWidth"]:
                    raise AssertionError("mobile matrix did not preserve its bounded scroll region")
                mobile_page.get_by_test_id("batch-analysis-view").scroll_into_view_if_needed()
                mobile_shot = output / "mobile.png"
                mobile_page.screenshot(path=str(mobile_shot), full_page=False)
                summary["screenshots"].append(screenshot_fact(mobile_shot))
                summary["checks"].append("mobile-supported-bounded-matrix-no-document-overflow")
                mobile.close()
                browser.close()
                browser = None

            external = [item for item in summary["network"] if item["origin"] != origin]
            writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
            http_errors = [item for item in summary["network"] if item["status"] >= 400]
            if summary["console_errors"] or summary["page_errors"] or summary["request_failures"]:
                raise AssertionError("Workbench emitted unexpected browser errors")
            if external or writes or http_errors:
                raise AssertionError("Workbench crossed the same-origin read-only network boundary")
            if not any(item["path"] == "/api/v1/catalog" for item in summary["network"]):
                raise AssertionError("production browser run did not observe the Catalog API")
            summary["network_request_count"] = len(summary["network"])
            summary["external_request_count"] = len(external)
            summary["write_request_count"] = len(writes)
            summary["http_error_count"] = len(http_errors)
            summary["checks"].append("console-network-same-origin-read-only-clean")
            summary["execution_status"] = "COMPLETED"
            summary["verdict"] = "PASS"
            exit_code = 0
    except Exception as error:
        summary["execution_status"] = "ERROR"
        summary["verdict"] = "FAIL"
        summary["failure_type"] = type(error).__name__
        print(
            f"M8 browser acceptance failed: {type(error).__name__}: {error}",
            file=sys.stderr,
        )
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
        (output / "acceptance.json").write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )

    if not summary["port_released"]:
        print("M8 browser acceptance did not release its loopback port.", file=sys.stderr)
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
                "port_released": summary["port_released"],
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
