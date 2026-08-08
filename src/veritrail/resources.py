from __future__ import annotations

import ctypes
import copy
import os
import platform
import shutil
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from veritrail.canonical import sha256_json

MEBIBYTE = 1024 * 1024
COLLECTOR_VERSION = "resource-preflight/0.1"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _windows_host_memory_bytes() -> tuple[int, int]:
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

    status = MemoryStatusEx()
    status.dwLength = ctypes.sizeof(status)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MemoryStatusEx)]
    kernel32.GlobalMemoryStatusEx.restype = ctypes.c_int
    if not kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise OSError(ctypes.get_last_error(), "GlobalMemoryStatusEx failed")
    return int(status.ullTotalPhys), int(status.ullAvailPhys)


def _proc_host_memory_bytes() -> tuple[int, int]:
    values: dict[str, int] = {}
    with Path("/proc/meminfo").open("r", encoding="ascii") as handle:
        for line in handle:
            name, raw = line.split(":", 1)
            if name in {"MemTotal", "MemAvailable"}:
                values[name] = int(raw.strip().split()[0]) * 1024
    if set(values) != {"MemTotal", "MemAvailable"}:
        raise OSError("required /proc/meminfo fields are unavailable")
    return values["MemTotal"], values["MemAvailable"]


def host_memory_bytes() -> tuple[int, int]:
    if os.name == "nt":
        return _windows_host_memory_bytes()
    if Path("/proc/meminfo").is_file():
        return _proc_host_memory_bytes()
    page_size = os.sysconf("SC_PAGE_SIZE")
    total_pages = os.sysconf("SC_PHYS_PAGES")
    available_pages = os.sysconf("SC_AVPHYS_PAGES")
    return int(page_size * total_pages), int(page_size * available_pages)


def _windows_process_rss_bytes() -> int:
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

    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    psapi.GetProcessMemoryInfo.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ProcessMemoryCounters),
        ctypes.c_ulong,
    ]
    psapi.GetProcessMemoryInfo.restype = ctypes.c_int
    process = kernel32.GetCurrentProcess()
    if not psapi.GetProcessMemoryInfo(process, ctypes.byref(counters), counters.cb):
        raise OSError(ctypes.get_last_error(), "GetProcessMemoryInfo failed")
    return int(counters.WorkingSetSize)


def process_rss_bytes() -> int:
    if os.name == "nt":
        return _windows_process_rss_bytes()
    statm = Path("/proc/self/statm")
    if statm.is_file():
        resident_pages = int(statm.read_text(encoding="ascii").split()[1])
        return resident_pages * int(os.sysconf("SC_PAGE_SIZE"))
    import resource

    maximum = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(maximum if sys.platform == "darwin" else maximum * 1024)


def _existing_ancestor(path: Path) -> Path:
    candidate = path.resolve()
    while not candidate.exists() and candidate.parent != candidate:
        candidate = candidate.parent
    if not candidate.exists():
        raise OSError("no existing ancestor for output volume")
    return candidate


def _proxy_presence() -> dict[str, bool]:
    def configured(*names: str) -> bool:
        return any(bool(os.environ.get(name)) for name in names)

    return {
        "http_configured": configured("HTTP_PROXY", "http_proxy"),
        "https_configured": configured("HTTPS_PROXY", "https_proxy"),
        "all_configured": configured("ALL_PROXY", "all_proxy"),
        "no_proxy_configured": configured("NO_PROXY", "no_proxy"),
    }


def environment_summary(total_memory_mb: int) -> dict[str, Any]:
    offset = datetime.now().astimezone().utcoffset()
    offset_minutes = int(offset.total_seconds() // 60) if offset is not None else 0
    return {
        "operating_system": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
        },
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
        },
        "cpu_logical_count": os.cpu_count(),
        "memory_total_mb": total_memory_mb,
        "timezone_offset_minutes": offset_minutes,
        "proxy": _proxy_presence(),
    }


def probe_loopback_ports(port_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for rule in port_rules:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(0.2)
            listening = client.connect_ex(("127.0.0.1", rule["port"])) == 0
        actual = "LISTENING" if listening else "FREE"
        results.append(
            {
                "port": rule["port"],
                "expected": rule["expected"],
                "actual": actual,
                "matched": actual == rule["expected"],
            }
        )
    return results


def staging_residue_count(output_parent: Path) -> int:
    if not output_parent.exists():
        return 0
    return sum(1 for item in output_parent.glob(".veritrail-*") if item.exists())


def collect_resource_sample(output_parent: Path) -> dict[str, Any]:
    total_memory, available_memory = host_memory_bytes()
    disk = shutil.disk_usage(_existing_ancestor(output_parent))
    return {
        "captured_at": _utc_now(),
        "memory_total_mb": round(total_memory / MEBIBYTE, 3),
        "available_memory_mb": round(available_memory / MEBIBYTE, 3),
        "disk_total_mb": round(disk.total / MEBIBYTE, 3),
        "disk_free_mb": round(disk.free / MEBIBYTE, 3),
        "collector_rss_mb": round(process_rss_bytes() / MEBIBYTE, 3),
    }


def assess_preflight(
    *,
    policy: dict[str, Any],
    samples: list[dict[str, Any]],
    port_checks: list[dict[str, Any]],
    residue_count: int,
    collection_errors: list[dict[str, str]],
    observer_start_rss_mb: float,
) -> dict[str, Any]:
    hard_reasons: list[dict[str, Any]] = []
    soft_reasons: list[dict[str, Any]] = []

    for error in collection_errors:
        hard_reasons.append(
            {
                "code": "COLLECTION_ERROR",
                "severity": "HARD",
                "collector": error["collector"],
            }
        )
    mismatches = [item for item in port_checks if not item["matched"]]
    for item in mismatches:
        hard_reasons.append(
            {
                "code": "PORT_STATE_MISMATCH",
                "severity": "HARD",
                "port": item["port"],
                "expected": item["expected"],
                "actual": item["actual"],
            }
        )
    if policy["require_clean_staging"] and residue_count:
        hard_reasons.append(
            {
                "code": "STAGING_RESIDUE",
                "severity": "HARD",
                "observed": residue_count,
                "threshold": 0,
                "unit": "entries",
            }
        )

    hard_memory_streak = 0
    max_hard_memory_streak = 0
    for sample in samples:
        if sample["available_memory_mb"] < policy["available_memory_hard_min_mb"]:
            hard_memory_streak += 1
            max_hard_memory_streak = max(max_hard_memory_streak, hard_memory_streak)
        else:
            hard_memory_streak = 0
    if max_hard_memory_streak >= policy["hard_breach_grace_samples"]:
        hard_reasons.append(
            {
                "code": "AVAILABLE_MEMORY_HARD_BREACH",
                "severity": "HARD",
                "observed": min(sample["available_memory_mb"] for sample in samples),
                "threshold": policy["available_memory_hard_min_mb"],
                "unit": "MiB",
                "max_consecutive_samples": max_hard_memory_streak,
            }
        )

    if samples:
        minimum_disk = min(sample["disk_free_mb"] for sample in samples)
        if minimum_disk < policy["disk_free_hard_min_mb"]:
            hard_reasons.append(
                {
                    "code": "DISK_FREE_HARD_BREACH",
                    "severity": "HARD",
                    "observed": minimum_disk,
                    "threshold": policy["disk_free_hard_min_mb"],
                    "unit": "MiB",
                }
            )
        peak_rss = max([observer_start_rss_mb, *(sample["collector_rss_mb"] for sample in samples)])
        if peak_rss > policy["collector_rss_hard_max_mb"]:
            hard_reasons.append(
                {
                    "code": "COLLECTOR_RSS_HARD_BREACH",
                    "severity": "HARD",
                    "observed": peak_rss,
                    "threshold": policy["collector_rss_hard_max_mb"],
                    "unit": "MiB",
                }
            )
        minimum_memory = min(sample["available_memory_mb"] for sample in samples)
        if minimum_memory < policy["available_memory_soft_min_mb"]:
            soft_reasons.append(
                {
                    "code": "AVAILABLE_MEMORY_SOFT_BREACH",
                    "severity": "SOFT",
                    "observed": minimum_memory,
                    "threshold": policy["available_memory_soft_min_mb"],
                    "unit": "MiB",
                }
            )
    else:
        peak_rss = observer_start_rss_mb

    observer_delta = max(0.0, round(peak_rss - observer_start_rss_mb, 3))
    if observer_delta > policy["observer_rss_delta_soft_max_mb"]:
        soft_reasons.append(
            {
                "code": "OBSERVER_RSS_DELTA_SOFT_BREACH",
                "severity": "SOFT",
                "observed": observer_delta,
                "threshold": policy["observer_rss_delta_soft_max_mb"],
                "unit": "MiB",
            }
        )

    decision = "ABORT" if hard_reasons else "STOP_ESCALATION" if soft_reasons else "PROCEED"
    return {
        "decision": decision,
        "decision_reasons": [*hard_reasons, *soft_reasons],
        "max_consecutive_memory_hard_breaches": max_hard_memory_streak,
        "observer_effect": {
            "rss_start_mb": observer_start_rss_mb,
            "rss_peak_mb": peak_rss,
            "rss_delta_mb": observer_delta,
        },
    }


def _known_observed_variables(plan: dict[str, Any], environment: dict[str, Any]) -> dict[str, Any]:
    known = {
        "operating_system": environment["operating_system"]["system"],
        "python_major_minor": ".".join(environment["python"]["version"].split(".")[:2]),
        "cpu_logical_count": environment["cpu_logical_count"],
    }
    declared_names = {variable["name"] for variable in plan["variables"]}
    return {name: value for name, value in known.items() if name in declared_names}


def collect_preflight_evidence(plan: dict[str, Any], output_parent: Path) -> dict[str, Any]:
    started_at = _utc_now()
    started_monotonic = time.monotonic()
    policy = plan["preflight"]
    errors: list[dict[str, str]] = []
    samples: list[dict[str, Any]] = []

    try:
        observer_start_rss_mb = round(process_rss_bytes() / MEBIBYTE, 3)
    except (OSError, ValueError) as exc:
        observer_start_rss_mb = 0.0
        errors.append({"collector": "process_rss", "error_type": type(exc).__name__})

    try:
        port_checks = probe_loopback_ports(policy["ports"])
    except OSError as exc:
        port_checks = []
        errors.append({"collector": "loopback_ports", "error_type": type(exc).__name__})

    try:
        residue_count = staging_residue_count(output_parent)
    except OSError as exc:
        residue_count = 0
        errors.append({"collector": "staging_residue", "error_type": type(exc).__name__})

    for index in range(policy["sample_count"]):
        try:
            samples.append(collect_resource_sample(output_parent))
        except (OSError, ValueError) as exc:
            errors.append({"collector": "resource_sample", "error_type": type(exc).__name__})
            break
        if index + 1 < policy["sample_count"]:
            time.sleep(policy["sampling_interval_ms"] / 1000)

    if samples:
        total_memory_mb = round(samples[0]["memory_total_mb"])
    else:
        total_memory_mb = 0
    environment = environment_summary(total_memory_mb)
    stable_environment = {
        "operating_system": environment["operating_system"],
        "python": environment["python"],
        "cpu_logical_count": environment["cpu_logical_count"],
        "memory_total_mb": environment["memory_total_mb"],
        "timezone_offset_minutes": environment["timezone_offset_minutes"],
        "proxy": environment["proxy"],
    }
    assessment = assess_preflight(
        policy=policy,
        samples=samples,
        port_checks=port_checks,
        residue_count=residue_count,
        collection_errors=errors,
        observer_start_rss_mb=observer_start_rss_mb,
    )
    snapshot_complete = not errors and len(samples) == policy["sample_count"]
    return {
        "schema_version": "0.1",
        "evidence_type": "runtime.preflight",
        "source": f"VeriTrail {COLLECTOR_VERSION}",
        "captured_at": started_at,
        "facts": {
            "collector_version": COLLECTOR_VERSION,
            "snapshot_complete": snapshot_complete,
            "decision": assessment["decision"],
            "decision_reasons": assessment["decision_reasons"],
            "policy": copy.deepcopy(policy),
            "environment": environment,
            "environment_fingerprint": sha256_json(stable_environment),
            "samples": samples,
            "sample_count_expected": policy["sample_count"],
            "sample_count_observed": len(samples),
            "max_consecutive_memory_hard_breaches": assessment[
                "max_consecutive_memory_hard_breaches"
            ],
            "port_checks": port_checks,
            "staging": {
                "clean_required": policy["require_clean_staging"],
                "residue_count": residue_count,
            },
            "observer_effect": assessment["observer_effect"],
            "collection_errors": errors,
            "collection_elapsed_ms": round((time.monotonic() - started_monotonic) * 1000, 3),
        },
        "observed_variables": _known_observed_variables(plan, environment),
        "metadata": {
            "network_scope": "loopback-only",
            "environment_values_redacted": True,
        },
    }
