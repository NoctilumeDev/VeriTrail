from __future__ import annotations

from typing import Any

from veritrail.acceptance_plan import seal_acceptance_plan


TARGET_SHA = "a" * 40


def public_render_plan(
    coordinates: dict[str, Any] | None = None,
    *,
    projections: list[str] | None = None,
) -> dict[str, Any]:
    resolved_coordinates = coordinates or {
        "owner": "NoctilumeDev",
        "repository": "VeriTrail",
        "target_kind": "GITHUB_MARKDOWN_FILE",
        "target_commit_sha": TARGET_SHA,
        "repository_path": "README.md",
        "viewport_profile": "DESKTOP_1365X768",
    }
    resolved_projections = projections or [
        "content.rendered_text_signature",
        "content.scope",
        "navigation.identity",
    ]
    unsigned = {
        "plan_kind": "ACCEPTANCE",
        "schema_version": "0.1",
        "plan_id": "github-p2-fixture",
        "version": 1,
        "subject": {
            "id": "veritrail",
            "version": TARGET_SHA,
            "source_ref": "github:noctilumedev/veritrail",
        },
        "question": "Does retained public Render evidence satisfy this coordinate?",
        "governance": {
            "claim_owner_ref": "human:owner",
            "drafter_ref": "test:p2-fixture",
            "seal_authority_ref": "human:owner",
            "seal_decision": "CONFIRMED",
        },
        "observation_specs": [
            {
                "id": "github-public-render",
                "contract": {
                    "id": "github-public-render-request",
                    "version": "0.1",
                },
                "evidence_type": "platform.github.public-render",
                "coordinates": resolved_coordinates,
                "projections": resolved_projections,
                "canonicalization_profile": "veritrail-json-c14n/1",
            }
        ],
        "evidence_requirements": [
            {
                "id": "github-public-render-evidence",
                "observation_spec_id": "github-public-render",
                "cardinality": "EXACTLY_ONE",
            }
        ],
        "sufficiency_rules": [
            {
                "id": "coverage-complete",
                "left": {
                    "requirement_id": "github-public-render-evidence",
                    "path": "/metadata/veritrail_observation/coverage",
                },
                "operator": "eq",
                "right": "COMPLETE",
            }
        ],
        "integrity_rules": [],
        "assertions": [
            {
                "id": "declared-request-coordinate",
                "severity": "HARD",
                "left": {
                    "requirement_id": "github-public-render-evidence",
                    "path": "/facts/navigation/requested_url",
                },
                "operator": "exists",
            }
        ],
        "resource_budget": {"network_requests": 512, "max_elapsed_ms": 45000},
        "change_scope": {
            "level": "L3_SYSTEM",
            "owner": "github-evidence-plugin",
            "consumers": ["acceptance-core"],
        },
        "reproduction_steps": ["Run the bounded public Render collector."],
        "cleanup_steps": ["Remove the generated Evidence file."],
    }
    return seal_acceptance_plan(unsigned)
