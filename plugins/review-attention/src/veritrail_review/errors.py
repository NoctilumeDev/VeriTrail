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


class DerivationInputFailureCode(str, Enum):
    INVALID_DERIVATION_INPUT_REQUEST = "INVALID_DERIVATION_INPUT_REQUEST"
    INPUT_ARTIFACT_UNAVAILABLE = "INPUT_ARTIFACT_UNAVAILABLE"
    INPUT_ARTIFACT_NOT_ORDINARY_FILE = "INPUT_ARTIFACT_NOT_ORDINARY_FILE"
    INPUT_ARTIFACT_TOO_LARGE = "INPUT_ARTIFACT_TOO_LARGE"
    INPUT_REPOSITORY_UNAVAILABLE = "INPUT_REPOSITORY_UNAVAILABLE"
    INPUT_RUNTIME_UNAVAILABLE = "INPUT_RUNTIME_UNAVAILABLE"
    NONCONFORMANT_SOURCE_SNAPSHOT = "NONCONFORMANT_SOURCE_SNAPSHOT"
    NONCONFORMANT_REVIEW_POLICY = "NONCONFORMANT_REVIEW_POLICY"
    NONCONFORMANT_DERIVATION_PROFILE = "NONCONFORMANT_DERIVATION_PROFILE"
    POLICY_SNAPSHOT_MISMATCH = "POLICY_SNAPSHOT_MISMATCH"
    POLICY_PROFILE_MISMATCH = "POLICY_PROFILE_MISMATCH"
    POLICY_SCOPE_MISMATCH = "POLICY_SCOPE_MISMATCH"
    MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT = "MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT"
    SOURCE_REACQUISITION_MISMATCH = "SOURCE_REACQUISITION_MISMATCH"
    INPUT_SAFETY_BUDGET_EXHAUSTED = "INPUT_SAFETY_BUDGET_EXHAUSTED"
    INTERNAL_INPUT_BINDING_ERROR = "INTERNAL_INPUT_BINDING_ERROR"


_DERIVATION_INPUT_MESSAGES = {
    DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST: (
        "the derivation input request is invalid"
    ),
    DerivationInputFailureCode.INPUT_ARTIFACT_UNAVAILABLE: (
        "a required derivation input artifact is unavailable"
    ),
    DerivationInputFailureCode.INPUT_ARTIFACT_NOT_ORDINARY_FILE: (
        "a derivation input artifact is not an ordinary local file"
    ),
    DerivationInputFailureCode.INPUT_ARTIFACT_TOO_LARGE: (
        "a derivation input artifact exceeds its fixed safety limit"
    ),
    DerivationInputFailureCode.INPUT_REPOSITORY_UNAVAILABLE: (
        "the local input repository is unavailable"
    ),
    DerivationInputFailureCode.INPUT_RUNTIME_UNAVAILABLE: (
        "the trusted derivation input runtime is unavailable"
    ),
    DerivationInputFailureCode.NONCONFORMANT_SOURCE_SNAPSHOT: (
        "the SourceSnapshot input does not satisfy the frozen contract"
    ),
    DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY: (
        "the ReviewPolicy input does not satisfy the frozen contract"
    ),
    DerivationInputFailureCode.NONCONFORMANT_DERIVATION_PROFILE: (
        "the DerivationProfile input does not satisfy the frozen contract"
    ),
    DerivationInputFailureCode.POLICY_SNAPSHOT_MISMATCH: (
        "the ReviewPolicy is bound to a different SourceSnapshot"
    ),
    DerivationInputFailureCode.POLICY_PROFILE_MISMATCH: (
        "the ReviewPolicy is bound to a different DerivationProfile"
    ),
    DerivationInputFailureCode.POLICY_SCOPE_MISMATCH: (
        "the ReviewPolicy scope does not cover the SourceSnapshot exactly"
    ),
    DerivationInputFailureCode.MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT: (
        "the Python module root is outside the SourceSnapshot analysis root"
    ),
    DerivationInputFailureCode.SOURCE_REACQUISITION_MISMATCH: (
        "the local repository cannot reproduce the imported SourceSnapshot"
    ),
    DerivationInputFailureCode.INPUT_SAFETY_BUDGET_EXHAUSTED: (
        "the derivation input binding safety budget was exhausted"
    ),
    DerivationInputFailureCode.INTERNAL_INPUT_BINDING_ERROR: (
        "derivation input binding failed internally"
    ),
}


class DerivationInputError(Exception):
    """Typed, path-free failure returned by the derivation input boundary."""

    def __init__(
        self,
        code: DerivationInputFailureCode,
        message: str | None = None,
    ) -> None:
        self.code = code
        self.safe_message = message or _DERIVATION_INPUT_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")
