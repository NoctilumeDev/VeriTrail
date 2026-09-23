from __future__ import annotations

from typing import Mapping

from veritrail_review._multi_provider_fact_composition import _fact_set_document
from veritrail_review._relation_set_admission import (
    _validate_qualification,
    _validate_admission_attempt_binding,
    admit_relation_set_for_private_closed_proof,
)
from veritrail_review._review_slice_input_cross_validation_values import (
    OwnedCrossValidatedAdmittedGraphSliceInput,
    _validate_cross_validated_input,
)
from veritrail_review._review_slice_input_values import (
    OwnedAdmittedGraphInputAuthority,
    OwnedAdmittedGraphSliceInput,
    OwnedRelationQualificationContinuation,
    _ReviewSliceInputError,
    _ReviewSliceInputFailureCode,
    _VALIDATED_ADMISSION_ATTEMPT_TOKEN,
)
from veritrail_review.canonical import canonical_json_bytes, sha256_bytes
from veritrail_review.derivation_input import (
    _parse_artifact,
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
    _validate_snapshot,
)
from veritrail_review.derivation_input_contracts import (
    DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
    DerivationInputSet,
)
from veritrail_review.errors import DerivationInputFailureCode
from veritrail_review.git_objects import verify_git_object_bytes


def admit_relation_set_for_slice_input_private_closed_proof(
    qualified: OwnedRelationQualificationContinuation,
) -> OwnedAdmittedGraphInputAuthority:
    """Bind exact admission to the still-live qualification attempt."""

    if type(qualified) is not OwnedRelationQualificationContinuation:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
        )
    try:
        admitted = admit_relation_set_for_private_closed_proof(
            qualified.qualification
        )
        _validate_admission_attempt_binding(qualified.qualification, admitted)
        return qualified._bind_admission(
            admitted,
            _validated_attempt_token=_VALIDATED_ADMISSION_ATTEMPT_TOKEN,
        )
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
        ) from exc


def claim_admitted_graph_slice_input(
    inputs: DerivationInputSet,
    authority: OwnedAdmittedGraphInputAuthority,
) -> OwnedAdmittedGraphSliceInput:
    """Claim one exact A-stage input without constructing a domain or Slice."""

    if (
        type(inputs) is not DerivationInputSet
        or type(authority) is not OwnedAdmittedGraphInputAuthority
    ):
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED
        )
    try:
        qualification, admitted, continuation = authority._coordinates()
        _validate_admission_attempt_binding(qualification, admitted)
        if not continuation._bound_to(inputs):
            continuation.revoke()
            raise ValueError
        input_coordinates = (
            inputs.source_snapshot_digest,
            inputs.policy_digest,
            inputs.analysis_scope_digest,
            inputs.slice_policy_digest,
            inputs.derivation_profile_digest,
        )
        qualification_coordinates = (
            qualification.source_snapshot_digest,
            qualification.policy_digest,
            qualification.analysis_scope_digest,
            qualification.slice_policy_digest,
            qualification.derivation_profile_digest,
        )
        if (
            input_coordinates != qualification_coordinates
            or qualification.derivation_id != admitted.derivation_id
            or qualification.source_snapshot_digest
            != admitted.source_snapshot_digest
            or qualification.policy_digest != admitted.policy_digest
            or qualification.analysis_scope_digest
            != admitted.analysis_scope_digest
            or qualification.slice_policy_digest != admitted.slice_policy_digest
            or qualification.derivation_profile_digest
            != admitted.derivation_profile_digest
            or qualification.fact_set_digest != admitted.fact_set_digest
            or qualification.observation_domain_digest
            != admitted.observation_domain_digest
            or qualification.qualification_digest
            != admitted.qualification_digest
            or qualification.candidate_composition_status
            != admitted.candidate_composition_status
        ):
            continuation.revoke()
            raise ValueError
        joined = authority._claim(inputs)
        if not joined.continuation_permitted():
            raise ValueError
        return joined
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED
        ) from exc


def cross_validate_admitted_graph_slice_input(
    joined: OwnedAdmittedGraphSliceInput,
) -> OwnedCrossValidatedAdmittedGraphSliceInput:
    """Reconstruct B-stage exact inputs without rereading paths or minting budget."""

    if type(joined) is not OwnedAdmittedGraphSliceInput:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED
        )
    try:
        joined._claim_cross_validation()
        state = _ContinuationValidationState(joined)
        inputs = joined._owned_inputs()
        if (
            type(inputs) is not DerivationInputSet
            or type(inputs.source_snapshot_canonical_bytes) is not bytes
            or type(inputs.review_policy_canonical_bytes) is not bytes
            or type(inputs.derivation_profile_canonical_bytes) is not bytes
        ):
            raise ValueError

        snapshot = _parse_artifact(
            inputs.source_snapshot_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_SOURCE_SNAPSHOT,
            state,  # type: ignore[arg-type]
        )
        policy = _parse_artifact(
            inputs.review_policy_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY,
            state,  # type: ignore[arg-type]
        )
        profile = _parse_artifact(
            inputs.derivation_profile_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_DERIVATION_PROFILE,
            state,  # type: ignore[arg-type]
        )
        _validate_snapshot(
            snapshot,
            inputs.source_snapshot_canonical_bytes,
            state,  # type: ignore[arg-type]
        )
        _validate_profile(profile, state)  # type: ignore[arg-type]
        _validate_policy(policy, profile, state)  # type: ignore[arg-type]
        _validate_cross_artifact_binding(snapshot, policy, profile, state)  # type: ignore[arg-type]
        if (
            snapshot["source_snapshot_digest"] != inputs.source_snapshot_digest
            or policy["source_snapshot_digest"] != inputs.source_snapshot_digest
            or policy["policy_digest"] != inputs.policy_digest
            or policy["analysis_scope_digest"] != inputs.analysis_scope_digest
            or policy["slice_policy_digest"] != inputs.slice_policy_digest
            or policy["derivation_profile_digest"]
            != inputs.derivation_profile_digest
            or profile["profile_digest"] != inputs.derivation_profile_digest
        ):
            raise ValueError

        qualification = joined._owned_qualification()
        admitted = joined._owned_admission()
        _validate_admission_attempt_binding(qualification, admitted)
        normalized = _validate_qualification(qualification)
        fact_set, fact_set_digest = _fact_set_document(
            inputs, normalized["facts"], ()
        )
        fact_set_bytes = canonical_json_bytes(fact_set)
        if (
            fact_set_digest != joined.fact_set_digest
            or fact_set_digest != qualification.fact_set_digest
            or fact_set_digest != admitted.fact_set_digest
            or fact_set["source_snapshot_digest"] != joined.source_snapshot_digest
            or fact_set["policy_digest"] != joined.policy_digest
            or fact_set["analysis_scope_digest"] != joined.analysis_scope_digest
            or fact_set["derivation_profile_digest"]
            != joined.derivation_profile_digest
        ):
            raise ValueError

        owned_blobs = _validate_verified_blob_snapshot(inputs, snapshot, state)
        state.checkpoint("slice-input-cross-validation-complete")
        result = OwnedCrossValidatedAdmittedGraphSliceInput._create(
            joined=joined,
            fact_set_document_bytes=fact_set_bytes,
            verified_blob_bytes_by_object_identity=owned_blobs,
        )
        _validate_cross_validated_input(result)
        if not result.continuation_permitted():
            raise ValueError
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED
        ) from exc


class _ContinuationValidationState:
    """Duck-typed validator state backed by the original derivation budget."""

    profile = DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE

    def __init__(self, joined: OwnedAdmittedGraphSliceInput) -> None:
        self.__joined = joined

    def checkpoint(self, _stage: str) -> None:
        if not self.__joined.continuation_permitted():
            raise _ReviewSliceInputError(
                _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED
            )


def _validate_verified_blob_snapshot(
    inputs: DerivationInputSet,
    snapshot: Mapping[str, object],
    state: _ContinuationValidationState,
) -> dict[str, bytes]:
    inventory = snapshot["inventory"]
    if not isinstance(inventory, list):
        raise ValueError
    expected: dict[str, tuple[str, int, str]] = {}
    for item in inventory:
        if not isinstance(item, Mapping):
            raise ValueError
        git_object = item["git_object"]
        if not isinstance(git_object, Mapping):
            raise ValueError
        if git_object["object_type"] != "BLOB":
            continue
        content = item.get("content")
        if not isinstance(content, Mapping):
            raise ValueError
        oid = git_object["hex"]
        algorithm = git_object["algorithm"]
        size = content["size_bytes"]
        digest = content["sha256"]
        if (
            not isinstance(oid, str)
            or not isinstance(algorithm, str)
            or type(size) is not int
            or size < 0
            or not isinstance(digest, str)
        ):
            raise ValueError
        identity = (algorithm, size, digest)
        previous = expected.setdefault(oid, identity)
        if previous != identity:
            raise ValueError

    supplied = inputs.verified_blob_bytes_by_object_identity
    if not isinstance(supplied, Mapping) or set(supplied) != set(expected):
        raise ValueError
    owned: dict[str, bytes] = {}
    for oid in sorted(expected):
        state.checkpoint("slice-input-blob-validation")
        value = supplied[oid]
        algorithm, size, digest = expected[oid]
        if (
            type(value) is not bytes
            or len(value) != size
            or sha256_bytes(value) != digest
        ):
            raise ValueError
        verify_git_object_bytes(
            algorithm=algorithm,
            object_type="blob",
            oid=oid,
            declared_size=size,
            body=value,
        )
        owned[oid] = value
    return owned
