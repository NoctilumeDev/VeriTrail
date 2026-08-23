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
    browser_application = False
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
            if self.browser_application:
                content = b"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="icon" href="data:,">
  <title>M10 browser fixture</title>
  <style>
    body { margin: 0; padding: 24px; font: 16px sans-serif; }
    main { width: min(100%, 720px); margin: 0 auto; }
    input, button { box-sizing: border-box; min-height: 40px; }
  </style>
</head>
<body>
  <main>
    <label>Run <input data-testid="run-label" autocomplete="off"></label>
    <button data-testid="load-evidence" type="button">Load evidence</button>
    <button data-testid="open-popup" type="button">Open popup</button>
    <p data-testid="status">waiting</p>
    <ul data-testid="evidence-list"></ul>
  </main>
  <script>
    const label = document.querySelector('[data-testid="run-label"]');
    const status = document.querySelector('[data-testid="status"]');
    const list = document.querySelector('[data-testid="evidence-list"]');
    document.querySelector('[data-testid="load-evidence"]').addEventListener('click', async () => {
      const response = await fetch(`/data.json?run=${encodeURIComponent(label.value)}`);
      const evidence = await response.json();
      list.replaceChildren(Object.assign(document.createElement('li'), {
        textContent: `dependency: ${evidence.dependency_status}`
      }));
      status.textContent = `evidence ready: ${label.value}`;
    });
    document.querySelector('[data-testid="open-popup"]').addEventListener('click', () => {
      window.open('/popup', '_blank');
    });
  </script>
</body>
</html>
"""
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
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
        if self.browser_application and self.path.startswith("/data.json?"):
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
        if self.browser_application and self.path == "/popup":
            content = b"<!doctype html><title>Unexpected popup</title><p>popup</p>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
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
    browser_application: bool = False,
) -> None:
    _Handler.status = status
    _Handler.response_size = response_size
    _Handler.dependency_status = dependency_status
    _Handler.browser_application = browser_application
    server = ThreadingHTTPServer((address, port), _Handler)
    print("listener-ready", flush=True)
    server.serve_forever()


def _serve_for(port: int, seconds: float) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    server.timeout = 0.05
    deadline = time.monotonic() + seconds
    print("listener-ready", flush=True)
    try:
        while time.monotonic() < deadline:
            server.handle_request()
    finally:
        server.server_close()


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

    serve_for = subparsers.add_parser("serve-for")
    serve_for.add_argument("port", type=int)
    serve_for.add_argument("seconds", type=float)

    child = subparsers.add_parser("child-listener")
    child.add_argument("port", type=int)

    application = subparsers.add_parser("application")
    application.add_argument("port", type=int)
    application.add_argument("dependency_origin")

    browser_application = subparsers.add_parser("browser-application")
    browser_application.add_argument("port", type=int)
    browser_application.add_argument("dependency_origin")

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
    elif args.mode == "serve-for":
        _serve_for(args.port, args.seconds)
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
    elif args.mode in {"application", "browser-application"}:
        dependency_status = _dependency_status(args.dependency_origin)
        if dependency_status != 200:
            return 41
        _serve(
            args.port,
            address="127.0.0.1",
            status=200,
            response_size=2,
            dependency_status=dependency_status,
            browser_application=args.mode == "browser-application",
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
