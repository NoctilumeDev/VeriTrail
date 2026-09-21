from __future__ import annotations

import ast
import copy
import time

from veritrail_review._relation_observation_application import (
    ValidatedRelationObservationRequest,
    build_provider_outcome,
)
from veritrail_review.canonical import semantic_digest


class ClosedRelationObservationProviderUnavailable(RuntimeError):
    pass


class ClosedRelationObservationProviderFailed(RuntimeError):
    pass


def run_closed_relation_observation_provider(
    request: ValidatedRelationObservationRequest, *, launch_key: str
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    if launch_key.endswith("-unavailable"):
        raise ClosedRelationObservationProviderUnavailable
    if launch_key.endswith("-failed"):
        raise ClosedRelationObservationProviderFailed
    if launch_key == "observation-b-slow":
        time.sleep(60)
        return [], []
    if launch_key == "observation-b-memory":
        retained: list[bytearray] = []
        while True:
            retained.append(bytearray(8 * 1024 * 1024))

    operation_paths = {
        fact["source_anchor"]["git_path"]["git_path_hex"]
        for fact in request.facts_by_id.values()
        if fact["fact_kind"] in {"MODULE", "IMPORT_DECLARATION"}
    }
    parsed_by_path: dict[str, ast.Module] = {}
    for path_hex in sorted(operation_paths, key=bytes.fromhex):
        parsed_by_path[path_hex] = _closed_deterministic_test_parser(
            request.source_blobs_by_path_hex[path_hex]
        )

    if launch_key.endswith("-empty"):
        return [], []

    assigned = request.document["assigned_observation_item_ids"]
    candidates: list[dict[str, object]] = []
    outcomes: list[dict[str, object]] = []
    for item_id in assigned:
        item = request.observation_items_by_id[item_id]
        subject = request.facts_by_id[item["subject_fact_id"]]
        path_hex = subject["source_anchor"]["git_path"]["git_path_hex"]
        tree = parsed_by_path[path_hex]
        raw = request.source_blobs_by_path_hex[path_hex]
        node, body_ordinal = _matching_import_node(raw, tree, subject)
        if item["relation_kind"] == "LEXICAL_CONTAINS":
            modules = [
                fact
                for fact in request.facts_by_id.values()
                if fact["fact_kind"] == "MODULE"
                and fact["source_anchor"]["git_path"]["git_path_hex"]
                == path_hex
            ]
            if len(modules) != 1:
                raise ClosedRelationObservationProviderFailed
            ordinal = body_ordinal
            if launch_key == "observation-b-conflict":
                ordinal += 1
            candidate = {
                "relation_space": "CHILD_EDGE",
                "relation_kind": "LEXICAL_CONTAINS",
                "source_fact_id": modules[0]["fact_id"],
                "local_ordinal": ordinal,
                "target": {
                    "target_kind": "FACT",
                    "fact_id": subject["fact_id"],
                },
                "semantic_attributes": {},
            }
        elif item["relation_kind"] == "IMPORT_TARGET_LITERAL":
            alias = node.names[0]
            attributes = subject["semantic_attributes"]
            if (
                alias.name.split(".") != attributes["module_parts"]
                or alias.asname != attributes["alias_name"]
            ):
                raise ClosedRelationObservationProviderFailed
            candidate = {
                "relation_space": "IMPORT_EDGE",
                "relation_kind": "IMPORT_TARGET_LITERAL",
                "source_fact_id": subject["fact_id"],
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
        else:
            raise ClosedRelationObservationProviderFailed
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
    return candidates, outcomes


def _candidate_relation_id(
    request: ValidatedRelationObservationRequest,
    candidate: dict[str, object],
) -> str:
    subject = semantic_digest(
        "veritrail.review.relation-subject/0.1",
        {
            "source_snapshot_digest": request.document[
                "source_snapshot_digest"
            ],
            "derivation_profile_digest": request.document[
                "derivation_profile_digest"
            ],
            "relation_space": candidate["relation_space"],
            "source_fact_id": candidate["source_fact_id"],
            "local_ordinal": candidate["local_ordinal"],
        },
    )
    return semantic_digest(
        "veritrail.review.structural-relation/0.1",
        {
            "relation_subject_digest": subject,
            "relation_kind": candidate["relation_kind"],
            "target": candidate["target"],
            "semantic_attributes": {},
        },
    )


def _matching_import_node(
    raw: bytes, tree: ast.Module, fact: dict[str, object]
) -> tuple[ast.Import, int]:
    matches: list[tuple[ast.Import, int]] = []
    span = (
        fact["source_anchor"]["start_byte"],
        fact["source_anchor"]["end_byte"],
    )
    for body_ordinal, node in enumerate(tree.body):
        if (
            isinstance(node, ast.Import)
            and len(node.names) == 1
            and _node_byte_span(raw, node) == span
        ):
            matches.append((node, body_ordinal))
    if len(matches) != 1:
        raise ClosedRelationObservationProviderFailed
    return matches[0]


def _closed_deterministic_test_parser(raw: bytes) -> ast.Module:
    try:
        text = raw.decode("utf-8-sig", errors="strict")
        return ast.parse(text, mode="exec", feature_version=(3, 10))
    except (SyntaxError, UnicodeError, ValueError) as exc:
        raise ClosedRelationObservationProviderFailed from exc


def _node_byte_span(raw: bytes, node: ast.AST) -> tuple[int, int]:
    coordinates = (
        getattr(node, "lineno", None),
        getattr(node, "col_offset", None),
        getattr(node, "end_lineno", None),
        getattr(node, "end_col_offset", None),
    )
    if not all(type(value) is int and value >= 0 for value in coordinates):
        raise ClosedRelationObservationProviderFailed
    lineno, col, end_lineno, end_col = coordinates
    lines = raw.splitlines(keepends=True)
    if lineno < 1 or end_lineno < lineno or end_lineno > len(lines):
        raise ClosedRelationObservationProviderFailed
    start = sum(len(line) for line in lines[: lineno - 1]) + col
    end = sum(len(line) for line in lines[: end_lineno - 1]) + end_col
    if start < 0 or end < start or end > len(raw):
        raise ClosedRelationObservationProviderFailed
    return start, end
