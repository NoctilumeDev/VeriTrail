"""Private Relation-transition to ReviewSliceSet/Coverage composition.

The bridge consumes the exact one-shot Fact -> Relation continuation.  It does
not relax the legacy Slice input gate and it does not grant manifest,
persistence, or public Review authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
from enum import Enum
from threading import Lock
from typing import Mapping, Sequence
from weakref import WeakKeyDictionary

from veritrail_review import _fact_relation_transition as transition
from veritrail_review._execution_cell_protocol import AttemptEligibilityState
from veritrail_review._review_coverage_ledger_conformance import (
    LEDGER_DIGEST_DOMAIN,
    ROOT_BINDING_DOMAIN,
    ROOT_BINDING_FUNCTION,
    ROOT_CHAIN_DOMAIN,
    TERMINAL_HISTORY_DOMAIN,
    bind_coverage_ledger_conformance_source,
    validate_review_coverage_ledger,
)
from veritrail_review._review_slice_input import _build_review_slice_obligation_domain
from veritrail_review._review_slice_traversal import _derive_normal_review_slice_candidate
from veritrail_review._review_slice_traversal_outcome_values import _validate_normal_slice
from veritrail_review.budget import BudgetContext, BudgetState, OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


BRIDGE_FUNCTION = "r1-relation-transition-to-slice-authority-bridge/0.1"
BRIDGE_REQUEST_FUNCTION = "r1-relation-transition-to-slice-authority-request/0.1"
BRIDGE_ADMISSION_FUNCTION = "r1-relation-transition-to-slice-authority-admission/0.1"
COMPOSITION_FUNCTION = "r1-review-slice-set-coverage-composition/0.1"
SLICE_SET_ADMISSION_FUNCTION = "r1-review-slice-set-successor-admission/0.1"
SLICE_SET_PRODUCING_FUNCTION = "r1-review-slice-set-successor/0.1"

_BRIDGE_TOKEN = object()
_BRIDGE_CONTINUATION_TOKEN = object()
_RESULT_TOKEN = object()
_CLAIM_LOCK = Lock()
_CLAIMED_TRANSITIONS: WeakKeyDictionary[object, bool] = WeakKeyDictionary()


class RelationTransitionSliceCompositionFailureCode(str, Enum):
    BRIDGE_INPUT_REJECTED = "BRIDGE_INPUT_REJECTED"
    BRIDGE_ALREADY_CONSUMED = "BRIDGE_ALREADY_CONSUMED"
    BRIDGE_ADMISSION_REJECTED = "BRIDGE_ADMISSION_REJECTED"
    BRIDGE_CONTINUATION_REJECTED = "BRIDGE_CONTINUATION_REJECTED"
    OBLIGATION_UNIVERSE_REJECTED = "OBLIGATION_UNIVERSE_REJECTED"
    COMPOSITION_RECONCILIATION_REJECTED = "COMPOSITION_RECONCILIATION_REJECTED"


class RelationTransitionSliceCompositionError(RuntimeError):
    def __init__(self, code: RelationTransitionSliceCompositionFailureCode) -> None:
        self.code = code
        super().__init__(code.value)


class OwnedRelationTransitionSliceBridgeAdmission:
    """Application-owned bridge authority bound to the original attempt."""

    def __init__(
        self,
        document: Mapping[str, object],
        *,
        claimed_transition: transition.ClaimedFactRelationTransitionContinuation,
        inputs: DerivationInputSet,
        context: BudgetContext,
        eligibility: object,
        committed_phase: OwnedPhaseResult,
        _token: object,
    ) -> None:
        if _token is not _BRIDGE_TOKEN:
            raise RelationTransitionSliceCompositionError(
                RelationTransitionSliceCompositionFailureCode.BRIDGE_ADMISSION_REJECTED
            )
        self.__bytes = canonical_json_bytes(dict(document))
        self.__bound_bytes = self.__bytes
        self.__claimed_transition = claimed_transition
        self.__bound_claimed_transition = claimed_transition
        self.__inputs = inputs
        self.__bound_inputs = inputs
        self.__context = context
        self.__bound_context = context
        self.__eligibility = eligibility
        self.__bound_eligibility = eligibility
        self.__committed_phase = committed_phase
        self.__bound_committed_phase = committed_phase
        self.__claimed = False
        self.__lock = Lock()

    def document_copy(self) -> dict[str, object]:
        self.__validate_live()
        return json.loads(self.__bytes)

    def claim_continuation(self) -> "ClaimedRelationTransitionSliceBridgeContinuation":
        with self.__lock:
            if self.__claimed:
                raise RelationTransitionSliceCompositionError(
                    RelationTransitionSliceCompositionFailureCode.BRIDGE_ALREADY_CONSUMED
                )
            self.__claimed = True
        try:
            self.__validate_live()
            return ClaimedRelationTransitionSliceBridgeContinuation(
                self, _token=_BRIDGE_CONTINUATION_TOKEN
            )
        except Exception:
            self.__eligibility.revoke()
            raise

    def __validate_live(self) -> None:
        try:
            if (
                self.__bytes is not self.__bound_bytes
                or self.__claimed_transition is not self.__bound_claimed_transition
                or self.__inputs is not self.__bound_inputs
                or self.__context is not self.__bound_context
                or self.__eligibility is not self.__bound_eligibility
                or self.__committed_phase is not self.__bound_committed_phase
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or self.__eligibility.state is not AttemptEligibilityState.ADMITTED
                or not self.__context.checkpoint()
                or self.__committed_phase.canonical_bytes != self.__bytes
            ):
                raise ValueError
            source = self.__claimed_transition._document_copy()
            if (
                self.__claimed_transition._inputs_ref() is not self.__inputs
                or self.__claimed_transition._context_ref() is not self.__context
                or self.__claimed_transition._eligibility_ref() is not self.__eligibility
            ):
                raise ValueError
            document = json.loads(self.__bytes)
            _validate_bridge_document(document, source, self.__inputs)
        except Exception as exc:
            self.__eligibility.revoke()
            if isinstance(exc, RelationTransitionSliceCompositionError):
                raise
            raise RelationTransitionSliceCompositionError(
                RelationTransitionSliceCompositionFailureCode.BRIDGE_ADMISSION_REJECTED
            ) from exc

    def _coordinates(self):
        self.__validate_live()
        return (
            self.__claimed_transition,
            self.__inputs,
            self.__context,
            self.__eligibility,
        )


class ClaimedRelationTransitionSliceBridgeContinuation:
    def __init__(
        self, admission: OwnedRelationTransitionSliceBridgeAdmission, *, _token: object
    ) -> None:
        if _token is not _BRIDGE_CONTINUATION_TOKEN:
            raise RelationTransitionSliceCompositionError(
                RelationTransitionSliceCompositionFailureCode.BRIDGE_CONTINUATION_REJECTED
            )
        self.__admission = admission
        self.__bound_admission = admission

    def _coordinates(self):
        if self.__admission is not self.__bound_admission:
            raise RelationTransitionSliceCompositionError(
                RelationTransitionSliceCompositionFailureCode.BRIDGE_CONTINUATION_REJECTED
            )
        return self.__admission._coordinates()

    def _admission_document_copy(self) -> dict[str, object]:
        self._coordinates()
        return self.__admission.document_copy()


class OwnedReviewSliceCoverageComposition:
    """Private closed proof; it grants no manifest or public product authority."""

    def __init__(
        self,
        document: Mapping[str, object],
        *,
        inputs: DerivationInputSet,
        context: BudgetContext,
        eligibility: object,
        conformance_source: object,
        committed_phase: OwnedPhaseResult,
        _token: object,
    ) -> None:
        if _token is not _RESULT_TOKEN:
            raise RelationTransitionSliceCompositionError(
                RelationTransitionSliceCompositionFailureCode.COMPOSITION_RECONCILIATION_REJECTED
            )
        self.__bytes = canonical_json_bytes(dict(document))
        self.__bound_bytes = self.__bytes
        self.__inputs = inputs
        self.__bound_inputs = inputs
        self.__context = context
        self.__bound_context = context
        self.__eligibility = eligibility
        self.__bound_eligibility = eligibility
        self.__conformance_source = conformance_source
        self.__bound_conformance_source = conformance_source
        self.__committed_phase = committed_phase
        self.__bound_committed_phase = committed_phase

    def document_copy(self) -> dict[str, object]:
        self.__validate_live()
        return json.loads(self.__bytes)

    def review_slice_set_document_copy(self) -> dict[str, object] | None:
        value = self.document_copy()["review_slice_set"]
        return None if value is None else copy.deepcopy(value)

    def coverage_ledger_document_copy(self) -> dict[str, object]:
        return copy.deepcopy(self.document_copy()["coverage_ledger"])

    def __validate_live(self) -> None:
        try:
            if (
                self.__bytes is not self.__bound_bytes
                or self.__inputs is not self.__bound_inputs
                or self.__context is not self.__bound_context
                or self.__eligibility is not self.__bound_eligibility
                or self.__conformance_source is not self.__bound_conformance_source
                or self.__committed_phase is not self.__bound_committed_phase
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or self.__eligibility.state is not AttemptEligibilityState.ADMITTED
                or not self.__context.checkpoint()
                or self.__committed_phase.canonical_bytes != self.__bytes
            ):
                raise ValueError
            document = json.loads(self.__bytes)
            unsigned = copy.deepcopy(document)
            digest = unsigned.pop("composition_digest")
            if digest != semantic_digest(COMPOSITION_FUNCTION, unsigned):
                raise ValueError
            slice_set = document["review_slice_set"]
            if slice_set is not None:
                _validate_slice_set(slice_set)
            validate_review_coverage_ledger(
                document["coverage_ledger"], self.__conformance_source
            )
        except Exception as exc:
            self.__eligibility.revoke()
            raise RelationTransitionSliceCompositionError(
                RelationTransitionSliceCompositionFailureCode.COMPOSITION_RECONCILIATION_REJECTED
            ) from exc


class _SuccessorSliceDomainView:
    def __init__(
        self,
        *,
        inputs: DerivationInputSet,
        fact_set: Mapping[str, object],
        relation_set: Mapping[str, object],
        context: BudgetContext,
        eligibility: object,
    ) -> None:
        self.source_snapshot_digest = inputs.source_snapshot_digest
        self.policy_digest = inputs.policy_digest
        self.analysis_scope_digest = inputs.analysis_scope_digest
        self.slice_policy_digest = inputs.slice_policy_digest
        self.derivation_profile_digest = inputs.derivation_profile_digest
        self.fact_set_digest = fact_set["fact_set_digest"]
        self.relation_set_digest = relation_set["relation_set_digest"]
        self.__inputs = inputs
        self.__fact_set = copy.deepcopy(dict(fact_set))
        self.__context = context
        self.__eligibility = eligibility

    def continuation_permitted(self) -> bool:
        return (
            self.__context.state is BudgetState.RUNNING
            and self.__context.stop_trigger is None
            and self.__eligibility.state is AttemptEligibilityState.ADMITTED
            and self.__context.checkpoint()
        )

    def review_policy_document_copy(self) -> dict[str, object]:
        if not self.continuation_permitted():
            raise ValueError
        return self.__inputs.review_policy_document_copy()

    def derivation_profile_document_copy(self) -> dict[str, object]:
        if not self.continuation_permitted():
            raise ValueError
        return self.__inputs.derivation_profile_document_copy()

    def fact_set_document_copy(self) -> dict[str, object]:
        if not self.continuation_permitted():
            raise ValueError
        return copy.deepcopy(self.__fact_set)


class _SuccessorTraversalBoundary:
    def __init__(
        self,
        *,
        spec: Mapping[str, object],
        fact_set: Mapping[str, object],
        relation_set: Mapping[str, object],
        context: BudgetContext,
        eligibility: object,
    ) -> None:
        self.slice_spec_digest = spec["slice_spec_digest"]
        self.__request = {
            "slice_spec": copy.deepcopy(dict(spec)),
            "fact_set": copy.deepcopy(dict(fact_set)),
            "relation_set": copy.deepcopy(dict(relation_set)),
        }
        self.__context = context
        self.__eligibility = eligibility

    def traversal_request_copy(self) -> dict[str, object]:
        if not self.continuation_permitted():
            raise ValueError
        return copy.deepcopy(self.__request)

    def continuation_permitted(self) -> bool:
        return (
            self.__context.state is BudgetState.RUNNING
            and self.__context.stop_trigger is None
            and self.__eligibility.state is AttemptEligibilityState.ADMITTED
            and self.__context.checkpoint()
        )


def admit_relation_transition_for_slice_composition(
    claimed: transition.ClaimedFactRelationTransitionContinuation,
) -> OwnedRelationTransitionSliceBridgeAdmission:
    """Consume one exact transition continuation and issue bridge authority."""

    if type(claimed) is not transition.ClaimedFactRelationTransitionContinuation:
        raise RelationTransitionSliceCompositionError(
            RelationTransitionSliceCompositionFailureCode.BRIDGE_INPUT_REJECTED
        )
    with _CLAIM_LOCK:
        if claimed in _CLAIMED_TRANSITIONS:
            raise RelationTransitionSliceCompositionError(
                RelationTransitionSliceCompositionFailureCode.BRIDGE_ALREADY_CONSUMED
            )
        _CLAIMED_TRANSITIONS[claimed] = True
    try:
        source = claimed._document_copy()
        inputs = claimed._inputs_ref()
        context = claimed._context_ref()
        eligibility = claimed._eligibility_ref()
        _revalidate_transition_world(source, inputs, context, eligibility)
        request = {
            "function": BRIDGE_REQUEST_FUNCTION,
            "transition_function": source["transition_function"],
            "transition_attempt_id": source["transition_attempt"]["attempt_id"],
            "transition_admission_digest": source["admission"]["admission_digest"],
            "handoff_claim_id": source["handoff"]["claim_id"],
            "fact_consumer_attempt_id": source["handoff"]["fact_consumer_attempt_id"],
            "fact_set_digest": source["fact_set"]["fact_set_digest"],
            "relation_set_digest": source["relation_set"]["relation_set_digest"],
            "input_identity": copy.deepcopy(source["input_identity"]),
        }
        request["request_digest"] = semantic_digest(BRIDGE_REQUEST_FUNCTION, request)
        admission_payload = {
            "function": BRIDGE_ADMISSION_FUNCTION,
            "status": "QUALIFIED",
            "request_digest": request["request_digest"],
            "transition_admission_digest": source["admission"]["admission_digest"],
            "transition_attempt_id": source["transition_attempt"]["attempt_id"],
            "relation_set_digest": source["relation_set"]["relation_set_digest"],
        }
        admission_payload["admission_digest"] = semantic_digest(
            BRIDGE_ADMISSION_FUNCTION, admission_payload
        )
        document = {
            "bridge_function": BRIDGE_FUNCTION,
            "request": request,
            "admission": admission_payload,
            "authority_ceiling": {
                "private_review_slice_set_coverage_composition": True,
                "legacy_slice_authority": False,
                "manifest": False,
                "persistence": False,
                "public_review": False,
            },
        }
        encoded = canonical_json_bytes(document)
        committed = context.try_complete_phase(encoded, resources_closed=True)
        if committed is None:
            raise ValueError
        return OwnedRelationTransitionSliceBridgeAdmission(
            document,
            claimed_transition=claimed,
            inputs=inputs,
            context=context,
            eligibility=eligibility,
            committed_phase=committed,
            _token=_BRIDGE_TOKEN,
        )
    except RelationTransitionSliceCompositionError:
        raise
    except Exception as exc:
        try:
            claimed._eligibility_ref().revoke()
        except Exception:
            pass
        raise RelationTransitionSliceCompositionError(
            RelationTransitionSliceCompositionFailureCode.BRIDGE_ADMISSION_REJECTED
        ) from exc


def compose_review_slice_set_and_coverage(
    continuation: ClaimedRelationTransitionSliceBridgeContinuation,
) -> OwnedReviewSliceCoverageComposition:
    """Derive and reconcile the complete private Slice/Coverage world."""

    if type(continuation) is not ClaimedRelationTransitionSliceBridgeContinuation:
        raise RelationTransitionSliceCompositionError(
            RelationTransitionSliceCompositionFailureCode.BRIDGE_CONTINUATION_REJECTED
        )
    try:
        claimed, inputs, context, eligibility = continuation._coordinates()
        bridge_admission = continuation._admission_document_copy()
        source = claimed._document_copy()
        _revalidate_transition_world(source, inputs, context, eligibility)
        fact_set = source["fact_set"]
        relation_set = source["relation_set"]
        conflicts = relation_set["conflicts"]
        domain_view = _SuccessorSliceDomainView(
            inputs=inputs,
            fact_set=fact_set,
            relation_set=relation_set,
            context=context,
            eligibility=eligibility,
        )
        if conflicts:
            obligation_domain = None
            slices = None
            branch = "PREDECESSOR_UNKNOWN"
        else:
            obligation_domain = _build_review_slice_obligation_domain(domain_view)
            _validate_complete_slice_obligation_domain(
                inputs,
                fact_set,
                relation_set,
                obligation_domain,
            )
            obligations = obligation_domain["obligations"]
            if not isinstance(obligations, list):
                raise ValueError
            candidates = []
            for spec in obligations:
                boundary = _SuccessorTraversalBoundary(
                    spec=spec,
                    fact_set=fact_set,
                    relation_set=relation_set,
                    context=context,
                    eligibility=eligibility,
                )
                candidate = _derive_normal_review_slice_candidate(boundary)
                _validate_normal_slice(candidate, boundary)
                candidates.append(candidate)
            candidates.sort(key=lambda item: item["slice_id"])
            if sorted(
                item["slice_spec"]["slice_spec_digest"] for item in candidates
            ) != sorted(item["slice_spec_digest"] for item in obligations):
                raise ValueError
            slices = _slice_set_document(inputs, fact_set, relation_set, candidates)
            branch = (
                "CLOSED_EMPTY"
                if not candidates
                else "NORMAL_PARTIAL"
                if any(item["coverage_status"] == "PARTIAL" for item in candidates)
                else "NORMAL_CLOSED"
            )
        projections, stages, source_digest = _coverage_history(
            inputs=inputs,
            transition_document=source,
            slice_set=slices,
            obligation_domain=obligation_domain,
            slice_branch=branch,
        )
        conformance_source = bind_coverage_ledger_conformance_source(
            fact_handoff_source_digest=source_digest,
            root_binding_projections=projections,
            stage_projections=stages,
            authority_safe=True,
        )
        ledger = _coverage_ledger_document(inputs, projections, stages, source_digest)
        validate_review_coverage_ledger(ledger, conformance_source)
        slice_admission_payload = {
            "function": SLICE_SET_ADMISSION_FUNCTION,
            "status": "QUALIFIED_UNKNOWN" if slices is None else "QUALIFIED",
            "terminal_branch": branch,
            "bridge_admission_digest": bridge_admission["admission"]["admission_digest"],
            "slice_obligation_domain_digest": (
                None
                if obligation_domain is None
                else obligation_domain["slice_obligation_domain_digest"]
            ),
            "slice_set_digest": None if slices is None else slices["slice_set_digest"],
            "coverage_ledger_digest": ledger["coverage_ledger_digest"],
        }
        slice_admission_payload["admission_digest"] = semantic_digest(
            SLICE_SET_ADMISSION_FUNCTION, slice_admission_payload
        )
        document = {
            "composition_function": COMPOSITION_FUNCTION,
            "bridge_admission": bridge_admission,
            "slice_obligation_domain": obligation_domain,
            "review_slice_set": slices,
            "slice_set_admission": slice_admission_payload,
            "coverage_ledger": ledger,
            "authority_ceiling": {
                "private_review_slice_set": slices is not None,
                "private_coverage_validation": True,
                "manifest": False,
                "persistence": False,
                "public_review": False,
            },
        }
        document["composition_digest"] = semantic_digest(
            COMPOSITION_FUNCTION, copy.deepcopy(document)
        )
        encoded = canonical_json_bytes(document)
        committed = context.try_complete_phase(encoded, resources_closed=True)
        if committed is None:
            raise ValueError
        return OwnedReviewSliceCoverageComposition(
            document,
            inputs=inputs,
            context=context,
            eligibility=eligibility,
            conformance_source=conformance_source,
            committed_phase=committed,
            _token=_RESULT_TOKEN,
        )
    except RelationTransitionSliceCompositionError:
        raise
    except Exception as exc:
        try:
            continuation._coordinates()[3].revoke()
        except Exception:
            pass
        raise RelationTransitionSliceCompositionError(
            RelationTransitionSliceCompositionFailureCode.COMPOSITION_RECONCILIATION_REJECTED
        ) from exc


def _revalidate_transition_world(source, inputs, context, eligibility) -> None:
    if (
        type(inputs) is not DerivationInputSet
        or type(context) is not BudgetContext
        or context.state is not BudgetState.RUNNING
        or context.stop_trigger is not None
        or eligibility.state is not AttemptEligibilityState.ADMITTED
        or not context.checkpoint()
        or source.get("transition_function") != transition.TRANSITION_FUNCTION
        or source.get("admission", {}).get("function") != transition.ADMISSION_FUNCTION
        or source.get("admission", {}).get("status") != "QUALIFIED"
        or source.get("authority_ceiling", {}).get("review_slice_set") is not False
        or source.get("authority_ceiling", {}).get("coverage") is not False
    ):
        raise ValueError
    merged, conflicts = transition._compose_carrier_candidates(source["provider_lineage"])
    expected_relation_set = transition._relation_set_document(
        inputs, source["fact_set"], merged, conflicts
    )
    if expected_relation_set != source["relation_set"]:
        raise ValueError
    expected_obligations = source["obligation_projection"]["obligations"]
    domain_items = source["observation_domain"]["observation_items"]
    expected_ids = sorted(
        item["provider_observation_item_id"] for item in expected_obligations
    )
    domain_ids = sorted(item["observation_item_id"] for item in domain_items)
    terminal_ids = sorted(
        outcome["observation_item_id"]
        for lineage in source["provider_lineage"]
        for outcome in lineage["terminal"]["observation_outcomes"]
    )
    if expected_ids != domain_ids or set(terminal_ids) != set(domain_ids):
        raise ValueError


def _validate_complete_slice_obligation_domain(
    inputs: DerivationInputSet,
    fact_set: Mapping[str, object],
    relation_set: Mapping[str, object],
    domain: Mapping[str, object],
) -> None:
    """Independently rederive the complete Slice denominator.

    This deliberately does not reuse ``_build_review_slice_obligation_domain``.
    A shared omission in the producer and its ordinary validator must not turn a
    smaller denominator into a qualified composition.
    """

    policy = inputs.review_policy_document_copy()
    profile = inputs.derivation_profile_document_copy()
    slice_policy = policy.get("slice_policy")
    profile_fact_kinds = profile.get("fact_kinds")
    facts = fact_set.get("facts")
    if (
        not isinstance(slice_policy, Mapping)
        or not isinstance(profile_fact_kinds, list)
        or not isinstance(facts, list)
    ):
        raise ValueError
    anchor_fact_kinds = slice_policy.get("anchor_fact_kinds")
    allowed_relations = slice_policy.get("allowed_relations")
    if (
        not isinstance(anchor_fact_kinds, list)
        or not isinstance(allowed_relations, list)
    ):
        raise ValueError
    fact_kind_rank = {
        fact_kind: index
        for index, fact_kind in enumerate(profile_fact_kinds)
        if isinstance(fact_kind, str)
    }
    if len(fact_kind_rank) != len(profile_fact_kinds):
        raise ValueError

    anchors: list[tuple[int, str]] = []
    for fact in facts:
        if not isinstance(fact, Mapping):
            raise ValueError
        fact_kind = fact.get("fact_kind")
        fact_id = fact.get("fact_id")
        if fact_kind not in fact_kind_rank or not isinstance(fact_id, str):
            raise ValueError
        if fact_kind in anchor_fact_kinds:
            anchors.append((fact_kind_rank[fact_kind], fact_id))
    anchors.sort()

    expected_obligations: list[dict[str, object]] = []
    for _, anchor_fact_id in anchors:
        spec: dict[str, object] = {
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "slice_policy_digest": inputs.slice_policy_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            "fact_set_digest": fact_set["fact_set_digest"],
            "relation_set_digest": relation_set["relation_set_digest"],
            "anchor_fact_id": anchor_fact_id,
            "allowed_relations": copy.deepcopy(allowed_relations),
            "max_depth": slice_policy["max_depth"],
            "max_symbols": slice_policy["max_symbols"],
            "max_files": slice_policy["max_files"],
            "max_relations": slice_policy["max_relations"],
        }
        spec["slice_spec_digest"] = semantic_digest(
            "veritrail.review.slice-spec/0.1", spec
        )
        expected_obligations.append(spec)

    expected_domain: dict[str, object] = {
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "policy_digest": inputs.policy_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "slice_policy_digest": inputs.slice_policy_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        "fact_set_digest": fact_set["fact_set_digest"],
        "relation_set_digest": relation_set["relation_set_digest"],
        "obligations": expected_obligations,
    }
    expected_domain["slice_obligation_domain_digest"] = semantic_digest(
        "veritrail.review.slice-obligation-domain/0.1",
        {
            key: copy.deepcopy(value)
            for key, value in expected_domain.items()
            if key != "policy_digest"
        },
    )
    if canonical_json_bytes(domain) != canonical_json_bytes(expected_domain):
        raise ValueError


def _validate_bridge_document(document, source, inputs) -> None:
    if set(document) != {"bridge_function", "request", "admission", "authority_ceiling"}:
        raise ValueError
    if document["bridge_function"] != BRIDGE_FUNCTION:
        raise ValueError
    request = document["request"]
    admission = document["admission"]
    unsigned_request = copy.deepcopy(request)
    request_digest = unsigned_request.pop("request_digest")
    if request_digest != semantic_digest(BRIDGE_REQUEST_FUNCTION, unsigned_request):
        raise ValueError
    unsigned_admission = copy.deepcopy(admission)
    admission_digest = unsigned_admission.pop("admission_digest")
    if admission_digest != semantic_digest(BRIDGE_ADMISSION_FUNCTION, unsigned_admission):
        raise ValueError
    if (
        request["transition_admission_digest"] != source["admission"]["admission_digest"]
        or request["transition_attempt_id"] != source["transition_attempt"]["attempt_id"]
        or request["handoff_claim_id"] != source["handoff"]["claim_id"]
        or request["fact_consumer_attempt_id"] != source["handoff"]["fact_consumer_attempt_id"]
        or request["fact_set_digest"] != source["fact_set"]["fact_set_digest"]
        or request["relation_set_digest"] != source["relation_set"]["relation_set_digest"]
        or request["input_identity"] != source["input_identity"]
        or request["input_identity"]
        != {
            key: getattr(inputs, key)
            for key in (
                "source_snapshot_digest",
                "policy_digest",
                "analysis_scope_digest",
                "slice_policy_digest",
                "derivation_profile_digest",
            )
        }
        or admission["request_digest"] != request_digest
        or admission["transition_admission_digest"] != request["transition_admission_digest"]
        or admission["transition_attempt_id"] != request["transition_attempt_id"]
        or admission["relation_set_digest"] != request["relation_set_digest"]
        or admission["status"] != "QUALIFIED"
    ):
        raise ValueError


def _slice_set_document(inputs, fact_set, relation_set, slices):
    document = {
        "artifact_kind": "REVIEW_SLICE_SET",
        "schema_version": "0.1",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "policy_digest": inputs.policy_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "slice_policy_digest": inputs.slice_policy_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        "fact_set_digest": fact_set["fact_set_digest"],
        "relation_set_digest": relation_set["relation_set_digest"],
        "slices": copy.deepcopy(slices),
    }
    payload = {
        key: copy.deepcopy(document[key])
        for key in (
            "source_snapshot_digest",
            "analysis_scope_digest",
            "slice_policy_digest",
            "derivation_profile_digest",
            "fact_set_digest",
            "relation_set_digest",
            "slices",
        )
    }
    document["slice_set_digest"] = semantic_digest(
        "veritrail.review.slice-set/0.1", payload
    )
    _validate_slice_set(document)
    return document


def _validate_slice_set(document):
    payload = {
        key: copy.deepcopy(document[key])
        for key in (
            "source_snapshot_digest",
            "analysis_scope_digest",
            "slice_policy_digest",
            "derivation_profile_digest",
            "fact_set_digest",
            "relation_set_digest",
            "slices",
        )
    }
    if (
        document.get("artifact_kind") != "REVIEW_SLICE_SET"
        or document.get("schema_version") != "0.1"
        or document.get("canonicalization_profile") != "veritrail-json-c14n/1"
        or document.get("slice_set_digest")
        != semantic_digest("veritrail.review.slice-set/0.1", payload)
        or document["slices"] != sorted(document["slices"], key=lambda item: item["slice_id"])
        or len({item["slice_id"] for item in document["slices"]}) != len(document["slices"])
    ):
        raise ValueError


def _item_ref(kind: str, value: str) -> dict[str, str]:
    return {"item_id": value, "item_kind": kind}


def _complete_stage(stage, upstream, refs, source_payload, *, frontier=()):
    refs = sorted(copy.deepcopy(list(refs)), key=lambda item: (item["item_kind"], item["item_id"]))
    frontier = sorted(
        copy.deepcopy(list(frontier)),
        key=lambda item: (item["slice_id"], canonical_json_bytes(item["frontier_item"])),
    )
    reasons = []
    for item in frontier:
        for reason in item["frontier_item"]["reason_codes"]:
            if reason not in reasons:
                reasons.append(reason)
    return {
        "stage": stage,
        "upstream_stage": upstream,
        "denominator": {
            "state": "KNOWN",
            "source_digest": semantic_digest(
                f"veritrail.review.coverage-stage-source/{stage.lower()}/0.1",
                source_payload,
            ),
            "item_refs": refs,
        },
        "eligible": copy.deepcopy(refs),
        "completed": copy.deepcopy(refs),
        "out_of_scope": [],
        "unsupported": [],
        "unresolved": [],
        "conflicts": [],
        "parse_failed": [],
        "execution_failed": [],
        "truncated": [],
        "blocked": [],
        "frontier": frontier,
        "reason_codes": reasons,
        "coverage_status": "PARTIAL" if frontier else "COMPLETE",
    }


def _unknown_stage(stage, upstream, known_refs):
    refs = sorted(copy.deepcopy(list(known_refs)), key=lambda item: (item["item_kind"], item["item_id"]))
    return {
        "stage": stage,
        "upstream_stage": upstream,
        "denominator": {
            "state": "UNKNOWN",
            "source_digest": None,
            "known_item_refs": refs,
            "reason_codes": ["UPSTREAM_DENOMINATOR_UNKNOWN"],
        },
        "eligible": [],
        "completed": [],
        "out_of_scope": [],
        "unsupported": [],
        "unresolved": [],
        "conflicts": [],
        "parse_failed": [],
        "execution_failed": [],
        "truncated": [],
        "blocked": [],
        "frontier": [],
        "reason_codes": ["UPSTREAM_DENOMINATOR_UNKNOWN"],
        "coverage_status": "UNKNOWN",
    }


def _materialize_projection(projection, predecessor):
    projection = copy.deepcopy(projection)
    history = projection["terminal_history_projection"]
    for member in history["history"]:
        if member["name"] == "predecessor_binding":
            member["value"] = predecessor
    value = copy.deepcopy(projection)
    value["terminal_history_digest"] = semantic_digest(TERMINAL_HISTORY_DOMAIN, history)
    value["predecessor_binding_digest"] = predecessor
    value["binding_digest"] = semantic_digest(ROOT_BINDING_DOMAIN, value)
    return projection, value


def _history_projection(stage, branch, function, source_digest, history, completion="COMPLETE"):
    return {
        "projection_identity": TERMINAL_HISTORY_DOMAIN,
        "stage": stage,
        "terminal_branch": branch,
        "producing_function": function,
        "same_attempt_source": source_digest,
        "completion_state": completion,
        "history": [{"name": name, "value": value} for name, value in history],
    }


def _coverage_history(*, inputs, transition_document, slice_set, obligation_domain, slice_branch):
    source = transition_document["fact_handoff_source"]
    fact_set = transition_document["fact_set"]
    relation_set = transition_document["relation_set"]
    source_digest = semantic_digest("veritrail.review.fact-handoff-source/0.1", source)
    fact_refs = [_item_ref("FACT", item["fact_id"]) for item in fact_set["facts"]]
    relation_refs = [_item_ref("RELATION", item["relation_id"]) for item in relation_set["relations"]]
    snapshot = inputs.source_snapshot_document_copy()
    inventory_refs = [
        _item_ref(
            "INVENTORY_ENTRY",
            semantic_digest("veritrail.review.coverage-inventory-entry/0.1", item),
        )
        for item in snapshot["inventory"]
    ]
    parse_partition = source["parse_partition"]
    parse_refs = [_item_ref("PARSE_UNIT", item) for item in parse_partition["denominator"]]
    stages = [
        _complete_stage("SNAPSHOT_INVENTORY", None, inventory_refs, snapshot),
        _complete_stage("POLICY_SCOPE", "SNAPSHOT_INVENTORY", inventory_refs, inputs.review_policy_document_copy()),
        _complete_stage("LANGUAGE_SUPPORT", "POLICY_SCOPE", parse_refs, parse_partition),
        _complete_stage("PARSE", "LANGUAGE_SUPPORT", parse_refs, parse_partition),
        _complete_stage("FACT_DERIVATION", "PARSE", fact_refs, source["fact_projection"]),
    ]
    conflicts = relation_set["conflicts"]
    if conflicts:
        conflict_ids = {
            relation_id
            for conflict in conflicts
            for relation_id in conflict["candidate_relation_ids"]
        }
        relation_stage = _complete_stage(
            "RELATION_DERIVATION", "FACT_DERIVATION", relation_refs, relation_set
        )
        relation_stage["completed"] = [
            item for item in relation_refs if item["item_id"] not in conflict_ids
        ]
        relation_stage["conflicts"] = [
            {"item_ref": item, "reason_codes": ["PROVIDER_CONFLICT"]}
            for item in relation_refs
            if item["item_id"] in conflict_ids
        ]
        relation_stage["reason_codes"] = ["PROVIDER_CONFLICT"]
        relation_stage["coverage_status"] = "PARTIAL"
        slice_stage = _unknown_stage("SLICE_DERIVATION", "RELATION_DERIVATION", [])
    else:
        relation_stage = _complete_stage(
            "RELATION_DERIVATION", "FACT_DERIVATION", relation_refs, relation_set
        )
        slice_refs = [_item_ref("REVIEW_SLICE", item["slice_id"]) for item in slice_set["slices"]]
        frontier = [
            {"slice_id": item["slice_id"], "frontier_item": edge}
            for item in slice_set["slices"]
            for edge in item["frontier"]
        ]
        slice_stage = _complete_stage(
            "SLICE_DERIVATION", "RELATION_DERIVATION", slice_refs, slice_set, frontier=frontier
        )
    stages.extend([relation_stage, slice_stage])

    fact_providers = [
        {
            "provider": item["descriptor"]["provider_id"],
            "state": item["lifecycle"],
        }
        for item in source["provider_history"]
    ]
    fact_responsibility = [
        {"provider": item["descriptor"]["provider_id"], "required": item["required"]}
        for item in source["provider_history"]
    ]
    fact_projection = {
        "stage": "FACT_SET",
        "binding_state": "ARTIFACT_PRESENT",
        "artifact_digest": fact_set["fact_set_digest"],
        "closure_digest": semantic_digest(
            "veritrail.review.fact-root-closure/0.1", source["fact_projection"]
        ),
        "producing_function": source["fact_projection"]["function"],
        "terminal_branch": "NORMAL_FULFILLED",
        "terminal_history_projection": _history_projection(
            "FACT_SET",
            "NORMAL_FULFILLED",
            source["fact_projection"]["function"],
            source_digest,
            (
                ("blockers", source["fact_projection"]["blockers"]),
                ("closure", {"member_count": len(fact_refs), "state": "COMPLETE"}),
                ("denominator", {"state": "KNOWN", "source_digest": fact_set["fact_set_digest"], "item_refs": fact_refs}),
                ("e", fact_refs),
                ("members", [item["fact_id"] for item in fact_set["facts"]]),
                ("provider_outcomes", fact_providers),
                ("provider_responsibility", fact_responsibility),
                ("u", fact_refs),
            ),
        ),
    }
    fact_projection, fact_binding = _materialize_projection(fact_projection, source_digest)

    relation_function = transition_document["transition_function"]
    relation_branch = "ADMITTED_CONFLICT" if conflicts else "ADMITTED"
    relation_providers = [
        {
            "provider": item["binding"]["provider_descriptor"]["provider_id"],
            "state": item["terminal"]["provider_run_status"],
        }
        for item in transition_document["provider_lineage"]
    ]
    relation_responsibility = [
        {
            "provider": item["binding"]["provider_descriptor"]["provider_id"],
            "required": True,
        }
        for item in transition_document["provider_lineage"]
    ]
    relation_projection = {
        "stage": "RELATION_SET",
        "binding_state": "ARTIFACT_PRESENT",
        "artifact_digest": relation_set["relation_set_digest"],
        "closure_digest": transition_document["admission"]["admission_digest"],
        "producing_function": relation_function,
        "terminal_branch": relation_branch,
        "terminal_history_projection": _history_projection(
            "RELATION_SET",
            relation_branch,
            relation_function,
            source_digest,
            (
                ("admission", {"branch": relation_branch, "qualified": True}),
                ("conflicts", [item["conflict_id"] for item in conflicts]),
                ("members", [item["relation_id"] for item in relation_set["relations"]]),
                ("obligation_universe", [
                    {"kind": "OBSERVATION_OBLIGATION", "value": item["observation_item_id"]}
                    for item in transition_document["observation_domain"]["observation_items"]
                ]),
                ("predecessor_binding", None),
                ("provider_outcomes", relation_providers),
                ("provider_responsibility", relation_responsibility),
            ),
        ),
    }
    relation_projection, relation_binding = _materialize_projection(
        relation_projection, fact_binding["binding_digest"]
    )

    if slice_set is None:
        slice_projection = {
            "stage": "REVIEW_SLICE_SET",
            "binding_state": "QUALIFIED_UNKNOWN",
            "known_prefix": {"complete": False, "members": []},
            "unknown_cause": "RELATION_CONFLICT",
            "producing_function": SLICE_SET_PRODUCING_FUNCTION,
            "terminal_branch": "PREDECESSOR_UNKNOWN",
            "terminal_history_projection": _history_projection(
                "REVIEW_SLICE_SET",
                "PREDECESSOR_UNKNOWN",
                SLICE_SET_PRODUCING_FUNCTION,
                source_digest,
                (
                    ("known_members", []),
                    ("missing_authority_slot", "REVIEW_SLICE_TERMINAL_COMPLETION"),
                    ("predecessor_binding", None),
                    ("unknown_cause", "RELATION_CONFLICT"),
                ),
                completion="KNOWN_PREFIX",
            ),
        }
    else:
        frontier_values = [
            {"slice_id": item["slice_id"], "frontier_item": edge}
            for item in slice_set["slices"]
            for edge in item["frontier"]
        ]
        outcomes = [
            {
                "member": item["slice_id"],
                "state": "NORMAL_PARTIAL" if item["frontier"] else "NORMAL_COMPLETE",
            }
            for item in slice_set["slices"]
        ]
        slice_projection = {
            "stage": "REVIEW_SLICE_SET",
            "binding_state": "ARTIFACT_PRESENT",
            "artifact_digest": slice_set["slice_set_digest"],
            "closure_digest": semantic_digest(
                "veritrail.review.slice-root-closure/0.1",
                {"branch": slice_branch, "domain": obligation_domain, "outcomes": outcomes},
            ),
            "producing_function": SLICE_SET_PRODUCING_FUNCTION,
            "terminal_branch": slice_branch,
            "terminal_history_projection": _history_projection(
                "REVIEW_SLICE_SET",
                slice_branch,
                SLICE_SET_PRODUCING_FUNCTION,
                source_digest,
                (
                    ("admission", {"branch": slice_branch, "qualified": True}),
                    ("closure", {"branch": slice_branch, "frontier_count": len(frontier_values)}),
                    ("frontier", frontier_values),
                    ("members", [item["slice_id"] for item in slice_set["slices"]]),
                    ("obligation_universe", [item["slice_spec_digest"] for item in obligation_domain["obligations"]]),
                    ("outcomes", outcomes),
                    ("predecessor_binding", None),
                ),
            ),
        }
    slice_projection, _ = _materialize_projection(
        slice_projection, relation_binding["binding_digest"]
    )
    return [fact_projection, relation_projection, slice_projection], stages, source_digest


def _coverage_ledger_document(inputs, projections, stages, source_digest):
    bindings = []
    predecessor = source_digest
    for projection in projections:
        projection, binding = _materialize_projection(projection, predecessor)
        bindings.append(binding)
        predecessor = binding["binding_digest"]
    root_payload = {
        "root_binding_function": ROOT_BINDING_FUNCTION,
        "root_chain_domain": ROOT_CHAIN_DOMAIN,
        "root_bindings": bindings,
    }
    statuses = [item["coverage_status"] for item in stages]
    document = {
        "artifact_kind": "COVERAGE_LEDGER",
        "schema_version": "0.3",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "policy_digest": inputs.policy_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "slice_policy_digest": inputs.slice_policy_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        **root_payload,
        "root_chain_digest": semantic_digest(ROOT_CHAIN_DOMAIN, root_payload),
        "stages": copy.deepcopy(stages),
        "overall_coverage_status": (
            "UNKNOWN" if "UNKNOWN" in statuses else "PARTIAL" if "PARTIAL" in statuses else "COMPLETE"
        ),
    }
    document["coverage_ledger_digest"] = semantic_digest(
        LEDGER_DIGEST_DOMAIN, copy.deepcopy(document)
    )
    return document
