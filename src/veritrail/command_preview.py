from __future__ import annotations

import hashlib
import os
import re
import stat
from pathlib import Path
from typing import Any, Mapping

from veritrail.canonical import sha256_bytes, sha256_json
from veritrail.errors import SafetyError, ValidationError
from veritrail.jsonio import load_json_object
from veritrail.plan import PLAN_ID_PATTERN, verify_sealed_plan
from veritrail.privacy import redact_string
from veritrail.windows_job import (
    require_windows_command_capability as _require_windows_command_capability,
)

TOOL_BINDINGS_FIELDS = {"schema_version", "bindings"}
TOOL_BINDING_FIELDS = {"executable"}
MAX_BINDINGS = 32
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
LOCAL_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:$")
FORBIDDEN_EXECUTABLES = {
    "bash.exe",
    "cmd.exe",
    "cscript.exe",
    "docker.exe",
    "gradle.exe",
    "maven.exe",
    "mshta.exe",
    "mvn.exe",
    "npm.exe",
    "pnpm.exe",
    "powershell.exe",
    "pwsh.exe",
    "regsvr32.exe",
    "rundll32.exe",
    "sh.exe",
    "wmic.exe",
    "wscript.exe",
    "wsl.exe",
    "yarn.exe",
    "zsh.exe",
}


def _reject_unknown_fields(
    value: dict[str, Any], allowed: set[str], path: str, errors: list[str]
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        errors.append(f"{path} has unsupported fields: {', '.join(unknown)}")


def load_tool_bindings(path: Path) -> dict[str, Any]:
    document = load_json_object(path, label="ToolBindings")
    errors: list[str] = []
    _reject_unknown_fields(document, TOOL_BINDINGS_FIELDS, "ToolBindings", errors)
    if document.get("schema_version") != "0.1":
        errors.append("ToolBindings.schema_version must be '0.1'")
    bindings = document.get("bindings")
    if not isinstance(bindings, dict) or not 1 <= len(bindings) <= MAX_BINDINGS:
        errors.append(f"ToolBindings.bindings must contain 1-{MAX_BINDINGS} entries")
    else:
        for binding_id, binding in bindings.items():
            prefix = f"ToolBindings.bindings[{binding_id!r}]"
            if not isinstance(binding_id, str) or not PLAN_ID_PATTERN.fullmatch(binding_id):
                errors.append("ToolBindings binding ids must be 2-64 character lowercase identifiers")
            if not isinstance(binding, dict):
                errors.append(f"{prefix} must be an object")
                continue
            _reject_unknown_fields(binding, TOOL_BINDING_FIELDS, prefix, errors)
            executable = binding.get("executable")
            if (
                not isinstance(executable, str)
                or not executable
                or len(executable) > 32767
                or any(ord(character) < 32 for character in executable)
            ):
                errors.append(f"{prefix}.executable must be a non-empty control-free path")
    if errors:
        raise ValidationError(errors)
    return document


def _is_reparse_point(path: Path) -> bool:
    try:
        details = path.lstat()
    except OSError as exc:
        raise ValidationError([f"cannot inspect local path entry {path.name!r}"]) from exc
    return path.is_symlink() or bool(getattr(details, "st_file_attributes", 0) & REPARSE_POINT)


def _resolve_subject_root(path: Path) -> Path:
    try:
        if not path.exists() or not path.is_dir() or _is_reparse_point(path):
            raise ValidationError(["subject root must be an existing ordinary directory"])
        return path.resolve(strict=True)
    except OSError as exc:
        raise ValidationError(["subject root must be an existing ordinary directory"]) from exc


def _resolve_subject_directory(subject_root: Path, relative: str, label: str) -> Path:
    current = subject_root
    if relative != ".":
        for segment in relative.split("/"):
            current = current / segment
            try:
                if not current.exists() or not current.is_dir() or _is_reparse_point(current):
                    raise ValidationError([f"{label} must resolve to an ordinary directory"])
            except OSError as exc:
                raise ValidationError([f"{label} must resolve to an ordinary directory"]) from exc
    try:
        resolved = current.resolve(strict=True)
        if os.path.commonpath((str(subject_root), str(resolved))) != str(subject_root):
            raise ValidationError([f"{label} must remain within the subject root"])
    except (OSError, ValueError) as exc:
        raise ValidationError([f"{label} must remain within the subject root"]) from exc
    return resolved


def _resolve_executable(raw_path: str) -> tuple[Path, dict[str, Any]]:
    if raw_path.startswith(("\\\\", "//")):
        raise ValidationError(["selected executable must use an absolute local drive path"])
    candidate = Path(raw_path)
    if not candidate.is_absolute() or not LOCAL_DRIVE_PATTERN.fullmatch(candidate.drive):
        raise ValidationError(["selected executable must use an absolute local drive path"])
    try:
        if (
            not candidate.exists()
            or not candidate.is_file()
            or _is_reparse_point(candidate)
            or candidate.suffix.casefold() != ".exe"
        ):
            raise ValidationError(["selected executable must be an existing ordinary .exe file"])
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ValidationError(["selected executable must be an existing ordinary .exe file"]) from exc

    basename = resolved.name
    if basename.casefold() in FORBIDDEN_EXECUTABLES:
        raise SafetyError("selected executable family is outside the frozen M9 ONESHOT boundary")
    if redact_string(basename)[1]:
        raise SafetyError("selected executable basename contains sensitive or personal data")

    digest = hashlib.sha256()
    signature = b""
    try:
        before = resolved.stat()
        with resolved.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                if not signature:
                    signature = chunk[:2]
                digest.update(chunk)
            opened = os.fstat(handle.fileno())
        after = resolved.stat()
    except OSError as exc:
        raise ValidationError(["selected executable could not be read for identity verification"]) from exc
    identity_fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
    if any(getattr(before, field) != getattr(opened, field) for field in identity_fields) or any(
        getattr(opened, field) != getattr(after, field) for field in identity_fields
    ):
        raise SafetyError("selected executable changed during identity verification")
    if signature != b"MZ":
        raise ValidationError(["selected executable must have a Windows PE signature"])

    normalized_path = os.path.normcase(str(resolved)).replace("\\", "/")
    identity = {
        "basename": basename,
        "size": after.st_size,
        "sha256": digest.hexdigest(),
        "path_identity_sha256": sha256_bytes(normalized_path.encode("utf-8")),
    }
    return resolved, identity


def _environment_projection(
    command: dict[str, Any], environment: Mapping[str, str]
) -> tuple[list[str], list[str], str]:
    available: dict[str, str] = {}
    for name, value in environment.items():
        normalized = name.upper()
        if normalized in available:
            raise SafetyError("parent environment contains case-insensitive duplicate names")
        available[normalized] = value

    inherited_values: dict[str, str] = {}
    inherit_names: list[str] = []
    for name in command["environment"]["inherit"]:
        normalized = name.upper()
        if normalized not in available:
            raise ValidationError([f"required inherited environment name {normalized} is unavailable"])
        value = available[normalized]
        if redact_string(value)[1] or any(ord(character) < 32 for character in value):
            raise SafetyError(f"inherited environment name {normalized} contains a disallowed value")
        inherited_values[normalized] = value
        inherit_names.append(normalized)

    explicit = dict(command["environment"]["set"])
    projection = {
        "inherited": {name: inherited_values[name] for name in sorted(inherited_values)},
        "set": {name: explicit[name] for name in sorted(explicit)},
        "runner": {"TEMP": "<RUN_WORK>", "TMP": "<RUN_WORK>"},
    }
    return sorted(inherit_names), sorted(explicit), sha256_json(projection)


def _preview_arguments(arguments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    preview: list[dict[str, Any]] = []
    for argument in arguments:
        if "literal" in argument:
            preview.append({"kind": "literal", "value": argument["literal"]})
        else:
            segments = list(argument["run_work_path"])
            preview.append(
                {
                    "kind": "run_work_path",
                    "segments": segments,
                    "value": "<RUN_WORK>/" + "/".join(segments),
                }
            )
    return preview


def build_command_preview(
    plan: dict[str, Any],
    *,
    subject_root: Path,
    tool_bindings_path: Path,
    environment: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    verify_sealed_plan(plan)
    if plan.get("schema_version") != "0.5":
        raise ValidationError(["command-preview requires ExperimentPlan schema_version '0.5'"])
    _require_windows_command_capability()

    bindings = load_tool_bindings(tool_bindings_path)
    command = plan["command"]
    binding_id = command["tool_binding"]
    binding = bindings["bindings"].get(binding_id)
    if not isinstance(binding, dict):
        raise ValidationError([f"ToolBindings does not define required binding {binding_id!r}"])

    resolved_subject = _resolve_subject_root(subject_root)
    working_directory = command["working_directory"]
    resolved_working = _resolve_subject_directory(
        resolved_subject, working_directory, "command.working_directory"
    )
    for index, root in enumerate(command["subject_watch_roots"]):
        _resolve_subject_directory(
            resolved_subject, root, f"command.subject_watch_roots[{index}]"
        )

    _, executable_identity = _resolve_executable(binding["executable"])
    inherited, explicit, environment_sha256 = _environment_projection(
        command, os.environ if environment is None else environment
    )
    subject_identity = sha256_bytes(
        os.path.normcase(str(resolved_subject)).replace("\\", "/").encode("utf-8")
    )
    working_identity = sha256_bytes(
        os.path.normcase(str(resolved_working)).replace("\\", "/").encode("utf-8")
    )

    preview: dict[str, Any] = {
        "schema_version": "0.1",
        "plan_sha256": plan["seal"]["digest"],
        "command_policy_sha256": sha256_json(command),
        "command_id": command["command_id"],
        "project_profile_id": command["project_profile_id"],
        "adapter": command["adapter"],
        "tool_binding_id": binding_id,
        "executable": executable_identity,
        "arguments": _preview_arguments(command["arguments"]),
        "argument_count": len(command["arguments"]),
        "subject_root_identity_sha256": subject_identity,
        "working_directory": working_directory,
        "working_directory_identity_sha256": working_identity,
        "environment": {
            "inherit_names": inherited,
            "set_names": explicit,
            "runner_names": ["TEMP", "TMP"],
            "projection_sha256": environment_sha256,
            "values_persisted": False,
        },
        "stdin": command["stdin"],
        "shell_used": False,
        "tty_used": False,
        "limits": {
            "timeout_ms": command["timeout_ms"],
            "descendant_exit_grace_ms": command["descendant_exit_grace_ms"],
            "expected_exit_codes": list(command["expected_exit_codes"]),
            "max_stdout_bytes": command["max_stdout_bytes"],
            "max_stderr_bytes": command["max_stderr_bytes"],
            "max_processes": command["max_processes"],
            "max_watch_files": command["max_watch_files"],
            "max_watch_total_bytes": command["max_watch_total_bytes"],
        },
        "write_policy": command["write_policy"],
        "subject_watch_roots": list(command["subject_watch_roots"]),
        "network_policy": command["network_policy"],
        "claims": {
            "filesystem_isolation": "NOT_PROVEN",
            "network_isolation": "NOT_PROVEN",
            "write_activity": "NOT_PROVEN",
            "executable_toctou_containment": "NOT_PROVEN",
            "untrusted_code_containment": "NOT_SUPPORTED",
            "process_limit_attempt_observation": "NOT_PROVEN",
        },
    }
    preview["preview_sha256"] = sha256_json(preview)
    return preview
