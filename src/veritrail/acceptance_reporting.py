from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from veritrail.acceptance_evaluation import evaluate_acceptance
from veritrail.acceptance_plan import verify_sealed_acceptance_plan
from veritrail.atomic_publish import publish_staged_directory
from veritrail.canonical import canonical_json_bytes
from veritrail.errors import SafetyError, ValidationError
from veritrail.evidence import (
    ImportedEvidence,
    import_evidence_files,
    validate_evidence_collection_budget,
)
from veritrail.markdown import markdown_code, markdown_json, markdown_text
from veritrail.resource_limits import (
    MAX_ARTIFACT_BYTES,
    MAX_BUNDLE_BYTES,
    MAX_BUNDLE_FILES,
)


ACCEPTANCE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


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


def _retained_digest(value: Any) -> str | None:
    """Retain only a syntactically valid digest from optional observation metadata."""
    return value if isinstance(value, str) and SHA256_PATTERN.fullmatch(value) else None


def _persist_evidence(
    stage: Path,
    evidence: list[ImportedEvidence],
    duplicates: list[str],
    acceptance_id: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    evidence_dir = stage / "evidence"
    evidence_dir.mkdir()
    entries: list[dict[str, Any]] = []
    for index, artifact in enumerate(evidence, start=1):
        evidence_type = artifact.document["evidence_type"]
        filename = f"{index:03d}-{evidence_type}-{artifact.sha256[:12]}.json"
        relative_path = Path("evidence") / filename
        (stage / relative_path).write_bytes(canonical_json_bytes(artifact.document))
        observation = None
        metadata = artifact.document.get("metadata")
        if isinstance(metadata, dict):
            observation = metadata.get("veritrail_observation")
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
            "source_name": artifact.input_name,
            "retention": "local-default",
            "observation_spec_digest": (
                _retained_digest(observation.get("observation_spec_digest"))
                if isinstance(observation, dict)
                else None
            ),
            "facts_digest": (
                _retained_digest(observation.get("facts_digest"))
                if isinstance(observation, dict)
                else None
            ),
        }
        entries.append(entry)
    manifest = {
        "manifest_kind": "ACCEPTANCE_EVIDENCE",
        "schema_version": "0.1",
        "acceptance_id": acceptance_id,
        "artifacts": entries,
        "duplicate_inputs_ignored": sorted(duplicates),
    }
    _write_json(stage / "acceptance-evidence-manifest.json", manifest)
    return manifest, entries


def render_acceptance_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# VeriTrail acceptance {markdown_code(report['acceptance_id'])}",
        "",
        f"- Execution status: {markdown_code(report['execution_status'])}",
        f"- Verdict: {markdown_code(report['verdict'])}",
        f"- Plan: {markdown_code(str(report['plan']['id']) + '@' + str(report['plan']['version']))}",
        f"- Plan SHA-256: {markdown_code(report['plan']['sha256'])}",
        f"- Created at: {markdown_code(report['created_at'])}",
        "",
        "## Reasons",
        "",
    ]
    for reason in report["reasons"]:
        requirement = (
            f" ({markdown_code(reason['requirement_id'])})"
            if reason.get("requirement_id")
            else ""
        )
        lines.append(
            f"- {markdown_code(reason['code'])}{requirement} — {markdown_text(reason['message'])}"
        )

    lines.extend(
        [
            "",
            "## Evidence bindings",
            "",
            "| Requirement | Type | Status | Evidence SHA-256 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for binding in report["evidence_bindings"]:
        lines.append(
            "| {requirement} | {type} | {status} | {digest} |".format(
                requirement=markdown_text(binding["requirement_id"]),
                type=markdown_text(binding["evidence_type"]),
                status=markdown_text(binding["status"]),
                digest=markdown_text(binding["evidence_sha256"] or "—"),
            )
        )

    lines.extend(
        [
            "",
            "## Deterministic rules",
            "",
            "| ID | Category | Status | Left | Right |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for rule in report["rule_results"]:
        lines.append(
            "| {id} | {category} | {status} | {left} | {right} |".format(
                id=markdown_text(rule["id"]),
                category=markdown_text(rule["category"]),
                status=markdown_text(rule["status"]),
                left=markdown_json(rule["left"]),
                right=markdown_json(rule["right"]),
            )
        )

    lines.extend(["", "## Evidence", ""])
    for artifact in report["evidence"]:
        lines.append(
            f"- {markdown_code(artifact['evidence_type'])} — "
            f"{markdown_code(artifact['sha256'])} ({artifact['size']} bytes, "
            f"redactions: {artifact['redacted_fields']})"
        )
    if not report["evidence"]:
        lines.append("- No Evidence was imported.")

    lines.extend(
        [
            "",
            "## Declared boundary",
            "",
            f"- Subject: {markdown_code(report['subject'], json_value=True)}",
            f"- Question: {markdown_code(report['question'])}",
            f"- Governance: {markdown_code(report['governance'], json_value=True)}",
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


def create_acceptance_bundle(
    *,
    plan: dict[str, Any],
    evidence_paths: list[Path],
    output: Path,
    acceptance_id: str,
    execution_status: str,
) -> dict[str, Any]:
    verify_sealed_acceptance_plan(plan)
    if not ACCEPTANCE_ID_PATTERN.fullmatch(acceptance_id):
        raise ValidationError(
            ["acceptance_id must be a 2-64 character lowercase identifier"]
        )
    if output.exists():
        raise SafetyError(
            f"refusing to overwrite existing output directory: {output.name}"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    imported, duplicates = import_evidence_files(evidence_paths, MAX_ARTIFACT_BYTES)
    validate_evidence_collection_budget(imported)

    stage = Path(tempfile.mkdtemp(prefix=".veritrail-acceptance-", dir=output.parent))
    try:
        _write_json(stage / "sealed-acceptance-plan.json", plan)
        _, evidence_entries = _persist_evidence(
            stage, imported, duplicates, acceptance_id
        )
        result = evaluate_acceptance(plan, imported, execution_status)
        report = {
            "report_kind": "ACCEPTANCE",
            "schema_version": "0.1",
            "acceptance_id": acceptance_id,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "plan": {
                "kind": "ACCEPTANCE",
                "id": plan["plan_id"],
                "version": plan["version"],
                "sha256": plan["seal"]["digest"],
            },
            "subject": plan["subject"],
            "question": plan["question"],
            "governance": plan["governance"],
            "resource_budget": plan["resource_budget"],
            "change_scope": plan["change_scope"],
            "reproduction_steps": plan["reproduction_steps"],
            "cleanup_steps": plan["cleanup_steps"],
            "evidence": evidence_entries,
            **result,
        }
        _write_json(stage / "acceptance-report.json", report)
        (stage / "acceptance-report.md").write_text(
            render_acceptance_markdown(report), encoding="utf-8", newline="\n"
        )

        bundle_files = sorted(
            path.relative_to(stage) for path in stage.rglob("*") if path.is_file()
        )
        if len(bundle_files) + 1 > MAX_BUNDLE_FILES:
            raise ValidationError(
                [
                    "AcceptanceBundle exceeds the fixed file-count limit of "
                    f"{MAX_BUNDLE_FILES} files"
                ]
            )
        manifest = {
            "bundle_kind": "ACCEPTANCE",
            "schema_version": "0.1",
            "acceptance_id": acceptance_id,
            "files": [
                _hash_file(stage / relative, relative) for relative in bundle_files
            ],
        }
        manifest_bytes = canonical_json_bytes(manifest) + b"\n"
        retained_bytes = sum(item["size"] for item in manifest["files"]) + len(
            manifest_bytes
        )
        if retained_bytes > MAX_BUNDLE_BYTES:
            raise ValidationError(
                [
                    "AcceptanceBundle exceeds the fixed retained-byte limit of "
                    f"{MAX_BUNDLE_BYTES} bytes"
                ]
            )
        (stage / "acceptance-bundle-manifest.json").write_bytes(manifest_bytes)
        publish_staged_directory(stage, output)
        return report
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
