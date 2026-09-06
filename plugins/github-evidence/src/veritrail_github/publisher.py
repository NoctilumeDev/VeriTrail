from __future__ import annotations

import os
import secrets
from pathlib import Path

from veritrail.canonical import canonical_json_bytes
from veritrail.evidence import ImportedEvidence, verify_imported_evidence

from veritrail_github.errors import CollectionError, GitHubEvidenceError


def _publish_bytes_create_new(
    path: Path,
    payload: bytes,
    *,
    label: str,
    error_type: type[GitHubEvidenceError] = CollectionError,
) -> None:
    if path.exists():
        raise error_type(f"refusing to overwrite existing {label}: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.parent / f".{path.name}.{secrets.token_hex(8)}.staging"
    try:
        with staging.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(staging, path)
        except FileExistsError as exc:
            raise error_type(
                f"refusing to overwrite existing {label}: {path.name}"
            ) from exc
        except OSError as exc:
            raise error_type(
                f"atomic create-new {label} publish is unavailable"
            ) from exc
    finally:
        try:
            staging.unlink()
        except FileNotFoundError:
            pass


def publish_evidence(path: Path, artifact: ImportedEvidence) -> None:
    """Create a complete Evidence file atomically without overwriting a target."""

    verify_imported_evidence(artifact)
    payload = canonical_json_bytes(artifact.document) + b"\n"
    _publish_bytes_create_new(path, payload, label="Evidence")
