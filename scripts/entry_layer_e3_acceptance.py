from __future__ import annotations

import argparse
import copy
import gzip
import json
import os
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Sequence

if __package__:
    from . import entry_layer_e1_acceptance as common
else:  # pragma: no cover - exercised through the subprocess regression
    import entry_layer_e1_acceptance as common


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STARTER_VERSION = "0.2.0"
SKILL_VERSION = "0.2.0"
CORE_VERSION = common.CORE_VERSION
CORE_RELEASE_WHEEL_SHA256 = common.CORE_RELEASE_WHEEL_SHA256
RELEASE_SOURCE_DATE_EPOCH = 1787529600  # 2026-08-24T00:00:00Z
PRESETS = ("single-webapp", "static-site")
STARTER_ASSET_NAMES = (
    "veritrail_starter-0.2.0-py3-none-any.whl",
    "veritrail_starter-0.2.0.tar.gz",
    "starter-e3-validation-summary.json",
    "SHA256SUMS-starter.txt",
)
SKILL_ASSET_NAMES = (
    "veritrail-authoring-0.2.0.zip",
    "authoring-skill-e3-validation-summary.json",
    "SHA256SUMS-authoring-skill.txt",
)
FROZEN_E3_OFFICIAL_SKILL_VALIDATION = {
    "status": "PASS",
    "validator": "skill-creator/quick_validate.py",
}


def normalize_sdist(path: Path) -> None:
    """Rewrite a setuptools sdist with frozen, host-independent archive metadata."""

    normalized = path.with_name(f".{path.name}.normalized")
    try:
        with tarfile.open(path, mode="r:gz") as source:
            members = sorted(source.getmembers(), key=lambda item: item.name)
            with normalized.open("wb") as raw_output:
                with gzip.GzipFile(
                    filename="",
                    mode="wb",
                    compresslevel=9,
                    fileobj=raw_output,
                    mtime=RELEASE_SOURCE_DATE_EPOCH,
                ) as compressed_output:
                    with tarfile.open(
                        fileobj=compressed_output,
                        mode="w",
                        format=tarfile.PAX_FORMAT,
                    ) as target:
                        for original in members:
                            member = copy.copy(original)
                            member.uid = 0
                            member.gid = 0
                            member.uname = ""
                            member.gname = ""
                            member.mtime = RELEASE_SOURCE_DATE_EPOCH
                            member.pax_headers = {}
                            payload = source.extractfile(original) if original.isreg() else None
                            try:
                                target.addfile(member, payload)
                            finally:
                                if payload is not None:
                                    payload.close()
        normalized.replace(path)
    finally:
        normalized.unlink(missing_ok=True)


def installed_versions(python_executable: Path) -> dict[str, str]:
    command = (
        "import json; "
        "from importlib.metadata import version; "
        "from veritrail import __version__ as core; "
        "from veritrail_starter import __version__ as starter; "
        "print(json.dumps({'core': core, 'starter': starter, "
        "'core_metadata': version('veritrail'), "
        "'starter_metadata': version('veritrail-starter')}, sort_keys=True))"
    )
    result = common.one_json_line(
        common.run_command(
            [str(python_executable), "-I", "-c", command],
            cwd=REPOSITORY_ROOT,
        ),
        "installed version readback",
    )
    expected = {
        "core": CORE_VERSION,
        "starter": STARTER_VERSION,
        "core_metadata": CORE_VERSION,
        "starter_metadata": STARTER_VERSION,
    }
    common.require(result == expected, f"installed version drifted: {result!r}")
    return expected


def installed_schema_names(python_executable: Path) -> list[str]:
    command = (
        "import json; "
        "from importlib.resources import files; "
        "root = files('veritrail_starter').joinpath('schemas'); "
        "print(json.dumps(sorted(item.name for item in root.iterdir() "
        "if item.name.endswith('.schema.json'))))"
    )
    completed = common.run_command(
        [str(python_executable), "-I", "-c", command],
        cwd=REPOSITORY_ROOT,
    )
    try:
        observed = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise common.AcceptanceFailure("installed Schema readback emitted invalid JSON") from exc
    expected = ["answers-0.1.schema.json", "answers-0.2.schema.json"]
    common.require(observed == expected, f"installed Schema set drifted: {observed!r}")
    return expected


def build_artifacts(
    *,
    build_python: Path,
    output: Path,
    temp_root: Path,
    public_core_wheel: Path,
) -> dict[str, Path]:
    _, starter_source = common.copy_build_sources(temp_root)
    core_wheel = public_core_wheel.resolve(strict=True)
    common.require(
        core_wheel.name == f"veritrail-{CORE_VERSION}-py3-none-any.whl",
        "public Core wheel name drifted",
    )
    common.require(
        common.sha256_file(core_wheel) == CORE_RELEASE_WHEEL_SHA256,
        "public Core v0.12.0 wheel digest drifted",
    )

    previous_source_date_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    os.environ["SOURCE_DATE_EPOCH"] = str(RELEASE_SOURCE_DATE_EPOCH)
    try:
        common.run_command(
            [
                str(build_python),
                "-I",
                "-m",
                "pip",
                "wheel",
                "--no-deps",
                "--no-build-isolation",
                "--wheel-dir",
                str(output),
                str(starter_source),
            ],
            cwd=temp_root,
        )
        starter_wheel = common.single_match(
            output, f"veritrail_starter-{STARTER_VERSION}-*.whl", "Starter wheel"
        )

        sdist_command = (
            "from setuptools import build_meta; "
            f"print(build_meta.build_sdist({str(output)!r}))"
        )
        common.run_command(
            [str(build_python), "-I", "-c", sdist_command],
            cwd=starter_source,
        )
        starter_sdist = common.single_match(
            output, f"veritrail_starter-{STARTER_VERSION}.tar.gz", "Starter sdist"
        )
        normalize_sdist(starter_sdist)

        skill_zip = output / f"veritrail-authoring-{SKILL_VERSION}.zip"
        skill_result = common.one_json_line(
            common.run_command(
                [
                    str(build_python),
                    "-I",
                    str(common.SKILL_BUILDER),
                    "--build",
                    "--output",
                    str(skill_zip),
                ],
                cwd=REPOSITORY_ROOT,
            ),
            "Skill builder",
        )
    finally:
        if previous_source_date_epoch is None:
            os.environ.pop("SOURCE_DATE_EPOCH", None)
        else:
            os.environ["SOURCE_DATE_EPOCH"] = previous_source_date_epoch
    common.require(skill_result.get("state") == "PASS", "Skill builder did not pass")
    common.require(skill_result.get("version") == SKILL_VERSION, "Skill version drifted")
    return {
        "core_wheel": core_wheel,
        "starter_wheel": starter_wheel,
        "starter_sdist": starter_sdist,
        "skill_zip": skill_zip,
    }


def run_skill_acceptance(
    *,
    product_python: Path,
    skill_root: Path,
    preset: str,
    optimized: bool,
) -> dict[str, Any]:
    command = [
        str(sys.executable),
        "-I",
        str(common.SKILL_ACCEPTANCE),
        "--python",
        str(product_python),
        "--authoring-script",
        str(skill_root / "scripts" / "authoring.py"),
        "--preset",
        preset,
    ]
    if optimized:
        command.append("--optimized")
    result = common.one_json_line(
        common.run_command(command, cwd=REPOSITORY_ROOT),
        f"Authoring Skill {preset} release acceptance",
    )
    common.require(result.get("state") == "PASS", f"{preset} acceptance failed")
    common.require(result.get("preset") == preset, f"{preset} identity drifted")
    common.require(
        result.get("draft_equivalence") == "BYTE_IDENTICAL",
        f"{preset} DRAFT equivalence failed",
    )
    return result


def stable_preset_facts(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "optimized"}


def exercise_matrix(
    *,
    pythons: list[Path],
    labels: list[str],
    artifacts: dict[str, Path],
    skill_root: Path,
    temp_root: Path,
) -> list[dict[str, Any]]:
    matrix: list[dict[str, Any]] = []
    for index, (owner_python, version) in enumerate(zip(pythons, labels, strict=True)):
        wheel_python = common.install_product(
            owner_python=owner_python,
            environment_root=temp_root / f"wheel-env-{index}",
            core_wheel=artifacts["core_wheel"],
            starter_artifact=artifacts["starter_wheel"],
            with_browser_authoring=True,
        )
        sdist_python = common.install_product(
            owner_python=owner_python,
            environment_root=temp_root / f"sdist-env-{index}",
            core_wheel=artifacts["core_wheel"],
            starter_artifact=artifacts["starter_sdist"],
            with_browser_authoring=False,
        )
        preset_facts: dict[str, Any] = {}
        for preset in PRESETS:
            normal = run_skill_acceptance(
                product_python=wheel_python,
                skill_root=skill_root,
                preset=preset,
                optimized=False,
            )
            optimized = run_skill_acceptance(
                product_python=wheel_python,
                skill_root=skill_root,
                preset=preset,
                optimized=True,
            )
            common.require(
                stable_preset_facts(normal) == stable_preset_facts(optimized),
                f"{preset} normal and python -O release behavior diverged",
            )
            preset_facts[preset] = {
                "answers_schema_version": normal["answers_schema_version"],
                "draft": normal["draft"],
                "draft_equivalence": normal["draft_equivalence"],
                "draft_file_count": normal["draft_file_count"],
                "optimized_equivalence": "IDENTICAL",
                "boundary": normal["boundary"],
                "conflict": normal["conflict"],
            }
        matrix.append(
            {
                "python": version,
                "wheel_versions": installed_versions(wheel_python),
                "wheel_schemas": installed_schema_names(wheel_python),
                "sdist_versions": installed_versions(sdist_python),
                "sdist_schemas": installed_schema_names(sdist_python),
                "presets": preset_facts,
            }
        )
    return matrix


def require_release_python_series(labels: list[str]) -> None:
    observed = {common.python_series(label) for label in labels}
    common.require(
        observed == {(3, 10), (3, 13)},
        f"E3 candidate requires Python 3.10 and 3.13, observed {sorted(observed)}",
    )


def release_artifacts_from_directory(
    source: Path, core_wheel: Path
) -> tuple[dict[str, Path], dict[str, str]]:
    source = source.resolve(strict=True)
    common.require(source.is_dir(), "--from-assets must name a directory")
    observed_names = sorted(item.name for item in source.iterdir())
    expected_names = sorted((*STARTER_ASSET_NAMES, *SKILL_ASSET_NAMES))
    common.require(
        observed_names == expected_names,
        f"downloaded E3 asset set drifted: {observed_names}",
    )
    paths = {name: source / name for name in expected_names}
    common.require(
        all(path.is_file() and not path.is_symlink() for path in paths.values()),
        "downloaded E3 assets must be ordinary files",
    )
    core_wheel = core_wheel.resolve(strict=True)
    common.require(
        core_wheel.name == f"veritrail-{CORE_VERSION}-py3-none-any.whl",
        "public Core wheel name drifted",
    )
    common.require(
        common.sha256_file(core_wheel) == CORE_RELEASE_WHEEL_SHA256,
        "public Core v0.12.0 wheel digest drifted",
    )
    starter_payloads = tuple(paths[name] for name in STARTER_ASSET_NAMES[:-1])
    skill_payloads = tuple(paths[name] for name in SKILL_ASSET_NAMES[:-1])
    digests = {
        **common.verify_checksum_manifest(paths[STARTER_ASSET_NAMES[-1]], starter_payloads),
        **common.verify_checksum_manifest(paths[SKILL_ASSET_NAMES[-1]], skill_payloads),
    }
    return (
        {
            "core_wheel": core_wheel,
            "starter_wheel": paths[STARTER_ASSET_NAMES[0]],
            "starter_sdist": paths[STARTER_ASSET_NAMES[1]],
            "starter_summary": paths[STARTER_ASSET_NAMES[2]],
            "skill_zip": paths[SKILL_ASSET_NAMES[0]],
            "skill_summary": paths[SKILL_ASSET_NAMES[1]],
        },
        digests,
    )


def starter_summary(
    matrix: list[dict[str, Any]], *, core_wheel: Path
) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "product": "veritrail-starter",
        "version": STARTER_VERSION,
        "state": "PASS",
        "source_date_epoch": RELEASE_SOURCE_DATE_EPOCH,
        "core_version": CORE_VERSION,
        "core_wheel_sha256": common.sha256_file(core_wheel),
        "core_wheel_provenance": "PUBLIC_V0.12.0_RELEASE",
        "install_modes": ["wheel", "sdist"],
        "presets": list(PRESETS),
        "python_matrix": matrix,
    }


def skill_summary(
    matrix: list[dict[str, Any]], *, skill_zip: Path
) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "product": "veritrail-authoring",
        "version": SKILL_VERSION,
        "state": "PASS",
        "source_date_epoch": RELEASE_SOURCE_DATE_EPOCH,
        "archive_sha256": common.sha256_file(skill_zip),
        "official_validation": dict(FROZEN_E3_OFFICIAL_SKILL_VALIDATION),
        "authority": ["doctor", "init", "validate", "review"],
        "boundary": ["NOT_SEALED", "NOT_RUN", "NO_VERDICT"],
        "presets": list(PRESETS),
        "python_matrix": matrix,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build or read back the VeriTrail E3 0.2 entry-layer release assets."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--python",
        dest="pythons",
        type=Path,
        action="append",
        help="Python executable; candidate builds require one 3.10 and one 3.13.",
    )
    parser.add_argument("--official-validator", type=Path)
    parser.add_argument("--core-wheel", type=Path, required=True)
    parser.add_argument(
        "--from-assets",
        type=Path,
        help="Revalidate seven downloaded E3 Release assets instead of building candidates.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        requested_output = args.output.resolve(strict=False)
        common.require(not requested_output.exists(), "E3 acceptance refuses to overwrite output")
        pythons = [
            item.resolve(strict=True) for item in (args.pythons or [Path(sys.executable)])
        ]
        labels = [common.python_version(item) for item in pythons]
        common.require(len(labels) == len(set(labels)), "each --python must be distinct")
        source_assets = (
            args.from_assets.resolve(strict=True) if args.from_assets is not None else None
        )
        validator = (
            args.official_validator.resolve(strict=True)
            if args.official_validator is not None
            else None
        )
        if source_assets is None:
            require_release_python_series(labels)
            common.require(
                validator is not None,
                "candidate build requires --official-validator",
            )
        public_core_wheel = args.core_wheel.resolve(strict=True)

        with tempfile.TemporaryDirectory(prefix="veritrail-entry-e3-") as raw_temp:
            temp_root = Path(raw_temp).resolve()
            if source_assets is None:
                output = temp_root / "release-assets"
                output.mkdir()
                build_python = common.prepare_build_python(
                    pythons[0], temp_root / "build-environment"
                )
                artifacts = build_artifacts(
                    build_python=build_python,
                    output=output,
                    temp_root=temp_root,
                    public_core_wheel=public_core_wheel,
                )
                published_digests: dict[str, str] = {}
            else:
                output = temp_root / "readback"
                output.mkdir()
                artifacts, published_digests = release_artifacts_from_directory(
                    source_assets, public_core_wheel
                )

            extracted_skill = common.extract_skill(
                artifacts["skill_zip"], temp_root / "skill"
            )
            if validator is not None:
                official_validation = common.validate_officially(
                    owner_python=pythons[0],
                    validator=validator,
                    skill_root=extracted_skill,
                    environment_root=temp_root / "validator-env",
                )
                common.require(
                    official_validation == FROZEN_E3_OFFICIAL_SKILL_VALIDATION,
                    "official Skill validation identity drifted",
                )
            else:
                official_validation = dict(FROZEN_E3_OFFICIAL_SKILL_VALIDATION)

            matrix = exercise_matrix(
                pythons=pythons,
                labels=labels,
                artifacts=artifacts,
                skill_root=extracted_skill,
                temp_root=temp_root,
            )
            expected_starter = starter_summary(
                matrix, core_wheel=artifacts["core_wheel"]
            )
            expected_skill = skill_summary(matrix, skill_zip=artifacts["skill_zip"])

            if source_assets is None:
                starter_summary_path = output / STARTER_ASSET_NAMES[2]
                skill_summary_path = output / SKILL_ASSET_NAMES[1]
                common.write_json(starter_summary_path, expected_starter)
                common.write_json(skill_summary_path, expected_skill)
                (output / STARTER_ASSET_NAMES[3]).write_text(
                    common.checksums(
                        [
                            artifacts["starter_wheel"],
                            artifacts["starter_sdist"],
                            starter_summary_path,
                        ]
                    ),
                    encoding="utf-8",
                    newline="\n",
                )
                (output / SKILL_ASSET_NAMES[2]).write_text(
                    common.checksums([artifacts["skill_zip"], skill_summary_path]),
                    encoding="utf-8",
                    newline="\n",
                )
                result = {
                    "schema_version": "0.1",
                    "acceptance": "entry-layer-e3",
                    "state": "PASS",
                    "source_date_epoch": RELEASE_SOURCE_DATE_EPOCH,
                    "python_versions": labels,
                    "presets": list(PRESETS),
                    "official_skill_validation": official_validation["status"],
                    "starter_assets": list(STARTER_ASSET_NAMES),
                    "skill_assets": list(SKILL_ASSET_NAMES),
                }
            else:
                observed_starter = common.read_json_object(
                    artifacts["starter_summary"], "Starter validation summary"
                )
                observed_skill = common.read_json_object(
                    artifacts["skill_summary"], "Authoring Skill validation summary"
                )
                common.verify_release_summary(observed_starter, expected_starter, "Starter")
                common.verify_release_summary(observed_skill, expected_skill, "Skill")
                result = {
                    "schema_version": "0.1",
                    "acceptance": "entry-layer-e3-release-readback",
                    "state": "PASS",
                    "source_date_epoch": RELEASE_SOURCE_DATE_EPOCH,
                    "python_versions": labels,
                    "presets": list(PRESETS),
                    "official_skill_validation": official_validation["status"],
                    "asset_set": [*STARTER_ASSET_NAMES, *SKILL_ASSET_NAMES],
                    "payload_sha256": published_digests,
                    "summary_equivalence": "BYTE_IDENTICAL_FACTS",
                    "draft_equivalence": "BYTE_IDENTICAL",
                }
                common.write_json(output / "entry-layer-e3-readback-summary.json", result)

            requested_output.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(output), str(requested_output))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        print(f"E3 acceptance failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
