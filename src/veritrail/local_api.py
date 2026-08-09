from __future__ import annotations

import json
import mimetypes
import os
import re
import socket
import sqlite3
import stat
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

from veritrail.catalog import (
    CATALOG_API_VERSION,
    CATALOG_SCHEMA_VERSION,
    CatalogError,
    _is_relative_to,
    _is_reparse,
    _root_binding,
    _sha256_file,
    load_catalog_manifest,
    open_catalog_readonly,
)
from veritrail.canonical import canonical_json_bytes

MAX_REQUEST_PATH = 2048
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 50
MAX_ISSUES_IN_RESPONSE = 100
MAX_STATIC_FILE_BYTES = 16 * 1024 * 1024
SOCKET_TIMEOUT_SECONDS = 5
MAX_CONNECTIONS = 8
CATALOG_RUN_ID_PATTERN = re.compile(r"^cr_[0-9a-f]{24}$")
CSP = (
    "default-src 'self'; img-src 'self' blob: data:; script-src 'self'; "
    "style-src 'self'; font-src 'none'; connect-src 'self'; object-src 'none'; "
    "base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
)
CONTENT_TYPES = {
    ".json": "application/json; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def _safe_relative_path(value: str) -> str:
    if (
        not value
        or "\\" in value
        or "\0" in value
        or value.startswith("/")
        or re.match(r"^[A-Za-z]:", value)
    ):
        raise ValueError("unsafe path")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("unsafe path")
    return "/".join(parts)


def _safe_file(root: Path, relative_path: str, *, max_bytes: int) -> tuple[Path, os.stat_result]:
    normalized = _safe_relative_path(relative_path)
    current = root
    for part in normalized.split("/"):
        current = current / part
        metadata = os.lstat(current)
        if current.is_symlink() or _is_reparse(metadata):
            raise ValueError("unsafe node")
    resolved = current.resolve(strict=True)
    resolved_root = root.resolve(strict=True)
    if not _is_relative_to(resolved, resolved_root):
        raise ValueError("root escape")
    metadata = os.lstat(current)
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
        raise ValueError("unsafe file")
    if metadata.st_size > max_bytes:
        raise ValueError("file too large")
    return current, metadata


class CatalogApplication:
    def __init__(self, catalog_root: Path, artifact_root: Path, web_root: Path) -> None:
        self.catalog_root = catalog_root.absolute()
        self.artifact_root = artifact_root.absolute()
        self.web_root = web_root.absolute()
        self.manifest = load_catalog_manifest(self.catalog_root)
        self._validate_roots()
        self._validate_database()

    def _validate_roots(self) -> None:
        for root, code, message in (
            (
                self.artifact_root,
                "UNSAFE_ARTIFACT_ROOT",
                "Artifact 根目录必须是普通本地目录。",
            ),
            (self.web_root, "UNSAFE_WEB_ROOT", "Workbench 生产构建目录不可用。"),
        ):
            try:
                metadata = os.lstat(root)
            except OSError as exc:
                raise CatalogError(code, message) from exc
            if root.is_symlink() or _is_reparse(metadata) or not stat.S_ISDIR(metadata.st_mode):
                raise CatalogError(code, message)
        if self.manifest.get("artifact_root_binding") != _root_binding(self.artifact_root):
            raise CatalogError("ARTIFACT_ROOT_MISMATCH", "Artifact 根目录与 Catalog 快照不匹配。")
        try:
            _safe_file(self.web_root, "index.html", max_bytes=MAX_STATIC_FILE_BYTES)
        except (OSError, ValueError) as exc:
            raise CatalogError("WEB_BUILD_INVALID", "Workbench 生产构建缺少安全的入口文件。") from exc

    def _validate_database(self) -> None:
        try:
            connection = open_catalog_readonly(self.catalog_root)
        except (OSError, sqlite3.Error) as exc:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库无法只读打开。") from exc
        try:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()
            if integrity is None or integrity[0] != "ok":
                raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库完整性检查失败。")
            metadata = dict(connection.execute("SELECT key, value FROM catalog_meta"))
        except sqlite3.Error as exc:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库结构无效。") from exc
        finally:
            connection.close()
        expected = {
            "schema_version": CATALOG_SCHEMA_VERSION,
            "api_version": CATALOG_API_VERSION,
            "catalog_id": self.manifest.get("catalog_id"),
            "bundle_set_sha256": self.manifest.get("bundle_set_sha256"),
            "artifact_root_binding": self.manifest.get("artifact_root_binding"),
        }
        if any(metadata.get(key) != value for key, value in expected.items()):
            raise CatalogError("CATALOG_MANIFEST_MISMATCH", "Catalog Manifest 与数据库元数据不一致。")

    def connection(self) -> sqlite3.Connection:
        return open_catalog_readonly(self.catalog_root)

    def health(self) -> dict[str, Any]:
        return {
            "schema_version": CATALOG_API_VERSION,
            "service": "veritrail-local-catalog",
            "api_version": CATALOG_API_VERSION,
            "catalog_schema_version": CATALOG_SCHEMA_VERSION,
            "catalog_id": self.manifest["catalog_id"],
            "read_only": True,
            "status": "READY",
        }

    def catalog(self, page: int, page_size: int) -> dict[str, Any]:
        offset = (page - 1) * page_size
        connection = self.connection()
        try:
            rows = connection.execute(
                """
                SELECT catalog_run_id, run_id, created_at, execution_status, verdict,
                       plan_id, plan_version, plan_sha256, bundle_sha256,
                       file_count, total_bytes, duplicate_count
                FROM catalog_runs
                ORDER BY created_at DESC, run_id ASC, catalog_run_id ASC
                LIMIT ? OFFSET ?
                """,
                (page_size, offset),
            ).fetchall()
            issues = connection.execute(
                """
                SELECT issue_id, code, candidate_id, run_id, bundle_digests_json, occurrence_count
                FROM catalog_issues
                ORDER BY code ASC, run_id ASC, issue_id ASC
                LIMIT ?
                """,
                (MAX_ISSUES_IN_RESPONSE,),
            ).fetchall()
        finally:
            connection.close()
        total_items = int(self.manifest["run_count"])
        total_pages = (total_items + page_size - 1) // page_size
        return {
            "schema_version": CATALOG_API_VERSION,
            "catalog": {
                "catalog_id": self.manifest["catalog_id"],
                "build_status": self.manifest["build_status"],
                "read_only": True,
                "run_count": total_items,
                "issue_count": self.manifest["issue_count"],
                "duplicate_count": self.manifest["duplicate_count"],
            },
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
            },
            "runs": [
                {
                    "catalog_run_id": row["catalog_run_id"],
                    "run_id": row["run_id"],
                    "created_at": row["created_at"],
                    "execution_status": row["execution_status"],
                    "verdict": row["verdict"],
                    "plan": {
                        "id": row["plan_id"],
                        "version": row["plan_version"],
                        "sha256": row["plan_sha256"],
                    },
                    "bundle": {
                        "sha256": row["bundle_sha256"],
                        "file_count": row["file_count"],
                        "total_bytes": row["total_bytes"],
                        "duplicate_count": row["duplicate_count"],
                        "base_url": f"/api/v1/runs/{row['catalog_run_id']}/bundle/",
                    },
                }
                for row in rows
            ],
            "issues": [
                {
                    "issue_id": row["issue_id"],
                    "code": row["code"],
                    "candidate_id": row["candidate_id"],
                    "run_id": row["run_id"],
                    "bundle_digests": json.loads(row["bundle_digests_json"]),
                    "occurrence_count": row["occurrence_count"],
                }
                for row in issues
            ],
            "issues_truncated": int(self.manifest["issue_count"]) > len(issues),
        }

    def bundle_file(
        self, catalog_run_id: str, relative_path: str
    ) -> tuple[Path, int, str, str]:
        if not CATALOG_RUN_ID_PATTERN.fullmatch(catalog_run_id):
            raise ApiError(HTTPStatus.NOT_FOUND, "RUN_NOT_FOUND", "Catalog Run 不存在。")
        try:
            normalized = _safe_relative_path(relative_path)
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "UNSAFE_PATH", "Bundle 路径不安全。") from exc
        connection = self.connection()
        try:
            row = connection.execute(
                """
                SELECT r.source_relative, f.sha256, f.size
                FROM catalog_runs AS r
                JOIN catalog_files AS f ON f.catalog_run_id = r.catalog_run_id
                WHERE r.catalog_run_id = ? AND f.path = ?
                """,
                (catalog_run_id, normalized),
            ).fetchone()
            run_exists = connection.execute(
                "SELECT 1 FROM catalog_runs WHERE catalog_run_id = ?", (catalog_run_id,)
            ).fetchone()
        finally:
            connection.close()
        if run_exists is None:
            raise ApiError(HTTPStatus.NOT_FOUND, "RUN_NOT_FOUND", "Catalog Run 不存在。")
        if row is None:
            raise ApiError(
                HTTPStatus.NOT_FOUND,
                "BUNDLE_FILE_NOT_FOUND",
                "该文件未由 Bundle Manifest 声明。",
            )
        try:
            source_relative = _safe_relative_path(row["source_relative"])
            bundle_root = self.artifact_root / Path(*source_relative.split("/"))
            bundle_root_metadata = os.lstat(bundle_root)
            if (
                bundle_root.is_symlink()
                or _is_reparse(bundle_root_metadata)
                or not stat.S_ISDIR(bundle_root_metadata.st_mode)
                or not _is_relative_to(bundle_root.resolve(strict=True), self.artifact_root.resolve(strict=True))
            ):
                raise ValueError("unsafe bundle root")
            path, metadata = _safe_file(bundle_root, normalized, max_bytes=10 * 1024 * 1024)
        except FileNotFoundError as exc:
            raise ApiError(
                HTTPStatus.CONFLICT, "BUNDLE_UNAVAILABLE", "源 Bundle 当前不可用。"
            ) from exc
        except (OSError, ValueError) as exc:
            raise ApiError(
                HTTPStatus.CONFLICT, "BUNDLE_UNAVAILABLE", "源 Bundle 当前不可安全读取。"
            ) from exc
        if metadata.st_size != row["size"] or _sha256_file(path) != row["sha256"]:
            raise ApiError(
                HTTPStatus.CONFLICT, "BUNDLE_CHANGED", "源 Bundle 已在索引后发生变化。"
            )
        content_type = CONTENT_TYPES.get(path.suffix.lower())
        if content_type is None:
            raise ApiError(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "BUNDLE_MEDIA_UNSUPPORTED",
                "该 Bundle 文件类型不允许通过本地 API 提供。",
            )
        return path, metadata.st_size, row["sha256"], content_type


class ApiError(Exception):
    def __init__(self, status: HTTPStatus, code: str, message: str) -> None:
        self.status = status
        self.code = code
        self.message = message
        super().__init__(message)


class CatalogRequestHandler(BaseHTTPRequestHandler):
    server: "BoundedCatalogServer"
    protocol_version = "HTTP/1.1"
    server_version = "VeriTrailLocal"
    sys_version = ""

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_error(
        self,
        code: int,
        message: str | None = None,
        explain: str | None = None,
    ) -> None:
        if code == HTTPStatus.NOT_IMPLEMENTED:
            self._json_error(
                HTTPStatus.METHOD_NOT_ALLOWED,
                "METHOD_NOT_ALLOWED",
                "本地 Catalog 只接受 GET 与 HEAD。",
                head_only=False,
                extra_headers={"Allow": "GET, HEAD"},
            )
            return
        status = HTTPStatus(code) if code in HTTPStatus._value2member_map_ else HTTPStatus.BAD_REQUEST
        stable_code = "REQUEST_PATH_TOO_LONG" if status == HTTPStatus.REQUEST_URI_TOO_LONG else "MALFORMED_REQUEST"
        self._json_error(status, stable_code, "HTTP 请求无效。", head_only=False)

    def do_GET(self) -> None:  # noqa: N802
        self._dispatch(head_only=False)

    def do_HEAD(self) -> None:  # noqa: N802
        self._dispatch(head_only=True)

    def do_POST(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_PUT(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_PATCH(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_DELETE(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_TRACE(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_CONNECT(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def _method_not_allowed(self) -> None:
        self._json_error(
            HTTPStatus.METHOD_NOT_ALLOWED,
            "METHOD_NOT_ALLOWED",
            "本地 Catalog 只接受 GET 与 HEAD。",
            head_only=False,
            extra_headers={"Allow": "GET, HEAD"},
        )

    def _dispatch(self, *, head_only: bool) -> None:
        try:
            if len(self.path) > MAX_REQUEST_PATH:
                raise ApiError(HTTPStatus.REQUEST_URI_TOO_LONG, "REQUEST_PATH_TOO_LONG", "请求路径过长。")
            hosts = self.headers.get_all("Host", failobj=[])
            expected_hosts = {
                f"127.0.0.1:{self.server.server_port}",
                f"localhost:{self.server.server_port}",
            }
            if len(hosts) != 1 or hosts[0] not in expected_hosts:
                raise ApiError(HTTPStatus.BAD_REQUEST, "HOST_REJECTED", "Host 不属于当前回环服务。")
            if self.headers.get("Range") is not None:
                raise ApiError(HTTPStatus.BAD_REQUEST, "RANGE_NOT_SUPPORTED", "本地 Catalog 不接受 Range 请求。")
            if self.headers.get("Transfer-Encoding") is not None:
                raise ApiError(HTTPStatus.BAD_REQUEST, "REQUEST_BODY_NOT_ALLOWED", "只读请求不接受正文。")
            content_length = self.headers.get("Content-Length")
            if content_length not in {None, "0"}:
                raise ApiError(HTTPStatus.BAD_REQUEST, "REQUEST_BODY_NOT_ALLOWED", "只读请求不接受正文。")
            split = urlsplit(self.path)
            if split.scheme or split.netloc:
                raise ApiError(HTTPStatus.BAD_REQUEST, "UNSAFE_REQUEST_TARGET", "请求目标必须是同源相对路径。")
            try:
                decoded_path = unquote(split.path, errors="strict")
            except UnicodeError as exc:
                raise ApiError(HTTPStatus.BAD_REQUEST, "UNSAFE_PATH", "请求路径编码无效。") from exc
            if decoded_path == "/api/v1/health":
                if split.query:
                    raise ApiError(HTTPStatus.BAD_REQUEST, "UNKNOWN_QUERY", "健康端点不接受查询参数。")
                self._send_json(HTTPStatus.OK, self.server.application.health(), head_only=head_only)
                return
            if decoded_path == "/api/v1/catalog":
                page, page_size = self._pagination(split.query)
                self._send_json(
                    HTTPStatus.OK,
                    self.server.application.catalog(page, page_size),
                    head_only=head_only,
                )
                return
            prefix = "/api/v1/runs/"
            if decoded_path.startswith(prefix):
                remainder = decoded_path[len(prefix) :]
                marker = "/bundle/"
                if marker not in remainder:
                    raise ApiError(HTTPStatus.NOT_FOUND, "API_NOT_FOUND", "API 端点不存在。")
                catalog_run_id, relative_path = remainder.split(marker, 1)
                if split.query:
                    raise ApiError(HTTPStatus.BAD_REQUEST, "UNKNOWN_QUERY", "Bundle 文件端点不接受查询参数。")
                self._send_bundle(catalog_run_id, relative_path, head_only=head_only)
                return
            if decoded_path.startswith("/api/"):
                raise ApiError(HTTPStatus.NOT_FOUND, "API_NOT_FOUND", "API 端点不存在。")
            if split.query and decoded_path != "/":
                raise ApiError(HTTPStatus.BAD_REQUEST, "UNKNOWN_QUERY", "静态资源不接受查询参数。")
            self._send_static(decoded_path, head_only=head_only)
        except ApiError as exc:
            self._json_error(exc.status, exc.code, exc.message, head_only=head_only)
        except (BrokenPipeError, ConnectionResetError, socket.timeout):
            self.close_connection = True
        except Exception:
            self._json_error(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "INTERNAL_ERROR",
                "本地 Catalog 服务发生未预期错误。",
                head_only=head_only,
            )

    def _pagination(self, query: str) -> tuple[int, int]:
        try:
            parsed = parse_qs(query, keep_blank_values=True, strict_parsing=True) if query else {}
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "INVALID_QUERY", "分页参数无效。") from exc
        if set(parsed) - {"page", "page_size"} or any(len(values) != 1 for values in parsed.values()):
            raise ApiError(HTTPStatus.BAD_REQUEST, "UNKNOWN_QUERY", "Catalog 包含未知或重复查询参数。")
        try:
            page = int(parsed.get("page", ["1"])[0])
            page_size = int(parsed.get("page_size", [str(DEFAULT_PAGE_SIZE)])[0])
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "INVALID_PAGINATION", "分页参数必须是整数。") from exc
        if page < 1 or page_size < 1 or page_size > MAX_PAGE_SIZE:
            raise ApiError(HTTPStatus.BAD_REQUEST, "INVALID_PAGINATION", "分页参数超出允许范围。")
        return page, page_size

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any], *, head_only: bool) -> None:
        body = canonical_json_bytes(payload) + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._security_headers()
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def _json_error(
        self,
        status: HTTPStatus,
        code: str,
        message: str,
        *,
        head_only: bool,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        body = canonical_json_bytes(
            {"schema_version": CATALOG_API_VERSION, "error": {"code": code, "message": message}}
        ) + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self._security_headers()
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def _send_bundle(self, catalog_run_id: str, relative_path: str, *, head_only: bool) -> None:
        path, size, digest, content_type = self.server.application.bundle_file(
            catalog_run_id, relative_path
        )
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(size))
        self.send_header("ETag", f'"sha256-{digest}"')
        self._security_headers()
        self.end_headers()
        if not head_only:
            with path.open("rb") as handle:
                while chunk := handle.read(64 * 1024):
                    self.wfile.write(chunk)

    def _send_static(self, request_path: str, *, head_only: bool) -> None:
        raw = request_path.lstrip("/") or "index.html"
        try:
            normalized = _safe_relative_path(raw)
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "UNSAFE_PATH", "静态资源路径不安全。") from exc
        try:
            path, metadata = _safe_file(
                self.server.application.web_root, normalized, max_bytes=MAX_STATIC_FILE_BYTES
            )
        except FileNotFoundError:
            if "." not in Path(normalized).name:
                path, metadata = _safe_file(
                    self.server.application.web_root,
                    "index.html",
                    max_bytes=MAX_STATIC_FILE_BYTES,
                )
            else:
                raise ApiError(HTTPStatus.NOT_FOUND, "STATIC_NOT_FOUND", "静态资源不存在。")
        except (OSError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "UNSAFE_PATH", "静态资源不可安全读取。") from exc
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"}:
            content_type += "; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(metadata.st_size))
        self._security_headers()
        self.end_headers()
        if not head_only:
            with path.open("rb") as handle:
                while chunk := handle.read(64 * 1024):
                    self.wfile.write(chunk)


class BoundedCatalogServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = MAX_CONNECTIONS
    allow_reuse_address = False

    def __init__(self, address: tuple[str, int], application: CatalogApplication) -> None:
        self.application = application
        self._slots = threading.BoundedSemaphore(MAX_CONNECTIONS)
        super().__init__(address, CatalogRequestHandler)

    def get_request(self) -> tuple[socket.socket, Any]:
        request, client_address = super().get_request()
        request.settimeout(SOCKET_TIMEOUT_SECONDS)
        return request, client_address

    def process_request(self, request: socket.socket, client_address: Any) -> None:
        if not self._slots.acquire(blocking=False):
            request.close()
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self._slots.release()
            raise

    def process_request_thread(self, request: socket.socket, client_address: Any) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._slots.release()


def create_catalog_server(
    *, catalog_root: Path, artifact_root: Path, web_root: Path, port: int
) -> BoundedCatalogServer:
    if port < 1024 or port > 65535:
        raise CatalogError("INVALID_PORT", "服务端口必须位于 1024 到 65535。")
    application = CatalogApplication(catalog_root, artifact_root, web_root)
    try:
        return BoundedCatalogServer(("127.0.0.1", port), application)
    except OSError as exc:
        raise CatalogError("PORT_UNAVAILABLE", "指定回环端口不可用。") from exc
