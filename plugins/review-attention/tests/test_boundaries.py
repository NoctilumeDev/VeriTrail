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
    BudgetContext,
    BudgetPrimitiveError,
    DerivationInputRequest,
    DerivationInputRuntime,
    SourceSnapshotRequest,
    SourceSnapshotRuntime,
    create_source_snapshot,
    admit_derivation_budget,
    bind_derivation_inputs,
)
from veritrail_review.budget import ExecutionBudgetLimits


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
        self.assertNotIn("ExecutionBudgetLimits", veritrail_review.__all__)
        self.assertNotIn("MemoryAttributionState", veritrail_review.__all__)
        self.assertNotIn("_run_owned_process_cell", veritrail_review.__all__)
        self.assertNotIn("closed_test_binding", veritrail_review.__all__)
        self.assertNotIn("run_closed_test_execution_cell", veritrail_review.__all__)
        self.assertNotIn(
            "run_closed_test_fact_evidence_closure", veritrail_review.__all__
        )
        self.assertFalse(hasattr(veritrail_review, "closed_test_binding"))
        self.assertFalse(hasattr(veritrail_review, "run_closed_test_execution_cell"))
        self.assertFalse(
            hasattr(veritrail_review, "run_closed_test_fact_evidence_closure")
        )

    def test_budget_context_has_no_public_caller_selected_limit_entry(self) -> None:
        self.assertEqual(
            set(inspect.signature(admit_derivation_budget).parameters), {"inputs"}
        )
        with self.assertRaises(BudgetPrimitiveError):
            BudgetContext(
                ExecutionBudgetLimits(
                    wall_clock_ms=1,
                    memory_bytes=1,
                    artifact_bytes=1,
                ),
                _admission_token=object(),
            )

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
                "budget",
                "_artifact_budget",
                "_windows_budget",
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

    def test_execution_cell_has_no_publication_or_real_parser_surface(self) -> None:
        execution_modules = sorted(
            (SOURCE_ROOT / "veritrail_review").glob("*execution_cell*.py")
        )
        self.assertTrue(execution_modules)
        forbidden_imports = {
            "ast",
            "veritrail_review.publisher",
            "veritrail_review._artifact_budget",
        }
        violations: list[str] = []
        for path in execution_modules:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                else:
                    names = []
                for name in names:
                    if name in forbidden_imports:
                        violations.append(f"{path.name}:{node.lineno}:{name}")
        self.assertEqual(violations, [])

        from veritrail_review._execution_cell import run_closed_test_execution_cell

        parameters = inspect.signature(run_closed_test_execution_cell).parameters
        self.assertNotIn("output_directory", parameters)
        self.assertNotIn("publisher", parameters)
        self.assertNotIn("manifest", parameters)

    def test_relation_cell_and_provider_are_private_and_nonpublishing(self) -> None:
        relation_modules = sorted(
            (SOURCE_ROOT / "veritrail_review").glob("_relation_execution_cell*.py")
        )
        self.assertTrue(relation_modules)
        forbidden_imports = {
            "veritrail_review.publisher",
            "veritrail_review._artifact_budget",
        }
        violations: list[str] = []
        for path in relation_modules:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                else:
                    names = []
                for name in names:
                    if name == "ast" or name in forbidden_imports:
                        violations.append(f"{path.name}:{node.lineno}:{name}")
        self.assertEqual(violations, [])

        provider_path = SOURCE_ROOT / "veritrail_review" / "_relation_closed_provider.py"
        provider_tree = ast.parse(
            provider_path.read_text(encoding="utf-8"), filename=str(provider_path)
        )
        provider_imports: list[str] = []
        for node in ast.walk(provider_tree):
            if isinstance(node, ast.Import):
                provider_imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                provider_imports.append(node.module)
        self.assertEqual(provider_imports.count("ast"), 1)
        self.assertTrue(forbidden_imports.isdisjoint(provider_imports))

        import veritrail_review

        self.assertFalse(
            hasattr(veritrail_review, "run_closed_test_relation_derivation")
        )
        self.assertNotIn(
            "run_closed_test_relation_derivation", veritrail_review.__all__
        )

    def test_fact_evidence_closure_is_private_and_has_no_publication_surface(self) -> None:
        from veritrail_review._fact_evidence_closure import (
            run_closed_test_fact_evidence_closure,
        )

        parameters = inspect.signature(
            run_closed_test_fact_evidence_closure
        ).parameters
        self.assertEqual(
            set(parameters),
            {
                "inputs",
                "derivation_id",
                "binding",
                "cancellation_requested",
                "transport_limits",
            },
        )
        for forbidden in (
            "output_directory",
            "output_path",
            "publisher",
            "manifest",
            "provider_discovery",
        ):
            self.assertNotIn(forbidden, parameters)

        closure_modules = sorted(
            (SOURCE_ROOT / "veritrail_review").glob("_fact_evidence*.py")
        )
        forbidden_imports = {
            "ast",
            "veritrail_review.publisher",
            "veritrail_review._artifact_budget",
        }
        violations: list[str] = []
        for path in closure_modules:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                else:
                    names = []
                for name in names:
                    if name in forbidden_imports:
                        violations.append(f"{path.name}:{node.lineno}:{name}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
