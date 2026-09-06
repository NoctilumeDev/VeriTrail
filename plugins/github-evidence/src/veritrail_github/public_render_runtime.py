from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as distribution_version
from pathlib import Path


PLAYWRIGHT_VERSION = "1.62.0"
BROWSER_ENGINE = "CHROMIUM"
BROWSER_DISTRIBUTION = "BUNDLED_MATCHING"


class RenderRuntimeUnavailable(RuntimeError):
    """The explicitly installed P2 browser capability is not ready."""


@dataclass(frozen=True)
class RenderRuntimePreflight:
    playwright_version: str
    browser_engine: str
    browser_distribution: str
    browser_version: str


def preflight_render_runtime() -> RenderRuntimePreflight:
    """Verify the frozen Playwright runtime without installing or substituting it."""

    try:
        installed_version = distribution_version("playwright")
    except PackageNotFoundError as error:
        raise RenderRuntimeUnavailable(
            "P2 render capability requires the explicit 'render' extra"
        ) from error
    if installed_version != PLAYWRIGHT_VERSION:
        raise RenderRuntimeUnavailable(
            "P2 render capability requires exactly "
            f"playwright=={PLAYWRIGHT_VERSION}"
        )

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RenderRuntimeUnavailable(
            "the installed Playwright distribution cannot load its sync API"
        ) from error

    browser = None
    try:
        with sync_playwright() as playwright:
            bundled_executable = Path(playwright.chromium.executable_path)
            if not bundled_executable.is_file():
                raise RenderRuntimeUnavailable(
                    "matching bundled Chromium is not preinstalled"
                )
            browser = playwright.chromium.launch(headless=True)
            browser_version = browser.version
            browser.close()
            browser = None
    except RenderRuntimeUnavailable:
        raise
    except Exception as error:
        raise RenderRuntimeUnavailable(
            "matching bundled Chromium failed its launch preflight"
        ) from error
    finally:
        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass

    return RenderRuntimePreflight(
        playwright_version=installed_version,
        browser_engine=BROWSER_ENGINE,
        browser_distribution=BROWSER_DISTRIBUTION,
        browser_version=browser_version,
    )
