from __future__ import annotations


class VeriTrailError(Exception):
    """Base class for expected user-facing errors."""


class ValidationError(VeriTrailError):
    """A structured input does not satisfy the public contract."""

    def __init__(self, errors: list[str] | tuple[str, ...]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


class SafetyError(VeriTrailError):
    """An operation would cross a persistence or overwrite boundary."""
