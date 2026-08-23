from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from veritrail.evidence import (
    ImportedEvidence,
    import_evidence_document,
    import_evidence_files,
    validate_evidence_collection_budget,
    verify_imported_evidence,
)
from veritrail.errors import ValidationError
from veritrail.privacy import redact_value

from tests.support import ROOT


class EvidenceTests(unittest.TestCase):
    def test_sensitive_fields_and_paths_are_redacted(self) -> None:
        value = {
            "authorization": "Bearer example-value",
            "nested": {
                "api_token": "synthetic-token",
                "username": "synthetic-user",
                "message": "loaded from C:\\Users\\alice\\project by alice@example.test at 192.0.2.1; password=demo",
                "headers": "Authorization: Basic ZGVtbzpkZW1v\nCookie: session_id=synthetic; theme=dark\nSet-Cookie: sid=synthetic",
                "session": "synthetic-session",
            },
        }
        redacted, count = redact_value(value)
        self.assertEqual("[REDACTED]", redacted["authorization"])
        self.assertEqual("[REDACTED]", redacted["nested"]["api_token"])
        self.assertEqual("[REDACTED]", redacted["nested"]["username"])
        self.assertIn("<USER_HOME>", redacted["nested"]["message"])
        self.assertIn("[REDACTED_EMAIL]", redacted["nested"]["message"])
        self.assertIn("[REDACTED_IP]", redacted["nested"]["message"])
        self.assertIn("password=[REDACTED]", redacted["nested"]["message"])
        self.assertIn("Authorization: [REDACTED]", redacted["nested"]["headers"])
        self.assertIn("Cookie: [REDACTED]", redacted["nested"]["headers"])
        self.assertIn("Set-Cookie: [REDACTED]", redacted["nested"]["headers"])
        self.assertEqual("[REDACTED]", redacted["nested"]["session"])
        self.assertGreaterEqual(count, 11)

    def test_duplicate_sanitized_evidence_is_imported_once(self) -> None:
        source = ROOT / "examples" / "minimal" / "evidence-pass.json"
        imported, duplicates = import_evidence_files([source, source], 1_048_576)
        self.assertEqual(1, len(imported))
        self.assertEqual([source.name], duplicates)
        self.assertEqual("[REDACTED]", imported[0].document["metadata"]["authorization"])

    def test_prefixed_and_structured_authentication_headers_are_redacted(self) -> None:
        value = {
            "X-API-Key": "opaque-one",
            "headers": [
                {"name": "Authorization", "value": "Basic opaque-two"},
                {"name": "X-Auth-Token", "values": ["opaque-three"]},
                {"name": "Content-Type", "value": "application/json"},
            ],
        }
        redacted, count = redact_value(value)
        self.assertEqual("[REDACTED]", redacted["X-API-Key"])
        self.assertEqual("[REDACTED]", redacted["headers"][0]["value"])
        self.assertEqual("[REDACTED]", redacted["headers"][1]["values"])
        self.assertEqual("application/json", redacted["headers"][2]["value"])
        self.assertEqual(3, count)

    def test_conflicting_header_aliases_cannot_hide_sensitive_values(self) -> None:
        sensitive = {
            "name": "Content-Type",
            "header-name": "Authorization",
            "value": "opaque-secret",
        }
        ordinary = {
            "name": "Content-Type",
            "header-name": "X-Trace-Id",
            "value": "trace-123",
        }

        redacted_sensitive, sensitive_count = redact_value(sensitive)
        redacted_ordinary, ordinary_count = redact_value(ordinary)

        self.assertEqual("[REDACTED]", redacted_sensitive["value"])
        self.assertEqual(1, sensitive_count)
        self.assertEqual("trace-123", redacted_ordinary["value"])
        self.assertEqual(0, ordinary_count)

    def test_artifact_limit_is_enforced_before_json_parse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.json"
            path.write_text(json.dumps({"value": "x" * 100}), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "limit is 10 bytes"):
                import_evidence_files([path], 10)

    def test_input_count_is_rejected_before_any_file_read(self) -> None:
        nonexistent = Path("does-not-exist.json")
        with self.assertRaisesRegex(ValidationError, "component limit"):
            import_evidence_files([nonexistent] * 251, 1024)

    def test_aggregate_evidence_size_has_an_immutable_ceiling(self) -> None:
        oversized = ImportedEvidence(
            document={},
            sha256="0" * 64,
            size=64 * 1024 * 1024 + 1,
            redacted_fields=0,
            input_name="oversized.json",
        )
        with self.assertRaisesRegex(ValidationError, "retained-byte limit"):
            validate_evidence_collection_budget([oversized])

    def test_imported_evidence_mutation_is_detected(self) -> None:
        document = {
            "schema_version": "0.1",
            "evidence_type": "automated.test-summary",
            "source": "mutation-test",
            "captured_at": "2026-08-09T00:00:00Z",
            "facts": {"passed": True},
        }
        artifact = import_evidence_document(document, "mutation-test.json")
        artifact.document["facts"]["passed"] = False
        with self.assertRaisesRegex(ValidationError, "changed after hashing"):
            verify_imported_evidence(artifact)


if __name__ == "__main__":
    unittest.main()
