from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qsl, urlsplit

from veritrail.canonical import canonical_json_bytes, sha256_bytes
from veritrail.errors import ValidationError
from veritrail.jsonio import load_json_object
from veritrail.privacy import redact_string, redact_value

EVIDENCE_TYPE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
ATTACHMENT_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,127}$")


@dataclass(frozen=True)
class ImportedEvidence:
    document: dict[str, Any]
    sha256: str
    size: int
    redacted_fields: int
    input_name: str
    attachments: tuple["EvidenceAttachment", ...] = ()


@dataclass(frozen=True)
class EvidenceAttachment:
    path: str
    content: bytes
    sha256: str
    size: int
    media_type: str
    logical_name: str


def _create_attachment(
    *,
    path: str,
    content: bytes,
    media_type: str,
    logical_name: str,
    suffix: str,
) -> EvidenceAttachment:
    _validate_attachment_path(path, suffix=suffix)
    if not isinstance(content, bytes):
        raise ValidationError(["evidence attachment content must be bytes"])
    if not isinstance(logical_name, str) or not ATTACHMENT_NAME_PATTERN.fullmatch(logical_name):
        raise ValidationError(
            ["evidence attachment logical_name must be a 2-128 character lowercase identifier"]
        )
    return EvidenceAttachment(
        path=path,
        content=content,
        sha256=sha256_bytes(content),
        size=len(content),
        media_type=media_type,
        logical_name=logical_name,
    )


def create_attachment(
    *, path: str, content: bytes, media_type: str, logical_name: str
) -> EvidenceAttachment:
    if media_type != "image/png":
        raise ValidationError(["M2 evidence attachments must use image/png"])
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValidationError(["image/png evidence attachment is missing the PNG signature"])
    return _create_attachment(
        path=path,
        content=content,
        media_type=media_type,
        logical_name=logical_name,
        suffix=".png",
    )


def create_text_attachment(
    *, path: str, content: bytes, logical_name: str
) -> EvidenceAttachment:
    try:
        content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValidationError(["text evidence attachment must contain valid UTF-8"]) from exc
    return _create_attachment(
        path=path,
        content=content,
        media_type="text/plain; charset=utf-8",
        logical_name=logical_name,
        suffix=".txt",
    )


def _validate_attachment_path(value: str, *, suffix: str | None = None) -> None:
    if not isinstance(value, str) or "\\" in value:
        raise ValidationError(["evidence attachment path must use a relative POSIX path"])
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or path.parts[0] != "attachments"
        or any(part in {"", ".", ".."} for part in path.parts)
        or (suffix is not None and path.suffix.lower() != suffix)
    ):
        ending = f" and end in {suffix}" if suffix is not None else ""
        raise ValidationError(
            [f"evidence attachment path must stay under attachments/{ending}"]
        )


def _validate_timestamp(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _browser_url_is_sanitized(value: Any, *, origin_only: bool = False) -> bool:
    if value == "[BLOCKED_NON_LOOPBACK_URL]":
        return not origin_only
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return False
    if (
        parsed.scheme != "http"
        or parsed.hostname != "localhost"
        or port is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
    ):
        return False
    if origin_only:
        return parsed.path in {"", "/"} and not parsed.query
    return all(item == "[REDACTED]" for _, item in parse_qsl(parsed.query, keep_blank_values=True))


def _validate_exact_items(
    items: Any,
    required: set[str],
    path: str,
    errors: list[str],
) -> None:
    if not isinstance(items, list):
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{path}[{index}] must be an object")
        elif set(item) != required:
            errors.append(f"{path}[{index}] must contain the exact supported fields")


def _validate_preflight_evidence(
    document: dict[str, Any], input_name: str, errors: list[str]
) -> None:
    facts = document.get("facts")
    if not isinstance(facts, dict):
        return
    required = {
        "collector_version",
        "snapshot_complete",
        "decision",
        "decision_reasons",
        "policy",
        "environment",
        "environment_fingerprint",
        "samples",
        "sample_count_expected",
        "sample_count_observed",
        "max_consecutive_memory_hard_breaches",
        "port_checks",
        "staging",
        "observer_effect",
        "collection_errors",
        "collection_elapsed_ms",
    }
    missing = sorted(required - set(facts))
    unknown = sorted(set(facts) - required)
    if missing:
        errors.append(f"{input_name}.facts is missing preflight fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{input_name}.facts has unsupported preflight fields: {', '.join(unknown)}")
    if not isinstance(facts.get("collector_version"), str) or not facts.get("collector_version", "").strip():
        errors.append(f"{input_name}.facts.collector_version must be a non-empty string")
    if not isinstance(facts.get("snapshot_complete"), bool):
        errors.append(f"{input_name}.facts.snapshot_complete must be a boolean")
    if facts.get("decision") not in {"PROCEED", "STOP_ESCALATION", "ABORT"}:
        errors.append(f"{input_name}.facts.decision is unsupported")
    for field in (
        "decision_reasons",
        "samples",
        "port_checks",
        "collection_errors",
    ):
        if not isinstance(facts.get(field), list):
            errors.append(f"{input_name}.facts.{field} must be a list")
    for field in ("policy", "environment", "staging", "observer_effect"):
        if not isinstance(facts.get(field), dict):
            errors.append(f"{input_name}.facts.{field} must be an object")
    fingerprint = facts.get("environment_fingerprint")
    if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
        errors.append(f"{input_name}.facts.environment_fingerprint must be a SHA-256 digest")
    errors_list = facts.get("collection_errors")
    samples = facts.get("samples")
    expected_count = facts.get("sample_count_expected")
    observed_count = facts.get("sample_count_observed")
    hard_streak = facts.get("max_consecutive_memory_hard_breaches")
    for field, value in (
        ("sample_count_expected", expected_count),
        ("sample_count_observed", observed_count),
        ("max_consecutive_memory_hard_breaches", hard_streak),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{input_name}.facts.{field} must be a non-negative integer")
    if isinstance(samples, list) and isinstance(observed_count, int) and observed_count != len(samples):
        errors.append(f"{input_name}.facts.sample_count_observed must equal the samples length")
    if (
        facts.get("snapshot_complete") is True
        and isinstance(expected_count, int)
        and isinstance(observed_count, int)
        and expected_count != observed_count
    ):
        errors.append(f"{input_name} cannot mark a partial sample set as complete")
    elapsed = facts.get("collection_elapsed_ms")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
        errors.append(f"{input_name}.facts.collection_elapsed_ms must be a non-negative number")
    if facts.get("snapshot_complete") is False and facts.get("decision") != "ABORT":
        errors.append(f"{input_name} must ABORT when the preflight snapshot is incomplete")
    if isinstance(errors_list, list) and errors_list and facts.get("decision") != "ABORT":
        errors.append(f"{input_name} must ABORT when collection_errors is non-empty")
    if facts.get("snapshot_complete") is True and isinstance(errors_list, list) and errors_list:
        errors.append(f"{input_name} cannot be complete when collection_errors is non-empty")


def _validate_browser_evidence(
    document: dict[str, Any], input_name: str, errors: list[str]
) -> None:
    facts = document.get("facts")
    if not isinstance(facts, dict):
        return
    required = {
        "collector_version",
        "policy_sha256",
        "playwright_version",
        "browser_engine",
        "browser_version",
        "headless",
        "start_url",
        "allowed_origins",
        "started_at",
        "ended_at",
        "capture_complete",
        "all_steps_passed",
        "cleanup_complete",
        "viewport_runs",
        "viewport_count",
        "steps",
        "console",
        "page_errors",
        "network",
        "screenshots",
        "screenshot_count",
        "unexpected_console_error_count",
        "page_error_count",
        "failed_request_count",
        "unexpected_http_error_count",
        "duplicate_write_request_groups",
        "duplicate_write_request_group_count",
        "horizontal_overflow_viewport_count",
        "collection_errors",
    }
    missing = sorted(required - set(facts))
    unknown = sorted(set(facts) - required)
    if missing:
        errors.append(f"{input_name}.facts is missing browser fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{input_name}.facts has unsupported browser fields: {', '.join(unknown)}")
    for field in ("collector_version", "playwright_version", "browser_version", "start_url"):
        if not isinstance(facts.get(field), str) or not facts.get(field, "").strip():
            errors.append(f"{input_name}.facts.{field} must be a non-empty string")
    if facts.get("browser_engine") != "chromium":
        errors.append(f"{input_name}.facts.browser_engine must be chromium")
    policy_digest = facts.get("policy_sha256")
    if not isinstance(policy_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", policy_digest):
        errors.append(f"{input_name}.facts.policy_sha256 must be a SHA-256 digest")
    for field in ("headless", "capture_complete", "all_steps_passed", "cleanup_complete"):
        if not isinstance(facts.get(field), bool):
            errors.append(f"{input_name}.facts.{field} must be a boolean")
    for field in ("started_at", "ended_at"):
        if not _validate_timestamp(facts.get(field)):
            errors.append(f"{input_name}.facts.{field} must be an ISO-8601 timestamp with timezone")
    for field in (
        "allowed_origins",
        "viewport_runs",
        "steps",
        "console",
        "page_errors",
        "network",
        "screenshots",
        "duplicate_write_request_groups",
        "collection_errors",
    ):
        if not isinstance(facts.get(field), list):
            errors.append(f"{input_name}.facts.{field} must be a list")
    exact_lists = {
        "viewport_runs": {
            "name",
            "width",
            "height",
            "is_mobile",
            "started_at",
            "ended_at",
            "status",
            "horizontal_overflow_px",
            "step_count",
            "network_request_count",
        },
        "steps": {
            "viewport",
            "step_id",
            "action",
            "started_at",
            "ended_at",
            "elapsed_ms",
            "status",
            "error_type",
            "error",
        },
        "console": {"captured_at", "viewport", "level", "text"},
        "page_errors": {"captured_at", "viewport", "error_type", "message"},
        "network": {
            "sequence",
            "captured_at",
            "viewport",
            "method",
            "url",
            "resource_type",
            "status",
            "finished",
            "failure",
            "redirected_from",
        },
        "duplicate_write_request_groups": {"viewport", "method", "url", "count"},
        "collection_errors": {"collector", "error_type"},
    }
    for field, item_fields in exact_lists.items():
        _validate_exact_items(
            facts.get(field), item_fields, f"{input_name}.facts.{field}", errors
        )
    origins = facts.get("allowed_origins")
    if isinstance(origins, list) and any(
        not _browser_url_is_sanitized(origin, origin_only=True) for origin in origins
    ):
        errors.append(f"{input_name}.facts.allowed_origins must contain sanitized loopback origins")
    if not _browser_url_is_sanitized(facts.get("start_url")):
        errors.append(f"{input_name}.facts.start_url must be a sanitized loopback URL")
    network = facts.get("network")
    if isinstance(network, list):
        for index, item in enumerate(network):
            if not isinstance(item, dict):
                continue
            if not _browser_url_is_sanitized(item.get("url")):
                errors.append(f"{input_name}.facts.network[{index}].url is not sanitized")
            redirected = item.get("redirected_from")
            if redirected is not None and not _browser_url_is_sanitized(redirected):
                errors.append(
                    f"{input_name}.facts.network[{index}].redirected_from is not sanitized"
                )
            status = item.get("status")
            if status is not None and (
                not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599
            ):
                errors.append(f"{input_name}.facts.network[{index}].status is invalid")
            if not isinstance(item.get("finished"), bool):
                errors.append(f"{input_name}.facts.network[{index}].finished must be a boolean")
    count_fields = {
        "unexpected_console_error_count": "console",
        "page_error_count": "page_errors",
        "failed_request_count": None,
        "unexpected_http_error_count": None,
        "duplicate_write_request_group_count": "duplicate_write_request_groups",
        "horizontal_overflow_viewport_count": None,
        "viewport_count": "viewport_runs",
        "screenshot_count": "screenshots",
    }
    for field, source in count_fields.items():
        value = facts.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{input_name}.facts.{field} must be a non-negative integer")
        elif source is not None and isinstance(facts.get(source), list):
            if field == "unexpected_console_error_count":
                expected = sum(
                    1
                    for item in facts[source]
                    if isinstance(item, dict) and item.get("level") in {"error", "assert"}
                )
            else:
                expected = len(facts[source])
            if value != expected:
                errors.append(f"{input_name}.facts.{field} does not match {source}")
    if isinstance(network, list):
        derived_counts = {
            "failed_request_count": sum(
                1 for item in network if isinstance(item, dict) and item.get("failure") is not None
            ),
            "unexpected_http_error_count": sum(
                1
                for item in network
                if isinstance(item, dict)
                and isinstance(item.get("status"), int)
                and item["status"] >= 400
            ),
        }
        for field, expected in derived_counts.items():
            if facts.get(field) != expected:
                errors.append(f"{input_name}.facts.{field} does not match network")
    viewport_runs = facts.get("viewport_runs")
    if isinstance(viewport_runs, list):
        overflow_count = sum(
            1
            for item in viewport_runs
            if isinstance(item, dict)
            and isinstance(item.get("horizontal_overflow_px"), int)
            and item["horizontal_overflow_px"] > 0
        )
        if facts.get("horizontal_overflow_viewport_count") != overflow_count:
            errors.append(
                f"{input_name}.facts.horizontal_overflow_viewport_count does not match viewport_runs"
            )
    screenshots = facts.get("screenshots")
    if isinstance(screenshots, list):
        seen_paths: set[str] = set()
        for index, screenshot in enumerate(screenshots):
            prefix = f"{input_name}.facts.screenshots[{index}]"
            if not isinstance(screenshot, dict):
                errors.append(f"{prefix} must be an object")
                continue
            required_screenshot = {"name", "viewport", "step_id", "path", "sha256", "size", "media_type"}
            if set(screenshot) != required_screenshot:
                errors.append(f"{prefix} must contain the exact screenshot fields")
                continue
            try:
                _validate_attachment_path(screenshot.get("path"))
            except ValidationError as exc:
                errors.extend(f"{prefix}: {message}" for message in exc.errors)
            path = screenshot.get("path")
            if path in seen_paths:
                errors.append(f"{prefix}.path duplicates {path!r}")
            elif isinstance(path, str):
                seen_paths.add(path)
            digest = screenshot.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"{prefix}.sha256 must be a SHA-256 digest")
            size = screenshot.get("size")
            if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
                errors.append(f"{prefix}.size must be a positive integer")
            if screenshot.get("media_type") != "image/png":
                errors.append(f"{prefix}.media_type must be image/png")
    if facts.get("capture_complete") is True and (
        facts.get("all_steps_passed") is not True or facts.get("collection_errors")
    ):
        errors.append(f"{input_name} cannot mark an incomplete browser session as complete")


def _validate_orchestration_evidence(
    document: dict[str, Any], input_name: str, errors: list[str]
) -> None:
    facts = document.get("facts")
    if not isinstance(facts, dict):
        return
    required = {
        "collector_version",
        "policy_sha256",
        "static_root_fingerprint",
        "file_count",
        "total_bytes",
        "origin",
        "started_at",
        "ended_at",
        "server_started",
        "ready",
        "ready_probe_count",
        "server_stopped",
        "thread_stopped",
        "port_released",
        "cleanup_complete",
        "browser_complete",
        "lifecycle_complete",
        "events",
        "requests",
        "request_count",
        "method_counts",
        "status_counts",
        "rejected_request_count",
        "collection_errors",
        "observer_effect",
        "collection_elapsed_ms",
    }
    missing = sorted(required - set(facts))
    unknown = sorted(set(facts) - required)
    if missing:
        errors.append(f"{input_name}.facts is missing orchestration fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{input_name}.facts has unsupported orchestration fields: {', '.join(unknown)}")
    if not isinstance(facts.get("collector_version"), str) or not facts.get(
        "collector_version", ""
    ).strip():
        errors.append(f"{input_name}.facts.collector_version must be a non-empty string")
    for field in ("policy_sha256", "static_root_fingerprint"):
        value = facts.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            errors.append(f"{input_name}.facts.{field} must be a SHA-256 digest")
    if not _browser_url_is_sanitized(facts.get("origin"), origin_only=True):
        errors.append(f"{input_name}.facts.origin must be a sanitized loopback origin")
    for field in ("started_at", "ended_at"):
        if not _validate_timestamp(facts.get(field)):
            errors.append(f"{input_name}.facts.{field} must be an ISO-8601 timestamp with timezone")
    for field in (
        "server_started",
        "ready",
        "server_stopped",
        "thread_stopped",
        "port_released",
        "cleanup_complete",
        "browser_complete",
        "lifecycle_complete",
    ):
        if not isinstance(facts.get(field), bool):
            errors.append(f"{input_name}.facts.{field} must be a boolean")
    for field in (
        "file_count",
        "total_bytes",
        "ready_probe_count",
        "request_count",
        "rejected_request_count",
    ):
        value = facts.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{input_name}.facts.{field} must be a non-negative integer")
    if facts.get("file_count") == 0:
        errors.append(f"{input_name}.facts.file_count must be positive")
    for field in ("events", "requests", "collection_errors"):
        if not isinstance(facts.get(field), list):
            errors.append(f"{input_name}.facts.{field} must be a list")
    for field in ("method_counts", "status_counts", "observer_effect"):
        if not isinstance(facts.get(field), dict):
            errors.append(f"{input_name}.facts.{field} must be an object")
    _validate_exact_items(
        facts.get("events"),
        {"sequence", "stage", "status", "started_at", "ended_at", "elapsed_ms", "error_type"},
        f"{input_name}.facts.events",
        errors,
    )
    _validate_exact_items(
        facts.get("requests"),
        {"sequence", "method", "path", "status", "bytes"},
        f"{input_name}.facts.requests",
        errors,
    )
    _validate_exact_items(
        facts.get("collection_errors"),
        {"stage", "error_type"},
        f"{input_name}.facts.collection_errors",
        errors,
    )
    events = facts.get("events")
    if isinstance(events, list):
        expected_stages = ["target-start"]
        if facts.get("server_started") is True:
            expected_stages.append("target-ready")
        if facts.get("ready") is True:
            expected_stages.append("browser-capture")
        expected_stages.append("target-cleanup")
        actual_stages = [
            event.get("stage") if isinstance(event, dict) else None for event in events
        ]
        if actual_stages != expected_stages:
            errors.append(f"{input_name}.facts.events does not match the lifecycle state machine")
        for index, event in enumerate(events):
            if not isinstance(event, dict):
                continue
            prefix = f"{input_name}.facts.events[{index}]"
            if event.get("sequence") != index + 1:
                errors.append(f"{prefix}.sequence must be contiguous")
            if event.get("status") not in {"PASSED", "FAILED"}:
                errors.append(f"{prefix}.status is unsupported")
            for field in ("started_at", "ended_at"):
                if not _validate_timestamp(event.get(field)):
                    errors.append(f"{prefix}.{field} must be an ISO-8601 timestamp")
            elapsed = event.get("elapsed_ms")
            if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
                errors.append(f"{prefix}.elapsed_ms must be a non-negative number")
            error_type = event.get("error_type")
            if event.get("status") == "FAILED" and not isinstance(error_type, str):
                errors.append(f"{prefix}.error_type is required for a failed event")
            if event.get("status") == "PASSED" and error_type is not None:
                errors.append(f"{prefix}.error_type must be null for a passed event")
    requests = facts.get("requests")
    if isinstance(requests, list):
        for index, request in enumerate(requests):
            if not isinstance(request, dict):
                continue
            prefix = f"{input_name}.facts.requests[{index}]"
            if request.get("sequence") != index + 1:
                errors.append(f"{prefix}.sequence must be contiguous")
            if request.get("method") not in {
                "GET",
                "HEAD",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "OPTIONS",
                "TRACE",
                "CONNECT",
            }:
                errors.append(f"{prefix}.method is unsupported")
            path = request.get("path")
            if (
                not isinstance(path, str)
                or len(path) > 2048
                or not (path.startswith("/") or path == "[REJECTED]")
                or any(character in path for character in ("?", "#", "\\", "\0"))
                or any(ord(character) < 32 for character in path)
            ):
                errors.append(f"{prefix}.path must be a sanitized path")
            status = request.get("status")
            if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599:
                errors.append(f"{prefix}.status is invalid")
            size = request.get("bytes")
            if not isinstance(size, int) or isinstance(size, bool) or size < 0:
                errors.append(f"{prefix}.bytes must be a non-negative integer")
        if facts.get("request_count") != len(requests):
            errors.append(f"{input_name}.facts.request_count does not match requests")
        expected_rejected = sum(
            1
            for request in requests
            if isinstance(request, dict)
            and isinstance(request.get("status"), int)
            and request["status"] >= 400
        )
        if facts.get("rejected_request_count") != expected_rejected:
            errors.append(f"{input_name}.facts.rejected_request_count does not match requests")
        expected_methods = Counter(
            request["method"] for request in requests if isinstance(request, dict) and "method" in request
        )
        expected_statuses = Counter(
            str(request["status"])
            for request in requests
            if isinstance(request, dict) and "status" in request
        )
        if facts.get("method_counts") != dict(sorted(expected_methods.items())):
            errors.append(f"{input_name}.facts.method_counts does not match requests")
        if facts.get("status_counts") != dict(sorted(expected_statuses.items())):
            errors.append(f"{input_name}.facts.status_counts does not match requests")
    observer = facts.get("observer_effect")
    if isinstance(observer, dict):
        expected_observer = {
            "rss_start_mb",
            "rss_peak_mb",
            "rss_delta_mb",
            "thread_start_count",
            "max_active_thread_count",
        }
        if set(observer) != expected_observer:
            errors.append(f"{input_name}.facts.observer_effect must contain exact supported fields")
        for field in ("rss_start_mb", "rss_peak_mb", "rss_delta_mb"):
            value = observer.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                errors.append(f"{input_name}.facts.observer_effect.{field} must be non-negative")
        for field in ("thread_start_count", "max_active_thread_count"):
            value = observer.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(f"{input_name}.facts.observer_effect.{field} must be a non-negative integer")
    elapsed = facts.get("collection_elapsed_ms")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
        errors.append(f"{input_name}.facts.collection_elapsed_ms must be a non-negative number")
    if facts.get("ready") is True and facts.get("server_started") is not True:
        errors.append(f"{input_name} cannot be ready when the server did not start")
    ready_probe_count = facts.get("ready_probe_count")
    if facts.get("ready") is True and (
        not isinstance(ready_probe_count, int)
        or isinstance(ready_probe_count, bool)
        or ready_probe_count < 1
    ):
        errors.append(f"{input_name} cannot be ready without a readiness probe")
    if facts.get("browser_complete") is True and facts.get("ready") is not True:
        errors.append(f"{input_name} cannot complete browser capture before readiness")
    if facts.get("cleanup_complete") is True and not all(
        facts.get(field) is True for field in ("server_stopped", "thread_stopped", "port_released")
    ):
        errors.append(f"{input_name} cannot mark incomplete cleanup as complete")
    if facts.get("lifecycle_complete") is True and (
        facts.get("server_started") is not True
        or facts.get("ready") is not True
        or facts.get("cleanup_complete") is not True
        or facts.get("collection_errors")
    ):
        errors.append(f"{input_name} cannot mark an incomplete lifecycle as complete")
    metadata = document.get("metadata")
    required_metadata = {
        "network_scope",
        "shell_used",
        "external_process_started",
        "writes_allowed",
        "request_headers_persisted",
        "request_bodies_persisted",
    }
    if not isinstance(metadata, dict) or set(metadata) != required_metadata:
        errors.append(f"{input_name}.metadata must contain exact orchestration safety fields")
    elif (
        metadata.get("network_scope") != "loopback-only"
        or metadata.get("shell_used") is not False
        or metadata.get("external_process_started") is not False
        or metadata.get("writes_allowed") is not False
        or metadata.get("request_headers_persisted") is not False
        or metadata.get("request_bodies_persisted") is not False
    ):
        errors.append(f"{input_name}.metadata violates the orchestration safety contract")


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _is_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _validate_command_identity(value: Any, path: str, errors: list[str]) -> None:
    required = {"basename", "size", "sha256", "path_identity_sha256"}
    if not isinstance(value, dict) or set(value) != required:
        errors.append(f"{path} must contain exact executable identity fields")
        return
    basename = value.get("basename")
    if (
        not isinstance(basename, str)
        or not basename.lower().endswith(".exe")
        or any(character in basename for character in ("/", "\\"))
        or any(ord(character) < 32 for character in basename)
        or redact_string(basename)[0] != basename
    ):
        errors.append(f"{path}.basename must be a path-free .exe name")
    if not _is_non_negative_int(value.get("size")) or value.get("size") == 0:
        errors.append(f"{path}.size must be a positive integer")
    for field in ("sha256", "path_identity_sha256"):
        if not _is_sha256(value.get(field)):
            errors.append(f"{path}.{field} must be a SHA-256 digest")


def _validate_command_stream(value: Any, path: str, errors: list[str]) -> None:
    required = {
        "attachment",
        "observed_bytes_lower_bound",
        "stream_complete",
        "persisted_bytes",
        "truncated",
        "overflowed",
        "redaction_count",
        "invalid_utf8_replacements",
        "control_character_replacements",
    }
    if not isinstance(value, dict) or set(value) != required:
        errors.append(f"{path} must contain exact command stream fields")
        return
    attachment = value.get("attachment")
    attachment_fields = {"path", "sha256", "size", "media_type", "logical_name"}
    if not isinstance(attachment, dict) or set(attachment) != attachment_fields:
        errors.append(f"{path}.attachment must contain exact attachment fields")
    else:
        try:
            _validate_attachment_path(attachment.get("path"), suffix=".txt")
        except ValidationError as exc:
            errors.extend(f"{path}.attachment: {message}" for message in exc.errors)
        if not _is_sha256(attachment.get("sha256")):
            errors.append(f"{path}.attachment.sha256 must be a SHA-256 digest")
        if attachment.get("media_type") != "text/plain; charset=utf-8":
            errors.append(f"{path}.attachment.media_type is unsupported")
        if not isinstance(attachment.get("logical_name"), str) or not ATTACHMENT_NAME_PATTERN.fullmatch(
            attachment.get("logical_name", "")
        ):
            errors.append(f"{path}.attachment.logical_name is invalid")
        if not _is_non_negative_int(attachment.get("size")):
            errors.append(f"{path}.attachment.size must be a non-negative integer")
    for field in (
        "observed_bytes_lower_bound",
        "persisted_bytes",
        "redaction_count",
        "invalid_utf8_replacements",
        "control_character_replacements",
    ):
        if not _is_non_negative_int(value.get(field)):
            errors.append(f"{path}.{field} must be a non-negative integer")
    for field in ("stream_complete", "truncated", "overflowed"):
        if not isinstance(value.get(field), bool):
            errors.append(f"{path}.{field} must be a boolean")
    if isinstance(attachment, dict) and value.get("persisted_bytes") != attachment.get("size"):
        errors.append(f"{path}.persisted_bytes must match the attachment size")
    if value.get("truncated") != value.get("overflowed"):
        errors.append(f"{path}.truncated must equal overflowed")
    if value.get("overflowed") is True and value.get("stream_complete") is not False:
        errors.append(f"{path} cannot be complete after output overflow")


def _validate_command_evidence(
    document: dict[str, Any], input_name: str, errors: list[str]
) -> None:
    facts = document.get("facts")
    if not isinstance(facts, dict):
        return
    required = {
        "collector_version",
        "plan_sha256",
        "command_policy_sha256",
        "preview_sha256",
        "command_id",
        "adapter",
        "tool_binding_id",
        "executable",
        "post_executable",
        "executable_postcheck_complete",
        "executable_identity_match",
        "argument_count",
        "argument_kinds",
        "arguments_sha256",
        "working_directory",
        "environment",
        "stdin",
        "tty_used",
        "shell_used",
        "started_at",
        "ended_at",
        "elapsed_ms",
        "process_created",
        "target_assigned",
        "target_resumed",
        "exit_code",
        "exit_expected",
        "termination_reason",
        "error_type",
        "oneshot_quiescent",
        "stdout",
        "stderr",
        "ownership",
        "subject",
        "run_work_created",
        "run_work_released",
        "capture_threads_stopped",
        "handles_released",
        "tree_released",
        "cleanup_complete",
        "observer_effect",
        "collection_errors",
    }
    missing = sorted(required - set(facts))
    unknown = sorted(set(facts) - required)
    if missing:
        errors.append(f"{input_name}.facts is missing command fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{input_name}.facts has unsupported command fields: {', '.join(unknown)}")
    if facts.get("collector_version") != "trusted-command/0.1":
        errors.append(f"{input_name}.facts.collector_version is unsupported")
    for field in ("plan_sha256", "command_policy_sha256", "preview_sha256", "arguments_sha256"):
        if not _is_sha256(facts.get(field)):
            errors.append(f"{input_name}.facts.{field} must be a SHA-256 digest")
    for field in ("command_id", "tool_binding_id"):
        value = facts.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{1,63}", value):
            errors.append(f"{input_name}.facts.{field} must be a stable lowercase identifier")
    if facts.get("adapter") != "TRUSTED_PROCESS_ONESHOT":
        errors.append(f"{input_name}.facts.adapter is unsupported")
    _validate_command_identity(facts.get("executable"), f"{input_name}.facts.executable", errors)
    post_identity = facts.get("post_executable")
    if post_identity is not None:
        _validate_command_identity(post_identity, f"{input_name}.facts.post_executable", errors)
    postcheck = facts.get("executable_postcheck_complete")
    identity_match = facts.get("executable_identity_match")
    if not isinstance(postcheck, bool):
        errors.append(f"{input_name}.facts.executable_postcheck_complete must be a boolean")
    if identity_match is not None and not isinstance(identity_match, bool):
        errors.append(f"{input_name}.facts.executable_identity_match must be boolean or null")
    if postcheck is True and (post_identity is None or not isinstance(identity_match, bool)):
        errors.append(f"{input_name}.facts executable postcheck fields are inconsistent")
    argument_count = facts.get("argument_count")
    argument_kinds = facts.get("argument_kinds")
    if not isinstance(argument_count, int) or isinstance(argument_count, bool) or not 1 <= argument_count <= 128:
        errors.append(f"{input_name}.facts.argument_count must be from 1 to 128")
    if (
        not isinstance(argument_kinds, list)
        or any(value not in {"literal", "run_work_path"} for value in argument_kinds)
        or argument_count != len(argument_kinds)
    ):
        errors.append(f"{input_name}.facts.argument_kinds must match argument_count")
    working = facts.get("working_directory")
    working_parts = working.split("/") if isinstance(working, str) else []
    if (
        not isinstance(working, str)
        or not working
        or "\\" in working
        or working.startswith("/")
        or re.match(r"^[A-Za-z]:", working)
        or any(ord(character) < 32 for character in working)
        or (working != "." and any(part in {"", ".", ".."} for part in working_parts))
        or redact_string(working)[0] != working
    ):
        errors.append(f"{input_name}.facts.working_directory must remain relative")
    environment = facts.get("environment")
    environment_fields = {
        "inherit_names",
        "set_names",
        "runner_names",
        "projection_sha256",
        "values_persisted",
    }
    if not isinstance(environment, dict) or set(environment) != environment_fields:
        errors.append(f"{input_name}.facts.environment must contain exact preview fields")
    else:
        for field in ("inherit_names", "set_names", "runner_names"):
            values = environment.get(field)
            if (
                not isinstance(values, list)
                or any(not isinstance(value, str) for value in values)
                or values != sorted(values)
                or len(values) != len(set(values))
            ):
                errors.append(f"{input_name}.facts.environment.{field} must be sorted and unique")
        if environment.get("runner_names") != ["TEMP", "TMP"]:
            errors.append(f"{input_name}.facts.environment.runner_names is unsupported")
        if not _is_sha256(environment.get("projection_sha256")):
            errors.append(f"{input_name}.facts.environment.projection_sha256 must be SHA-256")
        if environment.get("values_persisted") is not False:
            errors.append(f"{input_name}.facts.environment must not persist values")
    if facts.get("stdin") != "CLOSED" or facts.get("tty_used") is not False or facts.get("shell_used") is not False:
        errors.append(f"{input_name}.facts violates the closed-stdin no-TTY no-Shell boundary")
    for field in ("started_at", "ended_at"):
        if not _validate_timestamp(facts.get(field)):
            errors.append(f"{input_name}.facts.{field} must be an ISO-8601 timestamp")
    elapsed = facts.get("elapsed_ms")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
        errors.append(f"{input_name}.facts.elapsed_ms must be a non-negative number")
    booleans = (
        "process_created",
        "target_assigned",
        "target_resumed",
        "exit_expected",
        "oneshot_quiescent",
        "run_work_created",
        "run_work_released",
        "capture_threads_stopped",
        "handles_released",
        "tree_released",
        "cleanup_complete",
    )
    for field in booleans:
        if not isinstance(facts.get(field), bool):
            errors.append(f"{input_name}.facts.{field} must be a boolean")
    if facts.get("target_resumed") is True and facts.get("target_assigned") is not True:
        errors.append(f"{input_name}.facts cannot resume an unassigned target")
    if facts.get("target_assigned") is True and facts.get("process_created") is not True:
        errors.append(f"{input_name}.facts cannot assign a target that was not created")
    exit_code = facts.get("exit_code")
    if exit_code is not None and (
        not isinstance(exit_code, int) or isinstance(exit_code, bool) or not 0 <= exit_code <= 0xFFFFFFFF
    ):
        errors.append(f"{input_name}.facts.exit_code must be a Windows exit code or null")
    if facts.get("exit_expected") is True and exit_code is None:
        errors.append(f"{input_name}.facts.exit_expected requires an observed exit code")
    reasons = {
        "EXITED",
        "DESCENDANT_GRACE_EXPIRED",
        "TIMEOUT",
        "CANCELLED",
        "STDOUT_LIMIT_EXCEEDED",
        "STDERR_LIMIT_EXCEEDED",
        "PROCESS_CREATE_FAILED",
        "OWNERSHIP_ASSIGNMENT_FAILED",
        "TARGET_RESUME_FAILED",
        "PROCESS_WAIT_FAILED",
        "PROCESS_RUNNER_ERROR",
        "SUBJECT_SNAPSHOT_FAILED",
        "RUN_WORK_CREATE_FAILED",
    }
    if facts.get("termination_reason") not in reasons:
        errors.append(f"{input_name}.facts.termination_reason is unsupported")
    error_type = facts.get("error_type")
    if error_type is not None and (
        not isinstance(error_type, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]{1,63}", error_type)
    ):
        errors.append(f"{input_name}.facts.error_type must be a stable error identifier or null")
    _validate_command_stream(facts.get("stdout"), f"{input_name}.facts.stdout", errors)
    _validate_command_stream(facts.get("stderr"), f"{input_name}.facts.stderr", errors)
    for stream_name in ("stdout", "stderr"):
        stream = facts.get(stream_name)
        attachment = stream.get("attachment") if isinstance(stream, dict) else None
        if isinstance(attachment, dict) and (
            attachment.get("path") != f"attachments/command/{stream_name}.txt"
            or attachment.get("logical_name") != f"command-{stream_name}"
        ):
            errors.append(
                f"{input_name}.facts.{stream_name}.attachment must use the fixed command output identity"
            )
    ownership = facts.get("ownership")
    ownership_fields = {
        "backend",
        "parent_in_job",
        "active_process_limit",
        "active_process_limit_enforced",
        "process_limit_attempt_observation",
        "total_assigned_processes",
        "final_active_processes",
        "job_limit_terminated_processes",
        "forced_termination_requested",
        "forced_termination_processes_observed",
    }
    if not isinstance(ownership, dict) or set(ownership) != ownership_fields:
        errors.append(f"{input_name}.facts.ownership must contain exact ownership fields")
    else:
        if ownership.get("backend") != "WINDOWS_JOB_OBJECT_PYWIN32_312":
            errors.append(f"{input_name}.facts.ownership.backend is unsupported")
        for field in (
            "parent_in_job",
            "active_process_limit_enforced",
            "forced_termination_requested",
        ):
            if not isinstance(ownership.get(field), bool):
                errors.append(f"{input_name}.facts.ownership.{field} must be a boolean")
        if ownership.get("process_limit_attempt_observation") != "NOT_PROVEN":
            errors.append(f"{input_name}.facts.ownership overstates process-limit observation")
        for field in (
            "active_process_limit",
            "total_assigned_processes",
            "final_active_processes",
            "job_limit_terminated_processes",
            "forced_termination_processes_observed",
        ):
            if not _is_non_negative_int(ownership.get(field)):
                errors.append(f"{input_name}.facts.ownership.{field} must be non-negative")
        active_limit = ownership.get("active_process_limit")
        if (
            not isinstance(active_limit, int)
            or isinstance(active_limit, bool)
            or not 1 <= active_limit <= 32
        ):
            errors.append(f"{input_name}.facts.ownership.active_process_limit is out of range")
        if facts.get("tree_released") is True and ownership.get("final_active_processes") != 0:
            errors.append(f"{input_name}.facts.ownership cannot retain active processes after release")
        if facts.get("target_assigned") is True and ownership.get(
            "active_process_limit_enforced"
        ) is not True:
            errors.append(f"{input_name}.facts.ownership did not enforce the active-process limit")
    subject = facts.get("subject")
    subject_fields = {
        "policy",
        "watch_roots",
        "before_fingerprint",
        "after_fingerprint",
        "before_file_count",
        "after_file_count",
        "before_link_count",
        "after_link_count",
        "before_total_bytes",
        "after_total_bytes",
        "diff_counts",
        "final_state_drift_detected",
        "snapshot_complete",
        "write_activity",
    }
    if not isinstance(subject, dict) or set(subject) != subject_fields:
        errors.append(f"{input_name}.facts.subject must contain exact snapshot fields")
    else:
        if subject.get("policy") != "RUN_WORK_ONLY_DETECT_SUBJECT_CHANGES":
            errors.append(f"{input_name}.facts.subject.policy is unsupported")
        watch_roots = subject.get("watch_roots")
        if not isinstance(watch_roots, list) or not watch_roots:
            errors.append(f"{input_name}.facts.subject.watch_roots must be a non-empty list")
        else:
            for index, root in enumerate(watch_roots):
                parts = root.split("/") if isinstance(root, str) else []
                if (
                    not isinstance(root, str)
                    or not root
                    or "\\" in root
                    or root.startswith("/")
                    or re.match(r"^[A-Za-z]:", root)
                    or any(ord(character) < 32 for character in root)
                    or (root != "." and any(part in {"", ".", ".."} for part in parts))
                    or redact_string(root)[0] != root
                ):
                    errors.append(
                        f"{input_name}.facts.subject.watch_roots[{index}] must remain relative"
                    )
        for field in ("before_fingerprint", "after_fingerprint"):
            if subject.get(field) is not None and not _is_sha256(subject.get(field)):
                errors.append(f"{input_name}.facts.subject.{field} must be SHA-256 or null")
        for field in (
            "before_file_count",
            "after_file_count",
            "before_link_count",
            "after_link_count",
            "before_total_bytes",
            "after_total_bytes",
        ):
            if subject.get(field) is not None and not _is_non_negative_int(subject.get(field)):
                errors.append(f"{input_name}.facts.subject.{field} must be non-negative or null")
        diff = subject.get("diff_counts")
        diff_fields = {"added", "deleted", "modified", "type_changed", "link_changed"}
        if diff is not None and (
            not isinstance(diff, dict)
            or set(diff) != diff_fields
            or any(not _is_non_negative_int(value) for value in diff.values())
        ):
            errors.append(f"{input_name}.facts.subject.diff_counts is invalid")
        if subject.get("final_state_drift_detected") is not None and not isinstance(
            subject.get("final_state_drift_detected"), bool
        ):
            errors.append(f"{input_name}.facts.subject.final_state_drift_detected is invalid")
        if not isinstance(subject.get("snapshot_complete"), bool):
            errors.append(f"{input_name}.facts.subject.snapshot_complete must be a boolean")
        if subject.get("write_activity") != "NOT_PROVEN":
            errors.append(f"{input_name}.facts.subject.write_activity must remain NOT_PROVEN")
        if subject.get("snapshot_complete") is True and (
            subject.get("before_fingerprint") is None
            or subject.get("after_fingerprint") is None
            or diff is None
            or not isinstance(subject.get("final_state_drift_detected"), bool)
        ):
            errors.append(f"{input_name}.facts.subject complete snapshot fields are inconsistent")
    observer = facts.get("observer_effect")
    observer_fields = {
        "rss_start_mb",
        "rss_peak_mb",
        "rss_delta_mb",
        "sample_count",
        "thread_stopped",
    }
    if not isinstance(observer, dict) or set(observer) != observer_fields:
        errors.append(f"{input_name}.facts.observer_effect must contain exact fields")
    else:
        for field in ("rss_start_mb", "rss_peak_mb", "rss_delta_mb"):
            value = observer.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                errors.append(f"{input_name}.facts.observer_effect.{field} must be non-negative")
        if not _is_non_negative_int(observer.get("sample_count")):
            errors.append(f"{input_name}.facts.observer_effect.sample_count must be non-negative")
        if not isinstance(observer.get("thread_stopped"), bool):
            errors.append(f"{input_name}.facts.observer_effect.thread_stopped must be a boolean")
    _validate_exact_items(
        facts.get("collection_errors"),
        {"stage", "error_type"},
        f"{input_name}.facts.collection_errors",
        errors,
    )
    if not isinstance(facts.get("collection_errors"), list):
        errors.append(f"{input_name}.facts.collection_errors must be a list")
    observer_thread_stopped = (
        observer.get("thread_stopped") if isinstance(observer, dict) else None
    )
    if facts.get("cleanup_complete") is True and (
        not all(
            facts.get(field) is True
            for field in (
                "run_work_released",
                "capture_threads_stopped",
                "handles_released",
                "tree_released",
            )
        )
        or observer_thread_stopped is not True
    ):
        errors.append(f"{input_name}.facts cannot mark incomplete cleanup as complete")
    if facts.get("process_created") is True and facts.get("run_work_created") is not True:
        errors.append(f"{input_name}.facts cannot create a process without owned Run work")
    reason = facts.get("termination_reason")
    forced_termination = (
        ownership.get("forced_termination_requested")
        if isinstance(ownership, dict)
        else None
    )
    if reason == "EXITED" and (
        facts.get("exit_code") is None
        or facts.get("process_created") is not True
        or facts.get("target_assigned") is not True
        or facts.get("target_resumed") is not True
        or facts.get("error_type") is not None
    ):
        errors.append(f"{input_name}.facts EXITED state is internally inconsistent")
    if reason in {"TIMEOUT", "CANCELLED", "STDOUT_LIMIT_EXCEEDED", "STDERR_LIMIT_EXCEEDED"} and (
        facts.get("process_created") is not True
        or facts.get("target_assigned") is not True
        or facts.get("target_resumed") is not True
        or forced_termination is not True
    ):
        errors.append(f"{input_name}.facts forced termination state is internally inconsistent")
    if reason == "PROCESS_CREATE_FAILED" and (
        facts.get("process_created") is not False
        or facts.get("target_assigned") is not False
        or facts.get("target_resumed") is not False
        or facts.get("error_type") != "PROCESS_CREATE_FAILED"
    ):
        errors.append(f"{input_name}.facts process-create failure state is inconsistent")
    if facts.get("oneshot_quiescent") is True and (
        reason != "EXITED"
        or facts.get("tree_released") is not True
        or forced_termination is not False
    ):
        errors.append(f"{input_name}.facts oneshot quiescence is internally inconsistent")
    metadata = document.get("metadata")
    metadata_fields = {
        "structured_arguments",
        "environment_values_persisted",
        "absolute_paths_persisted",
        "raw_output_persisted",
        "filesystem_isolation",
        "network_isolation",
        "executable_toctou_containment",
        "untrusted_code_containment",
    }
    if not isinstance(metadata, dict) or set(metadata) != metadata_fields:
        errors.append(f"{input_name}.metadata must contain exact command safety fields")
    elif (
        metadata.get("structured_arguments") is not True
        or metadata.get("environment_values_persisted") is not False
        or metadata.get("absolute_paths_persisted") is not False
        or metadata.get("raw_output_persisted") is not False
        or metadata.get("filesystem_isolation") != "NOT_PROVEN"
        or metadata.get("network_isolation") != "NOT_PROVEN"
        or metadata.get("executable_toctou_containment") != "NOT_PROVEN"
        or metadata.get("untrusted_code_containment") != "NOT_SUPPORTED"
    ):
        errors.append(f"{input_name}.metadata overstates the command safety boundary")


def validate_evidence(document: dict[str, Any], input_name: str) -> None:
    errors: list[str] = []
    allowed_fields = {
        "schema_version",
        "evidence_type",
        "source",
        "captured_at",
        "facts",
        "observed_variables",
        "metadata",
    }
    unknown = sorted(set(document) - allowed_fields)
    if unknown:
        errors.append(f"{input_name} has unsupported fields: {', '.join(unknown)}")
    if document.get("schema_version") != "0.1":
        errors.append(f"{input_name}.schema_version must be '0.1'")
    evidence_type = document.get("evidence_type")
    if not isinstance(evidence_type, str) or not EVIDENCE_TYPE_PATTERN.fullmatch(evidence_type):
        errors.append(f"{input_name}.evidence_type must be a 2-64 character lowercase identifier")
    if not isinstance(document.get("source"), str) or not document.get("source", "").strip():
        errors.append(f"{input_name}.source must be a non-empty string")
    if not _validate_timestamp(document.get("captured_at")):
        errors.append(f"{input_name}.captured_at must be an ISO-8601 timestamp with timezone")
    if not isinstance(document.get("facts"), dict):
        errors.append(f"{input_name}.facts must be an object")
    observations = document.get("observed_variables", {})
    if not isinstance(observations, dict):
        errors.append(f"{input_name}.observed_variables must be an object when present")
    if document.get("evidence_type") == "runtime.preflight":
        _validate_preflight_evidence(document, input_name, errors)
    if document.get("evidence_type") == "browser.session":
        _validate_browser_evidence(document, input_name, errors)
    if document.get("evidence_type") == "runtime.orchestration":
        _validate_orchestration_evidence(document, input_name, errors)
    if document.get("evidence_type") == "runtime.command":
        _validate_command_evidence(document, input_name, errors)
    if document.get("evidence_type") == "runtime.bootstrap":
        from veritrail.bootstrap_evidence import validate_bootstrap_evidence

        validate_bootstrap_evidence(document, input_name, errors)
    try:
        canonical_json_bytes(document)
    except (TypeError, ValueError) as exc:
        errors.append(f"{input_name} must contain finite JSON values: {exc}")
    if errors:
        raise ValidationError(errors)


def import_evidence_document(
    document: dict[str, Any],
    input_name: str,
    *,
    attachments: tuple[EvidenceAttachment, ...] = (),
) -> ImportedEvidence:
    validate_evidence(document, input_name)
    sanitized, redacted_fields = redact_value(document)
    encoded = canonical_json_bytes(sanitized)
    return ImportedEvidence(
        document=sanitized,
        sha256=sha256_bytes(encoded),
        size=len(encoded),
        redacted_fields=redacted_fields,
        input_name=redact_string(input_name)[0],
        attachments=attachments,
    )


def verify_imported_evidence(artifact: ImportedEvidence) -> None:
    validate_evidence(artifact.document, artifact.input_name)
    encoded = canonical_json_bytes(artifact.document)
    if sha256_bytes(encoded) != artifact.sha256 or len(encoded) != artifact.size:
        raise ValidationError(
            [f"imported evidence {artifact.input_name} changed after hashing"]
        )
    attachment_by_path: dict[str, EvidenceAttachment] = {}
    for attachment in artifact.attachments:
        _validate_attachment_path(attachment.path)
        if attachment.media_type == "image/png":
            if not attachment.path.endswith(".png") or not attachment.content.startswith(
                b"\x89PNG\r\n\x1a\n"
            ):
                raise ValidationError([f"evidence attachment {attachment.path} is not a PNG"])
        elif attachment.media_type == "text/plain; charset=utf-8":
            if not attachment.path.endswith(".txt"):
                raise ValidationError([f"evidence attachment {attachment.path} is not text"])
            try:
                text = attachment.content.decode("utf-8", errors="strict")
            except UnicodeDecodeError as exc:
                raise ValidationError(
                    [f"evidence attachment {attachment.path} is not valid UTF-8"]
                ) from exc
            redacted_text, _ = redact_string(text)
            if (
                redacted_text != text
                or re.search(r"(?im)(?<![A-Za-z0-9_])[A-Z]:[\\/][^\r\n]*", text)
                or re.search(r"(?m)(?<!\\)\\\\[^\r\n]+", text)
            ):
                raise ValidationError(
                    [f"evidence attachment {attachment.path} contains unredacted sensitive text"]
                )
        else:
            raise ValidationError([f"evidence attachment {attachment.path} has unsupported media type"])
        if not ATTACHMENT_NAME_PATTERN.fullmatch(attachment.logical_name):
            raise ValidationError([f"evidence attachment {attachment.path} has an invalid logical name"])
        if attachment.path in attachment_by_path:
            raise ValidationError([f"duplicate evidence attachment path: {attachment.path}"])
        if (
            sha256_bytes(attachment.content) != attachment.sha256
            or len(attachment.content) != attachment.size
        ):
            raise ValidationError([f"evidence attachment {attachment.path} changed after hashing"])
        attachment_by_path[attachment.path] = attachment
    evidence_type = artifact.document.get("evidence_type")
    if evidence_type == "browser.session":
        screenshots = artifact.document.get("facts", {}).get("screenshots", [])
        referenced = {
            item["path"]: item
            for item in screenshots
            if isinstance(item, dict) and "path" in item
        }
        if set(referenced) != set(attachment_by_path):
            raise ValidationError(["browser screenshot references do not match generated attachments"])
        for path, reference in referenced.items():
            attachment = attachment_by_path[path]
            expected_logical_name = f"{reference.get('viewport')}-{reference.get('name')}"
            if (
                reference.get("sha256") != attachment.sha256
                or reference.get("size") != attachment.size
                or reference.get("media_type") != attachment.media_type
                or expected_logical_name != attachment.logical_name
            ):
                raise ValidationError(
                    [f"browser screenshot reference does not match attachment: {path}"]
                )
    elif evidence_type == "runtime.command":
        facts = artifact.document.get("facts", {})
        referenced = {
            stream["attachment"]["path"]: stream["attachment"]
            for stream in (facts.get("stdout"), facts.get("stderr"))
            if isinstance(stream, dict) and isinstance(stream.get("attachment"), dict)
        }
        if set(referenced) != set(attachment_by_path):
            raise ValidationError(["command output references do not match generated attachments"])
        for path, reference in referenced.items():
            attachment = attachment_by_path[path]
            if any(
                (
                    reference.get("sha256") != attachment.sha256,
                    reference.get("size") != attachment.size,
                    reference.get("media_type") != attachment.media_type,
                    reference.get("logical_name") != attachment.logical_name,
                )
            ):
                raise ValidationError(
                    [f"command output reference does not match attachment: {path}"]
                )
    elif evidence_type == "runtime.bootstrap":
        nodes = artifact.document.get("facts", {}).get("nodes", [])
        expected_attachment_count = (
            2
            if artifact.document.get("source")
            == "VeriTrail bootstrap-lifecycle/0.3"
            else 4
        )
        referenced = {
            stream["attachment"]["path"]: stream["attachment"]
            for node in nodes
            if isinstance(node, dict)
            for stream in (node.get("stdout"), node.get("stderr"))
            if isinstance(stream, dict) and isinstance(stream.get("attachment"), dict)
        }
        if (
            len(referenced) != expected_attachment_count
            or set(referenced) != set(attachment_by_path)
        ):
            raise ValidationError(
                [
                    "bootstrap output references do not match the collector attachment cardinality"
                ]
            )
        for path, reference in referenced.items():
            attachment = attachment_by_path[path]
            if any(
                (
                    reference.get("sha256") != attachment.sha256,
                    reference.get("size") != attachment.size,
                    reference.get("media_type") != attachment.media_type,
                    reference.get("logical_name") != attachment.logical_name,
                )
            ):
                raise ValidationError(
                    [f"bootstrap output reference does not match attachment: {path}"]
                )
    elif attachment_by_path:
        raise ValidationError(["this evidence type does not support generated attachments"])


def import_evidence_files(paths: list[Path], max_artifact_bytes: int) -> tuple[list[ImportedEvidence], list[str]]:
    imported: list[ImportedEvidence] = []
    duplicates: list[str] = []
    seen_hashes: set[str] = set()
    for path in paths:
        input_name, _ = redact_string(path.name)
        try:
            size = path.stat().st_size
        except OSError as exc:
            raise ValidationError([f"cannot inspect evidence {input_name}: {exc}"]) from exc
        if size > max_artifact_bytes:
            raise ValidationError(
                [f"evidence {input_name} is {size} bytes; limit is {max_artifact_bytes} bytes"]
            )
        document = load_json_object(path, label="evidence")
        artifact = import_evidence_document(document, input_name)
        verify_imported_evidence(artifact)
        if artifact.sha256 in seen_hashes:
            duplicates.append(input_name)
            continue
        seen_hashes.add(artifact.sha256)
        imported.append(artifact)
    return imported, duplicates
