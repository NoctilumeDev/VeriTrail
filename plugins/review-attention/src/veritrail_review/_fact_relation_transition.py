from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import asdict
from threading import Lock
from typing import Callable, Mapping, Sequence
from uuid import uuid4

from veritrail_review import _source_operation_controller_cell as _source_operation_cell
from veritrail_review._execution_cell import (
    DEFAULT_TRANSPORT_LIMITS,
    _owned_request_provenance,
    _utc_now,
)
from veritrail_review._execution_cell_binding import ProviderBinding, ProviderDescriptor
from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._execution_cell_values import ReleaseOutcome
from veritrail_review._fact_fulfillment import OwnedProductFactClosure
from veritrail_review._fact_fulfillment_binding import (
    build_fact_relation_stage_applicability,
)
from veritrail_review._language_support import (
    _revalidate_exact_inputs,
    classify_language_support,
)
from veritrail_review._language_support_values import OwnedLanguageSupportClassification
from veritrail_review._relation_observation_binding import (
    corrected_import_form_relation_observation_bindings,
    relation_observation_descriptor_rank,
)
from veritrail_review._relation_observation_cell_values import (
    OwnedRelationObservationCellPhaseResult,
)
from veritrail_review._relation_observation_application import (
    relation_observation_terminal_document,
    validate_relation_observation_terminal_document,
)
from veritrail_review._source_operation_relation_observation_application import (
    validate_relation_observation_source_operation_request_document,
)
from veritrail_review._relation_observation_domain import (
    build_declared_relation_observation_domain,
    observation_profile_document,
    validate_declared_relation_observation_domain,
)
from veritrail_review._relation_observation_qualification import (
    _compose_candidates,
    _observation_receipt,
    _receipt_complete,
)
from veritrail_review._source_operation_gate import create_source_operation_attempt_gate
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


TRANSITION_FUNCTION = "r1-fact-handoff-relation-transition/0.1"
HANDOFF_FUNCTION = "r1-fact-relation-handoff-claim/0.1"
PRODUCT_CLOSURE_FUNCTION = "r1-fact-relation-product-closure/0.1"
OBLIGATION_PROJECTION_FUNCTION = "r1-fact-relation-obligation-projection/0.1"
ADMISSION_FUNCTION = "r1-fact-relation-transition-admission/0.1"
RELATION_SET_FUNCTION = "veritrail.review.fact-handoff-relation-set/0.1"

_RESULT_TOKEN = object()
_CONTINUATION_TOKEN = object()


class FactRelationTransitionError(ValueError):
    """The private Fact handoff to Relation transition failed closed."""


class OwnedFactRelationTransitionAdmission:
    """Qualified private Relation authority; it grants no public product authority."""

    def __init__(
        self,
        document: Mapping[str, object],
        *,
        inputs: DerivationInputSet,
        context: BudgetContext,
        eligibility: AttemptEligibility,
        fact_handoff_source: Mapping[str, object],
        request_provenance: Mapping[str, object],
        transition_identity: Mapping[str, object],
        _token: object,
    ) -> None:
        if _token is not _RESULT_TOKEN:
            raise FactRelationTransitionError("transition admission is not constructible")
        self.__bytes = canonical_json_bytes(dict(document))
        self.__bound_bytes = self.__bytes
        self.__inputs = inputs
        self.__bound_inputs = inputs
        self.__context = context
        self.__bound_context = context
        self.__eligibility = eligibility
        self.__bound_eligibility = eligibility
        self.__fact_handoff_source_bytes = canonical_json_bytes(
            dict(fact_handoff_source)
        )
        self.__bound_fact_handoff_source_bytes = self.__fact_handoff_source_bytes
        self.__request_provenance_bytes = canonical_json_bytes(
            dict(request_provenance)
        )
        self.__bound_request_provenance_bytes = self.__request_provenance_bytes
        self.__transition_identity_bytes = canonical_json_bytes(
            dict(transition_identity)
        )
        self.__bound_transition_identity_bytes = self.__transition_identity_bytes
        self.__claimed = False
        self.__lock = Lock()

    def document_copy(self) -> dict[str, object]:
        self.__validate_live()
        return json.loads(self.__bytes)

    def claim_continuation(self) -> "ClaimedFactRelationTransitionContinuation":
        with self.__lock:
            if self.__claimed:
                raise FactRelationTransitionError("transition continuation already consumed")
            self.__claimed = True
        try:
            self.__validate_live()
            return ClaimedFactRelationTransitionContinuation(
                self, _token=_CONTINUATION_TOKEN
            )
        except Exception:
            self.__eligibility.revoke()
            raise

    def __validate_live(self) -> None:
        try:
            if (
                self.__bytes is not self.__bound_bytes
                or self.__inputs is not self.__bound_inputs
                or self.__context is not self.__bound_context
                or self.__eligibility is not self.__bound_eligibility
                or self.__fact_handoff_source_bytes
                is not self.__bound_fact_handoff_source_bytes
                or self.__request_provenance_bytes
                is not self.__bound_request_provenance_bytes
                or self.__transition_identity_bytes
                is not self.__bound_transition_identity_bytes
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or self.__eligibility.state is not AttemptEligibilityState.ADMITTED
                or not self.__context.checkpoint()
            ):
                raise ValueError
            _revalidate_exact_inputs(self.__inputs)
            document = json.loads(self.__bytes)
            if (
                document["transition_function"] != TRANSITION_FUNCTION
                or document["admission"]["function"] != ADMISSION_FUNCTION
                or document["admission"]["status"] != "QUALIFIED"
                or document["admission"]["carrier_digest"]
                != _carrier_digest(document)
                or document["admission"]["admission_digest"]
                != _admission_digest(document)
            ):
                raise ValueError
            _validate_document_links(
                document,
                self.__inputs,
                context=self.__context,
                fact_handoff_source_bytes=self.__fact_handoff_source_bytes,
                request_provenance_bytes=self.__request_provenance_bytes,
                transition_identity_bytes=self.__transition_identity_bytes,
            )
        except Exception as exc:
            self.__eligibility.revoke()
            raise FactRelationTransitionError(
                "transition admission is no longer live"
            ) from exc

    def _inputs_ref(self) -> DerivationInputSet:
        self.__validate_live()
        return self.__inputs

    def _context_ref(self) -> BudgetContext:
        self.__validate_live()
        return self.__context

    def _eligibility_ref(self) -> AttemptEligibility:
        self.__validate_live()
        return self.__eligibility


class ClaimedFactRelationTransitionContinuation:
    def __init__(
        self, admission: OwnedFactRelationTransitionAdmission, *, _token: object
    ) -> None:
        if _token is not _CONTINUATION_TOKEN:
            raise FactRelationTransitionError("continuation is not constructible")
        self.__admission = admission
        self.__bound_admission = admission

    def _document_copy(self) -> dict[str, object]:
        if self.__admission is not self.__bound_admission:
            raise FactRelationTransitionError("continuation identity changed")
        return self.__admission.document_copy()

    def _inputs_ref(self) -> DerivationInputSet:
        self._document_copy()
        return self.__admission._inputs_ref()

    def _context_ref(self) -> BudgetContext:
        self._document_copy()
        return self.__admission._context_ref()

    def _eligibility_ref(self) -> AttemptEligibility:
        self._document_copy()
        return self.__admission._eligibility_ref()


def run_fact_handoff_relation_transition(
    fact_closure: OwnedProductFactClosure,
    *,
    relation_bindings: Sequence[ProviderBinding] = (),
    cancellation_requested: Callable[[], bool] | None = None,
    transport_limits: ExecutionCellTransportSafetyLimits | None = None,
) -> OwnedFactRelationTransitionAdmission:
    """Consume one complete Fact handoff and qualify the bounded Relation edge."""

    if type(fact_closure) is not OwnedProductFactClosure:
        raise FactRelationTransitionError("transition requires an owned Fact closure")
    try:
        (
            source,
            context,
            inputs,
            classification,
            inherited_limits,
            inherited_cancellation,
        ) = fact_closure._claim_relation_handoff_source()
    except Exception as exc:
        raise FactRelationTransitionError("Fact handoff claim failed closed") from exc

    parent = AttemptEligibility()
    attempts = []
    try:
        if (
            type(inputs) is not DerivationInputSet
            or type(context) is not BudgetContext
            or type(classification) is not OwnedLanguageSupportClassification
            or context.state is not BudgetState.RUNNING
            or context.stop_trigger is not None
            or not context.checkpoint()
        ):
            raise ValueError
        _revalidate_exact_inputs(inputs)
        recomputed = classify_language_support(inputs)
        if (
            recomputed.classification_document_copy()
            != classification.classification_document_copy()
        ):
            raise ValueError
        _validate_source_identity(source, inputs, classification)
        applicability = build_fact_relation_stage_applicability(inputs)
        fact_set = _complete_fact_set(source)
        bindings = _normalize_relation_bindings(relation_bindings)
        product_closure = _build_product_closure(
            inputs, classification, source, fact_set
        )
        fact_partition = _build_total_fact_partition(fact_set, product_closure)
        expected = _independent_obligation_projection(
            inputs, fact_set, product_closure, bindings
        )
        domain = build_declared_relation_observation_domain(inputs, fact_set, bindings)
        _reconcile_expected_domain(expected, domain, bindings)

        if transport_limits is None:
            transport_limits = inherited_limits
        if type(transport_limits) is not ExecutionCellTransportSafetyLimits:
            raise ValueError
        if transport_limits != inherited_limits:
            raise ValueError("transition cannot replace inherited transport limits")
        if cancellation_requested is None:
            cancellation_requested = inherited_cancellation
        if cancellation_requested is not inherited_cancellation:
            raise ValueError("transition cannot replace inherited cancellation identity")

        transition_attempt_id = str(uuid4())
        handoff_claim_id = str(uuid4())
        attempt_started_at = _utc_now()
        transition_identity = {
            "transition_attempt_id": transition_attempt_id,
            "handoff_claim_id": handoff_claim_id,
            "attempt_started_at": attempt_started_at,
        }
        provenance = _owned_request_provenance(inputs)
        gate = create_source_operation_attempt_gate(
            inputs, context, parent, classification
        )
        for binding in bindings:
            attempts.append(
                _source_operation_cell.build_prepared_relation_observation_source_operation_attempt(
                    inputs,
                    derivation_id=source["input_identity"]["derivation_id"],
                    binding=binding,
                    cancellation_requested=cancellation_requested,
                    transport_limits=transport_limits,
                    context=context,
                    parent_eligibility=parent,
                    eligibility=AttemptEligibility(),
                    request_provenance=provenance,
                    attempt_started_at=attempt_started_at,
                    fact_set_document=fact_set,
                    observation_domain=domain,
                    classification=classification,
                    source_operation_gate=gate,
                )
            )
        gate.admit_parent()
        if not context.checkpoint():
            raise ValueError

        phases: list[OwnedRelationObservationCellPhaseResult] = []
        for attempt in attempts:
            if parent.state is not AttemptEligibilityState.ADMITTED:
                raise ValueError
            phases.append(
                _source_operation_cell.run_prepared_relation_observation_source_operation_attempt(
                    attempt
                )
            )

        receipts = [
            _observation_receipt(domain, binding.descriptor, phase)
            for binding, phase in zip(bindings, phases)
        ]
        if not all(_receipt_complete(receipt) for receipt in receipts):
            raise ValueError("required Relation observation closure is incomplete")
        if any(phase.release_outcome is not ReleaseOutcome.RELEASED for phase in phases):
            raise ValueError("Relation child release failed")
        _independent_terminal_reconciliation(
            inputs=inputs,
            derivation_id=source["input_identity"]["derivation_id"],
            attempt_started_at=attempt_started_at,
            provenance=provenance,
            bindings=bindings,
            expected=expected,
            domain=domain,
            receipts=receipts,
            phases=phases,
        )
        merged, conflicts = _compose_candidates(phases)
        relation_set = _relation_set_document(inputs, fact_set, merged, conflicts)
        carrier = _carrier_document(
            inputs=inputs,
            source=source,
            context=context,
            handoff_claim_id=handoff_claim_id,
            transition_attempt_id=transition_attempt_id,
            attempt_started_at=attempt_started_at,
            applicability=applicability,
            product_closure=product_closure,
            fact_partition=fact_partition,
            expected=expected,
            domain=domain,
            bindings=bindings,
            provenance=provenance,
            attempts=attempts,
            phases=phases,
            receipts=receipts,
            relation_set=relation_set,
        )
        admission_payload = {
            "function": ADMISSION_FUNCTION,
            "status": "QUALIFIED",
            "carrier_digest": _carrier_digest(carrier),
            "transition_attempt_id": transition_attempt_id,
            "fact_consumer_attempt_id": source["input_identity"][
                "fact_consumer_attempt_id"
            ],
            "handoff_claim_id": handoff_claim_id,
            "fact_set_digest": fact_set["fact_set_digest"],
            "observation_domain_digest": domain["observation_domain_digest"],
            "relation_set_digest": relation_set["relation_set_digest"],
            "provider_run_ids": [phase.provider_run_id for phase in phases],
        }
        document = {
            **carrier,
            "admission": {
                **admission_payload,
                "admission_digest": semantic_digest(
                    "veritrail.review.fact-relation-transition-admission/0.1",
                    admission_payload,
                ),
            },
        }
        if document["admission"]["admission_digest"] != _admission_digest(document):
            raise ValueError
        _validate_document_links(
            document,
            inputs,
            context=context,
            fact_handoff_source_bytes=canonical_json_bytes(source),
            request_provenance_bytes=canonical_json_bytes(provenance),
            transition_identity_bytes=canonical_json_bytes(transition_identity),
        )
        return OwnedFactRelationTransitionAdmission(
            document,
            inputs=inputs,
            context=context,
            eligibility=parent,
            fact_handoff_source=source,
            request_provenance=provenance,
            transition_identity=transition_identity,
            _token=_RESULT_TOKEN,
        )
    except Exception as exc:
        parent.revoke()
        for attempt in attempts:
            attempt.eligibility.revoke()
        if isinstance(exc, FactRelationTransitionError):
            raise
        raise FactRelationTransitionError(
            "Fact handoff to Relation transition failed closed"
        ) from exc


def _validate_source_identity(
    source: Mapping[str, object],
    inputs: DerivationInputSet,
    classification: OwnedLanguageSupportClassification,
) -> None:
    identity = source.get("input_identity")
    if (
        source.get("branch") != "NORMAL_FULFILLED"
        or not isinstance(identity, Mapping)
        or identity
        != {
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "policy_digest": inputs.policy_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "slice_policy_digest": inputs.slice_policy_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            "language_support_function": classification.language_support_function,
            "classification_digest": classification.classification_digest,
            "parse_function": source["parse_partition"]["parse_function"],
            "product_set_digest": source["parse_partition"]["product_set_digest"],
            "fact_consumer_function": "r1-parse-product-fact-consumer/0.2",
            "fact_consumer_attempt_id": identity.get("fact_consumer_attempt_id"),
            "derivation_id": identity.get("derivation_id"),
        }
        or not isinstance(identity.get("fact_consumer_attempt_id"), str)
        or not identity["fact_consumer_attempt_id"]
        or not isinstance(identity.get("derivation_id"), str)
        or not identity["derivation_id"]
        or source.get("whole_attempt", {}).get("budget_state") != "RUNNING"
        or source.get("whole_attempt", {}).get("stop_trigger") is not None
        or source.get("whole_attempt", {}).get("parent_eligibility") != "ADMITTED"
    ):
        raise ValueError("Fact handoff identity is not exact and live")


def _complete_fact_set(source: Mapping[str, object]) -> dict[str, object]:
    value = source.get("fact_set")
    if not isinstance(value, Mapping):
        raise ValueError("complete FactSet is missing")
    fact_set = copy.deepcopy(dict(value))
    if not isinstance(fact_set.get("facts"), list) or fact_set.get("conflicts") != []:
        raise ValueError("FactSet is incomplete or conflicted")
    return fact_set


def _build_product_closure(
    inputs: DerivationInputSet,
    classification: OwnedLanguageSupportClassification,
    source: Mapping[str, object],
    fact_set: Mapping[str, object],
) -> dict[str, object]:
    accepted = copy.deepcopy(source["parse_partition"]["accepted"])
    subjects = {
        item["subject_identity"]: item for item in classification.subjects_copy()
    }
    accepted_identities = [item["subject_identity"] for item in accepted]
    if (
        len(accepted_identities) != len(set(accepted_identities))
        or any(subject_identity not in subjects for subject_identity in accepted_identities)
    ):
        raise ValueError("accepted product identity is not total")
    accepted_paths = {
        item["subject_identity"]: subjects[item["subject_identity"]]["semantic_input"][
            "inventory_item"
        ]["git_path"]["git_path_hex"]
        for item in accepted
    }
    if len(accepted_paths.values()) != len(set(accepted_paths.values())):
        raise ValueError("parse product denominator is not total")
    by_path: dict[str, list[dict[str, object]]] = {
        path: [] for path in accepted_paths.values()
    }
    for fact in fact_set["facts"]:
        path = fact["source_anchor"]["git_path"]["git_path_hex"]
        if path not in by_path:
            raise ValueError("FactSet contains a fact outside the accepted product set")
        by_path[path].append(copy.deepcopy(fact))
    snapshot = inputs.source_snapshot_document_copy()
    inventory = {
        item["git_path"]["git_path_hex"]: item for item in snapshot["inventory"]
    }
    products = []
    represented_fact_ids: set[str] = set()
    for accepted_product in sorted(accepted, key=lambda item: item["subject_identity"]):
        subject_identity = accepted_product["subject_identity"]
        path = accepted_paths[subject_identity]
        facts = sorted(by_path[path], key=lambda item: item["fact_id"])
        modules = [item for item in facts if item["fact_kind"] == "MODULE"]
        if len(modules) != 1:
            raise ValueError("per-product MODULE closure is not exact")
        if path not in inventory:
            raise ValueError("accepted product lacks exact source inventory")
        entry = inventory[path]
        raw = inputs.verified_blob_bytes_by_object_identity[
            entry["git_object"]["hex"]
        ]
        if (
            len(raw) != entry["content"]["size_bytes"]
            or hashlib.sha256(raw).hexdigest() != entry["content"]["sha256"]
        ):
            raise ValueError("exact source blob changed")
        fact_ids = [item["fact_id"] for item in facts]
        if represented_fact_ids.intersection(fact_ids):
            raise ValueError("per-product Fact closures overlap")
        represented_fact_ids.update(fact_ids)
        product_payload = {
            "accepted_product_identity": subject_identity,
            "parse_obligation_id": accepted_product["obligation_id"],
            "product_semantic_digest": accepted_product["product_semantic_digest"],
            "git_path_hex": path,
            "module_fact_id": modules[0]["fact_id"],
            "fact_members": [
                {
                    "fact_id": item["fact_id"],
                    "fact_kind": item["fact_kind"],
                    "provenance_refs": copy.deepcopy(item["provenance_refs"]),
                }
                for item in facts
            ],
            "fact_ids": fact_ids,
            "source_object_identity": copy.deepcopy(entry["git_object"]),
            "source_sha256": entry["content"]["sha256"],
            "source_bytes_hex": raw.hex(),
        }
        products.append(
            {
                **product_payload,
                "product_closure_entry_digest": semantic_digest(
                    "veritrail.review.fact-relation-product-closure-entry/0.1",
                    product_payload,
                ),
            }
        )
    all_fact_ids = {item["fact_id"] for item in fact_set["facts"]}
    if len(all_fact_ids) != len(fact_set["facts"]) or represented_fact_ids != all_fact_ids:
        raise ValueError("per-product Fact closure is not total")
    payload = {
        "function": PRODUCT_CLOSURE_FUNCTION,
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "product_set_digest": source["parse_partition"]["product_set_digest"],
        "fact_set_digest": fact_set["fact_set_digest"],
        "products": products,
    }
    return {
        **payload,
        "product_closure_digest": semantic_digest(
            "veritrail.review.fact-relation-product-closure/0.1", payload
        ),
    }


def _build_total_fact_partition(
    fact_set: Mapping[str, object], product_closure: Mapping[str, object]
) -> dict[str, object]:
    all_ids = [item["fact_id"] for item in fact_set["facts"]]
    structural = [
        item["module_fact_id"] for item in product_closure["products"]
    ]
    applicable = [
        item["fact_id"]
        for item in fact_set["facts"]
        if item["fact_kind"] == "IMPORT_DECLARATION"
    ]
    classified = set(structural) | set(applicable)
    preserved = [item for item in all_ids if item not in classified]
    if (
        len(all_ids) != len(set(all_ids))
        or len(structural) != len(set(structural))
        or set(structural) & set(applicable)
        or set(structural) & set(preserved)
        or set(applicable) & set(preserved)
        or set(structural) | set(applicable) | set(preserved) != set(all_ids)
    ):
        raise ValueError("Fact applicability partition is not total")
    payload = {
        "function": "r1-fact-relation-total-fact-partition/0.1",
        "fact_set_digest": fact_set["fact_set_digest"],
        "all_fact_ids": sorted(all_ids),
        "structural_anchor_fact_ids": sorted(structural),
        "applicable_subject_fact_ids": sorted(applicable),
        "profile_non_applicable_fact_ids": sorted(preserved),
        "classification_rules": {
            "STRUCTURAL_ANCHOR": "per-product MODULE",
            "APPLICABLE_SUBJECT": "IMPORT_DECLARATION",
            "PROFILE_NON_APPLICABLE": "all remaining complete FactSet members",
        },
    }
    return {
        **payload,
        "fact_partition_digest": semantic_digest(
            "veritrail.review.fact-relation-total-fact-partition/0.1", payload
        ),
    }


def _independent_obligation_projection(
    inputs: DerivationInputSet,
    fact_set: Mapping[str, object],
    product_closure: Mapping[str, object],
    bindings: Sequence[ProviderBinding],
) -> dict[str, object]:
    profile = observation_profile_document(bindings)
    profile_payload = {
        **profile,
        "derivation_profile_digest": inputs.derivation_profile_digest,
    }
    profile_digest = semantic_digest(
        "veritrail.review.relation-observation-profile/0.1", profile_payload
    )
    closure_by_path = {
        item["git_path_hex"]: item for item in product_closure["products"]
    }
    obligations = []
    provider_items = []
    for fact in fact_set["facts"]:
        if fact["fact_kind"] != "IMPORT_DECLARATION":
            continue
        path = fact["source_anchor"]["git_path"]["git_path_hex"]
        product = closure_by_path.get(path)
        if product is None or fact["fact_id"] not in product["fact_ids"]:
            raise ValueError("applicable Fact lacks exact product closure")
        for relation_kind, subject_role in (
            ("LEXICAL_CONTAINS", "TARGET_FACT"),
            ("IMPORT_TARGET_LITERAL", "SOURCE_FACT"),
        ):
            provider_payload = {
                "source_snapshot_digest": inputs.source_snapshot_digest,
                "derivation_profile_digest": inputs.derivation_profile_digest,
                "fact_set_digest": fact_set["fact_set_digest"],
                "relation_kind": relation_kind,
                "subject_role": subject_role,
                "subject_fact_id": fact["fact_id"],
            }
            observation_item_id = semantic_digest(
                "veritrail.review.relation-observation-item/0.1", provider_payload
            )
            provider_items.append(
                {"observation_item_id": observation_item_id, **provider_payload}
            )
            obligation_payload = {
                "source_snapshot_digest": inputs.source_snapshot_digest,
                "policy_digest": inputs.policy_digest,
                "fact_set_digest": fact_set["fact_set_digest"],
                "relation_profile_id": profile["observation_profile_id"],
                "relation_profile_version": profile["observation_profile_version"],
                "relation_profile_digest": profile_digest,
                "product_closure_digest": product_closure[
                    "product_closure_digest"
                ],
                "product_closure_entry_digest": product[
                    "product_closure_entry_digest"
                ],
                "accepted_product_identity": product[
                    "accepted_product_identity"
                ],
                "git_path_hex": path,
                "module_fact_id": product["module_fact_id"],
                "relation_kind": relation_kind,
                "subject_role": subject_role,
                "subject_fact_id": fact["fact_id"],
                "obligation_projection_function": OBLIGATION_PROJECTION_FUNCTION,
                "provider_observation_item_id": observation_item_id,
            }
            obligations.append(
                {
                    "obligation_id": semantic_digest(
                        "veritrail.review.fact-relation-obligation/0.1",
                        obligation_payload,
                    ),
                    **obligation_payload,
                }
            )
    provider_items.sort(
        key=lambda item: (
            {"LEXICAL_CONTAINS": 0, "IMPORT_TARGET_LITERAL": 1}[
                item["relation_kind"]
            ],
            {"SOURCE_FACT": 0, "TARGET_FACT": 1}[item["subject_role"]],
            item["subject_fact_id"],
            item["observation_item_id"],
        )
    )
    obligation_by_observation = {
        item["provider_observation_item_id"]: item for item in obligations
    }
    obligations.sort(
        key=lambda item: next(
            index
            for index, provider_item in enumerate(provider_items)
            if provider_item["observation_item_id"]
            == item["provider_observation_item_id"]
        )
    )
    if (
        len({item["observation_item_id"] for item in provider_items})
        != len(provider_items)
        or len({item["obligation_id"] for item in obligations}) != len(obligations)
        or len(obligation_by_observation) != len(obligations)
    ):
        raise ValueError("obligation identity collision")
    rules = {
        canonical_json_bytes(item["provider_descriptor"]): item
        for item in profile["provider_responsibility_rules"]
    }
    assignment = []
    for binding in bindings:
        rule = rules.get(canonical_json_bytes(binding.descriptor.document()))
        if rule is None:
            raise ValueError("missing independent Provider responsibility")
        assigned_obligations = [
            item
            for item in obligations
            if item["relation_kind"] in rule["assigned_relation_families"]
        ]
        assignment.append(
            {
                "provider_descriptor": binding.descriptor.document(),
                "assigned_obligation_ids": sorted(
                    item["obligation_id"] for item in assigned_obligations
                ),
                "assigned_observation_item_ids": sorted(
                    item["provider_observation_item_id"]
                    for item in assigned_obligations
                ),
            }
        )
    payload = {
        "function": OBLIGATION_PROJECTION_FUNCTION,
        "policy_digest": inputs.policy_digest,
        "fact_set_digest": fact_set["fact_set_digest"],
        "relation_profile": copy.deepcopy(profile_payload),
        "relation_profile_digest": profile_digest,
        "product_closure_digest": product_closure["product_closure_digest"],
        "obligations": obligations,
        "provider_observation_items": provider_items,
        "provider_assignments": assignment,
    }
    return {
        **payload,
        "obligation_projection_digest": semantic_digest(
            "veritrail.review.fact-relation-obligation-projection/0.1", payload
        ),
    }


def _normalize_relation_bindings(
    bindings: Sequence[ProviderBinding],
) -> tuple[ProviderBinding, ...]:
    submitted = tuple(bindings) if bindings else corrected_import_form_relation_observation_bindings()
    normalized = tuple(
        sorted(submitted, key=lambda item: relation_observation_descriptor_rank(item.descriptor))
    )
    if normalized != corrected_import_form_relation_observation_bindings():
        raise ValueError("transition requires the complete frozen import-form Provider family")
    return tuple(
        ProviderBinding(ProviderDescriptor(**item.descriptor.document()), item.launch_key)
        for item in normalized
    )


def _reconcile_expected_domain(
    expected: Mapping[str, object],
    domain: Mapping[str, object],
    bindings: Sequence[ProviderBinding],
) -> None:
    actual_assignments = [
        {
            "provider_descriptor": copy.deepcopy(item["provider_descriptor"]),
            "assigned_observation_item_ids": copy.deepcopy(
                item["assigned_observation_item_ids"]
            ),
        }
        for item in domain["provider_responsibilities"]
    ]
    expected_assignments = [
        {
            "provider_descriptor": copy.deepcopy(item["provider_descriptor"]),
            "assigned_observation_item_ids": copy.deepcopy(
                item["assigned_observation_item_ids"]
            ),
        }
        for item in expected["provider_assignments"]
    ]
    if (
        domain["observation_items"] != expected["provider_observation_items"]
        or actual_assignments != expected_assignments
        or len(domain["provider_responsibilities"]) != len(bindings)
    ):
        raise ValueError("declared Relation domain differs from independent denominator")


def _independent_terminal_reconciliation(
    *,
    inputs: DerivationInputSet,
    derivation_id: str,
    attempt_started_at: str,
    provenance: Mapping[str, object],
    bindings: Sequence[ProviderBinding],
    expected: Mapping[str, object],
    domain: Mapping[str, object],
    receipts: Sequence[Mapping[str, object]],
    phases: Sequence[OwnedRelationObservationCellPhaseResult],
) -> None:
    provenance_bytes = canonical_json_bytes(provenance)
    if (
        len(phases) != len(bindings)
        or len({phase.provider_run_id for phase in phases}) != len(phases)
        or any(
            phase.derivation_id != derivation_id
            or phase.request_provenance_bytes != provenance_bytes
            or phase.attempt_started_at != attempt_started_at
            or phase.source_snapshot_digest != inputs.source_snapshot_digest
            or phase.policy_digest != inputs.policy_digest
            or phase.analysis_scope_digest != inputs.analysis_scope_digest
            or phase.slice_policy_digest != inputs.slice_policy_digest
            or phase.derivation_profile_digest != inputs.derivation_profile_digest
            or phase.fact_set_digest != domain["fact_set_digest"]
            or phase.observation_domain_digest != domain["observation_domain_digest"]
            or phase.provider_descriptor != binding.descriptor
            for phase, binding in zip(phases, bindings)
        )
    ):
        raise ValueError("Relation terminal lost same-attempt provenance")
    expected_ids = {
        item["observation_item_id"]
        for item in expected["provider_observation_items"]
    }
    domain_ids = {item["observation_item_id"] for item in domain["observation_items"]}
    emitted: dict[str, int] = {item_id: 0 for item_id in expected_ids}
    expected_count: dict[str, int] = {item_id: 0 for item_id in expected_ids}
    assigned_pairs = set()
    for receipt in receipts:
        descriptor_key = canonical_json_bytes(receipt["provider_descriptor"])
        for item_id in receipt["assigned_observation_item_ids"]:
            assigned_pairs.add((descriptor_key, item_id))
        for outcome in receipt["accepted_observation_outcomes"]:
            item_id = outcome["observation_item_id"]
            if item_id not in emitted:
                raise ValueError("foreign emitted obligation")
            emitted[item_id] += 1
    expected_pairs = {
        (canonical_json_bytes(item["provider_descriptor"]), obligation_id)
        for item in expected["provider_assignments"]
        for obligation_id in item["assigned_observation_item_ids"]
    }
    for _, item_id in expected_pairs:
        expected_count[item_id] += 1
    emitted_pairs = {
        (
            canonical_json_bytes(receipt["provider_descriptor"]),
            outcome["observation_item_id"],
        )
        for receipt in receipts
        for outcome in receipt["accepted_observation_outcomes"]
    }
    if (
        expected_ids != domain_ids
        or assigned_pairs != expected_pairs
        or emitted_pairs != expected_pairs
        or emitted != expected_count
        or len(phases) != len(receipts)
    ):
        raise ValueError("expected/assigned/emitted obligation reconciliation failed")


def _relation_set_document(
    inputs: DerivationInputSet,
    fact_set: Mapping[str, object],
    merged: Sequence[Mapping[str, object]],
    conflicts: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    relations = copy.deepcopy(list(merged))
    conflict_values = copy.deepcopy(list(conflicts))
    payload = {
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        "fact_set_digest": fact_set["fact_set_digest"],
        "relations": [
            {key: copy.deepcopy(value) for key, value in item.items() if key != "provenance_refs"}
            for item in relations
        ],
        "conflicts": [
            {key: copy.deepcopy(value) for key, value in item.items() if key != "provenance_refs"}
            for item in conflict_values
        ],
    }
    return {
        "artifact_kind": "PRIVATE_HANDOFF_RELATION_SET",
        "schema_version": "0.1",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "policy_digest": inputs.policy_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        "fact_set_digest": fact_set["fact_set_digest"],
        "relations": relations,
        "conflicts": conflict_values,
        "relation_set_digest": semantic_digest(RELATION_SET_FUNCTION, payload),
    }


def _compose_carrier_candidates(
    provider_lineage: Sequence[Mapping[str, object]],
) -> tuple[tuple[dict[str, object], ...], tuple[dict[str, object], ...]]:
    """Independently reconstruct merged Relation candidates from carrier terminals."""

    by_id: dict[str, dict[str, object]] = {}
    semantic_by_id: dict[str, bytes] = {}
    for lineage in provider_lineage:
        for raw in lineage["terminal"]["canonical_relations"]:
            relation = copy.deepcopy(dict(raw))
            relation_id = relation["relation_id"]
            semantic = {
                key: copy.deepcopy(value)
                for key, value in relation.items()
                if key != "provenance_refs"
            }
            semantic_bytes = canonical_json_bytes(semantic)
            previous = semantic_by_id.setdefault(relation_id, semantic_bytes)
            if previous != semantic_bytes:
                raise ValueError("carrier Relation identity collision")
            if relation_id not in by_id:
                by_id[relation_id] = relation
            provenance = set(by_id[relation_id]["provenance_refs"])
            provenance.update(relation["provenance_refs"])
            by_id[relation_id]["provenance_refs"] = sorted(provenance)
    merged = tuple(by_id[key] for key in sorted(by_id))
    by_subject: dict[str, list[dict[str, object]]] = {}
    for relation in merged:
        by_subject.setdefault(relation["relation_subject_digest"], []).append(
            relation
        )
    conflicts = []
    for subject, candidates in by_subject.items():
        candidate_ids = sorted({item["relation_id"] for item in candidates})
        if len(candidate_ids) < 2:
            continue
        provenance = sorted(
            {
                ref
                for candidate in candidates
                for ref in candidate["provenance_refs"]
            }
        )
        conflicts.append(
            {
                "conflict_id": semantic_digest(
                    "veritrail.review.relation-conflict/0.1",
                    {
                        "relation_subject_digest": subject,
                        "candidate_relation_ids": candidate_ids,
                    },
                ),
                "relation_subject_digest": subject,
                "candidate_relation_ids": candidate_ids,
                "provenance_refs": provenance,
            }
        )
    conflicts.sort(key=lambda item: item["conflict_id"])
    return merged, tuple(conflicts)


def _carrier_document(
    *,
    inputs: DerivationInputSet,
    source: Mapping[str, object],
    context: BudgetContext,
    handoff_claim_id: str,
    transition_attempt_id: str,
    attempt_started_at: str,
    applicability: Mapping[str, object],
    product_closure: Mapping[str, object],
    fact_partition: Mapping[str, object],
    expected: Mapping[str, object],
    domain: Mapping[str, object],
    bindings: Sequence[ProviderBinding],
    provenance: Mapping[str, object],
    attempts: Sequence[object],
    phases: Sequence[OwnedRelationObservationCellPhaseResult],
    receipts: Sequence[Mapping[str, object]],
    relation_set: Mapping[str, object],
) -> dict[str, object]:
    context_payload = {
        "budget_limits": asdict(context.limits),
        "started_at_monotonic": context.started_at_monotonic,
        "execution_deadline_monotonic": context.execution_deadline_monotonic,
    }
    provider_lineage = []
    for binding, attempt, phase, receipt in zip(bindings, attempts, phases, receipts):
        phase_document = {
            "provider_run_id": phase.provider_run_id,
            "provider_descriptor": phase.provider_descriptor.document(),
            "provider_run_status": phase.provider_run_status.value,
            "phase_status": phase.phase_status.value,
            "release_outcome": phase.release_outcome.value,
            "diagnostic_code": phase.diagnostic_code,
            "assigned_observation_item_ids": list(phase.assigned_observation_item_ids),
            "reported_relation_ids": list(phase.reported_relation_ids),
            "canonical_relations": list(phase.canonical_relations_copy()),
            "observation_outcomes": list(phase.observation_outcomes_copy()),
        }
        provider_lineage.append(
            {
                "binding": {
                    "provider_descriptor": binding.descriptor.document(),
                    "launch_key": binding.launch_key,
                },
                "request": copy.deepcopy(attempt.request_document),
                "request_sha256": hashlib.sha256(
                    canonical_json_bytes(attempt.request_document)
                ).hexdigest(),
                "terminal": phase_document,
                "terminal_sha256": hashlib.sha256(
                    canonical_json_bytes(phase_document)
                ).hexdigest(),
                "receipt": copy.deepcopy(receipt),
            }
        )
    return {
        "transition_function": TRANSITION_FUNCTION,
        "handoff": {
            "function": HANDOFF_FUNCTION,
            "claim_id": handoff_claim_id,
            "source_branch": source["branch"],
            "fact_consumer_attempt_id": source["input_identity"][
                "fact_consumer_attempt_id"
            ],
            "fact_derivation_id": source["input_identity"]["derivation_id"],
            "source_sha256": hashlib.sha256(
                canonical_json_bytes(source)
            ).hexdigest(),
        },
        "transition_attempt": {
            "attempt_id": transition_attempt_id,
            "attempt_started_at": attempt_started_at,
            "context_identity": semantic_digest(
                "veritrail.review.fact-relation-context/0.1", context_payload
            ),
            **context_payload,
            "request_provenance": copy.deepcopy(dict(provenance)),
        },
        "input_identity": {
            key: getattr(inputs, key)
            for key in (
                "source_snapshot_digest",
                "policy_digest",
                "analysis_scope_digest",
                "slice_policy_digest",
                "derivation_profile_digest",
            )
        },
        "stage_applicability": copy.deepcopy(dict(applicability)),
        "product_closure": copy.deepcopy(dict(product_closure)),
        "fact_partition": copy.deepcopy(dict(fact_partition)),
        "fact_handoff_source": copy.deepcopy(dict(source)),
        "fact_set": copy.deepcopy(source["fact_set"]),
        "obligation_projection": copy.deepcopy(dict(expected)),
        "observation_domain": copy.deepcopy(dict(domain)),
        "provider_lineage": provider_lineage,
        "relation_set": copy.deepcopy(dict(relation_set)),
        "authority_ceiling": {
            "private_relation_transition": True,
            "review_slice_set": False,
            "coverage": False,
            "manifest": False,
            "persistence": False,
            "public_review": False,
        },
    }


def _validate_document_links(
    document: Mapping[str, object],
    inputs: DerivationInputSet,
    *,
    context: BudgetContext,
    fact_handoff_source_bytes: bytes,
    request_provenance_bytes: bytes,
    transition_identity_bytes: bytes,
) -> None:
    """Recompute the transition carrier from its authoritative operands."""

    source = document["fact_handoff_source"]
    fact_set = document["fact_set"]
    handoff = document["handoff"]
    admission = document["admission"]
    classification = classify_language_support(inputs)
    _validate_source_identity(source, inputs, classification)
    expected_context = {
        "budget_limits": asdict(context.limits),
        "started_at_monotonic": context.started_at_monotonic,
        "execution_deadline_monotonic": context.execution_deadline_monotonic,
    }
    expected_whole_attempt = {
        **expected_context,
        "budget_state": "RUNNING",
        "stop_trigger": None,
        "parent_eligibility": "ADMITTED",
    }
    transition_attempt = document["transition_attempt"]
    try:
        expected_provenance = json.loads(request_provenance_bytes)
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("bound request provenance is not canonical JSON") from exc
    snapshot = inputs.source_snapshot_document_copy()
    coordinate = snapshot["source_coordinate"]
    commit_oid = coordinate["commit_oid"]
    expected_provenance_identity = {
        "requested_repository_id": snapshot["repository_id"],
        "requested_ref": (
            f"oid:{commit_oid['algorithm'].lower()}:{commit_oid['hex']}"
        ),
        "resolver_id": "veritrail-r1-owned-snapshot-exact-oid",
        "resolver_version": "0.1",
    }
    if (
        type(expected_provenance) is not dict
        or set(expected_provenance)
        != {*expected_provenance_identity, "resolved_at"}
        or {
            key: expected_provenance.get(key)
            for key in expected_provenance_identity
        }
        != expected_provenance_identity
        or not isinstance(expected_provenance.get("resolved_at"), str)
        or not expected_provenance["resolved_at"]
    ):
        raise ValueError("bound request provenance identity mismatch")
    try:
        expected_transition_identity = json.loads(transition_identity_bytes)
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("bound transition identity is not canonical JSON") from exc
    if (
        type(expected_transition_identity) is not dict
        or set(expected_transition_identity)
        != {
            "transition_attempt_id",
            "handoff_claim_id",
            "attempt_started_at",
        }
        or any(
            not isinstance(expected_transition_identity[key], str)
            or not expected_transition_identity[key]
            for key in expected_transition_identity
        )
    ):
        raise ValueError("bound transition identity is invalid")
    if (
        canonical_json_bytes(source) != fact_handoff_source_bytes
        or source["fact_set"] != fact_set
        or handoff["source_sha256"]
        != hashlib.sha256(canonical_json_bytes(source)).hexdigest()
        or handoff["fact_consumer_attempt_id"]
        != source["input_identity"]["fact_consumer_attempt_id"]
        or handoff["fact_derivation_id"]
        != source["input_identity"]["derivation_id"]
        or handoff["claim_id"]
        != expected_transition_identity["handoff_claim_id"]
        or transition_attempt.get("attempt_id")
        != expected_transition_identity["transition_attempt_id"]
        or transition_attempt.get("attempt_started_at")
        != expected_transition_identity["attempt_started_at"]
        or document["input_identity"]
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
        or source["whole_attempt"] != expected_whole_attempt
        or transition_attempt.get("context_identity")
        != semantic_digest(
            "veritrail.review.fact-relation-context/0.1", expected_context
        )
        or {
            key: transition_attempt.get(key)
            for key in (
                "budget_limits",
                "started_at_monotonic",
                "execution_deadline_monotonic",
            )
        }
        != expected_context
        or canonical_json_bytes(transition_attempt.get("request_provenance"))
        != request_provenance_bytes
    ):
        raise ValueError("Fact handoff carrier identity mismatch")

    expected_applicability = build_fact_relation_stage_applicability(inputs)
    expected_closure = _build_product_closure(
        inputs, classification, source, fact_set
    )
    expected_partition = _build_total_fact_partition(fact_set, expected_closure)
    bindings = tuple(
        ProviderBinding(
            ProviderDescriptor(**item["binding"]["provider_descriptor"]),
            item["binding"]["launch_key"],
        )
        for item in document["provider_lineage"]
    )
    bindings = _normalize_relation_bindings(bindings)
    expected_projection = _independent_obligation_projection(
        inputs, fact_set, expected_closure, bindings
    )
    if (
        document["stage_applicability"] != expected_applicability
        or document["product_closure"] != expected_closure
        or document["fact_partition"] != expected_partition
        or document["obligation_projection"] != expected_projection
    ):
        raise ValueError("transition proof projection mismatch")

    validated_domain = validate_declared_relation_observation_domain(
        document["observation_domain"],
        inputs=inputs,
        fact_set_document=fact_set,
        relation_bindings=bindings,
    )
    _reconcile_expected_domain(expected_projection, validated_domain, bindings)
    assignments = {
        canonical_json_bytes(item["provider_descriptor"]): item
        for item in expected_projection["provider_assignments"]
    }
    provider_run_ids = []
    for binding, lineage in zip(bindings, document["provider_lineage"]):
        terminal = lineage["terminal"]
        validated_request = (
            validate_relation_observation_source_operation_request_document(
                lineage["request"], launch_key=binding.launch_key
            )
        )
        assignment = assignments[canonical_json_bytes(binding.descriptor.document())]
        expected_assigned = assignment["assigned_observation_item_ids"]
        synthetic_terminal = relation_observation_terminal_document(
            validated_request,
            terminal_kind="COMPLETED",
            canonical_relations=copy.deepcopy(terminal["canonical_relations"]),
            observation_outcomes=copy.deepcopy(terminal["observation_outcomes"]),
        )
        validated_terminal = validate_relation_observation_terminal_document(
            synthetic_terminal, request=lineage["request"]
        )
        expected_terminal = {
            "provider_run_id": validated_terminal["provider_run_id"],
            "provider_descriptor": copy.deepcopy(
                validated_terminal["provider_descriptor"]
            ),
            "provider_run_status": "COMPLETED",
            "phase_status": "COMPLETED",
            "release_outcome": "RELEASED",
            "diagnostic_code": None,
            "assigned_observation_item_ids": copy.deepcopy(expected_assigned),
            "reported_relation_ids": copy.deepcopy(
                validated_terminal["reported_relation_ids"]
            ),
            "canonical_relations": copy.deepcopy(
                validated_terminal["canonical_relations"]
            ),
            "observation_outcomes": copy.deepcopy(
                validated_terminal["observation_outcomes"]
            ),
        }
        accepted_outcomes = sorted(
            copy.deepcopy(validated_terminal["observation_outcomes"]),
            key=lambda item: item["observation_outcome_id"],
        )
        expected_receipt = {
            "provider_run_id": validated_terminal["provider_run_id"],
            "provider_descriptor": binding.descriptor.document(),
            "required": True,
            "execution_status": "COMPLETED",
            "assigned_observation_item_ids": sorted(set(expected_assigned)),
            "accepted_observation_outcomes": accepted_outcomes,
            "missing_observation_item_ids": [],
            "unexpected_observation_item_ids": [],
            "duplicate_observation_item_ids": [],
            "unexpected_relation_ids": [],
            "unreferenced_relation_ids": [],
            "invalid_outcome_ids": [],
        }
        if (
            lineage["binding"]
            != {
                "provider_descriptor": binding.descriptor.document(),
                "launch_key": binding.launch_key,
            }
            or lineage["request_sha256"]
            != hashlib.sha256(canonical_json_bytes(lineage["request"])).hexdigest()
            or lineage["terminal_sha256"]
            != hashlib.sha256(canonical_json_bytes(terminal)).hexdigest()
            or lineage["receipt"]["provider_descriptor"]
            != binding.descriptor.document()
            or lineage["request"]["request_provenance"] != expected_provenance
            or any(
                lineage["request"].get(key) != getattr(inputs, key)
                for key in (
                    "source_snapshot_digest",
                    "policy_digest",
                    "analysis_scope_digest",
                    "slice_policy_digest",
                    "derivation_profile_digest",
                )
            )
            or lineage["request"]["derivation_id"] != handoff["fact_derivation_id"]
            or lineage["request"]["fact_set_digest"] != fact_set["fact_set_digest"]
            or lineage["request"]["observation_domain_digest"]
            != validated_domain["observation_domain_digest"]
            or lineage["request"]["assigned_observation_item_ids"]
            != expected_assigned
            or terminal != expected_terminal
            or lineage["receipt"] != expected_receipt
        ):
            raise ValueError("Provider lineage identity mismatch")
        provider_run_ids.append(terminal["provider_run_id"])

    relation_set = document["relation_set"]
    merged, conflicts = _compose_carrier_candidates(document["provider_lineage"])
    expected_relation_set = _relation_set_document(
        inputs, fact_set, merged, conflicts
    )
    relation_payload = {
        "source_snapshot_digest": inputs.source_snapshot_digest,
        "analysis_scope_digest": inputs.analysis_scope_digest,
        "derivation_profile_digest": inputs.derivation_profile_digest,
        "fact_set_digest": fact_set["fact_set_digest"],
        "relations": [
            {
                key: copy.deepcopy(value)
                for key, value in item.items()
                if key != "provenance_refs"
            }
            for item in relation_set["relations"]
        ],
        "conflicts": [
            {
                key: copy.deepcopy(value)
                for key, value in item.items()
                if key != "provenance_refs"
            }
            for item in relation_set["conflicts"]
        ],
    }
    if (
        relation_set != expected_relation_set
        or relation_set["relation_set_digest"]
        != semantic_digest(RELATION_SET_FUNCTION, relation_payload)
        or admission["fact_consumer_attempt_id"]
        != handoff["fact_consumer_attempt_id"]
        or admission["handoff_claim_id"] != handoff["claim_id"]
        or admission["transition_attempt_id"]
        != document["transition_attempt"]["attempt_id"]
        or admission["fact_set_digest"] != fact_set["fact_set_digest"]
        or admission["observation_domain_digest"]
        != validated_domain["observation_domain_digest"]
        or admission["relation_set_digest"] != relation_set["relation_set_digest"]
        or admission["provider_run_ids"] != provider_run_ids
        or document["authority_ceiling"]
        != {
            "private_relation_transition": True,
            "review_slice_set": False,
            "coverage": False,
            "manifest": False,
            "persistence": False,
            "public_review": False,
        }
    ):
        raise ValueError("transition admission link mismatch")


def _admission_digest(document: Mapping[str, object]) -> str:
    admission = document["admission"]
    payload = {
        key: copy.deepcopy(value)
        for key, value in admission.items()
        if key != "admission_digest"
    }
    return semantic_digest(
        "veritrail.review.fact-relation-transition-admission/0.1", payload
    )


def _carrier_digest(document: Mapping[str, object]) -> str:
    carrier = {
        key: copy.deepcopy(value)
        for key, value in document.items()
        if key != "admission"
    }
    return semantic_digest(
        "veritrail.review.fact-relation-transition-carrier/0.1", carrier
    )
