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
from veritrail.plan import seal_plan

from tests.support import bootstrap_plan, sealed_bootstrap_profile


class BootstrapPreviewCliTests(unittest.TestCase):
    def _fixture(self, root: Path) -> tuple[Path, Path, Path, Path]:
        subject = root / "subject"
        (subject / "src").mkdir(parents=True)
        (subject / "tests").mkdir()
        first = root / "dependency.exe"
        second = root / "application.exe"
        first.write_bytes(b"MZdependency")
        second.write_bytes(b"MZapplication")
        profile = sealed_bootstrap_profile()
        plan = seal_plan(bootstrap_plan(profile), profile)
        profile_path = root / "sealed-profile.json"
        plan_path = root / "sealed-plan.json"
        bindings_path = root / "tool-bindings.json"
        profile_path.write_text(json.dumps(profile), encoding="utf-8")
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        bindings_path.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "bindings": {
                        "python-dependency": {"executable": str(first.resolve())},
                        "python-application": {"executable": str(second.resolve())},
                    },
                }
            ),
            encoding="utf-8",
        )
        return subject, plan_path, profile_path, bindings_path

    def test_cli_outputs_only_preview_and_creates_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings = self._fixture(root)
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "veritrail.bootstrap_preview._require_windows_bootstrap_capability",
                return_value=None,
            ), mock.patch(
                "veritrail.bootstrap_preview.assert_loopback_ports_free",
                return_value=None,
            ), mock.patch.dict(
                os.environ,
                {"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
                clear=True,
            ), redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "bootstrap-preview",
                        "--plan",
                        str(plan),
                        "--profile",
                        str(profile),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings),
                    ]
                )
            self.assertEqual(0, code)
            self.assertEqual("", stderr.getvalue())
            preview = json.loads(stdout.getvalue())
            self.assertEqual("0.1", preview["schema_version"])
            self.assertNotIn(str(root.resolve()), stdout.getvalue())
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(before, after)

    def test_cli_rejects_unsealed_plan_before_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan_path, profile, bindings = self._fixture(root)
            plan_path.write_text(json.dumps(bootstrap_plan(sealed_bootstrap_profile())), encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "veritrail.bootstrap_preview._require_windows_bootstrap_capability"
            ) as capability, redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "bootstrap-preview",
                        "--plan",
                        str(plan_path),
                        "--profile",
                        str(profile),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings),
                    ]
                )
            self.assertEqual(2, code)
            capability.assert_not_called()
            self.assertIn("plan is not sealed", stderr.getvalue())

    def test_unexpected_internal_error_is_structured_path_free_and_non_persistent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, plan, profile, bindings = self._fixture(root)
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "veritrail.cli.build_bootstrap_preview",
                side_effect=RuntimeError(f"unexpected failure at {root.resolve()}"),
            ), redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "bootstrap-preview",
                        "--plan",
                        str(plan),
                        "--profile",
                        str(profile),
                        "--subject-root",
                        str(subject),
                        "--tool-bindings",
                        str(bindings),
                    ]
                )
            self.assertEqual(1, code)
            self.assertEqual("", stdout.getvalue())
            error = json.loads(stderr.getvalue())
            self.assertEqual("BOOTSTRAP_PREVIEW_INTERNAL_ERROR", error["error"]["code"])
            self.assertNotIn(str(root.resolve()), stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
