from __future__ import annotations

import ast
import copy
from typing import Mapping

from veritrail_review._relation_observation_application import (
    build_provider_outcome,
)
from veritrail_review._relation_observation_provider import _candidate_relation_id
from veritrail_review.canonical import canonical_json_bytes


class RelationImportFormProviderFailed(RuntimeError):
    """The versioned private import-form Provider could not prove conformance."""


def run_relation_import_form_provider(
    request: object, *, launch_key: str
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Execute exactly the application assignment over a complete source world."""

    try:
        families = _assigned_families(launch_key)
        facts_by_id = request.facts_by_id
        source_blobs = request.source_blobs_by_path_hex
        bindings = _bind_import_facts(facts_by_id, source_blobs)
        assigned = request.document["assigned_observation_item_ids"]
        _validate_complete_assignment(
            assigned,
            request.observation_items_by_id,
            bindings,
            families,
        )
        modules = _module_by_path(facts_by_id, source_blobs)

        candidates: list[dict[str, object]] = []
        outcomes: list[dict[str, object]] = []
        for item_id in assigned:
            item = request.observation_items_by_id[item_id]
            fact = facts_by_id[item["subject_fact_id"]]
            occurrence = bindings[fact["fact_id"]]
            path_hex = occurrence["path_hex"]
            if item["relation_kind"] == "LEXICAL_CONTAINS":
                candidate = {
                    "relation_space": "CHILD_EDGE",
                    "relation_kind": "LEXICAL_CONTAINS",
                    "source_fact_id": modules[path_hex]["fact_id"],
                    "local_ordinal": occurrence["lexical_child_ordinal"],
                    "target": {
                        "target_kind": "FACT",
                        "fact_id": fact["fact_id"],
                    },
                    "semantic_attributes": {},
                }
            elif item["relation_kind"] == "IMPORT_TARGET_LITERAL":
                attributes = fact["semantic_attributes"]
                candidate = {
                    "relation_space": "IMPORT_EDGE",
                    "relation_kind": "IMPORT_TARGET_LITERAL",
                    "source_fact_id": fact["fact_id"],
                    "local_ordinal": 0,
                    "target": {
                        "target_kind": "IMPORT_LITERAL",
                        "relative_level": attributes["relative_level"],
                        "module_parts": copy.deepcopy(attributes["module_parts"]),
                        "imported_name": attributes["imported_name"],
                        "resolution_status": "UNRESOLVED",
                        "topology_status": "UNKNOWN",
                        "resolved_fact_ids": [],
                    },
                    "semantic_attributes": {},
                }
            else:  # pragma: no cover - complete assignment validation owns this
                raise RelationImportFormProviderFailed
            relation_id = _candidate_relation_id(request, candidate)
            candidates.append(candidate)
            outcomes.append(
                build_provider_outcome(
                    provider_run_id_value=request.provider_run_id,
                    observation_item_id=item_id,
                    disposition="CANDIDATE_REPORTED",
                    reported_relation_ids=[relation_id],
                )
            )
        outcomes.sort(
            key=lambda item: (
                item["observation_item_id"],
                item["observation_outcome_id"],
            )
        )
        if len(outcomes) != len(assigned):
            raise RelationImportFormProviderFailed
        return candidates, outcomes
    except RelationImportFormProviderFailed:
        raise
    except Exception as exc:
        raise RelationImportFormProviderFailed from exc


def import_alias_occurrences(raw: bytes) -> tuple[dict[str, object], ...]:
    """Project the frozen CPython 3.10 import-alias occurrence universe."""

    try:
        text = raw.decode("utf-8-sig", errors="strict")
        tree = ast.parse(text, mode="exec", feature_version=(3, 10))
    except (SyntaxError, UnicodeError, ValueError) as exc:
        raise RelationImportFormProviderFailed from exc

    top_level = {id(node): ordinal for ordinal, node in enumerate(tree.body)}
    legacy: list[dict[str, object]] = []
    extension: list[dict[str, object]] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        start, end = _node_byte_span(raw, node)
        for alias_ordinal, alias in enumerate(node.names):
            occurrence = {
                "start_byte": start,
                "end_byte": end,
                "alias_ordinal": alias_ordinal,
                "attributes": _import_attributes(node, alias),
            }
            if (
                isinstance(node, ast.Import)
                and len(node.names) == 1
                and id(node) in top_level
                and alias_ordinal == 0
            ):
                occurrence["lexical_child_ordinal"] = top_level[id(node)]
                legacy.append(occurrence)
            else:
                extension.append(occurrence)

    extension.sort(key=_extension_rank)
    ranks = [_extension_rank(item) for item in extension]
    if len(ranks) != len(set(ranks)):
        raise RelationImportFormProviderFailed
    for offset, occurrence in enumerate(extension):
        occurrence["lexical_child_ordinal"] = len(tree.body) + offset

    result = sorted(
        (*legacy, *extension),
        key=lambda item: (
            item["start_byte"],
            item["end_byte"],
            item["alias_ordinal"],
            canonical_json_bytes(item["attributes"]),
        ),
    )
    ordinals = [item["lexical_child_ordinal"] for item in result]
    if len(ordinals) != len(set(ordinals)):
        raise RelationImportFormProviderFailed
    return tuple(copy.deepcopy(item) for item in result)


def _bind_import_facts(
    facts_by_id: Mapping[str, Mapping[str, object]],
    source_blobs: Mapping[str, bytes],
) -> dict[str, dict[str, object]]:
    expected: dict[tuple[object, ...], dict[str, object]] = {}
    for path_hex in sorted(source_blobs, key=bytes.fromhex):
        for occurrence in import_alias_occurrences(source_blobs[path_hex]):
            key = _occurrence_key(path_hex, occurrence)
            if key in expected:
                raise RelationImportFormProviderFailed
            expected[key] = occurrence

    actual: dict[tuple[object, ...], Mapping[str, object]] = {}
    for fact in facts_by_id.values():
        if fact["fact_kind"] != "IMPORT_DECLARATION":
            continue
        key = _fact_key(fact)
        if key in actual:
            raise RelationImportFormProviderFailed
        actual[key] = fact
    if set(expected) != set(actual):
        raise RelationImportFormProviderFailed
    return {
        actual[key]["fact_id"]: {
            **copy.deepcopy(expected[key]),
            "path_hex": key[0],
        }
        for key in sorted(expected)
    }


def _module_by_path(
    facts_by_id: Mapping[str, Mapping[str, object]],
    source_blobs: Mapping[str, bytes],
) -> dict[str, Mapping[str, object]]:
    result: dict[str, Mapping[str, object]] = {}
    for fact in facts_by_id.values():
        if fact["fact_kind"] != "MODULE":
            continue
        path_hex = fact["source_anchor"]["git_path"]["git_path_hex"]
        if path_hex in result:
            raise RelationImportFormProviderFailed
        result[path_hex] = fact
    if set(result) != set(source_blobs):
        raise RelationImportFormProviderFailed
    return result


def _validate_complete_assignment(
    assigned: object,
    items_by_id: Mapping[str, Mapping[str, object]],
    import_bindings: Mapping[str, Mapping[str, object]],
    families: tuple[str, ...],
) -> None:
    if not isinstance(assigned, list) or assigned != sorted(set(assigned)):
        raise RelationImportFormProviderFailed
    expected = {
        (fact_id, family) for fact_id in import_bindings for family in families
    }
    actual: set[tuple[object, object]] = set()
    for item_id in assigned:
        item = items_by_id.get(item_id)
        if item is None:
            raise RelationImportFormProviderFailed
        pair = (item["subject_fact_id"], item["relation_kind"])
        if pair in actual:
            raise RelationImportFormProviderFailed
        actual.add(pair)
    if actual != expected:
        raise RelationImportFormProviderFailed


def _assigned_families(launch_key: str) -> tuple[str, ...]:
    if launch_key == "import-form-observation-a":
        return ("LEXICAL_CONTAINS",)
    if launch_key == "import-form-observation-b":
        return ("LEXICAL_CONTAINS", "IMPORT_TARGET_LITERAL")
    raise RelationImportFormProviderFailed


def _import_attributes(
    node: ast.Import | ast.ImportFrom, alias: ast.alias
) -> dict[str, object]:
    if isinstance(node, ast.Import):
        return {
            "import_form": "IMPORT",
            "relative_level": 0,
            "module_parts": alias.name.split("."),
            "imported_name": None,
            "alias_name": alias.asname,
        }
    return {
        "import_form": "FROM_IMPORT",
        "relative_level": node.level,
        "module_parts": [] if node.module is None else node.module.split("."),
        "imported_name": alias.name,
        "alias_name": alias.asname,
    }


def _occurrence_key(
    path_hex: str, occurrence: Mapping[str, object]
) -> tuple[object, ...]:
    return (
        path_hex,
        occurrence["start_byte"],
        occurrence["end_byte"],
        occurrence["alias_ordinal"],
        canonical_json_bytes(occurrence["attributes"]),
    )


def _fact_key(fact: Mapping[str, object]) -> tuple[object, ...]:
    anchor = fact["source_anchor"]
    return (
        anchor["git_path"]["git_path_hex"],
        anchor["start_byte"],
        anchor["end_byte"],
        fact["local_ordinal"],
        canonical_json_bytes(fact["semantic_attributes"]),
    )


def _extension_rank(item: Mapping[str, object]) -> tuple[object, ...]:
    attributes = item["attributes"]
    return (
        item["start_byte"],
        item["end_byte"],
        attributes["import_form"],
        item["alias_ordinal"],
        canonical_json_bytes(attributes),
    )


def _node_byte_span(raw: bytes, node: ast.AST) -> tuple[int, int]:
    coordinates = (
        getattr(node, "lineno", None),
        getattr(node, "col_offset", None),
        getattr(node, "end_lineno", None),
        getattr(node, "end_col_offset", None),
    )
    if not all(type(value) is int and value >= 0 for value in coordinates):
        raise RelationImportFormProviderFailed
    lineno, col, end_lineno, end_col = coordinates
    prefix = 3 if raw.startswith(b"\xef\xbb\xbf") else 0
    lines = raw[prefix:].splitlines(keepends=True)
    if lineno < 1 or end_lineno < lineno or end_lineno > len(lines):
        raise RelationImportFormProviderFailed
    start = prefix + sum(len(line) for line in lines[: lineno - 1]) + col
    end = prefix + sum(len(line) for line in lines[: end_lineno - 1]) + end_col
    if start < 0 or end < start or end > len(raw):
        raise RelationImportFormProviderFailed
    return start, end
