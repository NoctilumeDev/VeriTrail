from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.entry_layer_e1_acceptance import (
    AcceptanceFailure,
    checksums,
    extract_skill,
    verify_release_summary,
    verify_checksum_manifest,
)


class EntryLayerE1AcceptanceTests(unittest.TestCase):
    def test_skill_extraction_rejects_parent_traversal_before_writing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-e1-zip-slip-") as raw_temp:
            root = Path(raw_temp)
            archive = root / "malicious.zip"
            destination = root / "extracted"
            escaped = root / "escaped.txt"
            with zipfile.ZipFile(archive, mode="w") as package:
                package.writestr("veritrail-authoring/SKILL.md", "---\nname: x\n---\n")
                package.writestr("../escaped.txt", "not allowed")

            with self.assertRaises(AcceptanceFailure):
                extract_skill(archive, destination)
            self.assertFalse(escaped.exists())
            self.assertEqual(list(destination.iterdir()), [])

    def test_checksum_manifest_is_sorted_by_the_explicit_release_order(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-e1-checksums-") as raw_temp:
            root = Path(raw_temp)
            first = root / "first.bin"
            second = root / "second.bin"
            first.write_bytes(b"first")
            second.write_bytes(b"second")
            lines = checksums([second, first]).splitlines()
            self.assertTrue(lines[0].endswith("  second.bin"))
            self.assertTrue(lines[1].endswith("  first.bin"))

    def test_checksum_manifest_requires_exact_order_name_and_lowercase_digest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-e1-checksum-verify-") as raw_temp:
            root = Path(raw_temp)
            first = root / "first.bin"
            second = root / "second.bin"
            manifest = root / "SHA256SUMS.txt"
            first.write_bytes(b"first")
            second.write_bytes(b"second")
            manifest.write_text(checksums([first, second]), encoding="utf-8")
            verified = verify_checksum_manifest(manifest, (first, second))
            self.assertEqual(list(verified), ["first.bin", "second.bin"])

            manifest.write_text(checksums([first, second]).upper(), encoding="utf-8")
            with self.assertRaises(AcceptanceFailure):
                verify_checksum_manifest(manifest, (first, second))

    def test_skill_extraction_rejects_symbolic_link_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-e1-zip-link-") as raw_temp:
            root = Path(raw_temp)
            archive = root / "malicious.zip"
            destination = root / "extracted"
            link = zipfile.ZipInfo("veritrail-authoring/SKILL.md")
            link.create_system = 3
            link.external_attr = 0o120777 << 16
            with zipfile.ZipFile(archive, mode="w") as package:
                package.writestr(link, "target")

            with self.assertRaises(AcceptanceFailure):
                extract_skill(archive, destination)
            self.assertEqual(list(destination.iterdir()), [])

    def test_release_summary_accepts_new_patch_in_the_same_python_series(self) -> None:
        released = {
            "state": "PASS",
            "python_matrix": [{"python": "3.10.6", "draft": "BYTE_IDENTICAL"}],
        }
        current = {
            "state": "PASS",
            "python_matrix": [{"python": "3.10.18", "draft": "BYTE_IDENTICAL"}],
        }
        verify_release_summary(released, current, "fixture")

    def test_release_summary_rejects_fact_drift_and_unknown_python_series(self) -> None:
        released = {
            "state": "PASS",
            "python_matrix": [{"python": "3.10.6", "draft": "BYTE_IDENTICAL"}],
        }
        drifted = {
            "state": "PASS",
            "python_matrix": [{"python": "3.10.18", "draft": "DIFFERENT"}],
        }
        unknown = {
            "state": "PASS",
            "python_matrix": [{"python": "3.11.9", "draft": "BYTE_IDENTICAL"}],
        }
        with self.assertRaises(AcceptanceFailure):
            verify_release_summary(released, drifted, "fixture")
        with self.assertRaises(AcceptanceFailure):
            verify_release_summary(released, unknown, "fixture")

if __name__ == "__main__":
    unittest.main()
