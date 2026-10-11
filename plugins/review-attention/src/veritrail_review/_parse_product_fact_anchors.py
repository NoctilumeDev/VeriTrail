from __future__ import annotations

from typing import Mapping

from veritrail_review._parse_product_fact_protocol import (
    ProductFactProtocolError,
    scalar,
    walk_product,
)


def product_byte_anchors(
    product: Mapping[str, object], raw: bytes, *, encoding: str
) -> dict[str, dict[str, int]]:
    """Application-only location translation. The worker never receives raw bytes."""
    if type(raw) is not bytes or encoding not in {"UTF-8", "UTF-8-SIG"}:
        raise ProductFactProtocolError("invalid exact anchor operands")
    prefix = 3 if encoding == "UTF-8-SIG" else 0
    if prefix and not raw.startswith(b"\xef\xbb\xbf"):
        raise ProductFactProtocolError("missing frozen BOM")
    raw[prefix:].decode("utf-8", errors="strict")
    starts = [prefix]
    ends: list[int] = []
    index = prefix
    while index < len(raw):
        if raw[index] in {10, 13}:
            ends.append(index)
            width = 2 if raw[index : index + 2] == b"\r\n" else 1
            index += width
            starts.append(index)
        else:
            index += 1
    ends.append(len(raw))

    def offset(line: object, column: object) -> int:
        if (
            type(line) is not int
            or type(column) is not int
            or not 1 <= line <= len(starts)
            or column < 0
        ):
            raise ProductFactProtocolError("invalid product source location")
        value = starts[line - 1] + column
        if value > ends[line - 1]:
            raise ProductFactProtocolError("product column crosses its raw line")
        # CPython columns count UTF-8 bytes. Reject a column inside a multibyte sequence.
        raw[starts[line - 1] : value].decode("utf-8", errors="strict")
        return value

    result: dict[str, dict[str, int]] = {}
    names = ("lineno", "col_offset", "end_lineno", "end_col_offset")
    for path, node in walk_product(product):
        attributes = node["attributes"]
        present = [name in attributes for name in names]
        if not any(present):
            continue
        if not all(present):
            raise ProductFactProtocolError("incomplete product source location")
        line, column, end_line, end_column = (
            scalar(attributes[name]) for name in names
        )
        start = offset(line, column)
        end = offset(end_line, end_column)
        if not 0 <= start <= end <= len(raw):
            raise ProductFactProtocolError(
                "product source location is outside exact bytes"
            )
        result[path] = {"start_byte": start, "end_byte": end}
    return result
