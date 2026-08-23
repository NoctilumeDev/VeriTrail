from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from veritrail.errors import SafetyError, ValidationError
from veritrail.jsonio import load_json_object

from veritrail_starter import __version__
from veritrail_starter.doctor import doctor_report, require_compatible_core
from veritrail_starter.errors import StarterError, invalid
from veritrail_starter.workspace import (
    handoff_workspace,
    initialize_workspace,
    review_workspace,
    validate_workspace,
)


class _JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        del message
        raise invalid("command line arguments are invalid")


def build_parser() -> argparse.ArgumentParser:
    parser = _JsonArgumentParser(
        prog="veritrail-starter",
        description="Create deterministic, unsealed VeriTrail single-webapp drafts.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="perform bounded read-only authoring checks")
    doctor.add_argument("--answers", type=Path, help="optional explicit Answers 0.1 JSON")

    init = subparsers.add_parser("init", help="atomically create a DRAFT workspace")
    init.add_argument("--preset", required=True, choices=("single-webapp",))
    init.add_argument("--answers", type=Path, required=True)

    for name in ("validate", "review", "handoff"):
        command = subparsers.add_parser(name, help=f"{name} an existing DRAFT workspace")
        command.add_argument("--workspace", type=Path, required=True)
    return parser


def _emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _success(command: str, result: dict[str, Any]) -> dict[str, Any]:
    return {"schema_version": "0.1", "command": command, "outcome": "OK", **result}


def main(argv: Sequence[str] | None = None) -> int:
    argument_list = list(sys.argv[1:] if argv is None else argv)
    command_hint = next(
        (
            item
            for item in argument_list
            if item in {"doctor", "init", "validate", "review", "handoff"}
        ),
        "cli",
    )
    command_name = command_hint
    try:
        args = build_parser().parse_args(argument_list)
        command_name = args.command
        require_compatible_core()
        if args.command == "doctor":
            answers = (
                load_json_object(args.answers, label="Answers") if args.answers is not None else None
            )
            _emit(_success("doctor", doctor_report(answers)))
            return 0
        if args.command == "init":
            answers = load_json_object(args.answers, label="Answers")
            _emit(_success("init", initialize_workspace(answers, args.preset)))
            return 0
        operations = {
            "validate": validate_workspace,
            "review": review_workspace,
            "handoff": handoff_workspace,
        }
        _emit(_success(args.command, operations[args.command](args.workspace)))
        return 0
    except StarterError as exc:
        _emit(
            {
                "schema_version": "0.1",
                "command": command_name,
                "outcome": "ERROR",
                "error": {"code": exc.code, "messages": list(exc.messages)},
            }
        )
        return exc.exit_code
    except (ValidationError, SafetyError) as exc:
        messages = list(exc.errors) if isinstance(exc, ValidationError) else [str(exc)]
        _emit(
            {
                "schema_version": "0.1",
                "command": command_name,
                "outcome": "ERROR",
                "error": {"code": "INVALID_INPUT", "messages": messages},
            }
        )
        return 2
    except Exception:
        print("veritrail-starter: unexpected internal error; no automatic fallback was attempted", file=sys.stderr)
        _emit(
            {
                "schema_version": "0.1",
                "command": command_name,
                "outcome": "ERROR",
                "error": {"code": "INTERNAL_ERROR", "messages": ["operation failed closed"]},
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
