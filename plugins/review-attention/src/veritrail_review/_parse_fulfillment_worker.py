from __future__ import annotations

import ast
import base64
import json
import struct
import sys
from typing import Any


PROTOCOL = "veritrail-r1-parse-worker/0.1"
REFERENCE_VERSION = (3, 10, 6)
MAX_FRAME_BYTES = 64 * 1024 * 1024


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _read_frame() -> dict[str, object]:
    header = sys.stdin.buffer.read(8)
    if len(header) != 8:
        raise ValueError("missing request frame header")
    size = struct.unpack(">Q", header)[0]
    if size < 1 or size > MAX_FRAME_BYTES:
        raise ValueError("request frame is outside its limit")
    raw = sys.stdin.buffer.read(size)
    if len(raw) != size or sys.stdin.buffer.read(1) != b"":
        raise ValueError("invalid request frame")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    if not isinstance(value, dict) or _canonical_bytes(value) != raw:
        raise ValueError("request frame is not canonical")
    return value


def _write_frame(value: dict[str, object]) -> None:
    raw = _canonical_bytes(value)
    sys.stdout.buffer.write(struct.pack(">Q", len(raw)) + raw)
    sys.stdout.buffer.flush()


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


def _scalar(value: object) -> object:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return {"scalar_kind": "FLOAT", "hex": value.hex()}
    if isinstance(value, complex):
        return {
            "scalar_kind": "COMPLEX",
            "real_hex": value.real.hex(),
            "imag_hex": value.imag.hex(),
        }
    if isinstance(value, bytes):
        return {
            "scalar_kind": "BYTES",
            "base64": base64.b64encode(value).decode("ascii"),
        }
    if value is Ellipsis:
        return {"scalar_kind": "ELLIPSIS"}
    raise TypeError("unsupported AST scalar")


def _tree_value(value: object) -> object:
    if isinstance(value, ast.AST):
        return {
            "value_kind": "AST",
            "node_type": type(value).__name__,
            "fields": {
                name: _tree_value(getattr(value, name)) for name in value._fields
            },
            "attributes": {
                name: _tree_value(getattr(value, name))
                for name in value._attributes
                if hasattr(value, name)
            },
        }
    if isinstance(value, list):
        return {"value_kind": "LIST", "items": [_tree_value(item) for item in value]}
    return {"value_kind": "SCALAR", "value": _scalar(value)}


def _terminal(request: dict[str, object]) -> dict[str, object]:
    if (
        set(request) != {"protocol", "message_kind", "source_text"}
        or request.get("protocol") != PROTOCOL
        or request.get("message_kind") != "PARSE_REQUEST"
        or not isinstance(request.get("source_text"), str)
    ):
        raise ValueError("invalid parse request")
    if sys.implementation.name != "cpython" or sys.version_info[:3] != REFERENCE_VERSION:
        return {
            "protocol": PROTOCOL,
            "message_kind": "PARSE_TERMINAL",
            "lifecycle": "REFERENCE_RUNTIME_UNAVAILABLE",
            "semantic_result": None,
        }
    try:
        product = _tree_value(
            ast.parse(
                request["source_text"],
                filename="<veritrail-r1-parse>",
                mode="exec",
                type_comments=False,
                feature_version=(3, 10),
            )
        )
    except (SyntaxError, ValueError):
        semantic_result: dict[str, object] = {
            "disposition": "REJECTED",
            "reason_codes": ["PARSE_ERROR"],
            "product": None,
        }
    except Exception:
        return {
            "protocol": PROTOCOL,
            "message_kind": "PARSE_TERMINAL",
            "lifecycle": "INTERNAL_PARSER_FAILURE",
            "semantic_result": None,
        }
    else:
        semantic_result = {
            "disposition": "ACCEPTED",
            "reason_codes": [],
            "product": product,
        }
    return {
        "protocol": PROTOCOL,
        "message_kind": "PARSE_TERMINAL",
        "lifecycle": "COMPLETED",
        "semantic_result": semantic_result,
    }


def main() -> int:
    try:
        _write_frame(_terminal(_read_frame()))
        return 0
    except Exception:
        return 65


if __name__ == "__main__":
    raise SystemExit(main())
