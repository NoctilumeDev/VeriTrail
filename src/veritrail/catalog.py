from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import stat
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from veritrail import __version__
from veritrail.canonical import canonical_json_bytes, sha256_bytes, sha256_json
from veritrail.evidence import ImportedEvidence, validate_evidence
from veritrail.errors import VeriTrailError
from veritrail.jsonio import load_json_object, load_json_object_bytes
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.verdict import evaluate

CATALOG_SCHEMA_VERSION = "0.1"
CATALOG_API_VERSION = "0.1"
MAX_CANDIDATES = 1000
MAX_FILES = 256
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_BUNDLE_BYTES = 64 * 1024 * 1024
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
EXECUTION_STATUSES = {"PLANNED", "RUNNING", "COMPLETED", "ABORTED", "ERROR"}
VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE", "PENDING"}
SAFE_ATTACHMENT_TYPES = {
    "image/png",
    "image/jpeg",
    "text/plain; charset=utf-8",
}
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


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
    return "/".join(parts)


def _required_string(value: Any) -> str:
    if not isinstance(value, str) or not value:
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
    return "cand_" + sha256_bytes(source_relative.encode("utf-8"))[:20]


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
    run_id = _required_string(value.get("run_id"))
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
    report_run_id = _required_string(report.get("run_id"))
    evidence_run_id = _required_string(evidence.get("run_id"))
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
    plan_id = _required_string(plan.get("id"))
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
    if canonical_json_bytes(report_artifacts) != canonical_json_bytes(evidence_artifacts):
        raise _CandidateRejected("EVIDENCE_INDEX_MISMATCH")
    duplicates = evidence.get("duplicate_inputs_ignored")
    if not isinstance(duplicates, list):
        raise _CandidateRejected("INVALID_BUNDLE_STRUCTURE")
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
            if len(references) != 4 or set(references) != set(indexed):
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
    if plan.get("schema_version") == "0.6":
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


def validate_bundle(candidate: Path, artifact_root: Path) -> ValidatedBundle:
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
    )


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
    for candidate in candidates:
        source_relative = candidate.relative_to(artifact_root).as_posix()
        try:
            bundles.append(validate_bundle(candidate, artifact_root))
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
        connection.executescript(
            """
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
                run_id TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                execution_status TEXT NOT NULL CHECK (execution_status IN ('PLANNED','RUNNING','COMPLETED','ABORTED','ERROR')),
                verdict TEXT NOT NULL CHECK (verdict IN ('PASS','FAIL','INCONCLUSIVE','PENDING')),
                plan_id TEXT NOT NULL,
                plan_version INTEGER NOT NULL CHECK (plan_version >= 0),
                plan_sha256 TEXT NOT NULL CHECK (length(plan_sha256) = 64),
                bundle_sha256 TEXT NOT NULL CHECK (length(bundle_sha256) = 64),
                file_count INTEGER NOT NULL CHECK (file_count > 0 AND file_count <= 256),
                total_bytes INTEGER NOT NULL CHECK (total_bytes >= 0 AND total_bytes <= 67108864),
                duplicate_count INTEGER NOT NULL CHECK (duplicate_count >= 0),
                source_relative TEXT NOT NULL UNIQUE
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
        )
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
                "size": database_size,
            },
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "tool_version": __version__,
        }
        (stage / "catalog-manifest.json").write_bytes(canonical_json_bytes(manifest) + b"\n")
        stage.rename(output)
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


def load_catalog_manifest(catalog_root: Path) -> dict[str, Any]:
    manifest_path = catalog_root / "catalog-manifest.json"
    try:
        manifest = load_json_object(manifest_path, label="Catalog Manifest")
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
    if not isinstance(manifest.get("generated_at"), str) or not isinstance(
        manifest.get("tool_version"), str
    ):
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 构建事实无效。")
    database = manifest.get("database")
    if not isinstance(database, dict) or database.get("name") != "catalog.sqlite3":
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 数据库声明无效。")
    if (
        not isinstance(database.get("sha256"), str)
        or not SHA256_PATTERN.fullmatch(database["sha256"])
        or isinstance(database.get("size"), bool)
        or not isinstance(database.get("size"), int)
        or database["size"] <= 0
    ):
        raise CatalogError("CATALOG_MANIFEST_INVALID", "Catalog Manifest 数据库摘要无效。")
    database_path = catalog_root / "catalog.sqlite3"
    try:
        size = database_path.stat().st_size
    except OSError as exc:
        raise CatalogError("CATALOG_DATABASE_UNAVAILABLE", "Catalog 数据库不可用。") from exc
    if size != database.get("size") or _sha256_file(database_path) != database.get("sha256"):
        raise CatalogError("CATALOG_DATABASE_CHANGED", "Catalog 数据库与 Manifest 不一致。")
    return manifest


def open_catalog_readonly(catalog_root: Path) -> sqlite3.Connection:
    database = (catalog_root / "catalog.sqlite3").resolve(strict=True)
    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro&immutable=1", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    return connection
