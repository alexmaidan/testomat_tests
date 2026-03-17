import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from tests.data.test_data import TestCompanies, TestPlans, TestProjects
from tests.fixtures.config import Config


def _visible_card_count(driver: WebDriver) -> int:
    """Return count of visible project cards (excludes CSS-hidden elements)."""
    return sum(
        1 for el in driver.find_elements(By.CSS_SELECTOR, "#grid ul.grid > li")
        if el.is_displayed()
    )


@pytest.fixture
def projects_page(logged_driver: WebDriver, configs: Config) -> WebDriver:
    """Navigate to projects page, verify it's loaded with expected company and plan."""
    wait = WebDriverWait(logged_driver, 10)
    logged_driver.get(configs.app_base_url)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#grid ul.grid")))

    select = Select(logged_driver.find_element(By.CSS_SELECTOR, "#company_id"))
    assert select.first_selected_option.text == TestCompanies.DEFAULT_COMPANY

    plan_badge = logged_driver.find_element(By.CSS_SELECTOR, ".tooltip-project-plan")
    assert TestPlans.ENTERPRISE.lower() in plan_badge.text.lower()

    return logged_driver


class TestProjectsPageLoaded:

    def test_projects_page_is_loaded_after_login(self, projects_page: WebDriver):
        assert projects_page.find_element(By.CSS_SELECTOR, ".common-page-header h2").text == "Projects"
        assert projects_page.find_element(By.CSS_SELECTOR, "#grid ul.grid").is_displayed()

    def test_projects_page_has_create_button(self, projects_page: WebDriver):
        create_btn = projects_page.find_element(By.CSS_SELECTOR, ".common-page-header a.common-btn-primary")
        assert create_btn.is_displayed()
        assert create_btn.text == "Create"

    def test_projects_page_displays_plan_badge(self, projects_page: WebDriver):
        plan_badge = projects_page.find_element(By.CSS_SELECTOR, ".tooltip-project-plan")
        assert "plan" in plan_badge.text.lower()


class TestProjectsSearch:
    """Tests for project search functionality."""

    def test_search_project_by_name(self, projects_page: WebDriver):
        initial_count = _visible_card_count(projects_page)

        search_input = projects_page.find_element(By.CSS_SELECTOR, ".common-page-header input#search")
        search_input.send_keys(TestProjects.TARGET_PROJECT)

        wait = WebDriverWait(projects_page, 10)
        wait.until(lambda d: _visible_card_count(d) == 1)

        assert _visible_card_count(projects_page) <= initial_count

    def test_clear_search_restores_projects(self, projects_page: WebDriver):
        initial_count = _visible_card_count(projects_page)

        search_input = projects_page.find_element(By.CSS_SELECTOR, ".common-page-header input#search")
        search_input.send_keys(TestProjects.TARGET_PROJECT)

        wait = WebDriverWait(projects_page, 10)
        wait.until(lambda d: _visible_card_count(d) == 1)

        # Use Ctrl+A + Delete to clear the input and trigger the JS input event
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)
        wait.until(lambda d: _visible_card_count(d) == initial_count)

        assert _visible_card_count(projects_page) == initial_count


class TestProjectCards:

    def test_project_card_displays_title(self, projects_page: WebDriver):
        card = projects_page.find_elements(By.CSS_SELECTOR, "#grid ul.grid > li")[0]
        title = card.find_element(By.CSS_SELECTOR, "h3")
        assert title.is_displayed()
        assert title.text != ""

    def test_project_card_displays_tests_count(self, projects_page: WebDriver):
        card = projects_page.find_elements(By.CSS_SELECTOR, "#grid ul.grid > li")[0]
        tests_count = card.find_element(By.CSS_SELECTOR, "p.text-gray-500")
        assert "tests" in tests_count.text.lower()

    def test_project_card_displays_badge(self, projects_page: WebDriver):
        card = projects_page.find_elements(By.CSS_SELECTOR, "#grid ul.grid > li")[0]
        badge = card.find_element(By.CSS_SELECTOR, ".project-badges .common-badge")
        assert badge.text != ""

    def test_project_card_has_href(self, projects_page: WebDriver):
        card = projects_page.find_elements(By.CSS_SELECTOR, "#grid ul.grid > li")[0]
        link = card.find_element(By.CSS_SELECTOR, "a")
        assert "/projects/" in link.get_attribute("href")

    def test_project_card_displays_member_avatars(self, projects_page: WebDriver):
        card = projects_page.find_elements(By.CSS_SELECTOR, "#grid ul.grid > li")[0]
        avatars = card.find_elements(By.CSS_SELECTOR, ".inline-flex img")
        assert len(avatars) > 0


class TestProfileMenu:

    def test_open_profile_menu(self, projects_page: WebDriver):
        projects_page.find_element(By.CSS_SELECTOR, "#toggle-profile-menu").click()
        WebDriverWait(projects_page, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#profile-menu"))
        )
        assert projects_page.find_element(By.CSS_SELECTOR, "#profile-menu").is_displayed()

    def test_profile_menu_contains_account_link(self, projects_page: WebDriver):
        projects_page.find_element(By.CSS_SELECTOR, "#toggle-profile-menu").click()
        WebDriverWait(projects_page, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#profile-menu a[href='/account']"))
        )
        assert projects_page.find_element(By.CSS_SELECTOR, "#profile-menu a[href='/account']").is_displayed()

    def test_profile_menu_contains_sign_out(self, projects_page: WebDriver):
        projects_page.find_element(By.CSS_SELECTOR, "#toggle-profile-menu").click()
        WebDriverWait(projects_page, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#profile-menu button[type='submit']"))
        )
        assert projects_page.find_element(By.CSS_SELECTOR, "#profile-menu button[type='submit']").is_displayed()


class TestHeaderNavigation:

    def test_dashboard_link_is_active(self, projects_page: WebDriver):
        dashboard_link = projects_page.find_element(
            By.CSS_SELECTOR, ".auth-header-nav-left-items a[href='/']"
        )
        assert "current" in dashboard_link.get_attribute("class")

    def test_companies_link_visible(self, projects_page: WebDriver):
        companies_link = projects_page.find_element(
            By.CSS_SELECTOR, ".auth-header-nav-left-items a[href='/companies']"
        )
        assert companies_link.is_displayed()

    def test_analytics_dropdown_toggle_visible(self, projects_page: WebDriver):
        toggle = projects_page.find_element(By.CSS_SELECTOR, "#analytics-dropdown-toggle")
        assert toggle.is_displayed()

    def test_open_analytics_dropdown(self, projects_page: WebDriver):
        projects_page.find_element(By.CSS_SELECTOR, "#analytics-dropdown-toggle").click()
        WebDriverWait(projects_page, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#analytics-dropdown-menu"))
        )
        assert projects_page.find_element(By.CSS_SELECTOR, "#analytics-dropdown-menu").is_displayed()


class TestViewToggle:

    def test_grid_view_is_active_by_default(self, projects_page: WebDriver):
        grid_view_btn = projects_page.find_element(By.CSS_SELECTOR, "#grid-view")
        assert "active_list_type" in grid_view_btn.get_attribute("class")

    def test_projects_grid_is_visible(self, projects_page: WebDriver):
        assert projects_page.find_element(By.CSS_SELECTOR, "#grid ul.grid").is_displayed()


class TestCompanySelector:

    def test_company_selector_is_visible(self, projects_page: WebDriver):
        assert projects_page.find_element(By.CSS_SELECTOR, "#company_id").is_displayed()

    def test_company_selector_has_options(self, projects_page: WebDriver):
        options = projects_page.find_elements(By.CSS_SELECTOR, "#company_id option")
        assert len(options) > 0
