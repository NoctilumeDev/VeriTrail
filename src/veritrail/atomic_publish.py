from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Callable

from veritrail.errors import SafetyError

WINDOWS_RETRYABLE_RENAME_ERRORS = {
    5,   # ERROR_ACCESS_DENIED
    32,  # ERROR_SHARING_VIOLATION
    33,  # ERROR_LOCK_VIOLATION
}
WINDOWS_RENAME_ATTEMPTS = 20
WINDOWS_RENAME_RETRY_SECONDS = 0.05


def publish_staged_directory(
    stage: Path,
    output: Path,
    *,
    rename: Callable[[Path, Path], None] = os.rename,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Atomically publish one same-volume staging directory without overwrite."""

    if stage.parent != output.parent:
        raise SafetyError("staging and output directories must share one parent")
    if output.exists():
        raise SafetyError(f"refusing to overwrite existing output directory: {output.name}")

    for attempt in range(WINDOWS_RENAME_ATTEMPTS):
        try:
            rename(stage, output)
            return
        except OSError as exc:
            retryable = (
                os.name == "nt"
                and getattr(exc, "winerror", None)
                in WINDOWS_RETRYABLE_RENAME_ERRORS
            )
            if not retryable:
                raise
            if output.exists():
                raise SafetyError(
                    f"refusing to overwrite existing output directory: {output.name}"
                ) from exc
            if attempt + 1 >= WINDOWS_RENAME_ATTEMPTS:
                raise
            sleep(WINDOWS_RENAME_RETRY_SECONDS)
