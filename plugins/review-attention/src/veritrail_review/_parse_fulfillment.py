from __future__ import annotations

import hashlib
import io
from pathlib import Path
from threading import Lock
from typing import Mapping, Sequence

from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    FrameProtocolError,
    encode_frame,
    read_frame,
)
from veritrail_review._language_support import (
    _revalidate_exact_inputs,
    classify_language_support,
)
from veritrail_review._language_support_values import (
    OwnedLanguageSupportClassification,
    _validate_language_support_classification,
)
from veritrail_review._parse_fulfillment_values import (
    PARSE_FUNCTION_ID,
    PARSE_WORKER_PROTOCOL,
    OwnedParseObservation,
    OwnedParseProductSet,
    OwnedParseRuntimeCapability,
    _validate_parse_observation,
    _validate_parse_product_set,
    _validate_runtime_capability,
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
from veritrail_review.derivation_input_contracts import DerivationInputSet
from veritrail_review.errors import BudgetPrimitiveError


_ATTEMPT_TOKEN = object()
_CLAIM_TOKEN = object()
_CLAIMED_TOKEN = object()
_CLOSURE_TOKEN = object()
_CONTINUATION_TOKEN = object()
_REQUEST_LIMIT = 64 * 1024 * 1024
_TERMINAL_LIMIT = 16 * 1024 * 1024


class _ParseFulfillmentError(ValueError):
    """One private Parse authority or reconciliation boundary failed closed."""


class OwnedParseFulfillmentAttempt:
    """Application-owned exact denominator and attempt authority."""

    __slots__ = (
        "__bound_classification",
        "__bound_context",
        "__bound_inputs",
        "__bound_parent_eligibility",
        "__bound_runtime",
        "__claims",
        "__classification",
        "__context",
        "__input_state_seal",
        "__inputs",
        "__lock",
        "__parent_eligibility",
        "__reconciliation_consumed",
        "__runtime",
    )

    def __init__(
        self,
        *,
        inputs: DerivationInputSet,
        context: BudgetContext,
        parent_eligibility: AttemptEligibility,
        classification: OwnedLanguageSupportClassification,
        runtime: OwnedParseRuntimeCapability,
        subject_documents: Sequence[Mapping[str, object]],
        _construction_token: object,
    ) -> None:
        if _construction_token is not _ATTEMPT_TOKEN:
            raise _ParseFulfillmentError("Parse attempt is not constructible")
        self.__bound_inputs = inputs
        self.__inputs = inputs
        self.__bound_context = context
        self.__context = context
        self.__bound_parent_eligibility = parent_eligibility
        self.__parent_eligibility = parent_eligibility
        self.__bound_classification = classification
        self.__classification = classification
        self.__bound_runtime = runtime
        self.__runtime = runtime
        self.__input_state_seal = _input_state_seal(inputs)
        self.__claims = tuple(
            OwnedParseSubjectClaim(
                attempt=self,
                subject_document=document,
                _construction_token=_CLAIM_TOKEN,
            )
            for document in subject_documents
        )
        self.__lock = Lock()
        self.__reconciliation_consumed = False
        self._validate_live()

    def claims(self) -> tuple["OwnedParseSubjectClaim", ...]:
        self._validate_live()
        return self.__claims

    def denominator_subject_ids(self) -> tuple[str, ...]:
        self._validate_live()
        return tuple(claim._subject_identity() for claim in self.__claims)

    def reconcile(
        self, observations: Sequence[OwnedParseObservation]
    ) -> "OwnedParseFulfillmentClosure":
        with self.__lock:
            if self.__reconciliation_consumed:
                raise _ParseFulfillmentError(
                    "Parse reconciliation was already consumed"
                )
            self.__reconciliation_consumed = True
        try:
            self._validate_live()
            observed = tuple(observations)
            claim_by_subject = {
                claim._subject_identity(): claim for claim in self.__claims
            }
            seen: set[str] = set()
            accepted: list[dict[str, str]] = []
            rejected: list[dict[str, str]] = []
            product_bytes: dict[str, bytes] = {}
            ordered_observations: list[OwnedParseObservation] = []
            for observation in observed:
                _validate_parse_observation(observation)
                subject = observation.subject_identity
                claim = claim_by_subject.get(subject)
                if (
                    claim is None
                    or subject in seen
                    or observation._attempt is not self
                    or observation._claim is not claim
                    or observation.obligation_id != claim._obligation_id()
                    or not claim._was_consumed()
                    or claim._child_eligibility().state
                    is not AttemptEligibilityState.ADMITTED
                    or observation.lifecycle != "COMPLETED"
                ):
                    raise _ParseFulfillmentError(
                        "Parse observation reconciliation was rejected"
                    )
                result = observation.semantic_result_copy()
                if result is None:
                    raise _ParseFulfillmentError(
                        "completed Parse observation has no semantic result"
                    )
                seen.add(subject)
                ordered_observations.append(observation)
                if result["disposition"] == "ACCEPTED":
                    product = result["product"]
                    raw_product = canonical_json_bytes(product)
                    product_bytes[subject] = raw_product
                    if observation.product_semantic_digest is None:
                        raise _ParseFulfillmentError(
                            "accepted Parse result has no product identity"
                        )
                    accepted.append(
                        {
                            "subject_identity": subject,
                            "obligation_id": observation.obligation_id,
                            "product_semantic_digest": (
                                observation.product_semantic_digest
                            ),
                        }
                    )
                else:
                    rejected.append(
                        {
                            "subject_identity": subject,
                            "obligation_id": observation.obligation_id,
                        }
                    )
            denominator = self.denominator_subject_ids()
            if seen != set(denominator) or len(observed) != len(denominator):
                raise _ParseFulfillmentError(
                    "Parse denominator was not reconciled completely"
                )
            position = {subject: index for index, subject in enumerate(denominator)}
            accepted.sort(key=lambda item: position[item["subject_identity"]])
            rejected.sort(key=lambda item: position[item["subject_identity"]])
            classification = self.__classification
            unsigned: dict[str, object] = {
                "source_snapshot_digest": classification.source_snapshot_digest,
                "policy_digest": classification.policy_digest,
                "analysis_scope_digest": classification.analysis_scope_digest,
                "derivation_profile_digest": classification.derivation_profile_digest,
                "language_support_function": classification.language_support_function,
                "classification_digest": classification.classification_digest,
                "parse_function": PARSE_FUNCTION_ID,
                "denominator": list(denominator),
                "accepted": accepted,
                "rejected": rejected,
            }
            document = {
                **unsigned,
                "product_set_digest": semantic_digest(
                    "veritrail.review.private-parse-product-set/0.1", unsigned
                ),
            }
            product_set = OwnedParseProductSet._create(
                source_snapshot_digest=classification.source_snapshot_digest,
                policy_digest=classification.policy_digest,
                analysis_scope_digest=classification.analysis_scope_digest,
                derivation_profile_digest=classification.derivation_profile_digest,
                language_support_function=classification.language_support_function,
                classification_digest=classification.classification_digest,
                product_set_document=document,
                product_bytes_by_subject=product_bytes,
            )
            return OwnedParseFulfillmentClosure(
                attempt=self,
                observations=tuple(ordered_observations),
                product_set=product_set,
                _construction_token=_CLOSURE_TOKEN,
            )
        except Exception as exc:
            self._fail_closed()
            if isinstance(exc, _ParseFulfillmentError):
                raise
            raise _ParseFulfillmentError("Parse reconciliation failed closed") from exc

    def _validate_live(self) -> None:
        if (
            self.__inputs is not self.__bound_inputs
            or self.__context is not self.__bound_context
            or self.__parent_eligibility is not self.__bound_parent_eligibility
            or self.__classification is not self.__bound_classification
            or self.__runtime is not self.__bound_runtime
            or _input_state_seal(self.__inputs) != self.__input_state_seal
            or type(self.__context) is not BudgetContext
            or self.__context.state is not BudgetState.RUNNING
            or type(self.__parent_eligibility) is not AttemptEligibility
            or self.__parent_eligibility.state
            is not AttemptEligibilityState.ADMITTED
        ):
            raise _ParseFulfillmentError("Parse attempt identity is no longer live")
        _validate_language_support_classification(self.__classification)
        _validate_runtime_capability(self.__runtime, check_executable=False)
        if not self.__context.checkpoint():
            raise _ParseFulfillmentError("Parse attempt budget is no longer live")
        if (
            self.__classification.source_snapshot_digest
            != self.__inputs.source_snapshot_digest
            or self.__classification.policy_digest != self.__inputs.policy_digest
            or self.__classification.analysis_scope_digest
            != self.__inputs.analysis_scope_digest
            or self.__classification.derivation_profile_digest
            != self.__inputs.derivation_profile_digest
        ):
            raise _ParseFulfillmentError(
                "Parse classification is not bound to exact inputs"
            )

    def _authorize_claim(self, claim: "OwnedParseSubjectClaim") -> None:
        with self.__lock:
            try:
                self._validate_live()
                if not any(item is claim for item in self.__claims):
                    raise _ParseFulfillmentError("foreign Parse claim")
                claim._validate_bound_state(require_consumed=True)
            except Exception:
                self._fail_closed()
                raise

    def _authorize_continuation(
        self, closure: "OwnedParseFulfillmentClosure"
    ) -> None:
        with self.__lock:
            self._validate_live()
            if not self.__reconciliation_consumed:
                raise _ParseFulfillmentError("Parse reconciliation did not occur")
            closure._validate_bound_state()
            for claim in self.__claims:
                claim._validate_bound_state(require_consumed=True)
                if claim._child_eligibility().state is not AttemptEligibilityState.ADMITTED:
                    raise _ParseFulfillmentError("Parse child lost admission")

    def _inputs_ref(self) -> DerivationInputSet:
        return self.__inputs

    def _context_ref(self) -> BudgetContext:
        return self.__context

    def _parent_eligibility_ref(self) -> AttemptEligibility:
        return self.__parent_eligibility

    def _classification_ref(self) -> OwnedLanguageSupportClassification:
        return self.__classification

    def _runtime_ref(self) -> OwnedParseRuntimeCapability:
        return self.__runtime

    def _fail_closed(self) -> None:
        for parent in (self.__bound_parent_eligibility, self.__parent_eligibility):
            if type(parent) is AttemptEligibility:
                parent.revoke()
        for claim in self.__claims:
            claim._revoke_child()


class OwnedParseSubjectClaim:
    """One exact denominator obligation; consumed even on failed execution."""

    __slots__ = (
        "__attempt",
        "__bound_child_eligibility",
        "__bound_document_bytes",
        "__child_eligibility",
        "__consumed",
        "__document_bytes",
        "__lock",
    )

    def __init__(
        self,
        *,
        attempt: OwnedParseFulfillmentAttempt,
        subject_document: Mapping[str, object],
        _construction_token: object,
    ) -> None:
        if _construction_token is not _CLAIM_TOKEN:
            raise _ParseFulfillmentError("Parse claim is not constructible")
        document_bytes = canonical_json_bytes(dict(subject_document))
        self.__attempt = attempt
        self.__bound_document_bytes = document_bytes
        self.__document_bytes = document_bytes
        child = AttemptEligibility()
        self.__bound_child_eligibility = child
        self.__child_eligibility = child
        self.__consumed = False
        self.__lock = Lock()
        self._validate_bound_state(require_consumed=False)

    def claim(self) -> "ClaimedParseRequest":
        with self.__lock:
            if self.__consumed:
                raise _ParseFulfillmentError("Parse claim was already consumed")
            self.__consumed = True
        try:
            self.__attempt._authorize_claim(self)
            return ClaimedParseRequest(
                claim=self, _construction_token=_CLAIMED_TOKEN
            )
        except Exception:
            self._revoke_child()
            raise

    def _validate_bound_state(self, *, require_consumed: bool) -> None:
        with self.__lock:
            if (
                self.__document_bytes is not self.__bound_document_bytes
                or self.__child_eligibility is not self.__bound_child_eligibility
                or self.__consumed is not require_consumed
            ):
                raise _ParseFulfillmentError("Parse claim identity changed")
            document = _subject_document(self.__document_bytes)
            if (
                document["parse_function"] != PARSE_FUNCTION_ID
                or self.__child_eligibility.state
                not in {
                    AttemptEligibilityState.PROVISIONAL,
                    AttemptEligibilityState.ADMITTED,
                }
            ):
                raise _ParseFulfillmentError("invalid Parse claim state")

    def _revoke_child(self) -> None:
        for child in (self.__bound_child_eligibility, self.__child_eligibility):
            if type(child) is AttemptEligibility:
                child.revoke()

    def _document_copy(self) -> dict[str, object]:
        return _subject_document(self.__document_bytes)

    def _subject_identity(self) -> str:
        return str(self._document_copy()["subject_identity"])

    def _obligation_id(self) -> str:
        return str(self._document_copy()["obligation_id"])

    def _child_eligibility(self) -> AttemptEligibility:
        return self.__child_eligibility

    def _attempt_ref(self) -> OwnedParseFulfillmentAttempt:
        return self.__attempt

    def _was_consumed(self) -> bool:
        with self.__lock:
            return self.__consumed


class ClaimedParseRequest:
    __slots__ = ("__claim",)

    def __init__(
        self, *, claim: OwnedParseSubjectClaim, _construction_token: object
    ) -> None:
        if _construction_token is not _CLAIMED_TOKEN:
            raise _ParseFulfillmentError("claimed Parse request is not constructible")
        self.__claim = claim

    def _authorize(self) -> None:
        self.__claim._attempt_ref()._authorize_claim(self.__claim)

    def _document_copy(self) -> dict[str, object]:
        self._authorize()
        return self.__claim._document_copy()

    def _claim_ref(self) -> OwnedParseSubjectClaim:
        self._authorize()
        return self.__claim


class OwnedParseFulfillmentClosure:
    __slots__ = (
        "__attempt",
        "__bound_observations",
        "__bound_product_set",
        "__claimed",
        "__lock",
        "__observations",
        "__product_set",
    )

    def __init__(
        self,
        *,
        attempt: OwnedParseFulfillmentAttempt,
        observations: tuple[OwnedParseObservation, ...],
        product_set: OwnedParseProductSet,
        _construction_token: object,
    ) -> None:
        if _construction_token is not _CLOSURE_TOKEN:
            raise _ParseFulfillmentError("Parse closure is not constructible")
        self.__attempt = attempt
        self.__bound_observations = observations
        self.__observations = observations
        self.__bound_product_set = product_set
        self.__product_set = product_set
        self.__claimed = False
        self.__lock = Lock()
        self._validate_bound_state()

    def product_set(self) -> OwnedParseProductSet:
        self._validate_bound_state()
        return self.__product_set

    def claim_continuation(self) -> "ClaimedParseContinuation":
        with self.__lock:
            if self.__claimed:
                raise _ParseFulfillmentError("Parse continuation was already claimed")
            self.__claimed = True
        try:
            self.__attempt._authorize_continuation(self)
            return ClaimedParseContinuation(
                closure=self, _construction_token=_CONTINUATION_TOKEN
            )
        except Exception:
            self.__attempt._fail_closed()
            raise

    def _validate_bound_state(self) -> None:
        if (
            self.__observations is not self.__bound_observations
            or self.__product_set is not self.__bound_product_set
        ):
            raise _ParseFulfillmentError("Parse closure identity changed")
        _validate_parse_product_set(self.__product_set)
        for observation in self.__observations:
            _validate_parse_observation(observation)
            if observation._attempt is not self.__attempt:
                raise _ParseFulfillmentError("foreign Parse closure observation")

    def _authorize_claimed(self) -> None:
        self.__attempt._authorize_continuation(self)
        with self.__lock:
            if not self.__claimed:
                raise _ParseFulfillmentError("Parse continuation is not claimed")

    def _product_set_ref(self) -> OwnedParseProductSet:
        return self.__product_set


class ClaimedParseContinuation:
    __slots__ = ("__closure",)

    def __init__(
        self,
        *,
        closure: OwnedParseFulfillmentClosure,
        _construction_token: object,
    ) -> None:
        if _construction_token is not _CONTINUATION_TOKEN:
            raise _ParseFulfillmentError(
                "claimed Parse continuation is not constructible"
            )
        self.__closure = closure

    def _product_set(self) -> OwnedParseProductSet:
        self.__closure._authorize_claimed()
        return self.__closure._product_set_ref()

    def _products_copy(self) -> dict[str, object]:
        return self._product_set().products_copy()


def qualify_parse_runtime(
    executable: Path, *, expected_sha256: str
) -> OwnedParseRuntimeCapability:
    """Bind an explicitly selected executable to caller-owned exact bytes."""

    path = Path(executable)
    if (
        type(expected_sha256) is not str
        or len(expected_sha256) != 64
        or not path.is_absolute()
    ):
        raise _ParseFulfillmentError("invalid Parse runtime request")
    value = OwnedParseRuntimeCapability._create(
        executable=path, executable_sha256=expected_sha256
    )
    try:
        _validate_runtime_capability(value, check_executable=True)
    except ValueError as exc:
        raise _ParseFulfillmentError("Parse runtime qualification failed") from exc
    return value


def create_parse_fulfillment_attempt(
    inputs: DerivationInputSet,
    context: BudgetContext,
    parent_eligibility: AttemptEligibility,
    classification: OwnedLanguageSupportClassification,
    runtime: OwnedParseRuntimeCapability,
) -> OwnedParseFulfillmentAttempt:
    """Create one private Parse denominator from exact eligible subjects."""

    try:
        if (
            type(inputs) is not DerivationInputSet
            or type(context) is not BudgetContext
            or context.state is not BudgetState.RUNNING
            or type(parent_eligibility) is not AttemptEligibility
            or parent_eligibility.state is not AttemptEligibilityState.ADMITTED
            or type(classification) is not OwnedLanguageSupportClassification
            or type(runtime) is not OwnedParseRuntimeCapability
        ):
            raise ValueError
        _validate_language_support_classification(classification)
        _validate_runtime_capability(runtime, check_executable=True)
        _, _, _, blobs = _revalidate_exact_inputs(inputs)
        recomputed = classify_language_support(inputs)
        if (
            recomputed.classification_document_bytes
            != classification.classification_document_bytes
            or recomputed.classification_digest != classification.classification_digest
        ):
            raise ValueError
        subjects: list[dict[str, object]] = []
        for item in classification.subjects_copy():
            if item["disposition"] != "ELIGIBLE":
                continue
            subjects.append(_parse_subject_document(item, blobs))
        attempt = OwnedParseFulfillmentAttempt(
            inputs=inputs,
            context=context,
            parent_eligibility=parent_eligibility,
            classification=classification,
            runtime=runtime,
            subject_documents=subjects,
            _construction_token=_ATTEMPT_TOKEN,
        )
        return attempt
    except Exception as exc:
        if type(parent_eligibility) is AttemptEligibility:
            parent_eligibility.revoke()
        if isinstance(exc, _ParseFulfillmentError):
            raise
        raise _ParseFulfillmentError("Parse attempt construction failed") from exc


def execute_parse_claim(
    claim: OwnedParseSubjectClaim,
) -> OwnedParseObservation:
    """Consume one obligation and obtain one contained candidate observation."""

    if type(claim) is not OwnedParseSubjectClaim:
        raise _ParseFulfillmentError("invalid Parse claim")
    claimed = claim.claim()
    attempt = claim._attempt_ref()
    document = claimed._document_copy()
    runtime = attempt._runtime_ref()
    child = claim._child_eligibility()
    try:
        _validate_runtime_capability(runtime, check_executable=True)
    except ValueError:
        child.revoke()
        return OwnedParseObservation._create(
            subject_identity=str(document["subject_identity"]),
            obligation_id=str(document["obligation_id"]),
            lifecycle="REFERENCE_RUNTIME_UNAVAILABLE",
            semantic_result=None,
            attempt=attempt,
            claim=claim,
        )
    request = {
        "protocol": PARSE_WORKER_PROTOCOL,
        "message_kind": "PARSE_REQUEST",
        "source_text": document["source_text"],
    }
    request_frame = encode_frame(request, payload_limit=_REQUEST_LIMIT)
    worker = Path(__file__).with_name("_parse_fulfillment_worker.py").resolve()
    admitted: list[bool] = []
    try:
        observation = run_windows_execution_cell(
            attempt._context_ref(),
            child,
            executable=runtime.executable,
            arguments=("-I", str(worker)),
            request_frame=request_frame,
            terminal_payload_limit=_TERMINAL_LIMIT,
            cancellation_requested=None,
            on_admitted=lambda: admitted.append(True),
        )
    except CellRuntimeUnavailableError:
        child.revoke()
        return _failed_observation(attempt, claim, document, "REFERENCE_RUNTIME_UNAVAILABLE")
    except CellReleaseError:
        child.revoke()
        return _failed_observation(attempt, claim, document, "RELEASE_FAILED")
    except CellPreparationError:
        child.revoke()
        lifecycle = (
            "INTERRUPTED"
            if attempt._context_ref().stop_trigger is not None
            else "INFRASTRUCTURE_FAILED"
        )
        return _failed_observation(attempt, claim, document, lifecycle)
    if not observation.admitted or admitted != [True]:
        child.revoke()
        return _failed_observation(attempt, claim, document, "INFRASTRUCTURE_FAILED")
    if observation.stop_trigger is not None:
        child.revoke()
        return _failed_observation(attempt, claim, document, "INTERRUPTED")
    if (
        observation.request_channel_failed
        or observation.result_channel_failed
        or observation.result_transport_exceeded
        or observation.root_exit_code != 0
        or not observation.active_process_zero
        or not observation.handles_released
        or not observation.channel_threads_released
    ):
        child.revoke()
        return _failed_observation(attempt, claim, document, "INFRASTRUCTURE_FAILED")
    try:
        terminal = read_frame(
            io.BytesIO(observation.terminal_bytes), payload_limit=_TERMINAL_LIMIT
        )
        lifecycle, semantic_result = _validate_terminal(terminal)
    except (FrameProtocolError, ValueError):
        child.revoke()
        return _failed_observation(attempt, claim, document, "INFRASTRUCTURE_FAILED")
    if lifecycle != "COMPLETED":
        child.revoke()
        return _failed_observation(attempt, claim, document, lifecycle)
    candidate = OwnedParseObservation._create(
        subject_identity=str(document["subject_identity"]),
        obligation_id=str(document["obligation_id"]),
        lifecycle="COMPLETED",
        semantic_result=semantic_result,
        attempt=attempt,
        claim=claim,
    )
    try:
        committed = (
            child.permits_phase_commit()
            and attempt._context_ref().try_complete_phase(
                canonical_json_bytes(terminal), resources_closed=True
            )
            is not None
        )
    except BudgetPrimitiveError:
        committed = False
    if not committed:
        child.revoke()
        lifecycle = (
            "INTERRUPTED"
            if attempt._context_ref().stop_trigger is not None
            else "INFRASTRUCTURE_FAILED"
        )
        return _failed_observation(attempt, claim, document, lifecycle)
    return candidate


def _parse_subject_document(
    subject: Mapping[str, object], blobs: Mapping[str, bytes]
) -> dict[str, object]:
    semantic_input = subject.get("semantic_input")
    if not isinstance(semantic_input, Mapping):
        raise ValueError
    inventory = semantic_input.get("inventory_item")
    if not isinstance(inventory, Mapping):
        raise ValueError
    git_object = inventory.get("git_object")
    if not isinstance(git_object, Mapping) or not isinstance(git_object.get("hex"), str):
        raise ValueError
    raw = blobs[git_object["hex"]]
    encoding = subject.get("effective_source_encoding")
    if encoding == "UTF-8":
        source_text = raw.decode("utf-8", errors="strict")
    elif encoding == "UTF-8-SIG":
        if not raw.startswith(b"\xef\xbb\xbf"):
            raise ValueError
        source_text = raw[3:].decode("utf-8", errors="strict")
    else:
        raise ValueError
    subject_identity = subject.get("subject_identity")
    if not isinstance(subject_identity, str):
        raise ValueError
    exact_input = {
        "subject_identity": subject_identity,
        "semantic_input": semantic_input,
        "effective_source_encoding": encoding,
        "parse_function": PARSE_FUNCTION_ID,
        "invocation": {
            "filename": "<veritrail-r1-parse>",
            "mode": "exec",
            "type_comments": False,
            "feature_version": [3, 10],
        },
    }
    return {
        "subject_identity": subject_identity,
        "obligation_id": semantic_digest(
            "veritrail.review.private-parse-obligation/0.1", exact_input
        ),
        "parse_function": PARSE_FUNCTION_ID,
        "source_text": source_text,
        "exact_input_digest": semantic_digest(
            "veritrail.review.private-parse-input/0.1", exact_input
        ),
    }


def _subject_document(raw: bytes) -> dict[str, object]:
    try:
        value = read_frame(
            io.BytesIO(len(raw).to_bytes(8, "big") + raw), payload_limit=_REQUEST_LIMIT
        )
    except FrameProtocolError as exc:
        raise _ParseFulfillmentError("invalid Parse subject document") from exc
    if (
        set(value)
        != {
            "subject_identity",
            "obligation_id",
            "parse_function",
            "source_text",
            "exact_input_digest",
        }
        or not all(
            isinstance(value[key], str)
            for key in (
                "subject_identity",
                "obligation_id",
                "parse_function",
                "source_text",
                "exact_input_digest",
            )
        )
        or value["parse_function"] != PARSE_FUNCTION_ID
    ):
        raise _ParseFulfillmentError("invalid Parse subject document")
    return value


def _validate_terminal(
    terminal: Mapping[str, object],
) -> tuple[str, Mapping[str, object] | None]:
    if (
        set(terminal)
        != {"protocol", "message_kind", "lifecycle", "semantic_result"}
        or terminal.get("protocol") != PARSE_WORKER_PROTOCOL
        or terminal.get("message_kind") != "PARSE_TERMINAL"
        or terminal.get("lifecycle")
        not in {
            "COMPLETED",
            "REFERENCE_RUNTIME_UNAVAILABLE",
            "INTERNAL_PARSER_FAILURE",
        }
    ):
        raise ValueError
    lifecycle = str(terminal["lifecycle"])
    semantic = terminal["semantic_result"]
    if lifecycle == "COMPLETED":
        if not isinstance(semantic, Mapping):
            raise ValueError
        # OwnedParseObservation performs the complete semantic/product validation.
        probe = OwnedParseObservation._create(
            subject_identity="0" * 64,
            obligation_id="1" * 64,
            lifecycle="COMPLETED",
            semantic_result=semantic,
            attempt=object(),
            claim=object(),
        )
        return lifecycle, probe.semantic_result_copy()
    if semantic is not None:
        raise ValueError
    return lifecycle, None


def _failed_observation(
    attempt: OwnedParseFulfillmentAttempt,
    claim: OwnedParseSubjectClaim,
    document: Mapping[str, object],
    lifecycle: str,
) -> OwnedParseObservation:
    return OwnedParseObservation._create(
        subject_identity=str(document["subject_identity"]),
        obligation_id=str(document["obligation_id"]),
        lifecycle=lifecycle,
        semantic_result=None,
        attempt=attempt,
        claim=claim,
    )
