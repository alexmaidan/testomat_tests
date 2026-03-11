"""Application fixtures for pytest."""

import json
from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.application import Application
from tests.conftest import TEST_RESULT_DIR
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper, save_storage_state

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_STATE_PATH = Path("test-result/.auth/free_project_state.json")
TRACES_DIR = TEST_RESULT_DIR / "traces"


# =============================================================================
# BROWSER CONTEXT BUILDER
# =============================================================================


def get_or_create_context(
    browser: Browser,
    base_url: str,
    storage_path: Path | None = None,
) -> tuple[BrowserContext, bool]:
    """Create a browser context, optionally restoring state from *storage_path*.

    Returns:
        A tuple of (context, needs_login) where *needs_login* is ``True``
        when no saved state was loaded.
    """
    has_state = storage_path is not None and storage_path.exists()

    kwargs: dict = {
        "base_url": base_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": str(TEST_RESULT_DIR / "videos"),
        "permissions": ["geolocation"],
    }
    if has_state:
        kwargs["storage_state"] = str(storage_path)

    context = browser.new_context(**kwargs)
    return context, not has_state


# =============================================================================
# 1. CLEAN APP - new page for each test (function scope)
# =============================================================================


@pytest.fixture(scope="function")
def app(browser: Browser, configs: Config) -> Generator[Application]:
    """Clean app instance - new page for each test."""
    context, _ = get_or_create_context(browser, configs.app_base_url)
    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


# =============================================================================
# 2. LOGGED APP - reuses authorization across tests (with cookie caching)
# =============================================================================


def create_free_project_state() -> None:
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
def logged_page(browser: Browser, configs: Config) -> Generator[Page]:
    """Session-scoped page with login - reuses auth state via storage."""
    context, needs_login = get_or_create_context(browser, configs.app_base_url, STORAGE_STATE_PATH)
    page = context.new_page()

    if needs_login:
        open_login_and_authorize(configs, page)
        save_storage_state(context, STORAGE_STATE_PATH)
        create_free_project_state()

    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: Page, request: pytest.FixtureRequest) -> Generator[Application]:
    start_tracing(logged_page)
    logged_page.goto("/projects")

    yield Application(logged_page)

    stop_tracing_on_failure(logged_page, request)


# =============================================================================
# 3. FREE PROJECT CONTEXT/APP - logged in without company/project context
# =============================================================================


@pytest.fixture(scope="session")
def free_project_page(browser: Browser, configs: Config) -> Generator[Page]:
    """Session-scoped page in the Free Projects company context."""
    context, needs_login = get_or_create_context(
        browser,
        configs.app_base_url,
        FREE_PROJECT_STORAGE_STATE_PATH,
    )
    page = context.new_page()

    if needs_login:
        app = open_login_and_authorize(configs, page)

        app.projects_page.is_loaded()
        app.projects_page.open()
        app.projects_page.header.select_company("Free Projects")
        expect(app.projects_page.header.free_plan_label).to_be_visible()

        save_storage_state(context, FREE_PROJECT_STORAGE_STATE_PATH)

    yield page
    context.close()


def open_login_and_authorize(configs: Config, page: Page) -> Application:
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    return app


@pytest.fixture(scope="function")
def free_project_app(free_project_page: Page, request: pytest.FixtureRequest) -> Generator[Application]:
    """App instance authenticated in the Free Projects company context."""
    start_tracing(free_project_page)
    free_project_page.goto("/projects")

    yield Application(free_project_page)

    stop_tracing_on_failure(free_project_page, request)


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
def shared_browser(browser: Browser, configs: Config) -> Generator[Page]:
    """Shared page for parametrized tests (module scope) - reuses same page across test params."""
    context, _ = get_or_create_context(browser, configs.app_base_url)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Generator[Application]:
    """Shared page with state clearing between tests."""
    yield Application(shared_browser)


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


def start_tracing(page: Page) -> None:
    """Start tracing on the browser context."""
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_tracing_on_failure(page: Page, request: pytest.FixtureRequest) -> None:
    """Stop tracing; save trace file only when the test has failed."""
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        trace_path = TRACES_DIR / f"trace-{request.node.name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        page.context.tracing.stop(path=str(trace_path))
    else:
        page.context.tracing.stop()
