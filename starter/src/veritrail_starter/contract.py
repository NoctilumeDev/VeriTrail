from __future__ import annotations

import copy
import os
import re
import stat
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from veritrail.canonical import sha256_json
from veritrail.errors import ValidationError
from veritrail.plan import validate_plan
from veritrail.project_profile import (
    project_profile_digest,
    validate_project_profile,
)

from veritrail_starter.errors import StarterError, invalid, unsupported

IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
WINDOWS_RESERVED_SEGMENT = re.compile(
    r"(?i)^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$"
)
SECRET_KEY = re.compile(
    r"(?i)(?:^|[-_])(password|passwd|token|secret|api[-_]?key|authorization|cookie|credential|private[-_]?key)(?:$|[-_])"
)
SECRET_VALUE = re.compile(
    r"(?i)(?:Bearer\s+[A-Za-z0-9._~+/=-]+|github_pat_[A-Za-z0-9_]{20,}|gh[opsu]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
SHELL_EXECUTABLES = {
    "bash.exe",
    "cmd.exe",
    "cscript.exe",
    "mshta.exe",
    "powershell.exe",
    "pwsh.exe",
    "sh.exe",
    "wscript.exe",
    "wsl.exe",
}
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)

TOP_LEVEL_FIELDS = {
    "schema_version",
    "preset",
    "workspace_id",
    "question",
    "subject",
    "application",
    "browser",
    "budgets",
    "timeouts",
    "random_seed",
}
SUBJECT_FIELDS = {
    "root",
    "id",
    "version",
    "source_ref",
    "working_directory",
    "watch_roots",
}
APPLICATION_FIELDS = {
    "executable",
    "arguments",
    "port",
    "health_path",
    "expected_status",
}
BROWSER_FIELDS = {
    "start_url",
    "allowed_origin",
    "headless",
    "timeout_ms",
    "viewports",
    "steps",
    "screenshot_safety",
}
BUDGET_FIELDS = {
    "max_artifact_bytes",
    "max_watch_files",
    "max_watch_total_bytes",
    "lifecycle_timeout_ms",
    "max_stdout_bytes",
    "max_stderr_bytes",
    "max_processes",
    "application_memory_mb",
    "browser_memory_mb",
}
TIMEOUT_FIELDS = {
    "readiness_attempt_ms",
    "readiness_total_ms",
    "readiness_interval_ms",
    "shutdown_process_ms",
    "shutdown_port_ms",
    "shutdown_reader_ms",
}
VIEWPORT_FIELDS = {"name", "width", "height", "is_mobile"}
ARGUMENT_FIELDS = {"literal", "run_work_path", "node_port", "node_origin"}
STEP_FIELDS = {
    "click": {"id", "action", "selector"},
    "fill": {"id", "action", "selector", "value"},
    "press": {"id", "action", "selector", "value"},
    "expect_visible": {"id", "action", "selector"},
    "expect_text": {"id", "action", "selector", "value"},
}


def _reject_unknown(value: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise invalid(f"{label} has unsupported fields: {', '.join(unknown)}")


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise invalid(f"{label} must be an object")
    return value


def _require_int(value: Any, label: str, minimum: int, maximum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise invalid(f"{label} must be an integer from {minimum} to {maximum}")
    return value


def _require_identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise invalid(f"{label} must be a 2-64 character lowercase identifier")
    return value


def _is_reparse(path: Path) -> bool:
    metadata = os.lstat(path)
    return path.is_symlink() or bool(
        getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT
    )


def _ordinary_directory(path: Path, label: str) -> Path:
    try:
        if (
            (os.name == "nt" and (not path.drive or str(path).startswith(("\\\\", "//"))))
            or not path.exists()
            or not path.is_dir()
            or _is_reparse(path)
        ):
            raise OSError("unsafe directory")
        return path.resolve(strict=True)
    except OSError as exc:
        raise invalid(f"{label} must be an existing ordinary directory") from exc


def _ordinary_executable(path: Path) -> Path:
    try:
        if (
            (os.name == "nt" and (not path.drive or str(path).startswith(("\\\\", "//"))))
            or not path.is_absolute()
            or not path.exists()
            or not path.is_file()
            or _is_reparse(path)
            or path.suffix.casefold() != ".exe"
        ):
            raise OSError("unsafe executable")
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise invalid("application.executable must be an existing ordinary local .exe file") from exc
    if resolved.name.casefold() in SHELL_EXECUTABLES:
        raise unsupported("Shell and script-host executables are outside single-webapp 0.1")
    return resolved


def _safe_relative(value: Any, label: str, *, allow_root: bool) -> str:
    if value == "." and allow_root:
        return value
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or value.startswith("/")
        or re.match(r"^[A-Za-z]:", value)
    ):
        raise invalid(f"{label} must be a safe relative POSIX path")
    parts = value.split("/")
    if not 1 <= len(parts) <= 8 or any(
        part in {"", ".", ".."}
        or not SAFE_SEGMENT.fullmatch(part)
        or part.rstrip(". ") != part
        or WINDOWS_RESERVED_SEGMENT.fullmatch(part)
        for part in parts
    ):
        raise invalid(f"{label} must contain 1-8 safe path segments")
    return value


def _resolve_inside(root: Path, relative: str, label: str) -> None:
    current = root
    if relative != ".":
        for segment in relative.split("/"):
            current = current / segment
            try:
                if not current.exists() or not current.is_dir() or _is_reparse(current):
                    raise OSError("unsafe directory")
            except OSError as exc:
                raise invalid(f"{label} must resolve to an ordinary directory inside subject.root") from exc
    try:
        resolved = current.resolve(strict=True)
        if os.path.commonpath((str(root), str(resolved))) != str(root):
            raise ValueError("outside root")
    except (OSError, ValueError) as exc:
        raise invalid(f"{label} must remain inside subject.root") from exc


def _scan_for_secrets(value: Any, label: str = "answers") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if SECRET_KEY.search(str(key)):
                raise unsupported(f"{label} contains a secret-bearing field")
            _scan_for_secrets(item, f"{label}.{key}")
    elif isinstance(value, list):
        for item in value:
            _scan_for_secrets(item, label)
    elif isinstance(value, str) and SECRET_VALUE.search(value):
        raise unsupported(f"{label} contains secret-like content")


def _loopback_origin(value: Any, label: str) -> tuple[str, str]:
    if not isinstance(value, str) or not value:
        raise invalid(f"{label} must be a loopback HTTP URL with an explicit port")
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise invalid(f"{label} must be a valid loopback HTTP URL") from exc
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or port is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise unsupported(f"{label} must use explicit IPv4 loopback HTTP without credentials, query, or fragment")
    return f"http://127.0.0.1:{port}", parsed.path or "/"


def _normalize_arguments(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not 1 <= len(value) <= 128:
        raise invalid("application.arguments must contain 1-128 structured arguments")
    result: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        obj = _require_object(item, f"application.arguments[{index}]")
        _reject_unknown(obj, ARGUMENT_FIELDS, f"application.arguments[{index}]")
        if len(obj) != 1:
            raise invalid(f"application.arguments[{index}] must have exactly one typed field")
        field, argument_value = next(iter(obj.items()))
        if field == "literal":
            if (
                not isinstance(argument_value, str)
                or len(argument_value) > 4096
                or any(ord(character) < 32 or ord(character) == 127 for character in argument_value)
            ):
                raise invalid(
                    f"application.arguments[{index}].literal must be a control-free string up to 4096 characters"
                )
        elif field == "run_work_path":
            if not isinstance(argument_value, list) or not 1 <= len(argument_value) <= 8:
                raise invalid(
                    f"application.arguments[{index}].run_work_path must contain 1-8 safe path segments"
                )
            for segment in argument_value:
                if (
                    not isinstance(segment, str)
                    or not SAFE_SEGMENT.fullmatch(segment)
                    or segment.rstrip(". ") != segment
                    or WINDOWS_RESERVED_SEGMENT.fullmatch(segment)
                ):
                    raise invalid(
                        f"application.arguments[{index}].run_work_path must contain safe path segments"
                    )
        elif _require_identifier(
            argument_value, f"application.arguments[{index}].{field}"
        ) != "application":
            raise unsupported(
                f"application.arguments[{index}].{field} may reference only the single application node"
            )
        result.append(copy.deepcopy(obj))
    return result


def _normalize_viewports(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) != 2:
        raise invalid("browser.viewports must contain exactly desktop and mobile entries")
    result: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, item in enumerate(value):
        obj = _require_object(item, f"browser.viewports[{index}]")
        _reject_unknown(obj, VIEWPORT_FIELDS, f"browser.viewports[{index}]")
        name = _require_identifier(obj.get("name"), f"browser.viewports[{index}].name")
        if name in names:
            raise invalid("browser viewport names must be unique")
        names.add(name)
        result.append(
            {
                "name": name,
                "width": _require_int(obj.get("width"), f"browser.viewports[{index}].width", 240, 3840),
                "height": _require_int(obj.get("height"), f"browser.viewports[{index}].height", 240, 2160),
                "is_mobile": obj.get("is_mobile"),
            }
        )
        if not isinstance(obj.get("is_mobile"), bool):
            raise invalid(f"browser.viewports[{index}].is_mobile must be a boolean")
    by_name = {item["name"]: item for item in result}
    if set(by_name) != {"desktop", "mobile"}:
        raise invalid("browser.viewports must be named desktop and mobile")
    if by_name["desktop"]["is_mobile"] or not by_name["mobile"]["is_mobile"]:
        raise invalid("desktop must be non-mobile and mobile must be mobile")
    return result


def _normalize_steps(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not 1 <= len(value) <= 49:
        raise invalid("browser.steps must contain 1-49 explicit business steps")
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    decisive = 0
    for index, item in enumerate(value):
        obj = _require_object(item, f"browser.steps[{index}]")
        action = obj.get("action")
        allowed = STEP_FIELDS.get(action)
        if allowed is None:
            raise invalid(f"browser.steps[{index}].action is unsupported by Starter 0.1")
        _reject_unknown(obj, allowed, f"browser.steps[{index}]")
        step_id = _require_identifier(obj.get("id"), f"browser.steps[{index}].id")
        if step_id in ids:
            raise invalid("browser step ids must be unique")
        ids.add(step_id)
        if action in {"expect_visible", "expect_text"}:
            decisive += 1
        selector = obj.get("selector")
        if not isinstance(selector, str) or not selector or len(selector) > 512:
            raise invalid(f"browser.steps[{index}].selector must be a non-empty string up to 512 characters")
        if "value" in allowed:
            step_value = obj.get("value")
            if not isinstance(step_value, str) or len(step_value) > 4096:
                raise invalid(f"browser.steps[{index}].value must be a string up to 4096 characters")
        result.append(copy.deepcopy(obj))
    if decisive < 1:
        raise unsupported("single-webapp requires at least one explicit expect_visible or expect_text business check")
    return result


def normalize_answers(document: dict[str, Any], *, inspect_paths: bool = True) -> dict[str, Any]:
    _reject_unknown(document, TOP_LEVEL_FIELDS, "Answers")
    if document.get("schema_version") != "0.1":
        raise invalid("Answers.schema_version must be '0.1'")
    if document.get("preset") != "single-webapp":
        raise unsupported("Starter 0.1 supports only the single-webapp preset")
    workspace_id = _require_identifier(document.get("workspace_id"), "workspace_id")
    question = document.get("question")
    if not isinstance(question, str) or not question.strip() or len(question) > 512:
        raise invalid("question must be a non-empty string up to 512 characters")
    _scan_for_secrets(document)

    subject = _require_object(document.get("subject"), "subject")
    _reject_unknown(subject, SUBJECT_FIELDS, "subject")
    root_raw = subject.get("root")
    if not isinstance(root_raw, str) or not Path(root_raw).is_absolute():
        raise invalid("subject.root must be an explicit absolute local path")
    root = _ordinary_directory(Path(root_raw), "subject.root") if inspect_paths else Path(root_raw)
    working = _safe_relative(subject.get("working_directory"), "subject.working_directory", allow_root=True)
    watch_value = subject.get("watch_roots")
    if not isinstance(watch_value, list) or not 1 <= len(watch_value) <= 8:
        raise invalid("subject.watch_roots must contain 1-8 paths")
    watch_roots = [
        _safe_relative(item, f"subject.watch_roots[{index}]", allow_root=True)
        for index, item in enumerate(watch_value)
    ]
    normalized_watch = [tuple() if item == "." else tuple(item.casefold().split("/")) for item in watch_roots]
    for index, current in enumerate(normalized_watch):
        for previous in normalized_watch[:index]:
            shorter, longer = sorted((current, previous), key=len)
            if longer[: len(shorter)] == shorter:
                raise invalid("subject.watch_roots must be unique and non-overlapping")
    if inspect_paths:
        _resolve_inside(root, working, "subject.working_directory")
        for index, item in enumerate(watch_roots):
            _resolve_inside(root, item, f"subject.watch_roots[{index}]")

    application = _require_object(document.get("application"), "application")
    _reject_unknown(application, APPLICATION_FIELDS, "application")
    executable_raw = application.get("executable")
    if not isinstance(executable_raw, str):
        raise invalid("application.executable must be an absolute local .exe path")
    executable = _ordinary_executable(Path(executable_raw)) if inspect_paths else Path(executable_raw)
    arguments = _normalize_arguments(application.get("arguments"))
    port = _require_int(application.get("port"), "application.port", 1024, 65535)
    health_path = application.get("health_path")
    try:
        parsed_health = urlsplit(health_path) if isinstance(health_path, str) else None
    except ValueError as exc:
        raise invalid(
            "application.health_path must be an absolute URL path without query or fragment"
        ) from exc
    if (
        parsed_health is None
        or not health_path.startswith("/")
        or health_path.startswith("//")
        or len(health_path) > 1024
        or parsed_health.scheme
        or parsed_health.netloc
        or parsed_health.query
        or parsed_health.fragment
    ):
        raise invalid("application.health_path must be an absolute URL path without query or fragment")
    if application.get("expected_status") != 200:
        raise invalid("application.expected_status must be 200")

    browser = _require_object(document.get("browser"), "browser")
    _reject_unknown(browser, BROWSER_FIELDS, "browser")
    start_origin, _ = _loopback_origin(browser.get("start_url"), "browser.start_url")
    allowed_origin, allowed_path = _loopback_origin(browser.get("allowed_origin"), "browser.allowed_origin")
    if allowed_path != "/" or start_origin != allowed_origin or urlsplit(start_origin).port != port:
        raise unsupported("browser URLs must use the application IPv4 loopback origin and port")
    if not isinstance(browser.get("headless"), bool):
        raise invalid("browser.headless must be a boolean")
    if browser.get("screenshot_safety") != "UNREDACTED_OPERATOR_ACKNOWLEDGED":
        raise unsupported("browser screenshot safety must be explicitly acknowledged")
    viewports = _normalize_viewports(browser.get("viewports"))
    steps = _normalize_steps(browser.get("steps"))

    budgets = _require_object(document.get("budgets"), "budgets")
    _reject_unknown(budgets, BUDGET_FIELDS, "budgets")
    budget_ranges = {
        "max_artifact_bytes": (1, 64 * 1024 * 1024),
        "max_watch_files": (1, 100_000),
        "max_watch_total_bytes": (1, 2_147_483_648),
        "lifecycle_timeout_ms": (1000, 600_000),
        "max_stdout_bytes": (1, 1_048_576),
        "max_stderr_bytes": (1, 1_048_576),
        "max_processes": (1, 32),
        "application_memory_mb": (64, 2048),
        "browser_memory_mb": (128, 2048),
    }
    normalized_budgets = {
        key: _require_int(budgets.get(key), f"budgets.{key}", *limits)
        for key, limits in budget_ranges.items()
    }

    timeouts = _require_object(document.get("timeouts"), "timeouts")
    _reject_unknown(timeouts, TIMEOUT_FIELDS, "timeouts")
    timeout_ranges = {
        "readiness_attempt_ms": (100, 2000),
        "readiness_total_ms": (500, 30_000),
        "readiness_interval_ms": (20, 1000),
        "shutdown_process_ms": (100, 10_000),
        "shutdown_port_ms": (100, 10_000),
        "shutdown_reader_ms": (100, 10_000),
    }
    normalized_timeouts = {
        key: _require_int(timeouts.get(key), f"timeouts.{key}", *limits)
        for key, limits in timeout_ranges.items()
    }
    if normalized_timeouts["readiness_total_ms"] <= normalized_timeouts["readiness_attempt_ms"]:
        raise invalid("timeouts.readiness_total_ms must exceed readiness_attempt_ms")

    source_ref = _safe_relative(subject.get("source_ref"), "subject.source_ref", allow_root=True)
    normalized = {
        "schema_version": "0.1",
        "preset": "single-webapp",
        "workspace_id": workspace_id,
        "question": question.strip(),
        "subject": {
            "root": str(root),
            "id": _require_identifier(subject.get("id"), "subject.id"),
            "version": str(subject.get("version", "")).strip(),
            "source_ref": source_ref,
            "working_directory": working,
            "watch_roots": watch_roots,
        },
        "application": {
            "executable": str(executable),
            "arguments": arguments,
            "port": port,
            "health_path": health_path,
            "expected_status": 200,
        },
        "browser": {
            "start_url": browser["start_url"],
            "allowed_origin": browser["allowed_origin"],
            "headless": browser["headless"],
            "timeout_ms": _require_int(browser.get("timeout_ms"), "browser.timeout_ms", 1000, 30_000),
            "viewports": viewports,
            "steps": steps,
            "screenshot_safety": browser["screenshot_safety"],
        },
        "budgets": normalized_budgets,
        "timeouts": normalized_timeouts,
        "random_seed": _require_int(document.get("random_seed"), "random_seed", 0, 2_147_483_647),
    }
    if not normalized["subject"]["version"]:
        raise invalid("subject.version must be a non-empty string")
    return normalized


def _tool_binding_id(executable: str) -> str:
    name = Path(executable).stem.casefold()
    if "python" in name:
        return "python-application"
    if name in {"node", "nodejs"}:
        return "node-application"
    return "application-tool"


def _derived_identifier(base: str, suffix: str) -> str:
    candidate = f"{base}-{suffix}"
    if len(candidate) <= 64:
        return candidate
    digest = sha256_json({"base": base, "suffix": suffix})[:8]
    prefix_length = 64 - len(suffix) - len(digest) - 2
    return f"{base[:prefix_length]}-{digest}-{suffix}"


def build_profile(answers: dict[str, Any]) -> dict[str, Any]:
    subject = answers["subject"]
    application = answers["application"]
    budgets = answers["budgets"]
    timeouts = answers["timeouts"]
    profile = {
        "schema_version": "0.2",
        "topology": "SINGLE_APPLICATION",
        "profile_id": _derived_identifier(answers["workspace_id"], "profile"),
        "version": 1,
        "platform": "WINDOWS_11",
        "cold_state": "C1_PROCESS_COLD",
        "nodes": [
            {
                "node_id": "application",
                "role": "APPLICATION",
                "adapter": "TRUSTED_PROCESS_SERVICE",
                "depends_on": [],
                "tool_binding": _tool_binding_id(application["executable"]),
                "arguments": copy.deepcopy(application["arguments"]),
                "working_directory": subject["working_directory"],
                "environment": {
                    "inherit": ["SYSTEMROOT", "WINDIR"],
                    "set": {"PYTHONDONTWRITEBYTECODE": "1"},
                },
                "port": application["port"],
                "readiness": {
                    "adapter": "HTTP_GET_LOOPBACK_OWNED_PID",
                    "path": application["health_path"],
                    "expected_status": 200,
                    "attempt_timeout_ms": timeouts["readiness_attempt_ms"],
                    "total_timeout_ms": timeouts["readiness_total_ms"],
                    "interval_ms": timeouts["readiness_interval_ms"],
                    "consecutive_successes": 2,
                    "max_response_bytes": 4096,
                },
                "limits": {
                    "max_stdout_bytes": budgets["max_stdout_bytes"],
                    "max_stderr_bytes": budgets["max_stderr_bytes"],
                    "max_processes": budgets["max_processes"],
                    "max_job_memory_mb": budgets["application_memory_mb"],
                },
                "shutdown": {
                    "adapter": "JOB_TERMINATE_AFTER_CAPTURE",
                    "process_release_timeout_ms": timeouts["shutdown_process_ms"],
                    "port_release_timeout_ms": timeouts["shutdown_port_ms"],
                    "reader_shutdown_timeout_ms": timeouts["shutdown_reader_ms"],
                },
            }
        ],
        "start_order": ["application"],
        "teardown_order": ["application"],
        "application_node_id": "application",
        "subject_watch_roots": copy.deepcopy(subject["watch_roots"]),
        "max_watch_files": budgets["max_watch_files"],
        "max_watch_total_bytes": budgets["max_watch_total_bytes"],
        "lifecycle_timeout_ms": budgets["lifecycle_timeout_ms"],
    }
    validate_project_profile(profile)
    return profile


def _assertions(viewport_count: int) -> list[dict[str, Any]]:
    rows = [
        ("starter-preflight-snapshot-complete", "runtime.preflight", "/facts/snapshot_complete", True),
        ("starter-bootstrap-service-ready", "runtime.bootstrap", "/facts/services_ready", True),
        ("starter-bootstrap-order", "runtime.bootstrap", "/facts/cleanup/reverse_order_complete", True),
        ("starter-browser-capture-complete", "browser.session", "/facts/capture_complete", True),
        ("starter-browser-business-steps-passed", "browser.session", "/facts/all_steps_passed", True),
        ("starter-browser-console-clean", "browser.session", "/facts/unexpected_console_error_count", 0),
        ("starter-browser-page-clean", "browser.session", "/facts/page_error_count", 0),
        ("starter-browser-request-clean", "browser.session", "/facts/failed_request_count", 0),
        ("starter-browser-http-clean", "browser.session", "/facts/unexpected_http_error_count", 0),
        ("starter-browser-write-clean", "browser.session", "/facts/duplicate_write_request_group_count", 0),
        ("starter-browser-overflow-clean", "browser.session", "/facts/horizontal_overflow_viewport_count", 0),
        ("starter-browser-viewport-coverage", "browser.session", "/facts/viewport_count", viewport_count),
        ("starter-browser-screenshot-coverage", "browser.session", "/facts/screenshot_count", viewport_count),
        ("starter-browser-cleanup-complete", "browser.session", "/facts/cleanup_complete", True),
        ("starter-bootstrap-cleanup-complete", "runtime.bootstrap", "/facts/cleanup_complete", True),
        ("starter-subject-unchanged", "runtime.bootstrap", "/facts/subject_observation/changed", False),
    ]
    return [
        {
            "id": identifier,
            "severity": "HARD",
            "evidence_type": evidence,
            "path": path,
            "operator": "eq",
            "expected": expected,
        }
        for identifier, evidence, path, expected in rows
    ]


def build_plan(answers: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    digest = project_profile_digest(profile)
    sealed_for_validation = copy.deepcopy(profile)
    sealed_for_validation["seal"] = {"algorithm": "sha256", "digest": digest}
    browser = answers["browser"]
    assertions = _assertions(len(browser["viewports"]))
    baseline_fingerprint = sha256_json(
        {
            "preset": "single-webapp",
            "preset_version": "0.1",
            "assertions": assertions,
        }
    )
    plan = {
        "schema_version": "0.7",
        "plan_id": _derived_identifier(answers["workspace_id"], "plan"),
        "version": 1,
        "subject": {
            "id": answers["subject"]["id"],
            "version": answers["subject"]["version"],
            "source_ref": answers["subject"]["source_ref"],
        },
        "question": answers["question"],
        "baseline": {
            "id": "starter-single-webapp-0.1",
            "status": "VALID",
            "fingerprint": baseline_fingerprint,
            "tolerances": {
                "viewport_count": len(browser["viewports"]),
                "unexpected_browser_errors": 0,
                "cleanup_failures": 0,
            },
        },
        "experiment_type": "SINGLE_VARIABLE",
        "variables": [
            {
                "name": "project_bootstrap_topology",
                "role": "PRIMARY",
                "value": "veritrail_managed_windows_c1_single_application",
                "source": "sealed-plan",
            },
            {
                "name": "browser_engine",
                "role": "CONTROLLED",
                "value": "chromium",
                "source": "browser-adapter",
            },
            {
                "name": "browser_headless",
                "role": "CONTROLLED",
                "value": browser["headless"],
                "source": "sealed-plan",
            },
            {
                "name": "viewport_profile_count",
                "role": "CONTROLLED",
                "value": len(browser["viewports"]),
                "unit": "profiles",
                "source": "sealed-plan",
            },
        ],
        "required_evidence": ["runtime.preflight", "runtime.bootstrap", "browser.session"],
        "assertions": assertions,
        "random_seed": answers["random_seed"],
        "resource_budget": {"max_artifact_bytes": answers["budgets"]["max_artifact_bytes"]},
        "preflight": {
            "sample_count": 3,
            "sampling_interval_ms": 50,
            "hard_breach_grace_samples": 2,
            "available_memory_soft_min_mb": 4096,
            "available_memory_hard_min_mb": 2048,
            "disk_free_hard_min_mb": 1024,
            "collector_rss_hard_max_mb": 256,
            "observer_rss_delta_soft_max_mb": 64,
            "ports": [{"port": answers["application"]["port"], "expected": "FREE"}],
            "require_clean_staging": True,
        },
        "browser": {
            "engine": "chromium",
            "headless": browser["headless"],
            "start_url": browser["start_url"],
            "allowed_origins": [browser["allowed_origin"]],
            "timeout_ms": browser["timeout_ms"],
            "viewports": copy.deepcopy(browser["viewports"]),
            "steps": copy.deepcopy(browser["steps"])
            + [{"id": "starter-final-screenshot", "action": "screenshot", "name": "starter-final"}],
            "screenshot_safety": browser["screenshot_safety"],
            "max_job_memory_mb": answers["budgets"]["browser_memory_mb"],
        },
        "bootstrap_profile": {
            "profile_id": profile["profile_id"],
            "profile_version": profile["version"],
            "profile_sha256": digest,
        },
        "load_model": {"virtual_users": 1, "in_flight_requests": 1},
        "change_scope": {
            "level": "L3_SYSTEM",
            "owner": "VeriTrail Starter / single-webapp operator-confirmed draft",
            "expected_blast_radius": "One managed application, browser evidence, cleanup evidence, Bundle and read-only analyses",
            "consumers": [
                "project-profile-validator",
                "plan-validator",
                "bootstrap-preview",
                "bootstrap-lifecycle",
                "browser-adapter",
                "artifact-store",
                "verdict-engine",
                "catalog",
                "workbench",
            ],
        },
        "reproduction_steps": [
            "Review every Starter answer and generated DRAFT before sealing.",
            "Seal ProjectProfile 0.2 and verify the prospective digest.",
            "Seal ExperimentPlan 0.7 against that sealed ProjectProfile.",
            "Approve the exact BootstrapPreview digest before a bounded Windows 11 C1 Run.",
        ],
        "cleanup_steps": [
            "Close Playwright contexts and Chromium.",
            "Terminate the owned application Job and release stream readers.",
            "Verify the fixed loopback port, run-work and staging are released before another Run.",
        ],
    }
    try:
        validate_plan(plan, sealed_for_validation)
    except ValidationError as exc:
        raise StarterError(
            "CORE_INCOMPATIBLE",
            [f"generated Plan was rejected by Core: {message}" for message in exc.errors],
            exit_code=5,
        ) from exc
    if "seal" in profile or "seal" in plan:
        raise RuntimeError("Starter invariant violated: persisted drafts must be unsealed")
    return plan


def build_documents(answers: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    profile = build_profile(answers)
    plan = build_plan(answers, profile)
    bindings = {
        "schema_version": "0.1",
        "bindings": {
            profile["nodes"][0]["tool_binding"]: {
                "executable": answers["application"]["executable"]
            }
        },
    }
    return profile, plan, bindings
