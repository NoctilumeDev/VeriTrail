from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def verify_project() -> int:
    try:
        html = (PROJECT_ROOT / "site" / "index.html").read_text(encoding="utf-8")
        payload = json.loads(
            (PROJECT_ROOT / "site" / "data.json").read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, json.JSONDecodeError):
        print("python-project-check:FAIL", file=sys.stderr)
        return 3

    required_markers = (
        "data-testid=\"run-label\"",
        "data-testid=\"load-evidence\"",
        "data-testid=\"status\"",
        "data-testid=\"evidence-list\"",
    )
    if not all(marker in html for marker in required_markers):
        print("python-project-check:FAIL", file=sys.stderr)
        return 3
    if payload != {"items": ["sealed plan", "bounded command", "browser evidence"]}:
        print("python-project-check:FAIL", file=sys.stderr)
        return 3

    print(
        json.dumps(
            {
                "check": "python-project",
                "items": len(payload["items"]),
                "status": "PASS",
            },
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("verify", "nonzero", "timeout", "canary", "drift", "descendant", "child-sleep"),
        default="verify",
    )
    args = parser.parse_args()

    if args.mode == "nonzero":
        print("python-project-check:EXPECTED-NONZERO", file=sys.stderr)
        return 7
    if args.mode == "timeout":
        time.sleep(5)
        return 0
    if args.mode == "child-sleep":
        time.sleep(5)
        return 0
    if args.mode == "descendant":
        subprocess.Popen(
            [sys.executable, "-m", "checks.verify_project", "--mode", "child-sleep"]
        )
        print("python-project-check:DESCENDANT-SPAWNED")
        return 0
    if args.mode == "drift":
        (PROJECT_ROOT / "checks" / "drift-marker.txt").write_text(
            "intentional final-state drift\n", encoding="utf-8"
        )
        print("python-project-check:DRIFT-CREATED")
        return 0

    result = verify_project()
    if result == 0 and args.mode == "canary":
        print("Authorization: Bearer " + "VT-M9-" + "SECRET-CANARY")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
