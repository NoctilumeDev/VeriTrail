from __future__ import annotations

import copy
from typing import Mapping, Sequence

from veritrail_review._execution_cell_binding import ProviderBinding, ProviderDescriptor
from veritrail_review._relation_observation_binding import (
    closed_test_relation_observation_bindings,
    relation_observation_descriptor_rank,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


OBSERVATION_PROFILE_ID = "closed-python-import-observation"
OBSERVATION_PROFILE_VERSION = "0.1-test"
CAPABILITY_ID = "review-relation-derivation"

_FAMILY_RANK = {"LEXICAL_CONTAINS": 0, "IMPORT_TARGET_LITERAL": 1}
_ROLE_RANK = {"SOURCE_FACT": 0, "TARGET_FACT": 1}


class RelationObservationDomainError(ValueError):
    pass


def observation_profile_document() -> dict[str, object]:
    bindings = closed_test_relation_observation_bindings()
    family_rules = [
        {
            "relation_kind": "LEXICAL_CONTAINS",
            "subject_role": "TARGET_FACT",
            "subject_fact_kinds": ["IMPORT_DECLARATION"],
            "candidate_cardinality": "EXACTLY_ONE",
            "negative_outcome_allowed": False,
        },
        {
            "relation_kind": "IMPORT_TARGET_LITERAL",
            "subject_role": "SOURCE_FACT",
            "subject_fact_kinds": ["IMPORT_DECLARATION"],
            "candidate_cardinality": "EXACTLY_ONE",
            "negative_outcome_allowed": False,
        },
    ]
    responsibilities = [
        {
            "provider_descriptor": bindings[0].descriptor.document(),
            "required": True,
            "assigned_relation_families": ["LEXICAL_CONTAINS"],
        },
        {
            "provider_descriptor": bindings[1].descriptor.document(),
            "required": True,
            "assigned_relation_families": [
                "LEXICAL_CONTAINS",
                "IMPORT_TARGET_LITERAL",
            ],
        },
    ]
    responsibilities.sort(
        key=lambda item: relation_observation_descriptor_rank(
            ProviderDescriptor(**item["provider_descriptor"])
        )
    )
    return {
        "observation_profile_id": OBSERVATION_PROFILE_ID,
        "observation_profile_version": OBSERVATION_PROFILE_VERSION,
        "capability_id": CAPABILITY_ID,
        "required": True,
        "composition_mode": "CUMULATIVE",
        "family_rules": family_rules,
        "provider_responsibility_rules": responsibilities,
    }


def build_declared_relation_observation_domain(
    inputs: DerivationInputSet,
    fact_set_document: Mapping[str, object],
    relation_bindings: Sequence[ProviderBinding],
) -> dict[str, object]:
    try:
        if not isinstance(inputs, DerivationInputSet):
            raise ValueError
        profile = inputs.derivation_profile_document_copy()
        policy = inputs.review_policy_document_copy()
        if (
            profile["profile_id"] != "veritrail-python-source-3.10"
            or profile["profile_version"] != "0.1"
            or profile["relation_kinds"]
            != ["LEXICAL_CONTAINS", "IMPORT_TARGET_LITERAL"]
        ):
            raise ValueError
        requirements = [
            item
            for item in policy["provider_requirements"]
            if item["capability_id"] == CAPABILITY_ID
        ]
        if requirements != [
            {
                "capability_id": CAPABILITY_ID,
                "required": True,
                "composition_mode": "CUMULATIVE",
            }
        ]:
            raise ValueError
        expected_bindings = closed_test_relation_observation_bindings()
        normalized = tuple(
            sorted(
                relation_bindings,
                key=lambda item: relation_observation_descriptor_rank(
                    item.descriptor
                ),
            )
        )
        if normalized != expected_bindings:
            raise ValueError
        facts = fact_set_document["facts"]
        conflicts = fact_set_document["conflicts"]
        if not isinstance(facts, list) or conflicts != []:
            raise ValueError
        if fact_set_document["fact_set_digest"] != _fact_set_digest(
            fact_set_document
        ):
            raise ValueError
        modules = [fact for fact in facts if fact.get("fact_kind") == "MODULE"]
        imports = [
            fact for fact in facts if fact.get("fact_kind") == "IMPORT_DECLARATION"
        ]
        if len(modules) != 1 or len(modules) + len(imports) != len(facts):
            raise ValueError
        module_path = modules[0]["source_anchor"]["git_path"]["git_path_hex"]
        snapshot = inputs.source_snapshot_document_copy()
        inventory_matches = [
            entry
            for entry in snapshot["inventory"]
            if entry["git_path"]["git_path_hex"] == module_path
        ]
        module_anchor = modules[0]["source_anchor"]
        if (
            len(inventory_matches) != 1
            or inventory_matches[0]["entry_kind"]
            not in set(profile["supported_entry_kinds"])
            or inventory_matches[0]["git_object"]["object_type"] != "BLOB"
            or modules[0]["local_ordinal"] != 0
            or module_anchor["start_byte"] != 0
            or module_anchor["end_byte"]
            != inventory_matches[0]["content"]["size_bytes"]
        ):
            raise ValueError
        for fact in imports:
            attributes = fact["semantic_attributes"]
            if (
                fact["source_anchor"]["git_path"]["git_path_hex"] != module_path
                or fact["local_ordinal"] != 0
                or set(attributes)
                != {
                    "import_form",
                    "relative_level",
                    "module_parts",
                    "imported_name",
                    "alias_name",
                }
                or attributes["import_form"] != "IMPORT"
                or attributes["relative_level"] != 0
                or not isinstance(attributes["module_parts"], list)
                or not attributes["module_parts"]
                or attributes["imported_name"] is not None
            ):
                raise ValueError

        items: list[dict[str, object]] = []
        for fact in imports:
            for relation_kind, subject_role in (
                ("LEXICAL_CONTAINS", "TARGET_FACT"),
                ("IMPORT_TARGET_LITERAL", "SOURCE_FACT"),
            ):
                payload = {
                    "source_snapshot_digest": inputs.source_snapshot_digest,
                    "derivation_profile_digest": inputs.derivation_profile_digest,
                    "fact_set_digest": fact_set_document["fact_set_digest"],
                    "relation_kind": relation_kind,
                    "subject_role": subject_role,
                    "subject_fact_id": fact["fact_id"],
                }
                items.append(
                    {
                        "observation_item_id": semantic_digest(
                            "veritrail.review.relation-observation-item/0.1",
                            payload,
                        ),
                        **payload,
                    }
                )
        items.sort(key=_item_rank)
        if len({item["observation_item_id"] for item in items}) != len(items):
            raise ValueError

        profile_document = observation_profile_document()
        profile_payload = {
            **profile_document,
            "derivation_profile_digest": inputs.derivation_profile_digest,
        }
        observation_profile_digest = semantic_digest(
            "veritrail.review.relation-observation-profile/0.1",
            profile_payload,
        )
        by_kind = {
            kind: [
                item["observation_item_id"]
                for item in items
                if item["relation_kind"] == kind
            ]
            for kind in _FAMILY_RANK
        }
        responsibilities: list[dict[str, object]] = []
        for rule in profile_document["provider_responsibility_rules"]:
            assigned = sorted(
                {
                    item_id
                    for kind in rule["assigned_relation_families"]
                    for item_id in by_kind[kind]
                }
            )
            responsibilities.append(
                {
                    "provider_descriptor": copy.deepcopy(
                        rule["provider_descriptor"]
                    ),
                    "required": True,
                    "assigned_observation_item_ids": assigned,
                }
            )
        responsibilities.sort(
            key=lambda item: relation_observation_descriptor_rank(
                ProviderDescriptor(**item["provider_descriptor"])
            )
        )
        projection = {
            "source_snapshot_digest": inputs.source_snapshot_digest,
            "analysis_scope_digest": inputs.analysis_scope_digest,
            "derivation_profile_digest": inputs.derivation_profile_digest,
            "fact_set_digest": fact_set_document["fact_set_digest"],
            "observation_profile_id": OBSERVATION_PROFILE_ID,
            "observation_profile_version": OBSERVATION_PROFILE_VERSION,
            "observation_profile_digest": observation_profile_digest,
            "capability_id": CAPABILITY_ID,
            "required": True,
            "composition_mode": "CUMULATIVE",
            "observation_items": items,
            "provider_responsibilities": responsibilities,
        }
        digest = semantic_digest(
            "veritrail.review.relation-observation-domain/0.1", projection
        )
        return {
            **copy.deepcopy(projection),
            "policy_digest": inputs.policy_digest,
            "observation_domain_digest": digest,
        }
    except Exception as exc:
        if isinstance(exc, RelationObservationDomainError):
            raise
        raise RelationObservationDomainError(
            "closed Relation observation domain is nonconformant"
        ) from exc


def validate_declared_relation_observation_domain(
    document: Mapping[str, object],
    *,
    inputs: DerivationInputSet,
    fact_set_document: Mapping[str, object],
    relation_bindings: Sequence[ProviderBinding],
) -> dict[str, object]:
    expected = build_declared_relation_observation_domain(
        inputs, fact_set_document, relation_bindings
    )
    if document != expected or canonical_json_bytes(document) != canonical_json_bytes(
        expected
    ):
        raise RelationObservationDomainError(
            "Relation observation domain identity mismatch"
        )
    return copy.deepcopy(expected)


def responsibility_for_descriptor(
    domain: Mapping[str, object], descriptor: ProviderDescriptor
) -> dict[str, object]:
    matches = [
        item
        for item in domain["provider_responsibilities"]
        if item["provider_descriptor"] == descriptor.document()
    ]
    if len(matches) != 1:
        raise RelationObservationDomainError("missing Provider responsibility")
    return copy.deepcopy(matches[0])


def family_rule_for_item(
    item: Mapping[str, object], *, derivation_profile_digest: str
) -> dict[str, object]:
    profile = observation_profile_document()
    rules = [
        rule
        for rule in profile["family_rules"]
        if rule["relation_kind"] == item["relation_kind"]
        and rule["subject_role"] == item["subject_role"]
    ]
    if len(rules) != 1 or item["derivation_profile_digest"] != derivation_profile_digest:
        raise RelationObservationDomainError("invalid observation family")
    return copy.deepcopy(rules[0])


def _item_rank(item: Mapping[str, object]) -> tuple[object, ...]:
    return (
        _FAMILY_RANK[str(item["relation_kind"])],
        _ROLE_RANK[str(item["subject_role"])],
        str(item["subject_fact_id"]),
    )


def _fact_set_digest(fact_set_document: Mapping[str, object]) -> str:
    facts = [
        {key: copy.deepcopy(value) for key, value in fact.items() if key != "provenance_refs"}
        for fact in fact_set_document["facts"]
    ]
    conflicts = [
        {key: copy.deepcopy(value) for key, value in conflict.items() if key != "provenance_refs"}
        for conflict in fact_set_document["conflicts"]
    ]
    return semantic_digest(
        "veritrail.review.fact-set/0.1",
        {
            "source_snapshot_digest": fact_set_document["source_snapshot_digest"],
            "analysis_scope_digest": fact_set_document["analysis_scope_digest"],
            "derivation_profile_digest": fact_set_document[
                "derivation_profile_digest"
            ],
            "facts": facts,
            "conflicts": conflicts,
        },
    )
