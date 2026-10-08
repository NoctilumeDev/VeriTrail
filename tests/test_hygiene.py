from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_hygiene import (
    broken_markdown_links,
    local_residuals,
    tracked_residual_reason,
)


class HygieneGateTests(unittest.TestCase):
    def test_current_repository_surface_passes(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, "-B", "scripts/check_hygiene.py"],
            cwd=repo,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("Residual Hygiene: PASS", completed.stdout)

    def test_known_transient_paths_are_rejected(self) -> None:
        cases = (
            "dist/veritrail.whl",
            "web/node_modules/pkg/index.js",
            ".env",
            ".env.local",
            "tmp/session.log",
            "runs/latest/result.json",
        )
        for relative in cases:
            with self.subTest(relative=relative):
                self.assertIsNotNone(tracked_residual_reason(relative))

    def test_owned_or_source_paths_are_not_classified_as_residuals(self) -> None:
        cases = (
            ".env.example",
            "docs/198-r1-language-support-qualification-contract.md",
            "docs/design-references/m12/01-home.png",
            "tests/fixtures/review_r1/qualification.json",
            "web/public/textures/paper-noise.png",
        )
        for relative in cases:
            with self.subTest(relative=relative):
                self.assertIsNone(tracked_residual_reason(relative))

    def test_local_markdown_link_requires_a_repository_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            (repo / "docs").mkdir()
            (repo / "README.md").write_text(
                "[present](docs/present.md) [missing](docs/missing.md) [external](https://example.com)",
                encoding="utf-8",
            )
            (repo / "docs" / "present.md").write_text("present", encoding="utf-8")

            broken = broken_markdown_links(
                repo,
                ("README.md", "docs/present.md"),
                ("README.md",),
            )

        self.assertEqual(broken, (("README.md", "docs/missing.md", "docs/missing.md"),))

    def test_local_residue_check_is_read_only_and_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            (repo / "dist").mkdir()
            (repo / "unrelated").mkdir()

            found = local_residuals(repo)

            self.assertEqual(found, ("dist",))
            self.assertTrue((repo / "dist").is_dir())
            self.assertTrue((repo / "unrelated").is_dir())


if __name__ == "__main__":
    unittest.main()
