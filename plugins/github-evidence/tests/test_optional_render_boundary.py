from __future__ import annotations

import builtins
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from support import acceptance_plan, base_transport

from veritrail_github.collector import GitHubCollector
from veritrail_github.contracts import derive_observation_request


class OptionalRenderBoundaryTests(unittest.TestCase):
    def test_playwright_is_an_exact_optional_extra(self) -> None:
        metadata = (Path(__file__).parents[1] / "pyproject.toml").read_text(
            encoding="utf-8"
        )
        self.assertRegex(
            metadata,
            re.compile(r'^dependencies = \["veritrail==0\.12\.2"\]$', re.MULTILINE),
        )
        self.assertRegex(
            metadata,
            re.compile(
                r'^\[project\.optional-dependencies\]\s*'
                r'^render = \["playwright==1\.62\.0"\]$',
                re.MULTILINE,
            ),
        )

    def test_p1_collection_does_not_import_playwright(self) -> None:
        self.assertFalse(any(name == "playwright" for name in sys.modules))
        original_import = builtins.__import__

        def reject_playwright(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "playwright" or name.startswith("playwright."):
                raise AssertionError("P1 attempted to import optional Playwright")
            return original_import(name, globals, locals, fromlist, level)

        plan = acceptance_plan(["commit.identity"])
        request = derive_observation_request(plan, "github-api", "request-no-browser")
        with patch("builtins.__import__", side_effect=reject_playwright):
            result = GitHubCollector(
                base_transport(),
                session_id_factory=lambda: "github-session-no-browser",
            ).collect(plan, request)

        self.assertEqual(
            result.artifact.document["metadata"]["veritrail_observation"]["coverage"],
            "COMPLETE",
        )


if __name__ == "__main__":
    unittest.main()
