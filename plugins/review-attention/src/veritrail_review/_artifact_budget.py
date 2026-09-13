from __future__ import annotations

import os
import shutil
from pathlib import Path, PurePosixPath

from veritrail_review.budget import BudgetContext
from veritrail_review.errors import BudgetPrimitiveError, BudgetPrimitiveFailureCode


class _StagingStopped(Exception):
    pass


class _OwnedArtifactStaging:
    """Testable create-new staging owned by one BudgetContext."""

    def __init__(self, root: Path, context: BudgetContext) -> None:
        if (
            not isinstance(context, BudgetContext)
            or not isinstance(root, Path)
            or not root.is_absolute()
        ):
            raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT)
        self._context = context
        self.path = root / ".veritrail-r1-budget-stage"
        if not context.checkpoint():
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.BUDGET_CONTEXT_NOT_RUNNING
            )
        if not root.is_dir():
            raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT)
        try:
            self.path.mkdir()
        except FileExistsError as exc:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.ARTIFACT_STAGING_FAILED
            ) from exc

    def write(self, relative_path: str, exact_bytes: bytes) -> bool:
        if not isinstance(relative_path, str) or not relative_path:
            raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT)
        relative = PurePosixPath(relative_path)
        if (
            relative.is_absolute()
            or "\\" in relative_path
            or ":" in relative_path
            or any(ord(character) < 32 for character in relative_path)
            or any(part in {"", ".", ".."} for part in relative.parts)
        ):
            raise BudgetPrimitiveError(BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT)
        try:
            owned_bytes = memoryview(exact_bytes).tobytes()
        except TypeError as exc:
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.INVALID_BUDGET_INPUT
            ) from exc
        if not self._context.reserve_artifact_bytes(owned_bytes):
            self.cleanup()
            return False
        target = self.path.joinpath(*relative.parts)
        try:
            if not self._context.checkpoint():
                self.cleanup()
                return False
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                for offset in range(0, len(owned_bytes), 65_536):
                    if not self._context.checkpoint():
                        raise _StagingStopped
                    stream.write(owned_bytes[offset : offset + 65_536])
                stream.flush()
                os.fsync(stream.fileno())
            if not self._context.checkpoint():
                raise _StagingStopped
            return True
        except _StagingStopped:
            self.cleanup()
            return False
        except (OSError, FileExistsError) as exc:
            self.cleanup()
            raise BudgetPrimitiveError(
                BudgetPrimitiveFailureCode.ARTIFACT_STAGING_FAILED
            ) from exc

    def cleanup(self) -> bool:
        """Remove only this staging resource and report its local residue fact."""

        shutil.rmtree(self.path, ignore_errors=True)
        return not self.path.exists()
