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
