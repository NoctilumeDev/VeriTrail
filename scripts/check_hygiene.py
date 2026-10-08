from __future__ import annotations

import argparse
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote


ACTIVE_MARKDOWN_SURFACE = (
    "README.md",
    "START_HERE.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "docs/working-method.md",
    "docs/hygiene.md",
)

RESIDUAL_DIRECTORY_NAMES = frozenset(
    {
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".veritrail",
        "__pycache__",
        "artifacts",
        "build",
        "dist",
        "htmlcov",
        "node_modules",
        "playwright-report",
        "runs",
        "test-results",
    }
)

RESIDUAL_SUFFIXES = (
    ".db",
    ".db-shm",
    ".db-wal",
    ".har",
    ".log",
    ".pid",
    ".pyc",
    ".pyo",
    ".sqlite",
    ".sqlite3",
    ".temp",
    ".tmp",
    ".trace.zip",
)

LOCAL_RESIDUAL_PATHS = (
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".venv313",
    ".veritrail",
    "artifacts",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "playwright-report",
    "runs",
    "test-results",
    "venv",
    "web/dist",
    "web/node_modules",
)

INLINE_LINK = re.compile(r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^\s)]+)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(?P<target><[^>]+>|\S+)", re.MULTILINE)
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _git_paths(repo: Path) -> tuple[str, ...]:
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
    )
    return tuple(
        item.decode("utf-8", errors="strict").replace("\\", "/")
        for item in completed.stdout.split(b"\0")
        if item
    )


def tracked_residual_reason(relative_path: str) -> str | None:
    normalized = relative_path.replace("\\", "/")
    path = PurePosixPath(normalized)
    if any(part in RESIDUAL_DIRECTORY_NAMES for part in path.parts[:-1]):
        return "generated or runtime directory"

    name = path.name.lower()
    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        return "private environment file"
    if name.endswith((".pem", ".key")):
        return "private key material"
    if name.endswith(RESIDUAL_SUFFIXES):
        return "transient runtime file"
    return None


def tracked_residuals(paths: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    return tuple(
        (path, reason)
        for path in paths
        if (reason := tracked_residual_reason(path)) is not None
    )


def _link_targets(markdown: str) -> tuple[str, ...]:
    return tuple(
        match.group("target").strip("<>")
        for pattern in (INLINE_LINK, REFERENCE_LINK)
        for match in pattern.finditer(markdown)
    )


def _normalize_link(source: str, target: str) -> str | None:
    decoded = unquote(target).split("#", 1)[0].split("?", 1)[0]
    if not decoded or decoded.startswith("#") or SCHEME.match(decoded) or decoded.startswith("//"):
        return None

    source_parent = PurePosixPath(source).parent
    candidate = PurePosixPath(decoded.lstrip("/")) if decoded.startswith("/") else source_parent / decoded
    parts: list[str] = []
    for part in candidate.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                return "../OUTSIDE_REPOSITORY"
            parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def broken_markdown_links(
    repo: Path,
    git_paths: tuple[str, ...],
    markdown_surface: tuple[str, ...] = ACTIVE_MARKDOWN_SURFACE,
) -> tuple[tuple[str, str, str], ...]:
    files = set(git_paths)
    directories = {
        "/".join(PurePosixPath(path).parts[:index])
        for path in git_paths
        for index in range(1, len(PurePosixPath(path).parts))
    }
    broken: list[tuple[str, str, str]] = []
    for source in markdown_surface:
        source_path = repo / Path(source)
        if not source_path.is_file():
            broken.append((source, source, "source Markdown is missing"))
            continue
        markdown = source_path.read_text(encoding="utf-8")
        for raw_target in _link_targets(markdown):
            normalized = _normalize_link(source, raw_target)
            if normalized is None:
                continue
            if normalized not in files and normalized not in directories:
                broken.append((source, raw_target, normalized))
    return tuple(broken)


def local_residuals(repo: Path) -> tuple[str, ...]:
    found: list[str] = []
    for relative in LOCAL_RESIDUAL_PATHS:
        candidate = repo / Path(relative)
        if candidate.exists() and not candidate.is_symlink():
            found.append(relative)
    return tuple(found)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only VeriTrail residual hygiene check")
    parser.add_argument(
        "--local",
        action="store_true",
        help="also report known disposable local build/runtime paths",
    )
    args = parser.parse_args(argv)

    repo = Path(__file__).resolve().parents[1]
    git_paths = _git_paths(repo)
    residuals = tracked_residuals(git_paths)
    broken_links = broken_markdown_links(repo, git_paths)
    local = local_residuals(repo) if args.local else ()

    for path, reason in residuals:
        print(f"ERROR tracked residual: {path} ({reason})")
    for source, target, normalized in broken_links:
        print(f"ERROR broken local link: {source} -> {target} ({normalized})")
    for path in local:
        print(f"REVIEW_REQUIRED local residue: {path}")

    if residuals or broken_links or local:
        print(
            "Residual Hygiene: REVIEW_REQUIRED "
            f"(tracked_residuals={len(residuals)}, broken_links={len(broken_links)}, local_residues={len(local)})"
        )
        return 1

    print(
        "Residual Hygiene: PASS "
        f"(surface_files={len(git_paths)}, markdown_entries={len(ACTIVE_MARKDOWN_SURFACE)}, local_checked={args.local})"
    )
    print(
        "Manual review still owns image consumers, evidence/provenance responsibility, unique local state, "
        "other worktrees, external services, and LOCAL_DORMANT."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
