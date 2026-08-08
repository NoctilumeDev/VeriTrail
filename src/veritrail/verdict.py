from __future__ import annotations

from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.evidence import ImportedEvidence

MISSING = object()
DECISIVE_SEVERITIES = {"HARD", "DEGRADATION_BOUNDARY"}


def _json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    current = document
    for raw_part in pointer.split("/")[1:]:
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return MISSING
    return current


def _same_value(left: Any, right: Any) -> bool:
    if left is MISSING or right is MISSING:
        return left is right
    return canonical_json_bytes(left) == canonical_json_bytes(right)


def _apply_operator(actual: Any, operator: str, expected: Any) -> bool:
    if operator == "exists":
        return (actual is not MISSING) is bool(expected)
    if actual is MISSING:
        return False
    if operator == "eq":
        return _same_value(actual, expected)
    if operator == "ne":
        return not _same_value(actual, expected)
    if operator == "lt":
        return actual < expected
    if operator == "lte":
        return actual <= expected
    if operator == "gt":
        return actual > expected
    if operator == "gte":
        return actual >= expected
    if operator == "contains":
        return expected in actual
    raise ValueError(f"unsupported operator: {operator}")


def _evaluate_assertions(plan: dict[str, Any], evidence: list[ImportedEvidence]) -> list[dict[str, Any]]:
    by_type: dict[str, list[ImportedEvidence]] = {}
    for artifact in evidence:
        by_type.setdefault(artifact.document["evidence_type"], []).append(artifact)

    results: list[dict[str, Any]] = []
    for assertion in plan["assertions"]:
        matching = by_type.get(assertion["evidence_type"], [])
        values: list[tuple[Any, str]] = []
        for artifact in matching:
            actual = _json_pointer(artifact.document, assertion["path"])
            if actual is not MISSING or assertion["operator"] == "exists":
                values.append((actual, artifact.sha256))

        base = {
            "id": assertion["id"],
            "severity": assertion["severity"],
            "evidence_type": assertion["evidence_type"],
            "path": assertion["path"],
            "operator": assertion["operator"],
            "expected": assertion["expected"],
            "evidence_sha256": [digest for _, digest in values],
        }
        if not values:
            results.append(
                {
                    **base,
                    "status": "NOT_EVALUATED",
                    "actual": None,
                    "explanation": "No imported evidence supplied the required fact.",
                }
            )
            continue

        first = values[0][0]
        if any(not _same_value(first, value) for value, _ in values[1:]):
            results.append(
                {
                    **base,
                    "status": "CONFLICT",
                    "actual": [value for value, _ in values],
                    "explanation": "Evidence artifacts supplied conflicting values.",
                }
            )
            continue

        try:
            passed = _apply_operator(first, assertion["operator"], assertion["expected"])
        except (TypeError, ValueError) as exc:
            results.append(
                {
                    **base,
                    "status": "ERROR",
                    "actual": None if first is MISSING else first,
                    "explanation": f"Rule could not compare the supplied values: {exc}",
                }
            )
            continue
        results.append(
            {
                **base,
                "status": "PASS" if passed else "FAIL",
                "actual": None if first is MISSING else first,
                "explanation": "The deterministic comparison passed." if passed else "The deterministic comparison failed.",
            }
        )
    return results


def _detect_variable_contamination(
    plan: dict[str, Any], evidence: list[ImportedEvidence]
) -> list[dict[str, Any]]:
    declared = {variable["name"]: variable for variable in plan["variables"]}
    observed: dict[str, list[tuple[Any, str]]] = {}
    for artifact in evidence:
        for name, value in artifact.document.get("observed_variables", {}).items():
            observed.setdefault(name, []).append((value, artifact.sha256))

    contamination: list[dict[str, Any]] = []
    for name, observations in sorted(observed.items()):
        first = observations[0][0]
        if any(not _same_value(first, value) for value, _ in observations[1:]):
            contamination.append(
                {
                    "code": "OBSERVATION_CONFLICT",
                    "variable": name,
                    "evidence_sha256": [digest for _, digest in observations],
                    "message": f"Observed variable {name!r} has conflicting values.",
                }
            )
            continue
        variable = declared.get(name)
        if variable is None:
            contamination.append(
                {
                    "code": "UNKNOWN_VARIABLE",
                    "variable": name,
                    "evidence_sha256": [digest for _, digest in observations],
                    "message": f"Observed variable {name!r} was not declared by the sealed plan.",
                }
            )
        elif variable["role"] in {"PRIMARY", "CONTROLLED"} and not _same_value(first, variable["value"]):
            contamination.append(
                {
                    "code": "VARIABLE_DRIFT",
                    "variable": name,
                    "expected": variable["value"],
                    "actual": first,
                    "evidence_sha256": [digest for _, digest in observations],
                    "message": f"Observed {variable['role'].lower()} variable {name!r} drifted from the sealed value.",
                }
            )
    return contamination


def _detect_preflight_contamination(
    plan: dict[str, Any], evidence: list[ImportedEvidence], execution_status: str
) -> list[dict[str, Any]]:
    if plan.get("schema_version") not in {"0.2", "0.3"}:
        return []
    preflight = [
        artifact for artifact in evidence if artifact.document["evidence_type"] == "runtime.preflight"
    ]
    contamination: list[dict[str, Any]] = []
    if len(preflight) > 1:
        contamination.append(
            {
                "code": "MULTIPLE_PREFLIGHT_EVIDENCE",
                "message": "A single Run must contain exactly one runtime.preflight artifact.",
            }
        )
    for artifact in preflight:
        facts = artifact.document["facts"]
        if not _same_value(facts["policy"], plan["preflight"]):
            contamination.append(
                {
                    "code": "PREFLIGHT_POLICY_DRIFT",
                    "evidence_sha256": artifact.sha256,
                    "message": "The observed preflight policy differs from the sealed Plan 0.2 policy.",
                }
            )
        if facts["decision"] == "ABORT" and execution_status != "ABORTED":
            contamination.append(
                {
                    "code": "PREFLIGHT_STATUS_CONFLICT",
                    "evidence_sha256": artifact.sha256,
                    "message": "Preflight decided ABORT but the Run execution status is not ABORTED.",
                }
            )
    return contamination


def _detect_browser_contamination(
    plan: dict[str, Any], evidence: list[ImportedEvidence], execution_status: str
) -> list[dict[str, Any]]:
    if plan.get("schema_version") != "0.3":
        return []
    sessions = [
        artifact for artifact in evidence if artifact.document["evidence_type"] == "browser.session"
    ]
    contamination: list[dict[str, Any]] = []
    if len(sessions) > 1:
        contamination.append(
            {
                "code": "MULTIPLE_BROWSER_EVIDENCE",
                "message": "A Plan 0.3 Run must contain exactly one browser.session artifact.",
            }
        )
    for artifact in sessions:
        facts = artifact.document["facts"]
        if facts["policy_sha256"] != sha256_json(plan["browser"]):
            contamination.append(
                {
                    "code": "BROWSER_POLICY_DRIFT",
                    "evidence_sha256": artifact.sha256,
                    "message": "The browser session policy differs from the sealed Plan 0.3 policy.",
                }
            )
        if facts["capture_complete"] is False and execution_status == "COMPLETED":
            contamination.append(
                {
                    "code": "BROWSER_STATUS_CONFLICT",
                    "evidence_sha256": artifact.sha256,
                    "message": "Browser capture is incomplete but the Run execution status is COMPLETED.",
                }
            )
    return contamination


def evaluate(
    plan: dict[str, Any], evidence: list[ImportedEvidence], execution_status: str
) -> dict[str, Any]:
    evidence_types = sorted({item.document["evidence_type"] for item in evidence})
    missing_evidence = sorted(set(plan["required_evidence"]) - set(evidence_types))
    assertion_results = _evaluate_assertions(plan, evidence)
    contamination = _detect_variable_contamination(plan, evidence)
    contamination.extend(_detect_preflight_contamination(plan, evidence, execution_status))
    contamination.extend(_detect_browser_contamination(plan, evidence, execution_status))
    if plan["baseline"]["status"] == "EXPIRED":
        contamination.append(
            {
                "code": "BASELINE_EXPIRED",
                "message": "The sealed plan references an expired baseline.",
            }
        )
    for result in assertion_results:
        if result["status"] in {"CONFLICT", "ERROR"}:
            contamination.append(
                {
                    "code": "EVIDENCE_CONFLICT" if result["status"] == "CONFLICT" else "RULE_ERROR",
                    "assertion": result["id"],
                    "message": result["explanation"],
                }
            )

    failed = [
        result
        for result in assertion_results
        if result["severity"] in DECISIVE_SEVERITIES and result["status"] == "FAIL"
    ]
    unevaluated = [
        result
        for result in assertion_results
        if result["severity"] in DECISIVE_SEVERITIES and result["status"] == "NOT_EVALUATED"
    ]
    reasons: list[dict[str, str]] = []
    if failed:
        verdict = "FAIL"
        reasons.append(
            {
                "code": "DECISIVE_ASSERTION_FAILED",
                "message": f"{len(failed)} hard or degradation-boundary assertion(s) failed.",
            }
        )
    elif contamination:
        verdict = "INCONCLUSIVE"
        reasons.append(
            {
                "code": "CAUSAL_ATTRIBUTION_BLOCKED",
                "message": f"{len(contamination)} contamination or evidence-integrity issue(s) block attribution.",
            }
        )
    elif execution_status != "COMPLETED" or missing_evidence or unevaluated:
        verdict = "PENDING"
        if execution_status != "COMPLETED":
            reasons.append(
                {
                    "code": "EXECUTION_NOT_COMPLETED",
                    "message": f"Execution status is {execution_status}; available facts are not sufficient for PASS.",
                }
            )
        if missing_evidence:
            reasons.append(
                {
                    "code": "REQUIRED_EVIDENCE_MISSING",
                    "message": f"Missing evidence types: {', '.join(missing_evidence)}.",
                }
            )
        if unevaluated:
            reasons.append(
                {
                    "code": "DECISIVE_ASSERTION_NOT_EVALUATED",
                    "message": f"{len(unevaluated)} decisive assertion(s) lack an input fact.",
                }
            )
    else:
        verdict = "PASS"
        reasons.append(
            {
                "code": "ALL_DECISIVE_ASSERTIONS_PASSED",
                "message": "All required evidence is present and every decisive assertion passed.",
            }
        )

    return {
        "execution_status": execution_status,
        "verdict": verdict,
        "reasons": reasons,
        "missing_evidence": missing_evidence,
        "contamination": contamination,
        "assertions": assertion_results,
    }
