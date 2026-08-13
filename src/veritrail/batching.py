from __future__ import annotations

import copy
import hashlib
import os
import re
import shutil
import stat
import tempfile
from dataclasses import dataclass
from datetime import datetime
from itertools import product
from pathlib import Path
from typing import Any

from veritrail.atomic_publish import publish_staged_directory
from veritrail.canonical import canonical_json_bytes, sha256_bytes, sha256_json
from veritrail.catalog import _CandidateRejected, validate_bundle
from veritrail.errors import VeriTrailError
from veritrail.jsonio import load_json_object
from veritrail.plan import verify_sealed_plan
from veritrail.privacy import redact_value

BATCH_PLAN_SCHEMA_VERSION = "0.1"
RUN_ASSIGNMENT_SCHEMA_VERSION = "0.1"
BATCH_ANALYSIS_SCHEMA_VERSION = "0.1"
BATCH_RULE_VERSION = "full-factorial-batch/0.1"
ORDER_ALGORITHM = "SHA256_RANK_V1"
PHASES = ("COVERAGE", "PERTURBATION")
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
MAX_DOCUMENT_BYTES = 1024 * 1024
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class BatchError(VeriTrailError):
    """Stable, sanitized failure exposed by M8 batch commands."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class BatchBuildResult:
    analysis_id: str
    coverage_status: str
    hypothesis_status: str
    slot_count: int
    source_count: int


@dataclass(frozen=True)
class _SourceRun:
    report: dict[str, Any]
    plan: dict[str, Any]
    bundle_sha256: str
    control_projection_sha256: str
    evidence: dict[str, dict[str, Any]]


def _same(left: Any, right: Any) -> bool:
    return canonical_json_bytes(left) == canonical_json_bytes(right)


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _string_list(value: Any, name: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{name} must be a non-empty list of strings")
    elif any(not _non_empty_string(item) for item in value):
        errors.append(f"{name} must contain only non-empty strings")


def _safe_relative_directory(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        return False
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        return False
    parts = value.split("/")
    return all(
        part not in {"", ".", ".."}
        and not part.startswith(".")
        and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", part))
        for part in parts
    )


def seeded_profile_order(profile_ids: list[str], seed: int, repetition: int) -> list[str]:
    """Return the cross-runtime SHA-256 rank order frozen by BatchPlan 0.1."""

    return sorted(
        profile_ids,
        key=lambda profile_id: (
            sha256_bytes(canonical_json_bytes([seed, repetition, profile_id])),
            profile_id,
        ),
    )


def _validate_dimensions(
    plan: dict[str, Any], errors: list[str]
) -> tuple[list[str], list[list[str]]]:
    dimensions = plan.get("dimensions")
    if not isinstance(dimensions, list) or not 2 <= len(dimensions) <= 4:
        errors.append("dimensions must contain 2-4 ordered dimensions")
        return [], []
    names: list[str] = []
    level_ids: list[list[str]] = []
    for index, dimension in enumerate(dimensions):
        prefix = f"dimensions[{index}]"
        if not isinstance(dimension, dict) or set(dimension) != {"name", "levels"}:
            errors.append(f"{prefix} must contain name and levels")
            continue
        name = dimension.get("name")
        if not isinstance(name, str) or not ID_PATTERN.fullmatch(name):
            errors.append(f"{prefix}.name must be a 2-64 character lowercase identifier")
            continue
        if name in names:
            errors.append(f"{prefix}.name duplicates {name!r}")
        names.append(name)
        levels = dimension.get("levels")
        if not isinstance(levels, list) or not 2 <= len(levels) <= 4:
            errors.append(f"{prefix}.levels must contain 2-4 ordered levels")
            level_ids.append([])
            continue
        ids: list[str] = []
        values: list[bytes] = []
        for level_index, level in enumerate(levels):
            level_prefix = f"{prefix}.levels[{level_index}]"
            if not isinstance(level, dict) or set(level) != {"id", "value"}:
                errors.append(f"{level_prefix} must contain id and value")
                continue
            level_id = level.get("id")
            if not isinstance(level_id, str) or not ID_PATTERN.fullmatch(level_id):
                errors.append(f"{level_prefix}.id must be a 2-64 character lowercase identifier")
                continue
            if level_id in ids:
                errors.append(f"{level_prefix}.id duplicates {level_id!r}")
            ids.append(level_id)
            try:
                encoded = canonical_json_bytes(level.get("value"))
            except (TypeError, ValueError) as exc:
                errors.append(f"{level_prefix}.value must be finite JSON: {exc}")
            else:
                if encoded in values:
                    errors.append(f"{prefix}.levels must not repeat the same value")
                values.append(encoded)
        level_ids.append(ids)
    return names, level_ids


def _validate_profiles(
    plan: dict[str, Any],
    dimension_names: list[str],
    dimension_levels: list[list[str]],
    errors: list[str],
) -> tuple[list[str], dict[str, int]]:
    profiles = plan.get("profiles")
    expected_cells = [dict(zip(dimension_names, cells)) for cells in product(*dimension_levels)]
    if not isinstance(profiles, list) or not 4 <= len(profiles) <= 16:
        errors.append("profiles must contain 4-16 full-factorial entries")
        return [], {}
    if len(expected_cells) != len(profiles):
        errors.append("profiles must equal the complete declared Cartesian product")
    profile_ids: list[str] = []
    memory: dict[str, int] = {}
    plan_digests: set[str] = set()
    fingerprints: set[str] = set()
    realizations: set[bytes] = set()
    actual_cells: list[dict[str, Any]] = []
    for index, profile in enumerate(profiles):
        prefix = f"profiles[{index}]"
        required = {"id", "cells", "plan_sha256", "realization", "estimated_memory_mb"}
        if not isinstance(profile, dict) or set(profile) != required:
            errors.append(f"{prefix} must contain exactly the supported profile fields")
            continue
        profile_id = profile.get("id")
        if not isinstance(profile_id, str) or not ID_PATTERN.fullmatch(profile_id):
            errors.append(f"{prefix}.id must be a 2-64 character lowercase identifier")
        elif profile_id in profile_ids:
            errors.append(f"{prefix}.id duplicates {profile_id!r}")
        else:
            profile_ids.append(profile_id)
        cells = profile.get("cells")
        if not isinstance(cells, dict) or set(cells) != set(dimension_names):
            errors.append(f"{prefix}.cells must contain exactly the declared dimensions")
        else:
            actual_cells.append(copy.deepcopy(cells))
            for dim_index, name in enumerate(dimension_names):
                if cells.get(name) not in dimension_levels[dim_index]:
                    errors.append(f"{prefix}.cells.{name} is not a declared level")
        digest = profile.get("plan_sha256")
        if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
            errors.append(f"{prefix}.plan_sha256 must be a lowercase SHA-256")
        elif digest in plan_digests:
            errors.append(f"{prefix}.plan_sha256 must identify a distinct Profile plan")
        else:
            plan_digests.add(digest)
        realization = profile.get("realization")
        realization_fields = {
            "subject_version",
            "subject_source_ref",
            "target_root",
            "static_root_fingerprint",
        }
        if not isinstance(realization, dict) or set(realization) != realization_fields:
            errors.append(f"{prefix}.realization must contain the fixed M8 implementation fields")
        else:
            if not _non_empty_string(realization.get("subject_version")):
                errors.append(f"{prefix}.realization.subject_version must be non-empty")
            for field in ("subject_source_ref", "target_root"):
                if not _safe_relative_directory(realization.get(field)):
                    errors.append(f"{prefix}.realization.{field} must be a safe relative path")
            fingerprint = realization.get("static_root_fingerprint")
            if not isinstance(fingerprint, str) or not SHA256_PATTERN.fullmatch(fingerprint):
                errors.append(f"{prefix}.realization.static_root_fingerprint must be a SHA-256")
            elif fingerprint in fingerprints:
                errors.append("each Profile must preregister a distinct static_root_fingerprint")
            else:
                fingerprints.add(fingerprint)
            try:
                realization_bytes = canonical_json_bytes(realization)
            except (TypeError, ValueError) as exc:
                errors.append(f"{prefix}.realization must contain finite JSON values: {exc}")
            else:
                if realization_bytes in realizations:
                    errors.append("Profile realization mappings must be distinct")
                realizations.add(realization_bytes)
        estimated = profile.get("estimated_memory_mb")
        if not _positive_int(estimated) or estimated > 8192:
            errors.append(f"{prefix}.estimated_memory_mb must be between 1 and 8192")
        elif isinstance(profile_id, str):
            memory[profile_id] = estimated
    if actual_cells != expected_cells:
        errors.append("profiles must follow canonical dimension/level Cartesian order")
    return profile_ids, memory


def _validate_schedule(
    plan: dict[str, Any], profile_ids: list[str], memory: dict[str, int], errors: list[str]
) -> None:
    policy = plan.get("execution_policy")
    required_policy = {
        "order_algorithm",
        "seed",
        "perturbation_repetitions",
        "max_parallel",
        "memory_budget_mb",
        "preflight_between_waves",
        "cleanup_between_waves",
    }
    if not isinstance(policy, dict) or set(policy) != required_policy:
        errors.append("execution_policy must contain exactly the supported M8 fields")
        return
    if policy.get("order_algorithm") != ORDER_ALGORITHM:
        errors.append(f"execution_policy.order_algorithm must be {ORDER_ALGORITHM}")
    seed = policy.get("seed")
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
        errors.append("execution_policy.seed must be a non-negative integer")
    repetitions = policy.get("perturbation_repetitions")
    if (
        not isinstance(repetitions, int)
        or isinstance(repetitions, bool)
        or not 1 <= repetitions <= 4
    ):
        errors.append("execution_policy.perturbation_repetitions must be between 1 and 4")
    max_parallel = policy.get("max_parallel")
    if (
        not isinstance(max_parallel, int)
        or isinstance(max_parallel, bool)
        or max_parallel not in {1, 2}
    ):
        errors.append("execution_policy.max_parallel must be 1 or 2")
    budget = policy.get("memory_budget_mb")
    if not _positive_int(budget) or budget > 16384:
        errors.append("execution_policy.memory_budget_mb must be between 1 and 16384")
    if policy.get("preflight_between_waves") is not True:
        errors.append("execution_policy.preflight_between_waves must be true")
    if policy.get("cleanup_between_waves") is not True:
        errors.append("execution_policy.cleanup_between_waves must be true")

    schedule = plan.get("schedule")
    expected_count = len(profile_ids) * (1 + repetitions) if isinstance(repetitions, int) else 0
    if not isinstance(schedule, list) or len(schedule) != expected_count:
        errors.append("schedule must contain every coverage and perturbation slot exactly once")
        return
    slot_ids: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, slot in enumerate(schedule):
        prefix = f"schedule[{index}]"
        fields = {"slot_id", "phase", "repetition", "wave", "position", "profile_id"}
        if not isinstance(slot, dict) or set(slot) != fields:
            errors.append(f"{prefix} must contain exactly the supported slot fields")
            continue
        valid_slot = True
        slot_id = slot.get("slot_id")
        if not isinstance(slot_id, str) or not ID_PATTERN.fullmatch(slot_id):
            errors.append(f"{prefix}.slot_id must be a 2-64 character lowercase identifier")
            valid_slot = False
        elif slot_id in slot_ids:
            errors.append(f"{prefix}.slot_id duplicates {slot_id!r}")
            valid_slot = False
        else:
            slot_ids.add(slot_id)
        if slot.get("phase") not in PHASES:
            errors.append(f"{prefix}.phase is unsupported")
            valid_slot = False
        for field in ("wave", "position"):
            if not _positive_int(slot.get(field)):
                errors.append(f"{prefix}.{field} must be a positive integer")
                valid_slot = False
        repetition = slot.get("repetition")
        if not isinstance(repetition, int) or isinstance(repetition, bool) or repetition < 0:
            errors.append(f"{prefix}.repetition must be a non-negative integer")
            valid_slot = False
        if slot.get("profile_id") not in profile_ids:
            errors.append(f"{prefix}.profile_id is not declared")
            valid_slot = False
        if valid_slot:
            normalized.append(slot)
    if len(normalized) != len(schedule):
        return

    coverage = [slot for slot in schedule if slot["phase"] == "COVERAGE"]
    if [slot["profile_id"] for slot in coverage] != profile_ids:
        errors.append("coverage must follow canonical Profile order exactly once")
    for index, slot in enumerate(coverage, start=1):
        if slot["repetition"] != 0 or slot["wave"] != index or slot["position"] != 1:
            errors.append("coverage must be serial with repetition 0 and contiguous waves")
            break

    perturbation = [slot for slot in schedule if slot["phase"] == "PERTURBATION"]
    if schedule != coverage + perturbation:
        errors.append("all coverage slots must precede every perturbation slot")
    if isinstance(repetitions, int) and isinstance(seed, int):
        expected_repetitions = list(range(1, repetitions + 1))
        actual_repetitions = []
        for slot in perturbation:
            if slot["repetition"] not in actual_repetitions:
                actual_repetitions.append(slot["repetition"])
        if actual_repetitions != expected_repetitions:
            errors.append("perturbation repetitions must be contiguous and ordered")
        for repetition in expected_repetitions:
            slots = [slot for slot in perturbation if slot["repetition"] == repetition]
            expected_order = seeded_profile_order(profile_ids, seed, repetition)
            if [slot["profile_id"] for slot in slots] != expected_order:
                errors.append(
                    f"perturbation repetition {repetition} violates SHA256_RANK_V1 order"
                )
            wave_numbers: list[int] = []
            for slot in slots:
                if slot["wave"] not in wave_numbers:
                    wave_numbers.append(slot["wave"])
            if wave_numbers != list(range(1, len(wave_numbers) + 1)):
                errors.append(f"perturbation repetition {repetition} waves must be contiguous")
            for wave in wave_numbers:
                members = [slot for slot in slots if slot["wave"] == wave]
                if [slot["position"] for slot in members] != list(range(1, len(members) + 1)):
                    errors.append(
                        f"perturbation repetition {repetition} wave {wave} positions "
                        "must be contiguous"
                    )
                if isinstance(max_parallel, int) and len(members) > max_parallel:
                    errors.append(
                        f"perturbation repetition {repetition} wave {wave} exceeds max_parallel"
                    )
                wave_memory = sum(memory.get(slot["profile_id"], 0) for slot in members)
                if isinstance(budget, int) and wave_memory > budget:
                    errors.append(
                        f"perturbation repetition {repetition} wave {wave} exceeds memory budget"
                    )


def validate_batch_plan(plan: dict[str, Any]) -> None:
    errors: list[str] = []
    allowed = {
        "schema_version",
        "batch_id",
        "version",
        "question",
        "primary_variable",
        "dimensions",
        "profiles",
        "execution_policy",
        "schedule",
        "outcomes",
        "limits",
        "reproduction_steps",
        "cleanup_steps",
        "seal",
    }
    unknown = sorted(set(plan) - allowed)
    if unknown:
        errors.append(f"batch plan has unsupported fields: {', '.join(unknown)}")
    if plan.get("schema_version") != BATCH_PLAN_SCHEMA_VERSION:
        errors.append("schema_version must be '0.1'")
    batch_id = plan.get("batch_id")
    if not isinstance(batch_id, str) or not ID_PATTERN.fullmatch(batch_id):
        errors.append("batch_id must be a 2-64 character lowercase identifier")
    if not _positive_int(plan.get("version")):
        errors.append("version must be a positive integer")
    if not _non_empty_string(plan.get("question")):
        errors.append("question must be a non-empty string")
    primary = plan.get("primary_variable")
    if (
        not isinstance(primary, dict)
        or not {"name", "source"}.issubset(primary)
        or set(primary) - {"name", "source", "unit"}
    ):
        errors.append("primary_variable must contain name, source, and optional unit")
    else:
        for field in ("name", "source"):
            if not _non_empty_string(primary.get(field)):
                errors.append(f"primary_variable.{field} must be a non-empty string")
        if "unit" in primary and not _non_empty_string(primary.get("unit")):
            errors.append("primary_variable.unit must be non-empty when present")

    names, levels = _validate_dimensions(plan, errors)
    profile_ids, memory = _validate_profiles(plan, names, levels, errors)
    _validate_schedule(plan, profile_ids, memory, errors)

    outcomes = plan.get("outcomes")
    outcome_ids: set[str] = set()
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
                errors.append(f"{prefix}.assertion_id must be non-empty")
            elif assertion_id in outcome_ids:
                errors.append(f"{prefix}.assertion_id duplicates {assertion_id!r}")
            else:
                outcome_ids.add(assertion_id)
            expected = outcome.get("expected_actual")
            if not isinstance(expected, dict) or set(expected) != set(profile_ids):
                errors.append(f"{prefix}.expected_actual must contain exactly every Profile ID")

    _string_list(plan.get("limits"), "limits", errors)
    _string_list(plan.get("reproduction_steps"), "reproduction_steps", errors)
    _string_list(plan.get("cleanup_steps"), "cleanup_steps", errors)
    unsealed = {key: value for key, value in plan.items() if key != "seal"}
    try:
        canonical_json_bytes(unsealed)
    except (TypeError, ValueError) as exc:
        errors.append(f"batch plan must contain finite JSON values: {exc}")
    _, sensitive_count = redact_value(unsealed)
    if sensitive_count:
        errors.append(
            f"batch plan contains {sensitive_count} sensitive value(s) or personal path(s)"
        )
    if errors:
        raise BatchError("BATCH_PLAN_INVALID", "; ".join(errors))


def batch_plan_digest(plan: dict[str, Any]) -> str:
    return sha256_json({key: value for key, value in plan.items() if key != "seal"})


def seal_batch_plan(plan: dict[str, Any]) -> dict[str, Any]:
    validate_batch_plan(plan)
    sealed = copy.deepcopy(plan)
    sealed["seal"] = {"algorithm": "sha256", "digest": batch_plan_digest(sealed)}
    return sealed


def verify_sealed_batch_plan(plan: dict[str, Any]) -> None:
    validate_batch_plan(plan)
    seal = plan.get("seal")
    if not isinstance(seal, dict) or set(seal) != {"algorithm", "digest"}:
        raise BatchError("BATCH_PLAN_UNSEALED", "BatchPlan 没有有效 seal。")
    if seal.get("algorithm") != "sha256" or seal.get("digest") != batch_plan_digest(plan):
        raise BatchError("BATCH_PLAN_SEAL_MISMATCH", "BatchPlan seal 与规范内容不一致。")


def _load_document(path: Path, label: str, unreadable_code: str) -> dict[str, Any]:
    try:
        if path.stat().st_size > MAX_DOCUMENT_BYTES:
            raise BatchError(unreadable_code, f"{label} 超过 1 MiB 上限。")
        return load_json_object(path, label=label)
    except BatchError:
        raise
    except Exception as exc:
        raise BatchError(unreadable_code, f"{label} 无法安全读取。") from exc


def load_and_seal_batch_plan(path: Path) -> dict[str, Any]:
    plan = _load_document(path, "BatchPlan", "BATCH_PLAN_UNREADABLE")
    if "seal" in plan:
        verify_sealed_batch_plan(plan)
        return plan
    return seal_batch_plan(plan)


def load_sealed_batch_plan(path: Path) -> dict[str, Any]:
    plan = _load_document(path, "BatchPlan", "BATCH_PLAN_UNREADABLE")
    if "seal" not in plan:
        raise BatchError("BATCH_PLAN_UNSEALED", "analyze-batch 只接受已封存 BatchPlan。")
    verify_sealed_batch_plan(plan)
    return plan


def write_sealed_batch_plan(path: Path, plan: dict[str, Any]) -> None:
    if path.exists():
        raise BatchError("BATCH_PLAN_OUTPUT_EXISTS", "拒绝覆盖已有 BatchPlan 输出。")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(canonical_json_bytes(plan) + b"\n")
    except FileExistsError as exc:
        raise BatchError("BATCH_PLAN_OUTPUT_EXISTS", "拒绝覆盖已有 BatchPlan 输出。") from exc
    except Exception:
        if path.exists():
            path.unlink()
        raise


def _load_assignment(path: Path, batch_plan: dict[str, Any]) -> dict[str, str]:
    assignment = _load_document(path, "RunAssignment", "RUN_ASSIGNMENT_UNREADABLE")
    if set(assignment) != {"schema_version", "batch_plan_sha256", "assignments"}:
        raise BatchError("RUN_ASSIGNMENT_INVALID", "RunAssignment 字段集合无效。")
    if assignment.get("schema_version") != RUN_ASSIGNMENT_SCHEMA_VERSION:
        raise BatchError("RUN_ASSIGNMENT_INVALID", "RunAssignment 版本不受支持。")
    if assignment.get("batch_plan_sha256") != batch_plan["seal"]["digest"]:
        raise BatchError("RUN_ASSIGNMENT_PLAN_MISMATCH", "RunAssignment 未绑定当前 BatchPlan。")
    raw_assignments = assignment.get("assignments")
    if not isinstance(raw_assignments, list) or len(raw_assignments) > len(batch_plan["schedule"]):
        raise BatchError("RUN_ASSIGNMENT_INVALID", "RunAssignment 条目数量无效。")
    valid_slots = {slot["slot_id"] for slot in batch_plan["schedule"]}
    result: dict[str, str] = {}
    bundles: set[str] = set()
    for raw in raw_assignments:
        if not isinstance(raw, dict) or set(raw) != {"slot_id", "bundle"}:
            raise BatchError("RUN_ASSIGNMENT_INVALID", "RunAssignment 条目字段无效。")
        slot_id = raw.get("slot_id")
        bundle = raw.get("bundle")
        if slot_id not in valid_slots or slot_id in result:
            raise BatchError("RUN_ASSIGNMENT_INVALID", "RunAssignment slot 未知或重复。")
        if not _safe_relative_directory(bundle):
            raise BatchError("RUN_ASSIGNMENT_UNSAFE_PATH", "RunAssignment 包含不安全相对目录。")
        if bundle in bundles:
            raise BatchError("RUN_ASSIGNMENT_DUPLICATE_TARGET", "RunAssignment 不得重复引用同一目录。")
        result[slot_id] = bundle
        bundles.add(bundle)
    return result


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def _resolve_bundle(root: Path, relative: str) -> Path:
    candidate = root
    try:
        for part in relative.split("/"):
            candidate = candidate / part
            metadata = os.lstat(candidate)
            if candidate.is_symlink() or _is_reparse(metadata):
                raise BatchError("RUN_ASSIGNMENT_UNSAFE_NODE", "RunAssignment 路径包含链接节点。")
        if not stat.S_ISDIR(os.lstat(candidate).st_mode):
            raise BatchError("SOURCE_BUNDLE_UNREADABLE", "来源 Run Bundle 不可用。")
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
        return candidate
    except BatchError:
        raise
    except (OSError, ValueError) as exc:
        raise BatchError("SOURCE_BUNDLE_UNREADABLE", "来源 Run Bundle 不可用。") from exc


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
        raise BatchError("SOURCE_PLAN_REFERENCE_MISMATCH", "来源 Run 报告与 sealed ExperimentPlan 不一致。")
    if report.get("plan") != {
        "id": plan["plan_id"],
        "version": plan["version"],
        "sha256": plan["seal"]["digest"],
    }:
        raise BatchError("SOURCE_PLAN_REFERENCE_MISMATCH", "来源 Run 的 ExperimentPlan 引用不一致。")
    planned = {item["id"]: item for item in plan["assertions"]}
    observed = {item["id"]: item for item in report["assertions"]}
    if set(planned) != set(observed):
        raise BatchError("SOURCE_PLAN_REFERENCE_MISMATCH", "来源 Run 的断言集合与 Plan 不一致。")
    for assertion_id, definition in planned.items():
        for field in ("severity", "evidence_type", "path", "operator", "expected"):
            if not _same(observed[assertion_id].get(field), definition[field]):
                raise BatchError("SOURCE_PLAN_REFERENCE_MISMATCH", "来源 Run 的断言定义与 Plan 不一致。")


def _control_projection(plan: dict[str, Any], primary_name: str) -> dict[str, Any]:
    projection = copy.deepcopy({key: value for key, value in plan.items() if key != "seal"})
    projection["version"] = "<BATCH_VERSION>"
    if isinstance(projection.get("subject"), dict):
        projection["subject"]["version"] = "<BATCH_SUBJECT_VERSION>"
        projection["subject"]["source_ref"] = "<BATCH_SUBJECT_SOURCE_REF>"
    if isinstance(projection.get("target"), dict):
        projection["target"]["root"] = "<BATCH_TARGET_ROOT>"
    if isinstance(projection.get("baseline"), dict):
        projection["baseline"]["fingerprint"] = "<BATCH_STATIC_ROOT_FINGERPRINT>"
    matches = [
        item
        for item in projection["variables"]
        if item.get("role") == "PRIMARY" and item.get("name") == primary_name
    ]
    if len(matches) == 1:
        matches[0]["value"] = "<BATCH_PROFILE_ID>"
    return projection


def _load_source(candidate: Path, runs_root: Path, primary_name: str) -> _SourceRun:
    try:
        validated = validate_bundle(candidate, runs_root)
    except (_CandidateRejected, OSError, ValueError) as exc:
        code = exc.code if isinstance(exc, _CandidateRejected) else "SOURCE_BUNDLE_UNREADABLE"
        raise BatchError(code, "来源 Run Bundle 未通过完整性校验。") from exc
    file_paths = {item.path for item in validated.files}
    if "sealed-plan.json" not in file_paths:
        raise BatchError("SOURCE_SEALED_PLAN_MISSING", "来源 Run Bundle 没有 sealed-plan.json。")
    try:
        plan = load_json_object(candidate / "sealed-plan.json", label="Sealed ExperimentPlan")
        report = load_json_object(candidate / "report.json", label="Report")
        if plan.get("schema_version") == "0.6":
            raise BatchError(
                "SOURCE_PLAN_VERSION_UNSUPPORTED",
                "M8 Batch 尚无 Plan 0.6 / ProjectProfile 兼容合同。",
            )
        verify_sealed_plan(plan)
    except BatchError:
        raise
    except Exception as exc:
        raise BatchError(
            "SOURCE_SEALED_PLAN_INVALID", "来源 Run 的 sealed ExperimentPlan 无效。"
        ) from exc
    _validate_report_plan_cross_reference(report, plan)
    evidence: dict[str, dict[str, Any]] = {}
    for entry in report["evidence"]:
        evidence_type = entry["evidence_type"]
        if evidence_type in evidence:
            continue
        evidence[evidence_type] = load_json_object(
            candidate / Path(*entry["path"].split("/")), label="Evidence"
        )
    return _SourceRun(
        report=report,
        plan=plan,
        bundle_sha256=validated.bundle_sha256,
        control_projection_sha256=sha256_json(_control_projection(plan, primary_name)),
        evidence=evidence,
    )


def _source_reference(source: _SourceRun) -> dict[str, Any]:
    primary = next(item for item in source.plan["variables"] if item["role"] == "PRIMARY")
    preflight = source.evidence.get("runtime.preflight", {}).get("facts", {})
    orchestration = source.evidence.get("runtime.orchestration", {}).get("facts", {})
    browser = source.evidence.get("browser.session", {}).get("facts", {})
    return {
        "run_id": source.report["run_id"],
        "created_at": source.report["created_at"],
        "execution_status": source.report["execution_status"],
        "verdict": source.report["verdict"],
        "plan": copy.deepcopy(source.report["plan"]),
        "random_seed": source.report["random_seed"],
        "primary_variable": copy.deepcopy(primary),
        "bundle_sha256": source.bundle_sha256,
        "control_projection_sha256": source.control_projection_sha256,
        "preflight_complete": preflight.get("snapshot_complete") is True
        and preflight.get("decision") == "PROCEED",
        "cleanup_complete": orchestration.get("cleanup_complete") is True,
        "browser_complete": browser.get("capture_complete") is True,
        "static_root_fingerprint": orchestration.get("static_root_fingerprint"),
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


def _reason(reasons: list[dict[str, str]], code: str, message: str) -> None:
    if code not in {item["code"] for item in reasons}:
        reasons.append({"code": code, "message": message})


def _created_at(source: _SourceRun) -> datetime | None:
    try:
        value = datetime.fromisoformat(source.report["created_at"].replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return value if value.tzinfo is not None else None


def _wave_key(slot: dict[str, Any]) -> tuple[int, int, int]:
    return (0 if slot["phase"] == "COVERAGE" else 1, slot["repetition"], slot["wave"])


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
        "# VeriTrail Full-factorial Batch Analysis",
        "",
        f"- Analysis: `{analysis['analysis_id']}`",
        f"- Batch plan: `{analysis['batch_plan']['id']}` / `{analysis['batch_plan']['sha256']}`",
        f"- Coverage: **{analysis['coverage_status']}**",
        f"- Hypothesis: **{analysis['hypothesis_status']}**",
        f"- Rule: `{analysis['rule_version']}`",
        "- Wave membership is a sealed schedule envelope; it does not prove real runtime overlap.",
        "",
        "## Reasons",
        "",
    ]
    lines.extend(f"- `{item['code']}` — {item['message']}" for item in analysis["reasons"])
    lines.extend(
        [
            "",
            "## Slots",
            "",
            "| Slot | Phase | Rep | Wave | Profile | Run | Execution | Verdict |",
            "| --- | --- | ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    for slot in analysis["slots"]:
        source = slot["source"]
        lines.append(
            f"| {slot['slot_id']} | {slot['phase']} | {slot['repetition']} | {slot['wave']} | "
            f"{slot['profile_id']} | {source['run_id'] if source else 'MISSING'} | "
            f"{source['execution_status'] if source else 'MISSING'} | "
            f"{source['verdict'] if source else 'MISSING'} |"
        )
    lines.extend(["", "## Profile outcomes", ""])
    for profile in analysis["profiles"]:
        lines.append(
            f"- `{profile['id']}` — occurrences `{profile['occurrence_count']}`, "
            f"completed `{profile['completed_count']}`, mismatches `{profile['mismatch_count']}`"
        )
    lines.extend(["", "## Unplanned assertion drift", ""])
    if analysis["unplanned_differences"]:
        for item in analysis["unplanned_differences"]:
            lines.append(f"- `{item['slot_id']}` / `{item['assertion_id']}`")
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


def create_batch_analysis_bundle(
    *, batch_plan_path: Path, assignment_path: Path, runs_root: Path, output: Path
) -> BatchBuildResult:
    if output.exists():
        raise BatchError("BATCH_OUTPUT_EXISTS", "拒绝覆盖已有 BatchAnalysis 输出目录。")
    batch_plan = load_sealed_batch_plan(batch_plan_path)
    assignments = _load_assignment(assignment_path, batch_plan)
    try:
        runs_root = runs_root.resolve(strict=True)
    except OSError as exc:
        raise BatchError("RUNS_ROOT_UNREADABLE", "显式 runs-root 不可用。") from exc
    primary_definition = batch_plan["primary_variable"]
    profiles = {profile["id"]: profile for profile in batch_plan["profiles"]}
    sources: dict[str, _SourceRun] = {}
    for slot in batch_plan["schedule"]:
        relative = assignments.get(slot["slot_id"])
        if relative is not None:
            candidate = _resolve_bundle(runs_root, relative)
            sources[slot["slot_id"]] = _load_source(
                candidate, runs_root, primary_definition["name"]
            )

    reasons: list[dict[str, str]] = []
    incomplete = False
    contaminated = False
    missing_slots = [
        slot["slot_id"]
        for slot in batch_plan["schedule"]
        if slot["slot_id"] not in sources
    ]
    if missing_slots:
        incomplete = True
        _reason(reasons, "SLOT_MISSING", "一个或多个预注册 slot 没有来源 Run。")

    source_values = list(sources.values())
    run_ids = [source.report["run_id"] for source in source_values]
    if len(run_ids) != len(set(run_ids)):
        contaminated = True
        _reason(reasons, "RUN_ID_REUSED", "不同 slot 复用了同一 Run ID。")
    bundle_digests = [source.bundle_sha256 for source in source_values]
    if len(bundle_digests) != len(set(bundle_digests)):
        contaminated = True
        _reason(reasons, "BUNDLE_REUSED", "不同 slot 复用了同一 Run Bundle。")

    control_digests = {source.control_projection_sha256 for source in source_values}
    if len(control_digests) > 1:
        contaminated = True
        _reason(reasons, "CONTROL_PROJECTION_MISMATCH", "ExperimentPlan 在固定实现映射之外发生漂移。")
    random_seeds = {source.report["random_seed"] for source in source_values}
    if len(random_seeds) > 1:
        contaminated = True
        _reason(reasons, "SOURCE_RANDOM_SEED_MISMATCH", "来源 ExperimentPlan 的随机种子不一致。")

    required_evidence = {"runtime.preflight", "runtime.orchestration", "browser.session"}
    for slot in batch_plan["schedule"]:
        source = sources.get(slot["slot_id"])
        if source is None:
            continue
        profile = profiles[slot["profile_id"]]
        if source.report["execution_status"] != "COMPLETED":
            incomplete = True
            _reason(reasons, "RUN_NOT_COMPLETED", "一个或多个来源 Run 未达到 COMPLETED。")
        if not required_evidence.issubset(source.evidence):
            incomplete = True
            _reason(reasons, "SOURCE_EVIDENCE_INCOMPLETE", "一个或多个来源 Run 缺少 M5 必需证据。")
        if (
            source.plan.get("schema_version") != "0.4"
            or source.plan.get("experiment_type") != "SINGLE_VARIABLE"
            or source.plan.get("target", {}).get("adapter") != "STATIC_HTTP"
        ):
            contaminated = True
            _reason(
                reasons,
                "SOURCE_PLAN_KIND_MISMATCH",
                "来源必须是 Plan 0.4 SINGLE_VARIABLE + STATIC_HTTP。",
            )
        if source.report["plan"]["sha256"] != profile["plan_sha256"]:
            contaminated = True
            _reason(reasons, "PROFILE_PLAN_DIGEST_MISMATCH", "来源 Plan digest 与 Profile 预注册值不一致。")
        primary = next(item for item in source.plan["variables"] if item["role"] == "PRIMARY")
        if (
            primary.get("name") != primary_definition["name"]
            or primary.get("source") != primary_definition["source"]
            or primary.get("unit") != primary_definition.get("unit")
            or primary.get("value") != slot["profile_id"]
        ):
            contaminated = True
            _reason(reasons, "PRIMARY_VARIABLE_MISMATCH", "来源主要变量与 slot Profile 不一致。")
        realization = profile["realization"]
        if (
            source.plan.get("subject", {}).get("version") != realization["subject_version"]
            or source.plan.get("subject", {}).get("source_ref")
            != realization["subject_source_ref"]
            or source.plan.get("target", {}).get("root") != realization["target_root"]
            or source.plan.get("baseline", {}).get("fingerprint")
            != realization["static_root_fingerprint"]
        ):
            contaminated = True
            _reason(reasons, "PROFILE_REALIZATION_MISMATCH", "来源 Plan 未实现 Profile 的固定映射。")
        source_ref = _source_reference(source)
        if source_ref["static_root_fingerprint"] != realization["static_root_fingerprint"]:
            contaminated = True
            _reason(
                reasons,
                "STATIC_ROOT_FINGERPRINT_MISMATCH",
                "实际静态目标 fingerprint 与 Profile 不一致。",
            )
        if required_evidence.issubset(source.evidence):
            if not source_ref["preflight_complete"]:
                contaminated = True
                _reason(reasons, "PREFLIGHT_BOUNDARY_FAILED", "来源 Run 未通过独立 preflight 边界。")
            if not source_ref["cleanup_complete"]:
                contaminated = True
                _reason(reasons, "CLEANUP_BOUNDARY_FAILED", "来源 Run 未完成 cleanup 边界。")
            if not source_ref["browser_complete"]:
                contaminated = True
                _reason(reasons, "BROWSER_BOUNDARY_FAILED", "来源 Run 未完成浏览器证据边界。")

    waves: list[tuple[tuple[int, int, int], list[dict[str, Any]]]] = []
    for slot in batch_plan["schedule"]:
        key = _wave_key(slot)
        if not waves or waves[-1][0] != key:
            waves.append((key, []))
        waves[-1][1].append(slot)
    for (_, earlier), (_, later) in zip(waves, waves[1:]):
        earlier_times = [
            value
            for slot in earlier
            if slot["slot_id"] in sources
            for value in [_created_at(sources[slot["slot_id"]])]
            if value is not None
        ]
        later_times = [
            value
            for slot in later
            if slot["slot_id"] in sources
            for value in [_created_at(sources[slot["slot_id"]])]
            if value is not None
        ]
        if earlier_times and later_times and max(earlier_times) >= min(later_times):
            contaminated = True
            _reason(reasons, "WAVE_ORDER_MISMATCH", "来源 Run 时间不符合预注册 phase/wave 顺序。")
            break
    if any(_created_at(source) is None for source in source_values):
        contaminated = True
        _reason(reasons, "SOURCE_TIME_INVALID", "来源 Run 缺少带时区的可比较时间事实。")

    report_assertions = {
        slot_id: {item["id"]: item for item in source.report["assertions"]}
        for slot_id, source in sources.items()
    }
    outcome_ids = {item["assertion_id"] for item in batch_plan["outcomes"]}
    if any(
        outcome_id not in report_assertions[slot_id]
        for slot_id in report_assertions
        for outcome_id in outcome_ids
    ):
        contaminated = True
        _reason(reasons, "OUTCOME_MISSING", "预注册 outcome 在来源 Report 中缺失。")

    unplanned_differences: list[dict[str, Any]] = []
    if sources:
        first_slot_id = next(
            slot["slot_id"]
            for slot in batch_plan["schedule"]
            if slot["slot_id"] in sources
        )
        baseline_assertions = report_assertions[first_slot_id]
        for slot in batch_plan["schedule"]:
            slot_id = slot["slot_id"]
            if slot_id not in sources or slot_id == first_slot_id:
                continue
            for assertion_id in sorted(set(baseline_assertions) - outcome_ids):
                baseline_projection = _assertion_projection(baseline_assertions[assertion_id])
                candidate = report_assertions[slot_id].get(assertion_id)
                observed = _assertion_projection(candidate) if candidate else None
                if not _same(baseline_projection, observed):
                    unplanned_differences.append(
                        {
                            "slot_id": slot_id,
                            "assertion_id": assertion_id,
                            "baseline": baseline_projection,
                            "observed": observed,
                        }
                    )
        if unplanned_differences:
            contaminated = True
            _reason(reasons, "UNDECLARED_OUTCOME_DRIFT", "非 outcome 断言出现未预注册漂移。")

    slot_models: list[dict[str, Any]] = []
    mismatch_count = 0
    observations_by_profile: dict[tuple[str, str], list[Any]] = {}
    for slot in batch_plan["schedule"]:
        source = sources.get(slot["slot_id"])
        slot_outcomes: list[dict[str, Any]] = []
        for outcome in batch_plan["outcomes"]:
            assertion_id = outcome["assertion_id"]
            expected_actual = copy.deepcopy(outcome["expected_actual"][slot["profile_id"]])
            assertion = report_assertions.get(slot["slot_id"], {}).get(assertion_id)
            actual = copy.deepcopy(assertion.get("actual")) if assertion else None
            matches = assertion is not None and _same(actual, expected_actual)
            if source is not None:
                observations_by_profile.setdefault(
                    (slot["profile_id"], assertion_id), []
                ).append(actual)
            if not matches:
                mismatch_count += 1
            slot_outcomes.append(
                {
                    "assertion_id": assertion_id,
                    "expected_actual": expected_actual,
                    "actual": actual,
                    "matches": matches,
                }
            )
        slot_models.append(
            {
                "slot_id": slot["slot_id"],
                "phase": slot["phase"],
                "repetition": slot["repetition"],
                "wave": slot["wave"],
                "position": slot["position"],
                "profile_id": slot["profile_id"],
                "source": _source_reference(source) if source else None,
                "outcomes": slot_outcomes,
            }
        )
    for values in observations_by_profile.values():
        if len(values) > 1 and any(not _same(values[0], value) for value in values[1:]):
            contaminated = True
            _reason(
                reasons,
                "PERTURBATION_OUTCOME_DRIFT",
                "同一 Profile 在 coverage 与扰动阶段出现不稳定 outcome。",
            )
            break

    if contaminated:
        coverage_status = "INCONCLUSIVE"
        hypothesis_status = "INCONCLUSIVE"
    elif incomplete:
        coverage_status = "INCOMPLETE"
        hypothesis_status = "INCONCLUSIVE"
    elif mismatch_count:
        coverage_status = "COMPLETE"
        hypothesis_status = "CONTRADICTED"
        _reason(reasons, "BATCH_HYPOTHESIS_CONTRADICTED", "完整且稳定的来源事实反驳至少一个预注册 outcome。")
    else:
        coverage_status = "COMPLETE"
        hypothesis_status = "SUPPORTED"
        _reason(
            reasons,
            "BATCH_HYPOTHESIS_SUPPORTED",
            "全因子覆盖完整，全部预注册 Profile outcome 在确定性与扰动阶段一致命中。",
        )

    ordered_digests = [
        sources[slot["slot_id"]].bundle_sha256
        if slot["slot_id"] in sources
        else "MISSING"
        for slot in batch_plan["schedule"]
    ]
    analysis_id = "batch_" + sha256_json(
        {
            "schema_version": BATCH_ANALYSIS_SCHEMA_VERSION,
            "rule_version": BATCH_RULE_VERSION,
            "batch_plan_sha256": batch_plan["seal"]["digest"],
            "ordered_bundle_sha256": ordered_digests,
        }
    )[:24]
    profile_models = []
    for profile in batch_plan["profiles"]:
        profile_slots = [slot for slot in slot_models if slot["profile_id"] == profile["id"]]
        profile_models.append(
            {
                "id": profile["id"],
                "cells": copy.deepcopy(profile["cells"]),
                "occurrence_count": len(profile_slots),
                "completed_count": sum(
                    1
                    for slot in profile_slots
                    if slot["source"] is not None
                    and slot["source"]["execution_status"] == "COMPLETED"
                ),
                "mismatch_count": sum(
                    1
                    for slot in profile_slots
                    for outcome in slot["outcomes"]
                    if not outcome["matches"]
                ),
            }
        )
    analysis = {
        "schema_version": BATCH_ANALYSIS_SCHEMA_VERSION,
        "analysis_id": analysis_id,
        "analysis_type": "PREREGISTERED_FULL_FACTORIAL_BATCH",
        "rule_version": BATCH_RULE_VERSION,
        "coverage_status": coverage_status,
        "hypothesis_status": hypothesis_status,
        "runtime_overlap_claim": "NOT_PROVEN",
        "batch_plan": {
            "id": batch_plan["batch_id"],
            "version": batch_plan["version"],
            "sha256": batch_plan["seal"]["digest"],
        },
        "primary_variable": copy.deepcopy(primary_definition),
        "execution_policy": copy.deepcopy(batch_plan["execution_policy"]),
        "reasons": reasons,
        "slots": slot_models,
        "profiles": profile_models,
        "unplanned_differences": unplanned_differences,
        "limits": copy.deepcopy(batch_plan["limits"]),
    }

    output = output.absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-batch-", dir=output.parent))
    try:
        (stage / "sealed-batch-plan.json").write_bytes(canonical_json_bytes(batch_plan) + b"\n")
        (stage / "batch-analysis.json").write_bytes(canonical_json_bytes(analysis) + b"\n")
        (stage / "batch-analysis.md").write_text(
            _render_markdown(analysis), encoding="utf-8", newline="\n"
        )
        files = [
            _file_entry(stage / "sealed-batch-plan.json", "sealed-batch-plan.json"),
            _file_entry(stage / "batch-analysis.json", "batch-analysis.json"),
            _file_entry(stage / "batch-analysis.md", "batch-analysis.md"),
        ]
        manifest = {
            "schema_version": BATCH_ANALYSIS_SCHEMA_VERSION,
            "analysis_id": analysis_id,
            "files": files,
        }
        (stage / "batch-analysis-manifest.json").write_bytes(
            canonical_json_bytes(manifest) + b"\n"
        )
        publish_staged_directory(stage, output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return BatchBuildResult(
        analysis_id=analysis_id,
        coverage_status=coverage_status,
        hypothesis_status=hypothesis_status,
        slot_count=len(batch_plan["schedule"]),
        source_count=len(sources),
    )
