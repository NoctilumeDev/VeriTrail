from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_bytes
from veritrail.acceptance_plan import observation_spec_digest
from veritrail.evidence import ImportedEvidence
from veritrail.evidence import import_evidence_document
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile

ROOT = Path(__file__).resolve().parents[1]


def example_plan() -> dict[str, Any]:
    with (ROOT / "examples" / "minimal" / "plan.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sealed_example_plan() -> dict[str, Any]:
    return seal_plan(example_plan())


def preflight_plan(profile: str = "proceed") -> dict[str, Any]:
    filename = {
        "proceed": "plan-proceed.json",
        "stop-escalation": "plan-stop-escalation.json",
        "abort": "plan-abort.json",
    }[profile]
    with (ROOT / "examples" / "preflight" / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def browser_plan() -> dict[str, Any]:
    with (ROOT / "examples" / "browser" / "plan.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def orchestration_plan() -> dict[str, Any]:
    with (ROOT / "examples" / "orchestration" / "plan.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return json.load(handle)


def command_plan() -> dict[str, Any]:
    plan = orchestration_plan()
    plan["schema_version"] = "0.5"
    for variable in plan["variables"]:
        if variable["name"] == "target_lifecycle_mode":
            variable["role"] = "CONTROLLED"
    plan["variables"].append(
        {
            "name": "pre_target_command_mode",
            "role": "PRIMARY",
            "value": "veritrail_managed_trusted_process_oneshot",
            "source": "sealed-plan",
        }
    )
    plan["required_evidence"].append("runtime.command")
    plan["assertions"].append(
        {
            "id": "command-exit-accepted",
            "severity": "HARD",
            "evidence_type": "runtime.command",
            "path": "/facts/exit_expected",
            "operator": "eq",
            "expected": True,
        }
    )
    plan["command"] = {
        "adapter": "TRUSTED_PROCESS_ONESHOT",
        "command_id": "python-unit-check",
        "purpose": "run the sealed Python unit-test entry point",
        "project_profile_id": "veritrail-self-check",
        "tool_binding": "python",
        "arguments": [
            {"literal": "-m"},
            {"literal": "unittest"},
            {"literal": "discover"},
            {"literal": "-s"},
            {"literal": "tests"},
        ],
        "working_directory": ".",
        "environment": {
            "inherit": ["SYSTEMROOT", "WINDIR"],
            "set": {"PYTHONDONTWRITEBYTECODE": "1"},
        },
        "stdin": "CLOSED",
        "timeout_ms": 300000,
        "descendant_exit_grace_ms": 2000,
        "expected_exit_codes": [0],
        "max_stdout_bytes": 1048576,
        "max_stderr_bytes": 1048576,
        "max_processes": 16,
        "write_policy": "RUN_WORK_ONLY_DETECT_SUBJECT_CHANGES",
        "subject_watch_roots": ["src", "tests"],
        "max_watch_files": 2000,
        "max_watch_total_bytes": 67108864,
        "network_policy": "NOT_REQUIRED_NOT_ENFORCED",
    }
    return plan


def bootstrap_profile() -> dict[str, Any]:
    readiness = {
        "adapter": "HTTP_GET_LOOPBACK_OWNED_PID",
        "path": "/health",
        "expected_status": 200,
        "attempt_timeout_ms": 500,
        "total_timeout_ms": 10000,
        "interval_ms": 100,
        "consecutive_successes": 2,
        "max_response_bytes": 4096,
    }
    limits = {
        "max_stdout_bytes": 262144,
        "max_stderr_bytes": 262144,
        "max_processes": 8,
        "max_job_memory_mb": 512,
    }
    shutdown = {
        "adapter": "JOB_TERMINATE_AFTER_CAPTURE",
        "process_release_timeout_ms": 5000,
        "port_release_timeout_ms": 5000,
        "reader_shutdown_timeout_ms": 5000,
    }
    environment = {
        "inherit": ["SYSTEMROOT", "WINDIR"],
        "set": {"PYTHONDONTWRITEBYTECODE": "1"},
    }
    return {
        "schema_version": "0.1",
        "profile_id": "two-node-python",
        "version": 1,
        "platform": "WINDOWS_11",
        "cold_state": "C1_PROCESS_COLD",
        "nodes": [
            {
                "node_id": "dependency",
                "role": "DEPENDENCY",
                "adapter": "TRUSTED_PROCESS_SERVICE",
                "depends_on": [],
                "tool_binding": "python-dependency",
                "arguments": [
                    {"literal": "-m"},
                    {"literal": "dependency_service"},
                    {"node_port": "dependency"},
                    {"run_work_path": ["dependency"]},
                ],
                "working_directory": ".",
                "environment": copy.deepcopy(environment),
                "port": 18771,
                "readiness": copy.deepcopy(readiness),
                "limits": copy.deepcopy(limits),
                "shutdown": copy.deepcopy(shutdown),
            },
            {
                "node_id": "application",
                "role": "APPLICATION",
                "adapter": "TRUSTED_PROCESS_SERVICE",
                "depends_on": ["dependency"],
                "tool_binding": "python-application",
                "arguments": [
                    {"literal": "-m"},
                    {"literal": "application_service"},
                    {"node_port": "application"},
                    {"node_origin": "dependency"},
                    {"run_work_path": ["application"]},
                ],
                "working_directory": ".",
                "environment": copy.deepcopy(environment),
                "port": 18772,
                "readiness": copy.deepcopy(readiness),
                "limits": copy.deepcopy(limits),
                "shutdown": copy.deepcopy(shutdown),
            },
        ],
        "start_order": ["dependency", "application"],
        "teardown_order": ["application", "dependency"],
        "application_node_id": "application",
        "subject_watch_roots": ["src", "tests"],
        "max_watch_files": 2000,
        "max_watch_total_bytes": 67108864,
        "lifecycle_timeout_ms": 120000,
    }


def sealed_bootstrap_profile() -> dict[str, Any]:
    return seal_project_profile(bootstrap_profile())


def single_bootstrap_profile() -> dict[str, Any]:
    profile = bootstrap_profile()
    application = copy.deepcopy(profile["nodes"][1])
    application["depends_on"] = []
    application["arguments"] = [
        {"literal": "-m"},
        {"literal": "application_service"},
        {"node_port": "application"},
        {"run_work_path": ["application"]},
    ]
    application["port"] = 18774
    profile.update(
        {
            "schema_version": "0.2",
            "topology": "SINGLE_APPLICATION",
            "profile_id": "single-application-python",
            "nodes": [application],
            "start_order": ["application"],
            "teardown_order": ["application"],
        }
    )
    return profile


def sealed_single_bootstrap_profile() -> dict[str, Any]:
    return seal_project_profile(single_bootstrap_profile())


def bootstrap_plan(profile: dict[str, Any] | None = None) -> dict[str, Any]:
    sealed_profile = sealed_bootstrap_profile() if profile is None else profile
    plan = orchestration_plan()
    plan["schema_version"] = "0.6"
    plan.pop("target")
    for variable in plan["variables"]:
        if variable["role"] == "PRIMARY":
            variable["role"] = "CONTROLLED"
    plan["variables"].append(
        {
            "name": "project_bootstrap_mode",
            "role": "PRIMARY",
            "value": "veritrail_managed_windows_c1_two_node_services",
            "source": "sealed-plan",
        }
    )
    plan["required_evidence"] = [
        evidence
        for evidence in plan["required_evidence"]
        if evidence != "runtime.orchestration"
    ]
    plan["required_evidence"].append("runtime.bootstrap")
    plan["assertions"] = [
        assertion
        for assertion in plan["assertions"]
        if assertion["evidence_type"] != "runtime.orchestration"
    ]
    plan["assertions"].append(
        {
            "id": "bootstrap-services-ready",
            "severity": "HARD",
            "evidence_type": "runtime.bootstrap",
            "path": "/facts/services_ready",
            "operator": "eq",
            "expected": True,
        }
    )
    plan["assertions"].append(
        {
            "id": "bootstrap-cleanup-complete",
            "severity": "HARD",
            "evidence_type": "runtime.bootstrap",
            "path": "/facts/cleanup_complete",
            "operator": "eq",
            "expected": True,
        }
    )
    plan["preflight"]["ports"] = [
        {"port": 18771, "expected": "FREE"},
        {"port": 18772, "expected": "FREE"},
    ]
    application_origin = "http://127.0.0.1:18772"
    plan["browser"]["start_url"] = f"{application_origin}/"
    plan["browser"]["allowed_origins"] = [application_origin]
    plan["browser"]["screenshot_safety"] = "UNREDACTED_OPERATOR_ACKNOWLEDGED"
    plan["browser"]["max_job_memory_mb"] = 1024
    for step in plan["browser"]["steps"]:
        if step["action"] == "goto":
            step["url"] = f"{application_origin}/"
    plan["bootstrap_profile"] = {
        "profile_id": sealed_profile["profile_id"],
        "profile_version": sealed_profile["version"],
        "profile_sha256": sealed_profile["seal"]["digest"],
    }
    return plan


def single_bootstrap_plan(profile: dict[str, Any] | None = None) -> dict[str, Any]:
    sealed_profile = sealed_single_bootstrap_profile() if profile is None else profile
    plan = bootstrap_plan(sealed_profile)
    plan["schema_version"] = "0.7"
    primary = next(item for item in plan["variables"] if item["role"] == "PRIMARY")
    primary["name"] = "project_bootstrap_topology"
    primary["value"] = "veritrail_managed_windows_c1_single_application"
    plan["preflight"]["ports"] = [{"port": 18774, "expected": "FREE"}]
    application_origin = "http://127.0.0.1:18774"
    plan["browser"]["start_url"] = f"{application_origin}/"
    plan["browser"]["allowed_origins"] = [application_origin]
    for step in plan["browser"]["steps"]:
        if step["action"] == "goto":
            step["url"] = f"{application_origin}/"
    return plan


def artifact(
    *,
    suite_passed: bool = True,
    failures: int = 0,
    observed_variables: dict[str, Any] | None = None,
) -> ImportedEvidence:
    document = {
        "schema_version": "0.1",
        "evidence_type": "automated.test-summary",
        "source": "unit-test",
        "captured_at": "2026-08-09T00:00:00Z",
        "facts": {
            "suite_passed": suite_passed,
            "failures": failures,
        },
        "observed_variables": observed_variables
        if observed_variables is not None
        else {"fixture_mode": "passing", "python_major_minor": "3.10"},
    }
    encoded = canonical_json_bytes(document)
    return ImportedEvidence(
        document=copy.deepcopy(document),
        sha256=sha256_bytes(encoded),
        size=len(encoded),
        redacted_fields=0,
        input_name="unit-test.json",
    )


def acceptance_plan() -> dict[str, Any]:
    return {
        "plan_kind": "ACCEPTANCE",
        "schema_version": "0.1",
        "plan_id": "platform-readback",
        "version": 1,
        "subject": {
            "id": "public-delivery",
            "version": "candidate-001",
            "source_ref": "public-contract-fixture",
        },
        "question": "Do retained observations satisfy the declared delivery coordinates?",
        "governance": {
            "claim_owner_ref": "fixture-claim-owner",
            "drafter_ref": "fixture-plan-drafter",
            "seal_authority_ref": "fixture-seal-authority",
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
                "left": {
                    "requirement_id": "api-evidence",
                    "path": "/facts/commit_sha",
                },
                "operator": "eq",
                "right": "candidate-001",
            },
            {
                "id": "same-visible-commit",
                "severity": "HARD",
                "left": {
                    "requirement_id": "api-evidence",
                    "path": "/facts/commit_sha",
                },
                "operator": "eq",
                "right": {
                    "requirement_id": "render-evidence",
                    "path": "/facts/commit_sha",
                },
            },
        ],
        "resource_budget": {},
        "change_scope": {
            "level": "L2_CONTRACT",
            "owner": "acceptance-core",
            "expected_blast_radius": "new acceptance-only path",
            "consumers": ["acceptance-cli"],
        },
        "reproduction_steps": ["Import the retained fixture evidence."],
        "cleanup_steps": ["Remove the generated temporary bundle."],
    }


def acceptance_artifact(
    sealed_plan: dict[str, Any],
    spec_id: str,
    *,
    facts: dict[str, Any],
    session_id: str = "collection-001",
    coverage: str = "COMPLETE",
    plan_digest: str | None = None,
    spec_digest: str | None = None,
    input_name: str | None = None,
) -> ImportedEvidence:
    spec = next(item for item in sealed_plan["observation_specs"] if item["id"] == spec_id)
    document = {
        "schema_version": "0.1",
        "evidence_type": spec["evidence_type"],
        "source": "fixture-collector/0.1",
        "captured_at": "2026-09-05T00:00:00Z",
        "facts": copy.deepcopy(facts),
        "metadata": {
            "veritrail_observation": {
                "schema_version": "0.1",
                "canonicalization_profile": "veritrail-json-c14n/1",
                "plan_digest": plan_digest or sealed_plan["seal"]["digest"],
                "observation_spec_digest": spec_digest or observation_spec_digest(spec),
                "request_seal_digest": sha256_bytes(b"fixture-request"),
                "collection_session_id": session_id,
                "collector_role": "fixture-collector",
                "coverage": coverage,
                "normalization_semantics_version": "fixture-normalization/0.1",
                "facts_digest": sha256_bytes(canonical_json_bytes(facts)),
            }
        },
    }
    return import_evidence_document(document, input_name or f"{spec_id}.json")
