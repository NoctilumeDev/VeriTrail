from __future__ import annotations

import hashlib
import json
from typing import Any, Callable, Iterator

from veritrail_review.errors import SourceSnapshotError, SourceSnapshotFailureCode


def canonical_json_bytes(value: Any) -> bytes:
    """Return the independently implemented veritrail-json-c14n/1 encoding."""

    return bounded_canonical_json_bytes(value)


def bounded_canonical_json_bytes(
    value: Any,
    *,
    max_bytes: int | None = None,
    deadline_check: Callable[[], None] | None = None,
) -> bytes:
    chunks = bytearray()
    try:
        for chunk in _canonical_chunks(value):
            if deadline_check is not None:
                deadline_check()
            if max_bytes is not None and len(chunks) + len(chunk) > max_bytes:
                raise SourceSnapshotError(
                    SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED
                )
            chunks.extend(chunk)
        return bytes(chunks)
    except SourceSnapshotError:
        raise
    except (TypeError, ValueError, UnicodeError) as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT
        ) from exc


def bounded_semantic_digest(
    domain: str,
    payload: Any,
    *,
    max_bytes: int,
    deadline_check: Callable[[], None] | None = None,
) -> str:
    digest = hashlib.sha256()
    consumed = 0
    try:
        for chunk in _canonical_chunks({"domain": domain, "payload": payload}):
            if deadline_check is not None:
                deadline_check()
            consumed += len(chunk)
            if consumed > max_bytes:
                raise SourceSnapshotError(
                    SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED
                )
            digest.update(chunk)
        return digest.hexdigest()
    except SourceSnapshotError:
        raise
    except (TypeError, ValueError, UnicodeError) as exc:
        raise SourceSnapshotError(
            SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT
        ) from exc


def _canonical_chunks(value: Any) -> Iterator[bytes]:
    encoder = json.JSONEncoder(
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    for text in encoder.iterencode(value):
        yield text.encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def semantic_digest(domain: str, payload: Any) -> str:
    return sha256_bytes(canonical_json_bytes({"domain": domain, "payload": payload}))
