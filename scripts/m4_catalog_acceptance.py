from __future__ import annotations

import argparse
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
DEFAULT_CATALOG = REPOSITORY_ROOT / "artifacts" / "m4-catalog-b"
DEFAULT_ARTIFACTS = REPOSITORY_ROOT / "artifacts" / "m4-seeds-b"
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m4-catalog-acceptance"
DEFAULT_RUN_ID = "m4-self-bootstrap-run-v2"
DEFAULT_PLAN_SHA256 = "d3a8cd4e1d7405e91fd7b0cdac0eef94772b09617a19d3dffcd473d8a05e3a08"


def require(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded M4 Catalog HTTP/browser acceptance.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--artifacts", type=Path, default=DEFAULT_ARTIFACTS)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--expected-run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--expected-plan-sha256", default=DEFAULT_PLAN_SHA256)
    parser.add_argument("--port", type=int, default=18768)
    return parser.parse_args()


def http_request(port: int, method: str, path: str, host: str | None = None) -> tuple[int, dict[str, str], bytes]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    headers = {"Host": host} if host is not None else {}
    connection.request(method, path, headers=headers)
    response = connection.getresponse()
    body = response.read()
    result = response.status, {key.lower(): value for key, value in response.getheaders()}, body
    connection.close()
    return result


def response_fact(response: Any) -> dict[str, Any]:
    parsed = urlsplit(response.url)
    return {
        "method": response.request.method,
        "origin": f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme != "blob" else "[blob]",
        "path": parsed.path if parsed.scheme != "blob" else "[blob]",
        "resource_type": response.request.resource_type,
        "status": response.status,
    }


def main() -> int:
    args = parse_args()
    catalog = args.catalog.resolve()
    artifacts = args.artifacts.resolve()
    dist = args.dist.resolve()
    output = args.output.resolve()
    if output.exists():
        print("M4 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535:
        print("M4 acceptance port must be between 1024 and 65535.", file=sys.stderr)
        return 2
    if not (catalog / "catalog-manifest.json").is_file() or not artifacts.is_dir():
        print("M4 acceptance requires a Catalog and its bound Artifact root.", file=sys.stderr)
        return 2
    if not (dist / "index.html").is_file():
        print("M4 acceptance requires an existing Workbench production build.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m4-local-run-catalog",
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "execution_status": "RUNNING",
        "checks": [],
        "console_errors": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
    }
    server = create_catalog_server(
        catalog_root=catalog,
        artifact_root=artifacts,
        web_root=dist,
        port=args.port,
    )
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    browser = None
    exit_code = 1
    origin = f"http://127.0.0.1:{args.port}"
    try:
        status, headers, body = http_request(args.port, "GET", "/api/v1/health")
        health = json.loads(body)
        require(
            status == 200 and health["status"] == "READY" and health["read_only"] is True,
            "catalog health endpoint must report a ready read-only service",
        )
        require(
            headers["x-content-type-options"] == "nosniff",
            "catalog health endpoint must emit nosniff",
        )
        require(
            "access-control-allow-origin" not in headers,
            "catalog API must not enable cross-origin access",
        )
        summary["checks"].append("http-health-readonly-security")

        status, _, body = http_request(args.port, "GET", "/api/v1/catalog?page=1&page_size=100")
        catalog_response = json.loads(body)
        require(
            status == 200 and catalog_response["catalog"]["run_count"] >= 3,
            "catalog endpoint must expose the seeded runs",
        )
        expected = next(
            item for item in catalog_response["runs"] if item["run_id"] == args.expected_run_id
        )
        require(
            expected["plan"]["sha256"] == args.expected_plan_sha256,
            "catalog plan digest must match the expected sealed plan",
        )
        catalog_run_id = expected["catalog_run_id"]
        summary["catalog_id"] = catalog_response["catalog"]["catalog_id"]
        summary["catalog_run_id"] = catalog_run_id
        summary["checks"].append("http-catalog-self-run")

        require(
            http_request(args.port, "HEAD", "/api/v1/catalog")[0] == 200,
            "catalog endpoint must support HEAD",
        )
        require(
            http_request(args.port, "POST", "/api/v1/catalog")[0] == 405,
            "catalog endpoint must reject POST",
        )
        require(
            http_request(args.port, "GET", "/api/not-real")[0] == 404,
            "catalog API must reject unknown paths",
        )
        require(
            http_request(args.port, "GET", "/api/v1/catalog?unknown=1")[0] == 400,
            "catalog endpoint must reject unknown query parameters",
        )
        require(
            http_request(
                args.port,
                "GET",
                "/api/v1/catalog",
                host="example.invalid",
            )[0]
            == 400,
            "catalog API must reject an untrusted Host header",
        )
        summary["checks"].append("http-negative-contract")

        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
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
                    {"method": request.method, "path": urlsplit(request.url).path}
                ),
            )
            page.on("response", lambda response: summary["network"].append(response_fact(response)))
            page.goto(f"{origin}/", wait_until="load")
            expect(page.get_by_test_id("run-catalog")).to_be_visible()
            require(
                page.get_by_test_id("status-gate").count() == 0,
                "catalog landing page must not expose a run status gate",
            )
            run_button = page.locator(f'[data-catalog-run-id="{catalog_run_id}"]')
            expect(run_button).to_contain_text(args.expected_run_id)
            run_button.click()
            expect(page.get_by_test_id("run-summary")).to_contain_text(args.expected_run_id)
            expect(page.get_by_test_id("status-gate")).to_contain_text("COMPLETED")
            expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
            require(
                page.get_by_test_id("run-summary").locator("code").get_attribute("title")
                == args.expected_plan_sha256,
                "run summary must expose the full expected plan digest",
            )
            require(
                page.evaluate(
                    "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                )
                == 0,
                "desktop catalog detail must not overflow horizontally",
            )
            summary["checks"].append("desktop-self-run-readback")

            page.get_by_test_id("catalog-return").click()
            require(
                page.evaluate(
                    "document.activeElement?.getAttribute('data-catalog-run-id')"
                )
                == catalog_run_id,
                "returning to the catalog must restore focus to the selected run",
            )
            run_button.click()
            page.go_back(wait_until="load")
            expect(page.get_by_test_id("run-catalog")).to_be_visible()
            page.go_forward(wait_until="load")
            expect(page.get_by_test_id("run-summary")).to_contain_text(args.expected_run_id)
            summary["checks"].append("desktop-focus-history")

            page.get_by_test_id("fixture-invalid").click()
            expect(page.get_by_test_id("error-state")).to_contain_text("MISSING_ROOT_FILE")
            require(
                page.get_by_test_id("status-gate").count() == 0,
                "invalid fixture must not expose a status gate",
            )
            page.get_by_test_id("retry-positive").click()
            expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")
            summary["checks"].append("m3-invalid-retry-compatibility")

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
            mobile_page.goto(f"{origin}/", wait_until="load")
            expect(mobile_page.get_by_test_id("run-catalog")).to_be_visible()
            mobile_page.locator(f'[data-catalog-run-id="{catalog_run_id}"]').click()
            expect(mobile_page.get_by_test_id("status-gate")).to_contain_text("PASS")
            require(
                mobile_page.evaluate(
                    "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)"
                )
                == 0,
                "mobile catalog detail must not overflow horizontally",
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
            summary["checks"].append("mobile-self-run-no-overflow")
            mobile.close()
            browser.close()
            browser = None

        unexpected_http = [item for item in summary["network"] if item["status"] >= 400]
        external = [
            item for item in summary["network"] if item["origin"] not in {origin, "[blob]"}
        ]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        if summary["console_errors"] or summary["page_errors"] or summary["request_failures"]:
            raise AssertionError("Workbench emitted unexpected browser errors.")
        if unexpected_http or external or writes:
            raise AssertionError("Workbench network crossed the frozen same-origin read-only boundary.")
        summary["network_request_count"] = len(summary["network"])
        summary["http_error_count"] = 0
        summary["external_request_count"] = 0
        summary["write_request_count"] = 0
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
        summary["ended_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        summary["network_request_count"] = len(summary["network"])
        with (output / "acceptance.json").open("w", encoding="utf-8", newline="\n") as stream:
            json.dump(summary, stream, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            stream.write("\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        port_released = probe.connect_ex(("127.0.0.1", args.port)) != 0
    sidecars = list(catalog.glob("catalog.sqlite3-*"))
    if not port_released or sidecars:
        print("M4 acceptance cleanup did not release the port or SQLite sidecars.", file=sys.stderr)
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
                "sqlite_sidecars": 0,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
