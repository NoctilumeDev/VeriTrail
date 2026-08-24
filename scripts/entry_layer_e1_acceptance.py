from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_BUILDER = REPOSITORY_ROOT / "scripts" / "build_authoring_skill.py"
SKILL_ACCEPTANCE = REPOSITORY_ROOT / "scripts" / "authoring_skill_acceptance.py"
STARTER_VERSION = "0.1.0"
SKILL_VERSION = "0.1.0"
CORE_VERSION = "0.12.0"
CORE_RELEASE_WHEEL_SHA256 = (
    "d0293f06e6a2b0271870ce032b2197c6ef7956db0ff3889230ca48234ff2fa45"
)
PLAYWRIGHT_VERSION = "1.62.0"
SETUPTOOLS_VERSION = "80.9.0"
WHEEL_VERSION = "0.45.1"
PYTHON_TIMEOUT_SECONDS = 300
STARTER_ASSET_NAMES = (
    "veritrail_starter-0.1.0-py3-none-any.whl",
    "veritrail_starter-0.1.0.tar.gz",
    "starter-e1-validation-summary.json",
    "SHA256SUMS-starter.txt",
)
SKILL_ASSET_NAMES = (
    "veritrail-authoring-0.1.0.zip",
    "authoring-skill-e1-validation-summary.json",
    "SHA256SUMS-authoring-skill.txt",
)
FROZEN_E1_OFFICIAL_SKILL_VALIDATION = {
    "status": "PASS",
    "validator": "skill-creator/quick_validate.py",
}


class AcceptanceFailure(RuntimeError):
    pass


def require(condition: object, message: str) -> None:
    if not condition:
        raise AcceptanceFailure(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, document: object) -> None:
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AcceptanceFailure(f"{label} is not valid UTF-8 JSON") from exc
    require(isinstance(document, dict), f"{label} must be one JSON object")
    return document


def run_command(
    command: list[str],
    *,
    cwd: Path,
    timeout: int = PYTHON_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONUTF8"] = "1"
    environment.pop("PYTHONPATH", None)
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=timeout,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if completed.returncode != 0:
        raise AcceptanceFailure(
            "command failed: "
            + " ".join(command[:4])
            + f"\nstdout: {completed.stdout[-4000:]}\nstderr: {completed.stderr[-4000:]}"
        )
    return completed


def one_json_line(completed: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    lines = completed.stdout.splitlines()
    require(len(lines) == 1, f"{label} did not emit exactly one JSON document")
    try:
        document = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise AcceptanceFailure(f"{label} emitted invalid JSON") from exc
    require(isinstance(document, dict), f"{label} output must be one object")
    return document


def python_version(python_executable: Path) -> str:
    completed = run_command(
        [str(python_executable), "-I", "-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))"],
        cwd=REPOSITORY_ROOT,
    )
    value = completed.stdout.strip()
    require(value.count(".") == 2, "Python version readback failed")
    return value


def venv_python(root: Path) -> Path:
    return root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def prepare_build_python(owner_python: Path, environment_root: Path) -> Path:
    run_command(
        [str(owner_python), "-I", "-m", "venv", str(environment_root)],
        cwd=REPOSITORY_ROOT,
    )
    build_python = venv_python(environment_root).resolve(strict=True)
    run_command(
        [
            str(build_python),
            "-I",
            "-m",
            "pip",
            "install",
            f"setuptools=={SETUPTOOLS_VERSION}",
            f"wheel=={WHEEL_VERSION}",
        ],
        cwd=REPOSITORY_ROOT,
    )
    return build_python


def copy_build_sources(temp_root: Path) -> tuple[Path, Path]:
    core_root = temp_root / "core-source"
    starter_root = temp_root / "starter-source"
    core_root.mkdir()
    for name in ("pyproject.toml", "README.md", "LICENSE"):
        shutil.copy2(REPOSITORY_ROOT / name, core_root / name)
    shutil.copytree(REPOSITORY_ROOT / "src", core_root / "src")

    def ignore_build_residue(_: str, names: list[str]) -> set[str]:
        ignored = {name for name in names if name == "__pycache__" or name.endswith(".egg-info")}
        ignored.update({"build", "dist"}.intersection(names))
        return ignored

    shutil.copytree(
        REPOSITORY_ROOT / "starter",
        starter_root,
        ignore=ignore_build_residue,
    )
    return core_root, starter_root


def single_match(root: Path, pattern: str, label: str) -> Path:
    matches = sorted(root.glob(pattern))
    require(len(matches) == 1, f"expected one {label}, found {[item.name for item in matches]}")
    return matches[0]


def build_artifacts(
    *,
    build_python: Path,
    output: Path,
    temp_root: Path,
    public_core_wheel: Path | None,
) -> dict[str, Path]:
    core_source, starter_source = copy_build_sources(temp_root)
    if public_core_wheel is None:
        core_wheel_root = temp_root / "core-wheel"
        core_wheel_root.mkdir()
        run_command(
            [
                str(build_python),
                "-I",
                "-m",
                "pip",
                "wheel",
                "--no-deps",
                "--no-build-isolation",
                "--wheel-dir",
                str(core_wheel_root),
                str(core_source),
            ],
            cwd=temp_root,
        )
        core_wheel = single_match(
            core_wheel_root, f"veritrail-{CORE_VERSION}-*.whl", "Core wheel"
        )
    else:
        core_wheel = public_core_wheel.resolve(strict=True)
        require(
            core_wheel.name == f"veritrail-{CORE_VERSION}-py3-none-any.whl",
            "public Core wheel name drifted",
        )
        require(
            sha256_file(core_wheel) == CORE_RELEASE_WHEEL_SHA256,
            "public Core v0.12.0 wheel digest drifted",
        )

    run_command(
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
    starter_wheel = single_match(
        output, f"veritrail_starter-{STARTER_VERSION}-*.whl", "Starter wheel"
    )

    sdist_command = (
        "from setuptools import build_meta; "
        f"print(build_meta.build_sdist({str(output)!r}))"
    )
    run_command(
        [str(build_python), "-I", "-c", sdist_command],
        cwd=starter_source,
    )
    starter_sdist = single_match(
        output, f"veritrail_starter-{STARTER_VERSION}.tar.gz", "Starter sdist"
    )

    skill_zip = output / f"veritrail-authoring-{SKILL_VERSION}.zip"
    skill_result = one_json_line(
        run_command(
            [
                str(build_python),
                "-I",
                str(SKILL_BUILDER),
                "--build",
                "--output",
                str(skill_zip),
            ],
            cwd=REPOSITORY_ROOT,
        ),
        "Skill builder",
    )
    require(skill_result.get("state") == "PASS", "Skill builder did not pass")
    return {
        "core_wheel": core_wheel,
        "starter_wheel": starter_wheel,
        "starter_sdist": starter_sdist,
        "skill_zip": skill_zip,
    }


def install_product(
    *,
    owner_python: Path,
    environment_root: Path,
    core_wheel: Path,
    starter_artifact: Path,
    with_browser_authoring: bool,
) -> Path:
    run_command(
        [str(owner_python), "-I", "-m", "venv", str(environment_root)],
        cwd=REPOSITORY_ROOT,
    )
    python_executable = venv_python(environment_root).resolve(strict=True)
    if starter_artifact.suffixes[-2:] == [".tar", ".gz"]:
        run_command(
            [
                str(python_executable),
                "-I",
                "-m",
                "pip",
                "install",
                f"setuptools=={SETUPTOOLS_VERSION}",
                f"wheel=={WHEEL_VERSION}",
            ],
            cwd=REPOSITORY_ROOT,
        )
    if with_browser_authoring:
        run_command(
            [
                str(python_executable),
                "-I",
                "-m",
                "pip",
                "install",
                f"playwright=={PLAYWRIGHT_VERSION}",
            ],
            cwd=REPOSITORY_ROOT,
        )
    run_command(
        [
            str(python_executable),
            "-I",
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-deps",
            str(core_wheel),
        ],
        cwd=REPOSITORY_ROOT,
    )
    starter_install = [
        str(python_executable),
        "-I",
        "-m",
        "pip",
        "install",
        "--no-index",
        "--no-deps",
    ]
    if starter_artifact.suffixes[-2:] == [".tar", ".gz"]:
        starter_install.append("--no-build-isolation")
    starter_install.append(str(starter_artifact))
    run_command(starter_install, cwd=REPOSITORY_ROOT)
    return python_executable


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
    result = one_json_line(
        run_command(
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
    require(result == expected, f"installed version drifted: {result!r}")
    return expected


def extract_skill(archive: Path, destination: Path) -> Path:
    destination.mkdir()
    destination_root = destination.resolve()
    with zipfile.ZipFile(archive, mode="r") as package:
        names: set[str] = set()
        for member in package.infolist():
            require(member.filename not in names, "Skill archive contains duplicate entries")
            names.add(member.filename)
            require(not member.is_dir(), "Skill archive contains an unexpected directory entry")
            unix_mode = member.external_attr >> 16
            require(
                unix_mode & 0o170000 != 0o120000,
                "Skill archive contains a symbolic link",
            )
            target = destination / member.filename
            resolved = target.resolve(strict=False)
            require(
                resolved == destination_root or destination_root in resolved.parents,
                "Skill archive escaped its destination",
            )
        package.extractall(destination)
    skill_root = destination / "veritrail-authoring"
    require((skill_root / "SKILL.md").is_file(), "extracted Skill is incomplete")
    return skill_root


def run_skill_acceptance(
    *, product_python: Path, skill_root: Path, optimized: bool
) -> dict[str, Any]:
    command = [
        str(sys.executable),
        "-I",
        str(SKILL_ACCEPTANCE),
        "--python",
        str(product_python),
        "--authoring-script",
        str(skill_root / "scripts" / "authoring.py"),
    ]
    if optimized:
        command.append("--optimized")
    result = one_json_line(
        run_command(command, cwd=REPOSITORY_ROOT),
        "Authoring Skill release acceptance",
    )
    require(result.get("state") == "PASS", "Authoring Skill release acceptance failed")
    require(result.get("draft_equivalence") == "BYTE_IDENTICAL", "DRAFT equivalence failed")
    return result


def validate_officially(
    *,
    owner_python: Path,
    validator: Path,
    skill_root: Path,
    environment_root: Path,
) -> dict[str, str]:
    run_command(
        [str(owner_python), "-I", "-m", "venv", str(environment_root)],
        cwd=REPOSITORY_ROOT,
    )
    validation_python = venv_python(environment_root).resolve(strict=True)
    run_command(
        [
            str(validation_python),
            "-I",
            "-m",
            "pip",
            "install",
            "PyYAML==6.0.2",
        ],
        cwd=REPOSITORY_ROOT,
    )
    completed = run_command(
        [str(validation_python), "-I", str(validator), str(skill_root)],
        cwd=REPOSITORY_ROOT,
    )
    require(completed.stdout.strip() == "Skill is valid!", "official Skill validator drifted")
    return {"status": "PASS", "validator": "skill-creator/quick_validate.py"}


def checksums(paths: list[Path]) -> str:
    return "".join(f"{sha256_file(path)}  {path.name}\n" for path in paths)


def verify_checksum_manifest(
    manifest: Path, expected_payloads: tuple[Path, ...]
) -> dict[str, str]:
    try:
        lines = manifest.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise AcceptanceFailure(f"invalid checksum manifest: {manifest.name}") from exc
    require(len(lines) == len(expected_payloads), "checksum manifest entry count drifted")
    result: dict[str, str] = {}
    for line, payload in zip(lines, expected_payloads, strict=True):
        parts = line.split("  ", maxsplit=1)
        require(len(parts) == 2, "checksum manifest line is malformed")
        digest, name = parts
        require(len(digest) == 64 and digest.isascii(), "checksum digest is malformed")
        require(
            all(character in "0123456789abcdef" for character in digest),
            "checksum digest is not lowercase SHA-256",
        )
        require(name == payload.name, "checksum manifest release order drifted")
        require(name not in result, "checksum manifest contains a duplicate asset")
        require(sha256_file(payload) == digest, f"checksum mismatch: {name}")
        result[name] = digest
    return result


def python_series(value: object) -> tuple[int, int]:
    require(isinstance(value, str), "Python version must be a string")
    parts = value.split(".")
    require(len(parts) == 3, f"Python version is malformed: {value!r}")
    try:
        numbers = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise AcceptanceFailure(f"Python version is malformed: {value!r}") from exc
    require(all(number >= 0 for number in numbers), "Python version cannot be negative")
    return numbers[0], numbers[1]


def verify_release_summary(
    observed: dict[str, Any], expected: dict[str, Any], label: str
) -> None:
    observed_top = dict(observed)
    expected_top = dict(expected)
    observed_matrix = observed_top.pop("python_matrix", None)
    expected_matrix = expected_top.pop("python_matrix", None)
    require(observed_top == expected_top, f"downloaded {label} summary metadata drifted")
    require(isinstance(observed_matrix, list), f"downloaded {label} matrix is malformed")
    require(isinstance(expected_matrix, list), f"current {label} matrix is malformed")

    observed_by_series: dict[tuple[int, int], dict[str, Any]] = {}
    for entry in observed_matrix:
        require(isinstance(entry, dict), f"downloaded {label} matrix entry is malformed")
        series = python_series(entry.get("python"))
        require(series not in observed_by_series, f"downloaded {label} matrix repeats Python {series}")
        observed_by_series[series] = entry

    for current_entry in expected_matrix:
        require(isinstance(current_entry, dict), f"current {label} matrix entry is malformed")
        series = python_series(current_entry.get("python"))
        released_entry = observed_by_series.get(series)
        require(released_entry is not None, f"downloaded {label} matrix lacks Python {series}")
        released_facts = dict(released_entry)
        current_facts = dict(current_entry)
        released_facts.pop("python", None)
        current_facts.pop("python", None)
        require(
            released_facts == current_facts,
            f"downloaded {label} facts drifted for Python {series[0]}.{series[1]}",
        )


def release_artifacts_from_directory(
    source: Path, core_wheel: Path
) -> tuple[dict[str, Path], dict[str, str]]:
    source = source.resolve(strict=True)
    require(source.is_dir(), "--from-assets must name a directory")
    observed_names = sorted(item.name for item in source.iterdir())
    expected_names = sorted((*STARTER_ASSET_NAMES, *SKILL_ASSET_NAMES))
    require(observed_names == expected_names, f"downloaded E1 asset set drifted: {observed_names}")
    paths = {name: source / name for name in expected_names}
    require(all(path.is_file() and not path.is_symlink() for path in paths.values()), "downloaded E1 assets must be ordinary files")
    core_wheel = core_wheel.resolve(strict=True)
    require(
        core_wheel.name == f"veritrail-{CORE_VERSION}-py3-none-any.whl",
        "public Core wheel name drifted",
    )
    require(
        sha256_file(core_wheel) == CORE_RELEASE_WHEEL_SHA256,
        "public Core v0.12.0 wheel digest drifted",
    )
    starter_payloads = tuple(paths[name] for name in STARTER_ASSET_NAMES[:-1])
    skill_payloads = tuple(paths[name] for name in SKILL_ASSET_NAMES[:-1])
    digests = {
        **verify_checksum_manifest(paths[STARTER_ASSET_NAMES[-1]], starter_payloads),
        **verify_checksum_manifest(paths[SKILL_ASSET_NAMES[-1]], skill_payloads),
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
        wheel_python = install_product(
            owner_python=owner_python,
            environment_root=temp_root / f"wheel-env-{index}",
            core_wheel=artifacts["core_wheel"],
            starter_artifact=artifacts["starter_wheel"],
            with_browser_authoring=True,
        )
        sdist_python = install_product(
            owner_python=owner_python,
            environment_root=temp_root / f"sdist-env-{index}",
            core_wheel=artifacts["core_wheel"],
            starter_artifact=artifacts["starter_sdist"],
            with_browser_authoring=False,
        )
        normal = run_skill_acceptance(
            product_python=wheel_python,
            skill_root=skill_root,
            optimized=False,
        )
        optimized = run_skill_acceptance(
            product_python=wheel_python,
            skill_root=skill_root,
            optimized=True,
        )
        require(
            {key: value for key, value in normal.items() if key != "optimized"}
            == {key: value for key, value in optimized.items() if key != "optimized"},
            "normal and python -O release behavior diverged",
        )
        matrix.append(
            {
                "python": version,
                "wheel_versions": installed_versions(wheel_python),
                "sdist_versions": installed_versions(sdist_python),
                "draft": normal["draft"],
                "draft_equivalence": normal["draft_equivalence"],
                "optimized_equivalence": "IDENTICAL",
                "boundary": normal["boundary"],
                "conflict": normal["conflict"],
            }
        )
    return matrix


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and clean-install the VeriTrail E1 entry-layer release candidates."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--python",
        dest="pythons",
        type=Path,
        action="append",
        help="Python executable to validate; repeat for the dual-Python matrix.",
    )
    parser.add_argument(
        "--official-validator",
        type=Path,
        help="Official skill-creator quick_validate.py; validated in an isolated environment.",
    )
    parser.add_argument(
        "--core-wheel",
        type=Path,
        help=(
            "Downloaded Core v0.12.0 release wheel. When supplied, its fixed public "
            "release digest is verified and no Core wheel is rebuilt."
        ),
    )
    parser.add_argument(
        "--from-assets",
        type=Path,
        help=(
            "Revalidate the seven downloaded E1 Release assets instead of building new "
            "ones. --core-wheel is required and --output receives a readback report."
        ),
    )
    return parser.parse_args(argv)


def starter_summary(
    matrix: list[dict[str, Any]], *, core_wheel: Path, provenance: str
) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "product": "veritrail-starter",
        "version": STARTER_VERSION,
        "state": "PASS",
        "core_version": CORE_VERSION,
        "core_wheel_sha256": sha256_file(core_wheel),
        "core_wheel_provenance": provenance,
        "install_modes": ["wheel", "sdist"],
        "python_matrix": matrix,
    }


def skill_summary(
    matrix: list[dict[str, Any]], *, skill_zip: Path, official_validation: dict[str, str]
) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "product": "veritrail-authoring",
        "version": SKILL_VERSION,
        "state": "PASS",
        "archive_sha256": sha256_file(skill_zip),
        "official_validation": official_validation,
        "authority": ["doctor", "init", "validate", "review"],
        "python_matrix": matrix,
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        requested_output = args.output.resolve(strict=False)
        require(not requested_output.exists(), "E1 acceptance refuses to overwrite its output")
        pythons = [
            item.resolve(strict=True)
            for item in (args.pythons or [Path(sys.executable)])
        ]
        labels = [python_version(item) for item in pythons]
        require(
            len(labels) == len(set(labels)),
            "each --python must name a distinct Python version",
        )
        validator = (
            args.official_validator.resolve(strict=True)
            if args.official_validator is not None
            else None
        )
        public_core_wheel = (
            args.core_wheel.resolve(strict=True) if args.core_wheel is not None else None
        )
        source_assets = (
            args.from_assets.resolve(strict=True) if args.from_assets is not None else None
        )
        if source_assets is not None:
            require(public_core_wheel is not None, "--from-assets requires --core-wheel")

        with tempfile.TemporaryDirectory(prefix="veritrail-entry-e1-") as raw_temp:
            temp_root = Path(raw_temp).resolve()
            if source_assets is None:
                output = temp_root / "release-assets"
                output.mkdir()
                build_python = prepare_build_python(
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
            extracted_skill = extract_skill(artifacts["skill_zip"], temp_root / "skill")
            if validator is not None:
                official_validation = validate_officially(
                    owner_python=pythons[0],
                    validator=validator,
                    skill_root=extracted_skill,
                    environment_root=temp_root / "validator-env",
                )
            elif source_assets is not None:
                # The immutable E1 checksum manifests bind both the published
                # package and its validation summary.  CI still clean-installs
                # and exercises those payloads below; this frozen field records
                # the official validation already performed for that release.
                official_validation = dict(FROZEN_E1_OFFICIAL_SKILL_VALIDATION)
            else:
                official_validation = {
                    "status": "NOT_REQUESTED",
                    "validator": "skill-creator/quick_validate.py",
                }
            matrix = exercise_matrix(
                pythons=pythons,
                labels=labels,
                artifacts=artifacts,
                skill_root=extracted_skill,
                temp_root=temp_root,
            )
            expected_starter = starter_summary(
                matrix,
                core_wheel=artifacts["core_wheel"],
                provenance=(
                    "PUBLIC_V0.12.0_RELEASE"
                    if public_core_wheel is not None
                    else "BUILT_FROM_FROZEN_SOURCE"
                ),
            )
            expected_skill = skill_summary(
                matrix,
                skill_zip=artifacts["skill_zip"],
                official_validation=official_validation,
            )

            if source_assets is None:
                starter_summary_path = output / STARTER_ASSET_NAMES[2]
                skill_summary_path = output / SKILL_ASSET_NAMES[1]
                write_json(starter_summary_path, expected_starter)
                write_json(skill_summary_path, expected_skill)
                (output / STARTER_ASSET_NAMES[3]).write_text(
                    checksums(
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
                    checksums([artifacts["skill_zip"], skill_summary_path]),
                    encoding="utf-8",
                    newline="\n",
                )
                result = {
                    "schema_version": "0.1",
                    "acceptance": "entry-layer-e1",
                    "state": "PASS",
                    "python_versions": labels,
                    "official_skill_validation": official_validation["status"],
                    "starter_assets": list(STARTER_ASSET_NAMES),
                    "skill_assets": list(SKILL_ASSET_NAMES),
                }
            else:
                observed_starter = read_json_object(
                    artifacts["starter_summary"], "Starter validation summary"
                )
                observed_skill = read_json_object(
                    artifacts["skill_summary"], "Authoring Skill validation summary"
                )
                verify_release_summary(observed_starter, expected_starter, "Starter")
                verify_release_summary(observed_skill, expected_skill, "Skill")
                result = {
                    "schema_version": "0.1",
                    "acceptance": "entry-layer-e1-release-readback",
                    "state": "PASS",
                    "python_versions": labels,
                    "official_skill_validation": official_validation["status"],
                    "asset_set": [*STARTER_ASSET_NAMES, *SKILL_ASSET_NAMES],
                    "payload_sha256": published_digests,
                    "summary_equivalence": "BYTE_IDENTICAL_FACTS",
                    "draft_equivalence": "BYTE_IDENTICAL",
                }
                write_json(output / "entry-layer-e1-readback-summary.json", result)
            requested_output.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(output), str(requested_output))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        print(f"E1 acceptance failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
