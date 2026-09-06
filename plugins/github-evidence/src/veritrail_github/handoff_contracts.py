from __future__ import annotations

import copy
import re
from collections.abc import Mapping
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_json

from veritrail_github.errors import ContractError


HANDOFF_SCHEMA_VERSION = "0.1"
HANDOFF_MANIFEST_KIND = "GITHUB_EVIDENCE_HANDOFF"
HANDOFF_COLLECTION_ORDER = ("github-api", "github-public-render")

_MANIFEST_FIELDS = frozenset(
    {"schema_version", "manifest_kind", "collection_order", "sides"}
)
_SIDE_FIELDS = frozenset(
    {
        "collector_role",
        "state",
        "evidence_path",
        "evidence_sha256",
        "error_code",
    }
)
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_SAFE_FILENAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{index}" for index in range(1, 10)}
    | {f"LPT{index}" for index in range(1, 10)}
)
_MISSING_ERROR_CODES = frozenset(
    {
        "COLLECTOR_FACTORY_ERROR",
        "COLLECTION_ERROR",
        "ARTIFACT_CONFORMANCE_ERROR",
        "SESSION_MISMATCH",
    }
)


def _copy_json(value: Any) -> Any:
    return copy.deepcopy(value)


def _reject_floats(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, float):
        errors.append(f"{path} must not contain floating-point values")
    elif isinstance(value, dict):
        for key, item in value.items():
            _reject_floats(item, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_floats(item, f"{path}[{index}]", errors)


def _valid_evidence_filename(value: Any) -> bool:
    if not isinstance(value, str) or not _SAFE_FILENAME_PATTERN.fullmatch(value):
        return False
    if value.endswith((".", " ")):
        return False
    device_name = value.split(".", 1)[0].upper()
    return device_name not in _WINDOWS_RESERVED_NAMES


def _validate_side(
    value: Any,
    *,
    index: int,
    expected_role: str,
    errors: list[str],
) -> dict[str, Any] | None:
    path = f"sides[{index}]"
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return None

    side = _copy_json(value)
    unknown = sorted(repr(field) for field in side if field not in _SIDE_FIELDS)
    missing = sorted(_SIDE_FIELDS - set(side))
    if unknown:
        errors.append(f"{path} has unsupported fields: {', '.join(unknown)}")
    if missing:
        errors.append(f"{path} is missing fields: {', '.join(missing)}")

    role = side.get("collector_role")
    if role != expected_role:
        errors.append(f"{path}.collector_role must equal {expected_role}")

    state = side.get("state")
    evidence_path = side.get("evidence_path")
    evidence_sha256 = side.get("evidence_sha256")
    error_code = side.get("error_code")

    if evidence_path is not None and not _valid_evidence_filename(evidence_path):
        errors.append(
            f"{path}.evidence_path must be one safe ordinary relative filename"
        )
    if evidence_sha256 is not None and (
        not isinstance(evidence_sha256, str)
        or not _SHA256_PATTERN.fullmatch(evidence_sha256)
    ):
        errors.append(f"{path}.evidence_sha256 must be a lowercase SHA-256")

    if state == "PUBLISHED":
        if not _valid_evidence_filename(evidence_path):
            errors.append(f"{path} PUBLISHED state requires evidence_path")
        if not isinstance(evidence_sha256, str) or not _SHA256_PATTERN.fullmatch(
            evidence_sha256
        ):
            errors.append(f"{path} PUBLISHED state requires evidence_sha256")
        if error_code is not None:
            errors.append(f"{path} PUBLISHED state requires null error_code")
    elif state == "COLLECTED_NOT_PUBLISHED":
        if evidence_path is not None:
            errors.append(
                f"{path} COLLECTED_NOT_PUBLISHED state requires null evidence_path"
            )
        if not isinstance(evidence_sha256, str) or not _SHA256_PATTERN.fullmatch(
            evidence_sha256
        ):
            errors.append(
                f"{path} COLLECTED_NOT_PUBLISHED state requires evidence_sha256"
            )
        if error_code != "PUBLISH_ERROR":
            errors.append(
                f"{path} COLLECTED_NOT_PUBLISHED state requires PUBLISH_ERROR"
            )
    elif state == "MISSING":
        if evidence_path is not None:
            errors.append(f"{path} MISSING state requires null evidence_path")
        if evidence_sha256 is not None:
            errors.append(f"{path} MISSING state requires null evidence_sha256")
        if error_code not in _MISSING_ERROR_CODES:
            errors.append(f"{path} MISSING state requires a frozen missing error_code")
    else:
        errors.append(
            f"{path}.state must be PUBLISHED, COLLECTED_NOT_PUBLISHED, or MISSING"
        )
    return side


def validate_handoff_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the frozen P3 handoff shape without interpreting Evidence."""

    if not isinstance(manifest, Mapping):
        raise ContractError(["handoff manifest must be an object"])
    candidate = _copy_json(dict(manifest))
    errors: list[str] = []

    unknown = sorted(
        repr(field) for field in candidate if field not in _MANIFEST_FIELDS
    )
    missing = sorted(_MANIFEST_FIELDS - set(candidate))
    if unknown:
        errors.append(f"handoff manifest has unsupported fields: {', '.join(unknown)}")
    if missing:
        errors.append(f"handoff manifest is missing fields: {', '.join(missing)}")

    if candidate.get("schema_version") != HANDOFF_SCHEMA_VERSION:
        errors.append("handoff manifest schema_version must equal 0.1")
    if candidate.get("manifest_kind") != HANDOFF_MANIFEST_KIND:
        errors.append(
            "handoff manifest manifest_kind must equal GITHUB_EVIDENCE_HANDOFF"
        )
    if candidate.get("collection_order") != list(HANDOFF_COLLECTION_ORDER):
        errors.append(
            "handoff manifest collection_order must equal the frozen P1 then P2 order"
        )

    sides = candidate.get("sides")
    verified_sides: list[dict[str, Any]] = []
    if not isinstance(sides, list) or len(sides) != len(HANDOFF_COLLECTION_ORDER):
        errors.append("handoff manifest sides must contain exactly two ordered entries")
    else:
        for index, expected_role in enumerate(HANDOFF_COLLECTION_ORDER):
            side = _validate_side(
                sides[index],
                index=index,
                expected_role=expected_role,
                errors=errors,
            )
            if side is not None:
                verified_sides.append(side)
        roles = [side.get("collector_role") for side in verified_sides]
        if len(roles) != len(set(roles)):
            errors.append(
                "handoff manifest sides must use two distinct collector roles"
            )

    _reject_floats(candidate, "handoff manifest", errors)
    try:
        canonical_json_bytes(candidate)
    except (TypeError, ValueError) as exc:
        errors.append(f"handoff manifest must contain finite JSON values: {exc}")
    if errors:
        raise ContractError(errors)
    return candidate


def handoff_manifest_digest(manifest: Mapping[str, Any]) -> str:
    """Return the canonical P3 manifest identity after closed-contract validation."""

    return sha256_json(validate_handoff_manifest(manifest))
