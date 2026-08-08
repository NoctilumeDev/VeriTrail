from __future__ import annotations

import re
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


def create_attachment(
    *, path: str, content: bytes, media_type: str, logical_name: str
) -> EvidenceAttachment:
    _validate_attachment_path(path)
    if not isinstance(content, bytes):
        raise ValidationError(["evidence attachment content must be bytes"])
    if media_type != "image/png":
        raise ValidationError(["M2 evidence attachments must use image/png"])
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValidationError(["image/png evidence attachment is missing the PNG signature"])
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


def _validate_attachment_path(value: str) -> None:
    if not isinstance(value, str) or "\\" in value:
        raise ValidationError(["evidence attachment path must use a relative POSIX path"])
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or path.parts[0] != "attachments"
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.suffix.lower() != ".png"
    ):
        raise ValidationError(["evidence attachment path must stay under attachments/ and end in .png"])


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
        if attachment.media_type != "image/png" or not attachment.content.startswith(
            b"\x89PNG\r\n\x1a\n"
        ):
            raise ValidationError([f"evidence attachment {attachment.path} is not a PNG"])
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
    screenshots = (
        artifact.document.get("facts", {}).get("screenshots", [])
        if artifact.document.get("evidence_type") == "browser.session"
        else []
    )
    referenced = {item["path"]: item for item in screenshots if isinstance(item, dict) and "path" in item}
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
            raise ValidationError([f"browser screenshot reference does not match attachment: {path}"])


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
