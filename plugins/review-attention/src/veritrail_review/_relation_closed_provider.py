from __future__ import annotations

import ast
import time

from veritrail_review._relation_execution_cell_application import (
    ValidatedRelationRequest,
)


class ClosedRelationProviderUnavailable(RuntimeError):
    pass


class ClosedRelationProviderFailed(RuntimeError):
    pass


def run_closed_relation_provider(
    request: ValidatedRelationRequest, *, launch_key: str
) -> list[dict[str, object]]:
    if launch_key == "relation-unavailable":
        raise ClosedRelationProviderUnavailable
    if launch_key == "relation-failed":
        raise ClosedRelationProviderFailed
    if launch_key == "relation-slow":
        time.sleep(60)
        return []
    if launch_key == "relation-memory":
        retained: list[bytearray] = []
        while True:
            retained.append(bytearray(8 * 1024 * 1024))
    candidates = _closed_fixture_relation_candidates(request)
    if launch_key == "relation-mutates-owned-input":
        request.document["fact_set"]["facts"].clear()
        request.facts_by_id.clear()
        request.source_blobs_by_path_hex.clear()
        return candidates
    if launch_key == "relation-bad-candidate":
        if candidates:
            candidates[0]["source_fact_id"] = "0" * 64
        else:
            candidates.append(
                {
                    "relation_space": "CHILD_EDGE",
                    "relation_kind": "LEXICAL_CONTAINS",
                    "source_fact_id": "0" * 64,
                    "local_ordinal": 0,
                    "target": {"target_kind": "FACT", "fact_id": "1" * 64},
                    "semantic_attributes": {},
                }
            )
    return candidates


def _closed_fixture_relation_candidates(
    request: ValidatedRelationRequest,
) -> list[dict[str, object]]:
    facts_by_path: dict[str, list[dict[str, object]]] = {}
    for fact in request.facts_by_id.values():
        path_hex = fact["source_anchor"]["git_path"]["git_path_hex"]
        facts_by_path.setdefault(path_hex, []).append(fact)
    candidates: list[dict[str, object]] = []
    for path_hex in sorted(facts_by_path, key=bytes.fromhex):
        raw = request.source_blobs_by_path_hex[path_hex]
        tree = _closed_deterministic_test_parser(raw)
        path_facts = facts_by_path[path_hex]
        modules = [fact for fact in path_facts if fact["fact_kind"] == "MODULE"]
        if len(modules) != 1:
            continue
        module = modules[0]
        imports = [
            fact for fact in path_facts if fact["fact_kind"] == "IMPORT_DECLARATION"
        ]
        for body_ordinal, node in enumerate(tree.body):
            if not isinstance(node, ast.Import) or len(node.names) != 1:
                continue
            span = _node_byte_span(raw, node)
            alias = node.names[0]
            matching = [
                fact
                for fact in imports
                if (
                    fact["source_anchor"]["start_byte"],
                    fact["source_anchor"]["end_byte"],
                )
                == span
                and fact["local_ordinal"] == 0
                and fact["semantic_attributes"]
                == {
                    "import_form": "IMPORT",
                    "relative_level": 0,
                    "module_parts": alias.name.split("."),
                    "imported_name": None,
                    "alias_name": alias.asname,
                }
            ]
            if len(matching) != 1:
                continue
            candidates.append(
                {
                    "relation_space": "CHILD_EDGE",
                    "relation_kind": "LEXICAL_CONTAINS",
                    "source_fact_id": module["fact_id"],
                    "local_ordinal": body_ordinal,
                    "target": {
                        "target_kind": "FACT",
                        "fact_id": matching[0]["fact_id"],
                    },
                    "semantic_attributes": {},
                }
            )
    return candidates


def _closed_deterministic_test_parser(raw: bytes) -> ast.Module:
    try:
        text = raw.decode("utf-8-sig", errors="strict")
        return ast.parse(text, mode="exec", feature_version=(3, 10))
    except (SyntaxError, UnicodeError, ValueError) as exc:
        raise ClosedRelationProviderFailed from exc


def _node_byte_span(raw: bytes, node: ast.AST) -> tuple[int, int]:
    lineno = getattr(node, "lineno", None)
    col = getattr(node, "col_offset", None)
    end_lineno = getattr(node, "end_lineno", None)
    end_col = getattr(node, "end_col_offset", None)
    coordinates = (lineno, col, end_lineno, end_col)
    if not all(type(value) is int and value >= 0 for value in coordinates):
        raise ClosedRelationProviderFailed
    lines = raw.splitlines(keepends=True)
    if lineno < 1 or end_lineno < lineno or end_lineno > len(lines):
        raise ClosedRelationProviderFailed
    start = sum(len(line) for line in lines[: lineno - 1]) + col
    end = sum(len(line) for line in lines[: end_lineno - 1]) + end_col
    if start < 0 or end < start or end > len(raw):
        raise ClosedRelationProviderFailed
    return start, end
