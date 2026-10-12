"""Application-owned U/E. It is never serialized into the child request."""

from __future__ import annotations

import copy
import unicodedata
from types import SimpleNamespace

from veritrail_review._execution_cell_application import _canonicalize_candidate
from veritrail_review._fact_fulfillment_ast import FIELDS
from veritrail_review._parse_product_fact_protocol import scalar
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input import (
    _is_python_identifier,
    _codepoint_in_ranges,
)
from veritrail_review.derivation_input import (
    _POST_PYTHON_310_START_RANGES,
    _POST_PYTHON_310_CONTINUE_RANGES,
)

FUNCTION = "r1-fact-projection-fulfillment/0.1"


def module_parts(path_hex, rule):
    # Only the hosts covered by the frozen feasibility/conformance boundary.
    if unicodedata.unidata_version not in {"13.0.0", "15.1.0"}:
        raise ValueError("unqualified identifier normalization host")
    root = rule["module_root"]
    prefix = (
        []
        if root["path_kind"] == "REPOSITORY_ROOT"
        else bytes.fromhex(root["git_path_hex"]).split(b"/")
    )
    parts = bytes.fromhex(path_hex).split(b"/")
    if parts[: len(prefix)] != prefix:
        return None
    parts = parts[len(prefix) :]
    if not parts or not parts[-1].endswith(b".py"):
        return None
    omit = parts[-1] == b"__init__.py"
    parts[-1] = parts[-1][:-3]
    if omit:
        parts.pop()
    result = list(rule["package_prefix"])
    try:
        for part in parts:
            raw = part.decode("utf-8", errors="strict")
            if (
                not raw.isidentifier()
                or _codepoint_in_ranges(ord(raw[0]), _POST_PYTHON_310_START_RANGES)
                or any(
                    _codepoint_in_ranges(ord(c), _POST_PYTHON_310_CONTINUE_RANGES)
                    for c in raw[1:]
                )
            ):
                return None
            normalized = unicodedata.normalize("NFKC", raw)
            if not _is_python_identifier(normalized):
                return None
            result.append(normalized)
    except UnicodeDecodeError:
        return None
    return result


def slots(member):
    """Visit every field/list edge. Return slots even when attributes are unrepresentable."""
    stack = [("$", member["product"], None)]
    while stack:
        path, value, edge = stack.pop()
        kind = value["value_kind"]
        if kind == "LIST":
            stack.extend(
                (path + "/items/" + str(i), v, edge)
                for i, v in reversed(list(enumerate(value["items"])))
            )
            continue
        if kind == "SCALAR":
            continue
        node_type, fields = value["node_type"], value["fields"]
        if node_type not in FIELDS or set(fields) != set(FIELDS[node_type]):
            raise ValueError("unknown or incomplete CPython 3.10 product node: " + path)
        stack.extend(
            (path + "/fields/" + k, fields[k], (node_type, k, fields[k]["value_kind"]))
            for k in reversed(sorted(fields))
        )
        if path == "$":
            if node_type != "Module":
                raise ValueError("expected Module")
            yield path, 0, "MODULE", {"module_key_parts": None}
        elif node_type == "ClassDef":
            yield path, 0, "CLASS_DECLARATION", {
                "declared_name": scalar(fields["name"])
            }
        elif node_type in {"FunctionDef", "AsyncFunctionDef"}:
            fact_kind = (
                "METHOD_DECLARATION"
                if edge == ("ClassDef", "body", "LIST")
                else "FUNCTION_DECLARATION"
            )
            yield path, 0, fact_kind, {
                "declared_name": scalar(fields["name"]),
                "function_form": "ASYNC" if node_type == "AsyncFunctionDef" else "SYNC",
            }
        elif node_type in {"Import", "ImportFrom"}:
            if fields["names"]["value_kind"] != "LIST":
                raise ValueError("missing import aliases")
            for i, alias in enumerate(fields["names"]["items"]):
                if alias.get("node_type") != "alias":
                    raise ValueError("invalid import alias")
                name = scalar(alias["fields"]["name"])
                module = name if node_type == "Import" else scalar(fields["module"])
                yield path, i, "IMPORT_DECLARATION", {
                    "import_form": "IMPORT" if node_type == "Import" else "FROM_IMPORT",
                    "relative_level": (
                        0 if node_type == "Import" else scalar(fields["level"])
                    ),
                    "module_parts": [] if module is None else module.split("."),
                    "imported_name": None if node_type == "Import" else name,
                    "alias_name": scalar(alias["fields"]["asname"]),
                }


def candidate(member, path, ordinal, kind, attributes):
    anchor = (
        {"start_byte": 0, "end_byte": member["source_size_bytes"]}
        if kind == "MODULE"
        else member["node_anchors"][path]
    )
    return {
        "subject_space": (
            "MODULE_ENTITY"
            if kind == "MODULE"
            else (
                "IMPORT_ALIAS" if kind == "IMPORT_DECLARATION" else "DECLARATION_NODE"
            )
        ),
        "fact_kind": kind,
        "source_anchor": {
            "git_path": {
                "path_kind": "GIT_PATH",
                "git_path_hex": member["git_path_hex"],
            },
            **anchor,
        },
        "local_ordinal": ordinal,
        "semantic_attributes": attributes,
    }


def qualify(projection):
    """Complete constructible U or raise integrity failure; complete E or explicit blocker."""
    universe, expected, blockers, limitations, keys = {}, {}, [], [], {}
    members = projection["assigned_products"]
    sizes = {m["git_path_hex"]: m["source_size_bytes"] for m in members}
    adapter = SimpleNamespace(
        document=projection,
        source_sizes_by_path_hex=sizes,
        in_scope_paths=frozenset(sizes),
        supported_paths=frozenset(sizes),
        provider_run_id="0" * 64,
    )
    for member in members:
        mapped = module_parts(
            member["git_path_hex"], projection["python_module_mapping"]
        )
        if mapped is None:
            limitations.append(
                {
                    "git_path_hex": member["git_path_hex"],
                    "reason": "MODULE_MAPPING_NULL",
                }
            )
        else:
            keys.setdefault(tuple(mapped), []).append(member["git_path_hex"])
        for path, ordinal, kind, attributes in slots(member):
            if kind == "MODULE":
                attributes = {"module_key_parts": mapped}
            value = candidate(member, path, ordinal, kind, attributes)
            subject = semantic_digest(
                "veritrail.review.fact-subject/0.1",
                {
                    "source_snapshot_digest": projection["source_snapshot_digest"],
                    "derivation_profile_digest": projection[
                        "derivation_profile_digest"
                    ],
                    "source_anchor": value["source_anchor"],
                    "subject_space": value["subject_space"],
                    "local_ordinal": ordinal,
                },
            )
            if subject in universe:
                raise ValueError("distinct slots collide in subject identity")
            universe[subject] = {
                "subject_key_digest": subject,
                "product_subject_identity": member["subject_identity"],
                "product_semantic_digest": member["product_semantic_digest"],
                "node_path": path,
                "alias_ordinal": ordinal,
            }
            try:
                fact = _canonicalize_candidate(adapter, value)
                expected[subject] = {
                    k: v for k, v in fact.items() if k != "provenance_refs"
                }
            except ValueError:
                blockers.append(
                    {
                        "slot": universe[subject],
                        "candidate": value,
                        "reason": "UNREPRESENTABLE_EXPECTED_FACT",
                    }
                )
    return {
        "function": FUNCTION,
        "status": "QUALIFIED" if not blockers else "BLOCKED_UNREPRESENTABLE",
        "universe": [universe[k] for k in sorted(universe)],
        "expected": [expected[k] for k in sorted(expected)],
        "blockers": blockers,
        "mapping_limitations": limitations,
        "mapping_collisions": [
            {"module_key_parts": list(k), "git_path_hexes": sorted(v)}
            for k, v in sorted(keys.items())
            if len(v) > 1
        ],
    }
