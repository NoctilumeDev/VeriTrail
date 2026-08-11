from __future__ import annotations

import argparse
import copy
import io
import json
import shutil
import socket
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from veritrail.canonical import canonical_json_bytes
from veritrail.catalog import build_catalog
from veritrail.cli import main as cli_main
from veritrail.orchestration import prepare_static_target
from veritrail.plan import seal_plan


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
M5_PLAN = REPOSITORY_ROOT / "examples" / "orchestration" / "plan.json"
PYTHON_SUBJECT = REPOSITORY_ROOT / "examples" / "command" / "python-project"
NODE_SUBJECT = REPOSITORY_ROOT / "examples" / "command" / "node-project"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m9-command-acceptance"
PYTHON_PORT = 18772
NODE_PORT = 18773
RAW_CANARY = "VT-M9-" + "SECRET-CANARY"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the frozen M9 real Python/Node command acceptance matrix."
    )
    parser.add_argument("--node-executable", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
        if exclusive is not None:
            probe.setsockopt(socket.SOL_SOCKET, exclusive, 1)
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(document) + b"\n")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        document = json.load(stream)
    if not isinstance(document, dict):
        raise AssertionError("expected a JSON object")
    return document


def command_assertions() -> list[dict[str, Any]]:
    return [
        {
            "id": "command-exit-accepted",
            "severity": "HARD",
            "evidence_type": "runtime.command",
            "path": "/facts/exit_expected",
            "operator": "eq",
            "expected": True,
        },
        {
            "id": "command-oneshot-quiescent",
            "severity": "HARD",
            "evidence_type": "runtime.command",
            "path": "/facts/oneshot_quiescent",
            "operator": "eq",
            "expected": True,
        },
        {
            "id": "command-subject-stable",
            "severity": "HARD",
            "evidence_type": "runtime.command",
            "path": "/facts/subject/final_state_drift_detected",
            "operator": "eq",
            "expected": False,
        },
        {
            "id": "command-cleanup-complete",
            "severity": "HARD",
            "evidence_type": "runtime.command",
            "path": "/facts/cleanup_complete",
            "operator": "eq",
            "expected": True,
        },
    ]


def base_plan(
    *,
    family: str,
    subject_root: Path,
    port: int,
    run_label: str,
) -> dict[str, Any]:
    plan = load_json(M5_PLAN)
    plan.pop("seal", None)
    plan["schema_version"] = "0.5"
    plan["plan_id"] = f"m9-{family}-trusted-command"
    plan["version"] = 1
    plan["subject"] = {
        "id": f"m9-{family}-subject",
        "version": "1",
        "source_ref": f"examples/command/{family}-project",
    }
    plan["question"] = (
        f"Can the sealed trusted {family} ONESHOT command complete before the existing "
        "static-target and browser evidence chain without subject drift or residual resources?"
    )
    plan["baseline"]["id"] = f"m9-{family}-static-baseline"
    plan["baseline"]["fingerprint"] = "0" * 64
    plan["baseline"]["tolerances"] = {
        "viewport_count": 2,
        "unexpected_browser_errors": 0,
        "cleanup_failures": 0,
        "subject_final_state_drift": 0,
    }
    for variable in plan["variables"]:
        if variable["name"] == "target_lifecycle_mode":
            variable["role"] = "CONTROLLED"
    plan["variables"].append(
        {
            "name": "pre_target_command_mode",
            "role": "PRIMARY",
            "value": "veritrail_managed_trusted_process_oneshot",
            "source": "sealed-plan",
        }
    )
    plan["required_evidence"].append("runtime.command")
    plan["assertions"].extend(command_assertions())
    plan["preflight"]["ports"] = [{"port": port, "expected": "FREE"}]
    origin = f"http://localhost:{port}"
    plan["browser"].update(
        start_url=f"{origin}/index.html",
        allowed_origins=[origin],
        steps=[
            {
                "id": "enter-run-label",
                "action": "fill",
                "selector": "[data-testid='run-label']",
                "value": run_label,
            },
            {
                "id": "load-evidence",
                "action": "click",
                "selector": "[data-testid='load-evidence']",
            },
            {
                "id": "wait-until-ready",
                "action": "expect_text",
                "selector": "[data-testid='status']",
                "value": f"evidence ready: {run_label}",
            },
            {
                "id": "evidence-list-visible",
                "action": "expect_visible",
                "selector": "[data-testid='evidence-list']",
            },
            {"id": "capture-ready", "action": "screenshot", "name": "ready"},
        ],
    )
    plan["target"].update(root="site", port=port)
    if family == "python":
        command = {
            "adapter": "TRUSTED_PROCESS_ONESHOT",
            "command_id": "python-project-check",
            "purpose": "verify the sealed lightweight Python subject",
            "project_profile_id": "m9-python-subject",
            "tool_binding": "python",
            "arguments": [{"literal": "-m"}, {"literal": "checks.verify_project"}],
            "working_directory": ".",
            "environment": {
                "inherit": ["SYSTEMROOT", "WINDIR"],
                "set": {"PYTHONDONTWRITEBYTECODE": "1"},
            },
            "stdin": "CLOSED",
            "timeout_ms": 30000,
            "descendant_exit_grace_ms": 1000,
            "expected_exit_codes": [0],
            "max_stdout_bytes": 65536,
            "max_stderr_bytes": 65536,
            "max_processes": 4,
            "write_policy": "RUN_WORK_ONLY_DETECT_SUBJECT_CHANGES",
            "subject_watch_roots": ["checks", "site"],
            "max_watch_files": 128,
            "max_watch_total_bytes": 8388608,
            "network_policy": "NOT_REQUIRED_NOT_ENFORCED",
        }
    else:
        command = {
            "adapter": "TRUSTED_PROCESS_ONESHOT",
            "command_id": "node-project-check",
            "purpose": "verify the sealed lightweight Node subject",
            "project_profile_id": "m9-node-subject",
            "tool_binding": "node",
            "arguments": [{"literal": "scripts/verify-project.mjs"}],
            "working_directory": ".",
            "environment": {"inherit": ["SYSTEMROOT", "WINDIR"], "set": {}},
            "stdin": "CLOSED",
            "timeout_ms": 30000,
            "descendant_exit_grace_ms": 1000,
            "expected_exit_codes": [0],
            "max_stdout_bytes": 65536,
            "max_stderr_bytes": 65536,
            "max_processes": 4,
            "write_policy": "RUN_WORK_ONLY_DETECT_SUBJECT_CHANGES",
            "subject_watch_roots": ["scripts", "site"],
            "max_watch_files": 128,
            "max_watch_total_bytes": 8388608,
            "network_policy": "NOT_REQUIRED_NOT_ENFORCED",
        }
    plan["command"] = command
    plan["change_scope"] = {
        "level": "L3_SYSTEM",
        "owner": "VeriTrail Core / Trusted Process Runner",
        "expected_blast_radius": (
            "Plan 0.5 command execution, M5 target/browser continuation, immutable Bundle, "
            "Catalog and generic Workbench consumers"
        ),
        "consumers": [
            "plan-validator",
            "command-preview",
            "trusted-process-runner",
            "bounded-orchestrator",
            "browser-adapter",
            "artifact-store",
            "verdict-engine",
            "catalog",
            "workbench",
        ],
    }
    plan["reproduction_steps"] = [
        "Preview this sealed Plan 0.5 against local ToolBindings.",
        "Approve the exact preview digest and run the trusted ONESHOT command.",
        "Verify the static target, both Chromium viewports, Bundle and cleanup facts.",
    ]
    plan["cleanup_steps"] = [
        "Release the Windows Job Object, process handles and capture threads.",
        "Remove the owned Run work directory after persisting redacted attachments.",
        "Stop Chromium and the static target, then verify the sealed port is free.",
    ]
    plan["baseline"]["fingerprint"] = prepare_static_target(plan, subject_root).fingerprint
    return plan


def python_variant(
    positive: dict[str, Any], *, version: int, mode: str
) -> dict[str, Any]:
    plan = copy.deepcopy(positive)
    plan.pop("seal", None)
    plan["version"] = version
    plan["question"] = f"Does the preregistered Python {mode} control preserve M9 status and cleanup semantics?"
    plan["command"]["command_id"] = f"python-project-{mode}"
    plan["command"]["purpose"] = f"run the preregistered Python {mode} acceptance control"
    plan["command"]["arguments"] = [
        {"literal": "-m"},
        {"literal": "checks.verify_project"},
        {"literal": "--mode"},
        {"literal": mode},
    ]
    command_items = [
        item for item in plan["assertions"] if item["evidence_type"] == "runtime.command"
    ]
    other_items = [
        item for item in plan["assertions"] if item["evidence_type"] != "runtime.command"
    ]
    if mode == "timeout":
        plan["command"]["timeout_ms"] = 1000
        command_items = [
            {
                "id": "command-shell-unused",
                "severity": "HARD",
                "evidence_type": "runtime.command",
                "path": "/facts/shell_used",
                "operator": "eq",
                "expected": False,
            },
            next(item for item in command_items if item["id"] == "command-cleanup-complete"),
        ]
    elif mode == "drift":
        command_items = [
            item for item in command_items if item["id"] != "command-subject-stable"
        ]
    elif mode == "descendant":
        plan["command"]["descendant_exit_grace_ms"] = 200
    plan["assertions"] = other_items + command_items
    return seal_plan(plan)


def call_cli(arguments: list[str]) -> dict[str, Any]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = cli_main(arguments)
    if code != 0:
        raise AssertionError(f"CLI control returned exit code {code}")
    payload = json.loads(stdout.getvalue())
    if not isinstance(payload, dict):
        raise AssertionError("CLI control returned a non-object payload")
    return payload


def preview(plan: Path, subject: Path, bindings: Path) -> dict[str, Any]:
    return call_cli(
        [
            "command-preview",
            "--plan",
            str(plan),
            "--subject-root",
            str(subject),
            "--tool-bindings",
            str(bindings),
        ]
    )


def run(
    *,
    plan: Path,
    subject: Path,
    bindings: Path,
    bundle: Path,
    run_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    command_preview = preview(plan, subject, bindings)
    payload = call_cli(
        [
            "run",
            "--plan",
            str(plan),
            "--subject-root",
            str(subject),
            "--tool-bindings",
            str(bindings),
            "--approve-command",
            command_preview["preview_sha256"],
            "--run-id",
            run_id,
            "--output",
            str(bundle),
        ]
    )
    return command_preview, payload


def evidence(bundle: Path, evidence_type: str) -> dict[str, Any]:
    matches: list[dict[str, Any]] = []
    for path in (bundle / "evidence").glob("*.json"):
        document = load_json(path)
        if document.get("evidence_type") == evidence_type:
            matches.append(document)
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one {evidence_type} artifact")
    return matches[0]


def assert_positive(bundle: Path, payload: dict[str, Any], marker: str) -> dict[str, Any]:
    if payload["execution_status"] != "COMPLETED" or payload["verdict"] != "PASS":
        raise AssertionError("positive command Run did not complete with PASS")
    if not payload["command_started"] or not payload["target_started"]:
        raise AssertionError("positive command Run did not reach both command and target")
    if not payload["cleanup_complete"] or not payload["command_cleanup_complete"]:
        raise AssertionError("positive command Run did not prove cleanup")
    report = load_json(bundle / "report.json")
    if sorted(item["evidence_type"] for item in report["evidence"]) != [
        "browser.session",
        "runtime.command",
        "runtime.orchestration",
        "runtime.preflight",
    ]:
        raise AssertionError("positive command Run did not retain the four-layer evidence chain")
    command = evidence(bundle, "runtime.command")
    facts = command["facts"]
    if not facts["oneshot_quiescent"] or not facts["cleanup_complete"]:
        raise AssertionError("positive command did not finish quiescent and clean")
    if facts["subject"]["final_state_drift_detected"]:
        raise AssertionError("positive command changed a monitored subject root")
    if facts["ownership"]["final_active_processes"] != 0 or not facts["tree_released"]:
        raise AssertionError("positive command retained an owned process")
    stdout = (bundle / "attachments" / "command" / "stdout.txt").read_text(encoding="utf-8")
    if marker not in stdout:
        raise AssertionError("positive command output marker is missing")
    return facts


def text_bundle(bundle: Path) -> str:
    return "\n".join(
        path.read_text(encoding="utf-8", errors="strict")
        for path in bundle.rglob("*")
        if path.is_file() and path.suffix.lower() not in {".png", ".sqlite3"}
    )


def case_fact(
    *,
    run_id: str,
    plan: dict[str, Any],
    preview_document: dict[str, Any],
    payload: dict[str, Any],
    command: dict[str, Any],
) -> dict[str, Any]:
    facts = command["facts"]
    return {
        "run_id": run_id,
        "plan_sha256": plan["seal"]["digest"],
        "preview_sha256": preview_document["preview_sha256"],
        "execution_status": payload["execution_status"],
        "verdict": payload["verdict"],
        "termination_reason": facts["termination_reason"],
        "exit_code": facts["exit_code"],
        "exit_expected": facts["exit_expected"],
        "oneshot_quiescent": facts["oneshot_quiescent"],
        "cleanup_complete": facts["cleanup_complete"],
        "final_active_processes": facts["ownership"]["final_active_processes"],
        "final_state_drift_detected": facts["subject"]["final_state_drift_detected"],
        "stdout_redaction_count": facts["stdout"]["redaction_count"],
        "stderr_redaction_count": facts["stderr"]["redaction_count"],
    }


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    node_executable = args.node_executable.resolve()
    if output.exists():
        print("M9 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not node_executable.is_file() or node_executable.suffix.casefold() != ".exe":
        print("M9 acceptance requires an explicit ordinary node.exe.", file=sys.stderr)
        return 2
    if not PYTHON_SUBJECT.is_dir() or not NODE_SUBJECT.is_dir():
        print("M9 acceptance subject fixtures are unavailable.", file=sys.stderr)
        return 2
    if not all(port_is_free(port) for port in (PYTHON_PORT, NODE_PORT)):
        print("M9 acceptance requires both sealed loopback ports to be free.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m9-controlled-project-command-runtime",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "verdict": "INCONCLUSIVE",
        "checks": [],
        "runs": {},
    }
    summary_path = output / "acceptance-summary.json"
    exit_code = 1
    try:
        subjects = output / "subjects"
        subject_paths: dict[str, Path] = {}
        for name, source in (
            ("python-positive", PYTHON_SUBJECT),
            ("python-nonzero", PYTHON_SUBJECT),
            ("python-timeout", PYTHON_SUBJECT),
            ("python-canary", PYTHON_SUBJECT),
            ("python-drift", PYTHON_SUBJECT),
            ("python-descendant", PYTHON_SUBJECT),
            ("node-positive", NODE_SUBJECT),
        ):
            target = subjects / name
            shutil.copytree(
                source,
                target,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            subject_paths[name] = target

        plans = output / "plans"
        python_positive = seal_plan(
            base_plan(
                family="python",
                subject_root=subject_paths["python-positive"],
                port=PYTHON_PORT,
                run_label="m9-python-run",
            )
        )
        node_positive = seal_plan(
            base_plan(
                family="node",
                subject_root=subject_paths["node-positive"],
                port=NODE_PORT,
                run_label="m9-node-run",
            )
        )
        sealed_plans = {
            "python-positive": python_positive,
            "python-nonzero": python_variant(python_positive, version=2, mode="nonzero"),
            "python-timeout": python_variant(python_positive, version=3, mode="timeout"),
            "python-canary": python_variant(python_positive, version=4, mode="canary"),
            "python-drift": python_variant(python_positive, version=5, mode="drift"),
            "python-descendant": python_variant(
                python_positive, version=6, mode="descendant"
            ),
            "node-positive": node_positive,
        }
        plan_paths: dict[str, Path] = {}
        for name, plan in sealed_plans.items():
            path = plans / f"{name}.json"
            write_json(path, plan)
            plan_paths[name] = path
        summary["checks"].append("all-positive-and-negative-plans-sealed-before-run")

        local = output / "local"
        bindings = local / "tool-bindings.json"
        write_json(
            bindings,
            {
                "schema_version": "0.1",
                "bindings": {
                    "python": {"executable": str(Path(sys.executable).resolve())},
                    "node": {"executable": str(node_executable)},
                },
            },
        )

        bundles = output / "bundles"
        bundles.mkdir()
        run_matrix = [
            ("python-positive", "m9-real-python-positive", "python-positive"),
            ("python-repeat", "m9-real-python-repeat", "python-positive"),
            ("node-positive", "m9-real-node-positive", "node-positive"),
            ("python-nonzero", "m9-real-python-nonzero", "python-nonzero"),
            ("python-timeout", "m9-real-python-timeout", "python-timeout"),
            ("python-canary", "m9-real-python-canary", "python-canary"),
            ("python-drift", "m9-real-python-drift", "python-drift"),
            ("python-descendant", "m9-real-python-descendant", "python-descendant"),
        ]
        for case, run_id, plan_name in run_matrix:
            subject_name = "python-positive" if case == "python-repeat" else case
            bundle = bundles / case
            preview_document, payload = run(
                plan=plan_paths[plan_name],
                subject=subject_paths[subject_name],
                bindings=bindings,
                bundle=bundle,
                run_id=run_id,
            )
            command = evidence(bundle, "runtime.command")
            summary["runs"][case] = case_fact(
                run_id=run_id,
                plan=sealed_plans[plan_name],
                preview_document=preview_document,
                payload=payload,
                command=command,
            )

            if case in {"python-positive", "python-repeat"}:
                assert_positive(bundle, payload, '"check": "python-project"')
            elif case == "node-positive":
                assert_positive(bundle, payload, '"check":"node-project"')
            elif case == "python-nonzero":
                if payload["execution_status"] != "COMPLETED" or payload["verdict"] != "FAIL":
                    raise AssertionError("nonzero control did not remain COMPLETED/FAIL")
                if payload["target_started"]:
                    raise AssertionError("nonzero control unexpectedly started the target")
            elif case == "python-timeout":
                if payload["execution_status"] != "ABORTED" or payload["verdict"] != "PENDING":
                    raise AssertionError("timeout control did not remain ABORTED/PENDING")
                if command["facts"]["termination_reason"] != "TIMEOUT":
                    raise AssertionError("timeout control recorded another termination reason")
            elif case == "python-canary":
                assert_positive(bundle, payload, '"check": "python-project"')
                encoded = text_bundle(bundle)
                if RAW_CANARY in encoded:
                    raise AssertionError("raw command canary reached the immutable Bundle")
                if "Authorization: Bearer [REDACTED]" not in encoded:
                    raise AssertionError("canary control did not retain an explicit redaction marker")
                if command["facts"]["stdout"]["redaction_count"] < 1:
                    raise AssertionError("canary control did not record output redaction")
            elif case == "python-drift":
                if payload["execution_status"] != "COMPLETED" or payload["verdict"] != "INCONCLUSIVE":
                    raise AssertionError("drift control did not remain COMPLETED/INCONCLUSIVE")
                marker = subject_paths[case] / "checks" / "drift-marker.txt"
                if not marker.is_file() or not command["facts"]["subject"]["final_state_drift_detected"]:
                    raise AssertionError("drift control did not preserve and report the project change")
            elif case == "python-descendant":
                if payload["execution_status"] != "COMPLETED" or payload["verdict"] != "FAIL":
                    raise AssertionError("descendant control did not remain COMPLETED/FAIL")
                facts = command["facts"]
                if facts["termination_reason"] != "DESCENDANT_GRACE_EXPIRED":
                    raise AssertionError("descendant control did not record the grace expiry")
                if facts["ownership"]["final_active_processes"] != 0 or not facts["cleanup_complete"]:
                    raise AssertionError("descendant control did not reap its owned process tree")
            if not port_is_free(PYTHON_PORT) or not port_is_free(NODE_PORT):
                raise AssertionError("a sealed target port remained occupied after a serial Run")
            summary["checks"].append(f"{case}-verified")

        if (
            summary["runs"]["python-positive"]["plan_sha256"]
            != summary["runs"]["python-repeat"]["plan_sha256"]
        ):
            raise AssertionError("Python repeat did not reuse the identical sealed Plan")
        comparison = call_cli(
            [
                "compare",
                "--baseline",
                str(bundles / "python-positive"),
                "--repeat",
                str(bundles / "python-repeat"),
                "--output",
                str(output / "comparison" / "python-repeat"),
            ]
        )
        if comparison["comparison_status"] != "MATCH":
            raise AssertionError("same-Plan Python repeat did not remain semantically stable")
        summary["comparison"] = {
            "status": comparison["comparison_status"],
            "comparison_id": comparison["comparison_id"],
        }
        summary["checks"].append("same-plan-python-repeat-compared")

        catalog = build_catalog(bundles, output / "catalog")
        if catalog.run_count != len(run_matrix) or catalog.issue_count != 0:
            raise AssertionError("Catalog did not accept every real M9 Bundle cleanly")
        summary["catalog"] = {
            "catalog_id": catalog.catalog_id,
            "run_count": catalog.run_count,
            "issue_count": catalog.issue_count,
            "duplicate_count": catalog.duplicate_count,
        }
        summary["checks"].append("catalog-indexed-all-real-command-bundles")

        residuals = [
            path.name
            for path in output.rglob(".veritrail-*")
            if path.is_dir() or path.is_file()
        ]
        if residuals:
            raise AssertionError("M9 acceptance left owned staging or Run work")
        if not all(port_is_free(port) for port in (PYTHON_PORT, NODE_PORT)):
            raise AssertionError("M9 acceptance left a loopback listener")
        summary["residuals"] = {
            "owned_staging_or_run_work": 0,
            "sealed_listening_ports": 0,
        }
        summary["checks"].append("owned-runtime-residuals-zero")
        summary["execution_status"] = "COMPLETED"
        summary["verdict"] = "PASS"
        exit_code = 0
    except Exception as exc:
        summary["execution_status"] = "ERROR"
        summary["error_type"] = type(exc).__name__
        print("M9 runtime acceptance failed; retained bounded evidence for review.", file=sys.stderr)
    finally:
        summary["ended_at"] = utc_now()
        write_json(summary_path, summary)

    if exit_code == 0:
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
