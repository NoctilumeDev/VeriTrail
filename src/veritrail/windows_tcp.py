from __future__ import annotations

import ctypes
import os
import socket
import struct
from dataclasses import dataclass

from veritrail.errors import SafetyError

AF_INET = 2
TCP_TABLE_OWNER_PID_LISTENER = 3
NO_ERROR = 0
ERROR_INSUFFICIENT_BUFFER = 122
MAX_TCP_TABLE_BYTES = 16 * 1024 * 1024
ROW_STRUCT = struct.Struct("<LLLLLL")


@dataclass(frozen=True)
class Ipv4TcpListener:
    local_address: str
    local_port: int
    owning_pid: int


def _parse_ipv4_tcp_listener_table(content: bytes) -> tuple[Ipv4TcpListener, ...]:
    if len(content) < 4:
        raise SafetyError("Windows TCP listener table returned a truncated header")
    (count,) = struct.unpack_from("<L", content, 0)
    required = 4 + count * ROW_STRUCT.size
    if required > len(content) or any(content[required:]):
        raise SafetyError("Windows TCP listener table returned an inconsistent row count")
    listeners: list[Ipv4TcpListener] = []
    offset = 4
    for _ in range(count):
        state, local_address, local_port, _remote_address, _remote_port, owning_pid = (
            ROW_STRUCT.unpack_from(content, offset)
        )
        offset += ROW_STRUCT.size
        if state != 2:
            raise SafetyError("Windows TCP listener table returned a non-LISTEN row")
        port = socket.ntohs(local_port & 0xFFFF)
        if not 1 <= port <= 65535 or owning_pid <= 0:
            raise SafetyError("Windows TCP listener table returned an invalid owner row")
        address = socket.inet_ntoa(local_address.to_bytes(4, byteorder="little"))
        listeners.append(
            Ipv4TcpListener(
                local_address=address,
                local_port=port,
                owning_pid=owning_pid,
            )
        )
    return tuple(listeners)


def _read_ipv4_tcp_listener_table() -> bytes:
    if os.name != "nt":
        raise SafetyError("Windows TCP listener ownership is available only on Windows")
    iphlpapi = ctypes.WinDLL("iphlpapi", use_last_error=True)
    query = iphlpapi.GetExtendedTcpTable
    query.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_ulong),
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_int,
        ctypes.c_ulong,
    ]
    query.restype = ctypes.c_ulong

    size = ctypes.c_ulong(0)
    result = int(
        query(
            None,
            ctypes.byref(size),
            0,
            AF_INET,
            TCP_TABLE_OWNER_PID_LISTENER,
            0,
        )
    )
    if result != ERROR_INSUFFICIENT_BUFFER:
        raise SafetyError("Windows TCP listener table size query failed")
    if not 4 <= size.value <= MAX_TCP_TABLE_BYTES:
        raise SafetyError("Windows TCP listener table requested an invalid buffer size")

    for _ in range(3):
        requested = int(size.value)
        buffer = ctypes.create_string_buffer(requested)
        result = int(
            query(
                buffer,
                ctypes.byref(size),
                0,
                AF_INET,
                TCP_TABLE_OWNER_PID_LISTENER,
                0,
            )
        )
        if result == NO_ERROR:
            used = int(size.value)
            if not 4 <= used <= requested:
                raise SafetyError("Windows TCP listener table returned an invalid byte count")
            return bytes(buffer.raw[:used])
        if result != ERROR_INSUFFICIENT_BUFFER:
            raise SafetyError("Windows TCP listener table query failed")
        if not 4 <= size.value <= MAX_TCP_TABLE_BYTES:
            raise SafetyError("Windows TCP listener table retry requested an invalid buffer size")
    raise SafetyError("Windows TCP listener table changed beyond the bounded retry limit")


def list_ipv4_tcp_listeners() -> tuple[Ipv4TcpListener, ...]:
    return _parse_ipv4_tcp_listener_table(_read_ipv4_tcp_listener_table())


def assert_loopback_ports_free(ports: list[int] | tuple[int, ...]) -> None:
    requested = set(ports)
    conflicts = [
        listener
        for listener in list_ipv4_tcp_listeners()
        if listener.local_port in requested
    ]
    if conflicts:
        raise SafetyError("ProjectProfile requires both sealed loopback ports to be FREE")
