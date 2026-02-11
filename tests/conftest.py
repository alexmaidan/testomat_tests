import os
from collections.abc import Generator
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.web.application import Application

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        login_url=os.getenv("APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


# =============================================================================
# BROWSER & CONTEXT FIXTURES
# =============================================================================


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright]:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser]:
    browser = playwright_instance.chromium.launch(
        headless=False,
        slow_mo=150,
        timeout=30000,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def context_args() -> dict:
    return {
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kiev",
        "record_video_dir": "videos/",
        "permissions": ["geolocation", "clipboard-read", "clipboard-write"],
    }


# =============================================================================
# 1. CLEAN APP - new page for each test (function scope)
# =============================================================================


@pytest.fixture(scope="function")
def context(browser: Browser, context_args: dict) -> Generator[BrowserContext]:
    ctx = browser.new_context(**context_args)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page]:
    pg = context.new_page()
    yield pg
    pg.close()


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    """Clean app instance - new page for each test."""
    return Application(page)


# =============================================================================
# 2. LOGGED APP - reuses authorization across tests
# =============================================================================


@pytest.fixture(scope="session")
def logged_context(browser: Browser, context_args: dict, configs: Config) -> Generator[BrowserContext]:
    """Session-scoped context with saved login state."""
    ctx = browser.new_context(**context_args)
    pg = ctx.new_page()

    # Perform login once
    app = Application(pg)
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    app.projects_page.is_loaded()

    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def logged_page(logged_context: BrowserContext) -> Generator[Page]:
    """New page in logged context - shares auth cookies."""
    pg = logged_context.new_page()
    yield pg
    pg.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: Page) -> Application:
    """App instance with pre-authenticated user."""
    return Application(logged_page)


# =============================================================================
# 3. REUSED CONTEXT - for parametrized tests (e.g., invalid login)
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


@pytest.fixture(scope="function")
def reused_app(reused_page: Page) -> Application:
    """App with reused context - for parametrized tests like invalid login."""
    return Application(reused_page)


# =============================================================================
# 4. PERSISTENT LOGIN PAGE - same page for all parametrized login tests
# =============================================================================


@pytest.fixture(scope="module")
def persistent_login_page(reused_context: BrowserContext) -> Generator[Page]:
    """Module-scoped page - keeps the same page for all tests in module."""
    pg = reused_context.new_page()
    yield pg
    pg.close()


@pytest.fixture(scope="module")
def persistent_login_app(persistent_login_page: Page) -> Application:
    """
    App with persistent page - navigates to login page once.
    All parametrized tests reuse the same page without reopening.
    """
    app = Application(persistent_login_page)
    app.login_page.open()
    app.login_page.is_loaded()
    return app


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


@pytest.fixture(scope="function")
def clean_app(clean_page: Page) -> Application:
    """App instance with cleared storage - ensures clean state."""
    return Application(clean_page)
