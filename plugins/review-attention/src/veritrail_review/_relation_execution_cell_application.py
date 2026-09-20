from __future__ import annotations

import base64
import copy
import hashlib
from dataclasses import dataclass
from typing import Mapping

from veritrail_review._execution_cell_application import (
    _WorkerValidationState,
    _nonempty_text,
    _validate_fact_projection,
    _validate_source_blobs,
    provider_run_id,
)
from veritrail_review._execution_cell_binding import ProviderDescriptor
from veritrail_review._relation_execution_cell_binding import (
    relation_descriptor_for_launch_key,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.contracts import validate_source_snapshot_document
from veritrail_review.derivation_input import (
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
)
from veritrail_review.derivation_input_contracts import DerivationInputSet


PROTOCOL = "veritrail-review-relation-cell/0.1"
REQUEST_KIND = "RELATION_CELL_REQUEST"
TERMINAL_KIND = "RELATION_CELL_TERMINAL"

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
        "fact_set_digest",
        "operands_digest",
        "source_snapshot",
        "review_policy",
        "derivation_profile",
        "fact_set",
        "source_blobs",
    }
)
_TERMINAL_KEYS = frozenset(
    {
        "protocol",
        "message_kind",
        "derivation_id",
        "provider_descriptor",
        "fact_set_digest",
        "operands_digest",
        "provider_run_id",
        "terminal_kind",
        "canonical_relations",
        "reported_fact_ids",
        "reported_relation_ids",
    }
)
_SEMANTIC_FACT_KEYS = frozenset(
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
    }
)
_FACT_SET_PROJECTION_KEYS = frozenset(
    {
        "source_snapshot_digest",
        "analysis_scope_digest",
        "derivation_profile_digest",
        "facts",
        "conflicts",
    }
)
_RELATION_CANDIDATE_KEYS = frozenset(
    {
        "relation_space",
        "relation_kind",
        "source_fact_id",
        "local_ordinal",
        "target",
        "semantic_attributes",
    }
)
_RELATION_KEYS = frozenset(
    {
        "relation_id",
        "relation_subject_digest",
        *_RELATION_CANDIDATE_KEYS,
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


class RelationApplicationProtocolError(ValueError):
    pass


@dataclass(frozen=True)
class ValidatedRelationRequest:
    document: dict[str, object]
    descriptor: ProviderDescriptor
    provider_run_id: str
    facts_by_id: Mapping[str, dict[str, object]]
    source_blobs_by_path_hex: Mapping[str, bytes]


def _copy_relation_request_for_provider(
    request: ValidatedRelationRequest,
) -> ValidatedRelationRequest:
    """Give Provider code an owned copy while retaining application authority."""

    return ValidatedRelationRequest(
        document=copy.deepcopy(request.document),
        descriptor=ProviderDescriptor(**request.descriptor.document()),
        provider_run_id=str(request.provider_run_id),
        facts_by_id=copy.deepcopy(dict(request.facts_by_id)),
        source_blobs_by_path_hex={
            str(path_hex): memoryview(raw).tobytes()
            for path_hex, raw in request.source_blobs_by_path_hex.items()
        },
    )


def relation_provider_operands_digest(
    inputs: DerivationInputSet,
    descriptor: ProviderDescriptor,
    fact_set_digest: str,
) -> str:
    return semantic_digest(
        "veritrail.review.provider-operands/0.2",
        {
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "policy_digest": inputs.policy_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "slice_policy_digest": inputs.slice_policy_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            **descriptor.document(),
            "fact_set_digest": fact_set_digest,
        },
    )


def fact_set_semantic_projection(
    fact_set_document: Mapping[str, object],
) -> dict[str, object]:
    try:
        facts = fact_set_document["facts"]
        conflicts = fact_set_document["conflicts"]
        if not isinstance(facts, list) or not isinstance(conflicts, list):
            raise ValueError
        return {
            "source_snapshot_digest": fact_set_document["source_snapshot_digest"],
            "analysis_scope_digest": fact_set_document["analysis_scope_digest"],
            "derivation_profile_digest": fact_set_document[
                "derivation_profile_digest"
            ],
            "facts": [
                {
                    key: copy.deepcopy(value)
                    for key, value in fact.items()
                    if key != "provenance_refs"
                }
                for fact in facts
            ],
            "conflicts": [
                {
                    key: copy.deepcopy(value)
                    for key, value in conflict.items()
                    if key != "provenance_refs"
                }
                for conflict in conflicts
            ],
        }
    except Exception as exc:
        raise RelationApplicationProtocolError("invalid FactSet operand") from exc


def build_relation_request_document(
    *,
    inputs: DerivationInputSet,
    derivation_id: str,
    request_provenance: Mapping[str, object],
    descriptor: ProviderDescriptor,
    fact_set_document: Mapping[str, object],
) -> dict[str, object]:
    snapshot = inputs.source_snapshot_document_copy()
    policy = inputs.review_policy_document_copy()
    profile = inputs.derivation_profile_document_copy()
    projection = fact_set_semantic_projection(fact_set_document)
    fact_set_digest = fact_set_document.get("fact_set_digest")
    if not isinstance(fact_set_digest, str):
        raise RelationApplicationProtocolError("invalid FactSet digest")
    if fact_set_digest != semantic_digest(
        "veritrail.review.fact-set/0.1", projection
    ):
        raise RelationApplicationProtocolError("FactSet digest mismatch")
    source_blobs = _owned_source_blobs(inputs, snapshot)
    operands_digest = relation_provider_operands_digest(
        inputs, descriptor, fact_set_digest
    )
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
        "provider_descriptor": descriptor.document(),
        "fact_set_digest": fact_set_digest,
        "operands_digest": operands_digest,
        "source_snapshot": snapshot,
        "review_policy": policy,
        "derivation_profile": profile,
        "fact_set": projection,
        "source_blobs": source_blobs,
    }


def validate_relation_request_document(
    document: Mapping[str, object], *, launch_key: str
) -> ValidatedRelationRequest:
    try:
        if set(document) != _REQUEST_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != REQUEST_KIND:
            raise ValueError
        derivation_id = document["derivation_id"]
        if not _nonempty_text(derivation_id):
            raise ValueError
        descriptor = _descriptor_from_document(document["provider_descriptor"])
        expected = relation_descriptor_for_launch_key(launch_key)
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
        _validate_relation_requirement(policy)
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
        sizes, supported = _validate_source_blobs(
            document["source_blobs"], snapshot, profile
        )
        source_blobs = _decode_source_blobs(document["source_blobs"])
        in_scope = frozenset(
            item["git_path"]["git_path_hex"]
            for item in policy["scope_decisions"]
            if item["disposition"] == "IN_SCOPE"
        )
        fact_projection = document["fact_set"]
        facts_by_id = _validate_fact_set_projection(
            fact_projection,
            fact_set_digest=document["fact_set_digest"],
            expected_digests=expected_digests,
            source_sizes_by_path_hex=sizes,
            in_scope_paths=in_scope,
            supported_paths=supported,
        )
        ephemeral_inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=canonical_json_bytes(snapshot) + b"\n",
            review_policy_canonical_bytes=canonical_json_bytes(policy) + b"\n",
            derivation_profile_canonical_bytes=canonical_json_bytes(profile) + b"\n",
            verified_blob_bytes_by_object_identity={},
            **expected_digests,
        )
        expected_operands = relation_provider_operands_digest(
            ephemeral_inputs, descriptor, document["fact_set_digest"]
        )
        if document["operands_digest"] != expected_operands:
            raise ValueError
        run_id = provider_run_id(derivation_id, descriptor, expected_operands)
        coordinate = snapshot["source_coordinate"]
        commit_oid = coordinate["commit_oid"]
        expected_ref = f"oid:{commit_oid['algorithm'].lower()}:{commit_oid['hex']}"
        if (
            request_provenance["requested_repository_id"] != snapshot["repository_id"]
            or request_provenance["requested_ref"] != expected_ref
            or request_provenance["resolver_id"]
            != "veritrail-r1-owned-snapshot-exact-oid"
            or request_provenance["resolver_version"] != "0.1"
            or not _nonempty_text(request_provenance["resolved_at"])
        ):
            raise ValueError
        return ValidatedRelationRequest(
            document=copy.deepcopy(dict(document)),
            descriptor=descriptor,
            provider_run_id=run_id,
            facts_by_id=facts_by_id,
            source_blobs_by_path_hex=source_blobs,
        )
    except Exception as exc:
        if isinstance(exc, RelationApplicationProtocolError):
            raise
        raise RelationApplicationProtocolError(
            "nonconformant Relation request envelope"
        ) from exc


def canonicalize_relation_candidates(
    request: ValidatedRelationRequest, candidates: object
) -> list[dict[str, object]]:
    if not isinstance(candidates, list):
        raise RelationApplicationProtocolError("Relation candidates are not a list")
    by_id: dict[str, dict[str, object]] = {}
    subject_to_id: dict[str, str] = {}
    for candidate in candidates:
        relation = _canonicalize_relation_candidate(request, candidate)
        relation_id = relation["relation_id"]
        subject = relation["relation_subject_digest"]
        previous = subject_to_id.setdefault(subject, relation_id)
        if previous != relation_id:
            raise RelationApplicationProtocolError(
                "one Relation Provider reported a conflict"
            )
        by_id[relation_id] = relation
    return [by_id[key] for key in sorted(by_id)]


def relation_terminal_document(
    request: ValidatedRelationRequest,
    *,
    terminal_kind: str,
    canonical_relations: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    relations = copy.deepcopy(canonical_relations or [])
    if terminal_kind not in _TERMINAL_KINDS:
        raise RelationApplicationProtocolError("invalid terminal kind")
    if terminal_kind != "COMPLETED" and relations:
        raise RelationApplicationProtocolError("non-success terminal retained candidates")
    return {
        "protocol": PROTOCOL,
        "message_kind": TERMINAL_KIND,
        "derivation_id": request.document["derivation_id"],
        "provider_descriptor": request.descriptor.document(),
        "fact_set_digest": request.document["fact_set_digest"],
        "operands_digest": request.document["operands_digest"],
        "provider_run_id": request.provider_run_id,
        "terminal_kind": terminal_kind,
        "canonical_relations": relations,
        "reported_fact_ids": [],
        "reported_relation_ids": [item["relation_id"] for item in relations],
    }


def validate_relation_terminal_document(
    document: Mapping[str, object], *, request: Mapping[str, object]
) -> dict[str, object]:
    try:
        if set(document) != _TERMINAL_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != TERMINAL_KIND:
            raise ValueError
        terminal_kind = document["terminal_kind"]
        if terminal_kind not in _TERMINAL_KINDS:
            raise ValueError
        descriptor = _descriptor_from_document(request["provider_descriptor"])
        run_id = provider_run_id(
            request["derivation_id"], descriptor, request["operands_digest"]
        )
        if (
            document["derivation_id"] != request["derivation_id"]
            or document["provider_descriptor"] != request["provider_descriptor"]
            or document["fact_set_digest"] != request["fact_set_digest"]
            or document["operands_digest"] != request["operands_digest"]
            or document["provider_run_id"] != run_id
            or document["reported_fact_ids"] != []
        ):
            raise ValueError
        relations = document["canonical_relations"]
        reported = document["reported_relation_ids"]
        if not isinstance(relations, list) or not isinstance(reported, list):
            raise ValueError
        if terminal_kind != "COMPLETED" and (relations or reported):
            raise ValueError
        facts = request["fact_set"]["facts"]
        facts_by_id = {fact["fact_id"]: copy.deepcopy(fact) for fact in facts}
        previous_id: str | None = None
        subjects: set[str] = set()
        for relation in relations:
            _validate_canonical_relation(
                relation, run_id=run_id, request=request, facts_by_id=facts_by_id
            )
            relation_id = relation["relation_id"]
            if previous_id is not None and relation_id <= previous_id:
                raise ValueError
            previous_id = relation_id
            subject = relation["relation_subject_digest"]
            if subject in subjects:
                raise ValueError
            subjects.add(subject)
        expected_ids = [relation["relation_id"] for relation in relations]
        if reported != expected_ids or reported != sorted(set(reported)):
            raise ValueError
        return copy.deepcopy(dict(document))
    except Exception as exc:
        if isinstance(exc, RelationApplicationProtocolError):
            raise
        raise RelationApplicationProtocolError(
            "nonconformant Relation terminal envelope"
        ) from exc


def _owned_source_blobs(
    inputs: DerivationInputSet, snapshot: Mapping[str, object]
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for entry in snapshot["inventory"]:
        git_object = entry.get("git_object")
        if not isinstance(git_object, dict) or git_object.get("object_type") != "BLOB":
            continue
        oid = git_object.get("hex")
        if not isinstance(oid, str):
            raise RelationApplicationProtocolError("invalid owned blob identity")
        blob = inputs.verified_blob_bytes_by_object_identity.get(oid)
        if blob is None:
            raise RelationApplicationProtocolError("owned blob is unavailable")
        result.append(
            {
                "git_path": copy.deepcopy(entry["git_path"]),
                "size_bytes": len(blob),
                "content_sha256": hashlib.sha256(blob).hexdigest(),
                "content_base64": base64.b64encode(blob).decode("ascii"),
            }
        )
    result.sort(key=lambda item: bytes.fromhex(item["git_path"]["git_path_hex"]))
    return result


def _decode_source_blobs(value: object) -> dict[str, bytes]:
    if not isinstance(value, list):
        raise ValueError
    result: dict[str, bytes] = {}
    for item in value:
        path_hex = item["git_path"]["git_path_hex"]
        encoded = item["content_base64"]
        result[path_hex] = base64.b64decode(encoded, validate=True)
    return result


def _validate_relation_requirement(policy: Mapping[str, object]) -> None:
    requirements = policy["provider_requirements"]
    allowed = {
        "python-ast": True,
        "python-ast-advisory": False,
        "review-relation-derivation": True,
    }
    seen: dict[str, bool] = {}
    for item in requirements:
        capability = item["capability_id"]
        if (
            capability not in allowed
            or item["required"] is not allowed[capability]
            or item["composition_mode"] != "CUMULATIVE"
            or capability in seen
        ):
            raise ValueError
        seen[capability] = item["required"]
    if "python-ast" not in seen or "review-relation-derivation" not in seen:
        raise ValueError
    if set(seen) not in (
        {"python-ast", "review-relation-derivation"},
        {"python-ast", "python-ast-advisory", "review-relation-derivation"},
    ):
        raise ValueError


def _validate_fact_set_projection(
    value: object,
    *,
    fact_set_digest: object,
    expected_digests: Mapping[str, object],
    source_sizes_by_path_hex: Mapping[str, int],
    in_scope_paths: frozenset[str],
    supported_paths: frozenset[str],
) -> dict[str, dict[str, object]]:
    if not isinstance(value, Mapping) or set(value) != _FACT_SET_PROJECTION_KEYS:
        raise ValueError
    if (
        value["source_snapshot_digest"] != expected_digests["source_snapshot_digest"]
        or value["analysis_scope_digest"] != expected_digests["analysis_scope_digest"]
        or value["derivation_profile_digest"]
        != expected_digests["derivation_profile_digest"]
        or value["conflicts"] != []
        or fact_set_digest
        != semantic_digest("veritrail.review.fact-set/0.1", value)
    ):
        raise ValueError
    facts = value["facts"]
    if not isinstance(facts, list):
        raise ValueError
    result: dict[str, dict[str, object]] = {}
    previous_id: str | None = None
    for fact in facts:
        if not isinstance(fact, Mapping) or set(fact) != _SEMANTIC_FACT_KEYS:
            raise ValueError
        owned = copy.deepcopy(dict(fact))
        _validate_semantic_fact(
            owned,
            expected_digests=expected_digests,
            source_sizes_by_path_hex=source_sizes_by_path_hex,
            in_scope_paths=in_scope_paths,
            supported_paths=supported_paths,
        )
        fact_id = owned["fact_id"]
        if not isinstance(fact_id, str) or (
            previous_id is not None and fact_id <= previous_id
        ):
            raise ValueError
        previous_id = fact_id
        result[fact_id] = owned
    return result


def _validate_semantic_fact(
    fact: Mapping[str, object],
    *,
    expected_digests: Mapping[str, object],
    source_sizes_by_path_hex: Mapping[str, int],
    in_scope_paths: frozenset[str],
    supported_paths: frozenset[str],
) -> None:
    anchor = fact["source_anchor"]
    if not isinstance(anchor, Mapping) or set(anchor) != {
        "git_path",
        "start_byte",
        "end_byte",
    }:
        raise ValueError
    git_path = anchor["git_path"]
    if not isinstance(git_path, Mapping) or set(git_path) != {
        "path_kind",
        "git_path_hex",
    } or git_path["path_kind"] != "GIT_PATH":
        raise ValueError
    path_hex = git_path["git_path_hex"]
    if path_hex not in in_scope_paths or path_hex not in supported_paths:
        raise ValueError
    size = source_sizes_by_path_hex[path_hex]
    start = anchor["start_byte"]
    end = anchor["end_byte"]
    ordinal = fact["local_ordinal"]
    if (
        type(start) is not int
        or type(end) is not int
        or start < 0
        or end < start
        or end > size
        or type(ordinal) is not int
        or ordinal < 0
    ):
        raise ValueError
    _validate_fact_projection(
        subject_space=fact["subject_space"],
        fact_kind=fact["fact_kind"],
        anchor_start=start,
        anchor_end=end,
        blob_size=size,
        ordinal=ordinal,
        attributes=fact["semantic_attributes"],
    )
    if (
        fact["source_snapshot_digest"] != expected_digests["source_snapshot_digest"]
        or fact["derivation_profile_digest"]
        != expected_digests["derivation_profile_digest"]
    ):
        raise ValueError
    subject = semantic_digest(
        "veritrail.review.fact-subject/0.1",
        {
            "source_snapshot_digest": fact["source_snapshot_digest"],
            "derivation_profile_digest": fact["derivation_profile_digest"],
            "source_anchor": copy.deepcopy(anchor),
            "subject_space": fact["subject_space"],
            "local_ordinal": ordinal,
        },
    )
    fact_id = semantic_digest(
        "veritrail.review.code-fact/0.1",
        {
            "subject_key_digest": subject,
            "fact_kind": fact["fact_kind"],
            "semantic_attributes": copy.deepcopy(fact["semantic_attributes"]),
        },
    )
    if fact["subject_key_digest"] != subject or fact["fact_id"] != fact_id:
        raise ValueError


def _canonicalize_relation_candidate(
    request: ValidatedRelationRequest, candidate: object
) -> dict[str, object]:
    if not isinstance(candidate, Mapping) or set(candidate) != _RELATION_CANDIDATE_KEYS:
        raise RelationApplicationProtocolError("nonconformant Relation candidate")
    source_id = candidate["source_fact_id"]
    target = candidate["target"]
    ordinal = candidate["local_ordinal"]
    if (
        candidate["relation_space"] != "CHILD_EDGE"
        or candidate["relation_kind"] != "LEXICAL_CONTAINS"
        or not isinstance(source_id, str)
        or source_id not in request.facts_by_id
        or type(ordinal) is not int
        or ordinal < 0
        or candidate["semantic_attributes"] != {}
        or not isinstance(target, Mapping)
        or set(target) != {"target_kind", "fact_id"}
        or target["target_kind"] != "FACT"
        or not isinstance(target["fact_id"], str)
        or target["fact_id"] not in request.facts_by_id
    ):
        raise RelationApplicationProtocolError("invalid Relation projection")
    source = request.facts_by_id[source_id]
    target_fact = request.facts_by_id[target["fact_id"]]
    if (
        source["fact_kind"] != "MODULE"
        or target_fact["fact_kind"] != "IMPORT_DECLARATION"
        or source["source_anchor"]["git_path"]
        != target_fact["source_anchor"]["git_path"]
    ):
        raise RelationApplicationProtocolError("invalid fixture Relation endpoints")
    owned_target = copy.deepcopy(dict(target))
    subject = semantic_digest(
        "veritrail.review.relation-subject/0.1",
        {
            "source_snapshot_digest": request.document["source_snapshot_digest"],
            "derivation_profile_digest": request.document[
                "derivation_profile_digest"
            ],
            "relation_space": "CHILD_EDGE",
            "source_fact_id": source_id,
            "local_ordinal": ordinal,
        },
    )
    relation_id = semantic_digest(
        "veritrail.review.structural-relation/0.1",
        {
            "relation_subject_digest": subject,
            "relation_kind": "LEXICAL_CONTAINS",
            "target": owned_target,
            "semantic_attributes": {},
        },
    )
    return {
        "relation_id": relation_id,
        "relation_subject_digest": subject,
        "relation_space": "CHILD_EDGE",
        "relation_kind": "LEXICAL_CONTAINS",
        "source_fact_id": source_id,
        "local_ordinal": ordinal,
        "target": owned_target,
        "semantic_attributes": {},
        "provenance_refs": [request.provider_run_id],
    }


def _validate_canonical_relation(
    relation: object,
    *,
    run_id: str,
    request: Mapping[str, object],
    facts_by_id: Mapping[str, dict[str, object]],
) -> None:
    if not isinstance(relation, Mapping) or set(relation) != _RELATION_KEYS:
        raise ValueError
    candidate = {
        key: copy.deepcopy(relation[key]) for key in _RELATION_CANDIDATE_KEYS
    }
    synthetic = ValidatedRelationRequest(
        document=copy.deepcopy(dict(request)),
        descriptor=_descriptor_from_document(request["provider_descriptor"]),
        provider_run_id=run_id,
        facts_by_id=facts_by_id,
        source_blobs_by_path_hex={},
    )
    expected = _canonicalize_relation_candidate(synthetic, candidate)
    if relation != expected or relation["provenance_refs"] != [run_id]:
        raise ValueError


def _descriptor_from_document(value: object) -> ProviderDescriptor:
    if not isinstance(value, Mapping) or set(value) != _DESCRIPTOR_KEYS:
        raise ValueError
    if any(not _nonempty_text(item) for item in value.values()):
        raise ValueError
    if value["capability_id"] != "review-relation-derivation":
        raise ValueError
    return ProviderDescriptor(**dict(value))  # type: ignore[arg-type]
