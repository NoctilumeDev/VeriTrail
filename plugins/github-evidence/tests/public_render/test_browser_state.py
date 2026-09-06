from __future__ import annotations

import unittest

from veritrail_github.public_render_browser import (
    FreshContextRejected,
    PublicRenderBrowserError,
    browser_context_options,
    post_navigation_storage_summary,
    validate_fresh_storage_state,
)


class BrowserContextPolicyTests(unittest.TestCase):
    def test_desktop_and_narrow_profiles_change_only_dimensions(self) -> None:
        desktop = browser_context_options("DESKTOP_1365X768")
        narrow = browser_context_options("NARROW_390X844")
        self.assertEqual(desktop["viewport"], {"width": 1365, "height": 768})
        self.assertEqual(narrow["viewport"], {"width": 390, "height": 844})
        for options in (desktop, narrow):
            self.assertFalse(options["is_mobile"])
            self.assertFalse(options["has_touch"])
            self.assertEqual(options["device_scale_factor"], 1)
            self.assertEqual(options["locale"], "en-US")
            self.assertEqual(options["timezone_id"], "UTC")
            self.assertEqual(options["color_scheme"], "light")
            self.assertEqual(options["reduced_motion"], "reduce")
            self.assertEqual(options["permissions"], [])
            self.assertEqual(options["service_workers"], "block")
            self.assertFalse(options["accept_downloads"])
            self.assertTrue(options["java_script_enabled"])
            for forbidden in (
                "user_data_dir",
                "storage_state",
                "proxy",
                "http_credentials",
                "client_certificates",
                "geolocation",
                "user_agent",
            ):
                self.assertNotIn(forbidden, options)

    def test_unknown_viewport_does_not_fall_back(self) -> None:
        with self.assertRaises(PublicRenderBrowserError):
            browser_context_options("MOBILE_DEVICE")


class FreshStorageStateTests(unittest.TestCase):
    def test_empty_state_proves_only_the_initial_context_boundary(self) -> None:
        self.assertEqual(
            validate_fresh_storage_state({"cookies": [], "origins": []}),
            {
                "kind": "ANONYMOUS_FRESH_CONTEXT",
                "cookies": 0,
                "origins": 0,
            },
        )

    def test_cookie_or_origin_presence_fails_before_navigation(self) -> None:
        states = (
            {"cookies": [{"name": "session", "value": "secret"}], "origins": []},
            {
                "cookies": [],
                "origins": [
                    {"origin": "https://github.com", "localStorage": []}
                ],
            },
        )
        for state in states:
            with self.subTest(state_keys=tuple(state)):
                with self.assertRaises(FreshContextRejected):
                    validate_fresh_storage_state(state)

    def test_malformed_state_is_not_reinterpreted_as_empty(self) -> None:
        for state in (
            {},
            {"cookies": []},
            {"cookies": [], "origins": [], "future": []},
            {"cookies": {}, "origins": []},
        ):
            with self.subTest(state=state):
                with self.assertRaises(PublicRenderBrowserError):
                    validate_fresh_storage_state(state)

    def test_post_navigation_summary_retains_no_cookie_identity_or_value(self) -> None:
        state = {
            "cookies": [
                {
                    "name": "user-auth-cookie",
                    "value": "top-secret",
                    "domain": ".github.com",
                    "secure": True,
                    "httpOnly": True,
                    "sameSite": "Lax",
                    "expires": -1,
                },
                {
                    "name": "telemetry",
                    "value": "also-secret",
                    "domain": ".github.com",
                    "secure": True,
                    "httpOnly": False,
                    "sameSite": "FutureValue",
                    "expires": 9999999999,
                },
            ],
            "origins": [
                {"origin": "https://github.com", "localStorage": []}
            ],
        }
        summary = post_navigation_storage_summary(state)
        self.assertEqual(summary["cookie_count"], 2)
        self.assertEqual(summary["origin_count"], 1)
        self.assertEqual(summary["secure_cookie_count"], 2)
        self.assertEqual(summary["http_only_cookie_count"], 1)
        self.assertEqual(summary["session_cookie_count"], 1)
        self.assertEqual(
            summary["same_site_counts"],
            {"Strict": 0, "Lax": 1, "None": 0, "Unknown": 1},
        )
        serialized = repr(summary)
        for forbidden in (
            "user-auth-cookie",
            "telemetry",
            "top-secret",
            "also-secret",
            ".github.com",
        ):
            self.assertNotIn(forbidden, serialized)


if __name__ == "__main__":
    unittest.main()
