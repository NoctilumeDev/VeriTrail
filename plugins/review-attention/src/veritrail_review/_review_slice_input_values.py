from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from threading import Lock

from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
)
from veritrail_review._relation_observation_qualification_values import (
    OwnedRelationCompositionQualificationResult,
)
from veritrail_review._relation_set_admission_values import (
    OwnedRelationSetAdmissionState,
)
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.budget import OwnedPhaseResult
from veritrail_review.derivation_input_contracts import DerivationInputSet


class _ReviewSliceInputFailureCode(str, Enum):
    CONTINUATION_UNAVAILABLE = "CONTINUATION_UNAVAILABLE"
    ADMISSION_BINDING_REJECTED = "ADMISSION_BINDING_REJECTED"
    INPUT_JOIN_REJECTED = "INPUT_JOIN_REJECTED"
    INPUT_CROSS_VALIDATION_REJECTED = "INPUT_CROSS_VALIDATION_REJECTED"
    OBLIGATION_DOMAIN_REJECTED = "OBLIGATION_DOMAIN_REJECTED"
    OBLIGATION_ASSIGNMENT_REJECTED = "OBLIGATION_ASSIGNMENT_REJECTED"
    TRAVERSAL_BOUNDARY_REJECTED = "TRAVERSAL_BOUNDARY_REJECTED"
    TRAVERSAL_OUTCOME_REJECTED = "TRAVERSAL_OUTCOME_REJECTED"
    OBLIGATION_RECONCILIATION_REJECTED = (
        "OBLIGATION_RECONCILIATION_REJECTED"
    )
    OBLIGATION_ACCOUNTING_REJECTED = "OBLIGATION_ACCOUNTING_REJECTED"


_FAILURE_MESSAGES = {
    _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE: (
        "the same-attempt Slice continuation is unavailable"
    ),
    _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED: (
        "the admitted Relation graph cannot bind the live qualification attempt"
    ),
    _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED: (
        "the exact admitted-graph Slice input join is not eligible"
    ),
    _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED: (
        "the exact admitted-graph Slice input history cannot be reconstructed"
    ),
    _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED: (
        "the admitted graph cannot establish one exact Slice obligation domain"
    ),
    _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED: (
        "the exact Slice obligation domain cannot establish private assignments"
    ),
    _ReviewSliceInputFailureCode.TRAVERSAL_BOUNDARY_REJECTED: (
        "the next private Slice obligation cannot enter its traversal boundary"
    ),
    _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED: (
        "the private Slice traversal cannot form one terminal normal outcome"
    ),
    _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED: (
        "the private Slice obligation outcomes cannot form one normal closure"
    ),
    _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED: (
        "the private Slice input cannot form one exact terminal accounting result"
    ),
}


class _ReviewSliceInputError(RuntimeError):
    """Private, path-free failure for the admitted-graph input boundary."""

    def __init__(self, code: _ReviewSliceInputFailureCode) -> None:
        self.code = code
        self.safe_message = _FAILURE_MESSAGES[code]
        super().__init__(f"{code.value}: {self.safe_message}")


_CONTINUATION_TOKEN = object()
_QUALIFICATION_BINDING_TOKEN = object()
_ADMISSION_BINDING_TOKEN = object()
_VALIDATED_ADMISSION_ATTEMPT_TOKEN = object()
_CLAIMED_CONTINUATION_TOKEN = object()


class _SameAttemptSliceContinuation:
    """Opaque, one-shot capability over the original live derivation attempt."""

    __slots__ = (
        "__attempt_eligibility",
        "__bound_context",
        "__bound_inputs",
        "__consumed",
        "__context",
        "__lock",
        "__revoked",
    )

    def __init__(
        self,
        *,
        inputs: DerivationInputSet,
        context: BudgetContext,
        attempt_eligibility: AttemptEligibility,
        _construction_token: object,
    ) -> None:
        if (
            _construction_token is not _CONTINUATION_TOKEN
            or type(inputs) is not DerivationInputSet
            or type(context) is not BudgetContext
            or type(attempt_eligibility) is not AttemptEligibility
        ):
            raise _ReviewSliceInputError(
                _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE
            )
        self.__bound_inputs = inputs
        self.__bound_context = context
        self.__context = context
        self.__attempt_eligibility = attempt_eligibility
        self.__lock = Lock()
        self.__consumed = False
        self.__revoked = False

    def available(self) -> bool:
        with self.__lock:
            return self.__available_locked()

    def claim(self, inputs: DerivationInputSet) -> "_ClaimedSliceContinuation":
        with self.__lock:
            if inputs is not self.__bound_inputs or not self.__available_locked():
                self.__revoked = True
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED
                )
            self.__consumed = True
            return _ClaimedSliceContinuation(
                context=self.__context,
                attempt_eligibility=self.__attempt_eligibility,
                _construction_token=_CLAIMED_CONTINUATION_TOKEN,
            )

    def revoke(self) -> None:
        with self.__lock:
            self.__revoked = True

    def _bound_to(self, inputs: DerivationInputSet) -> bool:
        return inputs is self.__bound_inputs

    def __available_locked(self) -> bool:
        if (
            self.__consumed
            or self.__revoked
            or self.__context is not self.__bound_context
        ):
            self.__revoked = True
            return False
        if self.__attempt_eligibility.state is not AttemptEligibilityState.ADMITTED:
            self.__revoked = True
            return False
        if not self.__context.checkpoint():
            self.__revoked = True
            return False
        available = (
            self.__context.state is BudgetState.RUNNING
            and self.__context.stop_trigger is None
        )
        if not available:
            self.__revoked = True
        return available


class _ClaimedSliceContinuation:
    """Claimed capability retained by one private admitted-graph input."""

    __slots__ = (
        "__attempt_eligibility",
        "__bound_context",
        "__context",
        "__cross_validation_claimed",
        "__obligation_domain_claimed",
        "__traversal_assignments_claimed",
        "__normal_reconciliation_claimed",
        "__closed_empty_reconciliation_claimed",
        "__blocked_input_receipt_claimed",
        "__lock",
    )

    def __init__(
        self,
        *,
        context: BudgetContext,
        attempt_eligibility: AttemptEligibility,
        _construction_token: object,
    ) -> None:
        if _construction_token is not _CLAIMED_CONTINUATION_TOKEN:
            raise _ReviewSliceInputError(
                _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE
            )
        self.__bound_context = context
        self.__context = context
        self.__attempt_eligibility = attempt_eligibility
        self.__lock = Lock()
        self.__cross_validation_claimed = False
        self.__obligation_domain_claimed = False
        self.__traversal_assignments_claimed = False
        self.__normal_reconciliation_claimed = False
        self.__closed_empty_reconciliation_claimed = False
        self.__blocked_input_receipt_claimed = False

    def permits_continuation(self) -> bool:
        with self.__lock:
            return self.__permits_continuation_locked()

    def claim_cross_validation(self) -> None:
        with self.__lock:
            if (
                self.__cross_validation_claimed
                or not self.__permits_continuation_locked()
            ):
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED
                )
            self.__cross_validation_claimed = True

    def claim_obligation_domain(self) -> None:
        with self.__lock:
            if (
                not self.__cross_validation_claimed
                or self.__obligation_domain_claimed
                or not self.__permits_continuation_locked()
            ):
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED
                )
            self.__obligation_domain_claimed = True

    def claim_traversal_assignments(self) -> None:
        with self.__lock:
            if (
                not self.__obligation_domain_claimed
                or self.__traversal_assignments_claimed
                or not self.__permits_continuation_locked()
            ):
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED
                )
            self.__traversal_assignments_claimed = True

    def try_complete_traversal_outcome(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        """Commit one private traversal result against the original live budget."""

        with self.__lock:
            if not self.__permits_continuation_locked():
                return None
            phase = self.__context.try_complete_phase(
                canonical_bytes, resources_closed=True
            )
            if phase is None:
                if self.__context.state is BudgetState.STOPPING:
                    self.__context._mark_release(residue_free=True)
                return None
            if (
                self.__attempt_eligibility.state
                is not AttemptEligibilityState.ADMITTED
            ):
                return None
            return phase

    def claim_normal_reconciliation(self) -> None:
        with self.__lock:
            if (
                not self.__traversal_assignments_claimed
                or self.__normal_reconciliation_claimed
                or self.__closed_empty_reconciliation_claimed
                or self.__blocked_input_receipt_claimed
                or not self.__permits_continuation_locked()
            ):
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED
                )
            self.__normal_reconciliation_claimed = True

    def claim_closed_empty_reconciliation(self) -> None:
        with self.__lock:
            if (
                not self.__traversal_assignments_claimed
                or self.__normal_reconciliation_claimed
                or self.__closed_empty_reconciliation_claimed
                or self.__blocked_input_receipt_claimed
                or not self.__permits_continuation_locked()
            ):
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED
                )
            self.__closed_empty_reconciliation_claimed = True

    def claim_blocked_input_receipt(self) -> None:
        with self.__lock:
            if (
                not self.__obligation_domain_claimed
                or self.__traversal_assignments_claimed
                or self.__normal_reconciliation_claimed
                or self.__closed_empty_reconciliation_claimed
                or self.__blocked_input_receipt_claimed
                or not self.__permits_continuation_locked()
            ):
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED
                )
            self.__blocked_input_receipt_claimed = True

    def try_complete_obligation_closure(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        """Commit one private closure against the original live budget."""

        with self.__lock:
            if not self.__normal_reconciliation_claimed:
                return None
            if not self.__permits_continuation_locked():
                return None
            phase = self.__context.try_complete_phase(
                canonical_bytes, resources_closed=True
            )
            if phase is None:
                if self.__context.state is BudgetState.STOPPING:
                    self.__context._mark_release(residue_free=True)
                return None
            if (
                self.__attempt_eligibility.state
                is not AttemptEligibilityState.ADMITTED
            ):
                return None
            return phase

    def try_complete_closed_empty_obligation_closure(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        """Commit one exact empty-domain closure against the live budget."""

        with self.__lock:
            if not self.__closed_empty_reconciliation_claimed:
                return None
            return self.__try_complete_private_phase_locked(canonical_bytes)

    def try_complete_blocked_input_receipt(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        """Commit one conflict-blocked receipt against the live budget."""

        with self.__lock:
            if not self.__blocked_input_receipt_claimed:
                return None
            return self.__try_complete_private_phase_locked(canonical_bytes)

    def __try_complete_private_phase_locked(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        if not self.__permits_continuation_locked():
            return None
        phase = self.__context.try_complete_phase(
            canonical_bytes, resources_closed=True
        )
        if phase is None:
            if self.__context.state is BudgetState.STOPPING:
                self.__context._mark_release(residue_free=True)
            return None
        if (
            self.__attempt_eligibility.state
            is not AttemptEligibilityState.ADMITTED
        ):
            return None
        return phase

    def __permits_continuation_locked(self) -> bool:
        return (
            self.__context is self.__bound_context
            and self.__attempt_eligibility.state
            is AttemptEligibilityState.ADMITTED
            and self.__context.checkpoint()
            and self.__context.state is BudgetState.RUNNING
            and self.__context.stop_trigger is None
        )


class OwnedRelationQualificationContinuation:
    """Exact qualification history plus its unclaimed live continuation."""

    __slots__ = ("__admission_bound", "__continuation", "__lock", "__qualification")

    def __init__(
        self,
        *,
        qualification: OwnedRelationCompositionQualificationResult,
        continuation: _SameAttemptSliceContinuation,
        _construction_token: object,
    ) -> None:
        if (
            _construction_token is not _QUALIFICATION_BINDING_TOKEN
            or type(qualification) is not OwnedRelationCompositionQualificationResult
            or type(continuation) is not _SameAttemptSliceContinuation
        ):
            raise _ReviewSliceInputError(
                _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE
            )
        self.__qualification = qualification
        self.__continuation = continuation
        self.__lock = Lock()
        self.__admission_bound = False

    @property
    def qualification(self) -> OwnedRelationCompositionQualificationResult:
        return self.__qualification

    def continuation_available(self) -> bool:
        return self.__continuation.available()

    def _bind_admission(
        self,
        admitted: OwnedRelationSetAdmissionState,
        *,
        _validated_attempt_token: object | None = None,
    ) -> "OwnedAdmittedGraphInputAuthority":
        with self.__lock:
            if self.__admission_bound:
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
                )
            if _validated_attempt_token is not _VALIDATED_ADMISSION_ATTEMPT_TOKEN:
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
                )
            if not self.__continuation.available():
                self.__continuation.revoke()
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
                )
            self.__admission_bound = True
            return OwnedAdmittedGraphInputAuthority(
                qualification=self.__qualification,
                admitted=admitted,
                continuation=self.__continuation,
                _construction_token=_ADMISSION_BINDING_TOKEN,
            )


class OwnedAdmittedGraphInputAuthority:
    """One private admission/qualification/continuation binding."""

    __slots__ = (
        "__admitted",
        "__claimed",
        "__continuation",
        "__lock",
        "__qualification",
    )

    def __init__(
        self,
        *,
        qualification: OwnedRelationCompositionQualificationResult,
        admitted: OwnedRelationSetAdmissionState,
        continuation: _SameAttemptSliceContinuation,
        _construction_token: object,
    ) -> None:
        if (
            _construction_token is not _ADMISSION_BINDING_TOKEN
            or type(qualification) is not OwnedRelationCompositionQualificationResult
            or type(admitted) is not OwnedRelationSetAdmissionState
            or type(continuation) is not _SameAttemptSliceContinuation
        ):
            raise _ReviewSliceInputError(
                _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
            )
        self.__qualification = qualification
        self.__admitted = admitted
        self.__continuation = continuation
        self.__lock = Lock()
        self.__claimed = False

    def continuation_available(self) -> bool:
        with self.__lock:
            return not self.__claimed and self.__continuation.available()

    def _claim(self, inputs: DerivationInputSet) -> "OwnedAdmittedGraphSliceInput":
        with self.__lock:
            if self.__claimed:
                raise _ReviewSliceInputError(
                    _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED
                )
            self.__claimed = True
            claimed = self.__continuation.claim(inputs)
            return OwnedAdmittedGraphSliceInput(
                derivation_id=self.__qualification.derivation_id,
                source_snapshot_digest=self.__qualification.source_snapshot_digest,
                policy_digest=self.__qualification.policy_digest,
                analysis_scope_digest=self.__qualification.analysis_scope_digest,
                slice_policy_digest=self.__qualification.slice_policy_digest,
                derivation_profile_digest=(
                    self.__qualification.derivation_profile_digest
                ),
                fact_set_digest=self.__qualification.fact_set_digest,
                observation_domain_digest=(
                    self.__qualification.observation_domain_digest
                ),
                qualification_digest=self.__qualification.qualification_digest,
                relation_set_digest=self.__admitted.relation_set_digest,
                admission_witness_digest=self.__admitted.admission_witness_digest,
                _inputs=inputs,
                _qualification=self.__qualification,
                _admitted=self.__admitted,
                _continuation=claimed,
            )

    def _coordinates(
        self,
    ) -> tuple[
        OwnedRelationCompositionQualificationResult,
        OwnedRelationSetAdmissionState,
        _SameAttemptSliceContinuation,
    ]:
        return self.__qualification, self.__admitted, self.__continuation


@dataclass(frozen=True)
class OwnedAdmittedGraphSliceInput:
    """Private A-stage join; no domain, Slice, Coverage, or publication authority."""

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
    _inputs: DerivationInputSet = field(repr=False, compare=False)
    _qualification: OwnedRelationCompositionQualificationResult = field(
        repr=False, compare=False
    )
    _admitted: OwnedRelationSetAdmissionState = field(repr=False, compare=False)
    _continuation: _ClaimedSliceContinuation = field(repr=False, compare=False)

    def continuation_permitted(self) -> bool:
        return self._continuation.permits_continuation()

    def _owned_inputs(self) -> DerivationInputSet:
        return self._inputs

    def _owned_qualification(self) -> OwnedRelationCompositionQualificationResult:
        return self._qualification

    def _owned_admission(self) -> OwnedRelationSetAdmissionState:
        return self._admitted

    def _claim_cross_validation(self) -> None:
        self._continuation.claim_cross_validation()

    def _claim_obligation_domain(self) -> None:
        self._continuation.claim_obligation_domain()

    def _claim_traversal_assignments(self) -> None:
        self._continuation.claim_traversal_assignments()

    def _try_complete_traversal_outcome(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        return self._continuation.try_complete_traversal_outcome(canonical_bytes)

    def _claim_normal_reconciliation(self) -> None:
        self._continuation.claim_normal_reconciliation()

    def _try_complete_obligation_closure(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        return self._continuation.try_complete_obligation_closure(canonical_bytes)

    def _claim_closed_empty_reconciliation(self) -> None:
        self._continuation.claim_closed_empty_reconciliation()

    def _try_complete_closed_empty_obligation_closure(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        return self._continuation.try_complete_closed_empty_obligation_closure(
            canonical_bytes
        )

    def _claim_blocked_input_receipt(self) -> None:
        self._continuation.claim_blocked_input_receipt()

    def _try_complete_blocked_input_receipt(
        self, canonical_bytes: bytes
    ) -> OwnedPhaseResult | None:
        return self._continuation.try_complete_blocked_input_receipt(canonical_bytes)


def _bind_qualification_continuation(
    qualification: OwnedRelationCompositionQualificationResult,
    *,
    inputs: DerivationInputSet,
    context: BudgetContext,
    attempt_eligibility: AttemptEligibility,
) -> OwnedRelationQualificationContinuation:
    if (
        type(qualification) is not OwnedRelationCompositionQualificationResult
        or qualification.qualification_status != "QUALIFIED"
    ):
        attempt_eligibility.revoke()
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE
        )
    continuation = _SameAttemptSliceContinuation(
        inputs=inputs,
        context=context,
        attempt_eligibility=attempt_eligibility,
        _construction_token=_CONTINUATION_TOKEN,
    )
    if not continuation.available():
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.CONTINUATION_UNAVAILABLE
        )
    return OwnedRelationQualificationContinuation(
        qualification=qualification,
        continuation=continuation,
        _construction_token=_QUALIFICATION_BINDING_TOKEN,
    )
