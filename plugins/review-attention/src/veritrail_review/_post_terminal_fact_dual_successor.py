"""Private post-terminal selector for the frozen Fact dual-successor seam.

The selector owns no Relation or Coverage result.  It preserves one live Fact
attempt and grants exactly one route-specific, non-serializable claim after the
Fact owner has produced and revalidated a complete terminal closure.
"""

from __future__ import annotations

import copy
import hashlib
import json
from enum import Enum
from threading import Lock
from typing import Callable, Mapping, Sequence
from uuid import uuid4

from veritrail_review._execution_cell import DEFAULT_TRANSPORT_LIMITS
from veritrail_review._execution_cell_binding import ProviderBinding
from veritrail_review._execution_cell_protocol import (
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._fact_fulfillment import (
    OwnedProductFactClaim,
    OwnedProductFactClosure,
    OwnedProductFactConsumer,
    OwnedProductFactObservation,
    _create_product_fact_consumer,
)
from veritrail_review._fact_fulfillment_binding import (
    _admit_relation_transition_fact_applicability,
)
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
)
from veritrail_review._parse_fulfillment import OwnedParseFulfillmentClosure
from veritrail_review._source_operation_gate import _input_state_seal
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


HANDOFF_DOMAIN = "POST_TERMINAL_DUAL_SUCCESSOR_0_1"
ROUTE_SELECTION_FUNCTION = "r1-post-terminal-fact-route-selection/0.1"
CLAIM_FUNCTION = "r1-post-terminal-fact-dual-successor-claim/0.1"
RELATION_ROUTE = "RELATION_HANDOFF"
EXACT_INPUT_ROUTE = "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"

_SELECTOR_TOKEN = object()
_RELATION_CARRIER_TOKEN = object()
_KNOWN_BRANCHES = (
    "NORMAL_FULFILLED",
    "ZERO_PARSE_DENOMINATOR",
    "ALL_PARSE_REJECTED",
    "PROJECTION_BLOCKED",
    "REQUIRED_PROVIDER_NON_SUCCESS",
)
_NEGATIVE_BRANCHES = frozenset(_KNOWN_BRANCHES[1:])
_CANONICAL_FIELDS = (
    "source_snapshot_canonical_bytes",
    "review_policy_canonical_bytes",
    "derivation_profile_canonical_bytes",
)
_DIGEST_FIELDS = (
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
)


class DualSuccessorState(str, Enum):
    SEALED_NOT_ROUTABLE = "SEALED_NOT_ROUTABLE"
    TERMINAL_READY = "TERMINAL_READY"
    CLAIMED_RELATION = "CLAIMED_RELATION"
    CLAIMED_EXACT_INPUT = "CLAIMED_EXACT_INPUT"
    REVOKED = "REVOKED"


class DualSuccessorFailureFamily(str, Enum):
    INPUT_REJECTED = "DUAL_SUCCESSOR_INPUT_REJECTED"
    PRE_TERMINAL_CLAIM_REJECTED = (
        "DUAL_SUCCESSOR_PRE_TERMINAL_CLAIM_REJECTED"
    )
    TERMINAL_SOURCE_REJECTED = "DUAL_SUCCESSOR_TERMINAL_SOURCE_REJECTED"
    BRANCH_RECONCILIATION_REJECTED = (
        "DUAL_SUCCESSOR_BRANCH_RECONCILIATION_REJECTED"
    )
    WRONG_ROUTE_REJECTED = "DUAL_SUCCESSOR_WRONG_ROUTE_REJECTED"
    ALREADY_CONSUMED = "DUAL_SUCCESSOR_ALREADY_CONSUMED"
    SAME_ATTEMPT_REJECTED = "DUAL_SUCCESSOR_SAME_ATTEMPT_REJECTED"
    CONTEXT_REVOKED = "DUAL_SUCCESSOR_CONTEXT_REVOKED"


class PostTerminalDualSuccessorError(ValueError):
    """A private route claim failed without creating downstream authority."""

    def __init__(
        self, failure_family: DualSuccessorFailureFamily, message: str
    ) -> None:
        super().__init__(message)
        self.failure_family = failure_family


class _SharedConsumeSlot:
    def __init__(self) -> None:
        self.lock = Lock()
        self.state = DualSuccessorState.SEALED_NOT_ROUTABLE
        self.failure_family: DualSuccessorFailureFamily | None = None
        self.claim_id: str | None = None
        self.route: str | None = None


def _copy_blob_map(inputs: DerivationInputSet) -> dict[str, bytes]:
    blobs = inputs.verified_blob_bytes_by_object_identity
    if not isinstance(blobs, Mapping):
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.INPUT_REJECTED,
            "verified blob map is invalid",
        )
    try:
        copied = {
            key: memoryview(value).tobytes()
            for key, value in sorted(blobs.items())
            if type(key) is str and type(value) is bytes
        }
    except Exception as exc:
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.INPUT_REJECTED,
            "verified blob map is invalid",
        ) from exc
    if len(copied) != len(blobs):
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.INPUT_REJECTED,
            "verified blob map is invalid",
        )
    return copied


def _selector_route_for_source(source: Mapping[str, object]) -> str:
    """Select only from frozen Fact terminal truth, never downstream output."""

    branch = source.get("branch")
    if branch == "NORMAL_FULFILLED":
        return RELATION_ROUTE
    if branch in _NEGATIVE_BRANCHES:
        return EXACT_INPUT_ROUTE
    raise PostTerminalDualSuccessorError(
        DualSuccessorFailureFamily.BRANCH_RECONCILIATION_REJECTED,
        "terminal branch has no frozen route",
    )


def _application_route_matches(branch: str, route: str) -> bool:
    """Independent application-side mapping; deliberately not the selector."""

    if branch == "NORMAL_FULFILLED":
        return route == RELATION_ROUTE
    if branch in {
        "ZERO_PARSE_DENOMINATOR",
        "ALL_PARSE_REJECTED",
        "PROJECTION_BLOCKED",
        "REQUIRED_PROVIDER_NON_SUCCESS",
    }:
        return route == EXACT_INPUT_ROUTE
    return False


def _validate_terminal_branch_semantics(source: Mapping[str, object]) -> str:
    if type(source) is not dict or set(_KNOWN_BRANCHES) != {
        "NORMAL_FULFILLED",
        "ZERO_PARSE_DENOMINATOR",
        "ALL_PARSE_REJECTED",
        "PROJECTION_BLOCKED",
        "REQUIRED_PROVIDER_NON_SUCCESS",
    }:
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
            "terminal branch vocabulary changed",
        )
    branch = source.get("branch")
    projection = source.get("fact_projection")
    partition = source.get("parse_partition")
    history = source.get("provider_history")
    whole = source.get("whole_attempt")
    if (
        branch not in _KNOWN_BRANCHES
        or not isinstance(projection, Mapping)
        or not isinstance(partition, Mapping)
        or not isinstance(history, list)
        or not isinstance(whole, Mapping)
        or whole.get("budget_state") != "RUNNING"
        or whole.get("stop_trigger") is not None
        or any(
            item.get("lifecycle") in {"RELEASE_FAILED", "INTERRUPTED"}
            for item in history
            if isinstance(item, Mapping)
        )
    ):
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
            "terminal source is malformed or unsafe",
        )
    denominator = partition.get("denominator")
    accepted = partition.get("accepted")
    if not isinstance(denominator, list) or not isinstance(accepted, list):
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
            "parse partition is malformed",
        )
    required_lifecycles = [
        item.get("lifecycle")
        for item in history
        if isinstance(item, Mapping) and item.get("required") is True
    ]
    if branch == "NORMAL_FULFILLED":
        valid = (
            projection.get("status") == "QUALIFIED"
            and isinstance(source.get("fact_set"), Mapping)
            and bool(accepted)
            and whole.get("parent_eligibility") == "ADMITTED"
            and bool(required_lifecycles)
            and all(value == "COMPLETED" for value in required_lifecycles)
        )
    elif branch == "ZERO_PARSE_DENOMINATOR":
        valid = (
            projection.get("status") == "BLOCKED_NO_ACCEPTED_PRODUCTS"
            and denominator == []
            and accepted == []
            and source.get("fact_set") is None
            and whole.get("parent_eligibility") == "ADMITTED"
        )
    elif branch == "ALL_PARSE_REJECTED":
        valid = (
            projection.get("status") == "BLOCKED_NO_ACCEPTED_PRODUCTS"
            and bool(denominator)
            and accepted == []
            and source.get("fact_set") is None
            and whole.get("parent_eligibility") == "ADMITTED"
        )
    elif branch == "PROJECTION_BLOCKED":
        valid = (
            projection.get("status") == "BLOCKED_UNREPRESENTABLE"
            and source.get("fact_set") is None
            and whole.get("parent_eligibility") == "ADMITTED"
        )
    else:
        valid = (
            projection.get("status") == "QUALIFIED"
            and source.get("fact_set") is None
            and whole.get("parent_eligibility") == "REVOKED"
            and any(
                value in {"FAILED", "UNAVAILABLE", "INFRASTRUCTURE_FAILED"}
                for value in required_lifecycles
            )
        )
    if not valid:
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.BRANCH_RECONCILIATION_REJECTED,
            "terminal branch disagrees with Fact history",
        )
    return branch


class OwnedPostTerminalFactDualSuccessor:
    """Pre-terminal Fact application plus one post-terminal shared route slot."""

    def __init__(
        self,
        consumer: OwnedProductFactConsumer,
        slot: _SharedConsumeSlot,
        sealed: Mapping[str, object],
        continuity_capture_slot: object,
        *,
        _token: object,
    ) -> None:
        if (
            _token is not _SELECTOR_TOKEN
            or type(consumer) is not OwnedProductFactConsumer
            or type(slot) is not _SharedConsumeSlot
            or sealed.get("consumer") is not consumer
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.INPUT_REJECTED,
                "dual-successor selector is not constructible",
            )
        self.__consumer = consumer
        self.__bound_consumer = consumer
        self.__slot = slot
        self.__bound_slot = slot
        self.__continuity_capture_slot = continuity_capture_slot
        self.__bound_continuity_capture_slot = continuity_capture_slot
        self.__attempt = sealed["attempt"]
        self.__inputs = sealed["inputs"]
        self.__context = sealed["context"]
        self.__classification = sealed["classification"]
        self.__continuation = sealed["continuation"]
        self.__product_set = sealed["product_set"]
        self.__eligibility = sealed["eligibility"]
        self.__bindings = sealed["bindings"]
        self.__required = copy.deepcopy(sealed["required"])
        self.__required_bytes = canonical_json_bytes(self.__required)
        self.__bound_required_bytes = self.__required_bytes
        self.__qualification_bytes = memoryview(
            sealed["qualification_bytes"]
        ).tobytes()
        self.__bound_qualification_bytes = self.__qualification_bytes
        self.__static_bytes = memoryview(sealed["static_bytes"]).tobytes()
        self.__bound_static_bytes = self.__static_bytes
        self.__transport_limits = sealed["transport_limits"]
        self.__cancellation_requested = sealed["cancellation_requested"]
        if (
            type(self.__inputs) is not DerivationInputSet
            or type(self.__context) is not BudgetContext
            or type(self.__classification) is not OwnedLanguageSupportClassification
            or type(self.__transport_limits)
            is not ExecutionCellTransportSafetyLimits
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.INPUT_REJECTED,
                "dual-successor sealed object graph is invalid",
            )
        self.__canonical_bytes = tuple(
            getattr(self.__inputs, name) for name in _CANONICAL_FIELDS
        )
        self.__digests = tuple(
            getattr(self.__inputs, name) for name in _DIGEST_FIELDS
        )
        self.__blob_bytes = _copy_blob_map(self.__inputs)
        self.__input_seal = _input_state_seal(self.__inputs)
        self.__classification_bytes = canonical_json_bytes(
            self.__classification.classification_document_copy()
        )
        self.__product_set_bytes = canonical_json_bytes(
            self.__product_set.product_set_document_copy()
        )
        self.__binding_bytes = canonical_json_bytes(
            [
                {
                    "descriptor": binding.descriptor.document(),
                    "launch_key": binding.launch_key,
                }
                for binding in self.__bindings
            ]
        )
        self.__terminal_closure: OwnedProductFactClosure | None = None
        self.__bound_terminal_closure: OwnedProductFactClosure | None = None
        self.__terminal_source_bytes: bytes | None = None
        self.__bound_terminal_source_bytes: bytes | None = None
        self.__branch: str | None = None
        self.__route: str | None = None
        self.__continuity_capture_slot._bind_selector(self, consumer)
        self.__validate_sealed_graph()

    def __copy__(self):
        self.__revoke(DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED)
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
            "dual-successor authority cannot be copied",
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()

    @property
    def state(self) -> DualSuccessorState:
        with self.__slot.lock:
            return self.__slot.state

    def claims(self) -> tuple[OwnedProductFactClaim, ...]:
        self.__validate_sealed_graph()
        return self.__consumer.claims()

    @property
    def scheduling_status(self) -> str:
        self.__validate_sealed_graph()
        return self.__consumer.scheduling_status

    def qualification_copy(self) -> dict[str, object]:
        self.__validate_sealed_graph()
        return self.__consumer.qualification_copy()

    def reconcile(
        self, observations: Sequence[OwnedProductFactObservation]
    ) -> OwnedProductFactClosure:
        try:
            closure = self.__consumer.reconcile(observations)
        except Exception as exc:
            self.__revoke(DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED)
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                "terminal Fact reconciliation failed closed",
            ) from exc
        with self.__slot.lock:
            if self.__slot.state is DualSuccessorState.REVOKED:
                return closure
            if self.__slot.state is not DualSuccessorState.SEALED_NOT_ROUTABLE:
                self.__revoke_locked(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED
                )
                raise self.__error_locked("terminal reconciliation was replayed")
            try:
                values = self.__terminal_tuple(closure)
                source = values[0]
                branch = _validate_terminal_branch_semantics(source)
                route = _selector_route_for_source(source)
                if not _application_route_matches(branch, route):
                    raise PostTerminalDualSuccessorError(
                        DualSuccessorFailureFamily.BRANCH_RECONCILIATION_REJECTED,
                        "application route reconciliation failed",
                    )
                source_bytes = canonical_json_bytes(source)
                self.__terminal_closure = closure
                self.__bound_terminal_closure = closure
                self.__terminal_source_bytes = source_bytes
                self.__bound_terminal_source_bytes = source_bytes
                self.__branch = branch
                self.__route = route
                self.__slot.route = route
                self.__slot.state = DualSuccessorState.TERMINAL_READY
                self.__continuity_capture_slot._capture_terminal_source(
                    selector=self,
                    closure=closure,
                    source=source,
                    branch=branch,
                    route=route,
                )
                return closure
            except PostTerminalDualSuccessorError as exc:
                self.__revoke_locked(exc.failure_family)
                raise
            except Exception as exc:
                self.__revoke_locked(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED
                )
                raise PostTerminalDualSuccessorError(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                    "terminal Fact source failed closed",
                ) from exc

    def claim_relation(
        self,
        *,
        handoff_domain: str = HANDOFF_DOMAIN,
        route_selection_function: str = ROUTE_SELECTION_FUNCTION,
        claim_function: str = CLAIM_FUNCTION,
    ) -> "ClaimedPostTerminalRelationSource":
        claimed = self.__claim_route(
            RELATION_ROUTE,
            handoff_domain=handoff_domain,
            route_selection_function=route_selection_function,
            claim_function=claim_function,
        )
        try:
            return ClaimedPostTerminalRelationSource(
                self, *claimed, _token=_RELATION_CARRIER_TOKEN
            )
        except Exception as exc:
            self.__revoke(DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED)
            if isinstance(exc, PostTerminalDualSuccessorError):
                raise
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                "Relation route carrier construction failed",
            ) from exc

    def claim_exact_input(
        self,
        *,
        handoff_domain: str = HANDOFF_DOMAIN,
        route_selection_function: str = ROUTE_SELECTION_FUNCTION,
        claim_function: str = CLAIM_FUNCTION,
    ):
        claimed = self.__claim_route(
            EXACT_INPUT_ROUTE,
            handoff_domain=handoff_domain,
            route_selection_function=route_selection_function,
            claim_function=claim_function,
        )
        claim_id, source, context, inputs, _classification, _limits, _cancel = claimed
        try:
            from veritrail_review._fact_to_coverage_exact_input_handoff import (
                _claim_fact_to_coverage_exact_input_from_post_terminal,
            )

            closure = self.__terminal_closure
            if type(closure) is not OwnedProductFactClosure:
                raise PostTerminalDualSuccessorError(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                    "terminal closure identity is unavailable",
                )
            return _claim_fact_to_coverage_exact_input_from_post_terminal(
                source=source,
                inputs=inputs,
                context=context,
                closure=closure,
                claim_id=claim_id,
                route_validator=lambda: self._validate_claimed_route(
                    EXACT_INPUT_ROUTE, claim_id
                )[:3],
                route_revoker=self._revoke_from_exact_input_handoff,
                route_replay_revoker=self._revoke_from_exact_input_replay,
                application_origin_validator=lambda: (
                    self._application_output_admission_origin(
                        EXACT_INPUT_ROUTE, claim_id
                    )
                ),
            )
        except Exception as exc:
            self.__revoke(DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED)
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                "exact-input route carrier construction failed",
            ) from exc

    def __claim_route(
        self,
        route: str,
        *,
        handoff_domain: str,
        route_selection_function: str,
        claim_function: str,
    ) -> tuple[
        str,
        dict[str, object],
        BudgetContext,
        DerivationInputSet,
        OwnedLanguageSupportClassification,
        ExecutionCellTransportSafetyLimits,
        Callable[[], bool] | None,
    ]:
        with self.__slot.lock:
            if self.__slot.state is DualSuccessorState.SEALED_NOT_ROUTABLE:
                self.__revoke_locked(
                    DualSuccessorFailureFamily.PRE_TERMINAL_CLAIM_REJECTED
                )
                raise self.__error_locked("route claim preceded terminal Fact closure")
            if self.__slot.state is DualSuccessorState.REVOKED:
                raise self.__error_locked("dual-successor route authority is revoked")
            if self.__slot.state in {
                DualSuccessorState.CLAIMED_RELATION,
                DualSuccessorState.CLAIMED_EXACT_INPUT,
            }:
                self.__revoke_locked(
                    DualSuccessorFailureFamily.ALREADY_CONSUMED
                )
                raise self.__error_locked(
                    "dual-successor route was already consumed"
                )
            if self.__slot.state is not DualSuccessorState.TERMINAL_READY:
                self.__revoke_locked(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED
                )
                raise self.__error_locked("terminal route state is invalid")
            if (
                type(handoff_domain) is not str
                or type(route_selection_function) is not str
                or type(claim_function) is not str
                or handoff_domain != HANDOFF_DOMAIN
                or route_selection_function != ROUTE_SELECTION_FUNCTION
                or claim_function != CLAIM_FUNCTION
            ):
                self.__revoke_locked(DualSuccessorFailureFamily.INPUT_REJECTED)
                raise self.__error_locked("dual-successor version is not supported")
            try:
                values = self.__terminal_tuple(self.__terminal_closure)
                source = values[0]
                branch = _validate_terminal_branch_semantics(source)
                selected = _selector_route_for_source(source)
                if (
                    selected != self.__route
                    or branch != self.__branch
                    or not _application_route_matches(branch, selected)
                ):
                    raise PostTerminalDualSuccessorError(
                        DualSuccessorFailureFamily.BRANCH_RECONCILIATION_REJECTED,
                        "terminal route changed",
                    )
                if route != selected:
                    raise PostTerminalDualSuccessorError(
                        DualSuccessorFailureFamily.WRONG_ROUTE_REJECTED,
                        "requested route does not own the terminal branch",
                    )
                if canonical_json_bytes(source) != self.__terminal_source_bytes:
                    raise PostTerminalDualSuccessorError(
                        DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                        "terminal source bytes changed",
                    )
                claim_id = semantic_digest(
                    "veritrail.review.post-terminal-dual-successor-claim/0.1",
                    {"nonce": uuid4().hex},
                )
                self.__slot.claim_id = claim_id
                self.__slot.route = route
                self.__slot.state = (
                    DualSuccessorState.CLAIMED_RELATION
                    if route == RELATION_ROUTE
                    else DualSuccessorState.CLAIMED_EXACT_INPUT
                )
                return (claim_id, *values)
            except PostTerminalDualSuccessorError as exc:
                self.__revoke_locked(exc.failure_family)
                raise
            except Exception as exc:
                self.__revoke_locked(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED
                )
                raise PostTerminalDualSuccessorError(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                    "dual-successor route validation failed",
                ) from exc

    def _validate_claimed_route(
        self, route: str, claim_id: str
    ) -> tuple[
        dict[str, object],
        BudgetContext,
        DerivationInputSet,
        OwnedLanguageSupportClassification,
        ExecutionCellTransportSafetyLimits,
        Callable[[], bool] | None,
    ]:
        with self.__slot.lock:
            expected_state = (
                DualSuccessorState.CLAIMED_RELATION
                if route == RELATION_ROUTE
                else DualSuccessorState.CLAIMED_EXACT_INPUT
            )
            if (
                self.__slot.state is not expected_state
                or self.__slot.route != route
                or self.__slot.claim_id != claim_id
                or type(claim_id) is not str
                or not claim_id
            ):
                self.__revoke_locked(
                    DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED
                )
                raise self.__error_locked("claimed route identity changed")
            try:
                values = self.__terminal_tuple(self.__terminal_closure)
                source = values[0]
                branch = _validate_terminal_branch_semantics(source)
                if (
                    canonical_json_bytes(source) != self.__terminal_source_bytes
                    or _selector_route_for_source(source) != route
                    or not _application_route_matches(branch, route)
                ):
                    raise PostTerminalDualSuccessorError(
                        DualSuccessorFailureFamily.BRANCH_RECONCILIATION_REJECTED,
                        "claimed route no longer matches terminal Fact truth",
                    )
                return values
            except PostTerminalDualSuccessorError as exc:
                self.__revoke_locked(exc.failure_family)
                raise
            except Exception as exc:
                self.__revoke_locked(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED
                )
                raise PostTerminalDualSuccessorError(
                    DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
                    "claimed route terminal source changed",
                ) from exc

    def _application_output_admission_origin(
        self, route: str, claim_id: str
    ) -> tuple[
        "OwnedPostTerminalFactDualSuccessor",
        OwnedProductFactClosure,
        object,
        object,
    ]:
        self._validate_claimed_route(route, claim_id)
        if type(self.__terminal_closure) is not OwnedProductFactClosure:
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
                "terminal closure identity is unavailable",
            )
        return (
            self,
            self.__terminal_closure,
            self.__attempt,
            self.__eligibility,
        )

    def __terminal_tuple(self, closure):
        self.__validate_sealed_graph()
        if (
            type(closure) is not OwnedProductFactClosure
            or (
                self.__bound_terminal_closure is not None
                and closure is not self.__bound_terminal_closure
            )
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
                "foreign or copied terminal closure",
            )
        values = self.__consumer._post_terminal_dual_successor_terminal_source(
            closure, self.__slot
        )
        source, context, inputs, classification, limits, cancellation = values
        if (
            context is not self.__context
            or inputs is not self.__inputs
            or classification is not self.__classification
            or limits is not self.__transport_limits
            or cancellation is not self.__cancellation_requested
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
                "terminal source left the original object graph",
            )
        return values

    def __validate_sealed_graph(self) -> None:
        try:
            if (
                self.__consumer is not self.__bound_consumer
                or self.__slot is not self.__bound_slot
                or self.__continuity_capture_slot
                is not self.__bound_continuity_capture_slot
                or type(self.__inputs) is not DerivationInputSet
                or type(self.__context) is not BudgetContext
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or not self.__context.checkpoint()
                or _input_state_seal(self.__inputs) != self.__input_seal
                or tuple(
                    getattr(self.__inputs, name) for name in _CANONICAL_FIELDS
                )
                != self.__canonical_bytes
                or tuple(getattr(self.__inputs, name) for name in _DIGEST_FIELDS)
                != self.__digests
                or _copy_blob_map(self.__inputs) != self.__blob_bytes
                or canonical_json_bytes(
                    self.__classification.classification_document_copy()
                )
                != self.__classification_bytes
                or canonical_json_bytes(
                    self.__product_set.product_set_document_copy()
                )
                != self.__product_set_bytes
                or canonical_json_bytes(
                    [
                        {
                            "descriptor": binding.descriptor.document(),
                            "launch_key": binding.launch_key,
                        }
                        for binding in self.__bindings
                    ]
                )
                != self.__binding_bytes
                or self.__required_bytes is not self.__bound_required_bytes
                or canonical_json_bytes(self.__required) != self.__required_bytes
                or self.__qualification_bytes
                is not self.__bound_qualification_bytes
                or self.__static_bytes is not self.__bound_static_bytes
            ):
                raise ValueError
        except PostTerminalDualSuccessorError:
            raise
        except Exception as exc:
            family = (
                DualSuccessorFailureFamily.CONTEXT_REVOKED
                if type(self.__context) is BudgetContext
                and (
                    self.__context.state is not BudgetState.RUNNING
                    or self.__context.stop_trigger is not None
                )
                else DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED
            )
            raise PostTerminalDualSuccessorError(
                family, "sealed dual-successor object graph changed"
            ) from exc

    def __revoke(self, family: DualSuccessorFailureFamily) -> None:
        with self.__slot.lock:
            self.__revoke_locked(family)

    def __revoke_locked(self, family: DualSuccessorFailureFamily) -> None:
        if self.__slot.failure_family is None:
            self.__slot.failure_family = family
        self.__slot.state = DualSuccessorState.REVOKED
        try:
            from veritrail_review._same_attempt_derivation_evidence_continuity import (
                EvidenceContinuityFailureFamily,
            )

            self.__bound_continuity_capture_slot._revoke(
                EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
            )
        except Exception:
            pass

    def __error_locked(self, message: str) -> PostTerminalDualSuccessorError:
        return PostTerminalDualSuccessorError(
            self.__slot.failure_family
            or DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED,
            message,
        )

    def _revoke_from_relation_transition(self) -> None:
        self.__revoke(DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED)

    def _revoke_from_exact_input_handoff(self) -> None:
        self.__revoke(DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED)

    def _revoke_from_exact_input_replay(self) -> None:
        self.__revoke(DualSuccessorFailureFamily.ALREADY_CONSUMED)

    def _revoke_for_failure(
        self, family: DualSuccessorFailureFamily
    ) -> None:
        if type(family) is not DualSuccessorFailureFamily:
            family = DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED
        self.__revoke(family)

    def _bind_same_attempt_continuity_application(
        self,
        *,
        route_claim: object,
        claim_id: str,
        source: Mapping[str, object],
        inputs: DerivationInputSet,
        context: BudgetContext,
        closure: OwnedProductFactClosure,
        fact_attempt: object,
        eligibility: object,
        route: str,
    ):
        self._validate_claimed_route(route, claim_id)
        return self.__continuity_capture_slot._bind_application_route(
            selector=self,
            route_claim=route_claim,
            claim_id=claim_id,
            source=source,
            inputs=inputs,
            context=context,
            closure=closure,
            fact_attempt=fact_attempt,
            eligibility=eligibility,
            route=route,
        )

    def _capture_same_attempt_continuity_transition(
        self, route_claim: object, admission: object
    ) -> None:
        self.__continuity_capture_slot._capture_normal_transition(
            selector=self,
            route_claim=route_claim,
            admission=admission,
        )


class ClaimedPostTerminalRelationSource:
    """Route-specific normal-world carrier; it owns no Relation result."""

    def __init__(
        self,
        selector: OwnedPostTerminalFactDualSuccessor,
        claim_id: str,
        source: Mapping[str, object],
        context: BudgetContext,
        inputs: DerivationInputSet,
        classification: OwnedLanguageSupportClassification,
        transport_limits: ExecutionCellTransportSafetyLimits,
        cancellation_requested: Callable[[], bool] | None,
        *,
        _token: object,
    ) -> None:
        if (
            _token is not _RELATION_CARRIER_TOKEN
            or type(selector) is not OwnedPostTerminalFactDualSuccessor
            or type(claim_id) is not str
            or not claim_id
            or source.get("branch") != "NORMAL_FULFILLED"
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.INPUT_REJECTED,
                "Relation route carrier is not constructible",
            )
        self.__selector = selector
        self.__bound_selector = selector
        self.__claim_id = claim_id
        self.__bound_claim_id = claim_id
        self.__source_bytes = canonical_json_bytes(dict(source))
        self.__bound_source_bytes = self.__source_bytes
        self.__context = context
        self.__bound_context = context
        self.__inputs = inputs
        self.__bound_inputs = inputs
        self.__classification = classification
        self.__bound_classification = classification
        self.__transport_limits = transport_limits
        self.__bound_transport_limits = transport_limits
        self.__cancellation_requested = cancellation_requested
        self.__bound_cancellation_requested = cancellation_requested
        self.__transition_lock = Lock()
        self.__transition_started = False
        self.__application_output_bound = False
        self.__document_bytes = canonical_json_bytes(
            {
                "handoff_domain": HANDOFF_DOMAIN,
                "route_selection_function": ROUTE_SELECTION_FUNCTION,
                "claim_function": CLAIM_FUNCTION,
                "route": RELATION_ROUTE,
                "terminal_branch": "NORMAL_FULFILLED",
                "claim_id": claim_id,
                "terminal_source_sha256": hashlib.sha256(
                    self.__source_bytes
                ).hexdigest(),
                "authority_ceiling": {
                    "post_terminal_relation_handoff_claim": True,
                    "post_terminal_exact_input_claim": False,
                    "relation_set": False,
                    "review_slice_set": False,
                    "coverage_ledger": False,
                    "global_composition_admission": False,
                    "manifest": False,
                    "evidence": False,
                    "persistence": False,
                    "public_review": False,
                    "r2_r6": False,
                },
            }
        )
        self.__bound_document_bytes = self.__document_bytes
        self._validate_relation_claim_for_admission()

    def __copy__(self):
        self.__selector._revoke_for_failure(
            DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED
        )
        raise PostTerminalDualSuccessorError(
            DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
            "Relation route authority cannot be copied",
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()

    def document_copy(self) -> dict[str, object]:
        self._validate_relation_claim_for_admission()
        return json.loads(self.__document_bytes)

    def _claim_transition_source(self):
        with self.__transition_lock:
            if self.__transition_started:
                self.__selector._revoke_for_failure(
                    DualSuccessorFailureFamily.ALREADY_CONSUMED
                )
                raise PostTerminalDualSuccessorError(
                    DualSuccessorFailureFamily.ALREADY_CONSUMED,
                    "Relation transition already consumed this route carrier",
                )
            values = self._validate_relation_claim_for_admission()
            self.__transition_started = True
            return values

    def _validate_relation_claim_for_admission(self):
        try:
            return self.__validate_relation_claim_for_admission()
        except Exception:
            self.__selector._revoke_for_failure(
                DualSuccessorFailureFamily.TERMINAL_SOURCE_REJECTED
            )
            raise

    def __validate_relation_claim_for_admission(self):
        if (
            self.__selector is not self.__bound_selector
            or self.__claim_id != self.__bound_claim_id
            or self.__source_bytes is not self.__bound_source_bytes
            or self.__document_bytes is not self.__bound_document_bytes
            or self.__context is not self.__bound_context
            or self.__inputs is not self.__bound_inputs
            or self.__classification is not self.__bound_classification
            or self.__transport_limits is not self.__bound_transport_limits
            or self.__cancellation_requested
            is not self.__bound_cancellation_requested
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
                "Relation route carrier identity changed",
            )
        values = self.__selector._validate_claimed_route(
            RELATION_ROUTE, self.__claim_id
        )
        source, context, inputs, classification, limits, cancellation = values
        if (
            canonical_json_bytes(source) != self.__source_bytes
            or context is not self.__context
            or inputs is not self.__inputs
            or classification is not self.__classification
            or limits is not self.__transport_limits
            or cancellation is not self.__cancellation_requested
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
                "Relation route carrier left the original attempt",
            )
        document = json.loads(self.__document_bytes)
        if (
            document.get("route") != RELATION_ROUTE
            or document.get("terminal_branch") != "NORMAL_FULFILLED"
            or any(
                document["authority_ceiling"][key] is not False
                for key in (
                    "post_terminal_exact_input_claim",
                    "relation_set",
                    "review_slice_set",
                    "coverage_ledger",
                    "global_composition_admission",
                    "manifest",
                    "evidence",
                    "persistence",
                    "public_review",
                    "r2_r6",
                )
            )
        ):
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.INPUT_REJECTED,
                "Relation route authority ceiling changed",
            )
        return values

    def _revoke_from_relation_transition(self) -> None:
        self.__selector._revoke_from_relation_transition()

    def _capture_same_attempt_continuity_transition(self, admission: object) -> None:
        self.__selector._capture_same_attempt_continuity_transition(self, admission)

    def _application_output_admission_coordinates(self):
        """Return the exact live route world to the sibling private owner."""

        if not self.__application_output_bound:
            raise PostTerminalDualSuccessorError(
                DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED,
                "Relation route has no application output owner",
            )
        values = self._validate_relation_claim_for_admission()
        origin = self.__selector._application_output_admission_origin(
            RELATION_ROUTE, self.__claim_id
        )
        source, context, inputs, classification, limits, cancellation = values
        return (
            self,
            self.__selector,
            self.__claim_id,
            source,
            context,
            inputs,
            classification,
            limits,
            cancellation,
            *origin[1:],
        )

    def _bind_application_output_admission(self):
        with self.__transition_lock:
            if self.__application_output_bound or self.__transition_started:
                self.__selector._revoke_for_failure(
                    DualSuccessorFailureFamily.ALREADY_CONSUMED
                )
                raise PostTerminalDualSuccessorError(
                    DualSuccessorFailureFamily.ALREADY_CONSUMED,
                    "Relation route cannot bind another or late application owner",
                )
            values = self._validate_relation_claim_for_admission()
            origin = self.__selector._application_output_admission_origin(
                RELATION_ROUTE, self.__claim_id
            )
            self.__application_output_bound = True
            source, context, inputs, classification, limits, cancellation = values
            return (
                self,
                self.__selector,
                self.__claim_id,
                source,
                context,
                inputs,
                classification,
                limits,
                cancellation,
                *origin[1:],
            )

    def _revoke_from_application_output_admission(self) -> None:
        self.__selector._revoke_for_failure(
            DualSuccessorFailureFamily.SAME_ATTEMPT_REJECTED
        )


def create_post_terminal_fact_dual_successor_consumer(
    closure: OwnedParseFulfillmentClosure,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
    cancellation_requested: Callable[[], bool] | None = None,
) -> OwnedPostTerminalFactDualSuccessor:
    """Create the exact new-domain Fact consumer and its sealed shared slot."""

    from veritrail_review._same_attempt_derivation_evidence_continuity import (
        _create_same_attempt_continuity_capture_slot,
    )

    slot = _SharedConsumeSlot()
    continuity_capture_slot = _create_same_attempt_continuity_capture_slot()
    consumer = _create_product_fact_consumer(
        closure,
        derivation_id=derivation_id,
        bindings=bindings,
        transport_limits=transport_limits,
        cancellation_requested=cancellation_requested,
        applicability_admitter=_admit_relation_transition_fact_applicability,
        handoff_domain=HANDOFF_DOMAIN,
        post_terminal_dual_successor_slot=slot,
        continuity_capture_slot=continuity_capture_slot,
    )
    sealed = consumer._post_terminal_dual_successor_sealed_state(slot)
    return OwnedPostTerminalFactDualSuccessor(
        consumer,
        slot,
        sealed,
        continuity_capture_slot,
        _token=_SELECTOR_TOKEN,
    )
