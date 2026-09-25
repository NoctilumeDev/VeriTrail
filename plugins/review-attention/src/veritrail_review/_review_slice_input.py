from __future__ import annotations

import copy
from typing import Mapping

from veritrail_review._multi_provider_fact_composition import _fact_set_document
from veritrail_review._relation_set_admission import (
    _validate_qualification,
    _validate_admission_attempt_binding,
    admit_relation_set_for_private_closed_proof,
)
from veritrail_review._review_slice_input_cross_validation_values import (
    OwnedCrossValidatedAdmittedGraphSliceInput,
    _validate_cross_validated_input,
)
from veritrail_review._review_slice_input_values import (
    OwnedAdmittedGraphInputAuthority,
    OwnedAdmittedGraphSliceInput,
    OwnedRelationQualificationContinuation,
    _ReviewSliceInputError,
    _ReviewSliceInputFailureCode,
    _VALIDATED_ADMISSION_ATTEMPT_TOKEN,
)
from veritrail_review._review_slice_blocked_input_receipt_values import (
    OwnedReviewSliceBlockedInputReceipt,
    _validate_blocked_input_receipt,
)
from veritrail_review._review_slice_empty_domain_closure_values import (
    OwnedReviewSliceEmptyDomainClosure,
    _validate_empty_domain_closure,
)
from veritrail_review._review_slice_obligation_domain_values import (
    OwnedReviewSliceObligationDomainGate,
    _validate_obligation_domain_gate,
)
from veritrail_review._review_slice_obligation_closure_values import (
    OwnedReviewSliceObligationClosure,
    _validate_slice_obligation_closure,
)
from veritrail_review._review_slice_traversal_assignment_values import (
    OwnedReviewSliceTraversalAssignments,
    OwnedReviewSliceTraversalBoundary,
    _validate_traversal_assignments,
    _validate_traversal_boundary,
)
from veritrail_review._review_slice_traversal import (
    _derive_normal_review_slice_candidate,
)
from veritrail_review._review_slice_traversal_outcome_values import (
    OwnedReviewSliceTraversalOutcome,
    _validate_traversal_outcome,
)
from veritrail_review.canonical import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from veritrail_review.derivation_input import (
    _parse_artifact,
    _validate_cross_artifact_binding,
    _validate_policy,
    _validate_profile,
    _validate_snapshot,
)
from veritrail_review.derivation_input_contracts import (
    DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE,
    DerivationInputSet,
)
from veritrail_review.errors import DerivationInputFailureCode
from veritrail_review.git_objects import verify_git_object_bytes


def admit_relation_set_for_slice_input_private_closed_proof(
    qualified: OwnedRelationQualificationContinuation,
) -> OwnedAdmittedGraphInputAuthority:
    """Bind exact admission to the still-live qualification attempt."""

    if type(qualified) is not OwnedRelationQualificationContinuation:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
        )
    try:
        admitted = admit_relation_set_for_private_closed_proof(
            qualified.qualification
        )
        _validate_admission_attempt_binding(qualified.qualification, admitted)
        return qualified._bind_admission(
            admitted,
            _validated_attempt_token=_VALIDATED_ADMISSION_ATTEMPT_TOKEN,
        )
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.ADMISSION_BINDING_REJECTED
        ) from exc


def claim_admitted_graph_slice_input(
    inputs: DerivationInputSet,
    authority: OwnedAdmittedGraphInputAuthority,
) -> OwnedAdmittedGraphSliceInput:
    """Claim one exact A-stage input without constructing a domain or Slice."""

    if (
        type(inputs) is not DerivationInputSet
        or type(authority) is not OwnedAdmittedGraphInputAuthority
    ):
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED
        )
    try:
        qualification, admitted, continuation = authority._coordinates()
        _validate_admission_attempt_binding(qualification, admitted)
        if not continuation._bound_to(inputs):
            continuation.revoke()
            raise ValueError
        input_coordinates = (
            inputs.source_snapshot_digest,
            inputs.policy_digest,
            inputs.analysis_scope_digest,
            inputs.slice_policy_digest,
            inputs.derivation_profile_digest,
        )
        qualification_coordinates = (
            qualification.source_snapshot_digest,
            qualification.policy_digest,
            qualification.analysis_scope_digest,
            qualification.slice_policy_digest,
            qualification.derivation_profile_digest,
        )
        if (
            input_coordinates != qualification_coordinates
            or qualification.derivation_id != admitted.derivation_id
            or qualification.source_snapshot_digest
            != admitted.source_snapshot_digest
            or qualification.policy_digest != admitted.policy_digest
            or qualification.analysis_scope_digest
            != admitted.analysis_scope_digest
            or qualification.slice_policy_digest != admitted.slice_policy_digest
            or qualification.derivation_profile_digest
            != admitted.derivation_profile_digest
            or qualification.fact_set_digest != admitted.fact_set_digest
            or qualification.observation_domain_digest
            != admitted.observation_domain_digest
            or qualification.qualification_digest
            != admitted.qualification_digest
            or qualification.candidate_composition_status
            != admitted.candidate_composition_status
        ):
            continuation.revoke()
            raise ValueError
        joined = authority._claim(inputs)
        if not joined.continuation_permitted():
            raise ValueError
        return joined
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_JOIN_REJECTED
        ) from exc


def cross_validate_admitted_graph_slice_input(
    joined: OwnedAdmittedGraphSliceInput,
) -> OwnedCrossValidatedAdmittedGraphSliceInput:
    """Reconstruct B-stage exact inputs without rereading paths or minting budget."""

    if type(joined) is not OwnedAdmittedGraphSliceInput:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED
        )
    try:
        joined._claim_cross_validation()
        state = _ContinuationValidationState(joined)
        inputs = joined._owned_inputs()
        if (
            type(inputs) is not DerivationInputSet
            or type(inputs.source_snapshot_canonical_bytes) is not bytes
            or type(inputs.review_policy_canonical_bytes) is not bytes
            or type(inputs.derivation_profile_canonical_bytes) is not bytes
        ):
            raise ValueError

        snapshot = _parse_artifact(
            inputs.source_snapshot_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_SOURCE_SNAPSHOT,
            state,  # type: ignore[arg-type]
        )
        policy = _parse_artifact(
            inputs.review_policy_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY,
            state,  # type: ignore[arg-type]
        )
        profile = _parse_artifact(
            inputs.derivation_profile_canonical_bytes,
            DerivationInputFailureCode.NONCONFORMANT_DERIVATION_PROFILE,
            state,  # type: ignore[arg-type]
        )
        _validate_snapshot(
            snapshot,
            inputs.source_snapshot_canonical_bytes,
            state,  # type: ignore[arg-type]
        )
        _validate_profile(profile, state)  # type: ignore[arg-type]
        _validate_policy(policy, profile, state)  # type: ignore[arg-type]
        _validate_cross_artifact_binding(snapshot, policy, profile, state)  # type: ignore[arg-type]
        if (
            snapshot["source_snapshot_digest"] != inputs.source_snapshot_digest
            or policy["source_snapshot_digest"] != inputs.source_snapshot_digest
            or policy["policy_digest"] != inputs.policy_digest
            or policy["analysis_scope_digest"] != inputs.analysis_scope_digest
            or policy["slice_policy_digest"] != inputs.slice_policy_digest
            or policy["derivation_profile_digest"]
            != inputs.derivation_profile_digest
            or profile["profile_digest"] != inputs.derivation_profile_digest
        ):
            raise ValueError

        qualification = joined._owned_qualification()
        admitted = joined._owned_admission()
        _validate_admission_attempt_binding(qualification, admitted)
        normalized = _validate_qualification(qualification)
        fact_set, fact_set_digest = _fact_set_document(
            inputs, normalized["facts"], ()
        )
        fact_set_bytes = canonical_json_bytes(fact_set)
        if (
            fact_set_digest != joined.fact_set_digest
            or fact_set_digest != qualification.fact_set_digest
            or fact_set_digest != admitted.fact_set_digest
            or fact_set["source_snapshot_digest"] != joined.source_snapshot_digest
            or fact_set["policy_digest"] != joined.policy_digest
            or fact_set["analysis_scope_digest"] != joined.analysis_scope_digest
            or fact_set["derivation_profile_digest"]
            != joined.derivation_profile_digest
        ):
            raise ValueError

        owned_blobs = _validate_verified_blob_snapshot(inputs, snapshot, state)
        state.checkpoint("slice-input-cross-validation-complete")
        result = OwnedCrossValidatedAdmittedGraphSliceInput._create(
            joined=joined,
            fact_set_document_bytes=fact_set_bytes,
            verified_blob_bytes_by_object_identity=owned_blobs,
        )
        _validate_cross_validated_input(result)
        if not result.continuation_permitted():
            raise ValueError
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED
        ) from exc


def construct_review_slice_obligation_domain(
    validated: OwnedCrossValidatedAdmittedGraphSliceInput,
) -> OwnedReviewSliceObligationDomainGate:
    """Apply the C-stage conflict gate and construct the exact private domain."""

    if type(validated) is not OwnedCrossValidatedAdmittedGraphSliceInput:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED
        )
    try:
        validated._claim_obligation_domain()
        _validate_cross_validated_input(validated)
        if not validated.continuation_permitted():
            raise ValueError
        relation_set = validated.relation_set_document_copy()
        witness = validated.admission_witness_copy()
        claim = witness.get("qualification_claim")
        conflicts = relation_set.get("conflicts")
        if not isinstance(claim, Mapping) or not isinstance(conflicts, list):
            raise ValueError
        composition_status = claim.get("candidate_composition_status")

        if composition_status == "CONFLICTING":
            if not conflicts:
                raise ValueError
            result = OwnedReviewSliceObligationDomainGate._create(
                validated=validated,
                candidate_composition_status="CONFLICTING",
                slice_input_status="BLOCKED_BY_RELATION_CONFLICT",
                obligation_domain_document=None,
            )
        elif composition_status == "CONSISTENT":
            if conflicts:
                raise ValueError
            domain = _build_review_slice_obligation_domain(validated)
            result = OwnedReviewSliceObligationDomainGate._create(
                validated=validated,
                candidate_composition_status="CONSISTENT",
                slice_input_status="ELIGIBLE",
                obligation_domain_document=domain,
            )
        else:
            raise ValueError

        _validate_obligation_domain_gate(result)
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_DOMAIN_REJECTED
        ) from exc


def assign_review_slice_obligations_for_traversal(
    gate: OwnedReviewSliceObligationDomainGate,
) -> OwnedReviewSliceTraversalAssignments:
    """Assign the exact D-stage domain without accepting caller-owned specs."""

    if type(gate) is not OwnedReviewSliceObligationDomainGate:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED
        )
    try:
        gate._claim_traversal_assignments()
        _validate_obligation_domain_gate(gate)
        obligations = gate.obligations_copy()
        if (
            gate.slice_input_status != "ELIGIBLE"
            or obligations is None
            or not gate.continuation_permitted()
        ):
            raise ValueError
        result = OwnedReviewSliceTraversalAssignments._create(
            gate=gate,
            obligations=obligations,
        )
        _validate_traversal_assignments(result)
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_ASSIGNMENT_REJECTED
        ) from exc


def claim_next_review_slice_traversal(
    assignments: OwnedReviewSliceTraversalAssignments,
) -> OwnedReviewSliceTraversalBoundary:
    """Claim one opaque assignment as an exact D-stage traversal boundary."""

    if type(assignments) is not OwnedReviewSliceTraversalAssignments:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.TRAVERSAL_BOUNDARY_REJECTED
        )
    try:
        _validate_traversal_assignments(assignments)
        assignment_ordinal, assignment_digest, slice_spec_bytes = (
            assignments._claim_next()
        )
        result = OwnedReviewSliceTraversalBoundary._create(
            assignments=assignments,
            assignment_ordinal=assignment_ordinal,
            assignment_digest=assignment_digest,
            slice_spec_bytes=slice_spec_bytes,
        )
        _validate_traversal_boundary(result)
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.TRAVERSAL_BOUNDARY_REJECTED
        ) from exc


def derive_review_slice_traversal_outcome(
    boundary: OwnedReviewSliceTraversalBoundary,
) -> OwnedReviewSliceTraversalOutcome:
    """Run one assigned deterministic traversal and commit its normal outcome."""

    if type(boundary) is not OwnedReviewSliceTraversalBoundary:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED
        )
    try:
        boundary._claim_outcome()
        _validate_traversal_boundary(boundary)
        candidate = _derive_normal_review_slice_candidate(boundary)
        frontier = candidate["frontier"]
        if not isinstance(frontier, list):
            raise ValueError
        outcome_status = (
            "NORMAL_PARTIAL" if frontier else "NORMAL_COMPLETE"
        )
        document: dict[str, object] = {
            "derivation_id": boundary.derivation_id,
            "admission_witness_digest": boundary.admission_witness_digest,
            "slice_obligation_domain_digest": (
                boundary.slice_obligation_domain_digest
            ),
            "assignment_ordinal": boundary.assignment_ordinal,
            "assignment_digest": boundary.assignment_digest,
            "slice_spec_digest": boundary.slice_spec_digest,
            "outcome_status": outcome_status,
            "normal_slice_candidate": candidate,
        }
        document["traversal_outcome_digest"] = semantic_digest(
            "veritrail.review.private-slice-traversal-outcome/0.1",
            copy.deepcopy(document),
        )
        commit_bytes = canonical_json_bytes(document)
        committed = boundary._try_complete_outcome(commit_bytes)
        if committed is None:
            raise ValueError
        result = OwnedReviewSliceTraversalOutcome._create(
            boundary=boundary,
            outcome_document=document,
            committed_phase=committed,
        )
        _validate_traversal_outcome(result)
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.TRAVERSAL_OUTCOME_REJECTED
        ) from exc


def reconcile_review_slice_traversal_outcomes(
    assignments: OwnedReviewSliceTraversalAssignments,
    outcomes: tuple[OwnedReviewSliceTraversalOutcome, ...],
) -> OwnedReviewSliceObligationClosure:
    """Close one non-empty F-stage domain from its exact owned outcomes."""

    if type(assignments) is not OwnedReviewSliceTraversalAssignments:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED
        )
    try:
        _validate_traversal_assignments(assignments)
        if assignments.assignment_count == 0:
            raise ValueError
        assignments._claim_normal_reconciliation()
        if type(outcomes) is not tuple:
            raise ValueError

        gate = assignments._owned_domain_gate()
        obligations = gate.obligations_copy()
        if (
            obligations is None
            or len(obligations) != assignments.assignment_count
        ):
            raise ValueError
        by_ordinal: dict[int, OwnedReviewSliceTraversalOutcome] = {}
        for outcome in outcomes:
            if type(outcome) is not OwnedReviewSliceTraversalOutcome:
                raise ValueError
            _validate_traversal_outcome(outcome)
            boundary = outcome._owned_boundary()
            if (
                boundary._owned_assignments() is not assignments
                or outcome.derivation_id != assignments.derivation_id
                or outcome.admission_witness_digest
                != assignments.admission_witness_digest
                or outcome.slice_obligation_domain_digest
                != assignments.slice_obligation_domain_digest
                or outcome.assignment_ordinal in by_ordinal
                or outcome.assignment_ordinal < 0
                or outcome.assignment_ordinal >= assignments.assignment_count
                or outcome.assignment_digest
                != assignments.assignment_digests[outcome.assignment_ordinal]
            ):
                raise ValueError
            spec = obligations[outcome.assignment_ordinal]
            candidate = outcome.normal_slice_candidate_copy()
            if (
                outcome.slice_spec_digest != spec["slice_spec_digest"]
                or canonical_json_bytes(candidate["slice_spec"])
                != canonical_json_bytes(spec)
                or canonical_json_bytes(candidate)
                != canonical_json_bytes(
                    _derive_normal_review_slice_candidate(boundary)
                )
            ):
                raise ValueError
            by_ordinal[outcome.assignment_ordinal] = outcome

        expected_ordinals = tuple(range(assignments.assignment_count))
        if (
            set(by_ordinal) != set(expected_ordinals)
            or len({item.traversal_outcome_digest for item in outcomes})
            != len(outcomes)
        ):
            raise ValueError
        ordered_outcomes = tuple(by_ordinal[index] for index in expected_ordinals)
        validated = gate._owned_cross_validated_input()
        document: dict[str, object] = {
            "derivation_id": assignments.derivation_id,
            "admission_witness_digest": assignments.admission_witness_digest,
            "source_snapshot_digest": validated.source_snapshot_digest,
            "policy_digest": validated.policy_digest,
            "analysis_scope_digest": validated.analysis_scope_digest,
            "slice_policy_digest": validated.slice_policy_digest,
            "derivation_profile_digest": validated.derivation_profile_digest,
            "fact_set_digest": validated.fact_set_digest,
            "relation_set_digest": validated.relation_set_digest,
            "slice_obligation_domain_digest": (
                assignments.slice_obligation_domain_digest
            ),
            "closure_status": "NORMAL_CLOSED",
            "traversal_outcomes": [
                item.outcome_document_copy() for item in ordered_outcomes
            ],
            "normal_slice_candidates": [
                item.normal_slice_candidate_copy() for item in ordered_outcomes
            ],
        }
        document["slice_obligation_closure_digest"] = semantic_digest(
            "veritrail.review.private-slice-obligation-closure/0.1",
            copy.deepcopy(document),
        )
        commit_bytes = canonical_json_bytes(document)
        committed = assignments._try_complete_obligation_closure(commit_bytes)
        if committed is None:
            raise ValueError
        result = OwnedReviewSliceObligationClosure._create(
            assignments=assignments,
            outcomes=ordered_outcomes,
            closure_document=document,
            committed_phase=committed,
        )
        _validate_slice_obligation_closure(result)
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_RECONCILIATION_REJECTED
        ) from exc


def close_empty_review_slice_obligation_domain(
    assignments: OwnedReviewSliceTraversalAssignments,
) -> OwnedReviewSliceEmptyDomainClosure:
    """Close one exact zero-anchor domain without inferring absence from output."""

    if type(assignments) is not OwnedReviewSliceTraversalAssignments:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED
        )
    try:
        _validate_traversal_assignments(assignments)
        gate = assignments._owned_domain_gate()
        obligations = gate.obligations_copy()
        if (
            gate.candidate_composition_status != "CONSISTENT"
            or gate.slice_input_status != "ELIGIBLE"
            or obligations != []
            or assignments.assignment_count != 0
            or assignments.remaining_assignment_count() != 0
        ):
            raise ValueError
        assignments._claim_closed_empty_reconciliation()
        validated = gate._owned_cross_validated_input()
        document: dict[str, object] = {
            "derivation_id": assignments.derivation_id,
            "admission_witness_digest": assignments.admission_witness_digest,
            "source_snapshot_digest": validated.source_snapshot_digest,
            "policy_digest": validated.policy_digest,
            "analysis_scope_digest": validated.analysis_scope_digest,
            "slice_policy_digest": validated.slice_policy_digest,
            "derivation_profile_digest": validated.derivation_profile_digest,
            "fact_set_digest": validated.fact_set_digest,
            "relation_set_digest": validated.relation_set_digest,
            "slice_obligation_domain_digest": (
                assignments.slice_obligation_domain_digest
            ),
            "closure_status": "CLOSED_EMPTY",
            "assignment_count": 0,
            "traversal_outcomes": [],
            "normal_slice_candidates": [],
        }
        document["empty_domain_closure_digest"] = semantic_digest(
            "veritrail.review.private-slice-empty-domain-closure/0.1",
            copy.deepcopy(document),
        )
        commit_bytes = canonical_json_bytes(document)
        committed = assignments._try_complete_closed_empty_obligation_closure(
            commit_bytes
        )
        if committed is None:
            raise ValueError
        result = OwnedReviewSliceEmptyDomainClosure._create(
            assignments=assignments,
            closure_document=document,
            committed_phase=committed,
        )
        _validate_empty_domain_closure(result)
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED
        ) from exc


def record_blocked_review_slice_input(
    gate: OwnedReviewSliceObligationDomainGate,
) -> OwnedReviewSliceBlockedInputReceipt:
    """Record one admitted conflict world without inventing a normal domain."""

    if type(gate) is not OwnedReviewSliceObligationDomainGate:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED
        )
    try:
        _validate_obligation_domain_gate(gate)
        if (
            gate.candidate_composition_status != "CONFLICTING"
            or gate.slice_input_status != "BLOCKED_BY_RELATION_CONFLICT"
            or gate.slice_obligation_domain_digest is not None
            or gate.obligation_domain_document_copy() is not None
            or gate.obligations_copy() is not None
        ):
            raise ValueError
        gate._claim_blocked_input_receipt()
        validated = gate._owned_cross_validated_input()
        relation_set = validated.relation_set_document_copy()
        conflicts = relation_set.get("conflicts")
        if not isinstance(conflicts, list) or not conflicts:
            raise ValueError
        conflict_ids = [item.get("conflict_id") for item in conflicts]
        if any(not isinstance(item, str) for item in conflict_ids):
            raise ValueError
        document: dict[str, object] = {
            "derivation_id": gate.derivation_id,
            "admission_witness_digest": gate.admission_witness_digest,
            "source_snapshot_digest": validated.source_snapshot_digest,
            "policy_digest": validated.policy_digest,
            "analysis_scope_digest": validated.analysis_scope_digest,
            "slice_policy_digest": validated.slice_policy_digest,
            "derivation_profile_digest": validated.derivation_profile_digest,
            "fact_set_digest": validated.fact_set_digest,
            "relation_set_digest": validated.relation_set_digest,
            "candidate_composition_status": "CONFLICTING",
            "slice_input_status": "BLOCKED_BY_RELATION_CONFLICT",
            "slice_obligation_domain_digest": None,
            "slice_derivation_denominator_status": "UNKNOWN",
            "reason_codes": [
                "PROVIDER_CONFLICT",
                "UPSTREAM_DENOMINATOR_UNKNOWN",
            ],
            "relation_conflict_ids": conflict_ids,
            "normal_slice_candidates": [],
        }
        document["blocked_input_receipt_digest"] = semantic_digest(
            "veritrail.review.private-slice-blocked-input-receipt/0.1",
            copy.deepcopy(document),
        )
        commit_bytes = canonical_json_bytes(document)
        committed = gate._try_complete_blocked_input_receipt(commit_bytes)
        if committed is None:
            raise ValueError
        result = OwnedReviewSliceBlockedInputReceipt._create(
            gate=gate,
            receipt_document=document,
            committed_phase=committed,
        )
        _validate_blocked_input_receipt(result)
        return result
    except _ReviewSliceInputError:
        raise
    except Exception as exc:
        raise _ReviewSliceInputError(
            _ReviewSliceInputFailureCode.OBLIGATION_ACCOUNTING_REJECTED
        ) from exc


def _build_review_slice_obligation_domain(
    validated: OwnedCrossValidatedAdmittedGraphSliceInput,
) -> dict[str, object]:
    if not validated.continuation_permitted():
        raise ValueError
    policy = validated.review_policy_document_copy()
    profile = validated.derivation_profile_document_copy()
    fact_set = validated.fact_set_document_copy()
    slice_policy = policy.get("slice_policy")
    facts = fact_set.get("facts")
    profile_fact_kinds = profile.get("fact_kinds")
    if (
        not isinstance(slice_policy, Mapping)
        or not isinstance(facts, list)
        or not isinstance(profile_fact_kinds, list)
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
    anchors: list[Mapping[str, object]] = []
    for fact in facts:
        if not validated.continuation_permitted() or not isinstance(fact, Mapping):
            raise ValueError
        fact_kind = fact.get("fact_kind")
        fact_id = fact.get("fact_id")
        if fact_kind not in fact_kind_rank or not isinstance(fact_id, str):
            raise ValueError
        if fact_kind in anchor_fact_kinds:
            anchors.append(fact)
    anchors.sort(key=lambda item: (fact_kind_rank[item["fact_kind"]], item["fact_id"]))

    obligations: list[dict[str, object]] = []
    for anchor in anchors:
        if not validated.continuation_permitted():
            raise ValueError
        spec: dict[str, object] = {
            "source_snapshot_digest": validated.source_snapshot_digest,
            "analysis_scope_digest": validated.analysis_scope_digest,
            "slice_policy_digest": validated.slice_policy_digest,
            "derivation_profile_digest": validated.derivation_profile_digest,
            "fact_set_digest": validated.fact_set_digest,
            "relation_set_digest": validated.relation_set_digest,
            "anchor_fact_id": anchor["fact_id"],
            "allowed_relations": copy.deepcopy(allowed_relations),
            "max_depth": slice_policy["max_depth"],
            "max_symbols": slice_policy["max_symbols"],
            "max_files": slice_policy["max_files"],
            "max_relations": slice_policy["max_relations"],
        }
        spec["slice_spec_digest"] = semantic_digest(
            "veritrail.review.slice-spec/0.1", spec
        )
        obligations.append(spec)
    if len({item["slice_spec_digest"] for item in obligations}) != len(
        obligations
    ):
        raise ValueError

    domain: dict[str, object] = {
        "source_snapshot_digest": validated.source_snapshot_digest,
        "policy_digest": validated.policy_digest,
        "analysis_scope_digest": validated.analysis_scope_digest,
        "slice_policy_digest": validated.slice_policy_digest,
        "derivation_profile_digest": validated.derivation_profile_digest,
        "fact_set_digest": validated.fact_set_digest,
        "relation_set_digest": validated.relation_set_digest,
        "obligations": obligations,
    }
    domain["slice_obligation_domain_digest"] = semantic_digest(
        "veritrail.review.slice-obligation-domain/0.1",
        {key: copy.deepcopy(item) for key, item in domain.items() if key != "policy_digest"},
    )
    return domain


class _ContinuationValidationState:
    """Duck-typed validator state backed by the original derivation budget."""

    profile = DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE

    def __init__(self, joined: OwnedAdmittedGraphSliceInput) -> None:
        self.__joined = joined

    def checkpoint(self, _stage: str) -> None:
        if not self.__joined.continuation_permitted():
            raise _ReviewSliceInputError(
                _ReviewSliceInputFailureCode.INPUT_CROSS_VALIDATION_REJECTED
            )


def _validate_verified_blob_snapshot(
    inputs: DerivationInputSet,
    snapshot: Mapping[str, object],
    state: _ContinuationValidationState,
) -> dict[str, bytes]:
    inventory = snapshot["inventory"]
    if not isinstance(inventory, list):
        raise ValueError
    expected: dict[str, tuple[str, int, str]] = {}
    for item in inventory:
        if not isinstance(item, Mapping):
            raise ValueError
        git_object = item["git_object"]
        if not isinstance(git_object, Mapping):
            raise ValueError
        if git_object["object_type"] != "BLOB":
            continue
        content = item.get("content")
        if not isinstance(content, Mapping):
            raise ValueError
        oid = git_object["hex"]
        algorithm = git_object["algorithm"]
        size = content["size_bytes"]
        digest = content["sha256"]
        if (
            not isinstance(oid, str)
            or not isinstance(algorithm, str)
            or type(size) is not int
            or size < 0
            or not isinstance(digest, str)
        ):
            raise ValueError
        identity = (algorithm, size, digest)
        previous = expected.setdefault(oid, identity)
        if previous != identity:
            raise ValueError

    supplied = inputs.verified_blob_bytes_by_object_identity
    if not isinstance(supplied, Mapping) or set(supplied) != set(expected):
        raise ValueError
    owned: dict[str, bytes] = {}
    for oid in sorted(expected):
        state.checkpoint("slice-input-blob-validation")
        value = supplied[oid]
        algorithm, size, digest = expected[oid]
        if (
            type(value) is not bytes
            or len(value) != size
            or sha256_bytes(value) != digest
        ):
            raise ValueError
        verify_git_object_bytes(
            algorithm=algorithm,
            object_type="blob",
            oid=oid,
            declared_size=size,
            body=value,
        )
        owned[oid] = value
    return owned
