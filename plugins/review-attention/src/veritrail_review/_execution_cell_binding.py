from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class ProviderDescriptor:
    capability_id: str
    provider_id: str
    provider_version: str
    parser_id: str
    parser_version: str
    runtime_id: str
    runtime_version: str

    def document(self) -> dict[str, str]:
        return {
            "capability_id": self.capability_id,
            "provider_id": self.provider_id,
            "provider_version": self.provider_version,
            "parser_id": self.parser_id,
            "parser_version": self.parser_version,
            "runtime_id": self.runtime_id,
            "runtime_version": self.runtime_version,
        }


@dataclass(frozen=True)
class ProviderBinding:
    descriptor: ProviderDescriptor
    launch_key: str


def _descriptor(provider_id: str) -> ProviderDescriptor:
    return ProviderDescriptor(
        capability_id="python-ast",
        provider_id=provider_id,
        provider_version="0.1-test",
        parser_id="closed-deterministic-test-parser",
        parser_version="0.1-test",
        runtime_id="veritrail-review-test-runtime",
        runtime_version="0.1-test",
    )


_CLOSED_TEST_PROVIDER_DESCRIPTORS: Mapping[str, ProviderDescriptor] = (
    MappingProxyType(
        {
            "stable-a": _descriptor("closed-test-provider-a"),
            "stable-b": _descriptor("closed-test-provider-b"),
            "empty": _descriptor("closed-test-provider-empty"),
            "failed": _descriptor("closed-test-provider-failed"),
            "unavailable": _descriptor("closed-test-provider-unavailable"),
            "bad-candidate": _descriptor("closed-test-provider-bad-candidate"),
            "no-envelope": _descriptor("closed-test-provider-no-envelope"),
            "abnormal-exit": _descriptor("closed-test-provider-abnormal-exit"),
            "trailing-terminal": _descriptor("closed-test-provider-trailing"),
            "partial-terminal": _descriptor("closed-test-provider-partial"),
            "duplicate-terminal": _descriptor("closed-test-provider-duplicate"),
            "terminal-then-sleep": _descriptor("closed-test-provider-terminal-sleep"),
            "facts-on-failure": _descriptor("closed-test-provider-facts-on-failure"),
            "self-reporting-candidate": _descriptor(
                "closed-test-provider-self-reporting"
            ),
            "memory": _descriptor("closed-test-provider-memory"),
            "slow": _descriptor("closed-test-provider-slow"),
        }
    )
)


def closed_test_binding(launch_key: str) -> ProviderBinding:
    """Internal conformance control; deliberately absent from the package API."""

    return ProviderBinding(_CLOSED_TEST_PROVIDER_DESCRIPTORS[launch_key], launch_key)


def binding_matches_closed_allow_list(binding: ProviderBinding) -> bool:
    if not isinstance(binding, ProviderBinding) or not isinstance(
        binding.descriptor, ProviderDescriptor
    ):
        return False
    expected = _CLOSED_TEST_PROVIDER_DESCRIPTORS.get(binding.launch_key)
    return expected is not None and expected == binding.descriptor


def descriptor_for_launch_key(launch_key: str) -> ProviderDescriptor | None:
    return _CLOSED_TEST_PROVIDER_DESCRIPTORS.get(launch_key)
