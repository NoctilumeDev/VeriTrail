from __future__ import annotations

import argparse
import json
import os
import re
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

import veritrail
import veritrail_github
from veritrail.acceptance_plan import seal_acceptance_plan
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


CORE_VERSION = "0.12.2"
PLUGIN_VERSION = "0.1.0"
COLLECTION_ORDER = ("github-api", "github-public-render")


def require(condition: object, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def release_acceptance_plan(
    *,
    owner: str,
    repository: str,
    target_commit_sha: str,
    repository_path: str,
    literal_marker: str,
) -> dict[str, Any]:
    require(
        re.fullmatch(r"[0-9a-f]{40}", target_commit_sha) is not None,
        "target commit must be 40 lowercase hexadecimal characters",
    )
    requested_path = (
        f"/{owner}/{repository}/blob/{target_commit_sha}/{repository_path}"
    )
    return seal_acceptance_plan(
        {
            "plan_kind": "ACCEPTANCE",
            "schema_version": "0.1",
            "plan_id": "github-evidence-p4-real-release-candidate",
            "version": 1,
            "subject": {
                "id": repository,
                "version": target_commit_sha,
                "source_ref": f"github:{owner.lower()}/{repository.lower()}",
            },
            "question": (
                "Does the installed GitHub Evidence release candidate retain "
                "the predeclared exact public repository facts?"
            ),
            "governance": {
                "claim_owner_ref": "human:owner",
                "drafter_ref": "probe:p4-release-acceptance",
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
                        "owner": owner,
                        "repository": repository,
                        "target_commit_sha": target_commit_sha,
                        "branch": "main",
                    },
                    "projections": ["commit.identity"],
                    "canonicalization_profile": "veritrail-json-c14n/1",
                },
                {
                    "id": "github-public-render",
                    "contract": {
                        "id": "github-public-render-request",
                        "version": "0.1",
                    },
                    "evidence_type": "platform.github.public-render",
                    "coordinates": {
                        "owner": owner,
                        "repository": repository,
                        "target_kind": "GITHUB_MARKDOWN_FILE",
                        "target_commit_sha": target_commit_sha,
                        "repository_path": repository_path,
                        "viewport_profile": "DESKTOP_1365X768",
                        "literal_markers": [literal_marker],
                    },
                    "projections": [
                        "content.literal_markers",
                        "navigation.identity",
                    ],
                    "canonicalization_profile": "veritrail-json-c14n/1",
                },
            ],
            "evidence_requirements": [
                {
                    "id": "github-api-evidence",
                    "observation_spec_id": "github-api",
                    "cardinality": "EXACTLY_ONE",
                },
                {
                    "id": "github-render-evidence",
                    "observation_spec_id": "github-public-render",
                    "cardinality": "EXACTLY_ONE",
                },
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
                },
                {
                    "id": "render-coverage-complete",
                    "left": {
                        "requirement_id": "github-render-evidence",
                        "path": "/metadata/veritrail_observation/coverage",
                    },
                    "operator": "eq",
                    "right": "COMPLETE",
                },
            ],
            "integrity_rules": [
                {
                    "id": "same-collection-session",
                    "left": {
                        "requirement_id": "github-api-evidence",
                        "path": (
                            "/metadata/veritrail_observation/"
                            "collection_session_id"
                        ),
                    },
                    "operator": "eq",
                    "right": {
                        "requirement_id": "github-render-evidence",
                        "path": (
                            "/metadata/veritrail_observation/"
                            "collection_session_id"
                        ),
                    },
                },
                {
                    "id": "same-target-commit",
                    "left": {
                        "requirement_id": "github-api-evidence",
                        "path": "/facts/commit/sha",
                    },
                    "operator": "eq",
                    "right": {
                        "requirement_id": "github-render-evidence",
                        "path": (
                            "/facts/target/source_coordinates/target_commit_sha"
                        ),
                    },
                },
            ],
            "assertions": [
                {
                    "id": "sealed-exact-commit",
                    "severity": "HARD",
                    "left": {
                        "requirement_id": "github-api-evidence",
                        "path": "/facts/commit/sha",
                    },
                    "operator": "eq",
                    "right": target_commit_sha,
                },
                {
                    "id": "render-requested-url-retained",
                    "severity": "HARD",
                    "left": {
                        "requirement_id": "github-render-evidence",
                        "path": "/facts/navigation/requested_url/path",
                    },
                    "operator": "eq",
                    "right": requested_path,
                },
                {
                    "id": "readme-marker-retained",
                    "severity": "HARD",
                    "left": {
                        "requirement_id": "github-render-evidence",
                        "path": (
                            "/facts/content/window/stable_facts/"
                            "literal_markers/0/rendered_text_occurrences"
                        ),
                    },
                    "operator": "gte",
                    "right": 1,
                },
            ],
            "resource_budget": {
                "network_requests": 512,
                "max_elapsed_ms": 45000,
            },
            "change_scope": {
                "level": "L2_PUBLIC_DISTRIBUTION_CONTRACT",
                "owner": "github-evidence-plugin",
                "consumers": ["acceptance-core"],
            },
            "reproduction_steps": [
                "Install the candidate Core and GitHub Evidence wheels.",
                "Preinstall the matching Chromium for Playwright 1.62.0.",
                "Run this P4 real GitHub acceptance probe.",
            ],
            "cleanup_steps": [
                "Close the owned BrowserContext and Chromium process tree.",
                "Remove the generated candidate acceptance directory.",
            ],
        }
    )


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


def _observations_by_role(imported_evidence: tuple[Any, ...]) -> dict[str, Any]:
    by_role: dict[str, Any] = {}
    for artifact in imported_evidence:
        observation = artifact.document["metadata"]["veritrail_observation"]
        role = observation["collector_role"]
        require(role not in by_role, f"duplicate Evidence role: {role}")
        by_role[role] = artifact
    require(set(by_role) == set(COLLECTION_ORDER), "Evidence role set drifted")
    return by_role


def run(
    *,
    output: Path,
    owner: str,
    repository: str,
    target_commit_sha: str,
    repository_path: str,
    literal_marker: str,
) -> dict[str, Any]:
    require(not output.exists(), "P4 real acceptance output already exists")
    repository_root = Path(__file__).resolve().parents[1]
    for module, label in (
        (veritrail, "Core"),
        (veritrail_github, "GitHub Evidence plugin"),
    ):
        module_path = Path(module.__file__).resolve()
        require(
            not module_path.is_relative_to(repository_root),
            f"{label} was imported from the checkout instead of an installed artifact",
        )
    require(version("veritrail") == CORE_VERSION, "installed Core version drifted")
    require(
        version("veritrail-github-evidence") == PLUGIN_VERSION,
        "installed plugin version drifted",
    )

    plan = release_acceptance_plan(
        owner=owner,
        repository=repository,
        target_commit_sha=target_commit_sha,
        repository_path=repository_path,
        literal_marker=literal_marker,
    )
    api_request = derive_observation_request(plan, "github-api", "p4-real-api")
    render_request = derive_public_render_request(
        plan, "github-public-render", "p4-real-render"
    )
    output.mkdir(parents=True)
    result = _coordinator(os.environ.get("GITHUB_TOKEN") or None).collect_and_publish(
        plan,
        api_request,
        render_request,
        api_output_path=output / "github-api.json",
        render_output_path=output / "github-public-render.json",
    )
    require(tuple(result.collection_order) == COLLECTION_ORDER, "collection order drifted")
    for side in (result.api, result.render):
        require(side.state == "PUBLISHED", f"{side.collector_role} was not published")
        require(side.coverage == "COMPLETE", f"{side.collector_role} was not complete")

    handoff_path = output / "github-evidence-handoff.json"
    handoff = publish_handoff_manifest(handoff_path, result)
    imported = import_verified_handoff_evidence(handoff_path)
    require(len(imported) == 2, "handoff did not retain exactly two Evidence snapshots")
    by_role = _observations_by_role(imported)
    sessions = {
        artifact.document["metadata"]["veritrail_observation"][
            "collection_session_id"
        ]
        for artifact in imported
    }
    require(sessions == {result.collection_session_id}, "paired session identity drifted")

    api_artifact = by_role["github-api"]
    render_artifact = by_role["github-public-render"]
    require(
        api_artifact.document["facts"]["commit"]["sha"] == target_commit_sha,
        "API Evidence commit drifted",
    )
    require(
        render_artifact.document["facts"]["target"]["source_coordinates"][
            "target_commit_sha"
        ]
        == target_commit_sha,
        "Render Evidence commit drifted",
    )
    marker = render_artifact.document["facts"]["content"]["window"][
        "stable_facts"
    ]["literal_markers"]
    require(
        len(marker) == 1
        and marker[0]["literal"] == literal_marker
        and marker[0]["rendered_text_occurrences"] >= 1,
        "Render Evidence marker drifted",
    )

    report = create_acceptance_bundle_from_imported(
        plan=plan,
        imported_evidence=list(imported),
        output=output / "acceptance-bundle",
        acceptance_id="github-evidence-p4-real-release-candidate",
        execution_status="COMPLETED",
    )
    require(report["verdict"] == "PASS", "P4 real release acceptance did not PASS")
    require(
        all(item["status"] == "PASS" for item in report["rule_results"]),
        "P4 real release acceptance retained a non-PASS rule",
    )
    summary = {
        "schema_version": "0.1",
        "acceptance_kind": "P4_REAL_GITHUB_RELEASE_CANDIDATE",
        "target_commit_sha": target_commit_sha,
        "plan_digest": plan["seal"]["digest"],
        "collection_session_id": result.collection_session_id,
        "collection_order": list(COLLECTION_ORDER),
        "handoff_digest": handoff_manifest_digest(handoff),
        "api_evidence_sha256": api_artifact.sha256,
        "render_evidence_sha256": render_artifact.sha256,
        "verdict": report["verdict"],
        "report_sha256": sha256_json(report),
        "installed_versions": {
            "veritrail": CORE_VERSION,
            "veritrail-github-evidence": PLUGIN_VERSION,
        },
        "boundary": "RELEASE_CANDIDATE_NOT_PUBLIC_DOWNLOAD_EVIDENCE",
    }
    (output / "p4-real-github-summary.json").write_bytes(
        canonical_json_bytes(summary) + b"\n"
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the installed P4 GitHub Evidence candidate against one predeclared exact commit."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--owner", default="NoctilumeDev")
    parser.add_argument("--repository", default="VeriTrail")
    parser.add_argument("--target-commit", required=True)
    parser.add_argument("--repository-path", default="README.md")
    parser.add_argument("--literal-marker", default="VeriTrail")
    args = parser.parse_args(argv)
    summary = run(
        output=args.output.resolve(),
        owner=args.owner,
        repository=args.repository,
        target_commit_sha=args.target_commit,
        repository_path=args.repository_path,
        literal_marker=args.literal_marker,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
