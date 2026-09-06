from __future__ import annotations

from pathlib import Path
from typing import Any

from veritrail.acceptance_reporting import create_acceptance_bundle_from_imported

from veritrail_github.handoff import import_verified_handoff_evidence


def create_reference_acceptance_bundle(
    *,
    plan: dict[str, Any],
    handoff_manifest_path: Path,
    output: Path,
    acceptance_id: str,
    execution_status: str,
) -> dict[str, Any]:
    """Exercise the public P3 handoff without adding plugin-side judgment."""

    imported = import_verified_handoff_evidence(handoff_manifest_path)
    return create_acceptance_bundle_from_imported(
        plan=plan,
        imported_evidence=list(imported),
        output=output,
        acceptance_id=acceptance_id,
        execution_status=execution_status,
    )
