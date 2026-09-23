from __future__ import annotations

from veritrail_review._relation_set_admission import (
    _validate_admission_attempt_binding,
    admit_relation_set_for_private_closed_proof,
)
from veritrail_review._review_slice_input_values import (
    OwnedAdmittedGraphInputAuthority,
    OwnedAdmittedGraphSliceInput,
    OwnedRelationQualificationContinuation,
    _ReviewSliceInputError,
    _ReviewSliceInputFailureCode,
    _VALIDATED_ADMISSION_ATTEMPT_TOKEN,
)
from veritrail_review.derivation_input_contracts import DerivationInputSet


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
