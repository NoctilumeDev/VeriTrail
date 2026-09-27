from __future__ import annotations

import hashlib
import io
from threading import Lock
from typing import Mapping

from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    read_frame,
)
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
    _validate_language_support_classification,
)
from veritrail_review._source_operation_projection_values import (
    OwnedSourceOperationProjection,
    _validate_source_operation_projection,
)
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


_GATE_TOKEN = object()
_CLAIM_TOKEN = object()
_CLAIMED_REQUEST_TOKEN = object()
_INPUT_STATE_DOMAIN = "veritrail.review.private-source-operation-gate-input/0.1"


class _SourceOperationGateError(ValueError):
    """One private B-stage live-authority binding failed closed."""


class OwnedSourceOperationAttemptGate:
    """Controller-owned parent gate; no semantic or publication authority."""

    __slots__ = (
        "__bound_classification",
        "__bound_context",
        "__bound_inputs",
        "__bound_parent_eligibility",
        "__children",
        "__classification",
        "__context",
        "__input_state_seal",
        "__inputs",
        "__lock",
        "__parent_eligibility",
    )

    def __init__(
        self,
        *,
        inputs: DerivationInputSet,
        context: BudgetContext,
        parent_eligibility: AttemptEligibility,
        classification: OwnedLanguageSupportClassification,
        _construction_token: object,
    ) -> None:
        if _construction_token is not _GATE_TOKEN:
            raise _SourceOperationGateError(
                "source operation gate is not constructible"
            )
        _validate_parent_binding(
            inputs,
            context,
            parent_eligibility,
            classification,
            require_provisional=True,
        )
        self.__bound_inputs = inputs
        self.__inputs = inputs
        self.__bound_context = context
        self.__context = context
        self.__bound_parent_eligibility = parent_eligibility
        self.__parent_eligibility = parent_eligibility
        self.__bound_classification = classification
        self.__classification = classification
        self.__input_state_seal = _input_state_seal(inputs)
        self.__children: list[OwnedSourceOperationChildClaim] = []
        self.__lock = Lock()

    def bind_child(
        self,
        *,
        projection: OwnedSourceOperationProjection,
        request_frame: bytes,
        transport_limits: ExecutionCellTransportSafetyLimits,
        child_eligibility: AttemptEligibility,
    ) -> "OwnedSourceOperationChildClaim":
        with self.__lock:
            try:
                self.__validate_parent_locked(
                    allowed_states={
                        AttemptEligibilityState.PROVISIONAL,
                        AttemptEligibilityState.ADMITTED,
                    }
                )
                _validate_child_binding(
                    self.__classification,
                    projection,
                    request_frame,
                    transport_limits,
                    child_eligibility,
                )
                if any(
                    item._bound_to_child(child_eligibility)
                    for item in self.__children
                ):
                    raise _SourceOperationGateError(
                        "source operation child eligibility was already bound"
                    )
                claim = OwnedSourceOperationChildClaim(
                    gate=self,
                    projection=projection,
                    request_frame=request_frame,
                    transport_limits=transport_limits,
                    child_eligibility=child_eligibility,
                    _construction_token=_CLAIM_TOKEN,
                )
                self.__children.append(claim)
                return claim
            except Exception as exc:
                if type(child_eligibility) is AttemptEligibility:
                    child_eligibility.revoke()
                self.__fail_closed_locked()
                if isinstance(exc, _SourceOperationGateError):
                    raise
                raise _SourceOperationGateError(
                    "source operation child binding was rejected"
                ) from exc

    def admit_parent(self) -> None:
        with self.__lock:
            try:
                self.__validate_parent_locked(
                    allowed_states={AttemptEligibilityState.PROVISIONAL}
                )
                if not self.__parent_eligibility.admit():
                    raise _SourceOperationGateError(
                        "source operation parent admission was rejected"
                    )
                self.__validate_parent_locked(
                    allowed_states={AttemptEligibilityState.ADMITTED}
                )
            except Exception as exc:
                self.__fail_closed_locked()
                if isinstance(exc, _SourceOperationGateError):
                    raise
                raise _SourceOperationGateError(
                    "source operation parent admission was rejected"
                ) from exc

    def _authorize_claim(
        self, claim: "OwnedSourceOperationChildClaim"
    ) -> None:
        with self.__lock:
            try:
                self.__validate_parent_locked(
                    allowed_states={AttemptEligibilityState.ADMITTED}
                )
                if not any(item is claim for item in self.__children):
                    raise _SourceOperationGateError(
                        "source operation claim is foreign to its parent"
                    )
                claim._validate_bound_state(require_consumed=True)
            except Exception as exc:
                self.__fail_closed_locked()
                if isinstance(exc, _SourceOperationGateError):
                    raise
                raise _SourceOperationGateError(
                    "source operation child claim was rejected"
                ) from exc

    def _authorize_claimed_request(
        self,
        claim: "OwnedSourceOperationChildClaim",
    ) -> None:
        with self.__lock:
            try:
                self.__validate_parent_locked(
                    allowed_states={AttemptEligibilityState.ADMITTED}
                )
                if not any(item is claim for item in self.__children):
                    raise _SourceOperationGateError(
                        "claimed request is foreign to its parent"
                    )
                claim._validate_bound_state(require_consumed=True)
            except Exception as exc:
                self.__fail_closed_locked()
                if isinstance(exc, _SourceOperationGateError):
                    raise
                raise _SourceOperationGateError(
                    "claimed source operation request is no longer live"
                ) from exc

    def _classification_ref(self) -> OwnedLanguageSupportClassification:
        return self.__classification

    def _inputs_ref(self) -> DerivationInputSet:
        return self.__inputs

    def _context_ref(self) -> BudgetContext:
        return self.__context

    def _parent_eligibility_ref(self) -> AttemptEligibility:
        return self.__parent_eligibility

    def __validate_parent_locked(
        self,
        *,
        allowed_states: set[AttemptEligibilityState],
    ) -> None:
        if (
            self.__inputs is not self.__bound_inputs
            or self.__context is not self.__bound_context
            or self.__parent_eligibility is not self.__bound_parent_eligibility
            or self.__classification is not self.__bound_classification
            or _input_state_seal(self.__inputs) != self.__input_state_seal
        ):
            raise _SourceOperationGateError(
                "source operation parent identity changed"
            )
        _validate_parent_binding(
            self.__inputs,
            self.__context,
            self.__parent_eligibility,
            self.__classification,
            require_provisional=False,
        )
        if self.__parent_eligibility.state not in allowed_states:
            raise _SourceOperationGateError(
                "source operation parent is not in the required state"
            )
        if not self.__context.checkpoint():
            raise _SourceOperationGateError(
                "source operation parent budget is no longer live"
            )

    def __fail_closed_locked(self) -> None:
        for parent in (
            self.__bound_parent_eligibility,
            self.__parent_eligibility,
        ):
            if type(parent) is AttemptEligibility:
                parent.revoke()
        for child in self.__children:
            child._revoke_bound_child()


class OwnedSourceOperationChildClaim:
    """One exact child request claim; consumed even when validation fails."""

    __slots__ = (
        "__bound_child_eligibility",
        "__bound_projection",
        "__bound_request_frame",
        "__bound_transport_limits",
        "__child_eligibility",
        "__consumed",
        "__frame_sha256",
        "__gate",
        "__lock",
        "__projection",
        "__request_frame",
        "__transport_limits",
    )

    def __init__(
        self,
        *,
        gate: OwnedSourceOperationAttemptGate,
        projection: OwnedSourceOperationProjection,
        request_frame: bytes,
        transport_limits: ExecutionCellTransportSafetyLimits,
        child_eligibility: AttemptEligibility,
        _construction_token: object,
    ) -> None:
        if _construction_token is not _CLAIM_TOKEN:
            raise _SourceOperationGateError(
                "source operation claim is not constructible"
            )
        self.__gate = gate
        self.__bound_projection = projection
        self.__projection = projection
        self.__bound_request_frame = request_frame
        self.__request_frame = request_frame
        self.__bound_transport_limits = transport_limits
        self.__transport_limits = transport_limits
        self.__bound_child_eligibility = child_eligibility
        self.__child_eligibility = child_eligibility
        self.__frame_sha256 = hashlib.sha256(request_frame).hexdigest()
        self.__lock = Lock()
        self.__consumed = False

    def claim(self) -> "ClaimedSourceOperationRequest":
        with self.__lock:
            if self.__consumed:
                raise _SourceOperationGateError(
                    "source operation child claim was already consumed"
                )
            self.__consumed = True
        try:
            self.__gate._authorize_claim(self)
            return ClaimedSourceOperationRequest(
                claim=self,
                _construction_token=_CLAIMED_REQUEST_TOKEN,
            )
        except Exception:
            self._revoke_bound_child()
            raise

    def _validate_bound_state(self, *, require_consumed: bool) -> None:
        with self.__lock:
            if (
                self.__projection is not self.__bound_projection
                or self.__request_frame is not self.__bound_request_frame
                or self.__transport_limits is not self.__bound_transport_limits
                or self.__child_eligibility is not self.__bound_child_eligibility
                or self.__consumed is not require_consumed
                or hashlib.sha256(self.__request_frame).hexdigest()
                != self.__frame_sha256
            ):
                raise _SourceOperationGateError(
                    "source operation child identity changed"
                )
            _validate_child_binding(
                self.__gate._classification_ref(),
                self.__projection,
                self.__request_frame,
                self.__transport_limits,
                self.__child_eligibility,
            )

    def _revoke_bound_child(self) -> None:
        with self.__lock:
            for child in (
                self.__bound_child_eligibility,
                self.__child_eligibility,
            ):
                if type(child) is AttemptEligibility:
                    child.revoke()

    def _projection_ref(self) -> OwnedSourceOperationProjection:
        return self.__projection

    def _request_frame_ref(self) -> bytes:
        return self.__request_frame

    def _transport_limits_ref(self) -> ExecutionCellTransportSafetyLimits:
        return self.__transport_limits

    def _child_eligibility_ref(self) -> AttemptEligibility:
        return self.__child_eligibility

    def _gate_ref(self) -> OwnedSourceOperationAttemptGate:
        return self.__gate

    def _bound_to_child(self, child: AttemptEligibility) -> bool:
        return child is self.__bound_child_eligibility

    def _authorize_claimed_request(self) -> None:
        self.__gate._authorize_claimed_request(self)


class ClaimedSourceOperationRequest:
    """Opaque claimed child boundary; still subject to parent/context recheck."""

    __slots__ = ("__claim",)

    def __init__(
        self,
        *,
        claim: OwnedSourceOperationChildClaim,
        _construction_token: object,
    ) -> None:
        if _construction_token is not _CLAIMED_REQUEST_TOKEN:
            raise _SourceOperationGateError(
                "claimed source operation request is not constructible"
            )
        self.__claim = claim

    def _owned_projection(self) -> OwnedSourceOperationProjection:
        self.__claim._authorize_claimed_request()
        return self.__claim._projection_ref()

    def _owned_inputs(self) -> DerivationInputSet:
        self.__claim._authorize_claimed_request()
        return self.__claim._gate_ref()._inputs_ref()

    def _owned_classification(self) -> OwnedLanguageSupportClassification:
        self.__claim._authorize_claimed_request()
        return self.__claim._gate_ref()._classification_ref()

    def _context(self) -> BudgetContext:
        self.__claim._authorize_claimed_request()
        return self.__claim._gate_ref()._context_ref()

    def _parent_eligibility(self) -> AttemptEligibility:
        self.__claim._authorize_claimed_request()
        return self.__claim._gate_ref()._parent_eligibility_ref()

    def _request_frame_copy(self) -> bytes:
        self.__claim._authorize_claimed_request()
        return memoryview(self.__claim._request_frame_ref()).tobytes()

    def _transport_limits(
        self,
    ) -> ExecutionCellTransportSafetyLimits:
        self.__claim._authorize_claimed_request()
        return self.__claim._transport_limits_ref()

    def _child_eligibility(self) -> AttemptEligibility:
        self.__claim._authorize_claimed_request()
        return self.__claim._child_eligibility_ref()


def create_source_operation_attempt_gate(
    inputs: DerivationInputSet,
    context: BudgetContext,
    parent_eligibility: AttemptEligibility,
    classification: OwnedLanguageSupportClassification,
) -> OwnedSourceOperationAttemptGate:
    """Mint one private parent gate from live controller-owned identities."""

    return OwnedSourceOperationAttemptGate(
        inputs=inputs,
        context=context,
        parent_eligibility=parent_eligibility,
        classification=classification,
        _construction_token=_GATE_TOKEN,
    )


def _validate_parent_binding(
    inputs: object,
    context: object,
    parent_eligibility: object,
    classification: object,
    *,
    require_provisional: bool,
) -> None:
    if (
        type(inputs) is not DerivationInputSet
        or type(context) is not BudgetContext
        or context.state is not BudgetState.RUNNING
        or type(parent_eligibility) is not AttemptEligibility
        or (
            require_provisional
            and parent_eligibility.state is not AttemptEligibilityState.PROVISIONAL
        )
        or type(classification) is not OwnedLanguageSupportClassification
    ):
        raise _SourceOperationGateError("invalid source operation parent binding")
    try:
        _validate_language_support_classification(classification)
        if (
            classification.source_snapshot_digest != inputs.source_snapshot_digest
            or classification.policy_digest != inputs.policy_digest
            or classification.analysis_scope_digest != inputs.analysis_scope_digest
            or classification.derivation_profile_digest
            != inputs.derivation_profile_digest
        ):
            raise ValueError
    except Exception as exc:
        raise _SourceOperationGateError(
            "Language Support classification is not bound to exact inputs"
        ) from exc


def _validate_child_binding(
    classification: object,
    projection: object,
    request_frame: object,
    transport_limits: object,
    child_eligibility: object,
) -> None:
    if (
        type(classification) is not OwnedLanguageSupportClassification
        or type(projection) is not OwnedSourceOperationProjection
        or type(request_frame) is not bytes
        or type(transport_limits) is not ExecutionCellTransportSafetyLimits
        or type(child_eligibility) is not AttemptEligibility
        or child_eligibility.state is not AttemptEligibilityState.PROVISIONAL
    ):
        raise _SourceOperationGateError("invalid source operation child binding")
    try:
        _validate_language_support_classification(classification)
        _validate_source_operation_projection(projection)
        read_frame(
            io.BytesIO(request_frame),
            payload_limit=transport_limits.request_payload_bytes,
        )
        if (
            projection.source_snapshot_digest
            != classification.source_snapshot_digest
            or projection.policy_digest != classification.policy_digest
            or projection.analysis_scope_digest
            != classification.analysis_scope_digest
            or projection.derivation_profile_digest
            != classification.derivation_profile_digest
            or projection.language_support_function
            != classification.language_support_function
            or projection.classification_digest
            != classification.classification_digest
        ):
            raise ValueError
    except Exception as exc:
        raise _SourceOperationGateError(
            "source operation child continuity was rejected"
        ) from exc


def _input_state_seal(inputs: DerivationInputSet) -> str:
    if type(inputs) is not DerivationInputSet:
        raise _SourceOperationGateError("invalid exact input identity")
    raw_fields = {
        "source_snapshot_canonical_bytes": inputs.source_snapshot_canonical_bytes,
        "review_policy_canonical_bytes": inputs.review_policy_canonical_bytes,
        "derivation_profile_canonical_bytes": (
            inputs.derivation_profile_canonical_bytes
        ),
    }
    if any(type(item) is not bytes for item in raw_fields.values()):
        raise _SourceOperationGateError("invalid exact input bytes")
    blobs = inputs.verified_blob_bytes_by_object_identity
    if not isinstance(blobs, Mapping):
        raise _SourceOperationGateError("invalid exact blob ownership")
    try:
        blob_digests = {
            str(key): hashlib.sha256(value).hexdigest()
            for key, value in sorted(blobs.items())
            if type(key) is str and type(value) is bytes
        }
        if len(blob_digests) != len(blobs):
            raise ValueError
    except Exception as exc:
        raise _SourceOperationGateError("invalid exact blob ownership") from exc
    payload = {
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "policy_digest": inputs.policy_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "slice_policy_digest": inputs.slice_policy_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        **{
            f"{key}_sha256": hashlib.sha256(value).hexdigest()
            for key, value in raw_fields.items()
        },
        "verified_blob_sha256_by_object_identity": blob_digests,
    }
    return semantic_digest(_INPUT_STATE_DOMAIN, payload)
