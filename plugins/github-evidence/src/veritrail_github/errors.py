from __future__ import annotations


class GitHubEvidenceError(Exception):
    """Base class for bounded, user-facing plugin failures."""


class ContractError(GitHubEvidenceError):
    """The request, policy, or normalized source data violates P1."""

    def __init__(self, errors: list[str] | tuple[str, ...]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


class TransportError(GitHubEvidenceError):
    """A transport failed without exposing request secrets or raw bodies."""


class CollectionError(GitHubEvidenceError):
    """The bounded collection could not produce a trustworthy artifact."""
