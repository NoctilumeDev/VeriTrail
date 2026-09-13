from __future__ import annotations

import json
import struct
from dataclasses import dataclass
from enum import Enum
from threading import Lock
from typing import BinaryIO, Mapping

from veritrail_review.canonical import canonical_json_bytes


FRAME_HEADER_BYTES = 8
MAX_REQUEST_PAYLOAD_BYTES = 64 * 1024 * 1024
MAX_TERMINAL_PAYLOAD_BYTES = 16 * 1024 * 1024


class FrameProtocolError(ValueError):
    """An internal execution-cell channel violated the frozen frame protocol."""


@dataclass(frozen=True)
class ExecutionCellTransportSafetyLimits:
    request_payload_bytes: int
    terminal_payload_bytes: int

    def __post_init__(self) -> None:
        if (
            type(self.request_payload_bytes) is not int
            or type(self.terminal_payload_bytes) is not int
            or self.request_payload_bytes <= 0
            or self.terminal_payload_bytes <= 0
            or self.request_payload_bytes > MAX_REQUEST_PAYLOAD_BYTES
            or self.terminal_payload_bytes > MAX_TERMINAL_PAYLOAD_BYTES
        ):
            raise FrameProtocolError("invalid execution-cell transport limits")


class AttemptEligibilityState(str, Enum):
    PROVISIONAL = "PROVISIONAL"
    ADMITTED = "ADMITTED"
    REVOKED = "REVOKED"


class AttemptEligibility:
    """Controller-owned, irreversible attempt admission gate."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._state = AttemptEligibilityState.PROVISIONAL

    @property
    def state(self) -> AttemptEligibilityState:
        with self._lock:
            return self._state

    def admit(self) -> bool:
        with self._lock:
            if self._state is not AttemptEligibilityState.PROVISIONAL:
                return False
            self._state = AttemptEligibilityState.ADMITTED
            return True

    def revoke(self) -> bool:
        with self._lock:
            changed = self._state is not AttemptEligibilityState.REVOKED
            self._state = AttemptEligibilityState.REVOKED
            return changed

    def permits_phase_commit(self) -> bool:
        with self._lock:
            return self._state is AttemptEligibilityState.ADMITTED


def encode_frame(document: Mapping[str, object], *, payload_limit: int) -> bytes:
    limit = _validate_payload_limit(payload_limit)
    if not isinstance(document, Mapping):
        raise FrameProtocolError("frame payload must be a JSON object")
    try:
        payload = canonical_json_bytes(dict(document))
    except Exception as exc:
        raise FrameProtocolError("frame payload is not canonicalizable") from exc
    if not payload or len(payload) > limit:
        raise FrameProtocolError("frame payload exceeds its inclusive limit")
    return struct.pack(">Q", len(payload)) + payload


def read_frame(stream: BinaryIO, *, payload_limit: int) -> dict[str, object]:
    limit = _validate_payload_limit(payload_limit)
    header = _read_exact(stream, FRAME_HEADER_BYTES)
    if len(header) != FRAME_HEADER_BYTES:
        raise FrameProtocolError("truncated frame header")
    declared_length = struct.unpack(">Q", header)[0]
    if declared_length < 1 or declared_length > limit:
        raise FrameProtocolError("declared frame length is outside its limit")
    payload = _read_exact(stream, declared_length)
    if len(payload) != declared_length:
        raise FrameProtocolError("truncated frame payload")
    if stream.read(1) != b"":
        raise FrameProtocolError("trailing or duplicate frame bytes")
    try:
        text = payload.decode("utf-8", errors="strict")
        document = json.loads(text, object_pairs_hook=_unique_object)
    except (UnicodeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise FrameProtocolError("frame payload is not one strict JSON object") from exc
    if not isinstance(document, dict):
        raise FrameProtocolError("frame payload must be a JSON object")
    try:
        canonical = canonical_json_bytes(document)
    except Exception as exc:
        raise FrameProtocolError("frame payload is not canonicalizable") from exc
    if canonical != payload:
        raise FrameProtocolError("frame payload bytes are not canonical")
    return document


def _validate_payload_limit(value: int) -> int:
    if type(value) is not int or value <= 0 or value > MAX_REQUEST_PAYLOAD_BYTES:
        raise FrameProtocolError("invalid frame payload limit")
    return value


def _read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < size:
        chunk = stream.read(size - len(chunks))
        if not chunk:
            break
        chunks.extend(chunk)
    return bytes(chunks)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object member")
        result[key] = value
    return result
