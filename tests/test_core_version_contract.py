from __future__ import annotations

import re
import unittest
from pathlib import Path

from veritrail import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPOSITORY_ROOT / "pyproject.toml"
FROZEN_CORE_BASELINE = "0.12.0"
MAINTENANCE_CORE_VERSION = "0.12.1"
CURRENT_STATUS_FILES = (
    REPOSITORY_ROOT / "AGENTS.md",
    REPOSITORY_ROOT / "CONTRIBUTING.md",
    REPOSITORY_ROOT / "SECURITY.md",
)


class CoreVersionContractTests(unittest.TestCase):
    def test_source_uses_the_current_maintenance_coordinate(self) -> None:
        pyproject = PYPROJECT.read_text(encoding="utf-8")
        match = re.search(
            r'(?ms)^\[project\]\s*.*?^version = "([^"]+)"$',
            pyproject,
        )
        self.assertIsNotNone(match, "[project].version is missing from pyproject.toml")
        project_version = match.group(1)

        self.assertEqual(project_version, MAINTENANCE_CORE_VERSION)
        self.assertEqual(__version__, MAINTENANCE_CORE_VERSION)
        self.assertNotEqual(project_version, FROZEN_CORE_BASELINE)

        self.assertIn('"Development Status :: 4 - Beta"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.10"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.13"', pyproject)
        self.assertNotIn('"Development Status :: 2 - Pre-Alpha"', pyproject)

    def test_current_status_documents_do_not_restore_the_pre_release_coordinate(self) -> None:
        for path in CURRENT_STATUS_FILES:
            with self.subTest(path=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertIn(MAINTENANCE_CORE_VERSION, content)
                self.assertNotIn("0.12.1.dev0", content)

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
