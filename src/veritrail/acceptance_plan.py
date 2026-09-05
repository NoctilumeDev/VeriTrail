from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.errors import SafetyError, ValidationError
from veritrail.jsonio import load_json_object
from veritrail.privacy import redact_value


ACCEPTANCE_PLAN_KIND = "ACCEPTANCE"
ACCEPTANCE_PLAN_SCHEMA_VERSION = "0.1"
CANONICALIZATION_PROFILE = "veritrail-json-c14n/1"

IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
EVIDENCE_TYPE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

RULE_OPERATORS = {
    "eq",
    "ne",
    "lt",
    "lte",
    "gt",
    "gte",
    "contains",
    "exists",
    "set_equals",
    "contains_all",
}
ASSERTION_SEVERITIES = {
    "HARD",
    "DEGRADATION_BOUNDARY",
    "OBJECTIVE",
    "OBSERVATION",
}

TOP_LEVEL_FIELDS = {
    "plan_kind",
    "schema_version",
    "plan_id",
    "version",
    "subject",
    "question",
    "governance",
    "observation_specs",
    "evidence_requirements",
    "sufficiency_rules",
    "integrity_rules",
    "assertions",
    "resource_budget",
    "change_scope",
    "reproduction_steps",
    "cleanup_steps",
    "seal",
}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _reject_unknown_fields(
    value: dict[str, Any], allowed: set[str], path: str, errors: list[str]
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        errors.append(f"{path} has unsupported fields: {', '.join(unknown)}")


def _validate_string_list(
    value: Any,
    path: str,
    errors: list[str],
    *,
    non_empty: bool,
    unique: bool = False,
) -> None:
    if not isinstance(value, list) or (non_empty and not value):
        expected = "a non-empty list" if non_empty else "a list"
        errors.append(f"{path} must be {expected} of non-empty strings")
        return
    if any(not _non_empty_string(item) for item in value):
        errors.append(f"{path} must contain only non-empty strings")
        return
    if unique and len(value) != len(set(value)):
        errors.append(f"{path} must not contain duplicates")


def _validate_no_floats(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, float):
        errors.append(f"{path} must not contain floating-point values")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _validate_no_floats(item, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _validate_no_floats(item, f"{path}[{index}]", errors)


def _validate_pointer(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or (value and not value.startswith("/")):
        errors.append(f"{path} must be an RFC 6901 JSON pointer")
        return
    if isinstance(value, str) and re.search(r"~(?:[^01]|$)", value):
        errors.append(f"{path} contains an invalid RFC 6901 escape")


def _validate_operand(
    value: Any,
    path: str,
    requirement_ids: set[str],
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an operand object")
        return
    _reject_unknown_fields(value, {"requirement_id", "path"}, path, errors)
    if set(value) != {"requirement_id", "path"}:
        errors.append(f"{path} must contain requirement_id and path")
        return
    requirement_id = value.get("requirement_id")
    if requirement_id not in requirement_ids:
        errors.append(f"{path}.requirement_id must reference a declared evidence requirement")
    _validate_pointer(value.get("path"), f"{path}.path", errors)


def _right_is_operand(value: Any) -> bool:
    return isinstance(value, dict) and set(value) == {"requirement_id", "path"}


def _validate_rule(
    rule: Any,
    path: str,
    category: str,
    requirement_ids: set[str],
    rule_ids: set[str],
    errors: list[str],
) -> bool:
    if not isinstance(rule, dict):
        errors.append(f"{path} must be an object")
        return False
    allowed = {"id", "left", "operator", "right"}
    if category == "ASSERTION":
        allowed.add("severity")
    _reject_unknown_fields(rule, allowed, path, errors)

    rule_id = rule.get("id")
    if not isinstance(rule_id, str) or not IDENTIFIER_PATTERN.fullmatch(rule_id):
        errors.append(f"{path}.id must be a 2-64 character lowercase identifier")
    elif rule_id in rule_ids:
        errors.append(f"{path}.id duplicates {rule_id!r}")
    else:
        rule_ids.add(rule_id)

    _validate_operand(rule.get("left"), f"{path}.left", requirement_ids, errors)
    operator = rule.get("operator")
    if operator not in RULE_OPERATORS:
        errors.append(f"{path}.operator is unsupported")
    if operator == "exists":
        if "right" in rule:
            errors.append(f"{path}.right must be absent for exists")
    elif "right" not in rule:
        errors.append(f"{path}.right is required")
    else:
        right = rule["right"]
        if _right_is_operand(right):
            _validate_operand(right, f"{path}.right", requirement_ids, errors)
        else:
            _validate_no_floats(right, f"{path}.right", errors)
            try:
                canonical_json_bytes(right)
            except (TypeError, ValueError) as exc:
                errors.append(f"{path}.right must be finite JSON: {exc}")

    if category == "ASSERTION":
        severity = rule.get("severity")
        if severity not in ASSERTION_SEVERITIES:
            errors.append(f"{path}.severity is unsupported")
        return severity in {"HARD", "DEGRADATION_BOUNDARY"}
    return False


def validate_acceptance_plan(plan: dict[str, Any]) -> None:
    errors: list[str] = []
    _reject_unknown_fields(plan, TOP_LEVEL_FIELDS, "acceptance plan", errors)

    if plan.get("plan_kind") != ACCEPTANCE_PLAN_KIND:
        errors.append("plan_kind must be ACCEPTANCE")
    if plan.get("schema_version") != ACCEPTANCE_PLAN_SCHEMA_VERSION:
        errors.append("schema_version must be '0.1'")
    plan_id = plan.get("plan_id")
    if not isinstance(plan_id, str) or not IDENTIFIER_PATTERN.fullmatch(plan_id):
        errors.append("plan_id must be a 2-64 character lowercase identifier")
    if not _positive_int(plan.get("version")):
        errors.append("version must be a positive integer")
    if not _non_empty_string(plan.get("question")):
        errors.append("question must be a non-empty string")

    subject = plan.get("subject")
    if not isinstance(subject, dict):
        errors.append("subject must be an object")
    else:
        _reject_unknown_fields(subject, {"id", "version", "source_ref"}, "subject", errors)
        for field in ("id", "version", "source_ref"):
            if not _non_empty_string(subject.get(field)):
                errors.append(f"subject.{field} must be a non-empty string")

    governance = plan.get("governance")
    if not isinstance(governance, dict):
        errors.append("governance must be an object")
    else:
        fields = {
            "claim_owner_ref",
            "drafter_ref",
            "seal_authority_ref",
            "seal_decision",
        }
        _reject_unknown_fields(governance, fields, "governance", errors)
        for field in ("claim_owner_ref", "drafter_ref", "seal_authority_ref"):
            if not _non_empty_string(governance.get(field)):
                errors.append(f"governance.{field} must be a non-empty string")
        if governance.get("seal_decision") != "CONFIRMED":
            errors.append("governance.seal_decision must be CONFIRMED")

    observation_specs = plan.get("observation_specs")
    spec_ids: set[str] = set()
    if not isinstance(observation_specs, list) or not observation_specs:
        errors.append("observation_specs must be a non-empty list")
    else:
        for index, spec in enumerate(observation_specs):
            path = f"observation_specs[{index}]"
            if not isinstance(spec, dict):
                errors.append(f"{path} must be an object")
                continue
            _reject_unknown_fields(
                spec,
                {
                    "id",
                    "contract",
                    "evidence_type",
                    "coordinates",
                    "projections",
                    "canonicalization_profile",
                },
                path,
                errors,
            )
            spec_id = spec.get("id")
            if not isinstance(spec_id, str) or not IDENTIFIER_PATTERN.fullmatch(spec_id):
                errors.append(f"{path}.id must be a 2-64 character lowercase identifier")
            elif spec_id in spec_ids:
                errors.append(f"{path}.id duplicates {spec_id!r}")
            else:
                spec_ids.add(spec_id)
            contract = spec.get("contract")
            if not isinstance(contract, dict):
                errors.append(f"{path}.contract must be an object")
            else:
                _reject_unknown_fields(contract, {"id", "version"}, f"{path}.contract", errors)
                for field in ("id", "version"):
                    if not _non_empty_string(contract.get(field)):
                        errors.append(f"{path}.contract.{field} must be a non-empty string")
            evidence_type = spec.get("evidence_type")
            if not isinstance(evidence_type, str) or not EVIDENCE_TYPE_PATTERN.fullmatch(
                evidence_type
            ):
                errors.append(
                    f"{path}.evidence_type must be a 2-64 character lowercase identifier"
                )
            if not isinstance(spec.get("coordinates"), dict):
                errors.append(f"{path}.coordinates must be an object")
            _validate_string_list(
                spec.get("projections"),
                f"{path}.projections",
                errors,
                non_empty=True,
                unique=True,
            )
            if spec.get("canonicalization_profile") != CANONICALIZATION_PROFILE:
                errors.append(
                    f"{path}.canonicalization_profile must be {CANONICALIZATION_PROFILE}"
                )

    requirements = plan.get("evidence_requirements")
    requirement_ids: set[str] = set()
    if not isinstance(requirements, list) or not requirements:
        errors.append("evidence_requirements must be a non-empty list")
    else:
        for index, requirement in enumerate(requirements):
            path = f"evidence_requirements[{index}]"
            if not isinstance(requirement, dict):
                errors.append(f"{path} must be an object")
                continue
            _reject_unknown_fields(
                requirement,
                {"id", "observation_spec_id", "cardinality"},
                path,
                errors,
            )
            requirement_id = requirement.get("id")
            if not isinstance(requirement_id, str) or not IDENTIFIER_PATTERN.fullmatch(
                requirement_id
            ):
                errors.append(f"{path}.id must be a 2-64 character lowercase identifier")
            elif requirement_id in requirement_ids:
                errors.append(f"{path}.id duplicates {requirement_id!r}")
            else:
                requirement_ids.add(requirement_id)
            if requirement.get("observation_spec_id") not in spec_ids:
                errors.append(f"{path}.observation_spec_id must reference an observation spec")
            if requirement.get("cardinality") != "EXACTLY_ONE":
                errors.append(f"{path}.cardinality must be EXACTLY_ONE")

    rule_ids: set[str] = set()
    decisive_count = 0
    for field, category in (
        ("sufficiency_rules", "SUFFICIENCY"),
        ("integrity_rules", "INTEGRITY"),
        ("assertions", "ASSERTION"),
    ):
        rules = plan.get(field)
        if not isinstance(rules, list):
            errors.append(f"{field} must be a list")
            continue
        for index, rule in enumerate(rules):
            if _validate_rule(
                rule,
                f"{field}[{index}]",
                category,
                requirement_ids,
                rule_ids,
                errors,
            ):
                decisive_count += 1
    if decisive_count < 1:
        errors.append("at least one HARD or DEGRADATION_BOUNDARY assertion is required")

    for field in ("resource_budget", "change_scope"):
        if not isinstance(plan.get(field), dict):
            errors.append(f"{field} must be an object")
    _validate_string_list(
        plan.get("reproduction_steps"),
        "reproduction_steps",
        errors,
        non_empty=True,
    )
    _validate_string_list(
        plan.get("cleanup_steps"),
        "cleanup_steps",
        errors,
        non_empty=True,
    )

    unsigned = {key: value for key, value in plan.items() if key != "seal"}
    _validate_no_floats(unsigned, "acceptance plan", errors)
    try:
        canonical_json_bytes(unsigned)
    except (TypeError, ValueError) as exc:
        errors.append(f"acceptance plan must contain finite JSON values: {exc}")
    _, sensitive_count = redact_value(unsigned)
    if sensitive_count:
        errors.append(
            "acceptance plan contains sensitive values or personal paths; replace them with stable references"
        )

    seal = plan.get("seal")
    if "seal" in plan:
        if not isinstance(seal, dict) or set(seal) != {"algorithm", "digest"}:
            errors.append("seal must contain exactly algorithm and digest")
        elif seal.get("algorithm") != "sha256" or not isinstance(
            seal.get("digest"), str
        ) or not SHA256_PATTERN.fullmatch(seal["digest"]):
            errors.append("seal must contain a lowercase SHA-256 digest")

    if errors:
        raise ValidationError(errors)


def observation_spec_digest(spec: dict[str, Any]) -> str:
    projection = {
        "canonicalization_profile": spec["canonicalization_profile"],
        "contract": spec["contract"],
        "evidence_type": spec["evidence_type"],
        "coordinates": spec["coordinates"],
        "projections": spec["projections"],
    }
    return sha256_json(projection)


def acceptance_plan_digest(plan: dict[str, Any]) -> str:
    return sha256_json({key: value for key, value in plan.items() if key != "seal"})


def seal_acceptance_plan(plan: dict[str, Any]) -> dict[str, Any]:
    validate_acceptance_plan(plan)
    sealed = copy.deepcopy(plan)
    sealed["seal"] = {
        "algorithm": "sha256",
        "digest": acceptance_plan_digest(sealed),
    }
    return sealed


def verify_sealed_acceptance_plan(plan: dict[str, Any]) -> None:
    validate_acceptance_plan(plan)
    if "seal" not in plan:
        raise ValidationError(["acceptance plan is not sealed"])
    if plan["seal"]["digest"] != acceptance_plan_digest(plan):
        raise ValidationError(
            ["acceptance plan seal does not match its canonical content"]
        )


def load_and_seal_acceptance_plan(path: Path) -> dict[str, Any]:
    plan = load_json_object(path, label="acceptance plan")
    if "seal" in plan:
        verify_sealed_acceptance_plan(plan)
        return plan
    return seal_acceptance_plan(plan)


def write_sealed_acceptance_plan(path: Path, plan: dict[str, Any]) -> None:
    verify_sealed_acceptance_plan(plan)
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
