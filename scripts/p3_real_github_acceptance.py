from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path
from typing import Any

from veritrail.acceptance_plan import verify_sealed_acceptance_plan
from veritrail.acceptance_reporting import create_acceptance_bundle_from_imported
from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail_github.collector import GitHubCollector
from veritrail_github.contracts import derive_observation_request
from veritrail_github.handoff import (
    import_verified_handoff_evidence,
    publish_handoff_manifest,
)
from veritrail_github.handoff_contracts import handoff_manifest_digest
from veritrail_github.paired_collection import PairedCollectionCoordinator
from veritrail_github.public_render_collector import PublicRenderCollector
from veritrail_github.public_render_contracts import derive_public_render_request
from veritrail_github.transport import UrllibTransport


EXPECTED_TARGET_SHA = "589bbad7261cceda1aa3a6412278a48473a9b1b7"
PLAN_FIXTURES = {
    "pass": "p3-acceptance-plan-pass.json",
    "fail": "p3-acceptance-plan-wrong-expectation.json",
}
EXPECTED_VERDICTS = {"pass": "PASS", "fail": "FAIL"}
EXPECTED_RENDER_PATH = (
    "/NoctilumeDev/VeriTrail/blob/"
    f"{EXPECTED_TARGET_SHA}/README.md"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"expected one JSON object: {path.name}")
    return value


def _load_presealed_plans(fixture_root: Path) -> dict[str, dict[str, Any]]:
    plans = {
        name: _read_json(fixture_root / filename)
        for name, filename in PLAN_FIXTURES.items()
    }
    for plan in plans.values():
        verify_sealed_acceptance_plan(plan)
        _require(
            plan["subject"]["version"] == EXPECTED_TARGET_SHA,
            "P3 real Plan targets an unexpected commit",
        )

    pass_semantics = copy.deepcopy(plans["pass"])
    fail_semantics = copy.deepcopy(plans["fail"])
    pass_semantics.pop("seal")
    fail_semantics.pop("seal")
    fail_semantics["version"] = pass_semantics["version"]
    fail_semantics["assertions"][0]["right"] = pass_semantics["assertions"][0][
        "right"
    ]
    _require(
        canonical_json_bytes(pass_semantics) == canonical_json_bytes(fail_semantics),
        "P3 real Plans differ by more than the presealed assertion expectation",
    )
    return plans


def _coordinator(token: str | None) -> PairedCollectionCoordinator:
    return PairedCollectionCoordinator(
        api_collector_factory=lambda session_factory: GitHubCollector(
            UrllibTransport(),
            token=token,
            session_id_factory=session_factory,
        ),
        render_collector_factory=lambda session_factory: PublicRenderCollector(
            session_id_factory=session_factory,
        ),
    )


def _observation_by_role(artifacts) -> dict[str, dict[str, Any]]:
    observations: dict[str, dict[str, Any]] = {}
    for artifact in artifacts:
        observation = artifact.document["metadata"]["veritrail_observation"]
        role = observation["collector_role"]
        _require(role not in observations, f"duplicate retained Evidence role: {role}")
        observations[role] = {
            "artifact": artifact,
            "observation": observation,
        }
    return observations


def _run_case(
    *,
    name: str,
    plan: dict[str, Any],
    output: Path,
    token: str | None,
) -> dict[str, Any]:
    case_root = output / name
    _require(not case_root.exists(), f"refusing to overwrite P3 real case: {name}")
    api_request = derive_observation_request(
        plan,
        "github-api",
        f"p3-real-{name}-api",
    )
    render_request = derive_public_render_request(
        plan,
        "github-public-render",
        f"p3-real-{name}-render",
    )
    result = _coordinator(token).collect_and_publish(
        plan,
        api_request,
        render_request,
        api_output_path=case_root / "github-api.json",
        render_output_path=case_root / "github-public-render.json",
    )
    for side in (result.api, result.render):
        _require(side.state == "PUBLISHED", f"{name} {side.collector_role}: {side}")
        _require(
            side.coverage == "COMPLETE",
            f"{name} {side.collector_role} coverage is not COMPLETE",
        )

    handoff_path = case_root / "github-evidence-handoff.json"
    handoff = publish_handoff_manifest(handoff_path, result)
    artifacts = import_verified_handoff_evidence(handoff_path)
    _require(len(artifacts) == 2, f"{name} did not retain two Evidence snapshots")
    by_role = _observation_by_role(artifacts)
    _require(
        set(by_role) == {"github-api", "github-public-render"},
        f"{name} retained unexpected collector roles",
    )
    sessions = {
        item["observation"]["collection_session_id"] for item in by_role.values()
    }
    _require(
        sessions == {result.collection_session_id},
        f"{name} Evidence did not retain the paired collection session",
    )
    _require(
        tuple(result.collection_order) == ("github-api", "github-public-render"),
        f"{name} did not retain the fixed P1 to P2 collection order",
    )
    _require(
        {
            item["observation"]["plan_digest"] for item in by_role.values()
        }
        == {plan["seal"]["digest"]},
        f"{name} Evidence did not retain the sealed Plan identity",
    )
    _require(
        len(
            {
                item["observation"]["request_seal_digest"]
                for item in by_role.values()
            }
        )
        == 2,
        f"{name} P1 and P2 Evidence collapsed separate request identities",
    )
    api_artifact = by_role["github-api"]["artifact"]
    render_artifact = by_role["github-public-render"]["artifact"]
    api_collection = api_artifact.document["metadata"]["github_collection"]
    render_collection = render_artifact.document["metadata"][
        "github_public_render_collection"
    ]
    _require(
        api_collection["atomic_snapshot_claimed"] is False
        and render_collection["atomic_snapshot_claimed"] is False,
        f"{name} Evidence overstated serial correlation as an atomic snapshot",
    )
    _require(
        api_collection["collection_completed_at"]
        <= render_collection["collection_started_at"],
        f"{name} P1 and P2 collection windows were not serial",
    )
    _require(
        api_artifact.document["facts"]["commit"]["sha"] == EXPECTED_TARGET_SHA,
        f"{name} API Evidence observed an unexpected commit",
    )
    _require(
        render_artifact.document["facts"]["target"]["source_coordinates"][
            "target_commit_sha"
        ]
        == EXPECTED_TARGET_SHA,
        f"{name} Render Evidence observed an unexpected commit",
    )
    _require(
        render_artifact.document["facts"]["navigation"]["requested_url"]["path"]
        == EXPECTED_RENDER_PATH,
        f"{name} Render Evidence did not retain the exact requested URL",
    )
    markers = render_artifact.document["facts"]["content"]["window"][
        "stable_facts"
    ]["literal_markers"]
    _require(
        len(markers) == 1
        and markers[0]["literal"] == "VeriTrail"
        and markers[0]["rendered_text_occurrences"] >= 1,
        f"{name} Render Evidence did not retain the predeclared README marker",
    )

    report = create_acceptance_bundle_from_imported(
        plan=plan,
        imported_evidence=list(artifacts),
        output=case_root / "acceptance-bundle",
        acceptance_id=f"p3-real-github-{name}",
        execution_status="COMPLETED",
    )
    expected = EXPECTED_VERDICTS[name]
    _require(report["verdict"] == expected, f"{name} expected {expected}: {report}")
    failed_rules = {
        (rule["category"], rule["id"])
        for rule in report["rule_results"]
        if rule["status"] != "PASS"
    }
    expected_failed_rules = (
        set() if name == "pass" else {("ASSERTION", "sealed-exact-commit")}
    )
    _require(
        failed_rules == expected_failed_rules,
        f"{name} did not preserve the single-variable Verdict model: "
        f"{sorted(failed_rules)}",
    )
    return {
        "plan_digest": plan["seal"]["digest"],
        "collection_session_id": result.collection_session_id,
        "collection_order": list(result.collection_order),
        "handoff_digest": handoff_manifest_digest(handoff),
        "api_evidence_sha256": api_artifact.sha256,
        "render_evidence_sha256": render_artifact.sha256,
        "verdict": report["verdict"],
        "report_sha256": sha256_json(report),
    }


def run(output: Path, fixture_root: Path) -> dict[str, Any]:
    _require(not output.exists(), "P3 real GitHub output already exists")
    plans = _load_presealed_plans(fixture_root)
    output.mkdir(parents=True)
    token = os.environ.get("GITHUB_TOKEN") or None
    results = {
        name: _run_case(
            name=name,
            plan=plans[name],
            output=output,
            token=token,
        )
        for name in ("pass", "fail")
    }
    summary = {
        "schema_version": "0.1",
        "acceptance_kind": "P3_REAL_GITHUB_PASS_FAIL",
        "target_commit_sha": EXPECTED_TARGET_SHA,
        "trust_boundary": "ONE_GITHUB_TRUST_DOMAIN_TWO_OBSERVATION_SURFACES",
        "temporal_semantics": "SERIAL_CORRELATION_WINDOW_NOT_ATOMIC_SNAPSHOT",
        "cases": results,
    }
    (output / "p3-real-github-summary.json").write_bytes(
        canonical_json_bytes(summary) + b"\n"
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="P3 real GitHub PASS/FAIL acceptance")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=(
            repository_root
            / "plugins"
            / "github-evidence"
            / "tests"
            / "fixtures"
        ),
    )
    args = parser.parse_args(argv)
    summary = run(args.output, args.fixtures)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
