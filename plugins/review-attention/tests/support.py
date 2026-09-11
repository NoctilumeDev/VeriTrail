from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import zlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FixtureRepository:
    path: Path
    algorithm: str
    commit_oid: str
    root_tree_oid: str
    analysis_tree_oid: str
    blob_oids: tuple[str, ...]
    terminal_count: int


def git_executable() -> Path:
    candidate = shutil.which("git")
    if not candidate:
        raise RuntimeError("Git is required for SourceSnapshot tests")
    return Path(candidate).resolve(strict=True)


def create_fixture_repository(
    root: Path,
    *,
    algorithm: str = "sha1",
    second_commit: bool = False,
) -> FixtureRepository:
    repo = root / f"repo-{algorithm}"
    command = [os.fspath(git_executable()), "init", "--quiet"]
    if algorithm == "sha256":
        command.append("--object-format=sha256")
    command.append(os.fspath(repo))
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    regular = write_object(repo, algorithm, "blob", b"print('regular')\n")
    executable = write_object(repo, algorithm, "blob", b"#!/usr/bin/env python\n")
    symlink = write_object(repo, algorithm, "blob", b"target.bin")
    raw_name_blob = write_object(repo, algorithm, "blob", b"raw-name\n")
    unknown_mode_blob = write_object(repo, algorithm, "blob", b"unusual-mode\n")
    nested_blob = write_object(repo, algorithm, "blob", b"nested\n")
    nested_tree = write_tree(
        repo,
        algorithm,
        [(b"100644", b"mod.py", nested_blob)],
    )
    analysis_tree = write_tree(
        repo,
        algorithm,
        [
            (b"100755", b"run.py", executable),
            (b"100644", b"regular.py", regular),
            (b"120000", b"link", symlink),
            (b"100600", b"odd.bin", unknown_mode_blob),
            (b"100644", b"\xff.py", raw_name_blob),
            (b"40000", b"nested", nested_tree),
            (b"160000", b"submodule", "d" * (40 if algorithm == "sha1" else 64)),
        ],
    )
    root_tree = write_tree(
        repo,
        algorithm,
        [(b"40000", b"pkg", analysis_tree)],
    )
    commit = write_commit(repo, algorithm, root_tree, b"fixture-one")
    if second_commit:
        replacement_blob = write_object(repo, algorithm, "blob", b"replacement\n")
        replacement_tree = write_tree(
            repo,
            algorithm,
            [(b"100644", b"replacement.py", replacement_blob)],
        )
        replacement_commit = write_commit(
            repo, algorithm, replacement_tree, b"fixture-two"
        )
        replace_path = repo / ".git" / "refs" / "replace" / commit
        replace_path.parent.mkdir(parents=True, exist_ok=True)
        replace_path.write_text(replacement_commit + "\n", encoding="ascii")
    return FixtureRepository(
        path=repo,
        algorithm=algorithm,
        commit_oid=commit,
        root_tree_oid=root_tree,
        analysis_tree_oid=analysis_tree,
        blob_oids=(regular, executable, symlink, raw_name_blob, unknown_mode_blob, nested_blob),
        terminal_count=7,
    )


def write_commit(repo: Path, algorithm: str, tree_oid: str, message: bytes) -> str:
    body = (
        b"tree "
        + tree_oid.encode("ascii")
        + b"\nauthor Fixture <fixture@example.invalid> 0 +0000"
        + b"\ncommitter Fixture <fixture@example.invalid> 0 +0000\n\n"
        + message
        + b"\n"
    )
    return write_object(repo, algorithm, "commit", body)


def write_tree(
    repo: Path,
    algorithm: str,
    entries: list[tuple[bytes, bytes, str]],
) -> str:
    body = b"".join(
        mode + b" " + name + b"\x00" + bytes.fromhex(oid)
        for mode, name, oid in entries
    )
    return write_object(repo, algorithm, "tree", body)


def write_object(
    repo: Path,
    algorithm: str,
    object_type: str,
    body: bytes,
) -> str:
    raw = object_type.encode("ascii") + b" " + str(len(body)).encode("ascii") + b"\x00" + body
    digest = hashlib.new(algorithm, raw).hexdigest()
    path = repo / ".git" / "objects" / digest[:2] / digest[2:]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(zlib.compress(raw))
    return digest


def object_body(repo: Path, oid: str) -> bytes:
    path = repo / ".git" / "objects" / oid[:2] / oid[2:]
    raw = zlib.decompress(path.read_bytes())
    _, body = raw.split(b"\x00", 1)
    return body


def corrupt_loose_object(repo: Path, oid: str) -> None:
    path = repo / ".git" / "objects" / oid[:2] / oid[2:]
    raw = bytearray(zlib.decompress(path.read_bytes()))
    raw[-1] ^= 0x01
    path.write_bytes(zlib.compress(bytes(raw)))
