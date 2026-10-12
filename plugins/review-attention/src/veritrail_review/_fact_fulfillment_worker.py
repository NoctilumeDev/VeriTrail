from __future__ import annotations

import contextlib
import io
import os
import sys
from pathlib import Path


if __package__ in {None, ""}:
    sys.path.insert(0, os.fspath(Path(__file__).resolve().parents[1]))

from veritrail_review._execution_cell_protocol import (  # noqa: E402
    FrameProtocolError,
    encode_frame,
    read_frame,
)
from veritrail_review._fact_fulfillment_protocol import (  # noqa: E402
    ProductFactProtocolError,
    product_candidate_records,
    terminal_document,
    validate_request,
)


def main(arguments: list[str] | None = None) -> int:
    """One closed product-only consumer; no source loader or parser invocation."""
    args = list(sys.argv[1:] if arguments is None else arguments)
    if len(args) != 3:
        return 64
    launch_key = args[0]
    try:
        request_limit, terminal_limit = int(args[1]), int(args[2])
        request = read_frame(sys.stdin.buffer, payload_limit=request_limit)
        validate_request(request, launch_key=launch_key)
    except (ValueError, FrameProtocolError, ProductFactProtocolError):
        return 65
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            records = product_candidate_records(request)
        terminal = terminal_document(
            request, terminal_kind="COMPLETED", records=records
        )
        frame = encode_frame(terminal, payload_limit=terminal_limit)
    except Exception:
        return 66
    sys.stdout.buffer.write(frame)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
