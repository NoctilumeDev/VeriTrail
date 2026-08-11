from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from veritrail.canonical import sha256_json
from veritrail.command_preview import build_command_preview, load_tool_bindings
from veritrail.errors import SafetyError, ValidationError
from veritrail.plan import seal_plan

from tests.support import command_plan


class CommandPreviewTests(unittest.TestCase):
    def _fixture(self, root: Path, *, executable_name: str = "python.exe") -> tuple[Path, Path, Path]:
        subject = root / "subject"
        (subject / "src").mkdir(parents=True)
        (subject / "tests").mkdir()
        executable = root / executable_name
        executable.write_bytes(b"MZ" + b"veritrail-test-executable")
        bindings = root / "tool-bindings.json"
        bindings.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "bindings": {"python": {"executable": str(executable.resolve())}},
                }
            ),
            encoding="utf-8",
        )
        return subject, executable, bindings

    def _preview(
        self,
        subject: Path,
        bindings: Path,
        *,
        environment: dict[str, str] | None = None,
    ) -> dict:
        with mock.patch(
            "veritrail.command_preview._require_windows_command_capability",
            return_value=None,
        ):
            return build_command_preview(
                seal_plan(command_plan()),
                subject_root=subject,
                tool_bindings_path=bindings,
                environment=environment
                or {"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
            )

    def test_preview_is_deterministic_bound_and_does_not_persist_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, executable, bindings = self._fixture(root)
            first = self._preview(subject, bindings)
            second = self._preview(subject, bindings)

            self.assertEqual(first, second)
            unsigned = copy.deepcopy(first)
            digest = unsigned.pop("preview_sha256")
            self.assertEqual(digest, sha256_json(unsigned))
            encoded = json.dumps(first, ensure_ascii=False, sort_keys=True)
            self.assertNotIn(str(subject.resolve()), encoded)
            self.assertNotIn(str(executable.resolve()), encoded)
            self.assertEqual("python.exe", first["executable"]["basename"])
            self.assertEqual(False, first["environment"]["values_persisted"])
            self.assertEqual("NOT_PROVEN", first["claims"]["write_activity"])

    def test_preview_changes_when_executable_path_or_environment_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, executable, bindings = self._fixture(root)
            first = self._preview(subject, bindings)

            second_executable = root / "tools" / "python.exe"
            second_executable.parent.mkdir()
            second_executable.write_bytes(executable.read_bytes())
            bindings.write_text(
                json.dumps(
                    {
                        "schema_version": "0.1",
                        "bindings": {
                            "python": {"executable": str(second_executable.resolve())}
                        },
                    }
                ),
                encoding="utf-8",
            )
            moved = self._preview(subject, bindings)
            self.assertEqual(first["executable"]["sha256"], moved["executable"]["sha256"])
            self.assertNotEqual(
                first["executable"]["path_identity_sha256"],
                moved["executable"]["path_identity_sha256"],
            )
            self.assertNotEqual(first["preview_sha256"], moved["preview_sha256"])

            changed_environment = self._preview(
                subject,
                bindings,
                environment={"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\WIN"},
            )
            self.assertNotEqual(
                moved["environment"]["projection_sha256"],
                changed_environment["environment"]["projection_sha256"],
            )
            self.assertNotEqual(moved["preview_sha256"], changed_environment["preview_sha256"])

    def test_tool_bindings_and_local_resolution_reject_unsafe_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, _, bindings = self._fixture(root)
            plan = seal_plan(command_plan())

            unsafe_documents = (
                {"schema_version": "0.2", "bindings": {"python": {"executable": "x"}}},
                {
                    "schema_version": "0.1",
                    "bindings": {"Python": {"executable": "x"}},
                },
                {
                    "schema_version": "0.1",
                    "bindings": {"python": {"executable": "x", "arguments": []}},
                },
            )
            for index, document in enumerate(unsafe_documents):
                with self.subTest(document=index):
                    bindings.write_text(json.dumps(document), encoding="utf-8")
                    with self.assertRaises(ValidationError):
                        load_tool_bindings(bindings)

            relative = {
                "schema_version": "0.1",
                "bindings": {"python": {"executable": "python.exe"}},
            }
            bindings.write_text(json.dumps(relative), encoding="utf-8")
            with mock.patch(
                "veritrail.command_preview._require_windows_command_capability",
                return_value=None,
            ), self.assertRaisesRegex(ValidationError, "absolute local drive"):
                build_command_preview(
                    plan,
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    environment={"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
                )

    def test_forbidden_executable_and_missing_subject_scope_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, _, bindings = self._fixture(root, executable_name="cmd.exe")
            with mock.patch(
                "veritrail.command_preview._require_windows_command_capability",
                return_value=None,
            ), self.assertRaisesRegex(SafetyError, "outside the frozen M9"):
                build_command_preview(
                    seal_plan(command_plan()),
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    environment={"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
                )

            safe_executable = root / "python.exe"
            safe_executable.write_bytes(b"MZsafe")
            bindings.write_text(
                json.dumps(
                    {
                        "schema_version": "0.1",
                        "bindings": {"python": {"executable": str(safe_executable.resolve())}},
                    }
                ),
                encoding="utf-8",
            )
            (subject / "tests").rmdir()
            with mock.patch(
                "veritrail.command_preview._require_windows_command_capability",
                return_value=None,
            ), self.assertRaisesRegex(ValidationError, "ordinary directory"):
                build_command_preview(
                    seal_plan(command_plan()),
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    environment={"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
                )

    def test_missing_capability_stops_before_local_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, _, bindings = self._fixture(root)
            with mock.patch(
                "veritrail.command_preview._require_windows_command_capability",
                side_effect=SafetyError("capability unavailable"),
            ), self.assertRaisesRegex(SafetyError, "capability unavailable"):
                build_command_preview(
                    seal_plan(command_plan()),
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    environment={"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
                )


if __name__ == "__main__":
    unittest.main()
