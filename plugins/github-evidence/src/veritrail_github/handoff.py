from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from veritrail.canonical import canonical_json_bytes
from veritrail.evidence import ImportedEvidence, import_evidence_files
from veritrail.errors import ValidationError
from veritrail.jsonio import load_json_object
from veritrail.resource_limits import MAX_ARTIFACT_BYTES

from veritrail_github.errors import ContractError, HandoffError
from veritrail_github.handoff_contracts import (
    HANDOFF_MANIFEST_KIND,
    HANDOFF_SCHEMA_VERSION,
    validate_handoff_manifest,
)
from veritrail_github.publisher import _publish_bytes_create_new


MAX_HANDOFF_MANIFEST_BYTES = 64 * 1024


class _PairedSideLike(Protocol):
    collector_role: str
    artifact_path: Path | None
    artifact_sha256: str | None
    state: str
    error_code: str | None


class _PairedResultLike(Protocol):
    collection_order: tuple[str, str]
    api: _PairedSideLike
    render: _PairedSideLike


def _published_filename(
    outcome: _PairedSideLike,
    *,
    manifest_path: Path,
) -> str | None:
    if outcome.state != "PUBLISHED":
        return None
    artifact_path = outcome.artifact_path
    if not isinstance(artifact_path, Path):
        raise ContractError(["PUBLISHED handoff side requires an artifact path"])
    if artifact_path.absolute().parent != manifest_path.absolute().parent:
        raise ContractError(
            ["PUBLISHED Evidence must share the handoff manifest directory"]
        )
    return artifact_path.name


def _manifest_side(
    outcome: _PairedSideLike,
    *,
    manifest_path: Path,
) -> dict[str, Any]:
    return {
        "collector_role": outcome.collector_role,
        "state": outcome.state,
        "evidence_path": _published_filename(
            outcome,
            manifest_path=manifest_path,
        ),
        "evidence_sha256": outcome.artifact_sha256,
        "error_code": outcome.error_code,
    }


def build_handoff_manifest(
    result: _PairedResultLike,
    *,
    manifest_path: Path,
) -> dict[str, Any]:
    """Build only the thin artifact-selection manifest from a paired outcome."""

    if not isinstance(manifest_path, Path) or not manifest_path.name:
        raise ContractError(["handoff manifest path must name a file"])
    manifest = {
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "manifest_kind": HANDOFF_MANIFEST_KIND,
        "collection_order": list(result.collection_order),
        "sides": [
            _manifest_side(result.api, manifest_path=manifest_path),
            _manifest_side(result.render, manifest_path=manifest_path),
        ],
    }
    return validate_handoff_manifest(manifest)


def publish_handoff_manifest(
    path: Path,
    result: _PairedResultLike,
) -> dict[str, Any]:
    """Atomically create one handoff manifest without overwriting a target."""

    manifest = build_handoff_manifest(result, manifest_path=path)
    payload = canonical_json_bytes(manifest) + b"\n"
    _publish_bytes_create_new(
        path,
        payload,
        label="handoff manifest",
        error_type=HandoffError,
    )
    return manifest


def import_verified_handoff_evidence(
    manifest_path: Path,
) -> tuple[ImportedEvidence, ...]:
    """Import each selected Evidence path once and verify its handoff identity."""

    try:
        manifest = validate_handoff_manifest(
            load_json_object(
                manifest_path,
                label="handoff manifest",
                max_bytes=MAX_HANDOFF_MANIFEST_BYTES,
            )
        )
    except (ContractError, ValidationError) as exc:
        raise HandoffError(
            f"cannot safely import handoff manifest {manifest_path.name}"
        ) from exc

    published_sides = [
        side for side in manifest["sides"] if side["state"] == "PUBLISHED"
    ]
    if not published_sides:
        return ()
    evidence_paths = [
        manifest_path.parent / side["evidence_path"] for side in published_sides
    ]
    try:
        imported, duplicates = import_evidence_files(
            evidence_paths,
            MAX_ARTIFACT_BYTES,
        )
    except ValidationError as exc:
        raise HandoffError("cannot safely import selected Evidence") from exc
    if duplicates or len(imported) != len(published_sides):
        raise HandoffError("handoff selected ambiguous duplicate Evidence")

    for side, artifact in zip(published_sides, imported, strict=True):
        if artifact.sha256 != side["evidence_sha256"]:
            raise HandoffError(
                f"Evidence digest does not match handoff side {side['collector_role']}"
            )
        metadata = artifact.document.get("metadata")
        observation = (
            metadata.get("veritrail_observation")
            if isinstance(metadata, dict)
            else None
        )
        collector_role = (
            observation.get("collector_role")
            if isinstance(observation, dict)
            else None
        )
        if collector_role != side["collector_role"]:
            raise HandoffError(
                f"Evidence role does not match handoff side {side['collector_role']}"
            )

    return tuple(imported)
