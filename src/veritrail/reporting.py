from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from veritrail.atomic_publish import publish_staged_directory
from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.errors import SafetyError, ValidationError
from veritrail.evidence import (
    ImportedEvidence,
    import_evidence_files,
    validate_evidence_collection_budget,
    verify_imported_evidence,
)
from veritrail.markdown import markdown_code, markdown_json, markdown_text
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.resource_limits import MAX_BUNDLE_BYTES, MAX_BUNDLE_FILES
from veritrail.verdict import evaluate

RUN_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")


def _write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_json_bytes(value) + b"\n")


def _hash_file(path: Path, relative_path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return {
        "path": relative_path.as_posix(),
        "sha256": digest.hexdigest(),
        "size": size,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# VeriTrail run {markdown_code(report['run_id'])}",
        "",
        f"- Execution status: {markdown_code(report['execution_status'])}",
        f"- Verdict: {markdown_code(report['verdict'])}",
        f"- Plan: {markdown_code(str(report['plan']['id']) + '@' + str(report['plan']['version']))}",
        f"- Plan SHA-256: {markdown_code(report['plan']['sha256'])}",
        f"- Baseline: {markdown_code(report['baseline']['id'])} "
        f"({markdown_code(report['baseline']['status'])})",
        f"- Random seed: {markdown_code(report['random_seed'])}",
        f"- Created at: {markdown_code(report['created_at'])}",
        "",
        "## Reasons",
        "",
    ]
    for reason in report["reasons"]:
        lines.append(
            f"- {markdown_code(reason['code'])} — {markdown_text(reason['message'])}"
        )
    lines.extend(["", "## Assertions", "", "| ID | Severity | Status | Actual | Expected |", "| --- | --- | --- | --- | --- |"])
    for assertion in report["assertions"]:
        lines.append(
            "| {id} | {severity} | {status} | {actual} | {expected} |".format(
                id=markdown_text(assertion["id"]),
                severity=markdown_text(assertion["severity"]),
                status=markdown_text(assertion["status"]),
                actual=markdown_json(assertion["actual"]),
                expected=markdown_json(assertion["expected"]),
            )
        )
    lines.extend(["", "## Evidence", ""])
    if report["evidence"]:
        for artifact in report["evidence"]:
            summary = artifact.get("summary", {})
            decision = (
                f", decision: {summary['resource_decision']}"
                if summary.get("resource_decision")
                else ""
            )
            attachment_note = (
                f", attachments: {len(artifact['attachments'])}"
                if artifact.get("attachments")
                else ""
            )
            lines.append(
                f"- {markdown_code(artifact['evidence_type'])} — {markdown_code(artifact['sha256'])} "
                f"({artifact['size']} bytes, redactions: {artifact['redacted_fields']}"
                f"{attachment_note}{decision})"
            )
    else:
        lines.append("- No evidence was imported.")
    lines.extend(["", "## Evidence gaps and contamination", ""])
    if report["missing_evidence"]:
        lines.append(f"- Missing evidence: {markdown_json(report['missing_evidence'])}")
    if report["contamination"]:
        for item in report["contamination"]:
            lines.append(
                f"- {markdown_code(item['code'])} — {markdown_text(item['message'])}"
            )
    if not report["missing_evidence"] and not report["contamination"]:
        lines.append("- None detected by the active deterministic rule set.")
    lines.extend(
        [
            "",
            "## Applicability boundary",
            "",
            f"- Subject: {markdown_code(report['subject'], json_value=True)}",
            f"- Primary variable: {markdown_code(report['primary_variable'], json_value=True)}",
            f"- Load model: {markdown_code(report['load_model'], json_value=True)}",
            f"- Resource budget: {markdown_code(report['resource_budget'], json_value=True)}",
            f"- Change scope: {markdown_code(report['change_scope'], json_value=True)}",
            "",
            "## Reproduction and cleanup",
            "",
        ]
    )
    for index, step in enumerate(report["reproduction_steps"], start=1):
        lines.append(f"{index}. {markdown_text(step)}")
    lines.extend(["", "Cleanup:", ""])
    for index, step in enumerate(report["cleanup_steps"], start=1):
        lines.append(f"{index}. {markdown_text(step)}")
    lines.append("")
    return "\n".join(lines)


def _artifact_manifest(
    stage: Path, evidence: list[ImportedEvidence], duplicates: list[str], run_id: str
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    evidence_dir = stage / "evidence"
    evidence_dir.mkdir()
    entries: list[dict[str, Any]] = []
    for index, artifact in enumerate(evidence, start=1):
        evidence_type = artifact.document["evidence_type"]
        filename = f"{index:03d}-{evidence_type}-{artifact.sha256[:12]}.json"
        relative_path = Path("evidence") / filename
        (stage / relative_path).write_bytes(canonical_json_bytes(artifact.document))
        attachment_entries: list[dict[str, Any]] = []
        for attachment in artifact.attachments:
            attachment_path = Path(*attachment.path.split("/"))
            target = stage / attachment_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(attachment.content)
            attachment_entries.append(
                {
                    "path": attachment.path,
                    "sha256": attachment.sha256,
                    "size": attachment.size,
                    "media_type": attachment.media_type,
                    "logical_name": attachment.logical_name,
                }
            )
        entry = {
            "evidence_type": evidence_type,
            "path": relative_path.as_posix(),
            "sha256": artifact.sha256,
            "size": artifact.size,
            "redacted_fields": artifact.redacted_fields,
            "redacted": artifact.redacted_fields > 0,
            "redaction_rule_version": "privacy/0.1",
            "parser_version": "evidence-json/0.1",
            "captured_at": artifact.document["captured_at"],
            "source": artifact.document["source"],
            "retention": "local-default",
            "source_name": artifact.input_name,
            "attachments": attachment_entries,
        }
        if evidence_type == "runtime.preflight":
            entry["summary"] = {
                "resource_decision": artifact.document["facts"].get("decision"),
                "snapshot_complete": artifact.document["facts"].get("snapshot_complete"),
            }
        entries.append(entry)
    manifest = {
        "schema_version": "0.1",
        "run_id": run_id,
        "artifacts": entries,
        "duplicate_inputs_ignored": sorted(duplicates),
    }
    _write_json(stage / "evidence-manifest.json", manifest)
    return manifest, entries


def create_bundle(
    *,
    plan: dict[str, Any],
    evidence_paths: list[Path],
    output: Path,
    run_id: str,
    execution_status: str,
    generated_evidence: list[ImportedEvidence] | None = None,
    project_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_version = plan.get("schema_version")
    if plan_version in {"0.6", "0.7"}:
        if project_profile is None:
            raise ValidationError(
                [f"ExperimentPlan {plan_version} Bundle requires a sealed ProjectProfile"]
            )
        verify_sealed_project_profile(project_profile)
        verify_sealed_plan(plan, project_profile)
    else:
        if project_profile is not None:
            raise ValidationError(
                ["sealed ProjectProfile is accepted only for ExperimentPlan 0.6 or 0.7"]
            )
        verify_sealed_plan(plan)
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValidationError(["run_id must be a 2-64 character lowercase identifier"])
    if output.exists():
        raise SafetyError(f"refusing to overwrite existing output directory: {output.name}")
    output.parent.mkdir(parents=True, exist_ok=True)
    max_bytes = plan["resource_budget"]["max_artifact_bytes"]
    imported, duplicates = import_evidence_files(evidence_paths, max_bytes)
    seen_hashes = {artifact.sha256 for artifact in imported}
    for artifact in generated_evidence or []:
        verify_imported_evidence(artifact)
        if artifact.size > max_bytes:
            raise ValidationError(
                [f"generated evidence {artifact.input_name} is {artifact.size} bytes; limit is {max_bytes} bytes"]
            )
        if artifact.sha256 in seen_hashes:
            duplicates.append(artifact.input_name)
            continue
        for attachment in artifact.attachments:
            if attachment.size > max_bytes:
                raise ValidationError(
                    [
                        f"generated attachment {attachment.logical_name} is {attachment.size} bytes; "
                        f"limit is {max_bytes} bytes"
                    ]
                )
        seen_hashes.add(artifact.sha256)
        imported.append(artifact)
    if project_profile is not None:
        preflight = [
            artifact
            for artifact in imported
            if artifact.document["evidence_type"] == "runtime.preflight"
        ]
        if len(preflight) != 1:
            raise ValidationError(
                [
                    f"ExperimentPlan {plan_version} Bundle requires exactly one runtime.preflight artifact"
                ]
            )
        bootstrap = [
            artifact
            for artifact in imported
            if artifact.document["evidence_type"] == "runtime.bootstrap"
        ]
        browser_artifacts = [
            artifact
            for artifact in imported
            if artifact.document["evidence_type"] == "browser.session"
        ]
        preflight_decision = preflight[0].document["facts"]["decision"]
        if preflight_decision != "PROCEED":
            errors: list[str] = []
            if execution_status != "ABORTED":
                errors.append(
                    f"a preflight-stopped ExperimentPlan {plan_version} Bundle must use execution_status ABORTED"
                )
            if bootstrap:
                errors.append(
                    f"a preflight-stopped ExperimentPlan {plan_version} Bundle must not contain runtime.bootstrap"
                )
            if browser_artifacts:
                errors.append(
                    f"a preflight-stopped ExperimentPlan {plan_version} Bundle must not contain browser.session"
                )
            if errors:
                raise ValidationError(errors)
        elif len(bootstrap) != 1:
            raise ValidationError(
                [
                    f"a PROCEED ExperimentPlan {plan_version} Bundle requires exactly one "
                    "runtime.bootstrap artifact"
                ]
            )
        else:
            facts = bootstrap[0].document["facts"]
            expected_profile = {
                "id": project_profile["profile_id"],
                "version": project_profile["version"],
                "sha256": project_profile["seal"]["digest"],
            }
            nodes = {node["node_id"]: node for node in facts["nodes"]}
            profile_nodes = {node["node_id"]: node for node in project_profile["nodes"]}
            if (
                facts["plan_sha256"] != plan["seal"]["digest"]
                or facts["profile"] != expected_profile
                or list(nodes) != project_profile["start_order"]
                or any(
                    nodes[node_id]["policy_sha256"] != sha256_json(profile_nodes[node_id])
                    for node_id in project_profile["start_order"]
                )
            ):
                raise ValidationError(
                    ["runtime.bootstrap authority differs from the sealed Plan or ProjectProfile"]
                )
            browser = facts["browser_exercise"]
            browser_matches = (
                len(browser_artifacts) == 1
                and browser["evidence_sha256"] == browser_artifacts[0].sha256
            )
            if browser["completed"] and not browser_matches:
                raise ValidationError(
                    ["runtime.bootstrap browser reference does not match the generated Evidence"]
                )
            if not browser["completed"] and browser_artifacts:
                raise ValidationError(
                    [
                        "runtime.bootstrap without a completed browser exercise must not be "
                        "accompanied by browser.session"
                    ]
                )
    attachment_paths = [
        attachment.path for artifact in imported for attachment in artifact.attachments
    ]
    if len(attachment_paths) != len(set(attachment_paths)):
        raise ValidationError(["generated evidence contains duplicate attachment paths"])
    validate_evidence_collection_budget(imported)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-", dir=output.parent))
    try:
        _write_json(stage / "sealed-plan.json", plan)
        if project_profile is not None:
            _write_json(stage / "sealed-profile.json", project_profile)
        _, evidence_entries = _artifact_manifest(stage, imported, duplicates, run_id)
        result = evaluate(plan, imported, execution_status)
        primary_variable = next(item for item in plan["variables"] if item["role"] == "PRIMARY")
        report = {
            "schema_version": "0.1",
            "run_id": run_id,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "plan": {
                "id": plan["plan_id"],
                "version": plan["version"],
                "sha256": plan["seal"]["digest"],
            },
            "subject": plan["subject"],
            "baseline": plan["baseline"],
            "random_seed": plan["random_seed"],
            "primary_variable": primary_variable,
            "load_model": plan["load_model"],
            "resource_budget": plan["resource_budget"],
            "change_scope": plan["change_scope"],
            "reproduction_steps": plan["reproduction_steps"],
            "cleanup_steps": plan["cleanup_steps"],
            "evidence": evidence_entries,
            **result,
        }
        _write_json(stage / "report.json", report)
        (stage / "report.md").write_text(render_markdown(report), encoding="utf-8", newline="\n")

        bundle_files = sorted(
            path.relative_to(stage)
            for path in stage.rglob("*")
            if path.is_file()
        )
        if len(bundle_files) + 1 > MAX_BUNDLE_FILES:
            raise ValidationError(
                [f"Bundle exceeds the fixed file-count limit of {MAX_BUNDLE_FILES} files"]
            )
        bundle_manifest = {
            "schema_version": "0.1",
            "run_id": run_id,
            "files": [_hash_file(stage / relative, relative) for relative in bundle_files],
        }
        manifest_bytes = canonical_json_bytes(bundle_manifest) + b"\n"
        retained_bytes = sum(item["size"] for item in bundle_manifest["files"]) + len(
            manifest_bytes
        )
        if retained_bytes > MAX_BUNDLE_BYTES:
            raise ValidationError(
                [f"Bundle exceeds the fixed retained-byte limit of {MAX_BUNDLE_BYTES} bytes"]
            )
        (stage / "bundle-manifest.json").write_bytes(manifest_bytes)
        publish_staged_directory(stage, output)
        return report
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
