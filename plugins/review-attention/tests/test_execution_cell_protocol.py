from __future__ import annotations

import io
import struct
import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from veritrail_review._execution_cell_protocol import (  # noqa: E402
    MAX_REQUEST_PAYLOAD_BYTES,
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    FrameProtocolError,
    encode_frame,
    read_frame,
)


class AttemptEligibilityTests(unittest.TestCase):
    def test_provisional_can_be_admitted_once(self) -> None:
        eligibility = AttemptEligibility()
        self.assertEqual(eligibility.state, AttemptEligibilityState.PROVISIONAL)
        self.assertFalse(eligibility.permits_phase_commit())
        self.assertTrue(eligibility.admit())
        self.assertEqual(eligibility.state, AttemptEligibilityState.ADMITTED)
        self.assertTrue(eligibility.permits_phase_commit())
        self.assertFalse(eligibility.admit())

    def test_revocation_is_irreversible_from_every_live_state(self) -> None:
        for admitted in (False, True):
            with self.subTest(admitted=admitted):
                eligibility = AttemptEligibility()
                if admitted:
                    self.assertTrue(eligibility.admit())
                self.assertTrue(eligibility.revoke())
                self.assertEqual(
                    eligibility.state, AttemptEligibilityState.REVOKED
                )
                self.assertFalse(eligibility.permits_phase_commit())
                self.assertFalse(eligibility.admit())
                self.assertFalse(eligibility.revoke())


class FrameCodecTests(unittest.TestCase):
    def test_round_trip_uses_exact_big_endian_length_and_immediate_eof(self) -> None:
        document = {"z": [1, True], "a": "验迹"}
        frame = encode_frame(document, payload_limit=1024)
        self.assertEqual(struct.unpack(">Q", frame[:8])[0], len(frame) - 8)
        self.assertEqual(read_frame(io.BytesIO(frame), payload_limit=1024), document)

    def test_payload_limit_is_inclusive(self) -> None:
        document = {"x": "y"}
        frame = encode_frame(document, payload_limit=9)
        self.assertEqual(len(frame) - 8, 9)
        self.assertEqual(read_frame(io.BytesIO(frame), payload_limit=9), document)
        with self.assertRaises(FrameProtocolError):
            encode_frame(document, payload_limit=8)
        with self.assertRaises(FrameProtocolError):
            read_frame(io.BytesIO(frame), payload_limit=8)

    def test_declared_length_is_rejected_before_large_payload_read(self) -> None:
        class HeaderOnly(io.BytesIO):
            body_read = False

            def read(self, size: int = -1) -> bytes:
                if self.tell() >= 8:
                    self.body_read = True
                return super().read(size)

        stream = HeaderOnly(struct.pack(">Q", 1025))
        with self.assertRaises(FrameProtocolError):
            read_frame(stream, payload_limit=1024)
        self.assertFalse(stream.body_read)

    def test_truncated_duplicate_trailing_and_noncanonical_frames_fail_closed(self) -> None:
        canonical = encode_frame({"a": 1}, payload_limit=1024)
        invalid = {
            "header": canonical[:7],
            "body": canonical[:-1],
            "trailing": canonical + b"x",
            "duplicate": canonical + canonical,
            "newline": struct.pack(">Q", 8) + b'{"a":1}\n',
            "whitespace": struct.pack(">Q", 8) + b'{"a": 1}',
            "duplicate-key": struct.pack(">Q", 13) + b'{"a":1,"a":2}',
            "array": struct.pack(">Q", 2) + b"[]",
            "bom": struct.pack(">Q", 10) + b'\xef\xbb\xbf{"a":1}',
        }
        for name, value in invalid.items():
            with self.subTest(name=name), self.assertRaises(FrameProtocolError):
                read_frame(io.BytesIO(value), payload_limit=1024)

    def test_transport_limits_are_positive_and_application_capped(self) -> None:
        limits = ExecutionCellTransportSafetyLimits(1024, 2048)
        self.assertEqual(limits.request_payload_bytes, 1024)
        for request, terminal in (
            (0, 1),
            (1, 0),
            (True, 1),
            (MAX_REQUEST_PAYLOAD_BYTES + 1, 1),
        ):
            with self.subTest(request=request, terminal=terminal):
                with self.assertRaises(FrameProtocolError):
                    ExecutionCellTransportSafetyLimits(request, terminal)


if __name__ == "__main__":
    unittest.main()
