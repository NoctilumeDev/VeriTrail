from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from veritrail.argument_policy import is_forbidden_inline_literal
from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.errors import SafetyError, ValidationError
from veritrail.jsonio import load_json_object
from veritrail.privacy import redact_value

IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
PATH_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_RESERVED_PATH_NAMES = {
    "aux",
    "clock$",
    "con",
    "nul",
    "prn",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}

PROFILE_V01_FIELDS = {
    "schema_version",
    "profile_id",
    "version",
    "platform",
    "cold_state",
    "nodes",
    "start_order",
    "teardown_order",
    "application_node_id",
    "subject_watch_roots",
    "max_watch_files",
    "max_watch_total_bytes",
    "lifecycle_timeout_ms",
    "seal",
}
PROFILE_V02_FIELDS = PROFILE_V01_FIELDS | {"topology"}
# Backward-compatible name for the frozen 0.1 contract.
PROFILE_FIELDS = PROFILE_V01_FIELDS
NODE_FIELDS = {
    "node_id",
    "role",
    "adapter",
    "depends_on",
    "tool_binding",
    "arguments",
    "working_directory",
    "environment",
    "port",
    "readiness",
    "limits",
    "shutdown",
}
ARGUMENT_FIELDS = {"literal", "run_work_path", "node_port", "node_origin"}
ENVIRONMENT_FIELDS = {"inherit", "set"}
READINESS_FIELDS = {
    "adapter",
    "path",
    "expected_status",
    "attempt_timeout_ms",
    "total_timeout_ms",
    "interval_ms",
    "consecutive_successes",
    "max_response_bytes",
}
LIMIT_FIELDS = {
    "max_stdout_bytes",
    "max_stderr_bytes",
    "max_processes",
    "max_job_memory_mb",
}
SHUTDOWN_FIELDS = {
    "adapter",
    "process_release_timeout_ms",
    "port_release_timeout_ms",
    "reader_shutdown_timeout_ms",
}


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _reject_unknown_fields(
    value: dict[str, Any], allowed: set[str], path: str, errors: list[str]
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        errors.append(f"{path} has unsupported fields: {', '.join(unknown)}")


def _validate_identifier(value: Any, path: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not IDENTIFIER_PATTERN.fullmatch(value):
        errors.append(f"{path} must be a 2-64 character lowercase identifier")
        return None
    return value


def _validate_relative_path(
    value: Any, path: str, errors: list[str], *, allow_root: bool
) -> tuple[str, ...] | None:
    if value == "." and allow_root:
        return ()
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or value.startswith("/")
        or re.match(r"^[A-Za-z]:", value)
    ):
        errors.append(f"{path} must be a safe relative POSIX path")
        return None
    parts = value.split("/")
    if not 1 <= len(parts) <= 8:
        errors.append(f"{path} must contain 1-8 safe path segments")
        return None
    for part in parts:
        basename = part.split(".", 1)[0].casefold()
        if (
            part in {"", ".", ".."}
            or not PATH_SEGMENT_PATTERN.fullmatch(part)
            or basename in WINDOWS_RESERVED_PATH_NAMES
        ):
            errors.append(f"{path} must contain 1-8 safe path segments")
            return None
    return tuple(part.casefold() for part in parts)


def _validate_non_overlapping_roots(value: Any, errors: list[str]) -> None:
    normalized: list[tuple[str, ...]] = []
    if not isinstance(value, list) or not 1 <= len(value) <= 8:
        errors.append("subject_watch_roots must contain 1-8 safe relative paths")
        return
    for index, root in enumerate(value):
        parsed = _validate_relative_path(
            root, f"subject_watch_roots[{index}]", errors, allow_root=True
        )
        if parsed is not None:
            normalized.append(parsed)
    for index, current in enumerate(normalized):
        for previous in normalized[:index]:
            shorter, longer = sorted((current, previous), key=len)
            if longer[: len(shorter)] == shorter:
                errors.append("subject_watch_roots must be unique and non-overlapping")
                return


def _validate_environment(value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    _reject_unknown_fields(value, ENVIRONMENT_FIELDS, prefix, errors)
    inherit = value.get("inherit")
    seen: set[str] = set()
    if not isinstance(inherit, list) or len(inherit) > 2:
        errors.append(f"{prefix}.inherit must be a list with at most 2 entries")
    else:
        for index, name in enumerate(inherit):
            normalized = name.upper() if isinstance(name, str) else None
            if normalized not in {"SYSTEMROOT", "WINDIR"}:
                errors.append(f"{prefix}.inherit[{index}] must be SYSTEMROOT or WINDIR")
            elif normalized in seen:
                errors.append(f"{prefix}.inherit[{index}] duplicates {normalized}")
            else:
                seen.add(normalized)
    if value.get("set") not in ({}, {"PYTHONDONTWRITEBYTECODE": "1"}):
        errors.append(
            f"{prefix}.set must be empty or exactly PYTHONDONTWRITEBYTECODE=1"
        )


def _validate_arguments(
    value: Any,
    *,
    prefix: str,
    node_id: str | None,
    tool_binding: object,
    allowed_node_refs: set[str],
    errors: list[str],
) -> None:
    if not isinstance(value, list) or not 1 <= len(value) <= 128:
        errors.append(f"{prefix} must contain 1-128 structured arguments")
        return
    for index, argument in enumerate(value):
        item_path = f"{prefix}[{index}]"
        if not isinstance(argument, dict):
            errors.append(f"{item_path} must be an object")
            continue
        _reject_unknown_fields(argument, ARGUMENT_FIELDS, item_path, errors)
        present = [field for field in ARGUMENT_FIELDS if field in argument]
        if len(present) != 1:
            errors.append(
                f"{item_path} must contain exactly one typed argument field"
            )
            continue
        field = present[0]
        if field == "literal":
            literal = argument[field]
            if (
                not isinstance(literal, str)
                or len(literal) > 4096
                or any(ord(character) < 32 or ord(character) == 127 for character in literal)
            ):
                errors.append(
                    f"{item_path}.literal must be a control-free string up to 4096 characters"
                )
            elif redact_value(literal)[1]:
                errors.append(
                    f"{item_path}.literal must not contain secrets or personal identifiers"
                )
            elif is_forbidden_inline_literal(literal, tool_binding):
                errors.append(f"{item_path}.literal uses a forbidden inline or Shell entry point")
        elif field == "run_work_path":
            segments = argument[field]
            if not isinstance(segments, list) or not 1 <= len(segments) <= 8:
                errors.append(f"{item_path}.run_work_path must contain 1-8 safe path segments")
                continue
            for segment in segments:
                basename = segment.split(".", 1)[0].casefold() if isinstance(segment, str) else ""
                if (
                    not isinstance(segment, str)
                    or not PATH_SEGMENT_PATTERN.fullmatch(segment)
                    or basename in WINDOWS_RESERVED_PATH_NAMES
                ):
                    errors.append(
                        f"{item_path}.run_work_path must contain individual safe segments"
                    )
                    break
        else:
            reference = argument[field]
            if not isinstance(reference, str) or not IDENTIFIER_PATTERN.fullmatch(reference):
                errors.append(f"{item_path}.{field} must reference a declared node id")
            elif reference not in allowed_node_refs:
                errors.append(
                    f"{item_path}.{field} may reference only {node_id!r} or an already declared dependency"
                )


def _validate_readiness(value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    _reject_unknown_fields(value, READINESS_FIELDS, prefix, errors)
    if value.get("adapter") != "HTTP_GET_LOOPBACK_OWNED_PID":
        errors.append(f"{prefix}.adapter must be HTTP_GET_LOOPBACK_OWNED_PID")
    path = value.get("path")
    valid_path = isinstance(path, str) and 1 <= len(path) <= 2048
    if valid_path:
        try:
            parsed = urlsplit(path)
        except ValueError:
            valid_path = False
        else:
            valid_path = (
                path.startswith("/")
                and not path.startswith("//")
                and not parsed.scheme
                and not parsed.netloc
                and not parsed.query
                and not parsed.fragment
                and not any(ord(character) < 32 or ord(character) == 127 for character in path)
            )
    if not valid_path:
        errors.append(f"{prefix}.path must be a safe absolute URL path without query or fragment")
    if value.get("expected_status") != 200:
        errors.append(f"{prefix}.expected_status must be 200")
    ranges = {
        "attempt_timeout_ms": (100, 2_000),
        "total_timeout_ms": (500, 30_000),
        "interval_ms": (20, 1_000),
        "max_response_bytes": (1, 65_536),
    }
    for field, (minimum, maximum) in ranges.items():
        item = value.get(field)
        if not _is_integer(item) or not minimum <= item <= maximum:
            errors.append(f"{prefix}.{field} must be an integer from {minimum} to {maximum}")
    attempt = value.get("attempt_timeout_ms")
    total = value.get("total_timeout_ms")
    if _is_integer(attempt) and _is_integer(total) and total <= attempt:
        errors.append(f"{prefix}.total_timeout_ms must be greater than attempt_timeout_ms")
    if value.get("consecutive_successes") != 2:
        errors.append(f"{prefix}.consecutive_successes must be 2")


def _validate_limits(value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    _reject_unknown_fields(value, LIMIT_FIELDS, prefix, errors)
    ranges = {
        "max_stdout_bytes": (1, 1_048_576),
        "max_stderr_bytes": (1, 1_048_576),
        "max_processes": (1, 32),
        "max_job_memory_mb": (64, 2048),
    }
    for field, (minimum, maximum) in ranges.items():
        item = value.get(field)
        if not _is_integer(item) or not minimum <= item <= maximum:
            errors.append(f"{prefix}.{field} must be an integer from {minimum} to {maximum}")


def _validate_shutdown(value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    _reject_unknown_fields(value, SHUTDOWN_FIELDS, prefix, errors)
    if value.get("adapter") != "JOB_TERMINATE_AFTER_CAPTURE":
        errors.append(f"{prefix}.adapter must be JOB_TERMINATE_AFTER_CAPTURE")
    for field in (
        "process_release_timeout_ms",
        "port_release_timeout_ms",
        "reader_shutdown_timeout_ms",
    ):
        item = value.get(field)
        if not _is_integer(item) or not 100 <= item <= 10_000:
            errors.append(f"{prefix}.{field} must be an integer from 100 to 10000")


def validate_project_profile(profile: dict[str, Any]) -> None:
    errors: list[str] = []
    schema_version = profile.get("schema_version")
    if schema_version == "0.1":
        _reject_unknown_fields(profile, PROFILE_V01_FIELDS, "ProjectProfile", errors)
    elif schema_version == "0.2":
        _reject_unknown_fields(profile, PROFILE_V02_FIELDS, "ProjectProfile", errors)
        if profile.get("topology") != "SINGLE_APPLICATION":
            errors.append("ProjectProfile 0.2 topology must be SINGLE_APPLICATION")
    else:
        _reject_unknown_fields(profile, PROFILE_V02_FIELDS, "ProjectProfile", errors)
        errors.append("ProjectProfile.schema_version must be '0.1' or '0.2'")
    _validate_identifier(profile.get("profile_id"), "profile_id", errors)
    version = profile.get("version")
    if not _is_integer(version) or version < 1:
        errors.append("version must be a positive integer")
    if profile.get("platform") != "WINDOWS_11":
        errors.append("platform must be WINDOWS_11")
    if profile.get("cold_state") != "C1_PROCESS_COLD":
        errors.append("cold_state must be C1_PROCESS_COLD")

    nodes = profile.get("nodes")
    node_map: dict[str, dict[str, Any]] = {}
    role_map: dict[str, str] = {}
    expected_node_count = 1 if schema_version == "0.2" else 2
    if not isinstance(nodes, list) or len(nodes) != expected_node_count:
        errors.append(
            "nodes must contain exactly one APPLICATION entry"
            if schema_version == "0.2"
            else "nodes must contain exactly two entries"
        )
    else:
        for index, node in enumerate(nodes):
            prefix = f"nodes[{index}]"
            if not isinstance(node, dict):
                errors.append(f"{prefix} must be an object")
                continue
            _reject_unknown_fields(node, NODE_FIELDS, prefix, errors)
            node_id = _validate_identifier(node.get("node_id"), f"{prefix}.node_id", errors)
            if node_id is not None:
                if node_id in node_map:
                    errors.append(f"{prefix}.node_id duplicates {node_id!r}")
                else:
                    node_map[node_id] = node
            role = node.get("role")
            allowed_roles = {"APPLICATION"} if schema_version == "0.2" else {
                "DEPENDENCY",
                "APPLICATION",
            }
            if role not in allowed_roles:
                errors.append(
                    f"{prefix}.role must be APPLICATION"
                    if schema_version == "0.2"
                    else f"{prefix}.role must be DEPENDENCY or APPLICATION"
                )
            elif role in role_map:
                errors.append(f"nodes must contain exactly one {role}")
            elif node_id is not None:
                role_map[role] = node_id
            if node.get("adapter") != "TRUSTED_PROCESS_SERVICE":
                errors.append(f"{prefix}.adapter must be TRUSTED_PROCESS_SERVICE")
            _validate_identifier(node.get("tool_binding"), f"{prefix}.tool_binding", errors)
            _validate_relative_path(
                node.get("working_directory"),
                f"{prefix}.working_directory",
                errors,
                allow_root=True,
            )
            _validate_environment(node.get("environment"), f"{prefix}.environment", errors)
            port = node.get("port")
            if not _is_integer(port) or not 1024 <= port <= 65535:
                errors.append(f"{prefix}.port must be an integer from 1024 to 65535")
            _validate_readiness(node.get("readiness"), f"{prefix}.readiness", errors)
            _validate_limits(node.get("limits"), f"{prefix}.limits", errors)
            _validate_shutdown(node.get("shutdown"), f"{prefix}.shutdown", errors)

    dependency_id = role_map.get("DEPENDENCY")
    application_id = role_map.get("APPLICATION")
    expected_start: list[str] | None = None
    if schema_version == "0.2":
        if set(role_map) != {"APPLICATION"}:
            errors.append("nodes must contain exactly one APPLICATION")
        if application_id is not None:
            application = node_map[application_id]
            if application.get("depends_on") != []:
                errors.append("application.depends_on must be [] for SINGLE_APPLICATION")
            _validate_arguments(
                application.get("arguments"),
                prefix=f"nodes[{nodes.index(application)}].arguments",
                node_id=application_id,
                tool_binding=application.get("tool_binding"),
                allowed_node_refs={application_id},
                errors=errors,
            )
            expected_start = [application_id]
        if expected_start is not None and profile.get("start_order") != expected_start:
            errors.append("start_order must contain only the APPLICATION node id")
        if expected_start is not None and profile.get("teardown_order") != expected_start:
            errors.append("teardown_order must contain only the APPLICATION node id")
    else:
        if set(role_map) != {"DEPENDENCY", "APPLICATION"}:
            errors.append("nodes must contain exactly one DEPENDENCY and one APPLICATION")
        if dependency_id is not None:
            dependency = node_map[dependency_id]
            if dependency.get("depends_on") != []:
                errors.append("dependency.depends_on must be []")
            _validate_arguments(
                dependency.get("arguments"),
                prefix=f"nodes[{nodes.index(dependency)}].arguments",
                node_id=dependency_id,
                tool_binding=dependency.get("tool_binding"),
                allowed_node_refs={dependency_id},
                errors=errors,
            )
        if application_id is not None and dependency_id is not None:
            application = node_map[application_id]
            if application.get("depends_on") != [dependency_id]:
                errors.append("application.depends_on must contain only the dependency node id")
            _validate_arguments(
                application.get("arguments"),
                prefix=f"nodes[{nodes.index(application)}].arguments",
                node_id=application_id,
                tool_binding=application.get("tool_binding"),
                allowed_node_refs={dependency_id, application_id},
                errors=errors,
            )
            expected_start = [dependency_id, application_id]
        if expected_start is not None and profile.get("start_order") != expected_start:
            errors.append("start_order must be [DEPENDENCY node id, APPLICATION node id]")
        if expected_start is not None and profile.get("teardown_order") != list(
            reversed(expected_start)
        ):
            errors.append("teardown_order must be the strict reverse of start_order")
    if application_id is not None and profile.get("application_node_id") != application_id:
        errors.append("application_node_id must reference the unique APPLICATION")
    if schema_version == "0.1" and isinstance(nodes, list) and len(nodes) == 2:
        ports = [node.get("port") for node in nodes if isinstance(node, dict)]
        if len(ports) == 2 and ports[0] == ports[1]:
            errors.append("node ports must be different")

    _validate_non_overlapping_roots(profile.get("subject_watch_roots"), errors)
    integer_ranges = {
        "max_watch_files": (1, 2_000),
        "max_watch_total_bytes": (1, 67_108_864),
        "lifecycle_timeout_ms": (5_000, 900_000),
    }
    for field, (minimum, maximum) in integer_ranges.items():
        item = profile.get(field)
        if not _is_integer(item) or not minimum <= item <= maximum:
            errors.append(f"{field} must be an integer from {minimum} to {maximum}")

    seal = profile.get("seal")
    if seal is not None:
        if not isinstance(seal, dict) or set(seal) != {"algorithm", "digest"}:
            errors.append("seal must contain exactly algorithm and digest")
        elif seal.get("algorithm") != "sha256" or not isinstance(
            seal.get("digest"), str
        ) or not SHA256_PATTERN.fullmatch(seal["digest"]):
            errors.append("seal must contain sha256 and a lowercase SHA-256 digest")

    try:
        canonical_json_bytes({key: value for key, value in profile.items() if key != "seal"})
    except (TypeError, ValueError) as exc:
        errors.append(f"ProjectProfile must contain finite JSON values: {exc}")
    _, sensitive_count = redact_value(
        {key: value for key, value in profile.items() if key != "seal"}
    )
    if sensitive_count:
        errors.append(
            f"ProjectProfile contains {sensitive_count} sensitive value(s) or personal path(s)"
        )
    if errors:
        raise ValidationError(errors)


def project_profile_digest(profile: dict[str, Any]) -> str:
    return sha256_json({key: value for key, value in profile.items() if key != "seal"})


def seal_project_profile(profile: dict[str, Any]) -> dict[str, Any]:
    validate_project_profile(profile)
    sealed = copy.deepcopy(profile)
    sealed["seal"] = {"algorithm": "sha256", "digest": project_profile_digest(sealed)}
    return sealed


def verify_sealed_project_profile(profile: dict[str, Any]) -> None:
    validate_project_profile(profile)
    seal = profile.get("seal")
    if not isinstance(seal, dict):
        raise ValidationError(["ProjectProfile is not sealed"])
    if seal.get("algorithm") != "sha256" or seal.get("digest") != project_profile_digest(profile):
        raise ValidationError(["ProjectProfile seal does not match its canonical content"])


def load_and_seal_project_profile(path: Path) -> dict[str, Any]:
    profile = load_json_object(path, label="ProjectProfile")
    if "seal" in profile:
        verify_sealed_project_profile(profile)
        return profile
    return seal_project_profile(profile)


def load_sealed_project_profile(path: Path) -> dict[str, Any]:
    profile = load_json_object(path, label="ProjectProfile")
    verify_sealed_project_profile(profile)
    return profile


def write_sealed_project_profile(path: Path, profile: dict[str, Any]) -> None:
    verify_sealed_project_profile(profile)
    if path.exists():
        raise SafetyError(f"refusing to overwrite existing output: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with path.open("xb") as handle:
            created = True
            handle.write(canonical_json_bytes(profile) + b"\n")
    except FileExistsError as exc:
        raise SafetyError(f"refusing to overwrite existing output: {path.name}") from exc
    except Exception:
        if created and path.exists():
            path.unlink()
        raise
