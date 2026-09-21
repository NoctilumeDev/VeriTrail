from __future__ import annotations

import contextlib
import io
import os
import sys
from pathlib import Path


if __package__ in {None, ""}:
    source_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, os.fspath(source_root))

from veritrail_review._execution_cell_protocol import (  # noqa: E402
    FrameProtocolError,
    encode_frame,
    read_frame,
)
from veritrail_review._relation_observation_application import (  # noqa: E402
    RelationObservationApplicationError,
    canonicalize_provider_observation_outcomes,
    canonicalize_relation_observation_candidates,
    copy_relation_observation_request_for_provider,
    relation_observation_terminal_document,
    validate_relation_observation_request_document,
)
from veritrail_review._relation_observation_provider import (  # noqa: E402
    ClosedRelationObservationProviderFailed,
    ClosedRelationObservationProviderUnavailable,
    run_closed_relation_observation_provider,
)


def main(arguments: list[str] | None = None) -> int:
    values = list(sys.argv[1:] if arguments is None else arguments)
    if len(values) != 3:
        return 64
    launch_key = values[0]
    try:
        request_limit = int(values[1])
        terminal_limit = int(values[2])
        request_document = read_frame(sys.stdin.buffer, payload_limit=request_limit)
        request = validate_relation_observation_request_document(
            request_document, launch_key=launch_key
        )
    except (ValueError, FrameProtocolError, RelationObservationApplicationError):
        return 65

    terminal_kind = "COMPLETED"
    relations: list[dict[str, object]] = []
    outcomes: list[dict[str, object]] = []
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            candidates, raw_outcomes = run_closed_relation_observation_provider(
                copy_relation_observation_request_for_provider(request),
                launch_key=launch_key,
            )
        relations = canonicalize_relation_observation_candidates(
            request, candidates
        )
        outcomes = canonicalize_provider_observation_outcomes(
            request, raw_outcomes
        )
    except ClosedRelationObservationProviderUnavailable:
        terminal_kind = "PROVIDER_UNAVAILABLE"
    except ClosedRelationObservationProviderFailed:
        terminal_kind = "PROVIDER_FAILED"
    except RelationObservationApplicationError:
        terminal_kind = "NONCONFORMANT_PROVIDER_OUTPUT"
    except Exception:
        terminal_kind = "INTERNAL_DERIVATION_ERROR"

    if terminal_kind != "COMPLETED":
        relations = []
        outcomes = []
    document = relation_observation_terminal_document(
        request,
        terminal_kind=terminal_kind,
        canonical_relations=relations,
        observation_outcomes=outcomes,
    )
    try:
        frame = encode_frame(document, payload_limit=terminal_limit)
    except FrameProtocolError:
        return 66
    sys.stdout.buffer.write(frame)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
