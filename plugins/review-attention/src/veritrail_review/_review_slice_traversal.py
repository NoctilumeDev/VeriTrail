from __future__ import annotations

import copy
import heapq
from typing import Mapping

from veritrail_review._review_slice_traversal_assignment_values import (
    OwnedReviewSliceTraversalBoundary,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


def _derive_normal_review_slice_candidate(
    boundary: OwnedReviewSliceTraversalBoundary,
) -> dict[str, object]:
    request = boundary.traversal_request_copy()
    spec = request.get("slice_spec")
    fact_set = request.get("fact_set")
    relation_set = request.get("relation_set")
    if (
        not isinstance(spec, Mapping)
        or not isinstance(fact_set, Mapping)
        or not isinstance(relation_set, Mapping)
    ):
        raise ValueError
    facts_raw = fact_set.get("facts")
    relations_raw = relation_set.get("relations")
    if not isinstance(facts_raw, list) or not isinstance(relations_raw, list):
        raise ValueError

    facts: dict[str, Mapping[str, object]] = {}
    for fact in facts_raw:
        _traversal_checkpoint(boundary)
        if not isinstance(fact, Mapping) or not isinstance(
            fact.get("fact_id"), str
        ):
            raise ValueError
        fact_id = fact["fact_id"]
        if fact_id in facts:
            raise ValueError
        _fact_path_identity(fact)
        facts[fact_id] = fact

    relations: list[Mapping[str, object]] = []
    relation_ids: set[str] = set()
    for relation in relations_raw:
        _traversal_checkpoint(boundary)
        if not isinstance(relation, Mapping) or not isinstance(
            relation.get("relation_id"), str
        ):
            raise ValueError
        relation_id = relation["relation_id"]
        if relation_id in relation_ids:
            raise ValueError
        _relation_endpoint(relation, facts)
        relation_ids.add(relation_id)
        relations.append(relation)

    anchor = spec.get("anchor_fact_id")
    if not isinstance(anchor, str) or anchor not in facts:
        raise ValueError
    limits = _slice_limits(spec)
    allowed, relation_kind_rank = _allowed_relation_directions(spec)

    included_facts = {anchor}
    included_relations: set[str] = set()
    included_files = {_fact_path_identity(facts[anchor])}
    queue: list[tuple[int, str]] = [(0, anchor)]
    expanded_facts: set[str] = set()
    frontier: list[dict[str, object]] = []
    frontier_keys: set[tuple[str, str, str]] = set()

    while queue:
        _traversal_checkpoint(boundary)
        depth, from_fact_id = heapq.heappop(queue)
        if from_fact_id in expanded_facts:
            continue
        expanded_facts.add(from_fact_id)
        candidates = _relation_candidates(
            from_fact_id=from_fact_id,
            relations=relations,
            allowed=allowed,
            relation_kind_rank=relation_kind_rank,
        )
        for relation, direction, candidate_fact_id in candidates:
            _traversal_checkpoint(boundary)
            relation_id = relation["relation_id"]
            if not isinstance(relation_id, str):
                raise ValueError
            if relation_id in included_relations:
                continue
            candidate_depth = depth + 1
            new_fact = (
                candidate_fact_id is not None
                and candidate_fact_id not in included_facts
            )
            literal_target = candidate_fact_id is None
            candidate_file: bytes | None = None
            if new_fact:
                candidate_file = _fact_path_identity(facts[candidate_fact_id])
            reasons: list[str] = []
            if (
                (new_fact or literal_target)
                and candidate_depth > limits["max_depth"]
            ):
                reasons.append("DEPTH_LIMIT")
            if new_fact and len(included_facts) + 1 > limits["max_symbols"]:
                reasons.append("SYMBOL_LIMIT")
            if (
                new_fact
                and candidate_file not in included_files
                and len(included_files) + 1 > limits["max_files"]
            ):
                reasons.append("FILE_LIMIT")
            if len(included_relations) + 1 > limits["max_relations"]:
                reasons.append("RELATION_LIMIT")
            if reasons:
                key = (from_fact_id, relation_id, direction)
                if key not in frontier_keys:
                    frontier_keys.add(key)
                    frontier.append(
                        {
                            "from_fact_id": from_fact_id,
                            "relation_id": relation_id,
                            "direction": direction,
                            "candidate_fact_id": candidate_fact_id,
                            "candidate_depth": candidate_depth,
                            "reason_codes": reasons,
                        }
                    )
                continue
            included_relations.add(relation_id)
            if new_fact:
                included_facts.add(candidate_fact_id)
                if candidate_file is None:
                    raise ValueError
                included_files.add(candidate_file)
                heapq.heappush(queue, (candidate_depth, candidate_fact_id))

    fact_ids = sorted(included_facts)
    accepted_relation_ids = sorted(included_relations)
    slice_id = semantic_digest(
        "veritrail.review.review-slice/0.1",
        {
            "slice_spec_digest": boundary.slice_spec_digest,
            "included_fact_ids": fact_ids,
            "included_relation_ids": accepted_relation_ids,
            "frontier": copy.deepcopy(frontier),
        },
    )
    return {
        "slice_id": slice_id,
        "slice_spec": copy.deepcopy(dict(spec)),
        "included_fact_ids": fact_ids,
        "included_relation_ids": accepted_relation_ids,
        "frontier": frontier,
        "coverage_status": "PARTIAL" if frontier else "COMPLETE",
    }


def _allowed_relation_directions(
    spec: Mapping[str, object],
) -> tuple[set[tuple[str, str]], dict[str, int]]:
    raw = spec.get("allowed_relations")
    if not isinstance(raw, list):
        raise ValueError
    allowed: set[tuple[str, str]] = set()
    relation_kind_rank: dict[str, int] = {}
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError
        kind = item.get("relation_kind")
        direction = item.get("direction")
        if (
            kind not in {"LEXICAL_CONTAINS", "IMPORT_TARGET_LITERAL"}
            or direction not in {"OUTBOUND", "INBOUND", "BOTH"}
        ):
            raise ValueError
        relation_kind_rank.setdefault(kind, len(relation_kind_rank))
        directions = (
            ("OUTBOUND", "INBOUND") if direction == "BOTH" else (direction,)
        )
        for expanded in directions:
            allowed.add((kind, expanded))
    return allowed, relation_kind_rank


def _relation_candidates(
    *,
    from_fact_id: str,
    relations: list[Mapping[str, object]],
    allowed: set[tuple[str, str]],
    relation_kind_rank: Mapping[str, int],
) -> list[tuple[Mapping[str, object], str, str | None]]:
    candidates: list[tuple[Mapping[str, object], str, str | None]] = []
    seen: set[tuple[str, str]] = set()
    for relation in relations:
        kind = relation["relation_kind"]
        relation_id = relation["relation_id"]
        source_fact_id = relation["source_fact_id"]
        target = relation["target"]
        if (
            not isinstance(kind, str)
            or not isinstance(relation_id, str)
            or not isinstance(source_fact_id, str)
            or not isinstance(target, Mapping)
        ):
            raise ValueError
        if kind not in relation_kind_rank:
            continue
        if (
            source_fact_id == from_fact_id
            and (kind, "OUTBOUND") in allowed
            and (relation_id, "OUTBOUND") not in seen
        ):
            seen.add((relation_id, "OUTBOUND"))
            target_fact_id = (
                target.get("fact_id") if target.get("target_kind") == "FACT" else None
            )
            if target_fact_id is not None and not isinstance(target_fact_id, str):
                raise ValueError
            candidates.append((relation, "OUTBOUND", target_fact_id))
        if (
            target.get("target_kind") == "FACT"
            and target.get("fact_id") == from_fact_id
            and (kind, "INBOUND") in allowed
            and (relation_id, "INBOUND") not in seen
        ):
            seen.add((relation_id, "INBOUND"))
            candidates.append((relation, "INBOUND", source_fact_id))
    direction_rank = {"OUTBOUND": 0, "INBOUND": 1}
    candidates.sort(
        key=lambda item: (
            relation_kind_rank[item[0]["relation_kind"]],
            direction_rank[item[1]],
            item[0]["relation_id"],
        )
    )
    return candidates


def _relation_endpoint(
    relation: Mapping[str, object],
    facts: Mapping[str, Mapping[str, object]],
) -> None:
    source = relation.get("source_fact_id")
    kind = relation.get("relation_kind")
    target = relation.get("target")
    if source not in facts or not isinstance(target, Mapping):
        raise ValueError
    if kind == "LEXICAL_CONTAINS":
        if target.get("target_kind") != "FACT" or target.get("fact_id") not in facts:
            raise ValueError
        return
    if (
        kind == "IMPORT_TARGET_LITERAL"
        and target.get("target_kind") == "IMPORT_LITERAL"
    ):
        return
    raise ValueError


def _slice_limits(spec: Mapping[str, object]) -> dict[str, int]:
    limits: dict[str, int] = {}
    for name, minimum in (
        ("max_depth", 0),
        ("max_symbols", 1),
        ("max_files", 1),
        ("max_relations", 0),
    ):
        value = spec.get(name)
        if type(value) is not int or value < minimum:
            raise ValueError
        limits[name] = value
    return limits


def _fact_path_identity(fact: Mapping[str, object]) -> bytes:
    anchor = fact.get("source_anchor")
    if not isinstance(anchor, Mapping):
        raise ValueError
    path = anchor.get("git_path")
    if not isinstance(path, Mapping):
        raise ValueError
    return canonical_json_bytes(dict(path))


def _traversal_checkpoint(boundary: OwnedReviewSliceTraversalBoundary) -> None:
    if not boundary.continuation_permitted():
        raise ValueError
