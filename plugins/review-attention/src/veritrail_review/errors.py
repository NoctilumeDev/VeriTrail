from __future__ import annotations

from enum import Enum


class SourceSnapshotFailureCode(str, Enum):
    INVALID_REQUEST = "INVALID_REQUEST"
    REPOSITORY_UNAVAILABLE = "REPOSITORY_UNAVAILABLE"
    UNSUPPORTED_OBJECT_FORMAT = "UNSUPPORTED_OBJECT_FORMAT"
    SOURCE_OBJECT_MISSING = "SOURCE_OBJECT_MISSING"
    SOURCE_OBJECT_TYPE_MISMATCH = "SOURCE_OBJECT_TYPE_MISMATCH"
    SOURCE_CONTENT_MISMATCH = "SOURCE_CONTENT_MISMATCH"
    MALFORMED_TREE = "MALFORMED_TREE"
    ANALYSIS_ROOT_NOT_TREE = "ANALYSIS_ROOT_NOT_TREE"
    SAFETY_BUDGET_EXHAUSTED = "SAFETY_BUDGET_EXHAUSTED"
    NONCONFORMANT_SNAPSHOT = "NONCONFORMANT_SNAPSHOT"
    OUTPUT_ALREADY_EXISTS = "OUTPUT_ALREADY_EXISTS"
    OUTPUT_PUBLICATION_FAILED = "OUTPUT_PUBLICATION_FAILED"
    INTERNAL_ACQUISITION_ERROR = "INTERNAL_ACQUISITION_ERROR"


_DEFAULT_MESSAGES = {
    SourceSnapshotFailureCode.INVALID_REQUEST: "the SourceSnapshot request is invalid",
    SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE: (
        "the local Git repository is unavailable"
    ),
    SourceSnapshotFailureCode.UNSUPPORTED_OBJECT_FORMAT: (
        "the repository object format is unsupported"
    ),
    SourceSnapshotFailureCode.SOURCE_OBJECT_MISSING: "a required local Git object is unavailable",
    SourceSnapshotFailureCode.SOURCE_OBJECT_TYPE_MISMATCH: (
        "a Git object has an unexpected type"
    ),
    SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH: (
        "Git object bytes do not match their declared identity"
    ),
    SourceSnapshotFailureCode.MALFORMED_TREE: "a Git tree object is malformed",
    SourceSnapshotFailureCode.ANALYSIS_ROOT_NOT_TREE: "the analysis root does not identify a tree",
    SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED: (
        "the SourceSnapshot acquisition safety budget was exhausted"
    ),
    SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT: (
        "the SourceSnapshot does not satisfy the frozen contract"
    ),
    SourceSnapshotFailureCode.OUTPUT_ALREADY_EXISTS: "the SourceSnapshot output already exists",
    SourceSnapshotFailureCode.OUTPUT_PUBLICATION_FAILED: (
        "the SourceSnapshot output could not be published atomically"
    ),
    SourceSnapshotFailureCode.INTERNAL_ACQUISITION_ERROR: "SourceSnapshot acquisition failed internally",
}


class SourceSnapshotError(Exception):
    """Typed, path-free failure returned by the SourceSnapshot boundary."""

    def __init__(
        self,
        code: SourceSnapshotFailureCode,
        message: str | None = None,
    ) -> None:
        self.code = code
        self.safe_message = message or _DEFAULT_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")
