from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.core_0123_release_probe import ReleaseProbeFailure, run
from veritrail.canonical import canonical_json_bytes


class Core0123ReleaseProbeTests(unittest.TestCase):
    def test_probe_writes_canonical_installed_distribution_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "probe.json"
            summary = run(output, None)

            self.assertEqual("PASS", summary["status"])
            self.assertEqual("0.12.3", summary["package_version"])
            self.assertEqual(
                "CORE_0.12.3_HOST_SOCKET_INSTALLED_DISTRIBUTION",
                summary["boundary"],
            )
            self.assertEqual(canonical_json_bytes(summary) + b"\n", output.read_bytes())
            self.assertEqual(summary, json.loads(output.read_bytes()))

            with self.assertRaisesRegex(
                ReleaseProbeFailure, "release probe output already exists"
            ):
                run(output, None)


if __name__ == "__main__":
    unittest.main()
