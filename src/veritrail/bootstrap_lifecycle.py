from __future__ import annotations

import threading
import time
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

from veritrail.bootstrap_preview import ResolvedBootstrap
from veritrail.errors import SafetyError
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.windows_readiness import (
    OwnedReadinessObservation,
    probe_owned_http_readiness,
)
from veritrail.windows_service import (
    OwnedServiceSession,
    OwnedServiceStartError,
    OwnedServiceStartObservation,
    OwnedServiceTeardownObservation,
)
from veritrail.windows_job import CapturedStream


@dataclass(frozen=True)
class BootstrapServiceSpec:
    node_id: str
    role: str
    executable: Path
    arguments: tuple[str, ...]
    working_directory: Path
    environment: dict[str, str]
    port: int
    readiness: dict[str, Any]
    limits: dict[str, int]
    shutdown: dict[str, Any]


@dataclass(frozen=True)
class BootstrapLifecycleEvent:
    ordinal: int
    stage: str
    result: str
    elapsed_ms: float


@dataclass(frozen=True)
class BootstrapNodeObservation:
    node_id: str
    role: str
    start: OwnedServiceStartObservation | None
    readiness: OwnedReadinessObservation | None
    teardown: OwnedServiceTeardownObservation | None


@dataclass(frozen=True)
class BootstrapLifecycleObservation:
    expected_start_order: tuple[str, str]
    actual_start_order: tuple[str, ...]
    expected_teardown_order: tuple[str, str]
    actual_teardown_order: tuple[str, ...]
    teardown_attempt_order: tuple[str, ...]
    events: tuple[BootstrapLifecycleEvent, ...]
    nodes: tuple[BootstrapNodeObservation, BootstrapNodeObservation]
    services_ready: bool
    ready_callback_started: bool
    ready_callback_completed: bool
    trigger_reason: str
    stop_reason: str
    cleanup_complete: bool
    elapsed_ms: float


@dataclass(frozen=True)
class BootstrapPreTeardownObservation:
    expected_start_order: tuple[str, str]
    actual_start_order: tuple[str, ...]
    expected_teardown_order: tuple[str, str]
    events: tuple[BootstrapLifecycleEvent, ...]
    nodes: tuple[BootstrapNodeObservation, BootstrapNodeObservation]
    services_ready: bool
    ready_callback_started: bool
    ready_callback_completed: bool
    trigger_reason: str
    streams: tuple["BootstrapPreTeardownStreams", ...]


@dataclass(frozen=True)
class BootstrapPreTeardownStreams:
    node_id: str
    stdout: CapturedStream | None
    stderr: CapturedStream | None


@dataclass
class _MutableNodeObservation:
    spec: BootstrapServiceSpec
    start: OwnedServiceStartObservation | None = None
    readiness: OwnedReadinessObservation | None = None
    teardown: OwnedServiceTeardownObservation | None = None


def materialize_bootstrap_service_specs(
    profile: dict[str, Any],
    resolved: ResolvedBootstrap,
    *,
    run_work: Path,
) -> tuple[BootstrapServiceSpec, BootstrapServiceSpec]:
    """Resolve typed Profile arguments into run-local, non-persistent values."""

    verify_sealed_project_profile(profile)
    try:
        work = run_work.resolve(strict=True)
    except OSError as exc:
        raise SafetyError("M10 run work must already exist") from exc
    if not work.is_dir():
        raise SafetyError("M10 run work must be a directory")

    expected_order = tuple(profile["start_order"])
    profile_nodes = {node["node_id"]: node for node in profile["nodes"]}
    resolved_nodes = {node.node_id: node for node in resolved.nodes}
    if (
        len(resolved_nodes) != 2
        or tuple(node.node_id for node in resolved.nodes) != expected_order
        or set(resolved_nodes) != set(expected_order)
    ):
        raise SafetyError("M10 resolved nodes do not match the sealed start order")

    node_temp_root = work / "node-temp"
    node_temp_root.mkdir()
    specs: list[BootstrapServiceSpec] = []
    for node_id in expected_order:
        policy = profile_nodes[node_id]
        resolved_node = resolved_nodes[node_id]
        temp_directory = node_temp_root / node_id
        temp_directory.mkdir()
        arguments: list[str] = []
        for argument in policy["arguments"]:
            if "literal" in argument:
                arguments.append(argument["literal"])
            elif "node_port" in argument:
                arguments.append(str(profile_nodes[argument["node_port"]]["port"]))
            elif "node_origin" in argument:
                port = profile_nodes[argument["node_origin"]]["port"]
                arguments.append(f"http://127.0.0.1:{port}")
            else:
                candidate = work.joinpath(*argument["run_work_path"])
                resolved_candidate = candidate.resolve(strict=False)
                try:
                    resolved_candidate.relative_to(work)
                except ValueError as exc:
                    raise SafetyError("M10 run-work argument escaped the owned root") from exc
                arguments.append(str(resolved_candidate))

        environment = {
            **resolved_node.inherited_environment,
            **resolved_node.explicit_environment,
            "TEMP": str(temp_directory),
            "TMP": str(temp_directory),
        }
        specs.append(
            BootstrapServiceSpec(
                node_id=node_id,
                role=policy["role"],
                executable=resolved_node.executable,
                arguments=tuple(arguments),
                working_directory=resolved_node.working_directory,
                environment=environment,
                port=policy["port"],
                readiness=deepcopy(policy["readiness"]),
                limits=deepcopy(policy["limits"]),
                shutdown=deepcopy(policy["shutdown"]),
            )
        )
    return specs[0], specs[1]


def _validate_specs(specs: Sequence[BootstrapServiceSpec]) -> None:
    if len(specs) != 2:
        raise SafetyError("M10 lifecycle requires exactly two service specifications")
    dependency, application = specs
    if dependency.role != "DEPENDENCY" or application.role != "APPLICATION":
        raise SafetyError("M10 lifecycle requires dependency then application")
    if dependency.node_id == application.node_id or dependency.port == application.port:
        raise SafetyError("M10 lifecycle requires distinct nodes and ports")


def _stop_reason(error_type: str | None) -> str:
    if error_type in {
        "READINESS_TIMEOUT",
        "LISTENER_OWNERSHIP_MISMATCH",
        "NODE_EARLY_EXIT",
        "USER_CANCELLED",
        "LIFECYCLE_TIMEOUT",
    }:
        return error_type
    return "COLLECTOR_ERROR"


def run_bootstrap_lifecycle(
    specs: Sequence[BootstrapServiceSpec],
    *,
    lifecycle_timeout_ms: int,
    cancel_event: threading.Event | None = None,
    on_services_ready: Callable[[], None] | None = None,
    on_evidence_finalize: Callable[[BootstrapPreTeardownObservation], None] | None = None,
    session_factory: Callable[..., OwnedServiceSession] = OwnedServiceSession.start,
    readiness_probe: Callable[..., OwnedReadinessObservation] = (
        probe_owned_http_readiness
    ),
) -> BootstrapLifecycleObservation:
    """Run the two service lifecycle without creating public Evidence or a Bundle."""

    _validate_specs(specs)
    if (
        not isinstance(lifecycle_timeout_ms, int)
        or isinstance(lifecycle_timeout_ms, bool)
        or not 5_000 <= lifecycle_timeout_ms <= 900_000
    ):
        raise SafetyError("M10 lifecycle timeout is outside the sealed range")

    started = time.monotonic()
    deadline = started + lifecycle_timeout_ms / 1000
    events: list[BootstrapLifecycleEvent] = []
    mutable = [_MutableNodeObservation(spec) for spec in specs]
    sessions: list[tuple[_MutableNodeObservation, OwnedServiceSession]] = []
    actual_start_order: list[str] = []
    teardown_attempt_order: list[str] = []
    actual_teardown_order: list[str] = []
    services_ready = False
    callback_started = False
    callback_completed = False
    trigger_reason = "NONE"
    cleanup_obligations_complete = True

    def event(stage: str, result: str) -> None:
        events.append(
            BootstrapLifecycleEvent(
                ordinal=len(events) + 1,
                stage=stage,
                result=result,
                elapsed_ms=round((time.monotonic() - started) * 1000, 3),
            )
        )

    def abort_if_needed() -> bool:
        nonlocal trigger_reason
        if cancel_event is not None and cancel_event.is_set():
            trigger_reason = "USER_CANCELLED"
            return True
        if time.monotonic() >= deadline:
            trigger_reason = "LIFECYCLE_TIMEOUT"
            return True
        return False

    event("PREPARED", "ENTERED")
    try:
        for index, node in enumerate(mutable):
            if abort_if_needed():
                event("ABORTING", trigger_reason)
                break
            stage = f"{node.spec.role}_STARTING"
            event(stage, "ENTERED")
            limits = node.spec.limits
            shutdown = node.spec.shutdown
            try:
                session = session_factory(
                    node_id=node.spec.node_id,
                    executable=node.spec.executable,
                    arguments=node.spec.arguments,
                    working_directory=node.spec.working_directory,
                    environment=node.spec.environment,
                    port=node.spec.port,
                    max_stdout_bytes=limits["max_stdout_bytes"],
                    max_stderr_bytes=limits["max_stderr_bytes"],
                    max_processes=limits["max_processes"],
                    process_release_timeout_ms=shutdown[
                        "process_release_timeout_ms"
                    ],
                    port_release_timeout_ms=shutdown["port_release_timeout_ms"],
                    reader_shutdown_timeout_ms=shutdown[
                        "reader_shutdown_timeout_ms"
                    ],
                )
            except OwnedServiceStartError as exc:
                node.start = exc.observation
                cleanup_obligations_complete = (
                    cleanup_obligations_complete
                    and exc.observation.cleanup_complete
                )
                trigger_reason = "COLLECTOR_ERROR"
                event(stage, exc.error_type)
                event("ABORTING", trigger_reason)
                break
            except Exception:
                cleanup_obligations_complete = False
                trigger_reason = "COLLECTOR_ERROR"
                event(stage, "SERVICE_START_INTERNAL_ERROR")
                event("ABORTING", trigger_reason)
                break
            node.start = session.start_observation
            sessions.append((node, session))
            actual_start_order.append(node.spec.node_id)
            event(stage, "STARTED")

            try:
                readiness = readiness_probe(
                    session,
                    node.spec.readiness,
                    cancel_event=cancel_event,
                    lifecycle_deadline=deadline,
                )
            except Exception:
                trigger_reason = "COLLECTOR_ERROR"
                event(f"{node.spec.role}_READY", "PROBE_INTERNAL_ERROR")
                event("ABORTING", trigger_reason)
                break
            node.readiness = readiness
            if not readiness.ready:
                trigger_reason = _stop_reason(readiness.error_type)
                event(f"{node.spec.role}_READY", readiness.error_type or "FAILED")
                event("ABORTING", trigger_reason)
                break
            event(f"{node.spec.role}_READY", "READY")
            if index == 1:
                services_ready = True
                event("SERVICES_READY", "READY")
        else:
            if abort_if_needed():
                event("ABORTING", trigger_reason)
            elif on_services_ready is not None:
                callback_started = True
                try:
                    on_services_ready()
                    callback_completed = True
                except Exception:
                    trigger_reason = "COLLECTOR_ERROR"
                    event("SERVICES_READY_CALLBACK", "FAILED")
                    event("ABORTING", trigger_reason)
                else:
                    event("SERVICES_READY_CALLBACK", "COMPLETED")
                    if abort_if_needed():
                        event("ABORTING", trigger_reason)
    finally:
        if on_evidence_finalize is not None:
            pre_teardown_nodes = tuple(
                BootstrapNodeObservation(
                    node_id=node.spec.node_id,
                    role=node.spec.role,
                    start=node.start,
                    readiness=node.readiness,
                    teardown=None,
                )
                for node in mutable
            )
            pre_teardown_streams: list[BootstrapPreTeardownStreams] = []
            sessions_by_node = {node.spec.node_id: session for node, session in sessions}
            for spec in specs:
                session = sessions_by_node.get(spec.node_id)
                stdout: CapturedStream | None = None
                stderr: CapturedStream | None = None
                if session is not None and hasattr(session, "snapshot_streams"):
                    try:
                        stdout, stderr = session.snapshot_streams()
                    except Exception:
                        stdout = None
                        stderr = None
                pre_teardown_streams.append(
                    BootstrapPreTeardownStreams(
                        node_id=spec.node_id,
                        stdout=stdout,
                        stderr=stderr,
                    )
                )
            try:
                on_evidence_finalize(
                    BootstrapPreTeardownObservation(
                        expected_start_order=(specs[0].node_id, specs[1].node_id),
                        actual_start_order=tuple(actual_start_order),
                        expected_teardown_order=(specs[1].node_id, specs[0].node_id),
                        events=tuple(events),
                        nodes=(pre_teardown_nodes[0], pre_teardown_nodes[1]),
                        services_ready=services_ready,
                        ready_callback_started=callback_started,
                        ready_callback_completed=callback_completed,
                        trigger_reason=trigger_reason,
                        streams=tuple(pre_teardown_streams),
                    )
                )
            except Exception:
                trigger_reason = "EVIDENCE_ERROR"
                event("EVIDENCE_FINALIZATION", "FAILED")
                event("ABORTING", trigger_reason)
            else:
                event("EVIDENCE_FINALIZED", "COMPLETE")
        for node, session in reversed(sessions):
            teardown_attempt_order.append(node.spec.node_id)
            event(f"TEARDOWN_{node.spec.role}", "ENTERED")
            try:
                node.teardown = session.terminate()
            except Exception:
                event(f"TEARDOWN_{node.spec.role}", "INTERNAL_ERROR")
                continue
            actual_teardown_order.append(node.spec.node_id)
            event(
                f"TEARDOWN_{node.spec.role}",
                "COMPLETE" if node.teardown.cleanup_complete else "INCOMPLETE",
            )

    cleanup_complete = (
        cleanup_obligations_complete
        and len(actual_teardown_order) == len(sessions)
        and all(
            node.teardown is not None and node.teardown.cleanup_complete
            for node, _ in sessions
        )
    )
    stop_reason = trigger_reason
    if not cleanup_complete:
        stop_reason = "CLEANUP_ERROR"
    event("TEARDOWN_COMPLETE", "COMPLETE" if cleanup_complete else "INCOMPLETE")
    observations = tuple(
        BootstrapNodeObservation(
            node_id=node.spec.node_id,
            role=node.spec.role,
            start=node.start,
            readiness=node.readiness,
            teardown=node.teardown,
        )
        for node in mutable
    )
    return BootstrapLifecycleObservation(
        expected_start_order=(specs[0].node_id, specs[1].node_id),
        actual_start_order=tuple(actual_start_order),
        expected_teardown_order=(specs[1].node_id, specs[0].node_id),
        actual_teardown_order=tuple(actual_teardown_order),
        teardown_attempt_order=tuple(teardown_attempt_order),
        events=tuple(events),
        nodes=(observations[0], observations[1]),
        services_ready=services_ready,
        ready_callback_started=callback_started,
        ready_callback_completed=callback_completed,
        trigger_reason=trigger_reason,
        stop_reason=stop_reason,
        cleanup_complete=cleanup_complete,
        elapsed_ms=round((time.monotonic() - started) * 1000, 3),
    )
