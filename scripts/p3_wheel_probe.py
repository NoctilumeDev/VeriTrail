from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any


TARGET_SHA = "589bbad7261cceda1aa3a6412278a48473a9b1b7"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _plan() -> dict[str, Any]:
    from veritrail.acceptance_plan import seal_acceptance_plan

    return seal_acceptance_plan(
        {
            "plan_kind": "ACCEPTANCE",
            "schema_version": "0.1",
            "plan_id": "p3-wheel-only-probe",
            "version": 1,
            "subject": {
                "id": "veritrail",
                "version": TARGET_SHA,
                "source_ref": "wheel-only:p3",
            },
            "question": "Does the retained synthetic API fact satisfy this wheel probe?",
            "governance": {
                "claim_owner_ref": "human:owner",
                "drafter_ref": "probe:p3-wheel-only",
                "seal_authority_ref": "human:owner",
                "seal_decision": "CONFIRMED",
            },
            "observation_specs": [
                {
                    "id": "github-api",
                    "contract": {
                        "id": "github-observation-request",
                        "version": "0.1",
                    },
                    "evidence_type": "platform.github.api.snapshot",
                    "coordinates": {
                        "owner": "NoctilumeDev",
                        "repository": "VeriTrail",
                        "target_commit_sha": TARGET_SHA,
                        "branch": "main",
                    },
                    "projections": ["commit.identity"],
                    "canonicalization_profile": "veritrail-json-c14n/1",
                }
            ],
            "evidence_requirements": [
                {
                    "id": "github-api-evidence",
                    "observation_spec_id": "github-api",
                    "cardinality": "EXACTLY_ONE",
                }
            ],
            "sufficiency_rules": [
                {
                    "id": "api-coverage-complete",
                    "left": {
                        "requirement_id": "github-api-evidence",
                        "path": "/metadata/veritrail_observation/coverage",
                    },
                    "operator": "eq",
                    "right": "COMPLETE",
                }
            ],
            "integrity_rules": [],
            "assertions": [
                {
                    "id": "exact-commit",
                    "severity": "HARD",
                    "left": {
                        "requirement_id": "github-api-evidence",
                        "path": "/facts/commit/sha",
                    },
                    "operator": "eq",
                    "right": TARGET_SHA,
                }
            ],
            "resource_budget": {},
            "change_scope": {
                "level": "L2_CONTRACT",
                "owner": "github-evidence-plugin",
                "consumers": ["acceptance-core"],
            },
            "reproduction_steps": ["Run the checkout-free P3 wheel probe."],
            "cleanup_steps": ["Remove the temporary probe directory."],
        }
    )


def prepare(output: Path) -> None:
    from importlib.util import find_spec

    from veritrail.acceptance_plan import observation_spec_digest
    from veritrail.canonical import sha256_json
    from veritrail.evidence import import_evidence_document
    from veritrail_github.handoff import publish_handoff_manifest
    from veritrail_github.publisher import publish_evidence
    from veritrail_github.reference_lab import create_reference_acceptance_bundle

    _require(find_spec("playwright") is None, "base P3 wheel probe found Playwright")
    _require(not output.exists(), "P3 wheel probe output already exists")
    output.mkdir(parents=True)
    plan = _plan()
    spec = plan["observation_specs"][0]
    facts = {"commit": {"sha": TARGET_SHA}}
    artifact = import_evidence_document(
        {
            "schema_version": "0.1",
            "evidence_type": spec["evidence_type"],
            "source": "wheel-only:p3",
            "captured_at": "2026-09-06T00:00:00Z",
            "facts": facts,
            "metadata": {
                "veritrail_observation": {
                    "schema_version": "0.1",
                    "canonicalization_profile": "veritrail-json-c14n/1",
                    "plan_digest": plan["seal"]["digest"],
                    "observation_spec_digest": observation_spec_digest(spec),
                    "request_seal_digest": sha256_json({"probe": "p3-wheel-only"}),
                    "collection_session_id": "p3-wheel-only-session",
                    "collector_role": "github-api",
                    "coverage": "COMPLETE",
                    "normalization_semantics_version": "p3-wheel-only/0.1",
                    "facts_digest": sha256_json(facts),
                }
            },
        },
        "p3-api.json",
    )
    evidence_path = output / "p3-api.json"
    publish_evidence(evidence_path, artifact)
    missing_render = output / "p3-render.json"
    result = SimpleNamespace(
        collection_order=("github-api", "github-public-render"),
        api=SimpleNamespace(
            collector_role="github-api",
            artifact_path=evidence_path,
            artifact_sha256=artifact.sha256,
            state="PUBLISHED",
            error_code=None,
        ),
        render=SimpleNamespace(
            collector_role="github-public-render",
            artifact_path=None,
            artifact_sha256=None,
            state="MISSING",
            error_code="COLLECTION_ERROR",
        ),
    )
    handoff_path = output / "p3-handoff.json"
    publish_handoff_manifest(handoff_path, result)
    report = create_reference_acceptance_bundle(
        plan=plan,
        handoff_manifest_path=handoff_path,
        output=output / "p3-bundle",
        acceptance_id="p3-wheel-only",
        execution_status="COMPLETED",
    )
    _require(report["verdict"] == "PASS", "P3 wheel probe did not produce PASS")
    _require(not missing_render.exists(), "P3 wheel probe invented missing Evidence")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify(output: Path) -> None:
    from importlib.util import find_spec

    from veritrail.acceptance_evaluation import evaluate_acceptance
    from veritrail.acceptance_plan import verify_sealed_acceptance_plan
    from veritrail.evidence import import_evidence_document

    _require(find_spec("veritrail_github") is None, "GitHub plugin remains installed")
    bundle = output / "p3-bundle"
    manifest = _read_json(bundle / "acceptance-bundle-manifest.json")
    declared = {item["path"]: item for item in manifest["files"]}
    actual = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file()
    }
    _require(
        actual == set(declared) | {"acceptance-bundle-manifest.json"},
        "P3 Bundle file set drifted after plugin uninstall",
    )
    for relative, item in declared.items():
        content = (bundle / relative).read_bytes()
        _require(len(content) == item["size"], f"P3 Bundle size drifted: {relative}")
        _require(
            hashlib.sha256(content).hexdigest() == item["sha256"],
            f"P3 Bundle digest drifted: {relative}",
        )

    plan = _read_json(bundle / "sealed-acceptance-plan.json")
    verify_sealed_acceptance_plan(plan)
    evidence_manifest = _read_json(bundle / "acceptance-evidence-manifest.json")
    artifacts = []
    for entry in evidence_manifest["artifacts"]:
        document = _read_json(bundle / entry["path"])
        artifact = import_evidence_document(document, entry["source_name"])
        _require(artifact.sha256 == entry["sha256"], "retained Evidence digest drifted")
        artifacts.append(artifact)
    report = _read_json(bundle / "acceptance-report.json")
    recomputed = evaluate_acceptance(plan, artifacts, report["execution_status"])
    for field in (
        "verdict",
        "reasons",
        "evidence_bindings",
        "rule_results",
        "missing_evidence",
    ):
        _require(report[field] == recomputed[field], f"P3 report drifted at {field}")
    _require(report["verdict"] == "PASS", "P3 retained Bundle no longer recomputes PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Checkout-free P3 wheel boundary probe")
    parser.add_argument("mode", choices=("prepare", "verify"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.mode == "prepare":
        prepare(args.output)
    else:
        verify(args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
