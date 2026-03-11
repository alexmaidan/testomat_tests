"""Playwright browser and context fixtures for pytest."""

from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

# =============================================================================
# BROWSER & CONTEXT FIXTURES
# =============================================================================


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright]:
    """Session-scoped Playwright instance."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser]:
    """Session-scoped browser instance."""
    browser = playwright_instance.chromium.launch(
        headless=False,
        slow_mo=150,
        timeout=30000,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def context_args() -> dict:
    """Default browser context arguments."""
    return {
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kiev",
        "record_video_dir": "videos/",
        "permissions": ["geolocation", "clipboard-read", "clipboard-write"],
    }


# =============================================================================
# 1. CLEAN CONTEXT - new page for each test (function scope)
# =============================================================================


@pytest.fixture(scope="function")
def context(browser: Browser, context_args: dict) -> Generator[BrowserContext]:
    """Function-scoped browser context - new context for each test."""
    ctx = browser.new_context(**context_args)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page]:
    """Function-scoped page - new page for each test."""
    pg = context.new_page()
    yield pg
    pg.close()


# =============================================================================
# 2. REUSED CONTEXT - for parametrized tests (e.g., invalid login)
# =============================================================================


@pytest.fixture(scope="module")
def reused_context(browser: Browser, context_args: dict) -> Generator[BrowserContext]:
    """Module-scoped context - reused across parametrized tests."""
    ctx = browser.new_context(**context_args)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def reused_page(reused_context: BrowserContext) -> Generator[Page]:
    """New page in reused context - faster for parametrized tests."""
    pg = reused_context.new_page()
    yield pg
    pg.close()


# =============================================================================
# 3. PERSISTENT PAGE - same page for all parametrized tests in module
# =============================================================================


@pytest.fixture(scope="module")
def persistent_page(reused_context: BrowserContext) -> Generator[Page]:
    """Module-scoped page - keeps the same page for all tests in module."""
    pg = reused_context.new_page()
    yield pg
    pg.close()


# =============================================================================
# CLEANUP UTILITIES
# =============================================================================


def clear_browser_data(context: BrowserContext, page: Page = None) -> None:
    """
    Clear cookies and local storage for a browser context.

    Args:
        context: BrowserContext to clear cookies from
        page: Optional Page to clear local/session storage from
    """
    # Clear all cookies from context
    context.clear_cookies()

    # Clear local storage and session storage if page is provided
    if page and not page.is_closed():
        page.evaluate("""
            () => {
                localStorage.clear();
                sessionStorage.clear();
            }
        """)


def clear_all_storage(page: Page) -> None:
    """
    Clear all browser storage (cookies, local storage, session storage) for a page.

    Args:
        page: Page to clear storage from
    """
    # Clear cookies from the page's context
    page.context.clear_cookies()

    # Clear local and session storage
    page.evaluate("""
        () => {
            localStorage.clear();
            sessionStorage.clear();
        }
    """)


@pytest.fixture(scope="function")
def clean_page(page: Page) -> Generator[Page]:
    """Page fixture that clears all storage before and after test."""
    clear_all_storage(page)
    yield page
    clear_all_storage(page)
