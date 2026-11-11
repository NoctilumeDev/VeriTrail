from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Mapping, Sequence

from veritrail_review._review_coverage_ledger_conformance import (
    CoverageLedgerConformanceSource,
    validate_review_coverage_ledger,
)
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


CONTRACT_FUNCTION = "r1-same-attempt-derivation-evidence-continuity/0.1"
PRIVATE_CONTINUITY_DOMAIN = "SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1"
CONTROLLER_CAPTURE_FUNCTION = "r1-derivation-evidence-controller-capture/0.1"
BRANCH_PROJECTION_FUNCTION = (
    "r1-derivation-evidence-continuity-branch-projection/0.1"
)
RECONCILIATION_FUNCTION = (
    "r1-derivation-evidence-continuity-reconciliation/0.1"
)
PRIVATE_BINDING_IDENTITY = (
    "r1-same-attempt-derivation-evidence-continuity-binding/0.1"
)
PRIVATE_PROFILE_IDENTITY = (
    "r1-same-attempt-derivation-evidence-continuity-profile/0.1"
)
PRIVATE_WIRE_IDENTITY = (
    "r1-same-attempt-derivation-evidence-continuity-private-wire/0.1"
)
PROOF_IS_NOT_PROBLEM_SOLVING = True
QUALIFICATION_INHERITANCE_ALLOWED = False
LOCAL_NOT_GLOBAL = True
POST_R1_GLOBAL_CHECK_REQUIRED = True

NORMAL_ROUTE = "RELATION_HANDOFF"
NEGATIVE_ROUTE = "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"
NORMAL_VARIANT = "NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY"
NEGATIVE_VARIANT = "NEGATIVE_WORLD_COVERAGE_CONTINUITY"

_NEGATIVE_BRANCHES = {
    "ZERO_PARSE_DENOMINATOR",
    "ALL_PARSE_REJECTED",
    "PROJECTION_BLOCKED",
    "REQUIRED_PROVIDER_NON_SUCCESS",
}
_INPUT_DIGEST_FIELDS = (
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
)
_SLOT_TOKEN = object()
_VALUE_TOKEN = object()


class EvidenceContinuityState(str, Enum):
    PROVISIONAL = "PROVISIONAL"
    CAPTURING_FACT = "CAPTURING_FACT"
    FACT_CLOSED = "FACT_CLOSED"
    CAPTURING_NORMAL = "CAPTURING_NORMAL"
    CAPTURING_NEGATIVE = "CAPTURING_NEGATIVE"
    OUTPUT_ADMITTED = "OUTPUT_ADMITTED"
    COMMITTED = "COMMITTED"
    REVOKED = "REVOKED"


class EvidenceContinuityFailureFamily(str, Enum):
    EVIDENCE_CONTINUITY_INPUT_REJECTED = (
        "EVIDENCE_CONTINUITY_INPUT_REJECTED"
    )
    EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED = (
        "EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED"
    )
    EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING = (
        "EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING"
    )
    EVIDENCE_CONTINUITY_CONTROLLER_TIMING_REJECTED = (
        "EVIDENCE_CONTINUITY_CONTROLLER_TIMING_REJECTED"
    )
    EVIDENCE_CONTINUITY_BRANCH_REJECTED = (
        "EVIDENCE_CONTINUITY_BRANCH_REJECTED"
    )
    EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED = (
        "EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED"
    )
    EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED = (
        "EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED"
    )
    EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED = (
        "EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED"
    )
    EVIDENCE_CONTINUITY_LEDGER_RECONCILIATION_REJECTED = (
        "EVIDENCE_CONTINUITY_LEDGER_RECONCILIATION_REJECTED"
    )
    EVIDENCE_CONTINUITY_LEGACY_ALIAS_REJECTED = (
        "EVIDENCE_CONTINUITY_LEGACY_ALIAS_REJECTED"
    )
    EVIDENCE_CONTINUITY_ALREADY_COMMITTED = (
        "EVIDENCE_CONTINUITY_ALREADY_COMMITTED"
    )
    EVIDENCE_CONTINUITY_CONTEXT_REVOKED = (
        "EVIDENCE_CONTINUITY_CONTEXT_REVOKED"
    )
    EVIDENCE_CONTINUITY_AUTHORITY_CEILING_REJECTED = (
        "EVIDENCE_CONTINUITY_AUTHORITY_CEILING_REJECTED"
    )


class SameAttemptDerivationEvidenceContinuityError(ValueError):
    def __init__(self, family: EvidenceContinuityFailureFamily) -> None:
        self.failure_family = family
        super().__init__(family.value)


def _route_for_branch(branch: object) -> str:
    if branch == "NORMAL_FULFILLED":
        return NORMAL_ROUTE
    if branch in _NEGATIVE_BRANCHES:
        return NEGATIVE_ROUTE
    raise SameAttemptDerivationEvidenceContinuityError(
        EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED
    )


def _variant_for_branch(branch: object) -> str:
    return NORMAL_VARIANT if _route_for_branch(branch) == NORMAL_ROUTE else NEGATIVE_VARIANT


def _wall_time(value: object) -> str:
    try:
        if type(value) is not str or not value.endswith("Z"):
            raise ValueError
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
        canonical = parsed.astimezone(timezone.utc).isoformat(
            timespec="microseconds"
        ).replace("+00:00", "Z")
        if canonical != value:
            raise ValueError
    except (TypeError, ValueError, OverflowError) as exc:
        raise SameAttemptDerivationEvidenceContinuityError(
            EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_REJECTED
        ) from exc
    return value


def _strict_time_chain(values: Sequence[str]) -> None:
    if any(left > right for left, right in zip(values, values[1:])):
        raise SameAttemptDerivationEvidenceContinuityError(
            EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_REJECTED
        )


def _context_is_live(context: object, identity: tuple[object, ...]) -> bool:
    return (
        type(context) is BudgetContext
        and (
            context.limits,
            context.started_at_monotonic,
            context.execution_deadline_monotonic,
        )
        == identity
        and context.state is BudgetState.RUNNING
        and context.stop_trigger is None
        and context.checkpoint()
    )


class _SameAttemptContinuityCaptureSlot:
    def __init__(self, *, _token: object) -> None:
        if _token is not _SLOT_TOKEN:
            raise SameAttemptDerivationEvidenceContinuityError(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_INPUT_REJECTED
            )
        self.__lock = RLock()
        self.__state = EvidenceContinuityState.PROVISIONAL
        self.__failure_family: EvidenceContinuityFailureFamily | None = None
        self.__consumer = None
        self.__attempt = None
        self.__inputs = None
        self.__context = None
        self.__eligibility = None
        self.__selector = None
        self.__closure = None
        self.__route_claim = None
        self.__result = None
        self.__result_kind = None
        self.__admitted = None
        self.__value = None
        self.__attempt_id = None
        self.__derivation_id = None
        self.__attempt_started_at = None
        self.__fact_phase_finished_at = None
        self.__terminal_source_bytes = None
        self.__branch = None
        self.__route = None
        self.__claim_id = None
        self.__context_identity = None
        self.__input_digests = None
        self.__fact_runs: dict[object, dict[str, object]] = {}
        self.__transition = None
        self.__application_admission_bytes = None
        self.__committed_bytes = None

    @property
    def state(self) -> EvidenceContinuityState:
        with self.__lock:
            return self.__state

    def _fail(self, family: EvidenceContinuityFailureFamily):
        self.__state = EvidenceContinuityState.REVOKED
        if self.__failure_family is None:
            self.__failure_family = family
        raise SameAttemptDerivationEvidenceContinuityError(family)

    def _revoke(self, family: EvidenceContinuityFailureFamily) -> None:
        with self.__lock:
            self.__state = EvidenceContinuityState.REVOKED
            if self.__failure_family is None:
                self.__failure_family = family

    def _admit_fact_attempt(
        self,
        *,
        consumer: object,
        attempt: object,
        inputs: object,
        context: object,
        eligibility: object,
        claims: tuple[object, ...],
        attempt_id: str,
        derivation_id: str,
        attempt_started_at: str,
    ) -> None:
        from veritrail_review._fact_fulfillment import OwnedProductFactConsumer

        with self.__lock:
            if self.__state is not EvidenceContinuityState.PROVISIONAL:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED
                )
            if (
                type(consumer) is not OwnedProductFactConsumer
                or type(inputs) is not DerivationInputSet
                or type(context) is not BudgetContext
                or type(claims) is not tuple
                or type(attempt_id) is not str
                or not attempt_id
                or type(derivation_id) is not str
                or not derivation_id
                or not _context_is_live(
                    context,
                    (
                        context.limits,
                        context.started_at_monotonic,
                        context.execution_deadline_monotonic,
                    ),
                )
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_INPUT_REJECTED
                )
            self.__consumer = consumer
            self.__attempt = attempt
            self.__inputs = inputs
            self.__context = context
            self.__eligibility = eligibility
            self.__attempt_id = attempt_id
            self.__derivation_id = derivation_id
            self.__attempt_started_at = _wall_time(attempt_started_at)
            self.__context_identity = (
                context.limits,
                context.started_at_monotonic,
                context.execution_deadline_monotonic,
            )
            self.__input_digests = tuple(
                getattr(inputs, name) for name in _INPUT_DIGEST_FIELDS
            )
            self.__expected_claims = claims
            self.__state = EvidenceContinuityState.CAPTURING_FACT

    def _bind_selector(self, selector: object, consumer: object) -> None:
        from veritrail_review._post_terminal_fact_dual_successor import (
            OwnedPostTerminalFactDualSuccessor,
        )

        with self.__lock:
            if (
                self.__state is not EvidenceContinuityState.CAPTURING_FACT
                or type(selector) is not OwnedPostTerminalFactDualSuccessor
                or consumer is not self.__consumer
                or self.__selector is not None
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            self.__selector = selector

    def _begin_fact_provider_run(
        self, consumer: object, claim: object, started_at: str
    ) -> None:
        with self.__lock:
            if (
                self.__state is not EvidenceContinuityState.CAPTURING_FACT
                or consumer is not self.__consumer
                or not any(claim is candidate for candidate in self.__expected_claims)
                or claim in self.__fact_runs
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED
                )
            started = _wall_time(started_at)
            _strict_time_chain((self.__attempt_started_at, started))
            self.__fact_runs[claim] = {
                "claim": claim,
                "started_at": started,
                "finished_at": None,
                "phase_finished_at": None,
                "lifecycle": None,
            }

    def _finish_fact_provider_run(
        self,
        consumer: object,
        claim: object,
        *,
        lifecycle: str,
        finished_at: str,
        phase_finished_at: str,
    ) -> None:
        with self.__lock:
            run = self.__fact_runs.get(claim)
            if (
                self.__state is not EvidenceContinuityState.CAPTURING_FACT
                or consumer is not self.__consumer
                or run is None
                or run["claim"] is not claim
                or run["finished_at"] is not None
                or type(lifecycle) is not str
                or not lifecycle
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED
                )
            finished = _wall_time(finished_at)
            phase_finished = _wall_time(phase_finished_at)
            _strict_time_chain((run["started_at"], finished, phase_finished))
            run["finished_at"] = finished
            run["phase_finished_at"] = phase_finished
            run["lifecycle"] = lifecycle

    def _close_fact_phase(
        self,
        consumer: object,
        closure: object,
        observations: tuple[object, ...],
        finished_at: str,
    ) -> None:
        from veritrail_review._fact_fulfillment import OwnedProductFactClosure

        with self.__lock:
            if (
                self.__state is not EvidenceContinuityState.CAPTURING_FACT
                or consumer is not self.__consumer
                or type(closure) is not OwnedProductFactClosure
                or type(observations) is not tuple
                or self.__closure is not None
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED
                )
            if len(observations) != len(self.__fact_runs):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING
                )
            for observation in observations:
                run = self.__fact_runs.get(observation._claim)
                if (
                    run is None
                    or run["finished_at"] is None
                    or run["phase_finished_at"] is None
                    or run["lifecycle"] != observation.lifecycle
                ):
                    self._fail(
                        EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING
                    )
            fact_finished = _wall_time(finished_at)
            for run in self.__fact_runs.values():
                _strict_time_chain((run["phase_finished_at"], fact_finished))
            self.__closure = closure
            self.__fact_phase_finished_at = fact_finished

    def _capture_terminal_source(
        self,
        *,
        selector: object,
        closure: object,
        source: Mapping[str, object],
        branch: str,
        route: str,
    ) -> None:
        with self.__lock:
            if (
                self.__state is not EvidenceContinuityState.CAPTURING_FACT
                or selector is not self.__selector
                or closure is not self.__closure
                or self.__fact_phase_finished_at is None
                or type(source) is not dict
                or branch != source.get("branch")
                or route != _route_for_branch(branch)
                or self.__terminal_source_bytes is not None
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED
                )
            identity = source.get("input_identity", {})
            if (
                identity.get("fact_consumer_attempt_id") != self.__attempt_id
                or identity.get("derivation_id") != self.__derivation_id
                or tuple(identity.get(name) for name in _INPUT_DIGEST_FIELDS)
                != self.__input_digests
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            self.__terminal_source_bytes = canonical_json_bytes(source)
            self.__branch = branch
            self.__route = route
            self.__state = EvidenceContinuityState.FACT_CLOSED

    def _bind_application_route(
        self,
        *,
        selector: object,
        route_claim: object,
        claim_id: str,
        source: Mapping[str, object],
        inputs: object,
        context: object,
        closure: object,
        fact_attempt: object,
        eligibility: object,
        route: str,
    ) -> "_SameAttemptContinuityCaptureSlot":
        with self.__lock:
            if (
                self.__state is not EvidenceContinuityState.FACT_CLOSED
                or selector is not self.__selector
                or route_claim is None
                or type(claim_id) is not str
                or not claim_id
                or inputs is not self.__inputs
                or context is not self.__context
                or closure is not self.__closure
                or fact_attempt is not self.__attempt
                or eligibility is not self.__eligibility
                or route != self.__route
                or canonical_json_bytes(source) != self.__terminal_source_bytes
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            self.__route_claim = route_claim
            self.__claim_id = claim_id
            self.__state = (
                EvidenceContinuityState.CAPTURING_NORMAL
                if route == NORMAL_ROUTE
                else EvidenceContinuityState.CAPTURING_NEGATIVE
            )
            return self

    def _capture_normal_transition(
        self, *, selector: object, route_claim: object, admission: object
    ) -> None:
        from veritrail_review._fact_relation_transition import (
            OwnedFactRelationTransitionAdmission,
        )

        with self.__lock:
            if self.__state is EvidenceContinuityState.FACT_CLOSED:
                self.__state = EvidenceContinuityState.REVOKED
                self.__failure_family = (
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED
                )
                return
            if (
                self.__state is not EvidenceContinuityState.CAPTURING_NORMAL
                or selector is not self.__selector
                or route_claim is not self.__route_claim
                or type(admission) is not OwnedFactRelationTransitionAdmission
                or self.__transition is not None
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            try:
                exact_admission, document, capture = (
                    admission._same_attempt_continuity_capture_coordinates()
                )
            except Exception as exc:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            if (
                exact_admission is not admission
                or document["handoff"]["claim_id"] != self.__claim_id
                or document["handoff"]["fact_consumer_attempt_id"]
                != self.__attempt_id
                or canonical_json_bytes(document["fact_handoff_source"])
                != self.__terminal_source_bytes
                or capture.get("attempt_started_at")
                != document["transition_attempt"]["attempt_started_at"]
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            self.__validate_relation_capture(document, capture)
            self.__transition = {
                "admission": admission,
                "document_bytes": canonical_json_bytes(document),
                "capture_bytes": canonical_json_bytes(capture),
            }

    def _commit(self, admitted: object) -> "CommittedSameAttemptDerivationEvidenceContinuity":
        with self.__lock:
            if self.__state in {
                EvidenceContinuityState.OUTPUT_ADMITTED,
                EvidenceContinuityState.COMMITTED,
            }:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_ALREADY_COMMITTED
                )
            expected = (
                EvidenceContinuityState.CAPTURING_NORMAL
                if self.__route == NORMAL_ROUTE
                else EvidenceContinuityState.CAPTURING_NEGATIVE
            )
            if self.__state is not expected:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED
                )
            if not _context_is_live(self.__context, self.__context_identity):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTEXT_REVOKED
                )
            self.__validate_controller_captures()
            try:
                coordinates = admitted._same_attempt_continuity_commit_coordinates()
            except Exception as exc:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
                )
            (
                exact_admitted,
                route_claim,
                selector,
                closure,
                source,
                inputs,
                context,
                fact_attempt,
                eligibility,
                result,
                result_kind,
                application_bytes,
            ) = coordinates
            if (
                exact_admitted is not admitted
                or route_claim is not self.__route_claim
                or selector is not self.__selector
                or closure is not self.__closure
                or canonical_json_bytes(source) != self.__terminal_source_bytes
                or inputs is not self.__inputs
                or context is not self.__context
                or fact_attempt is not self.__attempt
                or eligibility is not self.__eligibility
                or result is None
                or type(application_bytes) is not bytes
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            self.__result = result
            self.__result_kind = result_kind
            self.__admitted = admitted
            self.__application_admission_bytes = application_bytes
            self.__state = EvidenceContinuityState.OUTPUT_ADMITTED
            reconciliation = self.__independent_reconciliation(
                result=result,
                result_kind=result_kind,
                application_bytes=application_bytes,
            )
            document = self.__committed_document(
                result=result,
                result_kind=result_kind,
                reconciliation=reconciliation,
            )
            encoded = canonical_json_bytes(document)
            value = CommittedSameAttemptDerivationEvidenceContinuity(
                self,
                result,
                _variant_for_branch(self.__branch),
                encoded,
                _token=_VALUE_TOKEN,
            )
            self.__committed_bytes = encoded
            self.__value = value
            self.__state = EvidenceContinuityState.COMMITTED
            self._validate_committed_admission(admitted, result, application_bytes)
            return value

    def __validate_relation_capture(
        self, document: Mapping[str, object], capture: Mapping[str, object]
    ) -> None:
        try:
            expected_run_ids = document["admission"]["provider_run_ids"]
            lineage = document["provider_lineage"]
            provider_runs = capture["provider_runs"]
            if (
                capture.get("function") != CONTROLLER_CAPTURE_FUNCTION
                or capture.get("attempt_started_at")
                != document["transition_attempt"]["attempt_started_at"]
                or type(expected_run_ids) is not list
                or type(lineage) is not list
                or type(provider_runs) is not list
                or len(expected_run_ids) != len(lineage)
                or len(provider_runs) != len(lineage)
            ):
                raise ValueError
            lineage_by_run_id = {
                item["terminal"]["provider_run_id"]: item for item in lineage
            }
            if (
                len(lineage_by_run_id) != len(lineage)
                or [item.get("provider_run_id") for item in provider_runs]
                != expected_run_ids
                or list(lineage_by_run_id) != expected_run_ids
            ):
                raise ValueError
            relation_finished = _wall_time(capture.get("phase_finished_at"))
            _strict_time_chain((self.__fact_phase_finished_at, relation_finished))
            for run in provider_runs:
                terminal = lineage_by_run_id[run["provider_run_id"]]["terminal"]
                if any(
                    run.get(name) != terminal.get(name)
                    for name in (
                        "provider_descriptor",
                        "provider_run_status",
                        "release_outcome",
                        "phase_status",
                    )
                ):
                    raise ValueError
                _strict_time_chain(
                    (
                        self.__fact_phase_finished_at,
                        _wall_time(run.get("started_at")),
                        _wall_time(run.get("finished_at")),
                        _wall_time(run.get("phase_finished_at")),
                        relation_finished,
                    )
                )
        except SameAttemptDerivationEvidenceContinuityError:
            raise
        except Exception as exc:
            raise SameAttemptDerivationEvidenceContinuityError(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
            ) from exc

    def __validate_controller_captures(self) -> None:
        if (
            self.__attempt_started_at is None
            or self.__fact_phase_finished_at is None
            or len(self.__fact_runs) != len(self.__expected_claims)
        ):
            self._fail(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING
            )
        for claim in self.__expected_claims:
            run = self.__fact_runs.get(claim)
            if (
                run is None
                or run.get("claim") is not claim
                or run.get("finished_at") is None
                or run.get("phase_finished_at") is None
                or run.get("lifecycle") is None
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING
                )
            _strict_time_chain(
                (
                    _wall_time(self.__attempt_started_at),
                    _wall_time(run.get("started_at")),
                    _wall_time(run.get("finished_at")),
                    _wall_time(run.get("phase_finished_at")),
                    _wall_time(self.__fact_phase_finished_at),
                )
            )
        if self.__route == NORMAL_ROUTE:
            if self.__transition is None:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            try:
                transition = json.loads(self.__transition["document_bytes"])
                capture = json.loads(self.__transition["capture_bytes"])
            except Exception as exc:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            if transition["handoff"]["claim_id"] != self.__claim_id:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            try:
                self.__validate_relation_capture(transition, capture)
            except SameAttemptDerivationEvidenceContinuityError as exc:
                self._fail(exc.failure_family)
        elif self.__transition is not None:
            self._fail(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED
            )

    def __independent_reconciliation(
        self, *, result: object, result_kind: str, application_bytes: bytes
    ) -> dict[str, object]:
        from veritrail_review import (
            _negative_world_coverage_authority_recovery as negative,
        )
        from veritrail_review import _relation_transition_slice_composition as positive

        source = json.loads(self.__terminal_source_bytes)
        application = json.loads(application_bytes)
        branch = source.get("branch")
        route = _route_for_branch(branch)
        variant = _variant_for_branch(branch)
        if (
            route != self.__route
            or application.get("terminal_branch") != branch
            or application.get("selector_route") != route
            or application.get("selector_claim_id") != self.__claim_id
            or application.get("fact_consumer_attempt_id") != self.__attempt_id
            or application.get("terminal_source_sha256")
            != hashlib.sha256(self.__terminal_source_bytes).hexdigest()
        ):
            self._fail(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
            )

        if route == NORMAL_ROUTE:
            if (
                type(result) is not positive.OwnedReviewSliceCoverageComposition
                or result_kind != "NORMAL_REVIEW_SLICE_COVERAGE"
                or self.__transition is None
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED
                )
            coordinates = result._application_output_admission_coordinates()
            exact_result, inputs, context, _eligibility, conformance, _phase, document = coordinates
            if (
                exact_result is not result
                or inputs is not self.__inputs
                or context is not self.__context
                or type(conformance) is not CoverageLedgerConformanceSource
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            transition = json.loads(self.__transition["document_bytes"])
            request = document.get("bridge_admission", {}).get("request", {})
            if (
                request.get("handoff_claim_id") != self.__claim_id
                or request.get("transition_attempt_id")
                != transition["transition_attempt"]["attempt_id"]
                or request.get("relation_set_digest")
                != transition["relation_set"]["relation_set_digest"]
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            ledger = document.get("coverage_ledger")
            result_identity = document.get("composition_digest")
            qualified_absence = False
        else:
            if (
                type(result) is not negative.AdmittedNegativeWorldCoverage
                or result_kind != "NEGATIVE_WORLD_COVERAGE"
                or self.__transition is not None
                or source.get("fact_set") is not None
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED
                )
            coordinates = result._application_output_admission_coordinates()
            (
                exact_result,
                _attempt,
                _validation,
                _phase,
                candidate_bytes,
                conformance,
                _exact_attempt,
                carrier,
                claim_id,
                exact_source,
                inputs,
                context,
                exact_closure,
            ) = coordinates
            if (
                exact_result is not result
                or carrier is not self.__route_claim
                or claim_id != self.__claim_id
                or canonical_json_bytes(exact_source) != self.__terminal_source_bytes
                or inputs is not self.__inputs
                or context is not self.__context
                or exact_closure is not self.__closure
                or type(conformance) is not CoverageLedgerConformanceSource
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            ledger = json.loads(candidate_bytes)
            result_identity = ledger.get("coverage_ledger_digest")
            ceiling = result.authority_ceiling_copy()
            qualified_absence = all(
                ceiling.get(name) is False
                for name in ("fact_set", "relation_set", "review_slice_set")
            )
            if not qualified_absence:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_AUTHORITY_CEILING_REJECTED
                )

        if type(ledger) is not dict or type(result_identity) is not str:
            self._fail(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
            )
        try:
            validate_review_coverage_ledger(ledger, conformance)
        except Exception as exc:
            self._fail(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_LEDGER_RECONCILIATION_REJECTED
            )
        if (
            application.get("result_identity") != result_identity
            or application.get("coverage_ledger_digest")
            != ledger.get("coverage_ledger_digest")
            or application.get("root_chain_digest") != ledger.get("root_chain_digest")
        ):
            self._fail(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_LEDGER_RECONCILIATION_REJECTED
            )
        payload = {
            "function": RECONCILIATION_FUNCTION,
            "status": "RECONCILED",
            "terminal_branch": branch,
            "selector_route": route,
            "continuity_variant": variant,
            "qualified_absence": qualified_absence,
            "coverage_ledger_digest": ledger["coverage_ledger_digest"],
            "root_chain_digest": ledger["root_chain_digest"],
            "application_admission_digest": application[
                "application_admission_digest"
            ],
            "common_mode_trust_roots": [
                "veritrail-json-c14n/1",
                "validate_review_coverage_ledger",
            ],
        }
        payload["reconciliation_digest"] = semantic_digest(
            RECONCILIATION_FUNCTION, payload
        )
        return payload

    def __fact_capture_document(self) -> dict[str, object]:
        runs = []
        for claim in self.__expected_claims:
            run = self.__fact_runs.get(claim)
            if run is None:
                runs.append(
                    {
                        "provider_descriptor": claim.binding.descriptor.document(),
                        "launch_key": claim.binding.launch_key,
                        "lifecycle": "NOT_STARTED",
                        "started_at": None,
                        "finished_at": None,
                        "phase_finished_at": None,
                    }
                )
                continue
            runs.append(
                {
                    "provider_descriptor": claim.binding.descriptor.document(),
                    "launch_key": claim.binding.launch_key,
                    "lifecycle": run["lifecycle"],
                    "started_at": run["started_at"],
                    "finished_at": run["finished_at"],
                    "phase_finished_at": run["phase_finished_at"],
                }
            )
        return {
            "function": CONTROLLER_CAPTURE_FUNCTION,
            "attempt_started_at": self.__attempt_started_at,
            "provider_runs": runs,
            "phase_finished_at": self.__fact_phase_finished_at,
        }

    def __committed_document(
        self, *, result: object, result_kind: str, reconciliation: Mapping[str, object]
    ) -> dict[str, object]:
        application = json.loads(self.__application_admission_bytes)
        transition_capture = (
            None
            if self.__transition is None
            else json.loads(self.__transition["capture_bytes"])
        )
        transition_digest = (
            None
            if self.__transition is None
            else hashlib.sha256(self.__transition["document_bytes"]).hexdigest()
        )
        value = {
            "contract_function": CONTRACT_FUNCTION,
            "private_continuity_domain": PRIVATE_CONTINUITY_DOMAIN,
            "binding_identity": PRIVATE_BINDING_IDENTITY,
            "profile_identity": PRIVATE_PROFILE_IDENTITY,
            "wire_identity": PRIVATE_WIRE_IDENTITY,
            "branch_projection_function": BRANCH_PROJECTION_FUNCTION,
            "continuity_variant": _variant_for_branch(self.__branch),
            "terminal_branch": self.__branch,
            "selector_route": self.__route,
            "selector_claim_id": self.__claim_id,
            "derivation_id": self.__derivation_id,
            "fact_consumer_attempt_id": self.__attempt_id,
            "input_digests": {
                name: getattr(self.__inputs, name) for name in _INPUT_DIGEST_FIELDS
            },
            "terminal_source_sha256": hashlib.sha256(
                self.__terminal_source_bytes
            ).hexdigest(),
            "fact_controller_capture": self.__fact_capture_document(),
            "relation_controller_capture": transition_capture,
            "transition_admission_sha256": transition_digest,
            "result_kind": result_kind,
            "result_identity": application["result_identity"],
            "coverage_ledger_digest": application["coverage_ledger_digest"],
            "root_chain_digest": application["root_chain_digest"],
            "application_admission_digest": application[
                "application_admission_digest"
            ],
            "reconciliation": copy.deepcopy(dict(reconciliation)),
            "authority_ceiling": {
                "private_same_attempt_continuity": True,
                "exact_discriminated_one_shot_branch": True,
                "controller_timing_provenance_original_execution_only": True,
                "legacy_evidence_0_2": False,
                "public_evidence_schema": False,
                "manifest": False,
                "persistence": False,
                "public_review": False,
                "core_verdict": False,
                "global_composition_authority": False,
                "r2_r6": False,
            },
        }
        value["continuity_digest"] = semantic_digest(CONTRACT_FUNCTION, value)
        return value

    def _validate_committed_admission(
        self, admitted: object, result: object, application_bytes: bytes
    ) -> None:
        with self.__lock:
            if (
                self.__state is not EvidenceContinuityState.COMMITTED
                or admitted is not self.__admitted
                or result is not self.__result
                or type(self.__result_kind) is not str
                or application_bytes is not self.__application_admission_bytes
                or self.__value is None
                or type(self.__committed_bytes) is not bytes
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            if not _context_is_live(self.__context, self.__context_identity):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTEXT_REVOKED
                )
            self.__validate_controller_captures()
            try:
                committed = json.loads(self.__committed_bytes)
            except Exception as exc:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
                )
            if canonical_json_bytes(committed) != self.__committed_bytes:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
                )
            if tuple(
                getattr(self.__inputs, name) for name in _INPUT_DIGEST_FIELDS
            ) != self.__input_digests:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            if (
                canonical_json_bytes(self.__fact_capture_document())
                != canonical_json_bytes(committed["fact_controller_capture"])
                or hashlib.sha256(self.__terminal_source_bytes).hexdigest()
                != committed["terminal_source_sha256"]
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING
                )
            current_relation_capture = (
                None
                if self.__transition is None
                else json.loads(self.__transition["capture_bytes"])
            )
            if canonical_json_bytes(current_relation_capture) != canonical_json_bytes(
                committed["relation_controller_capture"]
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
                )
            try:
                current_reconciliation = self.__independent_reconciliation(
                    result=self.__result,
                    result_kind=self.__result_kind,
                    application_bytes=self.__application_admission_bytes,
                )
            except SameAttemptDerivationEvidenceContinuityError:
                raise
            except Exception:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
                )
            if canonical_json_bytes(current_reconciliation) != canonical_json_bytes(
                committed["reconciliation"]
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_LEDGER_RECONCILIATION_REJECTED
                )

    def _committed_value(self, admitted: object):
        with self.__lock:
            if admitted is not self.__admitted or self.__value is None:
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            self._validate_committed_admission(
                admitted, self.__result, self.__application_admission_bytes
            )
            return self.__value

    def _validate_value(self, value: object, result: object, encoded: bytes) -> None:
        with self.__lock:
            if (
                value is not self.__value
                or result is not self.__result
                or encoded is not self.__committed_bytes
            ):
                self._fail(
                    EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
                )
            self._validate_committed_admission(
                self.__admitted, self.__result, self.__application_admission_bytes
            )

    def _wrong_accessor(self) -> None:
        with self.__lock:
            self._fail(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_BRANCH_REJECTED
            )


class CommittedSameAttemptDerivationEvidenceContinuity:
    def __init__(
        self,
        owner: _SameAttemptContinuityCaptureSlot,
        result: object,
        variant: str,
        encoded: bytes,
        *,
        _token: object,
    ) -> None:
        if (
            _token is not _VALUE_TOKEN
            or type(owner) is not _SameAttemptContinuityCaptureSlot
            or variant not in {NORMAL_VARIANT, NEGATIVE_VARIANT}
            or type(encoded) is not bytes
        ):
            raise SameAttemptDerivationEvidenceContinuityError(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_INPUT_REJECTED
            )
        self.__owner = owner
        self.__bound_owner = owner
        self.__result = result
        self.__bound_result = result
        self.__variant = variant
        self.__encoded = encoded
        self.__bound_encoded = encoded

    def __copy__(self):
        self.__owner._revoke(
            EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
        )
        raise SameAttemptDerivationEvidenceContinuityError(
            EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()

    def __reduce__(self):
        return self.__copy__()

    def __reduce_ex__(self, _protocol):
        return self.__reduce__()

    def __getstate__(self):
        return self.__copy__()

    def to_json(self):
        return self.__copy__()

    def __validate(self) -> None:
        if (
            self.__owner is not self.__bound_owner
            or self.__result is not self.__bound_result
            or self.__encoded is not self.__bound_encoded
        ):
            self.__owner._wrong_accessor()
        self.__owner._validate_value(self, self.__result, self.__encoded)

    @property
    def continuity_variant(self) -> str:
        self.__validate()
        return self.__variant

    @property
    def terminal_branch(self) -> str:
        self.__validate()
        return json.loads(self.__encoded)["terminal_branch"]

    @property
    def selector_route(self) -> str:
        self.__validate()
        return json.loads(self.__encoded)["selector_route"]

    def normal_result(self):
        self.__validate()
        if self.__variant != NORMAL_VARIANT:
            self.__owner._wrong_accessor()
        return self.__result

    def negative_result(self):
        self.__validate()
        if self.__variant != NEGATIVE_VARIANT:
            self.__owner._wrong_accessor()
        return self.__result

    def authority_ceiling_copy(self) -> dict[str, object]:
        self.__validate()
        return json.loads(self.__encoded)["authority_ceiling"]

    def _document_copy(self) -> dict[str, object]:
        self.__validate()
        return json.loads(self.__encoded)


def _create_same_attempt_continuity_capture_slot() -> _SameAttemptContinuityCaptureSlot:
    return _SameAttemptContinuityCaptureSlot(_token=_SLOT_TOKEN)
