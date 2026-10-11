from __future__ import annotations

import ast
import copy
import io
import json
import os
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from threading import Barrier
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
for location in (PLUGIN_ROOT / "src", PLUGIN_ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from test_execution_cell import _canonical_artifact, _seal_policy  # noqa: E402
import test_language_support as language_tests  # noqa: E402
import test_parse_fulfillment as parse_tests  # noqa: E402
from veritrail_review import _parse_fulfillment as parse  # noqa: E402
from veritrail_review import _parse_product_fact_consumer as consumer  # noqa: E402
from veritrail_review import _parse_product_fact_protocol as protocol  # noqa: E402
from veritrail_review import _parse_product_fact_worker as worker  # noqa: E402
from veritrail_review._execution_cell_protocol import (  # noqa: E402
    AttemptEligibility,
    AttemptEligibilityState,
    ExecutionCellTransportSafetyLimits,
    encode_frame,
    read_frame,
)
from veritrail_review._language_support import classify_language_support  # noqa: E402
from veritrail_review._multi_provider_applicability import (
    closed_test_multi_provider_bindings,
)  # noqa: E402
from veritrail_review._parse_product_fact_anchors import (
    product_byte_anchors,
)  # noqa: E402
from veritrail_review._windows_execution_cell import (
    CellReleaseError,
    CellRuntimeUnavailableError,
)  # noqa: E402
from veritrail_review.budget import BudgetState  # noqa: E402
from veritrail_review.canonical import canonical_json_bytes  # noqa: E402
from veritrail_review.derivation_input_contracts import DerivationInputSet  # noqa: E402


BOM_SOURCE = (
    b"\xef\xbb\xbf# caf\xc3\xa9\r\nimport os\r\nclass C:\r\n"
    b"    def method(self):\r\n        return '\xc3\xa9'\r\n"
)
ParseHelper = parse_tests.ParseFulfillmentPrivateImplementationTests()


class ProductFactConsumerTests(unittest.TestCase):
    maxDiff = None

    def _inputs(self, bodies=None, *, advisory=False):
        inputs = language_tests.LanguageSupportPrivateClassifierTests()._inputs(
            [
                (path, body, "100644", "REGULAR_BLOB")
                for path, body in (
                    bodies
                    if bodies is not None
                    else [(b"pkg/a.py", BOM_SOURCE), (b"pkg/b.py", b"def bad(:\n")]
                )
            ]
        )
        if not advisory:
            return inputs
        policy = inputs.review_policy_document_copy()
        policy["provider_requirements"].append(
            {
                "capability_id": "python-ast-advisory",
                "required": False,
                "composition_mode": "CUMULATIVE",
            }
        )
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=inputs.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=inputs.verified_blob_bytes_by_object_identity,
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=inputs.derivation_profile_digest,
        )

    def _parse_world(self, inputs=None, *, real=False):
        inputs = self._inputs() if inputs is None else inputs
        context = ParseHelper._context()
        eligibility = AttemptEligibility()
        self.assertTrue(eligibility.admit())
        executable = (
            Path(os.environ["VERITRAIL_R1_REFERENCE_PYTHON"])
            if real
            else Path(sys.executable)
        )
        attempt = parse.create_parse_fulfillment_attempt(
            inputs,
            context,
            eligibility,
            classify_language_support(inputs),
            ParseHelper._runtime(executable.resolve()),
        )
        observations = []
        for claim in attempt.claims():
            if real:
                observations.append(parse.execute_parse_claim(claim))
                continue
            source = claim._document_copy()["source_text"]
            try:
                terminal = ParseHelper._accepted_terminal_for_source(source)
            except SyntaxError:
                terminal = ParseHelper._rejected_terminal()
            with mock.patch.object(
                parse,
                "run_windows_execution_cell",
                side_effect=ParseHelper._cell(terminal),
            ):
                observations.append(parse.execute_parse_claim(claim))
        return attempt, attempt.reconcile(observations), context, eligibility

    def _consumer(self, inputs=None, *, advisory=False, real=False, limits=None):
        if inputs is None:
            inputs = self._inputs(advisory=advisory)
        attempt, closure, context, eligibility = self._parse_world(inputs, real=real)
        kwargs = {} if limits is None else {"transport_limits": limits}
        parent = consumer.create_product_fact_consumer(
            closure,
            derivation_id="product-consumer-world",
            bindings=closed_test_multi_provider_bindings(include_advisory=advisory),
            **kwargs,
        )
        return parent, context, eligibility, closure, attempt

    @staticmethod
    def _cell(transform=None, *, kind="COMPLETED", lifecycle_change=None):
        def run(context, eligibility, **kwargs):
            request = read_frame(
                io.BytesIO(kwargs["request_frame"]), payload_limit=64 * 1024 * 1024
            )
            protocol.validate_request(request, launch_key=kwargs["arguments"][-3])
            records = (
                protocol.product_candidate_records(request)
                if kind == "COMPLETED"
                else []
            )
            terminal = protocol.terminal_document(
                request, terminal_kind=kind, records=records
            )
            if transform is not None:
                transform(terminal, request)
            result = ParseHelper._cell(terminal)(context, eligibility, **kwargs)
            return (
                result
                if lifecycle_change is None
                else replace(result, **lifecycle_change)
            )

        return run

    def _execute(self, parent, **kwargs):
        with mock.patch.object(
            consumer, "run_windows_execution_cell", side_effect=self._cell(**kwargs)
        ):
            return tuple(
                consumer.execute_product_fact_claim(c) for c in parent.claims()
            )

    def test_a_b_complete_accepted_membership_excludes_rejected_body(self):
        parent, _, _, closure, _ = self._consumer()
        accepted = closure.product_set().product_set_document_copy()["accepted"]
        projections = [c.projection_copy() for c in parent.claims()]
        self.assertEqual(len(projections), 2)
        self.assertEqual(
            [p["assigned_products"][0]["subject_identity"] for p in projections],
            [accepted[0]["subject_identity"]] * 2,
        )
        self.assertEqual(
            projections[0]["product_set_digest"], projections[1]["product_set_digest"]
        )
        self.assertNotEqual(
            protocol.projection_digest(projections[0]),
            protocol.projection_digest(projections[1]),
        )
        for projection in projections:
            self.assertEqual(len(projection["assigned_products"]), 1)
            self.assertNotIn(b"def bad", canonical_json_bytes(projection))
            self.assertEqual(
                projection["assigned_products"][0]["git_path_hex"], b"pkg/a.py".hex()
            )

    def test_pfc_i_001_equal_semantics_cannot_transplant_child_history(self):
        inputs = self._inputs()
        first, _, _, _, _ = self._consumer(inputs)
        second, _, _, _, _ = self._consumer(inputs)
        self.assertEqual(
            first.claims()[0].projection_copy(), second.claims()[0].projection_copy()
        )
        first_history, second_history = self._execute(first), self._execute(second)
        self.assertNotEqual(
            first_history[0].terminal_bytes, second_history[0].terminal_bytes
        )
        with self.assertRaises(consumer.ProductFactConsumerError):
            second.reconcile(first_history)

    def test_pfc_i_002_equal_limits_context_swap_rejected(self):
        parent, original, eligibility, _, _ = self._consumer()
        replacement = ParseHelper._context()
        self.assertIsNot(original, replacement)
        object.__setattr__(parent, "_OwnedProductFactConsumer__context", replacement)
        with self.assertRaises(consumer.ProductFactConsumerError):
            parent.claims()
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_pfc_i_003_caller_subset_has_no_membership_authority(self):
        _, closure, _, eligibility = self._parse_world()
        with self.assertRaises(consumer.ProductFactConsumerError):
            consumer.create_product_fact_consumer(
                closure,
                derivation_id="subset",
                bindings=closed_test_multi_provider_bindings()[:1],
            )
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)
        parent, _, _, _, _ = self._consumer(
            self._inputs([(b"a.py", b"pass\n"), (b"b.py", b"pass\n")])
        )
        claim = parent.claims()[0]
        projection = claim.projection_copy()
        projection["assigned_products"].pop()
        object.__setattr__(
            claim,
            "_OwnedProductFactClaim__projection",
            canonical_json_bytes(projection),
        )
        with self.assertRaises(consumer.ProductFactConsumerError):
            claim.claim()
        with self.assertRaises(consumer.ProductFactConsumerError):
            claim.claim()

    def test_pfc_i_004_foreign_provider_claim_and_terminal_rejected(self):
        parent, _, _, _, _ = self._consumer()
        a, b = parent.claims()
        request = a.claim().request_copy()
        with self.assertRaises(protocol.ProductFactProtocolError):
            protocol.validate_request(request, launch_key=b.binding.launch_key)
        wrong = protocol.terminal_document(
            b.claim().request_copy(), terminal_kind="COMPLETED", records=[]
        )
        with self.assertRaises(protocol.ProductFactProtocolError):
            protocol.admit_terminal(
                wrong, request=request, launch_key=a.binding.launch_key
            )

    def test_pfc_i_005_concurrent_claim_exactly_one_winner(self):
        parent, _, _, _, _ = self._consumer()
        claim = parent.claims()[0]
        barrier = Barrier(2)

        def compete(_):
            barrier.wait()
            try:
                return claim.claim()
            except consumer.ProductFactConsumerError as exc:
                return exc

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = tuple(pool.map(compete, range(2)))
        self.assertEqual(
            sum(type(r) is consumer.ClaimedProductFactRequest for r in results), 1
        )
        self.assertEqual(
            sum(type(r) is consumer.ProductFactConsumerError for r in results), 1
        )

    def test_pfc_i_006_raw_source_and_loader_fields_rejected_before_execution(self):
        parent, _, _, _, _ = self._consumer()
        claim = parent.claims()[0]
        request = claim.claim().request_copy()
        for field in ("source_blobs", "source_text", "repository_path", "path_loader"):
            with self.subTest(field=field):
                bad = copy.deepcopy(request)
                bad["projection"]["assigned_products"][0][field] = "raw authority"
                with self.assertRaises(protocol.ProductFactProtocolError):
                    protocol.validate_request(bad, launch_key=claim.binding.launch_key)
                # The actual worker entrypoint rejects the document before derivation.
                streams = type(
                    "Streams",
                    (),
                    {
                        "buffer": io.BytesIO(
                            encode_frame(bad, payload_limit=64 * 1024 * 1024)
                        )
                    },
                )()
                with (
                    mock.patch.object(worker.sys, "stdin", streams),
                    mock.patch.object(
                        worker, "product_candidate_records"
                    ) as derivation,
                ):
                    self.assertEqual(
                        worker.main([claim.binding.launch_key, "67108864", "16777216"]),
                        65,
                    )
                derivation.assert_not_called()

    def test_pfc_i_007_product_derivation_does_not_read_or_reparse(self):
        parent, _, _, _, _ = self._consumer()
        claim = parent.claims()[0]
        request = claim.claim().request_copy()
        with (
            mock.patch.object(ast, "parse", side_effect=AssertionError("reparse")),
            mock.patch.object(Path, "read_bytes", side_effect=AssertionError("reread")),
        ):
            records = protocol.product_candidate_records(request)
            _, facts = protocol.admit_terminal(
                protocol.terminal_document(
                    request, terminal_kind="COMPLETED", records=records
                ),
                request=request,
                launch_key=claim.binding.launch_key,
            )
        self.assertEqual(len(facts), 2)

    def test_pfc_i_008_009_foreign_candidate_invalidates_whole_child(self):
        parent, _, _, closure, _ = self._consumer()
        rejected = closure.product_set().product_set_document_copy()["rejected"][0][
            "subject_identity"
        ]

        def transform(terminal, request):
            bad = copy.deepcopy(terminal["candidate_records"][0])
            bad["product_subject_identity"] = rejected
            terminal["candidate_records"].append(bad)

        observations = self._execute(parent, transform=transform)
        self.assertTrue(all(o.terminal_frame_bytes for o in observations))
        self.assertTrue(
            all(
                o.lifecycle == "FAILED" and not o.canonical_fact_bytes
                for o in observations
            )
        )
        closed = parent.reconcile(observations)
        self.assertEqual(closed.document_copy()["consumer_status"], "FAILED")
        self.assertIsNone(closed.document_copy()["fact_set"])

    def test_pfc_i_010_digest_echo_cannot_qualify_unbound_candidate(self):
        for axis in (
            "node_path",
            "provider_run_id",
            "product_semantic_digest",
            "semantic_attributes",
        ):
            with self.subTest(axis=axis):
                parent, _, _, _, _ = self._consumer()

                def mutate(terminal, request):
                    record = terminal["candidate_records"][-1]
                    if axis == "semantic_attributes":
                        record["candidate"][axis] = {"declared_name": "Invented"}
                    else:
                        record[axis] = "foreign" if axis == "node_path" else "0" * 64

                result = self._execute(parent, transform=mutate)
                self.assertTrue(all(o.lifecycle == "FAILED" for o in result))

    def test_pfc_i_011_012_first_child_does_not_finish_original_attempt(self):
        parent, context, eligibility, _, _ = self._consumer()
        a, b = parent.claims()
        with mock.patch.object(
            consumer, "run_windows_execution_cell", side_effect=self._cell()
        ):
            first = consumer.execute_product_fact_claim(a)
            self.assertFalse(b._was_consumed())
            self.assertIs(context.state, BudgetState.RUNNING)
            self.assertIs(eligibility.state, AttemptEligibilityState.ADMITTED)
            second = consumer.execute_product_fact_claim(b)
        closed = parent.reconcile([second, first])
        document = closed.document_copy()
        self.assertEqual(document["consumer_status"], "COMPLETED")
        self.assertEqual(len(document["fact_set"]["facts"]), 2)
        self.assertTrue(
            all(len(f["provenance_refs"]) == 2 for f in document["fact_set"]["facts"])
        )
        continuation = closed.claim_continuation()
        self.assertIs(continuation._context_ref(), context)
        self.assertEqual(continuation._fact_set_copy(), document["fact_set"])
        with self.assertRaises(consumer.ProductFactConsumerError):
            closed.claim_continuation()

    def test_pfc_i_013_incomplete_parse_cannot_be_known_empty(self):
        inputs = self._inputs([(b"bad.py", b"def bad(:\n")])
        context, eligibility = ParseHelper._context(), AttemptEligibility()
        eligibility.admit()
        attempt = parse.create_parse_fulfillment_attempt(
            inputs,
            context,
            eligibility,
            classify_language_support(inputs),
            ParseHelper._runtime(Path(sys.executable).resolve()),
        )
        with self.assertRaises(parse._ParseFulfillmentError):
            attempt.reconcile([])
        with self.assertRaises(consumer.ProductFactConsumerError):
            consumer.create_product_fact_consumer(
                attempt,
                derivation_id="incomplete",
                bindings=closed_test_multi_provider_bindings(),
            )

    def test_pfc_i_014_zero_denominator_and_all_rejected_block_without_facts(self):
        identities = []
        for bodies in ([(b"other.txt", b"text\n")], [(b"bad.py", b"def bad(:\n")]):
            parent, _, _, closure, _ = self._consumer(self._inputs(bodies))
            identities.append(closure.product_set().product_set_digest)
            self.assertEqual(parent.scheduling_status, "BLOCKED_NO_ACCEPTED_PRODUCTS")
            self.assertEqual(parent.claims(), ())
            with mock.patch.object(consumer, "run_windows_execution_cell") as cell:
                blocked = parent.reconcile([])
            cell.assert_not_called()
            doc = blocked.document_copy()
            self.assertEqual(doc["consumer_status"], "BLOCKED_NO_ACCEPTED_PRODUCTS")
            self.assertEqual(doc["child_history"], [])
            self.assertIsNone(doc["fact_set"])
            with self.assertRaises(consumer.ProductFactConsumerError):
                blocked.claim_continuation()
        self.assertNotEqual(*identities)

    def test_pfc_i_015_product_location_outside_exact_bytes_rejected(self):
        parent, _, _, _, _ = self._consumer()
        member = parent.claims()[0].projection_copy()["assigned_products"][0]
        product = member["product"]
        node = next(
            n for _, n in protocol.walk_product(product) if n["node_type"] == "ClassDef"
        )
        node["attributes"]["end_col_offset"]["value"] = 10000
        with self.assertRaises(protocol.ProductFactProtocolError):
            product_byte_anchors(product, BOM_SOURCE, encoding="UTF-8-SIG")

    def test_pfc_i_016_bom_crlf_multibyte_exact_anchor(self):
        parent, _, _, _, _ = self._consumer()
        member = parent.claims()[0].projection_copy()["assigned_products"][0]
        path = next(
            p
            for p, n in protocol.walk_product(member["product"])
            if n["node_type"] == "ClassDef"
        )
        self.assertEqual(
            member["node_anchors"][path], {"start_byte": 23, "end_byte": 75}
        )

        def mutate(terminal, request):
            terminal["candidate_records"][-1]["candidate"]["source_anchor"][
                "start_byte"
            ] -= 3

        self.assertTrue(
            all(
                o.lifecycle == "FAILED" for o in self._execute(parent, transform=mutate)
            )
        )

    def test_pfc_i_017_private_successor_does_not_change_historical_protocols(self):
        import veritrail_review
        from veritrail_review import (
            _source_operation_fact_application,
            _source_operation_projection,
        )

        self.assertNotIn("create_product_fact_consumer", vars(veritrail_review))
        self.assertNotEqual(protocol.PROTOCOL, "veritrail-review-derivation-cell/0.2")
        self.assertNotEqual(
            protocol.PROJECTION_DOMAIN,
            "veritrail.review.private-source-operation-projection/0.1",
        )
        historical = Path(_source_operation_fact_application.__file__).read_text()
        self.assertEqual(
            _source_operation_fact_application.PROTOCOL,
            "veritrail-review-derivation-cell/0.2",
        )
        self.assertNotIn(protocol.CONSUMER_FUNCTION, historical)
        self.assertNotIn(
            protocol.CONSUMER_FUNCTION,
            Path(_source_operation_projection.__file__).read_text(),
        )

    def test_pfc_i_018_completed_echo_without_bound_terminal_is_failed(self):
        parent, _, _, _, _ = self._consumer()

        def mutate(terminal, request):
            terminal.clear()
            terminal.update(
                {
                    "terminal_kind": "COMPLETED",
                    "product_set_digest": request["projection"]["product_set_digest"],
                }
            )

        self.assertTrue(
            all(
                o.lifecycle == "FAILED" for o in self._execute(parent, transform=mutate)
            )
        )

    def test_optional_failure_does_not_replace_requiredness(self):
        parent, context, eligibility, _, _ = self._consumer(advisory=True)
        observations = []
        for claim in parent.claims():
            kind = (
                "PROVIDER_FAILED"
                if claim.binding.descriptor.capability_id.endswith("advisory")
                else "COMPLETED"
            )
            with mock.patch.object(
                consumer,
                "run_windows_execution_cell",
                side_effect=self._cell(kind=kind),
            ):
                observations.append(consumer.execute_product_fact_claim(claim))
        doc = parent.reconcile(observations).document_copy()
        self.assertEqual(doc["consumer_status"], "COMPLETED")
        self.assertEqual(
            [h["lifecycle"] for h in doc["child_history"]].count("FAILED"), 1
        )
        self.assertIs(context.state, BudgetState.RUNNING)
        self.assertIs(eligibility.state, AttemptEligibilityState.ADMITTED)

    def test_required_failure_precedence_and_full_request_history(self):
        parent, _, eligibility, _, _ = self._consumer()
        claims = parent.claims()
        with mock.patch.object(
            consumer,
            "run_windows_execution_cell",
            side_effect=self._cell(kind="PROVIDER_UNAVAILABLE"),
        ):
            unavailable = consumer.execute_product_fact_claim(claims[0])
        with mock.patch.object(
            consumer,
            "run_windows_execution_cell",
            side_effect=self._cell(kind="PROVIDER_FAILED"),
        ):
            failed = consumer.execute_product_fact_claim(claims[1])
        doc = parent.reconcile([unavailable, failed]).document_copy()
        self.assertEqual(doc["consumer_status"], "FAILED")
        self.assertTrue(
            all("child_attempt_id" in h["request"] for h in doc["child_history"])
        )
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_release_or_runtime_failure_has_no_facts(self):
        for exception, status in (
            (CellReleaseError("closed"), "RELEASE_FAILED"),
            (CellRuntimeUnavailableError("missing"), "UNAVAILABLE"),
        ):
            with self.subTest(status=status):
                parent, _, _, _, _ = self._consumer()
                with mock.patch.object(
                    consumer, "run_windows_execution_cell", side_effect=exception
                ):
                    observation = consumer.execute_product_fact_claim(
                        parent.claims()[0]
                    )
                self.assertEqual(observation.lifecycle, status)
                self.assertEqual(observation.canonical_fact_bytes, ())

    def test_lifecycle_evidence_required_even_for_valid_terminal(self):
        for flag in (
            "active_process_zero",
            "handles_released",
            "channel_threads_released",
        ):
            with self.subTest(flag=flag):
                parent, _, _, _, _ = self._consumer()
                observations = self._execute(parent, lifecycle_change={flag: False})
                self.assertTrue(
                    all(
                        o.lifecycle == "INFRASTRUCTURE_FAILED"
                        and not o.canonical_fact_bytes
                        for o in observations
                    )
                )

    def test_missing_duplicate_and_mutated_history_cannot_reconcile(self):
        for mode in ("missing", "duplicate", "mutation", "owner"):
            with self.subTest(mode=mode):
                parent, _, eligibility, _, _ = self._consumer()
                observations = list(self._execute(parent))
                if mode == "missing":
                    observations.pop()
                elif mode == "duplicate":
                    observations[1] = observations[0]
                elif mode == "mutation":
                    object.__setattr__(observations[0], "canonical_fact_bytes", ())
                else:
                    object.__setattr__(observations[0], "_parent", object())
                with self.assertRaises(consumer.ProductFactConsumerError):
                    parent.reconcile(observations)
                self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)
                with self.assertRaises(consumer.ProductFactConsumerError):
                    parent.reconcile(observations)

    def test_owned_request_copy_cannot_mutate_authority(self):
        parent, _, _, _, _ = self._consumer()
        claimed = parent.claims()[0].claim()
        request = claimed.request_copy()
        request["projection"]["assigned_products"].clear()
        self.assertEqual(
            len(claimed.request_copy()["projection"]["assigned_products"]), 1
        )

    def test_changed_product_with_echoed_identity_is_rejected(self):
        parent, _, _, _, _ = self._consumer()
        claim = parent.claims()[0]
        request = claim.claim().request_copy()
        member = request["projection"]["assigned_products"][0]
        node = next(
            n
            for _, n in protocol.walk_product(member["product"])
            if n["node_type"] == "ClassDef"
        )
        node["fields"]["name"]["value"] = "Different"
        with self.assertRaises(protocol.ProductFactProtocolError):
            protocol.validate_request(request, launch_key=claim.binding.launch_key)

    def test_original_input_drift_prevents_consumer_admission(self):
        attempt, closure, _, eligibility = self._parse_world()
        inputs = attempt._inputs_ref()
        object.__setattr__(inputs, "policy_digest", "0" * 64)
        with self.assertRaises(
            (consumer.ProductFactConsumerError, parse._ParseFulfillmentError)
        ):
            consumer.create_product_fact_consumer(
                closure,
                derivation_id="changed",
                bindings=closed_test_multi_provider_bindings(),
            )
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_late_child_revocation_prevents_continuation(self):
        parent, _, eligibility, _, _ = self._consumer()
        claims = parent.claims()
        closed = parent.reconcile(self._execute(parent))
        claims[0]._eligibility_ref().revoke()
        with self.assertRaises(consumer.ProductFactConsumerError):
            closed.claim_continuation()
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_original_budget_stop_prevents_claim_and_late_continuation(self):
        parent, context, _, _, _ = self._consumer()
        claim = parent.claims()[0]
        context.request_cancellation()
        with self.assertRaises(consumer.ProductFactConsumerError):
            claim.claim()
        with self.assertRaises(consumer.ProductFactConsumerError):
            claim.claim()
        parent, context, _, _, _ = self._consumer()
        closed = parent.reconcile(self._execute(parent))
        continuation = closed.claim_continuation()
        context.request_cancellation()
        with self.assertRaises(consumer.ProductFactConsumerError):
            continuation._fact_set_copy()

    def test_claim_descriptor_mutation_is_consumed_and_rejected(self):
        parent, _, _, _, _ = self._consumer()
        claim = parent.claims()[0]
        object.__setattr__(claim.binding.descriptor, "provider_id", "foreign")
        with self.assertRaises(consumer.ProductFactConsumerError):
            claim.claim()
        with self.assertRaises(consumer.ProductFactConsumerError):
            claim.claim()

    def test_utf8_column_inside_multibyte_character_is_rejected(self):
        parent, _, _, _, _ = self._consumer()
        member = parent.claims()[0].projection_copy()["assigned_products"][0]
        product = member["product"]
        node = next(
            n for _, n in protocol.walk_product(product) if n["node_type"] == "ClassDef"
        )
        # Line 1: '# caf' then two-byte é; byte column 6 splits that character.
        node["attributes"]["lineno"]["value"] = 1
        node["attributes"]["col_offset"]["value"] = 6
        with self.assertRaises(UnicodeDecodeError):
            product_byte_anchors(product, BOM_SOURCE, encoding="UTF-8-SIG")

    def test_multiple_accepted_products_all_reach_every_provider(self):
        parent, _, _, _, _ = self._consumer(
            self._inputs([(b"a.py", b"class A: pass\n"), (b"b.py", b"class B: pass\n")])
        )
        self.assertTrue(
            all(
                len(c.projection_copy()["assigned_products"]) == 2
                for c in parent.claims()
            )
        )
        doc = parent.reconcile(self._execute(parent)).document_copy()
        self.assertEqual(len(doc["fact_set"]["facts"]), 4)

    def test_closure_and_continuation_transplants_are_rejected(self):
        first, _, _, _, _ = self._consumer()
        second, _, _, _, _ = self._consumer()
        closed1 = first.reconcile(self._execute(first))
        closed2 = second.reconcile(self._execute(second))
        continuation = closed1.claim_continuation()
        object.__setattr__(
            continuation, "_ClaimedProductFactContinuation__closure", closed2
        )
        with self.assertRaises(consumer.ProductFactConsumerError):
            continuation._fact_set_copy()
        object.__setattr__(closed2, "_OwnedProductFactClosure__parent", first)
        with self.assertRaises(consumer.ProductFactConsumerError):
            closed2.document_copy()

    def test_zero_reported_facts_is_not_zero_input_or_fulfillment(self):
        parent, _, _, _, _ = self._consumer()

        def empty(terminal, request):
            terminal["candidate_records"] = []

        doc = parent.reconcile(self._execute(parent, transform=empty)).document_copy()
        self.assertEqual(doc["consumer_status"], "COMPLETED")
        self.assertTrue(
            all(
                len(h["request"]["projection"]["assigned_products"]) == 1
                for h in doc["child_history"]
            )
        )
        self.assertEqual(doc["fact_set"]["facts"], [])
        self.assertNotIn("fulfillment", doc)

    def test_transport_limit_failure_consumes_claim_without_child(self):
        limits = ExecutionCellTransportSafetyLimits(
            request_payload_bytes=8, terminal_payload_bytes=1024
        )
        parent, _, _, _, _ = self._consumer(limits=limits)
        claim = parent.claims()[0]
        with mock.patch.object(consumer, "run_windows_execution_cell") as cell:
            observation = consumer.execute_product_fact_claim(claim)
        cell.assert_not_called()
        self.assertEqual(observation.lifecycle, "INFRASTRUCTURE_FAILED")
        with self.assertRaises(consumer.ProductFactConsumerError):
            claim.claim()

    @unittest.skipUnless(
        os.name == "nt" and os.environ.get("VERITRAIL_R1_REFERENCE_PYTHON"),
        "requires explicit reference runtime and Windows cell",
    )
    def test_real_reference_parse_and_two_product_only_workers(self):
        parent, context, eligibility, closure, _ = self._consumer(real=True)
        digest = closure.product_set().product_set_digest
        observations = tuple(
            consumer.execute_product_fact_claim(c) for c in parent.claims()
        )
        self.assertEqual(
            [o.lifecycle for o in observations], ["COMPLETED", "COMPLETED"]
        )
        doc = parent.reconcile(observations).document_copy()
        self.assertEqual(doc["product_set_digest"], digest)
        self.assertEqual(
            {f["fact_kind"] for f in doc["fact_set"]["facts"]},
            {"MODULE", "CLASS_DECLARATION"},
        )
        self.assertIs(context.state, BudgetState.RUNNING)
        self.assertIs(eligibility.state, AttemptEligibilityState.ADMITTED)


if __name__ == "__main__":
    unittest.main()
