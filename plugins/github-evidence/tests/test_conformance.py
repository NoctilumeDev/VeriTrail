from __future__ import annotations

import copy
import unittest

from veritrail.evidence import import_evidence_document

from veritrail_github.conformance import verify_github_evidence
from veritrail_github.contracts import derive_observation_request
from veritrail_github.errors import ContractError

from support import acceptance_plan, base_transport
from test_collector import collect


class GitHubEvidenceConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = acceptance_plan(["commit.identity"])
        self.request = derive_observation_request(
            self.plan, "github-api", "request-001"
        )
        self.result = collect(self.plan, base_transport())

    def _tampered_artifact(self, mutate) -> object:
        document = copy.deepcopy(self.result.artifact.document)
        mutate(document)
        return import_evidence_document(document, "tampered.json")

    def test_collector_output_passes_adapter_conformance(self) -> None:
        verify_github_evidence(self.plan, self.request, self.result.artifact)

    def test_fact_change_without_adapter_digest_change_is_rejected(self) -> None:
        artifact = self._tampered_artifact(
            lambda document: document["facts"]["commit"].update({"sha": "b" * 40})
        )
        with self.assertRaisesRegex(ContractError, "facts_digest"):
            verify_github_evidence(self.plan, self.request, artifact)

    def test_session_binding_drift_is_rejected(self) -> None:
        artifact = self._tampered_artifact(
            lambda document: document["metadata"]["github_collection"].update(
                {"collection_session_id": "github-other-session"}
            )
        )
        with self.assertRaisesRegex(ContractError, "session identities"):
            verify_github_evidence(self.plan, self.request, artifact)

    def test_request_binding_drift_is_rejected(self) -> None:
        artifact = self._tampered_artifact(
            lambda document: document["metadata"]["github_collection"].update(
                {"request_id": "request-other"}
            )
        )
        with self.assertRaisesRegex(ContractError, "request_id"):
            verify_github_evidence(self.plan, self.request, artifact)

    def test_plugin_verdict_like_fact_is_rejected(self) -> None:
        artifact = self._tampered_artifact(
            lambda document: document["facts"].update(
                {"all_required_checks_passed": True}
            )
        )
        with self.assertRaisesRegex(ContractError, "Verdict-like"):
            verify_github_evidence(self.plan, self.request, artifact)


if __name__ == "__main__":
    unittest.main()
