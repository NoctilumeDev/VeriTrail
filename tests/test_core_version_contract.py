from __future__ import annotations

import re
import unittest
from pathlib import Path

from veritrail import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPOSITORY_ROOT / "pyproject.toml"
RELEASED_CORE_VERSION = "0.12.0"
DEVELOPMENT_CORE_VERSION = "0.12.1.dev0"


class CoreVersionContractTests(unittest.TestCase):
    def test_default_branch_uses_distinct_unreleased_core_coordinate(self) -> None:
        pyproject = PYPROJECT.read_text(encoding="utf-8")
        match = re.search(
            r'(?ms)^\[project\]\s*.*?^version = "([^"]+)"$',
            pyproject,
        )
        self.assertIsNotNone(match, "[project].version is missing from pyproject.toml")
        project_version = match.group(1)

        self.assertEqual(project_version, DEVELOPMENT_CORE_VERSION)
        self.assertEqual(__version__, DEVELOPMENT_CORE_VERSION)
        self.assertNotEqual(project_version, RELEASED_CORE_VERSION)


if __name__ == "__main__":
    unittest.main()
