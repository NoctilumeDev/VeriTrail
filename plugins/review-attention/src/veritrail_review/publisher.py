from __future__ import annotations

import os
import secrets
import shutil
from pathlib import Path
from typing import Callable

from veritrail_review.contracts import (
    OwnedSourceSnapshot,
    validate_source_snapshot_document,
)
from veritrail_review.errors import SourceSnapshotError, SourceSnapshotFailureCode


ARTIFACT_FILENAME = "source-snapshot.json"


def publish_source_snapshot(
    output_directory: Path,
    snapshot: OwnedSourceSnapshot,
    *,
    deadline_check: Callable[[str], None],
    max_canonical_bytes: int,
) -> Path:
    """Atomically publish exactly one create-new SourceSnapshot directory."""

    output = Path(output_directory)
    parent = output.parent
    if not output.name or output.name in {".", ".."}:
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    if os.name != "nt":
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.OUTPUT_PUBLICATION_FAILED
        )
    try:
        parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.OUTPUT_PUBLICATION_FAILED
        ) from exc
    if output.exists():
        raise SourceSnapshotError(SourceSnapshotFailureCode.OUTPUT_ALREADY_EXISTS)

    staging = parent / f".{output.name}.{secrets.token_hex(12)}.staging"
    try:
        deadline_check("publication-staging")
        staging.mkdir()
        artifact = staging / ARTIFACT_FILENAME
        with artifact.open("xb") as handle:
            handle.write(snapshot.canonical_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        deadline_check("publication-write")
        staged_bytes = artifact.read_bytes()
        deadline_check("publication-readback")
        if staged_bytes != snapshot.canonical_bytes:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.OUTPUT_PUBLICATION_FAILED
            )
        validate_source_snapshot_document(
            snapshot.document_copy(),
            expected_bytes=staged_bytes,
            max_canonical_bytes=max_canonical_bytes,
            deadline_check=lambda: deadline_check("publication-validation"),
        )
        deadline_check("publication-commit")
        try:
            os.rename(staging, output)
        except OSError as exc:
            if output.exists():
                raise SourceSnapshotError(
                    SourceSnapshotFailureCode.OUTPUT_ALREADY_EXISTS
                ) from exc
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.OUTPUT_PUBLICATION_FAILED
            ) from exc
        return output / ARTIFACT_FILENAME
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
