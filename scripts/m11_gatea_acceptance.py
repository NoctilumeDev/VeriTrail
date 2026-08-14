from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from veritrail.batching import BatchError, _load_source as load_batch_source
from veritrail.bootstrap_browser import (
    ObservedBrowserCollectionError,
    ObservedBrowserEvidence,
    collect_observed_browser_evidence,
)
from veritrail.bootstrap_preview import build_bootstrap_preview, resolve_bootstrap
from veritrail.bootstrap_public_run import BootstrapPublicRunResult, run_bootstrap_bundle
from veritrail.bootstrap_run import run_observed_bootstrap
from veritrail.canonical import canonical_json_bytes
from veritrail.catalog import build_catalog, validate_bundle
from veritrail.comparison import create_comparison_bundle
from veritrail.pairing import PairingError, _load_source as load_pairing_source
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile
from veritrail.resources import host_memory_bytes
from veritrail.windows_readiness import probe_owned_http_readiness
from veritrail.windows_service import OwnedServiceSession


EXAMPLE_ROOT = REPOSITORY_ROOT / "examples" / "bootstrap"
APPLICATION_PORT = 18774
MEBIBYTE = 1024 * 1024

RUNS = (
    ("m11-gatea-positive-01", "positive", "NONE", "COMPLETED", "PASS"),
    ("m11-gatea-positive-02", "positive", "NONE", "COMPLETED", "PASS"),
    ("m11-gatea-early-exit-01", "early-exit", "NODE_EARLY_EXIT", "COMPLETED", "FAIL"),
    (
        "m11-gatea-readiness-timeout-01",
        "readiness-timeout",
        "READINESS_TIMEOUT",
        "ABORTED",
        "FAIL",
    ),
    (
        "m11-gatea-owner-mismatch-01",
        "owner-mismatch",
        "LISTENER_OWNERSHIP_MISMATCH",
        "ABORTED",
        "FAIL",
    ),
    ("m11-gatea-port-conflict-01", "positive", None, "ABORTED", "PENDING"),
    (
        "m11-gatea-user-cancel-ready-01",
        "positive",
        "USER_CANCELLED",
        "ABORTED",
        "PENDING",
    ),
    (
        "m11-gatea-browser-negative-01",
        "browser-negative",
        "BROWSER_HARD_FAILURE",
        "COMPLETED",
        "FAIL",
    ),
    (
        "m11-gatea-browser-collector-error-01",
        "positive",
        "COLLECTOR_ERROR",
        "ERROR",
        "PENDING",
    ),
    (
        "m11-gatea-subject-drift-01",
        "positive",
        "SUBJECT_DRIFT",
        "COMPLETED",
        "INCONCLUSIVE",
    ),
    (
        "m11-gatea-cleanup-failure-01",
        "positive",
        "CLEANUP_ERROR",
        "ERROR",
        "FAIL",
    ),
    (
        "m11-gatea-staging-failure-01",
        "positive",
        "EVIDENCE_ERROR",
        "ERROR",
        "PENDING",
    ),
    (
        "m11-gatea-memory-stop-01",
        "positive",
        "RESOURCE_MEMORY_SOFT_LIMIT",
        "ABORTED",
        "PENDING",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the preregistered M11 Gate A single-application exits."
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise AssertionError(f"{path.name} must contain a JSON object")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value) + b"\n")


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


def wait_for_listener(process: subprocess.Popen[bytes], port: int) -> None:
    for _ in range(80):
        if not port_is_free(port):
            return
        if process.poll() is not None:
            raise AssertionError("external listener exited before becoming ready")
        time.sleep(0.05)
    raise AssertionError("external listener did not become ready")


def wait_for_port_free(port: int) -> bool:
    for _ in range(100):
        if port_is_free(port):
            return True
        time.sleep(0.05)
    return False


def bootstrap_artifact(
    bundle: Path,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    manifest = read_json(bundle / "evidence-manifest.json")
    entries = [
        item
        for item in manifest["artifacts"]
        if item["evidence_type"] == "runtime.bootstrap"
    ]
    if not entries:
        return None
    if len(entries) != 1:
        raise AssertionError(f"{bundle.name} has multiple bootstrap artifacts")
    entry = entries[0]
    return read_json(bundle / Path(*entry["path"].split("/"))), entry


def verify_single_application_artifact(
    run_id: str,
    document: dict[str, Any],
    manifest_entry: dict[str, Any],
) -> None:
    facts = document["facts"]
    if document["source"] != "VeriTrail bootstrap-lifecycle/0.3":
        raise AssertionError(f"{run_id} used the wrong collector")
    if len(facts["nodes"]) != 1 or facts["nodes"][0]["role"] != "APPLICATION":
        raise AssertionError(f"{run_id} fabricated a second node")
    if facts["resource_observation"]["dependency_peak_rss_mb"] is not None:
        raise AssertionError(f"{run_id} fabricated dependency RSS")

    sealed_start = facts["start_order"]["sealed"]
    actual_start = facts["start_order"]["actual"]
    sealed_teardown = facts["teardown_order"]["sealed"]
    attempted_teardown = facts["teardown_order"]["attempted"]
    completed_teardown = facts["teardown_order"]["completed"]
    if sealed_start != ["application"] or sealed_teardown != ["application"]:
        raise AssertionError(f"{run_id} did not preserve the sealed one-node order")
    if actual_start not in ([], ["application"]):
        raise AssertionError(f"{run_id} started a non-application node")
    if attempted_teardown != list(reversed(actual_start)):
        raise AssertionError(f"{run_id} did not attempt reverse-order teardown")
    if completed_teardown != attempted_teardown:
        raise AssertionError(f"{run_id} did not complete every attempted teardown")

    attachments = manifest_entry.get("attachments")
    if not isinstance(attachments, list) or len(attachments) != 2:
        raise AssertionError(f"{run_id} did not publish exactly two bootstrap streams")
    expected_paths = {
        "attachments/bootstrap/application/stdout.txt": "bootstrap-application-stdout",
        "attachments/bootstrap/application/stderr.txt": "bootstrap-application-stderr",
    }
    observed_paths = {
        item.get("path"): item.get("logical_name")
        for item in attachments
        if isinstance(item, dict)
    }
    if observed_paths != expected_paths:
        raise AssertionError(f"{run_id} bootstrap stream attachments drifted")
    node = facts["nodes"][0]
    referenced_paths = {
        node[stream_name]["attachment"]["path"]
        for stream_name in ("stdout", "stderr")
    }
    if referenced_paths != set(expected_paths):
        raise AssertionError(f"{run_id} bootstrap stream references drifted")


def prepare_authorities(
    output: Path, subject_root: Path, bindings: Path
) -> dict[str, dict[str, Any]]:
    base_plan = read_json(EXAMPLE_ROOT / "plan-positive.json")
    authority_set = read_json(EXAMPLE_ROOT / "authority-set.json")
    authorities: dict[str, dict[str, Any]] = {}
    for raw in authority_set["authorities"]:
        profile = seal_project_profile(read_json(EXAMPLE_ROOT / raw["profile"]))
        if profile["seal"]["digest"] != raw["profile_sha256"]:
            raise AssertionError(f"{raw['name']} Profile digest drifted")
        draft = copy.deepcopy(base_plan)
        draft["plan_id"] = raw["plan_id"]
        draft["bootstrap_profile"] = {
            "profile_id": profile["profile_id"],
            "profile_version": profile["version"],
            "profile_sha256": profile["seal"]["digest"],
        }
        missing_selector = raw["browser_missing_selector"]
        if missing_selector is not None:
            step = next(
                item
                for item in draft["browser"]["steps"]
                if item["id"] == "evidence-list-visible"
            )
            step["selector"] = missing_selector
        plan = seal_plan(draft, profile)
        if plan["seal"]["digest"] != raw["plan_sha256"]:
            raise AssertionError(f"{raw['name']} Plan digest drifted")
        preview = build_bootstrap_preview(
            plan,
            profile,
            subject_root=subject_root,
            tool_bindings_path=bindings,
        )
        authority_root = output / "authorities" / raw["name"]
        write_json(authority_root / "sealed-profile.json", profile)
        write_json(authority_root / "sealed-plan.json", plan)
        write_json(authority_root / "bootstrap-preview.json", preview)
        authorities[raw["name"]] = {
            "profile": profile,
            "plan": plan,
            "preview": preview,
        }
    return authorities


def observed_runner_with(
    **options: Any,
) -> Callable[..., Any]:
    def runner(
        plan: dict[str, Any],
        profile: dict[str, Any],
        resolved: Any,
        *,
        output_parent: Path,
        cancel_event: threading.Event | None,
    ) -> Any:
        return run_observed_bootstrap(
            plan,
            profile,
            resolved,
            output_parent=output_parent,
            cancel_event=cancel_event,
            **options,
        )

    return runner


def run_scenario(
    *,
    run_id: str,
    authority_name: str,
    authorities: dict[str, dict[str, Any]],
    subject_root: Path,
    bindings: Path,
    runs_root: Path,
) -> tuple[BootstrapPublicRunResult, dict[str, Any]]:
    authority = authorities[authority_name]
    plan = authority["plan"]
    profile = authority["profile"]
    preview = authority["preview"]
    output = runs_root / run_id
    cancellation: threading.Event | None = None
    resolver: Callable[..., Any] = resolve_bootstrap
    observed_runner: Callable[..., Any] = run_observed_bootstrap
    recovery = {
        "external_owner_preserved": None,
        "subject_restored": None,
        "actual_resource_recovery": None,
    }
    external_socket: socket.socket | None = None
    external_process: subprocess.Popen[bytes] | None = None

    if run_id == "m11-gatea-port-conflict-01":
        def resolve_then_contest(*args: Any, **kwargs: Any) -> Any:
            nonlocal external_socket
            resolved = resolve_bootstrap(*args, **kwargs)
            external_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            external_socket.bind(("127.0.0.1", APPLICATION_PORT))
            external_socket.listen(socket.SOMAXCONN)
            return resolved

        resolver = resolve_then_contest
    elif run_id == "m11-gatea-owner-mismatch-01":
        def owner_mismatch_runner(
            active_plan: dict[str, Any],
            active_profile: dict[str, Any],
            resolved: Any,
            *,
            output_parent: Path,
            cancel_event: threading.Event | None,
        ) -> Any:
            nonlocal external_process
            environment = {
                key: value
                for key, value in os.environ.items()
                if key.upper() in {"SYSTEMROOT", "WINDIR"}
            }
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            external_process = subprocess.Popen(
                [
                    sys.executable,
                    "gatea_helper.py",
                    "serve-for",
                    str(APPLICATION_PORT),
                    "30",
                ],
                cwd=subject_root / "examples" / "bootstrap",
                env=environment,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            wait_for_listener(external_process, APPLICATION_PORT)

            def probe_then_release_external_owner(
                session: Any,
                readiness: dict[str, Any],
                **kwargs: Any,
            ) -> Any:
                observation = probe_owned_http_readiness(
                    session,
                    readiness,
                    **kwargs,
                )
                if observation.error_type == "LISTENER_OWNERSHIP_MISMATCH":
                    recovery["external_owner_preserved"] = (
                        external_process is not None
                        and external_process.poll() is None
                    )
                    if external_process is not None and external_process.poll() is None:
                        external_process.terminate()
                        external_process.wait(timeout=5)
                    recovery["actual_resource_recovery"] = wait_for_port_free(
                        APPLICATION_PORT
                    )
                return observation

            return run_observed_bootstrap(
                active_plan,
                active_profile,
                resolved,
                output_parent=output_parent,
                cancel_event=cancel_event,
                readiness_probe=probe_then_release_external_owner,
            )

        observed_runner = owner_mismatch_runner
    elif run_id == "m11-gatea-user-cancel-ready-01":
        cancellation = threading.Event()

        def cancel_after_ready(session: Any, readiness: dict[str, Any], **kwargs: Any) -> Any:
            observation = probe_owned_http_readiness(session, readiness, **kwargs)
            if observation.ready:
                cancellation.set()
            return observation

        observed_runner = observed_runner_with(readiness_probe=cancel_after_ready)
    elif run_id == "m11-gatea-browser-collector-error-01":
        def fail_browser(active_plan: dict[str, Any]) -> ObservedBrowserEvidence:
            raise ObservedBrowserCollectionError(
                "SafetyError",
                peak_rss_mb=0.0,
                resource_sampling_complete=True,
                process_cleanup_complete=True,
                job_memory_limit_mb=active_plan["browser"]["max_job_memory_mb"],
                job_memory_limit_enforced=True,
            )

        observed_runner = observed_runner_with(browser_runner=fail_browser)
    elif run_id == "m11-gatea-subject-drift-01":
        state = subject_root / "examples" / "bootstrap" / "state.txt"

        def drift_after_browser(active_plan: dict[str, Any]) -> ObservedBrowserEvidence:
            observed = collect_observed_browser_evidence(active_plan)
            state.write_text("changed\n", encoding="utf-8")
            return observed

        observed_runner = observed_runner_with(browser_runner=drift_after_browser)
    elif run_id == "m11-gatea-cleanup-failure-01":
        class CleanupFailureProxy:
            def __init__(self, session: OwnedServiceSession) -> None:
                self._session = session
                self.node_id = session.node_id
                self.start_observation = session.start_observation

            def __getattr__(self, name: str) -> Any:
                return getattr(self._session, name)

            def terminate(self) -> Any:
                observation = self._session.terminate()
                return replace(
                    observation,
                    handles_released=False,
                    error_type="HANDLE_RELEASE_FAILED",
                    cleanup_complete=False,
                )

        def cleanup_failure_factory(**kwargs: Any) -> CleanupFailureProxy:
            return CleanupFailureProxy(OwnedServiceSession.start(**kwargs))

        observed_runner = observed_runner_with(session_factory=cleanup_failure_factory)
    elif run_id == "m11-gatea-staging-failure-01":
        def fail_staging(path: Path, content: bytes) -> None:
            path.write_bytes(content[:17])
            raise OSError("preregistered staging failure")

        observed_runner = observed_runner_with(staging_writer=fail_staging)
    elif run_id == "m11-gatea-memory-stop-01":
        observed_runner = observed_runner_with(
            host_memory_reader=lambda: (16 * 1024**3, 3500 * MEBIBYTE)
        )

    try:
        result = run_bootstrap_bundle(
            plan,
            profile,
            subject_root=subject_root,
            tool_bindings_path=bindings,
            approved_preview_sha256=preview["preview_sha256"],
            output=output,
            run_id=run_id,
            cancel_event=cancellation,
            resolver=resolver,
            observed_runner=observed_runner,
        )
        if external_socket is not None:
            recovery["external_owner_preserved"] = (
                external_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN) == 1
            )
        if (
            external_process is not None
            and recovery["external_owner_preserved"] is None
        ):
            recovery["external_owner_preserved"] = external_process.poll() is None
        if run_id == "m11-gatea-subject-drift-01":
            state = subject_root / "examples" / "bootstrap" / "state.txt"
            if state.read_text(encoding="utf-8") != "changed\n":
                raise AssertionError("subject drift was not preserved by VeriTrail")
            state.write_text("stable\n", encoding="utf-8")
            recovery["subject_restored"] = state.read_text(encoding="utf-8") == "stable\n"
        return result, recovery
    finally:
        if external_socket is not None:
            external_socket.close()
            recovery["actual_resource_recovery"] = wait_for_port_free(
                APPLICATION_PORT
            )
        if external_process is not None:
            if external_process.poll() is None:
                external_process.terminate()
                try:
                    external_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    external_process.kill()
                    external_process.wait(timeout=5)
            recovery["actual_resource_recovery"] = (
                external_process.poll() is not None
                and wait_for_port_free(APPLICATION_PORT)
            )


def scan_sensitive(runs_root: Path, forbidden: list[str]) -> int:
    checked = 0
    for path in runs_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        content = path.read_text(encoding="utf-8", errors="replace").casefold()
        for value in forbidden:
            if value and value.casefold() in content:
                raise AssertionError(f"sensitive value persisted in {path.name}")
        checked += 1
    return checked


def main() -> int:
    args = parse_args()
    if os.name != "nt":
        raise AssertionError("M11 Gate A acceptance is Windows-only")
    output = args.output.absolute()
    if output.exists():
        raise AssertionError("acceptance output already exists")
    if not port_is_free(APPLICATION_PORT):
        raise AssertionError("preregistered application port 18774 is occupied")
    total_memory, available_memory = host_memory_bytes()
    start_available_mb = available_memory // MEBIBYTE
    if start_available_mb < 4096:
        raise AssertionError("available memory is below the preregistered soft line")
    output.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(output.parent).free // MEBIBYTE < 1024:
        raise AssertionError("output volume is below the preregistered hard line")

    subject_root = output / "subject"
    subject_example = subject_root / "examples" / "bootstrap"
    shutil.copytree(EXAMPLE_ROOT, subject_example)
    (subject_example / "state.txt").write_text("stable\n", encoding="utf-8")
    bindings = output / "inputs" / "tool-bindings.json"
    write_json(
        bindings,
        {
            "schema_version": "0.1",
            "bindings": {
                "python-application": {
                    "executable": str(Path(sys.executable).resolve())
                }
            },
        },
    )
    authorities = prepare_authorities(output, subject_root, bindings)
    runs_root = output / "runs"
    runs_root.mkdir(parents=True)

    ledger: list[dict[str, Any]] = []
    resources: list[dict[str, Any]] = []
    for ordinal, (run_id, authority_name, expected_stop, status, verdict) in enumerate(
        RUNS, start=1
    ):
        result, recovery = run_scenario(
            run_id=run_id,
            authority_name=authority_name,
            authorities=authorities,
            subject_root=subject_root,
            bindings=bindings,
            runs_root=runs_root,
        )
        if result.report["execution_status"] != status or result.report["verdict"] != verdict:
            raise AssertionError(f"{run_id} status/verdict differs from the contract")
        validated = validate_bundle(runs_root / run_id, runs_root)
        artifact = bootstrap_artifact(runs_root / run_id)
        if artifact is not None:
            document, manifest_entry = artifact
            verify_single_application_artifact(run_id, document, manifest_entry)
            facts = document["facts"]
            actual_stop = facts["stop"]["reason"]
            resources.append(
                {
                    "run_id": run_id,
                    "host_available_memory_min_mb": facts["resource_observation"][
                        "host_available_memory_min_mb"
                    ],
                    "core_peak_rss_mb": facts["resource_observation"]["core_peak_rss_mb"],
                    "application_peak_rss_mb": facts["resource_observation"][
                        "application_peak_rss_mb"
                    ],
                    "browser_peak_rss_mb": facts["resource_observation"][
                        "browser_peak_rss_mb"
                    ],
                }
            )
        elif run_id != "m11-gatea-port-conflict-01":
            raise AssertionError(f"{run_id} did not publish bootstrap Evidence")
        else:
            actual_stop = None
        if actual_stop != expected_stop:
            raise AssertionError(f"{run_id} stop reason differs from the contract")
        if run_id in {
            "m11-gatea-port-conflict-01",
            "m11-gatea-owner-mismatch-01",
        } and (
            recovery["external_owner_preserved"] is not True
            or recovery["actual_resource_recovery"] is not True
        ):
            raise AssertionError(
                f"{run_id} did not preserve and independently recover its external owner"
            )
        if run_id == "m11-gatea-subject-drift-01":
            state = subject_root / "examples" / "bootstrap" / "state.txt"
            if (
                recovery["subject_restored"] is not True
                or state.read_text(encoding="utf-8") != "stable\n"
            ):
                raise AssertionError("the Subject drift fixture was not independently restored")
        if not port_is_free(APPLICATION_PORT):
            raise AssertionError(f"{run_id} left port 18774 occupied after recovery")
        residue = list(output.rglob(".veritrail-*"))
        if residue:
            raise AssertionError(f"{run_id} left owned staging residue")
        ledger.append(
            {
                "ordinal": ordinal,
                "run_id": run_id,
                "authority": authority_name,
                "stop_reason": actual_stop,
                "execution_status": validated.execution_status,
                "verdict": validated.verdict,
                "bundle_sha256": validated.bundle_sha256,
                "recovery": recovery,
            }
        )

    comparison = create_comparison_bundle(
        baseline=runs_root / "m11-gatea-positive-01",
        repeat=runs_root / "m11-gatea-positive-02",
        output=output / "comparison",
    )
    if not comparison.comparable or comparison.comparison_status != "MATCH":
        raise AssertionError("the two positive Gate A Runs did not compare as MATCH")
    comparison_document = read_json(output / "comparison" / "comparison.json")
    if comparison_document["differences"] != []:
        raise AssertionError("the positive Gate A Comparison contains differences")

    pairing_code = None
    try:
        load_pairing_source(
            runs_root / "m11-gatea-positive-01", "project_bootstrap_topology"
        )
    except PairingError as exc:
        pairing_code = exc.code
    if pairing_code != "SOURCE_PLAN_VERSION_UNSUPPORTED":
        raise AssertionError("Pairing did not explicitly reject Plan 0.7")
    batch_code = None
    try:
        load_batch_source(
            runs_root / "m11-gatea-positive-01",
            runs_root,
            "project_bootstrap_topology",
        )
    except BatchError as exc:
        batch_code = exc.code
    if batch_code != "SOURCE_PLAN_VERSION_UNSUPPORTED":
        raise AssertionError("Batch did not explicitly reject Plan 0.7")

    catalog = build_catalog(runs_root, output / "catalog")
    if catalog.status != "COMPLETED" or catalog.run_count != 13 or catalog.issue_count != 0:
        raise AssertionError("Catalog did not independently accept all 13 Gate A Bundles")
    sensitive_files = scan_sensitive(
        runs_root,
        [
            str(output),
            str(subject_root),
            str(Path.home()),
            "authorization:",
            "set-cookie:",
            "private key",
            ".env",
        ],
    )
    final_port_free = port_is_free(APPLICATION_PORT)
    final_residue = list(output.rglob(".veritrail-*"))
    if not final_port_free or final_residue:
        raise AssertionError("Gate A final residual gate failed")

    summary = {
        "schema_version": "0.1",
        "contract_version": "0.3",
        "platform": "WINDOWS_11",
        "cold_state": "C1_PROCESS_COLD",
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "start_resource": {
            "total_memory_mb": total_memory // MEBIBYTE,
            "available_memory_mb": start_available_mb,
        },
        "authorities": {
            name: {
                "profile_sha256": value["profile"]["seal"]["digest"],
                "plan_sha256": value["plan"]["seal"]["digest"],
                "preview_sha256": value["preview"]["preview_sha256"],
            }
            for name, value in authorities.items()
        },
        "runs": ledger,
        "resources": resources,
        "comparison": {
            "status": comparison.comparison_status,
            "difference_count": len(comparison_document["differences"]),
        },
        "catalog": {
            "status": catalog.status,
            "run_count": catalog.run_count,
            "issue_count": catalog.issue_count,
        },
        "derived_analysis": {
            "pairing_rejection": pairing_code,
            "batch_rejection": batch_code,
        },
        "sensitive_scan": {"checked_text_files": sensitive_files, "matches": 0},
        "residual": {
            "application_port_free": final_port_free,
            "owned_staging_count": len(final_residue),
        },
    }
    write_json(output / "acceptance.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
