from __future__ import annotations

import argparse
import copy
import http.client
import io
import json
import shutil
import socket
import sys
import tempfile
import threading
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from veritrail.cli import main as cli_main
from veritrail.orchestration import (
    RequestRecorder,
    collect_orchestrated_evidence,
    create_static_server,
    prepare_static_target,
)
from veritrail.plan import load_and_seal_plan


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = REPOSITORY_ROOT / "examples" / "orchestration" / "plan.json"
DEFAULT_SUBJECT = REPOSITORY_ROOT
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m5-orchestrator-acceptance"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded M5 orchestrator controls.")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--subject-root", type=Path, default=DEFAULT_SUBJECT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def exclusive_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
        if exclusive is not None:
            probe.setsockopt(socket.SOL_SOCKET, exclusive, 1)
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True


def request(
    port: int,
    method: str,
    path: str,
    *,
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, str], bytes]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
    request_headers = {"Host": f"127.0.0.1:{port}", **(headers or {})}
    try:
        connection.request(method, path, headers=request_headers)
        response = connection.getresponse()
        body = response.read()
        return (
            response.status,
            {name.lower(): value for name, value in response.getheaders()},
            body,
        )
    finally:
        connection.close()


def write_plan(path: Path, plan: dict[str, Any], version: int) -> None:
    candidate = copy.deepcopy(plan)
    candidate.pop("seal", None)
    candidate["version"] = version
    path.write_text(
        json.dumps(candidate, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def run_cli_control(
    *,
    plan_path: Path,
    subject_root: Path,
    output: Path,
    run_id: str,
) -> dict[str, Any]:
    stream = io.StringIO()
    with redirect_stdout(stream):
        code = cli_main(
            [
                "run",
                "--plan",
                str(plan_path),
                "--subject-root",
                str(subject_root),
                "--run-id",
                run_id,
                "--output",
                str(output),
            ]
        )
    if code != 0:
        raise AssertionError(f"run control returned exit code {code}")
    return json.loads(stream.getvalue())


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if output.exists():
        print("M5 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    plan = load_and_seal_plan(args.plan.resolve())
    if plan["schema_version"] != "0.4":
        print("M5 acceptance requires an ExperimentPlan 0.4 input.", file=sys.stderr)
        return 2
    source_root = args.subject_root.resolve()
    source_target = source_root / Path(plan["target"]["root"])
    if not source_target.is_dir():
        print("M5 acceptance target root is unavailable.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m5-bounded-run-orchestrator",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "checks": [],
        "controls": {},
    }
    active_server = None
    active_thread = None
    exit_code = 1
    port = plan["target"]["port"]
    try:
        if not exclusive_port_free(port):
            raise AssertionError("sealed target port is not free")
        with tempfile.TemporaryDirectory() as directory:
            isolated_root = Path(directory)
            isolated_target = isolated_root / Path(plan["target"]["root"])
            isolated_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source_target, isolated_target)
            snapshot = prepare_static_target(plan, isolated_root)
            if snapshot.fingerprint != plan["baseline"]["fingerprint"]:
                raise AssertionError("isolated target fingerprint differs from the sealed baseline")

            recorder = RequestRecorder()
            active_server = create_static_server(snapshot, port, recorder)
            active_thread = threading.Thread(target=active_server.serve_forever, daemon=True)
            active_thread.start()
            status, headers, body = request(port, "GET", "/data.json?run=private-value")
            if status != 200 or not body or "access-control-allow-origin" in headers:
                raise AssertionError("query-bearing read-only request contract failed")
            if request(port, "HEAD", "/index.html")[0] != 200:
                raise AssertionError("HEAD contract failed")
            if request(port, "POST", "/index.html")[0] != 405:
                raise AssertionError("write method was not rejected")
            if request(port, "GET", "/index.html", headers={"Range": "bytes=0-1"})[0] != 416:
                raise AssertionError("Range request was not rejected")
            if request(port, "GET", "/index.html", headers={"Host": "example.invalid"})[0] != 400:
                raise AssertionError("foreign Host was not rejected")
            if request(port, "GET", "/%2e%2e/private.txt")[0] != 400:
                raise AssertionError("encoded traversal was not rejected")
            if request(port, "GET", "/missing.txt")[0] != 404:
                raise AssertionError("missing resource did not remain missing")

            mutable = isolated_target / "data.json"
            original = mutable.read_bytes()
            mutated = bytes([original[0] ^ 1]) + original[1:]
            mutable.write_bytes(mutated)
            if request(port, "GET", "/data.json")[0] != 409:
                raise AssertionError("same-size source mutation was not rejected")
            mutable.write_bytes(original)
            if any(
                "?" in item["path"] or "private-value" in item["path"]
                for item in recorder.requests
            ):
                raise AssertionError("request recorder persisted a query value")
            summary["controls"]["http"] = {
                "query_get": 200,
                "head": 200,
                "post": 405,
                "range": 416,
                "foreign_host": 400,
                "encoded_traversal": 400,
                "missing": 404,
                "source_changed": 409,
                "query_values_persisted": False,
            }
            summary["checks"].append("static-http-negative-boundary")
            active_server.shutdown()
            active_server.server_close()
            active_thread.join(5)
            if active_thread.is_alive() or not exclusive_port_free(port):
                raise AssertionError("static HTTP control did not clean up")
            active_server = None
            active_thread = None

            abort_plan = copy.deepcopy(plan)
            abort_plan.pop("seal", None)
            abort_plan["preflight"].update(
                sample_count=1,
                sampling_interval_ms=0,
                hard_breach_grace_samples=1,
                available_memory_soft_min_mb=2_000_000,
                available_memory_hard_min_mb=2_000_000,
            )
            abort_path = isolated_root / "abort-plan.json"
            write_plan(abort_path, abort_plan, 10)
            abort = run_cli_control(
                plan_path=abort_path,
                subject_root=isolated_root,
                output=output / "abort-run",
                run_id="m5-acceptance-abort",
            )
            if abort["resource_decision"] != "ABORT" or abort["target_started"]:
                raise AssertionError("ABORT control started the target")
            summary["controls"]["preflight_abort"] = {
                "execution_status": abort["execution_status"],
                "verdict": abort["verdict"],
                "target_started": abort["target_started"],
            }
            summary["checks"].append("preflight-abort-no-start")

            stop_plan = copy.deepcopy(plan)
            stop_plan.pop("seal", None)
            stop_plan["preflight"].update(
                sample_count=1,
                sampling_interval_ms=0,
                hard_breach_grace_samples=1,
                available_memory_soft_min_mb=2_000_000,
                available_memory_hard_min_mb=1,
            )
            stop_path = isolated_root / "stop-plan.json"
            write_plan(stop_path, stop_plan, 11)
            stop = run_cli_control(
                plan_path=stop_path,
                subject_root=isolated_root,
                output=output / "stop-run",
                run_id="m5-acceptance-stop",
            )
            if stop["resource_decision"] != "STOP_ESCALATION" or stop["target_started"]:
                raise AssertionError("STOP_ESCALATION control started the target")
            summary["controls"]["preflight_stop"] = {
                "execution_status": stop["execution_status"],
                "verdict": stop["verdict"],
                "target_started": stop["target_started"],
            }
            summary["checks"].append("preflight-stop-no-start")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as blocker:
                blocker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
                blocker.bind(("127.0.0.1", port))
                blocker.listen(8)
                conflict = collect_orchestrated_evidence(plan, isolated_root)
                facts = conflict.orchestration.document["facts"]
                if (
                    conflict.execution_status != "ERROR"
                    or facts["server_started"]
                    or facts["port_released"]
                    or not any(
                        item["stage"] == "target-start"
                        for item in facts["collection_errors"]
                    )
                ):
                    raise AssertionError("port conflict was not contained")
            if not exclusive_port_free(port):
                raise AssertionError("external port blocker was not released by its owner")
            summary["controls"]["port_conflict"] = {
                "execution_status": conflict.execution_status,
                "server_started": facts["server_started"],
                "port_released_while_blocked": facts["port_released"],
                "external_listener_stopped_by_veritrail": False,
            }
            summary["checks"].append("port-conflict-contained")

            failure_plan = copy.deepcopy(plan)
            failure_plan.pop("seal", None)
            failure_plan["version"] = 12
            failure_plan["browser"]["timeout_ms"] = 1500
            failure_plan["browser"]["steps"][0]["selector"] = "[data-testid='missing-control']"
            failure_path = isolated_root / "browser-failure-plan.json"
            write_plan(failure_path, failure_plan, 12)
            browser_failure = run_cli_control(
                plan_path=failure_path,
                subject_root=isolated_root,
                output=output / "browser-failure-run",
                run_id="m5-acceptance-browser-failure",
            )
            if (
                browser_failure["execution_status"] != "ERROR"
                or browser_failure["target_ready"] is not True
                or browser_failure["cleanup_complete"] is not True
                or not exclusive_port_free(port)
            ):
                raise AssertionError("browser failure did not preserve target cleanup")
            summary["controls"]["browser_failure"] = {
                "execution_status": browser_failure["execution_status"],
                "verdict": browser_failure["verdict"],
                "target_ready": browser_failure["target_ready"],
                "cleanup_complete": browser_failure["cleanup_complete"],
                "port_released": True,
            }
            summary["checks"].append("browser-failure-cleanup")

        summary["execution_status"] = "COMPLETED"
        summary["verdict"] = "PASS"
        exit_code = 0
    except Exception as error:
        summary["execution_status"] = "ERROR"
        summary["verdict"] = "FAIL"
        summary["failure_type"] = type(error).__name__
    finally:
        if active_server is not None:
            active_server.shutdown()
            active_server.server_close()
        if active_thread is not None:
            active_thread.join(5)
        summary["ended_at"] = utc_now()
        summary["port_released"] = exclusive_port_free(port)
        (output / "acceptance.json").write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )

    print(
        json.dumps(
            {
                "execution_status": summary["execution_status"],
                "verdict": summary["verdict"],
                "checks": len(summary["checks"]),
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
