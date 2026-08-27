from __future__ import annotations

import re
import unittest
from pathlib import Path

from veritrail import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPOSITORY_ROOT / "pyproject.toml"
FROZEN_CORE_BASELINE = "0.12.0"
STABLE_CORE_VERSION = "0.12.1"
CURRENT_SOURCE_VERSION = "0.12.2"
CURRENT_STATUS_FILES = (
    REPOSITORY_ROOT / "AGENTS.md",
    REPOSITORY_ROOT / "CONTRIBUTING.md",
    REPOSITORY_ROOT / "SECURITY.md",
)
CURRENT_MAINTENANCE_CONTRACT = (
    REPOSITORY_ROOT / "docs" / "74-core-demo-catalog-binding-maintenance-contract.md"
)
CURRENT_RELEASE_NOTES = REPOSITORY_ROOT / "docs" / "75-v0.12.2-release-notes.md"


class CoreVersionContractTests(unittest.TestCase):
    def test_source_uses_the_new_maintenance_release_candidate_coordinate(self) -> None:
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
        self.assertNotEqual(project_version, STABLE_CORE_VERSION)

        self.assertIn('"Development Status :: 4 - Beta"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.10"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.13"', pyproject)
        self.assertNotIn('"Development Status :: 2 - Pre-Alpha"', pyproject)

    def test_stable_release_and_candidate_coordinates_are_not_conflated(self) -> None:
        for path in CURRENT_STATUS_FILES:
            with self.subTest(path=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertIn(STABLE_CORE_VERSION, content)
                self.assertNotIn("0.12.1.dev0", content)

        contract = CURRENT_MAINTENANCE_CONTRACT.read_text(encoding="utf-8")
        self.assertIn(STABLE_CORE_VERSION, contract)
        self.assertIn(CURRENT_SOURCE_VERSION, contract)
        self.assertIn("RELEASE CANDIDATE / PENDING PUBLIC READBACK", contract)

        release_notes = CURRENT_RELEASE_NOTES.read_text(encoding="utf-8")
        self.assertIn(STABLE_CORE_VERSION, release_notes)
        self.assertIn(CURRENT_SOURCE_VERSION, release_notes)
        self.assertIn("PENDING PUBLIC READBACK", release_notes)
        self.assertIn("veritrail-0.12.2-py3-none-any.whl", release_notes)

        contributing = (REPOSITORY_ROOT / "CONTRIBUTING.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(CURRENT_SOURCE_VERSION, contributing)
        self.assertIn("pending public readback", contributing.lower())

        bug_template = (
            REPOSITORY_ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("placeholder: v0.12.1 or 40-character commit SHA", bug_template)

        starter_readme = (REPOSITORY_ROOT / "starter" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "releases/download/v0.12.1/veritrail-0.12.1-py3-none-any.whl",
            starter_readme,
        )


if __name__ == "__main__":
    unittest.main()
