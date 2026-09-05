"""Independent read-only GitHub evidence collector for VeriTrail."""

from veritrail_github.collector import CollectionResult, GitHubCollector
from veritrail_github.conformance import verify_github_evidence
from veritrail_github.contracts import (
    DEFAULT_COLLECTOR_POLICY,
    derive_observation_request,
    facts_digest,
    validate_observation_request,
)
from veritrail_github.publisher import publish_evidence
from veritrail_github.transport import UrllibTransport

__all__ = [
    "CollectionResult",
    "DEFAULT_COLLECTOR_POLICY",
    "GitHubCollector",
    "UrllibTransport",
    "derive_observation_request",
    "facts_digest",
    "publish_evidence",
    "validate_observation_request",
    "verify_github_evidence",
]

__version__ = "0.1.0"
