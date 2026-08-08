from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from veritrail.errors import ValidationError


class _DuplicateKeyError(ValueError):
    pass


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateKeyError(f"duplicate object key {key!r}")
        value[key] = item
    return value


def load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
        value = json.loads(content, object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError, _DuplicateKeyError) as exc:
        raise ValidationError([f"cannot read {label} {path.name}: {exc}"]) from exc
    if not isinstance(value, dict):
        raise ValidationError([f"{label} {path.name} must contain a JSON object"])
    return value
