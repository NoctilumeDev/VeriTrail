from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from veritrail_github.collector import GitHubCollector
from veritrail_github.contracts import (
    DEFAULT_COLLECTOR_POLICY,
    derive_observation_request,
    facts_digest,
)
from veritrail_github.errors import ContractError
from veritrail_github.transport import TransportResponse

from support import (
    TARGET_SHA,
    MemoryTransport,
    acceptance_plan,
    base_transport,
)
from test_collector import collect


class DerivationBoundaryTests(unittest.TestCase):
    def test_unknown_projection_is_rejected_by_plugin_contract(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        plan.pop("seal")
        plan["observation_specs"][0]["projections"] = ["future.unknown"]
        from veritrail.acceptance_plan import seal_acceptance_plan

        sealed = seal_acceptance_plan(plan)
        with self.assertRaisesRegex(ContractError, "unsupported projection"):
            derive_observation_request(sealed, "github-api", "request-001")

    def test_missing_conditional_coordinate_is_rejected(self) -> None:
        plan = acceptance_plan(["pull_request.merge"], pull_request_number=28)
        plan.pop("seal")
        del plan["observation_specs"][0]["coordinates"]["pull_request_number"]
        from veritrail.acceptance_plan import seal_acceptance_plan

        sealed = seal_acceptance_plan(plan)
        with self.assertRaisesRegex(
            ContractError, "requires coordinates.pull_request_number"
        ):
            derive_observation_request(sealed, "github-api", "request-001")

    def test_policy_cannot_expand_frozen_resource_bounds(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        policy = dict(DEFAULT_COLLECTOR_POLICY)
        policy["max_total_requests"] = 25
        with self.assertRaisesRegex(ContractError, "max_total_requests"):
            derive_observation_request(
                plan, "github-api", "request-001", collector_policy=policy
            )

    def test_normalization_semantics_is_part_of_fact_identity(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        request = derive_observation_request(plan, "github-api", "request-001")
        facts = {"commit": {"sha": TARGET_SHA}}
        first = facts_digest(
            observation_spec_digest_value=request["observation_spec_digest"],
            source_coordinates=request["observation_spec"]["coordinates"],
            facts=facts,
            normalization_semantics_version="github-rest-facts/0.1",
        )
        second = facts_digest(
            observation_spec_digest_value=request["observation_spec_digest"],
            source_coordinates=request["observation_spec"]["coordinates"],
            facts=facts,
            normalization_semantics_version="github-rest-facts/0.2",
        )
        self.assertNotEqual(first, second)


class CollectionBoundaryTests(unittest.TestCase):
    def test_implementation_version_changes_evidence_not_fact_identity(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        first = collect(plan, base_transport(), session="github-session-same")
        with patch(
            "veritrail_github.collector.PARSER_IMPLEMENTATION_VERSION",
            "github-rest-parser/0.1.1",
        ):
            second = collect(plan, base_transport(), session="github-session-same")
        first_observation = first.artifact.document["metadata"]["veritrail_observation"]
        second_observation = second.artifact.document["metadata"][
            "veritrail_observation"
        ]
        self.assertEqual(
            first_observation["facts_digest"], second_observation["facts_digest"]
        )
        self.assertNotEqual(first.artifact.sha256, second.artifact.sha256)

    def test_request_budget_stops_before_an_unapproved_second_call(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        policy = dict(DEFAULT_COLLECTOR_POLICY)
        policy["max_total_requests"] = 1
        request = derive_observation_request(
            plan, "github-api", "request-budget", collector_policy=policy
        )
        transport = base_transport()
        result = GitHubCollector(
            transport,
            session_id_factory=lambda: "github-session-budget",
            sleep=lambda _seconds: None,
        ).collect(plan, request)
        self.assertEqual(len(transport.calls), 1)
        metadata = result.artifact.document["metadata"]
        self.assertEqual(metadata["veritrail_observation"]["coverage"], "ERROR")
        self.assertIn(
            "COLLECTION_BUDGET_EXHAUSTED",
            {item["code"] for item in metadata["github_collection"]["errors"]},
        )

    def test_multi_page_check_runs_follow_same_origin_link(self) -> None:
        plan = acceptance_plan(["checks.observed_runs"])
        first_path = (
            f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}"
            "/check-runs?filter=all&per_page=100"
        )
        second_path = (
            f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}"
            "/check-runs?page=2&per_page=100"
        )

        def run(identifier: int) -> dict[str, object]:
            return {
                "id": identifier,
                "name": f"check-{identifier}",
                "head_sha": TARGET_SHA,
                "status": "completed",
                "conclusion": "success",
                "app": {"id": 10, "slug": "actions"},
                "check_suite": {"id": 1000 + identifier},
            }

        transport = (
            base_transport()
            .add(
                first_path,
                {"total_count": 2, "check_runs": [run(1)]},
                headers={
                    "Link": (
                        "<https://api.github.com"
                        f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}"
                        '/check-runs?page=2&per_page=100>; rel="next"'
                    )
                },
            )
            .add(second_path, {"total_count": 2, "check_runs": [run(2)]})
            .add(
                f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}/status?per_page=100",
                {"state": "success", "statuses": []},
            )
        )
        result = collect(plan, transport)
        self.assertEqual(len(result.artifact.document["facts"]["observed_checks"]), 2)
        self.assertEqual(
            result.artifact.document["metadata"]["veritrail_observation"]["coverage"],
            "COMPLETE",
        )

    def test_cross_resource_pagination_link_fails_closed(self) -> None:
        plan = acceptance_plan(["checks.observed_runs"])
        path = (
            f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}"
            "/check-runs?filter=all&per_page=100"
        )
        transport = (
            base_transport()
            .add(
                path,
                {"total_count": 0, "check_runs": []},
                headers={"Link": '<https://api.github.com/user?page=2>; rel="next"'},
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}/status?per_page=100",
                {"state": "success", "statuses": []},
            )
        )
        result = collect(plan, transport)
        metadata = result.artifact.document["metadata"]
        self.assertEqual(metadata["veritrail_observation"]["coverage"], "PARTIAL")
        self.assertIn(
            "PAGINATION_ORIGIN_MISMATCH",
            {item["code"] for item in metadata["github_collection"]["errors"]},
        )

    def test_http_error_categories_are_retained_without_raw_response(self) -> None:
        cases = [
            (401, {}, "AUTHENTICATION_FAILED", 1),
            (403, {}, "PERMISSION_INSUFFICIENT", 1),
            (403, {"Retry-After": "0"}, "RATE_LIMITED", 3),
            (429, {"Retry-After": "0"}, "RATE_LIMITED", 3),
            (304, {}, "NOT_MODIFIED_WITHOUT_BOUND_EVIDENCE", 1),
            (500, {}, "SERVER_ERROR", 3),
        ]
        for status, headers, code, attempts in cases:
            with self.subTest(status=status, code=code):
                plan = acceptance_plan(["commit.identity"])
                transport = MemoryTransport()
                for _ in range(attempts):
                    transport.add(
                        "/repos/NoctilumeDev/VeriTrail",
                        {"message": "raw-body-must-not-survive"},
                        status=status,
                        headers=headers,
                    )
                result = collect(plan, transport)
                metadata = result.artifact.document["metadata"]
                self.assertEqual(metadata["veritrail_observation"]["coverage"], "ERROR")
                self.assertIn(
                    code,
                    {item["code"] for item in metadata["github_collection"]["errors"]},
                )
                self.assertNotIn(
                    "raw-body-must-not-survive", json.dumps(result.artifact.document)
                )

    def test_incomplete_check_producer_identity_is_an_explicit_conflict(self) -> None:
        plan = acceptance_plan(["checks.observed_runs"])
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
                            "app": None,
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
        result = collect(plan, transport)
        conflicts = result.artifact.document["facts"]["conflicts"]
        self.assertIn(
            "OBSERVED_CHECK_IDENTITY_INCOMPLETE",
            {item["code"] for item in conflicts},
        )

    def test_pagination_limit_retains_partial_page_and_truncation(self) -> None:
        plan = acceptance_plan(["checks.observed_runs"])
        policy = dict(DEFAULT_COLLECTOR_POLICY)
        policy["max_pages_per_probe"] = 1
        request = derive_observation_request(
            plan, "github-api", "request-page-limit", collector_policy=policy
        )
        first_path = (
            f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}"
            "/check-runs?filter=all&per_page=100"
        )
        transport = (
            base_transport()
            .add(
                first_path,
                {"total_count": 2, "check_runs": []},
                headers={
                    "Link": (
                        "<https://api.github.com"
                        f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}"
                        '/check-runs?page=2&per_page=100>; rel="next"'
                    )
                },
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}/status?per_page=100",
                {"state": "success", "sha": TARGET_SHA, "statuses": []},
            )
        )
        result = GitHubCollector(
            transport,
            session_id_factory=lambda: "github-page-limit",
            sleep=lambda _seconds: None,
        ).collect(plan, request)
        metadata = result.artifact.document["metadata"]
        self.assertEqual(metadata["veritrail_observation"]["coverage"], "PARTIAL")
        self.assertIn(
            "PAGINATION_LIMIT_REACHED",
            {item["code"] for item in metadata["github_collection"]["errors"]},
        )

    def test_wall_clock_jump_does_not_control_monotonic_window(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        request = derive_observation_request(plan, "github-api", "request-clock")
        wall_values = iter(
            [
                datetime(2026, 9, 5, 0, 0, 10, tzinfo=timezone.utc),
                datetime(2026, 9, 5, 0, 0, 20, tzinfo=timezone.utc),
                datetime(2026, 9, 5, 0, 0, 5, tzinfo=timezone.utc),
                datetime(2026, 9, 5, 0, 0, 1, tzinfo=timezone.utc),
            ]
        )
        monotonic_value = 0.0

        def monotonic() -> float:
            nonlocal monotonic_value
            monotonic_value += 0.001
            return monotonic_value

        result = GitHubCollector(
            base_transport(),
            clock=lambda: next(wall_values),
            monotonic=monotonic,
            session_id_factory=lambda: "github-clock-jump",
        ).collect(plan, request)
        collection = result.artifact.document["metadata"]["github_collection"]
        self.assertGreaterEqual(collection["collection_elapsed_ms"], 0)
        self.assertLess(
            collection["collection_completed_at"], collection["collection_started_at"]
        )
        self.assertEqual(
            result.artifact.document["metadata"]["veritrail_observation"]["coverage"],
            "COMPLETE",
        )

    def test_transport_cannot_redirect_collection_outside_api_origin(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        transport = MemoryTransport()
        transport._responses["/repos/NoctilumeDev/VeriTrail"].append(
            TransportResponse(
                status=200,
                headers={},
                body=json.dumps({"id": 1}).encode(),
                final_url="https://example.invalid/repos/NoctilumeDev/VeriTrail",
            )
        )
        transport._responses["/repos/NoctilumeDev/VeriTrail"].append(
            transport._responses["/repos/NoctilumeDev/VeriTrail"][0]
        )
        transport._responses["/repos/NoctilumeDev/VeriTrail"].append(
            transport._responses["/repos/NoctilumeDev/VeriTrail"][0]
        )
        result = collect(plan, transport)
        self.assertEqual(
            result.artifact.document["metadata"]["veritrail_observation"]["coverage"],
            "ERROR",
        )

    def test_requests_never_send_conditional_or_cookie_headers(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        transport = base_transport()
        collect(plan, transport)
        forbidden = {"if-none-match", "if-modified-since", "cookie"}
        for call in transport.calls:
            self.assertFalse(
                forbidden.intersection(key.casefold() for key in call["headers"])
            )

    def test_invalid_json_is_parser_error_not_empty_fact(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        transport = MemoryTransport()
        transport._responses["/repos/NoctilumeDev/VeriTrail"].append(
            TransportResponse(
                status=200,
                headers={},
                body=b"not-json",
                final_url="https://api.github.com/repos/NoctilumeDev/VeriTrail",
            )
        )
        result = collect(plan, transport)
        metadata = result.artifact.document["metadata"]
        self.assertEqual(metadata["veritrail_observation"]["coverage"], "ERROR")
        self.assertIn(
            "RESPONSE_JSON_INVALID",
            {item["code"] for item in metadata["github_collection"]["errors"]},
        )


if __name__ == "__main__":
    unittest.main()
