from __future__ import annotations

import argparse
import copy
import ctypes
import hashlib
import io
import json
import os
import shutil
import socket
import sys
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from veritrail.batching import seeded_profile_order
from veritrail.catalog import build_catalog
from veritrail.cli import main as cli_main
from veritrail.orchestration import prepare_static_target
from veritrail.plan import seal_plan


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BASE_PLAN = REPOSITORY_ROOT / "examples" / "orchestration" / "plan.json"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "m8-batch-acceptance"
PROFILE_CELLS = [
    ("baseline", "off", "off"),
    ("queue-only", "off", "on"),
    ("cache-only", "on", "off"),
    ("combined", "on", "on"),
]
ANALYSIS_FILES = (
    "sealed-batch-plan.json",
    "batch-analysis.json",
    "batch-analysis.md",
    "batch-analysis-manifest.json",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the real, bounded M8 2x2 batch matrix over frozen M5 Runs."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--port", type=int, default=18769)
    parser.add_argument("--seed", type=int, default=20260809)
    return parser.parse_args()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path.name} must contain a JSON object")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


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


def available_memory_mb() -> int:
    if sys.platform == "win32":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.c_ulong),
                ("memory_load", ctypes.c_ulong),
                ("total_physical", ctypes.c_ulonglong),
                ("available_physical", ctypes.c_ulonglong),
                ("total_page_file", ctypes.c_ulonglong),
                ("available_page_file", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong),
                ("available_virtual", ctypes.c_ulonglong),
                ("available_extended_virtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatus()
        status.length = ctypes.sizeof(MemoryStatus)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            raise OSError("GlobalMemoryStatusEx failed")
        return int(status.available_physical // (1024 * 1024))
    if hasattr(os, "sysconf"):
        page_size = int(os.sysconf("SC_PAGE_SIZE"))
        available_pages = int(os.sysconf("SC_AVPHYS_PAGES"))
        return int(page_size * available_pages // (1024 * 1024))
    raise OSError("available memory is not observable on this platform")


def run_cli(arguments: list[str]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = cli_main(arguments)
    output_text = stdout.getvalue().strip()
    error_text = stderr.getvalue().strip()
    output = json.loads(output_text) if output_text else {}
    error = json.loads(error_text) if error_text else {}
    return code, output, error


def require_cli(arguments: list[str]) -> dict[str, Any]:
    code, output, error = run_cli(arguments)
    if code != 0:
        error_code = error.get("error", {}).get("code", "UNKNOWN")
        raise AssertionError(f"CLI command {arguments[0]} failed with {error_code}")
    return output


def schedule(profile_ids: list[str], seed: int) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for index, profile_id in enumerate(profile_ids, start=1):
        slots.append(
            {
                "slot_id": f"coverage-{index:02d}",
                "phase": "COVERAGE",
                "repetition": 0,
                "wave": index,
                "position": 1,
                "profile_id": profile_id,
            }
        )
    order = seeded_profile_order(profile_ids, seed, 1)
    for index, profile_id in enumerate(order, start=1):
        slots.append(
            {
                "slot_id": f"perturbation-{index:02d}",
                "phase": "PERTURBATION",
                "repetition": 1,
                "wave": (index + 1) // 2,
                "position": 1 if index % 2 else 2,
                "profile_id": profile_id,
            }
        )
    return slots


def site_html(profile_id: str, *, planned_console_error: bool) -> str:
    error_script = (
        "if (window.innerWidth >= 1000) console.error('planned combined-profile signal');"
        if planned_console_error
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <title>VeriTrail M8 {profile_id}</title>
    <style>
      :root {{ color-scheme: light; font-family: system-ui, sans-serif; background: #f5f1e8; color: #203632; }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px; }}
      main {{ width: min(100%, 720px); border: 1px solid #718a83; padding: clamp(20px, 5vw, 48px); background: #fffdf7; }}
      form {{ display: grid; gap: 12px; margin-block: 24px; }}
      input, button {{ width: 100%; min-height: 44px; font: inherit; }}
      input {{ border: 1px solid #718a83; padding: 10px 12px; }}
      button {{ border: 0; background: #7a2e2e; color: white; font-weight: 700; }}
      [data-testid="status"] {{ min-height: 28px; font-weight: 700; }}
    </style>
  </head>
  <body>
    <main data-profile="{profile_id}">
      <p>Controlled full-factorial fixture</p>
      <h1>One sealed Profile, one immutable Run</h1>
      <form data-testid="fixture-form">
        <label for="label">Run label</label>
        <input id="label" data-testid="run-label" autocomplete="off" value="demo">
        <button data-testid="load-evidence" type="submit">Load evidence</button>
      </form>
      <p data-testid="status" aria-live="polite">idle</p>
      <ul data-testid="evidence-list" hidden></ul>
    </main>
    <script>
      const form = document.querySelector('[data-testid="fixture-form"]');
      const status = document.querySelector('[data-testid="status"]');
      const list = document.querySelector('[data-testid="evidence-list"]');
      form.addEventListener('submit', async (event) => {{
        event.preventDefault();
        status.textContent = 'loading';
        const response = await fetch('/data.json?run=fixture');
        if (!response.ok) throw new Error(`fixture request failed: ${{response.status}}`);
        const payload = await response.json();
        list.replaceChildren(...payload.layers.map((layer) => {{
          const item = document.createElement('li');
          item.textContent = layer;
          return item;
        }}));
        list.hidden = false;
        status.textContent = `evidence ready: ${{document.querySelector('[data-testid="run-label"]').value}}`;
        {error_script}
      }});
    </script>
  </body>
</html>
"""


def create_sites(subject_root: Path) -> None:
    for profile_id, cache_mode, queue_mode in PROFILE_CELLS:
        site = subject_root / "fixtures" / profile_id
        site.mkdir(parents=True)
        (site / "index.html").write_text(
            site_html(profile_id, planned_console_error=profile_id == "combined"),
            encoding="utf-8",
            newline="\n",
        )
        write_json(
            site / "data.json",
            {
                "profile": profile_id,
                "cache_mode": cache_mode,
                "queue_mode": queue_mode,
                "layers": ["Console", "Network", "Screenshot", "Viewport"],
            },
        )


def create_source_plans(
    subject_root: Path, plans_root: Path, port: int
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    base = read_json(BASE_PLAN)
    base.pop("seal", None)
    base["plan_id"] = "m8-real-static-profile"
    base["question"] = (
        "Does this preregistered static Profile preserve its browser outcome under the frozen M5 lifecycle?"
    )
    base["preflight"]["ports"] = [{"port": port, "expected": "FREE"}]
    origin = f"http://localhost:{port}"
    base["browser"]["start_url"] = f"{origin}/index.html"
    base["browser"]["allowed_origins"] = [origin]
    plans: dict[str, dict[str, Any]] = {}
    profiles: list[dict[str, Any]] = []
    for version, (profile_id, cache_mode, queue_mode) in enumerate(PROFILE_CELLS, start=1):
        relative_root = f"fixtures/{profile_id}"
        plan = copy.deepcopy(base)
        plan["version"] = version
        plan["subject"]["version"] = f"profile-{profile_id}"
        plan["subject"]["source_ref"] = relative_root
        plan["target"]["root"] = relative_root
        plan["target"]["port"] = port
        primary = next(item for item in plan["variables"] if item["role"] == "PRIMARY")
        primary.update(
            name="batch_profile",
            value=profile_id,
            source="sealed-batch-plan",
            unit="profile",
        )
        snapshot = prepare_static_target(plan, subject_root)
        plan["baseline"]["fingerprint"] = snapshot.fingerprint
        sealed = seal_plan(plan)
        plans[profile_id] = sealed
        write_json(plans_root / f"{profile_id}.json", sealed)
        profiles.append(
            {
                "id": profile_id,
                "cells": {"cache-mode": cache_mode, "queue-mode": queue_mode},
                "plan_sha256": sealed["seal"]["digest"],
                "realization": {
                    "subject_version": f"profile-{profile_id}",
                    "subject_source_ref": relative_root,
                    "target_root": relative_root,
                    "static_root_fingerprint": snapshot.fingerprint,
                },
                "estimated_memory_mb": 256,
            }
        )
    fingerprints = {
        profile["realization"]["static_root_fingerprint"] for profile in profiles
    }
    if len(fingerprints) != len(PROFILE_CELLS):
        raise AssertionError("every Profile must have a distinct static fingerprint")
    return plans, profiles


def create_batch_plan(
    profiles: list[dict[str, Any]], *, seed: int, version: int = 1
) -> dict[str, Any]:
    profile_ids = [profile["id"] for profile in profiles]
    return {
        "schema_version": "0.1",
        "batch_id": "m8-real-two-by-two",
        "version": version,
        "question": (
            "Do all four preregistered static Profiles preserve their expected browser outcome "
            "across canonical coverage and fixed-seed perturbation?"
        ),
        "primary_variable": {
            "name": "batch_profile",
            "source": "sealed-batch-plan",
            "unit": "profile",
        },
        "dimensions": [
            {
                "name": "cache-mode",
                "levels": [
                    {"id": "off", "value": False},
                    {"id": "on", "value": True},
                ],
            },
            {
                "name": "queue-mode",
                "levels": [
                    {"id": "off", "value": False},
                    {"id": "on", "value": True},
                ],
            },
        ],
        "profiles": copy.deepcopy(profiles),
        "execution_policy": {
            "order_algorithm": "SHA256_RANK_V1",
            "seed": seed,
            "perturbation_repetitions": 1,
            "max_parallel": 2,
            "memory_budget_mb": 512,
            "preflight_between_waves": True,
            "cleanup_between_waves": True,
        },
        "schedule": schedule(profile_ids, seed),
        "outcomes": [
            {
                "assertion_id": "console-errors-zero",
                "expected_actual": {
                    "baseline": 0,
                    "queue-only": 0,
                    "cache-only": 0,
                    "combined": 1,
                },
            }
        ],
        "limits": [
            "Profile-level observations do not prove component-level causality or statistical interaction.",
            "A wave is a sealed resource envelope and does not prove real runtime overlap.",
        ],
        "reproduction_steps": [
            "Seal this BatchPlan before creating any assigned source Run.",
            "Create one immutable Plan 0.4 Run for every slot in the sealed order.",
        ],
        "cleanup_steps": [
            "Verify every source Run records preflight, browser, orchestration, and cleanup facts.",
            "Verify no preview process, listening port, or staging directory remains.",
        ],
    }


def seal_batch(input_path: Path, output_path: Path) -> dict[str, Any]:
    result = require_cli(
        ["seal-batch", "--plan", str(input_path), "--output", str(output_path)]
    )
    sealed = read_json(output_path)
    if result["batch_plan_sha256"] != sealed["seal"]["digest"]:
        raise AssertionError("seal-batch result does not match the persisted BatchPlan")
    return sealed


def write_assignment(
    path: Path,
    batch: dict[str, Any],
    bundle_by_slot: dict[str, str],
    *,
    omitted: set[str] | None = None,
    remap: dict[str, str] | None = None,
) -> None:
    omitted = omitted or set()
    remap = remap or {}
    write_json(
        path,
        {
            "schema_version": "0.1",
            "batch_plan_sha256": batch["seal"]["digest"],
            "assignments": [
                {
                    "slot_id": slot["slot_id"],
                    "bundle": bundle_by_slot[remap.get(slot["slot_id"], slot["slot_id"])],
                }
                for slot in batch["schedule"]
                if slot["slot_id"] not in omitted
            ],
        },
    )


def assertion_actual(report: dict[str, Any], assertion_id: str) -> Any:
    return next(item for item in report["assertions"] if item["id"] == assertion_id)["actual"]


def run_source_matrix(
    batch: dict[str, Any],
    plans_root: Path,
    subject_root: Path,
    runs_root: Path,
    port: int,
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    runs_root.mkdir(parents=True)
    bundle_by_slot: dict[str, str] = {}
    facts: list[dict[str, Any]] = []
    expected = batch["outcomes"][0]["expected_actual"]
    for slot in batch["schedule"]:
        if not port_is_free(port):
            raise AssertionError("M5 port was not free before a source Run")
        slot_id = slot["slot_id"]
        profile_id = slot["profile_id"]
        bundle = slot_id
        result = require_cli(
            [
                "run",
                "--plan",
                str(plans_root / f"{profile_id}.json"),
                "--subject-root",
                str(subject_root),
                "--run-id",
                f"m8-{slot_id}",
                "--output",
                str(runs_root / bundle),
            ]
        )
        report = read_json(runs_root / bundle / "report.json")
        actual = assertion_actual(report, "console-errors-zero")
        expected_verdict = "FAIL" if profile_id == "combined" else "PASS"
        if (
            result.get("resource_decision") != "PROCEED"
            or result.get("target_started") is not True
            or result.get("target_ready") is not True
            or result.get("cleanup_complete") is not True
            or report.get("execution_status") != "COMPLETED"
            or report.get("verdict") != expected_verdict
            or actual != expected[profile_id]
            or not port_is_free(port)
        ):
            raise AssertionError(f"source Run contract failed for {slot_id}")
        bundle_by_slot[slot_id] = bundle
        facts.append(
            {
                "slot_id": slot_id,
                "profile_id": profile_id,
                "run_id": report["run_id"],
                "execution_status": report["execution_status"],
                "verdict": report["verdict"],
                "console_error_count": actual,
                "preflight": result["resource_decision"],
                "cleanup_complete": result["cleanup_complete"],
            }
        )
    return bundle_by_slot, facts


def analyze(
    *,
    plan: Path,
    assignment: Path,
    runs_root: Path,
    output: Path,
    expected_coverage: str,
    expected_hypothesis: str,
) -> dict[str, Any]:
    result = require_cli(
        [
            "analyze-batch",
            "--plan",
            str(plan),
            "--assignment",
            str(assignment),
            "--runs-root",
            str(runs_root),
            "--output",
            str(output),
        ]
    )
    analysis = read_json(output / "batch-analysis.json")
    if (
        result["coverage_status"] != expected_coverage
        or result["hypothesis_status"] != expected_hypothesis
        or analysis["coverage_status"] != expected_coverage
        or analysis["hypothesis_status"] != expected_hypothesis
        or analysis["runtime_overlap_claim"] != "NOT_PROVEN"
    ):
        raise AssertionError(f"unexpected BatchAnalysis state for {output.name}")
    return analysis


def file_hashes(root: Path) -> dict[str, str]:
    return {name: sha256_file(root / name) for name in ANALYSIS_FILES}


def staging_directories(root: Path) -> list[str]:
    return [
        path.name
        for path in root.rglob(".veritrail-*")
        if path.is_dir()
    ]


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if output.exists():
        print("M8 acceptance refuses to overwrite an existing output directory.", file=sys.stderr)
        return 2
    if not 1024 <= args.port <= 65535 or not port_is_free(args.port):
        print("M8 acceptance requires a free explicit loopback port.", file=sys.stderr)
        return 2
    memory_before = available_memory_mb()
    disk_before = shutil.disk_usage(REPOSITORY_ROOT).free // (1024 * 1024)
    if memory_before < 4096 or disk_before < 1024:
        print("M8 acceptance preflight rejected the current resource state.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "acceptance": "m8-real-preregistered-full-factorial-batch",
        "started_at": utc_now(),
        "execution_status": "RUNNING",
        "verdict": "INCONCLUSIVE",
        "execution_mode": "SERIAL",
        "runtime_overlap_claim": "NOT_PROVEN",
        "checks": [],
        "resources": {
            "available_memory_mb_before": memory_before,
            "disk_free_mb_before": disk_before,
            "memory_gate_mb": 4096,
            "disk_gate_mb": 1024,
        },
    }
    exit_code = 1
    try:
        inputs = output / "inputs"
        subject_root = inputs / "subject"
        plans_root = inputs / "plans"
        create_sites(subject_root)
        _, profiles = create_source_plans(subject_root, plans_root, args.port)
        summary["checks"].append("four-distinct-fixed-profile-realizations")

        unsealed_batch_path = inputs / "batch-plan.json"
        sealed_batch_path = inputs / "sealed-batch-plan.json"
        write_json(unsealed_batch_path, create_batch_plan(profiles, seed=args.seed))
        batch = seal_batch(unsealed_batch_path, sealed_batch_path)
        summary["checks"].append("batch-plan-sealed-before-source-runs")

        runs_root = output / "runs"
        bundle_by_slot, source_runs = run_source_matrix(
            batch, plans_root, subject_root, runs_root, args.port
        )
        summary["source_runs"] = source_runs
        if len(source_runs) != 8 or Counter(item["profile_id"] for item in source_runs) != {
            profile_id: 2 for profile_id, _, _ in PROFILE_CELLS
        }:
            raise AssertionError("real source matrix did not cover every Profile twice")
        if sum(item["verdict"] == "FAIL" for item in source_runs) != 2:
            raise AssertionError("the planned combined Profile FAIL signal was not preserved")
        summary["checks"].append("eight-real-m5-runs-with-planned-fail-preserved")

        assignments = output / "assignments"
        supported_assignment = assignments / "supported.json"
        write_assignment(supported_assignment, batch, bundle_by_slot)
        analyses = output / "analyses"
        supported = analyze(
            plan=sealed_batch_path,
            assignment=supported_assignment,
            runs_root=runs_root,
            output=analyses / "supported",
            expected_coverage="COMPLETE",
            expected_hypothesis="SUPPORTED",
        )
        supported_repeat = analyze(
            plan=sealed_batch_path,
            assignment=supported_assignment,
            runs_root=runs_root,
            output=analyses / "supported-repeat",
            expected_coverage="COMPLETE",
            expected_hypothesis="SUPPORTED",
        )
        if file_hashes(analyses / "supported") != file_hashes(analyses / "supported-repeat"):
            raise AssertionError("identical BatchAnalysis inputs were not byte deterministic")
        summary["checks"].append("supported-and-byte-deterministic")

        contradicted_plan = copy.deepcopy(batch)
        contradicted_plan.pop("seal")
        contradicted_plan["outcomes"][0]["expected_actual"]["combined"] = 0
        contradicted_input = inputs / "contradicted-batch-plan.json"
        contradicted_sealed = inputs / "sealed-contradicted-batch-plan.json"
        write_json(contradicted_input, contradicted_plan)
        contradicted_batch = seal_batch(contradicted_input, contradicted_sealed)
        contradicted_assignment = assignments / "contradicted.json"
        write_assignment(contradicted_assignment, contradicted_batch, bundle_by_slot)
        contradicted = analyze(
            plan=contradicted_sealed,
            assignment=contradicted_assignment,
            runs_root=runs_root,
            output=analyses / "contradicted",
            expected_coverage="COMPLETE",
            expected_hypothesis="CONTRADICTED",
        )

        incomplete_assignment = assignments / "incomplete.json"
        write_assignment(
            incomplete_assignment,
            batch,
            bundle_by_slot,
            omitted={batch["schedule"][-1]["slot_id"]},
        )
        incomplete = analyze(
            plan=sealed_batch_path,
            assignment=incomplete_assignment,
            runs_root=runs_root,
            output=analyses / "incomplete",
            expected_coverage="INCOMPLETE",
            expected_hypothesis="INCONCLUSIVE",
        )

        coverage_baseline = next(
            slot["slot_id"]
            for slot in batch["schedule"]
            if slot["phase"] == "COVERAGE" and slot["profile_id"] == "baseline"
        )
        perturbation_baseline = next(
            slot["slot_id"]
            for slot in batch["schedule"]
            if slot["phase"] == "PERTURBATION" and slot["profile_id"] == "baseline"
        )
        wrong_order_assignment = assignments / "wrong-order.json"
        write_assignment(
            wrong_order_assignment,
            batch,
            bundle_by_slot,
            remap={
                coverage_baseline: perturbation_baseline,
                perturbation_baseline: coverage_baseline,
            },
        )
        wrong_order = analyze(
            plan=sealed_batch_path,
            assignment=wrong_order_assignment,
            runs_root=runs_root,
            output=analyses / "inconclusive",
            expected_coverage="INCONCLUSIVE",
            expected_hypothesis="INCONCLUSIVE",
        )
        if "WAVE_ORDER_MISMATCH" not in {item["code"] for item in wrong_order["reasons"]}:
            raise AssertionError("wrong source order was not identified as contamination")
        summary["checks"].append("contradicted-incomplete-and-order-inconclusive")

        alternate_seed = args.seed + 1
        primary_order = [
            slot["profile_id"] for slot in batch["schedule"] if slot["phase"] == "PERTURBATION"
        ]
        while seeded_profile_order([item[0] for item in PROFILE_CELLS], alternate_seed, 1) == primary_order:
            alternate_seed += 1
        alternate_input = inputs / "alternate-seed-batch-plan.json"
        alternate_sealed_path = inputs / "sealed-alternate-seed-batch-plan.json"
        write_json(
            alternate_input,
            create_batch_plan(profiles, seed=alternate_seed),
        )
        alternate_batch = seal_batch(alternate_input, alternate_sealed_path)
        primary_projection = copy.deepcopy(batch)
        alternate_projection = copy.deepcopy(alternate_batch)
        for projection in (primary_projection, alternate_projection):
            projection.pop("seal")
            projection["execution_policy"]["seed"] = "<CONTROLLED_SEED>"
            projection["schedule"] = "<SEED_DERIVED_SCHEDULE>"
        if primary_projection != alternate_projection:
            raise AssertionError("alternate BatchPlan changed more than seed and derived schedule")
        primary_members = Counter(
            (slot["phase"], slot["profile_id"]) for slot in batch["schedule"]
        )
        alternate_members = Counter(
            (slot["phase"], slot["profile_id"]) for slot in alternate_batch["schedule"]
        )
        if primary_members != alternate_members or len(batch["schedule"]) != len(
            alternate_batch["schedule"]
        ):
            raise AssertionError("changed seed changed matrix membership or coverage")
        alternate_order = [
            slot["profile_id"]
            for slot in alternate_batch["schedule"]
            if slot["phase"] == "PERTURBATION"
        ]
        if alternate_order == primary_order:
            raise AssertionError("changed seed did not change perturbation order")
        summary["seed_control"] = {
            "primary_seed": args.seed,
            "alternate_seed": alternate_seed,
            "primary_perturbation_order": primary_order,
            "alternate_perturbation_order": alternate_order,
            "member_count_preserved": True,
            "only_seed_and_derived_schedule_changed": True,
        }
        summary["checks"].append("changed-seed-preserves-members-and-coverage")

        negative = output / "negative"
        reused_bundle = "reused-baseline"
        shutil.copytree(runs_root / coverage_baseline, runs_root / reused_bundle)
        reused_assignment = assignments / "reused.json"
        reused_mapping = dict(bundle_by_slot)
        reused_mapping[reused_bundle] = reused_bundle
        write_assignment(
            reused_assignment,
            batch,
            reused_mapping,
            remap={perturbation_baseline: reused_bundle},
        )
        reused = analyze(
            plan=sealed_batch_path,
            assignment=reused_assignment,
            runs_root=runs_root,
            output=negative / "reused-analysis",
            expected_coverage="INCONCLUSIVE",
            expected_hypothesis="INCONCLUSIVE",
        )
        reused_codes = {item["code"] for item in reused["reasons"]}
        if not {"RUN_ID_REUSED", "BUNDLE_REUSED"}.issubset(reused_codes):
            raise AssertionError("copied source Run reuse was not identified")

        unsafe_payload = read_json(supported_assignment)
        unsafe_payload["assignments"][0]["bundle"] = "../private-run"
        unsafe_assignment = assignments / "unsafe.json"
        write_json(unsafe_assignment, unsafe_payload)
        code, _, unsafe_error = run_cli(
            [
                "analyze-batch",
                "--plan",
                str(sealed_batch_path),
                "--assignment",
                str(unsafe_assignment),
                "--runs-root",
                str(runs_root),
                "--output",
                str(negative / "unsafe-never-created"),
            ]
        )
        if (
            code != 2
            or unsafe_error.get("error", {}).get("code") != "RUN_ASSIGNMENT_UNSAFE_PATH"
            or (negative / "unsafe-never-created").exists()
        ):
            raise AssertionError("unsafe assignment was not rejected before output creation")

        corrupt_runs = negative / "corrupt-runs"
        shutil.copytree(runs_root, corrupt_runs)
        corrupt_report = corrupt_runs / batch["schedule"][0]["slot_id"] / "report.json"
        corrupt_report.write_bytes(corrupt_report.read_bytes() + b" ")
        code, _, corrupt_error = run_cli(
            [
                "analyze-batch",
                "--plan",
                str(sealed_batch_path),
                "--assignment",
                str(supported_assignment),
                "--runs-root",
                str(corrupt_runs),
                "--output",
                str(negative / "corrupt-source-never-created"),
            ]
        )
        if (
            code != 2
            or not corrupt_error.get("error", {}).get("code")
            or (negative / "corrupt-source-never-created").exists()
        ):
            raise AssertionError("corrupt source Bundle was not rejected before output creation")

        overwrite_code, _, overwrite_error = run_cli(
            [
                "analyze-batch",
                "--plan",
                str(sealed_batch_path),
                "--assignment",
                str(supported_assignment),
                "--runs-root",
                str(runs_root),
                "--output",
                str(analyses / "supported"),
            ]
        )
        if (
            overwrite_code != 2
            or overwrite_error.get("error", {}).get("code") != "BATCH_OUTPUT_EXISTS"
        ):
            raise AssertionError("BatchAnalysis overwrite was not rejected")

        corrupt_analysis = negative / "corrupt-analysis"
        shutil.copytree(analyses / "supported", corrupt_analysis)
        corrupt_analysis_file = corrupt_analysis / "batch-analysis.json"
        corrupt_analysis_file.write_bytes(corrupt_analysis_file.read_bytes() + b" ")
        manifest = read_json(corrupt_analysis / "batch-analysis-manifest.json")
        analysis_entry = next(
            item for item in manifest["files"] if item["path"] == "batch-analysis.json"
        )
        if (
            corrupt_analysis_file.stat().st_size == analysis_entry["size"]
            or sha256_file(corrupt_analysis_file) == analysis_entry["sha256"]
        ):
            raise AssertionError("corrupt BatchAnalysis did not break its Manifest")

        catalog = build_catalog(analyses / "supported", output / "analysis-only-catalog")
        if catalog.run_count != 0:
            raise AssertionError("Catalog misclassified BatchAnalysis as a Run Bundle")
        summary["negative_controls"] = {
            "unsafe_assignment": "REJECTED",
            "corrupt_source_bundle": "REJECTED",
            "output_overwrite": "REJECTED",
            "source_run_reuse": sorted(reused_codes),
            "corrupt_analysis_manifest": "MISMATCH_DETECTED",
            "analysis_only_catalog_run_count": catalog.run_count,
        }
        summary["checks"].append("negative-boundaries-and-catalog-isolation")

        summary["analyses"] = {
            "supported": {
                "analysis_id": supported["analysis_id"],
                "coverage_status": supported["coverage_status"],
                "hypothesis_status": supported["hypothesis_status"],
                "source_fail_count": sum(
                    slot["source"]["verdict"] == "FAIL" for slot in supported["slots"]
                ),
                "files": file_hashes(analyses / "supported"),
            },
            "contradicted": {
                "analysis_id": contradicted["analysis_id"],
                "coverage_status": contradicted["coverage_status"],
                "hypothesis_status": contradicted["hypothesis_status"],
            },
            "incomplete": {
                "analysis_id": incomplete["analysis_id"],
                "coverage_status": incomplete["coverage_status"],
                "hypothesis_status": incomplete["hypothesis_status"],
            },
            "inconclusive": {
                "analysis_id": wrong_order["analysis_id"],
                "coverage_status": wrong_order["coverage_status"],
                "hypothesis_status": wrong_order["hypothesis_status"],
                "reason_codes": [item["code"] for item in wrong_order["reasons"]],
            },
        }
        if staging_directories(output):
            raise AssertionError("M8 acceptance left a staging directory")
        if not port_is_free(args.port):
            raise AssertionError("M8 acceptance left the loopback port occupied")
        summary["checks"].append("cleanup-port-and-staging-clean")
        summary["execution_status"] = "COMPLETED"
        summary["verdict"] = "PASS"
        exit_code = 0
    except Exception as error:
        summary["execution_status"] = "ERROR"
        summary["verdict"] = "FAIL"
        summary["failure_type"] = type(error).__name__
        print(f"M8 acceptance failed: {type(error).__name__}: {error}", file=sys.stderr)
    finally:
        summary["ended_at"] = utc_now()
        summary["resources"]["available_memory_mb_after"] = available_memory_mb()
        summary["resources"]["disk_free_mb_after"] = shutil.disk_usage(
            REPOSITORY_ROOT
        ).free // (1024 * 1024)
        summary["port_released"] = port_is_free(args.port)
        summary["staging_clean"] = not staging_directories(output)
        write_json(output / "acceptance.json", summary)

    print(
        json.dumps(
            {
                "execution_status": summary["execution_status"],
                "verdict": summary["verdict"],
                "checks": len(summary["checks"]),
                "source_run_count": len(summary.get("source_runs", [])),
                "execution_mode": summary["execution_mode"],
                "runtime_overlap_claim": summary["runtime_overlap_claim"],
                "port_released": summary["port_released"],
                "staging_clean": summary["staging_clean"],
                "output": output.name,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
