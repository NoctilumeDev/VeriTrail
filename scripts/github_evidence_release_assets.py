from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


DISTRIBUTION = "veritrail-github-evidence"
IMPORT_PACKAGE = "veritrail_github"
VERSION = "0.1.0"
CORE_REQUIREMENT = "veritrail==0.12.2"
RENDER_REQUIREMENT = "playwright==1.62.0"
WHEEL_NAME = "veritrail_github_evidence-0.1.0-py3-none-any.whl"
SDIST_NAME = "veritrail_github_evidence-0.1.0.tar.gz"
SUMMARY_NAME = "github-evidence-v0.1.0-validation-summary.json"
CHECKSUM_NAME = "SHA256SUMS-github-evidence.txt"
PAYLOAD_NAMES = (WHEEL_NAME, SDIST_NAME)
ASSET_NAMES = (*PAYLOAD_NAMES, SUMMARY_NAME, CHECKSUM_NAME)
READ_CHUNK_BYTES = 64 * 1024
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


class ReleaseAssetError(RuntimeError):
    pass


def require(condition: object, message: str) -> None:
    if not condition:
        raise ReleaseAssetError(message)


def require_exact_keys(
    value: Mapping[str, Any], expected: set[str], label: str
) -> None:
    require(
        set(value) == expected,
        f"{label} contains missing or undeclared fields",
    )


def require_positive_integer(value: object, label: str) -> int:
    require(
        isinstance(value, int) and not isinstance(value, bool) and value > 0,
        f"{label} must be a positive integer",
    )
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            chunk = source.read(READ_CHUNK_BYTES)
            if not chunk:
                return digest.hexdigest()
            digest.update(chunk)


def asset_identity(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"release payload is not an ordinary file: {path.name}")
    return {
        "filename": path.name,
        "size": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReleaseAssetError(f"{label} is not valid UTF-8 JSON") from exc
    require(isinstance(value, dict), f"{label} must be one JSON object")
    return value


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def run_command(
    command: Sequence[str],
    *,
    cwd: Path,
    environment: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env.pop("PYTHONPATH", None)
    if environment is not None:
        env.update(environment)
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=300,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise ReleaseAssetError(
            f"command failed ({completed.returncode}): {' '.join(command)}"
            + (f"\n{detail}" if detail else "")
        )
    return completed


def git_value(repository_root: Path, *arguments: str) -> str:
    return run_command(
        ("git", *arguments), cwd=repository_root
    ).stdout.strip()


def source_identity(repository_root: Path, expected_commit: str) -> dict[str, Any]:
    # Git SHA-1 repositories use a 40-character object name. Keep this separate
    # from the 64-character asset digest validator above.
    require(
        re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
        "expected commit must be 40 lowercase hex characters",
    )
    head = git_value(repository_root, "rev-parse", "HEAD")
    require(head == expected_commit, f"source HEAD drifted: {head}")
    status = git_value(
        repository_root, "status", "--porcelain=v1", "--untracked-files=all"
    )
    require(not status, "release source worktree is not clean")
    return {
        "commit": head,
        "tree": git_value(repository_root, "show", "-s", "--format=%T", "HEAD"),
        "commit_timestamp": git_value(
            repository_root, "show", "-s", "--format=%cI", "HEAD"
        ),
        "source_date_epoch": int(
            git_value(repository_root, "show", "-s", "--format=%ct", "HEAD")
        ),
        "worktree_clean": True,
    }


def _canonical_distribution_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _metadata_fields(payload: bytes, label: str) -> dict[str, Any]:
    message = BytesParser().parsebytes(payload)
    name = message.get("Name")
    version = message.get("Version")
    requires_python = message.get("Requires-Python")
    requirements = message.get_all("Requires-Dist") or []
    extras = message.get_all("Provides-Extra") or []
    require(
        isinstance(name, str)
        and _canonical_distribution_name(name) == DISTRIBUTION,
        f"{label} distribution name drifted",
    )
    require(version == VERSION, f"{label} version drifted")
    require(requires_python == ">=3.10", f"{label} Python declaration drifted")
    require(CORE_REQUIREMENT in requirements, f"{label} Core dependency drifted")
    require("render" in extras, f"{label} render extra is missing")
    require(
        any(
            requirement.startswith(RENDER_REQUIREMENT)
            and "extra == \"render\"" in requirement
            for requirement in requirements
        ),
        f"{label} render dependency drifted",
    )
    return {
        "name": name,
        "version": version,
        "requires_python": requires_python,
        "requires_dist": requirements,
        "provides_extra": extras,
    }


def _require_safe_archive_name(name: str, label: str) -> None:
    path = PurePosixPath(name)
    require(name != "", f"{label} contains an empty member name")
    require("\\" not in name, f"{label} contains a non-POSIX member name")
    require(not path.is_absolute(), f"{label} contains an absolute member name")
    require(
        all(part not in ("", ".", "..") for part in path.parts),
        f"{label} contains an unsafe member name",
    )


def inspect_wheel(path: Path) -> dict[str, Any]:
    require(path.name == WHEEL_NAME, "wheel filename drifted")
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            require(len(names) == len(set(names)), "wheel contains duplicate members")
            for info in archive.infolist():
                _require_safe_archive_name(info.filename.rstrip("/"), "wheel")
                unix_mode = info.external_attr >> 16
                require(
                    not (info.create_system == 3 and (unix_mode & 0o170000) == 0o120000),
                    "wheel contains a symbolic link",
                )
            metadata_names = [
                name for name in names if name.endswith(".dist-info/METADATA")
            ]
            require(len(metadata_names) == 1, "wheel must contain one METADATA")
            require(
                all(
                    "playwright" not in name.lower()
                    and "chromium" not in name.lower()
                    for name in names
                ),
                "wheel contains browser payloads",
            )
            metadata = _metadata_fields(
                archive.read(metadata_names[0]), "wheel METADATA"
            )
    except (OSError, zipfile.BadZipFile, KeyError) as exc:
        raise ReleaseAssetError("wheel is not a readable distribution archive") from exc
    return {"members": len(names), "metadata": metadata}


def inspect_sdist(path: Path) -> dict[str, Any]:
    require(path.name == SDIST_NAME, "sdist filename drifted")
    root = f"veritrail_github_evidence-{VERSION}"
    prefix = f"{root}/"
    try:
        with tarfile.open(path, mode="r:gz") as archive:
            members = archive.getmembers()
            names = [member.name for member in members]
            require(names, "sdist is empty")
            require(len(names) == len(set(names)), "sdist contains duplicate members")
            for member in members:
                _require_safe_archive_name(member.name.rstrip("/"), "sdist")
                require(
                    member.name == root or member.name.startswith(prefix),
                    "sdist root drifted",
                )
                require(
                    not (member.issym() or member.islnk()),
                    "sdist contains a link member",
                )
            metadata_names = [name for name in names if name == f"{prefix}PKG-INFO"]
            require(len(metadata_names) == 1, "sdist must contain one root PKG-INFO")
            extracted = archive.extractfile(metadata_names[0])
            require(extracted is not None, "sdist PKG-INFO is not a file")
            with extracted:
                metadata = _metadata_fields(extracted.read(), "sdist PKG-INFO")
            require(
                all(
                    "playwright" not in name.lower()
                    and "chromium" not in name.lower()
                    for name in names
                ),
                "sdist contains browser payloads",
            )
    except (OSError, tarfile.TarError, KeyError) as exc:
        raise ReleaseAssetError("sdist is not a readable distribution archive") from exc
    return {"members": len(members), "metadata": metadata}


def normalize_sdist(path: Path, source_date_epoch: int) -> None:
    normalized = path.with_name(f".{path.name}.normalized")
    try:
        with tarfile.open(path, mode="r:gz") as source:
            members = sorted(source.getmembers(), key=lambda item: item.name)
            with normalized.open("xb") as raw_output:
                with gzip.GzipFile(
                    filename="",
                    mode="wb",
                    compresslevel=9,
                    fileobj=raw_output,
                    mtime=source_date_epoch,
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
                            member.mtime = source_date_epoch
                            member.pax_headers = {}
                            payload = (
                                source.extractfile(original)
                                if original.isreg()
                                else None
                            )
                            try:
                                target.addfile(member, payload)
                            finally:
                                if payload is not None:
                                    payload.close()
        os.replace(normalized, path)
    finally:
        normalized.unlink(missing_ok=True)


def validate_source_contract(
    repository_root: Path, build_python: Path
) -> dict[str, Any]:
    pyproject_path = repository_root / "plugins" / "github-evidence" / "pyproject.toml"
    probe = (
        "import json, pathlib, sys, tomllib; "
        "document = tomllib.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')); "
        "print(json.dumps(document.get('project'), sort_keys=True))"
    )
    completed = run_command(
        (str(build_python), "-I", "-c", probe, str(pyproject_path)),
        cwd=repository_root,
    )
    try:
        project = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ReleaseAssetError("plugin pyproject probe did not return JSON") from exc
    require(isinstance(project, dict), "plugin pyproject has no project table")
    require(project.get("name") == DISTRIBUTION, "pyproject distribution drifted")
    require(project.get("version") == VERSION, "pyproject version drifted")
    require(project.get("requires-python") == ">=3.10", "pyproject Python declaration drifted")
    require(project.get("dependencies") == [CORE_REQUIREMENT], "pyproject Core dependency drifted")
    optional = project.get("optional-dependencies")
    require(isinstance(optional, dict), "pyproject optional dependencies are missing")
    require(optional.get("render") == [RENDER_REQUIREMENT], "pyproject render extra drifted")
    scripts = project.get("scripts")
    require(
        isinstance(scripts, dict)
        and scripts.get("veritrail-github-collect") == "veritrail_github.cli:main",
        "plugin CLI entry point drifted",
    )
    init_path = repository_root / "plugins" / "github-evidence" / "src" / IMPORT_PACKAGE / "__init__.py"
    require(
        f'__version__ = "{VERSION}"' in init_path.read_text(encoding="utf-8"),
        "import package version drifted",
    )
    return {
        "distribution": DISTRIBUTION,
        "import_package": IMPORT_PACKAGE,
        "version": VERSION,
        "requires_python": ">=3.10",
        "core_dependency": CORE_REQUIREMENT,
        "render_extra": [RENDER_REQUIREMENT],
        "cli": "veritrail-github-collect",
    }


def build_toolchain(build_python: Path) -> dict[str, str]:
    command = (
        "import json, platform, sys; "
        "from importlib.metadata import version; "
        "print(json.dumps({"
        "'python': platform.python_version(), "
        "'implementation': platform.python_implementation(), "
        "'pip': version('pip'), "
        "'build': version('build'), "
        "'setuptools': version('setuptools'), "
        "'wheel': version('wheel')}, sort_keys=True))"
    )
    completed = run_command((str(build_python), "-I", "-c", command), cwd=build_python.parent)
    value = json.loads(completed.stdout)
    require(isinstance(value, dict), "build toolchain probe did not return an object")
    return {str(key): str(item) for key, item in value.items()}


def _build_once(
    *,
    repository_root: Path,
    build_python: Path,
    destination: Path,
    source_date_epoch: int,
) -> dict[str, Any]:
    source = destination.parent / f"{destination.name}-source"
    shutil.copytree(repository_root / "plugins" / "github-evidence", source)
    destination.mkdir()
    run_command(
        (
            str(build_python),
            "-I",
            "-m",
            "build",
            "--wheel",
            "--sdist",
            "--no-isolation",
            "--outdir",
            str(destination),
            str(source),
        ),
        cwd=repository_root,
        environment={"SOURCE_DATE_EPOCH": str(source_date_epoch)},
    )
    observed = {path.name for path in destination.iterdir() if path.is_file()}
    require(observed == set(PAYLOAD_NAMES), f"built payload set drifted: {sorted(observed)}")
    normalize_sdist(destination / SDIST_NAME, source_date_epoch)
    return {
        WHEEL_NAME: asset_identity(destination / WHEEL_NAME),
        SDIST_NAME: asset_identity(destination / SDIST_NAME),
    }


def build_payloads(
    *,
    repository_root: Path,
    output: Path,
    build_facts_path: Path,
    build_python: Path,
    expected_commit: str,
) -> dict[str, Any]:
    require(not output.exists(), "candidate output already exists")
    require(not build_facts_path.exists(), "build facts already exist")
    require(build_facts_path.parent.is_dir(), "build facts parent does not exist")
    require(build_python.is_file(), "build Python does not exist")
    source = source_identity(repository_root, expected_commit)
    distribution = validate_source_contract(repository_root, build_python)
    toolchain = build_toolchain(build_python)
    with tempfile.TemporaryDirectory(
        prefix="veritrail-github-release-build-", dir=output.parent
    ) as raw_temp:
        temp_root = Path(raw_temp)
        first = _build_once(
            repository_root=repository_root,
            build_python=build_python,
            destination=temp_root / "build-1",
            source_date_epoch=source["source_date_epoch"],
        )
        second = _build_once(
            repository_root=repository_root,
            build_python=build_python,
            destination=temp_root / "build-2",
            source_date_epoch=source["source_date_epoch"],
        )
        require(first == second, "normalized double build was not byte-identical")
        inspect_wheel(temp_root / "build-1" / WHEEL_NAME)
        inspect_sdist(temp_root / "build-1" / SDIST_NAME)
        staging = temp_root / "candidate-assets"
        staging.mkdir()
        for name in PAYLOAD_NAMES:
            shutil.copy2(temp_root / "build-1" / name, staging / name)
        shutil.move(str(staging), str(output))
    facts = {
        "schema_version": "0.1",
        "state": "CANDIDATE_PAYLOADS_BUILT",
        "source": source,
        "distribution": distribution,
        "toolchain": toolchain,
        "build_comparison": {
            "build_count": 2,
            "source_copy_per_build": True,
            "wheel_byte_identical": True,
            "sdist_normalized_byte_identical": True,
        },
        "payloads": {
            name: asset_identity(output / name) for name in PAYLOAD_NAMES
        },
        "release_state": "PRE_TAG",
        "public_download_claim": "NONE",
    }
    build_facts_path.write_bytes(canonical_json_bytes(facts))
    return facts


def validate_validation_facts(
    document: Mapping[str, Any], source_commit: str
) -> dict[str, Any]:
    expected_top_level = {
        "schema_version",
        "state",
        "source_commit",
        "public_ci",
        "browser_smoke",
        "local_matrix",
    }
    require_exact_keys(document, expected_top_level, "validation facts")
    require(document.get("schema_version") == "0.1", "validation facts schema drifted")
    require(document.get("state") == "PUBLIC_GATES_GREEN", "public gates are not green")
    require(document.get("source_commit") == source_commit, "validation facts source drifted")
    public_ci = document.get("public_ci")
    require(isinstance(public_ci, dict), "validation facts have no Public CI object")
    require_exact_keys(
        public_ci,
        {"run_id", "head_sha", "attempt", "jobs", "status"},
        "Public CI facts",
    )
    require_positive_integer(public_ci.get("run_id"), "Public CI run identity")
    require(public_ci.get("head_sha") == source_commit, "Public CI source drifted")
    require(public_ci.get("status") == "SUCCESS", "Public CI did not succeed")
    require(
        require_positive_integer(public_ci.get("attempt"), "Public CI attempt") == 1,
        "Public CI was not the original attempt",
    )
    require(
        require_positive_integer(public_ci.get("jobs"), "Public CI job count") == 11,
        "Public CI job count drifted",
    )
    browser = document.get("browser_smoke")
    require(isinstance(browser, dict), "validation facts have no Browser Smoke object")
    require_exact_keys(
        browser,
        {"run_id", "head_sha", "attempt", "jobs", "status"},
        "Browser Smoke facts",
    )
    require_positive_integer(browser.get("run_id"), "Browser Smoke run identity")
    require(browser.get("head_sha") == source_commit, "Browser Smoke source drifted")
    require(browser.get("status") == "SUCCESS", "Browser Smoke did not succeed")
    require(
        require_positive_integer(browser.get("attempt"), "Browser Smoke attempt") == 1,
        "Browser Smoke was not the original attempt",
    )
    require(
        require_positive_integer(browser.get("jobs"), "Browser Smoke job count") == 1,
        "Browser Smoke job count drifted",
    )
    local = document.get("local_matrix")
    require(isinstance(local, dict), "validation facts have no local matrix")
    required = (
        "normal_and_optimized_regression",
        "base_wheel",
        "sdist",
        "render_extra",
        "p3_uninstall_core_readback",
        "real_github_pass",
        "cleanup",
    )
    require_exact_keys(
        local,
        {"status", "python_series", *required},
        "local release matrix",
    )
    require(local.get("status") == "PASS", "local release matrix did not pass")
    require(local.get("python_series") == ["3.10", "3.13"], "verified Python series drifted")
    require(
        all(local.get(name) == "PASS" for name in required),
        "local release matrix is incomplete",
    )
    # Return a fresh, explicitly shaped object. The release summary never
    # republishes arbitrary caller fields such as local paths, logs or tokens.
    return {
        "schema_version": "0.1",
        "state": "PUBLIC_GATES_GREEN",
        "source_commit": source_commit,
        "public_ci": dict(public_ci),
        "browser_smoke": dict(browser),
        "local_matrix": {
            "status": "PASS",
            "python_series": ["3.10", "3.13"],
            **{name: "PASS" for name in required},
        },
    }


def _validate_asset_record(
    value: object, expected_name: str, label: str
) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    require_exact_keys(value, {"filename", "size", "sha256"}, label)
    require(value.get("filename") == expected_name, f"{label} filename drifted")
    size = require_positive_integer(value.get("size"), f"{label} size")
    digest = value.get("sha256")
    require(
        isinstance(digest, str) and SHA256_PATTERN.fullmatch(digest) is not None,
        f"{label} digest is invalid",
    )
    return {"filename": expected_name, "size": size, "sha256": digest}


def _validate_recorded_source(value: object) -> dict[str, Any]:
    require(isinstance(value, dict), "recorded source is not an object")
    require_exact_keys(
        value,
        {
            "commit",
            "tree",
            "commit_timestamp",
            "source_date_epoch",
            "worktree_clean",
        },
        "recorded source",
    )
    commit = value.get("commit")
    tree = value.get("tree")
    timestamp = value.get("commit_timestamp")
    require(
        isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        "recorded source commit is invalid",
    )
    require(
        isinstance(tree, str) and re.fullmatch(r"[0-9a-f]{40}", tree) is not None,
        "recorded source tree is invalid",
    )
    require(
        isinstance(timestamp, str) and timestamp,
        "recorded source timestamp is invalid",
    )
    epoch = require_positive_integer(
        value.get("source_date_epoch"), "recorded source epoch"
    )
    require(value.get("worktree_clean") is True, "recorded source was not clean")
    return {
        "commit": commit,
        "tree": tree,
        "commit_timestamp": timestamp,
        "source_date_epoch": epoch,
        "worktree_clean": True,
    }


def _validate_recorded_distribution(value: object) -> dict[str, Any]:
    require(isinstance(value, dict), "recorded distribution is not an object")
    expected = {
        "distribution": DISTRIBUTION,
        "import_package": IMPORT_PACKAGE,
        "version": VERSION,
        "requires_python": ">=3.10",
        "core_dependency": CORE_REQUIREMENT,
        "render_extra": [RENDER_REQUIREMENT],
        "cli": "veritrail-github-collect",
    }
    require(value == expected, "recorded distribution contract drifted")
    return dict(expected)


def _validate_recorded_toolchain(value: object) -> dict[str, str]:
    require(isinstance(value, dict), "recorded toolchain is not an object")
    expected_keys = {"python", "implementation", "pip", "build", "setuptools", "wheel"}
    require_exact_keys(value, expected_keys, "recorded toolchain")
    require(
        all(isinstance(item, str) and item for item in value.values()),
        "recorded toolchain values are invalid",
    )
    require(value.get("implementation") == "CPython", "build implementation drifted")
    return {key: value[key] for key in sorted(expected_keys)}


def _validate_build_comparison(value: object) -> dict[str, Any]:
    expected = {
        "build_count": 2,
        "source_copy_per_build": True,
        "wheel_byte_identical": True,
        "sdist_normalized_byte_identical": True,
    }
    require(value == expected, "double-build comparison drifted")
    return dict(expected)


def validate_build_facts(
    document: Mapping[str, Any], observed_payloads: Mapping[str, Any]
) -> dict[str, Any]:
    require_exact_keys(
        document,
        {
            "schema_version",
            "state",
            "source",
            "distribution",
            "toolchain",
            "build_comparison",
            "payloads",
            "release_state",
            "public_download_claim",
        },
        "build facts",
    )
    require(document.get("schema_version") == "0.1", "build facts schema drifted")
    require(document.get("state") == "CANDIDATE_PAYLOADS_BUILT", "build facts state drifted")
    require(document.get("release_state") == "PRE_TAG", "build facts tag state drifted")
    require(
        document.get("public_download_claim") == "NONE",
        "build facts overstate public download",
    )
    source = _validate_recorded_source(document.get("source"))
    distribution = _validate_recorded_distribution(document.get("distribution"))
    toolchain = _validate_recorded_toolchain(document.get("toolchain"))
    comparison = _validate_build_comparison(document.get("build_comparison"))
    payload_document = document.get("payloads")
    require(isinstance(payload_document, dict), "build payload facts are not an object")
    require_exact_keys(payload_document, set(PAYLOAD_NAMES), "build payload facts")
    payloads = {
        name: _validate_asset_record(payload_document.get(name), name, f"build payload {name}")
        for name in PAYLOAD_NAMES
    }
    require(payloads == observed_payloads, "candidate payloads drifted after build")
    return {
        "schema_version": "0.1",
        "state": "CANDIDATE_PAYLOADS_BUILT",
        "source": source,
        "distribution": distribution,
        "toolchain": toolchain,
        "build_comparison": comparison,
        "payloads": payloads,
        "release_state": "PRE_TAG",
        "public_download_claim": "NONE",
    }


def _verify_payloads(assets: Path) -> dict[str, dict[str, Any]]:
    payloads = {name: asset_identity(assets / name) for name in PAYLOAD_NAMES}
    inspect_wheel(assets / WHEEL_NAME)
    inspect_sdist(assets / SDIST_NAME)
    return payloads


def finalize_assets(
    *, assets: Path, build_facts_path: Path, validation_facts_path: Path
) -> dict[str, Any]:
    require(assets.is_dir(), "candidate asset directory does not exist")
    observed = {path.name for path in assets.iterdir()}
    require(observed == set(PAYLOAD_NAMES), f"pre-final asset set drifted: {sorted(observed)}")
    payloads = _verify_payloads(assets)
    build_facts = validate_build_facts(
        read_json_object(build_facts_path, "build facts"), payloads
    )
    source = build_facts["source"]
    source_commit = source["commit"]
    validation = validate_validation_facts(
        read_json_object(validation_facts_path, "validation facts"), source_commit
    )
    summary = {
        "schema_version": "0.1",
        "release_kind": "VERITRAIL_GITHUB_EVIDENCE_PLUGIN",
        "version": VERSION,
        "state": "RELEASE_CANDIDATE",
        "public_gates": "PUBLIC_GATES_GREEN",
        "tag_state": "PRE_TAG",
        "public_download_claim": "NO_PUBLIC_DOWNLOAD_CLAIM",
        "source": source,
        "distribution": build_facts["distribution"],
        "toolchain": build_facts["toolchain"],
        "build_comparison": build_facts["build_comparison"],
        "payloads": payloads,
        "validation": validation,
        "scope": {
            "includes": ["P1", "P2", "P3"],
            "excludes": [
                "P4_FROZEN",
                "TAG_CREATED",
                "RELEASE_CREATED",
                "PUBLIC_DOWNLOAD_VERIFIED",
                "REVIEW_ATTENTION_R1",
            ],
        },
    }
    summary_path = assets / SUMMARY_NAME
    checksum_path = assets / CHECKSUM_NAME
    created: list[Path] = []
    try:
        with summary_path.open("xb") as output:
            output.write(canonical_json_bytes(summary))
        created.append(summary_path)
        checksum_lines = [
            f"{sha256_file(assets / name)}  {name}\n"
            for name in (*PAYLOAD_NAMES, SUMMARY_NAME)
        ]
        with checksum_path.open("xb") as output:
            output.write("".join(checksum_lines).encode("utf-8"))
        created.append(checksum_path)
        verify_assets(assets)
    except BaseException:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise
    return summary


def _parse_checksums(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\]+)", line)
        require(match is not None, "checksum manifest line is malformed")
        digest, name = match.groups()
        require(name not in values, "checksum manifest contains a duplicate filename")
        values[name] = digest
    return values


def verify_assets(assets: Path) -> dict[str, Any]:
    require(assets.is_dir(), "release asset directory does not exist")
    entries = list(assets.iterdir())
    require(all(path.is_file() for path in entries), "release asset set contains non-files")
    observed = {path.name for path in entries}
    require(observed == set(ASSET_NAMES), f"release asset set drifted: {sorted(observed)}")
    payloads = _verify_payloads(assets)
    summary = read_json_object(assets / SUMMARY_NAME, "validation summary")
    require_exact_keys(
        summary,
        {
            "schema_version",
            "release_kind",
            "version",
            "state",
            "public_gates",
            "tag_state",
            "public_download_claim",
            "source",
            "distribution",
            "toolchain",
            "build_comparison",
            "payloads",
            "validation",
            "scope",
        },
        "validation summary",
    )
    require(summary.get("schema_version") == "0.1", "summary schema drifted")
    require(
        summary.get("release_kind") == "VERITRAIL_GITHUB_EVIDENCE_PLUGIN",
        "summary release kind drifted",
    )
    require(summary.get("version") == VERSION, "summary version drifted")
    require(summary.get("state") == "RELEASE_CANDIDATE", "summary state drifted")
    require(summary.get("public_gates") == "PUBLIC_GATES_GREEN", "summary gate state drifted")
    require(summary.get("tag_state") == "PRE_TAG", "summary must remain pre-tag")
    require(
        summary.get("public_download_claim") == "NO_PUBLIC_DOWNLOAD_CLAIM",
        "summary overstates public download",
    )
    source = _validate_recorded_source(summary.get("source"))
    _validate_recorded_distribution(summary.get("distribution"))
    _validate_recorded_toolchain(summary.get("toolchain"))
    _validate_build_comparison(summary.get("build_comparison"))
    summary_payloads = summary.get("payloads")
    require(isinstance(summary_payloads, dict), "summary payloads are not an object")
    require_exact_keys(summary_payloads, set(PAYLOAD_NAMES), "summary payloads")
    normalized_payloads = {
        name: _validate_asset_record(
            summary_payloads.get(name), name, f"summary payload {name}"
        )
        for name in PAYLOAD_NAMES
    }
    require(normalized_payloads == payloads, "summary payload identity drifted")
    validation = summary.get("validation")
    require(isinstance(validation, dict), "summary validation is not an object")
    validate_validation_facts(validation, source["commit"])
    require(
        summary.get("scope")
        == {
            "includes": ["P1", "P2", "P3"],
            "excludes": [
                "P4_FROZEN",
                "TAG_CREATED",
                "RELEASE_CREATED",
                "PUBLIC_DOWNLOAD_VERIFIED",
                "REVIEW_ATTENTION_R1",
            ],
        },
        "summary scope drifted",
    )
    require("sha256" not in summary and "size" not in summary, "summary is self-referential")
    checksums = _parse_checksums(assets / CHECKSUM_NAME)
    expected_names = {*PAYLOAD_NAMES, SUMMARY_NAME}
    require(set(checksums) == expected_names, "checksum manifest payload set drifted")
    for name, expected in checksums.items():
        require(sha256_file(assets / name) == expected, f"checksum mismatch: {name}")
    return {
        "schema_version": "0.1",
        "state": "PASS",
        "asset_set": list(ASSET_NAMES),
        "assets": {name: asset_identity(assets / name) for name in ASSET_NAMES},
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build, finalize, or verify the frozen GitHub Evidence 0.1.0 release assets."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("--repository-root", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--build-facts", type=Path, required=True)
    build.add_argument("--build-python", type=Path, required=True)
    build.add_argument("--expected-commit", required=True)
    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("--assets", type=Path, required=True)
    finalize.add_argument("--build-facts", type=Path, required=True)
    finalize.add_argument("--validation-facts", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--assets", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "build":
        result = build_payloads(
            repository_root=args.repository_root.resolve(strict=True),
            output=args.output.resolve(),
            build_facts_path=args.build_facts.resolve(),
            build_python=args.build_python.resolve(strict=True),
            expected_commit=args.expected_commit,
        )
    elif args.command == "finalize":
        result = finalize_assets(
            assets=args.assets.resolve(strict=True),
            build_facts_path=args.build_facts.resolve(strict=True),
            validation_facts_path=args.validation_facts.resolve(strict=True),
        )
    else:
        result = verify_assets(args.assets.resolve(strict=True))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
