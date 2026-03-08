"""Application fixtures for pytest."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_STATE_PATH = Path("test-result/.auth/free_project_state.json")


# =============================================================================
# BROWSER CONTEXT BUILDER
# =============================================================================


def build_browser_context(
    browser: Browser,
    base_url: str,
    storage_state: Path | None = None,
) -> BrowserContext:
    """Build a browser context with standard settings."""
    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "test-result/videos/",
        "permissions": ["geolocation"],
    }
    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)
    return browser.new_context(**kwargs)


# =============================================================================
# 1. CLEAN APP - new page for each test (function scope)
# =============================================================================


@pytest.fixture(scope="function")
def app(browser: Browser, configs: Config) -> Application:
    """Clean app instance - new page for each test."""
    context = build_browser_context(browser, configs.base_url)
    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


# =============================================================================
# 2. LOGGED APP - reuses authorization across tests (with cookie caching)
# =============================================================================


def _save_free_project_storage_state() -> None:
    """
    Create free project storage state by copying storage state with empty company_id.

    This creates a storage state file that can be used for tests that require
    a logged-in user without any company/project context.
    """
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text(encoding="utf-8"))
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


@pytest.fixture(scope="session")
def logged_page(browser: Browser, configs: Config) -> Page:
    """
    Session-scoped page with saved login state.

    Optimization: Tries to restore session from cached cookies first,
    only performs full login if cached session is invalid or missing.
    """
    if STORAGE_STATE_PATH.exists():
        context = build_browser_context(browser, configs.base_url, storage_state=STORAGE_STATE_PATH)
        yield context.new_page()
        context.close()
        return

    context = build_browser_context(browser, configs.base_url)
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)

    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_STATE_PATH)
    _save_free_project_storage_state()

    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: Page) -> Application:
    """App instance with pre-authenticated user."""
    logged_page.goto("/projects")
    yield Application(logged_page)
    logged_page.close()


# =============================================================================
# 3. FREE PROJECT CONTEXT/APP - logged in without company/project context
# =============================================================================


@pytest.fixture(scope="session")
def free_project_page(browser: Browser, configs: Config) -> Page:
    """
    Session-scoped page authenticated in the Free Projects company context.

    Uses the free project storage state if available, otherwise logs in and
    selects the 'Free Projects' company via the UI.
    Opens only one browser window regardless of other session fixtures.
    """
    if FREE_PROJECT_STORAGE_STATE_PATH.exists():
        context = build_browser_context(browser, configs.base_url, storage_state=FREE_PROJECT_STORAGE_STATE_PATH)
        yield context.new_page()
        context.close()
        return

    context = build_browser_context(browser, configs.base_url)
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)

    app.projects_page.is_loaded()
    app.projects_page.open()
    app.projects_page.header.select_company("Free Projects")
    expect(app.projects_page.header.free_plan_label).to_be_visible()

    FREE_PROJECT_STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=FREE_PROJECT_STORAGE_STATE_PATH)

    yield page
    context.close()


@pytest.fixture(scope="function")
def free_project_app(free_project_page: Page) -> Application:
    """App instance authenticated in the Free Projects company context."""
    free_project_page.goto("/projects")
    yield Application(free_project_page)
    free_project_page.close()


# =============================================================================
# 4. REUSED APP - for parametrized tests (e.g., invalid login)
# =============================================================================


@pytest.fixture(scope="function")
def reused_app(reused_page: Page) -> Application:
    """App with reused context - for parametrized tests like invalid login."""
    return Application(reused_page)


# =============================================================================
# 5. PERSISTENT LOGIN APP - same page for all parametrized login tests
# =============================================================================


@pytest.fixture(scope="module")
def shared_browser(browser: Browser, configs: Config) -> Page:
    """Shared page for parametrized tests (module scope) - reuses same page across test params."""
    context = build_browser_context(browser, configs.base_url)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Application:
    """Shared page with state clearing between tests."""
    yield Application(shared_browser)


@pytest.fixture(scope="module")
def persistent_login_page(reused_context: BrowserContext) -> Page:
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
# 6. CLEAN APP - with cleared storage
# =============================================================================


@pytest.fixture(scope="function")
def clean_app(clean_page: Page) -> Application:
    """App instance with cleared storage - ensures clean state."""
    return Application(clean_page)


# =============================================================================
# 7. COOKIE HELPER - for managing cookies in tests
# =============================================================================


@pytest.fixture(scope="function")
def cookies(logged_page: Page) -> CookieHelper:
    """Cookie helper for managing cookies in logged context."""
    return CookieHelper(logged_page.context)


# =============================================================================
# 8. SESSION VALIDATION UTILITIES
# =============================================================================


def is_session_valid(page: Page) -> bool:
    """
    Check if the current page session is valid.

    Args:
        page: Page to check

    Returns:
        True if session appears valid, False otherwise
    """
    current_url = page.url
    return "/login" not in current_url and "/sign_in" not in current_url


def ensure_authenticated(app: Application, configs: Config) -> None:
    """
    Ensure the app is authenticated, logging in if necessary.


    Args:
        app: Application instance
        configs: Configuration with login credentials
    """
    if is_session_valid(app.page):
        return

    app.home_page.open()
    app.home_page.click_login()
    app.login_page.login_user(configs.email, configs.password)
    app.projects_page.is_loaded()
