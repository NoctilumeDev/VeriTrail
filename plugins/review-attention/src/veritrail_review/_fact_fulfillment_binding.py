"""Separate closed /0.2 conformance identities, not third-party Provider discovery."""

from __future__ import annotations

import copy
from typing import Mapping, Sequence

from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review._execution_cell_binding import ProviderBinding, ProviderDescriptor
from veritrail_review._execution_cell_protocol import ExecutionCellTransportSafetyLimits
from veritrail_review._language_support import _revalidate_exact_inputs
from veritrail_review._multi_provider_applicability import _descriptor_rank
from veritrail_review.derivation_input_contracts import DerivationInputSet


def descriptor_for_launch_key(key: str) -> ProviderDescriptor | None:
    if key not in {"fulfill-a", "fulfill-b", "fulfill-advisory"}:
        return None
    return ProviderDescriptor(
        capability_id=(
            "python-ast-advisory" if key == "fulfill-advisory" else "python-ast"
        ),
        provider_id="closed-fact-" + key,
        provider_version="0.2",
        parser_id="admitted-cpython-product",
        parser_version="3.10.6",
        runtime_id="veritrail-review-fact-worker",
        runtime_version="0.2",
    )


def closed_fact_bindings(
    *, include_advisory: bool = False
) -> tuple[ProviderBinding, ...]:
    keys = ["fulfill-a", "fulfill-b"] + (
        ["fulfill-advisory"] if include_advisory else []
    )
    return tuple(
        sorted(
            (ProviderBinding(descriptor_for_launch_key(k), k) for k in keys),
            key=lambda b: _descriptor_rank(b.descriptor),
        )
    )


def _admit_closed_applicability(
    inputs, *, derivation_id, bindings, cancellation_requested, transport_limits
):
    if (
        type(inputs) is not DerivationInputSet
        or type(derivation_id) is not str
        or not derivation_id
        or any(0xD800 <= ord(c) <= 0xDFFF for c in derivation_id)
        or not isinstance(bindings, Sequence)
        or isinstance(bindings, (str, bytes))
        or type(transport_limits) is not ExecutionCellTransportSafetyLimits
        or (cancellation_requested is not None and not callable(cancellation_requested))
    ):
        raise ValueError("invalid /0.2 applicability request")
    required = {}
    for item in inputs.review_policy_document_copy()["provider_requirements"]:
        if (
            set(item) != {"capability_id", "required", "composition_mode"}
            or item["capability_id"] not in {"python-ast", "python-ast-advisory"}
            or item["required"] is not (item["capability_id"] == "python-ast")
            or item["composition_mode"] != "CUMULATIVE"
            or item["capability_id"] in required
        ):
            raise ValueError("unqualified requiredness")
        required[item["capability_id"]] = item["required"]
    if "python-ast" not in required:
        raise ValueError("missing required capability")
    submitted = tuple(bindings)
    if any(
        type(b) is not ProviderBinding
        or b.descriptor != descriptor_for_launch_key(b.launch_key)
        or descriptor_for_launch_key(b.launch_key) is None
        for b in submitted
    ):
        raise ValueError("foreign /0.1 or unknown descriptor")
    expected = closed_fact_bindings(include_advisory="python-ast-advisory" in required)
    normalized = tuple(sorted(submitted, key=lambda b: _descriptor_rank(b.descriptor)))
    if normalized != expected:
        raise ValueError("caller cannot narrow Provider responsibility")
    return required, tuple(
        ProviderBinding(ProviderDescriptor(**b.descriptor.document()), b.launch_key)
        for b in normalized
    )


_STAGE_APPLICABILITY_FUNCTION = "r1-fact-relation-stage-applicability/0.2"
_PARENT_CORRECTION_FUNCTION = (
    "r1-fact-handoff-relation-interoperability-correction/0.2"
)
_OWNER_BY_CAPABILITY = {
    "python-ast": "FACT",
    "python-ast-advisory": "FACT",
    "review-relation-derivation": "RELATION",
}


def build_fact_relation_stage_applicability(inputs: DerivationInputSet) -> dict[str, object]:
    """Classify every exact Policy requirement into one and only one stage."""

    if type(inputs) is not DerivationInputSet:
        raise ValueError("invalid /0.2 stage applicability input")
    try:
        _revalidate_exact_inputs(inputs)
    except Exception as exc:
        raise ValueError("invalid /0.2 exact input world") from exc
    policy = inputs.review_policy_document_copy()
    rows = policy.get("provider_requirements")
    if not isinstance(rows, list):
        raise ValueError("invalid /0.2 Policy requirement universe")

    expected = {
        "python-ast": (True, "CUMULATIVE"),
        "python-ast-advisory": (False, "CUMULATIVE"),
        "review-relation-derivation": (True, "CUMULATIVE"),
    }
    seen: set[str] = set()
    owned: dict[str, list[dict[str, object]]] = {"FACT": [], "RELATION": []}
    exact_rows: list[dict[str, object]] = []
    for raw in rows:
        if not isinstance(raw, Mapping) or set(raw) != {
            "capability_id",
            "required",
            "composition_mode",
        }:
            raise ValueError("invalid /0.2 Policy requirement row")
        capability = raw["capability_id"]
        if (
            not isinstance(capability, str)
            or capability not in expected
            or capability in seen
            or (raw["required"], raw["composition_mode"]) != expected[capability]
        ):
            raise ValueError("unqualified /0.2 Policy requirement")
        seen.add(capability)
        row = copy.deepcopy(dict(raw))
        exact_rows.append(row)
        owned[_OWNER_BY_CAPABILITY[capability]].append(row)

    if "python-ast" not in seen or "review-relation-derivation" not in seen:
        raise ValueError("missing required /0.2 stage capability")
    if seen not in (
        {"python-ast", "review-relation-derivation"},
        {"python-ast", "python-ast-advisory", "review-relation-derivation"},
    ):
        raise ValueError("unknown /0.2 stage capability")

    fact_rows = owned["FACT"]
    relation_rows = owned["RELATION"]
    if (
        len(fact_rows) + len(relation_rows) != len(exact_rows)
        or {item["capability_id"] for item in fact_rows}
        & {item["capability_id"] for item in relation_rows}
        or sorted(
            item["capability_id"] for item in (*fact_rows, *relation_rows)
        )
        != sorted(item["capability_id"] for item in exact_rows)
    ):
        raise ValueError("non-total /0.2 stage ownership")

    policy_bytes = memoryview(inputs.review_policy_canonical_bytes).tobytes()
    if policy_bytes != canonical_json_bytes(policy) + b"\n":
        raise ValueError("Policy canonical bytes changed")
    stages = []
    for stage, applicable, non_applicable in (
        ("FACT", fact_rows, relation_rows),
        ("RELATION", relation_rows, fact_rows),
    ):
        payload = {
            "stage": stage,
            "applicable_requirements": copy.deepcopy(applicable),
            "non_applicable_requirements": copy.deepcopy(non_applicable),
        }
        stages.append(
            {
                **payload,
                "stage_partition_digest": semantic_digest(
                    "veritrail.review.fact-relation-stage-partition/0.2", payload
                ),
            }
        )
    ownership = [
        {"requirement": copy.deepcopy(row), "owner": _OWNER_BY_CAPABILITY[row["capability_id"]]}
        for row in exact_rows
    ]
    reconciliation_payload = {
        "requirements": copy.deepcopy(exact_rows),
        "ownership": ownership,
        "union_complete": True,
        "intersection_empty": True,
        "owner_count_per_requirement": 1,
    }
    return {
        "parent_correction_function": _PARENT_CORRECTION_FUNCTION,
        "stage_applicability_function": _STAGE_APPLICABILITY_FUNCTION,
        "policy_digest": inputs.policy_digest,
        "policy_canonical_bytes_hex": policy_bytes.hex(),
        "stages": stages,
        "cross_stage_reconciliation": {
            **reconciliation_payload,
            "reconciliation_digest": semantic_digest(
                "veritrail.review.fact-relation-stage-ownership/0.2",
                reconciliation_payload,
            ),
        },
    }


def _admit_relation_transition_fact_applicability(
    inputs, *, derivation_id, bindings, cancellation_requested, transport_limits
):
    applicability = build_fact_relation_stage_applicability(inputs)
    fact_rows = next(
        item for item in applicability["stages"] if item["stage"] == "FACT"
    )["applicable_requirements"]
    required = {item["capability_id"]: item["required"] for item in fact_rows}
    if (
        type(derivation_id) is not str
        or not derivation_id
        or any(0xD800 <= ord(c) <= 0xDFFF for c in derivation_id)
        or not isinstance(bindings, Sequence)
        or isinstance(bindings, (str, bytes))
        or type(transport_limits) is not ExecutionCellTransportSafetyLimits
        or (cancellation_requested is not None and not callable(cancellation_requested))
    ):
        raise ValueError("invalid /0.2 Fact-stage applicability request")
    submitted = tuple(bindings)
    if any(
        type(binding) is not ProviderBinding
        or descriptor_for_launch_key(binding.launch_key) is None
        or binding.descriptor != descriptor_for_launch_key(binding.launch_key)
        for binding in submitted
    ):
        raise ValueError("foreign /0.2 Fact-stage binding")
    expected_bindings = closed_fact_bindings(
        include_advisory="python-ast-advisory" in required
    )
    normalized = tuple(sorted(submitted, key=lambda item: _descriptor_rank(item.descriptor)))
    if normalized != expected_bindings:
        raise ValueError("caller cannot narrow Fact-stage responsibility")
    return required, tuple(
        ProviderBinding(ProviderDescriptor(**item.descriptor.document()), item.launch_key)
        for item in normalized
    )
