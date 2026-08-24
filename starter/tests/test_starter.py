from __future__ import annotations

import copy
import io
import importlib.resources
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from veritrail.errors import ValidationError
from veritrail.plan import validate_plan
from veritrail.project_profile import project_profile_digest, validate_project_profile

from veritrail_starter.cli import main
from veritrail_starter.contract import build_documents, normalize_answers
from veritrail_starter.doctor import supported_host
from veritrail_starter.errors import StarterError
from veritrail_starter.workspace import (
    handoff_workspace,
    initialize_workspace,
    render_workspace,
    validate_workspace,
)


class StarterContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        executable = Path(sys.executable)
        if executable.suffix.casefold() != ".exe":
            executable = self.root / "python.exe"
            executable.write_bytes(b"test executable identity only")
        self.answers = {
            "schema_version": "0.1",
            "preset": "single-webapp",
            "workspace_id": "starter-demo",
            "question": "Does the selected application satisfy the explicit browser checks?",
            "subject": {
                "root": str(self.root),
                "id": "starter-demo",
                "version": "1",
                "source_ref": ".",
                "working_directory": ".",
                "watch_roots": ["."],
            },
            "application": {
                "executable": str(executable),
                "arguments": [
                    {"literal": "-m"},
                    {"literal": "http.server"},
                    {"node_port": "application"},
                ],
                "port": 18774,
                "health_path": "/health",
                "expected_status": 200,
            },
            "browser": {
                "start_url": "http://127.0.0.1:18774/",
                "allowed_origin": "http://127.0.0.1:18774",
                "headless": True,
                "timeout_ms": 10000,
                "viewports": [
                    {"name": "desktop", "width": 1440, "height": 960, "is_mobile": False},
                    {"name": "mobile", "width": 390, "height": 844, "is_mobile": True},
                ],
                "steps": [
                    {"id": "page-ready", "action": "expect_visible", "selector": "body"}
                ],
                "screenshot_safety": "UNREDACTED_OPERATOR_ACKNOWLEDGED",
            },
            "budgets": {
                "max_artifact_bytes": 5242880,
                "max_watch_files": 2000,
                "max_watch_total_bytes": 67108864,
                "lifecycle_timeout_ms": 120000,
                "max_stdout_bytes": 262144,
                "max_stderr_bytes": 262144,
                "max_processes": 8,
                "application_memory_mb": 512,
                "browser_memory_mb": 1024,
            },
            "timeouts": {
                "readiness_attempt_ms": 500,
                "readiness_total_ms": 10000,
                "readiness_interval_ms": 100,
                "shutdown_process_ms": 5000,
                "shutdown_port_ms": 5000,
                "shutdown_reader_ms": 5000,
            },
            "random_seed": 20260823,
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def normalized(self) -> dict[str, object]:
        return normalize_answers(copy.deepcopy(self.answers))

    def static_answers(self) -> dict[str, object]:
        answers = copy.deepcopy(self.answers)
        (self.root / "index.html").write_text(
            "<!doctype html><html><body><main>static ready</main></body></html>",
            encoding="utf-8",
        )
        application = answers.pop("application")
        answers["schema_version"] = "0.2"
        answers["preset"] = "static-site"
        answers["question"] = "Does the static document satisfy the explicit browser checks?"
        answers["static_site"] = {
            "python_executable": application["executable"],
            "entry_file": "index.html",
            "port": application["port"],
            "expected_status": 200,
            "requires_build": False,
            "requires_remote_assets": False,
        }
        answers["browser"]["start_url"] = f"http://127.0.0.1:{application['port']}/index.html"
        return answers

    def test_packaged_answers_schema_is_strict_and_versioned(self) -> None:
        schema_path = importlib.resources.files("veritrail_starter").joinpath(
            "schemas/answers-0.1.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["budgets"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["timeouts"]["additionalProperties"])

        schema_02_path = importlib.resources.files("veritrail_starter").joinpath(
            "schemas/answers-0.2.schema.json"
        )
        schema_02 = json.loads(schema_02_path.read_text(encoding="utf-8"))
        self.assertEqual(schema_02["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(len(schema_02["oneOf"]), 2)
        self.assertFalse(schema_02["$defs"]["staticSite"]["additionalProperties"])
        self.assertFalse(schema_02["$defs"]["staticSiteRuntime"]["additionalProperties"])
        self.assertIsNotNone(
            re.fullmatch(schema_02["$defs"]["entryFile"]["pattern"], "INDEX.HTML")
        )
        self.assertIsNotNone(
            re.fullmatch(
                schema_02["$defs"]["entryFile"]["pattern"],
                f"pages/{'a' * 59}.html",
            )
        )
        self.assertIsNone(
            re.fullmatch(
                schema_02["$defs"]["entryFile"]["pattern"],
                f"pages/{'a' * 60}.html",
            )
        )

    def test_windows_11_detection_uses_kernel_build_not_release_label(self) -> None:
        windows_11 = mock.Mock(major=10, build=22621)
        windows_10 = mock.Mock(major=10, build=19045)
        with mock.patch("veritrail_starter.doctor.os.name", "nt"):
            with mock.patch(
                "veritrail_starter.doctor.sys.getwindowsversion",
                return_value=windows_11,
                create=True,
            ):
                self.assertTrue(supported_host())
            with mock.patch(
                "veritrail_starter.doctor.sys.getwindowsversion",
                return_value=windows_10,
                create=True,
            ):
                self.assertFalse(supported_host())

    def test_generated_drafts_are_core_valid_and_unsealed(self) -> None:
        profile, plan, bindings = build_documents(self.normalized())
        self.assertNotIn("seal", profile)
        self.assertNotIn("seal", plan)
        validate_project_profile(profile)
        digest = project_profile_digest(profile)
        ephemeral = copy.deepcopy(profile)
        ephemeral["seal"] = {"algorithm": "sha256", "digest": digest}
        validate_plan(plan, ephemeral)
        self.assertEqual(plan["bootstrap_profile"]["profile_sha256"], digest)
        self.assertEqual(bindings["schema_version"], "0.1")

    def test_static_site_generates_fixed_owned_server_drafts(self) -> None:
        answers = normalize_answers(self.static_answers())
        profile, plan, bindings = build_documents(answers)
        validate_project_profile(profile)
        digest = project_profile_digest(profile)
        ephemeral = copy.deepcopy(profile)
        ephemeral["seal"] = {"algorithm": "sha256", "digest": digest}
        validate_plan(plan, ephemeral)
        node = profile["nodes"][0]
        self.assertEqual(node["tool_binding"], "python-static-site")
        self.assertEqual(
            node["arguments"],
            [
                {"literal": "-m"},
                {"literal": "http.server"},
                {"node_port": "application"},
                {"literal": "--bind"},
                {"literal": "127.0.0.1"},
            ],
        )
        self.assertEqual(node["readiness"]["path"], "/index.html")
        self.assertEqual(plan["baseline"]["id"], "starter-static-site-0.2")
        self.assertEqual(set(bindings["bindings"]), {"python-static-site"})
        self.assertNotIn("seal", profile)
        self.assertNotIn("seal", plan)

    def test_static_site_fails_closed_for_build_remote_or_missing_entry(self) -> None:
        build = self.static_answers()
        build["static_site"]["requires_build"] = True
        with self.assertRaises(StarterError) as caught:
            normalize_answers(build)
        self.assertEqual(caught.exception.code, "UNSUPPORTED")

        remote = self.static_answers()
        remote["static_site"]["requires_remote_assets"] = True
        with self.assertRaises(StarterError) as caught:
            normalize_answers(remote)
        self.assertEqual(caught.exception.code, "UNSUPPORTED")

        missing = self.static_answers()
        missing["static_site"]["entry_file"] = "missing.html"
        missing["browser"]["start_url"] = "http://127.0.0.1:18774/missing.html"
        with self.assertRaises(StarterError) as caught:
            normalize_answers(missing)
        self.assertEqual(caught.exception.code, "INVALID_INPUT")

    def test_static_site_accepts_nested_ordinary_uppercase_html_entry(self) -> None:
        nested = self.root / "pages"
        nested.mkdir()
        (nested / "INDEX.HTML").write_text(
            "<!doctype html><html><body>ready</body></html>", encoding="utf-8"
        )
        answers = self.static_answers()
        answers["static_site"]["entry_file"] = "pages/INDEX.HTML"
        answers["browser"]["start_url"] = "http://127.0.0.1:18774/pages/INDEX.HTML"
        normalized = normalize_answers(answers)
        self.assertEqual(normalized["static_site"]["entry_file"], "pages/INDEX.HTML")

    def test_static_site_rejects_reparse_in_entry_path(self) -> None:
        nested = self.root / "pages"
        nested.mkdir()
        (nested / "index.html").write_text(
            "<!doctype html><html><body>ready</body></html>", encoding="utf-8"
        )
        answers = self.static_answers()
        answers["static_site"]["entry_file"] = "pages/index.html"
        answers["browser"]["start_url"] = "http://127.0.0.1:18774/pages/index.html"

        from veritrail_starter import contract as contract_module

        original = contract_module._is_reparse
        nested_resolved = nested.resolve(strict=True)

        def mark_nested_as_reparse(path: Path) -> bool:
            return path.resolve(strict=True) == nested_resolved or original(path)

        with mock.patch(
            "veritrail_starter.contract._is_reparse", side_effect=mark_nested_as_reparse
        ):
            with self.assertRaises(StarterError) as caught:
                normalize_answers(answers)
        self.assertEqual(caught.exception.code, "INVALID_INPUT")

    def test_render_is_byte_deterministic(self) -> None:
        answers = self.normalized()
        first = render_workspace(answers)
        second = render_workspace(copy.deepcopy(answers))
        self.assertEqual(first, second)
        self.assertNotIn(b"timestamp", b"".join(first.values()).lower())

    def test_long_workspace_id_produces_bounded_unique_identifiers(self) -> None:
        self.answers["workspace_id"] = "a" * 64
        profile, plan, _ = build_documents(self.normalized())
        self.assertLessEqual(len(profile["profile_id"]), 64)
        self.assertLessEqual(len(plan["plan_id"]), 64)
        self.assertNotEqual(profile["profile_id"], plan["plan_id"])

    def test_init_is_atomic_and_never_overwrites(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            result = initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        self.assertEqual(result["authoring_state"], "DRAFT")
        workspace = self.root / ".veritrail"
        self.assertTrue(validate_workspace(workspace)["valid"])
        before = {item.name: item.read_bytes() for item in workspace.iterdir()}
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            with self.assertRaises(StarterError) as caught:
                initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        self.assertEqual(caught.exception.code, "OUTPUT_CONFLICT")
        after = {item.name: item.read_bytes() for item in workspace.iterdir()}
        self.assertEqual(before, after)

    def test_static_site_workspace_manifest_is_preset_specific(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            initialize_workspace(self.static_answers(), "static-site")
        workspace = self.root / ".veritrail"
        manifest = json.loads((workspace / "starter-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["preset"], {"id": "static-site", "version": "0.2"})
        review = (workspace / "REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("Build required: `false`", review)
        self.assertIn("Required remote assets: `false`", review)
        self.assertTrue(validate_workspace(workspace)["valid"])

    def test_workspace_mutation_is_detected(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        workspace = self.root / ".veritrail"
        (workspace / "REVIEW.md").write_text("changed\n", encoding="utf-8")
        with self.assertRaises(StarterError) as caught:
            validate_workspace(workspace)
        self.assertEqual(caught.exception.code, "WORKSPACE_INVALID")

    def test_workspace_requires_the_exact_creating_starter_version(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        workspace = self.root / ".veritrail"
        manifest_path = workspace / "starter-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["starter_version"] = "0.1.0"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(StarterError) as caught:
            validate_workspace(workspace)
        self.assertEqual(caught.exception.code, "WORKSPACE_INVALID")

    def test_workspace_mutation_between_snapshots_is_detected(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        workspace = self.root / ".veritrail"
        from veritrail_starter import workspace as workspace_module

        original = workspace_module._read_workspace
        calls = 0

        def mutate_after_first_snapshot(path: Path):
            nonlocal calls
            result = original(path)
            calls += 1
            if calls == 1:
                (workspace / "REVIEW.md").write_text("changed after snapshot\n", encoding="utf-8")
            return result

        with mock.patch(
            "veritrail_starter.workspace._read_workspace",
            side_effect=mutate_after_first_snapshot,
        ):
            with self.assertRaises(StarterError) as caught:
                validate_workspace(workspace)
        self.assertEqual(caught.exception.code, "WORKSPACE_INVALID")

    def test_missing_local_fact_is_reported_as_workspace_invalid(self) -> None:
        executable = self.root / "application.exe"
        executable.write_bytes(b"test executable identity only")
        self.answers["application"]["executable"] = str(executable)
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        executable.unlink()
        with self.assertRaises(StarterError) as caught:
            validate_workspace(self.root / ".veritrail")
        self.assertEqual(caught.exception.code, "WORKSPACE_INVALID")

    def test_failed_publish_removes_only_the_owned_flat_temp_workspace(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            with mock.patch("pathlib.Path.rename", side_effect=OSError("publish failed")):
                with self.assertRaises(OSError):
                    initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        self.assertFalse((self.root / ".veritrail").exists())
        self.assertEqual(list(self.root.glob(".veritrail.tmp-*")), [])

    def test_workspace_reparse_entry_is_rejected(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        workspace = self.root / ".veritrail"
        with mock.patch("veritrail_starter.workspace._is_reparse", return_value=True):
            with self.assertRaises(StarterError) as caught:
                validate_workspace(workspace)
        self.assertEqual(caught.exception.code, "WORKSPACE_INVALID")

    def test_unsafe_workspace_file_read_maps_to_workspace_invalid(self) -> None:
        with mock.patch(
            "veritrail_starter.workspace._read_workspace",
            side_effect=ValidationError(["unsafe file node"]),
        ):
            with self.assertRaises(StarterError) as caught:
                validate_workspace(self.root / ".veritrail")
        self.assertEqual(caught.exception.code, "WORKSPACE_INVALID")

    def test_windows_reserved_relative_path_is_rejected(self) -> None:
        reserved = copy.deepcopy(self.answers)
        reserved["subject"]["working_directory"] = "CON.txt"
        with self.assertRaises(StarterError) as caught:
            normalize_answers(reserved)
        self.assertEqual(caught.exception.code, "INVALID_INPUT")

    def test_nested_argument_and_browser_step_types_are_rejected_early(self) -> None:
        bad_argument = copy.deepcopy(self.answers)
        bad_argument["application"]["arguments"] = [{"literal": ["not", "a", "string"]}]
        with self.assertRaises(StarterError) as caught:
            normalize_answers(bad_argument)
        self.assertEqual(caught.exception.code, "INVALID_INPUT")

        bad_step = copy.deepcopy(self.answers)
        bad_step["browser"]["steps"] = [
            {"id": "page-ready", "action": "expect_visible", "selector": 42}
        ]
        with self.assertRaises(StarterError) as caught:
            normalize_answers(bad_step)
        self.assertEqual(caught.exception.code, "INVALID_INPUT")

    def test_shell_secret_non_loopback_and_missing_business_check_fail_closed(self) -> None:
        shell = self.root / "cmd.exe"
        shell.write_bytes(b"not executed")
        shell_answers = copy.deepcopy(self.answers)
        shell_answers["application"]["executable"] = str(shell)
        with self.assertRaises(StarterError) as caught:
            normalize_answers(shell_answers)
        self.assertEqual(caught.exception.code, "UNSUPPORTED")

        secret_answers = copy.deepcopy(self.answers)
        secret_answers["question"] = "Bearer abcdefghijklmnopqrstuvwxyz"
        with self.assertRaises(StarterError) as caught:
            normalize_answers(secret_answers)
        self.assertEqual(caught.exception.code, "UNSUPPORTED")

        remote_answers = copy.deepcopy(self.answers)
        remote_answers["browser"]["start_url"] = "http://192.0.2.1:18774/"
        with self.assertRaises(StarterError) as caught:
            normalize_answers(remote_answers)
        self.assertEqual(caught.exception.code, "UNSUPPORTED")

        no_check = copy.deepcopy(self.answers)
        no_check["browser"]["steps"] = [
            {"id": "click-only", "action": "click", "selector": "button"}
        ]
        with self.assertRaises(StarterError) as caught:
            normalize_answers(no_check)
        self.assertEqual(caught.exception.code, "UNSUPPORTED")

    def test_handoff_only_prints_manual_commands(self) -> None:
        with mock.patch("veritrail_starter.workspace.require_supported_host"):
            initialize_workspace(copy.deepcopy(self.answers), "single-webapp")
        workspace = self.root / ".veritrail"
        report = handoff_workspace(workspace)
        self.assertEqual(report["execution"], "NOT_PERFORMED")
        script = (workspace / "handoff.ps1").read_text(encoding="utf-8")
        self.assertNotIn("Invoke-Expression", script)
        self.assertNotIn("Start-Process", script)
        self.assertNotIn("& veritrail", script)
        self.assertTrue(
            all(not line.strip() or line.startswith("#") or line.startswith("Write-Output") for line in script.splitlines())
        )

    def test_cli_stdout_is_exactly_one_json_document(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["doctor"])
        self.assertEqual(code, 0)
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        document = json.loads(lines[0])
        self.assertEqual(document["schema_version"], "0.1")
        self.assertEqual(document["command"], "doctor")

    def test_cli_parse_failure_uses_the_same_single_json_protocol(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["init"])
        self.assertEqual(code, 2)
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        document = json.loads(lines[0])
        self.assertEqual(document["command"], "init")
        self.assertEqual(document["outcome"], "ERROR")
        self.assertEqual(document["error"]["code"], "INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
