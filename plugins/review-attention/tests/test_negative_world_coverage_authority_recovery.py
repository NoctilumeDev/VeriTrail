from __future__ import annotations

import copy
import json
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / "src", ROOT / "tests"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_fact_fulfillment as fact_tests  # noqa: E402
import test_fact_to_coverage_exact_input_handoff as carrier_tests  # noqa: E402
import test_language_support as language_tests  # noqa: E402
from veritrail_review import (  # noqa: E402
    _fact_to_coverage_exact_input_handoff as handoff,
)
from veritrail_review import (  # noqa: E402
    _negative_world_coverage_authority_recovery as recovery,
)
from veritrail_review._review_coverage_ledger_conformance import (  # noqa: E402
    LEDGER_DIGEST_DOMAIN,
    bind_coverage_ledger_conformance_source,
    validate_review_coverage_ledger,
)
from veritrail_review.canonical import semantic_digest  # noqa: E402


class NegativeWorldCoverageAuthorityRecoveryTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.helper = fact_tests.FactFulfillmentTests()
        self.carrier_helper = carrier_tests.FactToCoverageExactInputHandoffTests()

    def _carrier(self, inputs, *, kind="COMPLETED"):
        parent, context, eligibility, *_ = self.helper._world(inputs)
        observations = (
            self.helper._execute(parent, kind=kind) if parent.claims() else ()
        )
        closure = parent.reconcile(observations)
        return (
            handoff.claim_fact_to_coverage_exact_input_handoff(closure),
            context,
            eligibility,
        )

    def _attempt(self, inputs, *, kind="COMPLETED"):
        carrier, context, eligibility = self._carrier(inputs, kind=kind)
        return (
            recovery.claim_negative_world_coverage_attempt(carrier),
            carrier,
            context,
            eligibility,
        )

    def _policy_excluded_inputs(self):
        return language_tests.LanguageSupportPrivateClassifierTests()._inputs(
            [(b"pkg/a.py", b"print('hidden')\n", "100644", "REGULAR_BLOB")],
            dispositions={b"pkg/a.py": "OUT_OF_SCOPE"},
        )

    @staticmethod
    def _resign(candidate):
        unsigned = copy.deepcopy(candidate)
        unsigned.pop("coverage_ledger_digest")
        candidate["coverage_ledger_digest"] = semantic_digest(
            LEDGER_DIGEST_DOMAIN, unsigned
        )

    def _worlds(self):
        return (
            (
                "zero_parse_empty",
                self.carrier_helper._empty_inputs(),
                "COMPLETED",
                "ZERO_PARSE_DENOMINATOR",
                ("COMPLETE",) * 7,
                "COMPLETE",
            ),
            (
                "zero_parse_unsupported",
                self.helper._inputs([(b"a.txt", b"ignored")]),
                "COMPLETED",
                "ZERO_PARSE_DENOMINATOR",
                (
                    "COMPLETE",
                    "COMPLETE",
                    "PARTIAL",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                ),
                "PARTIAL",
            ),
            (
                "zero_parse_policy_excluded",
                self._policy_excluded_inputs(),
                "COMPLETED",
                "ZERO_PARSE_DENOMINATOR",
                (
                    "COMPLETE",
                    "PARTIAL",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                ),
                "PARTIAL",
            ),
            (
                "all_parse_rejected",
                self.helper._inputs([(b"a.py", b"def bad(:\n")]),
                "COMPLETED",
                "ALL_PARSE_REJECTED",
                (
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "PARTIAL",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                ),
                "PARTIAL",
            ),
            (
                "projection_blocked",
                self.helper._inputs(
                    [
                        (
                            b"a.py",
                            "class ｉｆ:\n    pass\ndef later():\n    pass\n".encode(),
                        )
                    ]
                ),
                "COMPLETED",
                "PROJECTION_BLOCKED",
                (
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "PARTIAL",
                    "UNKNOWN",
                    "UNKNOWN",
                ),
                "UNKNOWN",
            ),
            (
                "required_provider_failed",
                self.helper._inputs(),
                "PROVIDER_FAILED",
                "REQUIRED_PROVIDER_NON_SUCCESS",
                (
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "PARTIAL",
                    "UNKNOWN",
                    "UNKNOWN",
                ),
                "UNKNOWN",
            ),
            (
                "required_provider_unavailable",
                self.helper._inputs(),
                "PROVIDER_UNAVAILABLE",
                "REQUIRED_PROVIDER_NON_SUCCESS",
                (
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "COMPLETE",
                    "PARTIAL",
                    "UNKNOWN",
                    "UNKNOWN",
                ),
                "UNKNOWN",
            ),
        )

    def test_nwcr_001_006_seven_live_worlds_retain_exact_partitions(self):
        digests = {}
        for name, inputs, kind, branch, statuses, overall in self._worlds():
            with self.subTest(name=name):
                attempt, _, _, _ = self._attempt(inputs, kind=kind)
                candidate = recovery.produce_negative_world_coverage_candidate(
                    attempt
                )
                validation = (
                    recovery.independently_validate_negative_world_coverage_candidate(
                        attempt, candidate
                    )
                )
                admitted = recovery.admit_negative_world_coverage_candidate(
                    attempt, candidate, validation
                )
                document = admitted.coverage_ledger_document_copy()
                self.assertEqual(
                    document["root_bindings"][0]["terminal_branch"], branch
                )
                self.assertEqual(
                    tuple(value["coverage_status"] for value in document["stages"]),
                    statuses,
                )
                self.assertEqual(document["overall_coverage_status"], overall)
                self.assertEqual(
                    document["coverage_ledger_digest"],
                    semantic_digest(
                        LEDGER_DIGEST_DOMAIN,
                        {
                            key: value
                            for key, value in document.items()
                            if key != "coverage_ledger_digest"
                        },
                    ),
                )
                self.assertEqual(
                    admitted.authority_ceiling_copy(),
                    {
                        "private_negative_world_coverage_ledger": True,
                        "fact_set": False,
                        "relation_set": False,
                        "review_slice_set": False,
                        "positive_composition": False,
                        "manifest": False,
                        "evidence": False,
                        "persistence": False,
                        "public_review": False,
                    },
                )
                digests[name] = document["coverage_ledger_digest"]
        self.assertEqual(len(set(digests.values())), len(digests))
        self.assertEqual(
            len(
                {
                    digests["zero_parse_empty"],
                    digests["zero_parse_unsupported"],
                    digests["zero_parse_policy_excluded"],
                }
            ),
            3,
        )

    def test_nwcr_000_normal_world_is_rejected_without_public_expansion(self):
        carrier, *_ = self._carrier(self.helper._inputs())
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.claim_negative_world_coverage_attempt(carrier)
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.UNSUPPORTED_TERMINAL_BRANCH,
        )
        public_methods = [name for name in dir(carrier) if not name.startswith("_")]
        self.assertEqual(
            public_methods,
            [
                "derivation_profile_document_copy",
                "fact_terminal_source_copy",
                "input_identity_copy",
                "review_policy_document_copy",
                "source_snapshot_document_copy",
                "verified_blob_bytes_copy",
            ],
        )
        import veritrail_review

        self.assertFalse(
            hasattr(veritrail_review, "claim_negative_world_coverage_attempt")
        )

    def test_nwcr_002_003_common_mode_shrink_and_branch_rewrite_rejected(self):
        inputs = self.helper._inputs([(b"a.py", b"def bad(:\n")])
        attempt, *_ = self._attempt(inputs)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        changed = copy.deepcopy(candidate)
        parse = next(
            value for value in changed["stages"] if value["stage"] == "PARSE"
        )
        parse["denominator"]["item_refs"] = []
        parse["eligible"] = []
        parse["completed"] = []
        parse["parse_failed"] = []
        parse["reason_codes"] = []
        parse["coverage_status"] = "COMPLETE"
        changed["overall_coverage_status"] = "COMPLETE"
        unsigned = copy.deepcopy(changed)
        unsigned.pop("coverage_ledger_digest")
        changed["coverage_ledger_digest"] = semantic_digest(
            LEDGER_DIGEST_DOMAIN, unsigned
        )
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.independently_validate_negative_world_coverage_candidate(
                attempt, changed
            )
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.CANDIDATE_RECONCILIATION_REJECTED,
        )

        attempt, *_ = self._attempt(inputs)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        candidate["root_bindings"][0]["terminal_branch"] = (
            "ZERO_PARSE_DENOMINATOR"
        )
        unsigned = copy.deepcopy(candidate)
        unsigned.pop("coverage_ledger_digest")
        candidate["coverage_ledger_digest"] = semantic_digest(
            LEDGER_DIGEST_DOMAIN, unsigned
        )
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.independently_validate_negative_world_coverage_candidate(
                attempt, candidate
            )
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.CANDIDATE_RECONCILIATION_REJECTED,
        )

    def test_nwcr_004_009_fact_and_downstream_semantics_are_exact(self):
        inputs = self.helper._inputs(
            [(b"a.py", "class ｉｆ:\n    pass\ndef later():\n    pass\n".encode())]
        )
        attempt, *_ = self._attempt(inputs)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        fact_stage = candidate["stages"][4]
        self.assertTrue(fact_stage["blocked"])
        self.assertTrue(fact_stage["completed"])
        self.assertEqual(
            fact_stage["blocked"][0]["reason_codes"],
            ["UNREPRESENTABLE_EXPECTED_FACT"],
        )
        self.assertEqual(candidate["stages"][5]["coverage_status"], "UNKNOWN")
        self.assertEqual(candidate["stages"][6]["coverage_status"], "UNKNOWN")
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        recovery.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )

        for kind, reason in (
            ("PROVIDER_FAILED", "DERIVATION_ERROR"),
            ("PROVIDER_UNAVAILABLE", "PROVIDER_UNAVAILABLE"),
        ):
            attempt, *_ = self._attempt(self.helper._inputs(), kind=kind)
            candidate = recovery.produce_negative_world_coverage_candidate(attempt)
            fact_stage = candidate["stages"][4]
            self.assertTrue(fact_stage["execution_failed"])
            self.assertEqual(fact_stage["reason_codes"], [reason])
            self.assertFalse(fact_stage["completed"])

    def test_nwcr_004_009_candidate_semantic_rewrites_are_rejected(self):
        blocked_inputs = self.helper._inputs(
            [(b"a.py", "class ｉｆ:\n    pass\n".encode())]
        )
        mutations = []

        attempt, *_ = self._attempt(blocked_inputs)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        changed = copy.deepcopy(candidate)
        fact_stage = changed["stages"][4]
        fact_stage["denominator"]["item_refs"] = copy.deepcopy(
            fact_stage["completed"]
        )
        fact_stage["eligible"] = copy.deepcopy(fact_stage["completed"])
        fact_stage["blocked"] = []
        fact_stage["reason_codes"] = []
        fact_stage["coverage_status"] = "COMPLETE"
        self._resign(changed)
        mutations.append((attempt, changed, "shrunk Fact universe"))

        attempt, *_ = self._attempt(blocked_inputs)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        changed = copy.deepcopy(candidate)
        fact_stage = changed["stages"][4]
        blocked = fact_stage["blocked"].pop()
        blocked.pop("disposition_family")
        blocked["reason_codes"] = ["DERIVATION_ERROR"]
        fact_stage["execution_failed"] = [blocked]
        fact_stage["reason_codes"] = ["DERIVATION_ERROR"]
        self._resign(changed)
        mutations.append((attempt, changed, "semantic blocker relabeled as execution"))

        attempt, *_ = self._attempt(
            self.helper._inputs(), kind="PROVIDER_UNAVAILABLE"
        )
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        changed = copy.deepcopy(candidate)
        fact_stage = changed["stages"][4]
        for disposition in fact_stage["execution_failed"]:
            disposition["reason_codes"] = ["DERIVATION_ERROR"]
        fact_stage["reason_codes"] = ["DERIVATION_ERROR"]
        self._resign(changed)
        mutations.append((attempt, changed, "provider lifecycle reason collapsed"))

        attempt, *_ = self._attempt(
            self.helper._inputs(), kind="PROVIDER_FAILED"
        )
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        changed = copy.deepcopy(candidate)
        fact_stage = changed["stages"][4]
        fact_stage["completed"] = copy.deepcopy(fact_stage["eligible"])
        fact_stage["execution_failed"] = []
        fact_stage["reason_codes"] = []
        fact_stage["coverage_status"] = "COMPLETE"
        self._resign(changed)
        mutations.append((attempt, changed, "expected promoted without completion"))

        attempt, *_ = self._attempt(blocked_inputs)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        changed = copy.deepcopy(candidate)
        changed["root_bindings"][0]["artifact_digest"] = "0" * 64
        self._resign(changed)
        mutations.append((attempt, changed, "absent root replaced by artifact"))

        attempt, *_ = self._attempt(blocked_inputs)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        changed = copy.deepcopy(candidate)
        for stage in changed["stages"][5:]:
            stage["coverage_status"] = "COMPLETE"
        changed["overall_coverage_status"] = "PARTIAL"
        self._resign(changed)
        mutations.append((attempt, changed, "dependent unknown forced complete"))

        for attempt, changed, name in mutations:
            with self.subTest(name=name):
                with self.assertRaises(
                    recovery.NegativeWorldCoverageError
                ) as observed:
                    recovery.independently_validate_negative_world_coverage_candidate(
                        attempt, changed
                    )
                self.assertIs(
                    observed.exception.code,
                    recovery.NegativeWorldCoverageFailureCode.CANDIDATE_RECONCILIATION_REJECTED,
                )

    def test_nwcr_006_007_mixed_provider_history_preserves_completed_facts(self):
        parent, context, eligibility, *_ = self.helper._world(
            self.helper._inputs()
        )
        observations = []
        for index, claim in enumerate(parent.claims()):
            with patch.object(
                fact_tests.consumer,
                "run_windows_execution_cell",
                side_effect=self.helper._cell(
                    kind="PROVIDER_FAILED" if index == 0 else "COMPLETED"
                ),
            ):
                observations.append(
                    fact_tests.consumer.execute_product_fact_claim(claim)
                )
        closure = parent.reconcile(observations)
        self.assertIsNone(closure.document_copy()["fact_set"])
        carrier = handoff.claim_fact_to_coverage_exact_input_handoff(closure)
        attempt = recovery.claim_negative_world_coverage_attempt(carrier)
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        fact_stage = candidate["stages"][4]
        self.assertTrue(fact_stage["completed"])
        self.assertFalse(fact_stage["execution_failed"])
        history = {
            value["name"]: value["value"]
            for value in candidate["root_bindings"][0][
                "terminal_history_projection"
            ]["history"]
        }
        self.assertEqual(
            {value["state"] for value in history["provider_outcomes"]},
            {"FAILED", "COMPLETED"},
        )
        self.assertEqual(history["provider_responsibility"], [])
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        admitted = recovery.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )
        self.assertEqual(
            admitted.coverage_ledger_document_copy()["coverage_ledger_digest"],
            candidate["coverage_ledger_digest"],
        )
        self.assertEqual(eligibility.state.value, "REVOKED")

    def test_nwcr_010_fixture_conformance_has_no_live_admission_authority(self):
        corpus = json.loads(
            (
                ROOT.parents[1]
                / "tests"
                / "fixtures"
                / "review-coverage-ledger-0.3"
                / "compatibility-cases.json"
            ).read_text(encoding="utf-8")
        )
        fixture = next(
            value
            for value in corpus["positive_cases"]
            if value["case_id"] == "all_parse_rejected"
        )
        source = fixture["source"]
        bound = bind_coverage_ledger_conformance_source(
            fact_handoff_source_digest=source["fact_handoff_source_digest"],
            root_binding_projections=source["root_binding_projections"],
            stage_projections=source["stage_projections"],
            authority_safe=True,
        )
        validate_review_coverage_ledger(fixture["document"], bound)
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            recovery.NegativeWorldCoverageValidation(
                attempt=object(),  # type: ignore[arg-type]
                candidate_bytes=json.dumps(fixture["document"]).encode(),
                source_digest=source["fact_handoff_source_digest"],
                _token=object(),
            )

    def test_nwcr_011_producer_stage_projector_cannot_be_validator_oracle(self):
        inputs = self.helper._inputs([(b"a.py", b"def bad(:\n")])
        attempt, *_ = self._attempt(inputs)
        original_projector = recovery._producer_known_stage

        def omit_parse_denominator(stage, *args, **kwargs):
            projection = original_projector(stage, *args, **kwargs)
            if stage == "PARSE":
                projection["denominator"]["item_refs"] = []
                projection["eligible"] = []
                projection["parse_failed"] = []
                projection["reason_codes"] = []
                projection["coverage_status"] = "COMPLETE"
            return projection

        with patch.object(
            recovery,
            "_producer_known_stage",
            side_effect=omit_parse_denominator,
        ):
            candidate = recovery.produce_negative_world_coverage_candidate(attempt)
            with self.assertRaises(
                recovery.NegativeWorldCoverageError
            ) as observed:
                recovery.independently_validate_negative_world_coverage_candidate(
                    attempt, candidate
                )
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.CANDIDATE_RECONCILIATION_REJECTED,
        )

    def test_nwcr_012_013_carrier_and_admission_are_exactly_once(self):
        carrier, *_ = self._carrier(self.carrier_helper._empty_inputs())
        barrier = Barrier(2)

        def consume():
            barrier.wait()
            try:
                return recovery.claim_negative_world_coverage_attempt(carrier)
            except recovery.NegativeWorldCoverageError:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            attempts = list(pool.map(lambda _: consume(), range(2)))
        attempts = [value for value in attempts if value is not None]
        self.assertEqual(len(attempts), 1)
        attempt = attempts[0]
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        barrier = Barrier(2)

        def admit():
            barrier.wait()
            try:
                return recovery.admit_negative_world_coverage_candidate(
                    attempt, candidate, validation
                )
            except recovery.NegativeWorldCoverageError:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: admit(), range(2)))
        results = [value for value in results if value is not None]
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].coverage_ledger_document_copy()[
                "coverage_ledger_digest"
            ],
            candidate["coverage_ledger_digest"],
        )

    def test_nwcr_012_copy_equal_carrier_and_foreign_validation_reject(self):
        carrier, *_ = self._carrier(self.carrier_helper._empty_inputs())
        duplicate = copy.copy(carrier)
        attempt = recovery.claim_negative_world_coverage_attempt(carrier)
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.claim_negative_world_coverage_attempt(duplicate)
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_ALREADY_CONSUMED,
        )

        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        foreign_attempt, *_ = self._attempt(
            self.carrier_helper._empty_inputs()
        )
        foreign_candidate = recovery.produce_negative_world_coverage_candidate(
            foreign_attempt
        )
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.admit_negative_world_coverage_candidate(
                foreign_attempt, foreign_candidate, validation
            )
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED,
        )

    def test_nwcr_012_attempt_validation_and_result_are_not_copyable(self):
        attempt, *_ = self._attempt(self.carrier_helper._empty_inputs())
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            copy.copy(attempt)
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            copy.deepcopy(attempt)

        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            copy.copy(validation)
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            copy.deepcopy(validation)

        admitted = recovery.admit_negative_world_coverage_candidate(
            attempt, candidate, validation
        )
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            copy.copy(admitted)
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            copy.deepcopy(admitted)

    def test_nwcr_014_post_validation_mutation_and_late_stop_revoke(self):
        attempt, _, _, eligibility = self._attempt(
            self.carrier_helper._empty_inputs()
        )
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        candidate["overall_coverage_status"] = "PARTIAL"
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            recovery.admit_negative_world_coverage_candidate(
                attempt, candidate, validation
            )
        self.assertEqual(eligibility.state.value, "REVOKED")

        attempt, _, context, eligibility = self._attempt(
            self.carrier_helper._empty_inputs()
        )
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        context.request_cancellation()
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            recovery.admit_negative_world_coverage_candidate(
                attempt, candidate, validation
            )
        self.assertEqual(eligibility.state.value, "REVOKED")

    def test_nwcr_016_closest_identities_fail_closed(self):
        carrier, *_ = self._carrier(self.carrier_helper._empty_inputs())
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            recovery.claim_negative_world_coverage_attempt(
                carrier, input_consumer=recovery.INPUT_CONSUMER + "-closest"
            )
        attempt = recovery.claim_negative_world_coverage_attempt(carrier)
        with self.assertRaises(recovery.NegativeWorldCoverageError):
            recovery.produce_negative_world_coverage_candidate(
                attempt,
                composition_function=recovery.COMPOSITION_FUNCTION + "-closest",
            )

    def test_private_failure_families_are_reachable_and_non_interchangeable(self):
        carrier, context, *_ = self._carrier(self.carrier_helper._empty_inputs())
        context.request_cancellation()
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.claim_negative_world_coverage_attempt(carrier)
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_REJECTED,
        )

        carrier, *_ = self._carrier(self.carrier_helper._empty_inputs())
        recovery.claim_negative_world_coverage_attempt(carrier)
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.claim_negative_world_coverage_attempt(carrier)
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.NEGATIVE_INPUT_ALREADY_CONSUMED,
        )

        attempt, *_ = self._attempt(self.carrier_helper._empty_inputs())
        with patch.object(
            recovery, "_producer_fact_partition", side_effect=ValueError
        ):
            with self.assertRaises(
                recovery.NegativeWorldCoverageError
            ) as observed:
                recovery.produce_negative_world_coverage_candidate(attempt)
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.FACT_OBLIGATION_BINDING_REJECTED,
        )

        attempt, *_ = self._attempt(self.carrier_helper._empty_inputs())
        with patch.object(
            recovery, "_producer_materialize_root_chain", side_effect=ValueError
        ):
            with self.assertRaises(
                recovery.NegativeWorldCoverageError
            ) as observed:
                recovery.produce_negative_world_coverage_candidate(attempt)
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.ROOT_PROJECTION_REJECTED,
        )

        attempt, *_ = self._attempt(self.carrier_helper._empty_inputs())
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.independently_validate_negative_world_coverage_candidate(
                attempt,
                candidate,
                validation_function=recovery.VALIDATION_FUNCTION + "-closest",
            )
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.INDEPENDENT_VALIDATION_REJECTED,
        )

        attempt, *_ = self._attempt(self.carrier_helper._empty_inputs())
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.admit_negative_world_coverage_candidate(
                attempt,
                candidate,
                validation,
                admission_function=recovery.ADMISSION_FUNCTION + "-closest",
            )
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED,
        )

        attempt, *_ = self._attempt(self.carrier_helper._empty_inputs())
        candidate = recovery.produce_negative_world_coverage_candidate(attempt)
        validation = recovery.independently_validate_negative_world_coverage_candidate(
            attempt, candidate
        )
        candidate["overall_coverage_status"] = "PARTIAL"
        with self.assertRaises(recovery.NegativeWorldCoverageError) as observed:
            recovery.admit_negative_world_coverage_candidate(
                attempt, candidate, validation
            )
        self.assertIs(
            observed.exception.code,
            recovery.NegativeWorldCoverageFailureCode.SAME_ATTEMPT_ADMISSION_REJECTED,
        )


if __name__ == "__main__":
    unittest.main()
