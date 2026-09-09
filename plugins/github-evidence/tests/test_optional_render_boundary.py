from __future__ import annotations

import re
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path


class OptionalRenderBoundaryTests(unittest.TestCase):
    def test_playwright_is_an_exact_optional_extra(self) -> None:
        metadata = (Path(__file__).parents[1] / "pyproject.toml").read_text(
            encoding="utf-8"
        )
        self.assertRegex(
            metadata,
            re.compile(r'^dependencies = \["veritrail==0\.13\.0"\]$', re.MULTILINE),
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
        repository_root = Path(__file__).resolve().parents[3]
        script = textwrap.dedent(
            """
            import builtins
            import sys

            sys.path[:0] = sys.argv[1:]
            original_import = builtins.__import__

            def reject_playwright(
                name, globals=None, locals=None, fromlist=(), level=0
            ):
                if name == "playwright" or name.startswith("playwright."):
                    raise AssertionError(
                        "P1 attempted to import optional Playwright"
                    )
                return original_import(name, globals, locals, fromlist, level)

            builtins.__import__ = reject_playwright

            from support import acceptance_plan, base_transport
            from veritrail_github.collector import GitHubCollector
            from veritrail_github.contracts import derive_observation_request

            plan = acceptance_plan(["commit.identity"])
            request = derive_observation_request(
                plan, "github-api", "request-no-browser"
            )
            result = GitHubCollector(
                base_transport(),
                session_id_factory=lambda: "github-session-no-browser",
            ).collect(plan, request)
            if any(
                name == "playwright" or name.startswith("playwright.")
                for name in sys.modules
            ):
                raise AssertionError("P1 left Playwright imported")
            print(
                result.artifact.document["metadata"]
                ["veritrail_observation"]["coverage"]
            )
            """
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                script,
                str(repository_root / "src"),
                str(repository_root / "plugins" / "github-evidence" / "src"),
                str(repository_root / "plugins" / "github-evidence" / "tests"),
            ],
            cwd=repository_root,
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("COMPLETE", completed.stdout.strip())


if __name__ == "__main__":
    unittest.main()
