from __future__ import annotations

import unittest

from veritrail_github.public_render_navigation import (
    PublicRenderNavigationError,
    PublicRenderNetworkPolicy,
    fixed_scope_selector,
    navigation_identity_conflicts,
    normalized_media_type,
    safe_public_url_facts,
)


class SafePublicUrlTests(unittest.TestCase):
    def test_query_and_fragment_values_are_not_retained(self) -> None:
        facts = safe_public_url_facts(
            "https://GitHub.com/NoctilumeDev/VeriTrail?token=secret#private"
        )
        self.assertEqual(
            facts,
            {
                "origin": "https://github.com",
                "host": "github.com",
                "path": "/NoctilumeDev/VeriTrail",
                "query_present": True,
                "fragment_present": True,
            },
        )
        self.assertNotIn("secret", repr(facts))
        self.assertNotIn("private", repr(facts))

    def test_unsafe_urls_fail_without_guessing(self) -> None:
        for value in (
            "http://github.com/owner/repo",
            "https://user:pass@github.com/owner/repo",
            "https://github.com:444/owner/repo",
            "https://github.com/owner/\x00repo",
            "https://github.com:invalid/owner/repo",
            "",
        ):
            with self.subTest(value=value):
                with self.assertRaises(PublicRenderNavigationError):
                    safe_public_url_facts(value)


class PublicRenderNetworkPolicyTests(unittest.TestCase):
    def _github_policy(self, *, max_requests: int = 8) -> PublicRenderNetworkPolicy:
        return PublicRenderNetworkPolicy(
            target_url="https://github.com/NoctilumeDev/VeriTrail",
            target_kind="GITHUB_REPOSITORY_README",
            max_requests=max_requests,
            max_redirects=2,
        )

    def test_github_main_document_is_exact_and_subresources_use_label_boundaries(
        self,
    ) -> None:
        cases = (
            ("https://github.com/NoctilumeDev/VeriTrail", True, True),
            ("https://raw.githubusercontent.com/a/b/c", False, True),
            ("https://github.githubassets.com/a.js", False, True),
            ("https://avatars.githubusercontent.com/u/1", False, True),
            ("https://assets.github.com/a.css", False, True),
            ("https://githubassets.com/a.css", False, False),
            ("https://githubusercontent.com/a", False, False),
            ("https://assets.github.com/a.css", True, False),
            ("https://evilgithub.com/a.js", False, False),
            ("https://githubassets.com.evil.test/a.js", False, False),
        )
        policy = self._github_policy(max_requests=len(cases))
        for url, main_document, expected in cases:
            with self.subTest(url=url, main_document=main_document):
                decision = policy.decide(
                    method="GET", url=url, main_document=main_document
                )
                self.assertEqual(decision.allowed, expected)

    def test_pages_allows_only_the_exact_target_origin(self) -> None:
        policy = PublicRenderNetworkPolicy(
            target_url="https://noctilumedev.github.io/VeriTrail/",
            target_kind="GITHUB_PAGES_DEFAULT",
            max_requests=3,
            max_redirects=1,
        )
        self.assertTrue(
            policy.decide(
                method="GET",
                url="https://noctilumedev.github.io/VeriTrail/app.js",
                main_document=False,
            ).allowed
        )
        self.assertFalse(
            policy.decide(
                method="GET",
                url="https://raw.githubusercontent.com/a/b/c",
                main_document=False,
            ).allowed
        )
        self.assertFalse(
            policy.decide(
                method="GET",
                url="https://other.github.io/VeriTrail/",
                main_document=True,
            ).allowed
        )

    def test_writes_are_blocked_without_becoming_content_failure(self) -> None:
        decision = self._github_policy().decide(
            method="POST",
            url="https://github.com/_private/browser/stats",
            main_document=False,
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reasons, ("METHOD_NOT_ALLOWED",))
        self.assertFalse(decision.affects_coverage)

    def test_unexpected_read_host_and_limits_affect_coverage(self) -> None:
        policy = self._github_policy(max_requests=1)
        first = policy.decide(
            method="GET", url="https://example.invalid/a", main_document=False
        )
        second = policy.decide(
            method="GET", url="https://github.com/a", main_document=False
        )
        self.assertEqual(first.reasons, ("HOST_NOT_ALLOWED",))
        self.assertTrue(first.affects_coverage)
        self.assertIn("REQUEST_LIMIT_EXCEEDED", second.reasons)
        self.assertTrue(second.affects_coverage)

    def test_redirect_depth_is_bounded_only_for_main_document(self) -> None:
        policy = self._github_policy()
        over = policy.decide(
            method="GET",
            url="https://github.com/a/b",
            main_document=True,
            redirect_depth=3,
        )
        subresource = policy.decide(
            method="GET",
            url="https://github.com/a.js",
            main_document=False,
            redirect_depth=99,
        )
        self.assertIn("REDIRECT_LIMIT_EXCEEDED", over.reasons)
        self.assertFalse(over.allowed)
        self.assertTrue(subresource.allowed)

    def test_websocket_is_always_blocked_without_payload(self) -> None:
        policy = self._github_policy(max_requests=1)
        decision = policy.reject_websocket(
            "wss://alive.github.com/socket?token=secret"
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reasons, ("WEBSOCKET_NOT_ALLOWED",))
        self.assertEqual(decision.sequence, 1)
        self.assertEqual(
            decision.safe_url,
            {"scheme_class": "wss", "host": "alive.github.com"},
        )
        self.assertNotIn("secret", repr(decision))
        over = policy.reject_websocket("wss://alive.github.com/second")
        self.assertIn("REQUEST_LIMIT_EXCEEDED", over.reasons)
        self.assertTrue(over.affects_coverage)


class NavigationIdentityTests(unittest.TestCase):
    def test_exact_coordinate_has_no_conflict(self) -> None:
        self.assertEqual(
            navigation_identity_conflicts(
                requested_url="https://github.com/NoctilumeDev/VeriTrail",
                final_url="https://github.com/NoctilumeDev/VeriTrail",
            ),
            [],
        )

    def test_coordinate_drift_and_decoration_remain_explicit(self) -> None:
        moved = navigation_identity_conflicts(
            requested_url="https://github.com/NoctilumeDev/VeriTrail",
            final_url="https://github.com/Other/VeriTrail",
        )
        decorated = navigation_identity_conflicts(
            requested_url="https://github.com/NoctilumeDev/VeriTrail",
            final_url="https://github.com/NoctilumeDev/VeriTrail?tab=readme",
        )
        self.assertEqual(moved[0]["code"], "FINAL_COORDINATE_MISMATCH")
        self.assertEqual(decorated[0]["code"], "FINAL_COORDINATE_DECORATED")
        self.assertNotIn("tab=readme", repr(decorated))

    def test_media_type_is_normalized_but_not_invented(self) -> None:
        self.assertEqual(
            normalized_media_type({"Content-Type": "Text/HTML; charset=utf-8"}),
            "text/html",
        )
        self.assertIsNone(normalized_media_type({}))
        with self.assertRaises(PublicRenderNavigationError):
            normalized_media_type(
                {"Content-Type": "text/html", "content-type": "text/plain"}
            )

    def test_target_kinds_have_fixed_non_fallback_scopes(self) -> None:
        self.assertEqual(
            fixed_scope_selector("GITHUB_REPOSITORY_README"),
            "article.markdown-body",
        )
        self.assertEqual(
            fixed_scope_selector("GITHUB_MARKDOWN_FILE"),
            "article.markdown-body",
        )
        self.assertEqual(
            fixed_scope_selector("GITHUB_RELEASE"), "main .markdown-body"
        )
        self.assertEqual(fixed_scope_selector("GITHUB_PAGES_DEFAULT"), "main")
        with self.assertRaises(PublicRenderNavigationError):
            fixed_scope_selector("BODY_FALLBACK")


if __name__ == "__main__":
    unittest.main()
