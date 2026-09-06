from __future__ import annotations

import ast
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

from importlib.metadata import PackageNotFoundError

from veritrail_github.public_render_runtime import (
    BROWSER_DISTRIBUTION,
    BROWSER_ENGINE,
    PLAYWRIGHT_VERSION,
    RenderRuntimeUnavailable,
    preflight_render_runtime,
)


class PublicRenderRuntimeBoundaryTests(unittest.TestCase):
    def test_missing_playwright_fails_without_installing_anything(self) -> None:
        with patch(
            "veritrail_github.public_render_runtime.distribution_version",
            side_effect=PackageNotFoundError,
        ):
            with self.assertRaisesRegex(RenderRuntimeUnavailable, "render.*extra"):
                preflight_render_runtime()

    def test_wrong_playwright_version_fails_before_sync_api_import(self) -> None:
        with patch(
            "veritrail_github.public_render_runtime.distribution_version",
            return_value="1.61.1",
        ):
            with self.assertRaisesRegex(RenderRuntimeUnavailable, "exactly"):
                preflight_render_runtime()

    def test_runtime_module_has_no_install_or_process_escape_hatch(self) -> None:
        source_path = (
            Path(__file__).parents[1]
            / "src"
            / "veritrail_github"
            / "public_render_runtime.py"
        )
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imports.update(
            node.module or ""
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        )
        self.assertFalse({"subprocess", "urllib", "requests"}.intersection(imports))
        self.assertNotIn("playwright install", source.casefold())
        self.assertNotIn("executable_path=", source)
        self.assertNotIn("channel=", source)

    @unittest.skipUnless(
        importlib.util.find_spec("playwright") is not None,
        "render extra is not installed",
    )
    def test_matching_bundled_chromium_launches_and_closes(self) -> None:
        result = preflight_render_runtime()
        self.assertEqual(result.playwright_version, PLAYWRIGHT_VERSION)
        self.assertEqual(result.browser_engine, BROWSER_ENGINE)
        self.assertEqual(result.browser_distribution, BROWSER_DISTRIBUTION)
        self.assertRegex(result.browser_version, r"^[0-9]+(?:\.[0-9]+){1,3}$")


if __name__ == "__main__":
    unittest.main()
