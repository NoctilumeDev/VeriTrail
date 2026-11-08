"""Private application admission for the two frozen Review/Coverage routes.

The owner binds an exact selector claim before downstream execution and later
admits only the exact nominal result from that same live object graph.  Nothing
in this module is exported by :mod:`veritrail_review`.
"""

from __future__ import annotations

import hashlib
import json
import threading
from enum import Enum
from typing import Mapping

from veritrail_review import _fact_to_coverage_exact_input_handoff as handoff
from veritrail_review import _negative_world_coverage_authority_recovery as negative
from veritrail_review import _post_terminal_fact_dual_successor as selector
from veritrail_review import _relation_transition_slice_composition as positive
from veritrail_review._fact_fulfillment import OwnedProductFactClosure
from veritrail_review._review_coverage_ledger_conformance import (
    CoverageLedgerConformanceSource,
    validate_review_coverage_ledger,
)
from veritrail_review.budget import BudgetContext, BudgetState, OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


ADMISSION_FUNCTION = (
    "r1-application-level-unified-review-coverage-output-admission/0.1"
)
ADMISSION_DOMAIN = "APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_0_1"
ROUTE_RESULT_BINDING_FUNCTION = (
    "r1-application-level-review-coverage-route-result-binding/0.1"
)
RECONCILIATION_FUNCTION = (
    "r1-application-level-review-coverage-output-reconciliation/0.1"
)
PROOF_IS_NOT_PROBLEM_SOLVING = True
QUALIFICATION_INHERITANCE_ALLOWED = False

NORMAL_ROUTE = "RELATION_HANDOFF"
NEGATIVE_ROUTE = "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"
NORMAL_RESULT_KIND = "NORMAL_REVIEW_SLICE_COVERAGE"
NEGATIVE_RESULT_KIND = "NEGATIVE_WORLD_COVERAGE"

_NEGATIVE_BRANCHES = frozenset(
    {
        "ZERO_PARSE_DENOMINATOR",
        "ALL_PARSE_REJECTED",
        "PROJECTION_BLOCKED",
        "REQUIRED_PROVIDER_NON_SUCCESS",
    }
)
_INPUT_DIGEST_FIELDS = (
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
)
_ADMITTED_TOKEN = object()


class UnifiedOutputAdmissionState(str, Enum):
    ROUTE_BOUND_NOT_ADMITTED = "ROUTE_BOUND_NOT_ADMITTED"
    ADMITTED_NORMAL = "ADMITTED_NORMAL"
    ADMITTED_NEGATIVE = "ADMITTED_NEGATIVE"
    REVOKED = "REVOKED"


class UnifiedOutputAdmissionFailureFamily(str, Enum):
    UNIFIED_OUTPUT_INPUT_REJECTED = "UNIFIED_OUTPUT_INPUT_REJECTED"
    UNIFIED_OUTPUT_ROUTE_REJECTED = "UNIFIED_OUTPUT_ROUTE_REJECTED"
    UNIFIED_OUTPUT_RESULT_TYPE_REJECTED = "UNIFIED_OUTPUT_RESULT_TYPE_REJECTED"
    UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED = (
        "UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED"
    )
    UNIFIED_OUTPUT_RESULT_BINDING_REJECTED = (
        "UNIFIED_OUTPUT_RESULT_BINDING_REJECTED"
    )
    UNIFIED_OUTPUT_LEDGER_RECONCILIATION_REJECTED = (
        "UNIFIED_OUTPUT_LEDGER_RECONCILIATION_REJECTED"
    )
    UNIFIED_OUTPUT_ALREADY_ADMITTED = "UNIFIED_OUTPUT_ALREADY_ADMITTED"
    UNIFIED_OUTPUT_CONTEXT_REVOKED = "UNIFIED_OUTPUT_CONTEXT_REVOKED"
    UNIFIED_OUTPUT_AUTHORITY_CEILING_REJECTED = (
        "UNIFIED_OUTPUT_AUTHORITY_CEILING_REJECTED"
    )


class UnifiedOutputAdmissionError(ValueError):
    """Typed private failure; it is not a Core Verdict or product reason."""

    def __init__(self, family: UnifiedOutputAdmissionFailureFamily) -> None:
        self.failure_family = family
        super().__init__(family.value)


class _ValidationFailure(ValueError):
    def __init__(self, family: UnifiedOutputAdmissionFailureFamily) -> None:
        self.family = family
        super().__init__(family.value)


def _route_for_terminal_branch(branch: object) -> str:
    """Independent five-branch projection owned by the application boundary."""

    if branch == "NORMAL_FULFILLED":
        return NORMAL_ROUTE
    if branch in _NEGATIVE_BRANCHES:
        return NEGATIVE_ROUTE
    raise _ValidationFailure(
        UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_ROUTE_REJECTED
    )


def _input_identity(source: Mapping[str, object]) -> dict[str, object]:
    value = source.get("input_identity")
    if type(value) is not dict:
        raise _ValidationFailure(
            UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED
        )
    attempt_id = value.get("fact_consumer_attempt_id")
    if type(attempt_id) is not str or not attempt_id:
        raise _ValidationFailure(
            UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED
        )
    digests = {name: value.get(name) for name in _INPUT_DIGEST_FIELDS}
    if any(type(item) is not str or not item for item in digests.values()):
        raise _ValidationFailure(
            UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED
        )
    return {"fact_consumer_attempt_id": attempt_id, **digests}


def _context_is_live(context: BudgetContext, budget_identity: tuple[object, ...]) -> bool:
    return (
        type(context) is BudgetContext
        and (
            context.limits,
            context.started_at_monotonic,
            context.execution_deadline_monotonic,
        )
        == budget_identity
        and context.state is BudgetState.RUNNING
        and context.stop_trigger is None
        and context.checkpoint()
    )


class BoundUnifiedReviewCoverageOutputAdmission:
    """One application attempt bound to one exact selector route claim."""

    def __init__(self, route_claim: object) -> None:
        self.__lock = threading.RLock()
        self.__state = UnifiedOutputAdmissionState.ROUTE_BOUND_NOT_ADMITTED
        self.__submission_attempted = False
        self.__result: object | None = None
        self.__result_kind: str | None = None
        self.__phase: OwnedPhaseResult | None = None
        self.__admission_bytes: bytes | None = None
        self.__admitted: AdmittedUnifiedReviewCoverageOutput | None = None
        self.__route_claim = route_claim
        self.__bound_route_claim = route_claim
        self.__selector: object | None = None
        self.__closure: OwnedProductFactClosure | None = None
        self.__fact_attempt: object | None = None
        self.__eligibility: object | None = None
        self.__aux_refs: tuple[object, ...] = ()
        try:
            self.__bind(route_claim)
        except _ValidationFailure as exc:
            self.__state = UnifiedOutputAdmissionState.REVOKED
            self.__revoke_route_claim()
            raise UnifiedOutputAdmissionError(exc.family) from exc
        except Exception as exc:
            self.__state = UnifiedOutputAdmissionState.REVOKED
            self.__revoke_route_claim()
            raise UnifiedOutputAdmissionError(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED
            ) from exc

    @property
    def state(self) -> UnifiedOutputAdmissionState:
        return self.__state

    def __copy__(self):
        self.__fail(
            UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()

    def __reduce__(self):
        self.__fail(
            UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
        )

    def __reduce_ex__(self, _protocol):
        return self.__reduce__()

    def __bind(self, route_claim: object) -> None:
        if type(route_claim) is selector.ClaimedPostTerminalRelationSource:
            values = route_claim._bind_application_output_admission()
            (
                exact_claim,
                exact_selector,
                claim_id,
                source,
                context,
                inputs,
                classification,
                limits,
                cancellation,
                closure,
                fact_attempt,
                eligibility,
            ) = values
            route = NORMAL_ROUTE
            self.__selector = exact_selector
            self.__closure = closure
            self.__fact_attempt = fact_attempt
            self.__eligibility = eligibility
            self.__aux_refs = (
                classification,
                limits,
                cancellation,
                closure,
                fact_attempt,
                eligibility,
            )
        elif type(route_claim) is handoff.ClaimedFactToCoverageExactInputHandoff:
            values = route_claim._bind_application_output_admission()
            (
                exact_claim,
                claim_id,
                source,
                inputs,
                context,
                closure,
                exact_selector,
                fact_attempt,
                eligibility,
            ) = values
            route = NEGATIVE_ROUTE
            if type(closure) is not OwnedProductFactClosure:
                raise _ValidationFailure(
                    UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED
                )
            self.__closure = closure
            self.__selector = exact_selector
            self.__fact_attempt = fact_attempt
            self.__eligibility = eligibility
            self.__aux_refs = (
                closure,
                exact_selector,
                fact_attempt,
                eligibility,
            )
        else:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED
            )
        if (
            exact_claim is not route_claim
            or type(claim_id) is not str
            or not claim_id
            or type(source) is not dict
            or type(inputs) is not DerivationInputSet
            or type(context) is not BudgetContext
            or _route_for_terminal_branch(source.get("branch")) != route
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_ROUTE_REJECTED
            )
        self.__selector_route = route
        self.__terminal_branch = source["branch"]
        self.__claim_id = claim_id
        self.__source_bytes = canonical_json_bytes(source)
        self.__inputs = inputs
        self.__context = context
        self.__input_identity = _input_identity(source)
        self.__budget_identity = (
            context.limits,
            context.started_at_monotonic,
            context.execution_deadline_monotonic,
        )
        if not _context_is_live(context, self.__budget_identity):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_CONTEXT_REVOKED
            )

    def __route_coordinates(self) -> tuple[object, ...]:
        if self.__route_claim is not self.__bound_route_claim:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
            )
        if not _context_is_live(self.__context, self.__budget_identity):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_CONTEXT_REVOKED
            )
        try:
            values = self.__route_claim._application_output_admission_coordinates()
        except Exception as exc:
            if not _context_is_live(self.__context, self.__budget_identity):
                family = (
                    UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_CONTEXT_REVOKED
                )
            else:
                family = (
                    UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
                )
            raise _ValidationFailure(family) from exc
        if self.__selector_route == NORMAL_ROUTE:
            exact_claim, exact_selector, claim_id, source, context, inputs, *aux = values
            if (
                exact_selector is not self.__selector
                or len(aux) != len(self.__aux_refs)
                or any(left is not right for left, right in zip(aux, self.__aux_refs))
            ):
                raise _ValidationFailure(
                    UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
                )
        else:
            (
                exact_claim,
                claim_id,
                source,
                inputs,
                context,
                closure,
                exact_selector,
                fact_attempt,
                eligibility,
            ) = values
            if (
                closure is not self.__closure
                or exact_selector is not self.__selector
                or fact_attempt is not self.__fact_attempt
                or eligibility is not self.__eligibility
                or any(
                    left is not right
                    for left, right in zip(
                        (closure, exact_selector, fact_attempt, eligibility),
                        self.__aux_refs,
                    )
                )
            ):
                raise _ValidationFailure(
                    UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
                )
        if (
            exact_claim is not self.__route_claim
            or claim_id != self.__claim_id
            or canonical_json_bytes(source) != self.__source_bytes
            or inputs is not self.__inputs
            or context is not self.__context
            or _route_for_terminal_branch(source.get("branch"))
            != self.__selector_route
            or _input_identity(source) != self.__input_identity
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
            )
        if not _context_is_live(self.__context, self.__budget_identity):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_CONTEXT_REVOKED
            )
        return values

    def __revoke_route_claim(self) -> None:
        try:
            self.__route_claim._revoke_from_application_output_admission()
        except Exception:
            pass

    @staticmethod
    def __revoke_result(result: object) -> None:
        if type(result) in {
            positive.OwnedReviewSliceCoverageComposition,
            negative.AdmittedNegativeWorldCoverage,
        }:
            try:
                result._revoke_from_application_output_admission()
            except Exception:
                pass

    def __fail(
        self,
        family: UnifiedOutputAdmissionFailureFamily,
        *,
        result: object | None = None,
    ) -> None:
        self.__state = UnifiedOutputAdmissionState.REVOKED
        self.__revoke_route_claim()
        self.__revoke_result(self.__result if result is None else result)
        raise UnifiedOutputAdmissionError(family)

    def submit(self, result: object) -> "AdmittedUnifiedReviewCoverageOutput":
        """Consume the only application admission opportunity."""

        with self.__lock:
            if (
                self.__submission_attempted
                or self.__state
                is not UnifiedOutputAdmissionState.ROUTE_BOUND_NOT_ADMITTED
            ):
                self.__fail(
                    UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_ALREADY_ADMITTED,
                    result=result,
                )
            self.__submission_attempted = True
            try:
                self.__route_coordinates()
                if self.__selector_route == NORMAL_ROUTE:
                    result_kind, ledger, result_identity = self.__validate_normal(
                        result
                    )
                    admitted_state = UnifiedOutputAdmissionState.ADMITTED_NORMAL
                else:
                    result_kind, ledger, result_identity = self.__validate_negative(
                        result
                    )
                    admitted_state = UnifiedOutputAdmissionState.ADMITTED_NEGATIVE
                document = self.__admission_document(
                    result_kind=result_kind,
                    ledger=ledger,
                    result_identity=result_identity,
                )
                encoded = canonical_json_bytes(document)
                phase = self.__context.try_complete_phase(
                    encoded, resources_closed=True
                )
                if phase is None or phase.canonical_bytes != encoded:
                    raise _ValidationFailure(
                        UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_CONTEXT_REVOKED
                    )
                admitted = AdmittedUnifiedReviewCoverageOutput(
                    owner=self,
                    result=result,
                    result_kind=result_kind,
                    phase=phase,
                    admission_bytes=encoded,
                    _token=_ADMITTED_TOKEN,
                )
                self.__result = result
                self.__result_kind = result_kind
                self.__phase = phase
                self.__admission_bytes = encoded
                self.__admitted = admitted
                self.__state = admitted_state
                self._validate_admitted(admitted)
                return admitted
            except _ValidationFailure as exc:
                self.__fail(exc.family, result=result)
            except UnifiedOutputAdmissionError:
                raise
            except Exception as exc:
                try:
                    self.__fail(
                        UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED,
                        result=result,
                    )
                except UnifiedOutputAdmissionError as error:
                    raise error from exc
        raise AssertionError("unreachable")

    def __validate_normal(
        self, result: object
    ) -> tuple[str, dict[str, object], str]:
        if type(result) is not positive.OwnedReviewSliceCoverageComposition:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_TYPE_REJECTED
            )
        (
            exact_result,
            inputs,
            context,
            _eligibility,
            conformance_source,
            phase,
            document,
        ) = result._application_output_admission_coordinates()
        if (
            exact_result is not result
            or inputs is not self.__inputs
            or context is not self.__context
            or type(conformance_source) is not CoverageLedgerConformanceSource
            or type(phase) is not OwnedPhaseResult
            or type(document) is not dict
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
            )
        request = document.get("bridge_admission", {}).get("request", {})
        if (
            request.get("handoff_claim_id") != self.__claim_id
            or request.get("fact_consumer_attempt_id")
            != self.__input_identity["fact_consumer_attempt_id"]
            or request.get("input_identity")
            != {
                name: self.__input_identity[name]
                for name in _INPUT_DIGEST_FIELDS
            }
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
            )
        ceiling = document.get("authority_ceiling")
        if (
            type(ceiling) is not dict
            or ceiling.get("private_coverage_validation") is not True
            or any(
                ceiling.get(name) is not False
                for name in ("manifest", "persistence", "public_review")
            )
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_AUTHORITY_CEILING_REJECTED
            )
        ledger = document.get("coverage_ledger")
        if type(ledger) is not dict:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_LEDGER_RECONCILIATION_REJECTED
            )
        try:
            validate_review_coverage_ledger(ledger, conformance_source)
        except Exception as exc:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_LEDGER_RECONCILIATION_REJECTED
            ) from exc
        identity = document.get("composition_digest")
        if type(identity) is not str or not identity:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
            )
        return NORMAL_RESULT_KIND, ledger, identity

    def __validate_negative(
        self, result: object
    ) -> tuple[str, dict[str, object], str]:
        if type(result) is not negative.AdmittedNegativeWorldCoverage:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_TYPE_REJECTED
            )
        values = result._application_output_admission_coordinates()
        (
            exact_result,
            attempt,
            validation,
            phase,
            candidate_bytes,
            conformance_source,
            exact_attempt,
            carrier,
            claim_id,
            source,
            inputs,
            context,
            closure,
        ) = values
        if (
            exact_result is not result
            or attempt is not exact_attempt
            or type(attempt) is not negative.ClaimedNegativeWorldCoverageAttempt
            or type(validation) is not negative.NegativeWorldCoverageValidation
            or type(phase) is not OwnedPhaseResult
            or type(candidate_bytes) is not bytes
            or type(conformance_source) is not CoverageLedgerConformanceSource
            or carrier is not self.__route_claim
            or claim_id != self.__claim_id
            or canonical_json_bytes(source) != self.__source_bytes
            or inputs is not self.__inputs
            or context is not self.__context
            or closure is not self.__closure
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
            )
        document = json.loads(candidate_bytes)
        validation_document = validation.document_copy()
        if (
            validation_document.get("carrier_claim_id") != self.__claim_id
            or validation_document.get("candidate_digest")
            != document.get("coverage_ledger_digest")
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
            )
        try:
            validate_review_coverage_ledger(document, conformance_source)
        except Exception as exc:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_LEDGER_RECONCILIATION_REJECTED
            ) from exc
        ceiling = result.authority_ceiling_copy()
        if (
            ceiling.get("private_negative_world_coverage_ledger") is not True
            or any(
                ceiling.get(name) is not False
                for name in (
                    "fact_set",
                    "relation_set",
                    "review_slice_set",
                    "positive_composition",
                    "manifest",
                    "evidence",
                    "persistence",
                    "public_review",
                )
            )
        ):
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_AUTHORITY_CEILING_REJECTED
            )
        identity = document.get("coverage_ledger_digest")
        if type(identity) is not str or not identity:
            raise _ValidationFailure(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
            )
        return NEGATIVE_RESULT_KIND, document, identity

    def __admission_document(
        self,
        *,
        result_kind: str,
        ledger: Mapping[str, object],
        result_identity: str,
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "admission_function": ADMISSION_FUNCTION,
            "admission_domain": ADMISSION_DOMAIN,
            "route_result_binding_function": ROUTE_RESULT_BINDING_FUNCTION,
            "reconciliation_function": RECONCILIATION_FUNCTION,
            "terminal_branch": self.__terminal_branch,
            "selector_route": self.__selector_route,
            "selector_claim_id": self.__claim_id,
            "fact_consumer_attempt_id": self.__input_identity[
                "fact_consumer_attempt_id"
            ],
            "input_digests": {
                name: self.__input_identity[name] for name in _INPUT_DIGEST_FIELDS
            },
            "terminal_source_sha256": hashlib.sha256(
                self.__source_bytes
            ).hexdigest(),
            "result_kind": result_kind,
            "result_identity": result_identity,
            "coverage_ledger_digest": ledger["coverage_ledger_digest"],
            "root_chain_digest": ledger["root_chain_digest"],
            "authority_ceiling": {
                "private_application_output_admission": True,
                "route_discriminant": "EXACT_ONE_SHOT",
                "manifest": False,
                "derivation_evidence": False,
                "persistence": False,
                "public_review": False,
                "core_verdict": False,
                "r2_r6": False,
            },
        }
        value["application_admission_digest"] = semantic_digest(
            ADMISSION_FUNCTION, value
        )
        return value

    def _validate_admitted(
        self, admitted: "AdmittedUnifiedReviewCoverageOutput"
    ) -> None:
        with self.__lock:
            if (
                admitted is not self.__admitted
                or self.__state
                not in {
                    UnifiedOutputAdmissionState.ADMITTED_NORMAL,
                    UnifiedOutputAdmissionState.ADMITTED_NEGATIVE,
                }
                or self.__result is None
                or self.__phase is None
                or self.__admission_bytes is None
                or self.__phase.canonical_bytes != self.__admission_bytes
                or admitted._result is not self.__result
                or admitted._result_kind != self.__result_kind
                or admitted._phase is not self.__phase
                or admitted._admission_bytes is not self.__admission_bytes
            ):
                self.__fail(
                    UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
                )
            try:
                self.__route_coordinates()
                if self.__selector_route == NORMAL_ROUTE:
                    kind, ledger, identity = self.__validate_normal(self.__result)
                else:
                    kind, ledger, identity = self.__validate_negative(self.__result)
                if (
                    kind != self.__result_kind
                    or self.__admission_document(
                        result_kind=kind,
                        ledger=ledger,
                        result_identity=identity,
                    )
                    != json.loads(self.__admission_bytes)
                ):
                    raise _ValidationFailure(
                        UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
                    )
            except _ValidationFailure as exc:
                self.__fail(exc.family)
            except UnifiedOutputAdmissionError:
                raise
            except Exception as exc:
                try:
                    self.__fail(
                        UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
                    )
                except UnifiedOutputAdmissionError as error:
                    raise error from exc

    def _wrong_accessor(self) -> None:
        with self.__lock:
            self.__fail(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_ROUTE_REJECTED
            )


class AdmittedUnifiedReviewCoverageOutput:
    """Private discriminated view of one admitted exact downstream result."""

    def __init__(
        self,
        *,
        owner: BoundUnifiedReviewCoverageOutputAdmission,
        result: object,
        result_kind: str,
        phase: OwnedPhaseResult,
        admission_bytes: bytes,
        _token: object,
    ) -> None:
        if (
            _token is not _ADMITTED_TOKEN
            or type(owner) is not BoundUnifiedReviewCoverageOutputAdmission
            or type(phase) is not OwnedPhaseResult
            or type(admission_bytes) is not bytes
            or result_kind not in {NORMAL_RESULT_KIND, NEGATIVE_RESULT_KIND}
        ):
            raise UnifiedOutputAdmissionError(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_INPUT_REJECTED
            )
        self.__owner = owner
        self.__bound_owner = owner
        self._result = result
        self._result_kind = result_kind
        self._phase = phase
        self._admission_bytes = admission_bytes

    def __copy__(self):
        self.__owner._wrong_accessor()

    def __deepcopy__(self, _memo):
        return self.__copy__()

    def __reduce__(self):
        self.__owner._wrong_accessor()

    def __reduce_ex__(self, _protocol):
        return self.__reduce__()

    def __getstate__(self):
        self.__owner._wrong_accessor()

    def to_json(self):
        """Reject explicit private-object serialization and revoke authority."""

        self.__owner._wrong_accessor()

    def __validate(self) -> None:
        if self.__owner is not self.__bound_owner:
            raise UnifiedOutputAdmissionError(
                UnifiedOutputAdmissionFailureFamily.UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
            )
        self.__owner._validate_admitted(self)

    @property
    def terminal_branch(self) -> str:
        self.__validate()
        return json.loads(self._admission_bytes)["terminal_branch"]

    @property
    def selector_route(self) -> str:
        self.__validate()
        return json.loads(self._admission_bytes)["selector_route"]

    @property
    def result_kind(self) -> str:
        self.__validate()
        return self._result_kind

    @property
    def application_admission_identity(self) -> str:
        self.__validate()
        return ADMISSION_FUNCTION

    def normal_result(self) -> positive.OwnedReviewSliceCoverageComposition:
        self.__validate()
        if self._result_kind != NORMAL_RESULT_KIND:
            self.__owner._wrong_accessor()
        return self._result

    def negative_result(self) -> negative.AdmittedNegativeWorldCoverage:
        self.__validate()
        if self._result_kind != NEGATIVE_RESULT_KIND:
            self.__owner._wrong_accessor()
        return self._result

    def authority_ceiling_copy(self) -> dict[str, object]:
        self.__validate()
        return json.loads(self._admission_bytes)["authority_ceiling"]


def bind_unified_review_coverage_output_admission(
    route_claim: object,
) -> BoundUnifiedReviewCoverageOutputAdmission:
    """Bind an exact frozen selector claim before its downstream executes."""

    return BoundUnifiedReviewCoverageOutputAdmission(route_claim)
