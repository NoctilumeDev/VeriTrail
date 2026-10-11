from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Iterator, Mapping

from veritrail_review._execution_cell_application import (
    _canonicalize_candidate,
    _descriptor_from_document,
    provider_run_id,
)
from veritrail_review._execution_cell_binding import (
    ProviderDescriptor,
    descriptor_for_launch_key,
)
from veritrail_review._parse_fulfillment_values import (
    PARSE_FUNCTION_ID,
    _validate_tree_value,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


CONSUMER_FUNCTION = "r1-parse-product-fact-consumer/0.1"
PROTOCOL = "veritrail-review-parse-product-fact-cell/0.1"
PROJECTION_DOMAIN = "veritrail.review.private-parse-product-fact-projection/0.1"
OPERANDS_DOMAIN = "veritrail.review.private-parse-product-fact-operands/0.1"
_PROJECTION_KEYS = frozenset(
    {
        "consumer_function",
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "slice_policy_digest",
        "derivation_profile_digest",
        "language_support_function",
        "classification_digest",
        "parse_function",
        "product_set_digest",
        "provider_descriptor",
        "assigned_products",
    }
)
_REQUEST_KEYS = frozenset(
    {
        "protocol",
        "message_kind",
        "derivation_id",
        "consumer_attempt_id",
        "child_attempt_id",
        "provider_run_id",
        "operands_digest",
        "consumer_projection_digest",
        "projection",
    }
)
_TERMINAL_KEYS = frozenset(
    {
        "protocol",
        "message_kind",
        "consumer_attempt_id",
        "child_attempt_id",
        "provider_run_id",
        "operands_digest",
        "consumer_projection_digest",
        "product_set_digest",
        "terminal_kind",
        "candidate_records",
    }
)
_MEMBER_KEYS = frozenset(
    {
        "subject_identity",
        "obligation_id",
        "product_semantic_digest",
        "git_path_hex",
        "source_size_bytes",
        "product",
        "node_anchors",
    }
)
_RECORD_KEYS = frozenset(
    {
        "product_subject_identity",
        "product_semantic_digest",
        "provider_run_id",
        "node_path",
        "candidate",
    }
)
_TERMINAL_KINDS = frozenset(
    {
        "COMPLETED",
        "PROVIDER_FAILED",
        "PROVIDER_UNAVAILABLE",
        "NONCONFORMANT_PROVIDER_OUTPUT",
        "INTERNAL_DERIVATION_ERROR",
    }
)


class ProductFactProtocolError(ValueError):
    """A private successor request or candidate lost its exact binding."""


@dataclass(frozen=True)
class ValidatedProductFactRequest:
    document: dict[str, object]
    descriptor: ProviderDescriptor
    provider_run_id: str
    source_sizes_by_path_hex: Mapping[str, int]
    in_scope_paths: frozenset[str]
    supported_paths: frozenset[str]


def scalar(value: object) -> object:
    if not isinstance(value, dict) or set(value) != {"value_kind", "value"}:
        raise ProductFactProtocolError("expected canonical scalar")
    if value["value_kind"] != "SCALAR":
        raise ProductFactProtocolError("expected canonical scalar")
    return value["value"]


def walk_product(
    value: Mapping[str, object], path: str = "$"
) -> Iterator[tuple[str, dict[str, object]]]:
    kind = value["value_kind"]
    if kind == "AST":
        yield path, value  # type: ignore[misc]
        for name in sorted(value["fields"]):  # type: ignore[arg-type]
            yield from walk_product(value["fields"][name], path + "/fields/" + name)  # type: ignore[index,arg-type]
    elif kind == "LIST":
        for index, child in enumerate(value["items"]):  # type: ignore[arg-type]
            yield from walk_product(child, path + "/items/" + str(index))


def _digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(c in "0123456789abcdef" for c in value)
    )


def validate_projection(document: Mapping[str, object]) -> dict[str, object]:
    try:
        if (
            set(document) != _PROJECTION_KEYS
            or document["consumer_function"] != CONSUMER_FUNCTION
        ):
            raise ValueError
        if document["parse_function"] != PARSE_FUNCTION_ID:
            raise ValueError
        for name in _PROJECTION_KEYS - {
            "consumer_function",
            "parse_function",
            "language_support_function",
            "provider_descriptor",
            "assigned_products",
        }:
            if not _digest(document[name]):
                raise ValueError
        if not isinstance(document["language_support_function"], str):
            raise ValueError
        _descriptor_from_document(document["provider_descriptor"])
        members = document["assigned_products"]
        if not isinstance(members, list) or not members:
            raise ValueError
        subjects: set[str] = set()
        previous_path: bytes | None = None
        for member in members:
            if not isinstance(member, dict) or set(member) != _MEMBER_KEYS:
                raise ValueError
            for name in (
                "subject_identity",
                "obligation_id",
                "product_semantic_digest",
            ):
                if not _digest(member[name]):
                    raise ValueError
            subject = member["subject_identity"]
            if subject in subjects:
                raise ValueError
            subjects.add(subject)
            path_hex = member["git_path_hex"]
            if not isinstance(path_hex, str):
                raise ValueError
            path = bytes.fromhex(path_hex)
            if (
                not path
                or path.hex() != path_hex
                or (previous_path is not None and path <= previous_path)
            ):
                raise ValueError
            previous_path = path
            size = member["source_size_bytes"]
            if type(size) is not int or size < 0:
                raise ValueError
            product = member["product"]
            _validate_tree_value(product)
            if product["value_kind"] != "AST" or product["node_type"] != "Module":
                raise ValueError
            if member["product_semantic_digest"] != semantic_digest(
                "veritrail.review.private-parse-product/0.1",
                {
                    "subject_identity": subject,
                    "obligation_id": member["obligation_id"],
                    "parse_function": PARSE_FUNCTION_ID,
                    "product": product,
                },
            ):
                raise ValueError
            anchors = member["node_anchors"]
            if not isinstance(anchors, dict):
                raise ValueError
            expected_paths = {
                p
                for p, node in walk_product(product)
                if all(
                    k in node["attributes"]
                    for k in ("lineno", "col_offset", "end_lineno", "end_col_offset")
                )
            }
            if set(anchors) != expected_paths:
                raise ValueError
            for anchor in anchors.values():
                if not isinstance(anchor, dict) or set(anchor) != {
                    "start_byte",
                    "end_byte",
                }:
                    raise ValueError
                start, end = anchor["start_byte"], anchor["end_byte"]
                if (
                    type(start) is not int
                    or type(end) is not int
                    or not 0 <= start <= end <= size
                ):
                    raise ValueError
        return copy.deepcopy(dict(document))
    except Exception as exc:
        raise ProductFactProtocolError("invalid product-only projection") from exc


def projection_digest(document: Mapping[str, object]) -> str:
    return semantic_digest(PROJECTION_DOMAIN, validate_projection(document))


def build_request(
    projection: Mapping[str, object], *, derivation_id: str, consumer_attempt_id: str
) -> dict[str, object]:
    owned = validate_projection(projection)
    digest = projection_digest(owned)
    child_id = semantic_digest(
        "veritrail.review.private-product-fact-child/0.1",
        {
            "consumer_attempt_id": consumer_attempt_id,
            "consumer_projection_digest": digest,
        },
    )
    operands = semantic_digest(
        OPERANDS_DOMAIN,
        {
            "derivation_id": derivation_id,
            "consumer_attempt_id": consumer_attempt_id,
            "child_attempt_id": child_id,
            "consumer_projection_digest": digest,
        },
    )
    descriptor = _descriptor_from_document(owned["provider_descriptor"])
    return {
        "protocol": PROTOCOL,
        "message_kind": "FACT_CONSUMER_REQUEST",
        "derivation_id": derivation_id,
        "consumer_attempt_id": consumer_attempt_id,
        "child_attempt_id": child_id,
        "provider_run_id": provider_run_id(derivation_id, descriptor, operands),
        "operands_digest": operands,
        "consumer_projection_digest": digest,
        "projection": owned,
    }


def validate_request(
    document: Mapping[str, object], *, launch_key: str
) -> ValidatedProductFactRequest:
    try:
        if (
            set(document) != _REQUEST_KEYS
            or document["protocol"] != PROTOCOL
            or document["message_kind"] != "FACT_CONSUMER_REQUEST"
        ):
            raise ValueError
        if (
            not isinstance(document["derivation_id"], str)
            or not document["derivation_id"]
        ):
            raise ValueError
        if not _digest(document["consumer_attempt_id"]):
            raise ValueError
        projection = validate_projection(document["projection"])  # type: ignore[arg-type]
        descriptor = _descriptor_from_document(projection["provider_descriptor"])
        if descriptor != descriptor_for_launch_key(launch_key):
            raise ValueError
        expected = build_request(
            projection,
            derivation_id=document["derivation_id"],
            consumer_attempt_id=document["consumer_attempt_id"],
        )
        if canonical_json_bytes(expected) != canonical_json_bytes(dict(document)):
            raise ValueError
        sizes = {
            m["git_path_hex"]: m["source_size_bytes"]
            for m in projection["assigned_products"]
        }
        return ValidatedProductFactRequest(
            document={
                **copy.deepcopy(dict(document)),
                "source_snapshot_digest": projection["source_snapshot_digest"],
                "derivation_profile_digest": projection["derivation_profile_digest"],
            },
            descriptor=descriptor,
            provider_run_id=document["provider_run_id"],
            source_sizes_by_path_hex=sizes,
            in_scope_paths=frozenset(sizes),
            supported_paths=frozenset(sizes),
        )
    except Exception as exc:
        raise ProductFactProtocolError("invalid product-only request") from exc


def candidate_from_product(
    member: Mapping[str, object], node_path: str
) -> dict[str, object]:
    """The closed conformance providers project MODULE and CLASS candidates only."""
    if node_path == "$":
        kind, space, attributes = "MODULE", "MODULE_ENTITY", {"module_key_parts": None}
        anchor = {"start_byte": 0, "end_byte": member["source_size_bytes"]}
    else:
        node = dict(walk_product(member["product"])).get(node_path)  # type: ignore[arg-type]
        if node is None or node["node_type"] != "ClassDef":
            raise ProductFactProtocolError(
                "candidate does not resolve to its product node"
            )
        kind, space = "CLASS_DECLARATION", "DECLARATION_NODE"
        attributes = {"declared_name": scalar(node["fields"]["name"])}
        anchor = member["node_anchors"][node_path]  # type: ignore[index]
    return {
        "subject_space": space,
        "fact_kind": kind,
        "source_anchor": {
            "git_path": {
                "path_kind": "GIT_PATH",
                "git_path_hex": member["git_path_hex"],
            },
            **anchor,
        },
        "local_ordinal": 0,
        "semantic_attributes": attributes,
    }


def product_candidate_records(request: Mapping[str, object]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for member in request["projection"]["assigned_products"]:  # type: ignore[index]
        paths = [
            "$",
            *(
                p
                for p, node in walk_product(member["product"])
                if node["node_type"] == "ClassDef"
            ),
        ]
        for path in paths:
            records.append(
                {
                    "product_subject_identity": member["subject_identity"],
                    "product_semantic_digest": member["product_semantic_digest"],
                    "provider_run_id": request["provider_run_id"],
                    "node_path": path,
                    "candidate": candidate_from_product(member, path),
                }
            )
    return records


def terminal_document(
    request: Mapping[str, object],
    *,
    terminal_kind: str,
    records: list[dict[str, object]],
) -> dict[str, object]:
    if terminal_kind not in _TERMINAL_KINDS or (
        terminal_kind != "COMPLETED" and records
    ):
        raise ProductFactProtocolError("invalid terminal kind or candidates")
    return {
        "protocol": PROTOCOL,
        "message_kind": "FACT_CONSUMER_TERMINAL",
        **{
            name: request[name]
            for name in (
                "consumer_attempt_id",
                "child_attempt_id",
                "provider_run_id",
                "operands_digest",
                "consumer_projection_digest",
            )
        },
        "product_set_digest": request["projection"]["product_set_digest"],  # type: ignore[index]
        "terminal_kind": terminal_kind,
        "candidate_records": copy.deepcopy(records),
    }


def admit_terminal(
    document: Mapping[str, object], *, request: Mapping[str, object], launch_key: str
) -> tuple[str, tuple[bytes, ...]]:
    """Admit every candidate against exact assigned product/node/run; never drop invalid rows."""
    try:
        validated = validate_request(request, launch_key=launch_key)
        if (
            set(document) != _TERMINAL_KEYS
            or document["terminal_kind"] not in _TERMINAL_KINDS
        ):
            raise ValueError
        records = document["candidate_records"]
        if not isinstance(records, list):
            raise ValueError
        expected = terminal_document(
            request, terminal_kind=document["terminal_kind"], records=records
        )
        if canonical_json_bytes(dict(document)) != canonical_json_bytes(expected):
            raise ValueError
        members = {
            m["subject_identity"]: m for m in request["projection"]["assigned_products"]
        }
        facts: dict[str, dict[str, object]] = {}
        by_subject: dict[str, str] = {}
        for record in records:
            if not isinstance(record, dict) or set(record) != _RECORD_KEYS:
                raise ValueError
            member = members.get(record["product_subject_identity"])
            if (
                member is None
                or record["product_semantic_digest"]
                != member["product_semantic_digest"]
                or record["provider_run_id"] != request["provider_run_id"]
            ):
                raise ValueError
            expected_candidate = candidate_from_product(member, record["node_path"])
            if canonical_json_bytes(record["candidate"]) != canonical_json_bytes(
                expected_candidate
            ):
                raise ValueError
            fact = _canonicalize_candidate(validated, record["candidate"])  # type: ignore[arg-type]
            previous = by_subject.setdefault(
                fact["subject_key_digest"], fact["fact_id"]
            )
            if previous != fact["fact_id"]:
                raise ValueError
            facts[fact["fact_id"]] = fact
        return document["terminal_kind"], tuple(canonical_json_bytes(facts[k]) for k in sorted(facts))  # type: ignore[return-value]
    except Exception as exc:
        raise ProductFactProtocolError(
            "product-bound terminal admission failed"
        ) from exc
