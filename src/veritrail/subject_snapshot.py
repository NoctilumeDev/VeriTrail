from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from veritrail.canonical import sha256_bytes, sha256_json
from veritrail.errors import SafetyError, ValidationError

SUBJECT_SNAPSHOT_POLICY_VERSION = "subject-tree-sha256/0.1"
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


@dataclass(frozen=True)
class SubjectSnapshot:
    entries: dict[str, tuple[str, int, str]]
    fingerprint: str
    file_count: int
    link_count: int
    total_bytes: int


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT)


def _hash_regular_file(path: Path, metadata: os.stat_result) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
            opened = os.fstat(handle.fileno())
        after = os.lstat(path)
    except OSError as exc:
        raise ValidationError(["subject snapshot contains an unreadable file"]) from exc
    identity = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_nlink")
    if any(getattr(metadata, field) != getattr(opened, field) for field in identity) or any(
        getattr(opened, field) != getattr(after, field) for field in identity
    ):
        raise SafetyError("subject file changed while its snapshot was being captured")
    return digest.hexdigest()


def capture_subject_root_snapshot(
    subject_root: Path,
    watch_roots: list[str],
    *,
    max_files: int,
    max_total_bytes: int,
) -> SubjectSnapshot:
    entries: dict[str, tuple[str, int, str]] = {}
    total_bytes = 0
    link_count = 0
    for relative_root in watch_roots:
        root = (
            subject_root
            if relative_root == "."
            else subject_root.joinpath(*relative_root.split("/"))
        )
        stack = [root]
        while stack:
            directory = stack.pop()
            try:
                children = sorted(os.scandir(directory), key=lambda entry: entry.name)
            except OSError as exc:
                raise ValidationError(["subject snapshot contains an unreadable directory"]) from exc
            for child in children:
                if any(ord(character) < 32 for character in child.name):
                    raise ValidationError(["subject snapshot contains a control-character path"])
                path = Path(child.path)
                try:
                    metadata = os.lstat(path)
                except OSError as exc:
                    raise ValidationError(["subject snapshot contains an unreadable node"]) from exc
                relative = path.relative_to(subject_root).as_posix()
                is_link = child.is_symlink() or _is_reparse(metadata)
                if is_link:
                    try:
                        target_digest = sha256_bytes(os.readlink(path).encode("utf-8"))
                    except OSError as exc:
                        raise ValidationError(
                            ["subject snapshot contains an unreadable link or reparse point"]
                        ) from exc
                    entries[relative] = ("LINK", int(metadata.st_size), target_digest)
                    link_count += 1
                elif stat.S_ISDIR(metadata.st_mode):
                    stack.append(path)
                    continue
                elif stat.S_ISREG(metadata.st_mode):
                    if metadata.st_nlink != 1:
                        raise SafetyError("subject snapshot contains an unsafe hard-linked file")
                    total_bytes += int(metadata.st_size)
                    if total_bytes > max_total_bytes:
                        raise ValidationError(
                            ["subject snapshot exceeds the sealed total-byte limit"]
                        )
                    entries[relative] = (
                        "FILE",
                        int(metadata.st_size),
                        _hash_regular_file(path, metadata),
                    )
                else:
                    raise ValidationError(["subject snapshot contains an unsupported node type"])
                if len(entries) > max_files:
                    raise ValidationError(["subject snapshot exceeds the sealed file-count limit"])
    ordered = [
        {"path": path, "kind": value[0], "size": value[1], "sha256": value[2]}
        for path, value in sorted(entries.items())
    ]
    return SubjectSnapshot(
        entries=entries,
        fingerprint=sha256_json(ordered),
        file_count=sum(1 for value in entries.values() if value[0] == "FILE"),
        link_count=link_count,
        total_bytes=total_bytes,
    )


def compare_subject_snapshots(
    before: SubjectSnapshot, after: SubjectSnapshot
) -> tuple[dict[str, int], bool]:
    before_paths = set(before.entries)
    after_paths = set(after.entries)
    added_paths = after_paths - before_paths
    deleted_paths = before_paths - after_paths
    modified = 0
    type_changed = 0
    link_changed = sum(
        1 for path in added_paths if after.entries[path][0] == "LINK"
    ) + sum(1 for path in deleted_paths if before.entries[path][0] == "LINK")
    for path in before_paths & after_paths:
        left = before.entries[path]
        right = after.entries[path]
        if left == right:
            continue
        if left[0] != right[0]:
            type_changed += 1
            if "LINK" in {left[0], right[0]}:
                link_changed += 1
        elif left[0] == "LINK":
            link_changed += 1
        else:
            modified += 1
    counts = {
        "added": len(added_paths),
        "deleted": len(deleted_paths),
        "modified": modified,
        "type_changed": type_changed,
        "link_changed": link_changed,
    }
    return counts, any(counts.values())


def subject_snapshot_projection(
    snapshot: SubjectSnapshot, watch_roots: list[str]
) -> dict[str, Any]:
    return {
        "policy_version": SUBJECT_SNAPSHOT_POLICY_VERSION,
        "watch_roots": list(watch_roots),
        "fingerprint": snapshot.fingerprint,
        "file_count": snapshot.file_count,
        "link_count": snapshot.link_count,
        "total_bytes": snapshot.total_bytes,
    }
