from __future__ import annotations

import copy
import json
import re
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Mapping
from urllib.parse import parse_qsl, quote, urlencode, urlsplit

from veritrail.canonical import canonical_json_bytes
from veritrail.evidence import ImportedEvidence, import_evidence_document

from veritrail_github.contracts import (
    NORMALIZATION_SEMANTICS_VERSION,
    facts_digest,
    validate_observation_request,
)
from veritrail_github.conformance import verify_github_evidence
from veritrail_github.errors import CollectionError, ContractError, TransportError
from veritrail_github.normalize import (
    annotated_tag_target,
    merge_required_checks,
    normalize_active_rules,
    normalize_branch_protection,
    normalize_commit,
    normalize_observed_checks,
    normalize_pages,
    normalize_pull_request,
    normalize_release,
    normalize_repository,
    ref_target,
)
from veritrail_github.transport import MAX_RESPONSE_BYTES, Transport


_SAFE_HEADER_FIELDS = {
    "etag",
    "x-github-request-id",
    "x-ratelimit-limit",
    "x-ratelimit-remaining",
    "x-ratelimit-reset",
    "x-ratelimit-resource",
    "x-ratelimit-used",
    "retry-after",
    "link",
}

COLLECTOR_IMPLEMENTATION_VERSION = "0.1.0"
PARSER_IMPLEMENTATION_VERSION = "github-rest-parser/0.2"


@dataclass(frozen=True)
class CollectionResult:
    request: dict[str, Any]
    artifact: ImportedEvidence


@dataclass
class _CollectionState:
    started_at: str
    started_monotonic: float
    request_count: int
    sequence: int
    records: list[dict[str, Any]]
    errors: list[dict[str, Any]]
    partial: bool
    fatal: bool
    visibility: str
    permission_observation: str


class _ProbeFailure(Exception):
    def __init__(self, code: str, *, status: int | None = None) -> None:
        self.code = code
        self.status = status
        super().__init__(code)


def _timestamp(clock: Callable[[], datetime]) -> str:
    value = clock()
    if value.tzinfo is None:
        raise CollectionError(
            "collector wall clock must return a timezone-aware datetime"
        )
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_int_header(headers: Mapping[str, str], key: str) -> int | None:
    value = headers.get(key)
    if value is None or not re.fullmatch(r"[0-9]+", value):
        return None
    return int(value)


def _safe_rate_limit(headers: Mapping[str, str]) -> dict[str, Any] | None:
    result = {
        "limit": _safe_int_header(headers, "x-ratelimit-limit"),
        "remaining": _safe_int_header(headers, "x-ratelimit-remaining"),
        "reset_epoch_seconds": _safe_int_header(headers, "x-ratelimit-reset"),
        "used": _safe_int_header(headers, "x-ratelimit-used"),
        "resource": headers.get("x-ratelimit-resource"),
    }
    return result if any(value is not None for value in result.values()) else None


def _returned_identifiers(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    fields = ("id", "node_id", "number", "sha", "full_name", "tag_name", "ref")
    return {
        field: payload[field]
        for field in fields
        if isinstance(payload.get(field), (str, int))
        and not isinstance(payload.get(field), bool)
    }


def _next_link(value: str | None, api_origin: str, expected_path: str) -> str | None:
    if not value:
        return None
    expected = urlsplit(api_origin)
    for part in value.split(","):
        sections = [section.strip() for section in part.split(";")]
        if (
            not sections
            or not sections[0].startswith("<")
            or not sections[0].endswith(">")
        ):
            continue
        if not any(section == 'rel="next"' for section in sections[1:]):
            continue
        parsed = urlsplit(sections[0][1:-1])
        if (
            parsed.scheme.lower() != expected.scheme.lower()
            or (parsed.hostname or "").lower() != (expected.hostname or "").lower()
            or parsed.port != expected.port
            or parsed.username is not None
            or parsed.password is not None
            or parsed.fragment
            or parsed.path != expected_path
        ):
            raise _ProbeFailure("PAGINATION_ORIGIN_MISMATCH")
        query_items = parse_qsl(parsed.query, keep_blank_values=True)
        if len(query_items) != len({key for key, _ in query_items}) or any(
            key not in {"filter", "page", "per_page"} for key, _ in query_items
        ):
            raise _ProbeFailure("PAGINATION_QUERY_UNSAFE")
        return parsed.path + (f"?{parsed.query}" if parsed.query else "")
    return None


def _safe_final_path(final_url: str, api_origin: str) -> str:
    expected = urlsplit(api_origin)
    parsed = urlsplit(final_url)
    if (
        parsed.scheme.lower() != expected.scheme.lower()
        or (parsed.hostname or "").lower() != (expected.hostname or "").lower()
        or parsed.port != expected.port
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or not parsed.path.startswith("/")
    ):
        raise TransportError(
            "transport returned a response outside the frozen API origin"
        )
    query_items = parse_qsl(parsed.query, keep_blank_values=True)
    if len(query_items) > 16 or any(
        key.casefold() in {"access_token", "authorization", "client_secret", "token"}
        for key, _ in query_items
    ):
        raise TransportError("transport returned an unsafe final query")
    return parsed.path + (f"?{parsed.query}" if parsed.query else "")


class GitHubCollector:
    """Strictly serial, read-only P1 GitHub REST collector."""

    def __init__(
        self,
        transport: Transport,
        *,
        token: str | None = None,
        clock: Callable[[], datetime] | None = None,
        monotonic: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        session_id_factory: Callable[[], str] | None = None,
    ) -> None:
        if token is not None and (
            not isinstance(token, str) or not token or "\r" in token or "\n" in token
        ):
            raise ContractError(
                ["runtime token must be a non-empty single-line secret"]
            )
        self._transport = transport
        self._token = token
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._monotonic = monotonic
        self._sleep = sleep
        self._session_id_factory = session_id_factory or (
            lambda: f"github-{uuid.uuid4().hex}"
        )
        self._last_link: str | None = None

    def collect(
        self, plan: dict[str, Any], request: dict[str, Any]
    ) -> CollectionResult:
        verified_request = validate_observation_request(plan, request)
        policy = verified_request["collector_policy"]
        started_monotonic = self._monotonic()
        state = _CollectionState(
            started_at=_timestamp(self._clock),
            started_monotonic=started_monotonic,
            request_count=0,
            sequence=0,
            records=[],
            errors=[],
            partial=False,
            fatal=False,
            visibility="UNKNOWN",
            permission_observation="SUFFICIENT",
        )
        session_id = self._session_id_factory()
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}", session_id):
            raise CollectionError(
                "collection session factory returned an invalid reference"
            )

        spec = verified_request["observation_spec"]
        coordinates = spec["coordinates"]
        projections = set(spec["projections"])
        owner = coordinates["owner"]
        repository = coordinates["repository"]
        target_sha = coordinates["target_commit_sha"]
        repository_path = f"/repos/{quote(owner, safe='')}/{quote(repository, safe='')}"
        conflicts: list[dict[str, Any]] = []
        facts: dict[str, Any] = {
            "repository": None,
            "commit": None,
            "pull_request": None,
            "required_checks": None,
            "observed_checks": None,
            "release": None,
            "tag": None,
            "pages": None,
            "conflicts": conflicts,
        }

        repository_payload = self._fetch(
            state,
            policy,
            "repository",
            repository_path,
            {},
            {"owner": owner, "repository": repository},
            fatal=True,
        )
        default_branch: str | None = coordinates.get("branch")
        if repository_payload is not None:
            try:
                repository_facts, observed_default, visibility = normalize_repository(
                    repository_payload,
                    owner=owner,
                    repository=repository,
                    projections=projections,
                    conflicts=conflicts,
                )
                facts["repository"] = repository_facts
                default_branch = default_branch or observed_default
                state.visibility = visibility
                if (
                    conflicts
                    and conflicts[-1]["code"] == "REPOSITORY_IDENTITY_MISMATCH"
                ):
                    state.fatal = True
            except ContractError:
                self._record_normalization_failure(state, "repository", fatal=True)

        commit_payload = None
        if not state.fatal:
            commit_payload = self._fetch(
                state,
                policy,
                "commit",
                f"{repository_path}/commits/{target_sha}",
                {},
                {"target_commit_sha": target_sha},
                fatal=True,
            )
        if commit_payload is not None:
            try:
                facts["commit"] = normalize_commit(
                    commit_payload,
                    target_commit_sha=target_sha,
                    projected="commit.identity" in projections,
                    conflicts=conflicts,
                )
                if conflicts and conflicts[-1]["code"] == "COMMIT_IDENTITY_MISMATCH":
                    state.fatal = True
            except ContractError:
                self._record_normalization_failure(state, "commit", fatal=True)

        if not state.fatal and "pull_request.merge" in projections:
            number = coordinates["pull_request_number"]
            payload = self._fetch(
                state,
                policy,
                "pull_request",
                f"{repository_path}/pulls/{number}",
                {},
                {"pull_request_number": number},
                fatal=False,
            )
            if payload is not None:
                try:
                    normalized_pull_request = normalize_pull_request(payload)
                    facts["pull_request"] = normalized_pull_request
                    if normalized_pull_request["number"] != number:
                        conflicts.append(
                            {
                                "code": "PULL_REQUEST_IDENTITY_MISMATCH",
                                "expected_number": number,
                                "observed_number": normalized_pull_request["number"],
                            }
                        )
                except ContractError:
                    self._record_normalization_failure(
                        state, "pull_request", fatal=False
                    )

        if not state.fatal and "rules.required_checks" in projections:
            if default_branch is None:
                self._record_error(
                    state,
                    "BRANCH_COORDINATE_UNAVAILABLE",
                    "required_checks",
                    fatal=False,
                )
            else:
                encoded_branch = quote(default_branch, safe="")
                rules_payload = self._fetch_pages(
                    state,
                    policy,
                    "active_rules",
                    f"{repository_path}/rules/branches/{encoded_branch}",
                    {"per_page": policy["per_page"]},
                    {"branch": default_branch},
                    fatal=False,
                    mode="list",
                )
                required_check_occurrences: list[dict[str, Any]] = []
                rules_observed = rules_payload is not None
                if rules_payload is not None:
                    try:
                        required_check_occurrences.extend(
                            normalize_active_rules(rules_payload)
                        )
                    except ContractError:
                        rules_observed = False
                        self._record_normalization_failure(
                            state, "active_rules", fatal=False
                        )
                protection_payload = self._fetch(
                    state,
                    policy,
                    "required_status_protection",
                    f"{repository_path}/branches/{encoded_branch}/protection/required_status_checks",
                    {},
                    {"branch": default_branch},
                    fatal=False,
                )
                protection_observed = protection_payload is not None
                if protection_payload is not None:
                    try:
                        required_check_occurrences.extend(
                            normalize_branch_protection(protection_payload)
                        )
                    except ContractError:
                        protection_observed = False
                        self._record_normalization_failure(
                            state, "required_status_protection", fatal=False
                        )
                if rules_observed or protection_observed:
                    facts["required_checks"] = {
                        "branch": default_branch,
                        "items": merge_required_checks(
                            required_check_occurrences, conflicts
                        ),
                    }

        if not state.fatal and "checks.observed_runs" in projections:
            check_runs = self._fetch_pages(
                state,
                policy,
                "check_runs",
                f"{repository_path}/commits/{target_sha}/check-runs",
                {"filter": "all", "per_page": policy["per_page"]},
                {"target_commit_sha": target_sha},
                fatal=False,
                mode="check_runs",
            )
            statuses = self._fetch_pages(
                state,
                policy,
                "combined_status",
                f"{repository_path}/commits/{target_sha}/status",
                {"per_page": policy["per_page"]},
                {"target_commit_sha": target_sha},
                fatal=False,
                mode="statuses",
            )
            if check_runs is not None and statuses is not None:
                try:
                    facts["observed_checks"] = normalize_observed_checks(
                        check_runs,
                        statuses,
                        target_commit_sha=target_sha,
                        conflicts=conflicts,
                    )
                except ContractError:
                    self._record_normalization_failure(
                        state, "observed_checks", fatal=False
                    )

        if not state.fatal and projections.intersection(
            {"release.identity", "release.assets"}
        ):
            release_tag = coordinates["release_tag"]
            release_payload = self._fetch(
                state,
                policy,
                "release",
                f"{repository_path}/releases/tags/{quote(release_tag, safe='')}",
                {},
                {"release_tag": release_tag},
                fatal=False,
            )
            if release_payload is not None:
                try:
                    normalized_release = normalize_release(
                        release_payload,
                        include_identity="release.identity" in projections,
                        include_assets="release.assets" in projections,
                        conflicts=conflicts,
                    )
                    facts["release"] = normalized_release
                    observed_tag = (
                        release_payload.get("tag_name")
                        if isinstance(release_payload, dict)
                        else None
                    )
                    if observed_tag != release_tag:
                        conflicts.append(
                            {
                                "code": "RELEASE_TAG_IDENTITY_MISMATCH",
                                "expected_tag": release_tag,
                                "observed_tag": observed_tag,
                            }
                        )
                except ContractError:
                    self._record_normalization_failure(state, "release", fatal=False)

        if not state.fatal and "tag.peeled_commit" in projections:
            normalized_tag = self._collect_tag(
                state,
                policy,
                repository_path,
                coordinates["release_tag"],
            )
            facts["tag"] = normalized_tag
            if (
                normalized_tag is not None
                and normalized_tag["peeled_commit_sha"] != target_sha
            ):
                conflicts.append(
                    {
                        "code": "TAG_TARGET_COMMIT_MISMATCH",
                        "expected_sha": target_sha,
                        "observed_sha": normalized_tag["peeled_commit_sha"],
                    }
                )

        if not state.fatal and "pages.metadata" in projections:
            pages_payload = self._fetch(
                state,
                policy,
                "pages",
                f"{repository_path}/pages",
                {},
                {},
                fatal=False,
            )
            if pages_payload is not None:
                try:
                    facts["pages"] = normalize_pages(pages_payload)
                except ContractError:
                    self._record_normalization_failure(state, "pages", fatal=False)

        conflicts.sort(key=canonical_json_bytes)
        if conflicts:
            state.partial = True
        completed_at = _timestamp(self._clock)
        elapsed_ms = max(0, int((self._monotonic() - started_monotonic) * 1000))
        coverage = (
            "ERROR" if state.fatal else ("PARTIAL" if state.partial else "COMPLETE")
        )
        fact_identity = facts_digest(
            observation_spec_digest_value=verified_request["observation_spec_digest"],
            source_coordinates=coordinates,
            facts=facts,
        )
        access_mode = "AUTHENTICATED_READ_ONLY" if self._token else "ANONYMOUS"
        document = {
            "schema_version": "0.1",
            "evidence_type": "platform.github.api.snapshot",
            "source": "veritrail-github-evidence/0.1",
            "captured_at": completed_at,
            "facts": facts,
            "metadata": {
                "veritrail_observation": {
                    "schema_version": "0.1",
                    "canonicalization_profile": "veritrail-json-c14n/1",
                    "plan_digest": verified_request["plan_digest"],
                    "observation_spec_digest": verified_request[
                        "observation_spec_digest"
                    ],
                    "request_seal_digest": verified_request["seal"]["digest"],
                    "collection_session_id": session_id,
                    "collector_role": "github-api",
                    "coverage": coverage,
                    "normalization_semantics_version": NORMALIZATION_SEMANTICS_VERSION,
                    "facts_digest": fact_identity,
                },
                "github_collection": {
                    "schema_version": "0.1",
                    "request_id": verified_request["request_id"],
                    "request_seal_digest": verified_request["seal"]["digest"],
                    "collector_policy_digest": verified_request[
                        "collector_policy_digest"
                    ],
                    "collection_session_id": session_id,
                    "collection_started_at": state.started_at,
                    "collection_completed_at": completed_at,
                    "collection_elapsed_ms": elapsed_ms,
                    "access_mode": access_mode,
                    "visibility": state.visibility,
                    "permission_observation": state.permission_observation,
                    "api_origin": policy["api_origin"],
                    "api_version": policy["api_version"],
                    "collector_version": COLLECTOR_IMPLEMENTATION_VERSION,
                    "parser_version": PARSER_IMPLEMENTATION_VERSION,
                    "probes": state.records,
                    "errors": state.errors,
                    "atomic_snapshot_claimed": False,
                },
            },
        }
        artifact = import_evidence_document(
            document, f"github-{verified_request['request_id']}.json"
        )
        verify_github_evidence(plan, verified_request, artifact)
        return CollectionResult(request=verified_request, artifact=artifact)

    def _headers(self, policy: dict[str, Any]) -> dict[str, str]:
        headers = {
            "Accept": policy["accept"],
            "User-Agent": policy["user_agent"],
            "X-GitHub-Api-Version": policy["api_version"],
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _budget_remaining(
        self, state: _CollectionState, policy: dict[str, Any]
    ) -> bool:
        elapsed_ms = int((self._monotonic() - state.started_monotonic) * 1000)
        return (
            elapsed_ms < policy["total_collection_timeout_ms"]
            and state.request_count < policy["max_total_requests"]
        )

    def _fetch(
        self,
        state: _CollectionState,
        policy: dict[str, Any],
        probe_id: str,
        path: str,
        query: dict[str, Any],
        operands: dict[str, Any],
        *,
        fatal: bool,
        page_number: int = 1,
    ) -> Any | None:
        safe_query = urlencode(
            sorted((key, str(value)) for key, value in query.items())
        )
        path_and_query = path + (f"?{safe_query}" if safe_query else "")
        return self._fetch_path(
            state,
            policy,
            probe_id,
            path_and_query,
            operands,
            fatal=fatal,
            page_number=page_number,
        )

    def _fetch_path(
        self,
        state: _CollectionState,
        policy: dict[str, Any],
        probe_id: str,
        path_and_query: str,
        operands: dict[str, Any],
        *,
        fatal: bool,
        page_number: int,
    ) -> Any | None:
        state.sequence += 1
        sequence = state.sequence
        logical_start = self._monotonic()
        attempts: list[dict[str, Any]] = []
        response_status: int | None = None
        response_headers: dict[str, str] = {}
        self._last_link = None
        final_path_and_query: str | None = None
        payload: Any | None = None
        outcome = "ERROR"
        error_code = "UNKNOWN_ERROR"

        for attempt in range(1, policy["max_attempts_per_request"] + 1):
            if not self._budget_remaining(state, policy):
                error_code = "COLLECTION_BUDGET_EXHAUSTED"
                break
            state.request_count += 1
            attempt_started = self._monotonic()
            observed_at = _timestamp(self._clock)
            try:
                response = self._transport.get(
                    api_origin=policy["api_origin"],
                    path_and_query=path_and_query,
                    headers=self._headers(policy),
                    connect_timeout_ms=policy["connect_timeout_ms"],
                    read_timeout_ms=policy["read_timeout_ms"],
                    max_redirects=policy["max_redirects"],
                )
                response_status = response.status
                final_path_and_query = _safe_final_path(
                    response.final_url, policy["api_origin"]
                )
                if len(response.body) > MAX_RESPONSE_BYTES:
                    raise TransportError(
                        "transport returned a response beyond the body limit"
                    )
                response_headers = {
                    key.lower(): value
                    for key, value in response.headers.items()
                    if key.lower() in _SAFE_HEADER_FIELDS
                }
                self._last_link = response_headers.get("link")
                attempts.append(
                    {
                        "attempt": attempt,
                        "observed_at": observed_at,
                        "http_status": response_status,
                        "elapsed_ms_monotonic": max(
                            0, int((self._monotonic() - attempt_started) * 1000)
                        ),
                    }
                )
                if response_status == 200:
                    try:
                        payload = json.loads(response.body.decode("utf-8"))
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        error_code = "RESPONSE_JSON_INVALID"
                        break
                    outcome = "SUCCESS"
                    error_code = ""
                    break
                rate_limited = self._is_rate_limited(
                    response_status, response_headers, response.body
                )
                error_code = self._http_error_code(
                    response_status, rate_limited=rate_limited
                )
                if not self._should_retry(
                    response_status, response_headers, rate_limited=rate_limited
                ):
                    break
            except TransportError:
                response_status = None
                response_headers = {}
                final_path_and_query = None
                self._last_link = None
                attempts.append(
                    {
                        "attempt": attempt,
                        "observed_at": observed_at,
                        "http_status": None,
                        "elapsed_ms_monotonic": max(
                            0, int((self._monotonic() - attempt_started) * 1000)
                        ),
                    }
                )
                error_code = "NETWORK_ERROR"
            if attempt < policy["max_attempts_per_request"]:
                delay_ms = self._retry_delay_ms(
                    attempt, response_status, response_headers, policy
                )
                elapsed_ms = int((self._monotonic() - state.started_monotonic) * 1000)
                if elapsed_ms + delay_ms >= policy["total_collection_timeout_ms"]:
                    error_code = "COLLECTION_BUDGET_EXHAUSTED"
                    break
                self._sleep(delay_ms / 1000)

        if outcome != "SUCCESS":
            self._record_error(
                state,
                error_code,
                probe_id,
                fatal=fatal
                or error_code
                in {
                    "AUTHENTICATION_FAILED",
                    "RATE_LIMITED",
                    "NOT_MODIFIED_WITHOUT_BOUND_EVIDENCE",
                    "COLLECTION_BUDGET_EXHAUSTED",
                    "RESPONSE_JSON_INVALID",
                    "NETWORK_ERROR",
                    "SERVER_ERROR",
                },
                status=response_status,
            )

        state.records.append(
            {
                "sequence": sequence,
                "probe_id": probe_id,
                "observed_at": attempts[-1]["observed_at"]
                if attempts
                else _timestamp(self._clock),
                "method": "GET",
                "actual_path_and_safe_query": path_and_query,
                "final_path_and_safe_query": final_path_and_query,
                "actual_operands": copy.deepcopy(operands),
                "http_status": response_status,
                "returned_identifiers": _returned_identifiers(payload),
                "etag_if_available": response_headers.get("etag"),
                "github_request_id_if_available": response_headers.get(
                    "x-github-request-id"
                ),
                "rate_limit_metadata_if_available": _safe_rate_limit(response_headers),
                "page_count": page_number,
                "attempt_count": len(attempts),
                "elapsed_ms_monotonic": max(
                    0, int((self._monotonic() - logical_start) * 1000)
                ),
                "outcome": outcome if outcome == "SUCCESS" else error_code,
                "attempt_observations": attempts,
            }
        )
        return payload

    def _fetch_pages(
        self,
        state: _CollectionState,
        policy: dict[str, Any],
        probe_id: str,
        path: str,
        query: dict[str, Any],
        operands: dict[str, Any],
        *,
        fatal: bool,
        mode: str,
    ) -> Any | None:
        safe_query = urlencode(
            sorted((key, str(value)) for key, value in query.items())
        )
        next_path = path + (f"?{safe_query}" if safe_query else "")
        pages: list[Any] = []
        for page_number in range(1, policy["max_pages_per_probe"] + 1):
            before = len(state.records)
            payload = self._fetch_path(
                state,
                policy,
                probe_id,
                next_path,
                operands,
                fatal=fatal,
                page_number=page_number,
            )
            if payload is None:
                return None
            pages.append(payload)
            headers_link = None
            if len(state.records) <= before:
                return None
            # Link is used transiently but not retained because it is a
            # URL-bearing transport detail rather than a normalized fact.
            headers_link = getattr(self, "_last_link", None)
            self._last_link = None
            try:
                candidate = _next_link(headers_link, policy["api_origin"], path)
            except _ProbeFailure as exc:
                self._record_error(state, exc.code, probe_id, fatal=fatal)
                return None
            if candidate is None:
                break
            next_path = candidate
        else:
            if next_path is not None:
                self._record_error(
                    state, "PAGINATION_LIMIT_REACHED", probe_id, fatal=False
                )

        if mode == "list":
            combined: list[Any] = []
            for page in pages:
                if not isinstance(page, list):
                    self._record_normalization_failure(state, probe_id, fatal=fatal)
                    return None
                combined.extend(page)
            return combined
        key = "check_runs" if mode == "check_runs" else "statuses"
        combined_items: list[Any] = []
        root: dict[str, Any] | None = None
        for page in pages:
            if not isinstance(page, dict) or not isinstance(page.get(key), list):
                self._record_normalization_failure(state, probe_id, fatal=fatal)
                return None
            root = root or copy.deepcopy(page)
            combined_items.extend(page[key])
        if root is None:
            self._record_normalization_failure(state, probe_id, fatal=fatal)
            return None
        root[key] = combined_items
        if key == "check_runs":
            root["total_count"] = len(combined_items)
        return root

    def _collect_tag(
        self,
        state: _CollectionState,
        policy: dict[str, Any],
        repository_path: str,
        release_tag: str,
    ) -> dict[str, Any] | None:
        payload = self._fetch(
            state,
            policy,
            "tag_ref",
            f"{repository_path}/git/ref/tags/{quote(release_tag, safe='')}",
            {},
            {"release_tag": release_tag},
            fatal=False,
        )
        if payload is None:
            return None
        try:
            ref_name, object_type, object_sha = ref_target(payload)
        except ContractError:
            self._record_normalization_failure(state, "tag_ref", fatal=False)
            return None
        expected_ref = f"refs/tags/{release_tag}"
        if ref_name != expected_ref:
            self._record_error(
                state, "TAG_REF_IDENTITY_MISMATCH", "tag_ref", fatal=False
            )
            return None
        chain = [{"object_type": object_type, "object_sha": object_sha}]
        seen = {object_sha}
        current_type = object_type
        current_sha = object_sha
        for depth in range(5):
            if current_type == "commit":
                return {
                    "ref": ref_name,
                    "ref_target_sha": object_sha,
                    "object_type": object_type,
                    "peel_chain": chain,
                    "peeled_commit_sha": current_sha,
                }
            if current_type != "tag":
                self._record_error(
                    state, "TAG_TARGET_NOT_COMMIT", "tag_peel", fatal=False
                )
                return None
            tag_payload = self._fetch(
                state,
                policy,
                "tag_peel",
                f"{repository_path}/git/tags/{current_sha}",
                {},
                {"tag_object_sha": current_sha, "depth": depth + 1},
                fatal=False,
            )
            if tag_payload is None:
                return None
            try:
                response_sha, current_type, current_sha = annotated_tag_target(
                    tag_payload
                )
            except ContractError:
                self._record_normalization_failure(state, "tag_peel", fatal=False)
                return None
            if response_sha != chain[-1]["object_sha"]:
                self._record_error(
                    state, "TAG_OBJECT_IDENTITY_MISMATCH", "tag_peel", fatal=False
                )
                return None
            if current_sha in seen:
                self._record_error(state, "TAG_PEEL_CYCLE", "tag_peel", fatal=False)
                return None
            seen.add(current_sha)
            chain.append({"object_type": current_type, "object_sha": current_sha})
            if current_type == "commit":
                return {
                    "ref": ref_name,
                    "ref_target_sha": object_sha,
                    "object_type": object_type,
                    "peel_chain": chain,
                    "peeled_commit_sha": current_sha,
                }
        self._record_error(state, "TAG_PEEL_LIMIT_REACHED", "tag_peel", fatal=False)
        return None

    def _retry_delay_ms(
        self,
        attempt: int,
        status: int | None,
        headers: Mapping[str, str],
        policy: dict[str, Any],
    ) -> int:
        retry_after = headers.get("retry-after") if status in {403, 429} else None
        if retry_after and re.fullmatch(r"[0-9]+", retry_after):
            return min(int(retry_after) * 1000, policy["total_collection_timeout_ms"])
        if retry_after:
            try:
                parsed = parsedate_to_datetime(retry_after)
                delta = parsed.timestamp() - self._clock().timestamp()
                return min(
                    max(0, int(delta * 1000)), policy["total_collection_timeout_ms"]
                )
            except (TypeError, ValueError, OverflowError):
                pass
        if status == 403 and headers.get("x-ratelimit-remaining") == "0":
            reset = headers.get("x-ratelimit-reset")
            if reset and re.fullmatch(r"[0-9]+", reset):
                delta = int(reset) - int(self._clock().timestamp())
                return min(max(0, delta * 1000), policy["total_collection_timeout_ms"])
        schedule = policy["retry_schedule_ms"]
        return schedule[min(attempt - 1, len(schedule) - 1)]

    @staticmethod
    def _should_retry(
        status: int,
        headers: Mapping[str, str],
        *,
        rate_limited: bool,
    ) -> bool:
        if status == 429 or 500 <= status <= 599:
            return True
        if status == 403:
            return rate_limited
        return False

    @staticmethod
    def _is_rate_limited(status: int, headers: Mapping[str, str], body: bytes) -> bool:
        if status == 429:
            return True
        if status != 403:
            return False
        if headers.get("x-ratelimit-remaining") == "0" or "retry-after" in headers:
            return True
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return False
        message = payload.get("message") if isinstance(payload, dict) else None
        return isinstance(message, str) and "rate limit" in message.casefold()

    @staticmethod
    def _http_error_code(
        status: int,
        *,
        rate_limited: bool,
    ) -> str:
        if status == 401:
            return "AUTHENTICATION_FAILED"
        if status == 403 and rate_limited:
            return "RATE_LIMITED"
        if status == 403:
            return "PERMISSION_INSUFFICIENT"
        if status == 404:
            return "NOT_VISIBLE_OR_NOT_FOUND"
        if status == 429:
            return "RATE_LIMITED"
        if status == 304:
            return "NOT_MODIFIED_WITHOUT_BOUND_EVIDENCE"
        if 500 <= status <= 599:
            return "SERVER_ERROR"
        return "HTTP_ERROR"

    def _record_error(
        self,
        state: _CollectionState,
        code: str,
        probe_id: str,
        *,
        fatal: bool,
        status: int | None = None,
    ) -> None:
        state.errors.append(
            {
                "code": code,
                "probe_id": probe_id,
                "http_status": status,
            }
        )
        state.fatal = state.fatal or fatal
        state.partial = state.partial or not fatal
        if code in {"AUTHENTICATION_FAILED", "PERMISSION_INSUFFICIENT"}:
            state.permission_observation = "INSUFFICIENT"
        elif code == "NOT_VISIBLE_OR_NOT_FOUND":
            state.permission_observation = "UNKNOWN"

    def _record_normalization_failure(
        self, state: _CollectionState, probe_id: str, *, fatal: bool
    ) -> None:
        self._record_error(state, "SOURCE_SEMANTICS_INVALID", probe_id, fatal=fatal)
