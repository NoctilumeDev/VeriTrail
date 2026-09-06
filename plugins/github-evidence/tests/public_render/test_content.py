from __future__ import annotations

import json
import unittest

from veritrail_github.public_render_content import (
    MAX_HEADINGS,
    MAX_LINKS,
    MAX_RENDERED_TEXT_BYTES,
    PublicRenderContentError,
    collect_content_sample,
    collect_content_window,
    collect_document_identity,
    in_initial_viewport,
    safe_link_target,
)

from public_render.support import public_render_plan
from veritrail_github.public_render_contracts import derive_public_render_request


class _Element:
    def __init__(
        self,
        *,
        text: str = "",
        tag_name: str | None = None,
        visible: bool = True,
        box: dict[str, float] | None = None,
        href: object = None,
        resolved_href: object = None,
    ) -> None:
        self.text = text
        self.tag_name = tag_name
        self.visible = visible
        self.box = box
        self.href = href
        self.resolved_href = resolved_href

    def evaluate(self, _script: str, **_kwargs: object) -> object:
        if "element.href" in _script:
            if self.resolved_href is not None:
                return self.resolved_href
            if isinstance(self.href, str) and self.href.startswith("/"):
                return f"https://github.com{self.href}"
            return self.href
        return self.tag_name

    def inner_text(self, **_kwargs: object) -> str:
        return self.text

    def is_visible(self, **_kwargs: object) -> bool:
        return self.visible

    def bounding_box(self, **_kwargs: object) -> dict[str, float] | None:
        return self.box

    def get_attribute(self, name: str, **_kwargs: object) -> object:
        if name != "href":
            raise AssertionError("unexpected attribute")
        return self.href


class _Elements:
    def __init__(self, items: list[_Element]) -> None:
        self.items = items

    def count(self) -> int:
        return len(self.items)

    def nth(self, index: int) -> _Element:
        return self.items[index]


class _Scope:
    def __init__(
        self,
        texts: list[str],
        *,
        headings: list[_Element] | None = None,
        links: list[_Element] | None = None,
    ) -> None:
        self._texts = list(texts)
        self._text_index = 0
        self._headings = _Elements(headings or [])
        self._links = _Elements(links or [])

    def inner_text(self, **_kwargs: object) -> str:
        index = min(self._text_index, len(self._texts) - 1)
        self._text_index += 1
        return self._texts[index]

    def locator(self, selector: str) -> _Elements:
        if selector.startswith("h1"):
            return self._headings
        if selector == "a[href]":
            return self._links
        raise AssertionError(f"unexpected selector: {selector}")


class _Page:
    def __init__(self, url: str) -> None:
        self.url = url


class _Session:
    def __init__(
        self,
        scope: _Scope,
        navigation_conflicts: tuple[dict[str, object], ...] = (),
    ) -> None:
        self.scope_locator = scope
        self.page = _Page("https://github.com/owner/repository")
        self.delays: list[int] = []
        self.health_checks = 0
        self._navigation_conflicts = navigation_conflicts

    def wait_for_policy_delay(self, delay_ms: int) -> None:
        self.delays.append(delay_ms)

    def assert_healthy(self) -> None:
        self.health_checks += 1

    def bounded_timeout_ms(self, requested_ms: int) -> int:
        return requested_ms

    def stability_navigation_conflicts(self) -> tuple[dict[str, object], ...]:
        return self._navigation_conflicts


class _DocumentPage:
    def __init__(self, title: str, language: str | None) -> None:
        self._title = title
        self._html = _Element(href=language)

    def title(self) -> str:
        return self._title

    def locator(self, selector: str) -> object:
        if selector != "html":
            raise AssertionError("unexpected selector")

        page = self

        class Html:
            def get_attribute(self, name: str, **_kwargs: object) -> object:
                if name != "lang":
                    raise AssertionError("unexpected attribute")
                return page._html.href

        return Html()


def _request(*, projections: list[str]) -> dict[str, object]:
    plan = public_render_plan(projections=projections)
    return derive_public_render_request(
        plan, "github-public-render", "content-window-001"
    )


class PublicRenderContentTests(unittest.TestCase):
    def test_document_identity_uses_frozen_text_normalization(self) -> None:
        result = collect_document_identity(
            _DocumentPage("  A\r\n  B  ", " en-US "), timeout_ms=1000
        )
        self.assertEqual({"title": "A\nB", "html_lang": "en-US"}, result)

    def test_literal_count_is_case_sensitive_and_non_overlapping(self) -> None:
        sample = collect_content_sample(
            _Scope(["aaaa AA"]),
            final_url="https://github.com/owner/repository",
            projections=frozenset(
                {
                    "content.literal_markers",
                    "content.rendered_text_signature",
                }
            ),
            literal_markers=["aa", "AA"],
            viewport={"width": 1365, "height": 768},
            timeout_ms=1000,
        )
        self.assertEqual(
            [
                {"literal": "aa", "rendered_text_occurrences": 2},
                {"literal": "AA", "rendered_text_occurrences": 1},
            ],
            sample.facts["literal_markers"],
        )
        signature = sample.facts["rendered_text_signature"]
        self.assertEqual(7, signature["utf8_byte_length"])
        self.assertEqual(1, signature["line_count"])

    def test_heading_visibility_and_positive_viewport_intersection_are_distinct(
        self,
    ) -> None:
        headings = [
            _Element(
                text="Visible",
                tag_name="H1",
                visible=True,
                box={"x": 0, "y": 0, "width": 10, "height": 10},
            ),
            _Element(
                text="Boundary",
                tag_name="H2",
                visible=True,
                box={"x": 1365, "y": 0, "width": 10, "height": 10},
            ),
            _Element(
                text="Hidden",
                tag_name="H3",
                visible=False,
                box={"x": 5, "y": 5, "width": 10, "height": 10},
            ),
        ]
        sample = collect_content_sample(
            _Scope(["unused"], headings=headings),
            final_url="https://github.com/owner/repository",
            projections=frozenset({"content.headings"}),
            literal_markers=[],
            viewport={"width": 1365, "height": 768},
            timeout_ms=1000,
        )
        items = sample.facts["headings"]["items"]
        self.assertEqual(
            [(True, True), (True, False), (False, True)],
            [
                (item["playwright_visible"], item["in_initial_viewport"])
                for item in items
            ],
        )

    def test_links_preserve_duplicates_and_drop_secret_payloads(self) -> None:
        links = [
            _Element(
                text="One",
                href="/path?token=secret#fragment",
                resolved_href=(
                    "https://github.com/path?token=secret#fragment"
                ),
            ),
            _Element(
                text="One",
                href="/path?token=secret#fragment",
                resolved_href=(
                    "https://github.com/path?token=secret#fragment"
                ),
            ),
            _Element(text="Mail", href="mailto:private@example.com"),
            _Element(text="Bad", href="https://user:pass@example.com/path"),
        ]
        sample = collect_content_sample(
            _Scope(["unused"], links=links),
            final_url="https://github.com/owner/repository",
            projections=frozenset({"content.links"}),
            literal_markers=[],
            viewport={"width": 1365, "height": 768},
            timeout_ms=1000,
        )
        items = sample.facts["links"]["items"]
        self.assertEqual(4, len(items))
        self.assertEqual(items[0]["target"], items[1]["target"])
        self.assertTrue(items[0]["target"]["query_present"])
        self.assertTrue(items[0]["target"]["fragment_present"])
        self.assertEqual({"scheme_class": "mailto"}, items[2]["target"])
        self.assertIsNone(items[3]["target"])
        serialized = json.dumps(sample.facts, sort_keys=True)
        self.assertNotIn("secret", serialized)
        self.assertNotIn("private@example.com", serialized)
        self.assertNotIn("user:pass", serialized)
        self.assertEqual("LINK_TARGET_UNREPRESENTABLE", sample.conflicts[0]["code"])

    def test_text_heading_and_link_limits_are_explicit(self) -> None:
        sample = collect_content_sample(
            _Scope(
                ["x" * (MAX_RENDERED_TEXT_BYTES + 1)],
                headings=[
                    _Element(
                        text=str(index),
                        tag_name="H1",
                        box={"x": 0, "y": 0, "width": 1, "height": 1},
                    )
                    for index in range(MAX_HEADINGS + 1)
                ],
                links=[
                    _Element(text=str(index), href="/safe")
                    for index in range(MAX_LINKS + 1)
                ],
            ),
            final_url="https://github.com/owner/repository",
            projections=frozenset(
                {
                    "content.rendered_text_signature",
                    "content.headings",
                    "content.links",
                }
            ),
            literal_markers=[],
            viewport={"width": 1365, "height": 768},
            timeout_ms=1000,
        )
        self.assertEqual(
            {
                "RENDERED_TEXT_LIMIT_EXCEEDED",
                "HEADING_LIMIT_EXCEEDED",
                "LINK_LIMIT_EXCEEDED",
            },
            {item["code"] for item in sample.truncations},
        )
        self.assertEqual(MAX_HEADINGS, sample.facts["headings"]["retained_count"])
        self.assertEqual(MAX_LINKS, sample.facts["links"]["retained_count"])

    def test_three_samples_must_all_match_to_be_stable(self) -> None:
        stable_session = _Session(_Scope(["same", "same", "same"]))
        stable = collect_content_window(
            stable_session,
            _request(projections=["content.rendered_text_signature"]),
        )
        self.assertTrue(stable.samples_stable)
        self.assertEqual(1, len(set(stable.sample_digests)))
        self.assertEqual([1000, 500, 500], stable_session.delays)

        unstable_session = _Session(_Scope(["one", "two", "two"]))
        unstable = collect_content_window(
            unstable_session,
            _request(projections=["content.rendered_text_signature"]),
        )
        self.assertFalse(unstable.samples_stable)
        self.assertEqual(2, len(set(unstable.sample_digests)))
        self.assertEqual(3, len(unstable.samples))

        navigated_session = _Session(
            _Scope(["same", "same", "same"]),
            ({"code": "MAIN_FRAME_NAVIGATED_DURING_STABILITY"},),
        )
        navigated = collect_content_window(
            navigated_session,
            _request(projections=["content.rendered_text_signature"]),
        )
        self.assertTrue(navigated.samples_stable)
        self.assertEqual(1, len(set(navigated.sample_digests)))
        self.assertEqual(
            "MAIN_FRAME_NAVIGATED_DURING_STABILITY",
            navigated.navigation_conflicts[0]["code"],
        )

    def test_safe_link_and_viewport_helpers_fail_closed(self) -> None:
        self.assertEqual(
            {"scheme_class": "javascript"},
            safe_link_target(
                "javascript:alert('secret')",
                final_url="https://github.com/owner/repository",
            ),
        )
        with self.assertRaises(PublicRenderContentError):
            safe_link_target(
                "https://user@example.com/path",
                final_url="https://github.com/owner/repository",
            )
        self.assertFalse(
            in_initial_viewport(
                {"x": 0, "y": 0, "width": float("nan"), "height": 1},
                {"width": 10, "height": 10},
            )
        )


if __name__ == "__main__":
    unittest.main()
