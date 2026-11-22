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
LEDGER_DIGEST_DOMAIN = "veritrail.review.coverage-ledger/0.3"
ROOT_BINDING_DOMAIN = "veritrail.review.coverage-root-binding/0.1"
ROOT_CHAIN_DOMAIN = "veritrail.review.coverage-root-chain/0.1"
ROOT_BINDING_FUNCTION = "r1-review-coverage-root-binding-correction/0.1"

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


def _validate_carrier_proof(
    report: object,
    records: list[dict[str, object]],
    ledger: Mapping[str, object],
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
    ):
        _fail("MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED")
    return copy.deepcopy(report)


def _validate_ledger(ledger: dict[str, object]) -> list[dict[str, object]]:
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
    for item in bindings:
        if type(item) is not dict:
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        unsigned_binding = copy.deepcopy(item)
        binding_digest = unsigned_binding.pop("binding_digest", None)
        if binding_digest != semantic_digest(
            ROOT_BINDING_DOMAIN, unsigned_binding
        ):
            _fail("MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED")
        if previous is not None and item.get(
            "predecessor_binding_digest"
        ) != previous:
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
    ledger = documents["COVERAGE_LEDGER"]
    bindings = _validate_ledger(ledger)
    _validate_root_topology(bindings, documents)
    carrier_proof = _validate_carrier_proof(
        snapshot.get("carrier_validation"), records, ledger
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
