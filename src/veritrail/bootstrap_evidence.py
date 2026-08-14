from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Sequence

from veritrail.bootstrap_lifecycle import BootstrapLifecycleObservation
from veritrail.canonical import sha256_json
from veritrail.command_execution import sanitize_output
from veritrail.evidence import (
    EvidenceAttachment,
    ImportedEvidence,
    create_text_attachment,
    import_evidence_document,
)
from veritrail.errors import SafetyError
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.windows_job import CapturedStream

COLLECTOR_VERSION = "bootstrap-lifecycle/0.3"
M10_COLLECTOR_VERSION = "bootstrap-lifecycle/0.2"
LEGACY_COLLECTOR_VERSION = "bootstrap-lifecycle/0.1"
LISTENER_OWNER_BACKEND = "WINDOWS_IP_HELPER_CTYPES_IPV4"
PROCESS_OWNERSHIP_BACKEND = "WINDOWS_JOB_OBJECT_PYWIN32_312"

STOP_REASONS = {
    "NONE",
    "RESOURCE_PREFLIGHT",
    "PORT_CONFLICT",
    "UNSUPPORTED_COLD_STATE",
    "EXECUTABLE_DRIFT",
    "SUBJECT_DRIFT",
    "READINESS_TIMEOUT",
    "LISTENER_OWNERSHIP_MISMATCH",
    "NODE_EARLY_EXIT",
    "USER_CANCELLED",
    "LIFECYCLE_TIMEOUT",
    "RESOURCE_MEMORY_SOFT_LIMIT",
    "RESOURCE_MEMORY_HARD_LIMIT",
    "BROWSER_HARD_FAILURE",
    "COLLECTOR_ERROR",
    "EVIDENCE_ERROR",
    "CLEANUP_ERROR",
}

STOP_CATEGORIES = {
    "NONE": "NONE",
    "RESOURCE_PREFLIGHT": "RESOURCE",
    "PORT_CONFLICT": "SAFETY",
    "UNSUPPORTED_COLD_STATE": "SAFETY",
    "EXECUTABLE_DRIFT": "SAFETY",
    "SUBJECT_DRIFT": "SAFETY",
    "READINESS_TIMEOUT": "SAFETY",
    "LISTENER_OWNERSHIP_MISMATCH": "SAFETY",
    "NODE_EARLY_EXIT": "SUBJECT",
    "USER_CANCELLED": "USER",
    "LIFECYCLE_TIMEOUT": "RESOURCE",
    "RESOURCE_MEMORY_SOFT_LIMIT": "RESOURCE",
    "RESOURCE_MEMORY_HARD_LIMIT": "RESOURCE",
    "BROWSER_HARD_FAILURE": "SUBJECT",
    "COLLECTOR_ERROR": "ERROR",
    "EVIDENCE_ERROR": "ERROR",
    "CLEANUP_ERROR": "ERROR",
}

RESOURCE_FIELDS = {
    "core_peak_rss_mb",
    "dependency_peak_rss_mb",
    "application_peak_rss_mb",
    "browser_peak_rss_mb",
    "host_available_memory_min_mb",
    "available_memory_soft_min_mb",
    "available_memory_hard_min_mb",
    "hard_breach_grace_samples",
    "max_consecutive_memory_hard_breaches",
    "limit_trigger_reason",
    "sampling_complete",
}
LEGACY_RESOURCE_FIELDS = {
    "core_peak_rss_mb",
    "dependency_peak_rss_mb",
    "application_peak_rss_mb",
    "browser_peak_rss_mb",
    "sampling_complete",
}
SUBJECT_FIELDS = {
    "before_fingerprint",
    "after_fingerprint",
    "changed",
    "scan_complete",
}
METADATA = {
    "structured_arguments": True,
    "environment_values_persisted": False,
    "absolute_paths_persisted": False,
    "raw_output_persisted": False,
    "response_bodies_persisted": False,
    "process_ids_persisted": False,
    "filesystem_isolation": "NOT_PROVEN",
    "network_isolation": "NOT_PROVEN",
    "graceful_shutdown": "NOT_PROVEN",
    "executable_toctou_containment": "NOT_PROVEN",
    "untrusted_code": "NOT_SUPPORTED",
    "listener_owner_backend": LISTENER_OWNER_BACKEND,
    "process_ownership_backend": PROCESS_OWNERSHIP_BACKEND,
}


@dataclass(frozen=True)
class BootstrapEvidenceResult:
    bootstrap: ImportedEvidence
    execution_status: str
    continue_pipeline: bool


def _empty_stream() -> CapturedStream:
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
    attachment: EvidenceAttachment,
    *,
    replacements: list[tuple[str, str]],
    limit: int,
) -> dict[str, Any]:
    sanitized = sanitize_output(
        stream.content,
        replacements=replacements,
        max_persisted_bytes=limit,
    )
    if sanitized.content != attachment.content:
        raise SafetyError("M10 bootstrap stream attachment does not match sanitized output")
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


def _execution_status(reason: str, browser_completed: bool, cleanup_complete: bool) -> str:
    if not cleanup_complete or reason in {"COLLECTOR_ERROR", "EVIDENCE_ERROR", "CLEANUP_ERROR"}:
        return "ERROR"
    if reason == "NODE_EARLY_EXIT":
        return "COMPLETED"
    if reason in {"SUBJECT_DRIFT", "BROWSER_HARD_FAILURE"} and browser_completed:
        return "COMPLETED"
    if reason == "NONE":
        return "COMPLETED" if browser_completed else "ERROR"
    if reason in {
        "RESOURCE_PREFLIGHT",
        "PORT_CONFLICT",
        "UNSUPPORTED_COLD_STATE",
        "SUBJECT_DRIFT",
        "READINESS_TIMEOUT",
        "LISTENER_OWNERSHIP_MISMATCH",
        "USER_CANCELLED",
        "LIFECYCLE_TIMEOUT",
        "RESOURCE_MEMORY_SOFT_LIMIT",
        "RESOURCE_MEMORY_HARD_LIMIT",
        "BROWSER_HARD_FAILURE",
    }:
        return "ABORTED"
    return "ERROR"


def _validate_preview(plan: dict[str, Any], profile: dict[str, Any], preview: dict[str, Any]) -> None:
    digest = preview.get("preview_sha256")
    unsigned = {key: value for key, value in preview.items() if key != "preview_sha256"}
    if not isinstance(digest, str) or digest != sha256_json(unsigned):
        raise SafetyError("M10 approved bootstrap Preview seal is invalid")
    expected = {
        "schema_version": "0.2" if plan["schema_version"] == "0.7" else "0.1",
        "plan_sha256": plan["seal"]["digest"],
        "profile_id": profile["profile_id"],
        "profile_version": profile["version"],
        "profile_sha256": profile["seal"]["digest"],
        "platform": profile["platform"],
        "cold_state": profile["cold_state"],
        "start_order": profile["start_order"],
        "teardown_order": profile["teardown_order"],
    }
    if plan["schema_version"] == "0.7":
        expected["topology"] = profile["topology"]
    if any(preview.get(key) != value for key, value in expected.items()):
        raise SafetyError("M10 approved bootstrap Preview identity drifted")


def _validate_observation_inputs(
    resource_observation: dict[str, Any], subject_observation: dict[str, Any]
) -> None:
    if set(resource_observation) != RESOURCE_FIELDS:
        raise SafetyError("M10 resource observation must contain exact fields")
    for name in RESOURCE_FIELDS - {"sampling_complete", "limit_trigger_reason"}:
        value = resource_observation[name]
        if value is not None and (
            not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0
        ):
            raise SafetyError("M10 resource observations must be non-negative or null")
    for name in (
        "available_memory_soft_min_mb",
        "available_memory_hard_min_mb",
        "hard_breach_grace_samples",
        "max_consecutive_memory_hard_breaches",
    ):
        value = resource_observation[name]
        if not isinstance(value, int) or isinstance(value, bool):
            raise SafetyError("M10 resource policies and counters must be integers")
    soft = resource_observation["available_memory_soft_min_mb"]
    hard = resource_observation["available_memory_hard_min_mb"]
    grace = resource_observation["hard_breach_grace_samples"]
    streak = resource_observation["max_consecutive_memory_hard_breaches"]
    if soft <= 0 or hard <= 0 or soft < hard or grace < 1 or streak < 0:
        raise SafetyError("M10 resource policies and counters are outside their bounds")
    if not isinstance(resource_observation["sampling_complete"], bool):
        raise SafetyError("M10 resource sampling completeness must be a boolean")
    if resource_observation["limit_trigger_reason"] not in {
        None,
        "RESOURCE_MEMORY_SOFT_LIMIT",
        "RESOURCE_MEMORY_HARD_LIMIT",
    }:
        raise SafetyError("M10 resource stop reason is invalid")
    if set(subject_observation) != SUBJECT_FIELDS:
        raise SafetyError("M10 subject observation must contain exact fields")
    for name in ("before_fingerprint", "after_fingerprint"):
        value = subject_observation[name]
        if value is not None and (
            not isinstance(value, str)
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise SafetyError("M10 subject fingerprints must be lowercase SHA-256 or null")
    if subject_observation["changed"] is not None and not isinstance(
        subject_observation["changed"], bool
    ):
        raise SafetyError("M10 subject changed observation must be boolean or null")
    if not isinstance(subject_observation["scan_complete"], bool):
        raise SafetyError("M10 subject scan completeness must be a boolean")


def collect_bootstrap_evidence(
    plan: dict[str, Any],
    profile: dict[str, Any],
    preview: dict[str, Any],
    lifecycle: BootstrapLifecycleObservation,
    *,
    browser_exercise: dict[str, Any],
    resource_observation: dict[str, Any],
    subject_observation: dict[str, Any],
    run_work_released: bool,
    staging_released: bool,
    path_replacements: Sequence[tuple[str, str]] = (),
    captured_at: str | None = None,
) -> BootstrapEvidenceResult:
    """Freeze a completed lifecycle observation into strict bootstrap Evidence."""

    verify_sealed_project_profile(profile)
    verify_sealed_plan(plan, profile)
    plan_version = plan.get("schema_version")
    if plan_version not in {"0.6", "0.7"}:
        raise SafetyError("bootstrap Evidence requires ExperimentPlan 0.6 or 0.7")
    _validate_preview(plan, profile, preview)
    _validate_observation_inputs(resource_observation, subject_observation)
    if set(browser_exercise) != {
        "started",
        "completed",
        "evidence_sha256",
        "job_memory_limit_mb",
        "job_memory_limit_enforced",
        "process_cleanup_complete",
    }:
        raise SafetyError("M10 browser exercise must contain exact fields")
    if not isinstance(browser_exercise["started"], bool) or not isinstance(
        browser_exercise["completed"], bool
    ):
        raise SafetyError("M10 browser exercise states must be booleans")
    if (
        browser_exercise["started"]
        and not isinstance(browser_exercise["process_cleanup_complete"], bool)
    ) or (
        not browser_exercise["started"]
        and browser_exercise["process_cleanup_complete"] is not None
    ):
        raise SafetyError("M10 browser process cleanup state conflicts with startup")
    if (
        not isinstance(browser_exercise["job_memory_limit_mb"], int)
        or isinstance(browser_exercise["job_memory_limit_mb"], bool)
        or not 128 <= browser_exercise["job_memory_limit_mb"] <= 2048
        or not isinstance(browser_exercise["job_memory_limit_enforced"], bool)
        or (
            browser_exercise["completed"]
            and not browser_exercise["job_memory_limit_enforced"]
        )
    ):
        raise SafetyError("M10 browser Job memory limit was not validly enforced")
    browser_digest = browser_exercise["evidence_sha256"]
    if browser_digest is not None and (
        not isinstance(browser_digest, str)
        or len(browser_digest) != 64
        or any(character not in "0123456789abcdef" for character in browser_digest)
    ):
        raise SafetyError("M10 browser Evidence reference must be SHA-256 or null")
    if browser_exercise["completed"] and (
        not browser_exercise["started"] or browser_digest is None
    ):
        raise SafetyError("M10 completed browser exercise requires its Evidence identity")
    if not isinstance(run_work_released, bool) or not isinstance(staging_released, bool):
        raise SafetyError("M10 cleanup release observations must be booleans")

    profile_nodes = {node["node_id"]: node for node in profile["nodes"]}
    lifecycle_nodes = {node.node_id: node for node in lifecycle.nodes}
    if tuple(lifecycle.expected_start_order) != tuple(profile["start_order"]):
        raise SafetyError("M10 lifecycle start order differs from the sealed Profile")
    if tuple(lifecycle.expected_teardown_order) != tuple(profile["teardown_order"]):
        raise SafetyError("M10 lifecycle teardown order differs from the sealed Profile")
    if set(lifecycle_nodes) != set(profile_nodes):
        raise SafetyError("M10 lifecycle nodes differ from the sealed Profile")
    finalized = [
        index
        for index, event in enumerate(lifecycle.events)
        if event.stage == "EVIDENCE_FINALIZED" and event.result == "COMPLETE"
    ]
    staging_failed = [
        index
        for index, event in enumerate(lifecycle.events)
        if event.stage == "EVIDENCE_FINALIZATION"
        and event.result == "EVIDENCE_STAGING_FAILED"
    ]
    teardown_events = [
        index
        for index, event in enumerate(lifecycle.events)
        if event.stage.startswith("TEARDOWN_")
    ]
    normal_finalization = len(finalized) == 1 and not staging_failed
    failure_finalization = (
        not finalized
        and len(staging_failed) == 1
        and lifecycle.stop_reason == "EVIDENCE_ERROR"
    )
    finalization_index = (
        finalized[0]
        if normal_finalization
        else staging_failed[0]
        if failure_finalization
        else None
    )
    if finalization_index is None or (
        teardown_events and finalization_index >= min(teardown_events)
    ):
        raise SafetyError(
            "M10 bootstrap Evidence requires one successful or explicit failed pre-teardown finalization"
        )

    replacements = [(left, right) for left, right in path_replacements if left]
    attachments: list[EvidenceAttachment] = []
    prepared_streams: dict[tuple[str, str], tuple[CapturedStream, EvidenceAttachment]] = {}
    for node_id in profile["start_order"]:
        policy = profile_nodes[node_id]
        observation = lifecycle_nodes[node_id]
        teardown = observation.teardown
        for stream_name in ("stdout", "stderr"):
            stream = getattr(teardown, stream_name) if teardown is not None else _empty_stream()
            sanitized = sanitize_output(
                stream.content,
                replacements=replacements,
                max_persisted_bytes=policy["limits"][f"max_{stream_name}_bytes"],
            )
            attachment = create_text_attachment(
                path=f"attachments/bootstrap/{node_id}/{stream_name}.txt",
                content=sanitized.content,
                logical_name=f"bootstrap-{node_id}-{stream_name}",
            )
            attachments.append(attachment)
            prepared_streams[(node_id, stream_name)] = (stream, attachment)

    node_facts: list[dict[str, Any]] = []
    for node_id in profile["start_order"]:
        policy = profile_nodes[node_id]
        observation = lifecycle_nodes[node_id]
        start = observation.start
        readiness = observation.readiness
        teardown = observation.teardown
        streams: dict[str, dict[str, Any]] = {}
        for stream_name in ("stdout", "stderr"):
            stream, attachment = prepared_streams[(node_id, stream_name)]
            streams[stream_name] = _stream_facts(
                stream,
                attachment,
                replacements=replacements,
                limit=policy["limits"][f"max_{stream_name}_bytes"],
            )
        attempts = [] if readiness is None else [
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
        ]
        error_type = (
            teardown.error_type
            if teardown is not None and teardown.error_type is not None
            else readiness.error_type
            if readiness is not None and readiness.error_type is not None
            else start.error_type
            if start is not None
            else None
        )
        node_facts.append(
            {
                "node_id": node_id,
                "role": policy["role"],
                "policy_sha256": sha256_json(policy),
                "process_created": start.process_created if start is not None else False,
                "target_assigned": start.target_assigned if start is not None else False,
                "target_resumed": start.target_resumed if start is not None else False,
                "root_exit_code": teardown.root_exit_code if teardown is not None else None,
                "termination_reason": (
                    teardown.termination_reason
                    if teardown is not None
                    else "START_FAILED"
                    if start is not None
                    else "NOT_STARTED"
                ),
                "error_type": error_type,
                "job": {
                    "backend": PROCESS_OWNERSHIP_BACKEND,
                    "parent_in_job": start.parent_in_job if start is not None else None,
                    "active_process_limit": policy["limits"]["max_processes"],
                    "active_process_limit_enforced": (
                        start.active_process_limit_enforced if start is not None else False
                    ),
                    "job_memory_limit_mb": policy["limits"]["max_job_memory_mb"],
                    "job_memory_limit_enforced": (
                        start.job_memory_limit_enforced if start is not None else False
                    ),
                    "total_assigned_processes": (
                        teardown.total_assigned_processes if teardown is not None else 0
                    ),
                    "final_active_processes": (
                        teardown.final_active_processes if teardown is not None else 0
                    ),
                    "handles_released": (
                        teardown.handles_released
                        if teardown is not None
                        else start.cleanup_complete
                        if start is not None
                        else True
                    ),
                },
                "readiness": {
                    "adapter": policy["readiness"]["adapter"],
                    "ready": readiness.ready if readiness is not None else False,
                    "error_type": readiness.error_type if readiness is not None else None,
                    "elapsed_ms": readiness.elapsed_ms if readiness is not None else 0.0,
                    "attempts": attempts,
                },
                "stdout": streams["stdout"],
                "stderr": streams["stderr"],
                "teardown": {
                    "requested": teardown.requested if teardown is not None else False,
                    "job_empty": (
                        teardown.final_active_processes == 0 if teardown is not None else True
                    ),
                    "root_signaled": teardown.root_signaled if teardown is not None else False,
                    "handles_released": (
                        teardown.handles_released
                        if teardown is not None
                        else start.cleanup_complete
                        if start is not None
                        else True
                    ),
                    "readers_released": teardown.readers_released if teardown is not None else True,
                    "port_free": teardown.port_free if teardown is not None else True,
                    "elapsed_ms": teardown.elapsed_ms if teardown is not None else 0.0,
                },
            }
        )

    node_cleanup = all(
        node["teardown"][field]
        for node in node_facts
        for field in ("job_empty", "handles_released", "readers_released", "port_free")
    )
    expected_actual_teardown = list(reversed(lifecycle.actual_start_order))
    cleanup = {
        "reverse_order_complete": list(lifecycle.actual_teardown_order)
        == expected_actual_teardown
        and list(lifecycle.teardown_attempt_order) == list(lifecycle.actual_teardown_order),
        "jobs_empty": all(node["teardown"]["job_empty"] for node in node_facts),
        "handles_released": all(node["teardown"]["handles_released"] for node in node_facts),
        "readers_released": all(node["teardown"]["readers_released"] for node in node_facts),
        "ports_free": all(node["teardown"]["port_free"] for node in node_facts),
        "run_work_released": run_work_released,
        "staging_released": staging_released,
    }
    cleanup_complete = (
        lifecycle.cleanup_complete
        and node_cleanup
        and all(cleanup.values())
        and (
            not browser_exercise["started"]
            or browser_exercise["process_cleanup_complete"] is True
        )
        and tuple(lifecycle.actual_teardown_order)
        == tuple(reversed(lifecycle.actual_start_order))
    )
    reason = lifecycle.stop_reason
    if reason not in STOP_REASONS:
        reason = "COLLECTOR_ERROR"
    if not subject_observation["scan_complete"] or not resource_observation["sampling_complete"]:
        reason = "EVIDENCE_ERROR"
    elif subject_observation["changed"] is True:
        reason = "SUBJECT_DRIFT"
    elif reason == "NONE" and not browser_exercise["completed"]:
        reason = (
            "BROWSER_HARD_FAILURE"
            if browser_exercise["started"]
            else "COLLECTOR_ERROR"
        )
    if not cleanup_complete:
        reason = "CLEANUP_ERROR"
    browser_completed = bool(browser_exercise["completed"])
    execution_status = _execution_status(reason, browser_completed, cleanup_complete)
    stop_stage = lifecycle.events[-1].stage if lifecycle.events else "DISCOVERED"
    collector_version = (
        COLLECTOR_VERSION if plan_version == "0.7" else M10_COLLECTOR_VERSION
    )
    observed_variables = (
        {
            "project_bootstrap_topology": (
                "veritrail_managed_windows_c1_single_application"
            )
        }
        if plan_version == "0.7"
        else {
            "project_bootstrap_mode": (
                "veritrail_managed_windows_c1_two_node_services"
            )
        }
    )
    document = {
        "schema_version": "0.1",
        "evidence_type": "runtime.bootstrap",
        "source": f"VeriTrail {collector_version}",
        "captured_at": captured_at
        or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "facts": {
            "plan_sha256": plan["seal"]["digest"],
            "profile": {
                "id": profile["profile_id"],
                "version": profile["version"],
                "sha256": profile["seal"]["digest"],
            },
            "preview_sha256": preview["preview_sha256"],
            "platform": {
                "declared": profile["platform"],
                "observed": "WINDOWS_11",
                "supported": profile["platform"] == "WINDOWS_11",
            },
            "cold_state": {
                "declared": profile["cold_state"],
                "observed": "C1_PROCESS_COLD",
                "supported": profile["cold_state"] == "C1_PROCESS_COLD",
            },
            "start_order": {
                "sealed": list(profile["start_order"]),
                "actual": list(lifecycle.actual_start_order),
            },
            "teardown_order": {
                "sealed": list(profile["teardown_order"]),
                "attempted": list(lifecycle.teardown_attempt_order),
                "completed": list(lifecycle.actual_teardown_order),
            },
            "lifecycle_events": [
                {
                    "ordinal": event.ordinal,
                    "stage": event.stage,
                    "result": event.result,
                    "elapsed_ms": event.elapsed_ms,
                }
                for event in lifecycle.events
            ],
            "nodes": node_facts,
            "services_ready": lifecycle.services_ready,
            "browser_exercise": dict(browser_exercise),
            "stop": {
                "reason": reason,
                "stage": stop_stage,
                "category": STOP_CATEGORIES[reason],
            },
            "resource_observation": dict(resource_observation),
            "subject_observation": dict(subject_observation),
            "cleanup": cleanup,
            "cleanup_complete": cleanup_complete,
        },
        "observed_variables": observed_variables,
        "metadata": dict(METADATA),
    }
    artifact = import_evidence_document(
        document,
        "generated-bootstrap.json",
        attachments=tuple(attachments),
    )
    return BootstrapEvidenceResult(
        bootstrap=artifact,
        execution_status=execution_status,
        continue_pipeline=(
            execution_status == "COMPLETED"
            and lifecycle.services_ready
            and browser_completed
            and cleanup_complete
            and subject_observation["scan_complete"]
            and subject_observation["changed"] is False
        ),
    )


def validate_bootstrap_evidence(
    document: dict[str, Any], input_name: str, errors: list[str]
) -> None:
    facts = document.get("facts")
    fact_fields = {
        "plan_sha256",
        "profile",
        "preview_sha256",
        "platform",
        "cold_state",
        "start_order",
        "teardown_order",
        "lifecycle_events",
        "nodes",
        "services_ready",
        "browser_exercise",
        "stop",
        "resource_observation",
        "subject_observation",
        "cleanup",
        "cleanup_complete",
    }
    if not isinstance(facts, dict) or set(facts) != fact_fields:
        errors.append(f"{input_name}.facts must contain exact bootstrap fields")
        return
    source = document.get("source")
    if source not in {
        f"VeriTrail {COLLECTOR_VERSION}",
        f"VeriTrail {M10_COLLECTOR_VERSION}",
        f"VeriTrail {LEGACY_COLLECTOR_VERSION}",
    }:
        errors.append(f"{input_name}.source must identify the frozen bootstrap collector")
    current_collector = source in {
        f"VeriTrail {COLLECTOR_VERSION}",
        f"VeriTrail {M10_COLLECTOR_VERSION}",
    }
    single_node_collector = source == f"VeriTrail {COLLECTOR_VERSION}"
    expected_variables = (
        {
            "project_bootstrap_topology": (
                "veritrail_managed_windows_c1_single_application"
            )
        }
        if single_node_collector
        else {
            "project_bootstrap_mode": (
                "veritrail_managed_windows_c1_two_node_services"
            )
        }
    )
    if document.get("observed_variables") != expected_variables:
        errors.append(f"{input_name}.observed_variables must contain the frozen bootstrap mode")

    def sha(value: Any) -> bool:
        return (
            isinstance(value, str)
            and len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
        )

    def number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0

    def nonnegative_integer(value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0

    if not sha(facts["plan_sha256"]) or not sha(facts["preview_sha256"]):
        errors.append(f"{input_name}.facts policy identities must be lowercase SHA-256")
    profile = facts["profile"]
    if (
        not isinstance(profile, dict)
        or set(profile) != {"id", "version", "sha256"}
        or not isinstance(profile.get("id"), str)
        or not isinstance(profile.get("version"), int)
        or isinstance(profile.get("version"), bool)
        or profile.get("version", 0) < 1
        or not sha(profile.get("sha256"))
    ):
        errors.append(f"{input_name}.facts.profile is invalid")
    for field, declared in (("platform", "WINDOWS_11"), ("cold_state", "C1_PROCESS_COLD")):
        value = facts[field]
        if (
            not isinstance(value, dict)
            or set(value) != {"declared", "observed", "supported"}
            or value.get("declared") != declared
            or value.get("observed") != declared
            or value.get("supported") is not True
        ):
            errors.append(f"{input_name}.facts.{field} is invalid")
    start = facts["start_order"]
    teardown = facts["teardown_order"]
    if not isinstance(start, dict) or set(start) != {"sealed", "actual"}:
        errors.append(f"{input_name}.facts.start_order must contain exact fields")
    if not isinstance(teardown, dict) or set(teardown) != {"sealed", "attempted", "completed"}:
        errors.append(f"{input_name}.facts.teardown_order must contain exact fields")
    sealed_start = start.get("sealed", []) if isinstance(start, dict) else []
    sealed_teardown = teardown.get("sealed", []) if isinstance(teardown, dict) else []
    expected_node_count = 1 if single_node_collector else 2
    if (
        not isinstance(sealed_start, list)
        or len(sealed_start) != expected_node_count
        or any(not isinstance(item, str) for item in sealed_start)
        or sealed_teardown != list(reversed(sealed_start))
    ):
        errors.append(f"{input_name}.facts sealed lifecycle order is invalid")
    actual_start = start.get("actual", []) if isinstance(start, dict) else []
    attempted_teardown = teardown.get("attempted", []) if isinstance(teardown, dict) else []
    completed_teardown = teardown.get("completed", []) if isinstance(teardown, dict) else []
    if (
        not isinstance(actual_start, list)
        or actual_start != sealed_start[: len(actual_start)]
        or attempted_teardown != list(reversed(actual_start))
        or completed_teardown != attempted_teardown
    ):
        errors.append(f"{input_name}.facts observed lifecycle order is invalid")
    events = facts["lifecycle_events"]
    if not isinstance(events, list):
        errors.append(f"{input_name}.facts.lifecycle_events must be a list")
    else:
        for index, event in enumerate(events, start=1):
            if (
                not isinstance(event, dict)
                or set(event) != {"ordinal", "stage", "result", "elapsed_ms"}
                or event.get("ordinal") != index
                or not isinstance(event.get("stage"), str)
                or not isinstance(event.get("result"), str)
                or not number(event.get("elapsed_ms"))
            ):
                errors.append(f"{input_name}.facts.lifecycle_events[{index - 1}] is invalid")
        finalized = [
            index
            for index, event in enumerate(events)
            if isinstance(event, dict)
            and event.get("stage") == "EVIDENCE_FINALIZED"
            and event.get("result") == "COMPLETE"
        ]
        staging_failed = [
            index
            for index, event in enumerate(events)
            if isinstance(event, dict)
            and event.get("stage") == "EVIDENCE_FINALIZATION"
            and event.get("result") == "EVIDENCE_STAGING_FAILED"
        ]
        teardown_events = [
            index
            for index, event in enumerate(events)
            if isinstance(event, dict)
            and isinstance(event.get("stage"), str)
            and event["stage"].startswith("TEARDOWN_")
        ]
        stop_reason = (
            facts.get("stop", {}).get("reason")
            if isinstance(facts.get("stop"), dict)
            else None
        )
        normal_finalization = len(finalized) == 1 and not staging_failed
        failure_finalization = (
            not finalized
            and len(staging_failed) == 1
            and stop_reason == "EVIDENCE_ERROR"
        )
        finalization_index = (
            finalized[0]
            if normal_finalization
            else staging_failed[0]
            if failure_finalization
            else None
        )
        if finalization_index is None or (
            teardown_events and finalization_index >= min(teardown_events)
        ):
            errors.append(
                f"{input_name}.facts lifecycle must record a successful or explicit failed pre-teardown finalization before cleanup"
            )
    nodes = facts["nodes"]
    node_fields = {
        "node_id", "role", "policy_sha256", "process_created", "target_assigned",
        "target_resumed", "root_exit_code", "termination_reason", "error_type", "job",
        "readiness", "stdout", "stderr", "teardown",
    }
    if not isinstance(nodes, list) or len(nodes) != expected_node_count:
        errors.append(
            f"{input_name}.facts.nodes must contain exactly {expected_node_count} node(s)"
        )
        nodes = []
    for index, node in enumerate(nodes):
        prefix = f"{input_name}.facts.nodes[{index}]"
        if not isinstance(node, dict) or set(node) != node_fields:
            errors.append(f"{prefix} must contain exact node fields")
            continue
        if (
            node.get("node_id")
            != (
                sealed_start[index]
                if len(sealed_start) == expected_node_count
                else None
            )
            or node.get("role")
            not in ({"APPLICATION"} if single_node_collector else {"DEPENDENCY", "APPLICATION"})
            or not sha(node.get("policy_sha256"))
        ):
            errors.append(f"{prefix} identity is invalid")
        for field in ("process_created", "target_assigned", "target_resumed"):
            if not isinstance(node.get(field), bool):
                errors.append(f"{prefix}.{field} must be a boolean")
        if node.get("target_assigned") is True and node.get("process_created") is not True:
            errors.append(f"{prefix} cannot assign a process that was not created")
        if node.get("target_resumed") is True and node.get("target_assigned") is not True:
            errors.append(f"{prefix} cannot resume a process that was not assigned")
        if node.get("root_exit_code") is not None and (
            not isinstance(node.get("root_exit_code"), int)
            or isinstance(node.get("root_exit_code"), bool)
        ):
            errors.append(f"{prefix}.root_exit_code must be integer or null")
        if not isinstance(node.get("termination_reason"), str):
            errors.append(f"{prefix}.termination_reason must be a string category")
        if node.get("error_type") is not None and not isinstance(node.get("error_type"), str):
            errors.append(f"{prefix}.error_type must be string or null")
        job = node.get("job")
        job_fields = {
            "backend", "parent_in_job", "active_process_limit",
            "active_process_limit_enforced", "job_memory_limit_mb",
            "job_memory_limit_enforced", "total_assigned_processes",
            "final_active_processes", "handles_released",
        }
        if (
            not isinstance(job, dict)
            or set(job) != job_fields
            or job.get("backend") != PROCESS_OWNERSHIP_BACKEND
            or not (
                job.get("parent_in_job") is None
                or isinstance(job.get("parent_in_job"), bool)
            )
            or not nonnegative_integer(job.get("active_process_limit"))
            or not isinstance(job.get("active_process_limit_enforced"), bool)
            or not nonnegative_integer(job.get("job_memory_limit_mb"))
            or not isinstance(job.get("job_memory_limit_enforced"), bool)
            or not nonnegative_integer(job.get("total_assigned_processes"))
            or not nonnegative_integer(job.get("final_active_processes"))
            or not isinstance(job.get("handles_released"), bool)
        ):
            errors.append(f"{prefix}.job is invalid")
        elif (
            not 64 <= job["job_memory_limit_mb"] <= 2048
            or (
                node.get("target_assigned") is True
                and (
                    job["active_process_limit_enforced"] is not True
                    or job["job_memory_limit_enforced"] is not True
                )
            )
        ):
            errors.append(f"{prefix}.job did not enforce the sealed process and memory limits")
        readiness = node.get("readiness")
        if not isinstance(readiness, dict) or set(readiness) != {
            "adapter", "ready", "error_type", "elapsed_ms", "attempts"
        }:
            errors.append(f"{prefix}.readiness is invalid")
        else:
            if (
                readiness.get("adapter") != "HTTP_GET_LOOPBACK_OWNED_PID"
                or not isinstance(readiness.get("ready"), bool)
                or (
                    readiness.get("error_type") is not None
                    and not isinstance(readiness.get("error_type"), str)
                )
                or not number(readiness.get("elapsed_ms"))
            ):
                errors.append(f"{prefix}.readiness state is invalid")
            attempts = readiness.get("attempts")
            if not isinstance(attempts, list):
                errors.append(f"{prefix}.readiness.attempts must be a list")
            else:
                attempt_fields = {
                    "ordinal", "elapsed_ms", "result", "http_status",
                    "response_byte_count", "listener_owner_in_job",
                    "job_active_process_count",
                }
                for ordinal, attempt in enumerate(attempts, start=1):
                    if (
                        not isinstance(attempt, dict)
                        or set(attempt) != attempt_fields
                        or attempt.get("ordinal") != ordinal
                        or not number(attempt.get("elapsed_ms"))
                        or not isinstance(attempt.get("result"), str)
                        or not isinstance(attempt.get("listener_owner_in_job"), bool)
                        or not nonnegative_integer(attempt.get("job_active_process_count"))
                        or (
                            attempt.get("http_status") is not None
                            and not nonnegative_integer(attempt.get("http_status"))
                        )
                        or (
                            attempt.get("response_byte_count") is not None
                            and not nonnegative_integer(attempt.get("response_byte_count"))
                        )
                    ):
                        errors.append(f"{prefix}.readiness.attempts[{ordinal - 1}] is invalid")
        for stream_name in ("stdout", "stderr"):
            stream = node.get(stream_name)
            stream_fields = {
                "attachment", "observed_bytes_lower_bound", "stream_complete",
                "persisted_bytes", "truncated", "overflowed", "redaction_count",
                "invalid_utf8_replacements", "control_character_replacements",
            }
            if not isinstance(stream, dict) or set(stream) != stream_fields:
                errors.append(f"{prefix}.{stream_name} is invalid")
                continue
            attachment = stream.get("attachment")
            expected_path = f"attachments/bootstrap/{node.get('node_id')}/{stream_name}.txt"
            if (
                not isinstance(attachment, dict)
                or set(attachment) != {"path", "sha256", "size", "media_type", "logical_name"}
                or attachment.get("path") != expected_path
                or not sha(attachment.get("sha256"))
                or attachment.get("media_type") != "text/plain; charset=utf-8"
                or attachment.get("logical_name") != f"bootstrap-{node.get('node_id')}-{stream_name}"
                or attachment.get("size") != stream.get("persisted_bytes")
            ):
                errors.append(f"{prefix}.{stream_name}.attachment is invalid")
            for field in (
                "observed_bytes_lower_bound",
                "persisted_bytes",
                "redaction_count",
                "invalid_utf8_replacements",
                "control_character_replacements",
            ):
                if not nonnegative_integer(stream.get(field)):
                    errors.append(f"{prefix}.{stream_name}.{field} must be non-negative")
            for field in ("stream_complete", "truncated", "overflowed"):
                if not isinstance(stream.get(field), bool):
                    errors.append(f"{prefix}.{stream_name}.{field} must be a boolean")
            if stream.get("truncated") != stream.get("overflowed"):
                errors.append(f"{prefix}.{stream_name} truncation facts conflict")
        td = node.get("teardown")
        if not isinstance(td, dict) or set(td) != {
            "requested", "job_empty", "root_signaled", "handles_released",
            "readers_released", "port_free", "elapsed_ms"
        }:
            errors.append(f"{prefix}.teardown is invalid")
        elif (
            any(
                not isinstance(td.get(field), bool)
                for field in (
                    "requested", "job_empty", "root_signaled", "handles_released",
                    "readers_released", "port_free",
                )
            )
            or not number(td.get("elapsed_ms"))
        ):
            errors.append(f"{prefix}.teardown observations are invalid")
    browser = facts["browser_exercise"]
    expected_browser_fields = {
        "started", "completed", "evidence_sha256",
        "job_memory_limit_mb", "job_memory_limit_enforced",
    }
    if current_collector:
        expected_browser_fields.add("process_cleanup_complete")
    if (
        not isinstance(browser, dict)
        or set(browser) != expected_browser_fields
        or not isinstance(browser.get("started"), bool)
        or not isinstance(browser.get("completed"), bool)
        or not isinstance(browser.get("job_memory_limit_mb"), int)
        or isinstance(browser.get("job_memory_limit_mb"), bool)
        or not 128 <= browser.get("job_memory_limit_mb", 0) <= 2048
        or not isinstance(browser.get("job_memory_limit_enforced"), bool)
        or (
            browser.get("completed")
            and browser.get("job_memory_limit_enforced") is not True
        )
        or (browser.get("evidence_sha256") is not None and not sha(browser.get("evidence_sha256")))
        or (browser.get("completed") and (not browser.get("started") or browser.get("evidence_sha256") is None))
        or (
            current_collector
            and (
                (
                    browser.get("started")
                    and not isinstance(browser.get("process_cleanup_complete"), bool)
                )
                or (
                    not browser.get("started")
                    and browser.get("process_cleanup_complete") is not None
                )
            )
        )
    ):
        errors.append(f"{input_name}.facts.browser_exercise is invalid")
    stop = facts["stop"]
    allowed_stop_reasons = (
        STOP_REASONS
        if current_collector
        else STOP_REASONS
        - {"RESOURCE_MEMORY_SOFT_LIMIT", "RESOURCE_MEMORY_HARD_LIMIT"}
    )
    if (
        not isinstance(stop, dict)
        or set(stop) != {"reason", "stage", "category"}
        or stop.get("reason") not in allowed_stop_reasons
        or stop.get("category") != STOP_CATEGORIES.get(stop.get("reason"))
        or not isinstance(stop.get("stage"), str)
    ):
        errors.append(f"{input_name}.facts.stop is invalid")
    resource = facts["resource_observation"]
    expected_resource_fields = RESOURCE_FIELDS if current_collector else LEGACY_RESOURCE_FIELDS
    if not isinstance(resource, dict) or set(resource) != expected_resource_fields:
        errors.append(f"{input_name}.facts.resource_observation is invalid")
    elif (
        not isinstance(resource.get("sampling_complete"), bool)
        or any(
            value is not None and not number(value)
            for key, value in resource.items()
            if key not in {"sampling_complete", "limit_trigger_reason"}
        )
        or (
            current_collector
            and resource.get("limit_trigger_reason")
            not in {None, "RESOURCE_MEMORY_SOFT_LIMIT", "RESOURCE_MEMORY_HARD_LIMIT"}
        )
    ):
        errors.append(f"{input_name}.facts.resource_observation values are invalid")
    if current_collector and isinstance(resource, dict) and isinstance(stop, dict):
        trigger = resource.get("limit_trigger_reason")
        reason = stop.get("reason")
        minimum = resource.get("host_available_memory_min_mb")
        soft = resource.get("available_memory_soft_min_mb")
        hard = resource.get("available_memory_hard_min_mb")
        grace = resource.get("hard_breach_grace_samples")
        streak = resource.get("max_consecutive_memory_hard_breaches")
        if any(
            not isinstance(value, int) or isinstance(value, bool)
            for value in (soft, hard, grace, streak)
        ):
            errors.append(
                f"{input_name}.facts resource policies and counters must be integers"
            )
        elif (
            soft <= 0
            or hard <= 0
            or soft < hard
            or grace < 1
            or streak < 0
        ):
            errors.append(
                f"{input_name}.facts resource policies and counters are outside their bounds"
            )
        if (
            trigger in {"RESOURCE_MEMORY_SOFT_LIMIT", "RESOURCE_MEMORY_HARD_LIMIT"}
            and reason
            not in {
                trigger,
                "USER_CANCELLED",
                "SUBJECT_DRIFT",
                "EVIDENCE_ERROR",
                "CLEANUP_ERROR",
            }
        ) or (
            reason in {"RESOURCE_MEMORY_SOFT_LIMIT", "RESOURCE_MEMORY_HARD_LIMIT"}
            and trigger != reason
        ):
            errors.append(f"{input_name}.facts resource stop reason conflicts with observations")
        if trigger == "RESOURCE_MEMORY_SOFT_LIMIT" and not (
            number(minimum) and number(soft) and minimum < soft
        ):
            errors.append(f"{input_name}.facts soft memory stop lacks a threshold breach")
        if trigger == "RESOURCE_MEMORY_HARD_LIMIT" and not (
            number(minimum)
            and number(hard)
            and isinstance(grace, int)
            and not isinstance(grace, bool)
            and grace >= 1
            and isinstance(streak, int)
            and not isinstance(streak, bool)
            and streak >= grace
            and minimum < hard
        ):
            errors.append(f"{input_name}.facts hard memory stop lacks a sustained breach")
        if trigger != "RESOURCE_MEMORY_HARD_LIMIT" and (
            isinstance(grace, int)
            and not isinstance(grace, bool)
            and isinstance(streak, int)
            and not isinstance(streak, bool)
            and streak >= grace
        ):
            errors.append(
                f"{input_name}.facts sustained hard memory breach lacks a hard trigger"
            )
        if single_node_collector and resource.get("dependency_peak_rss_mb") is not None:
            errors.append(
                f"{input_name}.facts single-node resource observation must not fabricate dependency RSS"
            )
        application_started = any(
            isinstance(node, dict)
            and node.get("role") == "APPLICATION"
            and node.get("process_created") is True
            for node in nodes
        )
        if (
            single_node_collector
            and application_started
            and not number(resource.get("application_peak_rss_mb"))
        ):
            errors.append(
                f"{input_name}.facts started application requires an application RSS observation"
            )
    subject = facts["subject_observation"]
    if not isinstance(subject, dict) or set(subject) != SUBJECT_FIELDS:
        errors.append(f"{input_name}.facts.subject_observation is invalid")
    elif (
        any(
            value is not None and not sha(value)
            for key, value in subject.items()
            if key in {"before_fingerprint", "after_fingerprint"}
        )
        or not (
            subject.get("changed") is None
            or isinstance(subject.get("changed"), bool)
        )
        or not isinstance(subject.get("scan_complete"), bool)
        or (
            subject.get("scan_complete")
            and (
                subject.get("before_fingerprint") is None
                or subject.get("after_fingerprint") is None
                or not isinstance(subject.get("changed"), bool)
            )
        )
    ):
        errors.append(f"{input_name}.facts.subject_observation values are invalid")
    cleanup = facts["cleanup"]
    cleanup_fields = {
        "reverse_order_complete", "jobs_empty", "handles_released", "readers_released",
        "ports_free", "run_work_released", "staging_released",
    }
    if (
        not isinstance(cleanup, dict)
        or set(cleanup) != cleanup_fields
        or any(not isinstance(value, bool) for value in cleanup.values())
    ):
        errors.append(f"{input_name}.facts.cleanup is invalid")
    elif facts["cleanup_complete"] is True and not all(cleanup.values()):
        errors.append(f"{input_name}.facts cannot overstate cleanup completeness")
    elif (
        current_collector
        and isinstance(browser, dict)
        and browser.get("started") is True
        and browser.get("process_cleanup_complete") is not True
        and facts["cleanup_complete"] is True
    ):
        errors.append(f"{input_name}.facts cannot omit Browser process cleanup failure")
    if not isinstance(facts["services_ready"], bool) or not isinstance(
        facts["cleanup_complete"], bool
    ):
        errors.append(f"{input_name}.facts completion fields must be booleans")
    elif (
        facts["cleanup_complete"] is True
        and isinstance(stop, dict)
        and stop.get("reason") == "CLEANUP_ERROR"
    ):
        errors.append(f"{input_name}.facts cleanup reason conflicts with completion")
    if facts["services_ready"] is True and (
        actual_start != sealed_start
        or len(nodes) != expected_node_count
        or any(
            not isinstance(node, dict)
            or not isinstance(node.get("readiness"), dict)
            or node["readiness"].get("ready") is not True
            for node in nodes
        )
    ):
        errors.append(f"{input_name}.facts cannot overstate service readiness")
    if isinstance(stop, dict) and stop.get("reason") == "NONE" and (
        facts["services_ready"] is not True
        or facts["cleanup_complete"] is not True
        or not isinstance(browser, dict)
        or browser.get("completed") is not True
        or (
            current_collector
            and browser.get("process_cleanup_complete") is not True
        )
        or not isinstance(resource, dict)
        or resource.get("sampling_complete") is not True
        or not isinstance(subject, dict)
        or subject.get("scan_complete") is not True
        or subject.get("changed") is not False
    ):
        errors.append(f"{input_name}.facts NONE stop reason requires a complete clean lifecycle")
    if (
        current_collector
        and isinstance(stop, dict)
        and isinstance(resource, dict)
        and isinstance(subject, dict)
        and (
            resource.get("sampling_complete") is False
            or subject.get("scan_complete") is False
        )
        and stop.get("reason") not in {"EVIDENCE_ERROR", "CLEANUP_ERROR"}
    ):
        errors.append(
            f"{input_name}.facts incomplete observations require an evidence or cleanup error"
        )
    if document.get("metadata") != METADATA:
        errors.append(f"{input_name}.metadata must contain exact bootstrap safety claims")
