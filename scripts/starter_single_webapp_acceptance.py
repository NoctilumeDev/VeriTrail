from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from veritrail.catalog import validate_bundle
from veritrail.local_api import create_catalog_server


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPOSITORY_ROOT / "examples" / "starter" / "single-webapp"
WEB_DIST = REPOSITORY_ROOT / "web" / "dist"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "starter-single-webapp-s1"
PASS_RUN_ID = "starter-s1-pass"
FAIL_RUN_ID = "starter-s1-fail"
RUN_EXPECTATIONS = {
    PASS_RUN_ID: ("COMPLETED", "PASS"),
    FAIL_RUN_ID: ("COMPLETED", "FAIL"),
}


def require(condition: object, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exercise the Starter single-webapp DRAFT through Core and Workbench."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--application-port", type=int, default=18789)
    parser.add_argument("--catalog-port", type=int, default=18790)
    return parser.parse_args()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, document: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(document, dict), f"{path.name} must contain one JSON object")
    return document


def port_is_free(port: int) -> bool:
    if not 1024 <= port <= 65535:
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
        if exclusive is not None:
            probe.setsockopt(socket.SOL_SOCKET, exclusive, 1)
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def run_json_module(module: str, arguments: list[str], *, cwd: Path) -> dict[str, Any]:
    environment = dict(os.environ)
    environment["PYTHONUTF8"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", module, *arguments],
        cwd=cwd,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
        encoding="utf-8",
        errors="strict",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    require(
        completed.returncode == 0,
        f"{module} {' '.join(arguments[:2])} failed with exit {completed.returncode}: {stderr}",
    )
    require(not stderr, f"{module} unexpectedly wrote to stderr: {stderr}")
    try:
        document = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{module} did not emit exactly one JSON document") from exc
    require(isinstance(document, dict), f"{module} output must be one JSON object")
    return document


def build_answers(subject_root: Path, port: int) -> dict[str, Any]:
    origin = f"http://127.0.0.1:{port}"
    return {
        "schema_version": "0.1",
        "preset": "single-webapp",
        "workspace_id": "starter-single-webapp-golden",
        "question": "Does the application return the preregistered ready evidence fact?",
        "subject": {
            "root": str(subject_root),
            "id": "starter-single-webapp",
            "version": "1.0",
            "source_ref": ".",
            "working_directory": ".",
            "watch_roots": ["app"],
        },
        "application": {
            "executable": str(Path(sys.executable).resolve()),
            "arguments": [
                {"literal": "app/server.py"},
                {"literal": "serve"},
                {"node_port": "application"},
            ],
            "port": port,
            "health_path": "/health",
            "expected_status": 200,
        },
        "browser": {
            "start_url": origin + "/",
            "allowed_origin": origin,
            "headless": True,
            "timeout_ms": 3000,
            "viewports": [
                {"name": "desktop", "width": 1440, "height": 960, "is_mobile": False},
                {"name": "mobile", "width": 390, "height": 844, "is_mobile": True},
            ],
            "steps": [
                {
                    "id": "starter-title-visible",
                    "action": "expect_visible",
                    "selector": "[data-testid='starter-title']",
                },
                {
                    "id": "starter-label-fill",
                    "action": "fill",
                    "selector": "[data-testid='run-label']",
                    "value": "starter-demo",
                },
                {
                    "id": "starter-load-evidence",
                    "action": "click",
                    "selector": "[data-testid='load-evidence']",
                },
                {
                    "id": "starter-ready-fact",
                    "action": "expect_text",
                    "selector": "[data-testid='status']",
                    "value": "evidence ready: starter-demo",
                },
            ],
            "screenshot_safety": "UNREDACTED_OPERATOR_ACKNOWLEDGED",
        },
        "budgets": {
            # Keep the generated DRAFT below Core's frozen 10 MiB verifier ceiling.
            "max_artifact_bytes": 8 * 1024 * 1024,
            "max_watch_files": 100,
            "max_watch_total_bytes": 8 * 1024 * 1024,
            "lifecycle_timeout_ms": 120000,
            "max_stdout_bytes": 262144,
            "max_stderr_bytes": 262144,
            "max_processes": 8,
            "application_memory_mb": 512,
            "browser_memory_mb": 1024,
        },
        "timeouts": {
            "readiness_attempt_ms": 500,
            "readiness_total_ms": 10000,
            "readiness_interval_ms": 100,
            "shutdown_process_ms": 5000,
            "shutdown_port_ms": 5000,
            "shutdown_reader_ms": 5000,
        },
        "random_seed": 20260823,
    }


def ordinary_file_digests(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def materialize_subjects(output: Path) -> tuple[Path, Path]:
    pass_root = output / "subjects" / "pass"
    fail_root = output / "subjects" / "fail"
    shutil.copytree(FIXTURE_ROOT, pass_root)
    shutil.copytree(FIXTURE_ROOT, fail_root)
    fail_fact = fail_root / "app" / "fact.json"
    write_json(fail_fact, {"status": "blocked"})

    pass_files = ordinary_file_digests(pass_root)
    fail_files = ordinary_file_digests(fail_root)
    require(set(pass_files) == set(fail_files), "PASS and FAIL subject file sets differ")
    differences = [name for name in sorted(pass_files) if pass_files[name] != fail_files[name]]
    require(
        differences == ["app/fact.json"],
        "PASS and FAIL subjects must differ only in app/fact.json",
    )
    require(read_json(pass_root / "app" / "fact.json") == {"status": "ready"}, "PASS fact drifted")
    require(read_json(fail_fact) == {"status": "blocked"}, "FAIL fact drifted")
    return pass_root, fail_root


def run_handoff_preview(script: Path, *, cwd: Path) -> str:
    completed = subprocess.run(
        [
            "powershell.exe",
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
        ],
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
        encoding="utf-8",
        errors="strict",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    require(completed.returncode == 0, "handoff.ps1 did not print cleanly")
    require(not completed.stderr.strip(), "handoff.ps1 unexpectedly wrote to stderr")
    text = completed.stdout
    for command in ("bootstrap-profile-seal", "bootstrap-preview", "veritrail run"):
        require(command in text, f"handoff.ps1 omitted {command}")
    return text


def http_json(port: int, path: str) -> tuple[int, dict[str, str], dict[str, Any]]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    connection.request("GET", path)
    response = connection.getresponse()
    body = response.read()
    headers = {key.lower(): value for key, value in response.getheaders()}
    connection.close()
    document = json.loads(body)
    require(isinstance(document, dict), f"{path} did not return one JSON object")
    return response.status, headers, document


def response_fact(response: Any) -> dict[str, Any]:
    parsed = urlsplit(response.url)
    return {
        "method": response.request.method,
        "path": parsed.path,
        "status": response.status,
    }


def verify_workbench(
    *,
    catalog_root: Path,
    runs_root: Path,
    output: Path,
    port: int,
) -> dict[str, Any]:
    require((WEB_DIST / "index.html").is_file(), "production web/dist is missing")
    require(port_is_free(port), "explicit Catalog port is not free")
    server = create_catalog_server(
        catalog_root=catalog_root,
        artifact_root=runs_root,
        web_root=WEB_DIST,
        port=port,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{port}"
    screenshots: list[dict[str, str]] = []
    console_errors: list[dict[str, str]] = []
    page_errors: list[dict[str, str]] = []
    request_failures: list[dict[str, str]] = []
    http_errors: list[dict[str, Any]] = []
    try:
        status, headers, health = http_json(port, "/api/v1/health")
        require(status == 200 and health.get("status") == "READY", "Catalog health is not READY")
        require(health.get("read_only") is True, "Workbench server is not read-only")
        require(headers.get("x-content-type-options") == "nosniff", "nosniff header is missing")

        status, _, catalog = http_json(port, "/api/v1/catalog?page=1&page_size=100")
        require(status == 200, "Catalog API did not return HTTP 200")
        require(catalog["catalog"]["run_count"] == 2, "Catalog must contain exactly two Runs")
        require(catalog["catalog"]["issue_count"] == 0, "Catalog must contain no issues")
        api_runs = {item["run_id"]: item for item in catalog["runs"]}
        require(set(api_runs) == set(RUN_EXPECTATIONS), "Catalog returned an unexpected Run set")
        for run_id, (execution, verdict) in RUN_EXPECTATIONS.items():
            require(api_runs[run_id]["execution_status"] == execution, f"{run_id} execution drifted")
            require(api_runs[run_id]["verdict"] == verdict, f"{run_id} verdict drifted")

        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for viewport in (
                    {"name": "desktop", "width": 1440, "height": 960, "is_mobile": False},
                    {"name": "mobile", "width": 390, "height": 844, "is_mobile": True},
                ):
                    context = browser.new_context(
                        viewport={"width": viewport["width"], "height": viewport["height"]},
                        is_mobile=viewport["is_mobile"],
                    )
                    try:
                        page = context.new_page()
                        page.on(
                            "console",
                            lambda message, name=viewport["name"]: console_errors.append(
                                {"viewport": name, "type": message.type, "text": message.text[:1024]}
                            )
                            if message.type in {"error", "assert"}
                            else None,
                        )
                        page.on(
                            "pageerror",
                            lambda error, name=viewport["name"]: page_errors.append(
                                {"viewport": name, "type": type(error).__name__, "message": str(error)[:1024]}
                            ),
                        )
                        page.on(
                            "requestfailed",
                            lambda request, name=viewport["name"]: request_failures.append(
                                {"viewport": name, "method": request.method, "path": urlsplit(request.url).path}
                            ),
                        )
                        page.on(
                            "response",
                            lambda response, name=viewport["name"]: http_errors.append(
                                {"viewport": name, **response_fact(response)}
                            )
                            if response.status >= 400
                            else None,
                        )
                        page.goto(origin + "/?view=runs", wait_until="load", timeout=15000)
                        page.locator('[data-testid="run-catalog"]').wait_for(state="visible", timeout=10000)
                        page.locator('[data-testid="catalog-runs"]').wait_for(state="visible", timeout=10000)
                        require(
                            page.locator("[data-catalog-run-id]").count() == 2,
                            f"{viewport['name']} Catalog did not render exactly two Runs",
                        )
                        overflow = page.evaluate(
                            "Math.ceil(Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth))"
                        )
                        require(overflow <= 0, f"{viewport['name']} Catalog has horizontal overflow")
                        catalog_shot = output / "screenshots" / f"{viewport['name']}-catalog.png"
                        catalog_shot.parent.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=str(catalog_shot), full_page=True)
                        screenshots.append(
                            {
                                "name": catalog_shot.relative_to(output).as_posix(),
                                "sha256": sha256_file(catalog_shot),
                            }
                        )

                        for run_id in (PASS_RUN_ID, FAIL_RUN_ID):
                            catalog_run_id = api_runs[run_id]["catalog_run_id"]
                            page.locator(f'[data-catalog-run-id="{catalog_run_id}"]').click()
                            summary = page.locator('[data-testid="run-summary"]')
                            summary.wait_for(state="visible", timeout=10000)
                            require(run_id in summary.inner_text(), f"{viewport['name']} did not open {run_id}")
                            overflow = page.evaluate(
                                "Math.ceil(Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth))"
                            )
                            require(overflow <= 0, f"{viewport['name']} {run_id} detail has horizontal overflow")
                            detail_shot = output / "screenshots" / f"{viewport['name']}-{run_id}.png"
                            page.screenshot(path=str(detail_shot), full_page=True)
                            screenshots.append(
                                {
                                    "name": detail_shot.relative_to(output).as_posix(),
                                    "sha256": sha256_file(detail_shot),
                                }
                            )
                            page.locator('[data-testid="catalog-return"]').click()
                            page.locator('[data-testid="run-catalog"]').wait_for(
                                state="visible", timeout=10000
                            )
                    finally:
                        context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    require(not thread.is_alive(), "Catalog server thread did not stop")
    require(port_is_free(port), "Catalog server did not release its port")
    require(not console_errors, f"Workbench emitted console errors: {console_errors}")
    require(not page_errors, f"Workbench emitted page errors: {page_errors}")
    require(not request_failures, f"Workbench emitted request failures: {request_failures}")
    require(not http_errors, f"Workbench emitted HTTP errors: {http_errors}")
    return {
        "health": "READY_READ_ONLY",
        "run_count": 2,
        "issue_count": 0,
        "viewports": ["desktop", "mobile"],
        "screenshots": screenshots,
        "console_error_count": 0,
        "page_error_count": 0,
        "request_failure_count": 0,
        "http_error_count": 0,
    }


def ensure_bundle_has_no_local_roots(bundle: Path, roots: list[Path]) -> None:
    needles = [str(root.resolve()).encode("utf-8") for root in roots]
    for path in bundle.rglob("*"):
        if not path.is_file():
            continue
        content = path.read_bytes()
        require(
            not any(needle in content for needle in needles),
            f"Bundle {bundle.name} leaked an absolute local root in {path.name}",
        )


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if os.name != "nt":
        print("Starter S1 acceptance supports only Windows 11.", file=sys.stderr)
        return 2
    if output.exists():
        print("Starter S1 acceptance refuses to overwrite its output directory.", file=sys.stderr)
        return 2
    if args.application_port == args.catalog_port or not port_is_free(args.application_port):
        print("Starter S1 acceptance requires a free explicit application port.", file=sys.stderr)
        return 2
    if not port_is_free(args.catalog_port):
        print("Starter S1 acceptance requires a free explicit Catalog port.", file=sys.stderr)
        return 2
    if not (FIXTURE_ROOT / "app" / "server.py").is_file():
        print("Starter S1 fixture is incomplete.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    try:
        pass_root, fail_root = materialize_subjects(output)
        answers_path = output / "answers.json"
        answers = build_answers(pass_root, args.application_port)
        write_json(answers_path, answers)

        doctor = run_json_module(
            "veritrail_starter", ["doctor", "--answers", str(answers_path)], cwd=REPOSITORY_ROOT
        )
        require(doctor.get("status") == "READY", "Starter doctor did not report READY")
        initialized = run_json_module(
            "veritrail_starter",
            ["init", "--preset", "single-webapp", "--answers", str(answers_path)],
            cwd=REPOSITORY_ROOT,
        )
        require(initialized.get("authoring_state") == "DRAFT", "Starter init lost DRAFT state")
        require(initialized.get("seal_state") == "NOT_SEALED", "Starter init unexpectedly sealed")
        workspace = pass_root / ".veritrail"
        for command in ("validate", "review", "handoff"):
            result = run_json_module(
                "veritrail_starter",
                [command, "--workspace", str(workspace)],
                cwd=REPOSITORY_ROOT,
            )
            require(result.get("valid") is True, f"Starter {command} did not validate the DRAFT")
            require(result.get("authoring_state") == "DRAFT", f"Starter {command} lost DRAFT state")
            require(result.get("seal_state") == "NOT_SEALED", f"Starter {command} unexpectedly sealed")
        handoff_text = run_handoff_preview(workspace / "handoff.ps1", cwd=pass_root)
        write_json(
            output / "handoff-preview.json",
            {"execution": "NOT_PERFORMED", "line_count": len(handoff_text.splitlines())},
        )

        authority = output / "authority"
        authority.mkdir()
        sealed_profile = authority / "profile.sealed.json"
        sealed_plan = authority / "plan.sealed.json"
        profile_result = run_json_module(
            "veritrail",
            [
                "bootstrap-profile-seal",
                "--profile",
                str(workspace / "profile.draft.json"),
                "--output",
                str(sealed_profile),
            ],
            cwd=REPOSITORY_ROOT,
        )
        plan_result = run_json_module(
            "veritrail",
            [
                "seal",
                "--plan",
                str(workspace / "plan.draft.json"),
                "--profile",
                str(sealed_profile),
                "--output",
                str(sealed_plan),
            ],
            cwd=REPOSITORY_ROOT,
        )
        require(len(profile_result.get("profile_sha256", "")) == 64, "Profile seal digest is invalid")
        require(len(plan_result.get("plan_sha256", "")) == 64, "Plan seal digest is invalid")

        runs = output / "runs"
        runs.mkdir()
        bindings = workspace / "tool-bindings.local.json"
        run_results: dict[str, dict[str, Any]] = {}
        preview_digests: dict[str, str] = {}
        for run_id, subject_root in ((PASS_RUN_ID, pass_root), (FAIL_RUN_ID, fail_root)):
            require(port_is_free(args.application_port), f"application port is busy before {run_id}")
            preview = run_json_module(
                "veritrail",
                [
                    "bootstrap-preview",
                    "--plan",
                    str(sealed_plan),
                    "--profile",
                    str(sealed_profile),
                    "--subject-root",
                    str(subject_root),
                    "--tool-bindings",
                    str(bindings),
                ],
                cwd=REPOSITORY_ROOT,
            )
            digest = preview.get("preview_sha256")
            require(
                isinstance(digest, str)
                and len(digest) == 64
                and digest == digest.casefold(),
                f"{run_id} preview digest is invalid",
            )
            preview_digests[run_id] = digest
            write_json(authority / f"preview-{run_id}.json", preview)
            run_output = runs / run_id
            result = run_json_module(
                "veritrail",
                [
                    "run",
                    "--plan",
                    str(sealed_plan),
                    "--profile",
                    str(sealed_profile),
                    "--subject-root",
                    str(subject_root),
                    "--tool-bindings",
                    str(bindings),
                    "--approve-bootstrap-preview-sha256",
                    digest,
                    "--run-id",
                    run_id,
                    "--output",
                    str(run_output),
                ],
                cwd=REPOSITORY_ROOT,
            )
            expected_execution, expected_verdict = RUN_EXPECTATIONS[run_id]
            require(result.get("execution_status") == expected_execution, f"{run_id} execution drifted")
            require(result.get("verdict") == expected_verdict, f"{run_id} verdict drifted")
            require(result.get("services_ready") is True, f"{run_id} service was not ready")
            require(result.get("cleanup_complete") is True, f"{run_id} cleanup was incomplete")
            require(
                result.get("bootstrap_preview_sha256") == digest,
                f"{run_id} did not use its live approved Preview",
            )
            require(port_is_free(args.application_port), f"{run_id} did not release the application port")
            validated = validate_bundle(run_output, runs, retain_snapshot=True)
            require(validated.run_id == run_id, f"{run_id} Bundle identity drifted")
            require(validated.execution_status == expected_execution, f"{run_id} Bundle execution drifted")
            require(validated.verdict == expected_verdict, f"{run_id} Bundle verdict drifted")
            report = read_json(run_output / "report.json")
            failed_assertions = sorted(
                item["id"] for item in report["assertions"] if item["status"] == "FAIL"
            )
            if run_id == PASS_RUN_ID:
                require(not failed_assertions, "PASS Bundle contains failed assertions")
                require(result.get("browser_capture_complete") is True, "PASS browser capture is incomplete")
            else:
                require(
                    "starter-browser-business-steps-passed" in failed_assertions,
                    "FAIL Bundle did not expose the preregistered business fact mismatch",
                )
                require(result.get("browser_capture_complete") is False, "FAIL capture unexpectedly passed")
            ensure_bundle_has_no_local_roots(run_output, [pass_root, fail_root, output])
            run_results[run_id] = {
                "execution_status": validated.execution_status,
                "verdict": validated.verdict,
                "bundle_sha256": validated.bundle_sha256,
                "failed_assertions": failed_assertions,
            }

        require(
            not list(runs.glob(".veritrail-bootstrap-run-*")),
            "owned bootstrap workspace residue remained after the two Runs",
        )
        final_draft_check = run_json_module(
            "veritrail_starter", ["validate", "--workspace", str(workspace)], cwd=REPOSITORY_ROOT
        )
        require(final_draft_check.get("valid") is True, "Starter DRAFT changed during Core execution")
        require(final_draft_check.get("seal_state") == "NOT_SEALED", "Starter DRAFT became sealed")

        catalog = output / "catalog"
        catalog_result = run_json_module(
            "veritrail",
            ["catalog-build", "--artifacts", str(runs), "--output", str(catalog)],
            cwd=REPOSITORY_ROOT,
        )
        require(catalog_result.get("run_count") == 2, "Catalog CLI did not index two Runs")
        require(catalog_result.get("issue_count") == 0, "Catalog CLI reported an issue")
        workbench = verify_workbench(
            catalog_root=catalog,
            runs_root=runs,
            output=output,
            port=args.catalog_port,
        )

        summary = {
            "schema_version": "0.1",
            "acceptance": "starter-single-webapp-s1",
            "execution_status": "COMPLETED",
            "verdict": "PASS",
            "starter": {
                "preset": "single-webapp-0.1",
                "authoring_state": "DRAFT",
                "seal_state": "NOT_SEALED",
                "doctor": "READY",
                "subject_delta": ["app/fact.json"],
            },
            "authority": {
                "profile_sha256": profile_result["profile_sha256"],
                "plan_sha256": plan_result["plan_sha256"],
                "run_count": 2,
                "preview_approval": "REGENERATED_PER_SUBJECT",
                "preview_sha256": preview_digests,
            },
            "runs": run_results,
            "catalog": {
                "status": catalog_result["status"],
                "catalog_id": catalog_result["catalog_id"],
                "run_count": catalog_result["run_count"],
                "issue_count": catalog_result["issue_count"],
                "bundle_set_sha256": catalog_result["bundle_set_sha256"],
            },
            "workbench": workbench,
            "cleanup": {
                "application_port_released": port_is_free(args.application_port),
                "catalog_port_released": port_is_free(args.catalog_port),
                "owned_workspace_residue_count": 0,
            },
            "scope": {
                "comparison_created": False,
                "reason": "independent acceptance pair; no causal Comparison claim",
            },
        }
        serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
        for local_root in (REPOSITORY_ROOT, output, pass_root, fail_root):
            require(str(local_root) not in serialized, "acceptance summary leaked an absolute local path")
        write_json(output / "acceptance.json", summary)
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        print(f"Starter S1 acceptance failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
