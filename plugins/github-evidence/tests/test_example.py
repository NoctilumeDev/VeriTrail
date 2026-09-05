from __future__ import annotations

import json
import unittest
from pathlib import Path

from veritrail.acceptance_plan import verify_sealed_acceptance_plan

from veritrail_github.contracts import derive_observation_request


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


class ExampleContractTests(unittest.TestCase):
    def test_reference_plan_is_sealed_and_derivable(self) -> None:
        plan = json.loads(
            (PLUGIN_ROOT / "examples" / "acceptance-plan.json").read_text(
                encoding="utf-8"
            )
        )
        verify_sealed_acceptance_plan(plan)
        request = derive_observation_request(plan, "github-api", "reference-001")
        self.assertEqual(
            request["observation_spec"]["coordinates"]["target_commit_sha"],
            "8d3728cd2255c6a042c41183f9dc9e63e7ce547d",
        )


if __name__ == "__main__":
    unittest.main()
