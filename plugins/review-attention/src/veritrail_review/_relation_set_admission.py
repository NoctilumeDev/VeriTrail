from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Mapping, Sequence

from veritrail_review._execution_cell_application import provider_run_id
from veritrail_review._execution_cell_binding import ProviderDescriptor
from veritrail_review._execution_cell_values import (
    OwnedExecutionCellPhaseResult,
    PhaseStatus,
    ProviderRunStatus,
    ReleaseOutcome,
)
from veritrail_review._multi_provider_applicability import (
    closed_test_multi_provider_bindings,
)
from veritrail_review._relation_observation_binding import (
    closed_test_relation_observation_bindings,
    relation_observation_descriptor_rank,
)
from veritrail_review._relation_observation_cell_values import (
    OwnedRelationObservationCellPhaseResult,
)
from veritrail_review._relation_observation_domain import (
    observation_profile_document,
)
from veritrail_review._relation_observation_qualification import (
    _compose_candidates,
    _observation_receipt,
    _provider_run_document as _relation_provider_run_document,
)
from veritrail_review._relation_observation_qualification_values import (
    OwnedRelationCompositionQualificationResult,
)
from veritrail_review._relation_set_admission_values import (
    OwnedDerivationEvidence02Projection,
    OwnedRelationSetAdmissionState,
    _RelationSetAdmissionError,
    _RelationSetAdmissionFailureCode,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


_ADMISSION_TOKEN = object()
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_FACT_KEYS = {
    "source_snapshot_digest",
    "derivation_profile_digest",
    "fact_id",
    "subject_key_digest",
    "subject_space",
    "fact_kind",
    "source_anchor",
    "local_ordinal",
    "semantic_attributes",
    "provenance_refs",
}
_RELATION_KEYS = {
    "relation_id",
    "relation_subject_digest",
    "relation_space",
    "relation_kind",
    "source_fact_id",
    "local_ordinal",
    "target",
    "semantic_attributes",
    "provenance_refs",
}
_DOMAIN_KEYS = {
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "derivation_profile_digest",
    "fact_set_digest",
    "observation_profile_id",
    "observation_profile_version",
    "observation_profile_digest",
    "capability_id",
    "required",
    "composition_mode",
    "observation_items",
    "provider_responsibilities",
    "observation_domain_digest",
}


def admit_relation_set_for_private_closed_proof(
    qualification: OwnedRelationCompositionQualificationResult,
) -> OwnedRelationSetAdmissionState:
    """Admit an exact qualified composition without creating any public file."""

    try:
        normalized = _validate_qualification(qualification)
    except _RelationSetAdmissionError:
        raise
    except Exception as exc:
        raise _RelationSetAdmissionError(
            _RelationSetAdmissionFailureCode.QUALIFICATION_REJECTED
        ) from exc

    try:
        relation_set = _relation_set_document(qualification, normalized)
        relation_set_bytes = canonical_json_bytes(relation_set)
    except Exception as exc:
        raise _RelationSetAdmissionError(
            _RelationSetAdmissionFailureCode.RELATION_SET_REJECTED
        ) from exc

    try:
        witness = _admission_witness(qualification, normalized, relation_set)
        witness_bytes = canonical_json_bytes(witness)
    except Exception as exc:
        raise _RelationSetAdmissionError(
            _RelationSetAdmissionFailureCode.WITNESS_REJECTED
        ) from exc

    phases = (
        *qualification.fact_phase_results,
        *qualification.relation_phase_results,
    )
    request_provenance_bytes = normalized["request_provenance_bytes"]
    provider_run_bytes = normalized["all_provider_run_bytes"]
    state_values = {
        "derivation_id": qualification.derivation_id,
        "source_snapshot_digest": qualification.source_snapshot_digest,
        "policy_digest": qualification.policy_digest,
        "analysis_scope_digest": qualification.analysis_scope_digest,
        "slice_policy_digest": qualification.slice_policy_digest,
        "derivation_profile_digest": qualification.derivation_profile_digest,
        "fact_set_digest": qualification.fact_set_digest,
        "observation_domain_digest": qualification.observation_domain_digest,
        "qualification_digest": qualification.qualification_digest,
        "candidate_composition_status": qualification.candidate_composition_status,
        "relation_set_document_bytes": relation_set_bytes,
        "canonical_relation_set_artifact_bytes": relation_set_bytes + b"\n",
        "relation_set_digest": relation_set["relation_set_digest"],
        "admission_witness_bytes": witness_bytes,
        "admission_witness_digest": witness["admission_claim"][
            "admission_witness_digest"
        ],
        "request_provenance_bytes": request_provenance_bytes,
        "provider_run_bytes": provider_run_bytes,
        "started_at": min(phase.attempt_started_at for phase in phases),
        "finished_at": max(phase.phase_finished_at for phase in phases),
        "admitted_relation_ids": tuple(
            relation["relation_id"] for relation in relation_set["relations"]
        ),
        "admitted_conflict_ids": tuple(
            conflict["conflict_id"] for conflict in relation_set["conflicts"]
        ),
    }
    return OwnedRelationSetAdmissionState(
        **state_values,
        _state_seal=_private_state_seal(state_values),
        _construction_token=_ADMISSION_TOKEN,
    )


def project_private_derivation_evidence_0_2(
    admitted: OwnedRelationSetAdmissionState,
) -> OwnedDerivationEvidence02Projection:
    """Serialize an established witness; never construct or infer one here."""

    try:
        _validate_admitted_state(admitted)
        provider_runs = admitted.provider_runs_copy()
        witness = admitted.admission_witness_copy()
        document: dict[str, object] = {
            "artifact_kind": "DERIVATION_EVIDENCE",
            "schema_version": "0.2",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "derivation_id": admitted.derivation_id,
            "request_provenance": admitted.request_provenance_copy(),
            "source_snapshot_digest": admitted.source_snapshot_digest,
            "policy_digest": admitted.policy_digest,
            "analysis_scope_digest": admitted.analysis_scope_digest,
            "slice_policy_digest": admitted.slice_policy_digest,
            "derivation_profile_digest": admitted.derivation_profile_digest,
            "provider_runs": provider_runs,
            "overall_execution_status": "COMPLETED",
            "started_at": admitted.started_at,
            "finished_at": admitted.finished_at,
            "diagnostics": [],
            "relation_admission": witness,
        }
        digest = semantic_digest(
            "veritrail.review.derivation-evidence/0.2", document
        )
        document["derivation_evidence_digest"] = digest
        _validate_evidence_projection(admitted, document)
        return OwnedDerivationEvidence02Projection(
            document_bytes=canonical_json_bytes(document),
            derivation_evidence_digest=digest,
        )
    except _RelationSetAdmissionError:
        raise
    except Exception as exc:
        raise _RelationSetAdmissionError(
            _RelationSetAdmissionFailureCode.EVIDENCE_PROJECTION_REJECTED
        ) from exc


def _validate_qualification(
    value: OwnedRelationCompositionQualificationResult,
) -> dict[str, object]:
    if type(value) is not OwnedRelationCompositionQualificationResult:
        raise ValueError
    if (
        value.qualification_status != "QUALIFIED"
        or value.required_source_set_terminal_closure != "COMPLETE"
        or value.required_observation_closure != "COMPLETE"
        or value.candidate_composition_status not in {"CONSISTENT", "CONFLICTING"}
        or value.reason_codes != ()
        or not value.derivation_id
    ):
        raise ValueError
    for digest in (
        value.source_snapshot_digest,
        value.policy_digest,
        value.analysis_scope_digest,
        value.slice_policy_digest,
        value.derivation_profile_digest,
        value.fact_set_digest,
        value.observation_domain_digest,
        value.qualification_digest,
    ):
        if not isinstance(digest, str) or _HEX_64.fullmatch(digest) is None:
            raise ValueError

    fact_phases = value.fact_phase_results
    relation_phases = value.relation_phase_results
    expected_fact = closed_test_multi_provider_bindings()
    expected_relation = closed_test_relation_observation_bindings()
    if (
        len(fact_phases) != len(expected_fact)
        or len(relation_phases) != len(expected_relation)
        or tuple(phase.provider_descriptor for phase in fact_phases)
        != tuple(binding.descriptor for binding in expected_fact)
        or tuple(phase.provider_descriptor for phase in relation_phases)
        != tuple(binding.descriptor for binding in expected_relation)
    ):
        raise ValueError

    request_provenance_bytes: bytes | None = None
    for phase in (*fact_phases, *relation_phases):
        if not isinstance(
            phase,
            (OwnedExecutionCellPhaseResult, OwnedRelationObservationCellPhaseResult),
        ):
            raise ValueError
        if (
            phase.derivation_id != value.derivation_id
            or phase.source_snapshot_digest != value.source_snapshot_digest
            or phase.policy_digest != value.policy_digest
            or phase.analysis_scope_digest != value.analysis_scope_digest
            or phase.slice_policy_digest != value.slice_policy_digest
            or phase.derivation_profile_digest != value.derivation_profile_digest
            or phase.provider_run_status is not ProviderRunStatus.COMPLETED
            or phase.phase_status is not PhaseStatus.COMPLETED
            or phase.release_outcome is not ReleaseOutcome.RELEASED
            or phase.diagnostic_code is not None
            or phase.provider_run_id
            != provider_run_id(
                value.derivation_id,
                phase.provider_descriptor,
                phase.operands_digest,
            )
        ):
            raise ValueError
        raw = memoryview(phase.request_provenance_bytes).tobytes()
        if canonical_json_bytes(_owned_object(raw)) != raw:
            raise ValueError
        if request_provenance_bytes is None:
            request_provenance_bytes = raw
        elif raw != request_provenance_bytes:
            raise ValueError
    if request_provenance_bytes is None:
        raise ValueError

    facts = _merge_and_validate_facts(value, fact_phases)
    expected_domain = _expected_observation_domain(value, facts)
    domain = value.observation_domain_copy()
    if (
        set(domain) != _DOMAIN_KEYS
        or domain != expected_domain
        or canonical_json_bytes(domain) != value.observation_domain_bytes
        or domain["observation_domain_digest"] != value.observation_domain_digest
    ):
        raise ValueError

    relation_runs: list[dict[str, object]] = []
    receipts: list[dict[str, object]] = []
    for phase in relation_phases:
        if (
            phase.fact_set_digest != value.fact_set_digest
            or phase.observation_domain_digest != value.observation_domain_digest
        ):
            raise ValueError
        responsibility = next(
            item
            for item in domain["provider_responsibilities"]
            if item["provider_descriptor"] == phase.provider_descriptor.document()
        )
        expected_operands = semantic_digest(
            "veritrail.review.provider-operands/0.3",
            {
                "source_snapshot_digest": value.source_snapshot_digest,
                "policy_digest": value.policy_digest,
                "analysis_scope_digest": value.analysis_scope_digest,
                "slice_policy_digest": value.slice_policy_digest,
                "derivation_profile_digest": value.derivation_profile_digest,
                **phase.provider_descriptor.document(),
                "fact_set_digest": value.fact_set_digest,
                "observation_domain_digest": value.observation_domain_digest,
                "assigned_observation_item_ids": responsibility[
                    "assigned_observation_item_ids"
                ],
            },
        )
        if (
            phase.operands_digest != expected_operands
            or list(phase.assigned_observation_item_ids)
            != responsibility["assigned_observation_item_ids"]
        ):
            raise ValueError
        receipt = _observation_receipt(domain, phase.provider_descriptor, phase)
        receipts.append(receipt)
        relation_runs.append(_relation_provider_run_document(phase))

    stored_receipts = list(value.observation_receipts_copy())
    stored_relation_runs = list(value.relation_provider_runs_copy())
    if receipts != stored_receipts or relation_runs != stored_relation_runs:
        raise ValueError
    if any(
        canonical_json_bytes(item) != raw
        for item, raw in zip(stored_receipts, value.observation_receipt_bytes)
    ) or any(
        canonical_json_bytes(item) != raw
        for item, raw in zip(stored_relation_runs, value.relation_provider_run_bytes)
    ):
        raise ValueError

    merged, conflicts = _compose_candidates(relation_phases)
    stored_merged = value.merged_candidates_copy()
    stored_conflicts = value.private_conflicts_copy()
    if merged != stored_merged or conflicts != stored_conflicts:
        raise ValueError
    if any(
        canonical_json_bytes(item) != raw
        for item, raw in zip(stored_merged, value.merged_candidate_bytes)
    ) or any(
        canonical_json_bytes(item) != raw
        for item, raw in zip(stored_conflicts, value.private_conflict_bytes)
    ):
        raise ValueError
    _validate_relations(value, facts, domain, merged, relation_runs)

    qualification_claim = _qualification_claim(value, relation_runs, receipts, merged, conflicts)
    if qualification_claim["qualification_digest"] != value.qualification_digest:
        raise ValueError

    fact_runs = tuple(_fact_provider_run_document(phase) for phase in fact_phases)
    all_runs = tuple(sorted((*fact_runs, *relation_runs), key=_provider_run_rank))
    return {
        "request_provenance_bytes": request_provenance_bytes,
        "facts": facts,
        "domain": domain,
        "receipts": receipts,
        "relation_runs": relation_runs,
        "qualification_claim": qualification_claim,
        "merged": merged,
        "conflicts": conflicts,
        "all_provider_run_bytes": tuple(canonical_json_bytes(item) for item in all_runs),
    }


def _validate_admission_attempt_binding(
    qualification: OwnedRelationCompositionQualificationResult,
    admitted: OwnedRelationSetAdmissionState,
) -> None:
    """Require admission and qualification to carry one exact attempt history."""

    normalized = _validate_qualification(qualification)
    _validate_admitted_state(admitted)
    phases = (*qualification.fact_phase_results, *qualification.relation_phase_results)
    if (
        qualification.derivation_id != admitted.derivation_id
        or qualification.source_snapshot_digest != admitted.source_snapshot_digest
        or qualification.policy_digest != admitted.policy_digest
        or qualification.analysis_scope_digest != admitted.analysis_scope_digest
        or qualification.slice_policy_digest != admitted.slice_policy_digest
        or qualification.derivation_profile_digest
        != admitted.derivation_profile_digest
        or qualification.fact_set_digest != admitted.fact_set_digest
        or qualification.observation_domain_digest
        != admitted.observation_domain_digest
        or qualification.qualification_digest != admitted.qualification_digest
        or qualification.candidate_composition_status
        != admitted.candidate_composition_status
        or admitted.request_provenance_bytes
        != normalized["request_provenance_bytes"]
        or admitted.provider_run_bytes != normalized["all_provider_run_bytes"]
        or admitted.started_at
        != min(phase.attempt_started_at for phase in phases)
        or admitted.finished_at
        != max(phase.phase_finished_at for phase in phases)
    ):
        raise ValueError


def _merge_and_validate_facts(
    qualification: OwnedRelationCompositionQualificationResult,
    phases: Sequence[OwnedExecutionCellPhaseResult],
) -> tuple[dict[str, object], ...]:
    by_id: dict[str, dict[str, object]] = {}
    semantics: dict[str, bytes] = {}
    for phase in phases:
        local = phase.canonical_facts_copy()
        ids = [item.get("fact_id") for item in local]
        if (
            ids != sorted(set(ids))
            or tuple(ids) != phase.reported_fact_ids
            or phase.reported_relation_ids != ()
            or len(local) != len(phase.canonical_fact_bytes)
        ):
            raise ValueError
        for fact, raw in zip(local, phase.canonical_fact_bytes):
            if canonical_json_bytes(fact) != raw:
                raise ValueError
            _validate_fact(qualification, fact, phase.provider_run_id)
            fact_id = fact["fact_id"]
            semantic = {
                key: copy.deepcopy(value)
                for key, value in fact.items()
                if key != "provenance_refs"
            }
            semantic_bytes = canonical_json_bytes(semantic)
            previous = semantics.setdefault(fact_id, semantic_bytes)
            if previous != semantic_bytes:
                raise ValueError
            if fact_id not in by_id:
                by_id[fact_id] = copy.deepcopy(fact)
            refs = set(by_id[fact_id]["provenance_refs"])
            refs.update(fact["provenance_refs"])
            by_id[fact_id]["provenance_refs"] = sorted(refs)
    facts = tuple(by_id[key] for key in sorted(by_id))
    expected_digest = semantic_digest(
        "veritrail.review.fact-set/0.1",
        {
            "source_snapshot_digest": qualification.source_snapshot_digest,
            "analysis_scope_digest": qualification.analysis_scope_digest,
            "derivation_profile_digest": qualification.derivation_profile_digest,
            "facts": [
                {key: copy.deepcopy(value) for key, value in fact.items() if key != "provenance_refs"}
                for fact in facts
            ],
            "conflicts": [],
        },
    )
    if expected_digest != qualification.fact_set_digest:
        raise ValueError
    return facts


def _validate_fact(
    qualification: OwnedRelationCompositionQualificationResult,
    fact: Mapping[str, object],
    run_id: str,
) -> None:
    if (
        set(fact) != _FACT_KEYS
        or fact["source_snapshot_digest"] != qualification.source_snapshot_digest
        or fact["derivation_profile_digest"]
        != qualification.derivation_profile_digest
        or fact["provenance_refs"] != [run_id]
    ):
        raise ValueError
    ordinal = fact["local_ordinal"]
    anchor = fact["source_anchor"]
    if (
        type(ordinal) is not int
        or ordinal < 0
        or not isinstance(anchor, Mapping)
        or set(anchor) != {"git_path", "start_byte", "end_byte"}
    ):
        raise ValueError
    subject = semantic_digest(
        "veritrail.review.fact-subject/0.1",
        {
            "source_snapshot_digest": qualification.source_snapshot_digest,
            "derivation_profile_digest": qualification.derivation_profile_digest,
            "source_anchor": copy.deepcopy(dict(anchor)),
            "subject_space": fact["subject_space"],
            "local_ordinal": ordinal,
        },
    )
    fact_id = semantic_digest(
        "veritrail.review.code-fact/0.1",
        {
            "subject_key_digest": subject,
            "fact_kind": fact["fact_kind"],
            "semantic_attributes": copy.deepcopy(fact["semantic_attributes"]),
        },
    )
    if fact["subject_key_digest"] != subject or fact["fact_id"] != fact_id:
        raise ValueError


def _expected_observation_domain(
    qualification: OwnedRelationCompositionQualificationResult,
    facts: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    modules = [item for item in facts if item["fact_kind"] == "MODULE"]
    imports = [item for item in facts if item["fact_kind"] == "IMPORT_DECLARATION"]
    if len(modules) != 1 or len(modules) + len(imports) != len(facts):
        raise ValueError
    module = modules[0]
    module_path = module["source_anchor"]["git_path"]
    if module["local_ordinal"] != 0:
        raise ValueError
    for item in imports:
        attributes = item["semantic_attributes"]
        if (
            item["source_anchor"]["git_path"] != module_path
            or item["local_ordinal"] != 0
            or not isinstance(attributes, Mapping)
            or set(attributes)
            != {"import_form", "relative_level", "module_parts", "imported_name", "alias_name"}
            or attributes["import_form"] != "IMPORT"
            or attributes["relative_level"] != 0
            or not isinstance(attributes["module_parts"], list)
            or not attributes["module_parts"]
            or attributes["imported_name"] is not None
        ):
            raise ValueError
    items: list[dict[str, object]] = []
    for fact in imports:
        for kind, role in (
            ("LEXICAL_CONTAINS", "TARGET_FACT"),
            ("IMPORT_TARGET_LITERAL", "SOURCE_FACT"),
        ):
            payload = {
                "source_snapshot_digest": qualification.source_snapshot_digest,
                "derivation_profile_digest": qualification.derivation_profile_digest,
                "fact_set_digest": qualification.fact_set_digest,
                "relation_kind": kind,
                "subject_role": role,
                "subject_fact_id": fact["fact_id"],
            }
            items.append(
                {
                    "observation_item_id": semantic_digest(
                        "veritrail.review.relation-observation-item/0.1", payload
                    ),
                    **payload,
                }
            )
    family_rank = {"LEXICAL_CONTAINS": 0, "IMPORT_TARGET_LITERAL": 1}
    role_rank = {"SOURCE_FACT": 0, "TARGET_FACT": 1}
    items.sort(
        key=lambda item: (
            family_rank[item["relation_kind"]],
            role_rank[item["subject_role"]],
            item["subject_fact_id"],
        )
    )
    profile = observation_profile_document()
    profile_digest = semantic_digest(
        "veritrail.review.relation-observation-profile/0.1",
        {**profile, "derivation_profile_digest": qualification.derivation_profile_digest},
    )
    by_kind = {
        kind: [item["observation_item_id"] for item in items if item["relation_kind"] == kind]
        for kind in family_rank
    }
    responsibilities: list[dict[str, object]] = []
    for rule in profile["provider_responsibility_rules"]:
        responsibilities.append(
            {
                "provider_descriptor": copy.deepcopy(rule["provider_descriptor"]),
                "required": True,
                "assigned_observation_item_ids": sorted(
                    {
                        item_id
                        for kind in rule["assigned_relation_families"]
                        for item_id in by_kind[kind]
                    }
                ),
            }
        )
    responsibilities.sort(
        key=lambda item: relation_observation_descriptor_rank(
            ProviderDescriptor(**item["provider_descriptor"])
        )
    )
    projection = {
        "source_snapshot_digest": qualification.source_snapshot_digest,
        "analysis_scope_digest": qualification.analysis_scope_digest,
        "derivation_profile_digest": qualification.derivation_profile_digest,
        "fact_set_digest": qualification.fact_set_digest,
        "observation_profile_id": profile["observation_profile_id"],
        "observation_profile_version": profile["observation_profile_version"],
        "observation_profile_digest": profile_digest,
        "capability_id": profile["capability_id"],
        "required": True,
        "composition_mode": "CUMULATIVE",
        "observation_items": items,
        "provider_responsibilities": responsibilities,
    }
    return {
        **copy.deepcopy(projection),
        "policy_digest": qualification.policy_digest,
        "observation_domain_digest": semantic_digest(
            "veritrail.review.relation-observation-domain/0.1", projection
        ),
    }


def _validate_relations(
    qualification: OwnedRelationCompositionQualificationResult,
    facts: Sequence[Mapping[str, object]],
    domain: Mapping[str, object],
    relations: Sequence[Mapping[str, object]],
    provider_runs: Sequence[Mapping[str, object]],
) -> None:
    facts_by_id = {item["fact_id"]: item for item in facts}
    run_ids = {item["provider_run_id"] for item in provider_runs}
    items = domain["observation_items"]
    accepted_by_relation: dict[str, set[str]] = {}
    for receipt in qualification.observation_receipts_copy():
        for outcome in receipt["accepted_observation_outcomes"]:
            for relation_id in outcome["reported_relation_ids"]:
                accepted_by_relation.setdefault(relation_id, set()).add(
                    outcome["provider_run_id"]
                )
    for relation in relations:
        if set(relation) != _RELATION_KEYS:
            raise ValueError
        source = facts_by_id.get(relation["source_fact_id"])
        ordinal = relation["local_ordinal"]
        refs = relation["provenance_refs"]
        if (
            source is None
            or type(ordinal) is not int
            or ordinal < 0
            or relation["semantic_attributes"] != {}
            or refs != sorted(set(refs))
            or not refs
            or not set(refs).issubset(run_ids)
            or set(refs) != accepted_by_relation.get(relation["relation_id"], set())
        ):
            raise ValueError
        target = relation["target"]
        if relation["relation_kind"] == "LEXICAL_CONTAINS":
            if (
                relation["relation_space"] != "CHILD_EDGE"
                or source["fact_kind"] != "MODULE"
                or not isinstance(target, Mapping)
                or set(target) != {"target_kind", "fact_id"}
                or target["target_kind"] != "FACT"
                or target["fact_id"] not in facts_by_id
                or facts_by_id[target["fact_id"]]["fact_kind"] != "IMPORT_DECLARATION"
            ):
                raise ValueError
        elif relation["relation_kind"] == "IMPORT_TARGET_LITERAL":
            attributes = source["semantic_attributes"]
            if (
                relation["relation_space"] != "IMPORT_EDGE"
                or source["fact_kind"] != "IMPORT_DECLARATION"
                or ordinal != 0
                or not isinstance(attributes, Mapping)
                or not isinstance(target, Mapping)
                or set(target)
                != {
                    "target_kind",
                    "relative_level",
                    "module_parts",
                    "imported_name",
                    "resolution_status",
                    "topology_status",
                    "resolved_fact_ids",
                }
                or target["target_kind"] != "IMPORT_LITERAL"
                or target["relative_level"] != attributes["relative_level"]
                or target["module_parts"] != attributes["module_parts"]
                or target["imported_name"] != attributes["imported_name"]
                or target["resolution_status"] != "UNRESOLVED"
                or target["topology_status"] != "UNKNOWN"
                or target["resolved_fact_ids"] != []
            ):
                raise ValueError
        else:
            raise ValueError
        subject = semantic_digest(
            "veritrail.review.relation-subject/0.1",
            {
                "source_snapshot_digest": qualification.source_snapshot_digest,
                "derivation_profile_digest": qualification.derivation_profile_digest,
                "relation_space": relation["relation_space"],
                "source_fact_id": relation["source_fact_id"],
                "local_ordinal": ordinal,
            },
        )
        relation_id = semantic_digest(
            "veritrail.review.structural-relation/0.1",
            {
                "relation_subject_digest": subject,
                "relation_kind": relation["relation_kind"],
                "target": copy.deepcopy(target),
                "semantic_attributes": {},
            },
        )
        if relation["relation_subject_digest"] != subject or relation["relation_id"] != relation_id:
            raise ValueError
        if not any(
            item["relation_kind"] == relation["relation_kind"]
            and item["subject_fact_id"]
            == (
                target["fact_id"]
                if relation["relation_kind"] == "LEXICAL_CONTAINS"
                else relation["source_fact_id"]
            )
            for item in items
        ):
            raise ValueError
    for run in provider_runs:
        accepted = sorted(
            {
                relation_id
                for relation_id, refs in accepted_by_relation.items()
                if run["provider_run_id"] in refs
            }
        )
        if run["reported_relation_ids"] != accepted:
            raise ValueError


def _qualification_claim(
    qualification: OwnedRelationCompositionQualificationResult,
    provider_runs: Sequence[Mapping[str, object]],
    receipts: Sequence[Mapping[str, object]],
    relations: Sequence[Mapping[str, object]],
    conflicts: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    payload = {
        "observation_domain_digest": qualification.observation_domain_digest,
        "provider_run_terminals": [
            {
                "provider_run_id": run["provider_run_id"],
                "execution_status": run["execution_status"],
            }
            for run in provider_runs
        ],
        "observation_receipts": copy.deepcopy(list(receipts)),
        "required_source_set_terminal_closure": "COMPLETE",
        "required_observation_closure": "COMPLETE",
        "candidate_composition_status": qualification.candidate_composition_status,
        "qualification_status": "QUALIFIED",
        "merged_candidate_relation_ids": [item["relation_id"] for item in relations],
        "private_conflict_ids": [item["conflict_id"] for item in conflicts],
        "reason_codes": [],
    }
    digest = semantic_digest(
        "veritrail.review.relation-composition-qualification/0.1", payload
    )
    return {**payload, "qualification_digest": digest}


def _relation_set_document(
    qualification: OwnedRelationCompositionQualificationResult,
    normalized: Mapping[str, object],
) -> dict[str, object]:
    relations = copy.deepcopy(list(normalized["merged"]))
    conflicts = copy.deepcopy(list(normalized["conflicts"]))
    payload = {
        "source_snapshot_digest": qualification.source_snapshot_digest,
        "analysis_scope_digest": qualification.analysis_scope_digest,
        "derivation_profile_digest": qualification.derivation_profile_digest,
        "fact_set_digest": qualification.fact_set_digest,
        "relations": [
            {key: copy.deepcopy(value) for key, value in item.items() if key != "provenance_refs"}
            for item in relations
        ],
        "conflicts": [
            {key: copy.deepcopy(value) for key, value in item.items() if key != "provenance_refs"}
            for item in conflicts
        ],
    }
    return {
        "artifact_kind": "RELATION_SET",
        "schema_version": "0.1",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "source_snapshot_digest": qualification.source_snapshot_digest,
        "policy_digest": qualification.policy_digest,
        "analysis_scope_digest": qualification.analysis_scope_digest,
        "derivation_profile_digest": qualification.derivation_profile_digest,
        "fact_set_digest": qualification.fact_set_digest,
        "relations": relations,
        "conflicts": conflicts,
        "relation_set_digest": semantic_digest(
            "veritrail.review.relation-set/0.1", payload
        ),
    }


def _admission_witness(
    qualification: OwnedRelationCompositionQualificationResult,
    normalized: Mapping[str, object],
    relation_set: Mapping[str, object],
) -> dict[str, object]:
    relation_runs = normalized["relation_runs"]
    qualification_claim = copy.deepcopy(normalized["qualification_claim"])
    admission_claim = {
        "derivation_id": qualification.derivation_id,
        "source_snapshot_digest": qualification.source_snapshot_digest,
        "policy_digest": qualification.policy_digest,
        "analysis_scope_digest": qualification.analysis_scope_digest,
        "derivation_profile_digest": qualification.derivation_profile_digest,
        "fact_set_digest": qualification.fact_set_digest,
        "observation_domain_digest": qualification.observation_domain_digest,
        "qualification_digest": qualification.qualification_digest,
        "relation_provider_run_ids": [item["provider_run_id"] for item in relation_runs],
        "admitted_relation_ids": [item["relation_id"] for item in relation_set["relations"]],
        "admitted_conflict_ids": [item["conflict_id"] for item in relation_set["conflicts"]],
        "relation_set_digest": relation_set["relation_set_digest"],
    }
    admission_claim["admission_witness_digest"] = semantic_digest(
        "veritrail.review.relation-set-admission-witness/0.1", admission_claim
    )
    return {
        "witness_version": "0.1",
        "observation_domain": copy.deepcopy(normalized["domain"]),
        "qualification_claim": qualification_claim,
        "admission_claim": admission_claim,
    }


def _fact_provider_run_document(
    phase: OwnedExecutionCellPhaseResult,
) -> dict[str, object]:
    return {
        "provider_run_id": phase.provider_run_id,
        **phase.provider_descriptor.document(),
        "operands_digest": phase.operands_digest,
        "started_at": phase.provider_run_started_at,
        "finished_at": phase.provider_run_finished_at,
        "execution_status": "COMPLETED",
        "reported_fact_ids": list(phase.reported_fact_ids),
        "reported_relation_ids": [],
        "diagnostics": [],
    }


def _provider_run_rank(run: Mapping[str, object]) -> tuple[str, ...]:
    return tuple(
        str(run[key])
        for key in (
            "capability_id",
            "provider_id",
            "provider_version",
            "parser_id",
            "parser_version",
            "runtime_id",
            "runtime_version",
            "provider_run_id",
        )
    )


def _validate_admitted_state(value: OwnedRelationSetAdmissionState) -> None:
    if (
        type(value) is not OwnedRelationSetAdmissionState
        or value._construction_token is not _ADMISSION_TOKEN
    ):
        raise ValueError
    state_values = {
        field: getattr(value, field)
        for field in (
            "derivation_id",
            "source_snapshot_digest",
            "policy_digest",
            "analysis_scope_digest",
            "slice_policy_digest",
            "derivation_profile_digest",
            "fact_set_digest",
            "observation_domain_digest",
            "qualification_digest",
            "candidate_composition_status",
            "relation_set_document_bytes",
            "canonical_relation_set_artifact_bytes",
            "relation_set_digest",
            "admission_witness_bytes",
            "admission_witness_digest",
            "request_provenance_bytes",
            "provider_run_bytes",
            "started_at",
            "finished_at",
            "admitted_relation_ids",
            "admitted_conflict_ids",
        )
    }
    if value._state_seal != _private_state_seal(state_values):
        raise ValueError
    relation_set = value.relation_set_document_copy()
    witness = value.admission_witness_copy()
    if (
        canonical_json_bytes(relation_set) != value.relation_set_document_bytes
        or value.canonical_relation_set_artifact_bytes
        != value.relation_set_document_bytes + b"\n"
        or relation_set["relation_set_digest"] != value.relation_set_digest
        or [item["relation_id"] for item in relation_set["relations"]]
        != list(value.admitted_relation_ids)
        or [item["conflict_id"] for item in relation_set["conflicts"]]
        != list(value.admitted_conflict_ids)
        or canonical_json_bytes(witness) != value.admission_witness_bytes
    ):
        raise ValueError
    relation_payload = {
        "source_snapshot_digest": relation_set["source_snapshot_digest"],
        "analysis_scope_digest": relation_set["analysis_scope_digest"],
        "derivation_profile_digest": relation_set["derivation_profile_digest"],
        "fact_set_digest": relation_set["fact_set_digest"],
        "relations": [
            {
                key: copy.deepcopy(item)
                for key, item in relation.items()
                if key != "provenance_refs"
            }
            for relation in relation_set["relations"]
        ],
        "conflicts": [
            {
                key: copy.deepcopy(item)
                for key, item in conflict.items()
                if key != "provenance_refs"
            }
            for conflict in relation_set["conflicts"]
        ],
    }
    if relation_set["relation_set_digest"] != semantic_digest(
        "veritrail.review.relation-set/0.1", relation_payload
    ):
        raise ValueError
    domain = witness["observation_domain"]
    domain_payload = {
        key: copy.deepcopy(item)
        for key, item in domain.items()
        if key not in {"policy_digest", "observation_domain_digest"}
    }
    if domain["observation_domain_digest"] != semantic_digest(
        "veritrail.review.relation-observation-domain/0.1", domain_payload
    ):
        raise ValueError
    qualification_claim = witness["qualification_claim"]
    unsigned_qualification = {
        key: copy.deepcopy(item)
        for key, item in qualification_claim.items()
        if key != "qualification_digest"
    }
    if qualification_claim["qualification_digest"] != semantic_digest(
        "veritrail.review.relation-composition-qualification/0.1",
        unsigned_qualification,
    ):
        raise ValueError
    claim = witness["admission_claim"]
    unsigned = {
        key: copy.deepcopy(item)
        for key, item in claim.items()
        if key != "admission_witness_digest"
    }
    expected_witness = semantic_digest(
        "veritrail.review.relation-set-admission-witness/0.1", unsigned
    )
    if (
        claim["admission_witness_digest"] != expected_witness
        or value.admission_witness_digest != expected_witness
        or claim["derivation_id"] != value.derivation_id
        or claim["qualification_digest"] != value.qualification_digest
        or claim["relation_set_digest"] != value.relation_set_digest
        or claim["admitted_relation_ids"] != list(value.admitted_relation_ids)
        or claim["admitted_conflict_ids"] != list(value.admitted_conflict_ids)
        or claim["observation_domain_digest"] != value.observation_domain_digest
        or domain["observation_domain_digest"] != value.observation_domain_digest
        or domain["source_snapshot_digest"] != value.source_snapshot_digest
        or domain["policy_digest"] != value.policy_digest
        or domain["analysis_scope_digest"] != value.analysis_scope_digest
        or domain["derivation_profile_digest"] != value.derivation_profile_digest
        or domain["fact_set_digest"] != value.fact_set_digest
        or qualification_claim["qualification_digest"]
        != value.qualification_digest
        or qualification_claim["merged_candidate_relation_ids"]
        != list(value.admitted_relation_ids)
        or qualification_claim["private_conflict_ids"]
        != list(value.admitted_conflict_ids)
        or witness["qualification_claim"]["candidate_composition_status"]
        != value.candidate_composition_status
    ):
        raise ValueError
    runs = value.provider_runs_copy()
    if (
        len(runs) != len(value.provider_run_bytes)
        or any(canonical_json_bytes(item) != raw for item, raw in zip(runs, value.provider_run_bytes))
        or [
            item["provider_run_id"]
            for item in runs
            if item["capability_id"] == "review-relation-derivation"
        ]
        != claim["relation_provider_run_ids"]
    ):
        raise ValueError


def _private_state_seal(values: Mapping[str, object]) -> str:
    payload: dict[str, object] = {}
    for key, value in values.items():
        if isinstance(value, bytes):
            payload[key] = hashlib.sha256(value).hexdigest()
        elif isinstance(value, tuple) and all(isinstance(item, bytes) for item in value):
            payload[key] = [hashlib.sha256(item).hexdigest() for item in value]
        elif isinstance(value, tuple):
            payload[key] = list(value)
        else:
            payload[key] = value
    return semantic_digest(
        "veritrail.review.private-relation-set-admission-state/0.1", payload
    )


def _validate_evidence_projection(
    admitted: OwnedRelationSetAdmissionState,
    document: Mapping[str, object],
) -> None:
    if document["relation_admission"] != admitted.admission_witness_copy():
        raise ValueError
    runs = document["provider_runs"]
    relation_ids = sorted(
        {
            relation_id
            for run in runs
            for relation_id in run["reported_relation_ids"]
        }
    )
    if (
        document["schema_version"] != "0.2"
        or document["overall_execution_status"] != "COMPLETED"
        or document["diagnostics"] != []
        or relation_ids != list(admitted.admitted_relation_ids)
    ):
        raise ValueError
    unsigned = {
        key: copy.deepcopy(value)
        for key, value in document.items()
        if key != "derivation_evidence_digest"
    }
    if document["derivation_evidence_digest"] != semantic_digest(
        "veritrail.review.derivation-evidence/0.2", unsigned
    ):
        raise ValueError


def _owned_object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError
    return value
