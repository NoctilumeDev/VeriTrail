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

import test_language_support as language_support_tests  # noqa: E402
import test_source_operation_projection as projection_support  # noqa: E402
from veritrail_review import _execution_cell_application as old_fact  # noqa: E402
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import _source_operation_fact_application as fact  # noqa: E402
from veritrail_review import _source_operation_projection as projection  # noqa: E402
from veritrail_review._execution_cell_binding import (  # noqa: E402
    closed_test_binding,
)
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    encode_frame,
    read_frame,
)
from veritrail_review.canonical import semantic_digest  # noqa: E402


class SourceOperationFactWireStageCTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        support = projection_support.SourceOperationProjectionStageATests(
            "test_a_001_fact_projection_is_exact_eligible_upper_bound"
        )
        support.setUp()
        self.support = support
        self.inputs = support.inputs
        self.classification = support.classification
        self.descriptor = support.fact_descriptor
        self.projection = (
            projection.build_fact_derivation_source_operation_projection(
                self.classification, self.descriptor
            )
        )
        self.provenance = self._provenance(self.inputs)
        self.request = fact.build_fact_source_operation_request_document(
            inputs=self.inputs,
            derivation_id="fact-wire-c",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
            classification=self.classification,
            projection=self.projection,
        )

    def test_c_001_corrected_request_filters_to_exact_fact_operation_set(self) -> None:
        self.assertEqual(self.request["protocol"], fact.PROTOCOL)
        self.assertEqual(fact.PROTOCOL, "veritrail-review-derivation-cell/0.2")
        self.assertEqual(
            fact.OPERANDS_DOMAIN, "veritrail.review.provider-operands/0.4"
        )
        self.assertEqual(
            self.request["language_support_classification"],
            self.classification.classification_document_copy(),
        )
        self.assertEqual(
            self.request["source_operation_projection"],
            self.projection.projection_document_copy(),
        )
        paths = [
            bytes.fromhex(item["git_path"]["git_path_hex"])
            for item in self.request["source_blobs"]
        ]
        self.assertEqual(paths, [b"pkg/a.py", b"pkg/b.py"])
        self.assertNotIn(b"pkg/c.py", paths)
        self.assertNotIn(b"pkg/out.py", paths)

    def test_c_002_worker_revalidates_exact_corrected_request(self) -> None:
        validated = fact.validate_fact_source_operation_request_document(
            self.request, launch_key="stable-a"
        )
        self.assertEqual(validated.descriptor, self.descriptor)
        self.assertEqual(
            validated.supported_paths,
            frozenset({b"pkg/a.py".hex(), b"pkg/b.py".hex()}),
        )
        self.assertEqual(
            set(validated.source_blobs_by_path_hex), validated.supported_paths
        )
        self.assertEqual(
            validated.provider_run_id,
            old_fact.provider_run_id(
                "fact-wire-c", self.descriptor, self.request["operands_digest"]
            ),
        )

    def test_c_003_old_and_new_wire_identities_do_not_fallback(self) -> None:
        with self.assertRaises(old_fact.ApplicationProtocolError):
            old_fact.validate_request_document(self.request, launch_key="stable-a")

        old_request = old_fact.build_request_document(
            inputs=self.inputs,
            derivation_id="old-fact-wire",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
        )
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_request_document(
                old_request, launch_key="stable-a"
            )

    def test_c_004_operands_extend_history_without_reusing_old_identity(self) -> None:
        expected = semantic_digest(
            "veritrail.review.provider-operands/0.4",
            {
                "source_snapshot_digest": self.inputs.source_snapshot_digest,
                "policy_digest": self.inputs.policy_digest,
                "analysis_scope_digest": self.inputs.analysis_scope_digest,
                "slice_policy_digest": self.inputs.slice_policy_digest,
                "derivation_profile_digest": self.inputs.derivation_profile_digest,
                **self.descriptor.document(),
                "language_support_function": (
                    self.classification.language_support_function
                ),
                "classification_digest": self.classification.classification_digest,
                "source_operation_projection_digest": (
                    self.projection.source_operation_projection_digest
                ),
            },
        )
        old_digest = old_fact.provider_operands_digest(self.inputs, self.descriptor)
        self.assertEqual(self.request["operands_digest"], expected)
        self.assertNotEqual(expected, old_digest)
        self.assertNotEqual(
            old_fact.provider_run_id("fact-wire-c", self.descriptor, expected),
            old_fact.provider_run_id("fact-wire-c", self.descriptor, old_digest),
        )

    def test_c_005_self_consistent_eligible_subset_is_still_rejected(self) -> None:
        changed = copy.deepcopy(self.request)
        projection_document = changed["source_operation_projection"]
        projection_document["operation_subject_ids"] = projection_document[
            "operation_subject_ids"
        ][:-1]
        projection_document["source_operation_projection_digest"] = semantic_digest(
            "veritrail.review.private-source-operation-projection/0.1",
            {
                key: value
                for key, value in projection_document.items()
                if key != "source_operation_projection_digest"
            },
        )
        changed["source_blobs"] = changed["source_blobs"][:-1]
        changed["operands_digest"] = semantic_digest(
            fact.OPERANDS_DOMAIN,
            {
                "source_snapshot_digest": changed["source_snapshot_digest"],
                "policy_digest": changed["policy_digest"],
                "analysis_scope_digest": changed["analysis_scope_digest"],
                "slice_policy_digest": changed["slice_policy_digest"],
                "derivation_profile_digest": changed[
                    "derivation_profile_digest"
                ],
                **self.descriptor.document(),
                "language_support_function": (
                    self.classification.language_support_function
                ),
                "classification_digest": self.classification.classification_digest,
                "source_operation_projection_digest": projection_document[
                    "source_operation_projection_digest"
                ],
            },
        )

        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_request_document(
                changed, launch_key="stable-a"
            )

    def test_c_006_included_body_set_and_bytes_are_exactly_reconciled(self) -> None:
        mutations = (
            lambda item: item["source_blobs"].pop(),
            lambda item: item["source_blobs"].append(
                copy.deepcopy(self._blob_for_path(self.inputs, b"pkg/c.py"))
            ),
            lambda item: item["source_blobs"][0].__setitem__(
                "content_base64", base64.b64encode(b"changed\n").decode("ascii")
            ),
            lambda item: item["source_blobs"].reverse(),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(self.request)
                mutate(changed)
                with self.assertRaises(fact.FactSourceOperationProtocolError):
                    fact.validate_fact_source_operation_request_document(
                        changed, launch_key="stable-a"
                    )

    def test_c_007_classification_projection_and_descriptor_tamper_fail_closed(
        self,
    ) -> None:
        mutations = (
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
                with self.assertRaises(fact.FactSourceOperationProtocolError):
                    fact.validate_fact_source_operation_request_document(
                        changed, launch_key="stable-a"
                    )

    def test_c_008_corrected_terminal_echoes_new_run_identity_only(self) -> None:
        validated = fact.validate_fact_source_operation_request_document(
            self.request, launch_key="stable-a"
        )
        candidate = self._candidate(validated)
        canonical = fact.canonicalize_fact_candidates(validated, [candidate])
        terminal = fact.fact_source_operation_terminal_document(
            validated, terminal_kind="COMPLETED", canonical_facts=canonical
        )
        self.assertEqual(terminal["protocol"], fact.PROTOCOL)
        self.assertEqual(terminal["provider_run_id"], validated.provider_run_id)
        self.assertEqual(
            fact.validate_fact_source_operation_terminal_document(
                terminal, request=self.request
            ),
            terminal,
        )
        with self.assertRaises(old_fact.ApplicationProtocolError):
            old_fact.validate_terminal_document(terminal, request=self.request)

    def test_c_009_old_terminal_is_not_accepted_by_corrected_validator(self) -> None:
        old_request = old_fact.build_request_document(
            inputs=self.inputs,
            derivation_id="old-fact-wire",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
        )
        old_validated = old_fact.validate_request_document(
            old_request, launch_key="stable-a"
        )
        old_terminal = old_fact.terminal_document(
            old_validated, terminal_kind="COMPLETED", canonical_facts=[]
        )
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_terminal_document(
                old_terminal, request=old_request
            )

    def test_c_010_non_success_terminal_cannot_retain_fact_output(self) -> None:
        validated = fact.validate_fact_source_operation_request_document(
            self.request, launch_key="stable-a"
        )
        canonical = fact.canonicalize_fact_candidates(
            validated, [self._candidate(validated)]
        )
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.fact_source_operation_terminal_document(
                validated,
                terminal_kind="PROVIDER_FAILED",
                canonical_facts=canonical,
            )
        terminal = fact.fact_source_operation_terminal_document(
            validated, terminal_kind="PROVIDER_FAILED"
        )
        terminal["reported_fact_ids"] = ["0" * 64]
        with self.assertRaises(fact.FactSourceOperationProtocolError):
            fact.validate_fact_source_operation_terminal_document(
                terminal, request=self.request
            )

    def test_c_011_all_unsupported_world_has_exact_empty_body_request(self) -> None:
        helper = language_support_tests.LanguageSupportPrivateClassifierTests()
        inputs = helper._inputs(
            [(b"pkg/c.py", b"# coding: utf.8\n", "100644", "REGULAR_BLOB")]
        )
        classification = language_support.classify_language_support(inputs)
        projection_value = (
            projection.build_fact_derivation_source_operation_projection(
                classification, self.descriptor
            )
        )
        request = fact.build_fact_source_operation_request_document(
            inputs=inputs,
            derivation_id="fact-empty-wire-c",
            request_provenance=self._provenance(inputs),
            descriptor=self.descriptor,
            classification=classification,
            projection=projection_value,
        )
        validated = fact.validate_fact_source_operation_request_document(
            request, launch_key="stable-a"
        )
        self.assertEqual(classification.denominator_count, 1)
        self.assertEqual(classification.eligible_count, 0)
        self.assertEqual(request["source_blobs"], [])
        self.assertEqual(validated.supported_paths, frozenset())

    def test_c_012_wire_is_private_and_does_not_mint_attempt_authority(self) -> None:
        import veritrail_review

        self.assertFalse(
            hasattr(veritrail_review, "ValidatedFactSourceOperationRequest")
        )
        self.assertFalse(
            hasattr(veritrail_review, "build_fact_source_operation_request_document")
        )
        parameters = inspect.signature(
            fact.build_fact_source_operation_request_document
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
        self.assertNotIn("attempt_id", self.request)
        self.assertNotIn("authority", self.request)

    def test_c_013_private_worker_round_trips_only_the_corrected_wire(self) -> None:
        completed = self._run_worker(self.request, launch_key="stable-a")
        self.assertEqual(completed.returncode, 0, completed.stderr.decode())
        terminal = read_frame(BytesIO(completed.stdout), payload_limit=1_048_576)
        self.assertEqual(terminal["protocol"], fact.PROTOCOL)
        self.assertEqual(len(terminal["canonical_facts"]), 1)
        self.assertEqual(
            fact.validate_fact_source_operation_terminal_document(
                terminal, request=self.request
            ),
            terminal,
        )

        old_request = old_fact.build_request_document(
            inputs=self.inputs,
            derivation_id="old-fact-wire-worker",
            request_provenance=self.provenance,
            descriptor=self.descriptor,
        )
        rejected = self._run_worker(old_request, launch_key="stable-a")
        self.assertEqual(rejected.returncode, 65)
        self.assertEqual(rejected.stdout, b"")

    def test_c_014_private_worker_has_no_controller_or_public_entrypoint(self) -> None:
        import veritrail_review
        from veritrail_review import _source_operation_fact_worker as worker

        self.assertFalse(hasattr(veritrail_review, "source_operation_fact_worker"))
        self.assertFalse(hasattr(veritrail_review, "run_source_operation_fact_cell"))
        self.assertEqual(worker.main([]), 64)
        source = inspect.getsource(worker)
        self.assertNotIn("BudgetContext", source)
        self.assertNotIn("AttemptEligibility", source)

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
    def _candidate(
        validated: fact.ValidatedFactSourceOperationRequest,
    ) -> dict[str, object]:
        path_hex = sorted(validated.supported_paths)[0]
        return {
            "subject_space": "MODULE_ENTITY",
            "fact_kind": "MODULE",
            "source_anchor": {
                "git_path": {
                    "path_kind": "GIT_PATH",
                    "git_path_hex": path_hex,
                },
                "start_byte": 0,
                "end_byte": validated.source_sizes_by_path_hex[path_hex],
            },
            "local_ordinal": 0,
            "semantic_attributes": {"module_key_parts": None},
        }

    @staticmethod
    def _run_worker(
        request: dict[str, object], *, launch_key: str
    ) -> subprocess.CompletedProcess[bytes]:
        worker_path = (
            SOURCE_ROOT / "veritrail_review" / "_source_operation_fact_worker.py"
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
