from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (
    corrupt_loose_object,
    create_fixture_repository,
    git_executable,
    object_body,
    write_commit,
    write_tree,
)
from veritrail_review import (
    SourceSnapshotError,
    SourceSnapshotFailureCode,
    SourceSnapshotRequest,
    SourceSnapshotRuntime,
    SourceSnapshotSpec,
    create_source_snapshot,
)
from veritrail_review.contracts import (
    DEFAULT_ACQUISITION_BUDGET,
    tightened_budget_for_testing,
)
from veritrail_review.publisher import publish_source_snapshot
from veritrail_review.source_snapshot import _create_source_snapshot


class _FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value


class SourceSnapshotRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        if os.name != "nt":
            self.skipTest("the frozen 0.1 publication baseline is Windows 11")
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name)
        self.runtime = SourceSnapshotRuntime(git_executable=git_executable())

    def tearDown(self) -> None:
        self._temp.cleanup()

    def request(
        self,
        fixture,
        output_name: str,
        *,
        analysis_root: dict[str, str] | None = None,
        commit_oid: str | None = None,
    ) -> SourceSnapshotRequest:
        return SourceSnapshotRequest(
            spec=SourceSnapshotSpec(
                repository_id="fixture/repository",
                commit_oid=commit_oid or fixture.commit_oid,
                analysis_root=analysis_root or {"path_kind": "REPOSITORY_ROOT"},
            ),
            repository_path=fixture.path,
            output_directory=self.root / output_name,
        )

    def create_with_budget(self, request, budget, *, clock=None, stage_hook=None):
        return _create_source_snapshot(
            request,
            runtime=self.runtime,
            budget=budget,
            clock=clock or __import__("time").monotonic,
            stage_hook=stage_hook,
        )

    def test_sha1_root_snapshot_preserves_terminal_modes_and_raw_paths(self) -> None:
        fixture = create_fixture_repository(self.root)
        result = create_source_snapshot(self.request(fixture, "sha1-root"), runtime=self.runtime)
        document = result.snapshot.document_copy()
        self.assertEqual(document["source_coordinate"]["commit_oid"]["algorithm"], "SHA1")
        self.assertEqual(len(document["inventory"]), fixture.terminal_count)
        self.assertEqual([item["git_path"]["git_path_hex"] for item in document["inventory"]], sorted(item["git_path"]["git_path_hex"] for item in document["inventory"]))
        by_path = {
            bytes.fromhex(item["git_path"]["git_path_hex"]): item
            for item in document["inventory"]
        }
        self.assertEqual(by_path[b"pkg/run.py"]["entry_kind"], "EXECUTABLE_BLOB")
        self.assertEqual(by_path[b"pkg/link"]["entry_kind"], "SYMLINK_BLOB")
        self.assertEqual(by_path[b"pkg/link"]["content"]["size_bytes"], len(b"target.bin"))
        self.assertEqual(by_path[b"pkg/submodule"]["entry_kind"], "GITLINK")
        self.assertNotIn("content", by_path[b"pkg/submodule"])
        self.assertEqual(by_path[b"pkg/odd.bin"]["entry_kind"], "OTHER_TRACKED_ENTRY")
        self.assertIn(b"pkg/\xff.py", by_path)
        self.assertEqual([path.name for path in result.artifact_path.parent.iterdir()], ["source-snapshot.json"])
        self.assertTrue(result.artifact_path.read_bytes().endswith(b"\n"))
        self.assertFalse(result.artifact_path.read_bytes().endswith(b"\n\n"))
        self.assertFalse((result.artifact_path.parent / "manifest.json").exists())

    def test_non_root_analysis_uses_repository_relative_inventory_paths(self) -> None:
        fixture = create_fixture_repository(self.root)
        root = {"path_kind": "GIT_PATH", "git_path_hex": b"pkg".hex()}
        result = create_source_snapshot(
            self.request(fixture, "analysis-root", analysis_root=root),
            runtime=self.runtime,
        )
        document = result.snapshot.document_copy()
        self.assertEqual(
            document["source_coordinate"]["analysis_tree_oid"]["hex"],
            fixture.analysis_tree_oid,
        )
        self.assertTrue(
            all(
                bytes.fromhex(item["git_path"]["git_path_hex"]).startswith(
                    b"pkg/"
                )
                for item in document["inventory"]
            )
        )

    def test_non_utf8_analysis_root_is_resolved_as_raw_git_bytes(self) -> None:
        fixture = create_fixture_repository(self.root)
        raw_root = b"\xfe"
        root_tree = write_tree(
            fixture.path,
            fixture.algorithm,
            [(b"40000", raw_root, fixture.analysis_tree_oid)],
        )
        commit = write_commit(
            fixture.path, fixture.algorithm, root_tree, b"raw-root"
        )
        analysis_root = {
            "path_kind": "GIT_PATH",
            "git_path_hex": raw_root.hex(),
        }
        result = create_source_snapshot(
            self.request(
                fixture,
                "raw-analysis-root",
                analysis_root=analysis_root,
                commit_oid=commit,
            ),
            runtime=self.runtime,
        )
        document = result.snapshot.document_copy()
        self.assertEqual(
            document["source_coordinate"]["analysis_root"], analysis_root
        )
        self.assertTrue(
            all(
                bytes.fromhex(item["git_path"]["git_path_hex"]).startswith(
                    raw_root + b"/"
                )
                for item in document["inventory"]
            )
        )
        self.assertEqual(
            result.runtime_provenance.acquisition_profile_id,
            "snapshot-acquisition/windows-reference/0.1",
        )
        self.assertEqual(result.runtime_provenance.os_name, "Windows")
        for forbidden in (
            "acquisition_profile_id",
            "git_executable",
            "git_version",
            "python_version",
            "os_name",
        ):
            self.assertNotIn(forbidden, document)

    def test_sha256_repository_uses_sha256_oids(self) -> None:
        try:
            fixture = create_fixture_repository(self.root, algorithm="sha256")
        except subprocess.CalledProcessError as exc:  # type: ignore[name-defined]
            self.skipTest(f"installed Git does not support SHA-256 fixtures: {exc.returncode}")
        result = create_source_snapshot(self.request(fixture, "sha256"), runtime=self.runtime)
        document = result.snapshot.document_copy()
        self.assertEqual(document["source_coordinate"]["commit_oid"]["algorithm"], "SHA256")
        self.assertTrue(all(len(item["git_object"]["hex"]) == 64 for item in document["inventory"]))

    def test_replace_ref_does_not_change_requested_commit(self) -> None:
        fixture = create_fixture_repository(self.root, second_commit=True)
        result = create_source_snapshot(self.request(fixture, "replace"), runtime=self.runtime)
        document = result.snapshot.document_copy()
        self.assertEqual(document["source_coordinate"]["commit_oid"]["hex"], fixture.commit_oid)
        self.assertEqual(document["source_coordinate"]["commit_tree_oid"]["hex"], fixture.root_tree_oid)

    def test_worktree_index_and_untracked_noise_do_not_change_snapshot_bytes(
        self,
    ) -> None:
        fixture = create_fixture_repository(self.root)
        first = create_source_snapshot(self.request(fixture, "before-dirty"), runtime=self.runtime)

        tracked_path = fixture.path / "pkg" / "regular.py"
        tracked_path.parent.mkdir(parents=True)
        tracked_path.write_text("working-tree-only\n", encoding="utf-8")
        (fixture.path / "untracked.py").write_text("changed", encoding="utf-8")

        subprocess.run(
            [
                os.fspath(self.runtime.git_executable),
                "-C",
                os.fspath(fixture.path),
                "update-index",
                "--add",
                "--cacheinfo",
                f"100644,{fixture.blob_oids[0]},index-only.py",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        second = create_source_snapshot(self.request(fixture, "after-dirty"), runtime=self.runtime)
        self.assertEqual(first.snapshot.canonical_bytes, second.snapshot.canonical_bytes)

    def test_missing_object_fails_without_output(self) -> None:
        fixture = create_fixture_repository(self.root)
        request = self.request(fixture, "missing", commit_oid="f" * 40)
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(request, runtime=self.runtime)
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.SOURCE_OBJECT_MISSING)
        self.assertFalse(request.output_directory.exists())

    def test_invalid_ref_is_rejected_before_repository_or_output_access(self) -> None:
        request = SourceSnapshotRequest(
            spec=SourceSnapshotSpec(
                repository_id="fixture/repository",
                commit_oid="HEAD",
                analysis_root={"path_kind": "REPOSITORY_ROOT"},
            ),
            repository_path=self.root / "missing-repository",
            output_directory=self.root / "invalid-ref-output",
        )
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(request, runtime=self.runtime)
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.INVALID_REQUEST)
        self.assertFalse(request.output_directory.exists())

    def test_invalid_nested_spec_is_a_typed_request_failure(self) -> None:
        output = self.root / "invalid-spec-output"
        request = SourceSnapshotRequest(
            spec=object(),  # type: ignore[arg-type]
            repository_path=self.root / "missing-repository",
            output_directory=output,
        )
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(request, runtime=self.runtime)
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.INVALID_REQUEST)
        self.assertFalse(output.exists())

    def test_missing_and_non_tree_analysis_roots_fail_closed(self) -> None:
        fixture = create_fixture_repository(self.root)
        roots = (
            b"missing",
            b"pkg/regular.py",
        )
        for index, raw in enumerate(roots):
            with self.subTest(raw=raw):
                request = self.request(
                    fixture,
                    f"invalid-root-{index}",
                    analysis_root={"path_kind": "GIT_PATH", "git_path_hex": raw.hex()},
                )
                with self.assertRaises(SourceSnapshotError) as raised:
                    create_source_snapshot(request, runtime=self.runtime)
                self.assertEqual(
                    raised.exception.code,
                    SourceSnapshotFailureCode.ANALYSIS_ROOT_NOT_TREE,
                )
                self.assertFalse(request.output_directory.exists())

    def test_repository_local_executable_cannot_select_the_toolchain(self) -> None:
        fixture = create_fixture_repository(self.root)
        fake_git = fixture.path / "git.exe"
        fake_git.write_bytes(b"not executable")
        request = self.request(fixture, "local-toolchain")
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(
                request,
                runtime=SourceSnapshotRuntime(git_executable=fake_git.resolve()),
            )
        self.assertEqual(
            raised.exception.code,
            SourceSnapshotFailureCode.REPOSITORY_UNAVAILABLE,
        )
        self.assertFalse(request.output_directory.exists())

    def test_malformed_tree_and_known_mode_type_mismatch_are_rejected(self) -> None:
        malformed = create_fixture_repository(self.root / "malformed-base")
        blob_oid = malformed.blob_oids[0]
        duplicate_tree = write_tree(
            malformed.path,
            malformed.algorithm,
            [(b"100644", b"same", blob_oid), (b"100644", b"same", blob_oid)],
        )
        malformed_commit = write_commit(
            malformed.path, malformed.algorithm, duplicate_tree, b"duplicate"
        )
        malformed_request = self.request(
            malformed, "malformed-tree", commit_oid=malformed_commit
        )
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(malformed_request, runtime=self.runtime)
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.MALFORMED_TREE)
        self.assertFalse(malformed_request.output_directory.exists())

        mismatch = create_fixture_repository(self.root / "mismatch-base")
        wrong_tree = write_tree(
            mismatch.path,
            mismatch.algorithm,
            [(b"100644", b"not-a-blob", mismatch.analysis_tree_oid)],
        )
        wrong_commit = write_commit(
            mismatch.path, mismatch.algorithm, wrong_tree, b"type-mismatch"
        )
        mismatch_request = self.request(
            mismatch, "type-mismatch", commit_oid=wrong_commit
        )
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(mismatch_request, runtime=self.runtime)
        self.assertEqual(
            raised.exception.code,
            SourceSnapshotFailureCode.SOURCE_OBJECT_TYPE_MISMATCH,
        )
        self.assertFalse(mismatch_request.output_directory.exists())

    def test_corrupted_loose_object_fails_closed(self) -> None:
        fixture = create_fixture_repository(self.root)
        corrupt_loose_object(fixture.path, fixture.blob_oids[0])
        request = self.request(fixture, "corrupt-object")
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(request, runtime=self.runtime)
        self.assertIn(
            raised.exception.code,
            {
                SourceSnapshotFailureCode.SOURCE_OBJECT_MISSING,
                SourceSnapshotFailureCode.SOURCE_CONTENT_MISMATCH,
            },
        )
        self.assertFalse(request.output_directory.exists())

    def test_different_sufficient_budgets_produce_identical_bytes(self) -> None:
        fixture = create_fixture_repository(self.root)
        first = self.create_with_budget(
            self.request(fixture, "budget-one"),
            tightened_budget_for_testing(wall_clock_ms=25_000),
        )
        second = self.create_with_budget(
            self.request(fixture, "budget-two"),
            tightened_budget_for_testing(wall_clock_ms=29_000),
        )
        self.assertEqual(first.snapshot.canonical_bytes, second.snapshot.canonical_bytes)

    def test_terminal_count_limit_is_inclusive_and_one_less_fails_closed(self) -> None:
        fixture = create_fixture_repository(self.root)
        exact = tightened_budget_for_testing(max_terminal_inventory_entries=fixture.terminal_count)
        self.create_with_budget(self.request(fixture, "exact-count"), exact)
        too_small = tightened_budget_for_testing(max_terminal_inventory_entries=fixture.terminal_count - 1)
        failed_request = self.request(fixture, "too-small")
        with self.assertRaises(SourceSnapshotError) as raised:
            self.create_with_budget(failed_request, too_small)
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED)
        self.assertFalse(failed_request.output_directory.exists())

    def test_byte_and_object_limits_are_inclusive(self) -> None:
        fixture = create_fixture_repository(self.root)
        tree_sizes = [
            len(object_body(fixture.path, oid))
            for oid in (
                fixture.root_tree_oid,
                fixture.analysis_tree_oid,
                self._nested_tree_oid(fixture),
            )
        ]
        blob_sizes = [len(object_body(fixture.path, oid)) for oid in fixture.blob_oids]
        exact = tightened_budget_for_testing(
            max_commit_bytes=len(object_body(fixture.path, fixture.commit_oid)),
            max_tree_depth=2,
            max_unique_tree_objects=3,
            max_expanded_tree_entries=9,
            max_single_tree_bytes=max(tree_sizes),
            max_total_unique_tree_bytes=sum(tree_sizes),
            max_terminal_inventory_entries=fixture.terminal_count,
            max_single_blob_bytes=max(blob_sizes),
            max_total_unique_blob_bytes=sum(blob_sizes),
        )
        complete = self.create_with_budget(self.request(fixture, "all-exact"), exact)
        canonical_size = len(complete.snapshot.canonical_bytes)
        canonical_exact = tightened_budget_for_testing(
            max_canonical_artifact_bytes=canonical_size
        )
        self.create_with_budget(
            self.request(fixture, "canonical-exact"), canonical_exact
        )
        failed_request = self.request(fixture, "canonical-too-small")
        with self.assertRaises(SourceSnapshotError) as raised:
            self.create_with_budget(
                failed_request,
                tightened_budget_for_testing(
                    max_canonical_artifact_bytes=canonical_size - 1
                ),
            )
        self.assertEqual(
            raised.exception.code,
            SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED,
        )
        self.assertFalse(failed_request.output_directory.exists())

        depth_request = self.request(fixture, "depth-too-small")
        with self.assertRaises(SourceSnapshotError) as raised:
            self.create_with_budget(
                depth_request,
                tightened_budget_for_testing(max_tree_depth=1),
            )
        self.assertEqual(
            raised.exception.code,
            SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED,
        )
        self.assertFalse(depth_request.output_directory.exists())

    def test_one_absolute_deadline_is_not_refreshed_between_stages(self) -> None:
        fixture = create_fixture_repository(self.root)
        clock = _FakeClock()

        def advance(stage: str) -> None:
            if stage == "commit-verified":
                clock.value = 0.031

        request = self.request(fixture, "deadline")
        with self.assertRaises(SourceSnapshotError) as raised:
            self.create_with_budget(
                request,
                tightened_budget_for_testing(wall_clock_ms=30),
                clock=clock,
                stage_hook=advance,
            )
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED)
        self.assertFalse(request.output_directory.exists())

    def test_deadline_exhaustion_at_later_stages_never_publishes(self) -> None:
        fixture = create_fixture_repository(self.root)
        stages = (
            "tree-header",
            "blob-header",
            "canonicalization-start",
            "producer-validation",
            "publication-write",
            "publication-commit",
        )
        for index, target_stage in enumerate(stages):
            with self.subTest(stage=target_stage):
                clock = _FakeClock()

                def advance(stage: str, *, target=target_stage) -> None:
                    if stage == target:
                        clock.value = 0.101

                request = self.request(fixture, f"deadline-stage-{index}")
                with self.assertRaises(SourceSnapshotError) as raised:
                    self.create_with_budget(
                        request,
                        tightened_budget_for_testing(wall_clock_ms=100),
                        clock=clock,
                        stage_hook=advance,
                    )
                self.assertEqual(
                    raised.exception.code,
                    SourceSnapshotFailureCode.SAFETY_BUDGET_EXHAUSTED,
                )
                self.assertFalse(request.output_directory.exists())
                self.assertEqual(
                    list(self.root.glob(f".{request.output_directory.name}.*.staging")),
                    [],
                )

    def test_preexisting_output_is_never_overwritten(self) -> None:
        fixture = create_fixture_repository(self.root)
        output = self.root / "existing"
        output.mkdir()
        marker = output / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(self.request(fixture, "existing"), runtime=self.runtime)
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.OUTPUT_ALREADY_EXISTS)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_preexisting_output_is_rejected_before_repository_access(self) -> None:
        output = self.root / "existing-before-repository"
        output.mkdir()
        request = SourceSnapshotRequest(
            spec=SourceSnapshotSpec(
                repository_id="fixture/repository",
                commit_oid="a" * 40,
                analysis_root={"path_kind": "REPOSITORY_ROOT"},
            ),
            repository_path=self.root / "missing-repository",
            output_directory=output,
        )
        with self.assertRaises(SourceSnapshotError) as raised:
            create_source_snapshot(request, runtime=self.runtime)
        self.assertEqual(
            raised.exception.code,
            SourceSnapshotFailureCode.OUTPUT_ALREADY_EXISTS,
        )

    def test_two_publishers_have_one_complete_winner(self) -> None:
        fixture = create_fixture_repository(self.root)
        source = create_source_snapshot(self.request(fixture, "source"), runtime=self.runtime)
        target = self.root / "race"
        outcomes: list[str] = []
        barrier = threading.Barrier(2)

        def publish() -> None:
            barrier.wait()
            try:
                publish_source_snapshot(
                    target,
                    source.snapshot,
                    deadline_check=lambda _stage: None,
                    max_canonical_bytes=DEFAULT_ACQUISITION_BUDGET.max_canonical_artifact_bytes,
                )
                outcomes.append("SUCCESS")
            except SourceSnapshotError as exc:
                outcomes.append(exc.code.value)

        threads = [threading.Thread(target=publish) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        self.assertEqual(sorted(outcomes), ["OUTPUT_ALREADY_EXISTS", "SUCCESS"])
        self.assertEqual((target / "source-snapshot.json").read_bytes(), source.snapshot.canonical_bytes)

    def test_publication_failure_cleans_staging_and_leaves_no_output(self) -> None:
        fixture = create_fixture_repository(self.root)
        source = create_source_snapshot(self.request(fixture, "source-failure"), runtime=self.runtime)
        target = self.root / "publication-failure"
        with mock.patch("veritrail_review.publisher.os.rename", side_effect=OSError("fixture")):
            with self.assertRaises(SourceSnapshotError) as raised:
                publish_source_snapshot(
                    target,
                    source.snapshot,
                    deadline_check=lambda _stage: None,
                    max_canonical_bytes=DEFAULT_ACQUISITION_BUDGET.max_canonical_artifact_bytes,
                )
        self.assertEqual(raised.exception.code, SourceSnapshotFailureCode.OUTPUT_PUBLICATION_FAILED)
        self.assertFalse(target.exists())
        self.assertEqual(list(self.root.glob(f".{target.name}.*.staging")), [])

    def test_validation_failure_never_reaches_publication(self) -> None:
        fixture = create_fixture_repository(self.root)
        request = self.request(fixture, "validation-failure")
        failure = SourceSnapshotError(
            SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT
        )
        with mock.patch(
            "veritrail_review.source_snapshot.validate_source_snapshot_document",
            side_effect=failure,
        ):
            with self.assertRaises(SourceSnapshotError) as raised:
                create_source_snapshot(request, runtime=self.runtime)
        self.assertEqual(
            raised.exception.code,
            SourceSnapshotFailureCode.NONCONFORMANT_SNAPSHOT,
        )
        self.assertFalse(request.output_directory.exists())
        self.assertEqual(
            list(self.root.glob(f".{request.output_directory.name}.*.staging")),
            [],
        )

    def test_exact_reference_lab(self) -> None:
        commit = "9ab64121350b69ce81e6be79961ad426026bbc39"
        root = b"plugins/github-evidence/src/veritrail_github"
        request = SourceSnapshotRequest(
            spec=SourceSnapshotSpec(
                repository_id="NoctilumeDev/VeriTrail",
                commit_oid=commit,
                analysis_root={"path_kind": "GIT_PATH", "git_path_hex": root.hex()},
            ),
            repository_path=REPOSITORY_ROOT,
            output_directory=self.root / "reference-lab",
        )
        result = create_source_snapshot(request, runtime=self.runtime)
        artifact_bytes = result.artifact_path.read_bytes()
        document = json.loads(artifact_bytes)
        self.assertEqual(len(document["inventory"]), 22)
        self.assertEqual(sum(item["content"]["size_bytes"] for item in document["inventory"]), 259_553)
        self.assertTrue(all(item["entry_kind"] == "REGULAR_BLOB" for item in document["inventory"]))
        self.assertEqual(
            document["source_snapshot_digest"],
            "08d32840ef56f0c7c0edd6e51d1c64e40b8f476af9330961d1b10c0916b9aaaa",
        )
        self.assertEqual(
            hashlib.sha256(artifact_bytes).hexdigest(),
            "e2e79a9e21da9c2484b885033cd75503501ec94476539ad575bb8161dd304083",
        )
        self.assertEqual(len(artifact_bytes), 10_611)
        schema_paths = (
            REPOSITORY_ROOT / "schemas" / "review-r1-common-0.1.schema.json",
            REPOSITORY_ROOT / "schemas" / "review-source-snapshot-0.1.schema.json",
        )
        schemas = [json.loads(path.read_bytes()) for path in schema_paths]
        registry = Registry().with_resources(
            [
                (schema["$id"], Resource.from_contents(schema))
                for schema in schemas
            ]
        )
        Draft202012Validator(schemas[1], registry=registry).validate(document)

    def test_importer_contract_fixture_keeps_verified_bytes_after_path_changes(self) -> None:
        fixture = create_fixture_repository(self.root)
        result = create_source_snapshot(self.request(fixture, "import-source"), runtime=self.runtime)
        retained = result.snapshot
        original = retained.canonical_bytes
        result.artifact_path.write_bytes(b"{}\n")
        copied = retained.document_copy()
        self.assertEqual(retained.canonical_bytes, original)
        self.assertEqual(copied["source_snapshot_digest"], retained.source_snapshot_digest)
        copied["repository_id"] = "mutated"
        self.assertEqual(retained.canonical_bytes, original)

    @staticmethod
    def _nested_tree_oid(fixture) -> str:
        raw = object_body(fixture.path, fixture.analysis_tree_oid)
        marker = b"40000 nested\x00"
        start = raw.index(marker) + len(marker)
        oid_size = 20 if fixture.algorithm == "sha1" else 32
        return raw[start : start + oid_size].hex()


if __name__ == "__main__":
    unittest.main()
