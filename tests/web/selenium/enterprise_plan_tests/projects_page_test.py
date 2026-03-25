"""Selenium tests for the projects page - enterprise plan."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.pages.projects_page import ProjectsPage
from tests.data.test_data import TestCompanies, TestPlans, TestProjects


@pytest.fixture
def logged_in_projects_page(logged_driver: WebDriver) -> ProjectsPage:
    projects_page = ProjectsPage(logged_driver)
    projects_page.is_loaded()
    assert projects_page.get_selected_company() == TestCompanies.DEFAULT_COMPANY
    projects_page.has_plan_badge(TestPlans.ENTERPRISE)
    return projects_page


@pytest.mark.selenium
class TestProjectsPageLoaded:

    def test_projects_page_is_loaded_after_login(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.is_loaded()

    def test_projects_page_has_create_button(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.has_create_button()

    def test_projects_page_displays_plan_badge(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.has_plan_badge("plan")


@pytest.mark.selenium
class TestProjectsSearch:

    def test_search_project_by_name(self, logged_in_projects_page: ProjectsPage):
        initial_count = logged_in_projects_page.get_visible_projects_count()
        logged_in_projects_page.search_project(TestProjects.TARGET_PROJECT)
        filtered_count = logged_in_projects_page.wait_for_projects_count(1)
        assert filtered_count <= initial_count

    def test_clear_search_restores_projects(self, logged_in_projects_page: ProjectsPage):
        initial_count = logged_in_projects_page.get_visible_projects_count()
        logged_in_projects_page.search_project(TestProjects.TARGET_PROJECT)
        logged_in_projects_page.wait_for_projects_count(1)
        logged_in_projects_page.clear_search()
        restored_count = logged_in_projects_page.wait_for_projects_count(initial_count)
        assert restored_count == initial_count


@pytest.mark.selenium
class TestProjectCards:

    def test_project_card_displays_title(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert card.is_visible()
        assert card.title != ""

    def test_project_card_displays_tests_count(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert "tests" in card.tests_count_text.lower()

    def test_project_card_displays_badge(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert card.badge != ""

    def test_project_card_has_href(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert "/projects/" in card.href

    def test_project_card_displays_member_avatars(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert card.get_member_avatars_count() > 0


@pytest.mark.selenium
class TestProfileMenu:

    def test_open_profile_menu(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_profile_menu()
        assert logged_in_projects_page.header.profile_menu.is_displayed()

    def test_profile_menu_contains_account_link(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_profile_menu()
        assert logged_in_projects_page.header.account_link.is_displayed()

    def test_profile_menu_contains_sign_out(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_profile_menu()
        assert logged_in_projects_page.header.sign_out_button.is_displayed()


@pytest.mark.selenium
class TestHeaderNavigation:

    def test_dashboard_link_is_active(self, logged_in_projects_page: ProjectsPage):
        assert "current" in logged_in_projects_page.header.dashboard_link.get_attribute("class")

    def test_companies_link_visible(self, logged_in_projects_page: ProjectsPage):
        assert logged_in_projects_page.header.companies_link.is_displayed()

    def test_analytics_dropdown_toggle_visible(self, logged_in_projects_page: ProjectsPage):
        assert logged_in_projects_page.header.analytics_dropdown_toggle.is_displayed()

    def test_open_analytics_dropdown(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_analytics_dropdown()
        assert logged_in_projects_page.header.analytics_dropdown_menu.is_displayed()


@pytest.mark.selenium
class TestViewToggle:

    def test_grid_view_is_active_by_default(self, logged_in_projects_page: ProjectsPage):
        assert "active_list_type" in logged_in_projects_page.grid_view_button.get_attribute("class")

    def test_projects_grid_is_visible(self, logged_in_projects_page: ProjectsPage):
        assert logged_in_projects_page.projects_grid.is_displayed()


@pytest.mark.selenium
class TestCompanySelector:

    def test_company_selector_is_visible(self, logged_in_projects_page: ProjectsPage):
        assert logged_in_projects_page.company_select.is_displayed()

    def test_company_selector_has_options(self, logged_in_projects_page: ProjectsPage):
        from selenium.webdriver.support.select import Select
        options = Select(logged_in_projects_page.company_select).options
        assert len(options) > 0