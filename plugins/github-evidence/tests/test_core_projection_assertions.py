from __future__ import annotations

import unittest

from veritrail.acceptance_evaluation import evaluate_acceptance

from support import BASE_SHA, TARGET_SHA, acceptance_plan, base_transport
from test_collector import collect


class CoreProjectionAssertionTests(unittest.TestCase):
    def _assert_pass(self, plan, transport) -> None:
        result = collect(plan, transport)
        report = evaluate_acceptance(plan, [result.artifact], "COMPLETED")
        self.assertEqual(report["verdict"], "PASS")

    def test_core_reads_pull_request_merge_without_plugin_verdict(self) -> None:
        plan = acceptance_plan(
            ["pull_request.merge"],
            pull_request_number=28,
            assertion_path="/facts/pull_request/merged",
            assertion_value=True,
        )
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/pulls/28",
            {
                "number": 28,
                "state": "closed",
                "merged": True,
                "head": {"sha": BASE_SHA},
                "base": {"sha": "e" * 40},
                "merge_commit_sha": TARGET_SHA,
            },
        )
        self._assert_pass(plan, transport)

    def test_core_reads_required_check_context_without_plugin_verdict(self) -> None:
        plan = acceptance_plan(
            ["rules.required_checks"],
            assertion_path="/facts/required_checks/items/0/context",
            assertion_value="build",
        )
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/rules/branches/main?per_page=100",
            [
                {
                    "type": "required_status_checks",
                    "parameters": {
                        "required_status_checks": [
                            {"context": "build", "integration_id": 10}
                        ]
                    },
                }
            ],
        )
        self._assert_pass(plan, transport)

    def test_core_reads_observed_check_source_without_plugin_verdict(self) -> None:
        plan = acceptance_plan(
            ["checks.observed_runs"],
            assertion_path="/facts/observed_checks/0/source_kind",
            assertion_value="CHECK_RUN",
        )
        transport = (
            base_transport()
            .add(
                f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}/check-runs?filter=all&per_page=100",
                {
                    "total_count": 1,
                    "check_runs": [
                        {
                            "id": 100,
                            "name": "build",
                            "head_sha": TARGET_SHA,
                            "status": "completed",
                            "conclusion": "success",
                            "app": {"id": 10, "slug": "actions"},
                            "check_suite": {"id": 1000},
                        }
                    ],
                },
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}/status?per_page=100",
                {"state": "success", "sha": TARGET_SHA, "statuses": []},
            )
        )
        self._assert_pass(plan, transport)

    def test_core_reads_tag_and_release_fields_without_plugin_verdict(self) -> None:
        plan = acceptance_plan(
            ["release.identity", "tag.peeled_commit"],
            release_tag="v0.1.0",
            assertion_path="/facts/tag/peeled_commit_sha",
            assertion_value=TARGET_SHA,
        )
        transport = (
            base_transport()
            .add(
                "/repos/NoctilumeDev/VeriTrail/releases/tags/v0.1.0",
                {
                    "id": 55,
                    "tag_name": "v0.1.0",
                    "target_commitish": "main",
                    "draft": False,
                    "prerelease": False,
                    "immutable": True,
                    "published_at": "2026-09-05T00:00:00Z",
                    "assets": [],
                },
            )
            .add(
                "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
                {
                    "ref": "refs/tags/v0.1.0",
                    "object": {"type": "commit", "sha": TARGET_SHA},
                },
            )
        )
        self._assert_pass(plan, transport)


if __name__ == "__main__":
    unittest.main()
