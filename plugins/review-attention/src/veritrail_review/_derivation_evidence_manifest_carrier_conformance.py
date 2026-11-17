"""Independent conformance for the private DerivationEvidence carrier successor.

This module deliberately does not import the producer module.  It consumes a
copy-owned validation view, recomputes every document and topology binding from
raw bytes plus frozen rules, and returns only a validation report.  It cannot
construct a candidate, repair bytes, create a Manifest, or grant a Verdict.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from typing import Mapping

from veritrail_review._review_coverage_ledger_conformance import (
    CoverageLedgerConformanceSource,
    validate_review_coverage_ledger,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


INDEPENDENT_CONFORMANCE_FUNCTION = (
    "r1-derivation-evidence-manifest-carrier-independent-conformance/0.1"
)
EVIDENCE_IDENTITY_DOMAIN = "veritrail.review.derivation-evidence/0.3"
FILE_BINDING_DOMAIN = "veritrail.review.manifest-carrier-file-binding/0.1"
TOPOLOGY_PROOF_DOMAIN = "veritrail.review.manifest-carrier-topology-proof/0.1"
VALIDATION_DOMAIN = "veritrail.review.manifest-carrier-validation/0.1"
ATTEMPT_BINDING_FUNCTION = "r1-manifest-carrier-successor-attempt-binding/0.1"
CONTEXT_IDENTITY_DOMAIN = "veritrail.review.manifest-carrier-context/0.1"

_EVIDENCE_KEYS = {
    "artifact_kind",
    "schema_version",
    "canonicalization_profile",
    "derivation_id",
    "request_provenance",
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
    "terminal_branch",
    "selector_route",
    "continuity_variant",
    "continuity_digest",
    "application_admission_digest",
    "coverage_ledger_digest",
    "root_chain_digest",
    "derivation_evidence_digest",
}
_INPUT_DIGEST_FIELDS = (
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
)
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
_SEMANTIC_DIGEST_KEYS = {
    "SOURCE_SNAPSHOT": "source_snapshot_digest",
    "REVIEW_POLICY": "policy_digest",
    "DERIVATION_PROFILE": "profile_digest",
    "DERIVATION_EVIDENCE": "derivation_evidence_digest",
    "FACT_SET": "fact_set_digest",
    "RELATION_SET": "relation_set_digest",
    "REVIEW_SLICE_SET": "slice_set_digest",
    "COVERAGE_LEDGER": "coverage_ledger_digest",
}
_ROOT_STAGES = ("FACT_SET", "RELATION_SET", "REVIEW_SLICE_SET")
_NEGATIVE_BRANCHES = {
    "ZERO_PARSE_DENOMINATOR",
    "ALL_PARSE_REJECTED",
    "PROJECTION_BLOCKED",
    "REQUIRED_PROVIDER_NON_SUCCESS",
}
_AUTHORITY_CEILING = {
    "private_copy_owned_manifest_carrier_successor": True,
    "future_manifest_consumption_one_shot": True,
    "manifest_created": False,
    "persistence": False,
    "public_review": False,
    "truth": False,
    "sufficiency": False,
    "core_verdict": False,
    "global_composition_authority": False,
    "r2_r6": False,
}


class IndependentCarrierConformanceFailure(ValueError):
    def __init__(self, family: str) -> None:
        self.family = family
        super().__init__(family)


def _fail(family: str) -> None:
    raise IndependentCarrierConformanceFailure(family)


def _document(raw: object, family: str) -> dict[str, object]:
    if type(raw) is not bytes:
        _fail(family)
    try:
        value = json.loads(raw)
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError):
        _fail(family)
    canonical = canonical_json_bytes(value)
    if type(value) is not dict or raw not in {canonical, canonical + b"\n"}:
        _fail(family)
    return value


def _validate_request_provenance(
    provenance: object, source_snapshot: Mapping[str, object]
) -> None:
    if type(provenance) is not dict or set(provenance) != {
        "requested_repository_id",
        "requested_ref",
        "resolver_id",
        "resolver_version",
        "resolved_at",
    }:
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")
    try:
        commit = source_snapshot["source_coordinate"]["commit_oid"]
        expected_ref = (
            f"oid:{commit['algorithm'].lower()}:{commit['hex']}"
        )
    except (KeyError, TypeError, AttributeError):
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")
    if (
        provenance["requested_repository_id"]
        != source_snapshot.get("repository_id")
        or provenance["requested_ref"] != expected_ref
        or provenance["resolver_id"] != "veritrail-r1-owned-snapshot-exact-oid"
        or provenance["resolver_version"] != "0.1"
        or type(provenance["resolved_at"]) is not str
        or not provenance["resolved_at"]
    ):
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")


def _validate_attempt_binding(
    attempt_binding: Mapping[str, object], continuity: Mapping[str, object]
) -> None:
    expected_keys = {
        "binding_function",
        "fact_consumer_attempt_id",
        "selector_claim_id",
        "derivation_id",
        "context_identity",
        "context",
        "budget_state",
        "stop_trigger",
        "parent_eligibility",
        "application_result_status",
        "continuity_state",
    }
    if type(attempt_binding) is not dict or set(attempt_binding) != expected_keys:
        _fail("MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED")
    context = attempt_binding.get("context")
    if type(context) is not dict or set(context) != {
        "budget_limits",
        "started_at_monotonic",
        "execution_deadline_monotonic",
    }:
        _fail("MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED")
    limits = context.get("budget_limits")
    if type(limits) is not dict or set(limits) != {
        "wall_clock_ms",
        "memory_bytes",
        "artifact_bytes",
    }:
        _fail("MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED")
    if any(type(limits[name]) is not int or limits[name] <= 0 for name in limits):
        _fail("MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED")
    started = context.get("started_at_monotonic")
    deadline = context.get("execution_deadline_monotonic")
    if (
        type(started) not in {int, float}
        or type(deadline) not in {int, float}
        or not math.isfinite(started)
        or not math.isfinite(deadline)
        or deadline <= started
    ):
        _fail("MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED")
    if (
        attempt_binding.get("binding_function") != ATTEMPT_BINDING_FUNCTION
        or attempt_binding.get("context_identity")
        != semantic_digest(CONTEXT_IDENTITY_DOMAIN, context)
        or attempt_binding.get("fact_consumer_attempt_id")
        != continuity.get("fact_consumer_attempt_id")
        or attempt_binding.get("selector_claim_id")
        != continuity.get("selector_claim_id")
        or attempt_binding.get("derivation_id") != continuity.get("derivation_id")
        or attempt_binding.get("budget_state") != "RUNNING"
        or attempt_binding.get("stop_trigger") is not None
        or attempt_binding.get("parent_eligibility") != "ADMITTED"
        or attempt_binding.get("application_result_status") != "ADMITTED"
        or attempt_binding.get("continuity_state") != "COMMITTED"
    ):
        _fail("MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED")


def _validate_evidence(
    evidence: dict[str, object],
    *,
    continuity: Mapping[str, object],
    application: Mapping[str, object],
    attempt_binding: Mapping[str, object],
    source_snapshot: Mapping[str, object],
) -> None:
    if evidence.get("schema_version") != "0.3":
        _fail("MANIFEST_CARRIER_SUCCESSOR_VERSION_REJECTED")
    if (
        set(evidence) != _EVIDENCE_KEYS
        or evidence.get("artifact_kind") != "DERIVATION_EVIDENCE"
        or evidence.get("canonicalization_profile") != "veritrail-json-c14n/1"
    ):
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")
    unsigned = copy.deepcopy(evidence)
    identity = unsigned.pop("derivation_evidence_digest")
    if identity != semantic_digest(EVIDENCE_IDENTITY_DOMAIN, unsigned):
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")

    branch = evidence["terminal_branch"]
    if type(branch) is not str:
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")
    if branch == "NORMAL_FULFILLED":
        expected_route = "RELATION_HANDOFF"
        expected_variant = "NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY"
        expected_result_kind = "NORMAL_REVIEW_SLICE_COVERAGE"
    elif branch in _NEGATIVE_BRANCHES:
        expected_route = "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"
        expected_variant = "NEGATIVE_WORLD_COVERAGE_CONTINUITY"
        expected_result_kind = "NEGATIVE_WORLD_COVERAGE"
    else:
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")
    if (
        evidence["selector_route"] != expected_route
        or evidence["continuity_variant"] != expected_variant
        or continuity.get("terminal_branch") != branch
        or continuity.get("selector_route") != expected_route
        or continuity.get("continuity_variant") != expected_variant
        or application.get("terminal_branch") != branch
        or application.get("selector_route") != expected_route
        or application.get("result_kind") != expected_result_kind
    ):
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")

    expected_cross_bindings = {
        "derivation_id": continuity.get("derivation_id"),
        "continuity_digest": continuity.get("continuity_digest"),
        "application_admission_digest": application.get(
            "application_admission_digest"
        ),
        "coverage_ledger_digest": application.get("coverage_ledger_digest"),
        "root_chain_digest": application.get("root_chain_digest"),
    }
    if any(evidence.get(key) != value for key, value in expected_cross_bindings.items()):
        _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")
    if (
        continuity.get("application_admission_digest")
        != application.get("application_admission_digest")
        or continuity.get("coverage_ledger_digest")
        != application.get("coverage_ledger_digest")
        or continuity.get("root_chain_digest")
        != application.get("root_chain_digest")
        or continuity.get("fact_consumer_attempt_id")
        != application.get("fact_consumer_attempt_id")
    ):
        _fail("MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED")
    _validate_attempt_binding(attempt_binding, continuity)
    for name in _INPUT_DIGEST_FIELDS:
        if (
            evidence.get(name) != continuity.get("input_digests", {}).get(name)
            or evidence.get(name) != application.get("input_digests", {}).get(name)
        ):
            _fail("MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED")
    _validate_request_provenance(
        evidence.get("request_provenance"), source_snapshot
    )


def _validate_files(
    entries: object,
    expected_records: object,
) -> tuple[dict[str, dict[str, object]], list[dict[str, object]]]:
    if type(entries) is not tuple:
        _fail("MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED")
    by_role: dict[str, dict[str, object]] = {}
    records: list[dict[str, object]] = []
    for item in entries:
        if type(item) is not dict or set(item) != {
            "role",
            "path",
            "bytes",
            "semantic_digest",
        }:
            _fail("MANIFEST_CARRIER_CHILD_BINDING_REJECTED")
        role = item["role"]
        if (
            type(role) is not str
            or type(item["path"]) is not str
            or type(item["semantic_digest"]) is not str
            or role not in _ROLE_PATHS
            or role in by_role
            or item["path"] != _ROLE_PATHS[role]
        ):
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        document = _document(
            item["bytes"], "MANIFEST_CARRIER_CHILD_BINDING_REJECTED"
        )
        digest_key = _SEMANTIC_DIGEST_KEYS[role]
        if (
            document.get(digest_key) != item["semantic_digest"]
        ):
            _fail("MANIFEST_CARRIER_CHILD_BINDING_REJECTED")
        record = {
            "role": role,
            "path": item["path"],
            "raw_sha256": hashlib.sha256(item["bytes"]).hexdigest(),
            "size_bytes": len(item["bytes"]),
            "semantic_digest": item["semantic_digest"],
        }
        by_role[role] = {**item, "document": document}
        records.append(record)
    expected_order = [
        role
        for role in (
            "SOURCE_SNAPSHOT",
            "REVIEW_POLICY",
            "DERIVATION_PROFILE",
            "DERIVATION_EVIDENCE",
            "FACT_SET",
            "RELATION_SET",
            "REVIEW_SLICE_SET",
            "COVERAGE_LEDGER",
        )
        if role in by_role
    ]
    if [item["role"] for item in entries] != expected_order:
        _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
    if expected_order[:4] != [
        "SOURCE_SNAPSHOT",
        "REVIEW_POLICY",
        "DERIVATION_PROFILE",
        "DERIVATION_EVIDENCE",
    ] or expected_order[-1:] != ["COVERAGE_LEDGER"]:
        _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
    if type(expected_records) is not tuple or list(expected_records) != records:
        _fail("MANIFEST_CARRIER_CHILD_BINDING_REJECTED")
    return by_role, records


def _validate_topology(
    *,
    evidence: Mapping[str, object],
    continuity: Mapping[str, object],
    application: Mapping[str, object],
    files: Mapping[str, Mapping[str, object]],
    ledger: Mapping[str, object],
) -> dict[str, object]:
    bindings = ledger.get("root_bindings")
    if (
        not isinstance(bindings, list)
        or [item.get("stage") for item in bindings] != list(_ROOT_STAGES)
    ):
        _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
    proof_rows = []
    for binding in bindings:
        stage = binding["stage"]
        state = binding.get("binding_state")
        present = stage in files
        if state == "ARTIFACT_PRESENT":
            if not present or binding.get("artifact_digest") != files[stage][
                "semantic_digest"
            ]:
                _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        elif state == "QUALIFIED_ABSENT":
            if present or type(binding.get("exact_absence")) is not str:
                _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        elif state == "QUALIFIED_UNKNOWN":
            if present or type(binding.get("unknown_cause")) is not str:
                _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        else:
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        proof_rows.append(copy.deepcopy(binding))

    branch = evidence["terminal_branch"]
    states = [row["binding_state"] for row in bindings]
    if branch == "NORMAL_FULFILLED":
        if states[:2] != ["ARTIFACT_PRESENT", "ARTIFACT_PRESENT"]:
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        relation_branch = bindings[1].get("terminal_branch")
        if relation_branch == "ADMITTED_CONFLICT":
            if states[2] != "QUALIFIED_UNKNOWN":
                _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        elif states[2] != "ARTIFACT_PRESENT":
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        if continuity.get("result_kind") != "NORMAL_REVIEW_SLICE_COVERAGE":
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
    else:
        if states != ["QUALIFIED_ABSENT"] * 3:
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        if any(stage in files for stage in _ROOT_STAGES):
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
        if continuity.get("result_kind") != "NEGATIVE_WORLD_COVERAGE":
            _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
    if (
        ledger.get("coverage_ledger_digest")
        != evidence.get("coverage_ledger_digest")
        or ledger.get("root_chain_digest") != evidence.get("root_chain_digest")
        or application.get("coverage_ledger_digest")
        != ledger.get("coverage_ledger_digest")
        or application.get("root_chain_digest") != ledger.get("root_chain_digest")
    ):
        _fail("MANIFEST_CARRIER_LEDGER_CONFORMANCE_REJECTED")
    return {
        "root_chain_digest": ledger["root_chain_digest"],
        "root_bindings": proof_rows,
    }


def validate_manifest_carrier_successor_snapshot(
    snapshot: Mapping[str, object],
) -> dict[str, object]:
    """Recompute a candidate without calling the producer projector."""

    if not isinstance(snapshot, Mapping):
        _fail("MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED")
    if (
        snapshot.get("independent_conformance_function")
        != INDEPENDENT_CONFORMANCE_FUNCTION
        or snapshot.get("producer_projection_function")
        == INDEPENDENT_CONFORMANCE_FUNCTION
        or snapshot.get("shared_expected_projector_state") is not False
    ):
        _fail("MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED")
    if snapshot.get("authority_ceiling") != _AUTHORITY_CEILING:
        _fail("MANIFEST_CARRIER_AUTHORITY_CEILING_REJECTED")

    continuity = _document(
        snapshot.get("continuity_bytes"),
        "MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED",
    )
    application = _document(
        snapshot.get("application_admission_bytes"),
        "MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED",
    )
    attempt_binding = _document(
        snapshot.get("attempt_binding_bytes"),
        "MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED",
    )
    files, records = _validate_files(
        snapshot.get("file_entries"), snapshot.get("file_records")
    )
    required_roles = {
        "SOURCE_SNAPSHOT",
        "REVIEW_POLICY",
        "DERIVATION_PROFILE",
        "DERIVATION_EVIDENCE",
        "COVERAGE_LEDGER",
    }
    if not required_roles <= set(files):
        _fail("MANIFEST_CARRIER_TOPOLOGY_REJECTED")
    evidence = files["DERIVATION_EVIDENCE"]["document"]
    source_snapshot = files["SOURCE_SNAPSHOT"]["document"]
    _validate_evidence(
        evidence,
        continuity=continuity,
        application=application,
        attempt_binding=attempt_binding,
        source_snapshot=source_snapshot,
    )

    expected_input_digests = {
        "source_snapshot_digest": source_snapshot.get("source_snapshot_digest"),
        "policy_digest": files["REVIEW_POLICY"]["document"].get("policy_digest"),
        "analysis_scope_digest": files["REVIEW_POLICY"]["document"].get(
            "analysis_scope_digest"
        ),
        "slice_policy_digest": files["REVIEW_POLICY"]["document"].get(
            "slice_policy_digest"
        ),
        "derivation_profile_digest": files["DERIVATION_PROFILE"]["document"].get(
            "profile_digest"
        ),
    }
    if any(evidence.get(key) != value for key, value in expected_input_digests.items()):
        _fail("MANIFEST_CARRIER_CHILD_BINDING_REJECTED")

    ledger = files["COVERAGE_LEDGER"]["document"]
    source = snapshot.get("coverage_ledger_conformance_source")
    if type(source) is not CoverageLedgerConformanceSource:
        _fail("MANIFEST_CARRIER_LEDGER_CONFORMANCE_REJECTED")
    try:
        validate_review_coverage_ledger(ledger, source)
    except Exception as exc:
        raise IndependentCarrierConformanceFailure(
            "MANIFEST_CARRIER_LEDGER_CONFORMANCE_REJECTED"
        ) from exc
    topology = _validate_topology(
        evidence=evidence,
        continuity=continuity,
        application=application,
        files=files,
        ledger=ledger,
    )
    file_binding_digest = semantic_digest(FILE_BINDING_DOMAIN, records)
    topology_digest = semantic_digest(TOPOLOGY_PROOF_DOMAIN, topology)
    report = {
        "validation_function": INDEPENDENT_CONFORMANCE_FUNCTION,
        "status": "QUALIFIED",
        "derivation_evidence_digest": evidence["derivation_evidence_digest"],
        "coverage_ledger_digest": ledger["coverage_ledger_digest"],
        "root_chain_digest": ledger["root_chain_digest"],
        "file_binding_digest": file_binding_digest,
        "topology_proof_digest": topology_digest,
    }
    report["validation_digest"] = semantic_digest(VALIDATION_DOMAIN, report)
    return report


def authority_ceiling_copy() -> dict[str, object]:
    return copy.deepcopy(_AUTHORITY_CEILING)
