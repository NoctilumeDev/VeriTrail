from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import stat
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from veritrail import __version__
from veritrail.atomic_publish import publish_staged_directory
from veritrail.canonical import canonical_json_bytes, sha256_bytes, sha256_json
from veritrail.evidence import ImportedEvidence, validate_evidence
from veritrail.errors import VeriTrailError
from veritrail.jsonio import load_json_object, load_json_object_bytes, read_stable_bytes
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.verdict import evaluate

CATALOG_SCHEMA_VERSION = "0.1"
CATALOG_API_VERSION = "0.1"
MAX_CANDIDATES = 1000
MAX_FILES = 256
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_BUNDLE_BYTES = 64 * 1024 * 1024
MAX_IMPORTED_STRING_BYTES = 16 * 1024
MAX_BUNDLE_PATH_BYTES = 1024
MAX_PATH_SEGMENT_BYTES = 255
MAX_METADATA_ITEMS = 4096
MAX_CATALOG_RETAINED_BYTES = 16 * 1024 * 1024
MAX_CATALOG_DATABASE_BYTES = 128 * 1024 * 1024
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
RUN_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
EXECUTION_STATUSES = {"PLANNED", "RUNNING", "COMPLETED", "ABORTED", "ERROR"}
VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE", "PENDING"}
SAFE_ATTACHMENT_TYPES = {
    "image/png",
    "image/jpeg",
    "text/plain; charset=utf-8",
}
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)

CATALOG_SCHEMA_SQL = """
PRAGMA page_size = 4096;
PRAGMA journal_mode = OFF;
PRAGMA synchronous = OFF;
PRAGMA temp_store = MEMORY;
PRAGMA foreign_keys = ON;
CREATE TABLE catalog_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) WITHOUT ROWID;
CREATE TABLE catalog_runs (
    catalog_run_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL UNIQUE CHECK (length(run_id) BETWEEN 2 AND 64),
    created_at TEXT NOT NULL,
    execution_status TEXT NOT NULL CHECK (execution_status IN ('PLANNED','RUNNING','COMPLETED','ABORTED','ERROR')),
    verdict TEXT NOT NULL CHECK (verdict IN ('PASS','FAIL','INCONCLUSIVE','PENDING')),
    plan_id TEXT NOT NULL CHECK (length(plan_id) BETWEEN 2 AND 64),
    plan_version INTEGER NOT NULL CHECK (plan_version >= 0),
    plan_sha256 TEXT NOT NULL CHECK (length(plan_sha256) = 64),
    bundle_sha256 TEXT NOT NULL CHECK (length(bundle_sha256) = 64),
    file_count INTEGER NOT NULL CHECK (file_count > 0 AND file_count <= 256),
    total_bytes INTEGER NOT NULL CHECK (total_bytes >= 0 AND total_bytes <= 67108864),
    duplicate_count INTEGER NOT NULL CHECK (duplicate_count >= 0),
    source_relative TEXT NOT NULL UNIQUE CHECK (length(source_relative) BETWEEN 1 AND 1024)
) WITHOUT ROWID;
CREATE TABLE catalog_files (
    catalog_run_id TEXT NOT NULL,
    path TEXT NOT NULL,
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
    size INTEGER NOT NULL CHECK (size >= 0 AND size <= 10485760),
    PRIMARY KEY (catalog_run_id, path),
    FOREIGN KEY (catalog_run_id) REFERENCES catalog_runs(catalog_run_id)
) WITHOUT ROWID;
CREATE TABLE catalog_issues (
    issue_id TEXT PRIMARY KEY,
    code TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    run_id TEXT,
    bundle_digests_json TEXT NOT NULL,
    occurrence_count INTEGER NOT NULL CHECK (occurrence_count > 0)
) WITHOUT ROWID;
CREATE INDEX catalog_runs_order
    ON catalog_runs(created_at DESC, run_id ASC, catalog_run_id ASC);
CREATE INDEX catalog_issues_order
    ON catalog_issues(code ASC, run_id ASC, issue_id ASC);
"""


class CatalogError(VeriTrailError):
    """Stable, sanitized failure exposed by M4 commands."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class _CandidateRejected(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class BundleFile:
    path: str
    sha256: str
    size: int


@dataclass(frozen=True)
class ValidatedBundle:
    source_relative: str
    run_id: str
    created_at: str
    execution_status: str
    verdict: str
    plan_id: str
    plan_version: int
    plan_sha256: str
    profile_sha256: str | None
    bundle_sha256: str
    files: tuple[BundleFile, ...]
    total_bytes: int
    owned_files: tuple[tuple[str, bytes], ...] = field(default=(), repr=False)

    def read_owned_file(self, path: str) -> bytes:
        for owned_path, content in self.owned_files:
            if owned_path == path:
                return content
        raise KeyError(path)

    def load_owned_json(self, path: str, *, label: str) -> dict[str, Any]:
        return load_json_object_bytes(
            self.read_owned_file(path), label=label, name=path
        )


@dataclass(frozen=True)
class CatalogIssue:
    code: str
    candidate_id: str
    run_id: str | None = None
    bundle_digests: tuple[str, ...] = ()
    occurrence_count: int = 1

    @property
    def issue_id(self) -> str:
        return "ci_" + sha256_json(
            {
                "code": self.code,
                "candidate_id": self.candidate_id,
                "run_id": self.run_id,
                "bundle_digests": list(self.bundle_digests),
                "occurrence_count": self.occurrence_count,
            }
        )[:24]


@dataclass(frozen=True)
class CatalogRun:
    bundle: ValidatedBundle
    catalog_run_id: str
    duplicate_count: int


@dataclass(frozen=True)
class CatalogBuildResult:
    status: str
    catalog_id: str
    run_count: int
    issue_count: int
    duplicate_count: int
    bundle_set_sha256: str


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _safe_bundle_path(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    if "\\" in value or "\0" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise _CandidateRejected("UNSAFE_BUNDLE_PATH")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise _CandidateRejected("UNSAFE_BUNDLE_PATH")
    try:
        value_bytes = len(value.encode("utf-8"))
        segment_bytes = [len(part.encode("utf-8")) for part in parts]
    except UnicodeError as exc:
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE") from exc
    if value_bytes > MAX_BUNDLE_PATH_BYTES or any(
        size > MAX_PATH_SEGMENT_BYTES for size in segment_bytes
    ):
        raise _CandidateRejected("BUNDLE_PATH_TOO_LONG")
    return "/".join(parts)


def _required_string(
    value: Any,
    *,
    max_bytes: int = MAX_IMPORTED_STRING_BYTES,
    pattern: re.Pattern[str] | None = None,
) -> str:
    if not isinstance(value, str) or not value:
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    try:
        encoded_size = len(value.encode("utf-8"))
    except UnicodeError as exc:
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE") from exc
    if encoded_size > max_bytes or (pattern is not None and not pattern.fullmatch(value)):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    return value


def _required_nonnegative_int(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    return value


def _required_sha256(value: Any) -> str:
    digest = _required_string(value)
    if not SHA256_PATTERN.fullmatch(digest):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    return digest


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _read_stable_file(path: Path) -> bytes:
    """Read one ordinary single-link file and bind parsing to those exact bytes."""

    try:
        before = os.lstat(path)
        if (
            _is_reparse(before)
            or not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
        ):
            raise _CandidateRejected("UNSAFE_BUNDLE_NODE")
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            content = handle.read(MAX_FILE_BYTES + 1)
        after = os.lstat(path)
    except _CandidateRejected:
        raise
    except OSError as exc:
        raise _CandidateRejected("BUNDLE_UNREADABLE") from exc
    identity_fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_nlink")
    if (
        _is_reparse(after)
        or not stat.S_ISREG(opened.st_mode)
        or not stat.S_ISREG(after.st_mode)
        or opened.st_nlink != 1
        or after.st_nlink != 1
        or any(getattr(before, field) != getattr(opened, field) for field in identity_fields)
        or any(getattr(opened, field) != getattr(after, field) for field in identity_fields)
    ):
        raise _CandidateRejected("BUNDLE_CHANGED_DURING_READ")
    if len(content) > MAX_FILE_BYTES:
        raise _CandidateRejected("BUNDLE_FILE_TOO_LARGE")
    return content


def _candidate_id(source_relative: str) -> str:
    return "cand_" + sha256_bytes(os.fsencode(source_relative))[:20]


def _root_binding(root: Path) -> str:
    normalized = os.path.normcase(str(root.resolve(strict=True)))
    return sha256_bytes(os.fsencode(normalized))


def _collect_regular_files(candidate: Path, root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    stack = [candidate]
    total_bytes = 0
    while stack:
        directory = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise _CandidateRejected("BUNDLE_UNREADABLE") from exc
        for entry in entries:
            path = Path(entry.path)
            try:
                # DirEntry.stat() reports st_nlink=0 on the supported Windows
                # runtime, so use lstat() for hard-link and reparse checks.
                metadata = os.lstat(path)
            except OSError as exc:
                raise _CandidateRejected("BUNDLE_UNREADABLE") from exc
            if entry.is_symlink() or _is_reparse(metadata):
                raise _CandidateRejected("UNSAFE_BUNDLE_NODE")
            try:
                resolved = path.resolve(strict=True)
            except OSError as exc:
                raise _CandidateRejected("BUNDLE_UNREADABLE") from exc
            if not _is_relative_to(resolved, root):
                raise _CandidateRejected("BUNDLE_ROOT_ESCAPE")
            mode = metadata.st_mode
            if stat.S_ISDIR(mode):
                stack.append(path)
                continue
            if not stat.S_ISREG(mode):
                raise _CandidateRejected("UNSAFE_BUNDLE_NODE")
            if metadata.st_nlink != 1:
                raise _CandidateRejected("UNSAFE_HARDLINK")
            relative = path.relative_to(candidate).as_posix()
            _safe_bundle_path(relative)
            size = metadata.st_size
            if size > MAX_FILE_BYTES:
                raise _CandidateRejected("BUNDLE_FILE_TOO_LARGE")
            total_bytes += size
            if total_bytes > MAX_BUNDLE_BYTES:
                raise _CandidateRejected("BUNDLE_TOO_LARGE")
            files[relative] = path
            if len(files) > MAX_FILES:
                raise _CandidateRejected("BUNDLE_FILE_LIMIT")
    return files


def _parse_bundle_manifest(value: dict[str, Any]) -> tuple[str, tuple[BundleFile, ...]]:
    if value.get("schema_version") != "0.1":
        raise _CandidateRejected("BUNDLE_VERSION_UNSUPPORTED")
    run_id = _required_string(value.get("run_id"), max_bytes=64, pattern=RUN_ID_PATTERN)
    raw_files = value.get("files")
    if not isinstance(raw_files, list):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    if len(raw_files) + 1 > MAX_FILES:
        raise _CandidateRejected("BUNDLE_FILE_LIMIT")
    entries: list[BundleFile] = []
    seen: set[str] = set()
    for raw in raw_files:
        if not isinstance(raw, dict):
            raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
        path = _safe_bundle_path(raw.get("path"))
        if path in seen:
            raise _CandidateRejected("DUPLICATE_BUNDLE_PATH")
        seen.add(path)
        entries.append(
            BundleFile(
                path=path,
                sha256=_required_sha256(raw.get("sha256")),
                size=_required_nonnegative_int(raw.get("size")),
            )
        )
    if not {"report.json", "evidence-manifest.json", "sealed-plan.json"}.issubset(seen):
        raise _CandidateRejected("MISSING_BUNDLE_ROOT_FILE")
    return run_id, tuple(sorted(entries, key=lambda item: item.path))


def _validate_report_and_evidence(
    report: dict[str, Any],
    evidence: dict[str, Any],
    manifest_run_id: str,
    declared: dict[str, BundleFile],
    file_bytes: dict[str, bytes],
) -> tuple[str, str, str, str, int, str]:
    if report.get("schema_version") != "0.1" or evidence.get("schema_version") != "0.1":
        raise _CandidateRejected("BUNDLE_VERSION_UNSUPPORTED")
    report_run_id = _required_string(
        report.get("run_id"), max_bytes=64, pattern=RUN_ID_PATTERN
    )
    evidence_run_id = _required_string(
        evidence.get("run_id"), max_bytes=64, pattern=RUN_ID_PATTERN
    )
    if report_run_id != manifest_run_id or evidence_run_id != manifest_run_id:
        raise _CandidateRejected("RUN_ID_MISMATCH")
    execution_status = _required_string(report.get("execution_status"))
    verdict = _required_string(report.get("verdict"))
    if execution_status not in EXECUTION_STATUSES:
        raise _CandidateRejected("INVALID_EXECUTION_STATUS")
    if verdict not in VERDICTS:
        raise _CandidateRejected("INVALID_VERDICT")
    created_at = _required_string(report.get("created_at"))
    try:
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise _CandidateRejected("INVALID_CREATED_AT") from exc
    plan = report.get("plan")
    if not isinstance(plan, dict):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    plan_id = _required_string(plan.get("id"), max_bytes=64, pattern=RUN_ID_PATTERN)
    plan_version = _required_nonnegative_int(plan.get("version"))
    plan_sha256 = _required_sha256(plan.get("sha256"))
    reasons = report.get("reasons")
    assertions = report.get("assertions")
    missing_evidence = report.get("missing_evidence")
    contamination = report.get("contamination")
    if (
        not isinstance(reasons, list)
        or not reasons
        or not isinstance(assertions, list)
        or not isinstance(missing_evidence, list)
        or not isinstance(contamination, list)
    ):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    if any(
        len(items) > MAX_METADATA_ITEMS
        for items in (reasons, assertions, missing_evidence, contamination)
    ):
        raise _CandidateRejected("BUNDLE_METADATA_LIMIT")
    for reason in reasons:
        if not isinstance(reason, dict):
            raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
        _required_string(reason.get("code"))
        _required_string(reason.get("message"))
    for assertion in assertions:
        if not isinstance(assertion, dict):
            raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
        _required_string(assertion.get("id"))
        _required_string(assertion.get("severity"))
        _required_string(assertion.get("status"))
    for missing in missing_evidence:
        _required_string(missing)
    if any(not isinstance(item, dict) for item in contamination):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    report_artifacts = report.get("evidence")
    evidence_artifacts = evidence.get("artifacts")
    if not isinstance(report_artifacts, list) or not isinstance(evidence_artifacts, list):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    if len(report_artifacts) > MAX_FILES or len(evidence_artifacts) > MAX_FILES:
        raise _CandidateRejected("BUNDLE_METADATA_LIMIT")
    if canonical_json_bytes(report_artifacts) != canonical_json_bytes(evidence_artifacts):
        raise _CandidateRejected("EVIDENCE_INDEX_MISMATCH")
    duplicates = evidence.get("duplicate_inputs_ignored")
    if not isinstance(duplicates, list):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
    if len(duplicates) > MAX_FILES:
        raise _CandidateRejected("BUNDLE_METADATA_LIMIT")
    for duplicate in duplicates:
        _required_string(duplicate)
    seen_artifacts: set[str] = set()
    seen_attachments: set[str] = set()
    for raw in evidence_artifacts:
        if not isinstance(raw, dict):
            raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
        evidence_type = _required_string(raw.get("evidence_type"))
        artifact_path = _safe_bundle_path(raw.get("path"))
        if artifact_path in seen_artifacts:
            raise _CandidateRejected("DUPLICATE_EVIDENCE_PATH")
        seen_artifacts.add(artifact_path)
        artifact = declared.get(artifact_path)
        if artifact is None:
            raise _CandidateRejected("MISSING_BUNDLE_REFERENCE")
        if artifact.sha256 != _required_sha256(raw.get("sha256")):
            raise _CandidateRejected("EVIDENCE_INDEX_MISMATCH")
        if artifact.size != _required_nonnegative_int(raw.get("size")):
            raise _CandidateRejected("EVIDENCE_INDEX_MISMATCH")
        if not isinstance(raw.get("redacted"), bool):
            raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
        _required_nonnegative_int(raw.get("redacted_fields"))
        for key in (
            "redaction_rule_version",
            "parser_version",
            "captured_at",
            "source",
            "source_name",
            "retention",
        ):
            _required_string(raw.get(key))
        try:
            document = load_json_object_bytes(
                file_bytes[artifact_path], label="Evidence", name=artifact_path
            )
        except Exception as exc:
            raise _CandidateRejected("INVALID_BUNDLE_JSON") from exc
        if document.get("schema_version") != "0.1":
            raise _CandidateRejected("BUNDLE_VERSION_UNSUPPORTED")
        if _required_string(document.get("evidence_type")) != evidence_type:
            raise _CandidateRejected("EVIDENCE_INDEX_MISMATCH")
        _required_string(document.get("source"))
        _required_string(document.get("captured_at"))
        if not isinstance(document.get("facts"), dict):
            raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
        if evidence_type == "runtime.bootstrap":
            try:
                validate_evidence(document, artifact_path)
            except Exception as exc:
                raise _CandidateRejected("INVALID_EVIDENCE_DOCUMENT") from exc
        attachments = raw.get("attachments")
        if not isinstance(attachments, list):
            raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
        for attachment_raw in attachments:
            if not isinstance(attachment_raw, dict):
                raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
            media_type = _required_string(attachment_raw.get("media_type"))
            if media_type not in SAFE_ATTACHMENT_TYPES:
                raise _CandidateRejected("UNSAFE_ATTACHMENT_TYPE")
            _required_string(attachment_raw.get("logical_name"))
            attachment_path = _safe_bundle_path(attachment_raw.get("path"))
            suffix = Path(attachment_path).suffix.lower()
            expected_suffixes = {
                "image/png": {".png"},
                "image/jpeg": {".jpg", ".jpeg"},
                "text/plain; charset=utf-8": {".txt"},
            }
            if suffix not in expected_suffixes[media_type]:
                raise _CandidateRejected("UNSAFE_ATTACHMENT_TYPE")
            if attachment_path in seen_attachments:
                raise _CandidateRejected("DUPLICATE_ATTACHMENT_PATH")
            seen_attachments.add(attachment_path)
            attachment = declared.get(attachment_path)
            if attachment is None:
                raise _CandidateRejected("MISSING_BUNDLE_REFERENCE")
            if attachment.sha256 != _required_sha256(attachment_raw.get("sha256")):
                raise _CandidateRejected("EVIDENCE_INDEX_MISMATCH")
            if attachment.size != _required_nonnegative_int(attachment_raw.get("size")):
                raise _CandidateRejected("EVIDENCE_INDEX_MISMATCH")
        if evidence_type == "runtime.bootstrap":
            references = {
                stream["attachment"]["path"]: stream["attachment"]
                for node in document["facts"]["nodes"]
                for stream in (node["stdout"], node["stderr"])
            }
            indexed = {item["path"]: item for item in attachments}
            expected_attachment_count = (
                2
                if document.get("source") == "VeriTrail bootstrap-lifecycle/0.3"
                else 4
            )
            if (
                len(references) != expected_attachment_count
                or set(references) != set(indexed)
            ):
                raise _CandidateRejected("BOOTSTRAP_ATTACHMENT_MISMATCH")
            for path, reference in references.items():
                item = indexed[path]
                if any(
                    canonical_json_bytes(reference.get(field))
                    != canonical_json_bytes(item.get(field))
                    for field in ("sha256", "size", "media_type", "logical_name")
                ):
                    raise _CandidateRejected("BOOTSTRAP_ATTACHMENT_MISMATCH")
    return created_at, execution_status, verdict, plan_id, plan_version, plan_sha256


def _validate_sealed_authorities(
    *,
    report: dict[str, Any],
    evidence: dict[str, Any],
    declared: dict[str, BundleFile],
    file_bytes: dict[str, bytes],
) -> str | None:
    try:
        plan = load_json_object_bytes(
            file_bytes["sealed-plan.json"], label="Sealed Plan", name="sealed-plan.json"
        )
    except Exception as exc:
        raise _CandidateRejected("INVALID_SEALED_PLAN") from exc
    profile: dict[str, Any] | None = None
    if plan.get("schema_version") in {"0.6", "0.7"}:
        if "sealed-profile.json" not in declared:
            raise _CandidateRejected("MISSING_SEALED_PROFILE")
        try:
            profile = load_json_object_bytes(
                file_bytes["sealed-profile.json"],
                label="Sealed ProjectProfile",
                name="sealed-profile.json",
            )
            verify_sealed_project_profile(profile)
            verify_sealed_plan(plan, profile)
        except Exception as exc:
            raise _CandidateRejected("INVALID_SEALED_AUTHORITY") from exc
    else:
        if "sealed-profile.json" in declared:
            raise _CandidateRejected("UNEXPECTED_SEALED_PROFILE")
        try:
            verify_sealed_plan(plan)
        except Exception as exc:
            raise _CandidateRejected("INVALID_SEALED_PLAN") from exc
    expected_report_plan = {
        "id": plan.get("plan_id"),
        "version": plan.get("version"),
        "sha256": plan.get("seal", {}).get("digest"),
    }
    if report.get("plan") != expected_report_plan:
        raise _CandidateRejected("SEALED_PLAN_REPORT_MISMATCH")
    imported: list[ImportedEvidence] = []
    evidence_documents: dict[str, dict[str, Any]] = {}
    for entry in evidence["artifacts"]:
        path = entry["path"]
        try:
            document = load_json_object_bytes(
                file_bytes[path], label="Evidence", name=path
            )
            validate_evidence(document, path)
        except Exception as exc:
            raise _CandidateRejected("INVALID_EVIDENCE_DOCUMENT") from exc
        evidence_documents[path] = document
        imported.append(
            ImportedEvidence(
                document=document,
                sha256=entry["sha256"],
                size=entry["size"],
                redacted_fields=entry["redacted_fields"],
                input_name=path,
            )
        )

    if profile is None:
        expected_result = evaluate(plan, imported, report["execution_status"])
        if any(
            canonical_json_bytes(report.get(field))
            != canonical_json_bytes(expected_result[field])
            for field in (
                "execution_status",
                "verdict",
                "reasons",
                "assertions",
                "missing_evidence",
                "contamination",
            )
        ):
            raise _CandidateRejected("REPORT_DERIVATION_MISMATCH")
        return None

    preflight_entries = [
        item
        for item in evidence["artifacts"]
        if item.get("evidence_type") == "runtime.preflight"
    ]
    if len(preflight_entries) != 1:
        raise _CandidateRejected("PREFLIGHT_EVIDENCE_CARDINALITY")
    preflight = evidence_documents[preflight_entries[0]["path"]]

    bootstrap_entries = [
        item
        for item in evidence["artifacts"]
        if item.get("evidence_type") == "runtime.bootstrap"
    ]
    browser_entries = [
        item for item in evidence["artifacts"] if item.get("evidence_type") == "browser.session"
    ]
    if preflight["facts"]["decision"] != "PROCEED":
        if report.get("execution_status") != "ABORTED":
            raise _CandidateRejected("PREFLIGHT_STATUS_CONFLICT")
        if bootstrap_entries:
            raise _CandidateRejected("BOOTSTRAP_EVIDENCE_CARDINALITY")
        if browser_entries:
            raise _CandidateRejected("BROWSER_EVIDENCE_CARDINALITY")
        if any(
            item.get("evidence_type") != "runtime.preflight"
            for item in evidence["artifacts"]
        ):
            raise _CandidateRejected("PREFLIGHT_EVIDENCE_APPLICABILITY")
        expected_result = evaluate(plan, imported, "ABORTED")
        if any(
            canonical_json_bytes(report.get(field))
            != canonical_json_bytes(expected_result[field])
            for field in (
                "execution_status",
                "verdict",
                "reasons",
                "assertions",
                "missing_evidence",
                "contamination",
            )
        ):
            raise _CandidateRejected("PREFLIGHT_REPORT_DERIVATION_MISMATCH")
        return profile["seal"]["digest"]

    if len(bootstrap_entries) != 1:
        raise _CandidateRejected("BOOTSTRAP_EVIDENCE_CARDINALITY")
    bootstrap = evidence_documents[bootstrap_entries[0]["path"]]
    facts = bootstrap["facts"]
    expected_profile = {
        "id": profile["profile_id"],
        "version": profile["version"],
        "sha256": profile["seal"]["digest"],
    }
    if (
        facts.get("plan_sha256") != plan["seal"]["digest"]
        or plan.get("bootstrap_profile")
        != {
            "profile_id": expected_profile["id"],
            "profile_version": expected_profile["version"],
            "profile_sha256": expected_profile["sha256"],
        }
        or facts.get("profile") != expected_profile
    ):
        raise _CandidateRejected("BOOTSTRAP_AUTHORITY_MISMATCH")
    profile_nodes = {node["node_id"]: node for node in profile["nodes"]}
    evidence_nodes = facts.get("nodes", [])
    if [node.get("node_id") for node in evidence_nodes] != profile["start_order"]:
        raise _CandidateRejected("BOOTSTRAP_AUTHORITY_MISMATCH")
    if any(
        node.get("policy_sha256") != sha256_json(profile_nodes[node["node_id"]])
        for node in evidence_nodes
    ):
        raise _CandidateRejected("BOOTSTRAP_AUTHORITY_MISMATCH")
    browser = facts["browser_exercise"]
    if browser["completed"] and (
        len(browser_entries) != 1
        or browser["evidence_sha256"] != browser_entries[0].get("sha256")
    ):
        raise _CandidateRejected("BOOTSTRAP_BROWSER_REFERENCE_MISMATCH")
    if not browser["completed"] and browser_entries:
        raise _CandidateRejected("BROWSER_EVIDENCE_CARDINALITY")
    expected_result = evaluate(plan, imported, report["execution_status"])
    if any(
        item.get("code") == "BOOTSTRAP_STATUS_CONFLICT"
        for item in expected_result["contamination"]
    ):
        raise _CandidateRejected("BOOTSTRAP_STATUS_CONFLICT")
    if any(
        canonical_json_bytes(report.get(field))
        != canonical_json_bytes(expected_result[field])
        for field in (
            "execution_status",
            "verdict",
            "reasons",
            "assertions",
            "missing_evidence",
            "contamination",
        )
    ):
        raise _CandidateRejected("BOOTSTRAP_REPORT_DERIVATION_MISMATCH")
    return profile["seal"]["digest"]


def validate_bundle(
    candidate: Path, artifact_root: Path, *, retain_snapshot: bool = False
) -> ValidatedBundle:
    root = artifact_root.resolve(strict=True)
    source_relative = candidate.relative_to(artifact_root).as_posix()
    metadata = os.lstat(candidate)
    if _is_reparse(metadata) or candidate.is_symlink() or not stat.S_ISDIR(metadata.st_mode):
        raise _CandidateRejected("UNSAFE_CANDIDATE")
    resolved_candidate = candidate.resolve(strict=True)
    if not _is_relative_to(resolved_candidate, root):
        raise _CandidateRejected("BUNDLE_ROOT_ESCAPE")
    files = _collect_regular_files(candidate, root)
    if "bundle-manifest.json" not in files:
        raise _CandidateRejected("MISSING_BUNDLE_MANIFEST")
    file_bytes = {path: _read_stable_file(value) for path, value in files.items()}
    try:
        manifest = load_json_object_bytes(
            file_bytes["bundle-manifest.json"],
            label="Bundle Manifest",
            name="bundle-manifest.json",
        )
    except Exception as exc:
        raise _CandidateRejected("INVALID_BUNDLE_JSON") from exc
    run_id, declared_files = _parse_bundle_manifest(manifest)
    declared = {entry.path: entry for entry in declared_files}
    if set(files) != set(declared) | {"bundle-manifest.json"}:
        raise _CandidateRejected("BUNDLE_FILE_SET_MISMATCH")
    for entry in declared_files:
        content = file_bytes[entry.path]
        if len(content) != entry.size:
            raise _CandidateRejected("BUNDLE_SIZE_MISMATCH")
        if sha256_bytes(content) != entry.sha256:
            raise _CandidateRejected("BUNDLE_HASH_MISMATCH")
    try:
        report = load_json_object_bytes(
            file_bytes["report.json"], label="Report", name="report.json"
        )
        evidence = load_json_object_bytes(
            file_bytes["evidence-manifest.json"],
            label="Evidence Manifest",
            name="evidence-manifest.json",
        )
    except Exception as exc:
        raise _CandidateRejected("INVALID_BUNDLE_JSON") from exc
    created_at, execution_status, verdict, plan_id, plan_version, plan_sha256 = (
        _validate_report_and_evidence(report, evidence, run_id, declared, file_bytes)
    )
    profile_sha256 = _validate_sealed_authorities(
        report=report,
        evidence=evidence,
        declared=declared,
        file_bytes=file_bytes,
    )
    bundle_sha256 = sha256_json(
        {
            "schema_version": "0.1",
            "run_id": run_id,
            "files": [
                {"path": item.path, "sha256": item.sha256, "size": item.size}
                for item in declared_files
            ],
        }
    )
    all_files = tuple(
        list(declared_files)
        + [
            BundleFile(
                path="bundle-manifest.json",
                sha256=sha256_bytes(file_bytes["bundle-manifest.json"]),
                size=len(file_bytes["bundle-manifest.json"]),
            )
        ]
    )
    return ValidatedBundle(
        source_relative=source_relative,
        run_id=run_id,
        created_at=created_at,
        execution_status=execution_status,
        verdict=verdict,
        plan_id=plan_id,
        plan_version=plan_version,
        plan_sha256=plan_sha256,
        profile_sha256=profile_sha256,
        bundle_sha256=bundle_sha256,
        files=tuple(sorted(all_files, key=lambda item: item.path)),
        total_bytes=sum(item.size for item in all_files),
        owned_files=(
            tuple(sorted(file_bytes.items())) if retain_snapshot else ()
        ),
    )


def _retained_bundle_bytes(bundle: ValidatedBundle) -> int:
    strings = (
        bundle.source_relative,
        bundle.run_id,
        bundle.created_at,
        bundle.execution_status,
        bundle.verdict,
        bundle.plan_id,
        bundle.plan_sha256,
        bundle.profile_sha256 or "",
        bundle.bundle_sha256,
        *(item.path for item in bundle.files),
        *(item.sha256 for item in bundle.files),
    )
    try:
        return sum(len(value.encode("utf-8")) for value in strings)
    except UnicodeError as exc:
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE") from exc


def _scan_bundles(artifact_root: Path) -> tuple[list[ValidatedBundle], list[CatalogIssue]]:
    try:
        root_metadata = os.lstat(artifact_root)
    except OSError as exc:
        raise CatalogError("ARTIFACT_ROOT_UNAVAILABLE", "Artifact 根目录不可用。") from exc
    if artifact_root.is_symlink() or _is_reparse(root_metadata) or not stat.S_ISDIR(root_metadata.st_mode):
        raise CatalogError("UNSAFE_ARTIFACT_ROOT", "Artifact 根目录必须是普通本地目录。")
    candidates: list[Path] = []
    try:
        for entry in sorted(os.scandir(artifact_root), key=lambda item: item.name):
            metadata = os.lstat(entry.path)
            if entry.is_symlink() or _is_reparse(metadata) or stat.S_ISDIR(metadata.st_mode):
                candidates.append(Path(entry.path))
    except OSError as exc:
        raise CatalogError("ARTIFACT_ROOT_UNAVAILABLE", "Artifact 根目录不可读取。") from exc
    if len(candidates) > MAX_CANDIDATES:
        raise CatalogError("CATALOG_CANDIDATE_LIMIT", "候选 Bundle 数量超过 1000 个上限。")
    bundles: list[ValidatedBundle] = []
    issues: list[CatalogIssue] = []
    retained_bytes = 0
    for candidate in candidates:
        source_relative = candidate.relative_to(artifact_root).as_posix()
        try:
            bundle = validate_bundle(candidate, artifact_root)
            retained_bytes += _retained_bundle_bytes(bundle)
            if retained_bytes > MAX_CATALOG_RETAINED_BYTES:
                raise CatalogError(
                    "CATALOG_METADATA_BUDGET",
                    "Catalog 保留元数据超过安全预算。",
                )
            bundles.append(bundle)
        except _CandidateRejected as exc:
            issues.append(CatalogIssue(exc.code, _candidate_id(source_relative)))
        except OSError:
            issues.append(CatalogIssue("BUNDLE_UNREADABLE", _candidate_id(source_relative)))
    return bundles, issues


def _resolve_runs(
    bundles: Iterable[ValidatedBundle], issues: list[CatalogIssue]
) -> tuple[list[CatalogRun], list[CatalogIssue]]:
    by_run: dict[str, list[ValidatedBundle]] = {}
    for bundle in bundles:
        by_run.setdefault(bundle.run_id, []).append(bundle)
    runs: list[CatalogRun] = []
    for run_id in sorted(by_run):
        candidates = sorted(by_run[run_id], key=lambda item: (item.bundle_sha256, item.source_relative))
        digests = sorted({item.bundle_sha256 for item in candidates})
        if len(digests) > 1:
            issues.append(
                CatalogIssue(
                    code="DUPLICATE_RUN_CONFLICT",
                    candidate_id="cand_" + sha256_json({"run_id": run_id, "digests": digests})[:20],
                    run_id=run_id,
                    bundle_digests=tuple(digests),
                    occurrence_count=len(candidates),
                )
            )
            continue
        representative = candidates[0]
        catalog_run_id = "cr_" + sha256_json(
            {"run_id": run_id, "bundle_sha256": representative.bundle_sha256}
        )[:24]
        runs.append(
            CatalogRun(
                bundle=representative,
                catalog_run_id=catalog_run_id,
                duplicate_count=len(candidates) - 1,
            )
        )
    return runs, issues


def _bundle_set_sha256(runs: list[CatalogRun], issues: list[CatalogIssue]) -> str:
    return sha256_json(
        {
            "schema_version": CATALOG_SCHEMA_VERSION,
            "runs": [
                {
                    "run_id": run.bundle.run_id,
                    "bundle_sha256": run.bundle.bundle_sha256,
                    "duplicate_count": run.duplicate_count,
                }
                for run in sorted(runs, key=lambda item: item.catalog_run_id)
            ],
            "issues": [
                {
                    "code": issue.code,
                    "run_id": issue.run_id,
                    "bundle_digests": list(issue.bundle_digests),
                    "occurrence_count": issue.occurrence_count,
                }
                for issue in sorted(
                    issues,
                    key=lambda item: (
                        item.code,
                        item.run_id or "",
                        item.bundle_digests,
                        item.occurrence_count,
                    ),
                )
            ],
        }
    )


def _create_database(
    path: Path,
    *,
    catalog_id: str,
    bundle_set_sha256: str,
    root_binding: str,
    runs: list[CatalogRun],
    issues: list[CatalogIssue],
) -> None:
    connection = sqlite3.connect(path)
    try:
        connection.executescript(CATALOG_SCHEMA_SQL)
        metadata = {
            "schema_version": CATALOG_SCHEMA_VERSION,
            "api_version": CATALOG_API_VERSION,
            "catalog_id": catalog_id,
            "bundle_set_sha256": bundle_set_sha256,
            "artifact_root_binding": root_binding,
            "tool_version": __version__,
        }
        connection.executemany(
            "INSERT INTO catalog_meta(key, value) VALUES (?, ?)", sorted(metadata.items())
        )
        for run in sorted(runs, key=lambda item: item.catalog_run_id):
            bundle = run.bundle
            connection.execute(
                """
                INSERT INTO catalog_runs(
                    catalog_run_id, run_id, created_at, execution_status, verdict,
                    plan_id, plan_version, plan_sha256, bundle_sha256, file_count,
                    total_bytes, duplicate_count, source_relative
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.catalog_run_id,
                    bundle.run_id,
                    bundle.created_at,
                    bundle.execution_status,
                    bundle.verdict,
                    bundle.plan_id,
                    bundle.plan_version,
                    bundle.plan_sha256,
                    bundle.bundle_sha256,
                    len(bundle.files),
                    bundle.total_bytes,
                    run.duplicate_count,
                    bundle.source_relative,
                ),
            )
            connection.executemany(
                "INSERT INTO catalog_files(catalog_run_id, path, sha256, size) VALUES (?, ?, ?, ?)",
                [
                    (run.catalog_run_id, item.path, item.sha256, item.size)
                    for item in bundle.files
                ],
            )
        connection.executemany(
            """
            INSERT INTO catalog_issues(
                issue_id, code, candidate_id, run_id, bundle_digests_json, occurrence_count
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    issue.issue_id,
                    issue.code,
                    issue.candidate_id,
                    issue.run_id,
                    canonical_json_bytes(list(issue.bundle_digests)).decode("utf-8"),
                    issue.occurrence_count,
                )
                for issue in sorted(issues, key=lambda item: item.issue_id)
            ],
        )
        connection.commit()
        connection.execute("VACUUM")
    finally:
        connection.close()


CATALOG_META_KEYS = {
    "schema_version",
    "api_version",
    "catalog_id",
    "bundle_set_sha256",
    "artifact_root_binding",
    "tool_version",
}
CATALOG_TABLE_QUERIES = {
    "meta": "SELECT key, value FROM catalog_meta ORDER BY key",
    "runs": """
        SELECT catalog_run_id, run_id, created_at, execution_status, verdict,
               plan_id, plan_version, plan_sha256, bundle_sha256, file_count,
               total_bytes, duplicate_count, source_relative
        FROM catalog_runs ORDER BY catalog_run_id
    """,
    "files": """
        SELECT catalog_run_id, path, sha256, size
        FROM catalog_files ORDER BY catalog_run_id, path
    """,
    "issues": """
        SELECT issue_id, code, candidate_id, run_id, bundle_digests_json,
               occurrence_count
        FROM catalog_issues ORDER BY issue_id
    """,
}


def _normalized_schema_sql(value: str | None) -> str | None:
    return None if value is None else " ".join(value.split())


def _schema_signature(connection: sqlite3.Connection) -> tuple[tuple[Any, ...], ...]:
    return tuple(
        (row[0], row[1], row[2], _normalized_schema_sql(row[3]))
        for row in connection.execute(
            "SELECT type, name, tbl_name, sql FROM sqlite_schema ORDER BY type, name, tbl_name"
        )
    )


def _expected_schema_signature() -> tuple[tuple[Any, ...], ...]:
    expected = sqlite3.connect(":memory:")
    try:
        expected.executescript(CATALOG_SCHEMA_SQL)
        return _schema_signature(expected)
    finally:
        expected.close()


def _catalog_rows(connection: sqlite3.Connection) -> dict[str, list[tuple[Any, ...]]]:
    return {
        name: [tuple(row) for row in connection.execute(query)]
        for name, query in CATALOG_TABLE_QUERIES.items()
    }


def _catalog_logical_sha256(rows: dict[str, list[tuple[Any, ...]]]) -> str:
    return sha256_json(
        {
            "schema_version": CATALOG_SCHEMA_VERSION,
            "meta": rows["meta"],
            "runs": rows["runs"],
            "files": rows["files"],
            "issues": rows["issues"],
        }
    )


def _database_logical_sha256(path: Path) -> str:
    connection = sqlite3.connect(f"file:{path.as_posix()}?mode=ro&immutable=1", uri=True)
    try:
        return _catalog_logical_sha256(_catalog_rows(connection))
    finally:
        connection.close()


def _catalog_text(value: Any, *, maximum: int, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value:
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库包含无效文本字段。")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeError as exc:
        raise CatalogError(
            "CATALOG_DATABASE_INVALID", "Catalog 数据库包含无效 Unicode 文本。"
        ) from exc
    if size > maximum:
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库文本字段超过安全上限。")
    return value


def _catalog_nonnegative_int(value: Any, *, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库包含无效数值字段。")
    return value


def _validate_catalog_database(
    connection: sqlite3.Connection, manifest: dict[str, Any]
) -> dict[str, list[tuple[Any, ...]]]:
    expected_schema = _expected_schema_signature()
    schema_count = connection.execute("SELECT COUNT(*) FROM sqlite_schema").fetchone()[0]
    if schema_count != len(expected_schema) or _schema_signature(connection) != expected_schema:
        raise CatalogError(
            "CATALOG_DATABASE_SCHEMA_REJECTED",
            "Catalog 数据库结构不在精确允许清单中。",
        )
    integrity = connection.execute("PRAGMA integrity_check(1)").fetchone()
    if integrity is None or integrity[0] != "ok":
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库完整性校验失败。")
    if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库引用完整性校验失败。")

    counts = {
        "meta": connection.execute("SELECT COUNT(*) FROM catalog_meta").fetchone()[0],
        "runs": connection.execute("SELECT COUNT(*) FROM catalog_runs").fetchone()[0],
        "files": connection.execute("SELECT COUNT(*) FROM catalog_files").fetchone()[0],
        "issues": connection.execute("SELECT COUNT(*) FROM catalog_issues").fetchone()[0],
    }
    if (
        counts["meta"] != len(CATALOG_META_KEYS)
        or counts["runs"] != manifest["run_count"]
        or counts["issues"] != manifest["issue_count"]
        or counts["runs"] > MAX_CANDIDATES
        or counts["issues"] > MAX_CANDIDATES
        or counts["files"] > MAX_CANDIDATES * MAX_FILES
    ):
        raise CatalogError("CATALOG_DATABASE_LIMIT", "Catalog 数据库行数或声明计数无效。")

    length_checks = (
        (
            "SELECT MAX(length(CAST(key AS BLOB))), "
            "MAX(length(CAST(value AS BLOB))) FROM catalog_meta",
            (64, MAX_IMPORTED_STRING_BYTES),
        ),
        (
            """
            SELECT MAX(length(CAST(catalog_run_id AS BLOB))),
                   MAX(length(CAST(run_id AS BLOB))),
                   MAX(length(CAST(created_at AS BLOB))),
                   MAX(length(CAST(execution_status AS BLOB))),
                   MAX(length(CAST(verdict AS BLOB))),
                   MAX(length(CAST(plan_id AS BLOB))),
                   MAX(length(CAST(plan_sha256 AS BLOB))),
                   MAX(length(CAST(bundle_sha256 AS BLOB))),
                   MAX(length(CAST(source_relative AS BLOB)))
            FROM catalog_runs
            """,
            (27, 64, 128, 16, 16, 64, 64, 64, MAX_BUNDLE_PATH_BYTES),
        ),
        (
            "SELECT MAX(length(CAST(catalog_run_id AS BLOB))), "
            "MAX(length(CAST(path AS BLOB))), "
            "MAX(length(CAST(sha256 AS BLOB))) FROM catalog_files",
            (27, MAX_BUNDLE_PATH_BYTES, 64),
        ),
        (
            """
            SELECT MAX(length(CAST(issue_id AS BLOB))),
                   MAX(length(CAST(code AS BLOB))),
                   MAX(length(CAST(candidate_id AS BLOB))),
                   MAX(length(CAST(run_id AS BLOB))),
                   MAX(length(CAST(bundle_digests_json AS BLOB)))
            FROM catalog_issues
            """,
            (27, 128, 25, 64, MAX_IMPORTED_STRING_BYTES),
        ),
    )
    for query, limits in length_checks:
        observed = connection.execute(query).fetchone()
        if observed is None or any(
            value is not None and (not isinstance(value, int) or value > limit)
            for value, limit in zip(observed, limits)
        ):
            raise CatalogError(
                "CATALOG_DATABASE_LIMIT", "Catalog 数据库字段长度超过安全上限。"
            )

    rows = _catalog_rows(connection)
    metadata = dict(rows["meta"])
    expected_metadata = {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "api_version": CATALOG_API_VERSION,
        "catalog_id": manifest["catalog_id"],
        "bundle_set_sha256": manifest["bundle_set_sha256"],
        "artifact_root_binding": manifest["artifact_root_binding"],
        "tool_version": manifest["tool_version"],
    }
    if set(metadata) != CATALOG_META_KEYS or metadata != expected_metadata:
        raise CatalogError("CATALOG_DATABASE_METADATA_MISMATCH", "Catalog 数据库元数据不一致。")
    for key, value in rows["meta"]:
        _catalog_text(key, maximum=64)
        _catalog_text(value, maximum=MAX_IMPORTED_STRING_BYTES)

    run_files: dict[str, tuple[int, int]] = {}
    duplicate_count = 0
    for row in rows["runs"]:
        (
            catalog_run_id,
            run_id,
            created_at,
            execution_status,
            verdict,
            plan_id,
            plan_version,
            plan_sha256,
            bundle_sha256,
            file_count,
            total_bytes,
            duplicates,
            source_relative,
        ) = row
        if not isinstance(catalog_run_id, str) or not re.fullmatch(r"cr_[0-9a-f]{24}", catalog_run_id):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Run 标识无效。")
        if not isinstance(run_id, str) or not RUN_ID_PATTERN.fullmatch(run_id):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Run ID 无效。")
        _catalog_text(created_at, maximum=128)
        try:
            datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Run 时间无效。") from exc
        if execution_status not in EXECUTION_STATUSES or verdict not in VERDICTS:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Run 状态无效。")
        if not isinstance(plan_id, str) or not RUN_ID_PATTERN.fullmatch(plan_id):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Plan ID 无效。")
        _catalog_nonnegative_int(plan_version, maximum=2**31 - 1)
        if not isinstance(plan_sha256, str) or not SHA256_PATTERN.fullmatch(plan_sha256):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Plan 摘要无效。")
        if not isinstance(bundle_sha256, str) or not SHA256_PATTERN.fullmatch(bundle_sha256):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Bundle 摘要无效。")
        file_count = _catalog_nonnegative_int(file_count, maximum=MAX_FILES)
        if file_count == 0:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Bundle 文件计数无效。")
        total_bytes = _catalog_nonnegative_int(total_bytes, maximum=MAX_BUNDLE_BYTES)
        duplicates = _catalog_nonnegative_int(duplicates, maximum=MAX_CANDIDATES)
        try:
            _safe_bundle_path(_catalog_text(source_relative, maximum=MAX_BUNDLE_PATH_BYTES))
        except _CandidateRejected as exc:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 来源路径无效。") from exc
        run_files[catalog_run_id] = (file_count, total_bytes)
        duplicate_count += duplicates

    observed_files: dict[str, tuple[int, int]] = {
        catalog_run_id: (0, 0) for catalog_run_id in run_files
    }
    for catalog_run_id, path, digest, size in rows["files"]:
        if catalog_run_id not in observed_files:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 文件引用未知 Run。")
        try:
            _safe_bundle_path(path)
        except _CandidateRejected as exc:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 文件路径无效。") from exc
        if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 文件摘要无效。")
        size = _catalog_nonnegative_int(size, maximum=MAX_FILE_BYTES)
        count, total = observed_files[catalog_run_id]
        observed_files[catalog_run_id] = (count + 1, total + size)
    if observed_files != run_files or duplicate_count != manifest["duplicate_count"]:
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 文件或重复项计数不一致。")

    for issue_id, code, candidate_id, run_id, digests_json, occurrence_count in rows["issues"]:
        if not isinstance(issue_id, str) or not re.fullmatch(r"ci_[0-9a-f]{24}", issue_id):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Issue 标识无效。")
        if not isinstance(candidate_id, str) or not re.fullmatch(r"cand_[0-9a-f]{20}", candidate_id):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Candidate 标识无效。")
        _catalog_text(code, maximum=128)
        if run_id is not None and (not isinstance(run_id, str) or not RUN_ID_PATTERN.fullmatch(run_id)):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Issue Run ID 无效。")
        _catalog_text(digests_json, maximum=MAX_IMPORTED_STRING_BYTES)
        try:
            digests = json.loads(digests_json)
        except (TypeError, ValueError) as exc:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Issue 摘要列表无效。") from exc
        if (
            not isinstance(digests, list)
            or len(digests) > MAX_CANDIDATES
            or any(not isinstance(item, str) or not SHA256_PATTERN.fullmatch(item) for item in digests)
            or canonical_json_bytes(digests).decode("utf-8") != digests_json
        ):
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Issue 摘要列表无效。")
        occurrence_count = _catalog_nonnegative_int(occurrence_count, maximum=MAX_CANDIDATES)
        if occurrence_count == 0:
            raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog Issue 次数无效。")

    expected_logical = manifest["database"]["logical_sha256"]
    if _catalog_logical_sha256(rows) != expected_logical:
        raise CatalogError(
            "CATALOG_DATABASE_LOGICAL_MISMATCH", "Catalog 数据库逻辑摘要与 Manifest 不一致。"
        )
    return rows


def _copy_catalog_rows(
    destination: sqlite3.Connection, rows: dict[str, list[tuple[Any, ...]]]
) -> None:
    destination.executemany("INSERT INTO catalog_meta(key, value) VALUES (?, ?)", rows["meta"])
    destination.executemany(
        """
        INSERT INTO catalog_runs(
            catalog_run_id, run_id, created_at, execution_status, verdict,
            plan_id, plan_version, plan_sha256, bundle_sha256, file_count,
            total_bytes, duplicate_count, source_relative
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows["runs"],
    )
    destination.executemany(
        "INSERT INTO catalog_files(catalog_run_id, path, sha256, size) VALUES (?, ?, ?, ?)",
        rows["files"],
    )
    destination.executemany(
        """
        INSERT INTO catalog_issues(
            issue_id, code, candidate_id, run_id, bundle_digests_json, occurrence_count
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows["issues"],
    )
    destination.commit()


def build_catalog(artifact_root: Path, output: Path) -> CatalogBuildResult:
    artifact_root = artifact_root.absolute()
    output = output.absolute()
    if output.exists():
        raise CatalogError("CATALOG_OUTPUT_EXISTS", "拒绝覆盖已有 Catalog 输出目录。")
    bundles, initial_issues = _scan_bundles(artifact_root)
    runs, issues = _resolve_runs(bundles, initial_issues)
    issues = sorted(issues, key=lambda item: item.issue_id)
    bundle_set_sha256 = _bundle_set_sha256(runs, issues)
    catalog_id = "cat_" + bundle_set_sha256[:24]
    status = "COMPLETED_WITH_ISSUES" if issues else "COMPLETED"
    duplicate_count = sum(run.duplicate_count for run in runs)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".veritrail-catalog-", dir=output.parent))
    try:
        database = stage / "catalog.sqlite3"
        _create_database(
            database,
            catalog_id=catalog_id,
            bundle_set_sha256=bundle_set_sha256,
            root_binding=_root_binding(artifact_root),
            runs=runs,
            issues=issues,
        )
        database_size = database.stat().st_size
        database_sha256 = _sha256_file(database)
        database_logical_sha256 = _database_logical_sha256(database)
        manifest = {
            "schema_version": CATALOG_SCHEMA_VERSION,
            "api_version": CATALOG_API_VERSION,
            "catalog_id": catalog_id,
            "bundle_set_sha256": bundle_set_sha256,
            "artifact_root_binding": _root_binding(artifact_root),
            "build_status": status,
            "run_count": len(runs),
            "issue_count": len(issues),
            "duplicate_count": duplicate_count,
            "database": {
                "name": "catalog.sqlite3",
                "sha256": database_sha256,
                "logical_sha256": database_logical_sha256,
                "size": database_size,
            },
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "tool_version": __version__,
        }
        (stage / "catalog-manifest.json").write_bytes(canonical_json_bytes(manifest) + b"\n")
        publish_staged_directory(stage, output)
    except CatalogError:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return CatalogBuildResult(
        status=status,
        catalog_id=catalog_id,
        run_count=len(runs),
        issue_count=len(issues),
        duplicate_count=duplicate_count,
        bundle_set_sha256=bundle_set_sha256,
    )


def load_catalog_snapshot(catalog_root: Path) -> tuple[dict[str, Any], bytes]:
    manifest_path = catalog_root / "catalog-manifest.json"
    try:
        manifest = load_json_object(
            manifest_path, label="Catalog Manifest", max_bytes=1024 * 1024
        )
    except Exception as exc:
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 不可读取或无效。") from exc
    if manifest.get("schema_version") != CATALOG_SCHEMA_VERSION:
        raise CatalogError("CATALOG_VERSION_UNSUPPORTED", "Catalog 版本不受支持。")
    if manifest.get("api_version") != CATALOG_API_VERSION:
        raise CatalogError("CATALOG_VERSION_UNSUPPORTED", "Catalog API 版本不受支持。")
    if not isinstance(manifest.get("catalog_id"), str) or not re.fullmatch(
        r"cat_[0-9a-f]{24}", manifest["catalog_id"]
    ):
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 标识无效。")
    for field in ("bundle_set_sha256", "artifact_root_binding"):
        if not isinstance(manifest.get(field), str) or not SHA256_PATTERN.fullmatch(manifest[field]):
            raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 摘要无效。")
    if manifest.get("build_status") not in {"COMPLETED", "COMPLETED_WITH_ISSUES"}:
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 构建状态无效。")
    for field in ("run_count", "issue_count", "duplicate_count"):
        if isinstance(manifest.get(field), bool) or not isinstance(manifest.get(field), int) or manifest[field] < 0:
            raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 计数无效。")
        if manifest[field] > MAX_CANDIDATES:
            raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 计数超过安全上限。")
    if not isinstance(manifest.get("generated_at"), str) or not isinstance(
        manifest.get("tool_version"), str
    ):
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 构建事实无效。")
    database = manifest.get("database")
    if (
        not isinstance(database, dict)
        or set(database) != {"name", "sha256", "logical_sha256", "size"}
        or database.get("name") != "catalog.sqlite3"
    ):
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 数据库声明无效。")
    if (
        not isinstance(database.get("sha256"), str)
        or not SHA256_PATTERN.fullmatch(database["sha256"])
        or not isinstance(database.get("logical_sha256"), str)
        or not SHA256_PATTERN.fullmatch(database["logical_sha256"])
        or isinstance(database.get("size"), bool)
        or not isinstance(database.get("size"), int)
        or database["size"] <= 0
        or database["size"] > MAX_CATALOG_DATABASE_BYTES
    ):
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 数据库摘要无效。")
    try:
        database_bytes = read_stable_bytes(
            catalog_root / "catalog.sqlite3",
            label="Catalog database",
            max_bytes=MAX_CATALOG_DATABASE_BYTES,
        )
    except Exception as exc:
        raise CatalogError("CATALOG_DATABASE_UNAVAILABLE", "Catalog 数据库不可用。") from exc
    if len(database_bytes) != database.get("size") or sha256_bytes(database_bytes) != database.get(
        "sha256"
    ):
        raise CatalogError("CATALOG_DATABASE_CHANGED", "Catalog 数据库与 Manifest 不一致。")
    return manifest, database_bytes


def load_catalog_manifest(catalog_root: Path) -> dict[str, Any]:
    manifest, _ = load_catalog_snapshot(catalog_root)
    return manifest


class CatalogSnapshotConnection(sqlite3.Connection):
    """Query-only connection containing only copied, validated Catalog rows."""

    _snapshot_path: Path | None = None

    def close(self) -> None:
        snapshot = self._snapshot_path
        self._snapshot_path = None
        try:
            super().close()
        finally:
            if snapshot is not None:
                try:
                    snapshot.unlink(missing_ok=True)
                    snapshot.parent.rmdir()
                except OSError:
                    shutil.rmtree(snapshot.parent, ignore_errors=True)


def open_catalog_snapshot_bytes(
    database_bytes: bytes,
    *,
    manifest: dict[str, Any],
    check_same_thread: bool = True,
) -> CatalogSnapshotConnection:
    if not database_bytes or len(database_bytes) > MAX_CATALOG_DATABASE_BYTES:
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库快照大小无效。")
    directory = Path(tempfile.mkdtemp(prefix="veritrail-catalog-snapshot-"))
    database = directory / "catalog.sqlite3"
    source: sqlite3.Connection | None = None
    trusted: CatalogSnapshotConnection | None = None
    try:
        with database.open("xb") as handle:
            handle.write(database_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        source = sqlite3.connect(
            f"file:{database.as_posix()}?mode=ro&immutable=1",
            uri=True,
        )
        source.execute("PRAGMA query_only = ON")
        rows = _validate_catalog_database(source, manifest)

        trusted = sqlite3.connect(
            ":memory:",
            check_same_thread=check_same_thread,
            factory=CatalogSnapshotConnection,
        )
        trusted.executescript(CATALOG_SCHEMA_SQL)
        _copy_catalog_rows(trusted, rows)
        trusted.row_factory = sqlite3.Row
        trusted.execute("PRAGMA query_only = ON")
        return trusted
    except CatalogError:
        if trusted is not None:
            trusted.close()
        raise
    except sqlite3.Error as exc:
        if trusted is not None:
            trusted.close()
        raise CatalogError("CATALOG_DATABASE_INVALID", "Catalog 数据库内容无效。") from exc
    except Exception:
        if trusted is not None:
            trusted.close()
        raise
    finally:
        if source is not None:
            source.close()
        shutil.rmtree(directory, ignore_errors=True)


def open_catalog_readonly(catalog_root: Path) -> sqlite3.Connection:
    manifest, database_bytes = load_catalog_snapshot(catalog_root)
    return open_catalog_snapshot_bytes(database_bytes, manifest=manifest)
