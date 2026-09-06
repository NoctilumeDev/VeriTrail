from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from veritrail.acceptance_plan import (
    observation_spec_digest,
    seal_acceptance_plan,
    verify_sealed_acceptance_plan,
)
from veritrail.canonical import canonical_json_bytes, sha256_json
from veritrail.evidence import import_evidence_document

from veritrail_github.handoff import publish_handoff_manifest
from veritrail_github.paired_collection import (
    PairedCollectionResult,
    PairedSideOutcome,
)
from veritrail_github.publisher import publish_evidence
from veritrail_github.reference_lab import create_reference_acceptance_bundle


TARGET_SHA = "589bbad7261cceda1aa3a6412278a48473a9b1b7"
WRONG_SHA = "0" * 40


def _plan(*, expected_sha: str = TARGET_SHA, version: int = 1) -> dict[str, Any]:
    return seal_acceptance_plan(
        {
            "plan_kind": "ACCEPTANCE",
            "schema_version": "0.1",
            "plan_id": "github-p3-synthetic-handoff",
            "version": version,
            "subject": {
                "id": "veritrail",
                "version": TARGET_SHA,
                "source_ref": "github:noctilumedev/veritrail",
            },
            "question": "Do the retained API and Render observations satisfy the sealed claim?",
            "governance": {
                "claim_owner_ref": "human:owner",
                "drafter_ref": "fixture:p3-reference-lab",
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
                },
                {
                    "id": "github-public-render",
                    "contract": {
                        "id": "github-public-render-request",
                        "version": "0.1",
                    },
                    "evidence_type": "platform.github.public-render",
                    "coordinates": {
                        "owner": "NoctilumeDev",
                        "repository": "VeriTrail",
                        "target_kind": "GITHUB_MARKDOWN_FILE",
                        "target_commit_sha": TARGET_SHA,
                        "repository_path": "README.md",
                        "viewport_profile": "DESKTOP_1365X768",
                        "literal_markers": ["VeriTrail"],
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
                        "path": "/metadata/veritrail_observation/collection_session_id",
                    },
                    "operator": "eq",
                    "right": {
                        "requirement_id": "github-render-evidence",
                        "path": "/metadata/veritrail_observation/collection_session_id",
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
                        "path": "/facts/target/source_coordinates/target_commit_sha",
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
                    "right": expected_sha,
                },
                {
                    "id": "render-requested-url-retained",
                    "severity": "HARD",
                    "left": {
                        "requirement_id": "github-render-evidence",
                        "path": "/facts/navigation/requested_url/path",
                    },
                    "operator": "eq",
                    "right": (
                        "/NoctilumeDev/VeriTrail/blob/"
                        f"{TARGET_SHA}/README.md"
                    ),
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
                "level": "L3_SYSTEM",
                "owner": "github-evidence-plugin",
                "consumers": ["acceptance-core"],
            },
            "reproduction_steps": ["Run the bounded P3 synthetic reference lab."],
            "cleanup_steps": ["Remove generated Evidence, handoff, and Bundle files."],
        }
    )


def _artifact(
    plan: dict[str, Any],
    spec_id: str,
    role: str,
    *,
    session_id: str = "p3-session-001",
    coverage: str = "COMPLETE",
):
    spec = next(item for item in plan["observation_specs"] if item["id"] == spec_id)
    if role == "github-api":
        facts = {"commit": {"sha": TARGET_SHA}}
    else:
        facts = {
            "target": {
                "source_coordinates": {"target_commit_sha": TARGET_SHA},
            },
            "navigation": {
                "requested_url": {
                    "path": (
                        "/NoctilumeDev/VeriTrail/blob/"
                        f"{TARGET_SHA}/README.md"
                    )
                }
            },
            "content": {
                "window": {
                    "stable_facts": {
                        "literal_markers": [
                            {
                                "literal": "VeriTrail",
                                "rendered_text_occurrences": 1,
                            }
                        ]
                    }
                }
            },
        }
    document = {
        "schema_version": "0.1",
        "evidence_type": spec["evidence_type"],
        "source": "p3-synthetic-reference/0.1",
        "captured_at": "2026-09-06T00:00:00Z",
        "facts": facts,
        "metadata": {
            "veritrail_observation": {
                "schema_version": "0.1",
                "canonicalization_profile": "veritrail-json-c14n/1",
                "plan_digest": plan["seal"]["digest"],
                "observation_spec_digest": observation_spec_digest(spec),
                "request_seal_digest": sha256_json(
                    {"fixture": "p3", "role": role, "plan": plan["seal"]["digest"]}
                ),
                "collection_session_id": session_id,
                "collector_role": role,
                "coverage": coverage,
                "normalization_semantics_version": "p3-synthetic/0.1",
                "facts_digest": sha256_json(facts),
            }
        },
    }
    return import_evidence_document(document, f"{role}.json")


def _published(role: str, path: Path, digest: str, coverage: str) -> PairedSideOutcome:
    return PairedSideOutcome(
        collector_role=role,
        requested_output_path=path,
        artifact_path=path,
        artifact_sha256=digest,
        coverage=coverage,
        state="PUBLISHED",
        error_code=None,
    )


def _missing(role: str, path: Path) -> PairedSideOutcome:
    return PairedSideOutcome(
        collector_role=role,
        requested_output_path=path,
        artifact_path=None,
        artifact_sha256=None,
        coverage=None,
        state="MISSING",
        error_code="COLLECTION_ERROR",
    )


class ReferenceLabTests(unittest.TestCase):
    def _run(
        self,
        root: Path,
        plan: dict[str, Any],
        *,
        api_session: str = "p3-session-001",
        render_session: str = "p3-session-001",
        api_coverage: str = "COMPLETE",
        render_coverage: str = "COMPLETE",
        render_missing: bool = False,
        execution_status: str = "COMPLETED",
        name: str = "case",
    ) -> dict[str, Any]:
        api = _artifact(
            plan,
            "github-api",
            "github-api",
            session_id=api_session,
            coverage=api_coverage,
        )
        render = _artifact(
            plan,
            "github-public-render",
            "github-public-render",
            session_id=render_session,
            coverage=render_coverage,
        )
        api_path = root / f"{name}-api.json"
        render_path = root / f"{name}-render.json"
        publish_evidence(api_path, api)
        api_outcome = _published("github-api", api_path, api.sha256, api_coverage)
        if render_missing:
            render_outcome = _missing("github-public-render", render_path)
        else:
            publish_evidence(render_path, render)
            render_outcome = _published(
                "github-public-render",
                render_path,
                render.sha256,
                render_coverage,
            )
        result = PairedCollectionResult(
            collection_session_id="outcome-provenance-only",
            collection_order=("github-api", "github-public-render"),
            api=api_outcome,
            render=render_outcome,
        )
        handoff = root / f"{name}-handoff.json"
        publish_handoff_manifest(handoff, result)
        bundle = root / f"{name}-bundle"
        report = create_reference_acceptance_bundle(
            plan=plan,
            handoff_manifest_path=handoff,
            output=bundle,
            acceptance_id=f"p3-{name}",
            execution_status=execution_status,
        )
        retained = json.loads(
            (bundle / "acceptance-report.json").read_text(encoding="utf-8")
        )
        self.assertEqual(report, retained)
        return report

    def test_presealed_plans_and_synthetic_handoff_produce_pass_and_fail(self) -> None:
        pass_plan = _plan()
        fail_plan = _plan(expected_sha=WRONG_SHA, version=2)
        verify_sealed_acceptance_plan(pass_plan)
        verify_sealed_acceptance_plan(fail_plan)
        self.assertNotEqual(pass_plan["seal"]["digest"], fail_plan["seal"]["digest"])
        pass_semantics = copy.deepcopy(pass_plan)
        fail_semantics = copy.deepcopy(fail_plan)
        pass_semantics.pop("seal")
        fail_semantics.pop("seal")
        fail_semantics["version"] = pass_semantics["version"]
        fail_semantics["assertions"][0]["right"] = pass_semantics["assertions"][0][
            "right"
        ]
        self.assertEqual(pass_semantics, fail_semantics)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual("PASS", self._run(root, pass_plan, name="pass")["verdict"])
            self.assertEqual("FAIL", self._run(root, fail_plan, name="fail")["verdict"])

    def test_decisive_false_beats_unrelated_missing_render(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = self._run(
                Path(directory),
                _plan(expected_sha=WRONG_SHA, version=2),
                render_missing=True,
                name="fail-with-missing-render",
            )
        self.assertEqual("FAIL", report["verdict"])

    def test_cross_session_is_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = self._run(
                Path(directory),
                _plan(),
                api_session="p3-session-a",
                render_session="p3-session-b",
                name="cross-session",
            )
        self.assertEqual("INCONCLUSIVE", report["verdict"])

    def test_integrity_false_beats_decisive_false(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = self._run(
                Path(directory),
                _plan(expected_sha=WRONG_SHA, version=2),
                api_session="p3-session-a",
                render_session="p3-session-b",
                name="integrity-before-fail",
            )
        self.assertEqual("INCONCLUSIVE", report["verdict"])
        statuses = {item["id"]: item["status"] for item in report["rule_results"]}
        self.assertEqual("FAIL", statuses["same-collection-session"])
        self.assertEqual("FAIL", statuses["sealed-exact-commit"])

    def test_missing_partial_error_and_running_are_pending(self) -> None:
        cases = (
            ("missing", {"render_missing": True}),
            ("partial", {"render_coverage": "PARTIAL"}),
            ("error", {"render_coverage": "ERROR"}),
            ("running", {"execution_status": "RUNNING"}),
        )
        for name, options in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                report = self._run(
                    Path(directory),
                    _plan(),
                    name=name,
                    **options,
                )
                self.assertEqual("PENDING", report["verdict"])

    def test_committed_example_plans_are_the_exact_presealed_vectors(self) -> None:
        fixture_root = Path(__file__).parent / "fixtures"
        expected = (
            ("p3-acceptance-plan-pass.json", _plan()),
            (
                "p3-acceptance-plan-wrong-expectation.json",
                _plan(expected_sha=WRONG_SHA, version=2),
            ),
        )
        for filename, generated in expected:
            with self.subTest(filename=filename):
                retained = json.loads(
                    (fixture_root / filename).read_text(encoding="utf-8")
                )
                verify_sealed_acceptance_plan(retained)
                self.assertEqual(canonical_json_bytes(generated), canonical_json_bytes(retained))


if __name__ == "__main__":
    unittest.main()
