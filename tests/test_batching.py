from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any

from veritrail.batching import (
    BatchError,
    create_batch_analysis_bundle,
    seal_batch_plan,
    seeded_profile_order,
    validate_batch_plan,
    verify_sealed_batch_plan,
    write_sealed_batch_plan,
)
from veritrail.catalog import build_catalog
from veritrail.cli import main
from veritrail.evidence import import_evidence_document
from veritrail.orchestration import collect_orchestrated_evidence, prepare_static_target
from veritrail.plan import seal_plan
from veritrail.reporting import create_bundle
from veritrail.resources import collect_preflight_evidence

from tests.support import ROOT
from tests.test_browser_evidence import _browser_artifact
from tests.test_orchestration import _free_port, _runtime_plan


PROFILE_CELLS = [
    ("baseline", "off", "off"),
    ("queue-only", "off", "on"),
    ("cache-only", "on", "off"),
    ("combined", "on", "on"),
]


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _schedule(profile_ids: list[str], seed: int = 20260809) -> list[dict[str, Any]]:
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


class BatchTests(unittest.TestCase):
    def _create_source_fixture(
        self, root: Path
    ) -> tuple[dict[str, Any], dict[str, Path], Path]:
        runs_root = root / "runs"
        runs_root.mkdir()
        sites_root = root / "sites"
        sites_root.mkdir()
        port = _free_port()
        plans: dict[str, dict[str, Any]] = {}
        profiles: list[dict[str, Any]] = []
        console_errors = {"baseline": 0, "queue-only": 0, "cache-only": 0, "combined": 1}

        for version, (profile_id, cache, queue) in enumerate(PROFILE_CELLS, start=1):
            site = sites_root / profile_id
            site.mkdir()
            (site / "index.html").write_text(
                f"<!doctype html><title>{profile_id}</title><main>{cache}-{queue}</main>",
                encoding="utf-8",
            )
            (site / "data.json").write_text(
                json.dumps({"profile": profile_id}), encoding="utf-8"
            )
            relative = f"sites/{profile_id}"
            plan = _runtime_plan(port)
            plan["plan_id"] = "m8-batch-static-profile"
            plan["version"] = version
            plan["subject"]["version"] = f"profile-{profile_id}"
            plan["subject"]["source_ref"] = relative
            plan["target"]["root"] = relative
            primary = next(item for item in plan["variables"] if item["role"] == "PRIMARY")
            primary.update(name="batch_profile", value=profile_id, source="sealed-batch-plan")
            snapshot = prepare_static_target(plan, root)
            plan["baseline"]["fingerprint"] = snapshot.fingerprint
            plans[profile_id] = seal_plan(plan)
            profiles.append(
                {
                    "id": profile_id,
                    "cells": {"cache-mode": cache, "queue-mode": queue},
                    "plan_sha256": plans[profile_id]["seal"]["digest"],
                    "realization": {
                        "subject_version": f"profile-{profile_id}",
                        "subject_source_ref": relative,
                        "target_root": relative,
                        "static_root_fingerprint": snapshot.fingerprint,
                    },
                    "estimated_memory_mb": 128,
                }
            )

        profile_ids = [item[0] for item in PROFILE_CELLS]
        batch = {
            "schema_version": "0.1",
            "batch_id": "m8-unit-two-by-two",
            "version": 1,
            "question": "Does each preregistered Profile retain its expected browser outcome?",
            "primary_variable": {"name": "batch_profile", "source": "sealed-batch-plan"},
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
            "profiles": profiles,
            "execution_policy": {
                "order_algorithm": "SHA256_RANK_V1",
                "seed": 20260809,
                "perturbation_repetitions": 1,
                "max_parallel": 2,
                "memory_budget_mb": 256,
                "preflight_between_waves": True,
                "cleanup_between_waves": True,
            },
            "schedule": _schedule(profile_ids),
            "outcomes": [
                {
                    "assertion_id": "console-errors-zero",
                    "expected_actual": console_errors,
                }
            ],
            "limits": [
                "Profile observations do not prove component-level causality.",
                "Wave membership does not prove actual runtime overlap.",
            ],
            "reproduction_steps": ["Execute every slot exactly once in sealed order."],
            "cleanup_steps": ["Verify every source Run records complete cleanup."],
        }
        sealed_batch = seal_batch_plan(batch)

        paths: dict[str, Path] = {}
        for slot in sealed_batch["schedule"]:
            profile_id = slot["profile_id"]
            plan = plans[profile_id]
            preflight = import_evidence_document(
                collect_preflight_evidence(plan, runs_root), "preflight.json"
            )
            orchestration = collect_orchestrated_evidence(
                plan,
                root,
                browser_collector=lambda candidate, fail=bool(console_errors[profile_id]): _browser_artifact(
                    candidate, console_error=fail
                ),
            )
            output = runs_root / slot["slot_id"]
            create_bundle(
                plan=plan,
                evidence_paths=[],
                output=output,
                run_id=f"m8-{slot['slot_id']}",
                execution_status=orchestration.execution_status,
                generated_evidence=[preflight, orchestration.orchestration, orchestration.browser],
            )
            paths[slot["slot_id"]] = output
        return sealed_batch, paths, runs_root

    def _write_inputs(
        self,
        root: Path,
        batch: dict[str, Any],
        paths: dict[str, Path],
        runs_root: Path,
        *,
        omitted: set[str] | None = None,
        remap: dict[str, str] | None = None,
        name: str = "input",
    ) -> tuple[Path, Path]:
        plan_path = root / f"{name}-batch-plan.json"
        write_sealed_batch_plan(plan_path, batch)
        omitted = omitted or set()
        remap = remap or {}
        assignment = {
            "schema_version": "0.1",
            "batch_plan_sha256": batch["seal"]["digest"],
            "assignments": [
                {
                    "slot_id": slot["slot_id"],
                    "bundle": paths[remap.get(slot["slot_id"], slot["slot_id"])]
                    .relative_to(runs_root)
                    .as_posix(),
                }
                for slot in batch["schedule"]
                if slot["slot_id"] not in omitted
            ],
        }
        assignment_path = root / f"{name}-assignment.json"
        _write_json(assignment_path, assignment)
        return plan_path, assignment_path

    def test_example_plan_seals_and_rejects_matrix_schedule_and_resource_drift(self) -> None:
        example = _json(ROOT / "examples" / "batch" / "batch-plan.json")
        validate_batch_plan(example)
        sealed = seal_batch_plan(example)
        verify_sealed_batch_plan(sealed)
        self.assertEqual(
            ["combined", "baseline", "queue-only", "cache-only"],
            seeded_profile_order(
                ["baseline", "queue-only", "cache-only", "combined"], 20260809, 1
            ),
        )

        missing_cell = copy.deepcopy(example)
        missing_cell["profiles"].pop()
        with self.assertRaisesRegex(BatchError, "full-factorial"):
            validate_batch_plan(missing_cell)

        label_only = copy.deepcopy(example)
        label_only["profiles"][1]["realization"]["static_root_fingerprint"] = label_only[
            "profiles"
        ][0]["realization"]["static_root_fingerprint"]
        with self.assertRaisesRegex(BatchError, "distinct static_root_fingerprint"):
            validate_batch_plan(label_only)

        forged_order = copy.deepcopy(example)
        forged_order["schedule"][-1]["profile_id"] = "combined"
        with self.assertRaisesRegex(BatchError, "SHA256_RANK_V1"):
            validate_batch_plan(forged_order)

        over_budget = copy.deepcopy(example)
        over_budget["execution_policy"]["memory_budget_mb"] = 700
        with self.assertRaisesRegex(BatchError, "memory budget"):
            validate_batch_plan(over_budget)

        tampered = copy.deepcopy(sealed)
        tampered["question"] = "Changed after sealing."
        with self.assertRaisesRegex(BatchError, "seal"):
            verify_sealed_batch_plan(tampered)

        malformed = copy.deepcopy(example)
        malformed["schedule"][-1]["profile_id"] = []
        with self.assertRaises(BatchError):
            validate_batch_plan(malformed)

        non_finite = copy.deepcopy(example)
        non_finite["profiles"][0]["realization"]["subject_version"] = float("nan")
        with self.assertRaises(BatchError):
            validate_batch_plan(non_finite)

    def test_supported_contradicted_incomplete_cli_and_deterministic_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            batch, paths, runs_root = self._create_source_fixture(root)
            plan_path, assignment_path = self._write_inputs(
                root, batch, paths, runs_root, name="supported"
            )

            first = root / "analysis-first"
            result = create_batch_analysis_bundle(
                batch_plan_path=plan_path,
                assignment_path=assignment_path,
                runs_root=runs_root,
                output=first,
            )
            analysis = _json(first / "batch-analysis.json")
            self.assertEqual("COMPLETE", result.coverage_status)
            self.assertEqual("SUPPORTED", result.hypothesis_status)
            self.assertEqual("NOT_PROVEN", analysis["runtime_overlap_claim"])
            self.assertIn("FAIL", {slot["source"]["verdict"] for slot in analysis["slots"]})
            self.assertEqual("SUPPORTED", analysis["hypothesis_status"])

            second = root / "analysis-second"
            create_batch_analysis_bundle(
                batch_plan_path=plan_path,
                assignment_path=assignment_path,
                runs_root=runs_root,
                output=second,
            )
            first_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in first.iterdir()
            }
            second_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in second.iterdir()
            }
            self.assertEqual(first_hashes, second_hashes)

            self.assertEqual(
                ["sealed-batch-plan.json", "batch-analysis.json", "batch-analysis.md"],
                [item["path"] for item in _json(first / "batch-analysis-manifest.json")["files"]],
            )
            persisted = b"".join(path.read_bytes() for path in first.iterdir())
            self.assertNotIn(str(root).encode(), persisted)
            with self.assertRaisesRegex(BatchError, "拒绝覆盖"):
                create_batch_analysis_bundle(
                    batch_plan_path=plan_path,
                    assignment_path=assignment_path,
                    runs_root=runs_root,
                    output=first,
                )

            contradicted = copy.deepcopy(batch)
            del contradicted["seal"]
            contradicted["outcomes"][0]["expected_actual"]["combined"] = 0
            contradicted = seal_batch_plan(contradicted)
            contradicted_plan, contradicted_assignment = self._write_inputs(
                root, contradicted, paths, runs_root, name="contradicted"
            )
            contradicted_result = create_batch_analysis_bundle(
                batch_plan_path=contradicted_plan,
                assignment_path=contradicted_assignment,
                runs_root=runs_root,
                output=root / "analysis-contradicted",
            )
            self.assertEqual("COMPLETE", contradicted_result.coverage_status)
            self.assertEqual("CONTRADICTED", contradicted_result.hypothesis_status)

            incomplete_plan, incomplete_assignment = self._write_inputs(
                root,
                batch,
                paths,
                runs_root,
                omitted={batch["schedule"][-1]["slot_id"]},
                name="incomplete",
            )
            incomplete_result = create_batch_analysis_bundle(
                batch_plan_path=incomplete_plan,
                assignment_path=incomplete_assignment,
                runs_root=runs_root,
                output=root / "analysis-incomplete",
            )
            self.assertEqual("INCOMPLETE", incomplete_result.coverage_status)
            self.assertEqual("INCONCLUSIVE", incomplete_result.hypothesis_status)

            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "analyze-batch",
                        "--plan",
                        str(plan_path),
                        "--assignment",
                        str(assignment_path),
                        "--runs-root",
                        str(runs_root),
                        "--output",
                        str(root / "analysis-cli"),
                    ]
                )
            payload = json.loads(stdout.getvalue())
            self.assertEqual(0, code)
            self.assertEqual("SUPPORTED", payload["hypothesis_status"])

            catalog = build_catalog(root / "analysis-first", root / "analysis-catalog")
            self.assertEqual(0, catalog.run_count)

    def test_markdown_escapes_batch_plan_control_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            batch, paths, runs_root = self._create_source_fixture(root)
            draft = copy.deepcopy(batch)
            draft.pop("seal")
            draft["limits"] = ["<svg onload=alert(1)>\n[unsafe](javascript:alert(1))"]
            sealed = seal_batch_plan(draft)
            plan_path, assignment_path = self._write_inputs(
                root, sealed, paths, runs_root, name="escaped"
            )

            output = root / "escaped-analysis"
            create_batch_analysis_bundle(
                batch_plan_path=plan_path,
                assignment_path=assignment_path,
                runs_root=runs_root,
                output=output,
            )
            markdown = (output / "batch-analysis.md").read_text(encoding="utf-8")

            self.assertNotIn("<svg", markdown)
            self.assertNotIn("[unsafe](javascript:", markdown)
            self.assertIn("&lt;svg", markdown)

    def test_wrong_wave_order_is_inconclusive_and_assignment_errors_are_sanitized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            batch, paths, runs_root = self._create_source_fixture(root)
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
            plan_path, assignment_path = self._write_inputs(
                root,
                batch,
                paths,
                runs_root,
                remap={
                    coverage_baseline: perturbation_baseline,
                    perturbation_baseline: coverage_baseline,
                },
                name="wrong-order",
            )
            result = create_batch_analysis_bundle(
                batch_plan_path=plan_path,
                assignment_path=assignment_path,
                runs_root=runs_root,
                output=root / "wrong-order-analysis",
            )
            self.assertEqual("INCONCLUSIVE", result.coverage_status)
            codes = {
                item["code"]
                for item in _json(root / "wrong-order-analysis" / "batch-analysis.json")[
                    "reasons"
                ]
            }
            self.assertIn("WAVE_ORDER_MISMATCH", codes)

            reused_copy = runs_root / "reused-copy"
            shutil.copytree(paths[coverage_baseline], reused_copy)
            paths["reused-copy"] = reused_copy
            reused_plan, reused_assignment = self._write_inputs(
                root,
                batch,
                paths,
                runs_root,
                remap={perturbation_baseline: "reused-copy"},
                name="reused",
            )
            reused_result = create_batch_analysis_bundle(
                batch_plan_path=reused_plan,
                assignment_path=reused_assignment,
                runs_root=runs_root,
                output=root / "reused-analysis",
            )
            reused_codes = {
                item["code"]
                for item in _json(root / "reused-analysis" / "batch-analysis.json")["reasons"]
            }
            self.assertEqual("INCONCLUSIVE", reused_result.coverage_status)
            self.assertIn("RUN_ID_REUSED", reused_codes)
            self.assertIn("BUNDLE_REUSED", reused_codes)

            fingerprint_drift = copy.deepcopy(batch)
            del fingerprint_drift["seal"]
            fingerprint_drift["profiles"][0]["realization"][
                "static_root_fingerprint"
            ] = "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
            fingerprint_drift = seal_batch_plan(fingerprint_drift)
            drift_plan, drift_assignment = self._write_inputs(
                root,
                fingerprint_drift,
                paths,
                runs_root,
                name="fingerprint-drift",
            )
            drift_result = create_batch_analysis_bundle(
                batch_plan_path=drift_plan,
                assignment_path=drift_assignment,
                runs_root=runs_root,
                output=root / "fingerprint-drift-analysis",
            )
            drift_codes = {
                item["code"]
                for item in _json(
                    root / "fingerprint-drift-analysis" / "batch-analysis.json"
                )["reasons"]
            }
            self.assertEqual("INCONCLUSIVE", drift_result.coverage_status)
            self.assertIn("PROFILE_REALIZATION_MISMATCH", drift_codes)
            self.assertIn("STATIC_ROOT_FINGERPRINT_MISMATCH", drift_codes)

            intermittent_plan_source = _json(
                paths[perturbation_baseline] / "sealed-plan.json"
            )
            intermittent_preflight = import_evidence_document(
                collect_preflight_evidence(intermittent_plan_source, runs_root),
                "intermittent-preflight.json",
            )
            intermittent_orchestration = collect_orchestrated_evidence(
                intermittent_plan_source,
                root,
                browser_collector=lambda candidate: _browser_artifact(
                    candidate, console_error=True
                ),
            )
            intermittent_path = runs_root / "intermittent-baseline"
            create_bundle(
                plan=intermittent_plan_source,
                evidence_paths=[],
                output=intermittent_path,
                run_id="m8-intermittent-baseline",
                execution_status=intermittent_orchestration.execution_status,
                generated_evidence=[
                    intermittent_preflight,
                    intermittent_orchestration.orchestration,
                    intermittent_orchestration.browser,
                ],
            )
            paths["intermittent-baseline"] = intermittent_path
            intermittent_plan, intermittent_assignment = self._write_inputs(
                root,
                batch,
                paths,
                runs_root,
                remap={perturbation_baseline: "intermittent-baseline"},
                name="intermittent",
            )
            intermittent_result = create_batch_analysis_bundle(
                batch_plan_path=intermittent_plan,
                assignment_path=intermittent_assignment,
                runs_root=runs_root,
                output=root / "intermittent-analysis",
            )
            intermittent_codes = {
                item["code"]
                for item in _json(
                    root / "intermittent-analysis" / "batch-analysis.json"
                )["reasons"]
            }
            self.assertEqual("INCONCLUSIVE", intermittent_result.coverage_status)
            self.assertEqual("INCONCLUSIVE", intermittent_result.hypothesis_status)
            self.assertIn("PERTURBATION_OUTCOME_DRIFT", intermittent_codes)

            unsafe = _json(assignment_path)
            unsafe["assignments"][0]["bundle"] = "../private-run"
            unsafe_path = root / "unsafe-assignment.json"
            _write_json(unsafe_path, unsafe)
            stderr = StringIO()
            with redirect_stderr(stderr):
                code = main(
                    [
                        "analyze-batch",
                        "--plan",
                        str(plan_path),
                        "--assignment",
                        str(unsafe_path),
                        "--runs-root",
                        str(runs_root),
                        "--output",
                        str(root / "never-created"),
                    ]
                )
            error = json.loads(stderr.getvalue())["error"]
            self.assertEqual(2, code)
            self.assertEqual("RUN_ASSIGNMENT_UNSAFE_PATH", error["code"])
            self.assertNotIn(str(root), stderr.getvalue())

            damaged_root = root / "damaged-runs"
            shutil.copytree(runs_root, damaged_root)
            damaged = damaged_root / batch["schedule"][0]["slot_id"] / "report.json"
            damaged.write_bytes(damaged.read_bytes() + b" ")
            _, damaged_assignment = self._write_inputs(
                root, batch, paths, runs_root, name="damaged"
            )
            damaged_payload = _json(damaged_assignment)
            for item in damaged_payload["assignments"]:
                item["bundle"] = item["bundle"]
            _write_json(damaged_assignment, damaged_payload)
            with self.assertRaises(BatchError):
                create_batch_analysis_bundle(
                    batch_plan_path=plan_path,
                    assignment_path=damaged_assignment,
                    runs_root=damaged_root,
                    output=root / "damaged-analysis",
                )
            self.assertFalse(list(root.glob(".veritrail-batch-*")))

    def test_seal_batch_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sealed.json"
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "seal-batch",
                        "--plan",
                        str(ROOT / "examples" / "batch" / "batch-plan.json"),
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(0, code)
            self.assertEqual("seal-batch", json.loads(stdout.getvalue())["command"])
            verify_sealed_batch_plan(_json(output))


if __name__ == "__main__":
    unittest.main()
