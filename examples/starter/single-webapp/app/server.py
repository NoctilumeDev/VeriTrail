from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


FACT_PATH = Path(__file__).with_name("fact.json")


def _load_status() -> str:
    document = json.loads(FACT_PATH.read_text(encoding="utf-8"))
    status = document.get("status")
    if not isinstance(status, str) or not status:
        raise ValueError("fact.json must contain a non-empty status string")
    return status


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlsplit(self.path)
        if parsed.path == "/health":
            self._send(b"ok", "text/plain; charset=utf-8")
            return
        if parsed.path == "/data.json":
            label = parse_qs(parsed.query).get("run", [""])[0]
            payload = json.dumps(
                {"label": label, "status": _load_status()},
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
            self._send(payload, "application/json; charset=utf-8")
            return
        if parsed.path == "/":
            self._send(_PAGE, "text/html; charset=utf-8")
            return
        self.send_error(404)

    def _send(self, content: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format: str, *args: object) -> None:
        return


_PAGE = b"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="icon" href="data:,">
  <title>VeriTrail Starter Golden Path</title>
  <style>
    :root { color-scheme: light dark; font: 16px/1.5 system-ui, sans-serif; }
    body { margin: 0; min-height: 100vh; display: grid; place-items: center; background: #102225; }
    main { box-sizing: border-box; width: min(92vw, 720px); padding: 32px; border: 1px solid #6e9796; border-radius: 18px; background: #f4efe4; color: #172728; }
    label { display: grid; gap: 8px; }
    input, button { box-sizing: border-box; min-height: 44px; padding: 10px 12px; font: inherit; }
    button { margin-top: 16px; cursor: pointer; }
  </style>
</head>
<body>
  <main>
    <h1 data-testid="starter-title">VeriTrail Starter Golden Path</h1>
    <label>Run label <input data-testid="run-label" autocomplete="off"></label>
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
      list.replaceChildren(Object.assign(document.createElement('li'), { textContent: evidence.status }));
      status.textContent = `evidence ${evidence.status}: ${evidence.label}`;
    });
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    serve = subparsers.add_parser("serve")
    serve.add_argument("port", type=int)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), _Handler)
    print("starter-golden-listener-ready", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
