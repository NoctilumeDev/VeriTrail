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


_PROVIDER_A = _descriptor("closed-relation-provider-a")
_PROVIDER_B = _descriptor("closed-relation-provider-b")

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
    }
)


def closed_test_relation_observation_bindings() -> tuple[ProviderBinding, ...]:
    """Return the exact private A/B responsibility sources."""

    return (
        ProviderBinding(_PROVIDER_A, "observation-a"),
        ProviderBinding(_PROVIDER_B, "observation-b"),
    )


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
