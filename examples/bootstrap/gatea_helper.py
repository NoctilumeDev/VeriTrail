from __future__ import annotations

import argparse
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            content = b"ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        if self.path == "/":
            content = b"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="icon" href="data:,">
  <title>Single application acceptance helper</title>
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
        textContent: evidence.status
      }));
      status.textContent = `evidence ready: ${label.value}`;
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
        if self.path.startswith("/data.json?"):
            content = json.dumps({"status": "ready"}, sort_keys=True).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        self.send_error(404)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    serve = subparsers.add_parser("serve")
    serve.add_argument("port", type=int)

    serve_for = subparsers.add_parser("serve-for")
    serve_for.add_argument("port", type=int)
    serve_for.add_argument("seconds", type=float)

    idle = subparsers.add_parser("idle")
    idle.add_argument("seconds", type=float)

    early_exit = subparsers.add_parser("early-exit")
    early_exit.add_argument("exit_code", type=int)

    args = parser.parse_args()
    if args.mode == "serve":
        server = ThreadingHTTPServer(("127.0.0.1", args.port), _Handler)
        print("listener-ready", flush=True)
        server.serve_forever()
    elif args.mode == "serve-for":
        server = ThreadingHTTPServer(("127.0.0.1", args.port), _Handler)
        server.timeout = 0.05
        deadline = time.monotonic() + args.seconds
        print("listener-ready", flush=True)
        try:
            while time.monotonic() < deadline:
                server.handle_request()
        finally:
            server.server_close()
    elif args.mode == "idle":
        time.sleep(args.seconds)
    else:
        return args.exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
