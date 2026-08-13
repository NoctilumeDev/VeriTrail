from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from veritrail.atomic_publish import (
    WINDOWS_RENAME_ATTEMPTS,
    publish_staged_directory,
)
from veritrail.errors import SafetyError


def _windows_rename_error(code: int) -> PermissionError:
    error = PermissionError(code, "rename blocked")
    error.winerror = code
    return error


class AtomicPublishTests(unittest.TestCase):
    def test_retries_only_transient_windows_lock_then_publishes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = root / ".stage"
            output = root / "bundle"
            stage.mkdir()
            (stage / "report.json").write_text("{}", encoding="utf-8")
            attempts = 0
            sleeps: list[float] = []

            def rename(source: Path, target: Path) -> None:
                nonlocal attempts
                attempts += 1
                if attempts < 3:
                    raise _windows_rename_error(32)
                source.rename(target)

            with patch("veritrail.atomic_publish.os.name", "nt"):
                publish_staged_directory(
                    stage,
                    output,
                    rename=rename,
                    sleep=sleeps.append,
                )

            self.assertEqual(3, attempts)
            self.assertEqual(2, len(sleeps))
            self.assertFalse(stage.exists())
            self.assertEqual("{}", (output / "report.json").read_text(encoding="utf-8"))

    def test_target_appearing_during_retry_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = root / ".stage"
            output = root / "bundle"
            stage.mkdir()

            def rename(_source: Path, target: Path) -> None:
                target.mkdir()
                (target / "owner.txt").write_text("external", encoding="utf-8")
                raise _windows_rename_error(5)

            with patch("veritrail.atomic_publish.os.name", "nt"):
                with self.assertRaisesRegex(SafetyError, "refusing to overwrite"):
                    publish_staged_directory(stage, output, rename=rename)

            self.assertTrue(stage.exists())
            self.assertEqual("external", (output / "owner.txt").read_text(encoding="utf-8"))

    def test_permanent_windows_lock_is_bounded_and_preserves_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = root / ".stage"
            output = root / "bundle"
            stage.mkdir()
            attempts = 0

            def rename(_source: Path, _target: Path) -> None:
                nonlocal attempts
                attempts += 1
                raise _windows_rename_error(33)

            with patch("veritrail.atomic_publish.os.name", "nt"):
                with self.assertRaises(PermissionError):
                    publish_staged_directory(
                        stage,
                        output,
                        rename=rename,
                        sleep=lambda _seconds: None,
                    )

            self.assertEqual(WINDOWS_RENAME_ATTEMPTS, attempts)
            self.assertTrue(stage.exists())
            self.assertFalse(output.exists())

    def test_non_windows_or_unrelated_error_is_not_retried(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = root / ".stage"
            output = root / "bundle"
            stage.mkdir()
            attempts = 0

            def rename(_source: Path, _target: Path) -> None:
                nonlocal attempts
                attempts += 1
                raise OSError(22, "invalid")

            with self.assertRaises(OSError):
                publish_staged_directory(
                    stage,
                    output,
                    rename=rename,
                    sleep=lambda _seconds: None,
                )

            self.assertEqual(1, attempts)


if __name__ == "__main__":
    unittest.main()
