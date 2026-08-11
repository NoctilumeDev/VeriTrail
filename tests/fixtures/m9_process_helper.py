from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        required=True,
        choices=(
            "argv",
            "canary",
            "echo",
            "exit-code",
            "marker",
            "sleep",
            "stdin-eof",
            "spawn-at-limit",
            "spawn-child",
            "spawn-child-overflow",
            "overflow",
        ),
    )
    parser.add_argument("--marker")
    parser.add_argument("--code", type=int, default=7)
    parser.add_argument("--seconds", type=float, default=5.0)
    parser.add_argument("values", nargs="*")
    args = parser.parse_args()

    if args.mode == "argv":
        print(json.dumps(args.values, ensure_ascii=False))
        return 0
    if args.mode == "echo":
        print("stdout-ok")
        print("stderr-ok", file=sys.stderr)
        return 0
    if args.mode == "canary":
        print("ghp_12345678901234567890 C:\\private\\unit alice@example.test")
        print("\\\\unit-server\\private\\trace", file=sys.stderr)
        return 0
    if args.mode == "exit-code":
        return args.code
    if args.mode == "marker":
        if args.marker is None:
            return 2
        Path(args.marker).write_text("resumed", encoding="utf-8")
        return 0
    if args.mode == "sleep":
        time.sleep(args.seconds)
        return 0
    if args.mode == "stdin-eof":
        print("eof" if sys.stdin.buffer.read(1) == b"" else "data")
        return 0
    if args.mode == "spawn-at-limit":
        try:
            child = subprocess.Popen(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--mode",
                    "sleep",
                    "--seconds",
                    str(args.seconds),
                ]
            )
        except OSError:
            print("spawn-denied")
            return 0
        child.wait(timeout=args.seconds + 1)
        print("spawn-created")
        return 0
    if args.mode == "spawn-child":
        subprocess.Popen(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--mode",
                "sleep",
                "--seconds",
                str(args.seconds),
            ]
        )
        print("child-started")
        return 0
    if args.mode == "spawn-child-overflow":
        subprocess.Popen(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--mode",
                "overflow",
                "--seconds",
                str(args.seconds),
            ]
        )
        return 0
    if args.mode == "overflow":
        sys.stdout.buffer.write(b"x" * 131_072)
        sys.stdout.buffer.flush()
        time.sleep(args.seconds)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
