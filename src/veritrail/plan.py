from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.errors import SafetyError, ValidationError
from veritrail.jsonio import load_json_object as load_strict_json_object
from veritrail.privacy import redact_value

SUPPORTED_SCHEMA_VERSIONS = {"0.1", "0.2"}
PLAN_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
VARIABLE_ROLES = {"PRIMARY", "CONTROLLED", "NUISANCE"}
ASSERTION_SEVERITIES = {
    "HARD",
    "DEGRADATION_BOUNDARY",
    "OBJECTIVE",
    "OBSERVATION",
}
ASSERTION_OPERATORS = {"eq", "ne", "lt", "lte", "gt", "gte", "contains", "exists"}
CHANGE_LEVELS = {"L0_PRESENTATION", "L1_COMPONENT", "L2_CONTRACT", "L3_SYSTEM"}
LOAD_FIELDS = {
    "virtual_users",
    "in_flight_requests",
    "total_requests",
    "target_rps",
    "hotspot_contenders",
    "connections",
    "message_rate",
    "duration_seconds",
    "think_time_ms",
    "ramp_steps",
}
TOP_LEVEL_FIELDS = {
    "schema_version",
    "plan_id",
    "version",
    "subject",
    "question",
    "baseline",
    "experiment_type",
    "variables",
    "required_evidence",
    "assertions",
    "random_seed",
    "resource_budget",
    "load_model",
    "change_scope",
    "reproduction_steps",
    "cleanup_steps",
    "preflight",
    "seal",
}
PREFLIGHT_FIELDS = {
    "sample_count",
    "sampling_interval_ms",
    "hard_breach_grace_samples",
    "available_memory_soft_min_mb",
    "available_memory_hard_min_mb",
    "disk_free_hard_min_mb",
    "collector_rss_hard_max_mb",
    "observer_rss_delta_soft_max_mb",
    "ports",
    "require_clean_staging",
}


def load_json_object(path: Path) -> dict[str, Any]:
    return load_strict_json_object(path, label="plan")


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _reject_unknown_fields(
    value: dict[str, Any], allowed: set[str], path: str, errors: list[str]
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        errors.append(f"{path} has unsupported fields: {', '.join(unknown)}")


def _validate_string_list(value: Any, path: str, errors: list[str], *, non_empty: bool) -> None:
    if not isinstance(value, list) or (non_empty and not value):
        suffix = "a non-empty list" if non_empty else "a list"
        errors.append(f"{path} must be {suffix} of strings")
        return
    if any(not _non_empty_string(item) for item in value):
        errors.append(f"{path} must contain only non-empty strings")


def _validate_load_model(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict) or not value:
        errors.append("load_model must be a non-empty object with explicit units")
        return
    unknown = sorted(set(value) - LOAD_FIELDS)
    if "concurrency" in value:
        errors.append("load_model.concurrency is ambiguous; use an explicit load dimension")
    if unknown:
        errors.append(f"load_model has unsupported fields: {', '.join(unknown)}")
    for name, item in value.items():
        if name == "ramp_steps" or name not in LOAD_FIELDS:
            continue
        if not isinstance(item, (int, float)) or isinstance(item, bool) or item < 0:
            errors.append(f"load_model.{name} must be a non-negative number")
    ramp_steps = value.get("ramp_steps")
    if ramp_steps is not None:
        if not isinstance(ramp_steps, list) or not ramp_steps:
            errors.append("load_model.ramp_steps must be a non-empty list when present")
        else:
            for index, step in enumerate(ramp_steps):
                if not isinstance(step, dict) or not step:
                    errors.append(f"load_model.ramp_steps[{index}] must be a non-empty object")


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_resource_budget(value: Any, schema_version: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("resource_budget must be an object")
        return
    if schema_version == "0.1":
        _reject_unknown_fields(
            value,
            {"memory_soft_mb", "memory_hard_mb", "max_artifact_bytes"},
            "resource_budget",
            errors,
        )
        soft = value.get("memory_soft_mb")
        hard = value.get("memory_hard_mb")
        if not _is_integer(soft) or soft <= 0:
            errors.append("resource_budget.memory_soft_mb must be a positive integer")
        if not _is_integer(hard) or hard <= 0:
            errors.append("resource_budget.memory_hard_mb must be a positive integer")
        if _is_integer(soft) and _is_integer(hard) and hard < soft:
            errors.append("resource_budget.memory_hard_mb must be >= memory_soft_mb")
    elif schema_version == "0.2":
        _reject_unknown_fields(
            value,
            {"max_artifact_bytes"},
            "resource_budget",
            errors,
        )
    maximum = value.get("max_artifact_bytes")
    if not _is_integer(maximum) or maximum <= 0:
        errors.append("resource_budget.max_artifact_bytes must be a positive integer")


def _validate_preflight(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("preflight must be an object for schema_version '0.2'")
        return
    _reject_unknown_fields(value, PREFLIGHT_FIELDS, "preflight", errors)

    ranges = {
        "sample_count": (1, 20),
        "sampling_interval_ms": (0, 5000),
        "available_memory_soft_min_mb": (1, None),
        "available_memory_hard_min_mb": (1, None),
        "disk_free_hard_min_mb": (1, None),
        "collector_rss_hard_max_mb": (1, None),
        "observer_rss_delta_soft_max_mb": (0, None),
    }
    for field, (minimum, maximum) in ranges.items():
        item = value.get(field)
        if not _is_integer(item) or item < minimum or (maximum is not None and item > maximum):
            upper = f" and <= {maximum}" if maximum is not None else ""
            errors.append(f"preflight.{field} must be an integer >= {minimum}{upper}")

    sample_count = value.get("sample_count")
    interval = value.get("sampling_interval_ms")
    grace = value.get("hard_breach_grace_samples")
    if not _is_integer(grace) or grace < 1:
        errors.append("preflight.hard_breach_grace_samples must be a positive integer")
    elif _is_integer(sample_count) and grace > sample_count:
        errors.append("preflight.hard_breach_grace_samples must be <= sample_count")
    if _is_integer(sample_count) and _is_integer(interval) and (sample_count - 1) * interval > 60_000:
        errors.append("preflight sampling window must not exceed 60000 ms")

    soft = value.get("available_memory_soft_min_mb")
    hard = value.get("available_memory_hard_min_mb")
    if _is_integer(soft) and _is_integer(hard) and soft < hard:
        errors.append(
            "preflight.available_memory_soft_min_mb must be >= available_memory_hard_min_mb"
        )
    observer_soft = value.get("observer_rss_delta_soft_max_mb")
    collector_hard = value.get("collector_rss_hard_max_mb")
    if _is_integer(observer_soft) and _is_integer(collector_hard) and observer_soft > collector_hard:
        errors.append(
            "preflight.observer_rss_delta_soft_max_mb must be <= collector_rss_hard_max_mb"
        )

    ports = value.get("ports")
    seen_ports: set[int] = set()
    if not isinstance(ports, list) or len(ports) > 32:
        errors.append("preflight.ports must be a list with at most 32 entries")
    else:
        for index, port_rule in enumerate(ports):
            prefix = f"preflight.ports[{index}]"
            if not isinstance(port_rule, dict):
                errors.append(f"{prefix} must be an object")
                continue
            _reject_unknown_fields(port_rule, {"port", "expected"}, prefix, errors)
            port = port_rule.get("port")
            if not _is_integer(port) or not 1 <= port <= 65535:
                errors.append(f"{prefix}.port must be an integer from 1 to 65535")
            elif port in seen_ports:
                errors.append(f"{prefix}.port duplicates {port}")
            else:
                seen_ports.add(port)
            if port_rule.get("expected") not in {"FREE", "LISTENING"}:
                errors.append(f"{prefix}.expected must be FREE or LISTENING")

    if not isinstance(value.get("require_clean_staging"), bool):
        errors.append("preflight.require_clean_staging must be a boolean")


def validate_plan(plan: dict[str, Any]) -> None:
    errors: list[str] = []
    unknown_fields = sorted(set(plan) - TOP_LEVEL_FIELDS)
    if unknown_fields:
        errors.append(f"plan has unsupported fields: {', '.join(unknown_fields)}")

    schema_version = plan.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append("schema_version must be '0.1' or '0.2'")
    plan_id = plan.get("plan_id")
    if not isinstance(plan_id, str) or not PLAN_ID_PATTERN.fullmatch(plan_id):
        errors.append("plan_id must be a 2-64 character lowercase identifier")
    if not isinstance(plan.get("version"), int) or isinstance(plan.get("version"), bool) or plan.get("version", 0) < 1:
        errors.append("version must be a positive integer")
    if not _non_empty_string(plan.get("question")):
        errors.append("question must be a non-empty string")

    subject = plan.get("subject")
    if not isinstance(subject, dict):
        errors.append("subject must be an object")
    else:
        _reject_unknown_fields(subject, {"id", "version", "source_ref"}, "subject", errors)
        for field in ("id", "version"):
            if not _non_empty_string(subject.get(field)):
                errors.append(f"subject.{field} must be a non-empty string")

    baseline = plan.get("baseline")
    if not isinstance(baseline, dict):
        errors.append("baseline must be an object")
    else:
        _reject_unknown_fields(baseline, {"id", "status", "fingerprint", "tolerances"}, "baseline", errors)
        if not _non_empty_string(baseline.get("id")):
            errors.append("baseline.id must be a non-empty string")
        if baseline.get("status") not in {"VALID", "EXPIRED"}:
            errors.append("baseline.status must be VALID or EXPIRED")
        fingerprint = baseline.get("fingerprint")
        if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
            errors.append("baseline.fingerprint must be a lowercase SHA-256 digest")

    if plan.get("experiment_type") != "SINGLE_VARIABLE":
        errors.append("experiment_type must be SINGLE_VARIABLE in the current contract")

    variables = plan.get("variables")
    variable_names: set[str] = set()
    primary_count = 0
    if not isinstance(variables, list) or not variables:
        errors.append("variables must be a non-empty list")
    else:
        for index, variable in enumerate(variables):
            prefix = f"variables[{index}]"
            if not isinstance(variable, dict):
                errors.append(f"{prefix} must be an object")
                continue
            _reject_unknown_fields(variable, {"name", "role", "value", "unit", "source"}, prefix, errors)
            name = variable.get("name")
            if not _non_empty_string(name):
                errors.append(f"{prefix}.name must be a non-empty string")
            elif name in variable_names:
                errors.append(f"{prefix}.name duplicates {name!r}")
            else:
                variable_names.add(name)
            role = variable.get("role")
            if role not in VARIABLE_ROLES:
                errors.append(f"{prefix}.role must be PRIMARY, CONTROLLED, or NUISANCE")
            elif role == "PRIMARY":
                primary_count += 1
            if "value" not in variable:
                errors.append(f"{prefix}.value is required")
            if not _non_empty_string(variable.get("source")):
                errors.append(f"{prefix}.source must be a non-empty string")
        if primary_count != 1:
            errors.append("a SINGLE_VARIABLE plan must declare exactly one PRIMARY variable")

    required_evidence = plan.get("required_evidence")
    _validate_string_list(required_evidence, "required_evidence", errors, non_empty=True)
    if isinstance(required_evidence, list) and len(required_evidence) != len(set(required_evidence)):
        errors.append("required_evidence must not contain duplicates")
    if schema_version == "0.2" and (
        not isinstance(required_evidence, list) or "runtime.preflight" not in required_evidence
    ):
        errors.append("schema_version '0.2' must require runtime.preflight evidence")

    assertions = plan.get("assertions")
    assertion_ids: set[str] = set()
    decisive_count = 0
    if not isinstance(assertions, list) or not assertions:
        errors.append("assertions must be a non-empty list")
    else:
        for index, assertion in enumerate(assertions):
            prefix = f"assertions[{index}]"
            if not isinstance(assertion, dict):
                errors.append(f"{prefix} must be an object")
                continue
            _reject_unknown_fields(
                assertion,
                {"id", "severity", "evidence_type", "path", "operator", "expected"},
                prefix,
                errors,
            )
            assertion_id = assertion.get("id")
            if not _non_empty_string(assertion_id):
                errors.append(f"{prefix}.id must be a non-empty string")
            elif assertion_id in assertion_ids:
                errors.append(f"{prefix}.id duplicates {assertion_id!r}")
            else:
                assertion_ids.add(assertion_id)
            severity = assertion.get("severity")
            if severity not in ASSERTION_SEVERITIES:
                errors.append(f"{prefix}.severity is unsupported")
            elif severity in {"HARD", "DEGRADATION_BOUNDARY"}:
                decisive_count += 1
            if not _non_empty_string(assertion.get("evidence_type")):
                errors.append(f"{prefix}.evidence_type must be a non-empty string")
            pointer = assertion.get("path")
            if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")):
                errors.append(f"{prefix}.path must be an RFC 6901 JSON pointer")
            if assertion.get("operator") not in ASSERTION_OPERATORS:
                errors.append(f"{prefix}.operator is unsupported")
            if "expected" not in assertion:
                errors.append(f"{prefix}.expected is required")
        if decisive_count < 1:
            errors.append("at least one HARD or DEGRADATION_BOUNDARY assertion is required")
        if schema_version == "0.2" and not any(
            isinstance(assertion, dict) and assertion.get("evidence_type") == "runtime.preflight"
            for assertion in assertions
        ):
            errors.append("schema_version '0.2' must define an assertion over runtime.preflight")

    random_seed = plan.get("random_seed")
    if not isinstance(random_seed, int) or isinstance(random_seed, bool) or random_seed < 0:
        errors.append("random_seed must be a non-negative integer")

    _validate_resource_budget(plan.get("resource_budget"), schema_version, errors)

    if schema_version == "0.1":
        if "preflight" in plan:
            errors.append("preflight requires schema_version '0.2'")
    elif schema_version == "0.2":
        _validate_preflight(plan.get("preflight"), errors)

    _validate_load_model(plan.get("load_model"), errors)

    scope = plan.get("change_scope")
    if not isinstance(scope, dict):
        errors.append("change_scope must be an object")
    else:
        _reject_unknown_fields(
            scope,
            {"level", "owner", "expected_blast_radius", "consumers"},
            "change_scope",
            errors,
        )
        if scope.get("level") not in CHANGE_LEVELS:
            errors.append("change_scope.level is unsupported")
        for field in ("owner", "expected_blast_radius"):
            if not _non_empty_string(scope.get(field)):
                errors.append(f"change_scope.{field} must be a non-empty string")
        _validate_string_list(scope.get("consumers"), "change_scope.consumers", errors, non_empty=False)
        if scope.get("level") in {"L2_CONTRACT", "L3_SYSTEM"} and not scope.get("consumers"):
            errors.append("L2/L3 change_scope must enumerate at least one consumer")

    _validate_string_list(plan.get("reproduction_steps"), "reproduction_steps", errors, non_empty=True)
    _validate_string_list(plan.get("cleanup_steps"), "cleanup_steps", errors, non_empty=True)

    try:
        canonical_json_bytes({key: value for key, value in plan.items() if key != "seal"})
    except (TypeError, ValueError) as exc:
        errors.append(f"plan must contain finite JSON values: {exc}")

    _, sensitive_count = redact_value({key: value for key, value in plan.items() if key != "seal"})
    if sensitive_count:
        errors.append(
            f"plan contains {sensitive_count} sensitive value(s) or personal path(s); replace them with stable references"
        )

    if errors:
        raise ValidationError(errors)


def plan_digest(plan: dict[str, Any]) -> str:
    unsigned = {key: value for key, value in plan.items() if key != "seal"}
    return sha256_json(unsigned)


def seal_plan(plan: dict[str, Any]) -> dict[str, Any]:
    validate_plan(plan)
    sealed = copy.deepcopy(plan)
    sealed["seal"] = {"algorithm": "sha256", "digest": plan_digest(sealed)}
    return sealed


def verify_sealed_plan(plan: dict[str, Any]) -> None:
    validate_plan(plan)
    seal = plan.get("seal")
    if not isinstance(seal, dict):
        raise ValidationError(["plan is not sealed"])
    if seal.get("algorithm") != "sha256" or seal.get("digest") != plan_digest(plan):
        raise ValidationError(["plan seal does not match its canonical content"])


def load_and_seal_plan(path: Path) -> dict[str, Any]:
    plan = load_json_object(path)
    if "seal" in plan:
        verify_sealed_plan(plan)
        return plan
    return seal_plan(plan)


def write_sealed_plan(path: Path, plan: dict[str, Any]) -> None:
    if path.exists():
        raise SafetyError(f"refusing to overwrite existing output: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with path.open("xb") as handle:
            created = True
            handle.write(canonical_json_bytes(plan) + b"\n")
    except FileExistsError as exc:
        raise SafetyError(f"refusing to overwrite existing output: {path.name}") from exc
    except Exception:
        if created and path.exists():
            path.unlink()
        raise
