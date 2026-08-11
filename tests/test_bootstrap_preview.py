from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from veritrail.bootstrap_preview import build_bootstrap_preview
from veritrail.errors import SafetyError, ValidationError
from veritrail.plan import seal_plan

from tests.support import ROOT, bootstrap_plan, sealed_bootstrap_profile


class BootstrapPreviewTests(unittest.TestCase):
    def _fixture(self, root: Path) -> tuple[Path, Path]:
        subject = root / "subject"
        (subject / "src").mkdir(parents=True)
        (subject / "tests").mkdir()
        dependency = root / "dependency.exe"
        application = root / "application.exe"
        dependency.write_bytes(b"MZdependency")
        application.write_bytes(b"MZapplication")
        bindings = root / "tool-bindings.json"
        bindings.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "bindings": {
                        "python-dependency": {"executable": str(dependency.resolve())},
                        "python-application": {"executable": str(application.resolve())},
                    },
                }
            ),
            encoding="utf-8",
        )
        return subject, bindings

    def test_preview_is_deterministic_path_free_and_typed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, bindings = self._fixture(root)
            profile = sealed_bootstrap_profile()
            plan = seal_plan(bootstrap_plan(profile), profile)
            environment = {"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"}
            with mock.patch(
                "veritrail.bootstrap_preview._require_windows_bootstrap_capability",
                return_value=None,
            ), mock.patch(
                "veritrail.bootstrap_preview.assert_loopback_ports_free",
                return_value=None,
            ):
                first = build_bootstrap_preview(
                    plan,
                    profile,
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    environment=environment,
                )
                second = build_bootstrap_preview(
                    plan,
                    profile,
                    subject_root=subject,
                    tool_bindings_path=bindings,
                    environment=environment,
                )
            self.assertEqual(first, second)
            self.assertEqual(["dependency", "application"], first["start_order"])
            self.assertEqual("node_origin", first["nodes"][1]["arguments"][3]["kind"])
            self.assertEqual(
                "http://127.0.0.1:18771", first["nodes"][1]["arguments"][3]["value"]
            )
            encoded = json.dumps(first)
            self.assertNotIn(str(subject.resolve()), encoded)
            self.assertNotIn(str(bindings.resolve()), encoded)
            self.assertEqual(64, len(first["preview_sha256"]))
            schema = json.loads(
                (ROOT / "schemas" / "bootstrap-preview-0.1.schema.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(set(schema["required"]), set(first))
            self.assertEqual(set(schema["$defs"]["node"]["required"]), set(first["nodes"][0]))

    def test_port_conflict_and_missing_binding_are_pre_run_rejections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subject, bindings = self._fixture(root)
            profile = sealed_bootstrap_profile()
            plan = seal_plan(bootstrap_plan(profile), profile)
            with mock.patch(
                "veritrail.bootstrap_preview._require_windows_bootstrap_capability",
                return_value=None,
            ), mock.patch(
                "veritrail.bootstrap_preview.assert_loopback_ports_free",
                side_effect=SafetyError(
                    "ProjectProfile requires both sealed loopback ports to be FREE"
                ),
            ):
                with self.assertRaisesRegex(SafetyError, "ports to be FREE"):
                    build_bootstrap_preview(
                        plan,
                        profile,
                        subject_root=subject,
                        tool_bindings_path=bindings,
                    )

            document = json.loads(bindings.read_text(encoding="utf-8"))
            del document["bindings"]["python-application"]
            bindings.write_text(json.dumps(document), encoding="utf-8")
            with mock.patch(
                "veritrail.bootstrap_preview._require_windows_bootstrap_capability",
                return_value=None,
            ), mock.patch(
                "veritrail.bootstrap_preview.assert_loopback_ports_free",
                return_value=None,
            ):
                with self.assertRaisesRegex(ValidationError, "required binding"):
                    build_bootstrap_preview(
                        plan,
                        profile,
                        subject_root=subject,
                        tool_bindings_path=bindings,
                        environment={"SYSTEMROOT": "C:\\Windows", "WINDIR": "C:\\Windows"},
                    )


if __name__ == "__main__":
    unittest.main()
