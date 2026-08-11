from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes, sha256_bytes
from veritrail.evidence import ImportedEvidence
from veritrail.plan import seal_plan

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
    plan["required_evidence"].append("runtime.command")
    plan["assertions"].append(
        {
            "id": "command-exit-accepted",
            "severity": "HARD",
            "evidence_type": "runtime.command",
            "path": "/exit_expected",
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
