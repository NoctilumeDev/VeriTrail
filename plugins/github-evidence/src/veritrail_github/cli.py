from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Sequence

from veritrail_github.collector import GitHubCollector
from veritrail_github.contracts import derive_observation_request
from veritrail_github.errors import GitHubEvidenceError
from veritrail_github.publisher import publish_evidence
from veritrail_github.transport import UrllibTransport


MAX_PLAN_BYTES = 1024 * 1024
TOKEN_ENVIRONMENT_VARIABLE = "VERITRAIL_GITHUB_TOKEN"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veritrail-github-collect",
        description="Collect bounded, read-only GitHub REST Evidence for a sealed Plan.",
    )
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--observation-spec-id", required=True)
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def _load_plan(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise GitHubEvidenceError("sealed Plan path is not a regular file")
    if path.stat().st_size > MAX_PLAN_BYTES:
        raise GitHubEvidenceError("sealed Plan exceeds the fixed 1 MiB input limit")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GitHubEvidenceError("sealed Plan is not readable finite JSON") from exc
    if not isinstance(value, dict):
        raise GitHubEvidenceError("sealed Plan must be a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        plan = _load_plan(args.plan)
        request = derive_observation_request(
            plan,
            args.observation_spec_id,
            args.request_id,
        )
        collector = GitHubCollector(
            UrllibTransport(), token=os.environ.get(TOKEN_ENVIRONMENT_VARIABLE)
        )
        result = collector.collect(plan, request)
        publish_evidence(args.output, result.artifact)
    except GitHubEvidenceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception:
        print("error: GitHub evidence collection failed", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "output": args.output.name,
                "evidence_sha256": result.artifact.sha256,
                "coverage": result.artifact.document["metadata"][
                    "veritrail_observation"
                ]["coverage"],
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0
