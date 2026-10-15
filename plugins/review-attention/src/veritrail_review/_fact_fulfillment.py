from __future__ import annotations

import hashlib
import io
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from threading import Lock
from typing import Callable, Mapping, Sequence
from uuid import uuid4

from veritrail_review._execution_cell import DEFAULT_TRANSPORT_LIMITS
from veritrail_review._execution_cell_binding import ProviderBinding
from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    FrameProtocolError,
    encode_frame,
    read_frame,
)
from veritrail_review._execution_cell_values import ProviderRunStatus
from veritrail_review._language_support import (
    _revalidate_exact_inputs,
    classify_language_support,
)
from veritrail_review._fact_fulfillment_binding import _admit_closed_applicability
from veritrail_review._fact_fulfillment_projection import qualify
from veritrail_review._multi_provider_fact_composition import (
    _fact_set_document,
    _merge_completed_sources,
)
from veritrail_review._parse_fulfillment import (
    ClaimedParseContinuation,
    OwnedParseFulfillmentClosure,
)
from veritrail_review._parse_product_fact_anchors import product_byte_anchors
from veritrail_review._fact_fulfillment_protocol import (
    CONSUMER_FUNCTION,
    ProductFactProtocolError,
    admit_terminal,
    build_request,
    validate_projection,
)
from veritrail_review._source_operation_gate import _input_state_seal
from veritrail_review._windows_execution_cell import (
    CellPreparationError,
    CellReleaseError,
    CellRuntimeUnavailableError,
    run_windows_execution_cell,
)
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.errors import BudgetPrimitiveError


_PARENT_TOKEN = object()
_CLAIM_TOKEN = object()
_CLAIMED_TOKEN = object()
_OBSERVATION_TOKEN = object()
_CLOSURE_TOKEN = object()
_CONTINUATION_TOKEN = object()


class ProductFactConsumerError(ValueError):
    """The private post-Parse consumer lost authority or complete reconciliation."""


def _observation_seal(binding, lifecycle, facts, terminal, frame, execution) -> str:
    return semantic_digest(
        "veritrail.review.private-product-fact-observation/0.2",
        {
            "binding": binding.descriptor.document(),
            "launch_key": binding.launch_key,
            "lifecycle": lifecycle,
            "execution_sha256": (
                None if execution is None else hashlib.sha256(execution).hexdigest()
            ),
            "fact_sha256": [hashlib.sha256(item).hexdigest() for item in facts],
            "terminal_sha256": (
                None if terminal is None else hashlib.sha256(terminal).hexdigest()
            ),
            "frame_sha256": (
                None if frame is None else hashlib.sha256(frame).hexdigest()
            ),
        },
    )


@dataclass(frozen=True)
class OwnedProductFactObservation:
    binding: ProviderBinding
    lifecycle: str
    canonical_fact_bytes: tuple[bytes, ...]
    terminal_bytes: bytes | None = field(repr=False)
    terminal_frame_bytes: bytes | None = field(repr=False)
    _parent: object = field(repr=False, compare=False)
    _claim: object = field(repr=False, compare=False)
    _seal: str = field(repr=False, compare=False)
    _token: object = field(repr=False, compare=False)
    execution_bytes: bytes | None = field(default=None, repr=False)
    _bound_parent: object = field(init=False, repr=False, compare=False)
    _bound_claim: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _OBSERVATION_TOKEN:
            raise ProductFactConsumerError("observation is not constructible")
        object.__setattr__(self, "_bound_parent", self._parent)
        object.__setattr__(self, "_bound_claim", self._claim)

    @property
    def provider_run_status(self) -> ProviderRunStatus:
        return {
            "COMPLETED": ProviderRunStatus.COMPLETED,
            "FAILED": ProviderRunStatus.FAILED,
            "UNAVAILABLE": ProviderRunStatus.UNAVAILABLE,
            "INFRASTRUCTURE_FAILED": ProviderRunStatus.FAILED,
            "RELEASE_FAILED": ProviderRunStatus.FAILED,
            "INTERRUPTED": ProviderRunStatus.INTERRUPTED,
        }[self.lifecycle]

    @property
    def phase(self) -> "OwnedProductFactObservation":
        """Structural adapter for the existing private Fact composition function."""
        return self

    def _validate(self) -> None:
        if (
            self._parent is not self._bound_parent
            or self._claim is not self._bound_claim
            or self._token is not _OBSERVATION_TOKEN
            or self._seal
            != _observation_seal(
                self.binding,
                self.lifecycle,
                self.canonical_fact_bytes,
                self.terminal_bytes,
                self.terminal_frame_bytes,
                self.execution_bytes,
            )
        ):
            raise ProductFactConsumerError("consumer observation changed")
        self.provider_run_status
        if self.lifecycle != "COMPLETED" and self.canonical_fact_bytes:
            raise ProductFactConsumerError("non-success child retained Facts")
        if self.lifecycle == "COMPLETED":
            if self.execution_bytes is None or self.terminal_frame_bytes is None:
                raise ProductFactConsumerError("completion has no execution witness")
            receipt = json.loads(self.execution_bytes)
            if (
                any(
                    receipt[k] is not True
                    for k in (
                        "admitted",
                        "process_created_suspended",
                        "process_assigned_before_resume",
                        "process_resumed",
                        "active_process_zero",
                        "handles_released",
                        "channel_threads_released",
                    )
                )
                or any(
                    receipt[k] is not False
                    for k in (
                        "request_channel_failed",
                        "result_channel_failed",
                        "result_transport_exceeded",
                    )
                )
                or receipt["root_exit_code"] != 0
                or receipt["stop_trigger"] is not None
                or receipt["admission_callbacks"] != 1
                or receipt["terminal_bytes"]
                != hashlib.sha256(self.terminal_frame_bytes).hexdigest()
            ):
                raise ProductFactConsumerError("completion lost truthful lifecycle")


class OwnedProductFactConsumer:
    """One original Parse attempt; complete application-owned Provider membership."""

    def __init__(
        self,
        continuation: ClaimedParseContinuation,
        *,
        derivation_id: str,
        bindings: tuple[ProviderBinding, ...],
        required: Mapping[str, bool],
        transport_limits: ExecutionCellTransportSafetyLimits,
        cancellation_requested: Callable[[], bool] | None,
        _token: object,
    ) -> None:
        if _token is not _PARENT_TOKEN:
            raise ProductFactConsumerError("consumer is not constructible")
        self.__continuation = continuation
        self.__bound_continuation = continuation
        self.__attempt = continuation._attempt_ref()
        self.__bound_attempt = self.__attempt
        self.__inputs = self.__attempt._inputs_ref()
        self.__bound_inputs = self.__inputs
        self.__input_seal = _input_state_seal(self.__inputs)
        self.__context = self.__attempt._context_ref()
        self.__bound_context = self.__context
        self.__budget_identity = (
            self.__context.limits,
            self.__context.started_at_monotonic,
            self.__context.execution_deadline_monotonic,
        )
        self.__eligibility = self.__attempt._parent_eligibility_ref()
        self.__bound_eligibility = self.__eligibility
        self.__product_set = continuation._product_set()
        self.__bound_product_set = self.__product_set
        self.__classification = self.__attempt._classification_ref()
        self.__bound_classification = self.__classification
        self.__derivation_id = derivation_id
        self.__attempt_id = semantic_digest(
            "veritrail.review.private-product-fact-attempt/0.2", {"nonce": uuid4().hex}
        )
        self.__bindings = bindings
        self.__bound_bindings = bindings
        self.__required = dict(required)
        self.__transport_limits = transport_limits
        self.__cancellation_requested = cancellation_requested
        self.__bound_cancellation_requested = cancellation_requested
        self.__lock = Lock()
        self.__reconciled = False
        self.__closure = None
        self.__bound_static = canonical_json_bytes(
            {
                "derivation_id": derivation_id,
                "consumer_attempt_id": self.__attempt_id,
                "bindings": [
                    {
                        "descriptor": binding.descriptor.document(),
                        "launch_key": binding.launch_key,
                    }
                    for binding in bindings
                ],
                "required": self.__required,
                "transport_limits": {
                    "request_payload_bytes": transport_limits.request_payload_bytes,
                    "terminal_payload_bytes": transport_limits.terminal_payload_bytes,
                },
            }
        )
        self.__reconciliation_history = ()
        self.__execution_history = ()
        self.__qualification = (
            canonical_json_bytes(qualify(self._projection(bindings[0])))
            if self.__product_set.accepted_count
            else canonical_json_bytes(
                {
                    "function": "r1-fact-projection-fulfillment/0.1",
                    "status": "BLOCKED_NO_ACCEPTED_PRODUCTS",
                    "universe": [],
                    "expected": [],
                    "parse_partition": self.__product_set.product_set_document_copy(),
                }
            )
        )
        self.__bound_qualification = self.__qualification
        self.__claims = (
            tuple(
                OwnedProductFactClaim(
                    self, binding, self._projection(binding), _token=_CLAIM_TOKEN
                )
                for binding in bindings
            )
            if self.__product_set.accepted_count
            and json.loads(self.__qualification)["status"] == "QUALIFIED"
            else ()
        )
        self.__bound_claims = self.__claims
        self._validate_live()

    @property
    def scheduling_status(self) -> str:
        self._validate_live()
        status = json.loads(self.__qualification)["status"]
        return "ELIGIBLE" if status == "QUALIFIED" else status

    def qualification_copy(self):
        if self.__qualification is not self.__bound_qualification:
            raise ProductFactConsumerError("application projection changed")
        return json.loads(self.__qualification)

    def retained_observations(self):
        return self.__execution_history

    def reconciliation_observations(self):
        return self.__reconciliation_history

    def _record_observation(self, observation):
        observation._validate()
        with self.__lock:
            if (
                observation._parent is not self
                or not any(c is observation._claim for c in self.__claims)
                or any(o._claim is observation._claim for o in self.__execution_history)
            ):
                raise ProductFactConsumerError(
                    "foreign or duplicate execution observation"
                )
            self.__execution_history += (observation,)

    def claims(self) -> tuple["OwnedProductFactClaim", ...]:
        self._validate_live()
        return self.__claims

    def _projection(self, binding: ProviderBinding) -> dict[str, object]:
        products = self.__product_set.products_copy()
        subjects = {
            s["subject_identity"]: s for s in self.__classification.subjects_copy()
        }
        members = []
        for accepted in self.__product_set.product_set_document_copy()["accepted"]:
            subject = subjects[accepted["subject_identity"]]
            inventory = subject["semantic_input"]["inventory_item"]
            raw = self.__inputs.verified_blob_bytes_by_object_identity[
                inventory["git_object"]["hex"]
            ]
            if (
                type(raw) is not bytes
                or len(raw) != inventory["content"]["size_bytes"]
                or hashlib.sha256(raw).hexdigest() != inventory["content"]["sha256"]
            ):
                raise ProductFactConsumerError("exact anchor body changed")
            product = products[accepted["subject_identity"]]
            members.append(
                {
                    **accepted,
                    "git_path_hex": inventory["git_path"]["git_path_hex"],
                    "source_size_bytes": len(raw),
                    "product": product,
                    "node_anchors": product_byte_anchors(
                        product, raw, encoding=subject["effective_source_encoding"]
                    ),
                }
            )
        return validate_projection(
            {
                "consumer_function": CONSUMER_FUNCTION,
                "qualification_function": "r1-fact-projection-fulfillment/0.1",
                "python_module_mapping": self.__inputs.review_policy_document_copy()[
                    "python_module_mapping"
                ],
                **{
                    k: getattr(self.__inputs, k)
                    for k in (
                        "source_snapshot_digest",
                        "policy_digest",
                        "analysis_scope_digest",
                        "slice_policy_digest",
                        "derivation_profile_digest",
                    )
                },
                "language_support_function": self.__classification.language_support_function,
                "classification_digest": self.__classification.classification_digest,
                "parse_function": self.__product_set.parse_function,
                "product_set_digest": self.__product_set.product_set_digest,
                "provider_descriptor": binding.descriptor.document(),
                "assigned_products": members,
            }
        )

    def _validate_live(self) -> None:
        try:
            if (
                self.__context is not self.__bound_context
                or (
                    self.__context.limits,
                    self.__context.started_at_monotonic,
                    self.__context.execution_deadline_monotonic,
                )
                != self.__budget_identity
                or self.__eligibility is not self.__bound_eligibility
                or self.__attempt is not self.__bound_attempt
                or self.__inputs is not self.__bound_inputs
                or self.__classification is not self.__bound_classification
                or self.__continuation is not self.__bound_continuation
                or self.__product_set is not self.__bound_product_set
                or self.__continuation._attempt_ref() is not self.__attempt
                or self.__continuation._product_set() is not self.__bound_product_set
                or self.__attempt._inputs_ref() is not self.__inputs
                or self.__attempt._classification_ref() is not self.__classification
                or self.__attempt._context_ref() is not self.__context
                or self.__attempt._parent_eligibility_ref() is not self.__eligibility
                or self.__qualification is not self.__bound_qualification
                or self.__claims is not self.__bound_claims
                or self.__bindings is not self.__bound_bindings
                or self.__cancellation_requested
                is not self.__bound_cancellation_requested
                or _input_state_seal(self.__inputs) != self.__input_seal
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or self.__eligibility.state is not AttemptEligibilityState.ADMITTED
                or not self.__context.checkpoint()
            ):
                raise ValueError
            static = canonical_json_bytes(
                {
                    "derivation_id": self.__derivation_id,
                    "consumer_attempt_id": self.__attempt_id,
                    "bindings": [
                        {
                            "descriptor": binding.descriptor.document(),
                            "launch_key": binding.launch_key,
                        }
                        for binding in self.__bindings
                    ],
                    "required": self.__required,
                    "transport_limits": {
                        "request_payload_bytes": self.__transport_limits.request_payload_bytes,
                        "terminal_payload_bytes": self.__transport_limits.terminal_payload_bytes,
                    },
                }
            )
            if static != self.__bound_static:
                raise ValueError
        except Exception as exc:
            self._revoke()
            raise ProductFactConsumerError(
                "original consumer attempt is no longer live"
            ) from exc

    def _authorize(self, claim: "OwnedProductFactClaim") -> None:
        self._validate_live()
        if not any(c is claim for c in self.__claims):
            raise ProductFactConsumerError("foreign Provider claim")
        claim._validate_bound_state()

    def _request(self, claim: "OwnedProductFactClaim") -> dict[str, object]:
        self._authorize(claim)
        return claim._request_document_copy()

    def _request_from_projection(
        self, projection: Mapping[str, object]
    ) -> dict[str, object]:
        return build_request(
            projection,
            derivation_id=self.__derivation_id,
            consumer_attempt_id=self.__attempt_id,
        )

    def _history_coordinates(self) -> dict[str, object]:
        return {
            "product_set_digest": self.__bound_product_set.product_set_digest,
            "consumer_attempt_id": self.__attempt_id,
            "parse_partition": self.__bound_product_set.product_set_document_copy(),
            "application_projection": self.qualification_copy(),
        }

    def _authorize_continuation(self, closure: "OwnedProductFactClosure") -> None:
        try:
            self._validate_live()
            if (
                closure is not self.__closure
                or closure.document_copy()["consumer_status"] != "COMPLETED"
            ):
                raise ProductFactConsumerError(
                    "foreign or non-success consumer closure"
                )
            closure._validate_child_authority()
        except Exception:
            self._revoke()
            raise

    def _context_ref(self) -> BudgetContext:
        self._validate_live()
        return self.__context

    def _limits_ref(self) -> ExecutionCellTransportSafetyLimits:
        return self.__transport_limits

    def _cancellation_ref(self) -> Callable[[], bool] | None:
        return self.__cancellation_requested

    def _revoke(self) -> None:
        for eligibility in (self.__bound_eligibility, self.__eligibility):
            eligibility.revoke()

    def _handoff_source_document(
        self, closure: "OwnedProductFactClosure"
    ) -> tuple[dict[str, object], BudgetContext]:
        """Revalidate and copy the complete owned Fact-stage history."""

        try:
            if (
                closure is not self.__closure
                or self.__attempt is not self.__bound_attempt
                or self.__inputs is not self.__bound_inputs
                or self.__context is not self.__bound_context
                or self.__eligibility is not self.__bound_eligibility
                or self.__continuation is not self.__bound_continuation
                or self.__product_set is not self.__bound_product_set
                or self.__classification is not self.__bound_classification
                or self.__bindings is not self.__bound_bindings
                or self.__qualification is not self.__bound_qualification
                or self.__claims is not self.__bound_claims
                or self.__cancellation_requested
                is not self.__bound_cancellation_requested
                or _input_state_seal(self.__inputs) != self.__input_seal
                or (
                    self.__context.limits,
                    self.__context.started_at_monotonic,
                    self.__context.execution_deadline_monotonic,
                )
                != self.__budget_identity
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or not self.__context.checkpoint()
                or not self.__reconciled
            ):
                raise ValueError

            static = canonical_json_bytes(
                {
                    "derivation_id": self.__derivation_id,
                    "consumer_attempt_id": self.__attempt_id,
                    "bindings": [
                        {
                            "descriptor": binding.descriptor.document(),
                            "launch_key": binding.launch_key,
                        }
                        for binding in self.__bindings
                    ],
                    "required": self.__required,
                    "transport_limits": {
                        "request_payload_bytes": self.__transport_limits.request_payload_bytes,
                        "terminal_payload_bytes": self.__transport_limits.terminal_payload_bytes,
                    },
                }
            )
            if static != self.__bound_static:
                raise ValueError

            _revalidate_exact_inputs(self.__inputs)
            recomputed_classification = classify_language_support(self.__inputs)
            if (
                recomputed_classification.classification_document_copy()
                != self.__classification.classification_document_copy()
            ):
                raise ValueError

            recomputed_qualification = (
                qualify(self._projection(self.__bindings[0]))
                if self.__product_set.accepted_count
                else {
                    "function": "r1-fact-projection-fulfillment/0.1",
                    "status": "BLOCKED_NO_ACCEPTED_PRODUCTS",
                    "universe": [],
                    "expected": [],
                    "parse_partition": self.__product_set.product_set_document_copy(),
                }
            )
            if canonical_json_bytes(recomputed_qualification) != self.__qualification:
                raise ValueError

            document = closure.document_copy()
            observations = closure._observations_ref()
            if len(observations) != len(self.__reconciliation_history) or any(
                not any(left is right for right in self.__reconciliation_history)
                for left in observations
            ):
                raise ValueError
            if len(observations) != len(self.__execution_history) or any(
                left is not right
                for left, right in zip(observations, self.__execution_history)
            ):
                raise ValueError

            qualification = self.qualification_copy()
            status = document["consumer_status"]
            if any(
                observation.lifecycle in {"RELEASE_FAILED", "INTERRUPTED"}
                for observation in observations
            ):
                raise ProductFactConsumerError(
                    "unsafe or interrupted history has no handoff claim"
                )
            if qualification["status"] != "QUALIFIED":
                if observations or document["fact_set"] is not None:
                    raise ValueError
                expected_parent_state = AttemptEligibilityState.ADMITTED
            elif status == "COMPLETED":
                if document["fact_set"] is None:
                    raise ValueError
                expected_parent_state = AttemptEligibilityState.ADMITTED
            elif status in {"FAILED", "UNAVAILABLE"}:
                if document["fact_set"] is not None:
                    raise ValueError
                expected_parent_state = AttemptEligibilityState.REVOKED
            else:
                raise ValueError
            if self.__eligibility.state is not expected_parent_state:
                raise ValueError
            if expected_parent_state is AttemptEligibilityState.ADMITTED and (
                self.__continuation._attempt_ref() is not self.__attempt
                or self.__continuation._product_set() is not self.__product_set
                or self.__attempt._inputs_ref() is not self.__inputs
                or self.__attempt._classification_ref() is not self.__classification
                or self.__attempt._context_ref() is not self.__context
                or self.__attempt._parent_eligibility_ref() is not self.__eligibility
            ):
                raise ValueError

            for observation in observations:
                observation._validate()
                claim = observation._claim
                claim._validate_bound_state()
                if (
                    observation._parent is not self
                    or not any(candidate is claim for candidate in self.__claims)
                    or not claim._was_consumed()
                    or observation.binding != claim.binding
                ):
                    raise ValueError
                expected_child_state = (
                    AttemptEligibilityState.ADMITTED
                    if observation.lifecycle == "COMPLETED"
                    else AttemptEligibilityState.REVOKED
                )
                if claim._eligibility_ref().state is not expected_child_state:
                    raise ValueError

            by_claim = {observation._claim: observation for observation in observations}
            provider_history = []
            for binding in self.__bindings:
                claim = next(
                    (
                        candidate
                        for candidate in self.__claims
                        if candidate.binding is binding
                    ),
                    None,
                )
                observation = None if claim is None else by_claim.get(claim)
                provider_history.append(
                    {
                        "descriptor": binding.descriptor.document(),
                        "launch_key": binding.launch_key,
                        "required": self.__required[
                            binding.descriptor.capability_id
                        ],
                        "request": (
                            None if claim is None else claim._request_document_copy()
                        ),
                        "lifecycle": (
                            "NOT_STARTED" if observation is None else observation.lifecycle
                        ),
                        "execution_bytes_hex": (
                            None
                            if observation is None or observation.execution_bytes is None
                            else observation.execution_bytes.hex()
                        ),
                        "terminal_bytes_hex": (
                            None
                            if observation is None or observation.terminal_bytes is None
                            else observation.terminal_bytes.hex()
                        ),
                        "terminal_frame_bytes_hex": (
                            None
                            if observation is None
                            or observation.terminal_frame_bytes is None
                            else observation.terminal_frame_bytes.hex()
                        ),
                        "canonical_fact_bytes_hex": (
                            []
                            if observation is None
                            else [value.hex() for value in observation.canonical_fact_bytes]
                        ),
                    }
                )

            parse_partition = self.__product_set.product_set_document_copy()
            if qualification["status"] == "BLOCKED_NO_ACCEPTED_PRODUCTS":
                branch = (
                    "ZERO_PARSE_DENOMINATOR"
                    if not parse_partition["denominator"]
                    else "ALL_PARSE_REJECTED"
                )
            elif qualification["status"] == "BLOCKED_UNREPRESENTABLE":
                branch = "PROJECTION_BLOCKED"
            elif status == "COMPLETED":
                branch = "NORMAL_FULFILLED"
            else:
                branch = "REQUIRED_PROVIDER_NON_SUCCESS"

            source = {
                "branch": branch,
                "input_identity": {
                    "source_snapshot_digest": self.__inputs.source_snapshot_digest,
                    "policy_digest": self.__inputs.policy_digest,
                    "analysis_scope_digest": self.__inputs.analysis_scope_digest,
                    "slice_policy_digest": self.__inputs.slice_policy_digest,
                    "derivation_profile_digest": self.__inputs.derivation_profile_digest,
                    "language_support_function": self.__classification.language_support_function,
                    "classification_digest": self.__classification.classification_digest,
                    "parse_function": self.__product_set.parse_function,
                    "product_set_digest": self.__product_set.product_set_digest,
                    "fact_consumer_function": CONSUMER_FUNCTION,
                    "fact_consumer_attempt_id": self.__attempt_id,
                    "derivation_id": self.__derivation_id,
                },
                "parse_partition": parse_partition,
                "fact_projection": qualification,
                "provider_history": provider_history,
                "fact_set": document["fact_set"],
                "whole_attempt": {
                    "budget_limits": asdict(self.__context.limits),
                    "started_at_monotonic": self.__context.started_at_monotonic,
                    "execution_deadline_monotonic": self.__context.execution_deadline_monotonic,
                    "budget_state": self.__context.state.value,
                    "stop_trigger": None,
                    "parent_eligibility": self.__eligibility.state.value,
                },
            }
            return source, self.__context
        except Exception as exc:
            self._revoke()
            if isinstance(exc, ProductFactConsumerError):
                raise
            raise ProductFactConsumerError(
                "Fact handoff source validation failed closed"
            ) from exc

    def reconcile(
        self, observations: Sequence[OwnedProductFactObservation]
    ) -> "OwnedProductFactClosure":
        with self.__lock:
            if self.__reconciled:
                raise ProductFactConsumerError(
                    "consumer reconciliation already consumed"
                )
            self.__reconciled = True
        observed = tuple(observations)
        self.__reconciliation_history = observed
        try:
            self._validate_live()
            if len(observed) != len(self.__claims):
                raise ProductFactConsumerError(
                    "consumer children are missing or duplicated"
                )
            if self.qualification_copy()["status"] != "QUALIFIED":
                self.__closure = OwnedProductFactClosure(
                    self,
                    self.qualification_copy()["status"],
                    (),
                    None,
                    _token=_CLOSURE_TOKEN,
                )
                return self.__closure
            by_claim: dict[OwnedProductFactClaim, OwnedProductFactObservation] = {}
            for observation in observed:
                if type(observation) is not OwnedProductFactObservation:
                    raise ValueError
                observation._validate()
                claim = observation._claim
                if (
                    observation._parent is not self
                    or not any(c is claim for c in self.__claims)
                    or claim in by_claim
                ):
                    raise ProductFactConsumerError("foreign or duplicate child history")
                claim._validate_bound_state()
                if not claim._was_consumed() or observation.binding != claim.binding:
                    raise ValueError
                if observation.lifecycle == "COMPLETED":
                    if (
                        claim._eligibility_ref().state
                        is not AttemptEligibilityState.ADMITTED
                        or observation.terminal_bytes is None
                    ):
                        raise ValueError
                    if observation.terminal_frame_bytes is None:
                        raise ValueError
                    terminal = read_frame(
                        io.BytesIO(observation.terminal_frame_bytes),
                        payload_limit=self.__transport_limits.terminal_payload_bytes,
                    )
                    if canonical_json_bytes(terminal) != observation.terminal_bytes:
                        raise ValueError
                    kind, facts = admit_terminal(
                        terminal,
                        request=self._request(claim),
                        launch_key=claim.binding.launch_key,
                    )
                    if kind != "COMPLETED" or facts != observation.canonical_fact_bytes:
                        raise ValueError
                elif (
                    claim._eligibility_ref().state
                    is not AttemptEligibilityState.REVOKED
                ):
                    raise ValueError
                by_claim[claim] = observation
            if set(by_claim) != set(self.__claims):
                raise ValueError
            ordered = tuple(by_claim[c] for c in self.__claims)
            if any(o.lifecycle in {"RELEASE_FAILED", "INTERRUPTED"} for o in ordered):
                raise ProductFactConsumerError(
                    "any-source unsafe release/shared stop blocks join"
                )
            # The oracle is bound to application inputs, never supplied by the child.
            if (
                canonical_json_bytes(
                    qualify(self._projection(self.__claims[0].binding))
                )
                != self.__qualification
            ):
                raise ProductFactConsumerError("application universe changed")
            required = [
                o
                for o in ordered
                if self.__required[o.binding.descriptor.capability_id]
            ]
            if any(
                o.provider_run_status
                in {ProviderRunStatus.FAILED, ProviderRunStatus.INTERRUPTED}
                for o in required
            ):
                status = "FAILED"
            elif any(
                o.provider_run_status is ProviderRunStatus.UNAVAILABLE for o in required
            ):
                status = "UNAVAILABLE"
            else:
                status = "COMPLETED"
            fact_set = None
            if status == "COMPLETED":
                facts, conflicts = _merge_completed_sources(ordered)  # type: ignore[arg-type]
                expected = self.qualification_copy()["expected"]
                actual = sorted(
                    (
                        {k: v for k, v in f.items() if k != "provenance_refs"}
                        for f in facts
                    ),
                    key=lambda f: f["subject_key_digest"],
                )
                if conflicts or canonical_json_bytes(actual) != canonical_json_bytes(
                    expected
                ):
                    raise ProductFactConsumerError(
                        "qualified sources lost full semantic content"
                    )
                by_run = {
                    json.loads(o.terminal_bytes)["provider_run_id"]: {
                        json.loads(f)["fact_id"] for f in o.canonical_fact_bytes
                    }
                    for o in ordered
                    if o.lifecycle == "COMPLETED"
                }
                for fact in facts:
                    refs = {
                        run for run, ids in by_run.items() if fact["fact_id"] in ids
                    }
                    if fact["provenance_refs"] != sorted(refs):
                        raise ProductFactConsumerError(
                            "merged run/fact provenance mismatch"
                        )
                fact_set, _ = _fact_set_document(self.__inputs, facts, conflicts)
                if (
                    self.__context.try_complete_phase(
                        canonical_json_bytes(fact_set), resources_closed=True
                    )
                    is None
                ):
                    raise ProductFactConsumerError(
                        "consumer join lost the original budget"
                    )
            else:
                self._revoke()
            self.__closure = OwnedProductFactClosure(
                self, status, ordered, fact_set, _token=_CLOSURE_TOKEN
            )
            return self.__closure
        except Exception as exc:
            self._revoke()
            if isinstance(exc, ProductFactConsumerError):
                raise
            raise ProductFactConsumerError(
                "consumer reconciliation failed closed"
            ) from exc


class OwnedProductFactClaim:
    def __init__(
        self,
        parent: OwnedProductFactConsumer,
        binding: ProviderBinding,
        projection: Mapping[str, object],
        *,
        _token: object,
    ) -> None:
        if _token is not _CLAIM_TOKEN:
            raise ProductFactConsumerError("claim is not constructible")
        self.__parent = parent
        self.__bound_parent = parent
        self.binding = binding
        self.__bound_binding = binding
        self.__projection = canonical_json_bytes(validate_projection(projection))
        self.__bound_projection = self.__projection
        self.__request_bytes = canonical_json_bytes(
            parent._request_from_projection(projection)
        )
        self.__bound_request_bytes = self.__request_bytes
        self.__binding_bytes = canonical_json_bytes(
            {
                "descriptor": binding.descriptor.document(),
                "launch_key": binding.launch_key,
            }
        )
        self.__eligibility = AttemptEligibility()
        self.__bound_eligibility = self.__eligibility
        self.__consumed = False
        self.__lock = Lock()

    def projection_copy(self) -> dict[str, object]:
        self._validate_bound_state()
        return json.loads(self.__projection)

    def _validate_bound_state(self) -> None:
        if (
            self.__parent is not self.__bound_parent
            or self.binding is not self.__bound_binding
            or self.__projection is not self.__bound_projection
            or self.__eligibility is not self.__bound_eligibility
            or self.__request_bytes is not self.__bound_request_bytes
            or self.__binding_bytes
            != canonical_json_bytes(
                {
                    "descriptor": self.binding.descriptor.document(),
                    "launch_key": self.binding.launch_key,
                }
            )
        ):
            raise ProductFactConsumerError("Provider claim binding changed")
        validate_projection(json.loads(self.__projection))
        if self.__consumed is not True and self.__consumed is not False:
            raise ProductFactConsumerError("invalid claim consumption state")

    def claim(self) -> "ClaimedProductFactRequest":
        with self.__lock:
            if self.__consumed:
                raise ProductFactConsumerError("Provider claim already consumed")
            self.__consumed = True
        try:
            self.__parent._authorize(self)
            if self.__eligibility.state is not AttemptEligibilityState.PROVISIONAL:
                raise ProductFactConsumerError(
                    "Provider claim is no longer provisional"
                )
            return ClaimedProductFactRequest(
                self, self.__parent._request(self), _token=_CLAIMED_TOKEN
            )
        except Exception:
            self.__bound_eligibility.revoke()
            self.__eligibility.revoke()
            raise

    def _was_consumed(self) -> bool:
        with self.__lock:
            return self.__consumed

    def _parent_ref(self) -> OwnedProductFactConsumer:
        self._validate_bound_state()
        return self.__parent

    def _request_document_copy(self) -> dict[str, object]:
        self._validate_bound_state()
        return json.loads(self.__request_bytes)

    def _eligibility_ref(self) -> AttemptEligibility:
        return self.__eligibility


class ClaimedProductFactRequest:
    def __init__(
        self,
        claim: OwnedProductFactClaim,
        request: Mapping[str, object],
        *,
        _token: object,
    ) -> None:
        if _token is not _CLAIMED_TOKEN:
            raise ProductFactConsumerError("claimed request is not constructible")
        self.__claim = claim
        self.__bound_claim = claim
        self.__bytes = canonical_json_bytes(dict(request))
        self.__bound_bytes = self.__bytes

    def request_copy(self) -> dict[str, object]:
        if (
            self.__claim is not self.__bound_claim
            or self.__bytes is not self.__bound_bytes
        ):
            raise ProductFactConsumerError("claimed request identity changed")
        parent = self.__claim._parent_ref()
        if self.__bytes != canonical_json_bytes(parent._request(self.__claim)):
            raise ProductFactConsumerError("claimed request changed")
        return json.loads(self.__bytes)


class OwnedProductFactClosure:
    def __init__(
        self,
        parent: OwnedProductFactConsumer,
        status: str,
        observations: tuple[OwnedProductFactObservation, ...],
        fact_set: Mapping[str, object] | None,
        *,
        _token: object,
    ) -> None:
        if _token is not _CLOSURE_TOKEN:
            raise ProductFactConsumerError("consumer closure is not constructible")
        self.__parent = parent
        self.__bound_parent = parent
        self.__observations = observations
        self.__bound_observations = observations
        self.__bytes = canonical_json_bytes(
            {
                "consumer_function": CONSUMER_FUNCTION,
                "consumer_status": status,
                **parent._history_coordinates(),
                "child_history": [
                    {
                        "request": o._claim._request_document_copy(),
                        "lifecycle": o.lifecycle,
                        "execution": (
                            None
                            if o.execution_bytes is None
                            else json.loads(o.execution_bytes)
                        ),
                        "reported_fact_ids": [
                            json.loads(f)["fact_id"] for f in o.canonical_fact_bytes
                        ],
                        "terminal_sha256": (
                            None
                            if o.terminal_bytes is None
                            else hashlib.sha256(o.terminal_bytes).hexdigest()
                        ),
                        "terminal_frame_sha256": (
                            None
                            if o.terminal_frame_bytes is None
                            else hashlib.sha256(o.terminal_frame_bytes).hexdigest()
                        ),
                    }
                    for o in observations
                ],
                "fact_set": None if fact_set is None else dict(fact_set),
            }
        )
        self.__bound_bytes = self.__bytes
        self.__claimed = False
        self.__claim_purpose = None
        self.__lock = Lock()

    def document_copy(self) -> dict[str, object]:
        if (
            self.__bytes is not self.__bound_bytes
            or self.__parent is not self.__bound_parent
            or self.__observations is not self.__bound_observations
        ):
            raise ProductFactConsumerError("consumer closure changed")
        for observation in self.__observations:
            observation._validate()
            if observation._parent is not self.__parent:
                raise ProductFactConsumerError("foreign closure observation")
        return json.loads(self.__bytes)

    def claim_continuation(self) -> "ClaimedProductFactContinuation":
        with self.__lock:
            if self.__claimed:
                raise ProductFactConsumerError("consumer continuation already consumed")
            self.__claimed = True
            self.__claim_purpose = "LEGACY_CONTINUATION"
        try:
            self.__parent._authorize_continuation(self)
            return ClaimedProductFactContinuation(
                self, self.__parent, _token=_CONTINUATION_TOKEN
            )
        except Exception:
            self.__parent._revoke()
            raise

    def _claim_handoff_source(
        self,
    ) -> tuple[dict[str, object], BudgetContext]:
        with self.__lock:
            if self.__claimed:
                raise ProductFactConsumerError("consumer source already consumed")
            self.__claimed = True
            self.__claim_purpose = "COVERAGE_HANDOFF"
        try:
            return self.__parent._handoff_source_document(self)
        except Exception:
            self.__parent._revoke()
            raise

    def _observations_ref(self) -> tuple[OwnedProductFactObservation, ...]:
        self.document_copy()
        return self.__observations

    def _revoke_handoff_source(self) -> None:
        self.__parent._revoke()

    def _validate_child_authority(self) -> None:
        self.document_copy()
        for observation in self.__observations:
            claim = observation._claim
            self.__parent._authorize(claim)
            expected = (
                AttemptEligibilityState.ADMITTED
                if observation.lifecycle == "COMPLETED"
                else AttemptEligibilityState.REVOKED
            )
            if claim._eligibility_ref().state is not expected:
                raise ProductFactConsumerError(
                    "reconciled child lost its qualified lifecycle"
                )

    def _authorize_claimed(self) -> None:
        self.__parent._authorize_continuation(self)
        with self.__lock:
            if not self.__claimed or self.__claim_purpose != "LEGACY_CONTINUATION":
                raise ProductFactConsumerError("consumer continuation is not claimed")


class ClaimedProductFactContinuation:
    def __init__(
        self,
        closure: OwnedProductFactClosure,
        parent: OwnedProductFactConsumer,
        *,
        _token: object,
    ) -> None:
        if _token is not _CONTINUATION_TOKEN:
            raise ProductFactConsumerError("continuation is not constructible")
        self.__closure = closure
        self.__bound_closure = closure
        self.__parent = parent
        self.__bound_parent = parent

    def _validate(self) -> None:
        if (
            self.__closure is not self.__bound_closure
            or self.__parent is not self.__bound_parent
        ):
            raise ProductFactConsumerError("consumer continuation identity changed")
        self.__closure._authorize_claimed()

    def _fact_set_copy(self) -> dict[str, object]:
        self._validate()
        return self.__closure.document_copy()["fact_set"]

    def _context_ref(self) -> BudgetContext:
        self._validate()
        return self.__parent._context_ref()


def create_product_fact_consumer(
    closure: OwnedParseFulfillmentClosure,
    *,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
    cancellation_requested: Callable[[], bool] | None = None,
) -> OwnedProductFactConsumer:
    if type(closure) is not OwnedParseFulfillmentClosure:
        raise ProductFactConsumerError("consumer requires an owned Parse closure")
    continuation = closure.claim_continuation()
    upstream = continuation._attempt_ref()
    try:
        inputs = upstream._inputs_ref()
        _revalidate_exact_inputs(inputs)
        classification = upstream._classification_ref()
        recomputed = classify_language_support(inputs)
        if (
            recomputed.classification_document_copy()
            != classification.classification_document_copy()
        ):
            raise ValueError
        products = continuation._product_set()
        denominator = tuple(
            s["subject_identity"]
            for s in classification.subjects_copy()
            if s["disposition"] == "ELIGIBLE"
        )
        if tuple(products.product_set_document_copy()["denominator"]) != denominator:
            raise ValueError
        for name in (
            "source_snapshot_digest",
            "policy_digest",
            "analysis_scope_digest",
            "derivation_profile_digest",
        ):
            if getattr(products, name) != getattr(inputs, name):
                raise ValueError
        if (
            products.classification_digest != classification.classification_digest
            or products.language_support_function
            != classification.language_support_function
        ):
            raise ValueError
        required, normalized = _admit_closed_applicability(
            inputs,
            derivation_id=derivation_id,
            bindings=bindings,
            cancellation_requested=cancellation_requested,
            transport_limits=transport_limits,
        )
        return OwnedProductFactConsumer(
            continuation,
            derivation_id=derivation_id,
            bindings=normalized,
            required=required,
            transport_limits=transport_limits,
            cancellation_requested=cancellation_requested,
            _token=_PARENT_TOKEN,
        )
    except Exception as exc:
        upstream._parent_eligibility_ref().revoke()
        raise ProductFactConsumerError(
            "post-Parse consumer admission failed closed"
        ) from exc


def _observation(
    claim: OwnedProductFactClaim,
    lifecycle: str,
    *,
    terminal: bytes | None = None,
    frame: bytes | None = None,
    facts: tuple[bytes, ...] = (),
    execution: bytes | None = None,
) -> OwnedProductFactObservation:
    value = OwnedProductFactObservation(
        claim.binding,
        lifecycle,
        facts,
        terminal,
        frame,
        claim._parent_ref(),
        claim,
        _observation_seal(claim.binding, lifecycle, facts, terminal, frame, execution),
        _OBSERVATION_TOKEN,
        execution,
    )
    value._validate()
    claim._parent_ref()._record_observation(value)
    return value


def execute_product_fact_claim(
    claim: OwnedProductFactClaim,
) -> OwnedProductFactObservation:
    if type(claim) is not OwnedProductFactClaim:
        raise ProductFactConsumerError("invalid product consumer claim")
    claimed = claim.claim()
    parent = claim._parent_ref()
    request = claimed.request_copy()
    limits = parent._limits_ref()
    context = parent._context_ref()
    child = claim._eligibility_ref()
    admitted: list[bool] = []
    try:
        frame = encode_frame(request, payload_limit=limits.request_payload_bytes)
        result = run_windows_execution_cell(
            context,
            child,
            executable=Path(sys.executable).resolve(),
            arguments=(
                "-I",
                str(Path(__file__).with_name("_fact_fulfillment_worker.py").resolve()),
                claim.binding.launch_key,
                str(limits.request_payload_bytes),
                str(limits.terminal_payload_bytes),
            ),
            request_frame=frame,
            terminal_payload_limit=limits.terminal_payload_bytes,
            cancellation_requested=parent._cancellation_ref(),
            on_admitted=lambda: admitted.append(True),
        )
    except CellRuntimeUnavailableError:
        child.revoke()
        return _observation(claim, "UNAVAILABLE")
    except CellReleaseError:
        child.revoke()
        observation = _observation(claim, "RELEASE_FAILED")
        parent._revoke()
        return observation
    except (CellPreparationError, FrameProtocolError):
        child.revoke()
        return _observation(
            claim, "INTERRUPTED" if context.stop_trigger else "INFRASTRUCTURE_FAILED"
        )
    except Exception as exc:
        child.revoke()
        observation = _observation(
            claim,
            "RELEASE_FAILED",
            execution=canonical_json_bytes(
                {
                    "unclassified_exception": type(exc).__name__,
                    "release_known": False,
                }
            ),
        )
        parent._revoke()
        return observation
    receipt = asdict(result)
    receipt["terminal_bytes"] = hashlib.sha256(result.terminal_bytes).hexdigest()
    receipt["stop_trigger"] = (
        None if result.stop_trigger is None else result.stop_trigger.value
    )
    receipt["admission_callbacks"] = len(admitted)
    execution = canonical_json_bytes(receipt)
    if result.stop_trigger is not None:
        child.revoke()
        return _observation(
            claim, "INTERRUPTED", frame=result.terminal_bytes, execution=execution
        )
    if (
        not result.active_process_zero
        or not result.handles_released
        or not result.channel_threads_released
    ):
        child.revoke()
        observation = _observation(
            claim, "RELEASE_FAILED", frame=result.terminal_bytes, execution=execution
        )
        parent._revoke()
        return observation
    if (
        not result.admitted
        or not result.process_created_suspended
        or not result.process_assigned_before_resume
        or not result.process_resumed
        or admitted != [True]
        or result.request_channel_failed
        or result.result_channel_failed
        or result.result_transport_exceeded
        or result.root_exit_code != 0
        or not result.active_process_zero
        or not result.handles_released
        or not result.channel_threads_released
    ):
        child.revoke()
        return _observation(
            claim,
            "INFRASTRUCTURE_FAILED",
            frame=result.terminal_bytes,
            execution=execution,
        )
    try:
        terminal = read_frame(
            io.BytesIO(result.terminal_bytes),
            payload_limit=limits.terminal_payload_bytes,
        )
        kind, facts = admit_terminal(
            terminal, request=request, launch_key=claim.binding.launch_key
        )
    except (FrameProtocolError, ProductFactProtocolError):
        child.revoke()
        return _observation(
            claim, "FAILED", frame=result.terminal_bytes, execution=execution
        )
    raw_terminal = canonical_json_bytes(terminal)
    if kind != "COMPLETED":
        child.revoke()
        return _observation(
            claim,
            "UNAVAILABLE" if kind == "PROVIDER_UNAVAILABLE" else "FAILED",
            terminal=raw_terminal,
            frame=result.terminal_bytes,
            execution=execution,
        )
    try:
        committed = (
            child.permits_phase_commit()
            and context.try_complete_phase(raw_terminal, resources_closed=True)
            is not None
        )
    except BudgetPrimitiveError:
        committed = False
    if not committed:
        child.revoke()
        return _observation(
            claim,
            "INTERRUPTED" if context.stop_trigger else "INFRASTRUCTURE_FAILED",
            frame=result.terminal_bytes,
            execution=execution,
        )
    return _observation(
        claim,
        "COMPLETED",
        terminal=raw_terminal,
        frame=result.terminal_bytes,
        facts=facts,
        execution=execution,
    )


def execute_fact_fulfillment(
    parent: OwnedProductFactConsumer,
) -> OwnedProductFactClosure:
    """Serial closed sources; ordinary failures never skip later responsibility."""
    if type(parent) is not OwnedProductFactConsumer:
        raise ProductFactConsumerError("foreign fulfillment owner")
    claims = parent.claims()
    observations = []
    for claim in claims:
        observation = execute_product_fact_claim(claim)
        observations.append(observation)
        if observation.lifecycle in {"INTERRUPTED", "RELEASE_FAILED"}:
            break
    return parent.reconcile(observations)
