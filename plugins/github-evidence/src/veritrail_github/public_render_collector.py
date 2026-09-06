from __future__ import annotations

import copy
import re
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from veritrail.canonical import canonical_json_bytes
from veritrail.evidence import ImportedEvidence, import_evidence_document

from veritrail_github.errors import CollectionError
from veritrail_github.public_render_browser import (
    BrowserSessionSnapshot,
    FreshContextRejected,
    PublicRenderBrowserError,
    RenderBrowserSession,
    RenderDeadlineExceeded,
    RenderNavigationFailed,
)
from veritrail_github.public_render_conformance import (
    expected_public_render_coverage,
    verify_public_render_evidence,
)
from veritrail_github.public_render_content import (
    ContentWindow,
    PublicRenderContentError,
    collect_content_window,
    collect_document_identity,
)
from veritrail_github.public_render_contracts import (
    PUBLIC_RENDER_EVIDENCE_TYPE,
    PUBLIC_RENDER_NORMALIZATION_SEMANTICS_VERSION,
    public_render_facts_digest,
    validate_public_render_request,
)
from veritrail_github.public_render_network import PublicRenderNetworkError
from veritrail_github.public_render_runtime import (
    RenderRuntimeUnavailable,
    preflight_render_runtime,
)


PUBLIC_RENDER_COLLECTOR_IMPLEMENTATION_VERSION = "0.1.0"
PUBLIC_RENDER_PARSER_IMPLEMENTATION_VERSION = "github-public-render-parser/0.1"
_SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")


@dataclass(frozen=True)
class PublicRenderCollectionResult:
    request: dict[str, Any]
    artifact: ImportedEvidence


class PublicRenderCollector:
    """Collect one bounded, anonymous GitHub public Render observation."""

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        monotonic: Callable[[], float] = time.monotonic,
        session_id_factory: Callable[[], str] | None = None,
        browser_session_factory: Callable[[Mapping[str, Any]], Any] | None = None,
        playwright_factory: Any | None = None,
        runtime_preflight: Any = preflight_render_runtime,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._monotonic = monotonic
        self._session_id_factory = session_id_factory or (
            lambda: f"github-render-{uuid.uuid4().hex}"
        )
        self._browser_session_factory = browser_session_factory
        self._playwright_factory = playwright_factory
        self._runtime_preflight = runtime_preflight

    def collect(
        self, plan: dict[str, Any], request: dict[str, Any]
    ) -> PublicRenderCollectionResult:
        verified_request = validate_public_render_request(plan, request)
        session_id = self._session_id_factory()
        if not isinstance(session_id, str) or not _SESSION_ID_PATTERN.fullmatch(
            session_id
        ):
            raise CollectionError(
                "public Render session factory returned an invalid reference"
            )

        started_at = _timestamp(self._clock)
        started_monotonic = self._monotonic()
        phases: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        session: Any | None = None
        browser_snapshot: BrowserSessionSnapshot | None = None
        document: dict[str, Any] | None = None
        content_window: ContentWindow | None = None
        projections = frozenset(
            verified_request["observation_spec"]["projections"]
        )
        content_requested = any(item.startswith("content.") for item in projections)

        try:
            session = self._create_browser_session(verified_request)
        except Exception as error:
            _record_error(errors, "session-create", error, fatal=True)

        if session is not None:
            try:
                self._observe_phase(phases, "open", session.open)
            except Exception as error:
                _record_error(errors, "open", error, fatal=True)
            else:
                try:
                    self._observe_phase(phases, "navigation", session.navigate)
                except Exception as error:
                    _record_error(errors, "navigation", error, fatal=True)
                else:
                    if "document.identity" in projections:
                        try:
                            document = self._observe_phase(
                                phases,
                                "document-identity",
                                lambda: collect_document_identity(
                                    session.page,
                                    timeout_ms=session.bounded_timeout_ms(
                                        verified_request["render_policy"][
                                            "scope_timeout_ms"
                                        ]
                                    ),
                                ),
                            )
                        except Exception as error:
                            _record_error(
                                errors,
                                "document-identity",
                                error,
                                fatal=False,
                            )

                    if content_requested:
                        scope_observed = False
                        try:
                            scope = self._observe_phase(
                                phases, "fixed-scope", session.locate_fixed_scope
                            )
                            scope_observed = scope is not None and scope.usable
                        except Exception as error:
                            _record_error(
                                errors, "fixed-scope", error, fatal=False
                            )
                        if scope_observed:
                            try:
                                content_window = self._observe_phase(
                                    phases,
                                    "content-window",
                                    lambda: collect_content_window(
                                        session, verified_request
                                    ),
                                )
                            except Exception as error:
                                _record_error(
                                    errors,
                                    "content-window",
                                    error,
                                    fatal=False,
                                )
                    try:
                        self._observe_phase(
                            phases, "final-health", session.assert_healthy
                        )
                    except Exception as error:
                        _record_error(errors, "final-health", error, fatal=True)
            finally:
                try:
                    self._observe_phase(phases, "cleanup", session.close)
                except Exception as error:
                    _record_error(errors, "cleanup", error, fatal=True)
                try:
                    browser_snapshot = session.snapshot()
                except Exception as error:
                    _record_error(errors, "snapshot", error, fatal=True)

        completed_at = _timestamp(self._clock)
        elapsed_ms = max(
            0, int((self._monotonic() - started_monotonic) * 1000)
        )
        artifact = assemble_public_render_artifact(
            plan,
            verified_request,
            session_id=session_id,
            started_at=started_at,
            completed_at=completed_at,
            elapsed_ms=elapsed_ms,
            browser_snapshot=browser_snapshot,
            document=document,
            content_window=content_window,
            phase_observations=phases,
            errors=errors,
        )
        return PublicRenderCollectionResult(
            request=verified_request, artifact=artifact
        )

    def _create_browser_session(self, request: Mapping[str, Any]) -> Any:
        if self._browser_session_factory is not None:
            return self._browser_session_factory(request)
        return RenderBrowserSession(
            request,
            playwright_factory=self._playwright_factory,
            runtime_preflight=self._runtime_preflight,
            monotonic=self._monotonic,
        )

    def _observe_phase(
        self, phases: list[dict[str, Any]], phase: str, operation: Callable[[], Any]
    ) -> Any:
        started = self._monotonic()
        outcome = "ERROR"
        try:
            result = operation()
            outcome = "OBSERVED"
            return result
        finally:
            phases.append(
                {
                    "sequence": len(phases) + 1,
                    "phase": phase,
                    "outcome": outcome,
                    "elapsed_ms_monotonic": max(
                        0, int((self._monotonic() - started) * 1000)
                    ),
                }
            )


def assemble_public_render_artifact(
    plan: dict[str, Any],
    verified_request: dict[str, Any],
    *,
    session_id: str,
    started_at: str,
    completed_at: str,
    elapsed_ms: int,
    browser_snapshot: BrowserSessionSnapshot | None,
    document: dict[str, Any] | None,
    content_window: ContentWindow | None,
    phase_observations: list[dict[str, Any]],
    errors: list[dict[str, Any]],
) -> ImportedEvidence:
    """Build and independently verify one standard Evidence 0.1 artifact."""

    request = validate_public_render_request(plan, verified_request)
    if not isinstance(session_id, str) or not _SESSION_ID_PATTERN.fullmatch(
        session_id
    ):
        raise CollectionError("public Render collection session id is invalid")
    if isinstance(elapsed_ms, bool) or not isinstance(elapsed_ms, int) or elapsed_ms < 0:
        raise CollectionError("public Render collection elapsed time is invalid")
    _validate_retained_timestamp(started_at, "started_at")
    _validate_retained_timestamp(completed_at, "completed_at")
    coordinates = request["observation_spec"]["coordinates"]
    projections = frozenset(request["observation_spec"]["projections"])
    facts = _normalized_facts(
        coordinates=coordinates,
        projections=projections,
        snapshot=browser_snapshot,
        document=document,
        content_window=content_window,
    )
    collection = {
        "schema_version": "0.1",
        "request_id": request["request_id"],
        "request_seal_digest": request["seal"]["digest"],
        "render_policy_digest": request["render_policy_digest"],
        "collection_session_id": session_id,
        "collection_started_at": started_at,
        "collection_completed_at": completed_at,
        "collection_elapsed_ms": elapsed_ms,
        "access_mode": "ANONYMOUS_FRESH_CONTEXT",
        "collector_version": PUBLIC_RENDER_COLLECTOR_IMPLEMENTATION_VERSION,
        "parser_version": PUBLIC_RENDER_PARSER_IMPLEMENTATION_VERSION,
        "browser_runtime": (
            copy.deepcopy(browser_snapshot.runtime)
            if browser_snapshot is not None
            else {}
        ),
        "initial_state_check": (
            copy.deepcopy(browser_snapshot.initial_state)
            if browser_snapshot is not None
            else {}
        ),
        "post_navigation_state": (
            copy.deepcopy(browser_snapshot.post_navigation_state)
            if browser_snapshot is not None
            else None
        ),
        "network_summary": _network_summary(browser_snapshot),
        "response_body_observation": (
            copy.deepcopy(browser_snapshot.response_bodies)
            if browser_snapshot is not None
            else None
        ),
        "runtime_events": (
            copy.deepcopy(browser_snapshot.runtime_events)
            if browser_snapshot is not None
            else {
                "console_categories": {},
                "page_error_count": 0,
                "request_failure_categories": {},
            }
        ),
        "phase_observations": copy.deepcopy(phase_observations),
        "errors": copy.deepcopy(errors),
        "cleanup_errors": (
            list(browser_snapshot.cleanup_errors)
            if browser_snapshot is not None
            else []
        ),
        "coverage_reasons": [],
        "atomic_snapshot_claimed": False,
    }
    coverage, coverage_reasons = expected_public_render_coverage(
        request, facts, collection
    )
    collection["coverage_reasons"] = coverage_reasons
    fact_identity = public_render_facts_digest(
        observation_spec_digest_value=request["observation_spec_digest"],
        source_coordinates=coordinates,
        facts=facts,
    )
    evidence_document = {
        "schema_version": "0.1",
        "evidence_type": PUBLIC_RENDER_EVIDENCE_TYPE,
        "source": "veritrail-github-evidence/0.1",
        "captured_at": completed_at,
        "facts": facts,
        "metadata": {
            "veritrail_observation": {
                "schema_version": "0.1",
                "canonicalization_profile": "veritrail-json-c14n/1",
                "plan_digest": request["plan_digest"],
                "observation_spec_digest": request["observation_spec_digest"],
                "request_seal_digest": request["seal"]["digest"],
                "collection_session_id": session_id,
                "collector_role": "github-public-render",
                "coverage": coverage,
                "normalization_semantics_version": (
                    PUBLIC_RENDER_NORMALIZATION_SEMANTICS_VERSION
                ),
                "facts_digest": fact_identity,
            },
            "github_public_render_collection": collection,
        },
    }
    artifact = import_evidence_document(
        evidence_document, f"github-render-{request['request_id']}.json"
    )
    verify_public_render_evidence(plan, request, artifact)
    return artifact


def _normalized_facts(
    *,
    coordinates: Mapping[str, Any],
    projections: frozenset[str],
    snapshot: BrowserSessionSnapshot | None,
    document: dict[str, Any] | None,
    content_window: ContentWindow | None,
) -> dict[str, Any]:
    navigation = None
    if "navigation.identity" in projections and snapshot is not None:
        navigation = _json_dataclass(snapshot.navigation)

    content_requested = any(item.startswith("content.") for item in projections)
    content = None
    conflicts: list[dict[str, Any]] = []
    if snapshot is not None:
        conflicts.extend(copy.deepcopy(list(snapshot.conflicts)))
        for record in snapshot.network:
            if record.get("affects_coverage") is True:
                conflicts.append(
                    {
                        "code": "NETWORK_POLICY_BOUNDARY",
                        "reasons": sorted(set(record.get("reasons", []))),
                        "url": copy.deepcopy(record.get("url")),
                    }
                )
    if content_window is not None:
        conflicts.extend(copy.deepcopy(list(content_window.navigation_conflicts)))
        for index, sample in enumerate(content_window.samples):
            for conflict in sample.conflicts:
                conflicts.append(
                    {
                        "code": "CONTENT_SAMPLE_CONFLICT",
                        "sample_index": index,
                        "detail": copy.deepcopy(conflict),
                    }
                )

    if content_requested:
        scope = None
        if snapshot is not None and snapshot.scope is not None:
            scope = {
                "profile": coordinates["target_kind"],
                "observed_count": snapshot.scope.count,
                "usable": snapshot.scope.usable,
            }
        window = None
        if content_window is not None:
            truncations = _unique_canonical(
                item
                for sample in content_window.samples
                for item in sample.truncations
            )
            window = {
                "samples_stable": content_window.samples_stable,
                "sample_digests": list(content_window.sample_digests),
                "stable_facts": (
                    copy.deepcopy(content_window.samples[0].facts)
                    if content_window.samples_stable and content_window.samples
                    else None
                ),
                "truncations": truncations,
            }
        content = {"scope": scope, "window": window}

    return {
        "target": {
            "target_kind": coordinates["target_kind"],
            "source_coordinates": copy.deepcopy(dict(coordinates)),
        },
        "navigation": navigation,
        "document": (
            copy.deepcopy(document) if "document.identity" in projections else None
        ),
        "content": content,
        "conflicts": _unique_canonical(conflicts),
    }


def _network_summary(snapshot: BrowserSessionSnapshot | None) -> dict[str, Any]:
    records = snapshot.network if snapshot is not None else ()
    reason_counts: dict[str, int] = {}
    allowed = 0
    affected = 0
    blocked_writes = 0
    blocked_read_hosts = 0
    blocked_websockets = 0
    for record in records:
        if record.get("allowed") is True:
            allowed += 1
        if record.get("affects_coverage") is True:
            affected += 1
        method = record.get("method")
        reasons = record.get("reasons", [])
        for reason in reasons:
            if isinstance(reason, str):
                reason_counts[reason] = reason_counts.get(reason, 0) + 1
        if record.get("allowed") is not True and method not in {"GET", "HEAD"}:
            blocked_writes += 1
        if method in {"GET", "HEAD"} and "HOST_NOT_ALLOWED" in reasons:
            blocked_read_hosts += 1
        if method == "WEBSOCKET":
            blocked_websockets += 1
    return {
        "request_count": len(records),
        "allowed_count": allowed,
        "blocked_count": len(records) - allowed,
        "blocked_write_count": blocked_writes,
        "blocked_read_host_count": blocked_read_hosts,
        "blocked_websocket_count": blocked_websockets,
        "affects_coverage_count": affected,
        "reason_counts": dict(sorted(reason_counts.items())),
    }


def _json_dataclass(value: Any) -> Any:
    if value is None:
        return None
    return _json_value(asdict(value))


def _json_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return copy.deepcopy(value)


def _unique_canonical(values: Any) -> list[dict[str, Any]]:
    by_bytes: dict[bytes, dict[str, Any]] = {}
    for value in values:
        candidate = copy.deepcopy(dict(value))
        by_bytes[canonical_json_bytes(candidate)] = candidate
    return [by_bytes[key] for key in sorted(by_bytes)]


def _timestamp(clock: Callable[[], datetime]) -> str:
    value = clock()
    if value.tzinfo is None:
        raise CollectionError(
            "public Render wall clock must return a timezone-aware datetime"
        )
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _validate_retained_timestamp(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise CollectionError(f"public Render {label} must be a UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise CollectionError(
            f"public Render {label} must be a UTC timestamp"
        ) from error
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise CollectionError(f"public Render {label} must be a UTC timestamp")


def _record_error(
    errors: list[dict[str, Any]],
    phase: str,
    error: Exception,
    *,
    fatal: bool,
) -> None:
    errors.append(
        {
            "phase": phase,
            "code": _error_code(error),
            "fatal": fatal,
        }
    )


def _error_code(error: Exception) -> str:
    mappings = (
        (RenderRuntimeUnavailable, "RENDER_RUNTIME_UNAVAILABLE"),
        (FreshContextRejected, "FRESH_CONTEXT_REJECTED"),
        (RenderDeadlineExceeded, "RENDER_DEADLINE_EXCEEDED"),
        (RenderNavigationFailed, "RENDER_NAVIGATION_FAILED"),
        (PublicRenderNetworkError, "RESPONSE_BODY_OBSERVATION_FAILED"),
        (PublicRenderContentError, "CONTENT_EXTRACTION_FAILED"),
        (PublicRenderBrowserError, "BROWSER_OBSERVATION_FAILED"),
        (CollectionError, "COLLECTION_FAILED"),
    )
    for error_type, code in mappings:
        if isinstance(error, error_type):
            return code
    return "UNEXPECTED_COLLECTOR_FAILURE"
