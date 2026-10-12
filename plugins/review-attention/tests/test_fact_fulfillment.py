from __future__ import annotations

import ast
import copy
import hashlib
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

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_parse_product_fact_consumer as old_tests
import test_parse_fulfillment as parse_tests
from veritrail_review import _fact_fulfillment as consumer
from veritrail_review import _fact_fulfillment_protocol as protocol
from veritrail_review import _fact_fulfillment_projection as projection
from veritrail_review import _parse_fulfillment as parse
from veritrail_review import _parse_fulfillment_worker as parser_worker
from veritrail_review import _parse_product_fact_consumer as old_consumer
from veritrail_review import _parse_product_fact_protocol as old_protocol
from veritrail_review._fact_fulfillment_binding import closed_fact_bindings
from veritrail_review._fact_fulfillment_ast import FIELDS
from veritrail_review._execution_cell_protocol import (
    AttemptEligibility,
    AttemptEligibilityState,
    encode_frame,
    read_frame,
)
from veritrail_review._language_support import classify_language_support
from veritrail_review._windows_execution_cell import CellReleaseError
from veritrail_review.budget import BudgetState
from veritrail_review.canonical import canonical_json_bytes
from veritrail_review.derivation_input_contracts import DerivationInputSet
from test_execution_cell import _seal_policy, _canonical_artifact

GOLD_SOURCE = b"""import os, pkg.mod as alias
from ..base import x, y as z
from . import *
class C:
    def m(self):
        def inner():
            pass
        return inner
    async def am(self):
        pass
    if flag:
        def conditional():
            pass
def top():
    class N:
        pass
    return N
async def atop():
    pass
"""

# Independent hand-written gold: it does not call the projection or worker walk.
GOLD_DECLARATIONS = {
    ("CLASS_DECLARATION", "C", None),
    ("CLASS_DECLARATION", "N", None),
    ("METHOD_DECLARATION", "m", "SYNC"),
    ("METHOD_DECLARATION", "am", "ASYNC"),
    ("FUNCTION_DECLARATION", "inner", "SYNC"),
    ("FUNCTION_DECLARATION", "conditional", "SYNC"),
    ("FUNCTION_DECLARATION", "top", "SYNC"),
    ("FUNCTION_DECLARATION", "atop", "ASYNC"),
}
GOLD_IMPORTS = [
    ("IMPORT", 0, ("os",), None, None, 0),
    ("IMPORT", 0, ("pkg", "mod"), None, "alias", 1),
    ("FROM_IMPORT", 2, ("base",), "x", None, 0),
    ("FROM_IMPORT", 2, ("base",), "y", "z", 1),
    ("FROM_IMPORT", 1, (), "*", None, 0),
]


def fixture_terminal(source):
    """Mock fixture only. Actual reference execution is tested separately."""
    tree = ast.parse(source, feature_version=(3, 10), type_comments=False)
    product = parser_worker._tree_value(tree)

    # The host 3.13 adds empty type_params; strip this in the mock fixture before
    # Parse admission, never in the product runtime or the U/E validator.
    def frozen(value):
        if value["value_kind"] == "AST":
            fields = value["fields"]
            for extra in set(fields) - set(FIELDS[value["node_type"]]):
                if extra != "type_params" or fields[extra] != {
                    "value_kind": "LIST",
                    "items": [],
                }:
                    raise ValueError("fixture is not a 3.10 world")
                del fields[extra]
            for group in ("fields", "attributes"):
                for item in value[group].values():
                    frozen(item)
        elif value["value_kind"] == "LIST":
            for item in value["items"]:
                frozen(item)

    frozen(product)
    result = parse_tests.ParseFulfillmentPrivateImplementationTests._rejected_terminal()
    result["semantic_result"] = {
        "disposition": "ACCEPTED",
        "reason_codes": [],
        "product": product,
    }
    return result


class FactFulfillmentTests(unittest.TestCase):
    maxDiff = None

    def _inputs(self, bodies=None, *, advisory=False, mapping=None):
        value = old_tests.ProductFactConsumerTests()._inputs(
            [(b"pkg/a.py", GOLD_SOURCE)] if bodies is None else bodies,
            advisory=advisory,
        )
        if mapping is None:
            return value
        policy = value.review_policy_document_copy()
        policy["python_module_mapping"] = mapping
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=value.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=value.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=value.verified_blob_bytes_by_object_identity,
            source_snapshot_digest=value.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=value.derivation_profile_digest,
        )

    def _world(self, inputs=None, *, advisory=False, real=False):
        helper = old_tests.ProductFactConsumerTests()
        inputs = self._inputs(advisory=advisory) if inputs is None else inputs
        with mock.patch.object(
            old_tests.ParseHelper,
            "_accepted_terminal_for_source",
            side_effect=fixture_terminal,
        ):
            attempt, closure, context, eligibility = helper._parse_world(
                inputs, real=real
            )
        parent = consumer.create_product_fact_consumer(
            closure,
            derivation_id="fact-fulfillment-world",
            bindings=closed_fact_bindings(include_advisory=advisory),
        )
        return parent, context, eligibility, closure, attempt

    @staticmethod
    def _cell(transform=None, *, kind="COMPLETED", lifecycle=None):
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
            if transform:
                transform(terminal, request)
            result = old_tests.ParseHelper._cell(terminal)(
                context, eligibility, **kwargs
            )
            return result if lifecycle is None else replace(result, **lifecycle)

        return run

    def _execute(self, parent, **kwargs):
        with mock.patch.object(
            consumer, "run_windows_execution_cell", side_effect=self._cell(**kwargs)
        ):
            return tuple(
                consumer.execute_product_fact_claim(c) for c in parent.claims()
            )

    def test_fpfct_001_mapping_is_semantic_input_not_path_only(self):
        original = self._inputs()
        a, *_ = self._world(original)
        changed = self._inputs(
            mapping={
                "module_root": {"path_kind": "REPOSITORY_ROOT"},
                "package_prefix": ["different"],
            }
        )
        b, *_ = self._world(changed)
        self.assertEqual(
            a.qualification_copy()["universe"], b.qualification_copy()["universe"]
        )
        self.assertNotEqual(
            a.qualification_copy()["expected"], b.qualification_copy()["expected"]
        )
        self.assertNotEqual(
            a.claims()[0].projection_copy(), b.claims()[0].projection_copy()
        )

    def test_fpfct_002_exact_inputs_cannot_change_after_parse(self):
        p, _, eligible, _, attempt = self._world()
        object.__setattr__(attempt._inputs_ref(), "policy_digest", "0" * 64)
        with self.assertRaises(consumer.ProductFactConsumerError):
            p.claims()
        self.assertIs(eligible.state, AttemptEligibilityState.REVOKED)

    def test_fpfct_003_004_005_independent_five_kind_gold(self):
        p, *_ = self._world()
        q = p.qualification_copy()
        self.assertEqual(len(q["universe"]), 14)
        facts = q["expected"]
        self.assertEqual(
            {
                (
                    f["fact_kind"],
                    f["semantic_attributes"]["declared_name"],
                    f["semantic_attributes"].get("function_form"),
                )
                for f in facts
                if f["fact_kind"]
                in {"CLASS_DECLARATION", "METHOD_DECLARATION", "FUNCTION_DECLARATION"}
            },
            GOLD_DECLARATIONS,
        )
        self.assertCountEqual(
            [
                (
                    a["import_form"],
                    a["relative_level"],
                    tuple(a["module_parts"]),
                    a["imported_name"],
                    a["alias_name"],
                    f["local_ordinal"],
                )
                for f in facts
                if f["fact_kind"] == "IMPORT_DECLARATION"
                for a in [f["semantic_attributes"]]
            ],
            GOLD_IMPORTS,
        )
        closure = p.reconcile(self._execute(p))
        self.assertEqual(len(closure.document_copy()["fact_set"]["facts"]), 14)

    def test_fpfct_006_empty_source_still_has_module(self):
        p, *_ = self._world(self._inputs([(b"empty.py", b"")]))
        self.assertEqual(len(p.qualification_copy()["universe"]), 1)
        self.assertEqual(p.qualification_copy()["expected"][0]["fact_kind"], "MODULE")
        observations = self._execute(
            p,
            transform=lambda t, r: t.update(candidate_records=[], reported_fact_ids=[]),
        )
        self.assertEqual([o.lifecycle for o in observations], ["FAILED", "FAILED"])
        self.assertIsNone(p.reconcile(observations).document_copy()["fact_set"])

    def test_fpfct_007_exact_bom_crlf_cr_unicode_decorator_anchors(self):
        raw = b'\xef\xbb\xbf# caf\xc3\xa9\r\n@decorate\r\nclass C:\r\n    pass\r\ndef f():\r    return "\xc3\xa9"\r'
        p, *_ = self._world(self._inputs([(b"a.py", raw)]))
        facts = p.qualification_copy()["expected"]
        by_kind = {f["fact_kind"]: f for f in facts}
        self.assertEqual(by_kind["MODULE"]["source_anchor"]["end_byte"], len(raw))
        for kind, start, end in [
            (
                "CLASS_DECLARATION",
                raw.index(b"class C:"),
                raw.index(b"    pass") + len(b"    pass"),
            ),
            (
                "FUNCTION_DECLARATION",
                raw.index(b"def f():"),
                raw.index(b"    return") + len(b'    return "\xc3\xa9"'),
            ),
        ]:
            anchor = by_kind[kind]["source_anchor"]
            self.assertEqual((anchor["start_byte"], anchor["end_byte"]), (start, end))

    def test_fpfct_008_unrepresentable_has_full_u_and_no_children(self):
        p, *_ = self._world(
            self._inputs(
                [(b"a.py", "class ｉｆ:\n    pass\ndef later():\n    pass\n".encode())]
            )
        )
        q = p.qualification_copy()
        self.assertEqual(q["status"], "BLOCKED_UNREPRESENTABLE")
        self.assertEqual(len(q["universe"]), 3)
        self.assertEqual(len(q["blockers"]), 1)
        self.assertEqual(p.claims(), ())
        closed = p.reconcile(())
        self.assertIsNone(closed.document_copy()["fact_set"])
        with self.assertRaises(consumer.ProductFactConsumerError):
            closed.claim_continuation()

    def test_fpfct_009_absence_and_all_fields_under_control_nodes(self):
        raw = b"if flag:\n    class C:\n        pass\ntry:\n    import os\nexcept Exception:\n    def f():\n        pass\n"
        p, *_ = self._world(self._inputs([(b"a.py", raw)]))
        self.assertEqual(
            {f["fact_kind"] for f in p.qualification_copy()["expected"]},
            {
                "MODULE",
                "CLASS_DECLARATION",
                "FUNCTION_DECLARATION",
                "IMPORT_DECLARATION",
            },
        )

    def test_fpfct_010_module_collision_keeps_both_subjects(self):
        p, *_ = self._world(
            self._inputs([(b"A.py", b"pass\n"), ("Ａ.py".encode(), b"pass\n")])
        )
        q = p.qualification_copy()
        self.assertEqual(len(q["universe"]), 2)
        self.assertEqual(len(q["mapping_collisions"]), 1)
        self.assertNotEqual(*[f["subject_key_digest"] for f in q["expected"]])

    def test_fpfct_011_raw_init_and_nullable_mapping(self):
        p, *_ = self._world(
            self._inputs(
                [
                    (b"pkg/__init__.py", b"pass\n"),
                    ("pkg/__ｉｎｉｔ__.py".encode(), b"pass\n"),
                    (b"bad-name.py", b"pass\n"),
                ],
                mapping={
                    "module_root": {"path_kind": "REPOSITORY_ROOT"},
                    "package_prefix": [],
                },
            )
        )
        q = p.qualification_copy()
        mappings = {
            f["source_anchor"]["git_path"]["git_path_hex"]: f["semantic_attributes"][
                "module_key_parts"
            ]
            for f in q["expected"]
        }
        self.assertEqual(mappings[b"pkg/__init__.py".hex()], ["pkg"])
        self.assertEqual(
            mappings["pkg/__ｉｎｉｔ__.py".encode().hex()], ["pkg", "__init__"]
        )
        self.assertIsNone(mappings[b"bad-name.py".hex()])
        self.assertEqual(len(q["mapping_limitations"]), 1)

    def test_fpfct_012_unknown_or_missing_product_position_blocks(self):
        p, *_ = self._world()
        value = p.claims()[0].projection_copy()
        value["assigned_products"][0]["product"]["fields"]["body"]["items"][0][
            "node_type"
        ] = "ForeignNode"
        with self.assertRaises(ValueError):
            projection.qualify(value)
        value = p.claims()[0].projection_copy()
        value["assigned_products"][0]["node_anchors"].pop(
            next(iter(value["assigned_products"][0]["node_anchors"]))
        )
        with self.assertRaises(ValueError):
            protocol.validate_projection(value)

    def test_fpfct_013_common_omission_is_detected_by_independent_gold(self):
        p, *_ = self._world()
        original = projection.slots

        def mutated(member):
            return (v for v in original(member) if v[2] != "IMPORT_DECLARATION")

        with mock.patch.object(projection, "slots", side_effect=mutated):
            corrupted = projection.qualify(p.claims()[0].projection_copy())
        self.assertNotEqual(len(corrupted["universe"]), 14)
        self.assertNotEqual(
            {f["fact_kind"] for f in corrupted["expected"]},
            {f["fact_kind"] for f in p.qualification_copy()["expected"]},
        )
        worker_records = protocol.product_candidate_records

        def worker_omission(request):
            return [
                r
                for r in worker_records(request)
                if r["candidate"]["fact_kind"] != "IMPORT_DECLARATION"
            ]

        # A common-mode mutant can look internally consistent. Its apparent
        # success must be killed by the independent, prewritten 14-slot gold.
        with (
            mock.patch.object(projection, "slots", side_effect=mutated),
            mock.patch.object(
                protocol, "product_candidate_records", side_effect=worker_omission
            ),
        ):
            mutant, *_ = self._world()
            closed = mutant.reconcile(self._execute(mutant))
            self.assertEqual(closed.document_copy()["consumer_status"], "COMPLETED")
            with self.assertRaises(AssertionError):
                self.assertEqual(len(closed.document_copy()["fact_set"]["facts"]), 14)

    def test_fpfct_014_two_partial_required_sources_never_repair_each_other(self):
        p, *_ = self._world()

        def half(t, r):
            rows = t["candidate_records"]
            t["candidate_records"] = (
                rows[: len(rows) // 2]
                if r["projection"]["provider_descriptor"]["provider_id"].endswith("-a")
                else rows[len(rows) // 2 :]
            )
            t["reported_fact_ids"] = protocol.reported_ids(r, t["candidate_records"])

        observations = self._execute(p, transform=half)
        self.assertEqual([o.lifecycle for o in observations], ["FAILED", "FAILED"])
        self.assertIsNone(p.reconcile(observations).document_copy()["fact_set"])

    def test_fpfct_015_partial_wrong_content_extra_and_alias_rejected(self):
        transforms = [
            lambda t, r: t["candidate_records"].pop(),
            lambda t, r: t["candidate_records"][0]["candidate"][
                "semantic_attributes"
            ].update(module_key_parts=["wrong"]),
            lambda t, r: t["candidate_records"][0].update(node_path="$/foreign"),
            lambda t, r: t["candidate_records"][1].update(alias_ordinal=True),
        ]
        for mutate in transforms:
            with self.subTest(mutate=transforms.index(mutate)):
                p, *_ = self._world()
                self.assertEqual(
                    [o.lifecycle for o in self._execute(p, transform=mutate)],
                    ["FAILED", "FAILED"],
                )

    def test_fpfct_016_identical_duplicate_ok_incompatible_and_terminal_duplicate_block(
        self,
    ):
        p, *_ = self._world()

        def duplicate(t, r):
            t["candidate_records"].append(copy.deepcopy(t["candidate_records"][0]))

        self.assertEqual(
            p.reconcile(self._execute(p, transform=duplicate)).document_copy()[
                "consumer_status"
            ],
            "COMPLETED",
        )
        p, *_ = self._world()

        def incompatible(t, r):
            duplicate(t, r)
            t["candidate_records"][-1]["candidate"]["semantic_attributes"][
                "module_key_parts"
            ] = ["wrong"]

        self.assertEqual(
            [o.lifecycle for o in self._execute(p, transform=incompatible)],
            ["FAILED", "FAILED"],
        )
        p, *_ = self._world()
        observations = self._execute(p)
        with self.assertRaises(consumer.ProductFactConsumerError):
            p.reconcile([observations[0], observations[0]])
        p, *_ = self._world()

        def duplicate_frame(context, eligibility, **kwargs):
            result = self._cell()(context, eligibility, **kwargs)
            return replace(result, terminal_bytes=result.terminal_bytes * 2)

        with mock.patch.object(
            consumer, "run_windows_execution_cell", side_effect=duplicate_frame
        ):
            observations = tuple(
                consumer.execute_product_fact_claim(c) for c in p.claims()
            )
        self.assertEqual([o.lifecycle for o in observations], ["FAILED", "FAILED"])

    def test_fpfct_017_optional_failure_is_retained_not_all_complete(self):
        p, *_ = self._world(advisory=True)
        claims = p.claims()
        observations = []
        for c in claims:
            optional = c.binding.descriptor.capability_id.endswith("advisory")
            with mock.patch.object(
                consumer,
                "run_windows_execution_cell",
                side_effect=self._cell(
                    kind="PROVIDER_FAILED" if optional else "COMPLETED"
                ),
            ):
                observations.append(consumer.execute_product_fact_claim(c))
        closed = p.reconcile(observations)
        self.assertEqual(closed.document_copy()["consumer_status"], "COMPLETED")
        self.assertEqual(
            [h["lifecycle"] for h in closed.document_copy()["child_history"]],
            ["COMPLETED", "COMPLETED", "FAILED"],
        )
        self.assertTrue(
            all(
                len(f["provenance_refs"]) == 2
                for f in closed.document_copy()["fact_set"]["facts"]
            )
        )

    def test_fpfct_018_serial_launch_keeps_later_children_after_required_failure(self):
        p, *_ = self._world()
        cells = [self._cell(kind="PROVIDER_FAILED"), self._cell()]
        count = []

        def run(*args, **kwargs):
            call = cells[len(count)]
            count.append(1)
            return call(*args, **kwargs)

        with mock.patch.object(consumer, "run_windows_execution_cell", side_effect=run):
            closed = consumer.execute_fact_fulfillment(p)
        self.assertEqual(len(count), 2)
        self.assertIsNone(closed.document_copy()["fact_set"])
        self.assertEqual(
            [h["lifecycle"] for h in closed.document_copy()["child_history"]],
            ["FAILED", "COMPLETED"],
        )

    def test_fpfct_019_worker_input_has_no_raw_source_or_expected_answers(self):
        p, *_ = self._world()
        raw = canonical_json_bytes(p.claims()[0].projection_copy())
        for key in (
            "expected",
            "universe",
            "source_text",
            "source_blobs",
            "repository",
            "raw_body",
        ):
            self.assertNotIn(('"' + key + '"').encode(), raw)
        worker_source = (
            ROOT / "src/veritrail_review/_fact_fulfillment_worker.py"
        ).read_text()
        self.assertNotIn("ast.parse", worker_source)
        self.assertNotIn("qualify(", worker_source)
        p, *_ = self._world()
        observations = self._execute(
            p,
            transform=lambda t, r: t["candidate_records"][0].update(
                product_semantic_digest="0" * 64
            ),
        )
        self.assertEqual([o.lifecycle for o in observations], ["FAILED", "FAILED"])

    def test_fpfct_020_equal_limits_and_foreign_attempt_are_not_authority(self):
        p, _, eligibility, *_ = self._world()
        object.__setattr__(
            p, "_OwnedProductFactConsumer__context", old_tests.ParseHelper._context()
        )
        with self.assertRaises(consumer.ProductFactConsumerError):
            p.claims()
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)
        inputs = self._inputs()
        a, *_ = self._world(inputs)
        b, *_ = self._world(inputs)
        observations = self._execute(a)
        self._execute(b)
        with self.assertRaises(consumer.ProductFactConsumerError):
            b.reconcile(observations)

    def test_fpfct_021_zero_denominator_all_rejected_and_missing_are_distinct(self):
        partitions = []
        for bodies in ([(b"a.txt", b"ignored")], [(b"a.py", b"def bad(:\n")]):
            p, *_ = self._world(self._inputs(bodies))
            self.assertEqual(p.claims(), ())
            closed = p.reconcile(())
            partitions.append(closed.document_copy()["parse_partition"])
            self.assertIsNone(closed.document_copy()["fact_set"])
        self.assertNotEqual(partitions[0], partitions[1])
        p, *_ = self._world()
        with self.assertRaises(consumer.ProductFactConsumerError):
            p.reconcile(())

    def test_fpfct_022_any_source_unsafe_release_cannot_be_optional_gap(self):
        for field in (
            "active_process_zero",
            "handles_released",
            "channel_threads_released",
        ):
            with self.subTest(field=field):
                p, *_ = self._world(advisory=True)
                observed = []
                for c in p.claims():
                    with mock.patch.object(
                        consumer,
                        "run_windows_execution_cell",
                        side_effect=self._cell(
                            lifecycle=(
                                {field: False}
                                if c.binding.descriptor.capability_id.endswith(
                                    "advisory"
                                )
                                else None
                            )
                        ),
                    ):
                        observed.append(consumer.execute_product_fact_claim(c))
                self.assertEqual(observed[-1].lifecycle, "RELEASE_FAILED")
                with self.assertRaises(consumer.ProductFactConsumerError):
                    p.reconcile(observed)
                self.assertEqual(p.retained_observations(), tuple(observed))

    def test_fpfct_022_cancellation_memory_deadline_block_same_continuation(self):
        for trigger in ("cancel", "memory", "deadline"):
            with self.subTest(trigger=trigger):
                p, context, *_ = self._world()
                closed = p.reconcile(self._execute(p))
                if trigger == "cancel":
                    context.request_cancellation()
                    # An accidentally revived state cannot erase the original latch.
                    object.__setattr__(context, "_state", BudgetState.RUNNING)
                elif trigger == "memory":
                    context._observe_owned_memory_limit()
                else:
                    object.__setattr__(
                        context, "_execution_deadline", context.started_at_monotonic
                    )
                with self.assertRaises(consumer.ProductFactConsumerError):
                    closed.claim_continuation()

    def test_fpfct_023_full_bytes_not_ids_and_bidirectional_provenance(self):
        mutations = [
            lambda t, r: t.update(reported_fact_ids=t["reported_fact_ids"][:-1]),
            lambda t, r: t.update(
                reported_fact_ids=t["reported_fact_ids"] + ["0" * 64]
            ),
            lambda t, r: t["candidate_records"][0].update(provider_run_id="0" * 64),
        ]
        for mutate in mutations:
            p, *_ = self._world()
            self.assertEqual(
                [o.lifecycle for o in self._execute(p, transform=mutate)],
                ["FAILED", "FAILED"],
            )

    def test_fpfct_024_old_request_binding_and_observation_rejected(self):
        p, *_ = self._world()
        request = p.claims()[0].claim().request_copy()
        request["protocol"] = old_protocol.PROTOCOL
        with self.assertRaises(protocol.ProductFactProtocolError):
            protocol.validate_request(request, launch_key="fulfill-a")
        inputs = self._inputs([(b"bad-name.py", b"pass\n")])
        with mock.patch.object(
            old_tests.ParseHelper,
            "_accepted_terminal_for_source",
            side_effect=fixture_terminal,
        ):
            old, *_ = old_tests.ProductFactConsumerTests()._consumer(inputs)
        history = old_tests.ProductFactConsumerTests()._execute(old)
        new, *_ = self._world(inputs)
        fresh_history = self._execute(new)

        def semantic(observation):
            return [
                {k: v for k, v in json.loads(raw).items() if k != "provenance_refs"}
                for raw in observation.canonical_fact_bytes
            ]

        self.assertEqual(semantic(history[0]), semantic(fresh_history[0]))
        with self.assertRaises(consumer.ProductFactConsumerError):
            new.reconcile(history)
        _, closure, _, eligibility = old_tests.ProductFactConsumerTests()._parse_world(
            self._inputs([(b"a.py", b"pass\n")])
        )
        from veritrail_review._multi_provider_applicability import (
            closed_test_multi_provider_bindings,
        )

        with self.assertRaises(consumer.ProductFactConsumerError):
            consumer.create_product_fact_consumer(
                closure,
                derivation_id="foreign-descriptor",
                bindings=closed_test_multi_provider_bindings(),
            )
        self.assertIs(eligibility.state, AttemptEligibilityState.REVOKED)

    def test_observations_survive_later_child_exception_and_preclaim_stop(self):
        p, *_ = self._world()
        calls = []

        def child(*args, **kwargs):
            calls.append(1)
            if len(calls) == 2:
                raise RuntimeError("unexpected cell failure; release unknown")
            return self._cell()(*args, **kwargs)

        with mock.patch.object(
            consumer, "run_windows_execution_cell", side_effect=child
        ):
            with self.assertRaises(consumer.ProductFactConsumerError):
                consumer.execute_fact_fulfillment(p)
        history = p.retained_observations()
        self.assertEqual(
            [o.lifecycle for o in history], ["COMPLETED", "RELEASE_FAILED"]
        )
        self.assertEqual(
            json.loads(history[-1].execution_bytes)["release_known"], False
        )
        self.assertEqual(p.reconciliation_observations(), history)
        p, context, *_ = self._world()
        claims = p.claims()
        with mock.patch.object(
            consumer, "run_windows_execution_cell", side_effect=self._cell()
        ):
            first = consumer.execute_product_fact_claim(claims[0])
        self.assertEqual(p.retained_observations(), (first,))
        context.request_cancellation()
        with self.assertRaises(consumer.ProductFactConsumerError):
            consumer.execute_product_fact_claim(claims[1])
        self.assertEqual(p.retained_observations(), (first,))

    def test_outside_root_and_invalid_utf8_path_keep_nullable_module(self):
        inputs = self._inputs(
            [(b"outside.py", b"pass\n"), (b"pkg/\xff.py", b"pass\n")],
            mapping={
                "module_root": {"path_kind": "GIT_PATH", "git_path_hex": b"pkg".hex()},
                "package_prefix": [],
            },
        )
        p, *_ = self._world(inputs)
        q = p.qualification_copy()
        self.assertEqual(len(q["universe"]), 2)
        self.assertEqual(len(q["mapping_limitations"]), 2)
        self.assertTrue(
            all(
                f["semantic_attributes"]["module_key_parts"] is None
                for f in q["expected"]
            )
        )
        self.assertEqual(
            p.reconcile(self._execute(p)).document_copy()["consumer_status"],
            "COMPLETED",
        )

    def test_claim_and_continuation_are_single_use_and_copy_owned(self):
        p, *_ = self._world()
        claim = p.claims()[0]
        barrier = Barrier(2)

        def use(_):
            barrier.wait()
            try:
                return claim.claim()
            except consumer.ProductFactConsumerError:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(v is not None for v in pool.map(use, range(2))), 1)
        p, context, *_ = self._world()
        closed = p.reconcile(self._execute(p))
        continuation = closed.claim_continuation()
        original = continuation._fact_set_copy()
        original["facts"].clear()
        self.assertEqual(len(continuation._fact_set_copy()["facts"]), 14)
        self.assertIs(continuation._context_ref(), context)
        with self.assertRaises(consumer.ProductFactConsumerError):
            closed.claim_continuation()

    def test_false_start_or_callback_cannot_admit_fact_results(self):
        for field in (
            "process_created_suspended",
            "process_assigned_before_resume",
            "process_resumed",
            "admitted",
        ):
            p, *_ = self._world()
            self.assertEqual(
                [o.lifecycle for o in self._execute(p, lifecycle={field: False})],
                ["INFRASTRUCTURE_FAILED"] * 2,
            )

    @unittest.skipUnless(
        os.name == "nt"
        and Path(os.environ.get("VERITRAIL_R1_REFERENCE_PYTHON", "")).is_file(),
        "explicit reference runtime/Windows required",
    )
    def test_actual_reference_parse_and_bounded_fact_children(self):
        p, context, *_ = self._world(real=True)
        closed = consumer.execute_fact_fulfillment(p)
        self.assertEqual(closed.document_copy()["consumer_status"], "COMPLETED")
        self.assertEqual(len(closed.document_copy()["fact_set"]["facts"]), 14)
        self.assertEqual(len(p.retained_observations()), 2)
        for observed in p.retained_observations():
            receipt = json.loads(observed.execution_bytes)
            self.assertTrue(receipt["process_assigned_before_resume"])
            self.assertTrue(receipt["active_process_zero"])
        self.assertIs(closed.claim_continuation()._context_ref(), context)


if __name__ == "__main__":
    unittest.main()
