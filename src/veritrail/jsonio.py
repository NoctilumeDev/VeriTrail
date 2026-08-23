from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

from veritrail.errors import ValidationError


class _DuplicateKeyError(ValueError):
    pass


DEFAULT_JSON_MAX_BYTES = 1024 * 1024
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def read_stable_bytes(path: Path, *, label: str, max_bytes: int) -> bytes:
    """Own one bounded, identity-stable ordinary-file snapshot."""

    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive")
    identity = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_nlink")
    try:
        before = os.lstat(path)
        if (
            path.is_symlink()
            or _is_reparse(before)
            or not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
        ):
            raise OSError("unsafe file node")
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            content = handle.read(max_bytes + 1)
        after = os.lstat(path)
    except OSError as exc:
        raise ValidationError([f"cannot read {label} {path.name}: unsafe or unavailable file"]) from exc
    if len(content) > max_bytes or opened.st_size > max_bytes:
        raise ValidationError(
            [f"cannot read {label} {path.name}: limit is {max_bytes} bytes"]
        )
    if (
        _is_reparse(after)
        or not stat.S_ISREG(opened.st_mode)
        or not stat.S_ISREG(after.st_mode)
        or opened.st_nlink != 1
        or after.st_nlink != 1
        or any(getattr(before, field) != getattr(opened, field) for field in identity)
        or any(getattr(opened, field) != getattr(after, field) for field in identity)
        or len(content) != opened.st_size
    ):
        raise ValidationError([f"cannot read {label} {path.name}: file changed during read"])
    return content


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateKeyError(f"duplicate object key {key!r}")
        value[key] = item
    return value


def load_json_object(
    path: Path, *, label: str, max_bytes: int = DEFAULT_JSON_MAX_BYTES
) -> dict[str, Any]:
    content = read_stable_bytes(path, label=label, max_bytes=max_bytes)
    return load_json_object_bytes(content, label=label, name=path.name)


def load_json_object_bytes(
    content: bytes, *, label: str, name: str
) -> dict[str, Any]:
    """Parse one already-owned byte snapshot without reopening a mutable path."""

    try:
        value = json.loads(
            content.decode("utf-8"), object_pairs_hook=_unique_object
        )
    except (UnicodeError, json.JSONDecodeError, _DuplicateKeyError) as exc:
        raise ValidationError([f"cannot read {label} {name}: {exc}"]) from exc
    if not isinstance(value, dict):
        raise ValidationError([f"{label} {name} must contain a JSON object"])
    return value
