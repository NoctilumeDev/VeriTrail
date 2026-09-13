from __future__ import annotations

import contextlib
import io
import os
import sys
from pathlib import Path


if __package__ in {None, ""}:
    # The controller launches this exact product-owned file under ``-I``.
    # Adding its sibling source root locates the application package only;
    # Provider selection remains the closed launch-key table.
    source_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, os.fspath(source_root))

from veritrail_review._execution_cell_application import (  # noqa: E402
    ApplicationProtocolError,
    ClosedProviderFailed,
    ClosedProviderUnavailable,
    canonicalize_candidates,
    run_closed_test_provider,
    terminal_document,
    validate_request_document,
)
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    FrameProtocolError,
    encode_frame,
    read_frame,
)


def main(arguments: list[str] | None = None) -> int:
    values = list(sys.argv[1:] if arguments is None else arguments)
    if len(values) != 3:
        return 64
    launch_key = values[0]
    try:
        request_limit = int(values[1])
        terminal_limit = int(values[2])
        request_document = read_frame(
            sys.stdin.buffer, payload_limit=request_limit
        )
        request = validate_request_document(request_document, launch_key=launch_key)
    except (ValueError, FrameProtocolError, ApplicationProtocolError):
        return 65

    if launch_key == "no-envelope":
        return 0
    if launch_key == "abnormal-exit":
        os._exit(23)

    terminal_kind = "COMPLETED"
    facts: list[dict[str, object]] = []
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            candidates = run_closed_test_provider(request, launch_key=launch_key)
        facts = canonicalize_candidates(request, candidates)
    except ClosedProviderUnavailable:
        terminal_kind = "PROVIDER_UNAVAILABLE"
    except ClosedProviderFailed:
        terminal_kind = "PROVIDER_FAILED"
    except ApplicationProtocolError:
        terminal_kind = "NONCONFORMANT_PROVIDER_OUTPUT"
    except Exception:
        terminal_kind = "INTERNAL_DERIVATION_ERROR"

    if terminal_kind != "COMPLETED":
        facts = []
    document = terminal_document(
        request, terminal_kind=terminal_kind, canonical_facts=facts
    )
    if launch_key == "facts-on-failure":
        document["terminal_kind"] = "PROVIDER_FAILED"
    try:
        frame = encode_frame(document, payload_limit=terminal_limit)
    except FrameProtocolError:
        return 66
    if launch_key == "trailing-terminal":
        frame += b"x"
    elif launch_key == "partial-terminal":
        frame = frame[:-1]
    elif launch_key == "duplicate-terminal":
        frame += frame
    sys.stdout.buffer.write(frame)
    sys.stdout.buffer.flush()
    if launch_key == "terminal-then-sleep":
        __import__("time").sleep(60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
