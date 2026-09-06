from __future__ import annotations

import hashlib
import math
import unicodedata
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urljoin, urlsplit

from veritrail.canonical import sha256_json
from veritrail_github.errors import CollectionError
from veritrail_github.public_render_contracts import (
    PUBLIC_RENDER_VIEWPORTS,
    normalize_rendered_text,
)
from veritrail_github.public_render_navigation import safe_public_url_facts


NORMALIZATION_SEMANTICS_VERSION = "github-public-render-facts/0.1"
MAX_RENDERED_TEXT_BYTES = 524_288
MAX_HEADINGS = 256
MAX_LINKS = 512


class PublicRenderContentError(CollectionError):
    """A fixed-scope DOM observation cannot be represented safely."""


@dataclass(frozen=True)
class ContentSample:
    digest: str
    facts: dict[str, Any]
    truncations: tuple[dict[str, Any], ...]
    conflicts: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class ContentWindow:
    samples_stable: bool
    sample_digests: tuple[str, ...]
    samples: tuple[ContentSample, ...]
    navigation_conflicts: tuple[dict[str, Any], ...]


def collect_document_identity(page: Any, *, timeout_ms: int) -> dict[str, Any]:
    """Collect only the normalized title and root language declaration."""

    try:
        title = normalize_rendered_text(page.title())
        language = page.locator("html").get_attribute("lang", timeout=timeout_ms)
    except Exception as error:
        raise PublicRenderContentError(
            "P2 document identity extraction failed"
        ) from error
    if language is not None:
        try:
            language = normalize_rendered_text(language)
        except Exception as error:
            raise PublicRenderContentError(
                "P2 document language is not representable"
            ) from error
    return {"title": title, "html_lang": language}


def collect_content_window(
    session: Any, verified_request: Mapping[str, Any]
) -> ContentWindow:
    """Take the frozen three fixed-scope samples without selecting an unstable one."""

    try:
        spec = verified_request["observation_spec"]
        projections = frozenset(spec["projections"])
        coordinates = spec["coordinates"]
        policy = verified_request["render_policy"]
        sample_count = policy["sample_count"]
        settle_delay_ms = policy["settle_delay_ms"]
        sample_interval_ms = policy["sample_interval_ms"]
        scope_timeout_ms = policy["scope_timeout_ms"]
        viewport = PUBLIC_RENDER_VIEWPORTS[coordinates["viewport_profile"]]
    except (KeyError, TypeError) as error:
        raise PublicRenderContentError(
            "P2 content sampling requires a validated Render request"
        ) from error
    if sample_count != 3:
        raise PublicRenderContentError("P2 content sampling requires exactly 3 samples")

    scope = session.scope_locator
    session.wait_for_policy_delay(settle_delay_ms)
    samples: list[ContentSample] = []
    for index in range(sample_count):
        session.assert_healthy()
        timeout_ms = session.bounded_timeout_ms(scope_timeout_ms)
        samples.append(
            collect_content_sample(
                scope,
                final_url=session.page.url,
                projections=projections,
                literal_markers=coordinates.get("literal_markers", []),
                viewport=viewport,
                timeout_ms=timeout_ms,
            )
        )
        session.assert_healthy()
        if index + 1 < sample_count:
            session.wait_for_policy_delay(sample_interval_ms)
    digests = tuple(sample.digest for sample in samples)
    navigation_conflicts = session.stability_navigation_conflicts()
    return ContentWindow(
        samples_stable=len(set(digests)) == 1,
        sample_digests=digests,
        samples=tuple(samples),
        navigation_conflicts=navigation_conflicts,
    )


def collect_content_sample(
    scope: Any,
    *,
    final_url: str,
    projections: frozenset[str],
    literal_markers: list[str],
    viewport: Mapping[str, int],
    timeout_ms: int,
) -> ContentSample:
    facts: dict[str, Any] = {}
    truncations: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []

    needs_text = bool(
        {
            "content.rendered_text_signature",
            "content.literal_markers",
        }
        & projections
    )
    normalized_text = ""
    if needs_text:
        try:
            normalized_text = normalize_rendered_text(
                scope.inner_text(timeout=timeout_ms)
            )
        except Exception as error:
            raise PublicRenderContentError(
                "P2 fixed-scope innerText extraction failed"
            ) from error
        encoded_text = normalized_text.encode("utf-8")
        text_signature = {
            "sha256": hashlib.sha256(encoded_text).hexdigest(),
            "utf8_byte_length": len(encoded_text),
            "line_count": 0 if not normalized_text else normalized_text.count("\n") + 1,
        }
        if len(encoded_text) > MAX_RENDERED_TEXT_BYTES:
            truncations.append(
                {
                    "code": "RENDERED_TEXT_LIMIT_EXCEEDED",
                    "observed_utf8_bytes": len(encoded_text),
                    "limit_utf8_bytes": MAX_RENDERED_TEXT_BYTES,
                }
            )
        if "content.rendered_text_signature" in projections:
            facts["rendered_text_signature"] = text_signature
        if "content.literal_markers" in projections:
            facts["literal_markers"] = [
                {
                    "literal": literal,
                    "rendered_text_occurrences": normalized_text.count(literal),
                }
                for literal in literal_markers
            ]

    if "content.headings" in projections:
        heading_facts, heading_truncations = _collect_headings(
            scope, viewport=viewport, timeout_ms=timeout_ms
        )
        facts["headings"] = heading_facts
        truncations.extend(heading_truncations)

    if "content.links" in projections:
        link_facts, link_truncations, link_conflicts = _collect_links(
            scope, final_url=final_url, timeout_ms=timeout_ms
        )
        facts["links"] = link_facts
        truncations.extend(link_truncations)
        conflicts.extend(link_conflicts)

    digest_input = {
        "normalization_semantics_version": NORMALIZATION_SEMANTICS_VERSION,
        "facts": facts,
        "truncations": truncations,
        "conflicts": conflicts,
    }
    return ContentSample(
        digest=sha256_json(digest_input),
        facts=facts,
        truncations=tuple(truncations),
        conflicts=tuple(conflicts),
    )


def safe_link_target(
    raw_href: Any,
    *,
    final_url: str,
    browser_resolved_href: Any | None = None,
) -> dict[str, Any]:
    """Resolve a link while retaining no query value or non-HTTPS payload."""

    if not isinstance(raw_href, str):
        raise PublicRenderContentError("P2 link href is not text")
    if any(
        unicodedata.category(character) in {"Cc", "Cs"}
        for character in raw_href
    ):
        raise PublicRenderContentError("P2 link href contains unsafe text")
    try:
        parsed = urlsplit(raw_href)
        _ = parsed.port
    except ValueError as error:
        raise PublicRenderContentError("P2 link href cannot be parsed") from error
    if parsed.username is not None or parsed.password is not None:
        raise PublicRenderContentError("P2 link href contains userinfo")
    scheme = parsed.scheme.casefold()
    if scheme and scheme != "https":
        return {"scheme_class": scheme}
    try:
        resolved = (
            urljoin(final_url, raw_href)
            if browser_resolved_href is None
            else browser_resolved_href
        )
        if not isinstance(resolved, str):
            raise PublicRenderContentError(
                "P2 browser-resolved link href is not text"
            )
        resolved_scheme = urlsplit(resolved).scheme.casefold()
        if resolved_scheme != "https":
            return {"scheme_class": resolved_scheme or "unknown"}
        return {"scheme_class": "https", **safe_public_url_facts(resolved)}
    except Exception as error:
        raise PublicRenderContentError(
            "P2 link target cannot be represented safely"
        ) from error


def in_initial_viewport(
    box: Mapping[str, Any] | None, viewport: Mapping[str, int]
) -> bool:
    if not isinstance(box, Mapping):
        return False
    values = [box.get(key) for key in ("x", "y", "width", "height")]
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for value in values
    ):
        return False
    x, y, width, height = values
    if width <= 0 or height <= 0:
        return False
    return (
        max(x, 0) < min(x + width, viewport["width"])
        and max(y, 0) < min(y + height, viewport["height"])
    )


def _collect_headings(
    scope: Any, *, viewport: Mapping[str, int], timeout_ms: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    locator = scope.locator("h1, h2, h3, h4, h5, h6")
    try:
        observed_count = _validated_element_count(locator.count(), "heading")
    except Exception as error:
        raise PublicRenderContentError("P2 heading count failed") from error
    retained_count = min(observed_count, MAX_HEADINGS)
    items: list[dict[str, Any]] = []
    for index in range(retained_count):
        heading = locator.nth(index)
        try:
            tag_name = heading.evaluate(
                "element => element.tagName", timeout=timeout_ms
            )
            text = normalize_rendered_text(heading.inner_text(timeout=timeout_ms))
            playwright_visible = heading.is_visible(timeout=timeout_ms)
            box = heading.bounding_box(timeout=timeout_ms)
        except Exception as error:
            raise PublicRenderContentError(
                "P2 heading extraction failed"
            ) from error
        if not isinstance(tag_name, str) or tag_name.upper() not in {
            "H1",
            "H2",
            "H3",
            "H4",
            "H5",
            "H6",
        }:
            raise PublicRenderContentError("P2 heading level is invalid")
        if not isinstance(playwright_visible, bool):
            raise PublicRenderContentError("P2 heading visibility is invalid")
        items.append(
            {
                "level": int(tag_name[1]),
                "text": text,
                "playwright_visible": playwright_visible,
                "in_initial_viewport": in_initial_viewport(box, viewport),
            }
        )
    result = {
        "observed_count": observed_count,
        "retained_count": retained_count,
        "limit": MAX_HEADINGS,
        "items": items,
    }
    truncations: list[dict[str, Any]] = []
    if observed_count > MAX_HEADINGS:
        truncations.append(
            {
                "code": "HEADING_LIMIT_EXCEEDED",
                "observed_count": observed_count,
                "limit": MAX_HEADINGS,
            }
        )
    return result, truncations


def _collect_links(
    scope: Any, *, final_url: str, timeout_ms: int
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    locator = scope.locator("a[href]")
    try:
        observed_count = _validated_element_count(locator.count(), "link")
    except Exception as error:
        raise PublicRenderContentError("P2 link count failed") from error
    retained_count = min(observed_count, MAX_LINKS)
    items: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for index in range(retained_count):
        link = locator.nth(index)
        try:
            text = normalize_rendered_text(link.inner_text(timeout=timeout_ms))
        except Exception as error:
            raise PublicRenderContentError(
                "P2 link text extraction failed"
            ) from error
        try:
            raw_href = link.get_attribute("href", timeout=timeout_ms)
            browser_resolved_href = link.evaluate(
                "element => element.href", timeout=timeout_ms
            )
        except Exception as error:
            raise PublicRenderContentError(
                "P2 link href extraction failed"
            ) from error
        try:
            target = safe_link_target(
                raw_href,
                final_url=final_url,
                browser_resolved_href=browser_resolved_href,
            )
        except Exception:
            target = None
            conflicts.append(
                {
                    "code": "LINK_TARGET_UNREPRESENTABLE",
                    "ordinal": index + 1,
                }
            )
        items.append(
            {
                "ordinal": index + 1,
                "text": text,
                "target": target,
            }
        )
    result = {
        "observed_count": observed_count,
        "retained_count": retained_count,
        "limit": MAX_LINKS,
        "items": items,
    }
    truncations: list[dict[str, Any]] = []
    if observed_count > MAX_LINKS:
        truncations.append(
            {
                "code": "LINK_LIMIT_EXCEEDED",
                "observed_count": observed_count,
                "limit": MAX_LINKS,
            }
        )
    return result, truncations, conflicts


def _validated_element_count(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise PublicRenderContentError(f"P2 {label} count is invalid")
    return value
