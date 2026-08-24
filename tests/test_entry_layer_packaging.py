from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = REPOSITORY_ROOT / "scripts" / "build_authoring_skill.py"
SKILL_MD = REPOSITORY_ROOT / "skills" / "veritrail-authoring" / "SKILL.md"
AUTHORING_SCRIPT = (
    REPOSITORY_ROOT / "skills" / "veritrail-authoring" / "scripts" / "authoring.py"
)
STARTER_PYPROJECT = REPOSITORY_ROOT / "starter" / "pyproject.toml"
STARTER_INIT = (
    REPOSITORY_ROOT / "starter" / "src" / "veritrail_starter" / "__init__.py"
)


class EntryLayerPackagingTests(unittest.TestCase):
    def _build(self, output: Path) -> dict[str, object]:
        completed = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "--build", "--output", str(output)],
            cwd=REPOSITORY_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertFalse(completed.stderr)
        return json.loads(completed.stdout)

    def test_skill_archive_is_deterministic_and_minimal(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-skill-package-") as raw_temp:
            root = Path(raw_temp)
            first = root / "first.zip"
            second = root / "second.zip"
            first_result = self._build(first)
            second_result = self._build(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first_result["sha256"], second_result["sha256"])
            self.assertEqual(first_result["version"], "0.1.0")

            with zipfile.ZipFile(first, mode="r") as archive:
                names = archive.namelist()
                self.assertEqual(
                    names,
                    [
                        "veritrail-authoring/SKILL.md",
                        "veritrail-authoring/agents/openai.yaml",
                        "veritrail-authoring/references/error-codes.md",
                        "veritrail-authoring/references/protocol.md",
                        "veritrail-authoring/scripts/authoring.py",
                        "veritrail-authoring/LICENSE",
                    ],
                )
                self.assertFalse(any("test" in name.casefold() for name in names))
                self.assertFalse(any("__pycache__" in name for name in names))
                self.assertFalse(any(Path(name).is_absolute() or ".." in Path(name).parts for name in names))

    def test_release_versions_are_aligned_without_widening_compatibility(self) -> None:
        starter_pyproject = STARTER_PYPROJECT.read_text(encoding="utf-8")
        starter_init = STARTER_INIT.read_text(encoding="utf-8")
        skill_md = SKILL_MD.read_text(encoding="utf-8")
        authoring = AUTHORING_SCRIPT.read_text(encoding="utf-8")
        self.assertRegex(starter_pyproject, r'(?m)^version = "0\.1\.0"$')
        self.assertRegex(starter_init, r'(?m)^__version__ = "0\.1\.0"$')
        self.assertRegex(skill_md, r'(?m)^  version: "0\.1\.0"$')
        self.assertRegex(skill_md, r'(?m)^  compatible_starter: "0\.1\.0"$')
        self.assertIn('SUPPORTED_STARTER_VERSIONS = frozenset({"0.1.0"})', authoring)
        self.assertNotIn("0.1.0.dev0", starter_pyproject + starter_init + skill_md + authoring)

    def test_builder_refuses_to_overwrite_an_existing_archive(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-skill-conflict-") as raw_temp:
            output = Path(raw_temp) / "skill.zip"
            output.write_bytes(b"keep")
            completed = subprocess.run(
                [sys.executable, str(BUILD_SCRIPT), "--build", "--output", str(output)],
                cwd=REPOSITORY_ROOT,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                text=True,
                encoding="utf-8",
                errors="strict",
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(output.read_bytes(), b"keep")
            result = json.loads(completed.stdout)
            self.assertEqual(result["state"], "ERROR")


if __name__ == "__main__":
    unittest.main()
