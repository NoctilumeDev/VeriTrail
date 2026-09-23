from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from veritrail_review._review_slice_input_values import (
    OwnedAdmittedGraphSliceInput,
)
from veritrail_review.canonical import semantic_digest


_CROSS_VALIDATED_INPUT_TOKEN = object()


@dataclass(frozen=True)
class OwnedCrossValidatedAdmittedGraphSliceInput:
    """Private B-stage exact input history; no domain or Slice authority."""

    derivation_id: str
    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    slice_policy_digest: str
    derivation_profile_digest: str
    fact_set_digest: str
    observation_domain_digest: str
    qualification_digest: str
    relation_set_digest: str
    admission_witness_digest: str
    source_snapshot_canonical_bytes: bytes = field(repr=False)
    review_policy_canonical_bytes: bytes = field(repr=False)
    derivation_profile_canonical_bytes: bytes = field(repr=False)
    fact_set_document_bytes: bytes = field(repr=False)
    canonical_fact_set_artifact_bytes: bytes = field(repr=False)
    relation_set_document_bytes: bytes = field(repr=False)
    admission_witness_bytes: bytes = field(repr=False)
    verified_blob_bytes_by_object_identity: Mapping[str, bytes] = field(
        repr=False, compare=False
    )
    _joined: OwnedAdmittedGraphSliceInput = field(repr=False, compare=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        joined: OwnedAdmittedGraphSliceInput,
        fact_set_document_bytes: bytes,
        verified_blob_bytes_by_object_identity: Mapping[str, bytes],
    ) -> "OwnedCrossValidatedAdmittedGraphSliceInput":
        inputs = joined._owned_inputs()
        admitted = joined._owned_admission()
        owned_blobs = MappingProxyType(
            {
                key: value
                for key, value in sorted(
                    verified_blob_bytes_by_object_identity.items()
                )
            }
        )
        values = {
            "derivation_id": joined.derivation_id,
            "source_snapshot_digest": joined.source_snapshot_digest,
            "policy_digest": joined.policy_digest,
            "analysis_scope_digest": joined.analysis_scope_digest,
            "slice_policy_digest": joined.slice_policy_digest,
            "derivation_profile_digest": joined.derivation_profile_digest,
            "fact_set_digest": joined.fact_set_digest,
            "observation_domain_digest": joined.observation_domain_digest,
            "qualification_digest": joined.qualification_digest,
            "relation_set_digest": joined.relation_set_digest,
            "admission_witness_digest": joined.admission_witness_digest,
            "source_snapshot_canonical_bytes": (
                inputs.source_snapshot_canonical_bytes
            ),
            "review_policy_canonical_bytes": inputs.review_policy_canonical_bytes,
            "derivation_profile_canonical_bytes": (
                inputs.derivation_profile_canonical_bytes
            ),
            "fact_set_document_bytes": fact_set_document_bytes,
            "canonical_fact_set_artifact_bytes": fact_set_document_bytes + b"\n",
            "relation_set_document_bytes": admitted.relation_set_document_bytes,
            "admission_witness_bytes": admitted.admission_witness_bytes,
            "verified_blob_bytes_by_object_identity": owned_blobs,
            "_joined": joined,
        }
        return cls(
            **values,
            _state_seal=_private_state_seal(values),
            _construction_token=_CROSS_VALIDATED_INPUT_TOKEN,
        )

    def source_snapshot_document_copy(self) -> dict[str, object]:
        return _object(self.source_snapshot_canonical_bytes)

    def review_policy_document_copy(self) -> dict[str, object]:
        return _object(self.review_policy_canonical_bytes)

    def derivation_profile_document_copy(self) -> dict[str, object]:
        return _object(self.derivation_profile_canonical_bytes)

    def fact_set_document_copy(self) -> dict[str, object]:
        return _object(self.fact_set_document_bytes)

    def relation_set_document_copy(self) -> dict[str, object]:
        return _object(self.relation_set_document_bytes)

    def admission_witness_copy(self) -> dict[str, object]:
        return _object(self.admission_witness_bytes)

    def continuation_permitted(self) -> bool:
        return self._joined.continuation_permitted()

    def _owned_joined_input(self) -> OwnedAdmittedGraphSliceInput:
        return self._joined

    def _claim_obligation_domain(self) -> None:
        self._joined._claim_obligation_domain()


def _validate_cross_validated_input(
    value: OwnedCrossValidatedAdmittedGraphSliceInput,
) -> None:
    if (
        type(value) is not OwnedCrossValidatedAdmittedGraphSliceInput
        or value._construction_token is not _CROSS_VALIDATED_INPUT_TOKEN
    ):
        raise ValueError
    values = {
        field_name: getattr(value, field_name)
        for field_name in (
            "derivation_id",
            "source_snapshot_digest",
            "policy_digest",
            "analysis_scope_digest",
            "slice_policy_digest",
            "derivation_profile_digest",
            "fact_set_digest",
            "observation_domain_digest",
            "qualification_digest",
            "relation_set_digest",
            "admission_witness_digest",
            "source_snapshot_canonical_bytes",
            "review_policy_canonical_bytes",
            "derivation_profile_canonical_bytes",
            "fact_set_document_bytes",
            "canonical_fact_set_artifact_bytes",
            "relation_set_document_bytes",
            "admission_witness_bytes",
            "verified_blob_bytes_by_object_identity",
            "_joined",
        )
    }
    joined = value._owned_joined_input()
    if (
        value._state_seal != _private_state_seal(values)
        or value.canonical_fact_set_artifact_bytes
        != value.fact_set_document_bytes + b"\n"
        or type(joined) is not OwnedAdmittedGraphSliceInput
        or (
            value.derivation_id,
            value.source_snapshot_digest,
            value.policy_digest,
            value.analysis_scope_digest,
            value.slice_policy_digest,
            value.derivation_profile_digest,
            value.fact_set_digest,
            value.observation_domain_digest,
            value.qualification_digest,
            value.relation_set_digest,
            value.admission_witness_digest,
        )
        != (
            joined.derivation_id,
            joined.source_snapshot_digest,
            joined.policy_digest,
            joined.analysis_scope_digest,
            joined.slice_policy_digest,
            joined.derivation_profile_digest,
            joined.fact_set_digest,
            joined.observation_domain_digest,
            joined.qualification_digest,
            joined.relation_set_digest,
            joined.admission_witness_digest,
        )
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    payload: dict[str, object] = {}
    for key, value in values.items():
        if isinstance(value, bytes):
            payload[key] = hashlib.sha256(value).hexdigest()
        elif key == "verified_blob_bytes_by_object_identity":
            if not isinstance(value, Mapping):
                raise ValueError
            blob_digests: dict[str, str] = {}
            for oid, raw in sorted(value.items()):
                if not isinstance(oid, str) or not isinstance(raw, bytes):
                    raise ValueError
                blob_digests[oid] = hashlib.sha256(raw).hexdigest()
            payload[key] = blob_digests
        elif key == "_joined":
            if not isinstance(value, OwnedAdmittedGraphSliceInput):
                raise ValueError
            payload[key] = {
                "derivation_id": value.derivation_id,
                "qualification_digest": value.qualification_digest,
                "admission_witness_digest": value.admission_witness_digest,
            }
        else:
            payload[key] = value
    return semantic_digest(
        "veritrail.review.private-cross-validated-slice-input/0.1", payload
    )


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("owned cross-validated Slice input is not an object")
    return value
