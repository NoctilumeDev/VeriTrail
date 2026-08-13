from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from veritrail.bootstrap_preview import ResolvedBootstrap, resolve_bootstrap
from veritrail.bootstrap_run import BootstrapObservedRunResult, run_observed_bootstrap
from veritrail.evidence import ImportedEvidence, import_evidence_document
from veritrail.errors import SafetyError, ValidationError
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.reporting import RUN_ID_PATTERN, create_bundle
from veritrail.resources import collect_preflight_evidence

SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class BootstrapPublicRunResult:
    report: dict[str, Any]
    preflight: ImportedEvidence
    observed: BootstrapObservedRunResult
    preview_sha256: str


def run_bootstrap_bundle(
    plan: dict[str, Any],
    profile: dict[str, Any],
    *,
    subject_root: Path,
    tool_bindings_path: Path,
    approved_preview_sha256: str,
    output: Path,
    run_id: str,
    resolver: Callable[..., ResolvedBootstrap] = resolve_bootstrap,
    preflight_collector: Callable[[dict[str, Any], Path], dict[str, Any]] = (
        collect_preflight_evidence
    ),
    observed_runner: Callable[..., BootstrapObservedRunResult] = run_observed_bootstrap,
) -> BootstrapPublicRunResult:
    """Create one immutable Plan 0.6 Bundle after an approved PROCEED preflight."""

    verify_sealed_project_profile(profile)
    verify_sealed_plan(plan, profile)
    if plan.get("schema_version") != "0.6":
        raise ValidationError(["bootstrap Run requires ExperimentPlan schema_version '0.6'"])
    if not isinstance(approved_preview_sha256, str) or not SHA256_PATTERN.fullmatch(
        approved_preview_sha256
    ):
        raise ValidationError(
            ["Plan 0.6 run requires a lowercase SHA-256 bootstrap Preview approval"]
        )
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValidationError(["run_id must be a 2-64 character lowercase identifier"])
    if output.exists():
        raise SafetyError(f"refusing to overwrite existing output directory: {output.name}")

    resolved = resolver(
        plan,
        profile,
        subject_root=subject_root,
        tool_bindings_path=tool_bindings_path,
    )
    preview_sha256 = resolved.preview.get("preview_sha256")
    if preview_sha256 != approved_preview_sha256:
        raise SafetyError(
            "approved bootstrap digest does not match the live BootstrapPreview"
        )

    preflight_document = preflight_collector(plan, output.parent)
    preflight = import_evidence_document(
        preflight_document, "generated-preflight.json"
    )
    decision = preflight.document["facts"]["decision"]
    if decision != "PROCEED":
        raise SafetyError(
            "M10 public Run does not yet emit a preflight-stopped Plan 0.6 Bundle"
        )

    observed = observed_runner(
        plan,
        profile,
        resolved,
        output_parent=output.parent,
    )
    if observed.evidence is None:
        raise SafetyError(
            "M10 observed Run cleaned its resources but could not finalize bootstrap Evidence"
        )

    generated = [preflight, observed.evidence.bootstrap]
    if observed.browser is not None:
        generated.append(observed.browser)
    report = create_bundle(
        plan=plan,
        project_profile=profile,
        evidence_paths=[],
        output=output,
        run_id=run_id,
        execution_status=observed.evidence.execution_status,
        generated_evidence=generated,
    )
    return BootstrapPublicRunResult(
        report=report,
        preflight=preflight,
        observed=observed,
        preview_sha256=preview_sha256,
    )
