from __future__ import annotations

import argparse
import http.client
import json
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


class _Handler(BaseHTTPRequestHandler):
    dependency_status: int | None = None
    response_size = 2
    status = 200

    def do_GET(self) -> None:
        if self.path == "/health":
            content = b"x" * self.response_size
            self.send_response(self.status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        if self.path == "/":
            content = json.dumps(
                {"dependency_status": self.dependency_status},
                sort_keys=True,
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        self.send_error(404)

    def log_message(self, format: str, *args: object) -> None:
        return


def _serve(
    port: int,
    *,
    address: str,
    status: int,
    response_size: int,
    dependency_status: int | None = None,
) -> None:
    _Handler.status = status
    _Handler.response_size = response_size
    _Handler.dependency_status = dependency_status
    server = ThreadingHTTPServer((address, port), _Handler)
    print("listener-ready", flush=True)
    server.serve_forever()


def _dependency_status(origin: str) -> int:
    parsed = urlsplit(origin)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.port is None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("dependency origin must be an exact loopback HTTP origin")
    connection = http.client.HTTPConnection("127.0.0.1", parsed.port, timeout=2)
    try:
        connection.request("GET", "/health", headers={"Connection": "close"})
        response = connection.getresponse()
        response.read(4097)
        return int(response.status)
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    serve = subparsers.add_parser("serve")
    serve.add_argument("port", type=int)
    serve.add_argument("--address", default="127.0.0.1")
    serve.add_argument("--status", type=int, default=200)
    serve.add_argument("--response-size", type=int, default=2)

    child = subparsers.add_parser("child-listener")
    child.add_argument("port", type=int)

    application = subparsers.add_parser("application")
    application.add_argument("port", type=int)
    application.add_argument("dependency_origin")

    sleep = subparsers.add_parser("sleep")
    sleep.add_argument("seconds", type=float)

    early_exit = subparsers.add_parser("early-exit")
    early_exit.add_argument("exit_code", type=int)

    spam = subparsers.add_parser("spam")
    spam.add_argument("stream", choices=("stdout", "stderr"))
    spam.add_argument("byte_count", type=int)

    args = parser.parse_args()
    if args.mode == "serve":
        _serve(
            args.port,
            address=args.address,
            status=args.status,
            response_size=args.response_size,
        )
    elif args.mode == "child-listener":
        child_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "tests.fixtures.m10_service_helper",
                "serve",
                str(args.port),
            ]
        )
        print("child-created", flush=True)
        return child_process.wait()
    elif args.mode == "application":
        dependency_status = _dependency_status(args.dependency_origin)
        if dependency_status != 200:
            return 41
        _serve(
            args.port,
            address="127.0.0.1",
            status=200,
            response_size=2,
            dependency_status=dependency_status,
        )
    elif args.mode == "sleep":
        time.sleep(args.seconds)
    elif args.mode == "early-exit":
        return args.exit_code
    else:
        stream = sys.stdout.buffer if args.stream == "stdout" else sys.stderr.buffer
        stream.write(b"x" * args.byte_count)
        stream.flush()
        time.sleep(30)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
