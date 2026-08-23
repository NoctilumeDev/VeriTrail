from __future__ import annotations

import os
import socket
import struct
import unittest
from unittest import mock

from veritrail.errors import SafetyError
from veritrail.windows_tcp import (
    Ipv4TcpListener,
    Ipv6TcpListener,
    _parse_ipv4_tcp_listener_table,
    _parse_ipv6_tcp_listener_table,
    assert_loopback_ports_free,
    list_tcp_listeners,
)


def _row(address: str, port: int, pid: int, *, state: int = 2) -> bytes:
    local_address = int.from_bytes(socket.inet_aton(address), byteorder="little")
    local_port = socket.htons(port)
    return struct.pack("<LLLLLL", state, local_address, local_port, 0, 0, pid)


def _ipv6_row(
    address: str, port: int, pid: int, *, scope_id: int = 0, state: int = 2
) -> bytes:
    return struct.pack(
        "<16sLL16sLLLL",
        socket.inet_pton(socket.AF_INET6, address),
        scope_id,
        socket.htons(port),
        b"\x00" * 16,
        0,
        0,
        state,
        pid,
    )


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

    def test_ipv6_parser_preserves_address_scope_port_and_owner(self) -> None:
        content = struct.pack("<L", 1) + _ipv6_row("::1", 18771, 1234, scope_id=3)
        self.assertEqual(
            (Ipv6TcpListener("::1", 18771, 1234, 3),),
            _parse_ipv6_tcp_listener_table(content),
        )

    def test_ipv6_parser_rejects_truncation_count_and_non_listener_rows(self) -> None:
        cases = [
            b"",
            struct.pack("<L", 2) + _ipv6_row("::1", 18771, 1234),
            struct.pack("<L", 1) + _ipv6_row("::1", 18771, 1234, state=5),
            struct.pack("<L", 1) + _ipv6_row("::1", 18771, 1234) + b"hidden",
        ]
        for content in cases:
            with self.subTest(size=len(content)), self.assertRaises(SafetyError):
                _parse_ipv6_tcp_listener_table(content)

    def test_free_gate_rejects_loopback_or_wildcard_owner_without_exposing_pid(self) -> None:
        listeners = (
            Ipv4TcpListener("0.0.0.0", 18771, 9999),
            Ipv4TcpListener("127.0.0.1", 18780, 8888),
        )
        with mock.patch(
            "veritrail.windows_tcp.list_tcp_listeners", return_value=listeners
        ):
            with self.assertRaisesRegex(SafetyError, "ports to be FREE") as caught:
                assert_loopback_ports_free([18771, 18772])
        self.assertNotIn("9999", str(caught.exception))

    def test_free_gate_rejects_ipv6_owner_on_a_sealed_port(self) -> None:
        listeners = (Ipv6TcpListener("::", 18771, 7777, 0),)
        with mock.patch(
            "veritrail.windows_tcp.list_tcp_listeners", return_value=listeners
        ):
            with self.assertRaisesRegex(SafetyError, "ports to be FREE") as caught:
                assert_loopback_ports_free([18771, 18772])
        self.assertNotIn("7777", str(caught.exception))

    @unittest.skipUnless(os.name == "nt" and socket.has_ipv6, "requires Windows IPv6")
    def test_combined_inventory_sees_ipv4_and_ipv6_on_the_same_port(self) -> None:
        ipv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        try:
            ipv4.bind(("127.0.0.1", 0))
            port = int(ipv4.getsockname()[1])
            ipv4.listen()
            ipv6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            try:
                ipv6.bind(("::", port))
            except OSError as exc:
                self.skipTest(f"IPv6 bind unavailable: {type(exc).__name__}")
            ipv6.listen()

            rows = [row for row in list_tcp_listeners() if row.local_port == port]
            self.assertTrue(any(isinstance(row, Ipv4TcpListener) for row in rows))
            self.assertTrue(any(isinstance(row, Ipv6TcpListener) for row in rows))
        finally:
            ipv6.close()
            ipv4.close()


if __name__ == "__main__":
    unittest.main()
