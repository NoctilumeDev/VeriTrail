from __future__ import annotations

import copy
import re
import unicodedata
from types import MappingProxyType
from typing import Any, Mapping
from urllib.parse import quote

from veritrail.acceptance_plan import (
    CANONICALIZATION_PROFILE,
    observation_spec_digest,
    verify_sealed_acceptance_plan,
)
from veritrail.canonical import canonical_json_bytes, sha256_json

from veritrail_github.errors import ContractError


PUBLIC_RENDER_REQUEST_SCHEMA_VERSION = "0.1"
PUBLIC_RENDER_DERIVATION_CONTRACT = MappingProxyType(
    {
        "id": "acceptance-plan-to-github-public-render-request",
        "version": "0.1",
    }
)
PUBLIC_RENDER_OBSERVATION_CONTRACT = MappingProxyType(
    {"id": "github-public-render-request", "version": "0.1"}
)
PUBLIC_RENDER_EVIDENCE_TYPE = "platform.github.public-render"

PUBLIC_RENDER_PROJECTIONS = frozenset(
    {
        "navigation.identity",
        "document.identity",
        "content.scope",
        "content.headings",
        "content.links",
        "content.literal_markers",
        "content.rendered_text_signature",
    }
)
PUBLIC_RENDER_TARGET_KINDS = frozenset(
    {
        "GITHUB_REPOSITORY_README",
        "GITHUB_MARKDOWN_FILE",
        "GITHUB_RELEASE",
        "GITHUB_PAGES_DEFAULT",
    }
)
PUBLIC_RENDER_VIEWPORTS = MappingProxyType(
    {
        "DESKTOP_1365X768": MappingProxyType(
            {"width": 1365, "height": 768, "device_scale_factor": 1}
        ),
        "NARROW_390X844": MappingProxyType(
            {"width": 390, "height": 844, "device_scale_factor": 1}
        ),
    }
)

DEFAULT_RENDER_POLICY: Mapping[str, Any] = MappingProxyType(
    {
        "engine": "CHROMIUM",
        "playwright_version": "1.62.0",
        "browser_distribution": "BUNDLED_MATCHING",
        "headless": True,
        "java_script_enabled": True,
        "accept_downloads": False,
        "network_profile": "github-public-readonly/0.1",
        "navigation_timeout_ms": 30000,
        "scope_timeout_ms": 10000,
        "settle_delay_ms": 1000,
        "sample_count": 3,
        "sample_interval_ms": 500,
        "max_redirects": 10,
        "max_requests": 512,
        "max_main_document_response_body_bytes": 8388608,
        "max_total_response_body_bytes": 33554432,
        "response_body_read_chunk_bytes": 65536,
        "content_encoding": "IDENTITY_ONLY",
        "max_elapsed_ms": 45000,
        "retries": 0,
        "service_workers": "BLOCK",
        "http_cache": "DISABLED",
    }
)

_OWNER_PATTERN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
_REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")
_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_REFERENCE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_PREENCODED_SEPARATOR_PATTERN = re.compile(r"%(?:2f|5c)", re.IGNORECASE)
_PREENCODED_OCTET_PATTERN = re.compile(r"%[0-9a-fA-F]{2}")

_COMMON_COORDINATES = frozenset(
    {"owner", "repository", "target_kind", "viewport_profile"}
)
_TARGET_COORDINATES = MappingProxyType(
    {
        "GITHUB_REPOSITORY_README": frozenset(),
        "GITHUB_MARKDOWN_FILE": frozenset(
            {"target_commit_sha", "repository_path"}
        ),
        "GITHUB_RELEASE": frozenset({"release_tag"}),
        "GITHUB_PAGES_DEFAULT": frozenset({"site_kind", "pages_path"}),
    }
)
_REQUEST_FIELDS = frozenset(
    {
        "schema_version",
        "request_id",
        "plan_digest",
        "derivation_contract",
        "observation_spec",
        "observation_spec_digest",
        "render_policy",
        "render_policy_digest",
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


def _valid_request_id(value: Any) -> bool:
    return isinstance(value, str) and bool(_REQUEST_ID_PATTERN.fullmatch(value))


def _bounded_integer(
    candidate: Mapping[str, Any],
    field: str,
    minimum: int,
    maximum: int,
    errors: list[str],
) -> None:
    value = candidate.get(field)
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value < minimum
        or value > maximum
    ):
        errors.append(
            f"render_policy.{field} must be an integer in [{minimum}, {maximum}]"
        )


def _validate_render_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(policy, Mapping):
        raise ContractError(["render_policy must be an object"])
    candidate = _copy_json(dict(policy))
    errors: list[str] = []
    expected_fields = set(DEFAULT_RENDER_POLICY)
    string_fields = {key for key in candidate if isinstance(key, str)}
    if len(string_fields) != len(candidate):
        errors.append("render_policy object keys must be strings")
    unknown = sorted(string_fields - expected_fields)
    missing = sorted(expected_fields - set(candidate))
    if unknown:
        errors.append(f"render_policy has unsupported fields: {', '.join(unknown)}")
    if missing:
        errors.append(f"render_policy is missing fields: {', '.join(missing)}")

    fixed = {
        "engine": "CHROMIUM",
        "playwright_version": "1.62.0",
        "browser_distribution": "BUNDLED_MATCHING",
        "headless": True,
        "java_script_enabled": True,
        "accept_downloads": False,
        "network_profile": "github-public-readonly/0.1",
        "sample_count": 3,
        "content_encoding": "IDENTITY_ONLY",
        "retries": 0,
        "service_workers": "BLOCK",
        "http_cache": "DISABLED",
    }
    for field, expected in fixed.items():
        if candidate.get(field) != expected:
            errors.append(f"render_policy.{field} must equal the frozen P2 value")

    for field, minimum, maximum in (
        ("navigation_timeout_ms", 1, 30000),
        ("scope_timeout_ms", 1, 10000),
        ("settle_delay_ms", 0, 1000),
        ("sample_interval_ms", 1, 500),
        ("max_redirects", 0, 10),
        ("max_requests", 1, 512),
        ("max_main_document_response_body_bytes", 1, 8388608),
        ("max_total_response_body_bytes", 1, 33554432),
        ("response_body_read_chunk_bytes", 1, 65536),
        ("max_elapsed_ms", 1, 45000),
    ):
        _bounded_integer(candidate, field, minimum, maximum, errors)
    main_limit = candidate.get("max_main_document_response_body_bytes")
    total_limit = candidate.get("max_total_response_body_bytes")
    if (
        isinstance(main_limit, int)
        and not isinstance(main_limit, bool)
        and isinstance(total_limit, int)
        and not isinstance(total_limit, bool)
        and main_limit > total_limit
    ):
        errors.append(
            "render_policy main-document response-body budget cannot exceed total budget"
        )

    _reject_floats(candidate, "render_policy", errors)
    try:
        canonical_json_bytes(candidate)
    except (TypeError, ValueError) as exc:
        errors.append(f"render_policy must be finite JSON: {exc}")
    if errors:
        raise ContractError(errors)
    return candidate


def render_policy_digest(policy: Mapping[str, Any]) -> str:
    return sha256_json(_validate_render_policy(policy))


def normalize_rendered_text(value: str) -> str:
    """Apply the frozen P2 innerText/literal normalization profile."""

    if not isinstance(value, str):
        raise ContractError(["render text must be a string"])
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ContractError(["render text must contain Unicode scalar values"])
    normalized = unicodedata.normalize("NFC", value).replace("\r\n", "\n")
    normalized = normalized.replace("\r", "\n")
    lines: list[str] = []
    for line in normalized.split("\n"):
        collapsed = re.sub(r"\s+", " ", line, flags=re.UNICODE).strip()
        if collapsed:
            lines.append(collapsed)
    return "\n".join(lines)


def _validate_owner_repository(
    owner: Any, repository: Any, errors: list[str]
) -> None:
    if not isinstance(owner, str) or not _OWNER_PATTERN.fullmatch(owner):
        errors.append("coordinates.owner must be an exact GitHub owner")
    if (
        not isinstance(repository, str)
        or not _REPOSITORY_PATTERN.fullmatch(repository)
        or repository in {".", ".."}
        or repository.lower().endswith(".git")
    ):
        errors.append("coordinates.repository must be an exact GitHub repository name")


def _has_control_character(value: str) -> bool:
    return any(unicodedata.category(character) == "Cc" for character in value)


def _has_surrogate(value: str) -> bool:
    return any(0xD800 <= ord(character) <= 0xDFFF for character in value)


def _validate_relative_path(
    value: Any,
    field: str,
    errors: list[str],
    *,
    allow_empty_root: bool,
) -> None:
    if not isinstance(value, str):
        errors.append(f"coordinates.{field} must be a relative POSIX path")
        return
    if value == "" and allow_empty_root:
        return
    if (
        not value
        or value.startswith("/")
        or value.endswith("/")
        or "\\" in value
        or "?" in value
        or "#" in value
        or _has_control_character(value)
        or _has_surrogate(value)
        or _PREENCODED_SEPARATOR_PATTERN.search(value)
    ):
        errors.append(f"coordinates.{field} must be a safe relative POSIX path")
        return
    segments = value.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        errors.append(f"coordinates.{field} contains an unsafe path segment")


def _validate_release_tag(value: Any, errors: list[str]) -> None:
    if not isinstance(value, str) or not _REFERENCE_PATTERN.fullmatch(value):
        errors.append("coordinates.release_tag must be a bounded exact GitHub tag")
        return
    segments = value.split("/")
    if (
        any(segment in {"", ".", ".."} for segment in segments)
        or _PREENCODED_OCTET_PATTERN.search(value)
    ):
        errors.append("coordinates.release_tag contains an unsafe path segment")


def _normalize_literal_markers(
    coordinates: Mapping[str, Any], projections: list[str], errors: list[str]
) -> None:
    projected = "content.literal_markers" in projections
    present = "literal_markers" in coordinates
    if projected != present:
        errors.append(
            "coordinates.literal_markers must be present exactly when its projection is requested"
        )
        return
    if not present:
        return
    markers = coordinates.get("literal_markers")
    if not isinstance(markers, list) or len(markers) > 32:
        errors.append("coordinates.literal_markers must contain at most 32 literals")
        return
    for index, marker in enumerate(markers):
        if not isinstance(marker, str):
            errors.append(f"coordinates.literal_markers[{index}] must be a string")
            continue
        try:
            normalized = normalize_rendered_text(marker)
        except ContractError:
            errors.append(
                f"coordinates.literal_markers[{index}] must contain Unicode scalar values"
            )
            continue
        if not normalized or len(normalized) > 256:
            errors.append(
                f"coordinates.literal_markers[{index}] must normalize to 1..256 Unicode scalars"
            )
        elif marker != normalized:
            errors.append(
                f"coordinates.literal_markers[{index}] must already use the frozen text normalization"
            )


def _normalized_coordinates(
    coordinates: Any, projections: list[str]
) -> dict[str, Any]:
    if not isinstance(coordinates, dict):
        raise ContractError(["observation spec coordinates must be an object"])
    candidate = _copy_json(coordinates)
    errors: list[str] = []
    target_kind = candidate.get("target_kind")
    if target_kind not in PUBLIC_RENDER_TARGET_KINDS:
        errors.append("coordinates.target_kind is unsupported")
        allowed = set(_COMMON_COORDINATES)
    else:
        allowed = set(_COMMON_COORDINATES | _TARGET_COORDINATES[target_kind])
    if "content.literal_markers" in projections:
        allowed.add("literal_markers")
    string_fields = {key for key in candidate if isinstance(key, str)}
    if len(string_fields) != len(candidate):
        errors.append("coordinates object keys must be strings")
    unknown = sorted(string_fields - allowed)
    missing = sorted(allowed - set(candidate))
    if unknown:
        errors.append(f"coordinates has unsupported fields: {', '.join(unknown)}")
    if missing:
        errors.append(f"coordinates is missing fields: {', '.join(missing)}")

    owner = candidate.get("owner")
    repository = candidate.get("repository")
    _validate_owner_repository(owner, repository, errors)
    if candidate.get("viewport_profile") not in PUBLIC_RENDER_VIEWPORTS:
        errors.append("coordinates.viewport_profile is unsupported")
    _normalize_literal_markers(candidate, projections, errors)

    if target_kind == "GITHUB_MARKDOWN_FILE":
        if not isinstance(candidate.get("target_commit_sha"), str) or not _SHA_PATTERN.fullmatch(
            candidate.get("target_commit_sha", "")
        ):
            errors.append(
                "coordinates.target_commit_sha must be a 40-character lowercase SHA"
            )
        _validate_relative_path(
            candidate.get("repository_path"),
            "repository_path",
            errors,
            allow_empty_root=False,
        )
    elif target_kind == "GITHUB_RELEASE":
        _validate_release_tag(candidate.get("release_tag"), errors)
    elif target_kind == "GITHUB_PAGES_DEFAULT":
        site_kind = candidate.get("site_kind")
        if site_kind not in {"OWNER", "PROJECT"}:
            errors.append("coordinates.site_kind must be OWNER or PROJECT")
        _validate_relative_path(
            candidate.get("pages_path"),
            "pages_path",
            errors,
            allow_empty_root=True,
        )
        if (
            site_kind == "OWNER"
            and isinstance(owner, str)
            and isinstance(repository, str)
            and repository.casefold() != f"{owner}.github.io".casefold()
        ):
            errors.append(
                "OWNER Pages requires repository to equal {owner}.github.io"
            )

    _reject_floats(candidate, "coordinates", errors)
    if errors:
        raise ContractError(errors)
    return candidate


def _normalized_spec(spec: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if spec.get("contract") != dict(PUBLIC_RENDER_OBSERVATION_CONTRACT):
        errors.append(
            "observation spec contract must be github-public-render-request 0.1"
        )
    if spec.get("evidence_type") != PUBLIC_RENDER_EVIDENCE_TYPE:
        errors.append(
            f"observation spec evidence_type must be {PUBLIC_RENDER_EVIDENCE_TYPE}"
        )
    if spec.get("canonicalization_profile") != CANONICALIZATION_PROFILE:
        errors.append(
            f"observation spec canonicalization_profile must be {CANONICALIZATION_PROFILE}"
        )
    projections = spec.get("projections")
    if not isinstance(projections, list) or not projections:
        errors.append("observation spec projections must be a non-empty list")
        projections = []
    elif any(
        not isinstance(item, str) or item not in PUBLIC_RENDER_PROJECTIONS
        for item in projections
    ):
        errors.append("observation spec projections contains an unsupported projection")
    elif len(projections) != len(set(projections)):
        errors.append("observation spec projections must not contain duplicates")
    elif projections != sorted(projections):
        errors.append(
            "sealed Plan projections must already use canonical lexical order for Core 0.12.2 binding"
        )
    if errors:
        raise ContractError(errors)
    coordinates = _normalized_coordinates(spec.get("coordinates"), projections)
    normalized = _copy_json(spec)
    normalized["coordinates"] = coordinates
    normalized["projections"] = list(projections)
    _reject_floats(normalized, "observation spec", errors)
    if errors:
        raise ContractError(errors)
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


def public_render_target_url(coordinates: Mapping[str, Any]) -> str:
    """Derive the only allowed HTTPS target from validated structured coordinates."""

    projections = (
        ["content.literal_markers"]
        if "literal_markers" in coordinates
        else ["navigation.identity"]
    )
    candidate = _normalized_coordinates(dict(coordinates), projections)
    owner = candidate["owner"]
    repository = candidate["repository"]
    kind = candidate["target_kind"]
    github_base = f"https://github.com/{quote(owner, safe='')}/{quote(repository, safe='')}"
    if kind == "GITHUB_REPOSITORY_README":
        return github_base
    if kind == "GITHUB_MARKDOWN_FILE":
        path = _encode_path(candidate["repository_path"])
        return f"{github_base}/blob/{candidate['target_commit_sha']}/{path}"
    if kind == "GITHUB_RELEASE":
        tag = _encode_path(candidate["release_tag"])
        return f"{github_base}/releases/tag/{tag}"

    pages_path = candidate["pages_path"]
    owner_host = owner.lower()
    if candidate["site_kind"] == "OWNER":
        pages_base = f"https://{owner_host}.github.io/"
    else:
        pages_base = (
            f"https://{owner_host}.github.io/{quote(repository, safe='')}/"
        )
    return pages_base if pages_path == "" else pages_base + _encode_path(pages_path)


def _encode_path(value: str) -> str:
    return "/".join(quote(segment, safe="") for segment in value.split("/"))


def derive_public_render_request(
    plan: dict[str, Any],
    observation_spec_id: str,
    request_id: str,
    *,
    render_policy: Mapping[str, Any] = DEFAULT_RENDER_POLICY,
) -> dict[str, Any]:
    """Mechanically derive and seal a P2 request before browser or network I/O."""

    try:
        verify_sealed_acceptance_plan(plan)
    except Exception as exc:
        raise ContractError(
            ["AcceptancePlan 0.1 must be valid and correctly sealed"]
        ) from exc
    if not _valid_request_id(request_id):
        raise ContractError(["request_id must be a stable 1-128 character reference"])
    source_spec = _find_spec(plan, observation_spec_id)
    normalized_spec = _normalized_spec(source_spec)
    # Derive the URL now so unsafe or unrepresentable coordinates fail before
    # a collection session or browser is created. The URL remains derived data,
    # not a caller-controlled request field.
    public_render_target_url(normalized_spec["coordinates"])
    spec_digest = observation_spec_digest(normalized_spec)
    policy = _validate_render_policy(render_policy)
    unsigned = {
        "schema_version": PUBLIC_RENDER_REQUEST_SCHEMA_VERSION,
        "request_id": request_id,
        "plan_digest": plan["seal"]["digest"],
        "derivation_contract": dict(PUBLIC_RENDER_DERIVATION_CONTRACT),
        "observation_spec": normalized_spec,
        "observation_spec_digest": spec_digest,
        "render_policy": policy,
        "render_policy_digest": sha256_json(policy),
        "canonicalization_profile": CANONICALIZATION_PROFILE,
    }
    return {
        **unsigned,
        "seal": {"algorithm": "sha256", "digest": sha256_json(unsigned)},
    }


def validate_public_render_request(
    plan: dict[str, Any], request: dict[str, Any]
) -> dict[str, Any]:
    """Fail closed unless request exactly equals its sealed Plan derivation."""

    if not isinstance(request, dict):
        raise ContractError(["public render request must be an object"])
    errors: list[str] = []
    string_fields = {key for key in request if isinstance(key, str)}
    if len(string_fields) != len(request):
        errors.append("public render request object keys must be strings")
    unknown = sorted(string_fields - _REQUEST_FIELDS)
    missing = sorted(_REQUEST_FIELDS - set(request))
    if unknown:
        errors.append(
            f"public render request has unsupported fields: {', '.join(unknown)}"
        )
    if missing:
        errors.append(
            f"public render request is missing fields: {', '.join(missing)}"
        )
    if errors:
        raise ContractError(errors)
    spec = request.get("observation_spec")
    spec_id = spec.get("id") if isinstance(spec, dict) else None
    if not isinstance(spec_id, str):
        raise ContractError(
            ["public render request spec must retain its sealed Plan id"]
        )
    expected = derive_public_render_request(
        plan,
        spec_id,
        request.get("request_id"),
        render_policy=request.get("render_policy"),
    )
    if canonical_json_bytes(request) != canonical_json_bytes(expected):
        raise ContractError(
            ["public render request does not match deterministic sealed Plan derivation"]
        )
    return _copy_json(expected)
