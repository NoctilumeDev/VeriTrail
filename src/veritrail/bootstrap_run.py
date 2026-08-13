from __future__ import annotations

import json
import os
import stat
import tempfile
import threading
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from veritrail.bootstrap_browser import (
    ObservedBrowserEvidence,
    collect_observed_browser_evidence,
)
from veritrail.bootstrap_evidence import (
    BootstrapEvidenceResult,
    collect_bootstrap_evidence,
)
from veritrail.bootstrap_lifecycle import (
    BootstrapLifecycleObservation,
    BootstrapPreTeardownObservation,
    materialize_bootstrap_service_specs,
    run_bootstrap_lifecycle,
)
from veritrail.bootstrap_preview import ResolvedBootstrap
from veritrail.canonical import canonical_json_bytes, sha256_bytes, sha256_json
from veritrail.command_execution import (
    SubjectSnapshot,
    capture_subject_root_snapshot,
    compare_subject_snapshots,
    sanitize_output,
)
from veritrail.errors import SafetyError, ValidationError
from veritrail.evidence import ImportedEvidence, verify_imported_evidence
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.resources import MEBIBYTE, process_rss_bytes
from veritrail.windows_readiness import (
    OwnedReadinessObservation,
    probe_owned_http_readiness,
)
from veritrail.windows_service import OwnedServiceSession

BOOTSTRAP_RUN_PREFIX = ".veritrail-bootstrap-run-"
STAGING_FILE = "pre-teardown.json"
OWNERSHIP_FILE = ".owner"
MAX_STAGED_BYTES = 5 * 1024 * 1024
SAMPLE_INTERVAL_SECONDS = 0.05
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


@dataclass(frozen=True)
class BootstrapObservedRunResult:
    lifecycle: BootstrapLifecycleObservation
    evidence: BootstrapEvidenceResult | None
    browser: ImportedEvidence | None
    resource_observation: dict[str, Any]
    subject_observation: dict[str, Any]
    run_work_released: bool
    staging_released: bool
    owned_root_released: bool
    staged_sha256: str | None
    error_type: str | None


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def _remove_tree_without_following_links(path: Path) -> bool:
    def remove(node: Path) -> None:
        metadata = os.lstat(node)
        if node.is_symlink() or _is_reparse(metadata):
            if stat.S_ISDIR(metadata.st_mode):
                node.rmdir()
            else:
                node.unlink()
            return
        if not stat.S_ISDIR(metadata.st_mode):
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


class _OwnedBootstrapWorkspace:
    def __init__(
        self,
        *,
        parent: Path,
        root: Path,
        run_work: Path,
        staging: Path,
        owner_token: str,
    ) -> None:
        self.parent = parent
        self.root = root
        self.run_work = run_work
        self.staging = staging
        self._owner_token = owner_token
        self._staged_sha256: str | None = None
        self._staged_size: int | None = None

    @classmethod
    def create(cls, output_parent: Path) -> _OwnedBootstrapWorkspace:
        output_parent.mkdir(parents=True, exist_ok=True)
        parent = output_parent.resolve(strict=True)
        if not parent.is_dir():
            raise SafetyError("M10 output parent must be a directory")
        root = Path(tempfile.mkdtemp(prefix=BOOTSTRAP_RUN_PREFIX, dir=parent)).resolve(
            strict=True
        )
        owner_token = uuid.uuid4().hex
        try:
            marker = root / OWNERSHIP_FILE
            with marker.open("x", encoding="ascii", newline="") as handle:
                handle.write(owner_token)
                handle.flush()
                os.fsync(handle.fileno())
            run_work = root / "work"
            staging = root / "staging"
            run_work.mkdir()
            staging.mkdir()
            return cls(
                parent=parent,
                root=root,
                run_work=run_work,
                staging=staging,
                owner_token=owner_token,
            )
        except Exception:
            _remove_tree_without_following_links(root)
            raise

    def _verify_root_ownership(self) -> None:
        try:
            if self.root.parent.resolve(strict=True) != self.parent:
                raise SafetyError("M10 owned workspace parent drifted")
            if not self.root.name.startswith(BOOTSTRAP_RUN_PREFIX):
                raise SafetyError("M10 owned workspace name drifted")
            root_metadata = os.lstat(self.root)
            if _is_reparse(root_metadata) or not stat.S_ISDIR(root_metadata.st_mode):
                raise SafetyError("M10 owned workspace root was replaced")
            marker = self.root / OWNERSHIP_FILE
            marker_metadata = os.lstat(marker)
            if (
                _is_reparse(marker_metadata)
                or not stat.S_ISREG(marker_metadata.st_mode)
                or marker_metadata.st_nlink != 1
                or marker.read_text(encoding="ascii") != self._owner_token
            ):
                raise SafetyError("M10 owned workspace marker was replaced")
        except OSError as exc:
            raise SafetyError("M10 could not verify owned workspace identity") from exc

    def _verify_directory(self, directory: Path) -> None:
        try:
            metadata = os.lstat(directory)
            if _is_reparse(metadata) or not stat.S_ISDIR(metadata.st_mode):
                raise SafetyError("M10 owned workspace directory was replaced")
            if directory.parent.resolve(strict=True) != self.root:
                raise SafetyError("M10 owned workspace directory escaped its root")
        except OSError as exc:
            raise SafetyError("M10 could not verify owned workspace directory") from exc

    def _verify_ownership(self) -> None:
        self._verify_root_ownership()
        self._verify_directory(self.run_work)
        self._verify_directory(self.staging)

    @staticmethod
    def _write_exclusive(path: Path, content: bytes) -> None:
        with path.open("xb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())

    def stage(
        self,
        document: dict[str, Any],
        *,
        writer: Callable[[Path, bytes], None] | None = None,
    ) -> str:
        self._verify_ownership()
        content = canonical_json_bytes(document)
        if len(content) > MAX_STAGED_BYTES:
            raise SafetyError("M10 pre-teardown staging exceeds the bounded size")
        path = self.staging / STAGING_FILE
        (writer or self._write_exclusive)(path, content)
        try:
            metadata = os.lstat(path)
            persisted = path.read_bytes()
        except OSError as exc:
            raise SafetyError("M10 pre-teardown staging could not be read back") from exc
        if (
            _is_reparse(metadata)
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
            or len(persisted) != len(content)
            or persisted != content
        ):
            raise SafetyError("M10 pre-teardown staging readback differs from memory")
        try:
            decoded = json.loads(persisted)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SafetyError("M10 pre-teardown staging is not canonical JSON") from exc
        if canonical_json_bytes(decoded) != persisted:
            raise SafetyError("M10 pre-teardown staging lost canonical form")
        self._staged_sha256 = sha256_bytes(persisted)
        self._staged_size = len(persisted)
        return self._staged_sha256

    def verify_staged(self) -> str:
        self._verify_ownership()
        if self._staged_sha256 is None or self._staged_size is None:
            raise SafetyError("M10 pre-teardown facts were not staged")
        path = self.staging / STAGING_FILE
        try:
            metadata = os.lstat(path)
            content = path.read_bytes()
        except OSError as exc:
            raise SafetyError("M10 staged facts disappeared before finalization") from exc
        if (
            _is_reparse(metadata)
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
            or len(content) != self._staged_size
            or sha256_bytes(content) != self._staged_sha256
        ):
            raise SafetyError("M10 staged facts drifted before finalization")
        return self._staged_sha256

    def release(self) -> tuple[bool, bool, bool]:
        try:
            self._verify_root_ownership()
        except SafetyError:
            return False, False, False
        run_work_released = _remove_tree_without_following_links(self.run_work)
        staging_released = _remove_tree_without_following_links(self.staging)
        owned_root_released = False
        if run_work_released and staging_released:
            try:
                (self.root / OWNERSHIP_FILE).unlink()
                self.root.rmdir()
                owned_root_released = not self.root.exists()
            except OSError:
                owned_root_released = False
        return run_work_released, staging_released, owned_root_released


class _BootstrapResourceMonitor:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._sessions: dict[str, Any] = {}
        self._roles: dict[str, str] = {}
        self._core_samples: list[float] = []
        self._node_samples: dict[str, list[float]] = {}

    def register(self, node_id: str, role: str, session: Any) -> None:
        with self._lock:
            self._sessions[node_id] = session
            self._roles[node_id] = role
            self._node_samples.setdefault(node_id, [])
        self._sample()

    def _sample(self) -> None:
        try:
            core = round(process_rss_bytes() / MEBIBYTE, 3)
        except (OSError, ValueError):
            core = None
        with self._lock:
            sessions = tuple(self._sessions.items())
            if core is not None:
                self._core_samples.append(core)
        for node_id, session in sessions:
            try:
                value = round(session.sample_rss_bytes() / MEBIBYTE, 3)
            except (AttributeError, OSError, SafetyError, ValueError):
                continue
            with self._lock:
                self._node_samples.setdefault(node_id, []).append(value)

    def _run(self) -> None:
        while not self._stop.wait(SAMPLE_INTERVAL_SECONDS):
            self._sample()

    def start(self) -> None:
        self._sample()
        self._thread = threading.Thread(
            target=self._run,
            name="veritrail-bootstrap-rss",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> bool:
        self._sample()
        self._stop.set()
        if self._thread is not None:
            self._thread.join(1.0)
        return self._thread is None or not self._thread.is_alive()

    def current_peaks(self) -> dict[str, float | None]:
        with self._lock:
            roles = dict(self._roles)
            samples = {key: list(value) for key, value in self._node_samples.items()}
            core = list(self._core_samples)
        result: dict[str, float | None] = {
            "core_peak_rss_mb": max(core) if core else None,
            "dependency_peak_rss_mb": None,
            "application_peak_rss_mb": None,
        }
        for node_id, role in roles.items():
            values = samples.get(node_id, [])
            result[f"{role.casefold()}_peak_rss_mb"] = max(values) if values else None
        return result

    def final_observation(
        self,
        *,
        actual_start_order: tuple[str, ...],
        browser_started: bool,
        browser_peak_rss_mb: float | None,
        browser_sampling_complete: bool,
        thread_stopped: bool,
    ) -> dict[str, Any]:
        peaks = self.current_peaks()
        with self._lock:
            sampled_nodes = {
                node_id for node_id, values in self._node_samples.items() if values
            }
            core_sampled = bool(self._core_samples)
        sampling_complete = (
            thread_stopped
            and core_sampled
            and set(actual_start_order).issubset(sampled_nodes)
            and (
                not browser_started
                or (
                    browser_peak_rss_mb is not None
                    and browser_sampling_complete
                )
            )
        )
        return {
            **peaks,
            "browser_peak_rss_mb": browser_peak_rss_mb,
            "sampling_complete": sampling_complete,
        }


def _validate_preview_identity(
    plan: dict[str, Any], profile: dict[str, Any], preview: dict[str, Any]
) -> None:
    digest = preview.get("preview_sha256")
    unsigned = {key: value for key, value in preview.items() if key != "preview_sha256"}
    expected = {
        "plan_sha256": plan["seal"]["digest"],
        "profile_id": profile["profile_id"],
        "profile_version": profile["version"],
        "profile_sha256": profile["seal"]["digest"],
        "platform": profile["platform"],
        "cold_state": profile["cold_state"],
        "start_order": profile["start_order"],
        "teardown_order": profile["teardown_order"],
    }
    if not isinstance(digest, str) or digest != sha256_json(unsigned):
        raise SafetyError("M10 approved bootstrap Preview seal is invalid")
    if any(preview.get(key) != value for key, value in expected.items()):
        raise SafetyError("M10 approved bootstrap Preview identity drifted")


def _stream_projection(
    stream: Any,
    *,
    replacements: list[tuple[str, str]],
    limit: int,
) -> dict[str, Any]:
    if stream is None:
        raise SafetyError("M10 pre-teardown stream snapshot is unavailable")
    sanitized = sanitize_output(
        stream.content,
        replacements=replacements,
        max_persisted_bytes=limit,
    )
    return {
        "content": sanitized.content.decode("utf-8"),
        "observed_bytes_lower_bound": stream.observed_bytes_lower_bound,
        "stream_complete": stream.stream_complete,
        "overflowed": stream.overflowed,
        "redaction_count": sanitized.redaction_count,
        "invalid_utf8_replacements": sanitized.invalid_utf8_replacements,
        "control_character_replacements": sanitized.control_character_replacements,
    }


def _stage_document(
    plan: dict[str, Any],
    profile: dict[str, Any],
    preview: dict[str, Any],
    observation: BootstrapPreTeardownObservation,
    *,
    browser_exercise: dict[str, Any],
    subject_before: SubjectSnapshot,
    resource_peaks: dict[str, float | None],
    replacements: list[tuple[str, str]],
) -> dict[str, Any]:
    profile_nodes = {node["node_id"]: node for node in profile["nodes"]}
    streams = {item.node_id: item for item in observation.streams}
    if set(streams) != set(profile_nodes):
        raise SafetyError("M10 pre-teardown stream snapshots differ from the Profile")
    nodes: list[dict[str, Any]] = []
    for node in observation.nodes:
        start = node.start
        readiness = node.readiness
        stream = streams[node.node_id]
        policy = profile_nodes[node.node_id]
        if start is not None and (stream.stdout is None or stream.stderr is None):
            raise SafetyError("M10 started node is missing a pre-teardown stream snapshot")
        nodes.append(
            {
                "node_id": node.node_id,
                "role": node.role,
                "start": None
                if start is None
                else {
                    "parent_in_job": start.parent_in_job,
                    "process_created": start.process_created,
                    "target_assigned": start.target_assigned,
                    "target_resumed": start.target_resumed,
                    "active_process_limit": start.active_process_limit,
                    "active_process_limit_enforced": start.active_process_limit_enforced,
                    "error_type": start.error_type,
                },
                "readiness": None
                if readiness is None
                else {
                    "ready": readiness.ready,
                    "error_type": readiness.error_type,
                    "attempts": [
                        {
                            "ordinal": attempt.ordinal,
                            "elapsed_ms": attempt.elapsed_ms,
                            "result": attempt.result,
                            "http_status": attempt.http_status,
                            "response_byte_count": attempt.response_byte_count,
                            "listener_owner_in_job": attempt.listener_owner_in_job,
                            "job_active_process_count": attempt.job_active_process_count,
                        }
                        for attempt in readiness.attempts
                    ],
                },
                "stdout": _stream_projection(
                    stream.stdout,
                    replacements=replacements,
                    limit=policy["limits"]["max_stdout_bytes"],
                )
                if start is not None and stream.stdout is not None
                else None,
                "stderr": _stream_projection(
                    stream.stderr,
                    replacements=replacements,
                    limit=policy["limits"]["max_stderr_bytes"],
                )
                if start is not None and stream.stderr is not None
                else None,
            }
        )
    return {
        "schema_version": "0.1",
        "record_type": "bootstrap.pre_teardown",
        "plan_sha256": plan["seal"]["digest"],
        "profile_sha256": profile["seal"]["digest"],
        "preview_sha256": preview["preview_sha256"],
        "start_order": {
            "sealed": list(observation.expected_start_order),
            "actual": list(observation.actual_start_order),
        },
        "teardown_order": {"sealed": list(observation.expected_teardown_order)},
        "events": [
            {
                "ordinal": event.ordinal,
                "stage": event.stage,
                "result": event.result,
                "elapsed_ms": event.elapsed_ms,
            }
            for event in observation.events
        ],
        "nodes": nodes,
        "services_ready": observation.services_ready,
        "ready_callback_started": observation.ready_callback_started,
        "ready_callback_completed": observation.ready_callback_completed,
        "trigger_reason": observation.trigger_reason,
        "browser_exercise": dict(browser_exercise),
        "resource_peaks": dict(resource_peaks),
        "subject_before": {
            "fingerprint": subject_before.fingerprint,
            "file_count": subject_before.file_count,
            "link_count": subject_before.link_count,
            "total_bytes": subject_before.total_bytes,
        },
        "privacy": {
            "absolute_paths_persisted": False,
            "process_ids_persisted": False,
            "environment_values_persisted": False,
            "raw_output_persisted": False,
            "response_bodies_persisted": False,
        },
    }


def _subject_observation(
    before: SubjectSnapshot, after: SubjectSnapshot | None
) -> dict[str, Any]:
    if after is None:
        return {
            "before_fingerprint": before.fingerprint,
            "after_fingerprint": None,
            "changed": None,
            "scan_complete": False,
        }
    _, changed = compare_subject_snapshots(before, after)
    return {
        "before_fingerprint": before.fingerprint,
        "after_fingerprint": after.fingerprint,
        "changed": changed,
        "scan_complete": True,
    }


def run_observed_bootstrap(
    plan: dict[str, Any],
    profile: dict[str, Any],
    resolved: ResolvedBootstrap,
    *,
    output_parent: Path,
    browser_runner: Callable[[dict[str, Any]], ObservedBrowserEvidence] | None = None,
    cancel_event: threading.Event | None = None,
    session_factory: Callable[..., Any] = OwnedServiceSession.start,
    readiness_probe: Callable[..., OwnedReadinessObservation] = (
        probe_owned_http_readiness
    ),
    staging_writer: Callable[[Path, bytes], None] | None = None,
) -> BootstrapObservedRunResult:
    """Run the M10 lifecycle through owned staging and post-teardown observations.

    This is an internal M10 slice. It intentionally does not expose the public CLI
    `run` path; it reuses the frozen M2 Browser adapter with M10-only observation.
    """

    verify_sealed_project_profile(profile)
    verify_sealed_plan(plan, profile)
    _validate_preview_identity(plan, profile, resolved.preview)
    before = capture_subject_root_snapshot(
        resolved.subject_root,
        profile["subject_watch_roots"],
        max_files=profile["max_watch_files"],
        max_total_bytes=profile["max_watch_total_bytes"],
    )
    workspace = _OwnedBootstrapWorkspace.create(output_parent)
    monitor = _BootstrapResourceMonitor()
    browser_exercise: dict[str, Any] = {
        "started": False,
        "completed": False,
        "evidence_sha256": None,
    }
    browser_peak_rss_mb: float | None = None
    browser_sampling_complete = False
    browser_artifact: ImportedEvidence | None = None
    staged_sha256: str | None = None
    stage_verified = False
    error_type: str | None = None
    monitor_stopped = True
    lifecycle: BootstrapLifecycleObservation
    path_replacements = [
        (str(workspace.root), "<RUN_ROOT>"),
        (str(workspace.run_work), "<RUN_WORK>"),
        (str(workspace.staging), "<STAGING>"),
        (str(resolved.subject_root), "<SUBJECT_ROOT>"),
    ]
    for node in resolved.nodes:
        path_replacements.extend(
            [
                (str(node.working_directory), f"<{node.node_id.upper()}_WORKING_DIRECTORY>"),
                (str(node.executable), f"<{node.node_id.upper()}_EXECUTABLE>"),
            ]
        )

    roles = {node["node_id"]: node["role"] for node in profile["nodes"]}

    def tracked_session_factory(**values: Any) -> Any:
        session = session_factory(**values)
        node_id = str(values["node_id"])
        monitor.register(node_id, roles[node_id], session)
        return session

    def exercise() -> str | None:
        nonlocal browser_artifact, browser_peak_rss_mb, browser_sampling_complete
        browser_exercise["started"] = True
        runner = browser_runner or collect_observed_browser_evidence
        observed = runner(plan)
        if (
            not isinstance(observed, ObservedBrowserEvidence)
            or isinstance(observed.peak_rss_mb, bool)
            or not isinstance(observed.peak_rss_mb, (int, float))
            or observed.peak_rss_mb < 0
            or not isinstance(observed.resource_sampling_complete, bool)
            or not isinstance(observed.process_cleanup_complete, bool)
        ):
            raise SafetyError("M10 Browser observation is invalid")
        verify_imported_evidence(observed.browser)
        facts = observed.browser.document.get("facts")
        if (
            observed.browser.document.get("evidence_type") != "browser.session"
            or not isinstance(facts, dict)
            or facts.get("policy_sha256") != sha256_json(plan["browser"])
        ):
            raise SafetyError("M10 Browser Evidence differs from the sealed policy")
        browser_artifact = observed.browser
        browser_peak_rss_mb = round(float(observed.peak_rss_mb), 3)
        browser_sampling_complete = observed.resource_sampling_complete
        browser_exercise.update(
            {
                "completed": True,
                "evidence_sha256": observed.browser.sha256,
            }
        )
        if (
            not observed.resource_sampling_complete
            or not observed.process_cleanup_complete
            or facts.get("cleanup_complete") is not True
            or facts.get("collection_errors") != []
        ):
            raise SafetyError("M10 Browser collection or owned cleanup is incomplete")
        if (
            facts.get("capture_complete") is not True
            or facts.get("all_steps_passed") is not True
        ):
            return "BROWSER_HARD_FAILURE"
        return None

    def stage_pre_teardown(observation: BootstrapPreTeardownObservation) -> None:
        nonlocal staged_sha256
        document = _stage_document(
            plan,
            profile,
            resolved.preview,
            observation,
            browser_exercise=browser_exercise,
            subject_before=before,
            resource_peaks=monitor.current_peaks(),
            replacements=path_replacements,
        )
        staged_sha256 = workspace.stage(document, writer=staging_writer)

    try:
        specs = materialize_bootstrap_service_specs(
            profile,
            resolved,
            run_work=workspace.run_work,
        )
        monitor.start()
        monitor_stopped = False
        lifecycle = run_bootstrap_lifecycle(
            specs,
            lifecycle_timeout_ms=profile["lifecycle_timeout_ms"],
            cancel_event=cancel_event,
            on_services_ready=exercise,
            on_evidence_finalize=stage_pre_teardown,
            session_factory=tracked_session_factory,
            readiness_probe=readiness_probe,
        )
        try:
            workspace.verify_staged()
            stage_verified = True
        except SafetyError:
            error_type = "EVIDENCE_STAGING_VERIFY_FAILED"
    except Exception:
        if not monitor_stopped:
            monitor_stopped = monitor.stop()
        workspace.release()
        raise
    finally:
        if not monitor_stopped:
            monitor_stopped = monitor.stop()

    resource = monitor.final_observation(
        actual_start_order=lifecycle.actual_start_order,
        browser_started=browser_exercise["started"],
        browser_peak_rss_mb=browser_peak_rss_mb,
        browser_sampling_complete=browser_sampling_complete,
        thread_stopped=monitor_stopped,
    )
    run_work_released, staging_released, owned_root_released = workspace.release()
    after: SubjectSnapshot | None = None
    try:
        after = capture_subject_root_snapshot(
            resolved.subject_root,
            profile["subject_watch_roots"],
            max_files=profile["max_watch_files"],
            max_total_bytes=profile["max_watch_total_bytes"],
        )
    except (OSError, SafetyError, ValidationError):
        if error_type is None:
            error_type = "SUBJECT_SNAPSHOT_FAILED"
    subject = _subject_observation(before, after)

    evidence: BootstrapEvidenceResult | None = None
    finalized = any(
        event.stage == "EVIDENCE_FINALIZED" and event.result == "COMPLETE"
        for event in lifecycle.events
    )
    if stage_verified and finalized:
        try:
            evidence = collect_bootstrap_evidence(
                plan,
                profile,
                resolved.preview,
                lifecycle,
                browser_exercise=browser_exercise,
                resource_observation=resource,
                subject_observation=subject,
                run_work_released=run_work_released and owned_root_released,
                staging_released=staging_released and owned_root_released,
                path_replacements=path_replacements,
            )
        except (SafetyError, ValidationError):
            if error_type is None:
                error_type = "BOOTSTRAP_EVIDENCE_BUILD_FAILED"
    elif error_type is None:
        error_type = "EVIDENCE_STAGING_FAILED"

    return BootstrapObservedRunResult(
        lifecycle=lifecycle,
        evidence=evidence,
        browser=browser_artifact,
        resource_observation=resource,
        subject_observation=subject,
        run_work_released=run_work_released,
        staging_released=staging_released,
        owned_root_released=owned_root_released,
        staged_sha256=staged_sha256,
        error_type=error_type,
    )
