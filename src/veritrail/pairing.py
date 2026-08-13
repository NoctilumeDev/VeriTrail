from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.catalog import _CandidateRejected, validate_bundle
from veritrail.errors import VeriTrailError
from veritrail.jsonio import load_json_object
from veritrail.plan import verify_sealed_plan
from veritrail.privacy import redact_value

PAIRING_PLAN_SCHEMA_VERSION = "0.1"
PAIRED_ANALYSIS_SCHEMA_VERSION = "0.1"
PAIRING_RULE_VERSION = "paired-counterfactual/0.1"
PAIRING_ROLES = (
    "BASELINE",
    "TREATMENT",
    "RESTORED_BASELINE",
    "NEGATIVE_CONTROL",
)
ANALYSIS_STATUSES = {"SUPPORTED", "CONTRADICTED", "INCONCLUSIVE"}
PAIRING_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
MAX_PAIRING_PLAN_BYTES = 1024 * 1024


class PairingError(VeriTrailError):
    """Stable, sanitized failure exposed by M7 pairing commands."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class PairingBuildResult:
    analysis_id: str
    analysis_status: str
    attributable: bool
    outcome_count: int
    run_ids: tuple[str, str, str, str]


@dataclass(frozen=True)
class _SourceRun:
    report: dict[str, Any]
    plan: dict[str, Any]
    bundle_sha256: str
    control_projection_sha256: str


def _same(left: Any, right: Any) -> bool:
    return canonical_json_bytes(left) == canonical_json_bytes(right)


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, name: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{name} must be a non-empty list of strings")
    elif any(not _non_empty_string(item) for item in value):
        errors.append(f"{name} must contain only non-empty strings")


def validate_pairing_plan(plan: dict[str, Any]) -> None:
    errors: list[str] = []
    allowed = {
        "schema_version",
        "pairing_id",
        "version",
        "question",
        "primary_variable",
        "roles",
        "sequence",
        "warmup",
        "outcomes",
        "limits",
        "reproduction_steps",
        "cleanup_steps",
        "seal",
    }
    unknown = sorted(set(plan) - allowed)
    if unknown:
        errors.append(f"pairing plan has unsupported fields: {', '.join(unknown)}")
    if plan.get("schema_version") != PAIRING_PLAN_SCHEMA_VERSION:
        errors.append("schema_version must be '0.1'")
    pairing_id = plan.get("pairing_id")
    if not isinstance(pairing_id, str) or not PAIRING_ID_PATTERN.fullmatch(pairing_id):
        errors.append("pairing_id must be a 2-64 character lowercase identifier")
    version = plan.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        errors.append("version must be a positive integer")
    if not _non_empty_string(plan.get("question")):
        errors.append("question must be a non-empty string")

    primary = plan.get("primary_variable")
    if not isinstance(primary, dict):
        errors.append("primary_variable must be an object")
    else:
        unknown_primary = sorted(set(primary) - {"name", "source", "unit"})
        if unknown_primary:
            errors.append(
                "primary_variable has unsupported fields: " + ", ".join(unknown_primary)
            )
        for field in ("name", "source"):
            if not _non_empty_string(primary.get(field)):
                errors.append(f"primary_variable.{field} must be a non-empty string")
        if "unit" in primary and not _non_empty_string(primary.get("unit")):
            errors.append("primary_variable.unit must be a non-empty string when present")

    roles = plan.get("roles")
    role_values: dict[str, Any] = {}
    if not isinstance(roles, dict) or set(roles) != set(PAIRING_ROLES):
        errors.append("roles must contain exactly the four fixed M7 roles")
    else:
        for role in PAIRING_ROLES:
            item = roles[role]
            if not isinstance(item, dict) or set(item) != {"plan_sha256", "primary_value"}:
                errors.append(f"roles.{role} must contain plan_sha256 and primary_value")
                continue
            digest = item.get("plan_sha256")
            if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
                errors.append(f"roles.{role}.plan_sha256 must be a lowercase SHA-256")
            role_values[role] = item.get("primary_value")
        if all(role in role_values for role in PAIRING_ROLES):
            if _same(role_values["BASELINE"], role_values["TREATMENT"]):
                errors.append("TREATMENT primary_value must differ from BASELINE")
            if not _same(role_values["BASELINE"], role_values["RESTORED_BASELINE"]):
                errors.append("RESTORED_BASELINE primary_value must equal BASELINE")
            if _same(role_values["NEGATIVE_CONTROL"], role_values["BASELINE"]) or _same(
                role_values["NEGATIVE_CONTROL"], role_values["TREATMENT"]
            ):
                errors.append(
                    "NEGATIVE_CONTROL primary_value must differ from BASELINE and TREATMENT"
                )
            if roles["BASELINE"].get("plan_sha256") != roles["RESTORED_BASELINE"].get(
                "plan_sha256"
            ):
                errors.append(
                    "RESTORED_BASELINE plan_sha256 must exactly equal BASELINE plan_sha256"
                )

    if plan.get("sequence") != list(PAIRING_ROLES):
        errors.append("sequence must be the fixed four-role M7 order")
    if plan.get("warmup") != {"mode": "NONE", "iterations": 0}:
        errors.append("warmup must be exactly NONE with zero iterations in PairingPlan 0.1")

    outcomes = plan.get("outcomes")
    outcome_ids: set[str] = set()
    treatment_effect_declared = False
    if not isinstance(outcomes, list) or not 1 <= len(outcomes) <= 64:
        errors.append("outcomes must contain 1-64 entries")
    else:
        for index, outcome in enumerate(outcomes):
            prefix = f"outcomes[{index}]"
            if not isinstance(outcome, dict) or set(outcome) != {
                "assertion_id",
                "expected_actual",
            }:
                errors.append(f"{prefix} must contain assertion_id and expected_actual")
                continue
            assertion_id = outcome.get("assertion_id")
            if not _non_empty_string(assertion_id):
                errors.append(f"{prefix}.assertion_id must be a non-empty string")
            elif assertion_id in outcome_ids:
                errors.append(f"{prefix}.assertion_id duplicates {assertion_id!r}")
            else:
                outcome_ids.add(assertion_id)
            expected = outcome.get("expected_actual")
            if not isinstance(expected, dict) or set(expected) != set(PAIRING_ROLES):
                errors.append(f"{prefix}.expected_actual must contain exactly the four roles")
                continue
            baseline_expected = expected["BASELINE"]
            if not _same(expected["RESTORED_BASELINE"], baseline_expected):
                errors.append(f"{prefix} restored expectation must equal baseline")
            if not _same(expected["NEGATIVE_CONTROL"], baseline_expected):
                errors.append(f"{prefix} negative-control expectation must equal baseline")
            if not _same(expected["TREATMENT"], baseline_expected):
                treatment_effect_declared = True
    if isinstance(outcomes, list) and outcomes and not treatment_effect_declared:
        errors.append("at least one outcome must declare a treatment effect")

    _string_list(plan.get("limits"), "limits", errors)
    _string_list(plan.get("reproduction_steps"), "reproduction_steps", errors)
    _string_list(plan.get("cleanup_steps"), "cleanup_steps", errors)
    try:
        canonical_json_bytes({key: value for key, value in plan.items() if key != "seal"})
    except (TypeError, ValueError) as exc:
        errors.append(f"pairing plan must contain finite JSON values: {exc}")
    _, sensitive_count = redact_value(
        {key: value for key, value in plan.items() if key != "seal"}
    )
    if sensitive_count:
        errors.append(
            f"pairing plan contains {sensitive_count} sensitive value(s) or personal path(s)"
        )
    if errors:
        raise PairingError("PAIRING_PLAN_INVALID", "; ".join(errors))


def pairing_plan_digest(plan: dict[str, Any]) -> str:
    return sha256_json({key: value for key, value in plan.items() if key != "seal"})


def seal_pairing_plan(plan: dict[str, Any]) -> dict[str, Any]:
    validate_pairing_plan(plan)
    sealed = copy.deepcopy(plan)
    sealed["seal"] = {"algorithm": "sha256", "digest": pairing_plan_digest(sealed)}
    return sealed


def verify_sealed_pairing_plan(plan: dict[str, Any]) -> None:
    validate_pairing_plan(plan)
    seal = plan.get("seal")
    if not isinstance(seal, dict) or set(seal) != {"algorithm", "digest"}:
        raise PairingError("PAIRING_PLAN_UNSEALED", "PairingPlan 没有有效 seal。")
    if seal.get("algorithm") != "sha256" or seal.get("digest") != pairing_plan_digest(plan):
        raise PairingError("PAIRING_PLAN_SEAL_MISMATCH", "PairingPlan seal 与规范内容不一致。")


def load_and_seal_pairing_plan(path: Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > MAX_PAIRING_PLAN_BYTES:
            raise PairingError("PAIRING_PLAN_TOO_LARGE", "PairingPlan 超过 1 MiB 上限。")
        plan = load_json_object(path, label="PairingPlan")
    except PairingError:
        raise
    except Exception as exc:
        raise PairingError("PAIRING_PLAN_UNREADABLE", "PairingPlan 无法安全读取。") from exc
    if "seal" in plan:
        verify_sealed_pairing_plan(plan)
        return plan
    return seal_pairing_plan(plan)


def load_sealed_pairing_plan(path: Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > MAX_PAIRING_PLAN_BYTES:
            raise PairingError("PAIRING_PLAN_TOO_LARGE", "PairingPlan 超过 1 MiB 上限。")
        plan = load_json_object(path, label="PairingPlan")
    except PairingError:
        raise
    except Exception as exc:
        raise PairingError("PAIRING_PLAN_UNREADABLE", "PairingPlan 无法安全读取。") from exc
    if "seal" not in plan:
        raise PairingError("PAIRING_PLAN_UNSEALED", "pair 命令只接受已封存 PairingPlan。")
    verify_sealed_pairing_plan(plan)
    return plan


def write_sealed_pairing_plan(path: Path, plan: dict[str, Any]) -> None:
    if path.exists():
        raise PairingError("PAIRING_PLAN_OUTPUT_EXISTS", "拒绝覆盖已有 PairingPlan 输出。")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(canonical_json_bytes(plan) + b"\n")
    except FileExistsError as exc:
        raise PairingError("PAIRING_PLAN_OUTPUT_EXISTS", "拒绝覆盖已有 PairingPlan 输出。") from exc
    except Exception:
        if path.exists():
            path.unlink()
        raise


def _validate_report_plan_cross_reference(report: dict[str, Any], plan: dict[str, Any]) -> None:
    primary = next(item for item in plan["variables"] if item["role"] == "PRIMARY")
    expected = {
        "subject": plan["subject"],
        "baseline": plan["baseline"],
        "random_seed": plan["random_seed"],
        "primary_variable": primary,
        "load_model": plan["load_model"],
        "resource_budget": plan["resource_budget"],
        "change_scope": plan["change_scope"],
        "reproduction_steps": plan["reproduction_steps"],
        "cleanup_steps": plan["cleanup_steps"],
    }
    if any(not _same(report.get(key), value) for key, value in expected.items()):
        raise PairingError(
            "SOURCE_PLAN_REFERENCE_MISMATCH",
            "来源 Run 的报告事实与 sealed ExperimentPlan 不一致。",
        )
    if report["plan"] != {
        "id": plan["plan_id"],
        "version": plan["version"],
        "sha256": plan["seal"]["digest"],
    }:
        raise PairingError(
            "SOURCE_PLAN_REFERENCE_MISMATCH",
            "来源 Run 的 ExperimentPlan 引用不一致。",
        )
    planned = {item["id"]: item for item in plan["assertions"]}
    observed = {item["id"]: item for item in report["assertions"]}
    if set(planned) != set(observed):
        raise PairingError(
            "SOURCE_PLAN_REFERENCE_MISMATCH", "来源 Run 的断言集合与 Plan 不一致。"
        )
    for assertion_id, definition in planned.items():
        for field in ("severity", "evidence_type", "path", "operator", "expected"):
            if not _same(observed[assertion_id].get(field), definition[field]):
                raise PairingError(
                    "SOURCE_PLAN_REFERENCE_MISMATCH", "来源 Run 的断言定义与 Plan 不一致。"
                )


def _control_projection(plan: dict[str, Any], primary_name: str) -> dict[str, Any]:
    projection = copy.deepcopy({key: value for key, value in plan.items() if key != "seal"})
    projection["version"] = "<PAIRING_VERSION>"
    primary_matches = [
        item
        for item in projection["variables"]
        if item.get("role") == "PRIMARY" and item.get("name") == primary_name
    ]
    if len(primary_matches) == 1:
        primary_matches[0]["value"] = "<PAIRING_PRIMARY_VALUE>"
    return projection


def _load_source(candidate: Path, primary_name: str) -> _SourceRun:
    candidate = candidate.absolute()
    try:
        validated = validate_bundle(candidate, candidate.parent)
    except (_CandidateRejected, OSError, ValueError) as exc:
        code = exc.code if isinstance(exc, _CandidateRejected) else "SOURCE_BUNDLE_UNREADABLE"
        raise PairingError(code, "来源 Run Bundle 未通过完整性校验。") from exc
    if "sealed-plan.json" not in {item.path for item in validated.files}:
        raise PairingError(
            "SOURCE_SEALED_PLAN_MISSING", "来源 Run Bundle 没有声明 sealed-plan.json。"
        )
    try:
        plan = load_json_object(candidate / "sealed-plan.json", label="Sealed ExperimentPlan")
        report = load_json_object(candidate / "report.json", label="Report")
        if plan.get("schema_version") == "0.6":
            raise PairingError(
                "SOURCE_PLAN_VERSION_UNSUPPORTED",
                "M7 Pairing 尚无 Plan 0.6 / ProjectProfile 兼容合同。",
            )
        verify_sealed_plan(plan)
    except PairingError:
        raise
    except Exception as exc:
        raise PairingError(
            "SOURCE_SEALED_PLAN_INVALID", "来源 Run 的 sealed ExperimentPlan 无效。"
        ) from exc
    _validate_report_plan_cross_reference(report, plan)
    projection = _control_projection(plan, primary_name)
    return _SourceRun(
        report=report,
        plan=plan,
        bundle_sha256=validated.bundle_sha256,
        control_projection_sha256=sha256_json(projection),
    )


def _source_reference(source: _SourceRun, role: str) -> dict[str, Any]:
    primary = next(item for item in source.plan["variables"] if item["role"] == "PRIMARY")
    return {
        "role": role,
        "run_id": source.report["run_id"],
        "created_at": source.report["created_at"],
        "execution_status": source.report["execution_status"],
        "verdict": source.report["verdict"],
        "plan": copy.deepcopy(source.report["plan"]),
        "random_seed": source.report["random_seed"],
        "primary_variable": copy.deepcopy(primary),
        "bundle_sha256": source.bundle_sha256,
        "control_projection_sha256": source.control_projection_sha256,
    }


def _assertion_projection(assertion: dict[str, Any]) -> dict[str, Any]:
    return {
        "severity": assertion["severity"],
        "status": assertion["status"],
        "operator": assertion.get("operator"),
        "path": assertion.get("path"),
        "evidence_type": assertion.get("evidence_type"),
        "expected": copy.deepcopy(assertion.get("expected")),
        "actual": copy.deepcopy(assertion.get("actual")),
    }


def _markdown_text(value: Any) -> str:
    rendered = str(value)
    for source, replacement in (
        ("\\", "\\\\"),
        ("`", "\\`"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ("!", "\\!"),
        ("[", "\\["),
        ("]", "\\]"),
        ("(", "\\("),
        (")", "\\)"),
    ):
        rendered = rendered.replace(source, replacement)
    return rendered.replace("\r", " ").replace("\n", " ")


def _render_markdown(analysis: dict[str, Any]) -> str:
    lines = [
        "# VeriTrail Paired Counterfactual Analysis",
        "",
        f"- Analysis: `{analysis['analysis_id']}`",
        f"- Pairing plan: `{analysis['pairing_plan']['id']}` / `{analysis['pairing_plan']['sha256']}`",
        f"- Rule: `{analysis['rule_version']}`",
        f"- Status: **{analysis['analysis_status']}**",
        f"- Attributable: `{str(analysis['attributable']).lower()}`",
        "",
        "## Sources",
        "",
    ]
    for role in PAIRING_ROLES:
        source = analysis["sources"][role]
        lines.append(
            f"- {role}: `{source['run_id']}` — `{source['execution_status']}` / "
            f"`{source['verdict']}` — primary `{json.dumps(source['primary_variable']['value'], ensure_ascii=False, sort_keys=True)}`"
        )
    lines.extend(["", "## Reasons", ""])
    lines.extend(f"- `{item['code']}` — {item['message']}" for item in analysis["reasons"])
    lines.extend(["", "## Outcomes", ""])
    for outcome in analysis["outcomes"]:
        lines.append(f"### `{outcome['assertion_id']}`")
        lines.append("")
        for role in PAIRING_ROLES:
            observation = outcome["roles"][role]
            expected = json.dumps(
                observation["expected_actual"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            actual = json.dumps(
                observation["actual"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            lines.append(
                f"- {role}: expected `{expected}`; actual `{actual}`; "
                f"match `{str(observation['matches']).lower()}`"
            )
        lines.append("")
    lines.extend(["## Unplanned assertion drift", ""])
    if analysis["unplanned_differences"]:
        for item in analysis["unplanned_differences"]:
            lines.append(f"- `{item['role']}` / `{item['assertion_id']}`")
    else:
        lines.append("- None.")
    lines.extend(["", "## Boundary", ""])
    lines.extend(f"- {_markdown_text(item)}" for item in analysis["limits"])
    lines.append("")
    return "\n".join(lines)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _file_entry(path: Path, relative: str) -> dict[str, Any]:
    return {"path": relative, "sha256": _sha256_file(path), "size": path.stat().st_size}


def create_paired_analysis_bundle(
    *,
    pairing_plan_path: Path,
    baseline: Path,
    treatment: Path,
    restored_baseline: Path,
    negative_control: Path,
    output: Path,
) -> PairingBuildResult:
    if output.exists():
        raise PairingError("PAIRED_OUTPUT_EXISTS", "拒绝覆盖已有 PairedAnalysis 输出目录。")
    pairing_plan = load_sealed_pairing_plan(pairing_plan_path)
    primary_definition = pairing_plan["primary_variable"]
    source_paths = {
        "BASELINE": baseline,
        "TREATMENT": treatment,
        "RESTORED_BASELINE": restored_baseline,
        "NEGATIVE_CONTROL": negative_control,
    }
    sources = {
        role: _load_source(source_paths[role], primary_definition["name"])
        for role in PAIRING_ROLES
    }
    reasons: list[dict[str, str]] = []

    run_ids = [sources[role].report["run_id"] for role in PAIRING_ROLES]
    if len(set(run_ids)) != len(PAIRING_ROLES):
        reasons.append(
            {"code": "RUN_ID_REUSED", "message": "四角色必须引用四个不同的 Run ID。"}
        )
    bundle_digests = [sources[role].bundle_sha256 for role in PAIRING_ROLES]
    if len(set(bundle_digests)) != len(PAIRING_ROLES):
        reasons.append(
            {"code": "BUNDLE_REUSED", "message": "四角色必须引用四个不同的 Run Bundle。"}
        )
    incomplete = [
        role
        for role in PAIRING_ROLES
        if sources[role].report["execution_status"] != "COMPLETED"
    ]
    if incomplete:
        reasons.append(
            {"code": "RUN_NOT_COMPLETED", "message": f"{', '.join(incomplete)} Run 未完整执行。"}
        )
    try:
        created = [
            datetime.fromisoformat(sources[role].report["created_at"].replace("Z", "+00:00"))
            for role in PAIRING_ROLES
        ]
    except (TypeError, ValueError):
        created = []
    if len(created) != len(PAIRING_ROLES) or any(
        left >= right for left, right in zip(created, created[1:])
    ):
        reasons.append(
            {"code": "ROLE_ORDER_MISMATCH", "message": "Run 创建时间不符合预注册四角色顺序。"}
        )

    plan_mismatches = [
        role
        for role in PAIRING_ROLES
        if sources[role].report["plan"]["sha256"]
        != pairing_plan["roles"][role]["plan_sha256"]
    ]
    if plan_mismatches:
        reasons.append(
            {
                "code": "ROLE_PLAN_DIGEST_MISMATCH",
                "message": f"{', '.join(plan_mismatches)} 未引用预注册 ExperimentPlan。",
            }
        )
    seeds = {sources[role].report["random_seed"] for role in PAIRING_ROLES}
    if len(seeds) != 1:
        reasons.append(
            {"code": "RANDOM_SEED_MISMATCH", "message": "四角色随机种子不一致。"}
        )

    primary_mismatches: list[str] = []
    for role in PAIRING_ROLES:
        primary = next(item for item in sources[role].plan["variables"] if item["role"] == "PRIMARY")
        expected_unit = primary_definition.get("unit")
        if (
            primary.get("name") != primary_definition["name"]
            or primary.get("source") != primary_definition["source"]
            or primary.get("unit") != expected_unit
            or not _same(primary.get("value"), pairing_plan["roles"][role]["primary_value"])
        ):
            primary_mismatches.append(role)
    if primary_mismatches:
        reasons.append(
            {
                "code": "PRIMARY_VARIABLE_MISMATCH",
                "message": f"{', '.join(primary_mismatches)} 主要变量不符合 PairingPlan。",
            }
        )
    control_digests = {sources[role].control_projection_sha256 for role in PAIRING_ROLES}
    if len(control_digests) != 1:
        reasons.append(
            {
                "code": "CONTROL_PROJECTION_MISMATCH",
                "message": "ExperimentPlan 在版本和唯一主要变量值之外发生漂移。",
            }
        )

    report_assertions = {
        role: {item["id"]: item for item in sources[role].report["assertions"]}
        for role in PAIRING_ROLES
    }
    outcome_ids = {item["assertion_id"] for item in pairing_plan["outcomes"]}
    missing_outcomes = sorted(
        {
            f"{role}:{outcome_id}"
            for role in PAIRING_ROLES
            for outcome_id in outcome_ids
            if outcome_id not in report_assertions[role]
        }
    )
    if missing_outcomes:
        reasons.append(
            {"code": "OUTCOME_MISSING", "message": "预注册 outcome 在来源 Report 中缺失。"}
        )

    unplanned_differences: list[dict[str, Any]] = []
    baseline_assertions = report_assertions["BASELINE"]
    for role in PAIRING_ROLES[1:]:
        for assertion_id in sorted(set(baseline_assertions) - outcome_ids):
            baseline_projection = _assertion_projection(baseline_assertions[assertion_id])
            candidate = report_assertions[role].get(assertion_id)
            observed_projection = _assertion_projection(candidate) if candidate else None
            if not _same(baseline_projection, observed_projection):
                unplanned_differences.append(
                    {
                        "role": role,
                        "assertion_id": assertion_id,
                        "baseline": baseline_projection,
                        "observed": observed_projection,
                    }
                )
    if unplanned_differences:
        reasons.append(
            {
                "code": "UNDECLARED_OUTCOME_DRIFT",
                "message": "非 outcome 断言出现未预注册漂移。",
            }
        )

    outcomes: list[dict[str, Any]] = []
    mismatch_roles: set[str] = set()
    for definition in pairing_plan["outcomes"]:
        assertion_id = definition["assertion_id"]
        role_observations: dict[str, Any] = {}
        for role in PAIRING_ROLES:
            assertion = report_assertions[role].get(assertion_id)
            actual = copy.deepcopy(assertion.get("actual")) if assertion else None
            expected_actual = copy.deepcopy(definition["expected_actual"][role])
            matches = assertion is not None and _same(actual, expected_actual)
            if not matches:
                mismatch_roles.add(role)
            role_observations[role] = {
                "expected_actual": expected_actual,
                "actual": actual,
                "matches": matches,
            }
        outcomes.append({"assertion_id": assertion_id, "roles": role_observations})

    if "BASELINE" in mismatch_roles:
        reasons.append(
            {
                "code": "BASELINE_OUTCOME_MISMATCH",
                "message": "基线 outcome 未命中预注册值，不能建立起点。",
            }
        )
    if "RESTORED_BASELINE" in mismatch_roles:
        reasons.append(
            {
                "code": "RESTORED_BASELINE_NOT_RESTORED",
                "message": "恢复基线未回到预注册 outcome。",
            }
        )
    if "NEGATIVE_CONTROL" in mismatch_roles:
        reasons.append(
            {
                "code": "NEGATIVE_CONTROL_EFFECT",
                "message": "负对照出现了不应出现的 outcome 变化。",
            }
        )

    inconclusive_codes = {item["code"] for item in reasons}
    if inconclusive_codes:
        analysis_status = "INCONCLUSIVE"
        attributable = False
    elif "TREATMENT" in mismatch_roles:
        analysis_status = "CONTRADICTED"
        attributable = True
        reasons.append(
            {
                "code": "TREATMENT_EFFECT_CONTRADICTED",
                "message": "处理组未出现预注册处理效果，完整配对反驳本轮处理假设。",
            }
        )
    else:
        analysis_status = "SUPPORTED"
        attributable = True
        reasons.append(
            {
                "code": "PAIRED_EFFECT_SUPPORTED",
                "message": "处理效果出现、恢复后消失且负对照未复制该效果。",
            }
        )

    pairing_digest = pairing_plan["seal"]["digest"]
    analysis_id = "pair_" + sha256_json(
        {
            "schema_version": PAIRED_ANALYSIS_SCHEMA_VERSION,
            "rule_version": PAIRING_RULE_VERSION,
            "pairing_plan_sha256": pairing_digest,
            "ordered_bundle_sha256": bundle_digests,
        }
    )[:24]
    analysis = {
        "schema_version": PAIRED_ANALYSIS_SCHEMA_VERSION,
        "analysis_id": analysis_id,
        "analysis_type": "FOUR_ROLE_PAIRED_COUNTERFACTUAL",
        "rule_version": PAIRING_RULE_VERSION,
        "analysis_status": analysis_status,
        "attributable": attributable,
        "pairing_plan": {
            "id": pairing_plan["pairing_id"],
            "version": pairing_plan["version"],
            "sha256": pairing_digest,
        },
        "sequence": list(PAIRING_ROLES),
        "warmup": copy.deepcopy(pairing_plan["warmup"]),
        "primary_variable": copy.deepcopy(primary_definition),
        "reasons": reasons,
        "sources": {role: _source_reference(sources[role], role) for role in PAIRING_ROLES},
        "outcomes": outcomes,
        "unplanned_differences": unplanned_differences,
        "limits": copy.deepcopy(pairing_plan["limits"]),
    }

    output = output.absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-pairing-", dir=output.parent))
    try:
        (stage / "sealed-pairing-plan.json").write_bytes(
            canonical_json_bytes(pairing_plan) + b"\n"
        )
        (stage / "paired-analysis.json").write_bytes(canonical_json_bytes(analysis) + b"\n")
        (stage / "paired-analysis.md").write_text(
            _render_markdown(analysis), encoding="utf-8", newline="\n"
        )
        files = [
            _file_entry(stage / "sealed-pairing-plan.json", "sealed-pairing-plan.json"),
            _file_entry(stage / "paired-analysis.json", "paired-analysis.json"),
            _file_entry(stage / "paired-analysis.md", "paired-analysis.md"),
        ]
        manifest = {
            "schema_version": PAIRED_ANALYSIS_SCHEMA_VERSION,
            "analysis_id": analysis_id,
            "files": files,
        }
        (stage / "paired-analysis-manifest.json").write_bytes(
            canonical_json_bytes(manifest) + b"\n"
        )
        stage.rename(output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return PairingBuildResult(
        analysis_id=analysis_id,
        analysis_status=analysis_status,
        attributable=attributable,
        outcome_count=len(outcomes),
        run_ids=tuple(run_ids),  # type: ignore[arg-type]
    )
