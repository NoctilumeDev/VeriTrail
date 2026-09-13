from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    mode = sys.argv[1]
    result = Path(sys.argv[2])
    if mode == "result":
        result.write_bytes(b'{"value":"stable"}\n')
        return 0
    if mode == "sleep":
        time.sleep(60)
        return 0
    if mode == "result-then-sleep":
        result.write_bytes(b'{"value":"late"}\n')
        time.sleep(60)
        return 0
    if mode == "memory":
        chunks: list[bytearray] = []
        while True:
            chunks.append(bytearray(4 * 1024 * 1024))
            time.sleep(0.01)
    if mode == "descendant":
        subprocess.Popen(
            [sys.executable, __file__, "sleep", str(result)],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        time.sleep(60)
        return 0
    raise ValueError("unknown helper mode")


if __name__ == "__main__":
    raise SystemExit(main())
