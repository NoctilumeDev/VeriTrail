from __future__ import annotations

import copy
import shutil
import tempfile
from pathlib import Path
from typing import Any

from veritrail import __version__
from veritrail.atomic_publish import publish_staged_directory
from veritrail.canonical import canonical_json_bytes
from veritrail.catalog import build_catalog
from veritrail.errors import SafetyError
from veritrail.evidence import import_evidence_document
from veritrail.plan import seal_plan
from veritrail.reporting import create_bundle


_DEMO_PLAN: dict[str, Any] = {
    "schema_version": "0.1",
    "plan_id": "core-first-run-demo",
    "version": 1,
    "subject": {
        "id": "veritrail-built-in-demo",
        "version": "1.0.0",
        "source_ref": "veritrail-core-demo",
    },
    "question": "Does the built-in fixture satisfy its two declared hard invariants?",
    "baseline": {
        "id": "core-first-run-baseline-v1",
        "status": "VALID",
        "fingerprint": "f548b41b230b12624db97b292309484aebc7d67a5b06b2c9fe6b381865bc1f14",
        "tolerances": {"fixture_contract": "exact"},
    },
    "experiment_type": "SINGLE_VARIABLE",
    "variables": [
        {
            "name": "fixture_outcome",
            "role": "PRIMARY",
            "value": "controlled",
            "source": "built-in demo",
        },
        {
            "name": "fixture_contract",
            "role": "CONTROLLED",
            "value": "core-first-run-v1",
            "source": "built-in demo",
        },
    ],
    "required_evidence": ["automated.test-summary"],
    "assertions": [
        {
            "id": "suite-completed-successfully",
            "severity": "HARD",
            "evidence_type": "automated.test-summary",
            "path": "/facts/suite_passed",
            "operator": "eq",
            "expected": True,
        },
        {
            "id": "suite-has-zero-failures",
            "severity": "HARD",
            "evidence_type": "automated.test-summary",
            "path": "/facts/failures",
            "operator": "eq",
            "expected": 0,
        },
    ],
    "random_seed": 20260825,
    "resource_budget": {
        "memory_soft_mb": 128,
        "memory_hard_mb": 256,
        "max_artifact_bytes": 1048576,
    },
    "load_model": {"total_requests": 1, "duration_seconds": 1},
    "change_scope": {
        "level": "L2_CONTRACT",
        "owner": "VeriTrail Core",
        "expected_blast_radius": "Built-in first-run Plan, Evidence, Verdict, Bundle, and Catalog",
        "consumers": ["CLI", "JSON report exporter", "Markdown report exporter", "Catalog"],
    },
    "reproduction_steps": [
        "Install a published VeriTrail Core wheel in an isolated Python environment.",
        "Run veritrail demo with a new output directory.",
        "Verify the PASS and intentional FAIL reports use the same sealed Plan.",
    ],
    "cleanup_steps": [
        "Remove only the demo output directory after reviewing its reports and Catalog manifest."
    ],
}


def _demo_evidence(*, passed: bool) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "evidence_type": "automated.test-summary",
        "source": "VeriTrail built-in deterministic demo",
        "captured_at": "2026-08-25T00:00:00+08:00",
        "facts": {
            "suite_passed": passed,
            "failures": 0 if passed else 1,
            "tests": 1,
        },
        "observed_variables": {
            "fixture_outcome": "controlled",
            "fixture_contract": "core-first-run-v1",
        },
    }


def create_first_run_demo(output: Path) -> dict[str, Any]:
    """Create one self-contained PASS/FAIL first run without repository files."""

    if output.exists():
        raise SafetyError(f"refusing to overwrite existing output directory: {output.name}")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-demo-", dir=output.parent))
    try:
        artifacts = stage / "artifacts"
        artifacts.mkdir()
        plan = seal_plan(copy.deepcopy(_DEMO_PLAN))
        reports: dict[str, dict[str, Any]] = {}
        for label, passed in (("pass", True), ("fail", False)):
            evidence = import_evidence_document(
                _demo_evidence(passed=passed),
                f"built-in-{label}-evidence.json",
            )
            reports[label] = create_bundle(
                plan=plan,
                evidence_paths=[],
                generated_evidence=[evidence],
                output=artifacts / f"demo-{label}",
                run_id=f"demo-{label}",
                execution_status="COMPLETED",
            )

        catalog = build_catalog(artifacts, stage / "catalog")
        summary = {
            "schema_version": "0.1",
            "command": "demo",
            "tool_version": __version__,
            "plan_sha256": plan["seal"]["digest"],
            "runs": {
                "pass": {
                    "run_id": reports["pass"]["run_id"],
                    "verdict": reports["pass"]["verdict"],
                    "report": "artifacts/demo-pass/report.json",
                },
                "fail": {
                    "run_id": reports["fail"]["run_id"],
                    "verdict": reports["fail"]["verdict"],
                    "report": "artifacts/demo-fail/report.json",
                },
            },
            "catalog": {
                "catalog_id": catalog.catalog_id,
                "run_count": catalog.run_count,
                "issue_count": catalog.issue_count,
                "manifest": "catalog/catalog-manifest.json",
            },
            "boundary": "SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE",
        }
        (stage / "demo-summary.json").write_bytes(canonical_json_bytes(summary) + b"\n")
        publish_staged_directory(stage, output)
        return summary
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
