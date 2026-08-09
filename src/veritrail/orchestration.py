from __future__ import annotations

import hashlib
import http.client
import mimetypes
import os
import re
import socket
import stat
import threading
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urlsplit

from veritrail.browser import collect_browser_evidence
from veritrail.canonical import sha256_bytes, sha256_json
from veritrail.evidence import ImportedEvidence, import_evidence_document
from veritrail.errors import ValidationError
from veritrail.resources import MEBIBYTE, process_rss_bytes

COLLECTOR_VERSION = "bounded-orchestrator/0.1"
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
MAX_REQUEST_EVENTS = 1000
MAX_REQUEST_PATH = 2048
MAX_CONNECTIONS = 8
SOCKET_TIMEOUT_SECONDS = 5
ALLOWED_SUFFIXES = {
    ".css",
    ".html",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".png",
    ".svg",
    ".txt",
    ".webp",
}
CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".ico": "image/x-icon",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".webp": "image/webp",
}
CSP = (
    "default-src 'self'; img-src 'self' data:; script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; font-src 'none'; connect-src 'self'; "
    "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class StaticFile:
    relative_path: str
    path: Path
    sha256: str
    size: int
    content_type: str


@dataclass(frozen=True)
class StaticSnapshot:
    root: Path
    files: dict[str, StaticFile]
    fingerprint: str
    total_bytes: int


@dataclass(frozen=True)
class OrchestrationResult:
    orchestration: ImportedEvidence
    browser: ImportedEvidence | None
    execution_status: str


def _safe_path_chain(root: Path, relative_path: str) -> Path:
    current = root
    for part in relative_path.split("/"):
        current = current / part
        metadata = os.lstat(current)
        if current.is_symlink() or _is_reparse(metadata):
            raise ValidationError(["target path contains an unsafe link or reparse point"])
    return current


def prepare_static_target(plan: dict[str, Any], subject_root: Path) -> StaticSnapshot:
    target = plan["target"]
    absolute_subject = subject_root.absolute()
    try:
        subject_metadata = os.lstat(absolute_subject)
    except OSError as exc:
        raise ValidationError(["subject root is unavailable"]) from exc
    if (
        absolute_subject.is_symlink()
        or _is_reparse(subject_metadata)
        or not stat.S_ISDIR(subject_metadata.st_mode)
    ):
        raise ValidationError(["subject root must be a regular local directory"])
    try:
        resolved_subject = absolute_subject.resolve(strict=True)
        target_root = _safe_path_chain(absolute_subject, target["root"])
        target_metadata = os.lstat(target_root)
        resolved_target = target_root.resolve(strict=True)
    except (OSError, ValidationError) as exc:
        if isinstance(exc, ValidationError):
            raise
        raise ValidationError(["target root is unavailable"]) from exc
    if not stat.S_ISDIR(target_metadata.st_mode) or not _is_relative_to(
        resolved_target, resolved_subject
    ):
        raise ValidationError(["target root must stay inside the subject root"])

    files: dict[str, StaticFile] = {}
    total_bytes = 0
    stack = [target_root]
    while stack:
        directory = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise ValidationError(["target root cannot be scanned"]) from exc
        for entry in entries:
            if entry.name.startswith(".") or any(ord(character) < 32 for character in entry.name):
                raise ValidationError(["target contains a hidden or control-character path"])
            path = Path(entry.path)
            try:
                metadata = os.lstat(path)
                resolved = path.resolve(strict=True)
            except OSError as exc:
                raise ValidationError(["target contains an unreadable node"]) from exc
            if entry.is_symlink() or _is_reparse(metadata):
                raise ValidationError(["target contains an unsafe link or reparse point"])
            if not _is_relative_to(resolved, resolved_target):
                raise ValidationError(["target node escapes the static root"])
            if stat.S_ISDIR(metadata.st_mode):
                stack.append(path)
                continue
            if not stat.S_ISREG(metadata.st_mode):
                raise ValidationError(["target contains a non-regular file"])
            if metadata.st_nlink != 1:
                raise ValidationError(["target contains an unsafe hard link"])
            relative = path.relative_to(target_root).as_posix()
            if any(part in {"", ".", ".."} for part in relative.split("/")):
                raise ValidationError(["target contains an unsafe relative path"])
            suffix = path.suffix.lower()
            if suffix not in ALLOWED_SUFFIXES:
                raise ValidationError(["target contains an unsupported static file type"])
            size = metadata.st_size
            if size > target["max_file_bytes"]:
                raise ValidationError(["target contains a file above the sealed size limit"])
            total_bytes += size
            if total_bytes > target["max_total_bytes"]:
                raise ValidationError(["target exceeds the sealed total size limit"])
            if len(files) + 1 > target["max_files"]:
                raise ValidationError(["target exceeds the sealed file-count limit"])
            files[relative] = StaticFile(
                relative_path=relative,
                path=path,
                sha256=_sha256_file(path),
                size=size,
                content_type=CONTENT_TYPES.get(
                    suffix, mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                ),
            )
    if "index.html" not in files:
        raise ValidationError(["target root must contain index.html"])
    fingerprint = sha256_json(
        [
            {"path": item.relative_path, "sha256": item.sha256, "size": item.size}
            for item in sorted(files.values(), key=lambda entry: entry.relative_path)
        ]
    )
    return StaticSnapshot(
        root=target_root,
        files=files,
        fingerprint=fingerprint,
        total_bytes=total_bytes,
    )


class RequestRecorder:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.requests: list[dict[str, Any]] = []
        self.collection_errors: list[dict[str, str]] = []

    def record(self, method: str, path: str, status: int, size: int) -> None:
        with self._lock:
            if len(self.requests) >= MAX_REQUEST_EVENTS:
                error = {"stage": "request-recorder", "error_type": "EventLimitExceeded"}
                if error not in self.collection_errors:
                    self.collection_errors.append(error)
                return
            self.requests.append(
                {
                    "sequence": len(self.requests) + 1,
                    "method": method,
                    "path": path,
                    "status": status,
                    "bytes": size,
                }
            )


class StaticApplication:
    def __init__(self, snapshot: StaticSnapshot, port: int, recorder: RequestRecorder) -> None:
        self.snapshot = snapshot
        self.port = port
        self.recorder = recorder

    def read_verified(self, relative_path: str) -> tuple[bytes, StaticFile]:
        item = self.snapshot.files[relative_path]
        try:
            current = _safe_path_chain(self.snapshot.root, relative_path)
            metadata = os.lstat(current)
            content = current.read_bytes()
        except (OSError, ValidationError) as exc:
            raise ValueError("source unavailable") from exc
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
            or metadata.st_size != item.size
            or len(content) != item.size
            or sha256_bytes(content) != item.sha256
        ):
            raise ValueError("source changed")
        return content, item


class StaticRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "VeriTrailStatic/0.1"
    sys_version = ""

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")

    def _reply(
        self,
        status: HTTPStatus,
        *,
        body: bytes = b"",
        content_type: str = "text/plain; charset=utf-8",
        head_only: bool = False,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self._security_headers()
        self.end_headers()
        if not head_only and body:
            self.wfile.write(body)

    def _normalized_path(self) -> str:
        if len(self.path) > MAX_REQUEST_PATH:
            raise ValueError("path too long")
        parsed = urlsplit(self.path)
        if parsed.scheme or parsed.netloc or parsed.fragment:
            raise ValueError("unsupported target")
        try:
            decoded = unquote(parsed.path, errors="strict")
        except UnicodeError as exc:
            raise ValueError("invalid encoding") from exc
        if (
            not decoded.startswith("/")
            or "\\" in decoded
            or "//" in decoded
            or any(ord(character) < 32 for character in decoded)
        ):
            raise ValueError("unsafe path")
        parts = decoded.split("/")[1:]
        if any(part in {".", ".."} or part.startswith(".") for part in parts if part):
            raise ValueError("unsafe path")
        if decoded == "/":
            return "index.html"
        if decoded.endswith("/"):
            parts.append("index.html")
        normalized = "/".join(part for part in parts if part)
        if not normalized:
            return "index.html"
        return normalized

    def _serve(self, *, head_only: bool) -> None:
        method = "HEAD" if head_only else "GET"
        application = self.server.application
        host = self.headers.get("Host", "")
        if host not in {f"127.0.0.1:{application.port}", f"localhost:{application.port}"}:
            self._reply(HTTPStatus.BAD_REQUEST, head_only=head_only)
            application.recorder.record(method, "[REJECTED]", HTTPStatus.BAD_REQUEST, 0)
            return
        if self.headers.get("Transfer-Encoding") or self.headers.get("Content-Length") not in {
            None,
            "0",
        }:
            self._reply(HTTPStatus.BAD_REQUEST, head_only=head_only)
            application.recorder.record(method, "[REJECTED]", HTTPStatus.BAD_REQUEST, 0)
            return
        if self.headers.get("Range"):
            self._reply(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE, head_only=head_only)
            application.recorder.record(
                method, "[REJECTED]", HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE, 0
            )
            return
        try:
            relative = self._normalized_path()
        except ValueError:
            self._reply(HTTPStatus.BAD_REQUEST, head_only=head_only)
            application.recorder.record(method, "[REJECTED]", HTTPStatus.BAD_REQUEST, 0)
            return
        if relative not in application.snapshot.files:
            self._reply(HTTPStatus.NOT_FOUND, head_only=head_only)
            application.recorder.record(method, "/" + relative, HTTPStatus.NOT_FOUND, 0)
            return
        try:
            content, item = application.read_verified(relative)
        except ValueError:
            self._reply(HTTPStatus.CONFLICT, head_only=head_only)
            application.recorder.record(method, "/" + relative, HTTPStatus.CONFLICT, 0)
            return
        self._reply(
            HTTPStatus.OK,
            body=content,
            content_type=item.content_type,
            head_only=head_only,
        )
        application.recorder.record(method, "/" + relative, HTTPStatus.OK, len(content))

    def do_GET(self) -> None:
        self._serve(head_only=False)

    def do_HEAD(self) -> None:
        self._serve(head_only=True)

    def _method_not_allowed(self) -> None:
        self._reply(
            HTTPStatus.METHOD_NOT_ALLOWED,
            extra_headers={"Allow": "GET, HEAD"},
        )
        self.server.application.recorder.record(
            self.command.upper(), "[REJECTED]", HTTPStatus.METHOD_NOT_ALLOWED, 0
        )

    do_POST = _method_not_allowed
    do_PUT = _method_not_allowed
    do_PATCH = _method_not_allowed
    do_DELETE = _method_not_allowed
    do_OPTIONS = _method_not_allowed
    do_TRACE = _method_not_allowed
    do_CONNECT = _method_not_allowed


class BoundedStaticServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = MAX_CONNECTIONS
    allow_reuse_address = False

    def __init__(self, address: tuple[str, int], application: StaticApplication) -> None:
        self.application = application
        self._slots = threading.BoundedSemaphore(MAX_CONNECTIONS)
        super().__init__(address, StaticRequestHandler)

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


def create_static_server(snapshot: StaticSnapshot, port: int, recorder: RequestRecorder) -> BoundedStaticServer:
    application = StaticApplication(snapshot, port, recorder)
    return BoundedStaticServer(("127.0.0.1", port), application)


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
        if exclusive is not None:
            probe.setsockopt(socket.SOL_SOCKET, exclusive, 1)
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True


def _wait_ready(port: int, path: str, timeout_ms: int) -> tuple[bool, int]:
    deadline = time.monotonic() + timeout_ms / 1000
    attempts = 0
    while time.monotonic() < deadline:
        attempts += 1
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=0.5)
        try:
            connection.request("GET", path, headers={"Host": f"127.0.0.1:{port}"})
            response = connection.getresponse()
            response.read()
            if response.status == HTTPStatus.OK:
                return True, attempts
        except OSError:
            pass
        finally:
            connection.close()
        time.sleep(0.05)
    return False, attempts


def _rss_mb() -> float:
    return round(process_rss_bytes() / MEBIBYTE, 3)


def _event(stage: str) -> tuple[dict[str, Any], float]:
    return (
        {
            "sequence": 0,
            "stage": stage,
            "status": "RUNNING",
            "started_at": _utc_now(),
            "ended_at": None,
            "elapsed_ms": None,
            "error_type": None,
        },
        time.monotonic(),
    )


def _finish_event(
    events: list[dict[str, Any]], entry: dict[str, Any], started: float, error: BaseException | None = None
) -> None:
    entry["sequence"] = len(events) + 1
    entry["ended_at"] = _utc_now()
    entry["elapsed_ms"] = round((time.monotonic() - started) * 1000, 3)
    entry["status"] = "FAILED" if error is not None else "PASSED"
    entry["error_type"] = type(error).__name__ if error is not None else None
    events.append(entry)


def collect_orchestrated_evidence(
    plan: dict[str, Any],
    subject_root: Path,
    *,
    browser_collector: Callable[[dict[str, Any]], ImportedEvidence] = collect_browser_evidence,
) -> OrchestrationResult:
    snapshot = prepare_static_target(plan, subject_root)
    policy = plan["target"]
    started_at = _utc_now()
    started_monotonic = time.monotonic()
    events: list[dict[str, Any]] = []
    collection_errors: list[dict[str, str]] = []
    recorder = RequestRecorder()
    browser_artifact: ImportedEvidence | None = None
    server: BoundedStaticServer | None = None
    server_thread: threading.Thread | None = None
    server_started = False
    ready = False
    ready_probe_count = 0
    server_stopped = True
    thread_stopped = True
    port_released = True
    rss_start = 0.0
    rss_peak = 0.0
    thread_start = threading.active_count()
    max_active_threads = thread_start

    try:
        rss_start = _rss_mb()
        rss_peak = rss_start
    except (OSError, ValueError) as exc:
        collection_errors.append({"stage": "observer-rss", "error_type": type(exc).__name__})

    start_event, start_clock = _event("target-start")
    try:
        server = create_static_server(snapshot, policy["port"], recorder)
        server_started = True
        server_stopped = False
        server_thread = threading.Thread(
            target=server.serve_forever,
            kwargs={"poll_interval": 0.05},
            name="veritrail-static-http",
            daemon=True,
        )
        server_thread.start()
        thread_stopped = False
        max_active_threads = max(max_active_threads, threading.active_count())
        _finish_event(events, start_event, start_clock)
    except Exception as exc:
        collection_errors.append({"stage": "target-start", "error_type": type(exc).__name__})
        _finish_event(events, start_event, start_clock, exc)

    if server_started:
        ready_event, ready_clock = _event("target-ready")
        try:
            ready, ready_probe_count = _wait_ready(
                policy["port"], policy["ready_path"], policy["startup_timeout_ms"]
            )
            if not ready:
                raise TimeoutError("target readiness timed out")
            _finish_event(events, ready_event, ready_clock)
        except Exception as exc:
            collection_errors.append({"stage": "target-ready", "error_type": type(exc).__name__})
            _finish_event(events, ready_event, ready_clock, exc)

    if ready:
        browser_event, browser_clock = _event("browser-capture")
        try:
            browser_artifact = browser_collector(plan)
            if browser_artifact.document["facts"].get("capture_complete") is not True:
                raise RuntimeError("browser capture incomplete")
            _finish_event(events, browser_event, browser_clock)
        except Exception as exc:
            if browser_artifact is None:
                collection_errors.append(
                    {"stage": "browser-capture", "error_type": type(exc).__name__}
                )
            _finish_event(events, browser_event, browser_clock, exc)

    cleanup_event, cleanup_clock = _event("target-cleanup")
    cleanup_error: BaseException | None = None
    if server is not None:
        try:
            server.shutdown()
            server.server_close()
            server_stopped = True
        except Exception as exc:
            cleanup_error = exc
            collection_errors.append({"stage": "target-cleanup", "error_type": type(exc).__name__})
    if server_thread is not None:
        server_thread.join(policy["shutdown_timeout_ms"] / 1000)
        thread_stopped = not server_thread.is_alive()
        if not thread_stopped and cleanup_error is None:
            cleanup_error = TimeoutError("target thread did not stop")
            collection_errors.append(
                {"stage": "target-cleanup", "error_type": "ThreadShutdownTimeout"}
            )
    deadline = time.monotonic() + policy["shutdown_timeout_ms"] / 1000
    port_released = _port_is_free(policy["port"])
    while not port_released and time.monotonic() < deadline:
        time.sleep(0.05)
        port_released = _port_is_free(policy["port"])
    if not port_released and cleanup_error is None:
        cleanup_error = TimeoutError("target port was not released")
        collection_errors.append({"stage": "target-cleanup", "error_type": "PortReleaseTimeout"})
    _finish_event(events, cleanup_event, cleanup_clock, cleanup_error)

    max_active_threads = max(max_active_threads, threading.active_count())
    try:
        rss_peak = max(rss_peak, _rss_mb())
    except (OSError, ValueError) as exc:
        error = {"stage": "observer-rss", "error_type": type(exc).__name__}
        if error not in collection_errors:
            collection_errors.append(error)
    for error in recorder.collection_errors:
        if error not in collection_errors:
            collection_errors.append(error)

    cleanup_complete = server_stopped and thread_stopped and port_released
    browser_complete = (
        browser_artifact is not None
        and browser_artifact.document["facts"].get("capture_complete") is True
    )
    lifecycle_complete = (
        server_started and ready and cleanup_complete and not collection_errors
    )
    status_counts = Counter(str(item["status"]) for item in recorder.requests)
    method_counts = Counter(item["method"] for item in recorder.requests)
    rejected_count = sum(1 for item in recorder.requests if item["status"] >= 400)
    ended_at = _utc_now()
    facts = {
        "collector_version": COLLECTOR_VERSION,
        "policy_sha256": sha256_json(policy),
        "static_root_fingerprint": snapshot.fingerprint,
        "file_count": len(snapshot.files),
        "total_bytes": snapshot.total_bytes,
        "origin": f"http://localhost:{policy['port']}",
        "started_at": started_at,
        "ended_at": ended_at,
        "server_started": server_started,
        "ready": ready,
        "ready_probe_count": ready_probe_count,
        "server_stopped": server_stopped,
        "thread_stopped": thread_stopped,
        "port_released": port_released,
        "cleanup_complete": cleanup_complete,
        "browser_complete": browser_complete,
        "lifecycle_complete": lifecycle_complete,
        "events": events,
        "requests": recorder.requests,
        "request_count": len(recorder.requests),
        "method_counts": dict(sorted(method_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "rejected_request_count": rejected_count,
        "collection_errors": collection_errors,
        "observer_effect": {
            "rss_start_mb": rss_start,
            "rss_peak_mb": rss_peak,
            "rss_delta_mb": max(0.0, round(rss_peak - rss_start, 3)),
            "thread_start_count": thread_start,
            "max_active_thread_count": max_active_threads,
        },
        "collection_elapsed_ms": round((time.monotonic() - started_monotonic) * 1000, 3),
    }
    declared = {item["name"] for item in plan["variables"]}
    observed = (
        {"target_lifecycle_mode": "veritrail_managed_static_http"}
        if "target_lifecycle_mode" in declared
        else {}
    )
    document = {
        "schema_version": "0.1",
        "evidence_type": "runtime.orchestration",
        "source": f"VeriTrail {COLLECTOR_VERSION}",
        "captured_at": started_at,
        "facts": facts,
        "observed_variables": observed,
        "metadata": {
            "network_scope": "loopback-only",
            "shell_used": False,
            "external_process_started": False,
            "writes_allowed": False,
            "request_headers_persisted": False,
            "request_bodies_persisted": False,
        },
    }
    orchestration = import_evidence_document(document, "generated-orchestration.json")
    execution_status = "COMPLETED" if lifecycle_complete and browser_complete else "ERROR"
    return OrchestrationResult(
        orchestration=orchestration,
        browser=browser_artifact,
        execution_status=execution_status,
    )
