from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from typing import Any

import veritrail
from veritrail.acceptance_evaluation import evaluate_acceptance
from veritrail.evidence import import_evidence_document


class FreezeFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FreezeFailure(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_json(value: Any) -> str:
    return digest_bytes(canonical_bytes(value))


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.name} must contain an object")
    return value


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_bytes(value) + b"\n")


def observation_spec_digest(spec: dict[str, Any]) -> str:
    return digest_json(
        {
            "canonicalization_profile": spec["canonicalization_profile"],
            "contract": spec["contract"],
            "evidence_type": spec["evidence_type"],
            "coordinates": spec["coordinates"],
            "projections": spec["projections"],
        }
    )


def acceptance_plan() -> dict[str, Any]:
    return {
        "plan_kind": "ACCEPTANCE",
        "schema_version": "0.1",
        "plan_id": "pc2-core-freeze",
        "version": 1,
        "subject": {
            "id": "acceptance-core",
            "version": "pc1-candidate",
            "source_ref": "pc2-local-fixture",
        },
        "question": "Do two independently retained observations expose the same declared commit?",
        "governance": {
            "claim_owner_ref": "pc2-contract-owner",
            "drafter_ref": "pc2-fixture-author",
            "seal_authority_ref": "pc2-freeze-gate",
            "seal_decision": "CONFIRMED",
        },
        "observation_specs": [
            {
                "id": "api-spec",
                "contract": {"id": "fixture.platform-api", "version": "0.1"},
                "evidence_type": "platform.api",
                "coordinates": {"resource": "release", "ref": "candidate-001"},
                "projections": ["commit_sha", "collection_session_id", "coverage"],
                "canonicalization_profile": "veritrail-json-c14n/1",
            },
            {
                "id": "render-spec",
                "contract": {"id": "fixture.public-render", "version": "0.1"},
                "evidence_type": "platform.render",
                "coordinates": {"resource": "readme", "ref": "candidate-001"},
                "projections": ["commit_sha", "collection_session_id", "coverage"],
                "canonicalization_profile": "veritrail-json-c14n/1",
            },
        ],
        "evidence_requirements": [
            {
                "id": "api-evidence",
                "observation_spec_id": "api-spec",
                "cardinality": "EXACTLY_ONE",
            },
            {
                "id": "render-evidence",
                "observation_spec_id": "render-spec",
                "cardinality": "EXACTLY_ONE",
            },
        ],
        "sufficiency_rules": [
            {
                "id": "api-coverage",
                "left": {
                    "requirement_id": "api-evidence",
                    "path": "/metadata/veritrail_observation/coverage",
                },
                "operator": "eq",
                "right": "COMPLETE",
            },
            {
                "id": "render-coverage",
                "left": {
                    "requirement_id": "render-evidence",
                    "path": "/metadata/veritrail_observation/coverage",
                },
                "operator": "eq",
                "right": "COMPLETE",
            },
        ],
        "integrity_rules": [
            {
                "id": "same-session",
                "left": {
                    "requirement_id": "api-evidence",
                    "path": "/metadata/veritrail_observation/collection_session_id",
                },
                "operator": "eq",
                "right": {
                    "requirement_id": "render-evidence",
                    "path": "/metadata/veritrail_observation/collection_session_id",
                },
            }
        ],
        "assertions": [
            {
                "id": "api-commit",
                "severity": "HARD",
                "left": {"requirement_id": "api-evidence", "path": "/facts/commit_sha"},
                "operator": "eq",
                "right": "candidate-001",
            },
            {
                "id": "same-visible-commit",
                "severity": "HARD",
                "left": {"requirement_id": "api-evidence", "path": "/facts/commit_sha"},
                "operator": "eq",
                "right": {
                    "requirement_id": "render-evidence",
                    "path": "/facts/commit_sha",
                },
            },
        ],
        "resource_budget": {"network": "NONE", "hardware": "CPU_ONLY"},
        "change_scope": {
            "level": "L2_CONTRACT_PLUS_L3_SYSTEM",
            "owner": "acceptance-core",
            "expected_blast_radius": "parallel acceptance-only path",
            "consumers": ["acceptance-cli"],
        },
        "reproduction_steps": ["Import two retained local fixture observations."],
        "cleanup_steps": ["Remove temporary source inputs and staging directories."],
    }


def evidence_document(
    sealed_plan: dict[str, Any], spec_id: str, commit_sha: str
) -> dict[str, Any]:
    spec = next(item for item in sealed_plan["observation_specs"] if item["id"] == spec_id)
    facts = {"commit_sha": commit_sha}
    return {
        "schema_version": "0.1",
        "evidence_type": spec["evidence_type"],
        "source": "pc2-local-fixture/0.1",
        "captured_at": "2026-09-05T00:00:00Z",
        "facts": facts,
        "metadata": {
            "collector_note": "pc2-sensitive" + "@" + "example.invalid",
            "veritrail_observation": {
                "schema_version": "0.1",
                "canonicalization_profile": "veritrail-json-c14n/1",
                "plan_digest": sealed_plan["seal"]["digest"],
                "observation_spec_digest": observation_spec_digest(spec),
                "request_seal_digest": digest_bytes(b"pc2-fixture-request"),
                "collection_session_id": "pc2-collection-001",
                "collector_role": "pc2-fixture-collector",
                "coverage": "COMPLETE",
                "normalization_semantics_version": "pc2-fixture-normalization/0.1",
                "facts_digest": digest_json(facts),
            },
        },
    }


def run_cli(arguments: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-I", "-m", "veritrail", *arguments],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise FreezeFailure(
            f"CLI failed ({completed.returncode}): {completed.stderr.strip()}"
        )
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise FreezeFailure("CLI did not emit one JSON result") from exc
    require(isinstance(value, dict), "CLI result must be an object")
    return value


def verify_bundle(bundle: Path, expected_verdict: str) -> dict[str, Any]:
    manifest_path = bundle / "acceptance-bundle-manifest.json"
    manifest = read_json(manifest_path)
    require(manifest.get("bundle_kind") == "ACCEPTANCE", "bundle kind drifted")
    declared = {entry["path"]: entry for entry in manifest["files"]}
    actual = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file()
    }
    require(
        actual == set(declared) | {"acceptance-bundle-manifest.json"},
        "bundle file set differs from its manifest",
    )
    for relative, entry in declared.items():
        content = (bundle / relative).read_bytes()
        require(len(content) == entry["size"], f"size mismatch for {relative}")
        require(digest_bytes(content) == entry["sha256"], f"digest mismatch for {relative}")

    forbidden_legacy = {
        "bundle-manifest.json",
        "evidence-manifest.json",
        "report.json",
        "sealed-plan.json",
    }
    require(not (actual & forbidden_legacy), "Acceptance bundle reused a legacy root filename")
    retained_text = b"\n".join(
        (bundle / relative).read_bytes() for relative in sorted(actual)
    )
    sensitive_marker = b"pc2-sensitive" + b"@" + b"example.invalid"
    require(sensitive_marker not in retained_text, "sensitive marker was retained")

    plan = read_json(bundle / "sealed-acceptance-plan.json")
    unsigned = {key: value for key, value in plan.items() if key != "seal"}
    require(plan["seal"]["digest"] == digest_json(unsigned), "Plan digest did not recompute")
    report = read_json(bundle / "acceptance-report.json")
    evidence_manifest = read_json(bundle / "acceptance-evidence-manifest.json")
    artifacts = []
    artifacts_by_type: dict[str, dict[str, Any]] = {}
    for entry in evidence_manifest["artifacts"]:
        content = (bundle / entry["path"]).read_bytes()
        require(len(content) == entry["size"], "Evidence size did not recompute")
        require(digest_bytes(content) == entry["sha256"], "Evidence SHA did not recompute")
        require(entry["redacted"] is True, "sensitive fixture was not marked redacted")
        require(entry["redacted_fields"] == 1, "unexpected redaction count")
        document = json.loads(content.decode("utf-8"))
        observation = document["metadata"]["veritrail_observation"]
        require(
            observation["facts_digest"] == digest_json(document["facts"]),
            "facts digest did not recompute",
        )
        artifact = import_evidence_document(document, entry["source_name"])
        require(artifact.sha256 == entry["sha256"], "Core Evidence identity drifted")
        artifacts.append(artifact)
        artifacts_by_type[entry["evidence_type"]] = entry

    recomputed = evaluate_acceptance(plan, artifacts, report["execution_status"])
    for field in (
        "execution_status",
        "verdict",
        "reasons",
        "evidence_bindings",
        "rule_results",
        "missing_evidence",
    ):
        require(report[field] == recomputed[field], f"report derivation drifted at {field}")
    require(report["verdict"] == expected_verdict, "unexpected Acceptance verdict")
    require(report["plan"]["sha256"] == plan["seal"]["digest"], "report Plan binding drifted")
    require(report["evidence"] == evidence_manifest["artifacts"], "Evidence manifest/report drifted")

    cross = next(item for item in report["rule_results"] if item["id"] == "same-visible-commit")
    require(cross["left"]["value"] == "candidate-001", "left operand value drifted")
    expected_right = "candidate-001" if expected_verdict == "PASS" else "other-visible-commit"
    require(cross["right"]["value"] == expected_right, "right operand value drifted")
    require(
        cross["left"]["evidence_sha256"] == artifacts_by_type["platform.api"]["sha256"],
        "left operand Evidence identity drifted",
    )
    require(
        cross["right"]["evidence_sha256"]
        == artifacts_by_type["platform.render"]["sha256"],
        "right operand Evidence identity drifted",
    )
    markdown = (bundle / "acceptance-report.md").read_text(encoding="utf-8")
    require(f"Verdict: `{expected_verdict}`" in markdown, "Markdown verdict drifted")
    require("same\\-visible\\-commit" in markdown, "Markdown omitted the cross-Evidence rule")
    require(
        expected_right.replace("-", "\\-") in markdown,
        "Markdown omitted the retained right operand",
    )
    return {
        "verdict": report["verdict"],
        "plan_sha256": plan["seal"]["digest"],
        "bundle_manifest_sha256": digest_bytes(manifest_path.read_bytes()),
        "evidence_sha256": sorted(entry["sha256"] for entry in evidence_manifest["artifacts"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded PC2 Acceptance Core freeze gate.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-source-root", type=Path)
    args = parser.parse_args()

    package_path = Path(veritrail.__file__).resolve()
    if args.expected_source_root is not None:
        source_package_root = (args.expected_source_root.resolve() / "src").resolve()
        require(
            not package_path.is_relative_to(source_package_root),
            "PC2 clean-install gate imported VeriTrail from the source checkout",
        )
    output = args.output.absolute()
    require(not output.exists(), "PC2 output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-pc2-", dir=output.parent))
    try:
        with tempfile.TemporaryDirectory(prefix="veritrail-pc2-input-") as temporary:
            inputs = Path(temporary)
            draft = inputs / "acceptance-plan.json"
            sealed = inputs / "sealed-acceptance-plan.json"
            write_json(draft, acceptance_plan())
            sealed_result = run_cli(
                ["acceptance-seal", "--plan", str(draft), "--output", str(sealed)],
                inputs,
            )
            require(sealed_result.get("command") == "acceptance-seal", "seal command drifted")
            plan = read_json(sealed)
            require(
                plan["seal"]["digest"]
                == digest_json({key: value for key, value in plan.items() if key != "seal"}),
                "sealed Plan failed independent digest verification",
            )

            cases = {
                "pass": {"api-spec": "candidate-001", "render-spec": "candidate-001"},
                "fail": {"api-spec": "candidate-001", "render-spec": "other-visible-commit"},
            }
            for case, observations in cases.items():
                evidence_paths = []
                for spec_id, commit_sha in observations.items():
                    evidence_path = inputs / f"{case}-{spec_id}.json"
                    write_json(evidence_path, evidence_document(plan, spec_id, commit_sha))
                    evidence_paths.append(evidence_path)
                command = [
                    "acceptance-evaluate",
                    "--plan",
                    str(sealed),
                    "--output",
                    str(stage / case),
                    "--acceptance-id",
                    f"pc2-{case}",
                ]
                for evidence_path in evidence_paths:
                    command.extend(["--evidence", str(evidence_path)])
                result = run_cli(command, inputs)
                require(result.get("verdict") == case.upper(), f"{case} CLI verdict drifted")

        positive = verify_bundle(stage / "pass", "PASS")
        negative = verify_bundle(stage / "fail", "FAIL")
        require(
            positive["plan_sha256"] == negative["plan_sha256"],
            "PASS and FAIL did not share one sealed Plan",
        )
        require(
            positive["evidence_sha256"] != negative["evidence_sha256"],
            "the single negative variable did not change Evidence identity",
        )
        write_json(
            stage / "pc2-summary.json",
            {
                "schema_version": "0.1",
                "status": "PASS",
                "boundary": "PC2_ACCEPTANCE_CORE_FREEZE_NOT_P1",
                "package_version": version("veritrail"),
                "package_origin": "installed-distribution",
                "cases": {"pass": positive, "fail": negative},
            },
        )
        os.replace(stage, output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise

    staging = [
        path.name
        for path in output.parent.iterdir()
        if path.is_dir() and path.name.startswith(".veritrail-pc2-")
    ]
    require(not staging, f"PC2 staging directories remain: {staging}")
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(output),
                "package": str(package_path),
                "boundary": "PC2_ACCEPTANCE_CORE_FREEZE_NOT_P1",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
