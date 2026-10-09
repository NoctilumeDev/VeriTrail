from __future__ import annotations

import ast
import hashlib
import inspect
import os
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_language_support as language_support_tests  # noqa: E402
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import _parse_fulfillment as parse  # noqa: E402
from veritrail_review import _parse_fulfillment_values as values  # noqa: E402
from veritrail_review import _parse_fulfillment_worker as worker  # noqa: E402
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    AttemptEligibility,
    AttemptEligibilityState,
    encode_frame,
)
from veritrail_review._windows_execution_cell import (  # noqa: E402
    WindowsExecutionCellObservation,
)
from veritrail_review.budget import (  # noqa: E402
    BudgetContext,
    ExecutionBudgetLimits,
)


class ParseFulfillmentPrivateImplementationTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.language_helper = language_support_tests.LanguageSupportPrivateClassifierTests()
        self.inputs = self.language_helper._inputs(
            [
                (b"pkg/a.py", b"pass\n", "100644", "REGULAR_BLOB"),
                (b"pkg/b.py", b"def bad(:\n", "100644", "REGULAR_BLOB"),
                (b"pkg/c.txt", b"ignored\n", "100644", "REGULAR_BLOB"),
            ]
        )
        self.classification = language_support.classify_language_support(self.inputs)
        self.context = self._context()
        self.parent = AttemptEligibility()
        self.assertTrue(self.parent.admit())
        self.runtime = self._runtime(Path(sys.executable).resolve())
        self.attempt = parse.create_parse_fulfillment_attempt(
            self.inputs,
            self.context,
            self.parent,
            self.classification,
            self.runtime,
        )

    def test_a_b_exact_eligible_denominator_and_frozen_decode(self) -> None:
        claims = self.attempt.claims()
        self.assertEqual(len(claims), 2)
        documents = [item._document_copy() for item in claims]
        self.assertEqual([item["source_text"] for item in documents], ["pass\n", "def bad(:\n"])
        self.assertEqual(
            [item["subject_identity"] for item in documents],
            list(self.attempt.denominator_subject_ids()),
        )
        joined_sources = b"".join(
            item._document_copy()["source_text"].encode() for item in claims
        )
        self.assertNotIn(b"ignored", joined_sources)

    def test_b_utf8_sig_is_inherited_without_redetection(self) -> None:
        inputs = self.language_helper._inputs(
            [(b"bom.py", b"\xef\xbb\xbfpass\n", "100644", "REGULAR_BLOB")]
        )
        classification = language_support.classify_language_support(inputs)
        attempt, _, _ = self._new_attempt(inputs=inputs, classification=classification)
        document = attempt.claims()[0]._document_copy()
        self.assertEqual(document["source_text"], "pass\n")

    def test_a_input_or_classification_drift_fails_closed(self) -> None:
        object.__setattr__(self.inputs, "policy_digest", "0" * 64)
        parent = AttemptEligibility()
        parent.admit()
        with self.assertRaises(parse._ParseFulfillmentError):
            parse.create_parse_fulfillment_attempt(
                self.inputs,
                self._context(),
                parent,
                self.classification,
                self.runtime,
            )
        self.assertIs(parent.state, AttemptEligibilityState.REVOKED)

    def test_c_runtime_capability_requires_exact_absolute_bytes(self) -> None:
        executable = Path(sys.executable).resolve()
        with self.assertRaises(parse._ParseFulfillmentError):
            parse.qualify_parse_runtime(executable, expected_sha256="0" * 64)
        with self.assertRaises(parse._ParseFulfillmentError):
            parse.qualify_parse_runtime(Path("python.exe"), expected_sha256="0" * 64)

    def test_c_claim_is_one_shot_and_concurrent_one_winner(self) -> None:
        claim = self.attempt.claims()[0]
        barrier = Barrier(2)

        def compete() -> object:
            barrier.wait()
            try:
                return claim.claim()
            except parse._ParseFulfillmentError as exc:
                return exc

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = tuple(pool.map(lambda _item: compete(), range(2)))
        self.assertEqual(sum(isinstance(item, parse.ClaimedParseRequest) for item in results), 1)
        self.assertEqual(
            sum(isinstance(item, parse._ParseFulfillmentError) for item in results),
            1,
        )

    def test_d_e_accepted_and_rejected_are_semantic_not_lifecycle(self) -> None:
        observations = self._execute_all(self.attempt)
        self.assertEqual([item.lifecycle for item in observations], ["COMPLETED", "COMPLETED"])
        self.assertEqual(
            [item.semantic_result_copy()["disposition"] for item in observations],
            ["ACCEPTED", "REJECTED"],
        )
        self.assertIsNotNone(observations[0].product_semantic_digest)
        self.assertIsNone(observations[1].product_semantic_digest)

    def test_e_runtime_unavailable_has_no_semantic_result(self) -> None:
        claim = self.attempt.claims()[0]
        terminal = {
            "protocol": values.PARSE_WORKER_PROTOCOL,
            "message_kind": "PARSE_TERMINAL",
            "lifecycle": "REFERENCE_RUNTIME_UNAVAILABLE",
            "semantic_result": None,
        }
        with mock.patch.object(
            parse, "run_windows_execution_cell", side_effect=self._cell(terminal)
        ):
            observation = parse.execute_parse_claim(claim)
        self.assertEqual(observation.lifecycle, "REFERENCE_RUNTIME_UNAVAILABLE")
        self.assertIsNone(observation.semantic_result_copy())
        with self.assertRaises(parse._ParseFulfillmentError):
            self.attempt.reconcile([observation])

    def test_e_runtime_byte_drift_is_not_parse_error(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            copied = Path(raw) / "python-copy.exe"
            copied.write_bytes(Path(sys.executable).read_bytes())
            runtime = self._runtime(copied)
            attempt, _, _ = self._new_attempt(runtime=runtime)
            copied.write_bytes(copied.read_bytes() + b"changed")
            observation = parse.execute_parse_claim(attempt.claims()[0])
            self.assertEqual(observation.lifecycle, "REFERENCE_RUNTIME_UNAVAILABLE")
            self.assertIsNone(observation.semantic_result_copy())

    def test_f_missing_duplicate_and_lifecycle_non_success_are_rejected(self) -> None:
        with self.subTest(world="missing"):
            observations = self._execute_all(self.attempt)
            with self.assertRaises(parse._ParseFulfillmentError):
                self.attempt.reconcile(observations[:1])

        self.setUp()
        with self.subTest(world="duplicate"):
            observations = self._execute_all(self.attempt)
            with self.assertRaises(parse._ParseFulfillmentError):
                self.attempt.reconcile([*observations, observations[0]])

        self.setUp()
        with self.subTest(world="lifecycle"):
            first = self._failed(self.attempt, self.attempt.claims()[0], "INFRASTRUCTURE_FAILED")
            second = self._failed(self.attempt, self.attempt.claims()[1], "INTERRUPTED")
            with self.assertRaises(parse._ParseFulfillmentError):
                self.attempt.reconcile([first, second])

    def test_f_foreign_attempt_is_rejected(self) -> None:
        other, _, _ = self._new_attempt()
        foreign = self._execute_all(other)[0]
        local = self._execute_all(self.attempt)
        with self.assertRaises(parse._ParseFulfillmentError):
            self.attempt.reconcile([foreign, local[1]])

    def test_f_dangling_and_cross_world_binding_are_rejected(self) -> None:
        local = self._execute_all(self.attempt)
        first_claim = self.attempt.claims()[0]
        semantic = local[0].semantic_result_copy()
        dangling = values.OwnedParseObservation._create(
            subject_identity="f" * 64,
            obligation_id="e" * 64,
            lifecycle="COMPLETED",
            semantic_result=semantic,
            attempt=self.attempt,
            claim=first_claim,
        )
        with self.assertRaises(parse._ParseFulfillmentError):
            self.attempt.reconcile([dangling, local[1]])

        self.setUp()
        local = self._execute_all(self.attempt)
        first_claim = self.attempt.claims()[0]
        document = first_claim._document_copy()
        cross_world = values.OwnedParseObservation._create(
            subject_identity=document["subject_identity"],
            obligation_id="d" * 64,
            lifecycle="COMPLETED",
            semantic_result=local[0].semantic_result_copy(),
            attempt=self.attempt,
            claim=first_claim,
        )
        with self.assertRaises(parse._ParseFulfillmentError):
            self.attempt.reconcile([cross_world, local[1]])

    def test_g_complete_reconciliation_owns_exact_product_set(self) -> None:
        closure = self.attempt.reconcile(self._execute_all(self.attempt))
        product_set = closure.product_set()
        document = product_set.product_set_document_copy()
        self.assertEqual(product_set.denominator_count, 2)
        self.assertEqual(product_set.accepted_count, 1)
        self.assertEqual(product_set.rejected_count, 1)
        self.assertEqual(len(document["accepted"]), 1)
        products = product_set.products_copy()
        self.assertEqual(set(products), {document["accepted"][0]["subject_identity"]})
        products.clear()
        self.assertEqual(len(product_set.products_copy()), 1)

    def test_g_same_tree_under_different_exact_subject_has_different_identity(self) -> None:
        first = self.attempt.reconcile(self._execute_all(self.attempt)).product_set()
        other_inputs = self.language_helper._inputs(
            [(b"pkg/other.py", b"pass\n", "100644", "REGULAR_BLOB")]
        )
        other_classification = language_support.classify_language_support(other_inputs)
        other, _, _ = self._new_attempt(
            inputs=other_inputs, classification=other_classification
        )
        second = other.reconcile(self._execute_all(other)).product_set()
        first_identity = first.product_set_document_copy()["accepted"][0][
            "product_semantic_digest"
        ]
        second_identity = second.product_set_document_copy()["accepted"][0][
            "product_semantic_digest"
        ]
        self.assertNotEqual(first_identity, second_identity)

    def test_g_same_membership_different_products_have_different_set_identity(
        self,
    ) -> None:
        first = self.attempt.reconcile(
            self._execute_with_accepted_source(self.attempt, "pass\n")
        ).product_set()
        second_attempt, _, _ = self._new_attempt()
        second = second_attempt.reconcile(
            self._execute_with_accepted_source(second_attempt, "value = 1\n")
        ).product_set()
        first_document = first.product_set_document_copy()
        second_document = second.product_set_document_copy()
        self.assertEqual(first_document["denominator"], second_document["denominator"])
        self.assertEqual(
            [item["subject_identity"] for item in first_document["accepted"]],
            [item["subject_identity"] for item in second_document["accepted"]],
        )
        self.assertNotEqual(
            first_document["accepted"][0]["product_semantic_digest"],
            second_document["accepted"][0]["product_semantic_digest"],
        )
        self.assertNotEqual(first.product_set_digest, second.product_set_digest)

    def test_g_zero_denominator_and_all_rejected_have_distinct_semantics(self) -> None:
        zero_inputs = self.language_helper._inputs(dispositions={b"pkg/module.py": "OUT_OF_SCOPE"})
        zero_classification = language_support.classify_language_support(zero_inputs)
        zero, _, _ = self._new_attempt(inputs=zero_inputs, classification=zero_classification)
        zero_set = zero.reconcile([]).product_set()

        rejected_inputs = self.language_helper._inputs(
            [(b"bad.py", b"def bad(:\n", "100644", "REGULAR_BLOB")]
        )
        rejected_classification = language_support.classify_language_support(rejected_inputs)
        rejected, _, _ = self._new_attempt(
            inputs=rejected_inputs, classification=rejected_classification
        )
        rejected_set = rejected.reconcile(self._execute_all(rejected)).product_set()
        self.assertEqual(zero_set.accepted_count, rejected_set.accepted_count, 0)
        self.assertNotEqual(zero_set.product_set_digest, rejected_set.product_set_digest)

    def test_h_continuation_is_one_shot_and_binds_original_live_attempt(self) -> None:
        closure = self.attempt.reconcile(self._execute_all(self.attempt))
        continuation = closure.claim_continuation()
        self.assertIs(continuation._product_set(), closure.product_set())
        with self.assertRaises(parse._ParseFulfillmentError):
            closure.claim_continuation()

        self.parent.revoke()
        with self.assertRaises(parse._ParseFulfillmentError):
            continuation._products_copy()

    def test_h_equal_semantics_do_not_transfer_continuation(self) -> None:
        first_closure = self.attempt.reconcile(self._execute_all(self.attempt))
        second, _, _ = self._new_attempt()
        second_closure = second.reconcile(self._execute_all(second))
        self.assertEqual(
            first_closure.product_set().product_set_digest,
            second_closure.product_set().product_set_digest,
        )
        self.assertIsNot(
            first_closure.claim_continuation(),
            second_closure.claim_continuation(),
        )

    def test_h_same_limits_fresh_context_cannot_replace_original(self) -> None:
        closure = self.attempt.reconcile(self._execute_all(self.attempt))
        fresh = self._context()
        self.assertEqual(fresh.limits, self.context.limits)
        object.__setattr__(
            self.attempt,
            "_OwnedParseFulfillmentAttempt__context",
            fresh,
        )
        with self.assertRaises(parse._ParseFulfillmentError):
            closure.claim_continuation()

    def test_private_boundary_does_not_change_fact_or_public_exports(self) -> None:
        import veritrail_review

        for name in (
            "OwnedParseFulfillmentAttempt",
            "OwnedParseProductSet",
            "create_parse_fulfillment_attempt",
            "execute_parse_claim",
        ):
            self.assertFalse(hasattr(veritrail_review, name))
            self.assertNotIn(name, veritrail_review.__all__)
        parameters = inspect.signature(
            parse.create_parse_fulfillment_attempt
        ).parameters
        self.assertNotIn("provider", parameters)
        document = (
            self.attempt.reconcile(self._execute_all(self.attempt))
            .product_set()
            .product_set_document_copy()
        )
        self.assertNotIn("artifact_kind", document)

    @unittest.skipUnless(
        os.name == "nt" and Path(r"D:\python-3.10.6\python.exe").is_file(),
        "local exact CPython 3.10.6 reference runtime is unavailable",
    )
    def test_local_exact_reference_runtime_witness(self) -> None:
        executable = Path(r"D:\python-3.10.6\python.exe")
        expected = "32ce1d2650ea8b9d394f5b8f94677d27888dccdc3713365bf903a8c465c9d776"
        if hashlib.sha256(executable.read_bytes()).hexdigest() != expected:
            self.skipTest("local exact CPython 3.10.6 bytes changed")
        inputs = self.language_helper._inputs(
            [
                (
                    b"pkg/except_star.py",
                    b"try:\n    pass\nexcept* Exception:\n    pass\n",
                    "100644",
                    "REGULAR_BLOB",
                ),
                (
                    b"pkg/match.py",
                    b"match value:\n    case _:\n        pass\n",
                    "100644",
                    "REGULAR_BLOB",
                ),
                (b"pkg/nul.py", b"pass\x00\n", "100644", "REGULAR_BLOB"),
                (b"pkg/top_return.py", b"return\n", "100644", "REGULAR_BLOB"),
            ]
        )
        classification = language_support.classify_language_support(inputs)
        attempt, _, _ = self._new_attempt(
            inputs=inputs,
            classification=classification,
            runtime=parse.qualify_parse_runtime(executable, expected_sha256=expected),
        )
        observations = [parse.execute_parse_claim(claim) for claim in attempt.claims()]
        closure = attempt.reconcile(observations)
        self.assertEqual(
            [item.semantic_result_copy()["disposition"] for item in observations],
            ["REJECTED", "ACCEPTED", "REJECTED", "ACCEPTED"],
        )
        self.assertEqual(closure.product_set().accepted_count, 2)

    @unittest.skipIf(
        sys.version_info[:3] == (3, 10, 6),
        "the ambient host is the exact reference runtime",
    )
    def test_ambient_runtime_cannot_impersonate_reference_runtime(self) -> None:
        observation = parse.execute_parse_claim(self.attempt.claims()[0])
        self.assertEqual(observation.lifecycle, "REFERENCE_RUNTIME_UNAVAILABLE")
        self.assertIsNone(observation.semantic_result_copy())

    def _new_attempt(self, *, inputs=None, classification=None, runtime=None):
        exact_inputs = self.inputs if inputs is None else inputs
        exact_classification = (
            language_support.classify_language_support(exact_inputs)
            if classification is None
            else classification
        )
        context = self._context()
        parent = AttemptEligibility()
        parent.admit()
        attempt = parse.create_parse_fulfillment_attempt(
            exact_inputs,
            context,
            parent,
            exact_classification,
            self.runtime if runtime is None else runtime,
        )
        return attempt, context, parent

    def _execute_all(self, attempt):
        observations = []
        for claim in attempt.claims():
            terminal = (
                self._rejected_terminal()
                if "def bad(:" in claim._document_copy()["source_text"]
                else self._accepted_terminal()
            )
            with mock.patch.object(
                parse,
                "run_windows_execution_cell",
                side_effect=self._cell(terminal),
            ):
                observations.append(parse.execute_parse_claim(claim))
        return observations

    def _execute_with_accepted_source(self, attempt, accepted_source):
        observations = []
        for claim in attempt.claims():
            terminal = (
                self._rejected_terminal()
                if "def bad(:" in claim._document_copy()["source_text"]
                else self._accepted_terminal_for_source(accepted_source)
            )
            with mock.patch.object(
                parse,
                "run_windows_execution_cell",
                side_effect=self._cell(terminal),
            ):
                observations.append(parse.execute_parse_claim(claim))
        return observations

    def _failed(self, attempt, claim, lifecycle):
        claimed = claim.claim()
        claimed._claim_ref()._child_eligibility().admit()
        document = claimed._document_copy()
        return values.OwnedParseObservation._create(
            subject_identity=document["subject_identity"],
            obligation_id=document["obligation_id"],
            lifecycle=lifecycle,
            semantic_result=None,
            attempt=attempt,
            claim=claim,
        )

    @staticmethod
    def _accepted_terminal():
        return ParseFulfillmentPrivateImplementationTests._accepted_terminal_for_source(
            "pass\n"
        )

    @staticmethod
    def _accepted_terminal_for_source(source):
        product = worker._tree_value(
            ast.parse(
                source,
                filename="<veritrail-r1-parse>",
                mode="exec",
                type_comments=False,
                feature_version=(3, 10),
            )
        )
        return {
            "protocol": values.PARSE_WORKER_PROTOCOL,
            "message_kind": "PARSE_TERMINAL",
            "lifecycle": "COMPLETED",
            "semantic_result": {
                "disposition": "ACCEPTED",
                "reason_codes": [],
                "product": product,
            },
        }

    @staticmethod
    def _rejected_terminal():
        return {
            "protocol": values.PARSE_WORKER_PROTOCOL,
            "message_kind": "PARSE_TERMINAL",
            "lifecycle": "COMPLETED",
            "semantic_result": {
                "disposition": "REJECTED",
                "reason_codes": ["PARSE_ERROR"],
                "product": None,
            },
        }

    @staticmethod
    def _cell(terminal):
        terminal_bytes = encode_frame(terminal, payload_limit=16 * 1024 * 1024)

        def run(context, eligibility, **kwargs):
            if not eligibility.admit():
                raise AssertionError("test cell could not admit child")
            kwargs["on_admitted"]()
            return WindowsExecutionCellObservation(
                admitted=True,
                process_created_suspended=True,
                process_assigned_before_resume=True,
                process_resumed=True,
                active_process_zero=True,
                handles_released=True,
                channel_threads_released=True,
                memory_limit_event_observed=False,
                stop_trigger=None,
                terminal_bytes=terminal_bytes,
                request_channel_failed=False,
                result_channel_failed=False,
                result_transport_exceeded=False,
                root_exit_code=0,
            )

        return run

    @staticmethod
    def _runtime(executable: Path):
        return parse.qualify_parse_runtime(
            executable,
            expected_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(),
        )

    @staticmethod
    def _context():
        return BudgetContext._admit_for_testing(
            ExecutionBudgetLimits(
                wall_clock_ms=60_000,
                memory_bytes=512 * 1024 * 1024,
                artifact_bytes=64 * 1024 * 1024,
            )
        )


if __name__ == "__main__":
    unittest.main()
