from __future__ import annotations

import json
import os
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from veritrail.evidence import import_evidence_document
from veritrail.errors import ValidationError
from veritrail.plan import seal_plan
from veritrail.resources import (
    assess_preflight,
    collect_preflight_evidence,
    environment_summary,
    probe_loopback_ports,
    staging_residue_count,
)
from veritrail.verdict import evaluate

from tests.support import preflight_plan


def sample(memory: float = 2048, disk: float = 4096, rss: float = 20) -> dict[str, float]:
    return {
        "available_memory_mb": memory,
        "disk_free_mb": disk,
        "collector_rss_mb": rss,
    }


def assess(
    samples: list[dict[str, float]],
    *,
    ports: list[dict[str, object]] | None = None,
    residue: int = 0,
    errors: list[dict[str, str]] | None = None,
    start_rss: float = 20,
) -> dict[str, object]:
    return assess_preflight(
        policy=preflight_plan()["preflight"],
        samples=samples,
        port_checks=ports or [],
        residue_count=residue,
        collection_errors=errors or [],
        observer_start_rss_mb=start_rss,
    )


class ResourceDecisionTests(unittest.TestCase):
    def test_proceed_soft_stop_and_hard_abort_are_distinct(self) -> None:
        self.assertEqual("PROCEED", assess([sample(), sample(), sample()])["decision"])
        self.assertEqual(
            "STOP_ESCALATION",
            assess([sample(memory=400), sample(memory=400), sample(memory=400)])["decision"],
        )
        self.assertEqual(
            "ABORT",
            assess([sample(memory=200), sample(memory=200), sample(memory=600)])["decision"],
        )

    def test_non_consecutive_hard_spikes_do_not_form_a_hard_streak(self) -> None:
        result = assess([sample(memory=200), sample(memory=600), sample(memory=200)])
        self.assertEqual("STOP_ESCALATION", result["decision"])
        self.assertEqual(1, result["max_consecutive_memory_hard_breaches"])

    def test_disk_collector_port_residue_and_collection_errors_abort(self) -> None:
        cases = {
            "disk": assess([sample(disk=64)]),
            "collector": assess([sample(rss=600)]),
            "port": assess(
                [sample()],
                ports=[{"port": 43210, "expected": "FREE", "actual": "LISTENING", "matched": False}],
            ),
            "residue": assess([sample()], residue=1),
            "collection": assess(
                [sample()], errors=[{"collector": "resource_sample", "error_type": "OSError"}]
            ),
        }
        for label, result in cases.items():
            with self.subTest(case=label):
                self.assertEqual("ABORT", result["decision"])

    def test_observer_delta_stops_escalation_without_hard_abort(self) -> None:
        result = assess([sample(rss=100)], start_rss=20)
        self.assertEqual("STOP_ESCALATION", result["decision"])
        self.assertEqual(80, result["observer_effect"]["rss_delta_mb"])

    def test_loopback_probe_observes_only_the_requested_port(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            port = server.getsockname()[1]
            listening = probe_loopback_ports([{"port": port, "expected": "LISTENING"}])
            self.assertTrue(listening[0]["matched"])
        free = probe_loopback_ports([{"port": port, "expected": "FREE"}])
        self.assertTrue(free[0]["matched"])

    def test_staging_residue_is_scoped_to_output_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".veritrail-leftover").mkdir()
            (root / "ordinary-run").mkdir()
            self.assertEqual(1, staging_residue_count(root))

    def test_live_evidence_contains_booleans_not_proxy_values_or_identity(self) -> None:
        plan = preflight_plan()
        marker = "http://proxy-value.invalid:9"
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ,
            {"HTTP_PROXY": marker, "HTTPS_PROXY": marker},
            clear=False,
        ):
            document = collect_preflight_evidence(plan, Path(directory))
        serialized = json.dumps(document, ensure_ascii=False)
        self.assertNotIn(marker, serialized)
        self.assertNotIn("hostname", serialized.lower())
        self.assertNotIn("username", serialized.lower())
        self.assertTrue(document["facts"]["snapshot_complete"])
        self.assertEqual("PROCEED", document["facts"]["decision"])
        self.assertEqual(
            {"operating_system", "python_major_minor", "cpu_logical_count"},
            set(document["observed_variables"]),
        )
        artifact = import_evidence_document(document, "generated-preflight.json")
        self.assertEqual("runtime.preflight", artifact.document["evidence_type"])

    def test_environment_summary_records_only_proxy_presence(self) -> None:
        marker = "http://another-proxy-value.invalid:9"
        with patch.dict(os.environ, {"ALL_PROXY": marker}, clear=True):
            summary = environment_summary(1024)
        self.assertTrue(summary["proxy"]["all_configured"])
        self.assertNotIn(marker, json.dumps(summary))

    def test_incomplete_preflight_evidence_must_abort(self) -> None:
        plan = preflight_plan()
        with tempfile.TemporaryDirectory() as directory:
            document = collect_preflight_evidence(plan, Path(directory))
        document["facts"]["snapshot_complete"] = False
        document["facts"]["decision"] = "PROCEED"
        with self.assertRaisesRegex(ValidationError, "must ABORT"):
            import_evidence_document(document, "invalid-preflight.json")

    def test_preflight_sample_counts_must_be_internally_consistent(self) -> None:
        plan = preflight_plan()
        with tempfile.TemporaryDirectory() as directory:
            document = collect_preflight_evidence(plan, Path(directory))
        document["facts"]["sample_count_observed"] += 1
        with self.assertRaisesRegex(ValidationError, "must equal the samples length"):
            import_evidence_document(document, "invalid-count.json")

    def test_abort_status_and_policy_drift_block_causal_pass(self) -> None:
        abort_plan = seal_plan(preflight_plan("abort"))
        with tempfile.TemporaryDirectory() as directory:
            abort_document = collect_preflight_evidence(abort_plan, Path(directory))
        abort_artifact = import_evidence_document(abort_document, "abort-preflight.json")
        status_conflict = evaluate(abort_plan, [abort_artifact], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", status_conflict["verdict"])
        self.assertTrue(
            any(item["code"] == "PREFLIGHT_STATUS_CONFLICT" for item in status_conflict["contamination"])
        )

        proceed_plan = seal_plan(preflight_plan())
        with tempfile.TemporaryDirectory() as directory:
            drift_document = collect_preflight_evidence(proceed_plan, Path(directory))
        drift_document["facts"]["policy"]["available_memory_soft_min_mb"] += 1
        drift_artifact = import_evidence_document(drift_document, "drift-preflight.json")
        policy_drift = evaluate(proceed_plan, [drift_artifact], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", policy_drift["verdict"])
        self.assertTrue(
            any(item["code"] == "PREFLIGHT_POLICY_DRIFT" for item in policy_drift["contamination"])
        )


if __name__ == "__main__":
    unittest.main()
