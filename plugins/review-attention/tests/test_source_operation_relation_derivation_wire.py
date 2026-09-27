from __future__ import annotations

import base64
import copy
import inspect
import subprocess
import sys
import unittest
from io import BytesIO
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_source_operation_projection as projection_support  # noqa: E402
import test_relation_derivation as relation_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _relation_execution_cell_application as old_relation,
)
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _source_operation_projection as projection,
)
from veritrail_review import (  # noqa: E402
    _source_operation_relation_derivation_application as relation,
)
from veritrail_review._execution_cell_application import (  # noqa: E402
    provider_run_id,
)
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    encode_frame,
    read_frame,
)
from veritrail_review._relation_execution_cell_binding import (  # noqa: E402
    closed_test_relation_binding,
)
from veritrail_review.canonical import semantic_digest  # noqa: E402


class SourceOperationRelationDerivationWireStageDTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        relation_support.RelationDerivationTests.setUpClass()
        support = projection_support.SourceOperationProjectionStageATests()
        self.support = support
        self.inputs = relation_support.RelationDerivationTests.relation_inputs
        self.classification = language_support.classify_language_support(self.inputs)
        self.descriptor = closed_test_relation_binding().descriptor
        eligible_paths = [
            bytes.fromhex(
                subject["semantic_input"]["inventory_item"]["git_path"][
                    "git_path_hex"
                ]
            )
            for subject in self.classification.subjects_copy()
            if subject["disposition"] == "ELIGIBLE"
        ]
        self.assertGreaterEqual(len(eligible_paths), 2)
        self.other_path = eligible_paths[0]
        self.operation_path = eligible_paths[-1]
        self.fact_set = support._fact_set(
            [
                support._module_fact(
                    self.operation_path, classification=self.classification
                )
            ],
            classification=self.classification,
        )
        self.projection = (
            projection.build_relation_derivation_source_operation_projection(
                self.classification, self.descriptor, self.fact_set
            )
        )
        self.provenance = self._provenance(self.inputs)
        self.request = relation.build_relation_source_operation_request_document(
            inputs=self.inputs,
            derivation_id="relation-wire-d",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            fact_set_document=self.fact_set,
            classification=self.classification,
            projection=self.projection,
        )

    def test_d_001_request_filters_to_fact_referenced_operation_set(self) -> None:
        self.assertEqual(relation.PROTOCOL, "veritrail-review-relation-cell/0.3")
        self.assertEqual(
            relation.OPERANDS_DOMAIN, "veritrail.review.provider-operands/0.5"
        )
        paths = [
            bytes.fromhex(item["git_path"]["git_path_hex"])
            for item in self.request["source_blobs"]
        ]
        self.assertEqual(paths, [self.operation_path])
        self.assertNotIn(self.other_path, paths)
        self.assertEqual(
            self.request["fact_set_digest"], self.fact_set["fact_set_digest"]
        )
        self.assertEqual(
            self.request["source_operation_projection"],
            self.projection.projection_document_copy(),
        )

    def test_d_002_worker_revalidates_exact_relation_operation(self) -> None:
        validated = relation.validate_relation_source_operation_request_document(
            self.request, launch_key="relation-a"
        )
        self.assertEqual(validated.descriptor, self.descriptor)
        self.assertEqual(
            set(validated.source_blobs_by_path_hex), {self.operation_path.hex()}
        )
        self.assertEqual(
            set(validated.facts_by_id),
            {self.fact_set["facts"][0]["fact_id"]},
        )
        self.assertEqual(
            validated.provider_run_id,
            provider_run_id(
                "relation-wire-d", self.descriptor, self.request["operands_digest"]
            ),
        )

    def test_d_003_old_and_new_wire_identities_do_not_fallback(self) -> None:
        with self.assertRaises(old_relation.RelationApplicationProtocolError):
            old_relation.validate_relation_request_document(
                self.request, launch_key="relation-a"
            )

        old_request = old_relation.build_relation_request_document(
            inputs=self.inputs,
            derivation_id="old-relation-wire",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            fact_set_document=self.fact_set,
        )
        with self.assertRaises(relation.RelationSourceOperationProtocolError):
            relation.validate_relation_source_operation_request_document(
                old_request, launch_key="relation-a"
            )

    def test_d_004_operands_extend_historical_relation_payload(self) -> None:
        expected = semantic_digest(
            relation.OPERANDS_DOMAIN,
            {
                "source_snapshot_digest": self.inputs.source_snapshot_digest,
                "policy_digest": self.inputs.policy_digest,
                "analysis_scope_digest": self.inputs.analysis_scope_digest,
                "slice_policy_digest": self.inputs.slice_policy_digest,
                "derivation_profile_digest": self.inputs.derivation_profile_digest,
                **self.descriptor.document(),
                "fact_set_digest": self.fact_set["fact_set_digest"],
                "language_support_function": (
                    self.classification.language_support_function
                ),
                "classification_digest": self.classification.classification_digest,
                "source_operation_projection_digest": (
                    self.projection.source_operation_projection_digest
                ),
            },
        )
        old_digest = old_relation.relation_provider_operands_digest(
            self.inputs, self.descriptor, self.fact_set["fact_set_digest"]
        )
        self.assertEqual(self.request["operands_digest"], expected)
        self.assertNotEqual(expected, old_digest)
        self.assertNotEqual(
            provider_run_id("relation-wire-d", self.descriptor, expected),
            provider_run_id("relation-wire-d", self.descriptor, old_digest),
        )

    def test_d_005_self_consistent_required_body_omission_is_rejected(self) -> None:
        changed = copy.deepcopy(self.request)
        projection_document = changed["source_operation_projection"]
        projection_document["operation_subject_ids"] = []
        projection_document["source_operation_projection_digest"] = semantic_digest(
            "veritrail.review.private-source-operation-projection/0.1",
            {
                key: value
                for key, value in projection_document.items()
                if key != "source_operation_projection_digest"
            },
        )
        changed["source_blobs"] = []
        changed["operands_digest"] = self._recomputed_operands(changed)
        with self.assertRaises(relation.RelationSourceOperationProtocolError):
            relation.validate_relation_source_operation_request_document(
                changed, launch_key="relation-a"
            )

    def test_d_006_body_set_order_and_bytes_are_exact(self) -> None:
        mutations = (
            lambda item: item["source_blobs"].clear(),
            lambda item: item["source_blobs"].append(
                self._blob_for_path(self.inputs, self.other_path)
            ),
            lambda item: item["source_blobs"][0].__setitem__(
                "content_base64", base64.b64encode(b"changed\n").decode("ascii")
            ),
            lambda item: item["source_blobs"].append(
                copy.deepcopy(item["source_blobs"][0])
            ),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(self.request)
                mutate(changed)
                with self.assertRaises(
                    relation.RelationSourceOperationProtocolError
                ):
                    relation.validate_relation_source_operation_request_document(
                        changed, launch_key="relation-a"
                    )

    def test_d_007_factset_and_gate_identity_tamper_fail_closed(self) -> None:
        mutations = (
            lambda item: item.__setitem__("fact_set_digest", "0" * 64),
            lambda item: item["fact_set"]["facts"][0].__setitem__(
                "local_ordinal", 1
            ),
            lambda item: item["language_support_classification"].__setitem__(
                "classification_digest", "0" * 64
            ),
            lambda item: item["source_operation_projection"].__setitem__(
                "source_operation_projection_digest", "0" * 64
            ),
            lambda item: item["provider_descriptor"].__setitem__(
                "provider_version", "changed"
            ),
            lambda item: item.__setitem__("operands_digest", "0" * 64),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(self.request)
                mutate(changed)
                with self.assertRaises(
                    relation.RelationSourceOperationProtocolError
                ):
                    relation.validate_relation_source_operation_request_document(
                        changed, launch_key="relation-a"
                    )

    def test_d_008_terminal_echoes_only_the_new_identity(self) -> None:
        validated = relation.validate_relation_source_operation_request_document(
            self.request, launch_key="relation-a"
        )
        terminal = relation.relation_source_operation_terminal_document(
            validated, terminal_kind="COMPLETED", canonical_relations=[]
        )
        self.assertEqual(terminal["protocol"], relation.PROTOCOL)
        self.assertEqual(terminal["provider_run_id"], validated.provider_run_id)
        self.assertEqual(
            relation.validate_relation_source_operation_terminal_document(
                terminal, request=self.request
            ),
            terminal,
        )
        with self.assertRaises(old_relation.RelationApplicationProtocolError):
            old_relation.validate_relation_terminal_document(
                terminal, request=self.request
            )

    def test_d_009_old_terminal_is_rejected_by_corrected_validator(self) -> None:
        old_request = old_relation.build_relation_request_document(
            inputs=self.inputs,
            derivation_id="old-relation-terminal",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            fact_set_document=self.fact_set,
        )
        old_validated = old_relation.validate_relation_request_document(
            old_request, launch_key="relation-a"
        )
        old_terminal = old_relation.relation_terminal_document(
            old_validated, terminal_kind="COMPLETED", canonical_relations=[]
        )
        with self.assertRaises(relation.RelationSourceOperationProtocolError):
            relation.validate_relation_source_operation_terminal_document(
                old_terminal, request=old_request
            )

    def test_d_010_non_success_terminal_cannot_retain_relations(self) -> None:
        validated = relation.validate_relation_source_operation_request_document(
            self.request, launch_key="relation-a"
        )
        with self.assertRaises(relation.RelationSourceOperationProtocolError):
            relation.relation_source_operation_terminal_document(
                validated,
                terminal_kind="PROVIDER_FAILED",
                canonical_relations=[{"relation_id": "0" * 64}],
            )
        terminal = relation.relation_source_operation_terminal_document(
            validated, terminal_kind="PROVIDER_FAILED"
        )
        terminal["reported_relation_ids"] = ["0" * 64]
        with self.assertRaises(relation.RelationSourceOperationProtocolError):
            relation.validate_relation_source_operation_terminal_document(
                terminal, request=self.request
            )

    def test_d_011_empty_factset_runs_an_exact_empty_body_shape(self) -> None:
        fact_set = self.support._fact_set(
            [], classification=self.classification
        )
        projection_value = (
            projection.build_relation_derivation_source_operation_projection(
                self.classification, self.descriptor, fact_set
            )
        )
        request = relation.build_relation_source_operation_request_document(
            inputs=self.inputs,
            derivation_id="relation-empty-wire-d",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            fact_set_document=fact_set,
            classification=self.classification,
            projection=projection_value,
        )
        validated = relation.validate_relation_source_operation_request_document(
            request, launch_key="relation-a"
        )
        self.assertGreater(self.classification.eligible_count, 0)
        self.assertEqual(request["source_blobs"], [])
        self.assertEqual(validated.source_blobs_by_path_hex, {})
        self.assertEqual(validated.facts_by_id, {})

    def test_d_012_provider_copy_cannot_mutate_application_state(self) -> None:
        validated = relation.validate_relation_source_operation_request_document(
            self.request, launch_key="relation-a"
        )
        provider_copy = relation.copy_relation_source_operation_request_for_provider(
            validated
        )
        provider_copy.document["fact_set"]["facts"].clear()
        provider_copy.facts_by_id.clear()
        provider_copy.source_blobs_by_path_hex.clear()
        self.assertEqual(len(validated.document["fact_set"]["facts"]), 1)
        self.assertEqual(len(validated.facts_by_id), 1)
        self.assertEqual(
            set(validated.source_blobs_by_path_hex), {self.operation_path.hex()}
        )
        self.assertNotIn(self.other_path.hex(), validated.source_blobs_by_path_hex)

    def test_d_013_private_worker_roundtrips_only_corrected_wire(self) -> None:
        completed = self._run_worker(self.request, launch_key="relation-a")
        self.assertEqual(completed.returncode, 0, completed.stderr.decode())
        terminal = read_frame(BytesIO(completed.stdout), payload_limit=1_048_576)
        self.assertEqual(terminal["protocol"], relation.PROTOCOL)
        self.assertEqual(terminal["canonical_relations"], [])
        self.assertEqual(
            relation.validate_relation_source_operation_terminal_document(
                terminal, request=self.request
            ),
            terminal,
        )

        positive_request = self._positive_relation_request()
        positive = self._run_worker(positive_request, launch_key="relation-a")
        self.assertEqual(positive.returncode, 0, positive.stderr.decode())
        positive_terminal = read_frame(
            BytesIO(positive.stdout), payload_limit=1_048_576
        )
        self.assertEqual(len(positive_terminal["canonical_relations"]), 1)
        self.assertEqual(
            relation.validate_relation_source_operation_terminal_document(
                positive_terminal, request=positive_request
            ),
            positive_terminal,
        )

        old_request = old_relation.build_relation_request_document(
            inputs=self.inputs,
            derivation_id="old-relation-worker",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            fact_set_document=self.fact_set,
        )
        rejected = self._run_worker(old_request, launch_key="relation-a")
        self.assertEqual(rejected.returncode, 65)
        self.assertEqual(rejected.stdout, b"")

    def test_d_014_wire_and_worker_mint_no_controller_authority(self) -> None:
        import veritrail_review
        from veritrail_review import (
            _source_operation_relation_derivation_worker as worker,
        )

        self.assertFalse(
            hasattr(
                veritrail_review,
                "ValidatedRelationSourceOperationRequest",
            )
        )
        self.assertFalse(
            hasattr(
                veritrail_review,
                "build_relation_source_operation_request_document",
            )
        )
        parameters = inspect.signature(
            relation.build_relation_source_operation_request_document
        ).parameters
        for forbidden in (
            "context",
            "budget_context",
            "parent_eligibility",
            "child_eligibility",
            "claim",
            "continuation",
        ):
            self.assertNotIn(forbidden, parameters)
        source = inspect.getsource(worker)
        self.assertNotIn("BudgetContext", source)
        self.assertNotIn("AttemptEligibility", source)
        self.assertEqual(worker.main([]), 64)

    def _recomputed_operands(self, request: dict[str, object]) -> str:
        return semantic_digest(
            relation.OPERANDS_DOMAIN,
            {
                "source_snapshot_digest": request["source_snapshot_digest"],
                "policy_digest": request["policy_digest"],
                "analysis_scope_digest": request["analysis_scope_digest"],
                "slice_policy_digest": request["slice_policy_digest"],
                "derivation_profile_digest": request[
                    "derivation_profile_digest"
                ],
                **self.descriptor.document(),
                "fact_set_digest": request["fact_set_digest"],
                "language_support_function": (
                    self.classification.language_support_function
                ),
                "classification_digest": self.classification.classification_digest,
                "source_operation_projection_digest": request[
                    "source_operation_projection"
                ]["source_operation_projection_digest"],
            },
        )

    @staticmethod
    def _provenance(inputs) -> dict[str, object]:
        snapshot = inputs.source_snapshot_document_copy()
        coordinate = snapshot["source_coordinate"]
        commit_oid = coordinate["commit_oid"]
        return {
            "requested_repository_id": snapshot["repository_id"],
            "requested_ref": (
                f"oid:{commit_oid['algorithm'].lower()}:{commit_oid['hex']}"
            ),
            "resolver_id": "veritrail-r1-owned-snapshot-exact-oid",
            "resolver_version": "0.1",
            "resolved_at": "2026-09-27T00:00:00Z",
        }

    @staticmethod
    def _blob_for_path(inputs, path: bytes) -> dict[str, object]:
        for item in inputs.source_snapshot_document_copy()["inventory"]:
            if bytes.fromhex(item["git_path"]["git_path_hex"]) != path:
                continue
            raw = inputs.verified_blob_bytes_by_object_identity[
                item["git_object"]["hex"]
            ]
            return {
                "git_path": copy.deepcopy(item["git_path"]),
                "size_bytes": len(raw),
                "content_sha256": item["content"]["sha256"],
                "content_base64": base64.b64encode(raw).decode("ascii"),
            }
        raise KeyError(path)

    def _positive_relation_request(self) -> dict[str, object]:
        inputs = relation_support.RelationDerivationTests.import_inputs
        classification = language_support.classify_language_support(inputs)
        raw = b"import pkg.mod\n"
        operation_path = next(
            bytes.fromhex(
                subject["semantic_input"]["inventory_item"]["git_path"][
                    "git_path_hex"
                ]
            )
            for subject in classification.subjects_copy()
            if subject["disposition"] == "ELIGIBLE"
            and base64.b64decode(
                self._blob_for_path(
                    inputs,
                    bytes.fromhex(
                        subject["semantic_input"]["inventory_item"]["git_path"][
                            "git_path_hex"
                        ]
                    ),
                )["content_base64"]
            )
            == raw
        )
        anchor = {
            "git_path": {
                "path_kind": "GIT_PATH",
                "git_path_hex": operation_path.hex(),
            },
            "start_byte": 0,
            "end_byte": len(raw.rstrip(b"\n")),
        }
        subject_key_digest = semantic_digest(
            "veritrail.review.fact-subject/0.1",
            {
                "source_snapshot_digest": classification.source_snapshot_digest,
                "derivation_profile_digest": (
                    classification.derivation_profile_digest
                ),
                "source_anchor": anchor,
                "subject_space": "IMPORT_ALIAS",
                "local_ordinal": 0,
            },
        )
        attributes = {
            "import_form": "IMPORT",
            "relative_level": 0,
            "module_parts": ["pkg", "mod"],
            "imported_name": None,
            "alias_name": None,
        }
        import_fact = {
            "fact_id": semantic_digest(
                "veritrail.review.code-fact/0.1",
                {
                    "subject_key_digest": subject_key_digest,
                    "fact_kind": "IMPORT_DECLARATION",
                    "semantic_attributes": attributes,
                },
            ),
            "subject_key_digest": subject_key_digest,
            "subject_space": "IMPORT_ALIAS",
            "fact_kind": "IMPORT_DECLARATION",
            "source_snapshot_digest": classification.source_snapshot_digest,
            "derivation_profile_digest": classification.derivation_profile_digest,
            "source_anchor": anchor,
            "local_ordinal": 0,
            "semantic_attributes": attributes,
            "provenance_refs": ["fixture-provider-run"],
        }
        fact_set = self.support._fact_set(
            [
                self.support._module_fact(
                    operation_path, classification=classification
                ),
                import_fact,
            ],
            classification=classification,
        )
        projection_value = (
            projection.build_relation_derivation_source_operation_projection(
                classification, self.descriptor, fact_set
            )
        )
        return relation.build_relation_source_operation_request_document(
            inputs=inputs,
            derivation_id="relation-wire-d-positive",
            request_provenance=self._provenance(inputs),
            descriptor=self.descriptor,
            fact_set_document=fact_set,
            classification=classification,
            projection=projection_value,
        )

    @staticmethod
    def _run_worker(
        request: dict[str, object], *, launch_key: str
    ) -> subprocess.CompletedProcess[bytes]:
        worker_path = (
            SOURCE_ROOT
            / "veritrail_review"
            / "_source_operation_relation_derivation_worker.py"
        )
        return subprocess.run(
            [
                sys.executable,
                "-I",
                str(worker_path),
                launch_key,
                "1048576",
                "1048576",
            ],
            input=encode_frame(request, payload_limit=1_048_576),
            capture_output=True,
            check=False,
            timeout=10,
        )


if __name__ == "__main__":
    unittest.main()
