"""Independent private conformance for Review Derivation Manifest 0.2.

The validator consumes one copy-owned carrier snapshot.  It does not import the
Manifest producer, read a path, invoke a Provider, repair bytes, publish a
Bundle, or decide truth, sufficiency, Verdict, or HumanDisposition.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Mapping

from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.contracts import validate_source_snapshot_document
from veritrail_review.derivation_input import (
    _BindingState,
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
)
from veritrail_review.derivation_input_contracts import (
    DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
)
from veritrail_review.errors import DerivationInputError, SourceSnapshotError


CONFORMANCE_IDENTITY = (
    "r1-review-derivation-manifest-coverage-topology/0.1"
)
PROJECTION_IDENTITY = "r1-review-derivation-manifest-0.2-projection/0.1"
VALIDATION_DOMAIN = (
    "veritrail.review.derivation-manifest-0.2-validation/0.1"
)
INPUT_SNAPSHOT_DOMAIN = (
    "veritrail.review.derivation-manifest-0.2-input-snapshot/0.1"
)
CARRIER_VALIDATION_FUNCTION = (
    "r1-derivation-evidence-manifest-carrier-independent-conformance/0.1"
)
CARRIER_VALIDATION_DOMAIN = "veritrail.review.manifest-carrier-validation/0.1"
CARRIER_FILE_BINDING_DOMAIN = (
    "veritrail.review.manifest-carrier-file-binding/0.1"
)
CARRIER_TOPOLOGY_PROOF_DOMAIN = (
    "veritrail.review.manifest-carrier-topology-proof/0.1"
)
EVIDENCE_IDENTITY_DOMAIN = "veritrail.review.derivation-evidence/0.3"
LEDGER_DIGEST_DOMAIN = "veritrail.review.coverage-ledger/0.3"
ROOT_BINDING_DOMAIN = "veritrail.review.coverage-root-binding/0.1"
ROOT_CHAIN_DOMAIN = "veritrail.review.coverage-root-chain/0.1"
ROOT_BINDING_FUNCTION = "r1-review-coverage-root-binding-correction/0.1"
TERMINAL_HISTORY_DOMAIN = (
    "veritrail.review.coverage-root-terminal-history/0.1"
)

_MANIFEST_KEYS = {
    "bundle_kind",
    "schema_version",
    "canonicalization_profile",
    "outcome_kind",
    "files",
}
_FILE_KEYS = {"role", "path", "sha256", "size_bytes", "semantic_digest"}
_CARRIER_RECORD_KEYS = {
    "role",
    "path",
    "raw_sha256",
    "size_bytes",
    "semantic_digest",
}
_ROLE_PATHS = {
    "SOURCE_SNAPSHOT": "source-snapshot.json",
    "REVIEW_POLICY": "review-policy.json",
    "DERIVATION_PROFILE": "derivation-profile.json",
    "DERIVATION_EVIDENCE": "derivation-evidence.json",
    "FACT_SET": "fact-set.json",
    "RELATION_SET": "relation-set.json",
    "REVIEW_SLICE_SET": "review-slices.json",
    "COVERAGE_LEDGER": "coverage-ledger.json",
}
_SEMANTIC_KEYS = {
    "SOURCE_SNAPSHOT": "source_snapshot_digest",
    "REVIEW_POLICY": "policy_digest",
    "DERIVATION_PROFILE": "profile_digest",
    "DERIVATION_EVIDENCE": "derivation_evidence_digest",
    "FACT_SET": "fact_set_digest",
    "RELATION_SET": "relation_set_digest",
    "REVIEW_SLICE_SET": "slice_set_digest",
    "COVERAGE_LEDGER": "coverage_ledger_digest",
}
_PREFIX = (
    "SOURCE_SNAPSHOT",
    "REVIEW_POLICY",
    "DERIVATION_PROFILE",
    "DERIVATION_EVIDENCE",
)
_OPTIONAL = ("FACT_SET", "RELATION_SET", "REVIEW_SLICE_SET")
_ROLE_ORDER = (*_PREFIX, *_OPTIONAL, "COVERAGE_LEDGER")
_HEX64 = re.compile(r"[0-9a-f]{64}")
_CARRIER_VALIDATION_KEYS = {
    "validation_function",
    "status",
    "derivation_evidence_digest",
    "coverage_ledger_digest",
    "root_chain_digest",
    "file_binding_digest",
    "topology_proof_digest",
    "validation_digest",
}
_LEDGER_KEYS = {
    "artifact_kind",
    "schema_version",
    "canonicalization_profile",
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
    "root_binding_function",
    "root_chain_domain",
    "root_bindings",
    "root_chain_digest",
    "stages",
    "overall_coverage_status",
    "coverage_ledger_digest",
}
_STAGE_KEYS = {
    "stage",
    "upstream_stage",
    "denominator",
    "eligible",
    "completed",
    "out_of_scope",
    "unsupported",
    "unresolved",
    "conflicts",
    "parse_failed",
    "execution_failed",
    "truncated",
    "frontier",
    "coverage_status",
    "reason_codes",
    "blocked",
}
_STAGE_ORDER = (
    "SNAPSHOT_INVENTORY",
    "POLICY_SCOPE",
    "LANGUAGE_SUPPORT",
    "PARSE",
    "FACT_DERIVATION",
    "RELATION_DERIVATION",
    "SLICE_DERIVATION",
)
_UPSTREAM_STAGE = {
    "SNAPSHOT_INVENTORY": None,
    "POLICY_SCOPE": "SNAPSHOT_INVENTORY",
    "LANGUAGE_SUPPORT": "POLICY_SCOPE",
    "PARSE": "LANGUAGE_SUPPORT",
    "FACT_DERIVATION": "PARSE",
    "RELATION_DERIVATION": "FACT_DERIVATION",
    "SLICE_DERIVATION": "RELATION_DERIVATION",
}
_ITEM_KINDS = {
    "INVENTORY_ENTRY",
    "PARSE_UNIT",
    "FACT",
    "RELATION",
    "REVIEW_SLICE",
}
_COVERAGE_REASONS = {
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
}
_DISPOSITION_REASONS = {
    "out_of_scope": {"POLICY_EXCLUDED"},
    "unsupported": {
        "UNCLASSIFIED_SOURCE",
        "UNSUPPORTED_ENTRY_KIND",
        "UNSUPPORTED_LANGUAGE",
        "UNSUPPORTED_SOURCE_ENCODING",
        "UNSUPPORTED_SYNTAX_VERSION",
    },
    "unresolved": {"TARGET_UNRESOLVED", "TARGET_EXTERNAL_TO_SNAPSHOT"},
    "conflicts": {"PROVIDER_CONFLICT"},
    "parse_failed": {"PARSE_ERROR"},
    "execution_failed": {"PROVIDER_UNAVAILABLE", "DERIVATION_ERROR"},
    "truncated": {"DEPTH_LIMIT", "SYMBOL_LIMIT", "FILE_LIMIT", "RELATION_LIMIT"},
}
_SINGLE_REASON_DISPOSITIONS = {
    "out_of_scope",
    "conflicts",
    "parse_failed",
}
_TRUNCATION_REASONS = {
    "DEPTH_LIMIT",
    "SYMBOL_LIMIT",
    "FILE_LIMIT",
    "RELATION_LIMIT",
}
_TERMINAL_KEYS = {
    "projection_identity",
    "stage",
    "terminal_branch",
    "producing_function",
    "same_attempt_source",
    "completion_state",
    "history",
}
_ROOT_BASE_KEYS = {
    "stage",
    "binding_state",
    "producing_function",
    "terminal_branch",
    "terminal_history_projection",
    "terminal_history_digest",
    "predecessor_binding_digest",
    "binding_digest",
}
_AUTHORITY_CEILING = {
    "private_manifest_0_2": True,
    "private_consumer": True,
    "private_caller_owned_staging": True,
    "public_bundle": False,
    "public_evidence": False,
    "cli": False,
    "workbench": False,
    "persistence": False,
    "truth": False,
    "sufficiency": False,
    "core_verdict": False,
    "human_disposition": False,
    "global_composition_authority": False,
    "r2_r6": False,
}
_SNAPSHOT_KEYS = {
    "producer_identity",
    "conformance_identity",
    "shared_expected_projector_state",
    "manifest_bytes",
    "carrier_admission_digest",
    "carrier_records",
    "carrier_bytes_by_role",
    "carrier_validation",
    "input_snapshot_digest",
    "authority_ceiling",
}


class Manifest02ConformanceFailure(ValueError):
    def __init__(self, family: str) -> None:
        self.family = family
        super().__init__(family)


def _fail(family: str) -> None:
    raise Manifest02ConformanceFailure(family)


def authority_ceiling_copy() -> dict[str, object]:
    return copy.deepcopy(_AUTHORITY_CEILING)


def _document(raw: object, family: str) -> dict[str, object]:
    if type(raw) is not bytes:
        _fail(family)
    try:
        value = json.loads(raw)
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError):
        _fail(family)
    if type(value) is not dict or raw not in {
        canonical_json_bytes(value),
        canonical_json_bytes(value) + b"\n",
    }:
        _fail(family)
    return value


def _is_digest(value: object) -> bool:
    return type(value) is str and _HEX64.fullmatch(value) is not None


def _unique_json(values: object) -> bool:
    if type(values) is not list:
        return False
    encoded = [canonical_json_bytes(value) for value in values]
    return len(encoded) == len(set(encoded))


def _reason_list(
    value: object,
    allowed: set[str],
    *,
    minimum: int = 1,
    maximum: int | None = None,
) -> bool:
    return (
        type(value) is list
        and len(value) >= minimum
        and (maximum is None or len(value) <= maximum)
        and all(type(item) is str and item in allowed for item in value)
        and len(value) == len(set(value))
    )


def _validate_item_ref(value: object) -> None:
    if type(value) is not dict or set(value) != {"item_kind", "item_id"}:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    kind = value.get("item_kind")
    item_id = value.get("item_id")
    if kind not in _ITEM_KINDS or type(item_id) is not str:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    if kind in {"INVENTORY_ENTRY", "PARSE_UNIT"}:
        if re.fullmatch(r"(?:[0-9a-f]{2})+", item_id) is None:
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    elif not _is_digest(item_id):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")


def _validate_item_ref_list(value: object) -> None:
    if not _unique_json(value):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    for item in value:
        _validate_item_ref(item)


def _validate_frontier(value: object) -> None:
    if not _unique_json(value):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    frontier_keys = {"slice_id", "frontier_item"}
    item_keys = {
        "from_fact_id",
        "relation_id",
        "direction",
        "candidate_fact_id",
        "candidate_depth",
        "reason_codes",
    }
    for row in value:
        if type(row) is not dict or set(row) != frontier_keys:
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        item = row.get("frontier_item")
        if (
            not _is_digest(row.get("slice_id"))
            or type(item) is not dict
            or set(item) != item_keys
            or not _is_digest(item.get("from_fact_id"))
            or not _is_digest(item.get("relation_id"))
            or item.get("direction") not in {"OUTBOUND", "INBOUND"}
            or (
                item.get("candidate_fact_id") is not None
                and not _is_digest(item.get("candidate_fact_id"))
            )
            or type(item.get("candidate_depth")) is not int
            or item["candidate_depth"] < 0
            or not _reason_list(item.get("reason_codes"), _TRUNCATION_REASONS)
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")


def _validate_stage_shape(value: object, expected_stage: str) -> None:
    if (
        type(value) is not dict
        or set(value) != _STAGE_KEYS
        or value.get("stage") != expected_stage
        or value.get("upstream_stage") != _UPSTREAM_STAGE[expected_stage]
        or value.get("coverage_status") not in {"COMPLETE", "PARTIAL", "UNKNOWN"}
        or not _reason_list(
            value.get("reason_codes"), _COVERAGE_REASONS, minimum=0
        )
    ):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    denominator = value.get("denominator")
    if type(denominator) is not dict:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    if denominator.get("state") == "KNOWN":
        if (
            set(denominator) != {"state", "source_digest", "item_refs"}
            or not _is_digest(denominator.get("source_digest"))
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        _validate_item_ref_list(denominator.get("item_refs"))
    elif denominator.get("state") == "UNKNOWN":
        if (
            set(denominator)
            != {"state", "source_digest", "known_item_refs", "reason_codes"}
            or denominator.get("source_digest") is not None
            or not _reason_list(
                denominator.get("reason_codes"), _COVERAGE_REASONS
            )
            or "UPSTREAM_DENOMINATOR_UNKNOWN"
            not in denominator["reason_codes"]
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        _validate_item_ref_list(denominator.get("known_item_refs"))
    else:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")

    for name in ("eligible", "completed"):
        _validate_item_ref_list(value.get(name))
    for name, allowed in _DISPOSITION_REASONS.items():
        rows = value.get(name)
        if not _unique_json(rows):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        for row in rows:
            if (
                type(row) is not dict
                or set(row) != {"item_ref", "reason_codes"}
                or not _reason_list(
                    row.get("reason_codes"),
                    allowed,
                    maximum=1 if name in _SINGLE_REASON_DISPOSITIONS else None,
                )
            ):
                _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
            _validate_item_ref(row.get("item_ref"))
    _validate_frontier(value.get("frontier"))
    if expected_stage != "SLICE_DERIVATION" and value["frontier"]:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")

    blocked = value.get("blocked")
    if not _unique_json(blocked):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    for row in blocked:
        if (
            type(row) is not dict
            or set(row) != {"item_ref", "disposition_family", "reason_codes"}
            or row.get("disposition_family") != "SEMANTIC_PROJECTION_BLOCKER"
            or row.get("reason_codes") != ["UNREPRESENTABLE_EXPECTED_FACT"]
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        _validate_item_ref(row.get("item_ref"))
        if row["item_ref"].get("item_kind") != "FACT":
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    if expected_stage != "FACT_DERIVATION" and blocked:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")


def _validate_root_binding_shape(value: object) -> None:
    if type(value) is not dict:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    state = value.get("binding_state")
    if state == "ARTIFACT_PRESENT":
        expected = _ROOT_BASE_KEYS | {"artifact_digest", "closure_digest"}
    elif state == "QUALIFIED_ABSENT":
        expected = _ROOT_BASE_KEYS | {"exact_absence"}
    elif state == "QUALIFIED_UNKNOWN":
        expected = _ROOT_BASE_KEYS | {"known_prefix", "unknown_cause"}
    else:
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    terminal = value.get("terminal_history_projection")
    if (
        set(value) != expected
        or type(value.get("producing_function")) is not str
        or not value["producing_function"]
        or type(value.get("terminal_branch")) is not str
        or not value["terminal_branch"]
        or not _is_digest(value.get("terminal_history_digest"))
        or not _is_digest(value.get("predecessor_binding_digest"))
        or not _is_digest(value.get("binding_digest"))
        or type(terminal) is not dict
        or set(terminal) != _TERMINAL_KEYS
        or terminal.get("projection_identity") != TERMINAL_HISTORY_DOMAIN
        or terminal.get("stage") != value.get("stage")
        or terminal.get("terminal_branch") != value.get("terminal_branch")
        or terminal.get("producing_function") != value.get("producing_function")
        or not _is_digest(terminal.get("same_attempt_source"))
        or terminal.get("completion_state") not in {"COMPLETE", "KNOWN_PREFIX"}
        or not _unique_json(terminal.get("history"))
        or not terminal["history"]
    ):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    for member in terminal["history"]:
        if (
            type(member) is not dict
            or set(member) != {"name", "value"}
            or type(member.get("name")) is not str
            or re.fullmatch(r"[a-z][a-z0-9_]*", member["name"]) is None
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    if value["terminal_history_digest"] != semantic_digest(
        TERMINAL_HISTORY_DOMAIN, terminal
    ):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    if state == "ARTIFACT_PRESENT":
        if not _is_digest(value.get("artifact_digest")) or not _is_digest(
            value.get("closure_digest")
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    elif state == "QUALIFIED_ABSENT":
        if type(value.get("exact_absence")) is not str or not value["exact_absence"]:
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    else:
        prefix = value.get("known_prefix")
        if (
            type(prefix) is not dict
            or set(prefix) != {"members", "complete"}
            or prefix.get("complete") is not False
            or not _unique_json(prefix.get("members"))
            or any(not _is_digest(item) for item in prefix["members"])
            or type(value.get("unknown_cause")) is not str
            or not value["unknown_cause"]
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")


def _validate_ledger_schema_shape(ledger: dict[str, object]) -> None:
    digest_fields = {
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "root_chain_digest",
        "coverage_ledger_digest",
    }
    if (
        set(ledger) != _LEDGER_KEYS
        or any(not _is_digest(ledger.get(name)) for name in digest_fields)
        or ledger.get("overall_coverage_status")
        not in {"COMPLETE", "PARTIAL", "UNKNOWN"}
        or type(ledger.get("stages")) is not list
        or len(ledger["stages"]) != len(_STAGE_ORDER)
        or type(ledger.get("root_bindings")) is not list
        or len(ledger["root_bindings"]) != len(_OPTIONAL)
    ):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    for expected_stage, stage in zip(_STAGE_ORDER, ledger["stages"]):
        _validate_stage_shape(stage, expected_stage)
    for expected_stage, binding in zip(_OPTIONAL, ledger["root_bindings"]):
        _validate_root_binding_shape(binding)
        if binding.get("stage") != expected_stage:
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")


def _carrier_records(value: object) -> list[dict[str, object]]:
    if type(value) is not tuple:
        _fail("MANIFEST_0_2_CARRIER_RECORD_REJECTED")
    result = []
    for item in value:
        if type(item) is not dict or set(item) != _CARRIER_RECORD_KEYS:
            _fail("MANIFEST_0_2_CARRIER_RECORD_REJECTED")
        if (
            item.get("role") not in _ROLE_PATHS
            or item.get("path") != _ROLE_PATHS[item["role"]]
            or not _is_digest(item.get("raw_sha256"))
            or type(item.get("size_bytes")) is not int
            or item["size_bytes"] < 0
            or not _is_digest(item.get("semantic_digest"))
        ):
            _fail("MANIFEST_0_2_CARRIER_RECORD_REJECTED")
        result.append(copy.deepcopy(item))
    return result


def _validate_prefix_documents(
    documents: Mapping[str, Mapping[str, object]],
) -> None:
    source_snapshot = documents["SOURCE_SNAPSHOT"]
    policy = documents["REVIEW_POLICY"]
    profile = documents["DERIVATION_PROFILE"]
    evidence = documents["DERIVATION_EVIDENCE"]
    ledger = documents["COVERAGE_LEDGER"]
    state = _BindingState(
        DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
        clock=lambda: 0.0,
        stage_hook=None,
    )
    try:
        validate_source_snapshot_document(source_snapshot)
        _validate_profile(profile, state)
        _validate_policy(policy, profile, state)
        _validate_cross_artifact_binding(source_snapshot, policy, profile, state)
    except (DerivationInputError, SourceSnapshotError, KeyError, TypeError, ValueError):
        _fail("MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED")

    unsigned_evidence = copy.deepcopy(dict(evidence))
    evidence_digest = unsigned_evidence.pop("derivation_evidence_digest", None)
    if evidence_digest != semantic_digest(
        EVIDENCE_IDENTITY_DOMAIN, unsigned_evidence
    ):
        _fail("MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED")
    expected = {
        "source_snapshot_digest": source_snapshot.get("source_snapshot_digest"),
        "policy_digest": policy.get("policy_digest"),
        "analysis_scope_digest": policy.get("analysis_scope_digest"),
        "slice_policy_digest": policy.get("slice_policy_digest"),
        "derivation_profile_digest": profile.get("profile_digest"),
    }
    if any(
        evidence.get(name) != digest or ledger.get(name) != digest
        for name, digest in expected.items()
    ) or (
        evidence.get("coverage_ledger_digest")
        != ledger.get("coverage_ledger_digest")
    ) or evidence.get("root_chain_digest") != ledger.get("root_chain_digest"):
        _fail("MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED")


def _validate_carrier_proof(
    report: object,
    records: list[dict[str, object]],
    ledger: Mapping[str, object],
    derivation_evidence: Mapping[str, object],
) -> dict[str, object]:
    if type(report) is not dict or set(report) != _CARRIER_VALIDATION_KEYS:
        _fail("MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED")
    unsigned = copy.deepcopy(report)
    validation_digest = unsigned.pop("validation_digest")
    topology = {
        "root_chain_digest": ledger.get("root_chain_digest"),
        "root_bindings": copy.deepcopy(ledger.get("root_bindings")),
    }
    if (
        report.get("validation_function") != CARRIER_VALIDATION_FUNCTION
        or report.get("status") != "QUALIFIED"
        or validation_digest
        != semantic_digest(CARRIER_VALIDATION_DOMAIN, unsigned)
        or report.get("file_binding_digest")
        != semantic_digest(CARRIER_FILE_BINDING_DOMAIN, records)
        or report.get("topology_proof_digest")
        != semantic_digest(CARRIER_TOPOLOGY_PROOF_DOMAIN, topology)
        or report.get("coverage_ledger_digest")
        != ledger.get("coverage_ledger_digest")
        or report.get("root_chain_digest") != ledger.get("root_chain_digest")
        or report.get("derivation_evidence_digest")
        != derivation_evidence.get("derivation_evidence_digest")
    ):
        _fail("MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED")
    return copy.deepcopy(report)


def _validate_ledger(ledger: dict[str, object]) -> list[dict[str, object]]:
    _validate_ledger_schema_shape(ledger)
    if (
        ledger.get("artifact_kind") != "COVERAGE_LEDGER"
        or ledger.get("schema_version") != "0.3"
        or ledger.get("canonicalization_profile")
        != "veritrail-json-c14n/1"
        or ledger.get("root_binding_function") != ROOT_BINDING_FUNCTION
        or ledger.get("root_chain_domain") != ROOT_CHAIN_DOMAIN
    ):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    unsigned = copy.deepcopy(ledger)
    digest = unsigned.pop("coverage_ledger_digest", None)
    if digest != semantic_digest(LEDGER_DIGEST_DOMAIN, unsigned):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    bindings = ledger.get("root_bindings")
    if (
        type(bindings) is not list
        or [item.get("stage") for item in bindings]
        != list(_OPTIONAL)
    ):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    previous = None
    same_attempt_source = bindings[0]["terminal_history_projection"].get(
        "same_attempt_source"
    )
    for item in bindings:
        if type(item) is not dict:
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        unsigned_binding = copy.deepcopy(item)
        binding_digest = unsigned_binding.pop("binding_digest", None)
        if binding_digest != semantic_digest(
            ROOT_BINDING_DOMAIN, unsigned_binding
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        predecessor = item.get("predecessor_binding_digest")
        if (
            previous is None
            and predecessor != same_attempt_source
        ) or (
            previous is not None and predecessor != previous
        ) or (
            item["terminal_history_projection"].get("same_attempt_source")
            != same_attempt_source
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        previous = binding_digest
    chain_payload = {
        "root_binding_function": ledger["root_binding_function"],
        "root_chain_domain": ledger["root_chain_domain"],
        "root_bindings": bindings,
    }
    if ledger.get("root_chain_digest") != semantic_digest(
        ROOT_CHAIN_DOMAIN, chain_payload
    ):
        _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
    return copy.deepcopy(bindings)


def _validate_files(
    manifest: dict[str, object],
    carrier_records: list[dict[str, object]],
    raw_by_role: object,
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    entries = manifest.get("files")
    if type(entries) is not list or not 5 <= len(entries) <= 8:
        _fail("MANIFEST_0_2_TOPOLOGY_REJECTED")
    if type(raw_by_role) is not dict:
        _fail("MANIFEST_0_2_CHILD_BINDING_REJECTED")
    roles = []
    paths = []
    records = []
    documents = {}
    for entry in entries:
        if type(entry) is not dict or set(entry) != _FILE_KEYS:
            _fail("MANIFEST_0_2_CHILD_BINDING_REJECTED")
        role = entry.get("role")
        path = entry.get("path")
        if (
            role not in _ROLE_PATHS
            or path != _ROLE_PATHS[role]
            or role in roles
            or path in paths
            or not _is_digest(entry.get("sha256"))
            or type(entry.get("size_bytes")) is not int
            or entry["size_bytes"] < 0
            or not _is_digest(entry.get("semantic_digest"))
        ):
            _fail("MANIFEST_0_2_ROLE_PATH_REJECTED")
        raw = raw_by_role.get(role)
        document = _document(raw, "MANIFEST_0_2_CHILD_BINDING_REJECTED")
        if (
            entry["sha256"] != hashlib.sha256(raw).hexdigest()
            or entry["size_bytes"] != len(raw)
            or entry["semantic_digest"]
            != document.get(_SEMANTIC_KEYS[role])
        ):
            _fail("MANIFEST_0_2_CHILD_BINDING_REJECTED")
        roles.append(role)
        paths.append(path)
        documents[role] = document
        records.append(
            {
                "role": role,
                "path": path,
                "raw_sha256": entry["sha256"],
                "size_bytes": entry["size_bytes"],
                "semantic_digest": entry["semantic_digest"],
            }
        )
    expected_order = [role for role in _ROLE_ORDER if role in roles]
    if (
        tuple(roles[:4]) != _PREFIX
        or roles[-1:] != ["COVERAGE_LEDGER"]
        or roles != expected_order
        or records != carrier_records
        or set(raw_by_role) != set(roles)
    ):
        _fail("MANIFEST_0_2_TOPOLOGY_REJECTED")
    return records, documents


def _validate_root_topology(
    bindings: list[dict[str, object]],
    documents: Mapping[str, Mapping[str, object]],
) -> None:
    for binding in bindings:
        role = binding["stage"]
        state = binding.get("binding_state")
        present = role in documents
        if state == "ARTIFACT_PRESENT":
            if (
                not present
                or binding.get("artifact_digest")
                != documents[role].get(_SEMANTIC_KEYS[role])
            ):
                _fail("MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED")
        elif state == "QUALIFIED_ABSENT":
            if present or type(binding.get("exact_absence")) is not str:
                _fail("MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED")
        elif state == "QUALIFIED_UNKNOWN":
            if present or type(binding.get("unknown_cause")) is not str:
                _fail("MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED")
        else:
            _fail("MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED")


def validate_review_derivation_manifest_0_2_snapshot(
    snapshot: Mapping[str, object],
) -> dict[str, object]:
    """Validate a producer-owned candidate without sharing its projector."""

    if type(snapshot) is not dict or set(snapshot) != _SNAPSHOT_KEYS:
        _fail("MANIFEST_0_2_SNAPSHOT_REJECTED")
    if (
        snapshot.get("conformance_identity") != CONFORMANCE_IDENTITY
        or snapshot.get("producer_identity") != PROJECTION_IDENTITY
        or snapshot.get("shared_expected_projector_state") is not False
        or snapshot.get("authority_ceiling") != _AUTHORITY_CEILING
    ):
        _fail("MANIFEST_0_2_COMMON_MODE_OR_AUTHORITY_REJECTED")
    manifest = _document(
        snapshot.get("manifest_bytes"), "MANIFEST_0_2_SHAPE_REJECTED"
    )
    if (
        set(manifest) != _MANIFEST_KEYS
        or manifest.get("bundle_kind") != "R1_DERIVATION"
        or manifest.get("schema_version") != "0.2"
        or manifest.get("canonicalization_profile")
        != "veritrail-json-c14n/1"
        or manifest.get("outcome_kind") != "COVERAGE"
    ):
        _fail("MANIFEST_0_2_VERSION_OR_SHAPE_REJECTED")
    carrier_records = _carrier_records(snapshot.get("carrier_records"))
    records, documents = _validate_files(
        manifest,
        carrier_records,
        snapshot.get("carrier_bytes_by_role"),
    )
    _validate_prefix_documents(documents)
    ledger = documents["COVERAGE_LEDGER"]
    bindings = _validate_ledger(ledger)
    _validate_root_topology(bindings, documents)
    carrier_proof = _validate_carrier_proof(
        snapshot.get("carrier_validation"),
        records,
        ledger,
        documents["DERIVATION_EVIDENCE"],
    )
    expected_snapshot_digest = semantic_digest(
        INPUT_SNAPSHOT_DOMAIN,
        {
            "carrier_admission_digest": snapshot.get(
                "carrier_admission_digest"
            ),
            "carrier_validation_digest": carrier_proof["validation_digest"],
            "manifest_raw_sha256": hashlib.sha256(
                snapshot["manifest_bytes"]
            ).hexdigest(),
            "records": records,
        },
    )
    if (
        not _is_digest(snapshot.get("carrier_admission_digest"))
        or snapshot.get("input_snapshot_digest")
        != expected_snapshot_digest
    ):
        _fail("MANIFEST_0_2_SNAPSHOT_REJECTED")
    report = {
        "conformance_identity": CONFORMANCE_IDENTITY,
        "status": "QUALIFIED",
        "manifest_raw_sha256": hashlib.sha256(
            snapshot["manifest_bytes"]
        ).hexdigest(),
        "carrier_admission_digest": snapshot["carrier_admission_digest"],
        "carrier_validation_digest": carrier_proof["validation_digest"],
        "file_binding_digest": carrier_proof["file_binding_digest"],
        "coverage_ledger_digest": ledger["coverage_ledger_digest"],
        "root_chain_digest": ledger["root_chain_digest"],
    }
    report["validation_digest"] = semantic_digest(VALIDATION_DOMAIN, report)
    return report
