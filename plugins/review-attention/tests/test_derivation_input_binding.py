from __future__ import annotations

import copy
import hashlib
import inspect
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zlib
from dataclasses import fields, replace
from pathlib import Path
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
FIXTURE_ROOT = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "review-r1-derivation-input-0.1"
    / "reference-lab"
)
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from support import (  # noqa: E402
    FixtureRepository,
    corrupt_loose_object,
    create_fixture_repository,
    git_executable,
    write_commit,
    write_object,
    write_tree,
)
from veritrail_review import (  # noqa: E402
    DerivationInputError,
    DerivationInputFailureCode,
    DerivationInputRequest,
    DerivationInputRuntime,
    SourceSnapshotRequest,
    SourceSnapshotRuntime,
    SourceSnapshotSpec,
    bind_derivation_inputs,
    create_source_snapshot,
)
from veritrail_review.canonical import (  # noqa: E402
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from veritrail_review.derivation_input import (  # noqa: E402
    _bind_derivation_inputs,
    _is_python_identifier,
)
from veritrail_review.derivation_input_contracts import (  # noqa: E402
    tightened_derivation_input_safety_profile_for_testing,
)


class _FakeClock:
    value = 0.0

    def __call__(self) -> float:
        return self.value


def _canonical_bytes(document: dict[str, object]) -> bytes:
    return canonical_json_bytes(document) + b"\n"


def _write_canonical(path: Path, document: dict[str, object]) -> None:
    path.write_bytes(_canonical_bytes(document))


def _profile_document() -> dict[str, object]:
    value = json.loads((FIXTURE_ROOT / "derivation-profile.json").read_bytes())
    assert isinstance(value, dict)
    return value


def _seal_policy(document: dict[str, object]) -> dict[str, object]:
    analysis_payload = {
        key: copy.deepcopy(document[key])
        for key in (
            "source_snapshot_digest",
            "derivation_profile_digest",
            "scope_decisions",
            "provider_requirements",
            "python_module_mapping",
        )
    }
    document["analysis_scope_digest"] = semantic_digest(
        "veritrail.review.analysis-scope/0.1", analysis_payload
    )
    document["slice_policy_digest"] = semantic_digest(
        "veritrail.review.slice-policy/0.1",
        {
            "analysis_scope_digest": document["analysis_scope_digest"],
            "slice_policy": copy.deepcopy(document["slice_policy"]),
        },
    )
    policy_payload = {
        key: copy.deepcopy(value)
        for key, value in document.items()
        if key
        not in {
            "analysis_scope_digest",
            "slice_policy_digest",
            "policy_digest",
            "seal",
        }
    }
    document["policy_digest"] = semantic_digest(
        "veritrail.review.review-policy/0.1", policy_payload
    )
    document.pop("seal", None)
    document["seal"] = {
        "algorithm": "sha256",
        "digest": sha256_bytes(canonical_json_bytes(document)),
    }
    return document


def _policy_document(
    snapshot: dict[str, object],
    *,
    module_root: dict[str, str] | None = None,
) -> dict[str, object]:
    profile = _profile_document()
    coordinate = snapshot["source_coordinate"]
    assert isinstance(coordinate, dict)
    inventory = snapshot["inventory"]
    assert isinstance(inventory, list)
    policy: dict[str, object] = {
        "artifact_kind": "REVIEW_POLICY",
        "schema_version": "0.1",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "policy_id": "synthetic-input-binding-policy",
        "version": 1,
        "source_snapshot_digest": snapshot["source_snapshot_digest"],
        "derivation_profile_digest": profile["profile_digest"],
        "scope_decisions": [
            {
                "git_path": copy.deepcopy(item["git_path"]),
                "disposition": "IN_SCOPE",
                "source_class": "FIRST_PARTY",
                "reason_code": "POLICY_INCLUDED",
            }
            for item in inventory
        ],
        "provider_requirements": [
            {
                "capability_id": "python-ast",
                "required": True,
                "composition_mode": "CUMULATIVE",
            }
        ],
        "python_module_mapping": {
            "module_root": copy.deepcopy(
                module_root if module_root is not None else coordinate["analysis_root"]
            ),
            "package_prefix": ["pkg"],
        },
        "slice_policy": {
            "anchor_fact_kinds": ["MODULE"],
            "allowed_relations": [
                {"relation_kind": "LEXICAL_CONTAINS", "direction": "OUTBOUND"},
                {
                    "relation_kind": "IMPORT_TARGET_LITERAL",
                    "direction": "OUTBOUND",
                },
            ],
            "max_depth": 1,
            "max_symbols": 128,
            "max_files": 32,
            "max_relations": 256,
        },
        "execution_budget": {
            "wall_clock_ms": 10_000,
            "memory_bytes": 268_435_456,
            "artifact_bytes": 16_777_216,
        },
        "governance": {
            "claim_owner_ref": "fixture-human",
            "drafter_ref": "fixture-drafter",
            "seal_authority_ref": "fixture-human",
            "seal_decision": "CONFIRMED",
        },
    }
    return _seal_policy(policy)


class DerivationInputBindingContractMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name)
        self.runtime = DerivationInputRuntime(git_executable=git_executable())
        self.fixture = create_fixture_repository(self.root / "fixture")
        self.request, self.snapshot, self.policy = self._materialize_inputs(
            self.fixture, name="default"
        )

    def tearDown(self) -> None:
        self._temporary.cleanup()

    def _materialize_inputs(
        self,
        fixture: FixtureRepository,
        *,
        name: str,
        analysis_root: bytes = b"pkg",
    ) -> tuple[DerivationInputRequest, dict[str, object], dict[str, object]]:
        directory = self.root / f"inputs-{name}"
        directory.mkdir()
        snapshot_publication = create_source_snapshot(
            SourceSnapshotRequest(
                spec=SourceSnapshotSpec(
                    repository_id="fixture/repository",
                    commit_oid=fixture.commit_oid,
                    analysis_root=(
                        {"path_kind": "REPOSITORY_ROOT"}
                        if not analysis_root
                        else {
                            "path_kind": "GIT_PATH",
                            "git_path_hex": analysis_root.hex(),
                        }
                    ),
                ),
                repository_path=fixture.path,
                output_directory=directory / "snapshot-publication",
            ),
            runtime=SourceSnapshotRuntime(git_executable=git_executable()),
        )
        snapshot_path = directory / "source-snapshot.json"
        snapshot_path.write_bytes(snapshot_publication.snapshot.canonical_bytes)
        snapshot = snapshot_publication.snapshot.document_copy()
        profile_path = directory / "derivation-profile.json"
        profile_path.write_bytes((FIXTURE_ROOT / "derivation-profile.json").read_bytes())
        policy = _policy_document(snapshot)
        policy_path = directory / "review-policy.json"
        _write_canonical(policy_path, policy)
        return (
            DerivationInputRequest(
                source_snapshot_path=snapshot_path.resolve(),
                review_policy_path=policy_path.resolve(),
                derivation_profile_path=profile_path.resolve(),
                repository_path=fixture.path.resolve(),
            ),
            snapshot,
            policy,
        )

    def _write_policy(self, document: dict[str, object]) -> None:
        _write_canonical(self.request.review_policy_path, document)

    def _bind_internal(self, *, profile=None, clock=None, stage_hook=None):
        return _bind_derivation_inputs(
            self.request,
            runtime=self.runtime,
            safety_profile=(
                profile
                if profile is not None
                else tightened_derivation_input_safety_profile_for_testing()
            ),
            clock=clock if clock is not None else __import__("time").monotonic,
            stage_hook=stage_hook,
        )

    def _assert_failure(
        self,
        code: DerivationInputFailureCode,
        *,
        request: DerivationInputRequest | None = None,
        runtime: DerivationInputRuntime | None = None,
    ) -> DerivationInputError:
        with self.assertRaises(DerivationInputError) as raised:
            bind_derivation_inputs(
                request or self.request,
                runtime=self.runtime if runtime is None else runtime,
            )
        self.assertEqual(raised.exception.code, code)
        self.assertNotIn(str(self.root), str(raised.exception))
        return raised.exception

    def test_row_01_success_returns_owned_values_and_performs_no_writes(self) -> None:
        before = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        result = bind_derivation_inputs(self.request, runtime=self.runtime)
        after = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        self.assertEqual(after, before)
        self.assertEqual(result.source_snapshot_digest, self.snapshot["source_snapshot_digest"])
        self.assertEqual(result.policy_digest, self.policy["policy_digest"])
        self.assertEqual(len(result.verified_blob_bytes_by_object_identity), 6)
        self.assertEqual(
            {item.name for item in fields(result)},
            {
                "source_snapshot_canonical_bytes",
                "review_policy_canonical_bytes",
                "derivation_profile_canonical_bytes",
                "verified_blob_bytes_by_object_identity",
                "source_snapshot_digest",
                "policy_digest",
                "analysis_scope_digest",
                "slice_policy_digest",
                "derivation_profile_digest",
            },
        )
        with self.assertRaises(TypeError):
            result.verified_blob_bytes_by_object_identity["new"] = b"x"  # type: ignore[index]
        copied = result.review_policy_document_copy()
        copied["policy_id"] = "mutated"
        self.assertEqual(
            result.review_policy_document_copy()["policy_id"],
            "synthetic-input-binding-policy",
        )

    def test_row_02_policy_snapshot_digest_mismatch_is_typed(self) -> None:
        self.policy["source_snapshot_digest"] = "0" * 64
        self._write_policy(_seal_policy(self.policy))
        self._assert_failure(DerivationInputFailureCode.POLICY_SNAPSHOT_MISMATCH)

    def test_row_03_policy_profile_digest_mismatch_is_typed(self) -> None:
        self.policy["derivation_profile_digest"] = "0" * 64
        self._write_policy(_seal_policy(self.policy))
        self._assert_failure(DerivationInputFailureCode.POLICY_PROFILE_MISMATCH)

    def test_row_04_scope_missing_duplicate_and_extra_paths_fail_closed(self) -> None:
        decisions = self.policy["scope_decisions"]
        assert isinstance(decisions, list)
        for name, replacement, expected in (
            (
                "missing",
                decisions[:-1],
                DerivationInputFailureCode.POLICY_SCOPE_MISMATCH,
            ),
            (
                "duplicate",
                sorted(
                    decisions + [copy.deepcopy(decisions[0])],
                    key=lambda item: bytes.fromhex(item["git_path"]["git_path_hex"]),
                ),
                DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY,
            ),
            (
                "extra",
                sorted(
                    decisions
                    + [
                        {
                            "git_path": {
                                "path_kind": "GIT_PATH",
                                "git_path_hex": b"pkg/zz-extra.py".hex(),
                            },
                            "disposition": "OUT_OF_SCOPE",
                            "source_class": "UNCLASSIFIED",
                            "reason_code": "POLICY_EXCLUDED",
                        }
                    ],
                    key=lambda item: bytes.fromhex(item["git_path"]["git_path_hex"]),
                ),
                DerivationInputFailureCode.POLICY_SCOPE_MISMATCH,
            ),
        ):
            with self.subTest(name=name):
                document = copy.deepcopy(self.policy)
                document["scope_decisions"] = replacement
                self._write_policy(_seal_policy(document))
                self._assert_failure(expected)

    def test_row_05_module_root_uses_raw_component_containment(self) -> None:
        for raw in (b"pkg", b"pkg/nested"):
            with self.subTest(raw=raw):
                document = copy.deepcopy(self.policy)
                document["python_module_mapping"]["module_root"] = {
                    "path_kind": "GIT_PATH",
                    "git_path_hex": raw.hex(),
                }
                self._write_policy(_seal_policy(document))
                bind_derivation_inputs(self.request, runtime=self.runtime)
        document = copy.deepcopy(self.policy)
        document["python_module_mapping"]["module_root"] = {
            "path_kind": "GIT_PATH",
            "git_path_hex": b"pkg2".hex(),
        }
        self._write_policy(_seal_policy(document))
        self._assert_failure(
            DerivationInputFailureCode.MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT
        )

    def test_row_06_each_artifact_rejects_noncanonical_or_bad_digest_and_seal(self) -> None:
        cases: list[tuple[str, Path, bytes, DerivationInputFailureCode]] = [
            (
                "snapshot-noncanonical",
                self.request.source_snapshot_path,
                b" " + self.request.source_snapshot_path.read_bytes(),
                DerivationInputFailureCode.NONCONFORMANT_SOURCE_SNAPSHOT,
            ),
            (
                "profile-digest",
                self.request.derivation_profile_path,
                _canonical_bytes(
                    {
                        **_profile_document(),
                        "profile_digest": "0" * 64,
                    }
                ),
                DerivationInputFailureCode.NONCONFORMANT_DERIVATION_PROFILE,
            ),
            (
                "policy-seal",
                self.request.review_policy_path,
                _canonical_bytes(
                    {
                        **self.policy,
                        "seal": {"algorithm": "sha256", "digest": "0" * 64},
                    }
                ),
                DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY,
            ),
        ]
        originals = {path: path.read_bytes() for _, path, _, _ in cases}
        for name, path, value, expected in cases:
            with self.subTest(name=name):
                for restore_path, original in originals.items():
                    restore_path.write_bytes(original)
                path.write_bytes(value)
                self._assert_failure(expected)

    def test_row_07_relative_missing_artifact_repository_and_git_are_typed(self) -> None:
        relative = replace(self.request, source_snapshot_path=Path("source-snapshot.json"))
        self._assert_failure(
            DerivationInputFailureCode.INVALID_DERIVATION_INPUT_REQUEST,
            request=relative,
        )
        missing_file = replace(
            self.request, source_snapshot_path=(self.root / "missing.json").resolve()
        )
        self._assert_failure(
            DerivationInputFailureCode.INPUT_ARTIFACT_UNAVAILABLE,
            request=missing_file,
        )
        missing_repo = replace(
            self.request, repository_path=(self.root / "missing-repository").resolve()
        )
        self._assert_failure(
            DerivationInputFailureCode.INPUT_REPOSITORY_UNAVAILABLE,
            request=missing_repo,
        )
        missing_git = DerivationInputRuntime(
            git_executable=(self.root / "missing-git.exe").resolve()
        )
        self._assert_failure(
            DerivationInputFailureCode.INPUT_RUNTIME_UNAVAILABLE,
            runtime=missing_git,
        )

    def test_row_08_directory_symlink_reparse_and_hardlink_are_not_ordinary_files(self) -> None:
        directory_request = replace(
            self.request, derivation_profile_path=self.root.resolve()
        )
        self._assert_failure(
            DerivationInputFailureCode.INPUT_ARTIFACT_NOT_ORDINARY_FILE,
            request=directory_request,
        )
        link = self.root / "profile-link.json"
        try:
            os.symlink(self.request.derivation_profile_path, link)
        except OSError as exc:
            self.skipTest(f"file symlink unavailable: {exc}")
        self._assert_failure(
            DerivationInputFailureCode.INPUT_ARTIFACT_NOT_ORDINARY_FILE,
            request=replace(self.request, derivation_profile_path=link.absolute()),
        )
        hardlink = self.root / "policy-hardlink.json"
        os.link(self.request.review_policy_path, hardlink)
        self._assert_failure(
            DerivationInputFailureCode.INPUT_ARTIFACT_NOT_ORDINARY_FILE,
            request=replace(self.request, review_policy_path=hardlink.resolve()),
        )

    def test_row_09_path_replacement_after_read_cannot_change_owned_bytes(self) -> None:
        originals = {
            self.request.source_snapshot_path: self.request.source_snapshot_path.read_bytes(),
            self.request.review_policy_path: self.request.review_policy_path.read_bytes(),
            self.request.derivation_profile_path: self.request.derivation_profile_path.read_bytes(),
        }
        replaced = False

        def replace_paths(stage: str) -> None:
            nonlocal replaced
            if stage == "source-snapshot-validation-start" and not replaced:
                replaced = True
                for path in originals:
                    path.write_bytes(b"{}\n")

        result = self._bind_internal(stage_hook=replace_paths)
        self.assertTrue(replaced)
        self.assertEqual(result.source_snapshot_canonical_bytes, originals[self.request.source_snapshot_path])
        self.assertEqual(result.review_policy_canonical_bytes, originals[self.request.review_policy_path])
        self.assertEqual(result.derivation_profile_canonical_bytes, originals[self.request.derivation_profile_path])

    def test_row_10_missing_corrupt_type_or_body_git_objects_map_to_reacquisition_mismatch(self) -> None:
        actions = ("missing", "corrupt", "type", "body")
        for action in actions:
            with self.subTest(action=action):
                fixture = create_fixture_repository(self.root / f"git-{action}")
                request, _, _ = self._materialize_inputs(fixture, name=f"git-{action}")
                oid = fixture.blob_oids[0]
                object_path = fixture.path / ".git" / "objects" / oid[:2] / oid[2:]
                if action == "missing":
                    object_path.unlink()
                elif action == "corrupt":
                    corrupt_loose_object(fixture.path, oid)
                elif action == "type":
                    body = b"100644 x.py\x00" + bytes.fromhex(oid)
                    object_path.write_bytes(
                        zlib.compress(b"tree " + str(len(body)).encode() + b"\x00" + body)
                    )
                else:
                    body = b"different-body\n"
                    object_path.write_bytes(
                        zlib.compress(b"blob " + str(len(body)).encode() + b"\x00" + body)
                    )
                self._assert_failure(
                    DerivationInputFailureCode.SOURCE_REACQUISITION_MISMATCH,
                    request=request,
                )

    def test_row_11_worktree_index_untracked_and_ref_noise_do_not_change_binding(self) -> None:
        (self.fixture.path / "pkg").mkdir()
        (self.fixture.path / "pkg" / "regular.py").write_text("dirty\n", encoding="utf-8")
        (self.fixture.path / "untracked.txt").write_text("noise\n", encoding="utf-8")
        subprocess.run(
            [os.fspath(git_executable()), "-C", os.fspath(self.fixture.path), "add", "."],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        ref = self.fixture.path / ".git" / "refs" / "heads" / "noise"
        ref.parent.mkdir(parents=True, exist_ok=True)
        ref.write_text("f" * 40 + "\n", encoding="ascii")
        result = bind_derivation_inputs(self.request, runtime=self.runtime)
        self.assertEqual(result.source_snapshot_digest, self.snapshot["source_snapshot_digest"])

    def test_row_12_two_sufficient_tighter_budgets_produce_identical_values(self) -> None:
        first = self._bind_internal(
            profile=tightened_derivation_input_safety_profile_for_testing(
                wall_clock_ms=25_000
            )
        )
        second = self._bind_internal(
            profile=tightened_derivation_input_safety_profile_for_testing(
                wall_clock_ms=29_000
            )
        )
        self.assertEqual(first, second)

    def test_row_13_same_bytes_at_different_absolute_paths_have_same_value(self) -> None:
        copied = self.root / "copied-inputs"
        copied.mkdir()
        request = replace(
            self.request,
            source_snapshot_path=(copied / "a.json").resolve(),
            review_policy_path=(copied / "b.json").resolve(),
            derivation_profile_path=(copied / "c.json").resolve(),
        )
        shutil.copyfile(self.request.source_snapshot_path, request.source_snapshot_path)
        shutil.copyfile(self.request.review_policy_path, request.review_policy_path)
        shutil.copyfile(self.request.derivation_profile_path, request.derivation_profile_path)
        self.assertEqual(
            bind_derivation_inputs(self.request, runtime=self.runtime),
            bind_derivation_inputs(request, runtime=self.runtime),
        )

    def test_row_14_one_deadline_covers_read_validate_cross_git_and_copy(self) -> None:
        stages = (
            "artifact-read-start",
            "source-snapshot-validation-start",
            "cross-artifact-validation-start",
            "source-reacquisition-start",
            "owned-copy-start",
        )
        for target in stages:
            with self.subTest(stage=target):
                clock = _FakeClock()

                def advance(stage: str, target_stage=target) -> None:
                    if stage == target_stage:
                        clock.value = 0.101

                with self.assertRaises(DerivationInputError) as raised:
                    self._bind_internal(
                        profile=tightened_derivation_input_safety_profile_for_testing(
                            wall_clock_ms=100
                        ),
                        clock=clock,
                        stage_hook=advance,
                    )
                self.assertEqual(
                    raised.exception.code,
                    DerivationInputFailureCode.INPUT_SAFETY_BUDGET_EXHAUSTED,
                )

    def test_row_15_artifact_size_limits_are_inclusive_and_preparse(self) -> None:
        cases = (
            ("source", "max_source_snapshot_bytes", self.request.source_snapshot_path),
            ("policy", "max_review_policy_bytes", self.request.review_policy_path),
            ("profile", "max_derivation_profile_bytes", self.request.derivation_profile_path),
        )
        for name, field_name, path in cases:
            with self.subTest(name=name, edge="exact"):
                self._bind_internal(
                    profile=tightened_derivation_input_safety_profile_for_testing(
                        **{field_name: path.stat().st_size}
                    )
                )
            with self.subTest(name=name, edge="plus-one"):
                with self.assertRaises(DerivationInputError) as raised:
                    self._bind_internal(
                        profile=tightened_derivation_input_safety_profile_for_testing(
                            **{field_name: path.stat().st_size - 1}
                        )
                    )
                self.assertEqual(
                    raised.exception.code,
                    DerivationInputFailureCode.INPUT_ARTIFACT_TOO_LARGE,
                )

    def test_row_16_repeated_blob_oid_is_retained_once(self) -> None:
        base = create_fixture_repository(self.root / "duplicate-oid")
        oid = base.blob_oids[0]
        analysis_tree = write_tree(
            base.path,
            base.algorithm,
            [(b"100644", b"a.py", oid), (b"100644", b"b.py", oid)],
        )
        root_tree = write_tree(
            base.path, base.algorithm, [(b"40000", b"pkg", analysis_tree)]
        )
        commit = write_commit(base.path, base.algorithm, root_tree, b"duplicate-oid")
        fixture = replace(
            base,
            commit_oid=commit,
            root_tree_oid=root_tree,
            analysis_tree_oid=analysis_tree,
            blob_oids=(oid,),
            terminal_count=2,
        )
        request, _, _ = self._materialize_inputs(fixture, name="duplicate-oid")
        result = bind_derivation_inputs(request, runtime=self.runtime)
        self.assertEqual(len(result.verified_blob_bytes_by_object_identity), 1)

    def test_row_17_raw_non_utf8_nfc_nfd_and_case_paths_remain_distinct(self) -> None:
        base = create_fixture_repository(self.root / "raw-paths")
        oid = write_object(base.path, base.algorithm, "blob", b"pass\n")
        names = (b"A.py", b"a.py", "é.py".encode(), "e\u0301.py".encode(), b"\xff.py")
        analysis_tree = write_tree(
            base.path,
            base.algorithm,
            [(b"100644", name, oid) for name in names],
        )
        root_tree = write_tree(
            base.path, base.algorithm, [(b"40000", b"pkg", analysis_tree)]
        )
        commit = write_commit(base.path, base.algorithm, root_tree, b"raw-paths")
        fixture = replace(
            base,
            commit_oid=commit,
            root_tree_oid=root_tree,
            analysis_tree_oid=analysis_tree,
            blob_oids=(oid,),
            terminal_count=len(names),
        )
        request, snapshot, _ = self._materialize_inputs(fixture, name="raw-paths")
        result = bind_derivation_inputs(request, runtime=self.runtime)
        document = result.review_policy_document_copy()
        expected = {b"pkg/" + name for name in names}
        actual = {
            bytes.fromhex(item["git_path"]["git_path_hex"])
            for item in document["scope_decisions"]
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(snapshot["inventory"]), len(names))

    def test_row_18_repository_root_and_nonroot_module_combinations(self) -> None:
        root_request, root_snapshot, root_policy = self._materialize_inputs(
            self.fixture, name="root-analysis", analysis_root=b""
        )
        for module_root in (
            {"path_kind": "REPOSITORY_ROOT"},
            {"path_kind": "GIT_PATH", "git_path_hex": b"pkg".hex()},
        ):
            with self.subTest(root_analysis=True, module_root=module_root):
                document = copy.deepcopy(root_policy)
                document["python_module_mapping"]["module_root"] = module_root
                _write_canonical(root_request.review_policy_path, _seal_policy(document))
                bind_derivation_inputs(root_request, runtime=self.runtime)
        document = copy.deepcopy(self.policy)
        document["python_module_mapping"]["module_root"] = {
            "path_kind": "REPOSITORY_ROOT"
        }
        self._write_policy(_seal_policy(document))
        self._assert_failure(
            DerivationInputFailureCode.MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT
        )
        self.assertEqual(root_snapshot["source_coordinate"]["analysis_root"], {"path_kind": "REPOSITORY_ROOT"})

    def test_row_19_legal_slice_relation_configuration_is_preserved_without_execution(self) -> None:
        document = copy.deepcopy(self.policy)
        document["slice_policy"] = {
            "anchor_fact_kinds": [
                "MODULE",
                "CLASS_DECLARATION",
                "FUNCTION_DECLARATION",
                "METHOD_DECLARATION",
                "IMPORT_DECLARATION",
            ],
            "allowed_relations": [
                {"relation_kind": "LEXICAL_CONTAINS", "direction": "OUTBOUND"},
                {"relation_kind": "LEXICAL_CONTAINS", "direction": "BOTH"},
                {"relation_kind": "IMPORT_TARGET_LITERAL", "direction": "INBOUND"},
            ],
            "max_depth": 0,
            "max_symbols": 1,
            "max_files": 1,
            "max_relations": 0,
        }
        self._write_policy(_seal_policy(document))
        result = bind_derivation_inputs(self.request, runtime=self.runtime)
        self.assertEqual(result.review_policy_document_copy()["slice_policy"], document["slice_policy"])
        forbidden = {"facts.json", "relations.json", "review-slices.json", "coverage.json", "manifest.json"}
        self.assertTrue(forbidden.isdisjoint({path.name for path in self.root.rglob("*")}))

    def test_row_20_public_result_is_independent_of_assert_optimization(self) -> None:
        source = inspect.getsource(_bind_derivation_inputs)
        self.assertNotIn("assert ", source)
        result = bind_derivation_inputs(self.request, runtime=self.runtime)
        self.assertEqual(result.source_snapshot_digest, self.snapshot["source_snapshot_digest"])

        python_310_policy = copy.deepcopy(self.policy)
        python_310_policy["python_module_mapping"]["package_prefix"] = ["变量"]
        self._write_policy(_seal_policy(python_310_policy))
        accepted = bind_derivation_inputs(self.request, runtime=self.runtime)
        self.assertEqual(
            accepted.review_policy_document_copy()["python_module_mapping"]["package_prefix"],
            ["变量"],
        )

        post_python_310_policy = copy.deepcopy(self.policy)
        post_python_310_policy["python_module_mapping"]["package_prefix"] = ["\u0870"]
        self._write_policy(_seal_policy(post_python_310_policy))
        self._assert_failure(DerivationInputFailureCode.NONCONFORMANT_REVIEW_POLICY)

        expected_identifier_digests = {
            "": "086ba2039596f4e84ca79818a445e195d71d9ee46fe52ea4cda47e541865f994",
            "a": "e3c579def9a076edb3e5bb842a10a6d85c2a0c4f0062c2d61b0897590b8413ff",
        }
        for prefix, expected_digest in expected_identifier_digests.items():
            digest = hashlib.sha256()
            for codepoint in range(sys.maxunicode + 1):
                digest.update(
                    b"1"
                    if _is_python_identifier(prefix + chr(codepoint))
                    else b"0"
                )
            self.assertEqual(digest.hexdigest(), expected_digest)

    def test_row_21_exact_reference_lab_matches_all_presealed_coordinates(self) -> None:
        temporary = self.root / "reference-lab-snapshot"
        root = b"plugins/github-evidence/src/veritrail_github"
        publication = create_source_snapshot(
            SourceSnapshotRequest(
                spec=SourceSnapshotSpec(
                    repository_id="NoctilumeDev/VeriTrail",
                    commit_oid="9ab64121350b69ce81e6be79961ad426026bbc39",
                    analysis_root={"path_kind": "GIT_PATH", "git_path_hex": root.hex()},
                ),
                repository_path=REPOSITORY_ROOT,
                output_directory=temporary,
            ),
            runtime=SourceSnapshotRuntime(git_executable=git_executable()),
        )
        expected = json.loads((FIXTURE_ROOT / "expected-digests.json").read_bytes())
        result = bind_derivation_inputs(
            DerivationInputRequest(
                publication.artifact_path.resolve(),
                (FIXTURE_ROOT / "review-policy.json").resolve(),
                (FIXTURE_ROOT / "derivation-profile.json").resolve(),
                REPOSITORY_ROOT.resolve(),
            ),
            runtime=self.runtime,
        )
        self.assertEqual(result.source_snapshot_digest, expected["source_snapshot_digest"])
        self.assertEqual(result.policy_digest, expected["policy_digest"])
        self.assertEqual(result.analysis_scope_digest, expected["analysis_scope_digest"])
        self.assertEqual(result.slice_policy_digest, expected["slice_policy_digest"])
        self.assertEqual(result.derivation_profile_digest, expected["derivation_profile_digest"])
        self.assertEqual(len(result.verified_blob_bytes_by_object_identity), 22)
        self.assertEqual(sum(map(len, result.verified_blob_bytes_by_object_identity.values())), 259_553)
        self.assertEqual(hashlib.sha256(result.source_snapshot_canonical_bytes).hexdigest(), expected["source_snapshot_file_sha256"])
        self.assertEqual(hashlib.sha256(result.review_policy_canonical_bytes).hexdigest(), expected["review_policy_file_sha256"])
        self.assertEqual(hashlib.sha256(result.derivation_profile_canonical_bytes).hexdigest(), expected["derivation_profile_file_sha256"])

    def test_row_22_public_api_has_no_output_or_downstream_product_controls(self) -> None:
        self.assertEqual(
            {item.value for item in DerivationInputFailureCode},
            {
                "INVALID_DERIVATION_INPUT_REQUEST",
                "INPUT_ARTIFACT_UNAVAILABLE",
                "INPUT_ARTIFACT_NOT_ORDINARY_FILE",
                "INPUT_ARTIFACT_TOO_LARGE",
                "INPUT_REPOSITORY_UNAVAILABLE",
                "INPUT_RUNTIME_UNAVAILABLE",
                "NONCONFORMANT_SOURCE_SNAPSHOT",
                "NONCONFORMANT_REVIEW_POLICY",
                "NONCONFORMANT_DERIVATION_PROFILE",
                "POLICY_SNAPSHOT_MISMATCH",
                "POLICY_PROFILE_MISMATCH",
                "POLICY_SCOPE_MISMATCH",
                "MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT",
                "SOURCE_REACQUISITION_MISMATCH",
                "INPUT_SAFETY_BUDGET_EXHAUSTED",
                "INTERNAL_INPUT_BINDING_ERROR",
            },
        )
        self.assertEqual(
            {item.name for item in fields(DerivationInputRequest)},
            {
                "source_snapshot_path",
                "review_policy_path",
                "derivation_profile_path",
                "repository_path",
            },
        )
        parameters = inspect.signature(bind_derivation_inputs).parameters
        forbidden = {
            "output",
            "output_directory",
            "manifest",
            "facts",
            "relations",
            "slices",
            "coverage",
            "budget",
            "safety_profile",
            "parser",
            "provider",
        }
        self.assertTrue(forbidden.isdisjoint(parameters))


if __name__ == "__main__":
    unittest.main()
