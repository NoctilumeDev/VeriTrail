from __future__ import annotations

import http.client
import hashlib
import json
import socket
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

from veritrail.catalog import CatalogError, build_catalog
from veritrail.local_api import create_catalog_server
from veritrail.reporting import create_bundle

from tests.support import ROOT, sealed_example_plan


def _available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


class CatalogApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.artifacts = self.base / "artifacts"
        self.artifacts.mkdir()
        self.bundle = self.artifacts / "run"
        create_bundle(
            plan=sealed_example_plan(),
            evidence_paths=[ROOT / "examples" / "minimal" / "evidence-pass.json"],
            output=self.bundle,
            run_id="api-run",
            execution_status="COMPLETED",
        )
        self.catalog = self.base / "catalog"
        build_catalog(self.artifacts, self.catalog)
        self.web = self.base / "web"
        self.web.mkdir()
        (self.web / "index.html").write_text("<!doctype html><title>Workbench</title>", encoding="utf-8")
        (self.web / "app.js").write_text("globalThis.ready = true", encoding="utf-8")
        self.port = _available_port()
        self.server = create_catalog_server(
            catalog_root=self.catalog,
            artifact_root=self.artifacts,
            web_root=self.web,
            port=self.port,
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.server_stopped = False

    def tearDown(self) -> None:
        if not self.server_stopped:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=5)
        self.temporary.cleanup()

    def _request(
        self,
        method: str,
        path: str,
        *,
        host: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        request_headers = dict(headers or {})
        if host is not None:
            request_headers["Host"] = host
        connection.request(method, path, headers=request_headers)
        response = connection.getresponse()
        body = response.read()
        result = response.status, {key.lower(): value for key, value in response.getheaders()}, body
        connection.close()
        return result

    def test_health_catalog_head_static_and_security_headers(self) -> None:
        status, headers, body = self._request("GET", "/api/v1/health")
        self.assertEqual(200, status)
        health = json.loads(body)
        self.assertEqual("READY", health["status"])
        self.assertTrue(health["read_only"])
        self.assertEqual("nosniff", headers["x-content-type-options"])
        self.assertIn("default-src 'self'", headers["content-security-policy"])
        self.assertNotIn("access-control-allow-origin", headers)

        status, headers, body = self._request("HEAD", "/api/v1/catalog")
        self.assertEqual(200, status)
        self.assertEqual(b"", body)
        self.assertGreater(int(headers["content-length"]), 0)

        status, _, body = self._request("GET", "/api/v1/catalog?page=1&page_size=1")
        self.assertEqual(200, status)
        catalog = json.loads(body)
        self.assertEqual(1, catalog["catalog"]["run_count"])
        self.assertEqual("api-run", catalog["runs"][0]["run_id"])
        self.assertNotIn(str(self.base), body.decode("utf-8"))

        status, headers, body = self._request("GET", "/")
        self.assertEqual(200, status)
        self.assertEqual(b"<!doctype html><title>Workbench</title>", body)
        self.assertTrue(headers["content-type"].startswith("text/html"))

    def test_method_query_host_and_api_fallback_are_rejected_as_json(self) -> None:
        status, headers, body = self._request("POST", "/api/v1/catalog")
        self.assertEqual(405, status)
        self.assertEqual("GET, HEAD", headers["allow"])
        self.assertEqual("METHOD_NOT_ALLOWED", json.loads(body)["error"]["code"])
        status, _, body = self._request("TRACE", "/api/v1/catalog")
        self.assertEqual(405, status)
        self.assertEqual("METHOD_NOT_ALLOWED", json.loads(body)["error"]["code"])
        status, _, body = self._request("BREW", "/api/v1/catalog")
        self.assertEqual(405, status)
        self.assertEqual("METHOD_NOT_ALLOWED", json.loads(body)["error"]["code"])

        status, _, body = self._request(
            "GET", "/api/v1/catalog", headers={"Range": "bytes=0-10"}
        )
        self.assertEqual(400, status)
        self.assertEqual("RANGE_NOT_SUPPORTED", json.loads(body)["error"]["code"])

        status, _, body = self._request("GET", "/api/v1/catalog?unknown=1")
        self.assertEqual(400, status)
        self.assertEqual("UNKNOWN_QUERY", json.loads(body)["error"]["code"])
        status, _, body = self._request("GET", "/api/v1/catalog?page_size=101")
        self.assertEqual(400, status)
        self.assertEqual("INVALID_PAGINATION", json.loads(body)["error"]["code"])

        status, _, body = self._request("GET", "/api/not-real")
        self.assertEqual(404, status)
        self.assertEqual("API_NOT_FOUND", json.loads(body)["error"]["code"])
        self.assertNotIn(b"<title>", body)

        status, _, body = self._request("GET", "/api/v1/health", host="example.invalid")
        self.assertEqual(400, status)
        self.assertEqual("HOST_REJECTED", json.loads(body)["error"]["code"])

    def test_bundle_file_rechecks_hash_and_rejects_traversal_or_missing_source(self) -> None:
        _, _, catalog_body = self._request("GET", "/api/v1/catalog")
        run = json.loads(catalog_body)["runs"][0]
        base_url = run["bundle"]["base_url"]
        status, headers, body = self._request("GET", base_url + "report.json")
        self.assertEqual(200, status)
        self.assertEqual("application/json; charset=utf-8", headers["content-type"])
        self.assertEqual("api-run", json.loads(body)["run_id"])

        status, _, body = self._request("GET", base_url + "%2e%2e/report.json")
        self.assertEqual(400, status)
        self.assertEqual("UNSAFE_PATH", json.loads(body)["error"]["code"])

        report = self.bundle / "report.json"
        original = report.read_bytes()
        changed = bytearray(original)
        changed[-2] = ord(" ") if changed[-2] != ord(" ") else ord("\t")
        report.write_bytes(changed)
        status, _, body = self._request("GET", base_url + "report.json")
        self.assertEqual(409, status)
        self.assertEqual("BUNDLE_CHANGED", json.loads(body)["error"]["code"])
        report.write_bytes(original)

        report.unlink()
        status, _, body = self._request("GET", base_url + "report.json")
        self.assertEqual(409, status)
        self.assertEqual("BUNDLE_UNAVAILABLE", json.loads(body)["error"]["code"])

    def test_service_creates_no_sqlite_sidecars(self) -> None:
        self._request("GET", "/api/v1/catalog")
        self.assertFalse(list(self.catalog.glob("catalog.sqlite3-*")))

    def test_static_hardlink_is_not_served(self) -> None:
        outside = self.base / "outside.js"
        outside.write_text("globalThis.outside = true", encoding="utf-8")
        (self.web / "linked.js").hardlink_to(outside)
        status, _, body = self._request("GET", "/linked.js")
        self.assertEqual(400, status)
        self.assertEqual("UNSAFE_PATH", json.loads(body)["error"]["code"])

    def test_unknown_database_metadata_is_rejected_even_with_updated_file_hash(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        self.server_stopped = True
        database = self.catalog / "catalog.sqlite3"
        connection = sqlite3.connect(database)
        try:
            connection.execute(
                "UPDATE catalog_meta SET value = '9.9' WHERE key = 'schema_version'"
            )
            connection.commit()
        finally:
            connection.close()
        manifest_path = self.catalog / "catalog-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["database"]["size"] = database.stat().st_size
        manifest["database"]["sha256"] = hashlib.sha256(database.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(CatalogError, "元数据"):
            create_catalog_server(
                catalog_root=self.catalog,
                artifact_root=self.artifacts,
                web_root=self.web,
                port=_available_port(),
            )


if __name__ == "__main__":
    unittest.main()
