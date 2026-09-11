from __future__ import annotations

import platform
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from veritrail_review.contracts import (
    DEFAULT_ACQUISITION_BUDGET,
    OwnedSourceSnapshot,
    SnapshotAcquisitionBudget,
    SourceSnapshotRequest,
    SourceSnapshotRuntime,
    SourceSnapshotSpec,
    build_source_snapshot_document,
    git_oid,
    validate_source_snapshot_document,
    validate_source_snapshot_spec,
)
from veritrail_review.errors import SourceSnapshotError, SourceSnapshotFailureCode
from veritrail_review.git_objects import GitAcquisition, acquire_git_snapshot
from veritrail_review.publisher import publish_source_snapshot


@dataclass(frozen=True)
class SourceSnapshotPublication:
    artifact_path: Path
    snapshot: OwnedSourceSnapshot
    runtime_provenance: "SourceSnapshotRuntimeProvenance"


@dataclass(frozen=True)
class SourceSnapshotRuntimeProvenance:
    acquisition_profile_id: str
    git_executable: Path
    git_version: str
    python_implementation: str
    python_version: str
    os_name: str
    os_release: str


def create_source_snapshot(
    request: SourceSnapshotRequest,
    *,
    runtime: SourceSnapshotRuntime | None = None,
) -> SourceSnapshotPublication:
    """Acquire, validate, and create-new publish one exact SourceSnapshot."""

    return _create_source_snapshot(
        request,
        runtime=runtime or SourceSnapshotRuntime(),
        budget=DEFAULT_ACQUISITION_BUDGET,
        clock=time.monotonic,
        stage_hook=None,
    )


def _create_source_snapshot(
    request: SourceSnapshotRequest,
    *,
    runtime: SourceSnapshotRuntime,
    budget: SnapshotAcquisitionBudget,
    clock: Callable[[], float],
    stage_hook: Callable[[str], None] | None,
) -> SourceSnapshotPublication:
    try:
        if (
            not isinstance(request, SourceSnapshotRequest)
            or not isinstance(request.spec, SourceSnapshotSpec)
            or not isinstance(runtime, SourceSnapshotRuntime)
        ):
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
        _validate_tightened_budget(budget)
        algorithm, root_bytes = validate_source_snapshot_spec(request.spec)
        if request.output_directory.exists():
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.OUTPUT_ALREADY_EXISTS
            )
        deadline = clock() + (budget.wall_clock_ms / 1000.0)
        acquisition = acquire_git_snapshot(
            repository_path=request.repository_path,
            git_executable=runtime.git_executable,
            commit_oid=request.spec.commit_oid,
            analysis_root=root_bytes,
            budget=budget,
            clock=clock,
            stage_hook=stage_hook,
            deadline=deadline,
        )
        if acquisition.algorithm != algorithm:
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
        snapshot, deadline_check = _owned_snapshot(
            request,
            acquisition,
            budget,
            clock,
            stage_hook,
            deadline,
        )
        artifact_path = publish_source_snapshot(
            request.output_directory,
            snapshot,
            deadline_check=deadline_check,
            max_canonical_bytes=budget.max_canonical_artifact_bytes,
        )
        return SourceSnapshotPublication(
            artifact_path=artifact_path,
            snapshot=snapshot,
            runtime_provenance=SourceSnapshotRuntimeProvenance(
                acquisition_profile_id=budget.profile_id,
                git_executable=acquisition.git_executable,
                git_version=acquisition.git_version,
                python_implementation=platform.python_implementation(),
                python_version=platform.python_version(),
                os_name=platform.system(),
                os_release=platform.release(),
            ),
        )
    except SourceSnapshotError:
        raise
    except Exception as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.INTERNAL_ACQUISITION_ERROR
        ) from exc


def _validate_tightened_budget(budget: SnapshotAcquisitionBudget) -> None:
    if budget.profile_id != DEFAULT_ACQUISITION_BUDGET.profile_id:
        raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
    for name in (
        "wall_clock_ms",
        "max_commit_bytes",
        "max_tree_depth",
        "max_unique_tree_objects",
        "max_expanded_tree_entries",
        "max_single_tree_bytes",
        "max_total_unique_tree_bytes",
        "max_terminal_inventory_entries",
        "max_single_blob_bytes",
        "max_total_unique_blob_bytes",
        "max_canonical_artifact_bytes",
    ):
        value = getattr(budget, name)
        if type(value) is not int or value < 0:
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)
        if value > getattr(DEFAULT_ACQUISITION_BUDGET, name):
            raise SourceSnapshotError(SourceSnapshotFailureCode.INVALID_REQUEST)


def _owned_snapshot(
    request: SourceSnapshotRequest,
    acquisition: GitAcquisition,
    budget: SnapshotAcquisitionBudget,
    clock: Callable[[], float],
    stage_hook: Callable[[str], None] | None,
    deadline: float,
) -> tuple[OwnedSourceSnapshot, Callable[[str], None]]:

    def check(stage: str) -> None:
        if stage_hook is not None:
            stage_hook(stage)
        if clock() >= deadline:
            raise SourceSnapshotError(
                SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED
            )

    check("canonicalization-start")
    algorithm = acquisition.algorithm
    root = dict(request.spec.analysis_root)
    document = build_source_snapshot_document(
        repository_id=request.spec.repository_id,
        commit_oid=git_oid(algorithm, acquisition.commit_oid),
        commit_tree_oid=git_oid(algorithm, acquisition.commit_tree_oid),
        analysis_tree_oid=git_oid(algorithm, acquisition.analysis_tree_oid),
        analysis_root=root,
        inventory=[dict(item) for item in acquisition.inventory],
        max_canonical_bytes=budget.max_canonical_artifact_bytes,
        deadline_check=lambda: check("canonicalization"),
    )
    check("canonicalization-complete")
    canonical = validate_source_snapshot_document(
        document,
        max_canonical_bytes=budget.max_canonical_artifact_bytes,
        deadline_check=lambda: check("producer-validation"),
    )
    return (
        OwnedSourceSnapshot.create(
            document, canonical, acquisition.blob_bytes_by_oid
        ),
        check,
    )
