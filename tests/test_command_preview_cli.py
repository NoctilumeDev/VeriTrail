from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from veritrail.cli import main
from veritrail.errors import SafetyError

from tests.support import command_plan, orchestration_plan


class CommandPreviewCliTests(unittest.TestCase):
    def _fixture(self, root: Path) -> tuple[Path, Path, Path]:
        subject = root / "subject"
        (subject / "src").mkdir(parents=True)
        (subject / "tests").mkdir()
        executable = root / "python.exe"
        executable.write_bytes(b"MZcli-preview")
        plan_path = root / "plan.json"
        plan_path.write_text(json.dumps(command_plan()), encoding="utf-8")
        bindings_path = root / "tool-bindings.json"
        bindings_path.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "bindings": {"python": {"executable": str(executable.resolve())}},
                }
            ),
            encoding="utf-8",
        )
        return subject, plan_path, bindings_path

    def test_command_preview_cli_outputs_only_the_normalized_preview(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, bindings_path = self._fixture(root)
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "veritrail.command_preview._require_windows_command_capability",
                return_value=None,
            ), mock.patch.dict(
                os.environ,
                {"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
                clear=True,
            ), redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "command-preview",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings_path),
                    ]
                )

            self.assertEqual(0, code)
            self.assertEqual("", stderr.getvalue())
            preview = json.loads(stdout.getvalue())
            self.assertEqual("0.1", preview["schema_version"])
            self.assertEqual("python-unit-check", preview["command_id"])
            self.assertEqual(64, len(preview["preview_sha256"]))
            self.assertNotIn(str(subject.resolve()), stdout.getvalue())
            self.assertNotIn(str(bindings_path.resolve()), stdout.getvalue())
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(before, after)

    def test_missing_capability_is_sanitized_and_creates_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, bindings_path = self._fixture(root)
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "veritrail.command_preview._require_windows_command_capability",
                side_effect=SafetyError("M9 command capability is unavailable"),
            ), redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "command-preview",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings_path),
                    ]
                )

            self.assertEqual(2, code)
            self.assertEqual("", stdout.getvalue())
            error = json.loads(stderr.getvalue())
            self.assertIn("capability is unavailable", error["error"])
            self.assertNotIn(str(root.resolve()), stderr.getvalue())
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(before, after)

    def test_plan_v04_is_rejected_before_capability_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, bindings_path = self._fixture(root)
            plan_path.write_text(json.dumps(orchestration_plan()), encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "veritrail.command_preview._require_windows_command_capability"
            ) as capability, redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "command-preview",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings_path),
                    ]
                )

            self.assertEqual(2, code)
            capability.assert_not_called()
            self.assertIn("schema_version '0.5'", stderr.getvalue())

    def test_unexpected_internal_error_is_structured_and_path_free(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, bindings_path = self._fixture(root)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "veritrail.cli.build_command_preview",
                side_effect=RuntimeError(f"unexpected failure at {root.resolve()}"),
            ), redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "command-preview",
                        "--plan",
                        str(plan_path),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings_path),
                    ]
                )

            self.assertEqual(1, code)
            self.assertEqual("", stdout.getvalue())
            error = json.loads(stderr.getvalue())
            self.assertEqual("COMMAND_PREVIEW_INTERNAL_ERROR", error["error"]["code"])
            self.assertNotIn(str(root.resolve()), stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
