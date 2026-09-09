from __future__ import annotations

import gzip
import io
import json
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.github_evidence_release_assets import (
    ASSET_NAMES,
    CHECKSUM_NAME,
    PAYLOAD_NAMES,
    SDIST_NAME,
    SUMMARY_NAME,
    VERSION,
    WHEEL_NAME,
    ReleaseAssetError,
    asset_identity,
    finalize_assets,
    inspect_sdist,
    inspect_wheel,
    normalize_sdist,
    source_identity,
    validate_build_facts,
    validate_validation_facts,
    verify_assets,
)
from scripts.p4_real_github_acceptance import release_acceptance_plan
from veritrail.acceptance_plan import verify_sealed_acceptance_plan


SOURCE_COMMIT = "a" * 40
SOURCE_DATE_EPOCH = 1_788_891_310
METADATA = b"""Metadata-Version: 2.4
Name: veritrail-github-evidence
Version: 0.1.0
Requires-Python: >=3.10
Requires-Dist: veritrail==0.13.0
Provides-Extra: render
Requires-Dist: playwright==1.62.0; extra == \"render\"

"""


def write_wheel(path: Path) -> None:
    metadata_path = (
        f"veritrail_github_evidence-{VERSION}.dist-info/METADATA"
    )
    with zipfile.ZipFile(path, mode="w") as archive:
        archive.writestr("veritrail_github/__init__.py", "__version__ = '0.1.0'\n")
        archive.writestr(metadata_path, METADATA)


def write_sdist(path: Path, *, gzip_mtime: int = 1, member_mtime: int = 2) -> None:
    root = f"veritrail_github_evidence-{VERSION}"
    with path.open("wb") as raw_output:
        with gzip.GzipFile(
            filename=f"source-{gzip_mtime}.tar",
            mode="wb",
            fileobj=raw_output,
            mtime=gzip_mtime,
        ) as compressed_output:
            with tarfile.open(fileobj=compressed_output, mode="w") as archive:
                directory = tarfile.TarInfo(root)
                directory.type = tarfile.DIRTYPE
                directory.mode = 0o755
                directory.mtime = member_mtime
                archive.addfile(directory)
                metadata = tarfile.TarInfo(f"{root}/PKG-INFO")
                metadata.size = len(METADATA)
                metadata.mode = 0o644
                metadata.mtime = member_mtime
                archive.addfile(metadata, io.BytesIO(METADATA))


def validation_facts(*, attempt: int = 1) -> dict[str, object]:
    return {
        "schema_version": "0.1",
        "state": "PUBLIC_GATES_GREEN",
        "source_commit": SOURCE_COMMIT,
        "public_ci": {
            "run_id": 101,
            "head_sha": SOURCE_COMMIT,
            "attempt": attempt,
            "jobs": 11,
            "status": "SUCCESS",
        },
        "browser_smoke": {
            "run_id": 102,
            "head_sha": SOURCE_COMMIT,
            "attempt": 1,
            "jobs": 1,
            "status": "SUCCESS",
        },
        "local_matrix": {
            "status": "PASS",
            "python_series": ["3.10", "3.13"],
            "normal_and_optimized_regression": "PASS",
            "base_wheel": "PASS",
            "sdist": "PASS",
            "render_extra": "PASS",
            "p3_uninstall_core_readback": "PASS",
            "real_github_pass": "PASS",
            "cleanup": "PASS",
        },
    }


def prepare_candidate(root: Path) -> tuple[Path, Path, Path]:
    assets = root / "assets"
    assets.mkdir()
    write_wheel(assets / WHEEL_NAME)
    write_sdist(assets / SDIST_NAME)
    normalize_sdist(assets / SDIST_NAME, SOURCE_DATE_EPOCH)
    build_facts_path = root / "build-facts.json"
    build_facts_path.write_text(
        json.dumps(
            {
                "schema_version": "0.1",
                "state": "CANDIDATE_PAYLOADS_BUILT",
                "source": {
                    "commit": SOURCE_COMMIT,
                    "tree": "b" * 40,
                    "commit_timestamp": "2026-09-08T00:00:00+00:00",
                    "source_date_epoch": SOURCE_DATE_EPOCH,
                    "worktree_clean": True,
                },
                "distribution": {
                    "distribution": "veritrail-github-evidence",
                    "import_package": "veritrail_github",
                    "version": VERSION,
                    "requires_python": ">=3.10",
                    "core_dependency": "veritrail==0.13.0",
                    "render_extra": ["playwright==1.62.0"],
                    "cli": "veritrail-github-collect",
                },
                "toolchain": {
                    "python": "3.13.13",
                    "implementation": "CPython",
                    "pip": "25.2",
                    "build": "1.3.0",
                    "setuptools": "80.9.0",
                    "wheel": "0.45.1",
                },
                "build_comparison": {
                    "build_count": 2,
                    "source_copy_per_build": True,
                    "wheel_byte_identical": True,
                    "sdist_normalized_byte_identical": True,
                },
                "payloads": {
                    name: asset_identity(assets / name) for name in PAYLOAD_NAMES
                },
                "release_state": "PRE_TAG",
                "public_download_claim": "NONE",
            }
        ),
        encoding="utf-8",
    )
    validation_path = root / "validation-facts.json"
    validation_path.write_text(json.dumps(validation_facts()), encoding="utf-8")
    return assets, build_facts_path, validation_path


class GitHubEvidenceReleaseAssetTests(unittest.TestCase):
    def test_real_release_plan_is_presealed_to_the_exact_target(self) -> None:
        plan = release_acceptance_plan(
            owner="NoctilumeDev",
            repository="VeriTrail",
            target_commit_sha=SOURCE_COMMIT,
            repository_path="README.md",
            literal_marker="VeriTrail",
        )
        verify_sealed_acceptance_plan(plan)
        self.assertEqual(plan["subject"]["version"], SOURCE_COMMIT)
        self.assertEqual(
            {
                item["coordinates"]["target_commit_sha"]
                for item in plan["observation_specs"]
            },
            {SOURCE_COMMIT},
        )
        self.assertEqual(plan["assertions"][0]["right"], SOURCE_COMMIT)
        self.assertIn(SOURCE_COMMIT, plan["assertions"][1]["right"])

    def test_sdist_normalization_removes_gzip_and_member_time_variance(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-normalize-") as raw_temp:
            root = Path(raw_temp)
            outputs: list[bytes] = []
            for index, mtime in enumerate((11, 22)):
                path = root / f"candidate-{index}.tar.gz"
                write_sdist(path, gzip_mtime=mtime, member_mtime=mtime + 1)
                normalize_sdist(path, SOURCE_DATE_EPOCH)
                outputs.append(path.read_bytes())

            self.assertEqual(outputs[0], outputs[1])
            with tarfile.open(fileobj=io.BytesIO(outputs[0]), mode="r:gz") as archive:
                self.assertTrue(archive.getmember(f"veritrail_github_evidence-{VERSION}").isdir())
                self.assertTrue(
                    all(member.mtime == SOURCE_DATE_EPOCH for member in archive.getmembers())
                )
                self.assertTrue(all(member.uid == 0 for member in archive.getmembers()))
                self.assertTrue(all(member.gid == 0 for member in archive.getmembers()))

    def test_distribution_inspection_accepts_frozen_metadata_and_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-inspect-") as raw_temp:
            root = Path(raw_temp)
            write_wheel(root / WHEEL_NAME)
            write_sdist(root / SDIST_NAME)

            self.assertEqual(inspect_wheel(root / WHEEL_NAME)["metadata"]["version"], VERSION)
            self.assertEqual(inspect_sdist(root / SDIST_NAME)["metadata"]["version"], VERSION)

    def test_validation_facts_are_exact_and_do_not_republish_unknown_fields(self) -> None:
        facts = validation_facts()
        validated = validate_validation_facts(facts, SOURCE_COMMIT)
        self.assertEqual(validated, facts)

        facts["local_log"] = "C:\\private\\token.txt"
        with self.assertRaisesRegex(ReleaseAssetError, "undeclared fields"):
            validate_validation_facts(facts, SOURCE_COMMIT)

    def test_validation_facts_reject_rerun_and_source_drift(self) -> None:
        with self.assertRaisesRegex(ReleaseAssetError, "original attempt"):
            validate_validation_facts(validation_facts(attempt=2), SOURCE_COMMIT)
        drifted = validation_facts()
        drifted["public_ci"]["head_sha"] = "b" * 40  # type: ignore[index]
        with self.assertRaisesRegex(ReleaseAssetError, "source drifted"):
            validate_validation_facts(drifted, SOURCE_COMMIT)

    def test_build_facts_reject_unknown_fields_before_summary_publication(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-build-facts-") as raw_temp:
            assets, build_facts_path, _ = prepare_candidate(Path(raw_temp))
            facts = json.loads(build_facts_path.read_text(encoding="utf-8"))
            facts["local_temp_path"] = "C:\\private\\candidate"
            with self.assertRaisesRegex(ReleaseAssetError, "undeclared fields"):
                validate_build_facts(
                    facts,
                    {name: asset_identity(assets / name) for name in PAYLOAD_NAMES},
                )

    def test_finalize_creates_exact_non_self_referential_asset_set(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-finalize-") as raw_temp:
            assets, build_facts, validation = prepare_candidate(Path(raw_temp))
            summary = finalize_assets(
                assets=assets,
                build_facts_path=build_facts,
                validation_facts_path=validation,
            )

            self.assertEqual({path.name for path in assets.iterdir()}, set(ASSET_NAMES))
            self.assertNotIn("sha256", summary)
            self.assertNotIn("size", summary)
            checksum_names = {
                line.split("  ", 1)[1]
                for line in (assets / CHECKSUM_NAME).read_text(encoding="utf-8").splitlines()
            }
            self.assertEqual(checksum_names, {*PAYLOAD_NAMES, SUMMARY_NAME})
            self.assertEqual(verify_assets(assets)["state"], "PASS")

    def test_verify_rejects_corrupt_payload_and_extra_asset(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-corrupt-") as raw_temp:
            assets, build_facts, validation = prepare_candidate(Path(raw_temp))
            finalize_assets(
                assets=assets,
                build_facts_path=build_facts,
                validation_facts_path=validation,
            )
            with (assets / WHEEL_NAME).open("ab") as output:
                output.write(b"drift")
            with self.assertRaises(ReleaseAssetError):
                verify_assets(assets)

        with tempfile.TemporaryDirectory(prefix="veritrail-p4-extra-") as raw_temp:
            assets, build_facts, validation = prepare_candidate(Path(raw_temp))
            finalize_assets(
                assets=assets,
                build_facts_path=build_facts,
                validation_facts_path=validation,
            )
            (assets / "unexpected.log").write_text("not a release asset", encoding="utf-8")
            with self.assertRaisesRegex(ReleaseAssetError, "asset set drifted"):
                verify_assets(assets)

    def test_verify_rejects_summary_semantic_drift_even_with_updated_checksum(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-summary-drift-") as raw_temp:
            assets, build_facts, validation = prepare_candidate(Path(raw_temp))
            finalize_assets(
                assets=assets,
                build_facts_path=build_facts,
                validation_facts_path=validation,
            )
            summary_path = assets / SUMMARY_NAME
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["tag_state"] = "TAGGED"
            summary_path.write_text(json.dumps(summary), encoding="utf-8")
            checksum_path = assets / CHECKSUM_NAME
            checksum_path.write_text(
                "".join(
                    f"{asset_identity(assets / name)['sha256']}  {name}\n"
                    for name in (*PAYLOAD_NAMES, SUMMARY_NAME)
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ReleaseAssetError, "pre-tag"):
                verify_assets(assets)

    def test_finalize_refuses_to_overwrite_closed_assets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-overwrite-") as raw_temp:
            assets, build_facts, validation = prepare_candidate(Path(raw_temp))
            finalize_assets(
                assets=assets,
                build_facts_path=build_facts,
                validation_facts_path=validation,
            )
            with self.assertRaisesRegex(ReleaseAssetError, "pre-final asset set drifted"):
                finalize_assets(
                    assets=assets,
                    build_facts_path=build_facts,
                    validation_facts_path=validation,
                )

    def test_source_identity_rejects_asset_digest_as_commit_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-p4-source-id-") as raw_temp:
            with self.assertRaisesRegex(ReleaseAssetError, "40 lowercase"):
                source_identity(Path(raw_temp), "a" * 64)


if __name__ == "__main__":
    unittest.main()
