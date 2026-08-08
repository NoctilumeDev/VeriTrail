from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_bytes
from veritrail.errors import ValidationError
from veritrail.jsonio import load_json_object
from veritrail.privacy import redact_string, redact_value

EVIDENCE_TYPE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")


@dataclass(frozen=True)
class ImportedEvidence:
    document: dict[str, Any]
    sha256: str
    size: int
    redacted_fields: int
    input_name: str


def _validate_timestamp(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


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
    try:
        canonical_json_bytes(document)
    except (TypeError, ValueError) as exc:
        errors.append(f"{input_name} must contain finite JSON values: {exc}")
    if errors:
        raise ValidationError(errors)


def import_evidence_document(document: dict[str, Any], input_name: str) -> ImportedEvidence:
    validate_evidence(document, input_name)
    sanitized, redacted_fields = redact_value(document)
    encoded = canonical_json_bytes(sanitized)
    return ImportedEvidence(
        document=sanitized,
        sha256=sha256_bytes(encoded),
        size=len(encoded),
        redacted_fields=redacted_fields,
        input_name=redact_string(input_name)[0],
    )


def verify_imported_evidence(artifact: ImportedEvidence) -> None:
    validate_evidence(artifact.document, artifact.input_name)
    encoded = canonical_json_bytes(artifact.document)
    if sha256_bytes(encoded) != artifact.sha256 or len(encoded) != artifact.size:
        raise ValidationError(
            [f"imported evidence {artifact.input_name} changed after hashing"]
        )


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
        if artifact.sha256 in seen_hashes:
            duplicates.append(input_name)
            continue
        seen_hashes.add(artifact.sha256)
        imported.append(artifact)
    return imported, duplicates
