from __future__ import annotations

from typing import Callable, Sequence

from veritrail_review._execution_cell_binding import (
    ProviderBinding,
    ProviderDescriptor,
    binding_matches_closed_allow_list,
    closed_test_binding,
)
from veritrail_review._execution_cell_protocol import (
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._multi_provider_values import (
    _MultiProviderCompositionError,
    _MultiProviderCompositionFailureCode,
)
from veritrail_review.derivation_input_contracts import DerivationInputSet


_REQUIRED_BINDING_KEYS = ("multi-a", "multi-b")
_ADVISORY_BINDING_KEY = "multi-advisory"
_ALLOWED_REQUIREMENTS = {
    "python-ast": True,
    "python-ast-advisory": False,
}


def _descriptor_rank(descriptor: ProviderDescriptor) -> tuple[str, ...]:
    return (
        descriptor.capability_id,
        descriptor.provider_id,
        descriptor.provider_version,
        descriptor.parser_id,
        descriptor.parser_version,
        descriptor.runtime_id,
        descriptor.runtime_version,
    )


def closed_test_multi_provider_bindings(
    *, include_advisory: bool = False
) -> tuple[ProviderBinding, ...]:
    """Return the private fixed binding set; absent from the package API."""

    keys = (*_REQUIRED_BINDING_KEYS, *(
        (_ADVISORY_BINDING_KEY,) if include_advisory else ()
    ))
    bindings = tuple(closed_test_binding(key) for key in keys)
    return tuple(sorted(bindings, key=lambda item: _descriptor_rank(item.descriptor)))


def _admit_closed_applicability(
    inputs: object,
    *,
    derivation_id: object,
    bindings: object,
    cancellation_requested: object,
    transport_limits: object,
) -> tuple[dict[str, bool], tuple[ProviderBinding, ...]]:
    valid_id = (
        isinstance(derivation_id, str)
        and bool(derivation_id)
        and all(not 0xD800 <= ord(character) <= 0xDFFF for character in derivation_id)
    )
    if (
        not isinstance(inputs, DerivationInputSet)
        or not valid_id
        or not isinstance(bindings, Sequence)
        or isinstance(bindings, (str, bytes, bytearray))
        or not isinstance(transport_limits, ExecutionCellTransportSafetyLimits)
        or (cancellation_requested is not None and not callable(cancellation_requested))
    ):
        raise _MultiProviderCompositionError(
            _MultiProviderCompositionFailureCode.INVALID_COMPOSITION_REQUEST
        )
    try:
        raw_requirements = inputs.review_policy_document_copy()["provider_requirements"]
        if not isinstance(raw_requirements, list):
            raise ValueError
        requirements: dict[str, bool] = {}
        for item in raw_requirements:
            if (
                not isinstance(item, dict)
                or set(item) != {"capability_id", "required", "composition_mode"}
                or item["capability_id"] not in _ALLOWED_REQUIREMENTS
                or item["required"] is not _ALLOWED_REQUIREMENTS[item["capability_id"]]
                or item["composition_mode"] != "CUMULATIVE"
                or item["capability_id"] in requirements
            ):
                raise ValueError
            requirements[item["capability_id"]] = item["required"]
        if "python-ast" not in requirements or set(requirements) not in (
            {"python-ast"},
            {"python-ast", "python-ast-advisory"},
        ):
            raise ValueError
    except Exception as exc:
        raise _MultiProviderCompositionError(
            _MultiProviderCompositionFailureCode.INVALID_COMPOSITION_REQUEST
        ) from exc

    expected = closed_test_multi_provider_bindings(
        include_advisory="python-ast-advisory" in requirements
    )
    try:
        submitted = tuple(bindings)
        if any(
            not isinstance(binding, ProviderBinding)
            or not isinstance(binding.descriptor, ProviderDescriptor)
            or not binding_matches_closed_allow_list(binding)
            for binding in submitted
        ):
            raise ValueError
        keys = [
            (binding.descriptor.capability_id, binding.descriptor.provider_id)
            for binding in submitted
        ]
        if len(keys) != len(set(keys)):
            raise ValueError
        normalized = tuple(
            sorted(submitted, key=lambda item: _descriptor_rank(item.descriptor))
        )
        if normalized != expected:
            raise ValueError
    except Exception as exc:
        raise _MultiProviderCompositionError(
            _MultiProviderCompositionFailureCode.APPLICABILITY_BINDING_MISMATCH
        ) from exc
    return requirements, tuple(
        ProviderBinding(
            ProviderDescriptor(**binding.descriptor.document()),
            str(binding.launch_key),
        )
        for binding in normalized
    )
