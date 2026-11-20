from __future__ import annotations

import unittest
from pathlib import Path

from veritrail_github import __version__
from veritrail_github.collector import COLLECTOR_IMPLEMENTATION_VERSION
from veritrail_github.contracts import NORMALIZATION_SEMANTICS_VERSION
from veritrail_github.public_render_collector import (
    PUBLIC_RENDER_COLLECTOR_IMPLEMENTATION_VERSION,
)
from veritrail_github.public_render_contracts import (
    PUBLIC_RENDER_NORMALIZATION_SEMANTICS_VERSION,
)


class ReleaseIdentityTests(unittest.TestCase):
    def test_distribution_and_collector_provenance_are_aligned(self) -> None:
        self.assertEqual(__version__, "0.1.1")
        self.assertEqual(COLLECTOR_IMPLEMENTATION_VERSION, "0.1.1")
        self.assertEqual(PUBLIC_RENDER_COLLECTOR_IMPLEMENTATION_VERSION, "0.1.1")

    def test_patch_release_does_not_change_normalization_semantics(self) -> None:
        self.assertEqual(NORMALIZATION_SEMANTICS_VERSION, "github-rest-facts/0.3")
        self.assertEqual(
            PUBLIC_RENDER_NORMALIZATION_SEMANTICS_VERSION,
            "github-public-render-facts/0.1",
        )

    def test_wheel_only_ci_binds_the_final_import_version(self) -> None:
        workflow = (
            Path(__file__).resolve().parents[3] / ".github" / "workflows" / "ci.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("__version__ == '0.1.1'", workflow)
        self.assertNotIn("__version__ == '0.1.1.dev0'", workflow)


if __name__ == "__main__":
    unittest.main()
