from __future__ import annotations

import copy
import unittest

from veritrail.acceptance_plan import seal_acceptance_plan
from veritrail.canonical import canonical_json_bytes, sha256_json

from veritrail_github.contracts import (
    DEFAULT_COLLECTOR_POLICY,
    derive_observation_request,
    facts_digest,
    validate_observation_request,
)
from veritrail_github.errors import ContractError

from support import TARGET_SHA, acceptance_plan


class CanonicalContractTests(unittest.TestCase):
    def test_frozen_canonical_vectors(self) -> None:
        vectors = [
            (
                {},
                b"{}",
                "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
            ),
            (
                {"b": 2, "a": 1},
                b'{"a":1,"b":2}',
                "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
            ),
            (
                {"enabled": True, "label": "验迹", "value": None},
                '{"enabled":true,"label":"验迹","value":null}'.encode(),
                "8e7d13a7fc5609925598e1f5a9b8db749a4c54a49c4bea2acda36adf1418c270",
            ),
            (
                {"nested": {"z": 0, "a": "A"}, "items": [3, 2, 1]},
                b'{"items":[3,2,1],"nested":{"a":"A","z":0}}',
                "3ec5a09f647d26013353111c8569e41444237e1c517fd481658b3587f03b0f30",
            ),
        ]
        for value, encoded, digest in vectors:
            with self.subTest(value=value):
                self.assertEqual(canonical_json_bytes(value), encoded)
                self.assertEqual(sha256_json(value), digest)


class RequestContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = acceptance_plan(["commit.identity", "repository.identity"])

    def test_derivation_is_deterministic_and_validates_exactly(self) -> None:
        first = derive_observation_request(self.plan, "github-api", "request-001")
        second = derive_observation_request(self.plan, "github-api", "request-001")
        self.assertEqual(first, second)
        self.assertEqual(validate_observation_request(self.plan, first), first)
        self.assertEqual(
            first["observation_spec"]["projections"],
            sorted(first["observation_spec"]["projections"]),
        )

    def test_request_instance_changes_only_request_identity(self) -> None:
        first = derive_observation_request(self.plan, "github-api", "request-001")
        second = derive_observation_request(self.plan, "github-api", "request-002")
        self.assertEqual(
            first["observation_spec_digest"], second["observation_spec_digest"]
        )
        self.assertEqual(
            first["collector_policy_digest"], second["collector_policy_digest"]
        )
        self.assertNotEqual(first["seal"]["digest"], second["seal"]["digest"])

    def test_unrelated_plan_revision_does_not_change_spec_or_fact_identity(
        self,
    ) -> None:
        changed = copy.deepcopy(self.plan)
        changed.pop("seal")
        changed["question"] = "A clarified but observation-equivalent question."
        changed = seal_acceptance_plan(changed)
        first = derive_observation_request(self.plan, "github-api", "request-001")
        second = derive_observation_request(changed, "github-api", "request-001")
        self.assertEqual(
            first["observation_spec_digest"], second["observation_spec_digest"]
        )
        self.assertNotEqual(first["plan_digest"], second["plan_digest"])
        self.assertNotEqual(first["seal"]["digest"], second["seal"]["digest"])
        normalized = {"repository": None, "commit": {"sha": TARGET_SHA}}
        self.assertEqual(
            facts_digest(
                observation_spec_digest_value=first["observation_spec_digest"],
                source_coordinates=first["observation_spec"]["coordinates"],
                facts=normalized,
            ),
            facts_digest(
                observation_spec_digest_value=second["observation_spec_digest"],
                source_coordinates=second["observation_spec"]["coordinates"],
                facts=normalized,
            ),
        )

    def test_policy_change_changes_policy_and_request_not_spec(self) -> None:
        changed_policy = dict(DEFAULT_COLLECTOR_POLICY)
        changed_policy["retry_schedule_ms"] = [500, 1500]
        first = derive_observation_request(self.plan, "github-api", "request-001")
        second = derive_observation_request(
            self.plan,
            "github-api",
            "request-001",
            collector_policy=changed_policy,
        )
        self.assertEqual(
            first["observation_spec_digest"], second["observation_spec_digest"]
        )
        self.assertNotEqual(
            first["collector_policy_digest"], second["collector_policy_digest"]
        )
        self.assertNotEqual(first["seal"]["digest"], second["seal"]["digest"])

    def test_unknown_request_field_and_tampering_fail_closed(self) -> None:
        request = derive_observation_request(self.plan, "github-api", "request-001")
        request["expected.commit_sha"] = TARGET_SHA
        with self.assertRaises(ContractError):
            validate_observation_request(self.plan, request)
        request.pop("expected.commit_sha")
        request["observation_spec"]["coordinates"]["url"] = "https://example.invalid"
        with self.assertRaises(ContractError):
            validate_observation_request(self.plan, request)

    def test_float_and_unknown_projection_fail_before_collection(self) -> None:
        broken = copy.deepcopy(self.plan)
        broken.pop("seal")
        broken["observation_specs"][0]["coordinates"]["weight"] = 1.5
        with self.assertRaises(Exception):
            seal_acceptance_plan(broken)

    def test_unsorted_sealed_projection_fails_instead_of_producing_unbindable_evidence(
        self,
    ) -> None:
        broken = copy.deepcopy(self.plan)
        broken.pop("seal")
        broken["observation_specs"][0]["projections"] = [
            "repository.identity",
            "commit.identity",
        ]
        broken = seal_acceptance_plan(broken)
        with self.assertRaisesRegex(ContractError, "canonical lexical order"):
            derive_observation_request(broken, "github-api", "request-001")


if __name__ == "__main__":
    unittest.main()
