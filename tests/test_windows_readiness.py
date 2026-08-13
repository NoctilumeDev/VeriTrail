from __future__ import annotations

import unittest
from unittest.mock import patch

from veritrail.windows_readiness import probe_owned_http_readiness
from veritrail.windows_tcp import Ipv4TcpListener


class _Response:
    status = 200

    def read(self, _limit: int) -> bytes:
        return b"ready"


class _Connection:
    def __init__(self, *_args, **_kwargs) -> None:
        self.closed = False

    def request(self, *_args, **_kwargs) -> None:
        return None

    def getresponse(self) -> _Response:
        return _Response()

    def close(self) -> None:
        self.closed = True


class _Session:
    port = 18779

    def stream_error_type(self) -> None:
        return None

    def root_exit_code(self) -> None:
        return None

    def active_process_ids(self) -> frozenset[int]:
        return frozenset({41})


READINESS = {
    "path": "/health",
    "expected_status": 200,
    "attempt_timeout_ms": 100,
    "total_timeout_ms": 500,
    "interval_ms": 1,
    "consecutive_successes": 1,
    "max_response_bytes": 64,
}


class WindowsReadinessTests(unittest.TestCase):
    @patch("veritrail.windows_readiness.http.client.HTTPConnection", _Connection)
    def test_ready_response_requires_the_same_owned_listener_after_response(self) -> None:
        owned = Ipv4TcpListener("127.0.0.1", _Session.port, 41)
        external = Ipv4TcpListener("127.0.0.1", _Session.port, 99)
        with patch(
            "veritrail.windows_readiness.list_ipv4_tcp_listeners",
            side_effect=[(owned,), (external,)],
        ):
            result = probe_owned_http_readiness(_Session(), READINESS)

        self.assertFalse(result.ready)
        self.assertEqual("LISTENER_OWNERSHIP_MISMATCH", result.error_type)
        self.assertEqual("LISTENER_OWNERSHIP_CHANGED", result.attempts[0].result)
        self.assertFalse(result.attempts[0].listener_owner_in_job)

    @patch("veritrail.windows_readiness.http.client.HTTPConnection", _Connection)
    def test_stable_owned_listener_can_become_ready(self) -> None:
        owned = Ipv4TcpListener("127.0.0.1", _Session.port, 41)
        with patch(
            "veritrail.windows_readiness.list_ipv4_tcp_listeners",
            side_effect=[(owned,), (owned,)],
        ):
            result = probe_owned_http_readiness(_Session(), READINESS)

        self.assertTrue(result.ready)
        self.assertIsNone(result.error_type)
        self.assertEqual("SUCCESS", result.attempts[0].result)
        self.assertTrue(result.attempts[0].listener_owner_in_job)


if __name__ == "__main__":
    unittest.main()
