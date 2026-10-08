from __future__ import annotations

import re
import unittest
from pathlib import Path

from veritrail import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPOSITORY_ROOT / "pyproject.toml"
FROZEN_CORE_BASELINE = "0.12.0"
PREVIOUS_MAINTENANCE_CORE_VERSION = "0.12.2"
PUBLIC_LATEST_CORE_VERSION = "0.13.0"
CURRENT_SOURCE_VERSION = "0.12.3"
HISTORICAL_MAINTENANCE_CONTRACT = (
    REPOSITORY_ROOT / "docs" / "74-core-demo-catalog-binding-maintenance-contract.md"
)
HISTORICAL_RELEASE_NOTES = REPOSITORY_ROOT / "docs" / "75-v0.12.2-release-notes.md"
CURRENT_RELEASE_NOTES = REPOSITORY_ROOT / "docs" / "77-v0.12.3-release-notes.md"
RELEASE_PROBE = REPOSITORY_ROOT / "scripts" / "core_0123_release_probe.py"


class CoreVersionContractTests(unittest.TestCase):
    def test_source_uses_the_unreleased_0_12_3_candidate_coordinate(self) -> None:
        pyproject = PYPROJECT.read_text(encoding="utf-8")
        match = re.search(
            r'(?ms)^\[project\]\s*.*?^version = "([^"]+)"$',
            pyproject,
        )
        self.assertIsNotNone(match, "[project].version is missing from pyproject.toml")
        project_version = match.group(1)

        self.assertEqual(project_version, CURRENT_SOURCE_VERSION)
        self.assertEqual(__version__, CURRENT_SOURCE_VERSION)
        self.assertNotEqual(project_version, FROZEN_CORE_BASELINE)
        self.assertNotEqual(project_version, PREVIOUS_MAINTENANCE_CORE_VERSION)

        self.assertIn('"Development Status :: 4 - Beta"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.10"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.13"', pyproject)
        self.assertNotIn('"Development Status :: 2 - Pre-Alpha"', pyproject)

    def test_candidate_and_existing_release_identities_are_not_conflated(self) -> None:
        contract = HISTORICAL_MAINTENANCE_CONTRACT.read_text(encoding="utf-8")
        release_0_12_2 = HISTORICAL_RELEASE_NOTES.read_text(encoding="utf-8")
        candidate = CURRENT_RELEASE_NOTES.read_text(encoding="utf-8")

        self.assertIn("0.12.2", contract)
        self.assertIn("0.12.2", release_0_12_2)
        self.assertNotIn("0.12.3", contract)
        self.assertNotIn("0.12.3", release_0_12_2)

        self.assertRegex(
            candidate,
            r"(?m)^> 状态：`RELEASE CANDIDATE / PENDING PUBLIC READBACK`$",
        )
        self.assertIn(f"当前公开 Latest Core：`{PUBLIC_LATEST_CORE_VERSION}`", candidate)
        self.assertIn(
            f"前一维护坐标：`{PREVIOUS_MAINTENANCE_CORE_VERSION}`", candidate
        )
        self.assertIn(f"候选源码版本：`{CURRENT_SOURCE_VERSION}`", candidate)
        self.assertIn("non-Latest", candidate)
        self.assertIn("net::ERR_NO_BUFFER_SPACE", candidate)
        self.assertIn("HostSocketNoBufferSpace", candidate)

        planned_assets = (
            "veritrail-0.12.3-py3-none-any.whl",
            "veritrail-0.12.3.tar.gz",
            "core-v0.12.3-validation-summary.json",
            "SHA256SUMS.txt",
        )
        for asset in planned_assets:
            self.assertIn(asset, candidate)
        self.assertNotIn("veritrail-workbench-0.12.3.zip", candidate)

    def test_candidate_includes_the_bounded_installed_distribution_probe(self) -> None:
        source = RELEASE_PROBE.read_text(encoding="utf-8")
        self.assertIn('EXPECTED_VERSION = "0.12.3"', source)
        self.assertIn("CORE_0.12.3_HOST_SOCKET_INSTALLED_DISTRIBUTION", source)
        self.assertNotIn("from tests", source)
        self.assertNotIn("import tests", source)


if __name__ == "__main__":
    unittest.main()
