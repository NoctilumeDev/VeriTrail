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
    try:
        canonical_json_bytes(document)
    except (TypeError, ValueError) as exc:
        errors.append(f"{input_name} must contain finite JSON values: {exc}")
    if errors:
        raise ValidationError(errors)


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
        validate_evidence(document, input_name)
        sanitized, redacted_fields = redact_value(document)
        encoded = canonical_json_bytes(sanitized)
        digest = sha256_bytes(encoded)
        if digest in seen_hashes:
            duplicates.append(input_name)
            continue
        seen_hashes.add(digest)
        imported.append(
            ImportedEvidence(
                document=sanitized,
                sha256=digest,
                size=len(encoded),
                redacted_fields=redacted_fields,
                input_name=input_name,
            )
        )
    return imported, duplicates
