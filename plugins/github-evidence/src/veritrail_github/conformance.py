from __future__ import annotations

from typing import Any

from veritrail.acceptance_evaluation import validate_observation_metadata
from veritrail.evidence import ImportedEvidence, verify_imported_evidence

from veritrail_github.contracts import (
    EVIDENCE_TYPE,
    NORMALIZATION_SEMANTICS_VERSION,
    facts_digest,
    validate_observation_request,
)
from veritrail_github.errors import ContractError


_VERDICT_LIKE_FIELDS = {
    "all_required_checks_passed",
    "release_is_correct",
    "merged_to_expected_sha",
    "acceptance_passed",
    "verdict",
}

_FACT_FIELDS = {
    "repository",
    "commit",
    "pull_request",
    "required_checks",
    "observed_checks",
    "release",
    "tag",
    "pages",
    "conflicts",
}
_COLLECTION_FIELDS = {
    "schema_version",
    "request_id",
    "request_seal_digest",
    "collector_policy_digest",
    "collection_session_id",
    "collection_started_at",
    "collection_completed_at",
    "collection_elapsed_ms",
    "access_mode",
    "visibility",
    "permission_observation",
    "api_origin",
    "api_version",
    "collector_version",
    "parser_version",
    "probes",
    "errors",
    "atomic_snapshot_claimed",
}
_PROBE_FIELDS = {
    "sequence",
    "probe_id",
    "observed_at",
    "method",
    "actual_path_and_safe_query",
    "final_path_and_safe_query",
    "actual_operands",
    "http_status",
    "returned_identifiers",
    "etag_if_available",
    "github_request_id_if_available",
    "rate_limit_metadata_if_available",
    "page_count",
    "attempt_count",
    "elapsed_ms_monotonic",
    "outcome",
    "attempt_observations",
}


def _find_forbidden_field(value: Any, path: str = "") -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            if key in _VERDICT_LIKE_FIELDS:
                return child
            found = _find_forbidden_field(item, child)
            if found:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = _find_forbidden_field(item, f"{path}[{index}]")
            if found:
                return found
    return None


def verify_github_evidence(
    plan: dict[str, Any],
    request: dict[str, Any],
    artifact: ImportedEvidence,
) -> None:
    """Recompute the adapter-owned identities in one retained Evidence artifact."""

    verified_request = validate_observation_request(plan, request)
    try:
        verify_imported_evidence(artifact)
        validate_observation_metadata(artifact.document, artifact.input_name)
    except Exception as exc:
        raise ContractError(
            ["Evidence does not satisfy the public Core 0.12.2 contract"]
        ) from exc

    document = artifact.document
    errors: list[str] = []
    if document.get("evidence_type") != EVIDENCE_TYPE:
        errors.append(f"Evidence type must be {EVIDENCE_TYPE}")
    facts = document.get("facts")
    metadata = document.get("metadata")
    if not isinstance(facts, dict) or not isinstance(metadata, dict):
        errors.append("Evidence facts and metadata must be objects")
        if errors:
            raise ContractError(errors)
    if set(facts) != _FACT_FIELDS:
        errors.append("Evidence facts must contain the exact P1 normalized partitions")

    observation = metadata.get("veritrail_observation")
    collection = metadata.get("github_collection")
    if not isinstance(observation, dict) or not isinstance(collection, dict):
        raise ContractError(
            ["Evidence must contain observation and GitHub collection metadata"]
        )
    if set(collection) != _COLLECTION_FIELDS:
        errors.append("metadata.github_collection must contain the exact P1 fields")
    if collection.get("schema_version") != "0.1":
        errors.append("metadata.github_collection.schema_version must be 0.1")
    if collection.get("access_mode") not in {
        "ANONYMOUS",
        "AUTHENTICATED_READ_ONLY",
    }:
        errors.append("metadata.github_collection.access_mode is unsupported")
    if collection.get("visibility") not in {
        "PUBLIC",
        "PRIVATE_OR_RESTRICTED",
        "UNKNOWN",
    }:
        errors.append("metadata.github_collection.visibility is unsupported")
    if collection.get("permission_observation") not in {
        "SUFFICIENT",
        "INSUFFICIENT",
        "UNKNOWN",
    }:
        errors.append(
            "metadata.github_collection.permission_observation is unsupported"
        )
    if collection.get("atomic_snapshot_claimed") is not False:
        errors.append("GitHub collection must not claim an atomic platform snapshot")
    elapsed = collection.get("collection_elapsed_ms")
    if not isinstance(elapsed, int) or isinstance(elapsed, bool) or elapsed < 0:
        errors.append(
            "metadata.github_collection.collection_elapsed_ms must be non-negative"
        )
    if (
        collection.get("api_origin")
        != verified_request["collector_policy"]["api_origin"]
    ):
        errors.append("metadata.github_collection.api_origin does not match policy")
    if (
        collection.get("api_version")
        != verified_request["collector_policy"]["api_version"]
    ):
        errors.append("metadata.github_collection.api_version does not match policy")
    probes = collection.get("probes")
    if not isinstance(probes, list):
        errors.append("metadata.github_collection.probes must be an array")
    else:
        sequences: list[int] = []
        total_attempts = 0
        for index, probe in enumerate(probes):
            if not isinstance(probe, dict) or set(probe) != _PROBE_FIELDS:
                errors.append(
                    f"metadata.github_collection.probes[{index}] has invalid fields"
                )
                continue
            sequence = probe.get("sequence")
            if not isinstance(sequence, int) or isinstance(sequence, bool):
                errors.append(
                    f"metadata.github_collection.probes[{index}].sequence is invalid"
                )
            else:
                sequences.append(sequence)
            if probe.get("method") != "GET":
                errors.append(
                    f"metadata.github_collection.probes[{index}].method must be GET"
                )
            attempt_count = probe.get("attempt_count")
            if (
                not isinstance(attempt_count, int)
                or isinstance(attempt_count, bool)
                or attempt_count < 0
            ):
                errors.append(
                    f"metadata.github_collection.probes[{index}].attempt_count is invalid"
                )
            else:
                total_attempts += attempt_count
        if sequences != list(range(1, len(probes) + 1)):
            errors.append("metadata.github_collection probe sequence is not contiguous")
        if total_attempts > verified_request["collector_policy"]["max_total_requests"]:
            errors.append(
                "metadata.github_collection exceeds the request-attempt budget"
            )
    if not isinstance(collection.get("errors"), list):
        errors.append("metadata.github_collection.errors must be an array")

    expected_observation = {
        "plan_digest": verified_request["plan_digest"],
        "observation_spec_digest": verified_request["observation_spec_digest"],
        "request_seal_digest": verified_request["seal"]["digest"],
        "collector_role": "github-api",
        "normalization_semantics_version": NORMALIZATION_SEMANTICS_VERSION,
    }
    for field, expected in expected_observation.items():
        if observation.get(field) != expected:
            errors.append(
                f"metadata.veritrail_observation.{field} does not match request"
            )

    expected_collection = {
        "request_id": verified_request["request_id"],
        "request_seal_digest": verified_request["seal"]["digest"],
        "collector_policy_digest": verified_request["collector_policy_digest"],
    }
    for field, expected in expected_collection.items():
        if collection.get(field) != expected:
            errors.append(f"metadata.github_collection.{field} does not match request")
    if collection.get("collection_session_id") != observation.get(
        "collection_session_id"
    ):
        errors.append(
            "GitHub collection and Core observation session identities differ"
        )

    expected_facts_digest = facts_digest(
        observation_spec_digest_value=verified_request["observation_spec_digest"],
        source_coordinates=verified_request["observation_spec"]["coordinates"],
        facts=facts,
        normalization_semantics_version=NORMALIZATION_SEMANTICS_VERSION,
    )
    if observation.get("facts_digest") != expected_facts_digest:
        errors.append(
            "metadata.veritrail_observation.facts_digest does not match facts"
        )

    forbidden = _find_forbidden_field(facts)
    if forbidden:
        errors.append(f"facts contains plugin-owned Verdict-like field: {forbidden}")
    if errors:
        raise ContractError(errors)
