from __future__ import annotations

import base64
import copy
import hashlib
from dataclasses import dataclass
from typing import Mapping

from veritrail_review._execution_cell_application import (
    ApplicationProtocolError,
    _canonicalize_candidate,
    _descriptor_from_document,
    _nonempty_text,
    provider_run_id,
)
from veritrail_review._execution_cell_binding import (
    ProviderDescriptor,
    descriptor_for_launch_key,
)
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
    _validate_language_support_classification,
)
from veritrail_review._source_operation_projection_values import (
    OwnedSourceOperationProjection,
    _validate_source_operation_projection,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.contracts import validate_source_snapshot_document
from veritrail_review.derivation_input import (
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
)
from veritrail_review.derivation_input_contracts import (
    DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
    DerivationInputSet,
)


PROTOCOL = "veritrail-review-derivation-cell/0.2"
REQUEST_KIND = "DERIVATION_CELL_REQUEST"
TERMINAL_KIND = "DERIVATION_CELL_TERMINAL"
OPERANDS_DOMAIN = "veritrail.review.provider-operands/0.4"

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
        "language_support_classification",
        "source_operation_projection",
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


class FactSourceOperationProtocolError(ValueError):
    """The private corrected Fact wire failed application validation."""


@dataclass(frozen=True)
class ValidatedFactSourceOperationRequest:
    document: dict[str, object]
    descriptor: ProviderDescriptor
    provider_run_id: str
    source_sizes_by_path_hex: Mapping[str, int]
    in_scope_paths: frozenset[str]
    supported_paths: frozenset[str]
    source_blobs_by_path_hex: Mapping[str, bytes]


class _WorkerValidationState:
    profile = DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE

    @staticmethod
    def checkpoint(_stage: str) -> None:
        return


def fact_source_operation_operands_digest(
    inputs: DerivationInputSet,
    descriptor: ProviderDescriptor,
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> str:
    """Bind the historical Fact operands plus exact 0.2 gate semantics."""

    _validate_language_support_classification(classification)
    _validate_source_operation_projection(projection)
    return _operands_digest_from_parts(
        source_snapshot_digest=inputs.source_snapshot_digest,
        policy_digest=inputs.policy_digest,
        analysis_scope_digest=inputs.analysis_scope_digest,
        slice_policy_digest=inputs.slice_policy_digest,
        derivation_profile_digest=inputs.derivation_profile_digest,
        descriptor=descriptor,
        language_support_function=classification.language_support_function,
        classification_digest=classification.classification_digest,
        source_operation_projection_digest=(
            projection.source_operation_projection_digest
        ),
    )


def build_fact_source_operation_request_document(
    *,
    inputs: DerivationInputSet,
    derivation_id: str,
    request_provenance: Mapping[str, object],
    descriptor: ProviderDescriptor,
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> dict[str, object]:
    """Build a corrected Fact request without integrating a controller."""

    snapshot = inputs.source_snapshot_document_copy()
    policy = inputs.review_policy_document_copy()
    profile = inputs.derivation_profile_document_copy()
    _validate_frozen_documents(snapshot, policy, profile)
    expected_digests = _expected_digests(snapshot, policy, profile)
    _require_input_digests(inputs, expected_digests)
    _validate_classification_metadata(
        classification, snapshot=snapshot, policy=policy, profile=profile
    )
    _validate_fact_projection(
        projection,
        classification=classification,
        descriptor=descriptor,
        expected_digests=expected_digests,
    )
    source_blobs, _, _ = _owned_operation_source_blobs(
        inputs, classification, projection
    )
    operands_digest = fact_source_operation_operands_digest(
        inputs, descriptor, classification, projection
    )
    return {
        "protocol": PROTOCOL,
        "message_kind": REQUEST_KIND,
        "derivation_id": derivation_id,
        "request_provenance": copy.deepcopy(dict(request_provenance)),
        **expected_digests,
        "provider_descriptor": descriptor.document(),
        "operands_digest": operands_digest,
        "source_snapshot": snapshot,
        "review_policy": policy,
        "derivation_profile": profile,
        "language_support_classification": (
            classification.classification_document_copy()
        ),
        "source_operation_projection": projection.projection_document_copy(),
        "source_blobs": source_blobs,
    }


def validate_fact_source_operation_request_document(
    document: Mapping[str, object], *, launch_key: str
) -> ValidatedFactSourceOperationRequest:
    """Validate the 0.2 request without reacquiring omitted source bodies."""

    try:
        if set(document) != _REQUEST_KEYS:
            raise ValueError
        if document["protocol"] != PROTOCOL or document["message_kind"] != REQUEST_KIND:
            raise ValueError
        derivation_id = document["derivation_id"]
        if not _nonempty_text(derivation_id):
            raise ValueError
        descriptor = _descriptor_from_document(document["provider_descriptor"])
        expected_descriptor = descriptor_for_launch_key(launch_key)
        if expected_descriptor is None or descriptor != expected_descriptor:
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
        classification_document = document["language_support_classification"]
        projection_document = document["source_operation_projection"]
        if not all(
            isinstance(value, Mapping)
            for value in (
                snapshot,
                policy,
                profile,
                classification_document,
                projection_document,
            )
        ):
            raise ValueError
        _validate_frozen_documents(snapshot, policy, profile)
        expected_digests = _expected_digests(snapshot, policy, profile)
        for key, expected_digest in expected_digests.items():
            if document[key] != expected_digest:
                raise ValueError
        classification = OwnedLanguageSupportClassification._create(
            source_snapshot_digest=expected_digests["source_snapshot_digest"],
            policy_digest=expected_digests["policy_digest"],
            analysis_scope_digest=expected_digests["analysis_scope_digest"],
            derivation_profile_digest=expected_digests[
                "derivation_profile_digest"
            ],
            classification_document=classification_document,
        )
        _validate_classification_metadata(
            classification, snapshot=snapshot, policy=policy, profile=profile
        )
        projection = OwnedSourceOperationProjection._create(projection_document)
        _validate_fact_projection(
            projection,
            classification=classification,
            descriptor=descriptor,
            expected_digests=expected_digests,
        )
        sizes, source_blobs = _validate_operation_source_blobs(
            document["source_blobs"], classification, projection
        )
        expected_operands = _operands_digest_from_parts(
            **expected_digests,
            descriptor=descriptor,
            language_support_function=classification.language_support_function,
            classification_digest=classification.classification_digest,
            source_operation_projection_digest=(
                projection.source_operation_projection_digest
            ),
        )
        if document["operands_digest"] != expected_operands:
            raise ValueError
        run_id = provider_run_id(derivation_id, descriptor, expected_operands)
        _validate_request_provenance(request_provenance, snapshot)
        denominator_paths = frozenset(
            _subject_path_hex(subject)
            for subject in classification.subjects_copy()
        )
        operation_paths = frozenset(source_blobs)
        return ValidatedFactSourceOperationRequest(
            document=copy.deepcopy(dict(document)),
            descriptor=descriptor,
            provider_run_id=run_id,
            source_sizes_by_path_hex=sizes,
            in_scope_paths=denominator_paths,
            supported_paths=operation_paths,
            source_blobs_by_path_hex=source_blobs,
        )
    except Exception as exc:
        if isinstance(exc, FactSourceOperationProtocolError):
            raise
        raise FactSourceOperationProtocolError(
            "nonconformant corrected Fact request envelope"
        ) from exc


def canonicalize_fact_candidates(
    request: ValidatedFactSourceOperationRequest, candidates: object
) -> list[dict[str, object]]:
    """Retain the frozen Fact candidate semantics under the corrected wire."""

    if not isinstance(candidates, list):
        raise FactSourceOperationProtocolError("Fact candidates are not a list")
    by_fact_id: dict[str, dict[str, object]] = {}
    subject_to_fact: dict[str, str] = {}
    try:
        for candidate in candidates:
            fact = _canonicalize_candidate(request, candidate)  # type: ignore[arg-type]
            fact_id = fact["fact_id"]
            subject = fact["subject_key_digest"]
            if not isinstance(fact_id, str) or not isinstance(subject, str):
                raise ValueError
            previous = subject_to_fact.setdefault(subject, fact_id)
            if previous != fact_id:
                raise ValueError
            by_fact_id[fact_id] = fact
        return [by_fact_id[key] for key in sorted(by_fact_id)]
    except (ApplicationProtocolError, ValueError) as exc:
        raise FactSourceOperationProtocolError(
            "nonconformant Fact candidates"
        ) from exc


def fact_source_operation_terminal_document(
    request: ValidatedFactSourceOperationRequest,
    *,
    terminal_kind: str,
    canonical_facts: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    facts = copy.deepcopy(canonical_facts or [])
    if terminal_kind not in _TERMINAL_KINDS:
        raise FactSourceOperationProtocolError("invalid terminal kind")
    if terminal_kind != "COMPLETED" and facts:
        raise FactSourceOperationProtocolError(
            "non-success terminal retained candidates"
        )
    return {
        "protocol": PROTOCOL,
        "message_kind": TERMINAL_KIND,
        "derivation_id": request.document["derivation_id"],
        "provider_descriptor": request.descriptor.document(),
        "operands_digest": request.document["operands_digest"],
        "provider_run_id": request.provider_run_id,
        "terminal_kind": terminal_kind,
        "canonical_facts": facts,
        "reported_fact_ids": [fact["fact_id"] for fact in facts],
        "reported_relation_ids": [],
    }


def validate_fact_source_operation_terminal_document(
    document: Mapping[str, object], *, request: Mapping[str, object]
) -> dict[str, object]:
    try:
        if set(document) != _TERMINAL_KEYS:
            raise ValueError
        if (
            document["protocol"] != PROTOCOL
            or document["message_kind"] != TERMINAL_KIND
        ):
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
            or document["operands_digest"] != request["operands_digest"]
            or document["provider_run_id"] != run_id
        ):
            raise ValueError
        facts = document["canonical_facts"]
        fact_ids = document["reported_fact_ids"]
        relation_ids = document["reported_relation_ids"]
        if not isinstance(facts, list) or not isinstance(fact_ids, list):
            raise ValueError
        if relation_ids != [] or (terminal_kind != "COMPLETED" and (facts or fact_ids)):
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
        if fact_ids != observed_ids or fact_ids != sorted(set(fact_ids)):
            raise ValueError
        return copy.deepcopy(dict(document))
    except Exception as exc:
        raise FactSourceOperationProtocolError(
            "nonconformant corrected Fact terminal envelope"
        ) from exc


def _operands_digest_from_parts(
    *,
    source_snapshot_digest: str,
    policy_digest: str,
    analysis_scope_digest: str,
    slice_policy_digest: str,
    derivation_profile_digest: str,
    descriptor: ProviderDescriptor,
    language_support_function: str,
    classification_digest: str,
    source_operation_projection_digest: str,
) -> str:
    return semantic_digest(
        OPERANDS_DOMAIN,
        {
            "source_snapshot_digest": source_snapshot_digest,
            "policy_digest": policy_digest,
            "analysis_scope_digest": analysis_scope_digest,
            "slice_policy_digest": slice_policy_digest,
            "derivation_profile_digest": derivation_profile_digest,
            **descriptor.document(),
            "language_support_function": language_support_function,
            "classification_digest": classification_digest,
            "source_operation_projection_digest": (
                source_operation_projection_digest
            ),
        },
    )


def _validate_frozen_documents(
    snapshot: Mapping[str, object],
    policy: Mapping[str, object],
    profile: Mapping[str, object],
) -> None:
    state = _WorkerValidationState()
    validate_source_snapshot_document(
        snapshot,
        expected_bytes=canonical_json_bytes(snapshot) + b"\n",
        max_canonical_bytes=state.profile.max_source_snapshot_bytes,
    )
    _validate_profile(profile, state)  # type: ignore[arg-type]
    _validate_policy(policy, profile, state)  # type: ignore[arg-type]
    _validate_cross_artifact_binding(
        snapshot, policy, profile, state  # type: ignore[arg-type]
    )


def _expected_digests(
    snapshot: Mapping[str, object],
    policy: Mapping[str, object],
    profile: Mapping[str, object],
) -> dict[str, str]:
    values = {
        "source_snapshot_digest": snapshot["source_snapshot_digest"],
        "policy_digest": policy["policy_digest"],
        "analysis_scope_digest": policy["analysis_scope_digest"],
        "slice_policy_digest": policy["slice_policy_digest"],
        "derivation_profile_digest": profile["profile_digest"],
    }
    if any(not isinstance(item, str) for item in values.values()):
        raise ValueError
    return values  # type: ignore[return-value]


def _require_input_digests(
    inputs: DerivationInputSet, expected: Mapping[str, str]
) -> None:
    for key, value in expected.items():
        if getattr(inputs, key) != value:
            raise FactSourceOperationProtocolError("exact input digest mismatch")


def _validate_classification_metadata(
    classification: OwnedLanguageSupportClassification,
    *,
    snapshot: Mapping[str, object],
    policy: Mapping[str, object],
    profile: Mapping[str, object],
) -> None:
    _validate_language_support_classification(classification)
    expected_digests = _expected_digests(snapshot, policy, profile)
    if (
        classification.source_snapshot_digest
        != expected_digests["source_snapshot_digest"]
        or classification.policy_digest != expected_digests["policy_digest"]
        or classification.analysis_scope_digest
        != expected_digests["analysis_scope_digest"]
        or classification.derivation_profile_digest
        != expected_digests["derivation_profile_digest"]
    ):
        raise ValueError
    inventory = snapshot["inventory"]
    decisions = policy["scope_decisions"]
    if not isinstance(inventory, list) or not isinstance(decisions, list):
        raise ValueError
    expected_subject_inputs: list[dict[str, object]] = []
    profile_semantics = {
        "language": profile["language"],
        "language_semantics": profile["language_semantics"],
        "supported_entry_kinds": list(profile["supported_entry_kinds"]),
        "accepted_source_encodings": sorted(
            set(profile["accepted_source_encodings"])
        ),
        "normalization_rules.path": profile["normalization_rules"]["path"],
    }
    for item, decision in zip(inventory, decisions, strict=True):
        if not isinstance(item, dict) or not isinstance(decision, dict):
            raise ValueError
        if item["git_path"] != decision["git_path"]:
            raise ValueError
        if decision["disposition"] != "IN_SCOPE":
            continue
        expected_subject_inputs.append(
            {
                "language_support_function": classification.language_support_function,
                "inventory_item": copy.deepcopy(item),
                "scope_semantics": {
                    "disposition": "IN_SCOPE",
                    "source_class": decision["source_class"],
                },
                "profile_support_semantics": copy.deepcopy(profile_semantics),
            }
        )
    expected_subject_inputs.sort(key=lambda item: _semantic_input_path(item))
    actual = [subject["semantic_input"] for subject in classification.subjects_copy()]
    if actual != expected_subject_inputs:
        raise ValueError


def _validate_fact_projection(
    projection: OwnedSourceOperationProjection,
    *,
    classification: OwnedLanguageSupportClassification,
    descriptor: ProviderDescriptor,
    expected_digests: Mapping[str, str],
) -> None:
    _validate_source_operation_projection(projection)
    eligible_ids = tuple(
        subject["subject_identity"]
        for subject in classification.subjects_copy()
        if subject["disposition"] == "ELIGIBLE"
    )
    if (
        projection.source_snapshot_digest
        != expected_digests["source_snapshot_digest"]
        or projection.policy_digest != expected_digests["policy_digest"]
        or projection.analysis_scope_digest
        != expected_digests["analysis_scope_digest"]
        or projection.derivation_profile_digest
        != expected_digests["derivation_profile_digest"]
        or projection.language_support_function
        != classification.language_support_function
        or projection.classification_digest
        != classification.classification_digest
        or projection.operation_kind != "FACT_DERIVATION"
        or projection.provider_descriptor_copy() != descriptor.document()
        or projection.fact_set_digest is not None
        or projection.observation_domain_digest is not None
        or projection.assigned_observation_item_ids != ()
        or projection.eligible_subject_ids != eligible_ids
        or projection.operation_subject_ids != eligible_ids
    ):
        raise ValueError


def _owned_operation_source_blobs(
    inputs: DerivationInputSet,
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> tuple[list[dict[str, object]], dict[str, int], dict[str, bytes]]:
    by_identity = {
        subject["subject_identity"]: subject
        for subject in classification.subjects_copy()
    }
    blobs: list[dict[str, object]] = []
    sizes: dict[str, int] = {}
    raw_by_path: dict[str, bytes] = {}
    for identity in projection.operation_subject_ids:
        subject = by_identity[identity]
        inventory = subject["semantic_input"]["inventory_item"]
        git_object = inventory["git_object"]
        content = inventory["content"]
        raw = inputs.verified_blob_bytes_by_object_identity[git_object["hex"]]
        path_hex = inventory["git_path"]["git_path_hex"]
        if (
            type(raw) is not bytes
            or len(raw) != content["size_bytes"]
            or hashlib.sha256(raw).hexdigest() != content["sha256"]
        ):
            raise FactSourceOperationProtocolError("owned operation body mismatch")
        blobs.append(
            {
                "git_path": copy.deepcopy(inventory["git_path"]),
                "size_bytes": len(raw),
                "content_sha256": hashlib.sha256(raw).hexdigest(),
                "content_base64": base64.b64encode(raw).decode("ascii"),
            }
        )
        sizes[path_hex] = len(raw)
        raw_by_path[path_hex] = memoryview(raw).tobytes()
    blobs.sort(
        key=lambda item: bytes.fromhex(
            item["git_path"]["git_path_hex"]  # type: ignore[index]
        )
    )
    return blobs, sizes, raw_by_path


def _validate_operation_source_blobs(
    value: object,
    classification: OwnedLanguageSupportClassification,
    projection: OwnedSourceOperationProjection,
) -> tuple[dict[str, int], dict[str, bytes]]:
    if not isinstance(value, list):
        raise ValueError
    by_identity = {
        subject["subject_identity"]: subject
        for subject in classification.subjects_copy()
    }
    if len(value) != len(projection.operation_subject_ids):
        raise ValueError
    sizes: dict[str, int] = {}
    raw_by_path: dict[str, bytes] = {}
    previous_path: bytes | None = None
    for blob, identity in zip(value, projection.operation_subject_ids, strict=True):
        subject = by_identity.get(identity)
        if not isinstance(blob, Mapping) or subject is None or set(blob) != {
            "git_path",
            "size_bytes",
            "content_sha256",
            "content_base64",
        }:
            raise ValueError
        inventory = subject["semantic_input"]["inventory_item"]
        if (
            subject["disposition"] != "ELIGIBLE"
            or blob["git_path"] != inventory["git_path"]
        ):
            raise ValueError
        path_hex = inventory["git_path"]["git_path_hex"]
        raw_path = bytes.fromhex(path_hex)
        if previous_path is not None and raw_path <= previous_path:
            raise ValueError
        previous_path = raw_path
        encoded = blob["content_base64"]
        if not isinstance(encoded, str):
            raise ValueError
        raw = base64.b64decode(encoded, validate=True)
        content = inventory["content"]
        digest = hashlib.sha256(raw).hexdigest()
        if (
            base64.b64encode(raw).decode("ascii") != encoded
            or type(blob["size_bytes"]) is not int
            or blob["size_bytes"] != len(raw)
            or blob["size_bytes"] != content["size_bytes"]
            or blob["content_sha256"] != digest
            or digest != content["sha256"]
        ):
            raise ValueError
        sizes[path_hex] = len(raw)
        raw_by_path[path_hex] = raw
    return sizes, raw_by_path


def _validate_request_provenance(
    value: Mapping[str, object], snapshot: Mapping[str, object]
) -> None:
    coordinate = snapshot["source_coordinate"]
    commit_oid = coordinate["commit_oid"]
    expected_ref = f"oid:{commit_oid['algorithm'].lower()}:{commit_oid['hex']}"
    if (
        value["requested_repository_id"] != snapshot["repository_id"]
        or value["requested_ref"] != expected_ref
        or value["resolver_id"] != "veritrail-r1-owned-snapshot-exact-oid"
        or value["resolver_version"] != "0.1"
        or not _nonempty_text(value["resolved_at"])
    ):
        raise ValueError


def _semantic_input_path(value: Mapping[str, object]) -> bytes:
    inventory = value["inventory_item"]
    return bytes.fromhex(inventory["git_path"]["git_path_hex"])  # type: ignore[index]


def _subject_path_hex(subject: Mapping[str, object]) -> str:
    semantic_input = subject["semantic_input"]
    inventory = semantic_input["inventory_item"]  # type: ignore[index]
    path = inventory["git_path"]  # type: ignore[index]
    return path["git_path_hex"]  # type: ignore[index,return-value]
