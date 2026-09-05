from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone

from veritrail.acceptance_evaluation import evaluate_acceptance
from veritrail.evidence import verify_imported_evidence

from veritrail_github.collector import GitHubCollector
from veritrail_github.contracts import derive_observation_request
from veritrail_github.errors import TransportError

from support import (
    BASE_SHA,
    TARGET_SHA,
    MemoryTransport,
    acceptance_plan,
    base_transport,
)


FIXED_TIME = datetime(2026, 9, 5, 0, 0, tzinfo=timezone.utc)


def collect(
    plan,
    transport,
    *,
    request_id="request-001",
    token=None,
    session="github-session-001",
):
    request = derive_observation_request(plan, "github-api", request_id)
    collector = GitHubCollector(
        transport,
        token=token,
        clock=lambda: FIXED_TIME,
        session_id_factory=lambda: session,
        sleep=lambda _seconds: None,
    )
    return collector.collect(plan, request)


class CollectorPositiveTests(unittest.TestCase):
    def test_repository_commit_evidence_imports_and_core_passes(self) -> None:
        plan = acceptance_plan(["commit.identity", "repository.identity"])
        result = collect(plan, base_transport())
        verify_imported_evidence(result.artifact)
        document = result.artifact.document
        self.assertEqual(document["facts"]["commit"]["sha"], TARGET_SHA)
        self.assertEqual(
            document["metadata"]["veritrail_observation"]["coverage"], "COMPLETE"
        )
        report = evaluate_acceptance(plan, [result.artifact], "COMPLETED")
        self.assertEqual(report["verdict"], "PASS")

    def test_replay_has_same_facts_and_different_evidence_identity(self) -> None:
        plan = acceptance_plan(["commit.identity", "repository.identity"])
        first = collect(plan, base_transport(), session="github-session-001")
        second = collect(plan, base_transport(), session="github-session-002")
        first_meta = first.artifact.document["metadata"]["veritrail_observation"]
        second_meta = second.artifact.document["metadata"]["veritrail_observation"]
        self.assertEqual(first_meta["facts_digest"], second_meta["facts_digest"])
        self.assertNotEqual(first.artifact.sha256, second.artifact.sha256)

    def test_read_only_headers_are_sent_but_token_is_not_retained(self) -> None:
        token = "test-read-only-credential"
        transport = base_transport()
        plan = acceptance_plan(["commit.identity"])
        result = collect(plan, transport, token=token)
        self.assertTrue(
            all(
                call["headers"]["Authorization"] == f"Bearer {token}"
                for call in transport.calls
            )
        )
        retained = json.dumps(result.artifact.document, sort_keys=True)
        self.assertNotIn(token, retained)
        self.assertNotIn("Authorization", retained)
        collection = result.artifact.document["metadata"]["github_collection"]
        self.assertEqual(collection["access_mode"], "AUTHENTICATED_READ_ONLY")

    def test_pull_request_coordinates_remain_descriptive(self) -> None:
        variants = [
            (False, TARGET_SHA),
            (True, TARGET_SHA),
            (True, "c" * 40),
            (True, "d" * 40),
        ]
        for merged, merge_sha in variants:
            with self.subTest(merged=merged, merge_sha=merge_sha):
                plan = acceptance_plan(["pull_request.merge"], pull_request_number=28)
                transport = base_transport().add(
                    "/repos/NoctilumeDev/VeriTrail/pulls/28",
                    {
                        "number": 28,
                        "state": "closed" if merged else "open",
                        "merged": merged,
                        "head": {"sha": BASE_SHA},
                        "base": {"sha": "e" * 40},
                        "merge_commit_sha": merge_sha,
                    },
                )
                facts = collect(plan, transport).artifact.document["facts"][
                    "pull_request"
                ]
                self.assertEqual(facts["merged"], merged)
                self.assertEqual(facts["head_sha"], BASE_SHA)
                self.assertEqual(facts["merge_commit_sha"], merge_sha)

    def test_required_and_observed_checks_stay_separate_and_keep_producer_identity(
        self,
    ) -> None:
        plan = acceptance_plan(["checks.observed_runs", "rules.required_checks"])
        transport = (
            base_transport()
            .add(
                "/repos/NoctilumeDev/VeriTrail/rules/branches/main?per_page=100",
                [
                    {
                        "type": "required_status_checks",
                        "parameters": {
                            "required_status_checks": [
                                {"context": "build", "integration_id": 10},
                                {"context": "build", "integration_id": 11},
                            ]
                        },
                    }
                ],
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}/check-runs?filter=all&per_page=100",
                {
                    "total_count": 2,
                    "check_runs": [
                        {
                            "id": 100,
                            "name": "build",
                            "head_sha": TARGET_SHA,
                            "status": "completed",
                            "conclusion": "success",
                            "app": {"id": 10, "slug": "actions"},
                            "check_suite": {"id": 1000},
                        },
                        {
                            "id": 101,
                            "name": "build",
                            "head_sha": TARGET_SHA,
                            "status": "completed",
                            "conclusion": "success",
                            "app": {"id": 11, "slug": "external-ci"},
                            "check_suite": {"id": 1001},
                        },
                    ],
                },
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}/status?per_page=100",
                {
                    "state": "success",
                    "statuses": [
                        {
                            "id": 102,
                            "context": "build",
                            "state": "success",
                            "sha": TARGET_SHA,
                            "creator": {"id": 12, "login": "legacy-ci"},
                        }
                    ],
                },
            )
        )
        facts = collect(plan, transport).artifact.document["facts"]
        self.assertEqual(len(facts["required_checks"]["items"]), 2)
        self.assertEqual(len(facts["observed_checks"]), 3)
        self.assertEqual(
            {item["source_kind"] for item in facts["observed_checks"]},
            {"CHECK_RUN", "COMMIT_STATUS"},
        )

    def test_annotated_tag_is_peeled_to_commit_without_using_release_commitish(
        self,
    ) -> None:
        tag_object = "f" * 40
        plan = acceptance_plan(["tag.peeled_commit"], release_tag="v0.1.0")
        transport = (
            base_transport()
            .add(
                "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
                {
                    "ref": "refs/tags/v0.1.0",
                    "object": {"type": "tag", "sha": tag_object},
                },
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/git/tags/{tag_object}",
                {"sha": tag_object, "object": {"type": "commit", "sha": TARGET_SHA}},
            )
        )
        tag = collect(plan, transport).artifact.document["facts"]["tag"]
        self.assertEqual(tag["peeled_commit_sha"], TARGET_SHA)
        self.assertEqual(
            [item["object_type"] for item in tag["peel_chain"]], ["tag", "commit"]
        )


class CollectorFailureTests(unittest.TestCase):
    def test_response_sha_mismatch_is_error_and_core_does_not_pass(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        result = collect(plan, base_transport(commit_sha="b" * 40))
        observation = result.artifact.document["metadata"]["veritrail_observation"]
        self.assertEqual(observation["coverage"], "ERROR")
        report = evaluate_acceptance(plan, [result.artifact], "COMPLETED")
        self.assertNotEqual(report["verdict"], "PASS")

    def test_ambiguous_404_is_not_normalized_as_absence(self) -> None:
        plan = acceptance_plan(["pages.metadata"])
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/pages", status=404
        )
        result = collect(plan, transport)
        document = result.artifact.document
        self.assertIsNone(document["facts"]["pages"])
        self.assertEqual(
            document["metadata"]["veritrail_observation"]["coverage"], "PARTIAL"
        )
        self.assertEqual(
            document["metadata"]["github_collection"]["permission_observation"],
            "UNKNOWN",
        )

    def test_network_failure_is_bounded_and_does_not_reuse_success(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        path = "/repos/NoctilumeDev/VeriTrail"
        transport = MemoryTransport()
        for _ in range(3):
            transport.add_exception(path, TransportError("secret raw failure"))
        result = collect(plan, transport)
        self.assertEqual(len(transport.calls), 3)
        self.assertEqual(
            result.artifact.document["metadata"]["veritrail_observation"]["coverage"],
            "ERROR",
        )
        retained = json.dumps(result.artifact.document)
        self.assertNotIn("secret raw failure", retained)


if __name__ == "__main__":
    unittest.main()
