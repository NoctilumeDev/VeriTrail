from __future__ import annotations

import argparse
import concurrent.futures
import ctypes
import http.client
import json
import math
import os
import random
import shutil
import socket
import subprocess
import sys
import threading
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tests.support import bootstrap_plan, bootstrap_profile
from veritrail.bootstrap_preview import build_bootstrap_preview
from veritrail.bootstrap_public_run import run_bootstrap_bundle
from veritrail.bootstrap_run import run_observed_bootstrap
from veritrail.canonical import canonical_json_bytes
from veritrail.catalog import build_catalog, validate_bundle
from veritrail.project_profile import seal_project_profile
from veritrail.plan import seal_plan
from veritrail.resources import collect_preflight_evidence
from veritrail.windows_readiness import probe_owned_http_readiness
from veritrail.windows_tcp import list_ipv4_tcp_listeners


SERVICE_HELPER = REPOSITORY_ROOT / "tests" / "fixtures" / "m10_service_helper.py"
SEED = 20260813
SOFT_FREE_MEMORY_MB = 3072
HARD_FREE_MEMORY_MB = 2048
PORTS = tuple(range(18870, 18891))
WORKER_TIMEOUT_SECONDS = 90


class MemoryStatusEx(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


class ProcessMemoryCounters(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.c_ulong),
        ("PageFaultCount", ctypes.c_ulong),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the preregistered bounded M10 stress audit."
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", choices=("normal", "cancel", "http-server"))
    parser.add_argument("--scenario", type=Path)
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--barrier-ready", type=Path)
    parser.add_argument("--barrier-release", type=Path)
    parser.add_argument("--cancel-delay-ms", type=int, default=0)
    parser.add_argument("--port", type=int)
    return parser.parse_args()


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(document) + b"\n")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        document = json.load(stream)
    if not isinstance(document, dict):
        raise AssertionError(f"{path.name} is not a JSON object")
    return document


def available_memory_mb() -> int:
    status = MemoryStatusEx()
    status.dwLength = ctypes.sizeof(MemoryStatusEx)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise ctypes.WinError()
    return int(status.ullAvailPhys // (1024 * 1024))


def process_rss_mb(pid: int) -> float:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel32.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
    kernel32.OpenProcess.restype = ctypes.c_void_p
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    psapi.GetProcessMemoryInfo.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ProcessMemoryCounters),
        ctypes.c_ulong,
    ]
    psapi.GetProcessMemoryInfo.restype = ctypes.c_int
    handle = kernel32.OpenProcess(0x1000 | 0x0010, False, pid)
    if not handle:
        raise OSError(ctypes.get_last_error(), "OpenProcess failed")
    try:
        counters = ProcessMemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        if not psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
            raise OSError(ctypes.get_last_error(), "GetProcessMemoryInfo failed")
        return round(int(counters.WorkingSetSize) / (1024 * 1024), 3)
    finally:
        kernel32.CloseHandle(handle)


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


def assert_start_gate() -> int:
    free_mb = available_memory_mb()
    if free_mb < HARD_FREE_MEMORY_MB:
        raise AssertionError("available memory is below the hard stop line")
    if free_mb < SOFT_FREE_MEMORY_MB:
        raise AssertionError("available memory is below the soft stop line")
    occupied = [port for port in PORTS if not port_is_free(port)]
    if occupied:
        raise AssertionError(f"preregistered ports are occupied: {occupied}")
    return free_mb


def prepare_scenario(
    root: Path,
    *,
    label: str,
    dependency_port: int,
    application_port: int,
) -> Path:
    scenario = root / "inputs" / label
    subject = scenario / "subject"
    watched = subject / "watched"
    watched.mkdir(parents=True)
    (watched / "state.txt").write_text("stable\n", encoding="utf-8")
    shutil.copy2(SERVICE_HELPER, subject / "service.py")

    raw_profile = bootstrap_profile()
    raw_profile["profile_id"] = f"m10-stress-{label}"
    raw_profile["subject_watch_roots"] = ["watched"]
    raw_profile["max_watch_files"] = 32
    raw_profile["max_watch_total_bytes"] = 1024 * 1024
    raw_profile["lifecycle_timeout_ms"] = 20_000
    nodes = {node["node_id"]: node for node in raw_profile["nodes"]}
    dependency = nodes["dependency"]
    dependency["port"] = dependency_port
    dependency["arguments"] = [
        {"literal": "service.py"},
        {"literal": "serve"},
        {"node_port": "dependency"},
    ]
    application = nodes["application"]
    application["port"] = application_port
    application["arguments"] = [
        {"literal": "service.py"},
        {"literal": "browser-application"},
        {"node_port": "application"},
        {"node_origin": "dependency"},
    ]
    for node in nodes.values():
        node["readiness"].update(
            {
                "attempt_timeout_ms": 250,
                "total_timeout_ms": 5_000,
                "interval_ms": 50,
                "consecutive_successes": 2,
            }
        )
    profile = seal_project_profile(raw_profile)

    raw_plan = bootstrap_plan(profile)
    raw_plan["plan_id"] = f"m10-stress-{label}"
    raw_plan["subject"] = {
        "id": f"m10-stress-{label}-subject",
        "version": "1",
        "source_ref": f"stress/{label}",
    }
    raw_plan["random_seed"] = SEED
    raw_plan["preflight"].update(
        {
            "sample_count": 1,
            "sampling_interval_ms": 0,
            "hard_breach_grace_samples": 1,
            "available_memory_soft_min_mb": SOFT_FREE_MEMORY_MB,
            "available_memory_hard_min_mb": HARD_FREE_MEMORY_MB,
            "disk_free_hard_min_mb": 1024,
            "collector_rss_hard_max_mb": 2048,
            "observer_rss_delta_soft_max_mb": 1024,
            "ports": [
                {"port": dependency_port, "expected": "FREE"},
                {"port": application_port, "expected": "FREE"},
            ],
        }
    )
    application_origin = f"http://127.0.0.1:{application_port}"
    raw_plan["browser"]["start_url"] = f"{application_origin}/"
    raw_plan["browser"]["allowed_origins"] = [application_origin]
    for step in raw_plan["browser"]["steps"]:
        if step["action"] == "goto":
            step["url"] = f"{application_origin}/"
        elif step["id"] == "enter-run-label":
            step["value"] = label
        elif step["id"] == "wait-until-ready":
            step["value"] = f"evidence ready: {label}"
    plan = seal_plan(raw_plan, profile)

    bindings = {
        "schema_version": "0.1",
        "bindings": {
            "python-dependency": {"executable": str(Path(sys.executable).resolve())},
            "python-application": {"executable": str(Path(sys.executable).resolve())},
        },
    }
    write_json(scenario / "sealed-profile.json", profile)
    write_json(scenario / "sealed-plan.json", plan)
    write_json(scenario / "tool-bindings.json", bindings)
    preview = build_bootstrap_preview(
        plan,
        profile,
        subject_root=subject,
        tool_bindings_path=scenario / "tool-bindings.json",
    )
    write_json(scenario / "preview.json", preview)
    write_json(
        scenario / "scenario.json",
        {
            "label": label,
            "dependency_port": dependency_port,
            "application_port": application_port,
        },
    )
    return scenario


def worker_summary(result: Any, bundle: Path, artifact_root: Path) -> dict[str, Any]:
    validated = validate_bundle(bundle, artifact_root)
    observed = result.observed
    resource = observed.resource_observation if observed is not None else None
    cleanup_facts = (
        observed.evidence.bootstrap.document["facts"]["cleanup"]
        if observed is not None and observed.evidence is not None
        else None
    )
    return {
        "status": "OK",
        "run_id": validated.run_id,
        "execution_status": validated.execution_status,
        "verdict": validated.verdict,
        "bundle_sha256": validated.bundle_sha256,
        "bundle_file_count": len(validated.files),
        "observed": observed is not None,
        "stop_reason": (
            observed.lifecycle.stop_reason if observed is not None else None
        ),
        "cleanup_complete": (
            observed.lifecycle.cleanup_complete if observed is not None else True
        ),
        "services_ready": (
            observed.lifecycle.services_ready if observed is not None else False
        ),
        "browser_started": (
            observed.lifecycle.ready_callback_started if observed is not None else False
        ),
        "resource_observation": resource,
        "cleanup_facts": cleanup_facts,
    }


def run_worker(args: argparse.Namespace) -> int:
    if not all((args.scenario, args.bundle, args.summary, args.run_id)):
        raise ValueError("worker requires scenario, bundle, summary and run-id")
    scenario = args.scenario.resolve()
    bundle = args.bundle.resolve()
    summary_path = args.summary.resolve()
    bundle.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        plan = read_json(scenario / "sealed-plan.json")
        profile = read_json(scenario / "sealed-profile.json")
        preview = read_json(scenario / "preview.json")
        cancellation = threading.Event()

        preflight_collector: Callable[[dict[str, Any], Path], dict[str, Any]] = (
            collect_preflight_evidence
        )
        if args.barrier_ready is not None or args.barrier_release is not None:
            if args.barrier_ready is None or args.barrier_release is None:
                raise ValueError("both barrier paths are required")

            def synchronized_preflight(
                observed_plan: dict[str, Any], output_parent: Path
            ) -> dict[str, Any]:
                args.barrier_ready.parent.mkdir(parents=True, exist_ok=True)
                args.barrier_ready.write_text("ready\n", encoding="utf-8")
                deadline = time.monotonic() + 20
                while not args.barrier_release.exists():
                    if time.monotonic() >= deadline:
                        raise TimeoutError("competition barrier release timed out")
                    time.sleep(0.01)
                return collect_preflight_evidence(observed_plan, output_parent)

            preflight_collector = synchronized_preflight

        observed_runner = run_observed_bootstrap
        if args.worker == "cancel":

            def cancel_after_ready(session: Any, readiness: Any, **kwargs: Any) -> Any:
                observation = probe_owned_http_readiness(session, readiness, **kwargs)
                if session.node_id == "application" and observation.ready:
                    time.sleep(args.cancel_delay_ms / 1000)
                    cancellation.set()
                return observation

            def cancelled_runner(
                observed_plan: dict[str, Any],
                observed_profile: dict[str, Any],
                resolved: Any,
                *,
                output_parent: Path,
                cancel_event: threading.Event | None,
            ) -> Any:
                if cancel_event is not cancellation:
                    raise AssertionError("cancel Event identity changed")
                return run_observed_bootstrap(
                    observed_plan,
                    observed_profile,
                    resolved,
                    output_parent=output_parent,
                    cancel_event=cancel_event,
                    readiness_probe=cancel_after_ready,
                )

            observed_runner = cancelled_runner

        started = time.monotonic()
        result = run_bootstrap_bundle(
            plan,
            profile,
            subject_root=scenario / "subject",
            tool_bindings_path=scenario / "tool-bindings.json",
            approved_preview_sha256=preview["preview_sha256"],
            output=bundle,
            run_id=args.run_id,
            cancel_event=cancellation,
            observed_runner=observed_runner,
            preflight_collector=preflight_collector,
        )
        summary = worker_summary(result, bundle, bundle.parent)
        summary["wall_time_ms"] = round((time.monotonic() - started) * 1000, 3)
        summary["cancel_delay_ms"] = (
            args.cancel_delay_ms if args.worker == "cancel" else None
        )
        write_json(summary_path, summary)
        return 0
    except BaseException as exc:
        write_json(
            summary_path,
            {
                "status": "ERROR",
                "error_type": type(exc).__name__,
                "message": str(exc)[:500],
            },
        )
        raise


def worker_command(
    *,
    mode: str,
    scenario: Path,
    bundle: Path,
    summary: Path,
    run_id: str,
    barrier_ready: Path | None = None,
    barrier_release: Path | None = None,
    cancel_delay_ms: int = 0,
) -> list[str]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        mode,
        "--scenario",
        str(scenario),
        "--bundle",
        str(bundle),
        "--summary",
        str(summary),
        "--run-id",
        run_id,
    ]
    if barrier_ready is not None and barrier_release is not None:
        command.extend(
            [
                "--barrier-ready",
                str(barrier_ready),
                "--barrier-release",
                str(barrier_release),
            ]
        )
    if mode == "cancel":
        command.extend(["--cancel-delay-ms", str(cancel_delay_ms)])
    return command


def start_worker(command: list[str]) -> subprocess.Popen[str]:
    return subprocess.Popen(
        command,
        cwd=REPOSITORY_ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def wait_workers(
    workers: list[tuple[str, subprocess.Popen[str], Path]],
) -> tuple[list[dict[str, Any]], int]:
    deadline = time.monotonic() + WORKER_TIMEOUT_SECONDS
    minimum_free = available_memory_mb()
    while any(process.poll() is None for _, process, _ in workers):
        free_mb = available_memory_mb()
        minimum_free = min(minimum_free, free_mb)
        if free_mb < HARD_FREE_MEMORY_MB:
            for _, process, _ in workers:
                if process.poll() is None:
                    process.terminate()
            raise AssertionError("hard memory stop line reached")
        if time.monotonic() >= deadline:
            for _, process, _ in workers:
                if process.poll() is None:
                    process.terminate()
            raise TimeoutError("worker wave timed out")
        time.sleep(0.05)

    summaries: list[dict[str, Any]] = []
    for label, process, summary_path in workers:
        stdout, stderr = process.communicate(timeout=5)
        if process.returncode != 0:
            detail = read_json(summary_path) if summary_path.is_file() else {}
            raise AssertionError(
                f"worker {label} failed: {detail}; stderr={stderr[-1000:]!r}; "
                f"stdout={stdout[-500:]!r}"
            )
        summary = read_json(summary_path)
        if summary.get("status") != "OK":
            raise AssertionError(f"worker {label} returned {summary}")
        summary["label"] = label
        summaries.append(summary)
    return summaries, minimum_free


def assert_wave_clean(root: Path, ports: tuple[int, ...]) -> dict[str, Any]:
    occupied = [port for port in ports if not port_is_free(port)]
    staging = sorted(
        path.name for path in (root / "run-roots").rglob(".veritrail-*")
    )
    if occupied or staging:
        raise AssertionError(
            f"wave residue detected: occupied={occupied}, staging={staging}"
        )
    return {"ports_released": True, "staging_count": 0}


def publish_bundles(root: Path, labels: list[str]) -> None:
    for label in labels:
        source = root / "run-roots" / label / "bundle"
        target = root / "artifacts" / label
        if not source.is_dir() or target.exists():
            raise AssertionError(f"cannot publish isolated Bundle for {label}")
        source.rename(target)
        validate_bundle(target, root / "artifacts")


def run_same_port_wave(root: Path, rng: random.Random) -> dict[str, Any]:
    scenario = prepare_scenario(
        root,
        label="same-port",
        dependency_port=18870,
        application_port=18871,
    )
    barrier = root / "barriers" / "same-port.release"
    labels = ["same-a", "same-b"]
    rng.shuffle(labels)
    workers: list[tuple[str, subprocess.Popen[str], Path]] = []
    for label in labels:
        summary = root / "worker-summaries" / f"{label}.json"
        ready = root / "barriers" / f"{label}.ready"
        command = worker_command(
            mode="normal",
            scenario=scenario,
            bundle=root / "run-roots" / label / "bundle",
            summary=summary,
            run_id=f"m10-stress-{label}",
            barrier_ready=ready,
            barrier_release=barrier,
        )
        workers.append((label, start_worker(command), summary))
    deadline = time.monotonic() + 20
    ready_paths = [root / "barriers" / f"{label}.ready" for label in labels]
    while not all(path.exists() for path in ready_paths):
        if any(process.poll() is not None for _, process, _ in workers):
            wait_workers(workers)
            raise AssertionError("same-port worker exited before synchronized release")
        if time.monotonic() >= deadline:
            raise TimeoutError("same-port workers did not reach the barrier")
        time.sleep(0.02)
    barrier.write_text("release\n", encoding="utf-8")
    summaries, minimum_free = wait_workers(workers)
    pass_count = sum(item["verdict"] == "PASS" for item in summaries)
    if pass_count > 1:
        raise AssertionError(f"same-port wave produced multiple PASS Runs: {summaries}")
    for item in summaries:
        if item["verdict"] == "PASS":
            if item["execution_status"] != "COMPLETED":
                raise AssertionError("same-port winner did not complete")
        elif item["verdict"] == "PENDING":
            if item["execution_status"] != "ABORTED" or item["observed"]:
                raise AssertionError(f"same-port preflight stop is invalid: {item}")
        elif item["verdict"] == "FAIL":
            cleanup = item.get("cleanup_facts")
            expected_contention_cleanup = (
                item["execution_status"] == "ERROR"
                and item["stop_reason"] == "CLEANUP_ERROR"
                and isinstance(cleanup, dict)
                and cleanup.get("ports_free") is False
                and all(
                    cleanup.get(field) is True
                    for field in (
                        "jobs_empty",
                        "handles_released",
                        "readers_released",
                        "reverse_order_complete",
                        "run_work_released",
                        "staging_released",
                    )
                )
            )
            expected_readiness_failure = (
                item["execution_status"] in {"ABORTED", "COMPLETED"}
                and item["stop_reason"]
                in {
                    "LISTENER_OWNERSHIP_MISMATCH",
                    "NODE_EARLY_EXIT",
                    "READINESS_TIMEOUT",
                }
                and item["cleanup_complete"]
            )
            if not expected_contention_cleanup and not expected_readiness_failure:
                raise AssertionError(f"same-port failure is unexplained: {item}")
        else:
            raise AssertionError(f"same-port result is unexplained: {item}")
    publish_bundles(root, ["same-a", "same-b"])
    clean = assert_wave_clean(root, (18870, 18871))
    return {
        "name": "same-port-competition",
        "start_order": labels,
        "minimum_free_memory_mb": minimum_free,
        "runs": summaries,
        "clean": clean,
    }


def run_independent_wave(
    root: Path,
    rng: random.Random,
    *,
    degree: int,
    definitions: list[tuple[str, int, int]],
) -> dict[str, Any]:
    if available_memory_mb() < SOFT_FREE_MEMORY_MB:
        raise AssertionError("soft memory stop line reached before independent wave")
    workers: list[tuple[str, subprocess.Popen[str], Path]] = []
    prepared: list[tuple[str, Path]] = []
    for label, dependency_port, application_port in definitions:
        scenario = prepare_scenario(
            root,
            label=label,
            dependency_port=dependency_port,
            application_port=application_port,
        )
        prepared.append((label, scenario))
    rng.shuffle(prepared)
    for label, scenario in prepared:
        summary = root / "worker-summaries" / f"{label}.json"
        workers.append(
            (
                label,
                start_worker(
                    worker_command(
                        mode="normal",
                        scenario=scenario,
                        bundle=root / "run-roots" / label / "bundle",
                        summary=summary,
                        run_id=f"m10-stress-{label}",
                    )
                ),
                summary,
            )
        )
    summaries, minimum_free = wait_workers(workers)
    if len(summaries) != degree or any(
        item["execution_status"] != "COMPLETED"
        or item["verdict"] != "PASS"
        or not item["cleanup_complete"]
        for item in summaries
    ):
        raise AssertionError(f"independent degree {degree} did not pass: {summaries}")
    publish_bundles(root, [label for label, _, _ in definitions])
    ports = tuple(port for _, dep, app in definitions for port in (dep, app))
    clean = assert_wave_clean(root, ports)
    return {
        "name": f"independent-degree-{degree}",
        "start_order": [label for label, _ in prepared],
        "minimum_free_memory_mb": minimum_free,
        "runs": summaries,
        "clean": clean,
    }


def run_cancel_wave(root: Path, rng: random.Random) -> dict[str, Any]:
    if available_memory_mb() < SOFT_FREE_MEMORY_MB:
        raise AssertionError("soft memory stop line reached before cancel wave")
    definitions = [
        ("cancel-a", 18884, 18885),
        ("cancel-b", 18886, 18887),
        ("cancel-c", 18888, 18889),
    ]
    delays = rng.sample([10, 30, 50, 70, 90], 3)
    prepared: list[tuple[str, Path, int]] = []
    for (label, dependency_port, application_port), delay in zip(definitions, delays):
        prepared.append(
            (
                label,
                prepare_scenario(
                    root,
                    label=label,
                    dependency_port=dependency_port,
                    application_port=application_port,
                ),
                delay,
            )
        )
    rng.shuffle(prepared)
    workers: list[tuple[str, subprocess.Popen[str], Path]] = []
    for label, scenario, delay in prepared:
        summary = root / "worker-summaries" / f"{label}.json"
        workers.append(
            (
                label,
                start_worker(
                    worker_command(
                        mode="cancel",
                        scenario=scenario,
                        bundle=root / "run-roots" / label / "bundle",
                        summary=summary,
                        run_id=f"m10-stress-{label}",
                        cancel_delay_ms=delay,
                    )
                ),
                summary,
            )
        )
    summaries, minimum_free = wait_workers(workers)
    if any(
        item["execution_status"] != "ABORTED"
        or item["verdict"] != "PENDING"
        or item["stop_reason"] != "USER_CANCELLED"
        or item["browser_started"]
        or not item["cleanup_complete"]
        for item in summaries
    ):
        raise AssertionError(f"cancel wave is inconsistent: {summaries}")
    publish_bundles(root, [label for label, _, _ in definitions])
    clean = assert_wave_clean(root, tuple(range(18884, 18890)))
    return {
        "name": "cancel-cleanup-interleave",
        "seed": SEED,
        "start_order": [label for label, _, _ in prepared],
        "delays_ms": {label: delay for label, _, delay in prepared},
        "minimum_free_memory_mb": minimum_free,
        "runs": summaries,
        "clean": clean,
    }


class HealthHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        if self.path != "/health":
            self.send_error(404)
            return
        content = b"m10-stress-ready"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, _format: str, *_args: object) -> None:
        return


def serve_http(port: int) -> int:
    server = ThreadingHTTPServer(("127.0.0.1", port), HealthHandler)
    server.daemon_threads = True
    print("READY", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


def tcp_state_counts(port: int) -> dict[str, int]:
    command = (
        f"$rows=Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue;"
        "$groups=@($rows|Group-Object State|ForEach-Object{"
        "[pscustomobject]@{state=$_.Name;count=$_.Count}});"
        "$groups|ConvertTo-Json -Compress"
    )
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=10,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        check=True,
    )
    value = completed.stdout.strip()
    if not value:
        return {}
    parsed = json.loads(value)
    rows = parsed if isinstance(parsed, list) else [parsed]
    return {str(row["state"]): int(row["count"]) for row in rows}


def request_partition(total: int, workers: int) -> list[int]:
    base, remainder = divmod(total, workers)
    return [base + (1 if index < remainder else 0) for index in range(workers)]


def request_worker(port: int, count: int) -> tuple[list[float], Counter[str]]:
    latencies: list[float] = []
    errors: Counter[str] = Counter()
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        for _ in range(count):
            started = time.perf_counter()
            try:
                connection.request("GET", "/health", headers={"Connection": "keep-alive"})
                response = connection.getresponse()
                content = response.read(1024)
                if response.status != 200:
                    errors[f"HTTP_{response.status}"] += 1
                elif content != b"m10-stress-ready":
                    errors["BODY_MISMATCH"] += 1
            except BaseException as exc:
                errors[type(exc).__name__] += 1
                connection.close()
                connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            latencies.append((time.perf_counter() - started) * 1000)
    finally:
        connection.close()
    return latencies, errors


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(len(ordered) * fraction) - 1))
    return round(ordered[index], 3)


def run_http_stage(port: int, total: int, in_flight: int) -> dict[str, Any]:
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=in_flight) as executor:
        futures = [
            executor.submit(request_worker, port, count)
            for count in request_partition(total, in_flight)
        ]
        time.sleep(0.02)
        states_during = tcp_state_counts(port)
        results = [future.result(timeout=30) for future in futures]
    elapsed = time.perf_counter() - started
    latencies = [latency for values, _ in results for latency in values]
    errors: Counter[str] = Counter()
    for _, observed in results:
        errors.update(observed)
    return {
        "in_flight": in_flight,
        "request_count": total,
        "completed_count": len(latencies),
        "errors": dict(sorted(errors.items())),
        "elapsed_ms": round(elapsed * 1000, 3),
        "requests_per_second": round(total / elapsed, 3),
        "p50_ms": percentile(latencies, 0.50),
        "p95_ms": percentile(latencies, 0.95),
        "p99_ms": percentile(latencies, 0.99),
        "tcp_states_during": states_during,
        "free_memory_mb_after": available_memory_mb(),
    }


def run_http_wave(root: Path) -> dict[str, Any]:
    if available_memory_mb() < SOFT_FREE_MEMORY_MB:
        raise AssertionError("soft memory stop line reached before HTTP wave")
    process = subprocess.Popen(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker",
            "http-server",
            "--port",
            "18890",
        ],
        cwd=REPOSITORY_ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    try:
        deadline = time.monotonic() + 10
        owner = None
        while time.monotonic() < deadline:
            rows = [
                row
                for row in list_ipv4_tcp_listeners()
                if row.local_address == "127.0.0.1" and row.local_port == 18890
            ]
            if len(rows) == 1:
                owner = rows[0].owning_pid
                break
            if process.poll() is not None:
                raise AssertionError("HTTP stress server exited before readiness")
            time.sleep(0.05)
        if owner != process.pid:
            raise AssertionError(
                f"HTTP listener owner mismatch: expected {process.pid}, observed {owner}"
            )
        stages: list[dict[str, Any]] = []
        minimum_free = available_memory_mb()
        for total, in_flight in ((100, 1), (200, 10), (300, 50), (400, 100)):
            free_mb = available_memory_mb()
            minimum_free = min(minimum_free, free_mb)
            if free_mb < SOFT_FREE_MEMORY_MB:
                raise AssertionError("soft memory stop line reached during HTTP ladder")
            stage = run_http_stage(18890, total, in_flight)
            stage["server_rss_mb"] = process_rss_mb(process.pid)
            stages.append(stage)
            minimum_free = min(minimum_free, int(stage["free_memory_mb_after"]))
            if stage["completed_count"] != total or stage["errors"]:
                raise AssertionError(f"HTTP stage failed: {stage}")
            rows = [
                row
                for row in list_ipv4_tcp_listeners()
                if row.local_address == "127.0.0.1" and row.local_port == 18890
            ]
            if len(rows) != 1 or rows[0].owning_pid != process.pid:
                raise AssertionError("HTTP listener ownership changed during ladder")
        if sum(int(stage["request_count"]) for stage in stages) != 1000:
            raise AssertionError("HTTP request total drifted from 1000")
        return {
            "name": "http-1000-total",
            "listener_owner_verified": True,
            "minimum_free_memory_mb": minimum_free,
            "stages": stages,
        }
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=5)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and not port_is_free(18890):
            time.sleep(0.05)
        if not port_is_free(18890):
            raise AssertionError("HTTP stress port was not released")


def run_parent(output: Path) -> int:
    if os.name != "nt":
        raise AssertionError("M10 stress acceptance is Windows-only")
    output = output.resolve()
    if output.exists():
        raise AssertionError("stress acceptance refuses to overwrite output")
    output.mkdir(parents=True)
    (output / "artifacts").mkdir()
    (output / "run-roots").mkdir()
    start_memory = assert_start_gate()
    rng = random.Random(SEED)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m10-bounded-stress-audit",
        "seed": SEED,
        "soft_free_memory_mb": SOFT_FREE_MEMORY_MB,
        "hard_free_memory_mb": HARD_FREE_MEMORY_MB,
        "start_free_memory_mb": start_memory,
        "execution_status": "RUNNING",
        "verdict": "INCONCLUSIVE",
        "waves": [],
    }
    summary_path = output / "stress-summary.json"
    write_json(summary_path, summary)
    try:
        summary["waves"].append(run_same_port_wave(output, rng))
        summary["waves"].append(
            run_independent_wave(
                output,
                rng,
                degree=1,
                definitions=[("independent-1a", 18872, 18873)],
            )
        )
        summary["waves"].append(
            run_independent_wave(
                output,
                rng,
                degree=2,
                definitions=[
                    ("independent-2a", 18874, 18875),
                    ("independent-2b", 18876, 18877),
                ],
            )
        )
        summary["waves"].append(
            run_independent_wave(
                output,
                rng,
                degree=3,
                definitions=[
                    ("independent-3a", 18878, 18879),
                    ("independent-3b", 18880, 18881),
                    ("independent-3c", 18882, 18883),
                ],
            )
        )
        summary["waves"].append(run_cancel_wave(output, rng))
        summary["waves"].append(run_http_wave(output))

        catalog = build_catalog(output / "artifacts", output / "catalog")
        expected_bundles = 2 + 1 + 2 + 3 + 3
        if (
            catalog.status != "COMPLETED"
            or catalog.run_count != expected_bundles
            or catalog.issue_count != 0
            or catalog.duplicate_count != 0
        ):
            raise AssertionError(f"final Catalog mismatch: {catalog}")
        for bundle in (output / "artifacts").iterdir():
            if bundle.is_dir():
                validate_bundle(bundle, output / "artifacts")
        clean = assert_wave_clean(output, PORTS)
        summary.update(
            {
                "execution_status": "COMPLETED",
                "verdict": "PASS",
                "end_free_memory_mb": available_memory_mb(),
                "minimum_free_memory_mb": min(
                    int(wave["minimum_free_memory_mb"]) for wave in summary["waves"]
                ),
                "catalog": {
                    "run_count": catalog.run_count,
                    "issue_count": catalog.issue_count,
                    "duplicate_count": catalog.duplicate_count,
                    "bundle_set_sha256": catalog.bundle_set_sha256,
                },
                "final_clean": clean,
            }
        )
        write_json(summary_path, summary)
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
        return 0
    except BaseException as exc:
        summary.update(
            {
                "execution_status": "ERROR",
                "verdict": "FAIL",
                "error_type": type(exc).__name__,
                "message": str(exc)[:1000],
                "end_free_memory_mb": available_memory_mb(),
            }
        )
        write_json(summary_path, summary)
        raise


def main() -> int:
    args = parse_args()
    if args.worker == "http-server":
        if args.port != 18890:
            raise ValueError("http-server worker requires preregistered port 18890")
        return serve_http(args.port)
    if args.worker in {"normal", "cancel"}:
        return run_worker(args)
    if args.output is None:
        raise ValueError("parent acceptance requires --output")
    return run_parent(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
