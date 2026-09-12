from __future__ import annotations

import ast
import inspect
import sys
import unittest
from dataclasses import fields
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

import veritrail_review
from veritrail_review import (
    DerivationInputRequest,
    DerivationInputRuntime,
    SourceSnapshotRequest,
    SourceSnapshotRuntime,
    create_source_snapshot,
    bind_derivation_inputs,
)


class SourceSnapshotBoundaryTests(unittest.TestCase):
    def test_product_modules_do_not_import_core_platform_browser_or_project_code(self) -> None:
        forbidden_roots = {
            "veritrail",
            "veritrail_github",
            "playwright",
            "jsonschema",
        }
        violations: list[str] = []
        for path in sorted((SOURCE_ROOT / "veritrail_review").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names.append(node.module)
                for name in names:
                    if name.split(".", 1)[0] in forbidden_roots:
                        violations.append(f"{path.name}:{node.lineno}:{name}")
        self.assertEqual(violations, [])

    def test_request_cannot_select_git_or_acquisition_budget(self) -> None:
        request_fields = {item.name for item in fields(SourceSnapshotRequest)}
        self.assertEqual(
            request_fields,
            {"spec", "repository_path", "output_directory"},
        )
        runtime_fields = {item.name for item in fields(SourceSnapshotRuntime)}
        self.assertEqual(runtime_fields, {"git_executable"})
        parameters = inspect.signature(create_source_snapshot).parameters
        self.assertNotIn("budget", parameters)
        self.assertNotIn("acquisition_budget", parameters)

    def test_top_level_api_does_not_publish_test_controls_or_release_identity(self) -> None:
        self.assertNotIn("tightened_budget_for_testing", veritrail_review.__all__)
        self.assertNotIn(
            "tightened_derivation_input_safety_profile_for_testing",
            veritrail_review.__all__,
        )
        self.assertNotIn(
            "DEFAULT_DERIVATION_INPUT_SAFETY_PROFILE",
            veritrail_review.__all__,
        )
        self.assertFalse(hasattr(veritrail_review, "__version__"))

    def test_derivation_input_request_cannot_select_outputs_or_execution_controls(self) -> None:
        self.assertEqual(
            {item.name for item in fields(DerivationInputRequest)},
            {
                "source_snapshot_path",
                "review_policy_path",
                "derivation_profile_path",
                "repository_path",
            },
        )
        self.assertEqual(
            {item.name for item in fields(DerivationInputRuntime)},
            {"git_executable"},
        )
        parameters = inspect.signature(bind_derivation_inputs).parameters
        self.assertEqual(set(parameters), {"request", "runtime"})

    def test_implemented_slices_have_no_cli_provider_or_derivation_products(self) -> None:
        module_names = {
            path.stem
            for path in (SOURCE_ROOT / "veritrail_review").glob("*.py")
        }
        self.assertTrue(
            {
                "canonical",
                "contracts",
                "errors",
                "git_objects",
                "publisher",
                "source_snapshot",
                "derivation_input",
                "derivation_input_contracts",
            }
            <= module_names
        )
        self.assertTrue(
            module_names.isdisjoint(
                {
                    "cli",
                    "provider",
                    "review_policy",
                    "facts",
                    "relations",
                    "slices",
                    "coverage",
                    "manifest",
                }
            )
        )


if __name__ == "__main__":
    unittest.main()
