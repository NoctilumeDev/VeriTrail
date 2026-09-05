from __future__ import annotations

import copy
from collections import defaultdict, deque
from typing import Any, Mapping

from veritrail.acceptance_plan import seal_acceptance_plan

from veritrail_github.transport import TransportResponse


TARGET_SHA = "a" * 40
BASE_SHA = "b" * 40


def acceptance_plan(
    projections: list[str],
    *,
    target_sha: str = TARGET_SHA,
    pull_request_number: int | None = None,
    release_tag: str | None = None,
    assertion_sha: str | None = None,
    assertion_path: str | None = None,
    assertion_value: Any | None = None,
    question: str = "Does retained GitHub evidence satisfy this declared coordinate?",
) -> dict[str, Any]:
    coordinates: dict[str, Any] = {
        "owner": "NoctilumeDev",
        "repository": "VeriTrail",
        "target_commit_sha": target_sha,
        "branch": "main",
    }
    if pull_request_number is not None:
        coordinates["pull_request_number"] = pull_request_number
    if release_tag is not None:
        coordinates["release_tag"] = release_tag
    resolved_assertion_path = assertion_path or "/facts/commit/sha"
    if assertion_path is None and "commit.identity" not in projections:
        resolved_assertion_path = "/metadata/veritrail_observation/coverage"
    if assertion_value is not None:
        resolved_assertion_value = assertion_value
    elif "commit.identity" in projections:
        resolved_assertion_value = assertion_sha or target_sha
    else:
        resolved_assertion_value = "COMPLETE"
    unsigned = {
        "plan_kind": "ACCEPTANCE",
        "schema_version": "0.1",
        "plan_id": "github-p1-fixture",
        "version": 1,
        "subject": {
            "id": "veritrail",
            "version": target_sha,
            "source_ref": "github:noctilumedev/veritrail",
        },
        "question": question,
        "governance": {
            "claim_owner_ref": "human:owner",
            "drafter_ref": "test:fixture",
            "seal_authority_ref": "human:owner",
            "seal_decision": "CONFIRMED",
        },
        "observation_specs": [
            {
                "id": "github-api",
                "contract": {"id": "github-observation-request", "version": "0.1"},
                "evidence_type": "platform.github.api.snapshot",
                "coordinates": coordinates,
                "projections": sorted(projections),
                "canonicalization_profile": "veritrail-json-c14n/1",
            }
        ],
        "evidence_requirements": [
            {
                "id": "github-evidence",
                "observation_spec_id": "github-api",
                "cardinality": "EXACTLY_ONE",
            }
        ],
        "sufficiency_rules": [
            {
                "id": "coverage-complete",
                "left": {
                    "requirement_id": "github-evidence",
                    "path": "/metadata/veritrail_observation/coverage",
                },
                "operator": "eq",
                "right": "COMPLETE",
            }
        ],
        "integrity_rules": [],
        "assertions": [
            {
                "id": "declared-observation",
                "severity": "HARD",
                "left": {
                    "requirement_id": "github-evidence",
                    "path": resolved_assertion_path,
                },
                "operator": "eq",
                "right": resolved_assertion_value,
            }
        ],
        "resource_budget": {"network_requests": 24},
        "change_scope": {
            "level": "L3_SYSTEM",
            "owner": "github-evidence-plugin",
            "consumers": ["acceptance-core"],
        },
        "reproduction_steps": ["Run the bounded fixture collector."],
        "cleanup_steps": ["Remove the generated Evidence file."],
    }
    return seal_acceptance_plan(unsigned)


def repository_payload() -> dict[str, Any]:
    return {
        "id": 123,
        "node_id": "R_123",
        "name": "VeriTrail",
        "full_name": "NoctilumeDev/VeriTrail",
        "private": False,
        "visibility": "public",
        "default_branch": "main",
        "owner": {"login": "NoctilumeDev"},
    }


def commit_payload(sha: str = TARGET_SHA) -> dict[str, Any]:
    return {"sha": sha, "node_id": "C_123"}


class MemoryTransport:
    def __init__(self) -> None:
        self._responses: dict[str, deque[TransportResponse | Exception]] = defaultdict(
            deque
        )
        self.calls: list[dict[str, Any]] = []

    def add(
        self,
        path_and_query: str,
        body: Any = None,
        *,
        status: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> "MemoryTransport":
        import json

        encoded = b"" if body is None else json.dumps(body).encode("utf-8")
        self._responses[path_and_query].append(
            TransportResponse(
                status=status,
                headers={key.lower(): value for key, value in (headers or {}).items()},
                body=encoded,
                final_url=f"https://api.github.com{path_and_query}",
            )
        )
        return self

    def add_exception(self, path_and_query: str, error: Exception) -> "MemoryTransport":
        self._responses[path_and_query].append(error)
        return self

    def get(
        self,
        *,
        api_origin: str,
        path_and_query: str,
        headers: Mapping[str, str],
        connect_timeout_ms: int,
        read_timeout_ms: int,
        max_redirects: int,
    ) -> TransportResponse:
        self.calls.append(
            {
                "api_origin": api_origin,
                "path_and_query": path_and_query,
                "headers": copy.deepcopy(dict(headers)),
                "connect_timeout_ms": connect_timeout_ms,
                "read_timeout_ms": read_timeout_ms,
                "max_redirects": max_redirects,
            }
        )
        queue = self._responses.get(path_and_query)
        if not queue:
            raise AssertionError(f"unexpected fixture request: {path_and_query}")
        response = queue.popleft()
        if isinstance(response, Exception):
            raise response
        return response


def base_transport(*, commit_sha: str = TARGET_SHA) -> MemoryTransport:
    return (
        MemoryTransport()
        .add("/repos/NoctilumeDev/VeriTrail", repository_payload())
        .add(
            f"/repos/NoctilumeDev/VeriTrail/commits/{TARGET_SHA}",
            commit_payload(commit_sha),
        )
    )
