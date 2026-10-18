"""Private CoverageLedger 0.3 conformance validation.

The caller supplies both an exact candidate and copy-owned, application-owned
terminal history.  This module validates; it does not enumerate roots, repair a
candidate, acquire a composition claim, or grant publication authority.
"""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence

from veritrail_review.canonical import canonical_json_bytes, semantic_digest


CONFORMANCE_IDENTITY = "r1-review-coverage-ledger-conformance/0.3"
LEDGER_DIGEST_DOMAIN = "veritrail.review.coverage-ledger/0.3"
ROOT_BINDING_DOMAIN = "veritrail.review.coverage-root-binding/0.1"
ROOT_CHAIN_DOMAIN = "veritrail.review.coverage-root-chain/0.1"
TERMINAL_HISTORY_DOMAIN = "veritrail.review.coverage-root-terminal-history/0.1"
ROOT_BINDING_FUNCTION = "r1-review-coverage-root-binding-correction/0.1"

ROOT_STAGE_ORDER = ("FACT_SET", "RELATION_SET", "REVIEW_SLICE_SET")
STAGE_ORDER = (
    "SNAPSHOT_INVENTORY",
    "POLICY_SCOPE",
    "LANGUAGE_SUPPORT",
    "PARSE",
    "FACT_DERIVATION",
    "RELATION_DERIVATION",
    "SLICE_DERIVATION",
)
UPSTREAM_STAGE = {
    "SNAPSHOT_INVENTORY": None,
    "POLICY_SCOPE": "SNAPSHOT_INVENTORY",
    "LANGUAGE_SUPPORT": "POLICY_SCOPE",
    "PARSE": "LANGUAGE_SUPPORT",
    "FACT_DERIVATION": "PARSE",
    "RELATION_DERIVATION": "FACT_DERIVATION",
    "SLICE_DERIVATION": "RELATION_DERIVATION",
}
ITEM_KIND_ORDER = {
    "INVENTORY_ENTRY": 0,
    "PARSE_UNIT": 1,
    "FACT": 2,
    "RELATION": 3,
    "REVIEW_SLICE": 4,
}
REASON_ORDER = (
    "POLICY_EXCLUDED",
    "UNCLASSIFIED_SOURCE",
    "UNSUPPORTED_ENTRY_KIND",
    "UNSUPPORTED_LANGUAGE",
    "UNSUPPORTED_SOURCE_ENCODING",
    "UNSUPPORTED_SYNTAX_VERSION",
    "PARSE_ERROR",
    "PROVIDER_UNAVAILABLE",
    "PROVIDER_CONFLICT",
    "TARGET_UNRESOLVED",
    "TARGET_EXTERNAL_TO_SNAPSHOT",
    "UPSTREAM_DENOMINATOR_UNKNOWN",
    "DEPTH_LIMIT",
    "SYMBOL_LIMIT",
    "FILE_LIMIT",
    "RELATION_LIMIT",
    "DERIVATION_ERROR",
    "UNREPRESENTABLE_EXPECTED_FACT",
)
_REASON_RANK = {reason: index for index, reason in enumerate(REASON_ORDER)}
_DISPOSITION_FIELDS = (
    "out_of_scope",
    "unsupported",
    "unresolved",
    "conflicts",
    "parse_failed",
    "execution_failed",
    "truncated",
    "blocked",
)
_INNER_DISPOSITION_FIELDS = (
    "unresolved",
    "conflicts",
    "parse_failed",
    "execution_failed",
    "truncated",
    "blocked",
)
_TERMINAL_HISTORY_MEMBER_NAMES = {
    ("FACT_SET", "NORMAL_FULFILLED"): (
        "blockers",
        "closure",
        "denominator",
        "e",
        "members",
        "provider_outcomes",
        "provider_responsibility",
        "u",
    ),
    ("FACT_SET", "ZERO_PARSE_DENOMINATOR"): (
        "absence",
        "blockers",
        "denominator",
        "e",
        "u",
    ),
    ("FACT_SET", "ALL_PARSE_REJECTED"): (
        "absence",
        "blockers",
        "denominator",
        "e",
        "rejected_parse_products",
        "u",
    ),
    ("FACT_SET", "PROJECTION_BLOCKED"): (
        "absence",
        "blockers",
        "denominator",
        "e",
        "u",
    ),
    ("FACT_SET", "REQUIRED_PROVIDER_NON_SUCCESS"): (
        "absence",
        "blockers",
        "denominator",
        "e",
        "provider_outcomes",
        "provider_responsibility",
        "u",
    ),
    ("RELATION_SET", "ADMITTED"): (
        "admission",
        "conflicts",
        "members",
        "obligation_universe",
        "predecessor_binding",
        "provider_outcomes",
        "provider_responsibility",
    ),
    ("RELATION_SET", "ADMITTED_CONFLICT"): (
        "admission",
        "conflicts",
        "members",
        "obligation_universe",
        "predecessor_binding",
        "provider_outcomes",
        "provider_responsibility",
    ),
    ("RELATION_SET", "PREDECESSOR_ABSENT"): (
        "absence",
        "predecessor_binding",
        "transition",
    ),
    ("RELATION_SET", "KNOWN_PREFIX_ONLY"): (
        "known_members",
        "missing_authority_slot",
        "predecessor_binding",
        "unknown_cause",
    ),
    ("REVIEW_SLICE_SET", "NORMAL_CLOSED"): (
        "admission",
        "closure",
        "frontier",
        "members",
        "obligation_universe",
        "outcomes",
        "predecessor_binding",
    ),
    ("REVIEW_SLICE_SET", "CLOSED_EMPTY"): (
        "admission",
        "closure",
        "frontier",
        "members",
        "obligation_universe",
        "outcomes",
        "predecessor_binding",
    ),
    ("REVIEW_SLICE_SET", "NORMAL_PARTIAL"): (
        "admission",
        "closure",
        "frontier",
        "members",
        "obligation_universe",
        "outcomes",
        "predecessor_binding",
    ),
    ("REVIEW_SLICE_SET", "PREDECESSOR_ABSENT"): (
        "absence",
        "predecessor_binding",
        "transition",
    ),
    ("REVIEW_SLICE_SET", "PREDECESSOR_UNKNOWN"): (
        "known_members",
        "missing_authority_slot",
        "predecessor_binding",
        "unknown_cause",
    ),
}


class CoverageLedgerConformanceFailureCode(str, Enum):
    UNKNOWN_CHILD_VERSION = "UNKNOWN_CHILD_VERSION"
    INVALID_CONFORMANCE_SOURCE = "INVALID_CONFORMANCE_SOURCE"
    UNSAFE_AUTHORITY_SOURCE = "UNSAFE_AUTHORITY_SOURCE"
    SOURCE_CANDIDATE_MISMATCH = "SOURCE_CANDIDATE_MISMATCH"
    NONCANONICAL_LEDGER = "NONCANONICAL_LEDGER"
    INVALID_ROOT_CHAIN = "INVALID_ROOT_CHAIN"
    INVALID_STAGE_PARTITION = "INVALID_STAGE_PARTITION"
    INVALID_LEDGER_DIGEST = "INVALID_LEDGER_DIGEST"


class CoverageLedgerConformanceError(ValueError):
    """Typed failure from the validation-only CoverageLedger boundary."""

    def __init__(self, code: CoverageLedgerConformanceFailureCode) -> None:
        self.code = code
        super().__init__(code.value)


@dataclass(frozen=True)
class CoverageLedgerConformanceSource:
    """Copy-owned snapshot of history already owned by the application.

    Constructing this value grants no live claim, attempt, continuation, or
    publication authority.  It only freezes the inputs against which a
    candidate is checked.
    """

    _bytes: bytes = field(repr=False)
    _authority_safe: bool = field(repr=False, compare=False)
    _bound_bytes: bytes = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_bound_bytes", self._bytes)

    def document_copy(self) -> dict[str, Any]:
        if self._bytes is not self._bound_bytes:
            raise CoverageLedgerConformanceError(
                CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE
            )
        value = json.loads(self._bytes)
        if not isinstance(value, dict):
            raise CoverageLedgerConformanceError(
                CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE
            )
        return value


def bind_coverage_ledger_conformance_source(
    *,
    fact_handoff_source_digest: str,
    root_binding_projections: Sequence[Mapping[str, Any]],
    stage_projections: Sequence[Mapping[str, Any]],
    authority_safe: bool,
) -> CoverageLedgerConformanceSource:
    """Snapshot explicit application history without constructing a Ledger."""

    value = {
        "conformance_identity": CONFORMANCE_IDENTITY,
        "fact_handoff_source_digest": fact_handoff_source_digest,
        "root_binding_projections": [copy.deepcopy(dict(item)) for item in root_binding_projections],
        "stage_projections": [copy.deepcopy(dict(item)) for item in stage_projections],
    }
    return CoverageLedgerConformanceSource(
        canonical_json_bytes(value), bool(authority_safe)
    )


def validate_review_coverage_ledger(
    candidate: Mapping[str, Any],
    source: CoverageLedgerConformanceSource,
) -> None:
    """Dispatch exactly to the implemented 0.3 conformance rule."""

    if not isinstance(candidate, Mapping):
        raise CoverageLedgerConformanceError(
            CoverageLedgerConformanceFailureCode.UNKNOWN_CHILD_VERSION
        )
    key = (candidate.get("artifact_kind"), candidate.get("schema_version"))
    if key != ("COVERAGE_LEDGER", "0.3"):
        raise CoverageLedgerConformanceError(
            CoverageLedgerConformanceFailureCode.UNKNOWN_CHILD_VERSION
        )
    _validate_0_3(copy.deepcopy(dict(candidate)), source)


def _fail(code: CoverageLedgerConformanceFailureCode) -> None:
    raise CoverageLedgerConformanceError(code)


def _item_key(value: Mapping[str, Any]) -> tuple[int, bytes]:
    try:
        kind = value["item_kind"]
        item_id = value["item_id"]
        rank = ITEM_KIND_ORDER[kind]
        encoded = item_id.encode("utf-8")
    except (KeyError, AttributeError, TypeError, UnicodeError):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
    return rank, encoded


def _reason_key(value: str) -> int:
    try:
        return _REASON_RANK[value]
    except (KeyError, TypeError):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)


def _canonical_item_refs(values: object) -> bool:
    if not isinstance(values, list):
        return False
    try:
        keys = [_item_key(value) for value in values]
    except CoverageLedgerConformanceError:
        return False
    return keys == sorted(keys) and len(keys) == len(set(keys))


def _disposition_key(field: str, value: Mapping[str, Any]) -> tuple[Any, ...]:
    reasons = value.get("reason_codes")
    if not isinstance(reasons, list):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
    return (
        *_item_key(value.get("item_ref", {})),
        field,
        tuple(_reason_key(reason) for reason in reasons),
    )


def _canonical_dispositions(field: str, values: object) -> bool:
    if not isinstance(values, list):
        return False
    try:
        keys = [_disposition_key(field, value) for value in values]
    except (CoverageLedgerConformanceError, AttributeError, TypeError):
        return False
    return keys == sorted(keys) and len(keys) == len(set(keys))


def _frontier_key(value: Mapping[str, Any]) -> tuple[bytes, bytes]:
    try:
        slice_id = value["slice_id"].encode("utf-8")
        frontier = canonical_json_bytes(value["frontier_item"])
    except (KeyError, AttributeError, TypeError, UnicodeError):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
    return slice_id, frontier


def _canonical_frontier(values: object) -> bool:
    if not isinstance(values, list):
        return False
    try:
        keys = [_frontier_key(value) for value in values]
    except CoverageLedgerConformanceError:
        return False
    return keys == sorted(keys) and len(keys) == len(set(keys))


def _ref_bytes(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(dict(value))


def _validate_terminal_history_members(
    terminal: Mapping[str, Any], *, predecessor: str
) -> None:
    members = terminal.get("history")
    if not isinstance(members, list) or not members:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    try:
        names = [member["name"] for member in members]
    except (KeyError, TypeError):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    expected_names = _TERMINAL_HISTORY_MEMBER_NAMES.get(
        (terminal.get("stage"), terminal.get("terminal_branch"))
    )
    if (
        any(not isinstance(member, Mapping) or set(member) != {"name", "value"} for member in members)
        or any(
            not isinstance(name, str)
            or re.fullmatch(r"[a-z][a-z0-9_]*", name) is None
            for name in names
        )
        or names != sorted(names)
        or len(names) != len(set(names))
        or tuple(names) != expected_names
    ):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    values = {member["name"]: member["value"] for member in members}
    if "predecessor_binding" in values and values["predecessor_binding"] != predecessor:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)


def _validate_stage(stage: Mapping[str, Any], expected_stage: str) -> None:
    if stage.get("stage") != expected_stage or stage.get("upstream_stage") != UPSTREAM_STAGE[expected_stage]:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
    denominator = stage.get("denominator")
    if not isinstance(denominator, Mapping):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)

    for field in ("eligible", "completed"):
        if not _canonical_item_refs(stage.get(field)):
            _fail(CoverageLedgerConformanceFailureCode.NONCANONICAL_LEDGER)
    for field in _DISPOSITION_FIELDS:
        if not _canonical_dispositions(field, stage.get(field)):
            _fail(CoverageLedgerConformanceFailureCode.NONCANONICAL_LEDGER)
    if not _canonical_frontier(stage.get("frontier")):
        _fail(CoverageLedgerConformanceFailureCode.NONCANONICAL_LEDGER)
    reasons = stage.get("reason_codes")
    if not isinstance(reasons, list) or reasons != sorted(set(reasons), key=_reason_key):
        _fail(CoverageLedgerConformanceFailureCode.NONCANONICAL_LEDGER)

    if denominator.get("state") == "UNKNOWN":
        if not _canonical_item_refs(denominator.get("known_item_refs")):
            _fail(CoverageLedgerConformanceFailureCode.NONCANONICAL_LEDGER)
        if stage.get("coverage_status") != "UNKNOWN":
            _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
        known = {_ref_bytes(item) for item in denominator["known_item_refs"]}
        observed = {
            _ref_bytes(item)
            for field in ("eligible", "completed")
            for item in stage[field]
        } | {
            _ref_bytes(item["item_ref"])
            for field in _DISPOSITION_FIELDS
            for item in stage[field]
        }
        if not observed <= known:
            _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
    elif denominator.get("state") == "KNOWN":
        if not _canonical_item_refs(denominator.get("item_refs")):
            _fail(CoverageLedgerConformanceFailureCode.NONCANONICAL_LEDGER)
        eligible = {_ref_bytes(item) for item in stage["eligible"]}
        outer = [
            _ref_bytes(item["item_ref"])
            for field in ("out_of_scope", "unsupported")
            for item in stage[field]
        ]
        inner = [
            _ref_bytes(item["item_ref"])
            for field in _INNER_DISPOSITION_FIELDS
            for item in stage[field]
        ] + [_ref_bytes(item) for item in stage["completed"]]
        denominator_items = [_ref_bytes(item) for item in denominator["item_refs"]]
        if len(outer) != len(set(outer)) or len(inner) != len(set(inner)):
            _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
        if set(outer) & eligible or set(inner) != eligible:
            _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
        if set(denominator_items) != eligible | set(outer):
            _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
        has_gap = bool(
            outer
            or any(stage[field] for field in _INNER_DISPOSITION_FIELDS)
            or stage.get("frontier")
        )
        expected_status = "PARTIAL" if has_gap else "COMPLETE"
        if stage.get("coverage_status") != expected_status:
            _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
    else:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)

    if expected_stage != "FACT_DERIVATION" and stage["blocked"]:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
    carrier_reasons = {
        reason
        for field in _DISPOSITION_FIELDS
        for item in stage[field]
        for reason in item["reason_codes"]
    }
    denominator_reasons = set(denominator.get("reason_codes", []))
    frontier_reasons = {
        reason
        for item in stage.get("frontier", [])
        for reason in item["frontier_item"]["reason_codes"]
    }
    expected_reasons = sorted(
        carrier_reasons | denominator_reasons | frontier_reasons,
        key=_reason_key,
    )
    if stage["reason_codes"] != expected_reasons:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)


def _validate_0_3(
    candidate: dict[str, Any], source: CoverageLedgerConformanceSource
) -> None:
    if not isinstance(source, CoverageLedgerConformanceSource):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    if not source._authority_safe:
        _fail(CoverageLedgerConformanceFailureCode.UNSAFE_AUTHORITY_SOURCE)
    history = source.document_copy()
    if history.get("conformance_identity") != CONFORMANCE_IDENTITY:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    projections = history.get("root_binding_projections")
    expected_stages = history.get("stage_projections")
    if not isinstance(projections, list) or len(projections) != len(ROOT_STAGE_ORDER):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    if not isinstance(expected_stages, list) or len(expected_stages) != len(STAGE_ORDER):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    if candidate.get("stages") != expected_stages:
        _fail(CoverageLedgerConformanceFailureCode.SOURCE_CANDIDATE_MISMATCH)

    bindings = candidate.get("root_bindings")
    if not isinstance(bindings, list) or len(bindings) != len(ROOT_STAGE_ORDER):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_ROOT_CHAIN)
    predecessor = history.get("fact_handoff_source_digest")
    if not isinstance(predecessor, str):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
    for index, (stage, projection) in enumerate(zip(ROOT_STAGE_ORDER, projections)):
        if not isinstance(projection, Mapping) or projection.get("stage") != stage:
            _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
        terminal = projection.get("terminal_history_projection")
        if not isinstance(terminal, Mapping):
            _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
        if (
            terminal.get("projection_identity") != TERMINAL_HISTORY_DOMAIN
            or terminal.get("stage") != stage
            or terminal.get("terminal_branch") != projection.get("terminal_branch")
            or terminal.get("producing_function") != projection.get("producing_function")
            or terminal.get("same_attempt_source") != history["fact_handoff_source_digest"]
        ):
            _fail(CoverageLedgerConformanceFailureCode.INVALID_CONFORMANCE_SOURCE)
        _validate_terminal_history_members(terminal, predecessor=predecessor)
        expected = copy.deepcopy(dict(projection))
        expected["terminal_history_digest"] = semantic_digest(
            TERMINAL_HISTORY_DOMAIN, terminal
        )
        expected["predecessor_binding_digest"] = predecessor
        unsigned = copy.deepcopy(expected)
        expected["binding_digest"] = semantic_digest(ROOT_BINDING_DOMAIN, unsigned)
        if bindings[index] != expected:
            _fail(CoverageLedgerConformanceFailureCode.INVALID_ROOT_CHAIN)
        if index and projections[index - 1]["binding_state"] == "QUALIFIED_UNKNOWN":
            if projection.get("binding_state") != "QUALIFIED_UNKNOWN":
                _fail(CoverageLedgerConformanceFailureCode.INVALID_ROOT_CHAIN)
        if index and projection.get("binding_state") == "ARTIFACT_PRESENT":
            if projections[index - 1]["binding_state"] != "ARTIFACT_PRESENT":
                _fail(CoverageLedgerConformanceFailureCode.INVALID_ROOT_CHAIN)
        predecessor = expected["binding_digest"]

    root_payload = {
        "root_binding_function": candidate.get("root_binding_function"),
        "root_chain_domain": candidate.get("root_chain_domain"),
        "root_bindings": bindings,
    }
    if (
        root_payload["root_binding_function"] != ROOT_BINDING_FUNCTION
        or root_payload["root_chain_domain"] != ROOT_CHAIN_DOMAIN
        or candidate.get("root_chain_digest")
        != semantic_digest(ROOT_CHAIN_DOMAIN, root_payload)
    ):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_ROOT_CHAIN)

    for expected_stage, stage in zip(STAGE_ORDER, candidate["stages"]):
        if not isinstance(stage, Mapping):
            _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)
        _validate_stage(stage, expected_stage)
    statuses = [stage["coverage_status"] for stage in candidate["stages"]]
    overall = "UNKNOWN" if "UNKNOWN" in statuses else "PARTIAL" if "PARTIAL" in statuses else "COMPLETE"
    if candidate.get("overall_coverage_status") != overall:
        _fail(CoverageLedgerConformanceFailureCode.INVALID_STAGE_PARTITION)

    unsigned_ledger = copy.deepcopy(candidate)
    actual_digest = unsigned_ledger.pop("coverage_ledger_digest", None)
    if actual_digest != semantic_digest(LEDGER_DIGEST_DOMAIN, unsigned_ledger):
        _fail(CoverageLedgerConformanceFailureCode.INVALID_LEDGER_DIGEST)
