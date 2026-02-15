"""Application fixtures for pytest."""

from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper, is_session_cookie_valid

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")

# =============================================================================
# 1. CLEAN APP - new page for each test (function scope)
# =============================================================================


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    """Clean app instance - new page for each test."""
    return Application(page)


# =============================================================================
# 2. LOGGED APP - reuses authorization across tests (with cookie caching)
# =============================================================================


def _try_restore_session(browser: Browser, context_args: dict) -> BrowserContext | None:
    """
    Try to restore session from cached storage state.

    Returns:
        BrowserContext with restored session, or None if restoration failed
    """
    if not STORAGE_STATE_PATH.exists():
        return None

    try:
        ctx = browser.new_context(**context_args, storage_state=STORAGE_STATE_PATH)
        pg = ctx.new_page()

        # Navigate to app to check if session is valid
        pg.goto("/projects")

        # Check if we're still logged in (not redirected to login page)
        if "/login" in pg.url or "/sign_in" in pg.url:
            pg.close()
            ctx.close()
            return None

        # Session is valid - check for valid session cookie
        if is_session_cookie_valid(ctx):
            pg.close()
            return ctx

        pg.close()
        ctx.close()
        return None
    except Exception:
        return None


def _perform_fresh_login(browser: Browser, context_args: dict, configs: Config) -> BrowserContext:
    """
    Perform a fresh login and save the session state.

    Returns:
        BrowserContext with fresh login session
    """
    ctx = browser.new_context(**context_args)
    pg = ctx.new_page()

    # Perform login
    app = Application(pg)
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    app.projects_page.is_loaded()

    # Save storage state for future runs
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ctx.storage_state(path=STORAGE_STATE_PATH)

    pg.close()
    return ctx


@pytest.fixture(scope="session")
def logged_context(browser: Browser, context_args: dict, configs: Config) -> Generator[BrowserContext]:
    """
    Session-scoped context with saved login state.

    Optimization: Tries to restore session from cached cookies first,
    only performs full login if cached session is invalid or missing.
    """
    # Try to restore from cached session cookies first
    ctx = _try_restore_session(browser, context_args)

    if ctx is None:
        # Cached session invalid or missing - perform fresh login
        ctx = _perform_fresh_login(browser, context_args, configs)

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


# =============================================================================
# 7. QUICK LOGIN APP - optimized for speed using storage state
# =============================================================================


@pytest.fixture(scope="function")
def quick_login_app(browser: Browser, context_args: dict, configs: Config) -> Generator[Application]:
    """
    Function-scoped app with cookie-based login optimization.

    Uses cached storage state if available and valid, otherwise performs
    login and caches for future use. Each test gets a fresh page but
    shares the authenticated session.

    Use this when you need:
    - Isolated page per test (function scope)
    - Fast authentication via cookies
    - Clean page state between tests
    """
    if STORAGE_STATE_PATH.exists():
        try:
            ctx = browser.new_context(**context_args, storage_state=STORAGE_STATE_PATH)
            pg = ctx.new_page()
            pg.goto("/projects")

            # Verify session is valid
            if "/login" not in pg.url and "/sign_in" not in pg.url:
                app = Application(pg)
                yield app
                pg.close()
                ctx.close()
                return

            pg.close()
            ctx.close()
        except Exception:
            pass

    # Fallback to fresh login
    ctx = browser.new_context(**context_args)
    pg = ctx.new_page()
    app = Application(pg)
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    app.projects_page.is_loaded()

    # Save for future use
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ctx.storage_state(path=STORAGE_STATE_PATH)

    yield app
    pg.close()
    ctx.close()


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

    Use this helper in tests that need to verify authentication
    state before proceeding.

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
