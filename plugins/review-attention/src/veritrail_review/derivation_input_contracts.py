from __future__ import annotations

import json
from dataclasses import dataclass, fields, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from veritrail_review.contracts import DEFAULT_ACQUISITION_BUDGET
from veritrail_review.errors import DerivationInputError, DerivationInputFailureCode


DERIVATION_INPUT_SAFETY_PROFILE_ID = "derivation-input/windows-reference/0.1"


@dataclass(frozen=True)
class DerivationInputSafetyProfile:
    """Trusted operational limits; none of these fields enter input identity."""

    profile_id: str = DERIVATION_INPUT_SAFETY_PROFILE_ID
    wall_clock_ms: int = 30_000
    max_source_snapshot_bytes: int = 67_108_864
    max_review_policy_bytes: int = 16_777_216
    max_derivation_profile_bytes: int = 65_536
    max_total_unique_blob_bytes: int = 268_435_456


DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE = DerivationInputSafetyProfile()


def tightened_derivation_input_safety_profile_for_testing(
    **overrides: int,
) -> DerivationInputSafetyProfile:
    """Return a test profile that can only tighten the frozen runtime limits."""

    valid_names = {item.name for item in fields(DerivationInputSafetyProfile)} - {
        "profile_id"
    }
    if set(overrides) - valid_names:
        raise DerivationInputError(
            DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST
        )
    for name, value in overrides.items():
        if type(value) is not int or value < 0:
            raise DerivationInputError(
                DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST
            )
        if value > getattr(DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE, name):
            raise DerivationInputError(
                DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST
            )
    return replace(DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE, **overrides)


@dataclass(frozen=True)
class DerivationInputRequest:
    source_snapshot_path: Path
    review_policy_path: Path
    derivation_profile_path: Path
    repository_path: Path

    def __post_init__(self) -> None:
        try:
            values = {
                item.name: Path(getattr(self, item.name))
                for item in fields(self)
            }
        except TypeError as exc:
            raise DerivationInputError(
                DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST
            ) from exc
        for name, value in values.items():
            object.__setattr__(self, name, value)


@dataclass(frozen=True)
class DerivationInputRuntime:
    """Trusted Git selection; never part of DerivationInputSet identity."""

    git_executable: Path | None = None

    def __post_init__(self) -> None:
        if self.git_executable is None:
            return
        try:
            object.__setattr__(self, "git_executable", Path(self.git_executable))
        except TypeError as exc:
            raise DerivationInputError(
                DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST
            ) from exc


@dataclass(frozen=True)
class DerivationInputSet:
    """Copy-owned immutable input snapshots for deterministic R1 derivation."""

    source_snapshot_canonical_bytes: bytes
    review_policy_canonical_bytes: bytes
    derivation_profile_canonical_bytes: bytes
    verified_blob_bytes_by_object_identity: Mapping[str, bytes]
    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    slice_policy_digest: str
    derivation_profile_digest: str

    @classmethod
    def create(
        cls,
        *,
        source_snapshot_canonical_bytes: bytes,
        review_policy_canonical_bytes: bytes,
        derivation_profile_canonical_bytes: bytes,
        verified_blob_bytes_by_object_identity: Mapping[str, bytes],
        source_snapshot_digest: str,
        policy_digest: str,
        analysis_scope_digest: str,
        slice_policy_digest: str,
        derivation_profile_digest: str,
    ) -> "DerivationInputSet":
        owned_blobs = {
            str(key): memoryview(value).tobytes()
            for key, value in verified_blob_bytes_by_object_identity.items()
        }
        return cls(
            memoryview(source_snapshot_canonical_bytes).tobytes(),
            memoryview(review_policy_canonical_bytes).tobytes(),
            memoryview(derivation_profile_canonical_bytes).tobytes(),
            MappingProxyType(owned_blobs),
            str(source_snapshot_digest),
            str(policy_digest),
            str(analysis_scope_digest),
            str(slice_policy_digest),
            str(derivation_profile_digest),
        )

    def source_snapshot_document_copy(self) -> dict[str, Any]:
        return _document_copy(self.source_snapshot_canonical_bytes)

    def review_policy_document_copy(self) -> dict[str, Any]:
        return _document_copy(self.review_policy_canonical_bytes)

    def derivation_profile_document_copy(self) -> dict[str, Any]:
        return _document_copy(self.derivation_profile_canonical_bytes)


def _document_copy(value: bytes) -> dict[str, Any]:
    document = json.loads(value)
    if not isinstance(document, dict):
        raise DerivationInputError(
            DerivationInputFailureCode.INTERNAL_INPUT_BINDING_ERROR
        )
    return document


def git_acquisition_budget_for_derivation_input(
    profile: DerivationInputSafetyProfile,
):
    """Project the input safety profile onto the frozen SourceSnapshot limits."""

    return replace(
        DEFAULT_ACQUISITION_BUDGET,
        wall_clock_ms=profile.wall_clock_ms,
        max_total_unique_blob_bytes=profile.max_total_unique_blob_bytes,
        max_canonical_artifact_bytes=profile.max_source_snapshot_bytes,
    )
