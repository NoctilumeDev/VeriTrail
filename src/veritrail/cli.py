from __future__ import annotations

import argparse
import json
import re
import signal
import sys
import threading
from contextlib import contextmanager
from pathlib import Path
from types import FrameType
from typing import Iterator

from veritrail import __version__
from veritrail.batching import (
    BatchError,
    create_batch_analysis_bundle,
    load_and_seal_batch_plan,
    write_sealed_batch_plan,
)
from veritrail.browser import collect_browser_evidence
from veritrail.bootstrap_preview import build_bootstrap_preview
from veritrail.bootstrap_public_run import run_bootstrap_bundle
from veritrail.catalog import CatalogError, build_catalog
from veritrail.comparison import ComparisonError, create_comparison_bundle
from veritrail.command_execution import collect_command_evidence
from veritrail.command_preview import build_command_preview, resolve_command
from veritrail.demo import create_first_run_demo
from veritrail.errors import SafetyError, ValidationError, VeriTrailError
from veritrail.evidence import import_evidence_document
from veritrail.local_api import create_catalog_server
from veritrail.orchestration import collect_orchestrated_evidence
from veritrail.pairing import (
    PairingError,
    create_paired_analysis_bundle,
    load_and_seal_pairing_plan,
    write_sealed_pairing_plan,
)
from veritrail.plan import (
    load_and_seal_plan,
    load_json_object as load_plan_json_object,
    seal_plan,
    verify_sealed_plan,
    write_sealed_plan,
)
from veritrail.project_profile import (
    load_and_seal_project_profile,
    load_sealed_project_profile,
    write_sealed_project_profile,
)
from veritrail.reporting import create_bundle
from veritrail.resources import collect_preflight_evidence


@contextmanager
def _bootstrap_interrupt_cancellation() -> Iterator[threading.Event]:
    """Translate console interrupts into cooperative M10 cancellation.

    The first and subsequent signals only request cancellation so the lifecycle can
    finalize evidence and clean owned resources. The caller's handlers are restored
    before returning to the surrounding CLI.
    """

    cancellation = threading.Event()
    if threading.current_thread() is not threading.main_thread():
        yield cancellation
        return

    handled_signals = [signal.SIGINT]
    if hasattr(signal, "SIGBREAK"):
        handled_signals.append(signal.SIGBREAK)
    previous = {item: signal.getsignal(item) for item in handled_signals}

    def request_cancel(_signum: int, _frame: FrameType | None) -> None:
        cancellation.set()

    try:
        for item in handled_signals:
            signal.signal(item, request_cancel)
        yield cancellation
    finally:
        for item, handler in previous.items():
            signal.signal(item, handler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veritrail",
        description="Seal controlled experiment plans and evaluate imported evidence.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    seal = subparsers.add_parser("seal", help="validate and seal an experiment plan")
    seal.add_argument("--plan", type=Path, required=True, help="unsealed or already sealed plan JSON")
    seal.add_argument(
        "--profile",
        type=Path,
        help="required sealed ProjectProfile 0.1/0.2 for Plan 0.6/0.7; rejected otherwise",
    )
    seal.add_argument("--output", type=Path, required=True, help="new sealed plan path")

    profile_seal = subparsers.add_parser(
        "bootstrap-profile-seal",
        help="validate and seal one ProjectProfile 0.1 or 0.2",
    )
    profile_seal.add_argument(
        "--profile", type=Path, required=True, help="unsealed or already sealed ProjectProfile"
    )
    profile_seal.add_argument(
        "--output", type=Path, required=True, help="new sealed ProjectProfile path"
    )

    bootstrap_preview = subparsers.add_parser(
        "bootstrap-preview",
        help="resolve a sealed Plan 0.6/0.7 and ProjectProfile without spawning processes",
    )
    bootstrap_preview.add_argument(
        "--plan", type=Path, required=True, help="sealed ExperimentPlan 0.6/0.7 JSON"
    )
    bootstrap_preview.add_argument(
        "--profile", type=Path, required=True, help="sealed ProjectProfile 0.1/0.2 JSON"
    )
    bootstrap_preview.add_argument(
        "--subject-root",
        type=Path,
        required=True,
        help="explicit local subject root; represented only by a digest",
    )
    bootstrap_preview.add_argument(
        "--tool-bindings",
        type=Path,
        required=True,
        help="local ToolBindings 0.1 JSON; never persisted",
    )

    evaluate = subparsers.add_parser("evaluate", help="import evidence and create a verdict bundle")
    evaluate.add_argument("--plan", type=Path, required=True, help="unsealed or sealed plan JSON")
    evaluate.add_argument(
        "--evidence",
        type=Path,
        action="append",
        default=[],
        help="structured evidence JSON; may be repeated",
    )
    evaluate.add_argument("--output", type=Path, required=True, help="new output directory")
    evaluate.add_argument("--run-id", required=True, help="stable caller-supplied run identifier")
    evaluate.add_argument(
        "--execution-status",
        choices=("PLANNED", "RUNNING", "COMPLETED", "ABORTED", "ERROR"),
        default="COMPLETED",
    )

    demo = subparsers.add_parser(
        "demo",
        help="create a self-contained synthetic PASS/FAIL first run and read-only Catalog",
    )
    demo.add_argument(
        "--output",
        type=Path,
        required=True,
        help="new output directory; no repository checkout or example files are required",
    )

    preflight = subparsers.add_parser(
        "preflight", help="collect a bounded local resource preflight and create a verdict bundle"
    )
    preflight.add_argument(
        "--plan", type=Path, required=True, help="unsealed or sealed Plan 0.2/0.3/0.4/0.5 JSON"
    )
    preflight.add_argument("--output", type=Path, required=True, help="new output directory")
    preflight.add_argument("--run-id", required=True, help="stable caller-supplied run identifier")

    browser_capture = subparsers.add_parser(
        "browser-capture",
        help="run Plan 0.3 preflight and collect bounded Chromium evidence",
    )
    browser_capture.add_argument(
        "--plan", type=Path, required=True, help="unsealed or sealed Plan 0.3 JSON"
    )
    browser_capture.add_argument("--output", type=Path, required=True, help="new output directory")
    browser_capture.add_argument(
        "--run-id", required=True, help="stable caller-supplied run identifier"
    )

    run = subparsers.add_parser(
        "run",
        help="run Plan 0.4, approved Plan 0.5, or approved Plan 0.6/0.7 bootstrap",
    )
    run.add_argument(
        "--plan", type=Path, required=True, help="Plan 0.4/0.5 JSON or sealed Plan 0.6/0.7 JSON"
    )
    run.add_argument(
        "--subject-root",
        type=Path,
        required=True,
        help="explicit local subject root; never persisted",
    )
    run.add_argument("--output", type=Path, required=True, help="new output directory")
    run.add_argument("--run-id", required=True, help="stable caller-supplied run identifier")
    run.add_argument(
        "--tool-bindings",
        type=Path,
        help="required local ToolBindings 0.1 JSON for Plan 0.5; never persisted",
    )
    run.add_argument(
        "--approve-command",
        help="required Plan 0.5 CommandPreview SHA-256 approval",
    )
    run.add_argument(
        "--profile",
        type=Path,
        help="required sealed ProjectProfile 0.1/0.2 for Plan 0.6/0.7",
    )
    run.add_argument(
        "--approve-bootstrap-preview-sha256",
        help="required Plan 0.6/0.7 BootstrapPreview SHA-256 approval",
    )

    command_preview = subparsers.add_parser(
        "command-preview",
        help="validate and preview one sealed Plan 0.5 trusted ONESHOT command without spawning",
    )
    command_preview.add_argument(
        "--plan", type=Path, required=True, help="unsealed or sealed Plan 0.5 JSON"
    )
    command_preview.add_argument(
        "--subject-root",
        type=Path,
        required=True,
        help="explicit local subject root; represented only by a digest",
    )
    command_preview.add_argument(
        "--tool-bindings",
        type=Path,
        required=True,
        help="local ToolBindings 0.1 JSON; never persisted",
    )

    catalog_build = subparsers.add_parser(
        "catalog-build",
        help="validate immutable bundles and create a read-only SQLite catalog snapshot",
    )
    catalog_build.add_argument(
        "--artifacts", type=Path, required=True, help="explicit Artifact root directory"
    )
    catalog_build.add_argument("--output", type=Path, required=True, help="new Catalog directory")

    catalog_serve = subparsers.add_parser(
        "catalog-serve",
        help="serve a frozen Catalog and production Workbench on fixed IPv4 loopback",
    )
    catalog_serve.add_argument("--catalog", type=Path, required=True, help="frozen Catalog directory")
    catalog_serve.add_argument(
        "--artifacts", type=Path, required=True, help="Artifact root bound to the Catalog"
    )
    catalog_serve.add_argument(
        "--web-root", type=Path, required=True, help="Vue production build directory"
    )
    catalog_serve.add_argument("--port", type=int, required=True, help="loopback TCP port")

    compare = subparsers.add_parser(
        "compare",
        help="compare two immutable Runs produced by the same sealed Plan",
    )
    compare.add_argument("--baseline", type=Path, required=True, help="baseline Run Bundle")
    compare.add_argument("--repeat", type=Path, required=True, help="independent repeat Run Bundle")
    compare.add_argument("--output", type=Path, required=True, help="new Comparison Bundle")

    seal_pairing = subparsers.add_parser(
        "seal-pairing", help="validate and seal a four-role PairingPlan"
    )
    seal_pairing.add_argument(
        "--plan", type=Path, required=True, help="unsealed or already sealed PairingPlan JSON"
    )
    seal_pairing.add_argument("--output", type=Path, required=True, help="new sealed PairingPlan")

    pair = subparsers.add_parser(
        "pair", help="analyze a preregistered four-role counterfactual group"
    )
    pair.add_argument("--plan", type=Path, required=True, help="sealed PairingPlan 0.1")
    pair.add_argument("--baseline", type=Path, required=True, help="BASELINE Run Bundle")
    pair.add_argument("--treatment", type=Path, required=True, help="TREATMENT Run Bundle")
    pair.add_argument(
        "--restored-baseline", type=Path, required=True, help="RESTORED_BASELINE Run Bundle"
    )
    pair.add_argument(
        "--negative-control", type=Path, required=True, help="NEGATIVE_CONTROL Run Bundle"
    )
    pair.add_argument("--output", type=Path, required=True, help="new PairedAnalysis Bundle")

    seal_batch = subparsers.add_parser(
        "seal-batch", help="validate and seal a preregistered full-factorial BatchPlan"
    )
    seal_batch.add_argument(
        "--plan", type=Path, required=True, help="unsealed or already sealed BatchPlan JSON"
    )
    seal_batch.add_argument("--output", type=Path, required=True, help="new sealed BatchPlan")

    analyze_batch = subparsers.add_parser(
        "analyze-batch", help="analyze assigned immutable Runs against a sealed BatchPlan"
    )
    analyze_batch.add_argument("--plan", type=Path, required=True, help="sealed BatchPlan 0.1")
    analyze_batch.add_argument(
        "--assignment", type=Path, required=True, help="strict RunAssignment 0.1 JSON"
    )
    analyze_batch.add_argument(
        "--runs-root", type=Path, required=True, help="explicit root for relative Run Bundle paths"
    )
    analyze_batch.add_argument("--output", type=Path, required=True, help="new BatchAnalysis Bundle")
    return parser


def _success(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True), flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "seal":
            raw_plan = load_plan_json_object(args.plan)
            is_bootstrap_plan = raw_plan.get("schema_version") in {"0.6", "0.7"}
            if is_bootstrap_plan and args.profile is None:
                raise ValidationError(
                    [f"Plan {raw_plan.get('schema_version')} seal requires --profile"]
                )
            if not is_bootstrap_plan and args.profile is not None:
                raise ValidationError(
                    ["--profile is accepted only when sealing Plan 0.6 or 0.7"]
                )
            profile = (
                load_sealed_project_profile(args.profile)
                if args.profile is not None
                else None
            )
            if "seal" in raw_plan:
                verify_sealed_plan(raw_plan, profile)
                plan = raw_plan
            else:
                plan = seal_plan(raw_plan, profile)
            write_sealed_plan(args.output, plan)
            _success(
                {
                    "command": "seal",
                    "output": str(args.output),
                    "plan_sha256": plan["seal"]["digest"],
                }
            )
            return 0
        if args.command == "bootstrap-profile-seal":
            profile = load_and_seal_project_profile(args.profile)
            write_sealed_project_profile(args.output, profile)
            _success(
                {
                    "command": "bootstrap-profile-seal",
                    "output": args.output.name,
                    "profile_id": profile["profile_id"],
                    "profile_version": profile["version"],
                    "profile_sha256": profile["seal"]["digest"],
                }
            )
            return 0
        if args.command == "bootstrap-preview":
            try:
                profile = load_sealed_project_profile(args.profile)
                plan = load_plan_json_object(args.plan)
                verify_sealed_plan(plan, profile)
                preview = build_bootstrap_preview(
                    plan,
                    profile,
                    subject_root=args.subject_root,
                    tool_bindings_path=args.tool_bindings,
                )
            except VeriTrailError:
                raise
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "BOOTSTRAP_PREVIEW_INTERNAL_ERROR",
                                "message": "Bootstrap preview encountered an unexpected internal error.",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(preview)
            return 0
        if args.command == "demo":
            try:
                summary = create_first_run_demo(args.output)
            except VeriTrailError:
                raise
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "DEMO_INTERNAL_ERROR",
                                "message": "Demo generation encountered an unexpected internal error.",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(
                {
                    "command": "demo",
                    "output": str(args.output),
                    "pass_verdict": summary["runs"]["pass"]["verdict"],
                    "fail_verdict": summary["runs"]["fail"]["verdict"],
                    "catalog_id": summary["catalog"]["catalog_id"],
                    "catalog_run_count": summary["catalog"]["run_count"],
                    "boundary": summary["boundary"],
                }
            )
            return 0
        if args.command == "evaluate":
            plan = load_and_seal_plan(args.plan)
            report = create_bundle(
                plan=plan,
                evidence_paths=args.evidence,
                output=args.output,
                run_id=args.run_id,
                execution_status=args.execution_status,
            )
            _success(
                {
                    "command": "evaluate",
                    "output": str(args.output),
                    "run_id": report["run_id"],
                    "execution_status": report["execution_status"],
                    "verdict": report["verdict"],
                }
            )
            return 0
        if args.command == "preflight":
            plan = load_and_seal_plan(args.plan)
            if plan["schema_version"] not in {"0.2", "0.3", "0.4", "0.5"}:
                raise ValidationError(
                    [
                        "preflight requires ExperimentPlan schema_version '0.2', '0.3', '0.4', or '0.5'; "
                        "Plan 0.1 remains read-only compatible"
                    ]
                )
            if args.output.exists():
                raise SafetyError(
                    f"refusing to overwrite existing output directory: {args.output.name}"
                )
            document = collect_preflight_evidence(plan, args.output.parent)
            artifact = import_evidence_document(document, "generated-preflight.json")
            decision = artifact.document["facts"]["decision"]
            execution_status = "ABORTED" if decision == "ABORT" else "COMPLETED"
            report = create_bundle(
                plan=plan,
                evidence_paths=[],
                output=args.output,
                run_id=args.run_id,
                execution_status=execution_status,
                generated_evidence=[artifact],
            )
            _success(
                {
                    "command": "preflight",
                    "output": str(args.output),
                    "run_id": report["run_id"],
                    "resource_decision": decision,
                    "execution_status": report["execution_status"],
                    "verdict": report["verdict"],
                }
            )
            return 0
        if args.command == "browser-capture":
            plan = load_and_seal_plan(args.plan)
            if plan["schema_version"] != "0.3":
                raise ValidationError(
                    ["browser-capture requires ExperimentPlan schema_version '0.3'"]
                )
            if args.output.exists():
                raise SafetyError(
                    f"refusing to overwrite existing output directory: {args.output.name}"
                )
            preflight_document = collect_preflight_evidence(plan, args.output.parent)
            preflight_artifact = import_evidence_document(
                preflight_document, "generated-preflight.json"
            )
            decision = preflight_artifact.document["facts"]["decision"]
            browser_started = decision == "PROCEED"
            generated = [preflight_artifact]
            if browser_started:
                browser_artifact = collect_browser_evidence(plan)
                generated.append(browser_artifact)
                execution_status = (
                    "COMPLETED"
                    if browser_artifact.document["facts"]["capture_complete"]
                    else "ERROR"
                )
            else:
                execution_status = "ABORTED" if decision == "ABORT" else "COMPLETED"
            report = create_bundle(
                plan=plan,
                evidence_paths=[],
                output=args.output,
                run_id=args.run_id,
                execution_status=execution_status,
                generated_evidence=generated,
            )
            _success(
                {
                    "command": "browser-capture",
                    "output": str(args.output),
                    "run_id": report["run_id"],
                    "resource_decision": decision,
                    "browser_started": browser_started,
                    "execution_status": report["execution_status"],
                    "verdict": report["verdict"],
                }
            )
            return 0
        if args.command == "command-preview":
            try:
                plan = load_and_seal_plan(args.plan)
                preview = build_command_preview(
                    plan,
                    subject_root=args.subject_root,
                    tool_bindings_path=args.tool_bindings,
                )
            except VeriTrailError:
                raise
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "COMMAND_PREVIEW_INTERNAL_ERROR",
                                "message": "Command preview encountered an unexpected internal error.",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(preview)
            return 0
        if args.command == "run":
            raw_plan = load_plan_json_object(args.plan)
            is_bootstrap_run = raw_plan.get("schema_version") in {"0.6", "0.7"}
            profile = None
            if is_bootstrap_run:
                if args.profile is None:
                    raise ValidationError(
                        [f"Plan {raw_plan.get('schema_version')} run requires --profile"]
                    )
                profile = load_sealed_project_profile(args.profile)
                verify_sealed_plan(raw_plan, profile)
                plan = raw_plan
            else:
                plan = load_and_seal_plan(args.plan)
            if plan["schema_version"] not in {"0.4", "0.5", "0.6", "0.7"}:
                raise ValidationError(
                    [
                        "run requires ExperimentPlan schema_version '0.4', '0.5', '0.6', or '0.7'"
                    ]
                )
            is_command_run = plan["schema_version"] == "0.5"
            if is_bootstrap_run:
                if args.tool_bindings is None:
                    raise ValidationError(
                        [f"Plan {plan['schema_version']} run requires --tool-bindings"]
                    )
                if args.approve_command is not None:
                    raise ValidationError(
                        [f"Plan {plan['schema_version']} run does not accept --approve-command"]
                    )
                if not isinstance(
                    args.approve_bootstrap_preview_sha256, str
                ) or not re.fullmatch(
                    r"[0-9a-f]{64}",
                    args.approve_bootstrap_preview_sha256,
                ):
                    raise ValidationError(
                        [
                            f"Plan {plan['schema_version']} run requires a lowercase SHA-256 "
                            "--approve-bootstrap-preview-sha256"
                        ]
                    )
            elif is_command_run:
                if args.tool_bindings is None:
                    raise ValidationError(["Plan 0.5 run requires --tool-bindings"])
                if not isinstance(args.approve_command, str) or not re.fullmatch(
                    r"[0-9a-f]{64}", args.approve_command
                ):
                    raise ValidationError(
                        ["Plan 0.5 run requires a lowercase SHA-256 --approve-command"]
                    )
                if (
                    args.profile is not None
                    or args.approve_bootstrap_preview_sha256 is not None
                ):
                    raise ValidationError(
                        ["Plan 0.5 run does not accept bootstrap approval arguments"]
                    )
            elif any(
                value is not None
                for value in (
                    args.tool_bindings,
                    args.approve_command,
                    args.profile,
                    args.approve_bootstrap_preview_sha256,
                )
            ):
                raise ValidationError(
                    ["Plan 0.4 run does not accept command or bootstrap approval arguments"]
                )
            if args.output.exists():
                raise SafetyError(
                    f"refusing to overwrite existing output directory: {args.output.name}"
                )
            if is_bootstrap_run:
                try:
                    with _bootstrap_interrupt_cancellation() as cancellation:
                        bootstrap_result = run_bootstrap_bundle(
                            plan,
                            profile,
                            subject_root=args.subject_root,
                            tool_bindings_path=args.tool_bindings,
                            approved_preview_sha256=(
                                args.approve_bootstrap_preview_sha256
                            ),
                            output=args.output,
                            run_id=args.run_id,
                            cancel_event=cancellation,
                        )
                except VeriTrailError:
                    raise
                except Exception:
                    print(
                        json.dumps(
                            {
                                "error": {
                                    "code": "BOOTSTRAP_RUN_INTERNAL_ERROR",
                                    "message": "Project bootstrap encountered an unexpected internal error.",
                                }
                            },
                            ensure_ascii=False,
                            sort_keys=True,
                        ),
                        file=sys.stderr,
                    )
                    return 1
                observed = bootstrap_result.observed
                lifecycle = observed.lifecycle if observed is not None else None
                browser_facts = (
                    observed.browser.document["facts"]
                    if observed is not None and observed.browser is not None
                    else None
                )
                report = bootstrap_result.report
                _success(
                    {
                        "command": "run",
                        "output": args.output.name,
                        "run_id": report["run_id"],
                        "resource_decision": bootstrap_result.preflight.document[
                            "facts"
                        ]["decision"],
                        "profile_sha256": profile["seal"]["digest"],
                        "bootstrap_preview_sha256": (
                            bootstrap_result.preview_sha256
                        ),
                        "bootstrap_started": observed is not None,
                        "services_ready": (
                            lifecycle.services_ready if lifecycle is not None else None
                        ),
                        "browser_started": (
                            lifecycle.ready_callback_started if lifecycle is not None else None
                        ),
                        "browser_completed": (
                            lifecycle.ready_callback_completed if lifecycle is not None else None
                        ),
                        "browser_capture_complete": (
                            browser_facts["capture_complete"]
                            if browser_facts is not None
                            else None
                        ),
                        "stop_reason": (
                            lifecycle.stop_reason if lifecycle is not None else None
                        ),
                        "cleanup_complete": (
                            lifecycle.cleanup_complete if lifecycle is not None else None
                        ),
                        "execution_status": report["execution_status"],
                        "verdict": report["verdict"],
                    }
                )
                return 0
            preflight_document = collect_preflight_evidence(plan, args.output.parent)
            preflight_artifact = import_evidence_document(
                preflight_document, "generated-preflight.json"
            )
            decision = preflight_artifact.document["facts"]["decision"]
            generated = [preflight_artifact]
            target_started = False
            target_ready = False
            cleanup_complete: bool | None = None
            command_started = False
            command_cleanup_complete: bool | None = None
            command_termination_reason: str | None = None
            if decision == "PROCEED":
                continue_pipeline = True
                if is_command_run:
                    try:
                        resolved = resolve_command(
                            plan,
                            subject_root=args.subject_root,
                            tool_bindings_path=args.tool_bindings,
                        )
                        if resolved.preview["preview_sha256"] != args.approve_command:
                            raise SafetyError(
                                "approved command digest does not match the live CommandPreview"
                            )
                        command_result = collect_command_evidence(
                            plan,
                            resolved,
                            tool_bindings_path=args.tool_bindings,
                            output_parent=args.output.parent,
                        )
                    except VeriTrailError:
                        raise
                    except Exception:
                        print(
                            json.dumps(
                                {
                                    "error": {
                                        "code": "COMMAND_RUN_INTERNAL_ERROR",
                                        "message": "Trusted command execution encountered an unexpected internal error.",
                                    }
                                },
                                ensure_ascii=False,
                                sort_keys=True,
                            ),
                            file=sys.stderr,
                        )
                        return 1
                    generated.append(command_result.command)
                    command_facts = command_result.command.document["facts"]
                    command_started = command_facts["target_resumed"]
                    command_cleanup_complete = command_facts["cleanup_complete"]
                    command_termination_reason = command_facts["termination_reason"]
                    cleanup_complete = command_cleanup_complete
                    execution_status = command_result.execution_status
                    continue_pipeline = command_result.continue_pipeline
                if continue_pipeline:
                    orchestration = collect_orchestrated_evidence(plan, args.subject_root)
                    generated.append(orchestration.orchestration)
                    if orchestration.browser is not None:
                        generated.append(orchestration.browser)
                    execution_status = orchestration.execution_status
                    orchestration_facts = orchestration.orchestration.document["facts"]
                    target_started = orchestration_facts["server_started"]
                    target_ready = orchestration_facts["ready"]
                    target_cleanup = orchestration_facts["cleanup_complete"]
                    cleanup_complete = (
                        target_cleanup
                        if command_cleanup_complete is None
                        else command_cleanup_complete and target_cleanup
                    )
            else:
                execution_status = "ABORTED" if decision == "ABORT" else "COMPLETED"
            report = create_bundle(
                plan=plan,
                evidence_paths=[],
                output=args.output,
                run_id=args.run_id,
                execution_status=execution_status,
                generated_evidence=generated,
            )
            payload = {
                "command": "run",
                "output": args.output.name,
                "run_id": report["run_id"],
                "resource_decision": decision,
                "target_started": target_started,
                "target_ready": target_ready,
                "cleanup_complete": cleanup_complete,
                "execution_status": report["execution_status"],
                "verdict": report["verdict"],
            }
            if is_command_run:
                payload.update(
                    {
                        "command_started": command_started,
                        "command_cleanup_complete": command_cleanup_complete,
                        "command_termination_reason": command_termination_reason,
                    }
                )
            _success(payload)
            return 0
        if args.command == "catalog-build":
            try:
                result = build_catalog(args.artifacts, args.output)
            except CatalogError as exc:
                print(
                    json.dumps(
                        {"error": {"code": exc.code, "message": exc.message}},
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "CATALOG_INTERNAL_ERROR",
                                "message": "Catalog 构建发生未预期内部错误。",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(
                {
                    "command": "catalog-build",
                    "status": result.status,
                    "catalog_id": result.catalog_id,
                    "run_count": result.run_count,
                    "issue_count": result.issue_count,
                    "duplicate_count": result.duplicate_count,
                    "bundle_set_sha256": result.bundle_set_sha256,
                }
            )
            return 0
        if args.command == "catalog-serve":
            try:
                server = create_catalog_server(
                    catalog_root=args.catalog,
                    artifact_root=args.artifacts,
                    web_root=args.web_root,
                    port=args.port,
                )
            except CatalogError as exc:
                print(
                    json.dumps(
                        {"error": {"code": exc.code, "message": exc.message}},
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "CATALOG_INTERNAL_ERROR",
                                "message": "Catalog 服务启动发生未预期内部错误。",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(
                {
                    "command": "catalog-serve",
                    "status": "READY",
                    "catalog_id": server.application.manifest["catalog_id"],
                    "origin": f"http://127.0.0.1:{args.port}",
                    "read_only": True,
                }
            )
            try:
                server.serve_forever(poll_interval=0.2)
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return 0
        if args.command == "compare":
            try:
                result = create_comparison_bundle(
                    baseline=args.baseline,
                    repeat=args.repeat,
                    output=args.output,
                )
            except ComparisonError as exc:
                print(
                    json.dumps(
                        {"error": {"code": exc.code, "message": exc.message}},
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "COMPARISON_INTERNAL_ERROR",
                                "message": "Comparison 构建发生未预期内部错误。",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(
                {
                    "command": "compare",
                    "comparison_id": result.comparison_id,
                    "comparison_status": result.comparison_status,
                    "comparable": result.comparable,
                    "difference_count": result.difference_count,
                    "baseline_run_id": result.baseline_run_id,
                    "repeat_run_id": result.repeat_run_id,
                    "output": args.output.name,
                }
            )
            return 0
        if args.command == "seal-pairing":
            try:
                plan = load_and_seal_pairing_plan(args.plan)
                write_sealed_pairing_plan(args.output, plan)
            except PairingError as exc:
                print(
                    json.dumps(
                        {"error": {"code": exc.code, "message": exc.message}},
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            _success(
                {
                    "command": "seal-pairing",
                    "output": args.output.name,
                    "pairing_plan_sha256": plan["seal"]["digest"],
                }
            )
            return 0
        if args.command == "pair":
            try:
                result = create_paired_analysis_bundle(
                    pairing_plan_path=args.plan,
                    baseline=args.baseline,
                    treatment=args.treatment,
                    restored_baseline=args.restored_baseline,
                    negative_control=args.negative_control,
                    output=args.output,
                )
            except PairingError as exc:
                print(
                    json.dumps(
                        {"error": {"code": exc.code, "message": exc.message}},
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "PAIRING_INTERNAL_ERROR",
                                "message": "PairedAnalysis 构建发生未预期内部错误。",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(
                {
                    "command": "pair",
                    "analysis_id": result.analysis_id,
                    "analysis_status": result.analysis_status,
                    "attributable": result.attributable,
                    "outcome_count": result.outcome_count,
                    "run_ids": result.run_ids,
                    "output": args.output.name,
                }
            )
            return 0
        if args.command == "seal-batch":
            try:
                plan = load_and_seal_batch_plan(args.plan)
                write_sealed_batch_plan(args.output, plan)
            except BatchError as exc:
                print(
                    json.dumps(
                        {"error": {"code": exc.code, "message": exc.message}},
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            _success(
                {
                    "command": "seal-batch",
                    "output": args.output.name,
                    "batch_plan_sha256": plan["seal"]["digest"],
                }
            )
            return 0
        if args.command == "analyze-batch":
            try:
                result = create_batch_analysis_bundle(
                    batch_plan_path=args.plan,
                    assignment_path=args.assignment,
                    runs_root=args.runs_root,
                    output=args.output,
                )
            except BatchError as exc:
                print(
                    json.dumps(
                        {"error": {"code": exc.code, "message": exc.message}},
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            except Exception:
                print(
                    json.dumps(
                        {
                            "error": {
                                "code": "BATCH_INTERNAL_ERROR",
                                "message": "BatchAnalysis 构建发生未预期内部错误。",
                            }
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 1
            _success(
                {
                    "command": "analyze-batch",
                    "analysis_id": result.analysis_id,
                    "coverage_status": result.coverage_status,
                    "hypothesis_status": result.hypothesis_status,
                    "slot_count": result.slot_count,
                    "source_count": result.source_count,
                    "output": args.output.name,
                }
            )
            return 0
    except VeriTrailError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
