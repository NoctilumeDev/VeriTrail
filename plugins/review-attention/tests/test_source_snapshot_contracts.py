from __future__ import annotations

import json
import hashlib
import os
import sys
import unittest
from pathlib import Path
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.contracts import (
    SourceSnapshotSpec,
    tightened_budget_for_testing,
    validate_source_snapshot_document,
    validate_source_snapshot_spec,
)
from veritrail_review.errors import SourceSnapshotError, SourceSnapshotFailureCode
from veritrail_review.git_objects import (
    _controlled_git_environment,
    verify_git_object_bytes,
)


class SourceSnapshotContractTests(unittest.TestCase):
    def test_frozen_source_snapshot_fixture_recomputes_exactly(self) -> None:
        path = (
            REPOSITORY_ROOT
            / "tests"
            / "fixtures"
            / "review-r1-schema-0.1"
            / "valid-complete"
            / "source-snapshot.json"
        )
        raw = path.read_bytes()
        document = json.loads(raw)
        self.assertEqual(validate_source_snapshot_document(document, expected_bytes=raw), raw)
        self.assertEqual(
            document["source_snapshot_digest"],
            "3acb02f99805fd684ff68a1e0d2a2e24a22d75232564a1f52646c89e4398f747",
        )

    def test_independent_canonicalization_matches_frozen_projection(self) -> None:
        payload = {"z": [2, 1], "a": "语义"}
        expected = b'{"domain":"fixture.domain/0.1","payload":{"a":"\xe8\xaf\xad\xe4\xb9\x89","z":[2,1]}}'
        self.assertEqual(
            canonical_json_bytes({"domain": "fixture.domain/0.1", "payload": payload}),
            expected,
        )
        self.assertEqual(
            semantic_digest("fixture.domain/0.1", payload),
            "4e3efcd187ed37f4016cadcab6d5046ae21b670427524ac4401e8ac8bce761ae",
        )

    def test_spec_rejects_refs_before_repository_access(self) -> None:
        for value in ("HEAD", "main", "a" * 12, "a" * 39, "A" * 40, "a" * 40 + "^{}"):
            with self.subTest(value=value):
                with self.assertRaises(SourceSnapshotError) as raised:
                    validate_source_snapshot_spec(
                        SourceSnapshotSpec(
                            repository_id="fixture/repository",
                            commit_oid=value,
                            analysis_root={"path_kind": "REPOSITORY_ROOT"},
                        )
                    )
                self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.INVALID_REQUEST)

    def test_analysis_root_rejects_ambiguous_components(self) -> None:
        for raw in (b".", b"..", b"/pkg", b"pkg/", b"pkg//mod", b"pkg/../mod"):
            with self.subTest(raw=raw):
                with self.assertRaises(SourceSnapshotError) as raised:
                    validate_source_snapshot_spec(
                        SourceSnapshotSpec(
                            repository_id="fixture/repository",
                            commit_oid="a" * 40,
                            analysis_root={"path_kind": "GIT_PATH", "git_path_hex": raw.hex()},
                        )
                    )
                self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.INVALID_REQUEST)

    def test_budget_helper_can_only_tighten_frozen_profile(self) -> None:
        budget = tightened_budget_for_testing(max_terminal_inventory_entries=3)
        self.assertEqual(budget.max_terminal_inventory_entries, 3)
        with self.assertRaises(SourceSnapshotError):
            tightened_budget_for_testing(wall_clock_ms=30_001)
        with self.assertRaises(SourceSnapshotError):
            tightened_budget_for_testing(unknown_limit=1)

    def test_document_validator_rejects_noncanonical_semantics(self) -> None:
        path = (
            REPOSITORY_ROOT
            / "tests"
            / "fixtures"
            / "review-r1-schema-0.1"
            / "valid-complete"
            / "source-snapshot.json"
        )
        document = json.loads(path.read_bytes())
        document["inventory_digest"] = "0" * 64
        with self.assertRaises(SourceSnapshotError) as raised:
            validate_source_snapshot_document(document)
        self.assertEqual(
            raised.exception.code,
            SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT,
        )

    def test_git_object_verification_recomputes_type_size_and_oid(self) -> None:
        body = b"exact bytes\x00with binary"
        raw = b"blob " + str(len(body)).encode("ascii") + b"\x00" + body
        oid = hashlib.sha1(raw).hexdigest()
        verify_git_object_bytes(
            algorithm="SHA1",
            object_type="blob",
            oid=oid,
            declared_size=len(body),
            body=body,
        )
        mutations = (
            {"declared_size": len(body) + 1},
            {"body": body + b"x"},
            {"object_type": "commit"},
            {"oid": "0" * 40},
        )
        base = {
            "algorithm": "SHA1",
            "object_type": "blob",
            "oid": oid,
            "declared_size": len(body),
            "body": body,
        }
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                with self.assertRaises(SourceSnapshotError) as raised:
                    verify_git_object_bytes(**{**base, **mutation})
                self.assertEqual(
                    raised.exception.code,
                    SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH,
                )

    def test_git_environment_removes_inherited_object_sources(self) -> None:
        inherited = {
            "GIT_DIR": "wrong",
            "GIT_OBJECT_DIRECTORY": "wrong",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "wrong",
            "GIT_NAMESPACE": "wrong",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "url.bad.insteadOf",
            "GIT_CONFIG_VALUE_0": "https://example.invalid/",
        }
        with mock.patch.dict(os.environ, inherited, clear=False):
            controlled = _controlled_git_environment()
        for key in inherited:
            self.assertNotIn(key, controlled)
        self.assertEqual(controlled["GIT_NO_REPLACE_OBJECTS"], "1")
        self.assertEqual(controlled["GIT_NO_LAZY_FETCH"], "1")
        self.assertEqual(controlled["GIT_OPTIONAL_LOCKS"], "0")

    def test_typed_diagnostics_do_not_expose_local_paths(self) -> None:
        local_path = r"C:\Users\example\secret-repository"
        error = SourceSnapshotError(SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE)
        self.assertNotIn(local_path, str(error))
        self.assertEqual(
            str(error),
            "REPOSITORY_UNAVAILABLE: the local Git repository is unavailable",
        )


if __name__ == "__main__":
    unittest.main()
