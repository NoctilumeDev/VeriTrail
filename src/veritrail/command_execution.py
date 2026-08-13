from __future__ import annotations

import codecs
import hashlib
import os
import re
import stat
import tempfile
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from veritrail.canonical import sha256_bytes, sha256_json
from veritrail.command_preview import ResolvedCommand, resolve_command
from veritrail.evidence import (
    EvidenceAttachment,
    ImportedEvidence,
    create_text_attachment,
    import_evidence_document,
)
from veritrail.errors import SafetyError, ValidationError
from veritrail.privacy import redact_string
from veritrail.resources import MEBIBYTE, process_rss_bytes
from veritrail.windows_job import CapturedStream, OwnedProcessResult, run_owned_process

COLLECTOR_VERSION = "trusted-command/0.1"
OWNERSHIP_BACKEND = "WINDOWS_JOB_OBJECT_PYWIN32_312"
RUN_WORK_PREFIX = ".veritrail-run-work-"
OUTPUT_REDACTION_CHUNK_BYTES = 4096
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
WINDOWS_ABSOLUTE_LINE = re.compile(r"(?im)(?<![A-Za-z0-9_])[A-Z]:[\\/][^\r\n]*")
UNC_ABSOLUTE_LINE = re.compile(r"(?m)(?<!\\)\\\\[^\r\n]+")


@dataclass(frozen=True)
class CommandExecutionResult:
    command: ImportedEvidence
    execution_status: str
    continue_pipeline: bool


@dataclass(frozen=True)
class SubjectSnapshot:
    entries: dict[str, tuple[str, int, str]]
    fingerprint: str
    file_count: int
    link_count: int
    total_bytes: int


@dataclass(frozen=True)
class SanitizedOutput:
    content: bytes
    redaction_count: int
    invalid_utf8_replacements: int
    control_character_replacements: int


class _RssMonitor:
    def __init__(self) -> None:
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.samples: list[float] = []
        self.errors: list[str] = []

    def _sample(self) -> None:
        try:
            self.samples.append(round(process_rss_bytes() / MEBIBYTE, 3))
        except (OSError, ValueError):
            if "PROCESS_RSS_SAMPLE_FAILED" not in self.errors:
                self.errors.append("PROCESS_RSS_SAMPLE_FAILED")

    def _run(self) -> None:
        while not self._stop.wait(0.05):
            self._sample()

    def start(self) -> None:
        self._sample()
        self._thread = threading.Thread(
            target=self._run,
            name="veritrail-command-rss",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> bool:
        self._sample()
        self._stop.set()
        if self._thread is not None:
            self._thread.join(1.0)
        return self._thread is None or not self._thread.is_alive()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def _hash_regular_file(path: Path, metadata: os.stat_result) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
            opened = os.fstat(handle.fileno())
        after = os.lstat(path)
    except OSError as exc:
        raise ValidationError(["subject snapshot contains an unreadable file"]) from exc
    identity = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_nlink")
    if any(getattr(metadata, field) != getattr(opened, field) for field in identity) or any(
        getattr(opened, field) != getattr(after, field) for field in identity
    ):
        raise SafetyError("subject file changed while its snapshot was being captured")
    return digest.hexdigest()


def capture_subject_root_snapshot(
    subject_root: Path,
    watch_roots: list[str],
    *,
    max_files: int,
    max_total_bytes: int,
) -> SubjectSnapshot:
    entries: dict[str, tuple[str, int, str]] = {}
    total_bytes = 0
    link_count = 0
    for relative_root in watch_roots:
        root = (
            subject_root
            if relative_root == "."
            else subject_root.joinpath(*relative_root.split("/"))
        )
        stack = [root]
        while stack:
            directory = stack.pop()
            try:
                children = sorted(os.scandir(directory), key=lambda entry: entry.name)
            except OSError as exc:
                raise ValidationError(["subject snapshot contains an unreadable directory"]) from exc
            for child in children:
                if any(ord(character) < 32 for character in child.name):
                    raise ValidationError(["subject snapshot contains a control-character path"])
                path = Path(child.path)
                try:
                    metadata = os.lstat(path)
                except OSError as exc:
                    raise ValidationError(["subject snapshot contains an unreadable node"]) from exc
                relative = path.relative_to(subject_root).as_posix()
                is_link = child.is_symlink() or _is_reparse(metadata)
                if is_link:
                    try:
                        target_digest = sha256_bytes(os.readlink(path).encode("utf-8"))
                    except OSError as exc:
                        raise ValidationError(
                            ["subject snapshot contains an unreadable link or reparse point"]
                        ) from exc
                    entries[relative] = ("LINK", int(metadata.st_size), target_digest)
                    link_count += 1
                elif stat.S_ISDIR(metadata.st_mode):
                    stack.append(path)
                    continue
                elif stat.S_ISREG(metadata.st_mode):
                    if metadata.st_nlink != 1:
                        raise SafetyError("subject snapshot contains an unsafe hard-linked file")
                    total_bytes += int(metadata.st_size)
                    if total_bytes > max_total_bytes:
                        raise ValidationError(
                            ["subject snapshot exceeds the sealed total-byte limit"]
                        )
                    entries[relative] = (
                        "FILE",
                        int(metadata.st_size),
                        _hash_regular_file(path, metadata),
                    )
                else:
                    raise ValidationError(["subject snapshot contains an unsupported node type"])
                if len(entries) > max_files:
                    raise ValidationError(["subject snapshot exceeds the sealed file-count limit"])
    ordered = [
        {"path": path, "kind": value[0], "size": value[1], "sha256": value[2]}
        for path, value in sorted(entries.items())
    ]
    return SubjectSnapshot(
        entries=entries,
        fingerprint=sha256_json(ordered),
        file_count=sum(1 for value in entries.values() if value[0] == "FILE"),
        link_count=link_count,
        total_bytes=total_bytes,
    )


def capture_subject_snapshot(
    resolved: ResolvedCommand,
    watch_roots: list[str],
    *,
    max_files: int,
    max_total_bytes: int,
) -> SubjectSnapshot:
    """Compatibility wrapper for the frozen M9 command observer."""

    return capture_subject_root_snapshot(
        resolved.subject_root,
        watch_roots,
        max_files=max_files,
        max_total_bytes=max_total_bytes,
    )


def _snapshot_diff(
    before: SubjectSnapshot, after: SubjectSnapshot
) -> tuple[dict[str, int], bool]:
    before_paths = set(before.entries)
    after_paths = set(after.entries)
    added_paths = after_paths - before_paths
    deleted_paths = before_paths - after_paths
    modified = 0
    type_changed = 0
    link_changed = sum(
        1 for path in added_paths if after.entries[path][0] == "LINK"
    ) + sum(1 for path in deleted_paths if before.entries[path][0] == "LINK")
    for path in before_paths & after_paths:
        left = before.entries[path]
        right = after.entries[path]
        if left == right:
            continue
        if left[0] != right[0]:
            type_changed += 1
            if "LINK" in {left[0], right[0]}:
                link_changed += 1
        elif left[0] == "LINK":
            link_changed += 1
        else:
            modified += 1
    counts = {
        "added": len(added_paths),
        "deleted": len(deleted_paths),
        "modified": modified,
        "type_changed": type_changed,
        "link_changed": link_changed,
    }
    return counts, any(counts.values())


def compare_subject_snapshots(
    before: SubjectSnapshot, after: SubjectSnapshot
) -> tuple[dict[str, int], bool]:
    """Expose the shared, count-only subject comparison without path disclosure."""

    return _snapshot_diff(before, after)


def _redact_output_text(text: str, replacements: list[tuple[str, str]]) -> tuple[str, int, int]:
    redactions = 0
    for raw, replacement in replacements:
        if not raw:
            continue
        text, count = re.subn(re.escape(raw), replacement, text, flags=re.IGNORECASE)
        redactions += count
    text, count = WINDOWS_ABSOLUTE_LINE.subn("[REDACTED_ABSOLUTE_PATH]", text)
    redactions += count
    text, count = UNC_ABSOLUTE_LINE.subn("[REDACTED_ABSOLUTE_PATH]", text)
    redactions += count
    text, count = redact_string(text)
    redactions += count
    sanitized: list[str] = []
    controls = 0
    for character in text:
        if ord(character) < 32 and character not in {"\r", "\n", "\t"}:
            sanitized.append("[CONTROL]")
            controls += 1
        else:
            sanitized.append(character)
    return "".join(sanitized), redactions, controls


def sanitize_output(
    raw: bytes,
    *,
    replacements: list[tuple[str, str]],
    chunk_bytes: int = OUTPUT_REDACTION_CHUNK_BYTES,
    max_persisted_bytes: int | None = None,
) -> SanitizedOutput:
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    chunks: list[str] = []
    redactions = 0
    controls = 0
    invalid = 0
    for offset in range(0, len(raw), chunk_bytes):
        decoded = decoder.decode(raw[offset : offset + chunk_bytes], final=False)
        invalid += decoded.count("\ufffd")
        redacted, count, control_count = _redact_output_text(decoded, replacements)
        chunks.append(redacted)
        redactions += count
        controls += control_count
    tail = decoder.decode(b"", final=True)
    invalid += tail.count("\ufffd")
    redacted_tail, count, control_count = _redact_output_text(tail, replacements)
    chunks.append(redacted_tail)
    redactions += count
    controls += control_count
    final, count, control_count = _redact_output_text("".join(chunks), replacements)
    redactions += count
    controls += control_count
    encoded = final.encode("utf-8")
    if max_persisted_bytes is not None and len(encoded) > max_persisted_bytes:
        encoded = encoded[:max_persisted_bytes]
        while True:
            try:
                encoded.decode("utf-8", errors="strict")
                break
            except UnicodeDecodeError as exc:
                encoded = encoded[: exc.start]
    return SanitizedOutput(
        content=encoded,
        redaction_count=redactions,
        invalid_utf8_replacements=invalid,
        control_character_replacements=controls,
    )


def _remove_owned_tree(path: Path, parent: Path) -> bool:
    try:
        if path.parent.resolve(strict=True) != parent.resolve(strict=True):
            return False
        if not path.name.startswith(RUN_WORK_PREFIX):
            return False
    except OSError:
        return False

    def remove(node: Path) -> None:
        metadata = os.lstat(node)
        if node.is_symlink() or _is_reparse(metadata) or not stat.S_ISDIR(metadata.st_mode):
            node.unlink()
            return
        for child in os.scandir(node):
            remove(Path(child.path))
        node.rmdir()

    try:
        if path.exists() or path.is_symlink():
            remove(path)
        return not path.exists() and not path.is_symlink()
    except OSError:
        return False


def _resolved_arguments(command: dict[str, Any], run_work: Path) -> list[str]:
    values: list[str] = []
    for argument in command["arguments"]:
        if "literal" in argument:
            values.append(argument["literal"])
            continue
        target = run_work.joinpath(*argument["run_work_path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        values.append(str(target))
    return values


def _empty_captured_stream() -> CapturedStream:
    return CapturedStream(
        content=b"",
        observed_bytes_lower_bound=0,
        stream_complete=False,
        overflowed=False,
        thread_stopped=True,
        error_type=None,
    )


def _stream_facts(
    stream: CapturedStream,
    sanitized: SanitizedOutput,
    attachment: EvidenceAttachment,
) -> dict[str, Any]:
    return {
        "attachment": {
            "path": attachment.path,
            "sha256": attachment.sha256,
            "size": attachment.size,
            "media_type": attachment.media_type,
            "logical_name": attachment.logical_name,
        },
        "observed_bytes_lower_bound": stream.observed_bytes_lower_bound,
        "stream_complete": stream.stream_complete,
        "persisted_bytes": attachment.size,
        "truncated": stream.overflowed,
        "overflowed": stream.overflowed,
        "redaction_count": sanitized.redaction_count,
        "invalid_utf8_replacements": sanitized.invalid_utf8_replacements,
        "control_character_replacements": sanitized.control_character_replacements,
    }


def _execution_status(reason: str, infrastructure_complete: bool) -> str:
    if not infrastructure_complete:
        return "ERROR"
    if reason in {"TIMEOUT", "CANCELLED", "STDOUT_LIMIT_EXCEEDED", "STDERR_LIMIT_EXCEEDED"}:
        return "ABORTED"
    if reason in {"EXITED", "DESCENDANT_GRACE_EXPIRED"}:
        return "COMPLETED"
    return "ERROR"


def collect_command_evidence(
    plan: dict[str, Any],
    resolved: ResolvedCommand,
    *,
    tool_bindings_path: Path,
    output_parent: Path,
    process_runner: Callable[..., OwnedProcessResult] = run_owned_process,
) -> CommandExecutionResult:
    command = plan["command"]
    started_at = _utc_now()
    started_clock = time.monotonic()
    collection_errors: list[dict[str, str]] = []
    before: SubjectSnapshot | None = None
    after: SubjectSnapshot | None = None
    diff_counts: dict[str, int] | None = None
    final_drift: bool | None = None
    run_work: Path | None = None
    run_work_parent: Path | None = None
    run_work_created = False
    run_work_released = True
    process_result: OwnedProcessResult | None = None
    termination_reason = "SUBJECT_SNAPSHOT_FAILED"
    error_type: str | None = "SUBJECT_SNAPSHOT_FAILED"
    monitor = _RssMonitor()
    observer_thread_stopped = True

    try:
        before = capture_subject_snapshot(
            resolved,
            command["subject_watch_roots"],
            max_files=command["max_watch_files"],
            max_total_bytes=command["max_watch_total_bytes"],
        )
    except (OSError, SafetyError, ValidationError):
        collection_errors.append(
            {"stage": "subject-snapshot-before", "error_type": "SUBJECT_SNAPSHOT_FAILED"}
        )

    if before is not None:
        live = resolve_command(
            plan,
            subject_root=resolved.subject_root,
            tool_bindings_path=tool_bindings_path,
        )
        if live.preview["preview_sha256"] != resolved.preview["preview_sha256"]:
            raise SafetyError("approved command preview drifted before process creation")
        resolved = live
        try:
            output_parent.mkdir(parents=True, exist_ok=True)
            run_work_parent = output_parent.resolve(strict=True)
            run_work = Path(
                tempfile.mkdtemp(prefix=RUN_WORK_PREFIX, dir=run_work_parent)
            ).resolve(strict=True)
            run_work_created = True
            run_work_released = False
            arguments = _resolved_arguments(command, run_work)
            environment = {
                **resolved.inherited_environment,
                **resolved.explicit_environment,
                "TEMP": str(run_work),
                "TMP": str(run_work),
            }
            monitor.start()
            try:
                process_result = process_runner(
                    executable=resolved.executable,
                    expected_executable_identity=resolved.executable_identity,
                    arguments=arguments,
                    working_directory=resolved.working_directory,
                    subject_root=resolved.subject_root,
                    environment=environment,
                    timeout_ms=command["timeout_ms"],
                    descendant_exit_grace_ms=command["descendant_exit_grace_ms"],
                    max_stdout_bytes=command["max_stdout_bytes"],
                    max_stderr_bytes=command["max_stderr_bytes"],
                    max_processes=command["max_processes"],
                )
                termination_reason = process_result.termination_reason
                error_type = process_result.error_type
            except Exception:
                termination_reason = "PROCESS_RUNNER_ERROR"
                error_type = "PROCESS_RUNNER_ERROR"
                collection_errors.append(
                    {"stage": "process-runner", "error_type": "PROCESS_RUNNER_ERROR"}
                )
            finally:
                observer_thread_stopped = monitor.stop()
        except (OSError, SafetyError, ValidationError):
            termination_reason = "RUN_WORK_CREATE_FAILED"
            error_type = "RUN_WORK_CREATE_FAILED"
            collection_errors.append(
                {"stage": "run-work-create", "error_type": "RUN_WORK_CREATE_FAILED"}
            )
        finally:
            if run_work is not None and run_work_parent is not None:
                run_work_released = _remove_owned_tree(run_work, run_work_parent)
                if not run_work_released:
                    collection_errors.append(
                        {"stage": "run-work-cleanup", "error_type": "RUN_WORK_CLEANUP_FAILED"}
                    )

        try:
            after = capture_subject_snapshot(
                resolved,
                command["subject_watch_roots"],
                max_files=command["max_watch_files"],
                max_total_bytes=command["max_watch_total_bytes"],
            )
            diff_counts, final_drift = _snapshot_diff(before, after)
        except (OSError, SafetyError, ValidationError):
            collection_errors.append(
                {"stage": "subject-snapshot-after", "error_type": "SUBJECT_SNAPSHOT_FAILED"}
            )

    post_identity: dict[str, Any] | None = None
    executable_postcheck_complete = False
    executable_identity_match: bool | None = None
    if before is not None:
        try:
            post = resolve_command(
                plan,
                subject_root=resolved.subject_root,
                tool_bindings_path=tool_bindings_path,
            )
            post_identity = post.executable_identity
            executable_postcheck_complete = True
            executable_identity_match = post_identity == resolved.executable_identity
        except (OSError, SafetyError, ValidationError):
            executable_identity_match = False
            collection_errors.append(
                {"stage": "executable-postcheck", "error_type": "EXECUTABLE_POSTCHECK_FAILED"}
            )

    captured_stdout = (
        process_result.stdout if process_result is not None else _empty_captured_stream()
    )
    captured_stderr = (
        process_result.stderr if process_result is not None else _empty_captured_stream()
    )
    path_replacements = [
        (str(run_work) if run_work is not None else "", "<RUN_WORK>"),
        (str(resolved.subject_root), "<SUBJECT_ROOT>"),
        (str(resolved.working_directory), "<WORKING_DIRECTORY>"),
        (str(resolved.executable), "<EXECUTABLE>"),
    ]
    stdout = sanitize_output(
        captured_stdout.content,
        replacements=path_replacements,
        max_persisted_bytes=command["max_stdout_bytes"],
    )
    stderr = sanitize_output(
        captured_stderr.content,
        replacements=path_replacements,
        max_persisted_bytes=command["max_stderr_bytes"],
    )
    stdout_attachment = create_text_attachment(
        path="attachments/command/stdout.txt",
        content=stdout.content,
        logical_name="command-stdout",
    )
    stderr_attachment = create_text_attachment(
        path="attachments/command/stderr.txt",
        content=stderr.content,
        logical_name="command-stderr",
    )

    process_created = process_result.process_created if process_result is not None else False
    target_assigned = process_result.target_assigned if process_result is not None else False
    target_resumed = process_result.target_resumed if process_result is not None else False
    exit_code = process_result.exit_code if process_result is not None else None
    exit_expected = isinstance(exit_code, int) and exit_code in command["expected_exit_codes"]
    tree_released = process_result.tree_released if process_result is not None else True
    handles_released = process_result.handles_released if process_result is not None else True
    capture_threads_stopped = (
        process_result.capture_threads_stopped if process_result is not None else True
    )
    oneshot_quiescent = (
        process_result is not None
        and termination_reason == "EXITED"
        and tree_released
        and not process_result.forced_termination_requested
    )
    for monitor_error in monitor.errors:
        collection_errors.append({"stage": "observer-rss", "error_type": monitor_error})
    snapshot_complete = before is not None and after is not None
    cleanup_complete = (
        run_work_released
        and tree_released
        and handles_released
        and capture_threads_stopped
        and observer_thread_stopped
        and (process_result.cleanup_complete if process_result is not None else True)
    )
    infrastructure_complete = (
        process_result is not None
        and error_type is None
        and cleanup_complete
        and snapshot_complete
        and executable_postcheck_complete
    )
    status = _execution_status(termination_reason, infrastructure_complete)
    continue_pipeline = (
        status == "COMPLETED"
        and exit_expected
        and oneshot_quiescent
        and final_drift is False
        and executable_identity_match is True
        and cleanup_complete
    )
    rss_start = monitor.samples[0] if monitor.samples else 0.0
    rss_peak = max(monitor.samples, default=0.0)
    ended_at = _utc_now()
    ownership = {
        "backend": OWNERSHIP_BACKEND,
        "parent_in_job": process_result.parent_in_job if process_result is not None else False,
        "active_process_limit": command["max_processes"],
        "active_process_limit_enforced": (
            process_result.active_process_limit_enforced if process_result is not None else False
        ),
        "process_limit_attempt_observation": "NOT_PROVEN",
        "total_assigned_processes": (
            process_result.total_assigned_processes if process_result is not None else 0
        ),
        "final_active_processes": (
            process_result.final_active_processes if process_result is not None else 0
        ),
        "job_limit_terminated_processes": (
            process_result.job_limit_terminated_processes if process_result is not None else 0
        ),
        "forced_termination_requested": (
            process_result.forced_termination_requested if process_result is not None else False
        ),
        "forced_termination_processes_observed": (
            process_result.forced_termination_processes_observed
            if process_result is not None
            else 0
        ),
    }
    subject = {
        "policy": command["write_policy"],
        "watch_roots": list(command["subject_watch_roots"]),
        "before_fingerprint": before.fingerprint if before is not None else None,
        "after_fingerprint": after.fingerprint if after is not None else None,
        "before_file_count": before.file_count if before is not None else None,
        "after_file_count": after.file_count if after is not None else None,
        "before_link_count": before.link_count if before is not None else None,
        "after_link_count": after.link_count if after is not None else None,
        "before_total_bytes": before.total_bytes if before is not None else None,
        "after_total_bytes": after.total_bytes if after is not None else None,
        "diff_counts": diff_counts,
        "final_state_drift_detected": final_drift,
        "snapshot_complete": snapshot_complete,
        "write_activity": "NOT_PROVEN",
    }
    document = {
        "schema_version": "0.1",
        "evidence_type": "runtime.command",
        "source": f"VeriTrail {COLLECTOR_VERSION}",
        "captured_at": started_at,
        "facts": {
            "collector_version": COLLECTOR_VERSION,
            "plan_sha256": plan["seal"]["digest"],
            "command_policy_sha256": sha256_json(command),
            "preview_sha256": resolved.preview["preview_sha256"],
            "command_id": command["command_id"],
            "adapter": command["adapter"],
            "tool_binding_id": command["tool_binding"],
            "executable": resolved.executable_identity,
            "post_executable": post_identity,
            "executable_postcheck_complete": executable_postcheck_complete,
            "executable_identity_match": executable_identity_match,
            "argument_count": len(command["arguments"]),
            "argument_kinds": [
                "literal" if "literal" in item else "run_work_path"
                for item in command["arguments"]
            ],
            "arguments_sha256": sha256_json(resolved.preview["arguments"]),
            "working_directory": command["working_directory"],
            "environment": resolved.preview["environment"],
            "stdin": command["stdin"],
            "tty_used": False,
            "shell_used": False,
            "started_at": started_at,
            "ended_at": ended_at,
            "elapsed_ms": round((time.monotonic() - started_clock) * 1000, 3),
            "process_created": process_created,
            "target_assigned": target_assigned,
            "target_resumed": target_resumed,
            "exit_code": exit_code,
            "exit_expected": exit_expected,
            "termination_reason": termination_reason,
            "error_type": error_type,
            "oneshot_quiescent": oneshot_quiescent,
            "stdout": _stream_facts(captured_stdout, stdout, stdout_attachment),
            "stderr": _stream_facts(captured_stderr, stderr, stderr_attachment),
            "ownership": ownership,
            "subject": subject,
            "run_work_created": run_work_created,
            "run_work_released": run_work_released,
            "capture_threads_stopped": capture_threads_stopped,
            "handles_released": handles_released,
            "tree_released": tree_released,
            "cleanup_complete": cleanup_complete,
            "observer_effect": {
                "rss_start_mb": rss_start,
                "rss_peak_mb": rss_peak,
                "rss_delta_mb": max(0.0, round(rss_peak - rss_start, 3)),
                "sample_count": len(monitor.samples),
                "thread_stopped": observer_thread_stopped,
            },
            "collection_errors": collection_errors,
        },
        "observed_variables": (
            {"pre_target_command_mode": "veritrail_managed_trusted_process_oneshot"}
            if any(item["name"] == "pre_target_command_mode" for item in plan["variables"])
            else {}
        ),
        "metadata": {
            "structured_arguments": True,
            "environment_values_persisted": False,
            "absolute_paths_persisted": False,
            "raw_output_persisted": False,
            "filesystem_isolation": "NOT_PROVEN",
            "network_isolation": "NOT_PROVEN",
            "executable_toctou_containment": "NOT_PROVEN",
            "untrusted_code_containment": "NOT_SUPPORTED",
        },
    }
    artifact = import_evidence_document(
        document,
        "generated-command.json",
        attachments=(stdout_attachment, stderr_attachment),
    )
    return CommandExecutionResult(
        command=artifact,
        execution_status=status,
        continue_pipeline=continue_pipeline,
    )
