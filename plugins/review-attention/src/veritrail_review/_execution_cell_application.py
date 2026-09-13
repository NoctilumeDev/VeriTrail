from __future__ import annotations

import base64
import copy
import hashlib
import time
from dataclasses import dataclass
from typing import Any, Mapping

from veritrail_review._execution_cell_binding import (
    ProviderDescriptor,
    descriptor_for_launch_key,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.contracts import validate_source_snapshot_document
from veritrail_review.derivation_input import (
    _is_python_identifier,
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
)
from veritrail_review.derivation_input_contracts import (
    DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
    DerivationInputSet,
)


PROTOCOL = "veritrail-review-derivation-cell/0.1"
REQUEST_KIND = "DERIVATION_CELL_REQUEST"
TERMINAL_KIND = "DERIVATION_CELL_TERMINAL"

_DESCRIPTOR_KEYS = frozenset(
    {
        "capability_id",
        "provider_id",
        "provider_version",
        "parser_id",
        "parser_version",
        "runtime_id",
        "runtime_version",
    }
)
_REQUEST_KEYS = frozenset(
    {
        "protocol",
        "message_kind",
        "derivation_id",
        "request_provenance",
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "provider_descriptor",
        "operands_digest",
        "source_snapshot",
        "review_policy",
        "derivation_profile",
        "source_blobs",
    }
)
_TERMINAL_KEYS = frozenset(
    {
        "protocol",
        "message_kind",
        "derivation_id",
        "provider_descriptor",
        "operands_digest",
        "provider_run_id",
        "terminal_kind",
        "canonical_facts",
        "reported_fact_ids",
        "reported_relation_ids",
    }
)
_CANDIDATE_KEYS = frozenset(
    {
        "subject_space",
        "fact_kind",
        "source_anchor",
        "local_ordinal",
        "semantic_attributes",
    }
)
_FACT_KEYS = frozenset(
    {
        "fact_id",
        "subject_key_digest",
        "subject_space",
        "fact_kind",
        "source_snapshot_digest",
        "derivation_profile_digest",
        "source_anchor",
        "local_ordinal",
        "semantic_attributes",
        "provenance_refs",
    }
)
_TERMINAL_KINDS = frozenset(
    {
        "COMPLETED",
        "PROVIDER_UNAVAILABLE",
        "PROVIDER_FAILED",
        "NONCONFORMANT_PROVIDER_OUTPUT",
        "INTERNAL_DERIVATION_ERROR",
    }
)


class ApplicationProtocolError(ValueError):
    pass


class ClosedProviderUnavailable(RuntimeError):
    pass


class ClosedProviderFailed(RuntimeError):
    pass


@dataclass(frozen=True)
class ValidatedRequest:
    document: dict[str, object]
    descriptor: ProviderDescriptor
    provider_run_id: str
    source_sizes_by_path_hex: Mapping[str, int]
    in_scope_paths: frozenset[str]
    supported_paths: frozenset[str]


class _WorkerValidationState:
    profile = DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE

    @staticmethod
    def checkpoint(_stage: str) -> None:
        return


def build_request_document(
    *,
    inputs: DerivationInputSet,
    derivation_id: str,
    request_provenance: Mapping[str, object],
    descriptor: ProviderDescriptor,
) -> dict[str, object]:
    snapshot = inputs.source_snapshot_document_copy()
    policy = inputs.review_policy_document_copy()
    profile = inputs.derivation_profile_document_copy()
    descriptor_document = descriptor.document()
    operands_digest = provider_operands_digest(inputs, descriptor)
    source_blobs: list[dict[str, object]] = []
    for entry in snapshot["inventory"]:
        if not isinstance(entry, dict):
            raise ApplicationProtocolError("invalid owned inventory")
        git_object = entry.get("git_object")
        if not isinstance(git_object, dict) or git_object.get("object_type") != "BLOB":
            continue
        oid = git_object.get("hex")
        content = entry.get("content")
        if not isinstance(oid, str) or not isinstance(content, dict):
            raise ApplicationProtocolError("invalid owned blob identity")
        blob = inputs.verified_blob_bytes_by_object_identity.get(oid)
        if blob is None:
            raise ApplicationProtocolError("owned blob is unavailable")
        source_blobs.append(
            {
                "git_path": copy.deepcopy(entry["git_path"]),
                "size_bytes": len(blob),
                "content_sha256": hashlib.sha256(blob).hexdigest(),
                "content_base64": base64.b64encode(blob).decode("ascii"),
            }
        )
    source_blobs.sort(key=lambda item: bytes.fromhex(item["git_path"]["git_path_hex"]))  # type: ignore[index]
    return {
        "protocol": PROTOCOL,
        "message_kind": REQUEST_KIND,
        "derivation_id": derivation_id,
        "request_provenance": copy.deepcopy(dict(request_provenance)),
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "policy_digest": inputs.policy_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "slice_policy_digest": inputs.slice_policy_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        "provider_descriptor": descriptor_document,
        "operands_digest": operands_digest,
        "source_snapshot": snapshot,
        "review_policy": policy,
        "derivation_profile": profile,
        "source_blobs": source_blobs,
    }


def provider_operands_digest(
    inputs: DerivationInputSet, descriptor: ProviderDescriptor
) -> str:
    return semantic_digest(
        "veritrail.review.provider-operands/0.1",
        {
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "policy_digest": inputs.policy_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "slice_policy_digest": inputs.slice_policy_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            **descriptor.document(),
        },
    )


def provider_run_id(
    derivation_id: str, descriptor: ProviderDescriptor, operands_digest: str
) -> str:
    return semantic_digest(
        "veritrail.review.provider-run/0.1",
        {
            "derivation_id": derivation_id,
            "capability_id": descriptor.capability_id,
            "provider_id": descriptor.provider_id,
            "operands_digest": operands_digest,
        },
    )


def validate_request_document(
    document: Mapping[str, object], *, launch_key: str
) -> ValidatedRequest:
    try:
        if set(document) != _REQUEST_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != REQUEST_KIND:
            raise ValueError
        derivation_id = document["derivation_id"]
        if not _nonempty_text(derivation_id):
            raise ValueError
        descriptor = _descriptor_from_document(document["provider_descriptor"])
        expected = descriptor_for_launch_key(launch_key)
        if expected is None or descriptor != expected:
            raise ValueError
        request_provenance = document["request_provenance"]
        if not isinstance(request_provenance, Mapping) or set(request_provenance) != {
            "requested_repository_id",
            "requested_ref",
            "resolver_id",
            "resolver_version",
            "resolved_at",
        }:
            raise ValueError
        snapshot = document["source_snapshot"]
        policy = document["review_policy"]
        profile = document["derivation_profile"]
        if not all(isinstance(value, Mapping) for value in (snapshot, policy, profile)):
            raise ValueError
        state = _WorkerValidationState()
        validate_source_snapshot_document(
            snapshot,
            expected_bytes=canonical_json_bytes(snapshot) + b"\n",
            max_canonical_bytes=state.profile.max_source_snapshot_bytes,
        )
        _validate_profile(profile, state)  # type: ignore[arg-type]
        _validate_policy(policy, profile, state)  # type: ignore[arg-type]
        _validate_cross_artifact_binding(snapshot, policy, profile, state)  # type: ignore[arg-type]
        expected_digests = {
            "source_snapshot_digest": snapshot["source_snapshot_digest"],
            "policy_digest": policy["policy_digest"],
            "analysis_scope_digest": policy["analysis_scope_digest"],
            "slice_policy_digest": policy["slice_policy_digest"],
            "derivation_profile_digest": profile["profile_digest"],
        }
        for key, expected_digest in expected_digests.items():
            if document[key] != expected_digest:
                raise ValueError
        ephemeral_inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=canonical_json_bytes(snapshot) + b"\n",
            review_policy_canonical_bytes=canonical_json_bytes(policy) + b"\n",
            derivation_profile_canonical_bytes=canonical_json_bytes(profile) + b"\n",
            verified_blob_bytes_by_object_identity={},
            **expected_digests,
        )
        expected_operands = provider_operands_digest(ephemeral_inputs, descriptor)
        if document["operands_digest"] != expected_operands:
            raise ValueError
        run_id = provider_run_id(derivation_id, descriptor, expected_operands)
        sizes, supported = _validate_source_blobs(
            document["source_blobs"], snapshot, profile
        )
        in_scope = frozenset(
            item["git_path"]["git_path_hex"]
            for item in policy["scope_decisions"]
            if item["disposition"] == "IN_SCOPE"
        )
        coordinate = snapshot["source_coordinate"]
        commit_oid = coordinate["commit_oid"]
        expected_ref = f"oid:{commit_oid['algorithm'].lower()}:{commit_oid['hex']}"
        if (
            request_provenance["requested_repository_id"] != snapshot["repository_id"]
            or request_provenance["requested_ref"] != expected_ref
            or request_provenance["resolver_id"] != "veritrail-r1-owned-snapshot-exact-oid"
            or request_provenance["resolver_version"] != "0.1"
            or not _nonempty_text(request_provenance["resolved_at"])
        ):
            raise ValueError
        return ValidatedRequest(
            document=copy.deepcopy(dict(document)),
            descriptor=descriptor,
            provider_run_id=run_id,
            source_sizes_by_path_hex=sizes,
            in_scope_paths=in_scope,
            supported_paths=supported,
        )
    except Exception as exc:
        if isinstance(exc, ApplicationProtocolError):
            raise
        raise ApplicationProtocolError("nonconformant request envelope") from exc


def run_closed_test_provider(
    request: ValidatedRequest, *, launch_key: str
) -> list[dict[str, object]]:
    if launch_key in {
        "stable-a",
        "stable-b",
        "trailing-terminal",
        "partial-terminal",
        "duplicate-terminal",
        "terminal-then-sleep",
        "facts-on-failure",
    }:
        path_hex = sorted(request.supported_paths)[0]
        size = request.source_sizes_by_path_hex[path_hex]
        return [
            {
                "subject_space": "MODULE_ENTITY",
                "fact_kind": "MODULE",
                "source_anchor": {
                    "git_path": {"path_kind": "GIT_PATH", "git_path_hex": path_hex},
                    "start_byte": 0,
                    "end_byte": size,
                },
                "local_ordinal": 0,
                "semantic_attributes": {"module_key_parts": None},
            }
        ]
    if launch_key == "empty":
        return []
    if launch_key == "failed":
        raise ClosedProviderFailed
    if launch_key == "unavailable":
        raise ClosedProviderUnavailable
    if launch_key == "bad-candidate":
        path_hex = sorted(request.supported_paths)[0]
        size = request.source_sizes_by_path_hex[path_hex]
        return [
            {
                "subject_space": "MODULE_ENTITY",
                "fact_kind": "MODULE",
                "source_anchor": {
                    "git_path": {"path_kind": "GIT_PATH", "git_path_hex": path_hex},
                    "start_byte": 0,
                    "end_byte": size + 1,
                },
                "local_ordinal": 0,
                "semantic_attributes": {"module_key_parts": None},
            }
        ]
    if launch_key == "slow":
        time.sleep(60)
        return []
    if launch_key == "memory":
        retained: list[bytearray] = []
        while True:
            retained.append(bytearray(8 * 1024 * 1024))
    if launch_key == "self-reporting-candidate":
        path_hex = sorted(request.supported_paths)[0]
        size = request.source_sizes_by_path_hex[path_hex]
        return [
            {
                "subject_space": "MODULE_ENTITY",
                "fact_kind": "MODULE",
                "source_anchor": {
                    "git_path": {"path_kind": "GIT_PATH", "git_path_hex": path_hex},
                    "start_byte": 0,
                    "end_byte": size,
                },
                "local_ordinal": 0,
                "semantic_attributes": {"module_key_parts": None},
                "fact_id": "0" * 64,
                "execution_status": "COMPLETED",
            }
        ]
    raise ClosedProviderFailed


def canonicalize_candidates(
    request: ValidatedRequest, candidates: object
) -> list[dict[str, object]]:
    if not isinstance(candidates, list):
        raise ApplicationProtocolError("Provider candidates are not a list")
    by_fact_id: dict[str, dict[str, object]] = {}
    subject_to_fact: dict[str, str] = {}
    for candidate in candidates:
        fact = _canonicalize_candidate(request, candidate)
        fact_id = fact["fact_id"]
        subject = fact["subject_key_digest"]
        if not isinstance(fact_id, str) or not isinstance(subject, str):
            raise ApplicationProtocolError("invalid canonical Fact identity")
        previous = subject_to_fact.setdefault(subject, fact_id)
        if previous != fact_id:
            raise ApplicationProtocolError("one Provider reported a conflict")
        by_fact_id[fact_id] = fact
    return [by_fact_id[key] for key in sorted(by_fact_id)]


def terminal_document(
    request: ValidatedRequest,
    *,
    terminal_kind: str,
    canonical_facts: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    facts = copy.deepcopy(canonical_facts or [])
    ids = sorted({fact["fact_id"] for fact in facts})
    return {
        "protocol": PROTOCOL,
        "message_kind": TERMINAL_KIND,
        "derivation_id": request.document["derivation_id"],
        "provider_descriptor": request.descriptor.document(),
        "operands_digest": request.document["operands_digest"],
        "provider_run_id": request.provider_run_id,
        "terminal_kind": terminal_kind,
        "canonical_facts": facts,
        "reported_fact_ids": ids,
        "reported_relation_ids": [],
    }


def validate_terminal_document(
    document: Mapping[str, object], *, request: Mapping[str, object]
) -> dict[str, object]:
    try:
        if set(document) != _TERMINAL_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != TERMINAL_KIND:
            raise ValueError
        kind = document["terminal_kind"]
        if kind not in _TERMINAL_KINDS:
            raise ValueError
        descriptor = _descriptor_from_document(request["provider_descriptor"])
        run_id = provider_run_id(
            request["derivation_id"], descriptor, request["operands_digest"]
        )
        if (
            document["derivation_id"] != request["derivation_id"]
            or document["provider_descriptor"] != request["provider_descriptor"]
            or document["operands_digest"] != request["operands_digest"]
            or document["provider_run_id"] != run_id
        ):
            raise ValueError
        facts = document["canonical_facts"]
        fact_ids = document["reported_fact_ids"]
        relation_ids = document["reported_relation_ids"]
        if not isinstance(facts, list) or not isinstance(fact_ids, list) or relation_ids != []:
            raise ValueError
        if kind != "COMPLETED" and (facts or fact_ids):
            raise ValueError
        observed_ids: list[str] = []
        previous_fact_id: str | None = None
        for fact in facts:
            if not isinstance(fact, Mapping) or set(fact) != _FACT_KEYS:
                raise ValueError
            canonical_json_bytes(fact)
            fact_id = fact["fact_id"]
            if not isinstance(fact_id, str) or (
                previous_fact_id is not None and fact_id <= previous_fact_id
            ):
                raise ValueError
            previous_fact_id = fact_id
            if fact["provenance_refs"] != [run_id]:
                raise ValueError
            observed_ids.append(fact_id)
        if fact_ids != sorted(set(observed_ids)):
            raise ValueError
        return copy.deepcopy(dict(document))
    except Exception as exc:
        raise ApplicationProtocolError("nonconformant terminal envelope") from exc


def _canonicalize_candidate(
    request: ValidatedRequest, candidate: object
) -> dict[str, object]:
    if not isinstance(candidate, Mapping) or set(candidate) != _CANDIDATE_KEYS:
        raise ApplicationProtocolError("nonconformant candidate shape")
    anchor = candidate["source_anchor"]
    if not isinstance(anchor, Mapping) or set(anchor) != {
        "git_path",
        "start_byte",
        "end_byte",
    }:
        raise ApplicationProtocolError("nonconformant source anchor")
    git_path = anchor["git_path"]
    if not isinstance(git_path, Mapping) or set(git_path) != {
        "path_kind",
        "git_path_hex",
    } or git_path["path_kind"] != "GIT_PATH":
        raise ApplicationProtocolError("nonconformant source path")
    path_hex = git_path["git_path_hex"]
    if (
        not isinstance(path_hex, str)
        or path_hex not in request.in_scope_paths
        or path_hex not in request.supported_paths
    ):
        raise ApplicationProtocolError("candidate source is not eligible")
    start = anchor["start_byte"]
    end = anchor["end_byte"]
    size = request.source_sizes_by_path_hex[path_hex]
    if (
        type(start) is not int
        or type(end) is not int
        or start < 0
        or end < start
        or end > size
    ):
        raise ApplicationProtocolError("candidate anchor is outside its blob")
    ordinal = candidate["local_ordinal"]
    if type(ordinal) is not int or ordinal < 0:
        raise ApplicationProtocolError("invalid local ordinal")
    subject_space = candidate["subject_space"]
    fact_kind = candidate["fact_kind"]
    attributes = candidate["semantic_attributes"]
    _validate_fact_projection(
        subject_space=subject_space,
        fact_kind=fact_kind,
        anchor_start=start,
        anchor_end=end,
        blob_size=size,
        ordinal=ordinal,
        attributes=attributes,
    )
    owned_anchor = copy.deepcopy(dict(anchor))
    owned_attributes = copy.deepcopy(dict(attributes))
    snapshot_digest = request.document["source_snapshot_digest"]
    profile_digest = request.document["derivation_profile_digest"]
    subject_digest = semantic_digest(
        "veritrail.review.fact-subject/0.1",
        {
            "source_snapshot_digest": snapshot_digest,
            "derivation_profile_digest": profile_digest,
            "source_anchor": owned_anchor,
            "subject_space": subject_space,
            "local_ordinal": ordinal,
        },
    )
    fact_id = semantic_digest(
        "veritrail.review.code-fact/0.1",
        {
            "subject_key_digest": subject_digest,
            "fact_kind": fact_kind,
            "semantic_attributes": owned_attributes,
        },
    )
    return {
        "fact_id": fact_id,
        "subject_key_digest": subject_digest,
        "subject_space": subject_space,
        "fact_kind": fact_kind,
        "source_snapshot_digest": snapshot_digest,
        "derivation_profile_digest": profile_digest,
        "source_anchor": owned_anchor,
        "local_ordinal": ordinal,
        "semantic_attributes": owned_attributes,
        "provenance_refs": [request.provider_run_id],
    }


def _validate_fact_projection(
    *,
    subject_space: object,
    fact_kind: object,
    anchor_start: int,
    anchor_end: int,
    blob_size: int,
    ordinal: int,
    attributes: object,
) -> None:
    if not isinstance(attributes, Mapping):
        raise ApplicationProtocolError("semantic attributes are not an object")
    expected_spaces = {
        "MODULE": "MODULE_ENTITY",
        "CLASS_DECLARATION": "DECLARATION_NODE",
        "FUNCTION_DECLARATION": "DECLARATION_NODE",
        "METHOD_DECLARATION": "DECLARATION_NODE",
        "IMPORT_DECLARATION": "IMPORT_ALIAS",
    }
    if expected_spaces.get(fact_kind) != subject_space:
        raise ApplicationProtocolError("invalid Fact kind/space pair")
    if fact_kind == "MODULE":
        parts = attributes.get("module_key_parts")
        if set(attributes) != {"module_key_parts"} or (
            parts is not None
            and (
                not isinstance(parts, list)
                or any(not _is_python_identifier(item) for item in parts)
            )
        ):
            raise ApplicationProtocolError("invalid MODULE attributes")
        if ordinal != 0 or anchor_start != 0 or anchor_end != blob_size:
            raise ApplicationProtocolError("invalid MODULE identity")
        return
    if fact_kind == "CLASS_DECLARATION":
        if set(attributes) != {"declared_name"} or not _is_python_identifier(
            attributes.get("declared_name")
        ):
            raise ApplicationProtocolError("invalid class attributes")
    elif fact_kind in {"FUNCTION_DECLARATION", "METHOD_DECLARATION"}:
        if (
            set(attributes) != {"declared_name", "function_form"}
            or not _is_python_identifier(attributes.get("declared_name"))
            or attributes.get("function_form") not in {"SYNC", "ASYNC"}
        ):
            raise ApplicationProtocolError("invalid function attributes")
    elif fact_kind == "IMPORT_DECLARATION":
        if set(attributes) != {
            "import_form",
            "relative_level",
            "module_parts",
            "imported_name",
            "alias_name",
        }:
            raise ApplicationProtocolError("invalid import attributes")
        form = attributes["import_form"]
        level = attributes["relative_level"]
        parts = attributes["module_parts"]
        imported = attributes["imported_name"]
        alias = attributes["alias_name"]
        if (
            form not in {"IMPORT", "FROM_IMPORT"}
            or type(level) is not int
            or level < 0
            or not isinstance(parts, list)
            or any(not _is_python_identifier(item) for item in parts)
            or (alias is not None and not _is_python_identifier(alias))
        ):
            raise ApplicationProtocolError("invalid import attributes")
        if form == "IMPORT" and (level != 0 or not parts or imported is not None):
            raise ApplicationProtocolError("invalid IMPORT attributes")
        if form == "FROM_IMPORT" and not (
            imported == "*" or _is_python_identifier(imported)
        ):
            raise ApplicationProtocolError("invalid FROM_IMPORT attributes")
        if imported == "*" and alias is not None:
            raise ApplicationProtocolError("wildcard import cannot have alias")
    if ordinal != 0 and fact_kind != "IMPORT_DECLARATION":
        raise ApplicationProtocolError("invalid declaration ordinal")


def _validate_source_blobs(
    value: object, snapshot: Mapping[str, object], profile: Mapping[str, object]
) -> tuple[dict[str, int], frozenset[str]]:
    if not isinstance(value, list):
        raise ValueError
    expected_entries = [
        item
        for item in snapshot["inventory"]
        if item["git_object"]["object_type"] == "BLOB"
    ]
    if len(value) != len(expected_entries):
        raise ValueError
    sizes: dict[str, int] = {}
    supported: set[str] = set()
    previous_path: bytes | None = None
    for blob, entry in zip(value, expected_entries):
        if not isinstance(blob, Mapping) or set(blob) != {
            "git_path",
            "size_bytes",
            "content_sha256",
            "content_base64",
        }:
            raise ValueError
        if blob["git_path"] != entry["git_path"]:
            raise ValueError
        path_hex = blob["git_path"]["git_path_hex"]
        raw_path = bytes.fromhex(path_hex)
        if previous_path is not None and raw_path <= previous_path:
            raise ValueError
        previous_path = raw_path
        encoded = blob["content_base64"]
        if not isinstance(encoded, str):
            raise ValueError
        raw = base64.b64decode(encoded, validate=True)
        if base64.b64encode(raw).decode("ascii") != encoded:
            raise ValueError
        if (
            type(blob["size_bytes"]) is not int
            or blob["size_bytes"] != len(raw)
            or blob["size_bytes"] != entry["content"]["size_bytes"]
            or blob["content_sha256"] != hashlib.sha256(raw).hexdigest()
            or blob["content_sha256"] != entry["content"]["sha256"]
        ):
            raise ValueError
        sizes[path_hex] = len(raw)
        if (
            entry["entry_kind"] in profile["supported_entry_kinds"]
            and raw_path.endswith(b".py")
        ):
            supported.add(path_hex)
    return sizes, frozenset(supported)


def _descriptor_from_document(value: object) -> ProviderDescriptor:
    if not isinstance(value, Mapping) or set(value) != _DESCRIPTOR_KEYS:
        raise ValueError
    if any(not _nonempty_text(item) for item in value.values()):
        raise ValueError
    if value["capability_id"] != "python-ast":
        raise ValueError
    return ProviderDescriptor(**dict(value))  # type: ignore[arg-type]


def _nonempty_text(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and all(not 0xD800 <= ord(character) <= 0xDFFF for character in value)
    )
