from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from veritrail_github.collector import GitHubCollector
from veritrail_github.contracts import derive_observation_request
from veritrail_github.errors import CollectionError
from veritrail_github.publisher import publish_evidence

from support import acceptance_plan, base_transport


class PublisherTests(unittest.TestCase):
    def test_atomic_create_new_and_staging_cleanup(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        request = derive_observation_request(plan, "github-api", "request-001")
        result = GitHubCollector(
            base_transport(), session_id_factory=lambda: "github-session-001"
        ).collect(plan, request)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            publish_evidence(output, result.artifact)
            self.assertTrue(output.is_file())
            self.assertFalse(list(Path(directory).glob("*.staging")))
            with self.assertRaises(CollectionError):
                publish_evidence(output, result.artifact)
            self.assertFalse(list(Path(directory).glob("*.staging")))


if __name__ == "__main__":
    unittest.main()
