from __future__ import annotations

import json
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_bytes
from veritrail.errors import SafetyError, ValidationError
from veritrail.evidence import ImportedEvidence, import_evidence_files, verify_imported_evidence
from veritrail.plan import verify_sealed_plan
from veritrail.verdict import evaluate

RUN_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")


def _write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_json_bytes(value) + b"\n")


def _hash_file(path: Path, relative_path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": relative_path.as_posix(),
        "sha256": sha256_bytes(content),
        "size": len(content),
    }


def _markdown_value(value: Any) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return rendered.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# VeriTrail run `{_markdown_value(report['run_id']).strip(chr(34))}`",
        "",
        f"- Execution status: `{report['execution_status']}`",
        f"- Verdict: `{report['verdict']}`",
        f"- Plan: `{report['plan']['id']}@{report['plan']['version']}`",
        f"- Plan SHA-256: `{report['plan']['sha256']}`",
        f"- Baseline: `{report['baseline']['id']}` (`{report['baseline']['status']}`)",
        f"- Random seed: `{report['random_seed']}`",
        f"- Created at: `{report['created_at']}`",
        "",
        "## Reasons",
        "",
    ]
    for reason in report["reasons"]:
        lines.append(f"- `{reason['code']}` — {_markdown_value(reason['message'])}")
    lines.extend(["", "## Assertions", "", "| ID | Severity | Status | Actual | Expected |", "| --- | --- | --- | --- | --- |"])
    for assertion in report["assertions"]:
        lines.append(
            "| {id} | {severity} | {status} | {actual} | {expected} |".format(
                id=_markdown_value(assertion["id"]),
                severity=assertion["severity"],
                status=assertion["status"],
                actual=_markdown_value(assertion["actual"]),
                expected=_markdown_value(assertion["expected"]),
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
            lines.append(
                f"- `{artifact['evidence_type']}` — `{artifact['sha256']}` "
                f"({artifact['size']} bytes, redactions: {artifact['redacted_fields']}{decision})"
            )
    else:
        lines.append("- No evidence was imported.")
    lines.extend(["", "## Evidence gaps and contamination", ""])
    if report["missing_evidence"]:
        lines.append(f"- Missing evidence: {_markdown_value(report['missing_evidence'])}")
    if report["contamination"]:
        for item in report["contamination"]:
            lines.append(f"- `{item['code']}` — {_markdown_value(item['message'])}")
    if not report["missing_evidence"] and not report["contamination"]:
        lines.append("- None detected by the active deterministic rule set.")
    lines.extend(
        [
            "",
            "## Applicability boundary",
            "",
            f"- Subject: `{_markdown_value(report['subject'])}`",
            f"- Primary variable: `{_markdown_value(report['primary_variable'])}`",
            f"- Load model: `{_markdown_value(report['load_model'])}`",
            f"- Resource budget: `{_markdown_value(report['resource_budget'])}`",
            f"- Change scope: `{_markdown_value(report['change_scope'])}`",
            "",
            "## Reproduction and cleanup",
            "",
        ]
    )
    for index, step in enumerate(report["reproduction_steps"], start=1):
        lines.append(f"{index}. {_markdown_value(step)}")
    lines.extend(["", "Cleanup:", ""])
    for index, step in enumerate(report["cleanup_steps"], start=1):
        lines.append(f"{index}. {_markdown_value(step)}")
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
) -> dict[str, Any]:
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
        seen_hashes.add(artifact.sha256)
        imported.append(artifact)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-", dir=output.parent))
    try:
        _write_json(stage / "sealed-plan.json", plan)
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
        bundle_manifest = {
            "schema_version": "0.1",
            "run_id": run_id,
            "files": [_hash_file(stage / relative, relative) for relative in bundle_files],
        }
        _write_json(stage / "bundle-manifest.json", bundle_manifest)
        stage.rename(output)
        return report
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
