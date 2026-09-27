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

import test_relation_observation_qualification as observation_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _relation_observation_application as old_observation,
)
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import (  # noqa: E402
    _source_operation_relation_observation_application as observation,
)
from veritrail_review._execution_cell_application import (  # noqa: E402
    provider_run_id,
)
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    encode_frame,
    read_frame,
)
from veritrail_review._relation_observation_binding import (  # noqa: E402
    closed_test_relation_observation_bindings,
)
from veritrail_review._source_operation_projection import (  # noqa: E402
    build_relation_observation_source_operation_projection,
)
from veritrail_review.canonical import semantic_digest  # noqa: E402


build_corrected_request = (
    observation.build_relation_observation_source_operation_request_document
)
validate_corrected_request = (
    observation.validate_relation_observation_source_operation_request_document
)
validate_corrected_terminal = (
    observation.validate_relation_observation_source_operation_terminal_document
)


class SourceOperationRelationObservationWireStageETests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        support = observation_support.RelationObservationQualificationTests
        support.setUpClass()
        cls.support = support
        cls.inputs = support.inputs
        cls.fact_set = support.fact_set
        cls.domain = support.positive.observation_domain_copy()
        cls.classification = language_support.classify_language_support(cls.inputs)
        cls.binding = closed_test_relation_observation_bindings()[1]
        cls.descriptor = cls.binding.descriptor
        cls.projection = build_relation_observation_source_operation_projection(
            cls.classification,
            cls.descriptor,
            cls.fact_set,
            cls.domain,
        )
        cls.provenance = cls._provenance(cls.inputs)
        cls.request = (
            build_corrected_request(
                inputs=cls.inputs,
                derivation_id="observation-wire-e",
                request_provenance=cls.provenance,
                descriptor=cls.descriptor,
                fact_set_document=cls.fact_set,
                observation_domain=cls.domain,
                classification=cls.classification,
                projection=cls.projection,
            )
        )

    def test_e_001_request_uses_exact_assigned_operation_source_set(self) -> None:
        self.assertEqual(observation.PROTOCOL, "veritrail-review-relation-cell/0.4")
        self.assertEqual(
            observation.OPERANDS_DOMAIN, "veritrail.review.provider-operands/0.6"
        )
        paths = {
            item["git_path"]["git_path_hex"] for item in self.request["source_blobs"]
        }
        self.assertEqual(len(paths), 1)
        self.assertEqual(len(self.projection.operation_subject_ids), 1)
        eligible = {
            item["semantic_input"]["inventory_item"]["git_path"]["git_path_hex"]
            for item in self.classification.subjects_copy()
            if item["disposition"] == "ELIGIBLE"
        }
        self.assertTrue(paths < eligible)

    def test_e_002_worker_revalidates_exact_observation_operation(self) -> None:
        validated = (
            validate_corrected_request(
                self.request, launch_key=self.binding.launch_key
            )
        )
        self.assertEqual(
            set(validated.source_blobs_by_path_hex),
            {
                item["git_path"]["git_path_hex"]
                for item in self.request["source_blobs"]
            },
        )
        self.assertEqual(
            validated.provider_run_id,
            provider_run_id(
                self.request["derivation_id"],
                self.descriptor,
                self.request["operands_digest"],
            ),
        )

    def test_e_003_old_and_new_wire_identities_do_not_fallback(self) -> None:
        old_request = old_observation.build_relation_observation_request_document(
            inputs=self.inputs,
            derivation_id="old-observation-wire",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            fact_set_document=self.fact_set,
            observation_domain=self.domain,
        )
        with self.assertRaises(
            observation.RelationObservationSourceOperationProtocolError
        ):
            validate_corrected_request(
                old_request, launch_key=self.binding.launch_key
            )
        with self.assertRaises(old_observation.RelationObservationApplicationError):
            old_observation.validate_relation_observation_request_document(
                self.request, launch_key=self.binding.launch_key
            )

    def test_e_004_operands_extend_historical_observation_payload(self) -> None:
        expected = semantic_digest(
            observation.OPERANDS_DOMAIN,
            {
                "source_snapshot_digest": self.request["source_snapshot_digest"],
                "policy_digest": self.request["policy_digest"],
                "analysis_scope_digest": self.request["analysis_scope_digest"],
                "slice_policy_digest": self.request["slice_policy_digest"],
                "derivation_profile_digest": self.request[
                    "derivation_profile_digest"
                ],
                **self.descriptor.document(),
                "fact_set_digest": self.request["fact_set_digest"],
                "observation_domain_digest": self.request[
                    "observation_domain_digest"
                ],
                "assigned_observation_item_ids": self.request[
                    "assigned_observation_item_ids"
                ],
                "language_support_function": (
                    self.classification.language_support_function
                ),
                "classification_digest": self.classification.classification_digest,
                "source_operation_projection_digest": (
                    self.projection.source_operation_projection_digest
                ),
            },
        )
        old_digest = old_observation.relation_observation_provider_operands_digest(
            self.inputs,
            self.descriptor,
            self.request["fact_set_digest"],
            self.request["observation_domain_digest"],
            self.request["assigned_observation_item_ids"],
        )
        self.assertEqual(self.request["operands_digest"], expected)
        self.assertNotEqual(expected, old_digest)

    def test_e_005_self_consistent_required_body_omission_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.request)
        projection = mutated["source_operation_projection"]
        projection["operation_subject_ids"] = []
        projection["source_operation_projection_digest"] = semantic_digest(
            "veritrail.review.private-source-operation-projection/0.1",
            {
                key: copy.deepcopy(value)
                for key, value in projection.items()
                if key != "source_operation_projection_digest"
            },
        )
        mutated["source_blobs"] = []
        mutated["operands_digest"] = self._recomputed_operands(mutated)
        with self.assertRaises(
            observation.RelationObservationSourceOperationProtocolError
        ):
            validate_corrected_request(
                mutated, launch_key=self.binding.launch_key
            )

    def test_e_006_body_order_size_hash_and_bytes_are_exact(self) -> None:
        paths = [
            bytes.fromhex(item["git_path"]["git_path_hex"])
            for item in self.request["source_blobs"]
        ]
        self.assertEqual(paths, sorted(paths))
        for item in self.request["source_blobs"]:
            raw = base64.b64decode(item["content_base64"])
            expected = self._blob_for_path(
                self.inputs, bytes.fromhex(item["git_path"]["git_path_hex"])
            )
            self.assertEqual(item, expected)
            self.assertEqual(item["size_bytes"], len(raw))

    def test_e_007_exact_coordinate_and_gate_tamper_fail_closed(self) -> None:
        mutators = (
            lambda item: item.__setitem__("fact_set_digest", "0" * 64),
            lambda item: item.__setitem__("observation_domain_digest", "1" * 64),
            lambda item: item["assigned_observation_item_ids"].clear(),
            lambda item: item["language_support_classification"].__setitem__(
                "classification_digest", "2" * 64
            ),
            lambda item: item["source_operation_projection"].__setitem__(
                "source_operation_projection_digest", "3" * 64
            ),
            lambda item: item["provider_descriptor"].__setitem__(
                "provider_id", "foreign-provider"
            ),
            lambda item: item.__setitem__("operands_digest", "4" * 64),
        )
        for mutate in mutators:
            with self.subTest(mutate=mutate):
                damaged = copy.deepcopy(self.request)
                mutate(damaged)
                with self.assertRaises(
                    observation.RelationObservationSourceOperationProtocolError
                ):
                    validate_corrected_request(
                        damaged, launch_key=self.binding.launch_key
                    )

    def test_e_008_terminal_echoes_only_the_new_identity(self) -> None:
        validated = (
            validate_corrected_request(
                self.request, launch_key=self.binding.launch_key
            )
        )
        terminal = observation.relation_observation_source_operation_terminal_document(
            validated, terminal_kind="COMPLETED"
        )
        self.assertEqual(terminal["protocol"], observation.PROTOCOL)
        self.assertEqual(terminal["operands_digest"], self.request["operands_digest"])
        self.assertEqual(terminal["assigned_observation_item_ids"], self.request[
            "assigned_observation_item_ids"
        ])
        self.assertEqual(
            validate_corrected_terminal(
                terminal, request=self.request
            ),
            terminal,
        )

    def test_e_009_old_terminal_is_rejected_by_corrected_validator(self) -> None:
        validated = (
            validate_corrected_request(
                self.request, launch_key=self.binding.launch_key
            )
        )
        terminal = observation.relation_observation_source_operation_terminal_document(
            validated, terminal_kind="COMPLETED"
        )
        terminal["protocol"] = old_observation.PROTOCOL
        with self.assertRaises(
            observation.RelationObservationSourceOperationProtocolError
        ):
            validate_corrected_terminal(
                terminal, request=self.request
            )

    def test_e_010_non_success_terminal_cannot_retain_output(self) -> None:
        validated = (
            validate_corrected_request(
                self.request, launch_key=self.binding.launch_key
            )
        )
        terminal = observation.relation_observation_source_operation_terminal_document(
            validated, terminal_kind="PROVIDER_FAILED"
        )
        self.assertEqual(terminal["canonical_relations"], [])
        self.assertEqual(terminal["observation_outcomes"], [])
        damaged = copy.deepcopy(terminal)
        damaged["observation_outcomes"] = [{"unexpected": True}]
        with self.assertRaises(
            observation.RelationObservationSourceOperationProtocolError
        ):
            validate_corrected_terminal(
                damaged, request=self.request
            )

    def test_e_011_empty_a_and_b_run_exact_empty_body_requests(self) -> None:
        inputs = self.support.empty_inputs
        fact_set = self.support._fact_set_for_result(self.support.empty, inputs)
        domain = self.support.empty.observation_domain_copy()
        classification = language_support.classify_language_support(inputs)
        for binding in closed_test_relation_observation_bindings():
            with self.subTest(binding=binding.launch_key):
                projection = (
                    build_relation_observation_source_operation_projection(
                        classification,
                        binding.descriptor,
                        fact_set,
                        domain,
                    )
                )
                request = (
                    build_corrected_request(
                        inputs=inputs,
                        derivation_id=f"empty-{binding.launch_key}",
                        request_provenance=self._provenance(inputs),
                        descriptor=binding.descriptor,
                        fact_set_document=fact_set,
                        observation_domain=domain,
                        classification=classification,
                        projection=projection,
                    )
                )
                self.assertEqual(request["source_blobs"], [])
                completed = self._run_worker(request, launch_key=binding.launch_key)
                self.assertEqual(completed.returncode, 0, completed.stderr.decode())
                terminal = read_frame(
                    BytesIO(completed.stdout), payload_limit=1_048_576
                )
                self.assertEqual(terminal["terminal_kind"], "COMPLETED")
                self.assertEqual(terminal["canonical_relations"], [])
                self.assertEqual(terminal["observation_outcomes"], [])

    def test_e_012_provider_copy_has_no_omitted_body_or_fact_view(self) -> None:
        validated = (
            validate_corrected_request(
                self.request, launch_key=self.binding.launch_key
            )
        )
        provider_copy = (
            observation.copy_relation_observation_source_operation_request_for_provider(
                validated
            )
        )
        operation_paths = set(validated.source_blobs_by_path_hex)
        self.assertEqual(set(provider_copy.source_blobs_by_path_hex), operation_paths)
        self.assertEqual(
            {
                fact["source_anchor"]["git_path"]["git_path_hex"]
                for fact in provider_copy.facts_by_id.values()
            },
            operation_paths,
        )
        provider_copy.document["fact_set"]["facts"].clear()
        provider_copy.facts_by_id.clear()
        provider_copy.source_blobs_by_path_hex.clear()
        self.assertEqual(len(validated.document["fact_set"]["facts"]), 2)
        self.assertEqual(len(validated.facts_by_id), 2)
        self.assertEqual(set(validated.source_blobs_by_path_hex), operation_paths)

    def test_e_013_private_worker_roundtrips_only_corrected_wire(self) -> None:
        for binding in closed_test_relation_observation_bindings():
            with self.subTest(binding=binding.launch_key):
                request = self._request_for_binding(binding)
                completed = self._run_worker(
                    request, launch_key=binding.launch_key
                )
                self.assertEqual(completed.returncode, 0, completed.stderr.decode())
                terminal = read_frame(
                    BytesIO(completed.stdout), payload_limit=1_048_576
                )
                expected = len(request["assigned_observation_item_ids"])
                self.assertEqual(terminal["protocol"], observation.PROTOCOL)
                self.assertEqual(len(terminal["canonical_relations"]), expected)
                self.assertEqual(len(terminal["observation_outcomes"]), expected)
                self.assertEqual(
                    validate_corrected_terminal(terminal, request=request),
                    terminal,
                )

        old_request = old_observation.build_relation_observation_request_document(
            inputs=self.inputs,
            derivation_id="old-observation-worker",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            fact_set_document=self.fact_set,
            observation_domain=self.domain,
        )
        rejected = self._run_worker(
            old_request, launch_key=self.binding.launch_key
        )
        self.assertEqual(rejected.returncode, 65)
        self.assertEqual(rejected.stdout, b"")

    def test_e_014_wire_and_worker_mint_no_controller_authority(self) -> None:
        import veritrail_review
        from veritrail_review import (
            _source_operation_relation_observation_worker as worker,
        )

        self.assertFalse(
            hasattr(
                veritrail_review,
                "ValidatedRelationObservationSourceOperationRequest",
            )
        )
        source = inspect.getsource(observation) + inspect.getsource(worker)
        for forbidden in (
            "BudgetContext",
            "AttemptEligibility",
            "claim_source_operation",
            "continuation",
        ):
            self.assertNotIn(forbidden, source)

    def _request_for_binding(self, binding) -> dict[str, object]:
        projection = build_relation_observation_source_operation_projection(
            self.classification,
            binding.descriptor,
            self.fact_set,
            self.domain,
        )
        return build_corrected_request(
            inputs=self.inputs,
            derivation_id=f"observation-wire-e-{binding.launch_key}",
            request_provenance=self.provenance,
            descriptor=binding.descriptor,
            fact_set_document=self.fact_set,
            observation_domain=self.domain,
            classification=self.classification,
            projection=projection,
        )

    def _recomputed_operands(self, request: dict[str, object]) -> str:
        return semantic_digest(
            observation.OPERANDS_DOMAIN,
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
                "observation_domain_digest": request[
                    "observation_domain_digest"
                ],
                "assigned_observation_item_ids": request[
                    "assigned_observation_item_ids"
                ],
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

    @staticmethod
    def _run_worker(
        request: dict[str, object], *, launch_key: str
    ) -> subprocess.CompletedProcess[bytes]:
        worker_path = (
            SOURCE_ROOT
            / "veritrail_review"
            / "_source_operation_relation_observation_worker.py"
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
