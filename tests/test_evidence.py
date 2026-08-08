from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from veritrail.evidence import import_evidence_files
from veritrail.errors import ValidationError
from veritrail.privacy import redact_value

from tests.support import ROOT


class EvidenceTests(unittest.TestCase):
    def test_sensitive_fields_and_paths_are_redacted(self) -> None:
        value = {
            "authorization": "Bearer example-value",
            "nested": {
                "api_token": "synthetic-token",
                "message": "loaded from C:\\Users\\alice\\project by alice@example.test at 192.0.2.1; password=demo",
            },
        }
        redacted, count = redact_value(value)
        self.assertEqual("[REDACTED]", redacted["authorization"])
        self.assertEqual("[REDACTED]", redacted["nested"]["api_token"])
        self.assertIn("<USER_HOME>", redacted["nested"]["message"])
        self.assertIn("[REDACTED_EMAIL]", redacted["nested"]["message"])
        self.assertIn("[REDACTED_IP]", redacted["nested"]["message"])
        self.assertIn("password=[REDACTED]", redacted["nested"]["message"])
        self.assertGreaterEqual(count, 6)

    def test_duplicate_sanitized_evidence_is_imported_once(self) -> None:
        source = ROOT / "examples" / "minimal" / "evidence-pass.json"
        imported, duplicates = import_evidence_files([source, source], 1_048_576)
        self.assertEqual(1, len(imported))
        self.assertEqual([source.name], duplicates)
        self.assertEqual("[REDACTED]", imported[0].document["metadata"]["authorization"])

    def test_artifact_limit_is_enforced_before_json_parse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.json"
            path.write_text(json.dumps({"value": "x" * 100}), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "limit is 10 bytes"):
                import_evidence_files([path], 10)


if __name__ == "__main__":
    unittest.main()
