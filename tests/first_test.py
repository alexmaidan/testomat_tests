"""Legacy integration tests - consider migrating to page object pattern.

These tests demonstrate basic Playwright functionality and may be useful
for quick validation. For new tests, prefer using page objects in tests/web/.
"""

import pytest
from playwright.sync_api import Page, expect

from src.utils.helpers import generate_random_password
from src.web.application import Application
from tests.conftest import Config
from tests.data.test_data import TestProjects, TestCompanies


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    """Login fixture using page objects."""
    page.goto(configs.login_url)
    page.locator("#content-desktop #user_email").fill(configs.email)
    page.locator("#content-desktop #user_password").fill(configs.password)
    page.get_by_role("button", name="Sign in").click()


def test_login_with_invalid_creds(app: Application, configs: Config):
    """Test login with invalid credentials shows error message."""
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    invalid_password = generate_random_password()
    app.login_page.login_user(configs.email, invalid_password)
    app.login_page.has_invalid_login_message()


def test_search_project_in_company(page: Page, login):
    """Test project search functionality."""
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(TestProjects.TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TestProjects.TARGET_PROJECT)).to_be_visible()


def test_should_be_possible_to_filter_by_free_projects(page: Page, login):
    """Test filtering projects by Free Projects company."""
    page.locator("#company_id").click()
    page.locator("#company_id").select_option(TestCompanies.FREE_PROJECTS)
    page.locator("#content-desktop #search").fill(TestProjects.TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TestProjects.TARGET_PROJECT)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def test_hover_features_menu(app: Application):
    """Test features menu hover interaction."""
    app.home_page.open()
    app.home_page.is_loaded()

    app.page.get_by_role("link", name="Features", exact=True).hover()
    expect(app.page.get_by_text("Explore features")).to_be_visible()


def test_social_media_links(app: Application):
    """Test social media link opens correct URL."""
    app.home_page.open()
    app.home_page.is_loaded()

    with app.page.context.expect_page() as new_page_info:
        app.page.locator(".socials > a").first.click()
    new_page = new_page_info.value
    expect(new_page).to_have_url("https://x.com/testomatio")


