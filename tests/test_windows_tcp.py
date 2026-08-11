from __future__ import annotations

import socket
import struct
import unittest
from unittest import mock

from veritrail.errors import SafetyError
from veritrail.windows_tcp import (
    Ipv4TcpListener,
    _parse_ipv4_tcp_listener_table,
    assert_loopback_ports_free,
)


def _row(address: str, port: int, pid: int, *, state: int = 2) -> bytes:
    local_address = int.from_bytes(socket.inet_aton(address), byteorder="little")
    local_port = socket.htons(port)
    return struct.pack("<LLLLLL", state, local_address, local_port, 0, 0, pid)


class WindowsTcpTests(unittest.TestCase):
    def test_parser_preserves_loopback_wildcard_port_and_owner(self) -> None:
        content = (
            struct.pack("<L", 2)
            + _row("127.0.0.1", 18771, 1234)
            + _row("0.0.0.0", 18772, 5678)
            + b"\x00" * 8
        )
        self.assertEqual(
            (
                Ipv4TcpListener("127.0.0.1", 18771, 1234),
                Ipv4TcpListener("0.0.0.0", 18772, 5678),
            ),
            _parse_ipv4_tcp_listener_table(content),
        )

    def test_parser_rejects_truncation_count_and_non_listener_rows(self) -> None:
        cases = [
            b"",
            struct.pack("<L", 2) + _row("127.0.0.1", 18771, 1234),
            struct.pack("<L", 1) + _row("127.0.0.1", 18771, 1234, state=5),
            struct.pack("<L", 1) + _row("127.0.0.1", 18771, 1234) + b"hidden",
        ]
        for content in cases:
            with self.subTest(size=len(content)), self.assertRaises(SafetyError):
                _parse_ipv4_tcp_listener_table(content)

    def test_free_gate_rejects_loopback_or_wildcard_owner_without_exposing_pid(self) -> None:
        listeners = (
            Ipv4TcpListener("0.0.0.0", 18771, 9999),
            Ipv4TcpListener("127.0.0.1", 18780, 8888),
        )
        with mock.patch(
            "veritrail.windows_tcp.list_ipv4_tcp_listeners", return_value=listeners
        ):
            with self.assertRaisesRegex(SafetyError, "ports to be FREE") as caught:
                assert_loopback_ports_free([18771, 18772])
        self.assertNotIn("9999", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
