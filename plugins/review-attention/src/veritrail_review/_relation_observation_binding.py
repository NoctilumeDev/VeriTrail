from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from veritrail_review._execution_cell_binding import (
    ProviderBinding,
    ProviderDescriptor,
)


def _descriptor(provider_id: str) -> ProviderDescriptor:
    return ProviderDescriptor(
        capability_id="review-relation-derivation",
        provider_id=provider_id,
        provider_version="0.1-test",
        parser_id="closed-deterministic-test-parser",
        parser_version="0.1-test",
        runtime_id="veritrail-review-test-runtime",
        runtime_version="0.1-test",
    )


def _import_form_successor_descriptor(provider_id: str) -> ProviderDescriptor:
    return ProviderDescriptor(
        capability_id="review-relation-derivation",
        provider_id=provider_id,
        provider_version="0.1-test",
        parser_id="cpython-3.10.6-import-alias-occurrence-parser",
        parser_version="0.1-test",
        runtime_id="veritrail-review-test-runtime",
        runtime_version="0.1-test",
    )


_PROVIDER_A = _descriptor("closed-relation-provider-a")
_PROVIDER_B = _descriptor("closed-relation-provider-b")
_IMPORT_FORM_PROVIDER_A = _import_form_successor_descriptor(
    "relation-import-form-provider-a"
)
_IMPORT_FORM_PROVIDER_B = _import_form_successor_descriptor(
    "relation-import-form-provider-b"
)

_LAUNCH_KEYS: Mapping[str, ProviderDescriptor] = MappingProxyType(
    {
        "observation-a": _PROVIDER_A,
        "observation-b": _PROVIDER_B,
        "observation-a-failed": _PROVIDER_A,
        "observation-b-failed": _PROVIDER_B,
        "observation-a-unavailable": _PROVIDER_A,
        "observation-b-unavailable": _PROVIDER_B,
        "observation-a-empty": _PROVIDER_A,
        "observation-b-empty": _PROVIDER_B,
        "observation-b-conflict": _PROVIDER_B,
        "observation-b-slow": _PROVIDER_B,
        "observation-b-memory": _PROVIDER_B,
        "import-form-observation-a": _IMPORT_FORM_PROVIDER_A,
        "import-form-observation-b": _IMPORT_FORM_PROVIDER_B,
    }
)


def closed_test_relation_observation_bindings() -> tuple[ProviderBinding, ...]:
    """Return the exact private A/B responsibility sources."""

    return (
        ProviderBinding(_PROVIDER_A, "observation-a"),
        ProviderBinding(_PROVIDER_B, "observation-b"),
    )


def corrected_import_form_relation_observation_bindings(
) -> tuple[ProviderBinding, ...]:
    """Return the versioned private import-form successor responsibility sources."""

    return (
        ProviderBinding(_IMPORT_FORM_PROVIDER_A, "import-form-observation-a"),
        ProviderBinding(_IMPORT_FORM_PROVIDER_B, "import-form-observation-b"),
    )


def relation_observation_binding_family_for_descriptor(
    descriptor: ProviderDescriptor,
) -> tuple[ProviderBinding, ...] | None:
    """Resolve only an exact, complete private binding family."""

    for bindings in (
        closed_test_relation_observation_bindings(),
        corrected_import_form_relation_observation_bindings(),
    ):
        if any(binding.descriptor == descriptor for binding in bindings):
            return bindings
    return None


def relation_observation_binding_family_for_launch_key(
    launch_key: str,
) -> tuple[ProviderBinding, ...] | None:
    descriptor = relation_observation_descriptor_for_launch_key(launch_key)
    if descriptor is None:
        return None
    return relation_observation_binding_family_for_descriptor(descriptor)


def relation_observation_binding_matches_allow_list(binding: object) -> bool:
    if not isinstance(binding, ProviderBinding) or not isinstance(
        binding.descriptor, ProviderDescriptor
    ):
        return False
    expected = _LAUNCH_KEYS.get(binding.launch_key)
    return expected is not None and expected == binding.descriptor


def relation_observation_descriptor_for_launch_key(
    launch_key: str,
) -> ProviderDescriptor | None:
    return _LAUNCH_KEYS.get(launch_key)


def relation_observation_descriptor_rank(
    descriptor: ProviderDescriptor,
) -> tuple[str, ...]:
    return (
        descriptor.capability_id,
        descriptor.provider_id,
        descriptor.provider_version,
        descriptor.parser_id,
        descriptor.parser_version,
        descriptor.runtime_id,
        descriptor.runtime_version,
    )
