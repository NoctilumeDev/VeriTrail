from __future__ import annotations

import copy
import re
from types import MappingProxyType
from typing import Any, Mapping

from veritrail.acceptance_plan import (
    CANONICALIZATION_PROFILE,
    observation_spec_digest,
    verify_sealed_acceptance_plan,
)
from veritrail.canonical import canonical_json_bytes, sha256_json

from veritrail_github.errors import ContractError


REQUEST_SCHEMA_VERSION = "0.1"
DERIVATION_CONTRACT = MappingProxyType(
    {"id": "acceptance-plan-to-github-request", "version": "0.1"}
)
OBSERVATION_CONTRACT = MappingProxyType(
    {"id": "github-observation-request", "version": "0.1"}
)
EVIDENCE_TYPE = "platform.github.api.snapshot"
NORMALIZATION_SEMANTICS_VERSION = "github-rest-facts/0.2"

ALLOWED_PROJECTIONS = frozenset(
    {
        "repository.identity",
        "repository.default_branch",
        "commit.identity",
        "pull_request.merge",
        "rules.required_checks",
        "checks.observed_runs",
        "release.identity",
        "release.assets",
        "tag.peeled_commit",
        "pages.metadata",
    }
)
ALLOWED_COORDINATES = frozenset(
    {
        "owner",
        "repository",
        "target_commit_sha",
        "pull_request_number",
        "release_tag",
        "branch",
    }
)

_OWNER_PATTERN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
_REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")
_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_REFERENCE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")

DEFAULT_COLLECTOR_POLICY: Mapping[str, Any] = MappingProxyType(
    {
        "schema_version": "0.1",
        "policy_id": "github-rest-read-only",
        "api_origin": "https://api.github.com",
        "api_version": "2026-03-10",
        "accept": "application/vnd.github+json",
        "user_agent": "veritrail-github-evidence/0.1",
        "conditional_get": False,
        "execution": "STRICT_SERIAL",
        "concurrency": 1,
        "per_page": 100,
        "max_pages_per_probe": 5,
        "max_total_requests": 24,
        "connect_timeout_ms": 5000,
        "read_timeout_ms": 15000,
        "total_collection_timeout_ms": 60000,
        "max_attempts_per_request": 3,
        "retry_schedule_ms": (1000, 3000),
        "max_redirects": 3,
        "same_origin_redirects_only": True,
    }
)

_POLICY_FIELDS = frozenset(DEFAULT_COLLECTOR_POLICY)
_REQUEST_FIELDS = frozenset(
    {
        "schema_version",
        "request_id",
        "plan_digest",
        "derivation_contract",
        "observation_spec",
        "observation_spec_digest",
        "collector_policy",
        "collector_policy_digest",
        "canonicalization_profile",
        "seal",
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


def _valid_ref(value: Any) -> bool:
    return isinstance(value, str) and bool(_REFERENCE_PATTERN.fullmatch(value))


def _validate_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    candidate = _copy_json(dict(policy))
    errors: list[str] = []
    unknown = sorted(set(candidate) - _POLICY_FIELDS)
    missing = sorted(_POLICY_FIELDS - set(candidate))
    if unknown:
        errors.append(f"collector_policy has unsupported fields: {', '.join(unknown)}")
    if missing:
        errors.append(f"collector_policy is missing fields: {', '.join(missing)}")
    fixed = {
        "schema_version": "0.1",
        "policy_id": "github-rest-read-only",
        "api_origin": "https://api.github.com",
        "api_version": "2026-03-10",
        "accept": "application/vnd.github+json",
        "user_agent": "veritrail-github-evidence/0.1",
        "conditional_get": False,
        "execution": "STRICT_SERIAL",
        "concurrency": 1,
        "same_origin_redirects_only": True,
    }
    for field, expected in fixed.items():
        if candidate.get(field) != expected:
            errors.append(f"collector_policy.{field} must equal the frozen P1 value")
    bounded_integers = {
        "per_page": (1, 100),
        "max_pages_per_probe": (1, 5),
        "max_total_requests": (1, 24),
        "connect_timeout_ms": (1, 5000),
        "read_timeout_ms": (1, 15000),
        "total_collection_timeout_ms": (1, 60000),
        "max_attempts_per_request": (1, 3),
        "max_redirects": (0, 3),
    }
    for field, (minimum, maximum) in bounded_integers.items():
        value = candidate.get(field)
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value < minimum
            or value > maximum
        ):
            errors.append(
                f"collector_policy.{field} must be an integer in [{minimum}, {maximum}]"
            )
    schedule = candidate.get("retry_schedule_ms")
    attempts = candidate.get("max_attempts_per_request")
    if (
        not isinstance(schedule, (list, tuple))
        or not isinstance(attempts, int)
        or len(schedule) != max(0, attempts - 1)
        or any(
            not isinstance(value, int)
            or isinstance(value, bool)
            or value < 0
            or value > 3000
            for value in schedule
        )
    ):
        errors.append(
            "collector_policy.retry_schedule_ms must contain one bounded delay per retry"
        )
    elif isinstance(schedule, tuple):
        candidate["retry_schedule_ms"] = list(schedule)
    _reject_floats(candidate, "collector_policy", errors)
    try:
        canonical_json_bytes(candidate)
    except (TypeError, ValueError) as exc:
        errors.append(f"collector_policy must be finite JSON: {exc}")
    if errors:
        raise ContractError(errors)
    return candidate


def collector_policy_digest(policy: Mapping[str, Any]) -> str:
    return sha256_json(_validate_policy(policy))


def _normalized_spec(spec: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if spec.get("contract") != dict(OBSERVATION_CONTRACT):
        errors.append(
            "observation spec contract must be github-observation-request 0.1"
        )
    if spec.get("evidence_type") != EVIDENCE_TYPE:
        errors.append(f"observation spec evidence_type must be {EVIDENCE_TYPE}")
    if spec.get("canonicalization_profile") != CANONICALIZATION_PROFILE:
        errors.append(
            f"observation spec canonicalization_profile must be {CANONICALIZATION_PROFILE}"
        )

    coordinates = spec.get("coordinates")
    if not isinstance(coordinates, dict):
        errors.append("observation spec coordinates must be an object")
        coordinates = {}
    else:
        unknown = sorted(set(coordinates) - ALLOWED_COORDINATES)
        if unknown:
            errors.append(f"coordinates has unsupported fields: {', '.join(unknown)}")
    owner = coordinates.get("owner")
    repository = coordinates.get("repository")
    commit_sha = coordinates.get("target_commit_sha")
    if not isinstance(owner, str) or not _OWNER_PATTERN.fullmatch(owner):
        errors.append("coordinates.owner must be an exact GitHub owner")
    if (
        not isinstance(repository, str)
        or not _REPOSITORY_PATTERN.fullmatch(repository)
        or repository.lower().endswith(".git")
    ):
        errors.append("coordinates.repository must be an exact GitHub repository name")
    if not isinstance(commit_sha, str) or not _SHA_PATTERN.fullmatch(commit_sha):
        errors.append(
            "coordinates.target_commit_sha must be a 40-character lowercase SHA"
        )

    for field in ("branch", "release_tag"):
        value = coordinates.get(field)
        if value is not None and (
            not isinstance(value, str)
            or not value
            or len(value) > 255
            or any(character in value for character in "\r\n\0")
        ):
            errors.append(f"coordinates.{field} must be a bounded exact reference")
    pr_number = coordinates.get("pull_request_number")
    if pr_number is not None and (
        not isinstance(pr_number, int) or isinstance(pr_number, bool) or pr_number < 1
    ):
        errors.append("coordinates.pull_request_number must be a positive integer")

    projections = spec.get("projections")
    if not isinstance(projections, list) or not projections:
        errors.append("observation spec projections must be a non-empty list")
        projections = []
    elif any(
        not isinstance(item, str) or item not in ALLOWED_PROJECTIONS
        for item in projections
    ):
        errors.append("observation spec projections contains an unsupported projection")
    elif len(projections) != len(set(projections)):
        errors.append("observation spec projections must not contain duplicates")

    projection_set = set(projections)
    if "pull_request.merge" in projection_set and pr_number is None:
        errors.append("pull_request.merge requires coordinates.pull_request_number")
    if projection_set.intersection(
        {"release.identity", "release.assets", "tag.peeled_commit"}
    ) and not coordinates.get("release_tag"):
        errors.append("release and tag projections require coordinates.release_tag")

    _reject_floats(spec, "observation spec", errors)
    if errors:
        raise ContractError(errors)

    normalized = _copy_json(spec)
    normalized["projections"] = sorted(projections)
    return normalized


def _find_spec(plan: dict[str, Any], observation_spec_id: str) -> dict[str, Any]:
    matches = [
        item
        for item in plan["observation_specs"]
        if item.get("id") == observation_spec_id
    ]
    if len(matches) != 1:
        raise ContractError(
            ["observation_spec_id must select exactly one sealed Plan observation spec"]
        )
    return matches[0]


def derive_observation_request(
    plan: dict[str, Any],
    observation_spec_id: str,
    request_id: str,
    *,
    collector_policy: Mapping[str, Any] = DEFAULT_COLLECTOR_POLICY,
) -> dict[str, Any]:
    """Mechanically derive and seal a P1 request before any network I/O."""

    try:
        verify_sealed_acceptance_plan(plan)
    except Exception as exc:
        raise ContractError(
            ["AcceptancePlan 0.1 must be valid and correctly sealed"]
        ) from exc
    if not _valid_ref(request_id):
        raise ContractError(["request_id must be a stable 1-128 character reference"])

    source_spec = _find_spec(plan, observation_spec_id)
    if source_spec.get("projections") != sorted(source_spec.get("projections", [])):
        raise ContractError(
            [
                "sealed Plan projections must already use canonical lexical order for Core 0.12.2 binding"
            ]
        )
    normalized_spec = _normalized_spec(source_spec)
    # Core 0.12.2 binds Evidence to this exact digest. Sorting makes the
    # set-like projection representation deterministic without inventing a
    # second plugin-owned spec identity.
    spec_digest = observation_spec_digest(normalized_spec)
    policy = _validate_policy(collector_policy)
    unsigned = {
        "schema_version": REQUEST_SCHEMA_VERSION,
        "request_id": request_id,
        "plan_digest": plan["seal"]["digest"],
        "derivation_contract": dict(DERIVATION_CONTRACT),
        "observation_spec": normalized_spec,
        "observation_spec_digest": spec_digest,
        "collector_policy": policy,
        "collector_policy_digest": sha256_json(policy),
        "canonicalization_profile": CANONICALIZATION_PROFILE,
    }
    return {
        **unsigned,
        "seal": {"algorithm": "sha256", "digest": sha256_json(unsigned)},
    }


def validate_observation_request(
    plan: dict[str, Any], request: dict[str, Any]
) -> dict[str, Any]:
    """Fail closed unless the request is the exact derivation from its Plan."""

    if not isinstance(request, dict):
        raise ContractError(["observation request must be an object"])
    errors: list[str] = []
    unknown = sorted(set(request) - _REQUEST_FIELDS)
    missing = sorted(_REQUEST_FIELDS - set(request))
    if unknown:
        errors.append(
            f"observation request has unsupported fields: {', '.join(unknown)}"
        )
    if missing:
        errors.append(f"observation request is missing fields: {', '.join(missing)}")
    if errors:
        raise ContractError(errors)

    spec = request.get("observation_spec")
    spec_id = spec.get("id") if isinstance(spec, dict) else None
    if not isinstance(spec_id, str):
        raise ContractError(["observation request spec must retain its sealed Plan id"])
    expected = derive_observation_request(
        plan,
        spec_id,
        request.get("request_id"),
        collector_policy=request.get("collector_policy"),
    )
    if canonical_json_bytes(request) != canonical_json_bytes(expected):
        raise ContractError(
            ["observation request does not match deterministic sealed Plan derivation"]
        )
    return _copy_json(expected)


def facts_digest(
    *,
    observation_spec_digest_value: str,
    source_coordinates: dict[str, Any],
    facts: dict[str, Any],
    normalization_semantics_version: str = NORMALIZATION_SEMANTICS_VERSION,
) -> str:
    """Identify normalized facts without request, policy, or session noise."""

    if not re.fullmatch(r"[0-9a-f]{64}", observation_spec_digest_value):
        raise ContractError(
            ["observation_spec_digest must be a lowercase SHA-256 digest"]
        )
    projection = {
        "canonicalization_profile": CANONICALIZATION_PROFILE,
        "observation_spec_digest": observation_spec_digest_value,
        "normalization_semantics_version": normalization_semantics_version,
        "source_coordinates": _copy_json(source_coordinates),
        "facts": _copy_json(facts),
    }
    errors: list[str] = []
    _reject_floats(projection, "facts identity", errors)
    try:
        digest = sha256_json(projection)
    except (TypeError, ValueError) as exc:
        errors.append(f"facts identity must be finite JSON: {exc}")
        digest = ""
    if errors:
        raise ContractError(errors)
    return digest
