from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from veritrail.errors import SafetyError
from veritrail.reporting import create_bundle

from tests.support import ROOT, sealed_example_plan


class ReportingTests(unittest.TestCase):
    def test_bundle_is_consistent_redacted_and_refuses_overwrite(self) -> None:
        evidence_path = ROOT / "examples" / "minimal" / "evidence-pass.json"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "m0-pass"
            report = create_bundle(
                plan=sealed_example_plan(),
                evidence_paths=[evidence_path],
                output=output,
                run_id="m0-pass",
                execution_status="COMPLETED",
            )
            self.assertEqual("PASS", report["verdict"])
            report_json = json.loads((output / "report.json").read_text(encoding="utf-8"))
            report_markdown = (output / "report.md").read_text(encoding="utf-8")
            self.assertEqual("PASS", report_json["verdict"])
            self.assertIn("Verdict: `PASS`", report_markdown)

            evidence_file = next((output / "evidence").glob("*.json"))
            persisted = json.loads(evidence_file.read_text(encoding="utf-8"))
            self.assertEqual("[REDACTED]", persisted["metadata"]["authorization"])
            self.assertEqual(
                report_json["evidence"][0]["sha256"],
                hashlib.sha256(evidence_file.read_bytes()).hexdigest(),
            )

            bundle = json.loads((output / "bundle-manifest.json").read_text(encoding="utf-8"))
            serialized_manifest = json.dumps(bundle, ensure_ascii=False)
            self.assertNotIn("C:\\", serialized_manifest)
            self.assertNotIn("Users", serialized_manifest)
            for entry in bundle["files"]:
                target = output / Path(entry["path"])
                content = target.read_bytes()
                self.assertEqual(entry["sha256"], hashlib.sha256(content).hexdigest())
                self.assertEqual(entry["size"], len(content))

            with self.assertRaisesRegex(SafetyError, "refusing to overwrite"):
                create_bundle(
                    plan=sealed_example_plan(),
                    evidence_paths=[evidence_path],
                    output=output,
                    run_id="m0-pass-again",
                    execution_status="COMPLETED",
                )


if __name__ == "__main__":
    unittest.main()
