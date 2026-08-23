from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_bytes, sha256_json
from veritrail.errors import ValidationError
from veritrail.jsonio import load_json_object_bytes, read_stable_bytes
from veritrail.plan import validate_plan
from veritrail.project_profile import project_profile_digest, validate_project_profile

from veritrail_starter import __version__
from veritrail_starter.contract import build_documents, normalize_answers
from veritrail_starter.doctor import require_compatible_core, require_supported_host
from veritrail_starter.errors import StarterError, conflict, invalid, workspace_invalid

WORKSPACE_NAME = ".veritrail"
MANIFEST_NAME = "starter-manifest.json"
PAYLOAD_NAMES = (
    "answers.snapshot.json",
    "profile.draft.json",
    "plan.draft.json",
    "tool-bindings.local.json",
    "REVIEW.md",
    "handoff.ps1",
)
EXPECTED_NAMES = frozenset((MANIFEST_NAME, *PAYLOAD_NAMES))
MAX_WORKSPACE_FILE_BYTES = 2 * 1024 * 1024
TEMP_PREFIX = ".veritrail.tmp-"
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def _json_bytes(value: Any) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _is_reparse(path: Path) -> bool:
    metadata = os.lstat(path)
    return path.is_symlink() or bool(
        getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT
    )


def _markdown_text(value: str) -> str:
    return value.replace("`", "\\`").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _review_markdown(answers: dict[str, Any], profile: dict[str, Any], plan: dict[str, Any]) -> bytes:
    step_rows = "\n".join(
        f"- `{_markdown_text(step['id'])}`: `{step['action']}`"
        for step in answers["browser"]["steps"]
    )
    text = f"""# VeriTrail Starter Review

> `DRAFT / NOT_SEALED`
>
> This file is an authoring review aid. It is not a Preview, ExecutionStatus, Verdict, or approval.

## USER_SUPPLIED

- Workspace ID: `{answers['workspace_id']}`
- Question: {_markdown_text(answers['question'])}
- Subject: `{answers['subject']['id']}` version `{_markdown_text(answers['subject']['version'])}`
- Subject root: recorded only in `answers.snapshot.json`
- Executable: recorded only in `tool-bindings.local.json`
- Fixed port: `{answers['application']['port']}`
- Health path: `{_markdown_text(answers['application']['health_path'])}`
- Browser origin: `{_markdown_text(answers['browser']['allowed_origin'])}`
- Screenshot safety: `{answers['browser']['screenshot_safety']}`

### Explicit browser checks

{step_rows}

## DERIVED_FROM_PRESET

- ProjectProfile: `{profile['profile_id']}` / Schema 0.2 / `SINGLE_APPLICATION`
- ExperimentPlan: `{plan['plan_id']}` / Schema 0.7
- Prospective Profile digest: `{project_profile_digest(profile)}`
- Runtime evidence: `runtime.preflight`, `runtime.bootstrap`, `browser.session`
- Lifecycle, browser-integrity, screenshot-coverage, subject-integrity, and cleanup assertions are fixed by preset 0.1.

## DISCOVERED_CANDIDATE

No discovery result is promoted into this DRAFT. `doctor` reports candidates separately.

## NOT_PROVEN

- The application has not been started.
- Chromium has not been used by this workspace operation.
- No ProjectProfile or ExperimentPlan has been sealed.
- No BootstrapPreview digest has been approved.
- No Evidence, Bundle, ExecutionStatus, or Verdict exists.

## STOP LINE

Read every JSON draft and local binding. If any fact is wrong or incomplete, discard this workspace and create a new Answers file. Do not weaken assertions after observing a failure.
"""
    return text.encode("utf-8")


def _handoff_script() -> bytes:
    text = r"""# DRAFT helper: prints commands only. It never invokes VeriTrail Core.
Write-Output 'Run these commands manually from the subject root only after reviewing every DRAFT:'
Write-Output '1. veritrail bootstrap-profile-seal --profile .veritrail\profile.draft.json --output artifacts\starter-handoff\profile.sealed.json'
Write-Output '2. veritrail seal --plan .veritrail\plan.draft.json --profile artifacts\starter-handoff\profile.sealed.json --output artifacts\starter-handoff\plan.sealed.json'
Write-Output '3. veritrail bootstrap-preview --plan artifacts\starter-handoff\plan.sealed.json --profile artifacts\starter-handoff\profile.sealed.json --subject-root . --tool-bindings .veritrail\tool-bindings.local.json'
Write-Output '4. Inspect the exact Preview and replace <REVIEWED_PREVIEW_SHA256> below yourself.'
Write-Output '5. veritrail run --plan artifacts\starter-handoff\plan.sealed.json --profile artifacts\starter-handoff\profile.sealed.json --subject-root . --tool-bindings .veritrail\tool-bindings.local.json --approve-bootstrap-preview-sha256 <REVIEWED_PREVIEW_SHA256> --run-id <NEW_RUN_ID> --output artifacts\<NEW_RUN_ID>'
"""
    return text.encode("utf-8")


def render_workspace(answers: dict[str, Any]) -> dict[str, bytes]:
    profile, plan, bindings = build_documents(answers)
    payloads = {
        "answers.snapshot.json": _json_bytes(answers),
        "profile.draft.json": _json_bytes(profile),
        "plan.draft.json": _json_bytes(plan),
        "tool-bindings.local.json": _json_bytes(bindings),
        "REVIEW.md": _review_markdown(answers, profile, plan),
        "handoff.ps1": _handoff_script(),
    }
    manifest = {
        "schema_version": "0.1",
        "starter_version": __version__,
        "preset": {"id": "single-webapp", "version": "0.1"},
        "workspace_id": answers["workspace_id"],
        "authoring_state": "DRAFT",
        "seal_state": "NOT_SEALED",
        "input_sha256": sha256_json(answers),
        "prospective_profile_sha256": project_profile_digest(profile),
        "files": {
            name: {"sha256": sha256_bytes(content), "size": len(content)}
            for name, content in sorted(payloads.items())
        },
    }
    return {MANIFEST_NAME: _json_bytes(manifest), **payloads}


def _safe_remove_temp(temp: Path, subject_root: Path) -> None:
    try:
        resolved_root = subject_root.resolve(strict=True)
        if not temp.exists() or _is_reparse(temp):
            return
        resolved_temp = temp.resolve(strict=True)
        if (
            resolved_temp.parent == resolved_root
            and resolved_temp.name.startswith(TEMP_PREFIX)
        ):
            entries = list(resolved_temp.iterdir())
            if any(entry.name not in EXPECTED_NAMES for entry in entries):
                return
            for entry in entries:
                metadata = os.lstat(entry)
                if (
                    entry.is_symlink()
                    or bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)
                    or not stat.S_ISREG(metadata.st_mode)
                    or metadata.st_nlink != 1
                ):
                    return
            for entry in entries:
                entry.unlink()
            resolved_temp.rmdir()
    except OSError:
        return


def initialize_workspace(answers_document: dict[str, Any], preset: str) -> dict[str, Any]:
    require_compatible_core()
    require_supported_host()
    if preset != "single-webapp":
        raise invalid("--preset must be single-webapp")
    answers = normalize_answers(answers_document)
    if answers["preset"] != preset:
        raise invalid("--preset must match Answers.preset")
    subject_root = Path(answers["subject"]["root"])
    target = subject_root / WORKSPACE_NAME
    if os.path.lexists(target):
        raise conflict("the .veritrail workspace already exists; Starter never overwrites")
    rendered = render_workspace(answers)
    temp = Path(tempfile.mkdtemp(prefix=TEMP_PREFIX, dir=subject_root))
    try:
        for name, content in rendered.items():
            path = temp / name
            with path.open("xb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
        try:
            temp.rename(target)
        except OSError as exc:
            if os.path.lexists(target):
                raise conflict(
                    "the .veritrail workspace appeared during creation; nothing was overwritten"
                ) from exc
            raise
    except Exception:
        _safe_remove_temp(temp, subject_root)
        raise
    return {
        "workspace": WORKSPACE_NAME,
        "authoring_state": "DRAFT",
        "seal_state": "NOT_SEALED",
        "files": sorted(rendered),
        "input_sha256": sha256_json(answers),
    }


def _read_workspace(workspace: Path) -> tuple[Path, dict[str, Any], dict[str, bytes]]:
    try:
        if not workspace.exists() or _is_reparse(workspace):
            raise OSError("unsafe workspace")
        resolved = workspace.resolve(strict=True)
    except OSError as exc:
        raise workspace_invalid("workspace must be an existing ordinary .veritrail directory") from exc
    if resolved.name != WORKSPACE_NAME or not resolved.is_dir():
        raise workspace_invalid("workspace must be an existing ordinary .veritrail directory")
    try:
        names = {item.name for item in resolved.iterdir()}
    except OSError as exc:
        raise workspace_invalid("workspace could not be enumerated safely") from exc
    if names != EXPECTED_NAMES:
        raise workspace_invalid("workspace file set does not match Starter 0.1")
    content = {
        name: read_stable_bytes(
            resolved / name,
            label="Starter workspace file",
            max_bytes=MAX_WORKSPACE_FILE_BYTES,
        )
        for name in sorted(names)
    }
    manifest = load_json_object_bytes(
        content[MANIFEST_NAME], label="Starter manifest", name=MANIFEST_NAME
    )
    return resolved, manifest, content


def _validate_workspace(workspace: Path) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    require_compatible_core()
    try:
        resolved, manifest, actual = _read_workspace(workspace)
    except ValidationError as exc:
        raise workspace_invalid("workspace could not be read as one safe snapshot") from exc
    if manifest.get("authoring_state") != "DRAFT" or manifest.get("seal_state") != "NOT_SEALED":
        raise workspace_invalid("workspace must remain DRAFT / NOT_SEALED")
    try:
        answers = load_json_object_bytes(
            actual["answers.snapshot.json"],
            label="Answers snapshot",
            name="answers.snapshot.json",
        )
        normalized = normalize_answers(answers)
        expected = render_workspace(normalized)
    except (StarterError, ValidationError, ValueError) as exc:
        raise workspace_invalid("workspace content no longer satisfies Starter/Core contracts") from exc
    if actual != expected:
        raise workspace_invalid("workspace bytes differ from deterministic Starter output")
    profile = load_json_object_bytes(
        actual["profile.draft.json"], label="Profile draft", name="profile.draft.json"
    )
    plan = load_json_object_bytes(
        actual["plan.draft.json"], label="Plan draft", name="plan.draft.json"
    )
    if "seal" in profile or "seal" in plan:
        raise workspace_invalid("drafts must not contain a seal")
    validate_project_profile(profile)
    digest = project_profile_digest(profile)
    ephemeral = dict(profile)
    ephemeral["seal"] = {"algorithm": "sha256", "digest": digest}
    validate_plan(plan, ephemeral)
    # ToolBindings bytes are already required to equal render_workspace(normalized),
    # whose structure comes from build_documents. Do not reopen a mutable path and
    # mix two different workspace snapshots in one validation result.
    load_json_object_bytes(
        actual["tool-bindings.local.json"],
        label="ToolBindings",
        name="tool-bindings.local.json",
    )
    try:
        _, confirmation_manifest, confirmation = _read_workspace(resolved)
    except (StarterError, ValidationError) as exc:
        raise workspace_invalid("workspace changed during validation") from exc
    if confirmation_manifest != manifest or confirmation != actual:
        raise workspace_invalid("workspace changed during validation")
    report = {
        "workspace": WORKSPACE_NAME,
        "valid": True,
        "authoring_state": "DRAFT",
        "seal_state": "NOT_SEALED",
        "input_sha256": manifest["input_sha256"],
        "prospective_profile_sha256": digest,
        "file_count": len(actual),
    }
    return report, resolved, normalized


def validate_workspace(workspace: Path) -> dict[str, Any]:
    report, _, _ = _validate_workspace(workspace)
    return report


def review_workspace(workspace: Path) -> dict[str, Any]:
    report, _, answers = _validate_workspace(workspace)
    return {
        **report,
        "review_file": "REVIEW.md",
        "business_step_ids": [item["id"] for item in answers["browser"]["steps"]],
        "stop_line": "HUMAN_REVIEW_REQUIRED_BEFORE_CORE_HANDOFF",
    }


def handoff_workspace(workspace: Path) -> dict[str, Any]:
    report, _, _ = _validate_workspace(workspace)
    return {
        **report,
        "handoff_script": "handoff.ps1",
        "execution": "NOT_PERFORMED",
        "preview_approval": "OPERATOR_MUST_SUPPLY_EXACT_DIGEST",
        "next_action": "RUN_HANDOFF_SCRIPT_TO_PRINT_MANUAL_COMMANDS",
    }
