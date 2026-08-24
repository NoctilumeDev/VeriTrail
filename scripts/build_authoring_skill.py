from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / "skills" / "veritrail-authoring"
LICENSE_PATH = REPOSITORY_ROOT / "LICENSE"
ARCHIVE_ROOT = "veritrail-authoring"
SOURCE_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/error-codes.md",
    "references/protocol.md",
    "scripts/authoring.py",
)
GENERATED_FILES = ("LICENSE",)
EXPECTED_FILES = SOURCE_FILES + GENERATED_FILES
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
VERSION_PATTERN = re.compile(
    r'^\s{2}version:\s*["\'](?P<version>[0-9]+\.[0-9]+\.[0-9]+)["\']\s*$',
    re.MULTILINE,
)


class PackageFailure(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def skill_version() -> str:
    content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = VERSION_PATTERN.search(content)
    if match is None:
        raise PackageFailure("SKILL.md must declare metadata.version")
    return match.group("version")


def default_output() -> Path:
    return REPOSITORY_ROOT / "dist" / f"veritrail-authoring-{skill_version()}.zip"


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.flag_bits |= 0x800
    return info


def _source_bytes(relative: str) -> bytes:
    if relative == "LICENSE":
        path = LICENSE_PATH
    else:
        path = SKILL_ROOT / Path(relative)
    if not path.is_file() or path.is_symlink():
        raise PackageFailure(f"required ordinary Skill file is unavailable: {relative}")
    return path.read_bytes()


def build_archive(output: Path) -> dict[str, object]:
    output = output.resolve(strict=False)
    if output.exists():
        raise PackageFailure(f"output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(
            output,
            mode="x",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as archive:
            for relative in EXPECTED_FILES:
                archive.writestr(
                    _zip_info(f"{ARCHIVE_ROOT}/{relative}"),
                    _source_bytes(relative),
                    compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )
        verification = verify_archive(output)
    except Exception:
        output.unlink(missing_ok=True)
        raise
    return {
        "schema_version": "0.1",
        "product": "veritrail-authoring",
        "version": skill_version(),
        "archive": output.name,
        "sha256": sha256_file(output),
        "size_bytes": output.stat().st_size,
        "entries": verification["entries"],
    }


def verify_archive(archive_path: Path) -> dict[str, object]:
    archive_path = archive_path.resolve(strict=True)
    expected = [f"{ARCHIVE_ROOT}/{relative}" for relative in EXPECTED_FILES]
    with zipfile.ZipFile(archive_path, mode="r") as archive:
        names = archive.namelist()
        if names != expected:
            raise PackageFailure(f"archive entries drifted: {names!r}")
        for info, expected_name in zip(archive.infolist(), expected, strict=True):
            if info.filename != expected_name or info.is_dir():
                raise PackageFailure(f"invalid archive entry: {info.filename}")
            if info.date_time != FIXED_TIMESTAMP:
                raise PackageFailure(f"archive timestamp drifted: {info.filename}")
            if info.file_size <= 0:
                raise PackageFailure(f"archive entry is empty: {info.filename}")
            if info.file_size > 2 * 1024 * 1024:
                raise PackageFailure(f"archive entry is unexpectedly large: {info.filename}")
            normalized = Path(info.filename)
            if normalized.is_absolute() or ".." in normalized.parts:
                raise PackageFailure(f"archive entry escaped its root: {info.filename}")
            archive.read(info)
    return {
        "schema_version": "0.1",
        "product": "veritrail-authoring",
        "version": skill_version(),
        "archive": archive_path.name,
        "sha256": sha256_file(archive_path),
        "size_bytes": archive_path.stat().st_size,
        "entries": names,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or verify the Authoring Skill ZIP.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--build", action="store_true")
    action.add_argument("--verify", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.build:
            result = build_archive(args.output or default_output())
        else:
            if args.output is not None:
                raise PackageFailure("--output is only valid with --build")
            result = verify_archive(args.verify)
    except (OSError, PackageFailure, zipfile.BadZipFile) as exc:
        print(json.dumps({"state": "ERROR", "message": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({**result, "state": "PASS"}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
