from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path

from scripts.m10_stress_acceptance import (
    port_is_free,
    request_partition,
    terminate_worker_trees,
)


@unittest.skipUnless(os.name == "nt", "M10 stress acceptance is Windows-only")
class M10StressAcceptanceTests(unittest.TestCase):
    def test_request_partition_preserves_total_and_bound(self) -> None:
        partition = request_partition(400, 100)

        self.assertEqual(len(partition), 100)
        self.assertEqual(sum(partition), 400)
        self.assertEqual(set(partition), {4})

    def test_emergency_cleanup_terminates_venv_launcher_tree(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.bind(("127.0.0.1", 0))
            port = int(probe.getsockname()[1])

        child_code = (
            "import socket,time;"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            "s.setsockopt(socket.SOL_SOCKET,socket.SO_EXCLUSIVEADDRUSE,1);"
            f"s.bind(('127.0.0.1',{port}));s.listen();time.sleep(60)"
        )
        parent_code = (
            "import subprocess,sys,time;"
            f"p=subprocess.Popen([sys.executable,'-c',{child_code!r}]);"
            "print(p.pid,flush=True);time.sleep(60)"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", parent_code],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        workers = [("probe", process, Path("unused.json"))]
        try:
            self.assertTrue(process.stdout)
            self.assertTrue(process.stdout.readline().strip().isdigit())
            deadline = time.monotonic() + 10
            while port_is_free(port) and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertFalse(port_is_free(port))

            terminate_worker_trees(workers)

            deadline = time.monotonic() + 5
            while not port_is_free(port) and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertIsNotNone(process.returncode)
            self.assertTrue(port_is_free(port))
        finally:
            if process.poll() is None:
                terminate_worker_trees(workers)


if __name__ == "__main__":
    unittest.main()
