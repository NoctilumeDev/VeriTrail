from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from veritrail import __version__
from veritrail.errors import VeriTrailError
from veritrail.plan import load_and_seal_plan, write_sealed_plan
from veritrail.reporting import create_bundle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veritrail",
        description="Seal controlled experiment plans and evaluate imported evidence.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    seal = subparsers.add_parser("seal", help="validate and seal an experiment plan")
    seal.add_argument("--plan", type=Path, required=True, help="unsealed or already sealed plan JSON")
    seal.add_argument("--output", type=Path, required=True, help="new sealed plan path")

    evaluate = subparsers.add_parser("evaluate", help="import evidence and create a verdict bundle")
    evaluate.add_argument("--plan", type=Path, required=True, help="unsealed or sealed plan JSON")
    evaluate.add_argument(
        "--evidence",
        type=Path,
        action="append",
        default=[],
        help="structured evidence JSON; may be repeated",
    )
    evaluate.add_argument("--output", type=Path, required=True, help="new output directory")
    evaluate.add_argument("--run-id", required=True, help="stable caller-supplied run identifier")
    evaluate.add_argument(
        "--execution-status",
        choices=("PLANNED", "RUNNING", "COMPLETED", "ABORTED", "ERROR"),
        default="COMPLETED",
    )
    return parser


def _success(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "seal":
            plan = load_and_seal_plan(args.plan)
            write_sealed_plan(args.output, plan)
            _success(
                {
                    "command": "seal",
                    "output": str(args.output),
                    "plan_sha256": plan["seal"]["digest"],
                }
            )
            return 0
        if args.command == "evaluate":
            plan = load_and_seal_plan(args.plan)
            report = create_bundle(
                plan=plan,
                evidence_paths=args.evidence,
                output=args.output,
                run_id=args.run_id,
                execution_status=args.execution_status,
            )
            _success(
                {
                    "command": "evaluate",
                    "output": str(args.output),
                    "run_id": report["run_id"],
                    "execution_status": report["execution_status"],
                    "verdict": report["verdict"],
                }
            )
            return 0
    except VeriTrailError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
