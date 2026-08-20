"""Production acceptance for the integrated M12 Palace Evidence candidate.

It consumes frozen, read-only M2/M6/M7/M8/M11 material. No subject Run is
created and no input Bundle is modified; all temporary corruption checks use a
new temporary directory outside those inputs.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import http.client
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = REPOSITORY_ROOT / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import m12_d1_comparison_acceptance as comparison_checks
import m12_d2_pairing_acceptance as pairing_checks
import m12_d3_batch_acceptance as batch_checks
import m12_e_browser_evidence_acceptance as browser_checks
from veritrail.local_api import create_catalog_server


DEFAULT_GATE_B = REPOSITORY_ROOT / "tmp" / "m11-gateb-contract04-20260814-161647"
DEFAULT_DRIFT = REPOSITORY_ROOT / "artifacts" / "m6-comparison-drift-20260809"
DEFAULT_INCONCLUSIVE = REPOSITORY_ROOT / "artifacts" / "m6-comparison-inconclusive-20260809"
DEFAULT_PAIRING_ROOT = REPOSITORY_ROOT / "artifacts"
DEFAULT_BATCH_ROOT = REPOSITORY_ROOT / "artifacts" / "m8-batch-runtime-v3-20260811" / "analyses"
DEFAULT_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m12-f-final-acceptance"

EXPECTED_RUNS = {
    "m11-gateb-v2-ink-positive-01": ("COMPLETED", "PASS"),
    "m11-gateb-v2-ink-browser-negative-01": ("COMPLETED", "FAIL"),
    "m11-gateb-v2-ink-port-conflict-01": ("ABORTED", "PENDING"),
    "m11-gateb-v2-ink-recovery-positive-02": ("COMPLETED", "PASS"),
}
PAIRING_INPUTS = {
    "SUPPORTED": "m7-paired-supported-20260809",
    "CONTRADICTED": "m7-paired-contradicted-20260809",
    "INCONCLUSIVE": "m7-paired-inconclusive-20260809",
}
M12_ALLOWED_PATHS = {
    "AGENTS.md",
    "README.md",
    "docs/34-m12-d-derived-analysis-plan.md",
    "docs/39-m12-d2-pairing-presentation-plan.md",
    "docs/40-m12-d2-pairing-facts.md",
    "docs/41-m12-d3-batch-presentation-plan.md",
    "docs/42-m12-d3-batch-facts.md",
    "docs/43-m12-e-browser-evidence-and-global-state-plan.md",
    "docs/44-m12-e-browser-evidence-and-global-state-facts.md",
    "docs/45-m12-f-final-validation-and-freeze-plan.md",
    "docs/milestones.md",
    "scripts/m12_d2_pairing_acceptance.py",
    "scripts/m12_d3_batch_acceptance.py",
    "scripts/m12_e_browser_evidence_acceptance.py",
    "scripts/m12_f_final_acceptance.py",
    "web/src/App.vue",
    "web/src/components/BatchAnalysisView.vue",
    "web/src/components/BrowserEvidence.vue",
    "web/src/components/PairedAnalysisView.vue",
    "web/src/styles/components.css",
    "web/tests/app.test.ts",
    "web/tests/batch.test.ts",
    "web/tests/browser-evidence.test.ts",
    "web/tests/pairing.test.ts",
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


def require(condition: object, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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
    overflow = page.evaluate("Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)")
    require(overflow == 0, f"{label} overflowed horizontally by {overflow}px.")


def save_screenshot(page: Any, output: Path, summary: dict[str, Any], name: str) -> None:
    path = output / name
    page.screenshot(path=str(path), full_page=False)
    summary["screenshots"].append(
        {"path": name, "sha256": sha256_file(path), "size": path.stat().st_size}
    )


def git_result(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        text=True,
    )


def candidate_snapshot(dist: Path) -> dict[str, Any]:
    diff_check = git_result("diff", "--check")
    require(diff_check.returncode == 0, "Candidate failed git diff --check.")
    head = git_result("rev-parse", "HEAD")
    require(head.returncode == 0, "Unable to resolve candidate HEAD.")
    changed = git_result("diff", "--name-only")
    untracked = git_result("ls-files", "--others", "--exclude-standard")
    require(changed.returncode == 0 and untracked.returncode == 0, "Unable to read candidate file list.")
    paths = sorted(
        {line.strip().replace("\\", "/") for line in (changed.stdout + "\n" + untracked.stdout).splitlines() if line.strip()}
    )
    unexpected = [path for path in paths if path not in M12_ALLOWED_PATHS]
    require(not unexpected, f"Candidate crossed M12 ownership boundary: {unexpected}")
    assets = [path for path in sorted(dist.rglob("*")) if path.is_file()]
    require(assets and (dist / "index.html").is_file(), "Production Workbench build is incomplete.")
    return {
        "head": head.stdout.strip(),
        "changed_paths": paths,
        "asset_sha256": {
            path.relative_to(dist).as_posix(): sha256_file(path)
            for path in assets
        },
    }


def input_records(paths: list[Path]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for path in paths:
        require(path.is_file(), f"Required frozen input is missing: {path.name}")
        records.append({"name": path.name, "sha256": sha256_file(path)})
    return records


def batch_files(path: Path) -> list[str]:
    return [str(path / name) for name in batch_checks.BATCH_FILES]


def pairing_files(path: Path) -> list[str]:
    return [str(path / name) for name in pairing_checks.PAIRING_FILES]


def verify_cross_axis(page: Any, expect: Any, origin: str) -> None:
    page.goto(origin, wait_until="load")
    toggle = page.get_by_test_id("cross-axis-toggle")
    expect(toggle).to_have_attribute("aria-expanded", "false")
    toggle.click()
    expect(toggle).to_have_attribute("aria-expanded", "true")
    targets = {
        "runs": page.get_by_test_id("cross-axis-runs"),
        "batch": page.get_by_test_id("cross-axis-batch"),
        "comparison": page.get_by_test_id("cross-axis-comparison"),
        "pairing": page.get_by_test_id("cross-axis-pairing"),
    }
    require(sum(target.count() for target in targets.values()) == 4, "Cross axis lost a public view target.")
    targets["runs"].press("ArrowRight")
    expect(targets["batch"]).to_be_focused()
    targets["batch"].press("ArrowDown")
    expect(targets["comparison"]).to_be_focused()
    targets["comparison"].press("ArrowLeft")
    expect(targets["pairing"]).to_be_focused()
    targets["pairing"].press("Escape")
    expect(toggle).to_be_focused()
    expect(toggle).to_have_attribute("aria-expanded", "false")

    toggle.click()
    targets["comparison"].click()
    expect(page.get_by_test_id("view-comparison-title")).to_be_focused()
    page.go_back(wait_until="load")
    expect(page.get_by_test_id("view-runs-title")).to_be_focused()
    page.go_forward(wait_until="load")
    expect(page.get_by_test_id("view-comparison-title")).to_be_focused()
    page.goto(origin, wait_until="load")
    require_no_root_overflow(page, "cross-axis navigation")


def verify_catalog_runs(page: Any, expect: Any, origin: str, catalog_runs: dict[str, Any]) -> None:
    page.goto(origin, wait_until="load")
    expect(page.get_by_test_id("run-catalog")).to_be_visible()
    rows = page.locator("[data-catalog-run-id]")
    require(rows.count() == len(EXPECTED_RUNS), "Catalog did not expose exactly the frozen M11 Run set.")
    for run_id, (execution, verdict) in EXPECTED_RUNS.items():
        catalog_run_id = catalog_runs[run_id]["catalog_run_id"]
        row = page.locator(f'[data-catalog-run-id="{catalog_run_id}"]')
        expect(row).to_contain_text(run_id)
        expect(row).to_contain_text(execution)
        expect(row).to_contain_text(verdict)
        row.click()
        expect(page.get_by_test_id("run-summary")).to_contain_text(run_id)
        expect(page.get_by_test_id("status-gate")).to_contain_text(execution)
        expect(page.get_by_test_id("status-gate")).to_contain_text(verdict)
        page.get_by_test_id("catalog-return").click()
        require(
            page.evaluate("document.activeElement?.getAttribute('data-catalog-run-id')") == catalog_run_id,
            f"Catalog return did not restore focus for {run_id}.",
        )
    require_no_root_overflow(page, "M11 Run Catalog")


def verify_comparisons(page: Any, expect: Any, origin: str, match: Path, drift: Path, inconclusive: Path) -> None:
    comparison_checks.open_comparison_view(page, origin, expect)
    comparison_checks.assert_comparison(page, expect, match, "MATCH", "M12-F M11 MATCH")
    comparison_checks.assert_comparison(page, expect, drift, "DRIFT", "M12-F DRIFT")
    comparison_checks.assert_comparison(page, expect, inconclusive, "INCONCLUSIVE", "M12-F INCONCLUSIVE")
    page.get_by_test_id("local-comparison-input").set_input_files(str(match))
    page.reload(wait_until="load")
    expect(page.get_by_test_id("error-state")).to_contain_text("COMPARISON_RESELECT_REQUIRED")
    require(page.get_by_test_id("comparison-view").count() == 0, "Refresh retained local Comparison facts.")


def verify_pairings(page: Any, expect: Any, origin: str, analyses: dict[str, Path]) -> None:
    pairing_checks.open_pairing_view(page, origin, expect)
    for status in ("SUPPORTED", "CONTRADICTED", "INCONCLUSIVE"):
        pairing_checks.assert_pairing(page, expect, analyses[status], status, f"M12-F {status}")
        pairing_checks.verify_status_specific_facts(page, expect, status)
    page.get_by_test_id("local-pairing-input").set_input_files(pairing_files(analyses["SUPPORTED"]))
    page.reload(wait_until="load")
    expect(page.get_by_test_id("error-state")).to_contain_text("PAIRING_RESELECT_REQUIRED")
    require(page.get_by_test_id("paired-analysis-view").count() == 0, "Refresh retained local Pairing facts.")


def verify_batches(page: Any, expect: Any, origin: str, analyses: dict[str, Path]) -> None:
    batch_checks.open_batch_view(page, origin, expect)
    for status in ("SUPPORTED", "CONTRADICTED", "INCOMPLETE", "INCONCLUSIVE"):
        batch_checks.import_and_verify_batch(
            page, expect, analyses[status], f"M12-F {status}", status, status == "SUPPORTED"
        )
    page.get_by_test_id("local-batch-input").set_input_files(batch_files(analyses["SUPPORTED"]))
    page.reload(wait_until="load")
    expect(page.get_by_test_id("error-state")).to_contain_text("BATCH_RESELECT_REQUIRED")
    require(page.get_by_test_id("batch-analysis-view").count() == 0, "Refresh retained local Batch facts.")


def verify_corruption_boundary(page: Any, expect: Any, origin: str, comparison: Path, pairing: Path, batch: Path) -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary = Path(temporary_directory)
        corrupted_comparison = temporary / "comparison"
        shutil.copytree(comparison, corrupted_comparison)
        changed = corrupted_comparison / "comparison.json"
        changed.write_bytes(changed.read_bytes() + b" ")
        comparison_checks.open_comparison_view(page, origin, expect)
        page.get_by_test_id("local-comparison-input").set_input_files(str(corrupted_comparison))
        expect(page.get_by_test_id("error-state")).to_contain_text("COMPARISON_SIZE_MISMATCH")
        require(page.get_by_test_id("comparison-view").count() == 0, "Corrupt Comparison exposed trusted content.")

        corrupted_pairing = temporary / "pairing"
        shutil.copytree(pairing, corrupted_pairing)
        changed = corrupted_pairing / "paired-analysis.json"
        changed.write_bytes(changed.read_bytes() + b" ")
        pairing_checks.open_pairing_view(page, origin, expect)
        page.get_by_test_id("local-pairing-input").set_input_files(pairing_files(corrupted_pairing))
        expect(page.get_by_test_id("error-state")).to_contain_text("PAIRING_SIZE_MISMATCH")
        require(page.get_by_test_id("paired-analysis-view").count() == 0, "Corrupt Pairing exposed trusted content.")

        corrupted_batch = temporary / "batch"
        shutil.copytree(batch, corrupted_batch)
        changed = corrupted_batch / "batch-analysis.json"
        changed.write_bytes(changed.read_bytes() + b" ")
        batch_checks.open_batch_view(page, origin, expect)
        page.get_by_test_id("local-batch-input").set_input_files(batch_files(corrupted_batch))
        expect(page.get_by_test_id("error-state")).to_contain_text("BATCH_SIZE_MISMATCH")
        require(page.get_by_test_id("batch-analysis-view").count() == 0, "Corrupt Batch exposed trusted content.")


def verify_global_states(page: Any, expect: Any, origin: str, catalog_runs: dict[str, Any], batch: Path) -> None:
    browser_checks.verify_negative_browser_evidence(page, expect, origin)
    page.goto(f"{origin}?fixture=invalid", wait_until="load")
    invalid = page.get_by_test_id("error-state")
    expect(invalid).to_have_attribute("data-state-kind", "invalid")
    expect(invalid).to_contain_text("MISSING_ROOT_FILE")
    expect(page.get_by_test_id("run-summary")).not_to_be_visible()
    page.get_by_test_id("retry-positive").click()
    expect(page.get_by_test_id("status-gate")).to_contain_text("PASS")

    no_browser = catalog_runs["m11-gateb-v2-ink-port-conflict-01"]
    page.goto(f"{origin}?run={no_browser['catalog_run_id']}", wait_until="load")
    expect(page.get_by_test_id("status-gate")).to_contain_text("ABORTED")
    expect(page.get_by_test_id("status-gate")).to_contain_text("PENDING")
    absent = page.get_by_test_id("browser-empty")
    expect(absent).to_have_attribute("data-state-kind", "no-browser")
    expect(absent).to_contain_text("不等于浏览器检查通过")

    page.goto(f"{origin}?run=cr_000000000000000000000000", wait_until="load")
    operational = page.get_by_test_id("error-state")
    expect(operational).to_have_attribute("data-state-kind", "operational")
    expect(operational).to_contain_text("RUN_NOT_FOUND")

    batch_checks.open_batch_view(page, origin, expect)
    page.get_by_test_id("local-batch-input").set_input_files(batch_files(batch))
    expect(page.get_by_test_id("batch-analysis-view")).to_be_visible()
    page.reload(wait_until="load")
    privacy = page.get_by_test_id("error-state")
    expect(privacy).to_have_attribute("data-state-kind", "privacy")
    expect(privacy).to_contain_text("BATCH_RESELECT_REQUIRED")
    expect(privacy).to_contain_text("为保护隐私")


def verify_mobile(
    browser: Any,
    expect: Any,
    origin: str,
    output: Path,
    summary: dict[str, Any],
    pairings: dict[str, Path],
    batches: dict[str, Path],
) -> None:
    for width, height in ((390, 844), (360, 800)):
        context = browser.new_context(
            viewport={"width": width, "height": height}, is_mobile=True, reduced_motion="reduce"
        )
        page = context.new_page()
        add_page_observers(page, summary)
        try:
            browser_checks.verify_negative_browser_evidence(page, expect, origin)
            require(
                page.get_by_role("tab").first.evaluate("element => element.offsetHeight >= 44"),
                f"{width}px Browser tab fell below the 44px target height.",
            )
            pairing_checks.open_pairing_view(page, origin, expect)
            pairing_status = "SUPPORTED" if width == 390 else "INCONCLUSIVE"
            pairing_checks.assert_pairing(page, expect, pairings[pairing_status], pairing_status, f"{width}px Pairing")
            pairing_checks.verify_status_specific_facts(page, expect, pairing_status)
            batch_checks.open_batch_view(page, origin, expect)
            batch_status = "SUPPORTED" if width == 390 else "INCOMPLETE"
            batch_checks.import_and_verify_batch(
                page, expect, batches[batch_status], f"{width}px Batch", batch_status, False
            )
            batch_checks.require_local_matrix_scroll(page, f"{width}px Batch matrix")
            require_no_root_overflow(page, f"{width}px integrated M12")
            save_screenshot(page, output, summary, f"mobile-{width}-batch-{batch_status.lower()}.png")
            summary["checks"].append(f"mobile-{width}-browser-pairing-batch-no-root-overflow")
        finally:
            context.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the integrated M12 Palace Evidence candidate.")
    parser.add_argument("--gate-b", type=Path, default=DEFAULT_GATE_B)
    parser.add_argument("--drift", type=Path, default=DEFAULT_DRIFT)
    parser.add_argument("--inconclusive", type=Path, default=DEFAULT_INCONCLUSIVE)
    parser.add_argument("--pairing-root", type=Path, default=DEFAULT_PAIRING_ROOT)
    parser.add_argument("--batch-root", type=Path, default=DEFAULT_BATCH_ROOT)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18783)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate_b = args.gate_b.resolve()
    catalog = gate_b / "catalog"
    runs = gate_b / "runs"
    match = gate_b / "comparison"
    drift = args.drift.resolve()
    inconclusive = args.inconclusive.resolve()
    pairings = {status: (args.pairing_root / name).resolve() for status, name in PAIRING_INPUTS.items()}
    batches = {status: (args.batch_root / status.lower()).resolve() for status in batch_checks.EXPECTED_STATES}
    dist = args.dist.resolve()
    output = args.output.resolve()
    port = args.port

    if output.exists():
        print("M12-F acceptance refuses to overwrite its output directory.", file=sys.stderr)
        return 2
    if not 1024 <= port <= 65535 or not port_is_free(port):
        print("M12-F acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    if available_memory_mb() < 4096:
        print("M12-F acceptance requires at least 4096 MiB available memory before Chromium starts.", file=sys.stderr)
        return 2

    try:
        require((catalog / "catalog-manifest.json").is_file(), "Frozen M11 Catalog manifest is missing.")
        require((catalog / "catalog.sqlite3").is_file(), "Frozen M11 Catalog SQLite is missing.")
        require(runs.is_dir() and (dist / "index.html").is_file(), "Frozen Runs or production build is missing.")
        comparison_checks.require_complete_comparison(match, "M11 MATCH")
        comparison_checks.require_complete_comparison(drift, "DRIFT")
        comparison_checks.require_complete_comparison(inconclusive, "INCONCLUSIVE")
        for status, path in pairings.items():
            pairing_checks.require_complete_pairing(path, status)
        for status, path in batches.items():
            batch_checks.require_complete_batch(path, status)
        require(not list(catalog.glob("catalog.sqlite3-*")), "Frozen Catalog already has SQLite sidecars.")
    except (RuntimeError, ValueError) as error:
        print(f"M12-F input audit failed: {error}", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m12-f-integrated-palace-evidence",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "verdict": "PENDING",
        "checks": [],
        "console_messages": [],
        "page_errors": [],
        "request_failures": [],
        "network": [],
        "screenshots": [],
        "start_available_memory_mb": available_memory_mb(),
        "gate_b_directory": gate_b.name,
        "output_directory": output.name,
    }
    server = None
    server_thread = None
    server_started = False
    browser = None
    exit_code = 1
    origin = f"http://127.0.0.1:{port}"

    try:
        summary["candidate"] = candidate_snapshot(dist)
        summary["frozen_inputs"] = input_records(
            [
                catalog / "catalog-manifest.json",
                catalog / "catalog.sqlite3",
                match / "comparison-manifest.json",
                drift / "comparison-manifest.json",
                inconclusive / "comparison-manifest.json",
                *(path / "paired-analysis-manifest.json" for path in pairings.values()),
                *(path / "batch-analysis-manifest.json" for path in batches.values()),
                dist / "fixtures" / "m2-positive" / "evidence-manifest.json",
                dist / "fixtures" / "m2-negative" / "evidence-manifest.json",
                dist / "fixtures" / "m2-invalid" / "report.json",
            ]
        )
        server = create_catalog_server(catalog_root=catalog, artifact_root=runs, web_root=dist, port=port)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        server_started = True

        health_status, health_headers, health_body = http_request(port, "GET", "/api/v1/health")
        health = json.loads(health_body)
        require(
            health_status == 200 and health["status"] == "READY" and health["read_only"] is True,
            "Production server did not enter read-only READY state.",
        )
        require(health_headers.get("x-content-type-options") == "nosniff", "Health response omitted nosniff.")
        catalog_status, _, catalog_body = http_request(port, "GET", "/api/v1/catalog?page=1&page_size=100")
        catalog_response = json.loads(catalog_body)
        require(catalog_status == 200, "Catalog endpoint did not return HTTP 200.")
        catalog_runs = {item["run_id"]: item for item in catalog_response["runs"]}
        require(set(catalog_runs) == set(EXPECTED_RUNS), "M12-F found an unexpected M11 Run set.")
        for run_id, (execution, verdict) in EXPECTED_RUNS.items():
            require(catalog_runs[run_id]["execution_status"] == execution, f"Execution drifted for {run_id}.")
            require(catalog_runs[run_id]["verdict"] == verdict, f"Verdict drifted for {run_id}.")
        require(http_request(port, "HEAD", "/api/v1/catalog")[0] == 200, "Catalog HEAD failed.")
        require(http_request(port, "POST", "/api/v1/catalog")[0] == 405, "Catalog accepted a write request.")
        summary["checks"].append("candidate-inputs-and-read-only-catalog")

        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            summary["browser_version"] = browser.version

            desktop = browser.new_context(viewport={"width": 1440, "height": 960})
            page = desktop.new_page()
            add_page_observers(page, summary)
            verify_cross_axis(page, expect, origin)
            summary["checks"].append("desktop-cross-axis-keyboard-history-and-focus")
            verify_catalog_runs(page, expect, origin, catalog_runs)
            summary["checks"].append("desktop-m11-catalog-all-statuses-and-return-focus")
            verify_comparisons(page, expect, origin, match, drift, inconclusive)
            summary["checks"].append("desktop-comparison-match-drift-inconclusive-and-privacy")
            verify_pairings(page, expect, origin, pairings)
            summary["checks"].append("desktop-pairing-tristate-order-and-privacy")
            verify_batches(page, expect, origin, batches)
            summary["checks"].append("desktop-batch-four-state-order-scroll-and-privacy")
            verify_corruption_boundary(page, expect, origin, match, pairings["SUPPORTED"], batches["SUPPORTED"])
            summary["checks"].append("desktop-local-corruption-never-exposes-partial-facts")
            verify_global_states(page, expect, origin, catalog_runs, batches["SUPPORTED"])
            summary["checks"].append("desktop-browser-evidence-invalid-operational-no-browser-and-privacy")
            save_screenshot(page, output, summary, "desktop-final-state.png")
            desktop.close()

            medium = browser.new_context(viewport={"width": 1024, "height": 768}, reduced_motion="reduce")
            medium_page = medium.new_page()
            add_page_observers(medium_page, summary)
            verify_cross_axis(medium_page, expect, origin)
            require_no_root_overflow(medium_page, "1024px cross axis")
            save_screenshot(medium_page, output, summary, "medium-cross-axis.png")
            medium.close()
            summary["checks"].append("medium-1024-cross-axis-no-root-overflow")

            narrow_desktop = browser.new_context(viewport={"width": 1280, "height": 800})
            narrow_page = narrow_desktop.new_page()
            add_page_observers(narrow_page, summary)
            pairing_checks.open_pairing_view(narrow_page, origin, expect)
            pairing_checks.assert_pairing(narrow_page, expect, pairings["SUPPORTED"], "SUPPORTED", "1280px Pairing")
            batch_checks.open_batch_view(narrow_page, origin, expect)
            batch_checks.import_and_verify_batch(
                narrow_page, expect, batches["CONTRADICTED"], "1280px Batch", "CONTRADICTED", False
            )
            require_no_root_overflow(narrow_page, "1280px Pairing and Batch")
            narrow_desktop.close()
            summary["checks"].append("narrow-desktop-1280-pairing-and-batch-no-root-overflow")

            verify_mobile(browser, expect, origin, output, summary, pairings, batches)

            forced = browser.new_context(
                viewport={"width": 390, "height": 844}, is_mobile=True, forced_colors="active", reduced_motion="reduce"
            )
            forced_page = forced.new_page()
            add_page_observers(forced_page, summary)
            browser_checks.verify_negative_browser_evidence(forced_page, expect, origin)
            forced_page.get_by_role("tab").nth(3).press("Home")
            expect(forced_page.get_by_role("tab").nth(0)).to_be_focused()
            require_no_root_overflow(forced_page, "forced-colors Browser Evidence")
            forced.close()
            summary["checks"].append("forced-colors-browser-evidence-text-boundaries-and-focus")

            browser.close()
            browser = None

        external = [item for item in summary["network"] if item["origin"] not in {origin, "[blob]"}]
        writes = [item for item in summary["network"] if item["method"] not in {"GET", "HEAD"}]
        http_errors = [item for item in summary["network"] if item["status"] >= 400]
        summary["network_request_count"] = len(summary["network"])
        summary["external_request_count"] = len(external)
        summary["write_request_count"] = len(writes)
        summary["http_error_count"] = len(http_errors)
        summary["duplicate_non_idempotent_request_count"] = len(writes)
        require(not summary["console_messages"], "Production Workbench emitted Console warnings or errors.")
        require(not summary["page_errors"], "Production Workbench emitted a page error.")
        require(not summary["request_failures"], "Production Workbench emitted a request failure.")
        require(not external and not writes and not http_errors, "Production Workbench crossed its read-only network boundary.")
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
        summary["port_released"] = port_is_free(port)
        summary["sqlite_sidecars_absent"] = not list(catalog.glob("catalog.sqlite3-*"))
        summary["end_available_memory_mb"] = available_memory_mb()
        summary["ended_at"] = utc_now()
        summary["network_request_count"] = len(summary["network"])
        (output / "acceptance.json").write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    if not summary["port_released"] or not summary["server_thread_stopped"] or not summary["sqlite_sidecars_absent"]:
        print("M12-F acceptance left a listener, service thread, or SQLite sidecar behind.", file=sys.stderr)
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
