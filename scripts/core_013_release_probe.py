from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from importlib.metadata import version
from pathlib import Path
from typing import Any

import veritrail
from pc2_acceptance_core_freeze import acceptance_plan, evidence_document
from veritrail.acceptance_evaluation import evaluate_acceptance
from veritrail.acceptance_plan import seal_acceptance_plan
from veritrail.acceptance_reporting import create_acceptance_bundle_from_imported
from veritrail.canonical import canonical_json_bytes, sha256_bytes
from veritrail.evidence import ImportedEvidence, import_evidence_document


EXPECTED_VERSION = "0.13.0"


class ReleaseProbeFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseProbeFailure(message)


def artifact(
    plan: dict[str, Any],
    spec_id: str,
    commit_sha: str,
    *,
    session_id: str = "pc2-collection-001",
    coverage: str = "COMPLETE",
) -> ImportedEvidence:
    document = evidence_document(plan, spec_id, commit_sha)
    observation = document["metadata"]["veritrail_observation"]
    observation["collection_session_id"] = session_id
    observation["coverage"] = coverage
    return import_evidence_document(document, f"{spec_id}.json")


def artifacts(
    plan: dict[str, Any],
    *,
    api_commit: str = "candidate-001",
    render_commit: str = "candidate-001",
    api_session: str = "pc2-collection-001",
    render_session: str = "pc2-collection-001",
    api_coverage: str = "COMPLETE",
    include_render: bool = True,
) -> list[ImportedEvidence]:
    result = [
        artifact(
            plan,
            "api-spec",
            api_commit,
            session_id=api_session,
            coverage=api_coverage,
        )
    ]
    if include_render:
        result.append(
            artifact(
                plan,
                "render-spec",
                render_commit,
                session_id=render_session,
            )
        )
    return result


def verify_bundle(bundle: Path, imported: list[ImportedEvidence]) -> dict[str, Any]:
    report = json.loads((bundle / "acceptance-report.json").read_text(encoding="utf-8"))
    require(report["verdict"] == "PASS", "imported-snapshot Bundle did not PASS")
    evidence_manifest = json.loads(
        (bundle / "acceptance-evidence-manifest.json").read_text(encoding="utf-8")
    )
    retained = sorted(item["sha256"] for item in evidence_manifest["artifacts"])
    expected = sorted(item.sha256 for item in imported)
    require(retained == expected, "Bundle did not retain the verified imported snapshots")

    manifest = json.loads(
        (bundle / "acceptance-bundle-manifest.json").read_text(encoding="utf-8")
    )
    declared = {item["path"]: item for item in manifest["files"]}
    actual = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file() and path.name != "acceptance-bundle-manifest.json"
    }
    require(actual == set(declared), "Acceptance Bundle file set drifted")
    for relative, item in declared.items():
        payload = (bundle / relative).read_bytes()
        require(item["size"] == len(payload), f"Bundle size drifted: {relative}")
        require(
            item["sha256"] == sha256_bytes(payload),
            f"Bundle digest drifted: {relative}",
        )
    return report


def run(output: Path, expected_source_root: Path | None) -> dict[str, Any]:
    package_path = Path(veritrail.__file__).resolve()
    require(veritrail.__version__ == EXPECTED_VERSION, "Core runtime version drifted")
    require(version("veritrail") == EXPECTED_VERSION, "Core distribution version drifted")
    if expected_source_root is not None:
        source_root = (expected_source_root.resolve() / "src").resolve()
        require(
            not package_path.is_relative_to(source_root),
            "release probe imported Core from the source checkout",
        )

    require(not output.exists(), "release probe output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-core-013-", dir=output.parent))
    try:
        plan = seal_acceptance_plan(acceptance_plan())
        cases = {
            "PASS": artifacts(plan),
            "FAIL": artifacts(plan, render_commit="other-visible-commit"),
            "INCONCLUSIVE": artifacts(
                plan,
                api_commit="wrong-commit",
                render_session="different-session",
            ),
            "PENDING": artifacts(plan, include_render=False),
        }
        verdicts: dict[str, str] = {}
        for expected, imported in cases.items():
            result = evaluate_acceptance(plan, imported, "COMPLETED")
            require(result["verdict"] == expected, f"{expected} case drifted")
            verdicts[expected] = result["verdict"]

        pass_imported = cases["PASS"]
        bundle = stage / "acceptance-bundle"
        create_acceptance_bundle_from_imported(
            plan=plan,
            imported_evidence=pass_imported,
            output=bundle,
            acceptance_id="core-0.13.0-release-probe",
            execution_status="COMPLETED",
        )
        report = verify_bundle(bundle, pass_imported)
        summary = {
            "schema_version": "0.1",
            "status": "PASS",
            "boundary": "CORE_0.13.0_INSTALLED_DISTRIBUTION_PROBE",
            "package_version": version("veritrail"),
            "package_path": str(package_path),
            "verdicts": verdicts,
            "plan_digest": plan["seal"]["digest"],
            "report_verdict": report["verdict"],
            "evidence_sha256": sorted(item.sha256 for item in pass_imported),
        }
        (stage / "summary.json").write_bytes(canonical_json_bytes(summary) + b"\n")
        stage.replace(output)
        return summary
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the installed Core 0.13.0 four-verdict and snapshot boundary."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-source-root", type=Path)
    args = parser.parse_args()
    summary = run(args.output.absolute(), args.expected_source_root)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
