from __future__ import annotations

import contextlib
import io
import os
import sys
from pathlib import Path


if __package__ in {None, ""}:
    source_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, os.fspath(source_root))

from veritrail_review import (  # noqa: E402
    _source_operation_relation_observation_application as _app,
)
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    FrameProtocolError,
    encode_frame,
    read_frame,
)
from veritrail_review._relation_observation_provider import (  # noqa: E402
    ClosedRelationObservationProviderFailed,
    ClosedRelationObservationProviderUnavailable,
    run_closed_relation_observation_provider,
)


def main(arguments: list[str] | None = None) -> int:
    """Serve only corrected observation input; no controller authority."""

    values = list(sys.argv[1:] if arguments is None else arguments)
    if len(values) != 3:
        return 64
    launch_key = values[0]
    try:
        request_limit = int(values[1])
        terminal_limit = int(values[2])
        request_document = read_frame(sys.stdin.buffer, payload_limit=request_limit)
        request = (
            _app.validate_relation_observation_source_operation_request_document(
                request_document, launch_key=launch_key
            )
        )
    except (
        ValueError,
        FrameProtocolError,
        _app.RelationObservationSourceOperationProtocolError,
    ):
        return 65

    terminal_kind = "COMPLETED"
    relations: list[dict[str, object]] = []
    outcomes: list[dict[str, object]] = []
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            candidates, raw_outcomes = run_closed_relation_observation_provider(
                _app.copy_relation_observation_source_operation_request_for_provider(
                    request
                ),
                launch_key=launch_key,
            )
        relations = (
            _app.canonicalize_relation_observation_source_operation_candidates(
                request, candidates
            )
        )
        outcomes = (
            _app.canonicalize_relation_observation_source_operation_outcomes(
                request, raw_outcomes
            )
        )
    except ClosedRelationObservationProviderUnavailable:
        terminal_kind = "PROVIDER_UNAVAILABLE"
    except ClosedRelationObservationProviderFailed:
        terminal_kind = "PROVIDER_FAILED"
    except _app.RelationObservationSourceOperationProtocolError:
        terminal_kind = "NONCONFORMANT_PROVIDER_OUTPUT"
    except Exception:
        terminal_kind = "INTERNAL_DERIVATION_ERROR"

    if terminal_kind != "COMPLETED":
        relations = []
        outcomes = []
    document = _app.relation_observation_source_operation_terminal_document(
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
