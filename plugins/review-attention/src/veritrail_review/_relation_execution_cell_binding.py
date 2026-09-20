from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from veritrail_review._execution_cell_binding import (
    ProviderBinding,
    ProviderDescriptor,
)


def _relation_descriptor() -> ProviderDescriptor:
    return ProviderDescriptor(
        capability_id="review-relation-derivation",
        provider_id="closed-relation-provider-a",
        provider_version="0.1-test",
        parser_id="closed-deterministic-test-parser",
        parser_version="0.1-test",
        runtime_id="veritrail-review-test-runtime",
        runtime_version="0.1-test",
    )


_CLOSED_RELATION_DESCRIPTOR = _relation_descriptor()
_CLOSED_RELATION_LAUNCH_KEYS: Mapping[str, ProviderDescriptor] = MappingProxyType(
    {
        "relation-a": _CLOSED_RELATION_DESCRIPTOR,
        "relation-unavailable": _CLOSED_RELATION_DESCRIPTOR,
        "relation-failed": _CLOSED_RELATION_DESCRIPTOR,
        "relation-bad-candidate": _CLOSED_RELATION_DESCRIPTOR,
        "relation-mutates-owned-input": _CLOSED_RELATION_DESCRIPTOR,
        "relation-slow": _CLOSED_RELATION_DESCRIPTOR,
        "relation-memory": _CLOSED_RELATION_DESCRIPTOR,
    }
)


def closed_test_relation_binding(
    launch_key: str = "relation-a",
) -> ProviderBinding:
    """Return a private closed Relation binding; absent from the package API."""

    return ProviderBinding(_CLOSED_RELATION_LAUNCH_KEYS[launch_key], launch_key)


def relation_binding_matches_closed_allow_list(binding: object) -> bool:
    if not isinstance(binding, ProviderBinding) or not isinstance(
        binding.descriptor, ProviderDescriptor
    ):
        return False
    expected = _CLOSED_RELATION_LAUNCH_KEYS.get(binding.launch_key)
    return expected is not None and expected == binding.descriptor


def relation_descriptor_for_launch_key(
    launch_key: str,
) -> ProviderDescriptor | None:
    return _CLOSED_RELATION_LAUNCH_KEYS.get(launch_key)
