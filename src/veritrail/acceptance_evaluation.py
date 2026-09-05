from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from veritrail.acceptance_plan import (
    CANONICALIZATION_PROFILE,
    observation_spec_digest,
    verify_sealed_acceptance_plan,
)
from veritrail.canonical import canonical_json_bytes
from veritrail.errors import ValidationError
from veritrail.evidence import ImportedEvidence, verify_imported_evidence


EXECUTION_STATUSES = {"PLANNED", "RUNNING", "COMPLETED", "ABORTED", "ERROR"}
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
REFERENCE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")

OBSERVATION_METADATA_FIELDS = {
    "schema_version",
    "canonicalization_profile",
    "plan_digest",
    "observation_spec_digest",
    "request_seal_digest",
    "collection_session_id",
    "collector_role",
    "coverage",
    "normalization_semantics_version",
    "facts_digest",
}
COVERAGE_VALUES = {"COMPLETE", "PARTIAL", "ERROR", "NOT_APPLICABLE"}

_MISSING = object()


@dataclass(frozen=True)
class _ResolvedOperand:
    requirement_id: str
    path: str
    resolution: str
    value: Any
    evidence_sha256: str | None


def validate_observation_metadata(document: dict[str, Any], input_name: str) -> None:
    errors: list[str] = []
    metadata = document.get("metadata")
    observation = (
        metadata.get("veritrail_observation") if isinstance(metadata, dict) else None
    )
    path = f"{input_name}.metadata.veritrail_observation"
    if not isinstance(observation, dict):
        raise ValidationError([f"{path} must be an object"])
    unknown = sorted(set(observation) - OBSERVATION_METADATA_FIELDS)
    missing = sorted(OBSERVATION_METADATA_FIELDS - set(observation))
    if unknown:
        errors.append(f"{path} has unsupported fields: {', '.join(unknown)}")
    if missing:
        errors.append(f"{path} is missing fields: {', '.join(missing)}")
    if observation.get("schema_version") != "0.1":
        errors.append(f"{path}.schema_version must be '0.1'")
    if observation.get("canonicalization_profile") != CANONICALIZATION_PROFILE:
        errors.append(
            f"{path}.canonicalization_profile must be {CANONICALIZATION_PROFILE}"
        )
    for field in (
        "plan_digest",
        "observation_spec_digest",
        "request_seal_digest",
        "facts_digest",
    ):
        value = observation.get(field)
        if not isinstance(value, str) or not SHA256_PATTERN.fullmatch(value):
            errors.append(f"{path}.{field} must be a lowercase SHA-256 digest")
    for field in (
        "collection_session_id",
        "collector_role",
        "normalization_semantics_version",
    ):
        value = observation.get(field)
        if not isinstance(value, str) or not REFERENCE_PATTERN.fullmatch(value):
            errors.append(f"{path}.{field} must be a stable 1-128 character reference")
    if observation.get("coverage") not in COVERAGE_VALUES:
        errors.append(f"{path}.coverage is unsupported")
    if errors:
        raise ValidationError(errors)


def _decode_pointer_token(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def _json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    current = document
    for raw_token in pointer.split("/")[1:]:
        token = _decode_pointer_token(raw_token)
        if isinstance(current, dict):
            if token not in current:
                return _MISSING
            current = current[token]
        elif isinstance(current, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                return _MISSING
            index = int(token)
            if index >= len(current):
                return _MISSING
            current = current[index]
        else:
            return _MISSING
    return current


def _operand_result(value: _ResolvedOperand, *, kind: str = "EVIDENCE") -> dict[str, Any]:
    return {
        "kind": kind,
        "requirement_id": value.requirement_id,
        "path": value.path,
        "resolution": value.resolution,
        "resolved": value.resolution == "RESOLVED",
        "value": None if value.value is _MISSING else value.value,
        "evidence_sha256": value.evidence_sha256,
    }


def _literal_result(value: Any) -> dict[str, Any]:
    return {
        "kind": "LITERAL",
        "requirement_id": None,
        "path": None,
        "resolution": "RESOLVED",
        "resolved": True,
        "value": value,
        "evidence_sha256": None,
    }


def _none_result() -> dict[str, Any]:
    return {
        "kind": "NONE",
        "requirement_id": None,
        "path": None,
        "resolution": "NOT_APPLICABLE",
        "resolved": False,
        "value": None,
        "evidence_sha256": None,
    }


def _resolve_operand(
    operand: dict[str, Any],
    bindings: dict[str, ImportedEvidence],
) -> _ResolvedOperand:
    requirement_id = operand["requirement_id"]
    path = operand["path"]
    artifact = bindings.get(requirement_id)
    if artifact is None:
        return _ResolvedOperand(
            requirement_id,
            path,
            "MISSING_REQUIREMENT",
            _MISSING,
            None,
        )
    value = _json_pointer(artifact.document, path)
    return _ResolvedOperand(
        requirement_id,
        path,
        "MISSING_PATH" if value is _MISSING else "RESOLVED",
        value,
        artifact.sha256,
    )


def _same_value(left: Any, right: Any) -> bool:
    return canonical_json_bytes(left) == canonical_json_bytes(right)


def _canonical_set(value: Any) -> set[bytes]:
    if not isinstance(value, list):
        raise TypeError("set operator operands must be arrays")
    items = [canonical_json_bytes(item) for item in value]
    if len(items) != len(set(items)):
        raise ValueError("set operator operands must not contain canonical duplicates")
    return set(items)


def _apply_operator(operator: str, left: Any, right: Any) -> bool:
    if operator == "eq":
        return _same_value(left, right)
    if operator == "ne":
        return not _same_value(left, right)
    if operator in {"lt", "lte", "gt", "gte"}:
        if (
            not isinstance(left, int)
            or isinstance(left, bool)
            or not isinstance(right, int)
            or isinstance(right, bool)
        ):
            raise TypeError("numeric comparison operands must be integers")
        if operator == "lt":
            return left < right
        if operator == "lte":
            return left <= right
        if operator == "gt":
            return left > right
        return left >= right
    if operator == "contains":
        if isinstance(left, str) and isinstance(right, str):
            return right in left
        if isinstance(left, list):
            return any(_same_value(item, right) for item in left)
        raise TypeError("contains requires string/string or array/value operands")
    if operator == "set_equals":
        return _canonical_set(left) == _canonical_set(right)
    if operator == "contains_all":
        return _canonical_set(left).issuperset(_canonical_set(right))
    raise TypeError("unsupported rule operator")


def _evaluate_rule(
    rule: dict[str, Any],
    category: str,
    bindings: dict[str, ImportedEvidence],
) -> dict[str, Any]:
    left = _resolve_operand(rule["left"], bindings)
    left_result = _operand_result(left)
    operator = rule["operator"]
    result: dict[str, Any] = {
        "id": rule["id"],
        "category": category,
        "operator": operator,
        "left": left_result,
        "right": _none_result(),
        "status": "NOT_EVALUATED",
        "explanation": "The required Evidence is not uniquely bound.",
    }
    if category == "ASSERTION":
        result["severity"] = rule["severity"]

    if left.resolution == "MISSING_REQUIREMENT":
        return result
    if operator == "exists":
        passed = left.resolution == "RESOLVED"
        result["status"] = "PASS" if passed else "FAIL"
        result["explanation"] = (
            "The declared Evidence path exists."
            if passed
            else "The declared Evidence path does not exist."
        )
        return result
    if left.resolution == "MISSING_PATH":
        result["explanation"] = "The left Evidence path is not present."
        return result

    right_value = rule["right"]
    if isinstance(right_value, dict) and set(right_value) == {"requirement_id", "path"}:
        right = _resolve_operand(right_value, bindings)
        result["right"] = _operand_result(right)
        if right.resolution != "RESOLVED":
            result["explanation"] = (
                "The right requirement is not uniquely bound."
                if right.resolution == "MISSING_REQUIREMENT"
                else "The right Evidence path is not present."
            )
            return result
        resolved_right = right.value
    else:
        result["right"] = _literal_result(right_value)
        resolved_right = right_value

    try:
        passed = _apply_operator(operator, left.value, resolved_right)
    except (TypeError, ValueError) as exc:
        result["status"] = "ERROR"
        result["explanation"] = str(exc)
        return result
    result["status"] = "PASS" if passed else "FAIL"
    result["explanation"] = (
        "The resolved operands satisfy the declared rule."
        if passed
        else "The resolved operands do not satisfy the declared rule."
    )
    return result


def _binding_reason(code: str, requirement_id: str) -> dict[str, str]:
    messages = {
        "OBSERVATION_MISSING": "No Evidence artifact was supplied for the requirement.",
        "OBSERVATION_BINDING_MISMATCH": "Same-type Evidence was supplied but did not match the sealed Plan and observation spec.",
        "OBSERVATION_CARDINALITY_CONFLICT": "More than one Evidence artifact matched an EXACTLY_ONE requirement.",
        "OBSERVATION_REUSE_CONFLICT": "One Evidence artifact was consumed by more than one requirement.",
    }
    return {
        "code": code,
        "requirement_id": requirement_id,
        "message": messages[code],
    }


def evaluate_acceptance(
    plan: dict[str, Any],
    evidence: list[ImportedEvidence],
    execution_status: str,
) -> dict[str, Any]:
    verify_sealed_acceptance_plan(plan)
    if execution_status not in EXECUTION_STATUSES:
        raise ValidationError(["execution_status is unsupported"])
    for artifact in evidence:
        verify_imported_evidence(artifact)

    plan_digest = plan["seal"]["digest"]
    specs = {item["id"]: item for item in plan["observation_specs"]}
    bindings: dict[str, ImportedEvidence] = {}
    binding_results: list[dict[str, Any]] = []
    reasons: list[dict[str, str]] = []
    blockers = False

    for requirement in plan["evidence_requirements"]:
        requirement_id = requirement["id"]
        spec = specs[requirement["observation_spec_id"]]
        spec_digest = observation_spec_digest(spec)
        same_type = [
            artifact
            for artifact in evidence
            if artifact.document["evidence_type"] == spec["evidence_type"]
        ]
        exact: list[ImportedEvidence] = []
        metadata_errors: list[str] = []
        for artifact in same_type:
            try:
                validate_observation_metadata(artifact.document, artifact.input_name)
            except ValidationError as exc:
                metadata_errors.extend(exc.errors)
                continue
            observation = artifact.document["metadata"]["veritrail_observation"]
            if (
                observation["plan_digest"] == plan_digest
                and observation["observation_spec_digest"] == spec_digest
            ):
                exact.append(artifact)

        status = "RESOLVED"
        evidence_sha256: str | None = None
        if not exact:
            if same_type:
                status = "BINDING_MISMATCH"
                reasons.append(
                    _binding_reason("OBSERVATION_BINDING_MISMATCH", requirement_id)
                )
                blockers = True
            else:
                status = "MISSING"
                reasons.append(_binding_reason("OBSERVATION_MISSING", requirement_id))
        elif len(exact) > 1:
            status = "CARDINALITY_CONFLICT"
            reasons.append(
                _binding_reason("OBSERVATION_CARDINALITY_CONFLICT", requirement_id)
            )
            blockers = True
        else:
            bindings[requirement_id] = exact[0]
            evidence_sha256 = exact[0].sha256
        binding_results.append(
            {
                "requirement_id": requirement_id,
                "observation_spec_id": spec["id"],
                "observation_spec_digest": spec_digest,
                "evidence_type": spec["evidence_type"],
                "cardinality": "EXACTLY_ONE",
                "status": status,
                "evidence_sha256": evidence_sha256,
                "candidate_count": len(same_type),
                "exact_match_count": len(exact),
                "metadata_error_count": len(metadata_errors),
            }
        )

    consumed: dict[str, list[str]] = {}
    for requirement_id, artifact in bindings.items():
        consumed.setdefault(artifact.sha256, []).append(requirement_id)
    reused = {
        digest: requirement_ids
        for digest, requirement_ids in consumed.items()
        if len(requirement_ids) > 1
    }
    if reused:
        blockers = True
        for digest, requirement_ids in sorted(reused.items()):
            for requirement_id in requirement_ids:
                reasons.append(
                    _binding_reason("OBSERVATION_REUSE_CONFLICT", requirement_id)
                )
                for binding in binding_results:
                    if binding["requirement_id"] == requirement_id:
                        binding["status"] = "REUSE_CONFLICT"
                        binding["evidence_sha256"] = digest
            for requirement_id in requirement_ids:
                bindings.pop(requirement_id, None)

    rule_results: list[dict[str, Any]] = []
    for field, category in (
        ("sufficiency_rules", "SUFFICIENCY"),
        ("integrity_rules", "INTEGRITY"),
        ("assertions", "ASSERTION"),
    ):
        rule_results.extend(
            _evaluate_rule(rule, category, bindings) for rule in plan[field]
        )

    rule_error = any(item["status"] == "ERROR" for item in rule_results)
    integrity_false = any(
        item["category"] == "INTEGRITY" and item["status"] == "FAIL"
        for item in rule_results
    )
    decisive = [
        item
        for item in rule_results
        if item["category"] == "ASSERTION"
        and item.get("severity") in {"HARD", "DEGRADATION_BOUNDARY"}
    ]
    decisive_false = any(item["status"] == "FAIL" for item in decisive)
    pending_rules = any(
        (
            item["category"] in {"SUFFICIENCY", "INTEGRITY"}
            and item["status"] in {"FAIL", "NOT_EVALUATED"}
        )
        or (item in decisive and item["status"] == "NOT_EVALUATED")
        for item in rule_results
    )
    missing = [
        item["requirement_id"]
        for item in binding_results
        if item["status"] == "MISSING"
    ]

    if blockers or rule_error or integrity_false:
        verdict = "INCONCLUSIVE"
        reasons.append(
            {
                "code": "ACCEPTANCE_INTEGRITY_BLOCKED",
                "requirement_id": "",
                "message": "Binding or rule integrity prevents a reliable acceptance conclusion.",
            }
        )
    elif decisive_false:
        verdict = "FAIL"
        reasons.append(
            {
                "code": "ACCEPTANCE_ASSERTION_FAILED",
                "requirement_id": "",
                "message": "At least one decisive assertion is false.",
            }
        )
    elif execution_status != "COMPLETED" or missing or pending_rules:
        verdict = "PENDING"
        reasons.append(
            {
                "code": "ACCEPTANCE_EVIDENCE_PENDING",
                "requirement_id": "",
                "message": "Execution or required Evidence is not complete enough for a verdict.",
            }
        )
    else:
        verdict = "PASS"
        reasons.append(
            {
                "code": "ACCEPTANCE_PASS",
                "requirement_id": "",
                "message": "All required Evidence and decisive rules pass.",
            }
        )

    return {
        "execution_status": execution_status,
        "verdict": verdict,
        "reasons": reasons,
        "evidence_bindings": binding_results,
        "rule_results": rule_results,
        "missing_evidence": missing,
    }
