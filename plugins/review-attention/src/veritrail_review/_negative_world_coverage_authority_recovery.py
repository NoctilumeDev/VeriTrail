"""Private negative-world Coverage producer, validator, and admission.

The producer and validator deliberately rederive the semantic history through
separate code paths.  Shared helpers below are limited to the frozen
CoverageLedger 0.3 wire shape, canonical ordering, and digest materialization.
No symbol in this module is exported from the public package.
"""

from __future__ import annotations

import copy
import json
import threading
from enum import Enum
from typing import Any, Mapping, Sequence

from veritrail_review import _fact_to_coverage_exact_input_handoff as handoff
from veritrail_review._fact_fulfillment import OwnedProductFactClosure
from veritrail_review._language_support import classify_language_support
from veritrail_review._review_coverage_ledger_conformance import (
    ITEM_KIND_ORDER,
    LEDGER_DIGEST_DOMAIN,
    REASON_ORDER,
    ROOT_BINDING_DOMAIN,
    ROOT_BINDING_FUNCTION,
    ROOT_CHAIN_DOMAIN,
    STAGE_ORDER,
    TERMINAL_HISTORY_DOMAIN,
    bind_coverage_ledger_conformance_source,
    validate_review_coverage_ledger,
)
from veritrail_review.budget import BudgetContext, BudgetState, OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


INPUT_CONSUMER = "r1-negative-world-coverage-exact-input-consumer/0.1"
COMPOSITION_FUNCTION = "r1-negative-world-review-coverage-composition/0.1"
VALIDATION_FUNCTION = (
    "r1-negative-world-review-coverage-independent-validation/0.1"
)
ADMISSION_FUNCTION = "r1-negative-world-review-coverage-admission/0.1"
RELATION_ABSENCE_FUNCTION = (
    "r1-negative-world-relation-set-predecessor-absence/0.1"
)
SLICE_ABSENCE_FUNCTION = (
    "r1-negative-world-review-slice-set-predecessor-absence/0.1"
)
UNREPRESENTABLE_OBLIGATION_DOMAIN = (
    "veritrail.review.negative-world-unrepresentable-fact-obligation/0.1"
)
FACT_SOURCE_DOMAIN = "veritrail.review.fact-handoff-source/0.1"

_NEGATIVE_BRANCHES = frozenset(
    {
        "ZERO_PARSE_DENOMINATOR",
        "ALL_PARSE_REJECTED",
        "PROJECTION_BLOCKED",
        "REQUIRED_PROVIDER_NON_SUCCESS",
    }
)
_DISPOSITION_FIELDS = (
    "out_of_scope",
    "unsupported",
    "unresolved",
    "conflicts",
    "parse_failed",
    "execution_failed",
    "truncated",
    "blocked",
)
_UPSTREAM_STAGE = {
    "SNAPSHOT_INVENTORY": None,
    "POLICY_SCOPE": "SNAPSHOT_INVENTORY",
    "LANGUAGE_SUPPORT": "POLICY_SCOPE",
    "PARSE": "LANGUAGE_SUPPORT",
    "FACT_DERIVATION": "PARSE",
    "RELATION_DERIVATION": "FACT_DERIVATION",
    "SLICE_DERIVATION": "RELATION_DERIVATION",
}
_ATTEMPT_TOKEN = object()
_VALIDATION_TOKEN = object()
_ADMISSION_TOKEN = object()
_REASON_RANK = {value: index for index, value in enumerate(REASON_ORDER)}


class NegativeWorldCoverageFailureCode(str, Enum):
    NEGATIVE_INPUT_REJECTED = "NEGATIVE_INPUT_REJECTED"
    NEGATIVE_INPUT_ALREADY_CONSUMED = "NEGATIVE_INPUT_ALREADY_CONSUMED"
    UNSUPPORTED_TERMINAL_BRANCH = "UNSUPPORTED_TERMINAL_BRANCH"
    DENOMINATOR_DERIVATION_REJECTED = "DENOMINATOR_DERIVATION_REJECTED"
    FACT_OBLIGATION_BINDING_REJECTED = "FACT_OBLIGATION_BINDING_REJECTED"
    ROOT_PROJECTION_REJECTED = "ROOT_PROJECTION_REJECTED"
    CANDIDATE_RECONCILIATION_REJECTED = (
        "CANDIDATE_RECONCILIATION_REJECTED"
    )
    INDEPENDENT_VALIDATION_REJECTED = "INDEPENDENT_VALIDATION_REJECTED"
    SAME_ATTEMPT_ADMISSION_REJECTED = "SAME_ATTEMPT_ADMISSION_REJECTED"


class NegativeWorldCoverageError(ValueError):
    """Typed fail-closed result from the private negative-world seam."""

    def __init__(self, code: NegativeWorldCoverageFailureCode) -> None:
        self.code = code
        super().__init__(code.value)


class _NegativeWorldDerivationError(ValueError):
    """Internal ownership marker for one frozen derivation boundary."""

    def __init__(self, code: NegativeWorldCoverageFailureCode) -> None:
        self.code = code
        super().__init__(code.value)


def _item_ref(kind: str, value: str) -> dict[str, str]:
    if kind not in ITEM_KIND_ORDER or type(value) is not str or not value:
        raise ValueError
    return {"item_id": value, "item_kind": kind}


def _item_key(value: Mapping[str, Any]) -> tuple[int, bytes]:
    return ITEM_KIND_ORDER[value["item_kind"]], value["item_id"].encode("utf-8")


def _sorted_refs(values: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    owned = [copy.deepcopy(dict(value)) for value in values]
    owned.sort(key=_item_key)
    if len({canonical_json_bytes(value) for value in owned}) != len(owned):
        raise ValueError
    return owned


def _sorted_dispositions(
    values: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    owned = [copy.deepcopy(dict(value)) for value in values]
    for value in owned:
        reasons = value.get("reason_codes")
        if not isinstance(reasons, list) or any(
            reason not in _REASON_RANK for reason in reasons
        ):
            raise ValueError
        value["reason_codes"] = sorted(set(reasons), key=_REASON_RANK.__getitem__)
    owned.sort(
        key=lambda value: (
            *_item_key(value["item_ref"]),
            tuple(_REASON_RANK[reason] for reason in value["reason_codes"]),
            canonical_json_bytes(value),
        )
    )
    if len({canonical_json_bytes(value["item_ref"]) for value in owned}) != len(
        owned
    ):
        raise ValueError
    return owned


def _producer_known_stage(
    stage: str,
    source_payload: object,
    denominator_refs: Sequence[Mapping[str, Any]],
    eligible_refs: Sequence[Mapping[str, Any]],
    completed_refs: Sequence[Mapping[str, Any]],
    *,
    dispositions: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
) -> dict[str, Any]:
    if stage not in STAGE_ORDER:
        raise ValueError
    denominator = _sorted_refs(denominator_refs)
    eligible = _sorted_refs(eligible_refs)
    completed = _sorted_refs(completed_refs)
    supplied = dispositions or {}
    carriers = {
        field: _sorted_dispositions(supplied.get(field, ()))
        for field in _DISPOSITION_FIELDS
    }
    reasons = sorted(
        {
            reason
            for values in carriers.values()
            for value in values
            for reason in value["reason_codes"]
        },
        key=_REASON_RANK.__getitem__,
    )
    has_gap = any(carriers.values())
    return {
        "stage": stage,
        "upstream_stage": _UPSTREAM_STAGE[stage],
        "denominator": {
            "state": "KNOWN",
            "source_digest": semantic_digest(
                f"veritrail.review.coverage-stage-source/{stage.lower()}/0.1",
                source_payload,
            ),
            "item_refs": denominator,
        },
        "eligible": eligible,
        "completed": completed,
        **carriers,
        "frontier": [],
        "reason_codes": reasons,
        "coverage_status": "PARTIAL" if has_gap else "COMPLETE",
    }


def _producer_unknown_stage(stage: str) -> dict[str, Any]:
    if stage not in {"RELATION_DERIVATION", "SLICE_DERIVATION"}:
        raise ValueError
    return {
        "stage": stage,
        "upstream_stage": _UPSTREAM_STAGE[stage],
        "denominator": {
            "state": "UNKNOWN",
            "source_digest": None,
            "known_item_refs": [],
            "reason_codes": ["UPSTREAM_DENOMINATOR_UNKNOWN"],
        },
        "eligible": [],
        "completed": [],
        **{field: [] for field in _DISPOSITION_FIELDS},
        "frontier": [],
        "reason_codes": ["UPSTREAM_DENOMINATOR_UNKNOWN"],
        "coverage_status": "UNKNOWN",
    }


def _producer_history_projection(
    stage: str,
    branch: str,
    function: str,
    source_digest: str,
    history: Mapping[str, object],
) -> dict[str, Any]:
    return {
        "projection_identity": TERMINAL_HISTORY_DOMAIN,
        "stage": stage,
        "terminal_branch": branch,
        "producing_function": function,
        "same_attempt_source": source_digest,
        "completion_state": "COMPLETE",
        "history": [
            {"name": name, "value": copy.deepcopy(history[name])}
            for name in sorted(history)
        ],
    }


def _producer_materialize_root_chain(
    projections: Sequence[Mapping[str, Any]], source_digest: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    owned = [copy.deepcopy(dict(value)) for value in projections]
    bindings: list[dict[str, Any]] = []
    predecessor = source_digest
    for projection in owned:
        terminal = projection["terminal_history_projection"]
        for member in terminal["history"]:
            if member["name"] == "predecessor_binding":
                member["value"] = predecessor
        binding = copy.deepcopy(projection)
        binding["terminal_history_digest"] = semantic_digest(
            TERMINAL_HISTORY_DOMAIN, terminal
        )
        binding["predecessor_binding_digest"] = predecessor
        binding["binding_digest"] = semantic_digest(ROOT_BINDING_DOMAIN, binding)
        bindings.append(binding)
        predecessor = binding["binding_digest"]
    payload = {
        "root_binding_function": ROOT_BINDING_FUNCTION,
        "root_chain_domain": ROOT_CHAIN_DOMAIN,
        "root_bindings": bindings,
    }
    return owned, bindings, semantic_digest(ROOT_CHAIN_DOMAIN, payload)


def _producer_overall(stages: Sequence[Mapping[str, Any]]) -> str:
    statuses = [stage["coverage_status"] for stage in stages]
    return (
        "UNKNOWN"
        if "UNKNOWN" in statuses
        else "PARTIAL"
        if "PARTIAL" in statuses
        else "COMPLETE"
    )


class ClaimedNegativeWorldCoverageAttempt:
    """One consumed carrier and its same-object-graph negative attempt."""

    def __init__(
        self,
        *,
        carrier: handoff.ClaimedFactToCoverageExactInputHandoff,
        source: Mapping[str, object],
        inputs: DerivationInputSet,
        context: BudgetContext,
        closure: OwnedProductFactClosure,
        carrier_claim_id: str,
        _token: object,
    ) -> None:
        if (
            _token is not _ATTEMPT_TOKEN
            or type(carrier)
            is not handoff.ClaimedFactToCoverageExactInputHandoff
            or type(inputs) is not DerivationInputSet
            or type(context) is not BudgetContext
            or type(closure) is not OwnedProductFactClosure
            or type(carrier_claim_id) is not str
            or not carrier_claim_id
        ):
            raise NegativeWorldCoverageError(
                NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
            )
        self.__lock = threading.RLock()
        self.__carrier = carrier
        self.__bound_carrier = carrier
        self.__inputs = inputs
        self.__bound_inputs = inputs
        self.__context = context
        self.__bound_context = context
        self.__closure = closure
        self.__bound_closure = closure
        self.__carrier_claim_id = carrier_claim_id
        self.__source_bytes = canonical_json_bytes(dict(source))
        self.__identity_bytes = canonical_json_bytes(carrier.input_identity_copy())
        self.__snapshot_bytes = canonical_json_bytes(
            carrier.source_snapshot_document_copy()
        )
        self.__policy_bytes = canonical_json_bytes(
            carrier.review_policy_document_copy()
        )
        self.__profile_bytes = canonical_json_bytes(
            carrier.derivation_profile_document_copy()
        )
        self.__blob_bytes = carrier.verified_blob_bytes_copy()
        self.__budget_identity = (
            context.limits,
            context.started_at_monotonic,
            context.execution_deadline_monotonic,
        )
        self.__failed = False
        self.__admission_attempted = False
        self.__phase: OwnedPhaseResult | None = None
        self.__admitted_candidate_bytes: bytes | None = None
        self._validate_live()

    def __copy__(self):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
        )

    def __deepcopy__(self, _memo):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
        )

    def _revoke(self) -> None:
        self.__failed = True
        try:
            self.__closure._revoke_handoff_source()
        except Exception:
            pass

    def _raise(
        self,
        code: NegativeWorldCoverageFailureCode,
        *,
        preserve_admitted: bool = False,
    ) -> None:
        if not (preserve_admitted and self.__phase is not None):
            self._revoke()
        raise NegativeWorldCoverageError(code)

    def _validate_live(self) -> None:
        try:
            if (
                self.__failed
                or self.__carrier is not self.__bound_carrier
                or self.__inputs is not self.__bound_inputs
                or self.__context is not self.__bound_context
                or self.__closure is not self.__bound_closure
                or (
                    self.__context.limits,
                    self.__context.started_at_monotonic,
                    self.__context.execution_deadline_monotonic,
                )
                != self.__budget_identity
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or not self.__context.checkpoint()
                or canonical_json_bytes(self.__carrier.fact_terminal_source_copy())
                != self.__source_bytes
                or canonical_json_bytes(self.__carrier.input_identity_copy())
                != self.__identity_bytes
                or canonical_json_bytes(
                    self.__carrier.source_snapshot_document_copy()
                )
                != self.__snapshot_bytes
                or canonical_json_bytes(
                    self.__carrier.review_policy_document_copy()
                )
                != self.__policy_bytes
                or canonical_json_bytes(
                    self.__carrier.derivation_profile_document_copy()
                )
                != self.__profile_bytes
                or self.__carrier.verified_blob_bytes_copy() != self.__blob_bytes
            ):
                raise ValueError
        except Exception as exc:
            self._revoke()
            raise NegativeWorldCoverageError(
                NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
            ) from exc

    def _original_world(self):
        with self.__lock:
            self._validate_live()
            return (
                json.loads(self.__source_bytes),
                self.__inputs,
                json.loads(self.__snapshot_bytes),
                json.loads(self.__policy_bytes),
                json.loads(self.__profile_bytes),
                json.loads(self.__identity_bytes),
            )

    def _claim_id(self) -> str:
        return self.__carrier_claim_id

    def _admit(
        self,
        candidate: Mapping[str, Any],
        validation: "NegativeWorldCoverageValidation",
    ) -> "AdmittedNegativeWorldCoverage":
        with self.__lock:
            self._validate_live()
            if self.__admission_attempted:
                self._raise(
                    NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED,
                    preserve_admitted=True,
                )
            self.__admission_attempted = True
            try:
                if (
                    type(validation) is not NegativeWorldCoverageValidation
                    or validation._attempt is not self
                ):
                    raise ValueError
                candidate_bytes = canonical_json_bytes(dict(candidate))
                validation._validate_binding(candidate_bytes)
                phase = self.__context.try_complete_phase(
                    candidate_bytes, resources_closed=True
                )
                if phase is None or phase.canonical_bytes != candidate_bytes:
                    raise ValueError
                self.__phase = phase
                self.__admitted_candidate_bytes = candidate_bytes
                return AdmittedNegativeWorldCoverage(
                    attempt=self,
                    validation=validation,
                    phase=phase,
                    candidate_bytes=candidate_bytes,
                    _token=_ADMISSION_TOKEN,
                )
            except NegativeWorldCoverageError as exc:
                self._revoke()
                raise NegativeWorldCoverageError(
                    NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
                ) from exc
            except Exception as exc:
                self._revoke()
                raise NegativeWorldCoverageError(
                    NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
                ) from exc

    def _validate_admitted(
        self,
        phase: OwnedPhaseResult,
        candidate_bytes: bytes,
        validation: "NegativeWorldCoverageValidation",
    ) -> None:
        with self.__lock:
            self._validate_live()
            if (
                self.__phase is not phase
                or self.__admitted_candidate_bytes is not candidate_bytes
                or phase.canonical_bytes != candidate_bytes
                or validation._attempt is not self
            ):
                self._raise(
                    NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
                )
            try:
                validation._validate_binding(candidate_bytes)
            except NegativeWorldCoverageError:
                self._raise(
                    NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
                )


class NegativeWorldCoverageValidation:
    """Unforgeable binding between one attempt and one validated candidate."""

    def __init__(
        self,
        *,
        attempt: ClaimedNegativeWorldCoverageAttempt,
        candidate_bytes: bytes,
        source_digest: str,
        _token: object,
    ) -> None:
        if (
            _token is not _VALIDATION_TOKEN
            or type(attempt) is not ClaimedNegativeWorldCoverageAttempt
            or type(candidate_bytes) is not bytes
            or type(source_digest) is not str
        ):
            raise NegativeWorldCoverageError(
                NegativeWorldCoverageFailureCode.INDEPENDENT_VALIDATION_REJECTED
            )
        self._attempt = attempt
        self.__candidate_bytes = candidate_bytes
        self.__source_digest = source_digest
        self.__document_bytes = canonical_json_bytes(
            {
                "validation_function": VALIDATION_FUNCTION,
                "carrier_claim_id": attempt._claim_id(),
                "candidate_digest": json.loads(candidate_bytes)[
                    "coverage_ledger_digest"
                ],
                "fact_handoff_source_digest": source_digest,
                "result": "VALIDATED",
            }
        )
        self.__bound_document_bytes = self.__document_bytes

    def __copy__(self):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.INDEPENDENT_VALIDATION_REJECTED
        )

    def __deepcopy__(self, _memo):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.INDEPENDENT_VALIDATION_REJECTED
        )

    def _validate_binding(self, candidate_bytes: bytes) -> None:
        self._attempt._validate_live()
        if (
            self.__document_bytes is not self.__bound_document_bytes
            or candidate_bytes != self.__candidate_bytes
        ):
            raise NegativeWorldCoverageError(
                NegativeWorldCoverageFailureCode.INDEPENDENT_VALIDATION_REJECTED
            )

    def document_copy(self) -> dict[str, Any]:
        self._validate_binding(self.__candidate_bytes)
        return json.loads(self.__document_bytes)


class AdmittedNegativeWorldCoverage:
    """Private admitted Coverage result with a strict authority ceiling."""

    def __init__(
        self,
        *,
        attempt: ClaimedNegativeWorldCoverageAttempt,
        validation: NegativeWorldCoverageValidation,
        phase: OwnedPhaseResult,
        candidate_bytes: bytes,
        _token: object,
    ) -> None:
        if (
            _token is not _ADMISSION_TOKEN
            or type(attempt) is not ClaimedNegativeWorldCoverageAttempt
            or type(validation) is not NegativeWorldCoverageValidation
            or type(phase) is not OwnedPhaseResult
            or type(candidate_bytes) is not bytes
        ):
            raise NegativeWorldCoverageError(
                NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
            )
        self.__attempt = attempt
        self.__validation = validation
        self.__phase = phase
        self.__candidate_bytes = candidate_bytes
        self.__bound_candidate_bytes = candidate_bytes
        attempt._validate_admitted(phase, candidate_bytes, validation)

    def __copy__(self):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
        )

    def __deepcopy__(self, _memo):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
        )

    def coverage_ledger_document_copy(self) -> dict[str, Any]:
        self.__attempt._validate_admitted(
            self.__phase, self.__candidate_bytes, self.__validation
        )
        if self.__candidate_bytes is not self.__bound_candidate_bytes:
            raise NegativeWorldCoverageError(
                NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
            )
        return json.loads(self.__candidate_bytes)

    def authority_ceiling_copy(self) -> dict[str, bool]:
        self.coverage_ledger_document_copy()
        return {
            "private_negative_world_coverage_ledger": True,
            "fact_set": False,
            "relation_set": False,
            "review_slice_set": False,
            "positive_composition": False,
            "manifest": False,
            "evidence": False,
            "persistence": False,
            "public_review": False,
        }


def claim_negative_world_coverage_attempt(
    carrier: handoff.ClaimedFactToCoverageExactInputHandoff,
    *,
    input_consumer: str = INPUT_CONSUMER,
    composition_function: str = COMPOSITION_FUNCTION,
) -> ClaimedNegativeWorldCoverageAttempt:
    if (
        type(carrier) is not handoff.ClaimedFactToCoverageExactInputHandoff
        or input_consumer != INPUT_CONSUMER
        or composition_function != COMPOSITION_FUNCTION
    ):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
        )
    try:
        source = carrier.fact_terminal_source_copy()
        if source.get("branch") not in _NEGATIVE_BRANCHES:
            raise NegativeWorldCoverageError(
                NegativeWorldCoverageFailureCode.UNSUPPORTED_TERMINAL_BRANCH
            )
        source, inputs, context, closure, claim_id = (
            carrier._consume_negative_world_authority(
                _token=handoff._NEGATIVE_WORLD_CONSUMER_TOKEN
            )
        )
        return ClaimedNegativeWorldCoverageAttempt(
            carrier=carrier,
            source=source,
            inputs=inputs,
            context=context,
            closure=closure,
            carrier_claim_id=claim_id,
            _token=_ATTEMPT_TOKEN,
        )
    except NegativeWorldCoverageError:
        raise
    except handoff.FactToCoverageExactInputHandoffError as exc:
        try:
            carrier.fact_terminal_source_copy()
        except Exception:
            code = NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
        else:
            code = (
                NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_ALREADY_CONSUMED
            )
        raise NegativeWorldCoverageError(
            code
        ) from exc
    except Exception as exc:
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
        ) from exc


def _producer_fact_partition(
    source: Mapping[str, Any], carrier_identity: Mapping[str, Any]
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, Any],
]:
    projection = source["fact_projection"]
    universe = projection.get("universe")
    expected = projection.get("expected")
    blockers = projection.get("blockers", [])
    if not all(isinstance(value, list) for value in (universe, expected, blockers)):
        raise ValueError
    slots: dict[str, dict[str, Any]] = {}
    for slot in universe:
        key = slot["subject_key_digest"]
        if type(key) is not str or key in slots:
            raise ValueError
        slots[key] = copy.deepcopy(slot)
    expected_by_slot: dict[str, dict[str, Any]] = {}
    for fact in expected:
        key = fact["subject_key_digest"]
        if key in expected_by_slot or type(fact.get("fact_id")) is not str:
            raise ValueError
        expected_by_slot[key] = copy.deepcopy(fact)
    blocker_by_slot: dict[str, dict[str, Any]] = {}
    for blocker in blockers:
        if blocker.get("reason") != "UNREPRESENTABLE_EXPECTED_FACT":
            raise ValueError
        key = blocker["slot"]["subject_key_digest"]
        if key in blocker_by_slot or blocker["slot"] != slots.get(key):
            raise ValueError
        canonical_json_bytes(blocker["candidate"])
        blocker_by_slot[key] = copy.deepcopy(blocker)
    if set(slots) != set(expected_by_slot) | set(blocker_by_slot) or set(
        expected_by_slot
    ) & set(blocker_by_slot):
        raise ValueError

    refs_by_slot: dict[str, dict[str, Any]] = {}
    for key in sorted(slots):
        if key in expected_by_slot:
            refs_by_slot[key] = _item_ref("FACT", expected_by_slot[key]["fact_id"])
        else:
            refs_by_slot[key] = _item_ref(
                "FACT",
                semantic_digest(
                    UNREPRESENTABLE_OBLIGATION_DOMAIN,
                    {
                        "input_identity": copy.deepcopy(carrier_identity),
                        "slot": slots[key],
                        "candidate": blocker_by_slot[key]["candidate"],
                    },
                ),
            )
    if len({value["item_id"] for value in refs_by_slot.values()}) != len(
        refs_by_slot
    ):
        raise ValueError
    denominator = _sorted_refs(list(refs_by_slot.values()))
    completed: list[dict[str, Any]] = []
    dispositions = {field: [] for field in _DISPOSITION_FIELDS}
    details: dict[str, Any] = {
        "blockers": copy.deepcopy(blockers),
        "provider_outcomes": [],
        "provider_responsibility": [],
    }
    branch = source["branch"]
    if branch in {"ZERO_PARSE_DENOMINATOR", "ALL_PARSE_REJECTED"}:
        if denominator or expected or blockers:
            raise ValueError
    elif branch == "PROJECTION_BLOCKED":
        if not blocker_by_slot:
            raise ValueError
        completed = _sorted_refs(
            [refs_by_slot[key] for key in expected_by_slot]
        )
        dispositions["blocked"] = [
            {
                "item_ref": refs_by_slot[key],
                "reason_codes": ["UNREPRESENTABLE_EXPECTED_FACT"],
                "disposition_family": "SEMANTIC_PROJECTION_BLOCKER",
            }
            for key in blocker_by_slot
        ]
    elif branch == "REQUIRED_PROVIDER_NON_SUCCESS":
        if blockers:
            raise ValueError
        expected_by_id = {
            value["fact_id"]: value for value in expected_by_slot.values()
        }
        completed_ids: set[str] = set()
        providers = source.get("provider_history")
        if not isinstance(providers, list):
            raise ValueError
        responsibility_by_subject: dict[str, list[dict[str, str]]] = {}
        outcomes = []
        for provider in providers:
            provider_id = provider["descriptor"]["provider_id"]
            lifecycle = provider["lifecycle"]
            assigned = []
            request = provider.get("request")
            if isinstance(request, Mapping):
                assigned = [
                    value["subject_identity"]
                    for value in request["projection"]["assigned_products"]
                ]
            provider_fact_ids = []
            canonical_fact_hex = provider.get("canonical_fact_bytes_hex", [])
            if not isinstance(canonical_fact_hex, list) or (
                lifecycle != "COMPLETED" and canonical_fact_hex
            ):
                raise ValueError
            for encoded in canonical_fact_hex:
                raw = bytes.fromhex(encoded)
                fact = json.loads(raw)
                if canonical_json_bytes(fact) != raw:
                    raise ValueError
                fact_id = fact.get("fact_id")
                semantic_fact = {
                    key: value
                    for key, value in fact.items()
                    if key != "provenance_refs"
                }
                if (
                    fact_id not in expected_by_id
                    or semantic_fact != expected_by_id[fact_id]
                ):
                    raise ValueError
                completed_ids.add(fact_id)
                provider_fact_ids.append(fact_id)
            outcomes.append(
                {
                    "provider": provider_id,
                    "required": provider["required"],
                    "state": lifecycle,
                    "assigned_subject_identities": sorted(set(assigned)),
                    "completed_fact_ids": sorted(set(provider_fact_ids)),
                }
            )
            if provider["required"] and lifecycle in {"FAILED", "UNAVAILABLE"}:
                reason = (
                    "DERIVATION_ERROR"
                    if lifecycle == "FAILED"
                    else "PROVIDER_UNAVAILABLE"
                )
                for subject in assigned:
                    responsibility_by_subject.setdefault(subject, []).append(
                        {"provider": provider_id, "state": lifecycle, "reason": reason}
                    )
        completed = _sorted_refs(
            [_item_ref("FACT", value) for value in completed_ids]
        )
        responsibilities = []
        for key, fact in expected_by_slot.items():
            if fact["fact_id"] in completed_ids:
                continue
            providers = responsibility_by_subject.get(
                slots[key]["product_subject_identity"], []
            )
            if not providers:
                raise ValueError
            reasons = sorted(
                {value["reason"] for value in providers},
                key=_REASON_RANK.__getitem__,
            )
            dispositions["execution_failed"].append(
                {"item_ref": refs_by_slot[key], "reason_codes": reasons}
            )
            responsibilities.append(
                {
                    "item_ref": refs_by_slot[key],
                    "providers": sorted(
                        providers,
                        key=lambda value: (
                            value["provider"], value["state"], value["reason"]
                        ),
                    ),
                }
            )
        details["provider_outcomes"] = sorted(
            outcomes, key=lambda value: value["provider"]
        )
        details["provider_responsibility"] = sorted(
            responsibilities, key=lambda value: _item_key(value["item_ref"])
        )
    else:
        raise ValueError
    return denominator, completed, dispositions, details


def _producer_history(attempt: ClaimedNegativeWorldCoverageAttempt):
    source, inputs, snapshot, policy, _profile, identity = attempt._original_world()
    classification = classify_language_support(inputs).classification_document_copy()
    inventory = snapshot.get("inventory")
    decisions = policy.get("scope_decisions")
    subjects = classification.get("subjects")
    if (
        not isinstance(inventory, list)
        or not isinstance(decisions, list)
        or len(inventory) != len(decisions)
        or not isinstance(subjects, list)
    ):
        raise ValueError
    inventory_refs = [
        _item_ref(
            "INVENTORY_ENTRY",
            semantic_digest("veritrail.review.coverage-inventory-entry/0.1", item),
        )
        for item in inventory
    ]
    decision_by_path: dict[bytes, Mapping[str, Any]] = {}
    for decision in decisions:
        path_key = canonical_json_bytes(decision["git_path"])
        if path_key in decision_by_path:
            raise ValueError
        decision_by_path[path_key] = decision
    policy_eligible = []
    policy_out = []
    for item, ref in zip(inventory, inventory_refs, strict=True):
        decision = decision_by_path.pop(
            canonical_json_bytes(item["git_path"]), None
        )
        if decision is None:
            raise ValueError
        if decision.get("disposition") == "IN_SCOPE":
            policy_eligible.append(ref)
        else:
            policy_out.append(
                {"item_ref": ref, "reason_codes": ["POLICY_EXCLUDED"]}
            )
    if decision_by_path:
        raise ValueError
    language_refs = {
        subject["subject_identity"]: _item_ref(
            "PARSE_UNIT", subject["subject_identity"]
        )
        for subject in subjects
    }
    if len(language_refs) != len(subjects):
        raise ValueError
    language_eligible = [
        language_refs[subject["subject_identity"]]
        for subject in subjects
        if subject.get("disposition") == "ELIGIBLE"
    ]
    language_unsupported = [
        {
            "item_ref": language_refs[subject["subject_identity"]],
            "reason_codes": list(subject["reason_codes"]),
        }
        for subject in subjects
        if subject.get("disposition") != "ELIGIBLE"
    ]
    parse = source["parse_partition"]
    projection_parse = source["fact_projection"].get("parse_partition")
    if projection_parse is not None and canonical_json_bytes(
        projection_parse
    ) != canonical_json_bytes(parse):
        raise ValueError
    denominator_ids = list(parse["denominator"])
    if set(denominator_ids) != {
        value["item_id"] for value in language_eligible
    } or len(denominator_ids) != len(set(denominator_ids)):
        raise ValueError
    accepted_ids = [value["subject_identity"] for value in parse["accepted"]]
    rejected_ids = [value["subject_identity"] for value in parse["rejected"]]
    if (
        set(accepted_ids) | set(rejected_ids) != set(denominator_ids)
        or set(accepted_ids) & set(rejected_ids)
        or len(accepted_ids) != len(set(accepted_ids))
        or len(rejected_ids) != len(set(rejected_ids))
    ):
        raise ValueError
    parse_refs = {value: _item_ref("PARSE_UNIT", value) for value in denominator_ids}
    try:
        fact_u, fact_e, fact_dispositions, fact_details = (
            _producer_fact_partition(source, identity)
        )
    except Exception as exc:
        raise _NegativeWorldDerivationError(
            NegativeWorldCoverageFailureCode.FACT_OBLIGATION_BINDING_REJECTED
        ) from exc
    stages = [
        _producer_known_stage(
            "SNAPSHOT_INVENTORY",
            snapshot,
            inventory_refs,
            inventory_refs,
            inventory_refs,
        ),
        _producer_known_stage(
            "POLICY_SCOPE",
            policy,
            inventory_refs,
            policy_eligible,
            policy_eligible,
            dispositions={"out_of_scope": policy_out},
        ),
        _producer_known_stage(
            "LANGUAGE_SUPPORT",
            classification,
            list(language_refs.values()),
            language_eligible,
            language_eligible,
            dispositions={"unsupported": language_unsupported},
        ),
        _producer_known_stage(
            "PARSE",
            parse,
            list(parse_refs.values()),
            list(parse_refs.values()),
            [parse_refs[value] for value in accepted_ids],
            dispositions={
                "parse_failed": [
                    {
                        "item_ref": parse_refs[value],
                        "reason_codes": ["PARSE_ERROR"],
                    }
                    for value in rejected_ids
                ]
            },
        ),
        _producer_known_stage(
            "FACT_DERIVATION",
            source["fact_projection"],
            fact_u,
            fact_u,
            fact_e,
            dispositions=fact_dispositions,
        ),
    ]
    downstream_unknown = source["branch"] in {
        "PROJECTION_BLOCKED",
        "REQUIRED_PROVIDER_NON_SUCCESS",
    }
    if downstream_unknown:
        stages.extend(
            [
                _producer_unknown_stage("RELATION_DERIVATION"),
                _producer_unknown_stage("SLICE_DERIVATION"),
            ]
        )
    else:
        stages.extend(
            [
                _producer_known_stage(
                    "RELATION_DERIVATION",
                    {"fact_branch": source["branch"], "known_empty": True},
                    [],
                    [],
                    [],
                ),
                _producer_known_stage(
                    "SLICE_DERIVATION",
                    {"fact_branch": source["branch"], "known_empty": True},
                    [],
                    [],
                    [],
                ),
            ]
        )
    source_digest = semantic_digest(FACT_SOURCE_DOMAIN, source)
    fact_history = {
        "absence": {"branch": source["branch"], "qualified": True},
        "blockers": fact_details["blockers"],
        "denominator": copy.deepcopy(stages[4]["denominator"]),
        "e": fact_e,
        "u": fact_u,
    }
    if source["branch"] == "ALL_PARSE_REJECTED":
        fact_history["rejected_parse_products"] = copy.deepcopy(parse["rejected"])
    if source["branch"] == "REQUIRED_PROVIDER_NON_SUCCESS":
        fact_history["provider_outcomes"] = fact_details["provider_outcomes"]
        fact_history["provider_responsibility"] = fact_details[
            "provider_responsibility"
        ]
    roots = [
        {
            "stage": "FACT_SET",
            "binding_state": "QUALIFIED_ABSENT",
            "exact_absence": f"FACT_SET:{source['branch']}",
            "producing_function": source["fact_projection"]["function"],
            "terminal_branch": source["branch"],
            "terminal_history_projection": _producer_history_projection(
                "FACT_SET",
                source["branch"],
                source["fact_projection"]["function"],
                source_digest,
                fact_history,
            ),
        },
        {
            "stage": "RELATION_SET",
            "binding_state": "QUALIFIED_ABSENT",
            "exact_absence": "RELATION_SET:PREDECESSOR_ABSENT",
            "producing_function": RELATION_ABSENCE_FUNCTION,
            "terminal_branch": "PREDECESSOR_ABSENT",
            "terminal_history_projection": _producer_history_projection(
                "RELATION_SET",
                "PREDECESSOR_ABSENT",
                RELATION_ABSENCE_FUNCTION,
                source_digest,
                {
                    "absence": {"branch": "PREDECESSOR_ABSENT", "qualified": True},
                    "predecessor_binding": None,
                    "transition": source["branch"],
                },
            ),
        },
        {
            "stage": "REVIEW_SLICE_SET",
            "binding_state": "QUALIFIED_ABSENT",
            "exact_absence": "REVIEW_SLICE_SET:PREDECESSOR_ABSENT",
            "producing_function": SLICE_ABSENCE_FUNCTION,
            "terminal_branch": "PREDECESSOR_ABSENT",
            "terminal_history_projection": _producer_history_projection(
                "REVIEW_SLICE_SET",
                "PREDECESSOR_ABSENT",
                SLICE_ABSENCE_FUNCTION,
                source_digest,
                {
                    "absence": {"branch": "PREDECESSOR_ABSENT", "qualified": True},
                    "predecessor_binding": None,
                    "transition": source["branch"],
                },
            ),
        },
    ]
    try:
        roots, bindings, chain_digest = _producer_materialize_root_chain(
            roots, source_digest
        )
    except Exception as exc:
        raise _NegativeWorldDerivationError(
            NegativeWorldCoverageFailureCode.ROOT_PROJECTION_REJECTED
        ) from exc
    return inputs, roots, bindings, stages, source_digest, chain_digest


def produce_negative_world_coverage_candidate(
    attempt: ClaimedNegativeWorldCoverageAttempt,
    *,
    composition_function: str = COMPOSITION_FUNCTION,
) -> dict[str, Any]:
    if (
        type(attempt) is not ClaimedNegativeWorldCoverageAttempt
        or composition_function != COMPOSITION_FUNCTION
    ):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED
        )
    try:
        inputs, _roots, bindings, stages, _source_digest, chain_digest = (
            _producer_history(attempt)
        )
        document = {
            "artifact_kind": "COVERAGE_LEDGER",
            "schema_version": "0.3",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "policy_digest": inputs.policy_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "slice_policy_digest": inputs.slice_policy_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            "root_binding_function": ROOT_BINDING_FUNCTION,
            "root_chain_domain": ROOT_CHAIN_DOMAIN,
            "root_bindings": bindings,
            "root_chain_digest": chain_digest,
            "stages": stages,
            "overall_coverage_status": _producer_overall(stages),
        }
        document["coverage_ledger_digest"] = semantic_digest(
            LEDGER_DIGEST_DOMAIN, document
        )
        return copy.deepcopy(document)
    except _NegativeWorldDerivationError as exc:
        attempt._revoke()
        raise NegativeWorldCoverageError(exc.code) from exc
    except NegativeWorldCoverageError:
        raise
    except Exception as exc:
        attempt._revoke()
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.DENOMINATOR_DERIVATION_REJECTED
        ) from exc


def _validator_known_stage(
    stage: str,
    source_payload: object,
    denominator_refs: Sequence[Mapping[str, Any]],
    eligible_refs: Sequence[Mapping[str, Any]],
    completed_refs: Sequence[Mapping[str, Any]],
    *,
    dispositions: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
) -> dict[str, Any]:
    if stage not in STAGE_ORDER:
        raise ValueError
    denominator = _sorted_refs(denominator_refs)
    eligible = _sorted_refs(eligible_refs)
    completed = _sorted_refs(completed_refs)
    supplied = dispositions or {}
    disposition_projection: dict[str, list[dict[str, Any]]] = {}
    all_reasons: set[str] = set()
    for field in _DISPOSITION_FIELDS:
        values = _sorted_dispositions(supplied.get(field, ()))
        disposition_projection[field] = values
        for value in values:
            all_reasons.update(value["reason_codes"])
    return {
        "stage": stage,
        "upstream_stage": _UPSTREAM_STAGE[stage],
        "denominator": {
            "state": "KNOWN",
            "source_digest": semantic_digest(
                f"veritrail.review.coverage-stage-source/{stage.lower()}/0.1",
                source_payload,
            ),
            "item_refs": denominator,
        },
        "eligible": eligible,
        "completed": completed,
        **disposition_projection,
        "frontier": [],
        "reason_codes": sorted(all_reasons, key=_REASON_RANK.__getitem__),
        "coverage_status": (
            "PARTIAL"
            if any(disposition_projection.values())
            else "COMPLETE"
        ),
    }


def _validator_unknown_stage(stage: str) -> dict[str, Any]:
    if stage not in {"RELATION_DERIVATION", "SLICE_DERIVATION"}:
        raise ValueError
    unknown_reason = "UPSTREAM_DENOMINATOR_UNKNOWN"
    return {
        "stage": stage,
        "upstream_stage": _UPSTREAM_STAGE[stage],
        "denominator": {
            "state": "UNKNOWN",
            "source_digest": None,
            "known_item_refs": [],
            "reason_codes": [unknown_reason],
        },
        "eligible": [],
        "completed": [],
        **{field: [] for field in _DISPOSITION_FIELDS},
        "frontier": [],
        "reason_codes": [unknown_reason],
        "coverage_status": "UNKNOWN",
    }


def _validator_history_projection(
    stage: str,
    branch: str,
    function: str,
    source_digest: str,
    history: Mapping[str, object],
) -> dict[str, Any]:
    members = []
    for name in sorted(history):
        members.append({"name": name, "value": copy.deepcopy(history[name])})
    return {
        "projection_identity": TERMINAL_HISTORY_DOMAIN,
        "stage": stage,
        "terminal_branch": branch,
        "producing_function": function,
        "same_attempt_source": source_digest,
        "completion_state": "COMPLETE",
        "history": members,
    }


def _validator_materialize_root_chain(
    projections: Sequence[Mapping[str, Any]], source_digest: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    owned = [copy.deepcopy(dict(value)) for value in projections]
    materialized: list[dict[str, Any]] = []
    previous_digest = source_digest
    for projection in owned:
        terminal_projection = projection["terminal_history_projection"]
        for member in terminal_projection["history"]:
            if member["name"] == "predecessor_binding":
                member["value"] = previous_digest
        binding = copy.deepcopy(projection)
        binding["terminal_history_digest"] = semantic_digest(
            TERMINAL_HISTORY_DOMAIN, terminal_projection
        )
        binding["predecessor_binding_digest"] = previous_digest
        binding["binding_digest"] = semantic_digest(
            ROOT_BINDING_DOMAIN, binding
        )
        materialized.append(binding)
        previous_digest = binding["binding_digest"]
    chain_payload = {
        "root_binding_function": ROOT_BINDING_FUNCTION,
        "root_chain_domain": ROOT_CHAIN_DOMAIN,
        "root_bindings": materialized,
    }
    return (
        owned,
        materialized,
        semantic_digest(ROOT_CHAIN_DOMAIN, chain_payload),
    )


def _validator_overall(stages: Sequence[Mapping[str, Any]]) -> str:
    status_set = {stage["coverage_status"] for stage in stages}
    if "UNKNOWN" in status_set:
        return "UNKNOWN"
    if "PARTIAL" in status_set:
        return "PARTIAL"
    return "COMPLETE"


def _validator_fact_partition(
    source: Mapping[str, Any], carrier_identity: Mapping[str, Any]
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, Any],
]:
    projection = source["fact_projection"]
    raw_universe = projection["universe"]
    raw_expected = projection["expected"]
    raw_blockers = projection.get("blockers", [])
    if not all(
        isinstance(value, list)
        for value in (raw_universe, raw_expected, raw_blockers)
    ):
        raise ValueError
    slot_index = {}
    for value in raw_universe:
        identifier = value.get("subject_key_digest")
        if type(identifier) is not str or identifier in slot_index:
            raise ValueError
        slot_index[identifier] = copy.deepcopy(value)
    fact_index = {}
    for value in raw_expected:
        identifier = value.get("subject_key_digest")
        if (
            identifier not in slot_index
            or identifier in fact_index
            or type(value.get("fact_id")) is not str
        ):
            raise ValueError
        fact_index[identifier] = copy.deepcopy(value)
    blocker_index = {}
    for value in raw_blockers:
        slot = value.get("slot")
        if not isinstance(slot, Mapping):
            raise ValueError
        identifier = slot.get("subject_key_digest")
        if (
            identifier not in slot_index
            or identifier in blocker_index
            or dict(slot) != slot_index[identifier]
            or value.get("reason") != "UNREPRESENTABLE_EXPECTED_FACT"
        ):
            raise ValueError
        canonical_json_bytes(value["candidate"])
        blocker_index[identifier] = copy.deepcopy(value)
    if (
        set(slot_index) != set(fact_index).union(blocker_index)
        or set(fact_index).intersection(blocker_index)
    ):
        raise ValueError
    reference_index = {}
    for identifier in sorted(slot_index):
        if identifier in fact_index:
            reference_index[identifier] = _item_ref(
                "FACT", fact_index[identifier]["fact_id"]
            )
        else:
            reference_index[identifier] = _item_ref(
                "FACT",
                semantic_digest(
                    UNREPRESENTABLE_OBLIGATION_DOMAIN,
                    {
                        "input_identity": copy.deepcopy(carrier_identity),
                        "slot": slot_index[identifier],
                        "candidate": blocker_index[identifier]["candidate"],
                    },
                ),
            )
    if len({value["item_id"] for value in reference_index.values()}) != len(
        reference_index
    ):
        raise ValueError
    universe_refs = _sorted_refs(list(reference_index.values()))
    completed_refs: list[dict[str, Any]] = []
    stage_dispositions = {field: [] for field in _DISPOSITION_FIELDS}
    history_details: dict[str, Any] = {
        "blockers": copy.deepcopy(raw_blockers),
        "provider_outcomes": [],
        "provider_responsibility": [],
    }
    terminal_branch = source["branch"]
    if terminal_branch in {"ZERO_PARSE_DENOMINATOR", "ALL_PARSE_REJECTED"}:
        if universe_refs or raw_expected or raw_blockers:
            raise ValueError
    elif terminal_branch == "PROJECTION_BLOCKED":
        if not blocker_index:
            raise ValueError
        completed_refs = _sorted_refs(
            [reference_index[value] for value in fact_index]
        )
        stage_dispositions["blocked"] = [
            {
                "item_ref": reference_index[value],
                "reason_codes": ["UNREPRESENTABLE_EXPECTED_FACT"],
                "disposition_family": "SEMANTIC_PROJECTION_BLOCKER",
            }
            for value in blocker_index
        ]
    elif terminal_branch == "REQUIRED_PROVIDER_NON_SUCCESS":
        if raw_blockers:
            raise ValueError
        expected_ids = {
            value["fact_id"]: value for value in fact_index.values()
        }
        observed_ids: set[str] = set()
        non_success_by_subject: dict[str, list[dict[str, str]]] = {}
        outcome_projection = []
        provider_history = source["provider_history"]
        if not isinstance(provider_history, list):
            raise ValueError
        for run in provider_history:
            descriptor = run.get("descriptor")
            if not isinstance(descriptor, Mapping):
                raise ValueError
            provider_name = descriptor.get("provider_id")
            lifecycle = run.get("lifecycle")
            request = run.get("request")
            assigned_subjects: list[str] = []
            if isinstance(request, Mapping):
                projection_value = request.get("projection")
                if not isinstance(projection_value, Mapping):
                    raise ValueError
                assigned_products = projection_value.get("assigned_products")
                if not isinstance(assigned_products, list):
                    raise ValueError
                assigned_subjects = [
                    value["subject_identity"] for value in assigned_products
                ]
            run_fact_ids = []
            canonical_fact_hex = run.get("canonical_fact_bytes_hex", [])
            if not isinstance(canonical_fact_hex, list) or (
                lifecycle != "COMPLETED" and canonical_fact_hex
            ):
                raise ValueError
            for encoded in canonical_fact_hex:
                fact_bytes = bytes.fromhex(encoded)
                fact_document = json.loads(fact_bytes)
                if canonical_json_bytes(fact_document) != fact_bytes:
                    raise ValueError
                fact_identifier = fact_document.get("fact_id")
                semantic_fact = {
                    key: value
                    for key, value in fact_document.items()
                    if key != "provenance_refs"
                }
                if (
                    fact_identifier not in expected_ids
                    or semantic_fact != expected_ids[fact_identifier]
                ):
                    raise ValueError
                observed_ids.add(fact_identifier)
                run_fact_ids.append(fact_identifier)
            outcome_projection.append(
                {
                    "provider": provider_name,
                    "required": run.get("required"),
                    "state": lifecycle,
                    "assigned_subject_identities": sorted(set(assigned_subjects)),
                    "completed_fact_ids": sorted(set(run_fact_ids)),
                }
            )
            if run.get("required") is True and lifecycle in {"FAILED", "UNAVAILABLE"}:
                mapped_reason = (
                    "DERIVATION_ERROR"
                    if lifecycle == "FAILED"
                    else "PROVIDER_UNAVAILABLE"
                )
                for subject_identifier in assigned_subjects:
                    non_success_by_subject.setdefault(
                        subject_identifier, []
                    ).append(
                        {
                            "provider": provider_name,
                            "state": lifecycle,
                            "reason": mapped_reason,
                        }
                    )
        completed_refs = _sorted_refs(
            [_item_ref("FACT", value) for value in observed_ids]
        )
        responsibility_projection = []
        for identifier, fact_document in fact_index.items():
            if fact_document["fact_id"] in observed_ids:
                continue
            responsible = non_success_by_subject.get(
                slot_index[identifier]["product_subject_identity"], []
            )
            if not responsible:
                raise ValueError
            mapped_reasons = sorted(
                {value["reason"] for value in responsible},
                key=_REASON_RANK.__getitem__,
            )
            stage_dispositions["execution_failed"].append(
                {
                    "item_ref": reference_index[identifier],
                    "reason_codes": mapped_reasons,
                }
            )
            responsibility_projection.append(
                {
                    "item_ref": reference_index[identifier],
                    "providers": sorted(
                        responsible,
                        key=lambda value: (
                            value["provider"], value["state"], value["reason"]
                        ),
                    ),
                }
            )
        history_details["provider_outcomes"] = sorted(
            outcome_projection, key=lambda value: value["provider"]
        )
        history_details["provider_responsibility"] = sorted(
            responsibility_projection,
            key=lambda value: _item_key(value["item_ref"]),
        )
    else:
        raise ValueError
    return universe_refs, completed_refs, stage_dispositions, history_details


def _validator_history(attempt: ClaimedNegativeWorldCoverageAttempt):
    original_source, original_inputs, snapshot, policy, _profile, identity = (
        attempt._original_world()
    )
    classification = classify_language_support(
        original_inputs
    ).classification_document_copy()
    inventory_values = snapshot["inventory"]
    policy_values = policy["scope_decisions"]
    classification_values = classification["subjects"]
    if (
        not isinstance(inventory_values, list)
        or not isinstance(policy_values, list)
        or len(inventory_values) != len(policy_values)
        or not isinstance(classification_values, list)
    ):
        raise ValueError
    policy_by_path: dict[tuple[str, str], Mapping[str, Any]] = {}
    for policy_value in policy_values:
        policy_path = policy_value["git_path"]
        policy_key = (
            policy_path["path_kind"],
            policy_path.get("git_path_hex", ""),
        )
        if policy_key in policy_by_path:
            raise ValueError
        policy_by_path[policy_key] = policy_value
    snapshot_refs = []
    in_scope_refs = []
    excluded = []
    for inventory_value in inventory_values:
        inventory_path = inventory_value["git_path"]
        inventory_key = (
            inventory_path["path_kind"],
            inventory_path.get("git_path_hex", ""),
        )
        policy_value = policy_by_path.pop(inventory_key, None)
        if policy_value is None:
            raise ValueError
        ref = _item_ref(
            "INVENTORY_ENTRY",
            semantic_digest(
                "veritrail.review.coverage-inventory-entry/0.1", inventory_value
            ),
        )
        snapshot_refs.append(ref)
        if policy_value["disposition"] == "IN_SCOPE":
            in_scope_refs.append(ref)
        else:
            excluded.append(
                {"item_ref": ref, "reason_codes": ["POLICY_EXCLUDED"]}
            )
    if policy_by_path:
        raise ValueError
    subject_refs = {}
    accepted_language_refs = []
    rejected_language = []
    for classification_value in classification_values:
        identifier = classification_value["subject_identity"]
        if identifier in subject_refs:
            raise ValueError
        subject_refs[identifier] = _item_ref("PARSE_UNIT", identifier)
        if classification_value["disposition"] == "ELIGIBLE":
            accepted_language_refs.append(subject_refs[identifier])
        else:
            rejected_language.append(
                {
                    "item_ref": subject_refs[identifier],
                    "reason_codes": list(classification_value["reason_codes"]),
                }
            )
    parse_history = original_source["parse_partition"]
    projection_parse = original_source["fact_projection"].get("parse_partition")
    if projection_parse is not None and canonical_json_bytes(
        projection_parse
    ) != canonical_json_bytes(parse_history):
        raise ValueError
    parse_denominator = list(parse_history["denominator"])
    language_eligible_ids = {value["item_id"] for value in accepted_language_refs}
    if (
        set(parse_denominator) != language_eligible_ids
        or len(parse_denominator) != len(set(parse_denominator))
    ):
        raise ValueError
    accepted_parse_ids = [
        value["subject_identity"] for value in parse_history["accepted"]
    ]
    rejected_parse_ids = [
        value["subject_identity"] for value in parse_history["rejected"]
    ]
    if (
        set(accepted_parse_ids).union(rejected_parse_ids)
        != set(parse_denominator)
        or set(accepted_parse_ids).intersection(rejected_parse_ids)
        or len(accepted_parse_ids) != len(set(accepted_parse_ids))
        or len(rejected_parse_ids) != len(set(rejected_parse_ids))
    ):
        raise ValueError
    parse_ref_index = {
        identifier: _item_ref("PARSE_UNIT", identifier)
        for identifier in parse_denominator
    }
    try:
        (
            fact_denominator,
            fact_completed,
            fact_dispositions,
            fact_history_values,
        ) = _validator_fact_partition(original_source, identity)
    except Exception as exc:
        raise _NegativeWorldDerivationError(
            NegativeWorldCoverageFailureCode.FACT_OBLIGATION_BINDING_REJECTED
        ) from exc
    independently_derived_stages = [
        _validator_known_stage(
            "SNAPSHOT_INVENTORY",
            snapshot,
            snapshot_refs,
            snapshot_refs,
            snapshot_refs,
        ),
        _validator_known_stage(
            "POLICY_SCOPE",
            policy,
            snapshot_refs,
            in_scope_refs,
            in_scope_refs,
            dispositions={"out_of_scope": excluded},
        ),
        _validator_known_stage(
            "LANGUAGE_SUPPORT",
            classification,
            list(subject_refs.values()),
            accepted_language_refs,
            accepted_language_refs,
            dispositions={"unsupported": rejected_language},
        ),
        _validator_known_stage(
            "PARSE",
            parse_history,
            list(parse_ref_index.values()),
            list(parse_ref_index.values()),
            [parse_ref_index[value] for value in accepted_parse_ids],
            dispositions={
                "parse_failed": [
                    {
                        "item_ref": parse_ref_index[value],
                        "reason_codes": ["PARSE_ERROR"],
                    }
                    for value in rejected_parse_ids
                ]
            },
        ),
        _validator_known_stage(
            "FACT_DERIVATION",
            original_source["fact_projection"],
            fact_denominator,
            fact_denominator,
            fact_completed,
            dispositions=fact_dispositions,
        ),
    ]
    if original_source["branch"] in {
        "PROJECTION_BLOCKED",
        "REQUIRED_PROVIDER_NON_SUCCESS",
    }:
        independently_derived_stages.append(
            _validator_unknown_stage("RELATION_DERIVATION")
        )
        independently_derived_stages.append(
            _validator_unknown_stage("SLICE_DERIVATION")
        )
    else:
        independently_derived_stages.append(
            _validator_known_stage(
                "RELATION_DERIVATION",
                {"fact_branch": original_source["branch"], "known_empty": True},
                [],
                [],
                [],
            )
        )
        independently_derived_stages.append(
            _validator_known_stage(
                "SLICE_DERIVATION",
                {"fact_branch": original_source["branch"], "known_empty": True},
                [],
                [],
                [],
            )
        )
    exact_source_digest = semantic_digest(FACT_SOURCE_DOMAIN, original_source)
    fact_terminal_members = {
        "absence": {"branch": original_source["branch"], "qualified": True},
        "blockers": fact_history_values["blockers"],
        "denominator": copy.deepcopy(
            independently_derived_stages[4]["denominator"]
        ),
        "e": fact_completed,
        "u": fact_denominator,
    }
    if original_source["branch"] == "ALL_PARSE_REJECTED":
        fact_terminal_members["rejected_parse_products"] = copy.deepcopy(
            parse_history["rejected"]
        )
    if original_source["branch"] == "REQUIRED_PROVIDER_NON_SUCCESS":
        fact_terminal_members["provider_outcomes"] = fact_history_values[
            "provider_outcomes"
        ]
        fact_terminal_members["provider_responsibility"] = fact_history_values[
            "provider_responsibility"
        ]
    independently_derived_roots = [
        {
            "stage": "FACT_SET",
            "binding_state": "QUALIFIED_ABSENT",
            "exact_absence": f"FACT_SET:{original_source['branch']}",
            "producing_function": original_source["fact_projection"]["function"],
            "terminal_branch": original_source["branch"],
            "terminal_history_projection": _validator_history_projection(
                "FACT_SET",
                original_source["branch"],
                original_source["fact_projection"]["function"],
                exact_source_digest,
                fact_terminal_members,
            ),
        },
        {
            "stage": "RELATION_SET",
            "binding_state": "QUALIFIED_ABSENT",
            "exact_absence": "RELATION_SET:PREDECESSOR_ABSENT",
            "producing_function": RELATION_ABSENCE_FUNCTION,
            "terminal_branch": "PREDECESSOR_ABSENT",
            "terminal_history_projection": _validator_history_projection(
                "RELATION_SET",
                "PREDECESSOR_ABSENT",
                RELATION_ABSENCE_FUNCTION,
                exact_source_digest,
                {
                    "absence": {
                        "branch": "PREDECESSOR_ABSENT",
                        "qualified": True,
                    },
                    "predecessor_binding": None,
                    "transition": original_source["branch"],
                },
            ),
        },
        {
            "stage": "REVIEW_SLICE_SET",
            "binding_state": "QUALIFIED_ABSENT",
            "exact_absence": "REVIEW_SLICE_SET:PREDECESSOR_ABSENT",
            "producing_function": SLICE_ABSENCE_FUNCTION,
            "terminal_branch": "PREDECESSOR_ABSENT",
            "terminal_history_projection": _validator_history_projection(
                "REVIEW_SLICE_SET",
                "PREDECESSOR_ABSENT",
                SLICE_ABSENCE_FUNCTION,
                exact_source_digest,
                {
                    "absence": {
                        "branch": "PREDECESSOR_ABSENT",
                        "qualified": True,
                    },
                    "predecessor_binding": None,
                    "transition": original_source["branch"],
                },
            ),
        },
    ]
    try:
        (
            independently_derived_roots,
            expected_bindings,
            expected_chain_digest,
        ) = _validator_materialize_root_chain(
            independently_derived_roots, exact_source_digest
        )
    except Exception as exc:
        raise _NegativeWorldDerivationError(
            NegativeWorldCoverageFailureCode.ROOT_PROJECTION_REJECTED
        ) from exc
    return (
        original_inputs,
        independently_derived_roots,
        expected_bindings,
        independently_derived_stages,
        exact_source_digest,
        expected_chain_digest,
    )


def independently_validate_negative_world_coverage_candidate(
    attempt: ClaimedNegativeWorldCoverageAttempt,
    candidate: Mapping[str, Any],
    *,
    validation_function: str = VALIDATION_FUNCTION,
) -> NegativeWorldCoverageValidation:
    if (
        type(attempt) is not ClaimedNegativeWorldCoverageAttempt
        or not isinstance(candidate, Mapping)
        or validation_function != VALIDATION_FUNCTION
    ):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.INDEPENDENT_VALIDATION_REJECTED
        )
    try:
        (
            inputs,
            roots,
            expected_bindings,
            stages,
            source_digest,
            expected_chain_digest,
        ) = _validator_history(attempt)
        exact_keys = {
            "artifact_kind",
            "schema_version",
            "canonicalization_profile",
            "source_snapshot_digest",
            "policy_digest",
            "analysis_scope_digest",
            "slice_policy_digest",
            "derivation_profile_digest",
            "root_binding_function",
            "root_chain_domain",
            "root_bindings",
            "root_chain_digest",
            "stages",
            "overall_coverage_status",
            "coverage_ledger_digest",
        }
        document = copy.deepcopy(dict(candidate))
        if (
            set(document) != exact_keys
            or document["artifact_kind"] != "COVERAGE_LEDGER"
            or document["schema_version"] != "0.3"
            or document["canonicalization_profile"] != "veritrail-json-c14n/1"
            or document["source_snapshot_digest"] != inputs.source_snapshot_digest
            or document["policy_digest"] != inputs.policy_digest
            or document["analysis_scope_digest"] != inputs.analysis_scope_digest
            or document["slice_policy_digest"] != inputs.slice_policy_digest
            or document["derivation_profile_digest"]
            != inputs.derivation_profile_digest
            or document["root_binding_function"] != ROOT_BINDING_FUNCTION
            or document["root_chain_domain"] != ROOT_CHAIN_DOMAIN
            or document["root_bindings"] != expected_bindings
            or document["root_chain_digest"] != expected_chain_digest
            or document["stages"] != stages
            or document["overall_coverage_status"] != _validator_overall(stages)
        ):
            raise _NegativeWorldDerivationError(
                NegativeWorldCoverageFailureCode.CANDIDATE_RECONCILIATION_REJECTED
            )
        try:
            conformance_source = bind_coverage_ledger_conformance_source(
                fact_handoff_source_digest=source_digest,
                root_binding_projections=roots,
                stage_projections=stages,
                authority_safe=True,
            )
            validate_review_coverage_ledger(document, conformance_source)
        except Exception as exc:
            raise _NegativeWorldDerivationError(
                NegativeWorldCoverageFailureCode.CANDIDATE_RECONCILIATION_REJECTED
            ) from exc
        candidate_bytes = canonical_json_bytes(document)
        return NegativeWorldCoverageValidation(
            attempt=attempt,
            candidate_bytes=candidate_bytes,
            source_digest=source_digest,
            _token=_VALIDATION_TOKEN,
        )
    except _NegativeWorldDerivationError as exc:
        attempt._revoke()
        raise NegativeWorldCoverageError(exc.code) from exc
    except NegativeWorldCoverageError:
        attempt._revoke()
        raise
    except Exception as exc:
        attempt._revoke()
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.INDEPENDENT_VALIDATION_REJECTED
        ) from exc


def admit_negative_world_coverage_candidate(
    attempt: ClaimedNegativeWorldCoverageAttempt,
    candidate: Mapping[str, Any],
    validation: NegativeWorldCoverageValidation,
    *,
    admission_function: str = ADMISSION_FUNCTION,
) -> AdmittedNegativeWorldCoverage:
    if (
        type(attempt) is not ClaimedNegativeWorldCoverageAttempt
        or not isinstance(candidate, Mapping)
        or type(validation) is not NegativeWorldCoverageValidation
        or admission_function != ADMISSION_FUNCTION
    ):
        raise NegativeWorldCoverageError(
            NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED
        )
    return attempt._admit(candidate, validation)
