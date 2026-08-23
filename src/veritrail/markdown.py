from __future__ import annotations

import json
import re
from typing import Any


_BACKTICK_RUN = re.compile(r"`+")
_AUTOLINK_PROTOCOL = re.compile(r"\bhttps?://", re.IGNORECASE)
_AUTOLINK_WWW = re.compile(r"\bwww\.", re.IGNORECASE)
_AUTOLINK_BREAK = "\u2060"


def _neutralize_gfm_autolinks(value: str) -> str:
    value = _AUTOLINK_PROTOCOL.sub(
        lambda match: f"{match.group(0)[:-2]}{_AUTOLINK_BREAK}//", value
    )
    value = _AUTOLINK_WWW.sub(
        lambda match: f"{match.group(0)[:-1]}{_AUTOLINK_BREAK}.", value
    )
    return value.replace("@", f"{_AUTOLINK_BREAK}@")


def markdown_text(value: Any) -> str:
    """Render imported text without allowing it to create Markdown structure."""

    rendered = str(value).replace("\r", " ").replace("\n", " ")
    rendered = _neutralize_gfm_autolinks(rendered)
    rendered = rendered.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for character in "\\`*_{}[]()#+-.!|":
        rendered = rendered.replace(character, f"\\{character}")
    return rendered


def markdown_json(value: Any) -> str:
    return markdown_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )


def markdown_code(value: Any, *, json_value: bool = False) -> str:
    """Create an inert CommonMark inline-code span with a safe delimiter."""

    rendered = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        if json_value
        else str(value)
    )
    rendered = rendered.replace("\r", " ").replace("\n", " ")
    longest = max((len(match.group(0)) for match in _BACKTICK_RUN.finditer(rendered)), default=0)
    delimiter = "`" * (longest + 1)
    if rendered.startswith(("`", " ")) or rendered.endswith(("`", " ")):
        rendered = f" {rendered} "
    return f"{delimiter}{rendered}{delimiter}"
