from __future__ import annotations

import ctypes
import importlib.util
import os
import platform
import shutil
import socket
import sys
from pathlib import Path
from typing import Any

from veritrail import __version__ as core_version

from veritrail_starter.contract import normalize_answers
from veritrail_starter.errors import StarterError, incompatible, unsupported


def _version_tuple(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    try:
        numbers = tuple(int(item) for item in parts[:3])
    except ValueError as exc:
        raise incompatible("VeriTrail Core version is not parseable") from exc
    return (numbers + (0, 0, 0))[:3]


def require_compatible_core() -> None:
    if not (0, 12, 0) <= _version_tuple(core_version) < (0, 13, 0):
        raise incompatible("Starter 0.1 requires VeriTrail Core >=0.12,<0.13")


def supported_host() -> bool:
    if os.name != "nt" or not hasattr(sys, "getwindowsversion"):
        return False
    windows = sys.getwindowsversion()
    return windows.major == 10 and windows.build >= 22000


def require_supported_host() -> None:
    if not supported_host():
        raise unsupported("single-webapp 0.1 supports only Windows 11")


def _port_is_free(port: int) -> bool:
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        probe.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        probe.close()


def _chromium_present() -> bool:
    candidates: list[Path] = []
    configured = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if configured and configured != "0":
        candidates.append(Path(configured))
    elif configured == "0":
        spec = importlib.util.find_spec("playwright")
        if spec is not None and spec.origin:
            candidates.append(
                Path(spec.origin).parent / "driver" / "package" / ".local-browsers"
            )
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        candidates.append(Path(local_app_data) / "ms-playwright")
    for root in candidates:
        try:
            if root.is_dir() and any(root.glob("chromium-*")):
                return True
        except OSError:
            continue
    return False


def _available_memory_mb() -> int | None:
    if platform.system() != "Windows":
        return None

    class MemoryStatus(ctypes.Structure):
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

    status = MemoryStatus()
    status.length = ctypes.sizeof(MemoryStatus)
    try:
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return None
    except (AttributeError, OSError):
        return None
    return status.available_physical // (1024 * 1024)


def doctor_report(answers: dict[str, Any] | None) -> dict[str, Any]:
    require_compatible_core()
    checks: list[dict[str, Any]] = [
        {"id": "core-version", "status": "READY", "detail": "Core >=0.12,<0.13"},
        {
            "id": "host-platform",
            "status": "READY" if supported_host() else "UNSUPPORTED",
            "detail": "Windows 11 required",
        },
    ]
    if not supported_host():
        return {"status": "UNSUPPORTED", "checks": checks}
    if answers is None:
        checks.append(
            {"id": "explicit-answers", "status": "NEEDS_INPUT", "detail": "--answers is required for project checks"}
        )
        return {"status": "NEEDS_INPUT", "checks": checks}
    try:
        normalized = normalize_answers(answers)
    except StarterError as exc:
        status = "UNSUPPORTED" if exc.code == "UNSUPPORTED" else "NEEDS_INPUT"
        checks.append(
            {"id": "explicit-answers", "status": status, "detail": exc.messages[0]}
        )
        return {"status": status, "checks": checks}
    checks.append(
        {"id": "explicit-answers", "status": "READY", "detail": "explicit Answers 0.1 validated"}
    )

    port_ready = _port_is_free(normalized["application"]["port"])
    checks.append(
        {
            "id": "fixed-loopback-port",
            "status": "READY" if port_ready else "NEEDS_INPUT",
            "detail": "selected port is free" if port_ready else "selected port is occupied",
        }
    )
    playwright_ready = importlib.util.find_spec("playwright") is not None
    checks.append(
        {
            "id": "playwright-package",
            "status": "READY" if playwright_ready else "NEEDS_INPUT",
            "detail": "Playwright import is available" if playwright_ready else "Playwright is not installed",
        }
    )
    chromium_ready = playwright_ready and _chromium_present()
    checks.append(
        {
            "id": "chromium-runtime",
            "status": "READY" if chromium_ready else "NEEDS_INPUT",
            "detail": "Chromium cache is present" if chromium_ready else "Chromium cache was not confirmed",
        }
    )
    try:
        free_disk_mb = shutil.disk_usage(normalized["subject"]["root"]).free // (1024 * 1024)
    except OSError:
        free_disk_mb = 0
    disk_ready = free_disk_mb >= 1024
    checks.append(
        {
            "id": "disk-budget",
            "status": "READY" if disk_ready else "NEEDS_INPUT",
            "detail": "at least 1024 MiB free" if disk_ready else "less than 1024 MiB free",
        }
    )
    free_memory_mb = _available_memory_mb()
    memory_ready = free_memory_mb is not None and free_memory_mb >= 2048
    checks.append(
        {
            "id": "memory-budget",
            "status": "READY" if memory_ready else "NEEDS_INPUT",
            "detail": "at least 2048 MiB available" if memory_ready else "available memory was not confirmed above 2048 MiB",
        }
    )
    status = "READY" if all(item["status"] == "READY" for item in checks) else "NEEDS_INPUT"
    return {"status": status, "checks": checks}
