"""Application fixtures for pytest."""

from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")

# =============================================================================
# 1. CLEAN APP - new page for each test (function scope)
# =============================================================================


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

    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ctx.storage_state(path=STORAGE_STATE_PATH)

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
# 3. REUSED APP - for parametrized tests (e.g., invalid login)
# =============================================================================


@pytest.fixture(scope="function")
def reused_app(reused_page: Page) -> Application:
    """App with reused context - for parametrized tests like invalid login."""
    return Application(reused_page)


# =============================================================================
# 4. PERSISTENT LOGIN APP - same page for all parametrized login tests
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
# 5. CLEAN APP - with cleared storage
# =============================================================================


@pytest.fixture(scope="function")
def clean_app(clean_page: Page) -> Application:
    """App instance with cleared storage - ensures clean state."""
    return Application(clean_page)


# =============================================================================
# 6. COOKIE HELPER - for managing cookies in tests
# =============================================================================


@pytest.fixture(scope="function")
def cookies(logged_context: BrowserContext) -> CookieHelper:
    """Cookie helper for managing cookies in logged context."""
    return CookieHelper(logged_context)
