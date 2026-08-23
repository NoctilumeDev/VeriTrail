from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from veritrail.catalog import (
    CatalogError,
    build_catalog,
    load_catalog_manifest,
    load_catalog_snapshot,
    open_catalog_snapshot_bytes,
    open_catalog_readonly,
    validate_bundle,
)
from veritrail.reporting import create_bundle

from tests.support import ROOT, sealed_example_plan


def _database_rows(database: Path, table: str) -> list[tuple[object, ...]]:
    connection = sqlite3.connect(database)
    try:
        return connection.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()
    finally:
        connection.close()


class CatalogTests(unittest.TestCase):
    def _bundle(self, root: Path, name: str, run_id: str, evidence: str = "evidence-pass.json") -> Path:
        output = root / name
        create_bundle(
            plan=sealed_example_plan(),
            evidence_paths=[ROOT / "examples" / "minimal" / evidence],
            output=output,
            run_id=run_id,
            execution_status="COMPLETED",
        )
        return output

    def test_empty_and_single_catalog_are_read_only_rebuildable_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            empty_root = base / "empty"
            empty_root.mkdir()
            empty_output = base / "empty-catalog"
            empty = build_catalog(empty_root, empty_output)
            self.assertEqual("COMPLETED", empty.status)
            self.assertEqual(0, empty.run_count)

            root = base / "bundles"
            root.mkdir()
            source = self._bundle(root, "run-a", "catalog-run-a")
            source_hashes = {
                item.relative_to(source).as_posix(): hashlib.sha256(item.read_bytes()).hexdigest()
                for item in source.rglob("*")
                if item.is_file()
            }
            output_a = base / "catalog-a"
            output_b = base / "catalog-b"
            first = build_catalog(root, output_a)
            second = build_catalog(root, output_b)
            self.assertEqual(first.catalog_id, second.catalog_id)
            self.assertEqual(first.bundle_set_sha256, second.bundle_set_sha256)
            self.assertEqual(
                hashlib.sha256((output_a / "catalog.sqlite3").read_bytes()).hexdigest(),
                hashlib.sha256((output_b / "catalog.sqlite3").read_bytes()).hexdigest(),
            )
            self.assertEqual(
                _database_rows(output_a / "catalog.sqlite3", "catalog_runs"),
                _database_rows(output_b / "catalog.sqlite3", "catalog_runs"),
            )
            self.assertEqual(
                source_hashes,
                {
                    item.relative_to(source).as_posix(): hashlib.sha256(item.read_bytes()).hexdigest()
                    for item in source.rglob("*")
                    if item.is_file()
                },
            )
            manifest = load_catalog_manifest(output_a)
            self.assertEqual(first.catalog_id, manifest["catalog_id"])
            self.assertFalse(list(output_a.glob("catalog.sqlite3-*")))

    def test_identical_duplicates_merge_and_conflicting_run_is_quarantined(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            duplicate_root = base / "duplicates"
            duplicate_root.mkdir()
            first = self._bundle(duplicate_root, "one", "same-run")
            shutil.copytree(first, duplicate_root / "two")
            duplicate_output = base / "duplicate-catalog"
            duplicate = build_catalog(duplicate_root, duplicate_output)
            self.assertEqual("COMPLETED", duplicate.status)
            self.assertEqual(1, duplicate.run_count)
            self.assertEqual(1, duplicate.duplicate_count)
            rows = _database_rows(duplicate_output / "catalog.sqlite3", "catalog_runs")
            self.assertEqual(1, rows[0][11])

            conflict_root = base / "conflicts"
            conflict_root.mkdir()
            self._bundle(conflict_root, "pass", "conflicting-run")
            self._bundle(conflict_root, "fail", "conflicting-run", "evidence-fail.json")
            conflict_output = base / "conflict-catalog"
            conflict = build_catalog(conflict_root, conflict_output)
            self.assertEqual("COMPLETED_WITH_ISSUES", conflict.status)
            self.assertEqual(0, conflict.run_count)
            self.assertEqual(1, conflict.issue_count)
            issues = _database_rows(conflict_output / "catalog.sqlite3", "catalog_issues")
            self.assertEqual("DUPLICATE_RUN_CONFLICT", issues[0][1])
            self.assertEqual("conflicting-run", issues[0][3])

    def test_corrupt_bundle_isolated_and_existing_output_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            bundle = self._bundle(root, "corrupt", "corrupt-run")
            report = bundle / "report.json"
            report.write_bytes(report.read_bytes() + b" ")
            output = base / "catalog"
            result = build_catalog(root, output)
            self.assertEqual("COMPLETED_WITH_ISSUES", result.status)
            self.assertEqual(0, result.run_count)
            issues = _database_rows(output / "catalog.sqlite3", "catalog_issues")
            self.assertEqual("BUNDLE_SIZE_MISMATCH", issues[0][1])
            with self.assertRaisesRegex(CatalogError, "拒绝覆盖"):
                build_catalog(root, output)
            self.assertFalse(list(base.glob(".veritrail-catalog-*")))

    def test_forged_report_verdict_is_rejected_even_with_recomputed_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            bundle = self._bundle(root, "forged", "forged-verdict-run")
            report_path = bundle / "report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["verdict"] = "FAIL"
            forged = json.dumps(report, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            report_path.write_bytes(forged)
            manifest_path = bundle / "bundle-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            report_entry = next(item for item in manifest["files"] if item["path"] == "report.json")
            report_entry["sha256"] = hashlib.sha256(forged).hexdigest()
            report_entry["size"] = len(forged)
            manifest_path.write_text(
                json.dumps(manifest, separators=(",", ":"), ensure_ascii=False),
                encoding="utf-8",
            )

            output = base / "catalog"
            result = build_catalog(root, output)

            self.assertEqual("COMPLETED_WITH_ISSUES", result.status)
            issues = _database_rows(output / "catalog.sqlite3", "catalog_issues")
            self.assertEqual("REPORT_DERIVATION_MISMATCH", issues[0][1])

    def test_catalog_manifest_detects_database_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            self._bundle(root, "one", "manifest-run")
            output = base / "catalog"
            build_catalog(root, output)
            database = output / "catalog.sqlite3"
            database.write_bytes(database.read_bytes() + b"changed")
            with self.assertRaisesRegex(CatalogError, "Manifest"):
                load_catalog_manifest(output)

    def test_retained_bundle_snapshot_is_unchanged_after_source_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            bundle = self._bundle(root, "one", "snapshot-run")
            validated = validate_bundle(bundle, root, retain_snapshot=True)
            original = validated.load_owned_json("report.json", label="Report")

            (bundle / "report.json").write_text('{"run_id":"replacement"}', encoding="utf-8")

            retained = validated.load_owned_json("report.json", label="Report")
            self.assertEqual("snapshot-run", retained["run_id"])
            self.assertEqual(original, retained)

    def test_database_contains_no_absolute_paths_or_evidence_bodies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            self._bundle(root, "one", "privacy-run")
            output = base / "catalog"
            build_catalog(root, output)
            database_bytes = (output / "catalog.sqlite3").read_bytes()
            self.assertNotIn(str(base).encode("utf-8"), database_bytes)
            self.assertNotIn(b"suite_passed", database_bytes)
            manifest_text = json.dumps(load_catalog_manifest(output), ensure_ascii=False)
            self.assertNotIn(str(base), manifest_text)

    def test_manifest_path_version_and_reference_failures_are_stable_issues(self) -> None:
        mutations = {
            "version": ("BUNDLE_VERSION_UNSUPPORTED", lambda value: value.update(schema_version="9.9")),
            "unsafe-path": (
                "UNSAFE_BUNDLE_PATH",
                lambda value: value["files"][0].update(path="../escape.json"),
            ),
            "duplicate-path": (
                "DUPLICATE_BUNDLE_PATH",
                lambda value: value["files"].append(dict(value["files"][0])),
            ),
            "missing-root": (
                "MISSING_BUNDLE_ROOT_FILE",
                lambda value: value.update(
                    files=[entry for entry in value["files"] if entry["path"] != "report.json"]
                ),
            ),
            "overlong-run-id": (
                "INVALID_BUNDLE_STRUCTURE",
                lambda value: value.update(run_id="r" * 65),
            ),
            "overlong-path": (
                "BUNDLE_PATH_TOO_LONG",
                lambda value: value["files"][0].update(path="p" * 1025),
            ),
            "invalid-unicode": (
                "INVALID_BUNDLE_STRUCTURE",
                lambda value: value["files"][0].update(path="evidence/\ud800.json"),
            ),
        }
        for name, (expected, mutate) in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                base = Path(directory)
                root = base / "bundles"
                root.mkdir()
                bundle = self._bundle(root, "candidate", f"invalid-{name}")
                manifest_path = bundle / "bundle-manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                mutate(manifest)
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                output = base / "catalog"
                result = build_catalog(root, output)
                self.assertEqual("COMPLETED_WITH_ISSUES", result.status)
                issues = _database_rows(output / "catalog.sqlite3", "catalog_issues")
                self.assertEqual(expected, issues[0][1])

    def test_hardlinked_bundle_file_is_quarantined(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            bundle = self._bundle(root, "candidate", "hardlink-run")
            external = base / "external-report.json"
            shutil.copy2(bundle / "report.json", external)
            (bundle / "report.json").unlink()
            try:
                (bundle / "report.json").hardlink_to(external)
            except OSError as exc:
                self.skipTest(f"hard links unavailable: {exc}")
            output = base / "catalog"
            result = build_catalog(root, output)
            self.assertEqual("COMPLETED_WITH_ISSUES", result.status)
            issues = _database_rows(output / "catalog.sqlite3", "catalog_issues")
            self.assertEqual("UNSAFE_HARDLINK", issues[0][1])

    def test_readonly_connection_rejects_writes_and_order_query_uses_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            self._bundle(root, "one", "readonly-run")
            output = base / "catalog"
            build_catalog(root, output)
            connection = open_catalog_readonly(output)
            try:
                with self.assertRaises(sqlite3.OperationalError):
                    connection.execute(
                        "INSERT INTO catalog_meta(key, value) VALUES ('write', 'denied')"
                    )
                plan = connection.execute(
                    """
                    EXPLAIN QUERY PLAN
                    SELECT catalog_run_id FROM catalog_runs
                    ORDER BY created_at DESC, run_id ASC, catalog_run_id ASC
                    LIMIT 50
                    """
                ).fetchall()
                self.assertIn("catalog_runs_order", " ".join(str(row[3]) for row in plan))
                database_list = connection.execute("PRAGMA database_list").fetchall()
                self.assertEqual("", database_list[0][2])
            finally:
                connection.close()
            self.assertFalse(list(output.glob("catalog.sqlite3-*")))

    def test_database_logical_digest_rejects_valid_schema_row_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            self._bundle(root, "one", "logical-digest-run")
            output = base / "catalog"
            build_catalog(root, output)
            database = output / "catalog.sqlite3"
            connection = sqlite3.connect(database)
            try:
                connection.execute(
                    "UPDATE catalog_runs SET source_relative = 'changed-source'"
                )
                connection.commit()
            finally:
                connection.close()
            manifest_path = output / "catalog-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["database"]["size"] = database.stat().st_size
            manifest["database"]["sha256"] = hashlib.sha256(database.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(CatalogError, "逻辑摘要"):
                open_catalog_readonly(output)

    def test_database_exact_schema_rejects_extra_view_before_queries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            self._bundle(root, "one", "schema-allowlist-run")
            output = base / "catalog"
            build_catalog(root, output)
            database = output / "catalog.sqlite3"
            connection = sqlite3.connect(database)
            try:
                connection.execute(
                    "CREATE VIEW unexpected_amplifier AS SELECT * FROM catalog_runs"
                )
                connection.commit()
            finally:
                connection.close()
            manifest_path = output / "catalog-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["database"]["size"] = database.stat().st_size
            manifest["database"]["sha256"] = hashlib.sha256(database.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            manifest, database_bytes = load_catalog_snapshot(output)
            with self.assertRaisesRegex(CatalogError, "精确允许清单"):
                open_catalog_snapshot_bytes(database_bytes, manifest=manifest)

    def test_internal_database_failure_leaves_no_output_or_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "bundles"
            root.mkdir()
            self._bundle(root, "one", "stage-cleanup-run")
            output = base / "catalog"
            with patch("veritrail.catalog._create_database", side_effect=RuntimeError("failure")):
                with self.assertRaises(RuntimeError):
                    build_catalog(root, output)
            self.assertFalse(output.exists())
            self.assertFalse(list(base.glob(".veritrail-catalog-*")))


if __name__ == "__main__":
    unittest.main()
