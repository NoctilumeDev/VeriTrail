from __future__ import annotations

import os
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from veritrail.canonical import sha256_bytes, sha256_json
from veritrail.command_preview import (
    _environment_projection,
    _resolve_executable,
    _resolve_subject_directory,
    _resolve_subject_root,
    load_tool_bindings,
)
from veritrail.errors import SafetyError, ValidationError
from veritrail.plan import verify_sealed_plan
from veritrail.project_profile import verify_sealed_project_profile
from veritrail.windows_job import require_windows_command_capability
from veritrail.windows_tcp import assert_loopback_ports_free


@dataclass(frozen=True)
class ResolvedBootstrapNode:
    node_id: str
    executable: Path
    executable_identity: dict[str, Any]
    working_directory: Path
    inherited_environment: dict[str, str]
    explicit_environment: dict[str, str]


@dataclass(frozen=True)
class ResolvedBootstrap:
    preview: dict[str, Any]
    subject_root: Path
    nodes: tuple[ResolvedBootstrapNode, ...]


def _require_windows_bootstrap_capability() -> None:
    if os.name != "nt" or not hasattr(sys, "getwindowsversion"):
        raise SafetyError("M10 bootstrap capability is available only on Windows 11")
    windows = sys.getwindowsversion()
    if windows.major != 10 or windows.build < 22000:
        raise SafetyError("M10 bootstrap capability requires Windows 11")
    try:
        require_windows_command_capability()
    except SafetyError as exc:
        message = str(exc).replace("M9 command capability", "M10 bootstrap capability")
        raise SafetyError(message) from exc


def _resolve_bootstrap_executable(raw_path: str) -> tuple[Path, dict[str, Any]]:
    try:
        return _resolve_executable(raw_path)
    except SafetyError as exc:
        message = str(exc).replace(
            "frozen M9 ONESHOT boundary", "frozen M10 trusted-service boundary"
        )
        raise SafetyError(message) from exc


def _path_identity(path: Path) -> str:
    normalized = os.path.normcase(str(path)).replace("\\", "/")
    return sha256_bytes(normalized.encode("utf-8"))


def _preview_arguments(
    arguments: list[dict[str, Any]], nodes: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    preview: list[dict[str, Any]] = []
    for argument in arguments:
        if "literal" in argument:
            preview.append({"kind": "literal", "value": argument["literal"]})
        elif "run_work_path" in argument:
            segments = list(argument["run_work_path"])
            preview.append(
                {
                    "kind": "run_work_path",
                    "segments": segments,
                    "value": "<RUN_WORK>/" + "/".join(segments),
                }
            )
        elif "node_port" in argument:
            reference = argument["node_port"]
            preview.append(
                {
                    "kind": "node_port",
                    "node_id": reference,
                    "value": nodes[reference]["port"],
                }
            )
        else:
            reference = argument["node_origin"]
            preview.append(
                {
                    "kind": "node_origin",
                    "node_id": reference,
                    "value": f"http://127.0.0.1:{nodes[reference]['port']}",
                }
            )
    return preview


def resolve_bootstrap(
    plan: dict[str, Any],
    profile: dict[str, Any],
    *,
    subject_root: Path,
    tool_bindings_path: Path,
    environment: Mapping[str, str] | None = None,
) -> ResolvedBootstrap:
    verify_sealed_project_profile(profile)
    verify_sealed_plan(plan, profile)
    plan_version = plan.get("schema_version")
    if plan_version not in {"0.6", "0.7"}:
        raise ValidationError(
            ["bootstrap-preview requires ExperimentPlan schema_version '0.6' or '0.7'"]
        )
    _require_windows_bootstrap_capability()

    bindings = load_tool_bindings(tool_bindings_path)
    resolved_subject = _resolve_subject_root(subject_root)
    for index, root in enumerate(profile["subject_watch_roots"]):
        _resolve_subject_directory(
            resolved_subject, root, f"ProjectProfile.subject_watch_roots[{index}]"
        )

    nodes_by_id = {node["node_id"]: node for node in profile["nodes"]}
    sealed_ports = [nodes_by_id[node_id]["port"] for node_id in profile["start_order"]]
    assert_loopback_ports_free(sealed_ports)

    resolved_nodes: list[ResolvedBootstrapNode] = []
    preview_nodes: list[dict[str, Any]] = []
    live_environment = os.environ if environment is None else environment
    for node_id in profile["start_order"]:
        node = nodes_by_id[node_id]
        binding_id = node["tool_binding"]
        binding = bindings["bindings"].get(binding_id)
        if not isinstance(binding, dict):
            raise ValidationError(
                [f"ToolBindings does not define required binding {binding_id!r}"]
            )
        working = _resolve_subject_directory(
            resolved_subject,
            node["working_directory"],
            f"ProjectProfile node {node_id!r} working_directory",
        )
        executable, executable_identity = _resolve_bootstrap_executable(binding["executable"])
        inherited, explicit, environment_sha256 = _environment_projection(
            node, live_environment
        )
        preview_node = {
            "node_id": node_id,
            "role": node["role"],
            "depends_on": list(node["depends_on"]),
            "adapter": node["adapter"],
            "tool_binding_id": binding_id,
            "executable": executable_identity,
            "arguments": _preview_arguments(node["arguments"], nodes_by_id),
            "working_directory": node["working_directory"],
            "working_directory_identity_sha256": _path_identity(working),
            "environment": {
                "inherit_names": sorted(inherited),
                "set_names": sorted(explicit),
                "runner_names": ["TEMP", "TMP"],
                "projection_sha256": environment_sha256,
                "values_persisted": False,
            },
            "port": node["port"],
            "port_preflight": "FREE",
            "readiness": deepcopy(node["readiness"]),
            "limits": deepcopy(node["limits"]),
            "shutdown": deepcopy(node["shutdown"]),
            "node_policy_sha256": sha256_json(node),
        }
        preview_nodes.append(preview_node)
        resolved_nodes.append(
            ResolvedBootstrapNode(
                node_id=node_id,
                executable=executable,
                executable_identity=executable_identity,
                working_directory=working,
                inherited_environment=inherited,
                explicit_environment=explicit,
            )
        )

    application = nodes_by_id[profile["application_node_id"]]
    preview: dict[str, Any] = {
        "schema_version": "0.2" if plan_version == "0.7" else "0.1",
        "plan_sha256": plan["seal"]["digest"],
        "profile_id": profile["profile_id"],
        "profile_version": profile["version"],
        "profile_sha256": profile["seal"]["digest"],
        "subject_root_identity_sha256": _path_identity(resolved_subject),
        "platform": profile["platform"],
        "cold_state": profile["cold_state"],
        "nodes": preview_nodes,
        "start_order": list(profile["start_order"]),
        "teardown_order": list(profile["teardown_order"]),
        "application_origin": f"http://127.0.0.1:{application['port']}",
        "browser_policy_sha256": sha256_json(plan["browser"]),
        "resource_policy_sha256": sha256_json(
            {
                "resource_budget": plan["resource_budget"],
                "preflight": plan["preflight"],
            }
        ),
        "claims": {
            "filesystem_isolation": "NOT_PROVEN",
            "network_isolation": "NOT_PROVEN",
            "graceful_shutdown": "NOT_PROVEN",
            "executable_toctou_containment": "NOT_PROVEN",
            "untrusted_code": "NOT_SUPPORTED",
            "c0_running": "NOT_SUPPORTED",
            "c2_workspace_cold": "NOT_SUPPORTED",
            "c3_host_cold": "NOT_SUPPORTED",
            "linux": "NOT_SUPPORTED",
            "macos": "NOT_SUPPORTED",
            "docker": "NOT_SUPPORTED",
        },
    }
    if plan_version == "0.7":
        preview["topology"] = profile["topology"]
    preview["preview_sha256"] = sha256_json(preview)
    return ResolvedBootstrap(
        preview=preview,
        subject_root=resolved_subject,
        nodes=tuple(resolved_nodes),
    )


def build_bootstrap_preview(
    plan: dict[str, Any],
    profile: dict[str, Any],
    *,
    subject_root: Path,
    tool_bindings_path: Path,
    environment: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    return deepcopy(
        resolve_bootstrap(
            plan,
            profile,
            subject_root=subject_root,
            tool_bindings_path=tool_bindings_path,
            environment=environment,
        ).preview
    )
