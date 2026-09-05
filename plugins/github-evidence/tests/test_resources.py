from __future__ import annotations

import unittest

from veritrail.acceptance_evaluation import evaluate_acceptance

from support import TARGET_SHA, acceptance_plan, base_transport
from test_collector import collect


class ResourceProjectionTests(unittest.TestCase):
    def test_release_assets_are_normalized_without_download_urls(self) -> None:
        plan = acceptance_plan(
            ["release.assets", "release.identity"], release_tag="v0.1.0"
        )
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/releases/tags/v0.1.0",
            {
                "id": 55,
                "tag_name": "v0.1.0",
                "target_commitish": "main",
                "draft": False,
                "prerelease": False,
                "immutable": True,
                "published_at": "2026-09-05T00:00:00Z",
                "assets": [
                    {
                        "id": 2,
                        "name": "plugin.whl",
                        "size": 1234,
                        "state": "uploaded",
                        "digest": "sha256:abc",
                        "browser_download_url": "https://example.invalid/ignored",
                    }
                ],
            },
        )
        release = collect(plan, transport).artifact.document["facts"]["release"]
        self.assertEqual(release["id"], 55)
        self.assertEqual(release["assets"][0]["size_bytes"], 1234)
        self.assertNotIn("browser_download_url", release["assets"][0])

    def test_pages_metadata_does_not_claim_rendered_content(self) -> None:
        plan = acceptance_plan(["pages.metadata"])
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/pages",
            {
                "status": "built",
                "cname": None,
                "custom_404": False,
                "html_url": "https://noctilumedev.github.io/VeriTrail/",
                "build_type": "workflow",
                "source": {"branch": "main", "path": "/"},
                "https_enforced": True,
                "public": True,
                "protected_domain_state": None,
                "pending_domain_unverified_at": None,
            },
        )
        pages = collect(plan, transport).artifact.document["facts"]["pages"]
        self.assertEqual(pages["status"], "built")
        self.assertNotIn("rendered", pages)
        self.assertNotIn("content", pages)

    def test_lightweight_tag_is_already_a_commit(self) -> None:
        plan = acceptance_plan(["tag.peeled_commit"], release_tag="v0.1.0")
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
            {
                "ref": "refs/tags/v0.1.0",
                "object": {"type": "commit", "sha": TARGET_SHA},
            },
        )
        tag = collect(plan, transport).artifact.document["facts"]["tag"]
        self.assertEqual(tag["peeled_commit_sha"], TARGET_SHA)
        self.assertEqual(len(tag["peel_chain"]), 1)

    def test_non_commit_tag_target_is_partial_not_a_false_commit(self) -> None:
        plan = acceptance_plan(["tag.peeled_commit"], release_tag="v0.1.0")
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
            {
                "ref": "refs/tags/v0.1.0",
                "object": {"type": "tree", "sha": "f" * 40},
            },
        )
        result = collect(plan, transport)
        self.assertIsNone(result.artifact.document["facts"]["tag"])
        self.assertEqual(
            result.artifact.document["metadata"]["veritrail_observation"]["coverage"],
            "PARTIAL",
        )

    def test_wrong_tag_commit_is_retained_as_a_conflict_and_core_non_pass(self) -> None:
        wrong_sha = "c" * 40
        plan = acceptance_plan(
            ["tag.peeled_commit"],
            release_tag="v0.1.0",
            assertion_path="/facts/tag/peeled_commit_sha",
            assertion_value=TARGET_SHA,
        )
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
            {
                "ref": "refs/tags/v0.1.0",
                "object": {"type": "commit", "sha": wrong_sha},
            },
        )
        result = collect(plan, transport)
        document = result.artifact.document
        self.assertEqual(document["facts"]["tag"]["peeled_commit_sha"], wrong_sha)
        self.assertIn(
            "TAG_TARGET_COMMIT_MISMATCH",
            {item["code"] for item in document["facts"]["conflicts"]},
        )
        self.assertNotEqual(
            evaluate_acceptance(plan, [result.artifact], "COMPLETED")["verdict"],
            "PASS",
        )

    def test_tag_cycle_is_distinct_from_non_commit_target(self) -> None:
        tag_object = "f" * 40
        plan = acceptance_plan(["tag.peeled_commit"], release_tag="v0.1.0")
        transport = (
            base_transport()
            .add(
                "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
                {
                    "ref": "refs/tags/v0.1.0",
                    "object": {"type": "tag", "sha": tag_object},
                },
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/git/tags/{tag_object}",
                {"sha": tag_object, "object": {"type": "tag", "sha": tag_object}},
            )
        )
        result = collect(plan, transport)
        self.assertIn(
            "TAG_PEEL_CYCLE",
            {
                item["code"]
                for item in result.artifact.document["metadata"]["github_collection"][
                    "errors"
                ]
            },
        )

    def test_tag_peel_limit_is_distinct_from_cycle(self) -> None:
        tag_shas = [f"{index:x}" * 40 for index in range(1, 7)]
        plan = acceptance_plan(["tag.peeled_commit"], release_tag="v0.1.0")
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
            {
                "ref": "refs/tags/v0.1.0",
                "object": {"type": "tag", "sha": tag_shas[0]},
            },
        )
        for current, following in zip(tag_shas, tag_shas[1:]):
            transport.add(
                f"/repos/NoctilumeDev/VeriTrail/git/tags/{current}",
                {"sha": current, "object": {"type": "tag", "sha": following}},
            )
        result = collect(plan, transport)
        self.assertIn(
            "TAG_PEEL_LIMIT_REACHED",
            {
                item["code"]
                for item in result.artifact.document["metadata"]["github_collection"][
                    "errors"
                ]
            },
        )

    def test_lightweight_and_annotated_tags_share_fact_but_not_peel_provenance(
        self,
    ) -> None:
        plan = acceptance_plan(["tag.peeled_commit"], release_tag="v0.1.0")
        lightweight = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
            {
                "ref": "refs/tags/v0.1.0",
                "object": {"type": "commit", "sha": TARGET_SHA},
            },
        )
        tag_object = "f" * 40
        annotated = (
            base_transport()
            .add(
                "/repos/NoctilumeDev/VeriTrail/git/ref/tags/v0.1.0",
                {
                    "ref": "refs/tags/v0.1.0",
                    "object": {"type": "tag", "sha": tag_object},
                },
            )
            .add(
                f"/repos/NoctilumeDev/VeriTrail/git/tags/{tag_object}",
                {"sha": tag_object, "object": {"type": "commit", "sha": TARGET_SHA}},
            )
        )
        first = collect(plan, lightweight).artifact.document["facts"]["tag"]
        second = collect(plan, annotated).artifact.document["facts"]["tag"]
        self.assertEqual(first["peeled_commit_sha"], second["peeled_commit_sha"])
        self.assertNotEqual(first["peel_chain"], second["peel_chain"])

    def test_release_tag_mismatch_and_duplicate_assets_are_not_collapsed(self) -> None:
        plan = acceptance_plan(
            ["release.assets", "release.identity"], release_tag="v0.1.0"
        )
        duplicate = {
            "id": 2,
            "name": "plugin.whl",
            "size": 1234,
            "state": "uploaded",
            "digest": "sha256:abc",
        }
        transport = base_transport().add(
            "/repos/NoctilumeDev/VeriTrail/releases/tags/v0.1.0",
            {
                "id": 55,
                "tag_name": "v0.0.9",
                "target_commitish": "main",
                "draft": False,
                "prerelease": False,
                "immutable": False,
                "published_at": "2026-09-05T00:00:00Z",
                "assets": [duplicate, duplicate],
            },
        )
        result = collect(plan, transport)
        facts = result.artifact.document["facts"]
        self.assertEqual(len(facts["release"]["assets"]), 2)
        codes = {item["code"] for item in facts["conflicts"]}
        self.assertIn("RELEASE_TAG_IDENTITY_MISMATCH", codes)
        self.assertIn("RELEASE_ASSET_IDENTITY_DUPLICATED", codes)

    def test_unrequested_pages_are_not_probed_or_claimed(self) -> None:
        plan = acceptance_plan(["commit.identity"])
        transport = base_transport()
        result = collect(plan, transport)
        self.assertIsNone(result.artifact.document["facts"]["pages"])
        self.assertFalse(
            any(call["path_and_query"].endswith("/pages") for call in transport.calls)
        )


if __name__ == "__main__":
    unittest.main()
