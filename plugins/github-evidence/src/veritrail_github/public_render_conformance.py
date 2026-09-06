from __future__ import annotations

import re
from typing import Any, Mapping

from veritrail.acceptance_evaluation import validate_observation_metadata
from veritrail.evidence import ImportedEvidence, verify_imported_evidence

from veritrail_github.errors import ContractError
from veritrail_github.public_render_contracts import (
    PUBLIC_RENDER_EVIDENCE_TYPE,
    PUBLIC_RENDER_NORMALIZATION_SEMANTICS_VERSION,
    public_render_facts_digest,
    validate_public_render_request,
)


PUBLIC_RENDER_FACT_FIELDS = {
    "target",
    "navigation",
    "document",
    "content",
    "conflicts",
}
PUBLIC_RENDER_COLLECTION_FIELDS = {
    "schema_version",
    "request_id",
    "request_seal_digest",
    "render_policy_digest",
    "collection_session_id",
    "collection_started_at",
    "collection_completed_at",
    "collection_elapsed_ms",
    "access_mode",
    "collector_version",
    "parser_version",
    "browser_runtime",
    "initial_state_check",
    "post_navigation_state",
    "network_summary",
    "response_body_observation",
    "runtime_events",
    "phase_observations",
    "errors",
    "cleanup_errors",
    "coverage_reasons",
    "atomic_snapshot_claimed",
}
_PHASE_FIELDS = {"sequence", "phase", "outcome", "elapsed_ms_monotonic"}
_ERROR_FIELDS = {"phase", "code", "fatal"}
_BROWSER_RUNTIME_FIELDS = {
    "playwright_version",
    "browser_engine",
    "browser_distribution",
    "browser_version",
}
_INITIAL_STATE_FIELDS = {"kind", "cookies", "origins"}
_POST_STATE_FIELDS = {
    "cookie_count",
    "origin_count",
    "secure_cookie_count",
    "http_only_cookie_count",
    "session_cookie_count",
    "same_site_counts",
}
_NETWORK_SUMMARY_FIELDS = {
    "request_count",
    "allowed_count",
    "blocked_count",
    "blocked_write_count",
    "blocked_read_host_count",
    "blocked_websocket_count",
    "affects_coverage_count",
    "reason_counts",
}
_RUNTIME_EVENT_FIELDS = {
    "console_categories",
    "page_error_count",
    "request_failure_categories",
}
_RESPONSE_BODY_FIELDS = {
    "total_response_body_bytes",
    "main_document_response_body_bytes",
    "delivered_response_body_bytes",
    "completed_responses",
    "closed_streams",
    "active_streams",
    "request_stage_pauses",
    "response_error_reason_counts",
    "failure",
}
_SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")

_VERDICT_LIKE_FIELDS = {
    "page_is_current",
    "render_matches_api",
    "all_markers_present",
    "release_is_correct",
    "public_delivery_passed",
    "acceptance_passed",
    "verdict",
}


def expected_public_render_coverage(
    request: Mapping[str, Any],
    facts: Mapping[str, Any],
    collection: Mapping[str, Any],
) -> tuple[str, list[str]]:
    """Derive collection completeness without evaluating Plan assertions."""

    fatal_reasons: list[str] = []
    partial_reasons: list[str] = []
    elapsed_ms = collection.get("collection_elapsed_ms")
    max_elapsed_ms = request.get("render_policy", {}).get("max_elapsed_ms")
    if (
        _is_non_negative_int(elapsed_ms)
        and _is_non_negative_int(max_elapsed_ms)
        and elapsed_ms > max_elapsed_ms
    ):
        fatal_reasons.append("COLLECTION_WINDOW_EXCEEDED")
    errors = collection.get("errors")
    if isinstance(errors, list):
        for error in errors:
            if not isinstance(error, Mapping):
                fatal_reasons.append("COLLECTION_ERROR_METADATA_INVALID")
                continue
            code = error.get("code")
            code = code if isinstance(code, str) and code else "COLLECTION_ERROR"
            if error.get("fatal") is True:
                fatal_reasons.append(code)
            else:
                partial_reasons.append(code)
    else:
        fatal_reasons.append("COLLECTION_ERRORS_INVALID")

    cleanup_errors = collection.get("cleanup_errors")
    if not isinstance(cleanup_errors, list):
        fatal_reasons.append("CLEANUP_METADATA_INVALID")
    elif cleanup_errors:
        fatal_reasons.append("CLEANUP_FAILED")

    phases = collection.get("phase_observations")
    phase_outcomes = {
        item.get("phase"): item.get("outcome")
        for item in phases
        if isinstance(item, Mapping)
    } if isinstance(phases, list) else {}
    if phase_outcomes.get("open") != "OBSERVED":
        fatal_reasons.append("BROWSER_NOT_OPENED")
    if phase_outcomes.get("navigation") != "OBSERVED":
        fatal_reasons.append("NAVIGATION_NOT_OBSERVED")
    if phase_outcomes.get("cleanup") != "OBSERVED":
        fatal_reasons.append("CLEANUP_NOT_OBSERVED")

    initial_state = collection.get("initial_state_check")
    expected_initial_state = {
        "kind": "ANONYMOUS_FRESH_CONTEXT",
        "cookies": 0,
        "origins": 0,
    }
    if initial_state not in ({}, expected_initial_state):
        fatal_reasons.append("INITIAL_STATE_INVALID")
    if phase_outcomes.get("open") == "OBSERVED" and initial_state == {}:
        fatal_reasons.append("INITIAL_STATE_MISSING")

    response_body = collection.get("response_body_observation")
    if isinstance(response_body, Mapping):
        if response_body.get("failure") is not None:
            fatal_reasons.append("RESPONSE_BODY_OBSERVATION_FAILED")
        active_streams = response_body.get("active_streams")
        if isinstance(active_streams, int) and active_streams > 0:
            fatal_reasons.append("RESPONSE_BODY_STREAM_RETAINED")

    conflicts = facts.get("conflicts")
    if not isinstance(conflicts, list):
        fatal_reasons.append("FACT_CONFLICTS_INVALID")
    elif conflicts:
        partial_reasons.append("FACT_CONFLICTS_RETAINED")

    network = collection.get("network_summary")
    if not isinstance(network, Mapping):
        fatal_reasons.append("NETWORK_SUMMARY_INVALID")
    else:
        count = network.get("affects_coverage_count")
        if isinstance(count, int) and not isinstance(count, bool) and count > 0:
            partial_reasons.append("NETWORK_POLICY_AFFECTED_COVERAGE")

    projections = request.get("observation_spec", {}).get("projections", [])
    if "navigation.identity" in projections and facts.get("navigation") is None:
        fatal_reasons.append("NAVIGATION_PROJECTION_MISSING")
    if "document.identity" in projections and facts.get("document") is None:
        partial_reasons.append("DOCUMENT_IDENTITY_MISSING")
    if "navigation.identity" not in projections and facts.get("navigation") is not None:
        fatal_reasons.append("UNREQUESTED_NAVIGATION_FACTS")
    if "document.identity" not in projections and facts.get("document") is not None:
        fatal_reasons.append("UNREQUESTED_DOCUMENT_FACTS")

    content_requested = any(
        isinstance(item, str) and item.startswith("content.")
        for item in projections
    )
    content = facts.get("content")
    if content_requested:
        if not isinstance(content, Mapping):
            partial_reasons.append("CONTENT_OBSERVATION_MISSING")
        else:
            scope = content.get("scope")
            if not isinstance(scope, Mapping) or scope.get("usable") is not True:
                partial_reasons.append("CONTENT_SCOPE_NOT_UNIQUE")
            window = content.get("window")
            if not isinstance(window, Mapping):
                partial_reasons.append("CONTENT_WINDOW_MISSING")
            else:
                if window.get("samples_stable") is not True:
                    partial_reasons.append("CONTENT_SAMPLES_UNSTABLE")
                truncations = window.get("truncations")
                if isinstance(truncations, list) and truncations:
                    partial_reasons.append("CONTENT_TRUNCATED")
    elif content is not None:
        fatal_reasons.append("UNREQUESTED_CONTENT_FACTS")

    if fatal_reasons:
        return "ERROR", sorted(set(fatal_reasons))
    if partial_reasons:
        return "PARTIAL", sorted(set(partial_reasons))
    return "COMPLETE", []


def verify_public_render_evidence(
    plan: dict[str, Any],
    request: dict[str, Any],
    artifact: ImportedEvidence,
) -> None:
    """Recompute P2-owned identities and collection-completeness semantics."""

    verified_request = validate_public_render_request(plan, request)
    try:
        verify_imported_evidence(artifact)
        validate_observation_metadata(artifact.document, artifact.input_name)
    except Exception as exc:
        raise ContractError(
            ["Evidence does not satisfy the public Core 0.12.2 contract"]
        ) from exc

    document = artifact.document
    errors: list[str] = []
    if document.get("evidence_type") != PUBLIC_RENDER_EVIDENCE_TYPE:
        errors.append(f"Evidence type must be {PUBLIC_RENDER_EVIDENCE_TYPE}")
    facts = document.get("facts")
    metadata = document.get("metadata")
    if not isinstance(facts, dict) or not isinstance(metadata, dict):
        raise ContractError(["Evidence facts and metadata must be objects"])
    if set(facts) != PUBLIC_RENDER_FACT_FIELDS:
        errors.append("Evidence facts must contain the exact P2 partitions")

    observation = metadata.get("veritrail_observation")
    collection = metadata.get("github_public_render_collection")
    if not isinstance(observation, dict) or not isinstance(collection, dict):
        raise ContractError(
            ["Evidence must contain observation and public Render metadata"]
        )
    if set(collection) != PUBLIC_RENDER_COLLECTION_FIELDS:
        errors.append("public Render metadata must contain the exact P2 fields")
    if collection.get("schema_version") != "0.1":
        errors.append("public Render collection schema_version must be 0.1")
    if collection.get("access_mode") != "ANONYMOUS_FRESH_CONTEXT":
        errors.append("public Render access_mode must be ANONYMOUS_FRESH_CONTEXT")
    if collection.get("atomic_snapshot_claimed") is not False:
        errors.append("public Render collection must not claim an atomic snapshot")
    elapsed = collection.get("collection_elapsed_ms")
    if not isinstance(elapsed, int) or isinstance(elapsed, bool) or elapsed < 0:
        errors.append("public Render collection elapsed time must be non-negative")
    _validate_collection_shapes(collection, errors)

    expected_observation = {
        "plan_digest": verified_request["plan_digest"],
        "observation_spec_digest": verified_request["observation_spec_digest"],
        "request_seal_digest": verified_request["seal"]["digest"],
        "collector_role": "github-public-render",
        "normalization_semantics_version": (
            PUBLIC_RENDER_NORMALIZATION_SEMANTICS_VERSION
        ),
    }
    for field, expected in expected_observation.items():
        if observation.get(field) != expected:
            errors.append(f"veritrail_observation.{field} does not match request")

    expected_collection = {
        "request_id": verified_request["request_id"],
        "request_seal_digest": verified_request["seal"]["digest"],
        "render_policy_digest": verified_request["render_policy_digest"],
    }
    for field, expected in expected_collection.items():
        if collection.get(field) != expected:
            errors.append(f"public Render collection {field} does not match request")
    if collection.get("collection_session_id") != observation.get(
        "collection_session_id"
    ):
        errors.append("public Render session identities differ")
    session_id = collection.get("collection_session_id")
    if not isinstance(session_id, str) or not _SESSION_ID_PATTERN.fullmatch(
        session_id
    ):
        errors.append("public Render collection_session_id is invalid")

    target = facts.get("target")
    expected_target = {
        "target_kind": verified_request["observation_spec"]["coordinates"][
            "target_kind"
        ],
        "source_coordinates": verified_request["observation_spec"]["coordinates"],
    }
    if target != expected_target:
        errors.append("facts.target does not match the sealed source coordinates")
    _validate_fact_shapes(verified_request, facts, errors)

    expected_digest = public_render_facts_digest(
        observation_spec_digest_value=verified_request["observation_spec_digest"],
        source_coordinates=verified_request["observation_spec"]["coordinates"],
        facts=facts,
    )
    if observation.get("facts_digest") != expected_digest:
        errors.append("veritrail_observation.facts_digest does not match facts")

    coverage, reasons = expected_public_render_coverage(
        verified_request, facts, collection
    )
    if observation.get("coverage") != coverage:
        errors.append("veritrail_observation.coverage does not match observations")
    if collection.get("coverage_reasons") != reasons:
        errors.append("public Render coverage_reasons are not deterministic")
    if observation.get("coverage") == "NOT_APPLICABLE":
        errors.append("P2 0.1 must not produce NOT_APPLICABLE")

    forbidden = _find_forbidden_field(facts)
    if forbidden:
        errors.append(f"facts contains plugin-owned Verdict-like field: {forbidden}")
    if errors:
        raise ContractError(errors)


def _validate_collection_shapes(
    collection: Mapping[str, Any], errors: list[str]
) -> None:
    runtime = collection.get("browser_runtime")
    if runtime != {} and (
        not isinstance(runtime, dict) or set(runtime) != _BROWSER_RUNTIME_FIELDS
    ):
        errors.append("public Render browser_runtime has unsupported fields")
    elif isinstance(runtime, dict) and any(
        not isinstance(value, str) or not value for value in runtime.values()
    ):
        errors.append("public Render browser_runtime values must be non-empty text")
    initial = collection.get("initial_state_check")
    if initial != {} and (
        not isinstance(initial, dict) or set(initial) != _INITIAL_STATE_FIELDS
    ):
        errors.append("public Render initial_state_check has unsupported fields")
    post = collection.get("post_navigation_state")
    if post is not None and (
        not isinstance(post, dict) or set(post) != _POST_STATE_FIELDS
    ):
        errors.append("public Render post_navigation_state has unsupported fields")
    elif isinstance(post, dict):
        for field in _POST_STATE_FIELDS - {"same_site_counts"}:
            if not _is_non_negative_int(post.get(field)):
                errors.append(f"public Render post_navigation_state.{field} is invalid")
        same_site = post.get("same_site_counts")
        if not isinstance(same_site, dict) or set(same_site) != {
            "Strict",
            "Lax",
            "None",
            "Unknown",
        } or not _valid_count_map(same_site):
            errors.append("public Render same_site_counts is invalid")
    network = collection.get("network_summary")
    if not isinstance(network, dict) or set(network) != _NETWORK_SUMMARY_FIELDS:
        errors.append("public Render network_summary has unsupported fields")
    elif not all(
        _is_non_negative_int(network.get(field))
        for field in _NETWORK_SUMMARY_FIELDS - {"reason_counts"}
    ):
        errors.append("public Render network_summary counts are invalid")
    elif network.get("request_count") != (
        network.get("allowed_count") + network.get("blocked_count")
    ):
        errors.append("public Render network_summary totals are inconsistent")
    elif not _valid_count_map(network.get("reason_counts")):
        errors.append("public Render network reason_counts is invalid")
    response_body = collection.get("response_body_observation")
    if response_body is not None and (
        not isinstance(response_body, dict)
        or set(response_body) != _RESPONSE_BODY_FIELDS
    ):
        errors.append("public Render response_body_observation has unsupported fields")
    elif isinstance(response_body, dict):
        for field in _RESPONSE_BODY_FIELDS - {
            "failure",
            "response_error_reason_counts",
        }:
            if not _is_non_negative_int(response_body.get(field)):
                errors.append(f"public Render response body {field} is invalid")
        if not _valid_count_map(response_body.get("response_error_reason_counts")):
            errors.append("public Render response error counts are invalid")
        if response_body.get("failure") is not None and not isinstance(
            response_body.get("failure"), str
        ):
            errors.append("public Render response body failure is invalid")
    runtime_events = collection.get("runtime_events")
    if not isinstance(runtime_events, dict) or set(runtime_events) != _RUNTIME_EVENT_FIELDS:
        errors.append("public Render runtime_events has unsupported fields")
    elif (
        not _valid_count_map(runtime_events.get("console_categories"))
        or not _is_non_negative_int(runtime_events.get("page_error_count"))
        or not _valid_count_map(runtime_events.get("request_failure_categories"))
    ):
        errors.append("public Render runtime event counts are invalid")

    phases = collection.get("phase_observations")
    if not isinstance(phases, list):
        errors.append("public Render phase_observations must be an array")
    else:
        sequences: list[int] = []
        for index, phase in enumerate(phases):
            if not isinstance(phase, dict) or set(phase) != _PHASE_FIELDS:
                errors.append(
                    f"public Render phase_observations[{index}] has invalid fields"
                )
                continue
            sequence = phase.get("sequence")
            elapsed = phase.get("elapsed_ms_monotonic")
            if not isinstance(sequence, int) or isinstance(sequence, bool):
                errors.append(
                    f"public Render phase_observations[{index}] sequence is invalid"
                )
            else:
                sequences.append(sequence)
            if phase.get("outcome") not in {"OBSERVED", "ERROR"}:
                errors.append(
                    f"public Render phase_observations[{index}] outcome is invalid"
                )
            if not isinstance(elapsed, int) or isinstance(elapsed, bool) or elapsed < 0:
                errors.append(
                    f"public Render phase_observations[{index}] elapsed is invalid"
                )
            if not isinstance(phase.get("phase"), str) or not phase.get("phase"):
                errors.append(
                    f"public Render phase_observations[{index}] phase is invalid"
                )
        if sequences != list(range(1, len(phases) + 1)):
            errors.append("public Render phase sequence is not contiguous")

    collection_errors = collection.get("errors")
    if not isinstance(collection_errors, list):
        errors.append("public Render errors must be an array")
    else:
        for index, error in enumerate(collection_errors):
            if not isinstance(error, dict) or set(error) != _ERROR_FIELDS:
                errors.append(f"public Render errors[{index}] has invalid fields")
            elif error.get("fatal") not in {True, False}:
                errors.append(f"public Render errors[{index}] fatal is invalid")
            elif not isinstance(error.get("phase"), str) or not isinstance(
                error.get("code"), str
            ):
                errors.append(f"public Render errors[{index}] identity is invalid")
    cleanup_errors = collection.get("cleanup_errors")
    if not isinstance(cleanup_errors, list) or any(
        not isinstance(item, str) for item in cleanup_errors
    ):
        errors.append("public Render cleanup_errors must be a string array")
    coverage_reasons = collection.get("coverage_reasons")
    if not isinstance(coverage_reasons, list) or any(
        not isinstance(item, str) for item in coverage_reasons
    ):
        errors.append("public Render coverage_reasons must be a string array")


def _validate_fact_shapes(
    request: Mapping[str, Any], facts: Mapping[str, Any], errors: list[str]
) -> None:
    projections = set(request["observation_spec"]["projections"])
    navigation = facts.get("navigation")
    if "navigation.identity" not in projections and navigation is not None:
        errors.append("unrequested public Render navigation facts are present")
    if navigation is not None:
        expected_navigation_fields = {
            "requested_url",
            "redirect_chain",
            "final_url",
            "top_level_http_status",
            "media_type",
        }
        if not isinstance(navigation, dict) or set(navigation) != expected_navigation_fields:
            errors.append("public Render navigation facts have unsupported fields")
        elif (
            not _is_non_negative_int(navigation.get("top_level_http_status"))
            or navigation.get("top_level_http_status") > 599
            or navigation.get("top_level_http_status") < 100
        ):
            errors.append("public Render top-level HTTP status is invalid")
        else:
            if not _valid_safe_url(navigation.get("requested_url")):
                errors.append("public Render requested URL facts are invalid")
            if not _valid_safe_url(navigation.get("final_url")):
                errors.append("public Render final URL facts are invalid")
            chain = navigation.get("redirect_chain")
            if not isinstance(chain, list) or any(
                not isinstance(item, dict)
                or set(item) != {"url", "http_status"}
                or not _valid_safe_url(item.get("url"))
                or (
                    item.get("http_status") is not None
                    and not _is_non_negative_int(item.get("http_status"))
                )
                for item in chain
            ):
                errors.append("public Render redirect chain is invalid")

    document = facts.get("document")
    if "document.identity" not in projections and document is not None:
        errors.append("unrequested public Render document facts are present")
    if document is not None and (
        not isinstance(document, dict)
        or set(document) != {"title", "html_lang"}
        or not isinstance(document.get("title"), str)
        or (
            document.get("html_lang") is not None
            and not isinstance(document.get("html_lang"), str)
        )
    ):
        errors.append("public Render document facts have unsupported fields")

    content_requested = any(item.startswith("content.") for item in projections)
    content = facts.get("content")
    if not content_requested and content is not None:
        errors.append("unrequested public Render content facts are present")
    if content_requested and isinstance(content, dict):
        if set(content) != {"scope", "window"}:
            errors.append("public Render content facts have unsupported fields")
        scope = content.get("scope")
        if scope is not None:
            if not isinstance(scope, dict) or set(scope) != {
                "profile",
                "observed_count",
                "usable",
            }:
                errors.append("public Render scope facts have unsupported fields")
            elif (
                scope.get("profile")
                != request["observation_spec"]["coordinates"]["target_kind"]
                or not _is_non_negative_int(scope.get("observed_count"))
                or scope.get("usable") not in {True, False}
            ):
                errors.append("public Render scope facts are invalid")
        window = content.get("window")
        if window is not None:
            if not isinstance(window, dict) or set(window) != {
                "samples_stable",
                "sample_digests",
                "stable_facts",
                "truncations",
            }:
                errors.append("public Render content window has unsupported fields")
            else:
                digests = window.get("sample_digests")
                valid_digests = (
                    isinstance(digests, list)
                    and len(digests) == 3
                    and all(
                        isinstance(item, str)
                        and len(item) == 64
                        and all(
                            character in "0123456789abcdef" for character in item
                        )
                        for item in digests
                    )
                )
                if not valid_digests:
                    errors.append("public Render sample digests are invalid")
                stable = window.get("samples_stable")
                if stable not in {True, False}:
                    errors.append("public Render sample stability is invalid")
                if stable is True and (
                    not valid_digests
                    or len(set(digests)) != 1
                    or not isinstance(window.get("stable_facts"), dict)
                ):
                    errors.append("stable public Render window is inconsistent")
                if stable is False and window.get("stable_facts") is not None:
                    errors.append("unstable public Render window selected sample facts")
                if stable is True and isinstance(window.get("stable_facts"), dict):
                    expected_stable_fields = {
                        field
                        for projection, field in {
                            "content.headings": "headings",
                            "content.links": "links",
                            "content.literal_markers": "literal_markers",
                            "content.rendered_text_signature": (
                                "rendered_text_signature"
                            ),
                        }.items()
                        if projection in projections
                    }
                    if set(window["stable_facts"]) != expected_stable_fields:
                        errors.append(
                            "stable public Render facts do not match projections"
                        )
                if not isinstance(window.get("truncations"), list):
                    errors.append("public Render truncations must be an array")

    conflicts = facts.get("conflicts")
    if not isinstance(conflicts, list) or any(
        not isinstance(item, dict) or not isinstance(item.get("code"), str)
        for item in conflicts
    ):
        errors.append("public Render conflicts must be coded objects")


def _is_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _valid_count_map(value: Any) -> bool:
    return isinstance(value, dict) and all(
        isinstance(key, str) and key and _is_non_negative_int(count)
        for key, count in value.items()
    )


def _valid_safe_url(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and set(value)
        == {"origin", "host", "path", "query_present", "fragment_present"}
        and isinstance(value.get("origin"), str)
        and isinstance(value.get("host"), str)
        and isinstance(value.get("path"), str)
        and isinstance(value.get("query_present"), bool)
        and isinstance(value.get("fragment_present"), bool)
    )


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
