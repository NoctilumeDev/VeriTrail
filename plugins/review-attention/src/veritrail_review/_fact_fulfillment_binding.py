"""Separate closed /0.2 conformance identities, not third-party Provider discovery."""

from __future__ import annotations

from typing import Sequence

from veritrail_review._execution_cell_binding import ProviderBinding, ProviderDescriptor
from veritrail_review._execution_cell_protocol import ExecutionCellTransportSafetyLimits
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
