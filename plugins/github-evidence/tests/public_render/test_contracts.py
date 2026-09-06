from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from veritrail.acceptance_plan import seal_acceptance_plan

from veritrail_github.contracts import derive_observation_request
from veritrail_github.errors import ContractError
from veritrail_github.public_render_contracts import (
    DEFAULT_RENDER_POLICY,
    derive_public_render_request,
    public_render_target_url,
    render_policy_digest,
    validate_public_render_request,
)

from public_render.support import TARGET_SHA, public_render_plan
from support import acceptance_plan


PLUGIN_ROOT = Path(__file__).resolve().parents[2]


class PublicRenderRequestContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = public_render_plan()

    def test_public_fixture_preserves_frozen_spec_and_plan_vectors(self) -> None:
        plan = json.loads(
            (
                PLUGIN_ROOT
                / "examples"
                / "public-render-acceptance-plan.json"
            ).read_text(encoding="utf-8")
        )
        request = derive_public_render_request(
            plan, "github-public-readme", "render-request-001"
        )
        self.assertEqual(
            request["observation_spec_digest"],
            "fcdaaf5428814d2556426fdf0626199e0400f386172de764203ead7f0e6c28d8",
        )
        self.assertEqual(
            request["plan_digest"],
            "d08e2da6b665ebedaa1032eaf9834950a3d1e984b5b7c9e31f3d63d5ec4097ae",
        )
        self.assertEqual(validate_public_render_request(plan, request), request)
        self.assertEqual(
            public_render_target_url(request["observation_spec"]["coordinates"]),
            "https://github.com/NoctilumeDev/VeriTrail/blob/"
            "cdc2c250f21b37a0be9f815295f7b7c3c5081d0d/README.md",
        )
        self.assertNotIn("target_url", request)
        self.assertNotIn("collection_session_id", request)

    def test_derivation_is_deterministic_and_request_instance_is_separate(self) -> None:
        first = derive_public_render_request(
            self.plan, "github-public-render", "render-request-001"
        )
        repeated = derive_public_render_request(
            self.plan, "github-public-render", "render-request-001"
        )
        second = derive_public_render_request(
            self.plan, "github-public-render", "render-request-002"
        )
        self.assertEqual(first, repeated)
        self.assertEqual(
            first["observation_spec_digest"], second["observation_spec_digest"]
        )
        self.assertEqual(
            first["render_policy_digest"], second["render_policy_digest"]
        )
        self.assertNotEqual(first["seal"]["digest"], second["seal"]["digest"])

    def test_policy_change_does_not_change_observation_identity(self) -> None:
        changed_policy = dict(DEFAULT_RENDER_POLICY)
        changed_policy["navigation_timeout_ms"] = 15000
        first = derive_public_render_request(
            self.plan, "github-public-render", "render-request-001"
        )
        second = derive_public_render_request(
            self.plan,
            "github-public-render",
            "render-request-001",
            render_policy=changed_policy,
        )
        self.assertEqual(
            first["observation_spec_digest"], second["observation_spec_digest"]
        )
        self.assertNotEqual(
            first["render_policy_digest"], second["render_policy_digest"]
        )
        self.assertNotEqual(first["seal"]["digest"], second["seal"]["digest"])

    def test_request_tampering_and_caller_owned_url_fail_closed(self) -> None:
        request = derive_public_render_request(
            self.plan, "github-public-render", "render-request-001"
        )
        request["target_url"] = "https://example.invalid/"
        with self.assertRaisesRegex(ContractError, "unsupported fields"):
            validate_public_render_request(self.plan, request)
        request.pop("target_url")
        request["observation_spec"]["coordinates"]["repository_path"] = (
            "docs/other.md"
        )
        with self.assertRaisesRegex(ContractError, "deterministic sealed Plan"):
            validate_public_render_request(self.plan, request)

    def test_render_policy_is_bounded_and_contains_no_proxy_or_expectation(self) -> None:
        self.assertEqual(
            render_policy_digest(DEFAULT_RENDER_POLICY),
            render_policy_digest(dict(DEFAULT_RENDER_POLICY)),
        )
        for field, value in (
            ("max_requests", 513),
            ("max_elapsed_ms", 45001),
            ("response_body_read_chunk_bytes", 65537),
            ("sample_count", 2),
        ):
            with self.subTest(field=field):
                policy = dict(DEFAULT_RENDER_POLICY)
                policy[field] = value
                with self.assertRaises(ContractError):
                    derive_public_render_request(
                        self.plan,
                        "github-public-render",
                        "render-request-policy",
                        render_policy=policy,
                    )
        for field in ("proxy", "expected.marker", "browser_args"):
            with self.subTest(field=field):
                policy = dict(DEFAULT_RENDER_POLICY)
                policy[field] = "forbidden"
                with self.assertRaisesRegex(ContractError, "unsupported fields"):
                    derive_public_render_request(
                        self.plan,
                        "github-public-render",
                        "render-request-policy",
                        render_policy=policy,
                    )

    def test_non_string_object_keys_fail_as_contract_errors(self) -> None:
        policy = dict(DEFAULT_RENDER_POLICY)
        policy[1] = "not-a-json-object-key"
        with self.assertRaisesRegex(ContractError, "keys must be strings"):
            derive_public_render_request(
                self.plan,
                "github-public-render",
                "render-request-policy-key",
                render_policy=policy,
            )

        request = derive_public_render_request(
            self.plan, "github-public-render", "render-request-envelope-key"
        )
        request[1] = "not-a-json-object-key"
        with self.assertRaisesRegex(ContractError, "keys must be strings"):
            validate_public_render_request(self.plan, request)


class PublicRenderTargetUrlTests(unittest.TestCase):
    def _derive_url(self, coordinates: dict[str, object]) -> str:
        plan = public_render_plan(coordinates)
        request = derive_public_render_request(
            plan, "github-public-render", "render-request-target"
        )
        return public_render_target_url(request["observation_spec"]["coordinates"])

    def test_all_four_target_kinds_have_unique_structured_urls(self) -> None:
        cases = [
            (
                {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_REPOSITORY_README",
                    "viewport_profile": "DESKTOP_1365X768",
                },
                "https://github.com/NoctilumeDev/VeriTrail",
            ),
            (
                {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_MARKDOWN_FILE",
                    "target_commit_sha": TARGET_SHA,
                    "repository_path": "docs/设计 notes.md",
                    "viewport_profile": "NARROW_390X844",
                },
                "https://github.com/NoctilumeDev/VeriTrail/blob/"
                f"{TARGET_SHA}/docs/%E8%AE%BE%E8%AE%A1%20notes.md",
            ),
            (
                {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_RELEASE",
                    "release_tag": "release/v1.0:rc1",
                    "viewport_profile": "DESKTOP_1365X768",
                },
                "https://github.com/NoctilumeDev/VeriTrail/releases/tag/"
                "release/v1.0%3Arc1",
            ),
            (
                {
                    "owner": "NoctilumeDev",
                    "repository": "NoctilumeDev.github.io",
                    "target_kind": "GITHUB_PAGES_DEFAULT",
                    "site_kind": "OWNER",
                    "pages_path": "",
                    "viewport_profile": "DESKTOP_1365X768",
                },
                "https://noctilumedev.github.io/",
            ),
            (
                {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_PAGES_DEFAULT",
                    "site_kind": "PROJECT",
                    "pages_path": "",
                    "viewport_profile": "DESKTOP_1365X768",
                },
                "https://noctilumedev.github.io/VeriTrail/",
            ),
            (
                {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_PAGES_DEFAULT",
                    "site_kind": "PROJECT",
                    "pages_path": "guides/开始.html",
                    "viewport_profile": "NARROW_390X844",
                },
                "https://noctilumedev.github.io/VeriTrail/guides/"
                "%E5%BC%80%E5%A7%8B.html",
            ),
        ]
        for coordinates, expected in cases:
            with self.subTest(kind=coordinates["target_kind"], expected=expected):
                self.assertEqual(self._derive_url(coordinates), expected)

    def test_target_specific_fields_are_exact_not_ignored(self) -> None:
        coordinates = {
            "owner": "NoctilumeDev",
            "repository": "VeriTrail",
            "target_kind": "GITHUB_REPOSITORY_README",
            "viewport_profile": "DESKTOP_1365X768",
            "release_tag": "v1.0.0",
        }
        with self.assertRaisesRegex(ContractError, "unsupported fields"):
            self._derive_url(coordinates)

    def test_markdown_and_pages_paths_reject_aliases_and_encoded_separators(self) -> None:
        unsafe = [
            "",
            "/README.md",
            "docs/",
            "docs//README.md",
            "docs/./README.md",
            "docs/../README.md",
            "docs\\README.md",
            "docs/%2fREADME.md",
            "docs/%5CREADME.md",
            "docs/README.md?raw=1",
            "docs/README.md#section",
            "docs/\x00README.md",
        ]
        for path in unsafe:
            with self.subTest(markdown_path=path):
                coordinates = {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_MARKDOWN_FILE",
                    "target_commit_sha": TARGET_SHA,
                    "repository_path": path,
                    "viewport_profile": "DESKTOP_1365X768",
                }
                with self.assertRaises(ContractError):
                    self._derive_url(coordinates)

        for path in [
            "/",
            ".",
            "./",
            "a/",
            "a//b",
            "a/../b",
            "a\\b",
            "a/%2fb",
            "a?query=1",
            "a#fragment",
        ]:
            with self.subTest(pages_path=path):
                coordinates = {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_PAGES_DEFAULT",
                    "site_kind": "PROJECT",
                    "pages_path": path,
                    "viewport_profile": "DESKTOP_1365X768",
                }
                with self.assertRaises(ContractError):
                    self._derive_url(coordinates)

    def test_coordinates_require_json_object_keys(self) -> None:
        coordinates = {
            "owner": "NoctilumeDev",
            "repository": "VeriTrail",
            "target_kind": "GITHUB_REPOSITORY_README",
            "viewport_profile": "DESKTOP_1365X768",
            1: "not-a-json-object-key",
        }
        with self.assertRaisesRegex(ContractError, "keys must be strings"):
            public_render_target_url(coordinates)

    def test_url_derivation_rejects_non_scalar_path_text(self) -> None:
        for coordinates in (
            {
                "owner": "NoctilumeDev",
                "repository": "VeriTrail",
                "target_kind": "GITHUB_MARKDOWN_FILE",
                "target_commit_sha": TARGET_SHA,
                "repository_path": "docs/\ud800README.md",
                "viewport_profile": "DESKTOP_1365X768",
            },
            {
                "owner": "NoctilumeDev",
                "repository": "VeriTrail",
                "target_kind": "GITHUB_PAGES_DEFAULT",
                "site_kind": "PROJECT",
                "pages_path": "a/\ud800",
                "viewport_profile": "DESKTOP_1365X768",
            },
        ):
            with self.subTest(target_kind=coordinates["target_kind"]):
                with self.assertRaises(ContractError):
                    public_render_target_url(coordinates)

    def test_release_tag_rejects_aliases_queries_and_preencoding(self) -> None:
        for tag in ["", ".", "..", "a//b", "a/../b", "v1%2Frc1", "v1?x=1"]:
            with self.subTest(tag=tag):
                coordinates = {
                    "owner": "NoctilumeDev",
                    "repository": "VeriTrail",
                    "target_kind": "GITHUB_RELEASE",
                    "release_tag": tag,
                    "viewport_profile": "DESKTOP_1365X768",
                }
                with self.assertRaises(ContractError):
                    self._derive_url(coordinates)

    def test_owner_pages_repository_identity_is_not_guessed(self) -> None:
        coordinates = {
            "owner": "NoctilumeDev",
            "repository": "Other.github.io",
            "target_kind": "GITHUB_PAGES_DEFAULT",
            "site_kind": "OWNER",
            "pages_path": "",
            "viewport_profile": "DESKTOP_1365X768",
        }
        with self.assertRaisesRegex(ContractError, "OWNER Pages"):
            self._derive_url(coordinates)


class PublicRenderProjectionTests(unittest.TestCase):
    def test_literal_projection_controls_field_presence(self) -> None:
        base = {
            "owner": "NoctilumeDev",
            "repository": "VeriTrail",
            "target_kind": "GITHUB_REPOSITORY_README",
            "viewport_profile": "DESKTOP_1365X768",
        }
        with_unrequested_field = dict(base, literal_markers=[])
        with self.assertRaisesRegex(ContractError, "literal_markers"):
            derive_public_render_request(
                public_render_plan(with_unrequested_field),
                "github-public-render",
                "render-request-literal",
            )
        with self.assertRaisesRegex(ContractError, "literal_markers"):
            derive_public_render_request(
                public_render_plan(
                    base,
                    projections=["content.literal_markers", "navigation.identity"],
                ),
                "github-public-render",
                "render-request-literal",
            )
        accepted = derive_public_render_request(
            public_render_plan(
                dict(base, literal_markers=[]),
                projections=["content.literal_markers", "navigation.identity"],
            ),
            "github-public-render",
            "render-request-literal",
        )
        self.assertEqual(
            accepted["observation_spec"]["coordinates"]["literal_markers"], []
        )

    def test_literals_must_already_use_frozen_normalization_and_bounds(self) -> None:
        base = {
            "owner": "NoctilumeDev",
            "repository": "VeriTrail",
            "target_kind": "GITHUB_REPOSITORY_README",
            "viewport_profile": "DESKTOP_1365X768",
        }
        invalid_sets = [["   "], [" A   B "], ["x" * 257], ["x"] * 33]
        for markers in invalid_sets:
            with self.subTest(marker_count=len(markers)):
                with self.assertRaises(ContractError):
                    derive_public_render_request(
                        public_render_plan(
                            dict(base, literal_markers=markers),
                            projections=[
                                "content.literal_markers",
                                "navigation.identity",
                            ],
                        ),
                        "github-public-render",
                        "render-request-literal",
                    )

    def test_projections_are_set_like_but_plan_must_store_canonical_order(self) -> None:
        plan = public_render_plan(
            projections=["navigation.identity", "content.scope"]
        )
        with self.assertRaisesRegex(ContractError, "canonical lexical order"):
            derive_public_render_request(
                plan, "github-public-render", "render-request-projection"
            )

    def test_unknown_projection_and_viewport_fail_before_browser_creation(self) -> None:
        plan = public_render_plan(projections=["content.javascript"])
        with self.assertRaisesRegex(ContractError, "unsupported projection"):
            derive_public_render_request(
                plan, "github-public-render", "render-request-projection"
            )
        coordinates = copy.deepcopy(
            self._valid_readme_coordinates()
        )
        coordinates["viewport_profile"] = "MOBILE_DEVICE"
        with self.assertRaisesRegex(ContractError, "viewport_profile"):
            derive_public_render_request(
                public_render_plan(coordinates),
                "github-public-render",
                "render-request-viewport",
            )

    @staticmethod
    def _valid_readme_coordinates() -> dict[str, object]:
        return {
            "owner": "NoctilumeDev",
            "repository": "VeriTrail",
            "target_kind": "GITHUB_REPOSITORY_README",
            "viewport_profile": "DESKTOP_1365X768",
        }


class P1P2CoordinateConformanceTests(unittest.TestCase):
    def test_owner_and_repository_boundaries_conform_without_shared_validator(self) -> None:
        cases = [
            ("NoctilumeDev", "VeriTrail", True),
            ("A", "repo_1.2", True),
            ("a-", "repo", True),
            ("-bad", "repo", False),
            ("bad/name", "repo", False),
            ("NoctilumeDev", ".", False),
            ("NoctilumeDev", "..", False),
            ("NoctilumeDev", "repo.git", False),
            ("NoctilumeDev", "bad/name", False),
            ("NoctilumeDev", "r" * 101, False),
        ]
        for owner, repository, expected in cases:
            with self.subTest(owner=owner, repository=repository):
                p1 = acceptance_plan(["repository.identity"])
                p1.pop("seal")
                p1["observation_specs"][0]["coordinates"]["owner"] = owner
                p1["observation_specs"][0]["coordinates"]["repository"] = repository
                p1 = seal_acceptance_plan(p1)
                p2_coordinates = {
                    "owner": owner,
                    "repository": repository,
                    "target_kind": "GITHUB_REPOSITORY_README",
                    "viewport_profile": "DESKTOP_1365X768",
                }
                p2 = public_render_plan(p2_coordinates)
                p1_accepted = True
                p2_accepted = True
                try:
                    derive_observation_request(p1, "github-api", "coordinate-check")
                except ContractError:
                    p1_accepted = False
                try:
                    derive_public_render_request(
                        p2, "github-public-render", "coordinate-check"
                    )
                except ContractError:
                    p2_accepted = False
                self.assertEqual(p1_accepted, expected)
                self.assertEqual(p2_accepted, expected)
                self.assertEqual(p1_accepted, p2_accepted)


if __name__ == "__main__":
    unittest.main()
