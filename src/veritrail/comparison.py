from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from veritrail.atomic_publish import publish_staged_directory
from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.catalog import _CandidateRejected, validate_bundle
from veritrail.errors import VeriTrailError
from veritrail.jsonio import load_json_object
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile

COMPARISON_SCHEMA_VERSION = "0.1"
COMPARISON_RULE_VERSION = "rerun-semantic/0.1"
COMPARISON_STATUSES = {"MATCH", "DRIFT", "INCONCLUSIVE"}
COMPARISON_ID_PREFIX = "cmp_"


class ComparisonError(VeriTrailError):
    """Stable, sanitized failure exposed by the M6 comparison command."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class ComparisonBuildResult:
    comparison_id: str
    comparison_status: str
    comparable: bool
    difference_count: int
    baseline_run_id: str
    repeat_run_id: str


@dataclass(frozen=True)
class _SourceRun:
    report: dict[str, Any]
    plan: dict[str, Any]
    bundle_sha256: str
    semantic_projection: dict[str, Any]
    semantic_sha256: str
    profile_sha256: str | None


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _same(left: Any, right: Any) -> bool:
    return canonical_json_bytes(left) == canonical_json_bytes(right)


def _strip_evidence_digests(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_evidence_digests(item)
            for key, item in sorted(value.items())
            if key != "evidence_sha256"
        }
    if isinstance(value, list):
        return [_strip_evidence_digests(item) for item in value]
    return copy.deepcopy(value)


def _artifact_shape(artifact: dict[str, Any]) -> dict[str, Any]:
    attachments = [
        {
            "logical_name": attachment["logical_name"],
            "media_type": attachment["media_type"],
        }
        for attachment in artifact["attachments"]
    ]
    attachments.sort(key=lambda item: canonical_json_bytes(item))
    shape = {
        "evidence_type": artifact["evidence_type"],
        "source": artifact["source"],
        "parser_version": artifact["parser_version"],
        "redaction_rule_version": artifact["redaction_rule_version"],
        "retention": artifact["retention"],
        "redacted": artifact["redacted"],
        "redacted_fields": artifact["redacted_fields"],
        "attachments": attachments,
    }
    if "summary" in artifact:
        shape["summary"] = copy.deepcopy(artifact["summary"])
    return shape


def _semantic_projection(report: dict[str, Any]) -> dict[str, Any]:
    assertions: dict[str, dict[str, Any]] = {}
    for assertion in report["assertions"]:
        assertions[assertion["id"]] = {
            "severity": assertion["severity"],
            "status": assertion["status"],
            "operator": assertion.get("operator"),
            "path": assertion.get("path"),
            "evidence_type": assertion.get("evidence_type"),
            "expected": copy.deepcopy(assertion.get("expected")),
            "actual": copy.deepcopy(assertion.get("actual")),
        }
    evidence_shape = [_artifact_shape(artifact) for artifact in report["evidence"]]
    evidence_shape.sort(key=lambda item: canonical_json_bytes(item))
    contamination = [_strip_evidence_digests(item) for item in report["contamination"]]
    contamination.sort(key=lambda item: canonical_json_bytes(item))
    return {
        "execution_status": report["execution_status"],
        "verdict": report["verdict"],
        "reason_codes": [reason["code"] for reason in report["reasons"]],
        "assertions": {key: assertions[key] for key in sorted(assertions)},
        "missing_evidence": sorted(report["missing_evidence"]),
        "contamination": contamination,
        "evidence_shape": evidence_shape,
    }


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
        raise ComparisonError(
            "SOURCE_PLAN_REFERENCE_MISMATCH",
            "来源 Run 的报告事实与 sealed Plan 不一致。",
        )
    if report["plan"] != {
        "id": plan["plan_id"],
        "version": plan["version"],
        "sha256": plan["seal"]["digest"],
    }:
        raise ComparisonError(
            "SOURCE_PLAN_REFERENCE_MISMATCH",
            "来源 Run 的 Plan 引用与 sealed Plan 不一致。",
        )
    plan_assertions = {item["id"]: item for item in plan["assertions"]}
    report_assertions = {item["id"]: item for item in report["assertions"]}
    if set(plan_assertions) != set(report_assertions):
        raise ComparisonError(
            "SOURCE_PLAN_REFERENCE_MISMATCH",
            "来源 Run 的断言集合与 sealed Plan 不一致。",
        )
    for assertion_id, planned in plan_assertions.items():
        actual = report_assertions[assertion_id]
        for field in ("severity", "evidence_type", "path", "operator", "expected"):
            if not _same(actual.get(field), planned[field]):
                raise ComparisonError(
                    "SOURCE_PLAN_REFERENCE_MISMATCH",
                    "来源 Run 的断言定义与 sealed Plan 不一致。",
                )


def _load_source(candidate: Path) -> _SourceRun:
    candidate = candidate.absolute()
    try:
        validated = validate_bundle(candidate, candidate.parent)
    except (_CandidateRejected, OSError, ValueError) as exc:
        code = exc.code if isinstance(exc, _CandidateRejected) else "SOURCE_BUNDLE_UNREADABLE"
        raise ComparisonError(code, "来源 Run Bundle 未通过完整性校验。") from exc
    declared = {item.path for item in validated.files}
    if "sealed-plan.json" not in declared:
        raise ComparisonError(
            "SOURCE_SEALED_PLAN_MISSING",
            "来源 Run Bundle 没有声明 sealed-plan.json。",
        )
    try:
        plan = load_json_object(candidate / "sealed-plan.json", label="Sealed Plan")
        report = load_json_object(candidate / "report.json", label="Report")
        profile_sha256: str | None = None
        if plan.get("schema_version") in {"0.6", "0.7"}:
            if "sealed-profile.json" not in declared:
                raise ValueError("missing sealed ProjectProfile")
            profile = load_json_object(
                candidate / "sealed-profile.json", label="Sealed ProjectProfile"
            )
            verify_sealed_project_profile(profile)
            verify_sealed_plan(plan, profile)
            profile_sha256 = profile["seal"]["digest"]
        else:
            verify_sealed_plan(plan)
    except Exception as exc:
        raise ComparisonError(
            "SOURCE_SEALED_PLAN_INVALID",
            "来源 Run 的 sealed Plan 无效。",
        ) from exc
    _validate_report_plan_cross_reference(report, plan)
    projection = _semantic_projection(report)
    return _SourceRun(
        report=report,
        plan=plan,
        bundle_sha256=validated.bundle_sha256,
        semantic_projection=projection,
        semantic_sha256=sha256_json(projection),
        profile_sha256=profile_sha256,
    )


def _escape_pointer(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _differences(left: Any, right: Any, path: str = "") -> list[dict[str, Any]]:
    if _same(left, right):
        return []
    if isinstance(left, dict) and isinstance(right, dict):
        differences: list[dict[str, Any]] = []
        for key in sorted(set(left) | set(right)):
            child = f"{path}/{_escape_pointer(key)}"
            if key not in left:
                differences.append(
                    {
                        "path": child,
                        "baseline_present": False,
                        "repeat_present": True,
                        "baseline": None,
                        "repeat": copy.deepcopy(right[key]),
                    }
                )
            elif key not in right:
                differences.append(
                    {
                        "path": child,
                        "baseline_present": True,
                        "repeat_present": False,
                        "baseline": copy.deepcopy(left[key]),
                        "repeat": None,
                    }
                )
            else:
                differences.extend(_differences(left[key], right[key], child))
        return differences
    return [
        {
            "path": path or "/",
            "baseline_present": True,
            "repeat_present": True,
            "baseline": copy.deepcopy(left),
            "repeat": copy.deepcopy(right),
        }
    ]


def _source_reference(source: _SourceRun, role: str) -> dict[str, Any]:
    report = source.report
    reference = {
        "role": role,
        "run_id": report["run_id"],
        "created_at": report["created_at"],
        "execution_status": report["execution_status"],
        "verdict": report["verdict"],
        "plan": copy.deepcopy(report["plan"]),
        "random_seed": report["random_seed"],
        "bundle_sha256": source.bundle_sha256,
        "semantic_sha256": source.semantic_sha256,
    }
    if source.profile_sha256 is not None:
        reference["project_profile_sha256"] = source.profile_sha256
    return reference


def _render_markdown(comparison: dict[str, Any]) -> str:
    baseline = comparison["sources"]["baseline"]
    repeat = comparison["sources"]["repeat"]
    lines = [
        "# VeriTrail Rerun Comparison",
        "",
        f"- Comparison: `{comparison['comparison_id']}`",
        f"- Rule: `{comparison['rule_version']}`",
        f"- Status: **{comparison['comparison_status']}**",
        f"- Comparable: `{str(comparison['comparable']).lower()}`",
        "",
        "## Sources",
        "",
        f"- Baseline: `{baseline['run_id']}` — `{baseline['execution_status']}` / `{baseline['verdict']}`",
        f"- Repeat: `{repeat['run_id']}` — `{repeat['execution_status']}` / `{repeat['verdict']}`",
        f"- Plan: `{baseline['plan']['id']}` / `{baseline['plan']['sha256']}`",
        "",
        "## Reasons",
        "",
    ]
    lines.extend(
        f"- `{reason['code']}` — {reason['message']}" for reason in comparison["reasons"]
    )
    lines.extend(["", "## Differences", ""])
    if comparison["differences"]:
        for difference in comparison["differences"]:
            baseline_value = json.dumps(
                difference["baseline"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            repeat_value = json.dumps(
                difference["repeat"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            lines.append(
                f"- `{difference['path']}` — baseline `{baseline_value}`; repeat `{repeat_value}`"
            )
    else:
        lines.append("- No differences in the frozen M6 semantic projection.")
    lines.extend(["", "## Boundary", ""])
    lines.extend(f"- {item}" for item in comparison["limits"])
    lines.append("")
    return "\n".join(lines)


def _file_entry(path: Path, relative: str) -> dict[str, Any]:
    return {"path": relative, "sha256": _sha256_file(path), "size": path.stat().st_size}


def create_comparison_bundle(
    *, baseline: Path, repeat: Path, output: Path
) -> ComparisonBuildResult:
    if output.exists():
        raise ComparisonError("COMPARISON_OUTPUT_EXISTS", "拒绝覆盖已有 Comparison 输出目录。")
    baseline_source = _load_source(baseline)
    repeat_source = _load_source(repeat)
    differences = _differences(
        baseline_source.semantic_projection, repeat_source.semantic_projection
    )
    reasons: list[dict[str, str]] = []
    if baseline_source.report["run_id"] == repeat_source.report["run_id"]:
        reasons.append(
            {
                "code": "SAME_RUN_REUSED",
                "message": "两侧引用同一 Run ID，不能证明独立复跑。",
            }
        )
    if baseline_source.report["plan"]["sha256"] != repeat_source.report["plan"]["sha256"]:
        reasons.append(
            {
                "code": "PLAN_DIGEST_MISMATCH",
                "message": "两侧不是同一 sealed Plan，不能进行同计划复跑判断。",
            }
        )
    if baseline_source.profile_sha256 != repeat_source.profile_sha256:
        reasons.append(
            {
                "code": "PROFILE_DIGEST_MISMATCH",
                "message": "两侧不是同一 sealed ProjectProfile，不能进行 M10 同配置复跑判断。",
            }
        )
    if baseline_source.report["random_seed"] != repeat_source.report["random_seed"]:
        reasons.append(
            {
                "code": "RANDOM_SEED_MISMATCH",
                "message": "两侧随机种子不同，不能进行同种子复跑判断。",
            }
        )
    incomplete = [
        role
        for role, source in (("baseline", baseline_source), ("repeat", repeat_source))
        if source.report["execution_status"] != "COMPLETED"
    ]
    if incomplete:
        reasons.append(
            {
                "code": "RUN_NOT_COMPLETED",
                "message": f"{', '.join(incomplete)} Run 未完整执行。",
            }
        )
    comparable = not reasons
    if not comparable:
        comparison_status = "INCONCLUSIVE"
    elif differences:
        comparison_status = "DRIFT"
        reasons.append(
            {
                "code": "RERUN_SEMANTIC_DRIFT",
                "message": f"冻结语义投影存在 {len(differences)} 处差异。",
            }
        )
    else:
        comparison_status = "MATCH"
        reasons.append(
            {
                "code": "RERUN_SEMANTICS_MATCH",
                "message": "两次独立 Run 的冻结语义投影一致。",
            }
        )
    comparison_id = COMPARISON_ID_PREFIX + sha256_json(
        {
            "schema_version": COMPARISON_SCHEMA_VERSION,
            "rule_version": COMPARISON_RULE_VERSION,
            "baseline_bundle_sha256": baseline_source.bundle_sha256,
            "repeat_bundle_sha256": repeat_source.bundle_sha256,
        }
    )[:24]
    comparison = {
        "schema_version": COMPARISON_SCHEMA_VERSION,
        "comparison_id": comparison_id,
        "comparison_type": "SAME_PLAN_RERUN",
        "rule_version": COMPARISON_RULE_VERSION,
        "comparison_status": comparison_status,
        "comparable": comparable,
        "reasons": reasons,
        "sources": {
            "baseline": _source_reference(baseline_source, "BASELINE"),
            "repeat": _source_reference(repeat_source, "REPEAT"),
        },
        "differences": differences,
        "limits": [
            "MATCH 表示 M6 冻结语义投影一致，不等于来源 Run 的 Verdict 为 PASS。",
            "本比较不支持不同 Plan 的处理组因果归因。",
            "未进入 sealed assertion 或 Evidence 形态的原始业务事实不在本结论范围内。",
        ],
    }
    output = output.absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-comparison-", dir=output.parent))
    try:
        (stage / "comparison.json").write_bytes(canonical_json_bytes(comparison) + b"\n")
        (stage / "comparison.md").write_text(
            _render_markdown(comparison), encoding="utf-8", newline="\n"
        )
        files = [
            _file_entry(stage / "comparison.json", "comparison.json"),
            _file_entry(stage / "comparison.md", "comparison.md"),
        ]
        manifest = {
            "schema_version": COMPARISON_SCHEMA_VERSION,
            "comparison_id": comparison_id,
            "files": files,
        }
        (stage / "comparison-manifest.json").write_bytes(canonical_json_bytes(manifest) + b"\n")
        publish_staged_directory(stage, output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return ComparisonBuildResult(
        comparison_id=comparison_id,
        comparison_status=comparison_status,
        comparable=comparable,
        difference_count=len(differences),
        baseline_run_id=baseline_source.report["run_id"],
        repeat_run_id=repeat_source.report["run_id"],
    )
