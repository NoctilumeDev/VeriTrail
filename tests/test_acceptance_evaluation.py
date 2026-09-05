from __future__ import annotations

import copy
import unittest

from veritrail.acceptance_evaluation import (
    evaluate_acceptance,
    validate_observation_metadata,
)
from veritrail.acceptance_plan import seal_acceptance_plan
from veritrail.canonical import sha256_bytes
from veritrail.errors import ValidationError
from veritrail.evidence import import_evidence_document

from tests.support import acceptance_artifact, acceptance_plan


class AcceptanceEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = seal_acceptance_plan(acceptance_plan())

    def artifacts(
        self,
        *,
        api_commit: str = "candidate-001",
        render_commit: str = "candidate-001",
        api_session: str = "collection-001",
        render_session: str = "collection-001",
        api_coverage: str = "COMPLETE",
        render_coverage: str = "COMPLETE",
    ):
        return [
            acceptance_artifact(
                self.plan,
                "api-spec",
                facts={"commit_sha": api_commit},
                session_id=api_session,
                coverage=api_coverage,
            ),
            acceptance_artifact(
                self.plan,
                "render-spec",
                facts={"commit_sha": render_commit},
                session_id=render_session,
                coverage=render_coverage,
            ),
        ]

    def test_cross_evidence_pass_retains_operands_and_artifact_hashes(self) -> None:
        evidence = self.artifacts()
        result = evaluate_acceptance(self.plan, evidence, "COMPLETED")
        self.assertEqual("PASS", result["verdict"])
        relation = next(
            item for item in result["rule_results"] if item["id"] == "same-visible-commit"
        )
        self.assertEqual("PASS", relation["status"])
        self.assertEqual("candidate-001", relation["left"]["value"])
        self.assertEqual("candidate-001", relation["right"]["value"])
        self.assertEqual(evidence[0].sha256, relation["left"]["evidence_sha256"])
        self.assertEqual(evidence[1].sha256, relation["right"]["evidence_sha256"])

    def test_decisive_false_beats_unrelated_missing_evidence(self) -> None:
        evidence = [
            acceptance_artifact(
                self.plan,
                "api-spec",
                facts={"commit_sha": "wrong-commit"},
            )
        ]
        result = evaluate_acceptance(self.plan, evidence, "COMPLETED")
        self.assertEqual("FAIL", result["verdict"])
        self.assertEqual(["render-evidence"], result["missing_evidence"])

    def test_integrity_false_blocks_decisive_false(self) -> None:
        evidence = self.artifacts(
            api_commit="wrong-commit",
            api_session="collection-001",
            render_session="collection-002",
        )
        result = evaluate_acceptance(self.plan, evidence, "COMPLETED")
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        integrity = next(item for item in result["rule_results"] if item["id"] == "same-session")
        self.assertEqual("FAIL", integrity["status"])

    def test_wrong_cross_evidence_target_is_fail(self) -> None:
        result = evaluate_acceptance(
            self.plan,
            self.artifacts(render_commit="other-visible-commit"),
            "COMPLETED",
        )
        self.assertEqual("FAIL", result["verdict"])

    def test_missing_requirement_is_pending(self) -> None:
        result = evaluate_acceptance(self.plan, [], "COMPLETED")
        self.assertEqual("PENDING", result["verdict"])
        self.assertEqual(["api-evidence", "render-evidence"], result["missing_evidence"])

    def test_same_type_with_wrong_binding_is_inconclusive(self) -> None:
        evidence = self.artifacts()
        wrong = acceptance_artifact(
            self.plan,
            "api-spec",
            facts={"commit_sha": "candidate-001"},
            plan_digest=sha256_bytes(b"other-plan"),
        )
        result = evaluate_acceptance(self.plan, [wrong, evidence[1]], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        binding = next(
            item for item in result["evidence_bindings"] if item["requirement_id"] == "api-evidence"
        )
        self.assertEqual("BINDING_MISMATCH", binding["status"])

    def test_same_type_with_wrong_spec_digest_is_inconclusive(self) -> None:
        evidence = self.artifacts()
        wrong = acceptance_artifact(
            self.plan,
            "api-spec",
            facts={"commit_sha": "candidate-001"},
            spec_digest=sha256_bytes(b"other-spec"),
        )
        result = evaluate_acceptance(self.plan, [wrong, evidence[1]], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        binding = next(
            item for item in result["evidence_bindings"] if item["requirement_id"] == "api-evidence"
        )
        self.assertEqual("BINDING_MISMATCH", binding["status"])

    def test_two_exact_artifacts_conflict(self) -> None:
        evidence = self.artifacts()
        second_api = acceptance_artifact(
            self.plan,
            "api-spec",
            facts={"commit_sha": "candidate-001", "probe": 2},
            input_name="api-second.json",
        )
        result = evaluate_acceptance(self.plan, [evidence[0], second_api, evidence[1]], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        binding = next(
            item for item in result["evidence_bindings"] if item["requirement_id"] == "api-evidence"
        )
        self.assertEqual("CARDINALITY_CONFLICT", binding["status"])

    def test_one_artifact_cannot_satisfy_two_requirements(self) -> None:
        draft = acceptance_plan()
        draft["evidence_requirements"][1]["observation_spec_id"] = "api-spec"
        draft["sufficiency_rules"][1]["left"]["requirement_id"] = "api-evidence"
        draft["integrity_rules"] = []
        draft["assertions"][1]["right"] = "candidate-001"
        plan = seal_acceptance_plan(draft)
        artifact = acceptance_artifact(
            plan, "api-spec", facts={"commit_sha": "candidate-001"}
        )
        result = evaluate_acceptance(plan, [artifact], "COMPLETED")
        self.assertEqual("INCONCLUSIVE", result["verdict"])
        self.assertEqual(
            ["REUSE_CONFLICT", "REUSE_CONFLICT"],
            [item["status"] for item in result["evidence_bindings"]],
        )

    def test_missing_paths_and_exists_have_distinct_semantics(self) -> None:
        draft = acceptance_plan()
        draft["assertions"] = [
            {
                "id": "ordinary-missing",
                "severity": "HARD",
                "left": {"requirement_id": "api-evidence", "path": "/facts/absent"},
                "operator": "eq",
                "right": True,
            }
        ]
        plan = seal_acceptance_plan(draft)
        evidence = [
            acceptance_artifact(plan, "api-spec", facts={"commit_sha": "candidate-001"}),
            acceptance_artifact(plan, "render-spec", facts={"commit_sha": "candidate-001"}),
        ]
        result = evaluate_acceptance(plan, evidence, "COMPLETED")
        self.assertEqual("PENDING", result["verdict"])
        self.assertEqual("NOT_EVALUATED", result["rule_results"][-1]["status"])

        draft["assertions"][0]["operator"] = "exists"
        del draft["assertions"][0]["right"]
        plan = seal_acceptance_plan(draft)
        evidence = [
            acceptance_artifact(plan, "api-spec", facts={"commit_sha": "candidate-001"}),
            acceptance_artifact(plan, "render-spec", facts={"commit_sha": "candidate-001"}),
        ]
        result = evaluate_acceptance(plan, evidence, "COMPLETED")
        self.assertEqual("FAIL", result["verdict"])
        self.assertEqual("FAIL", result["rule_results"][-1]["status"])

    def test_error_coverage_without_target_fact_is_pending(self) -> None:
        evidence = self.artifacts(api_coverage="ERROR")
        api_document = copy.deepcopy(evidence[0].document)
        api_document["facts"] = {}
        evidence[0] = import_evidence_document(api_document, "api-error.json")
        result = evaluate_acceptance(self.plan, evidence, "COMPLETED")
        self.assertEqual("PENDING", result["verdict"])

    def test_partial_coverage_with_valid_target_fact_remains_pending(self) -> None:
        result = evaluate_acceptance(
            self.plan,
            self.artifacts(api_coverage="PARTIAL"),
            "COMPLETED",
        )
        self.assertEqual("PENDING", result["verdict"])

    def test_non_completed_execution_remains_pending_after_rules_pass(self) -> None:
        result = evaluate_acceptance(self.plan, self.artifacts(), "ABORTED")
        self.assertEqual("PENDING", result["verdict"])

    def test_operator_type_error_and_duplicate_set_are_inconclusive(self) -> None:
        for operator, left_value, right_value in (
            ("lt", "1", 2),
            ("set_equals", ["a", "a"], ["a"]),
        ):
            with self.subTest(operator=operator):
                draft = acceptance_plan()
                draft["assertions"] = [
                    {
                        "id": "operator-contract",
                        "severity": "HARD",
                        "left": {"requirement_id": "api-evidence", "path": "/facts/value"},
                        "operator": operator,
                        "right": right_value,
                    }
                ]
                plan = seal_acceptance_plan(draft)
                evidence = [
                    acceptance_artifact(plan, "api-spec", facts={"value": left_value}),
                    acceptance_artifact(plan, "render-spec", facts={"commit_sha": "candidate-001"}),
                ]
                result = evaluate_acceptance(plan, evidence, "COMPLETED")
                self.assertEqual("INCONCLUSIVE", result["verdict"])
                self.assertEqual("ERROR", result["rule_results"][-1]["status"])

    def test_plugin_verdict_like_fields_are_not_implicitly_trusted(self) -> None:
        evidence = self.artifacts(api_commit="wrong-commit")
        mutated = copy.deepcopy(evidence[0].document)
        mutated["facts"].update(
            {"all_required_checks_passed": True, "api_render_match": True}
        )
        evidence[0] = import_evidence_document(mutated, "api-private-verdict.json")
        result = evaluate_acceptance(self.plan, evidence, "COMPLETED")
        self.assertEqual("FAIL", result["verdict"])

    def test_observation_metadata_is_strict(self) -> None:
        artifact = self.artifacts()[0]
        validate_observation_metadata(artifact.document, artifact.input_name)
        malformed = copy.deepcopy(artifact.document)
        malformed["metadata"]["veritrail_observation"]["surprise"] = True
        with self.assertRaisesRegex(ValidationError, "unsupported fields: surprise"):
            validate_observation_metadata(malformed, "malformed.json")

        malformed_artifact = import_evidence_document(malformed, "malformed.json")
        result = evaluate_acceptance(
            self.plan, [malformed_artifact, self.artifacts()[1]], "COMPLETED"
        )
        self.assertEqual("INCONCLUSIVE", result["verdict"])

    def test_bounded_operator_set_has_deterministic_positive_cases(self) -> None:
        cases = (
            ("eq", {"id": 1}, {"id": 1}),
            ("ne", 1, 2),
            ("lt", 1, 2),
            ("lte", 2, 2),
            ("gt", 3, 2),
            ("contains", "alpha-beta", "beta"),
            ("contains", [{"id": 1}, {"id": 2}], {"id": 2}),
            ("set_equals", ["a", "b"], ["b", "a"]),
            ("contains_all", ["a", "b", "c"], ["c", "a"]),
            ("gte", 2, 2),
        )
        for operator, left_value, right_value in cases:
            with self.subTest(operator=operator, left=left_value):
                draft = acceptance_plan()
                draft["assertions"] = [
                    {
                        "id": "operator-positive",
                        "severity": "HARD",
                        "left": {"requirement_id": "api-evidence", "path": "/facts/value"},
                        "operator": operator,
                        "right": right_value,
                    }
                ]
                plan = seal_acceptance_plan(draft)
                evidence = [
                    acceptance_artifact(plan, "api-spec", facts={"value": left_value}),
                    acceptance_artifact(plan, "render-spec", facts={"commit_sha": "candidate-001"}),
                ]
                result = evaluate_acceptance(plan, evidence, "COMPLETED")
                self.assertEqual("PASS", result["verdict"])

    def test_exists_treats_a_present_null_as_present(self) -> None:
        draft = acceptance_plan()
        draft["assertions"] = [
            {
                "id": "null-is-present",
                "severity": "HARD",
                "left": {"requirement_id": "api-evidence", "path": "/facts/value"},
                "operator": "exists",
            }
        ]
        plan = seal_acceptance_plan(draft)
        evidence = [
            acceptance_artifact(plan, "api-spec", facts={"value": None}),
            acceptance_artifact(plan, "render-spec", facts={"commit_sha": "candidate-001"}),
        ]
        result = evaluate_acceptance(plan, evidence, "COMPLETED")
        self.assertEqual("PASS", result["verdict"])

    def test_objective_false_does_not_override_decisive_pass(self) -> None:
        draft = acceptance_plan()
        draft["assertions"].append(
            {
                "id": "quality-objective",
                "severity": "OBJECTIVE",
                "left": {"requirement_id": "api-evidence", "path": "/facts/commit_sha"},
                "operator": "eq",
                "right": "preferred-but-not-required",
            }
        )
        plan = seal_acceptance_plan(draft)
        evidence = [
            acceptance_artifact(plan, "api-spec", facts={"commit_sha": "candidate-001"}),
            acceptance_artifact(plan, "render-spec", facts={"commit_sha": "candidate-001"}),
        ]
        result = evaluate_acceptance(plan, evidence, "COMPLETED")
        self.assertEqual("PASS", result["verdict"])
        self.assertEqual("FAIL", result["rule_results"][-1]["status"])


if __name__ == "__main__":
    unittest.main()
