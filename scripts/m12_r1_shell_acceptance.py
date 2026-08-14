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
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m12-r1-shell-acceptance"


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


def verify_desktop_shell(page: Any, expect: Any, output: Path, summary: dict[str, Any]) -> None:
    page.goto(summary["origin"], wait_until="load")
    expect(page.get_by_test_id("run-catalog")).to_be_visible()
    expect(page.locator("[data-catalog-run-id]").first).to_be_visible()

    geometry = page.evaluate(
        """() => {
          const rect = (selector) => {
            const node = document.querySelector(selector)
            if (!node) return null
            const box = node.getBoundingClientRect()
            return { top: box.top, bottom: box.bottom, width: box.width, height: box.height }
          }
          return {
            viewportHeight: window.innerHeight,
            masthead: rect('.masthead'),
            hub: rect('[data-testid="cross-axis-toggle"]'),
            viewTitle: rect('[data-testid="view-runs-title"]'),
            firstRun: rect('[data-catalog-run-id]'),
          }
        }"""
    )
    require(all(geometry[key] is not None for key in ("masthead", "hub", "viewTitle", "firstRun")), "R1 desktop shell lost a required first-screen element.")
    require(
        geometry["masthead"]["height"] <= geometry["viewportHeight"] / 2,
        "R1 masthead and hub still consume more than half of the desktop viewport.",
    )
    require(
        0 <= geometry["firstRun"]["top"] < geometry["viewportHeight"],
        "R1 desktop first screen does not expose a real Catalog Run.",
    )
    require(root_overflow(page) == 0, "R1 desktop collapsed shell overflowed horizontally.")
    summary["desktop_collapsed_geometry"] = geometry
    save_screenshot(page, output, summary, "desktop-collapsed.png")

    first_run_top = geometry["firstRun"]["top"]
    center = page.get_by_test_id("cross-axis-toggle")
    expect(center).to_have_attribute("aria-expanded", "false")
    center.click()
    expect(center).to_have_attribute("aria-expanded", "true")
    targets = {
        "runs": page.get_by_test_id("cross-axis-runs"),
        "batch": page.get_by_test_id("cross-axis-batch"),
        "comparison": page.get_by_test_id("cross-axis-comparison"),
        "pairing": page.get_by_test_id("cross-axis-pairing"),
    }
    target_sizes: dict[str, dict[str, float]] = {}
    for label, target in targets.items():
        expect(target).to_be_visible()
        box = target.bounding_box()
        require(box is not None and box["width"] >= 44 and box["height"] >= 44, f"R1 desktop {label} target is below 44 x 44 CSS px.")
        target_sizes[label] = {"width": round(box["width"], 3), "height": round(box["height"], 3)}

    expanded_first_run = page.locator("[data-catalog-run-id]").first.bounding_box()
    require(expanded_first_run is not None, "R1 desktop lost the first Catalog Run after expansion.")
    expanded_first_run_top = expanded_first_run["y"]
    require(
        abs(expanded_first_run_top - first_run_top) <= 24,
        "R1 cross-axis expansion shifted the first Catalog Run by more than 24 px.",
    )
    require(root_overflow(page) == 0, "R1 desktop expanded shell overflowed horizontally.")
    summary["desktop_expanded_target_sizes"] = target_sizes
    summary["desktop_catalog_first_run_shift_px"] = round(
        abs(expanded_first_run_top - first_run_top), 3
    )
    save_screenshot(page, output, summary, "desktop-expanded.png")

    targets["runs"].focus()
    targets["runs"].press("ArrowRight")
    require(
        page.evaluate("document.activeElement?.getAttribute('data-testid')") == "cross-axis-batch",
        "R1 desktop ArrowRight did not preserve declared cross-axis geometry.",
    )
    targets["batch"].press("Escape")
    expect(center).to_have_attribute("aria-expanded", "false")
    require(
        page.evaluate("document.activeElement?.getAttribute('data-testid')") == "cross-axis-toggle",
        "R1 desktop Escape did not return focus to the center control.",
    )
    summary["checks"].append("desktop-first-screen-stability-target-size-and-keyboard")


def verify_mobile_shell(
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
        expect(page.get_by_test_id("run-catalog")).to_be_visible()
        center = page.get_by_test_id("cross-axis-toggle")
        center.click()
        target_sizes: dict[str, dict[str, float]] = {}
        for label in ("runs", "batch", "comparison", "pairing"):
            box = page.get_by_test_id(f"cross-axis-{label}").bounding_box()
            require(box is not None and box["width"] >= 44 and box["height"] >= 44, f"R1 {width}px {label} target is below 44 x 44 CSS px.")
            target_sizes[label] = {"width": round(box["width"], 3), "height": round(box["height"], 3)}
        require(root_overflow(page) == 0, f"R1 {width}px expanded shell overflowed horizontally.")
        summary.setdefault("mobile_expanded_target_sizes", {})[str(width)] = target_sizes
        save_screenshot(page, output, summary, f"mobile-{width}-expanded.png")
        summary["checks"].append(f"mobile-{width}-cross-axis-targets-and-no-overflow")
    finally:
        context.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate M12 R1 compact shell presentation.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18781)
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
        print("M12 R1 acceptance refuses to overwrite its output directory.", file=sys.stderr)
        return 2
    if not 1024 <= port <= 65535 or not port_is_free(port):
        print("M12 R1 acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if not (catalog / "catalog.sqlite3").is_file() or not artifacts.is_dir() or not (dist / "index.html").is_file():
        print("M12 R1 acceptance requires the complete M11 Gate B catalog and production build.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m12-r1-compact-shell-presentation",
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
                verify_desktop_shell(page, expect, output, summary)
                desktop.close()
                verify_mobile_shell(browser, expect, output, summary, 390, 844)
                verify_mobile_shell(browser, expect, output, summary, 360, 800)
            finally:
                browser.close()
                browser = None

        external = [item for item in summary["network"] if item["origin"] not in {summary["origin"], "[blob]"}]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        require(not summary["console_messages"], "M12 R1 emitted Console warnings or errors.")
        require(not summary["page_errors"], "M12 R1 emitted page errors.")
        require(not summary["request_failures"], "M12 R1 emitted failed network requests.")
        require(not external and not writes and not http_errors, "M12 R1 crossed its same-origin read-only network boundary.")
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
    print(json.dumps({key: summary[key] for key in ("checks", "execution_status", "verdict", "port_released", "server_thread_stopped")}, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
