
import re

import pytest
from playwright.sync_api import expect

from src.web.Application import Application
from src.web.pages.ProjectsPage import ProjectsPage
from tests.conftest import Config


@pytest.fixture
def logged_in_projects_page(app: Application, configs: Config) -> ProjectsPage:
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)

    app.projects_page.is_loaded()
    assert app.projects_page.get_selected_company() == "QA Club Lviv"
    app.projects_page.has_plan_badge("Enterprise plan")
    return app.projects_page


class TestProjectsPageLoaded:

    def test_projects_page_is_loaded_after_login(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.is_loaded()

    def test_projects_page_has_create_button(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.has_create_button()

    def test_projects_page_displays_plan_badge(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.has_plan_badge("plan")




class TestProjectsSearch:
    target_project_name: str = "A Passage to India"

    def test_search_project_by_name(self, logged_in_projects_page: ProjectsPage):
        initial_count = logged_in_projects_page.count_of_projects_visible(43)
        logged_in_projects_page.search_project(self.target_project_name)
        assert logged_in_projects_page.count_of_projects_visible(1) <= initial_count

    def test_clear_search_restores_projects(self, logged_in_projects_page: ProjectsPage):
        initial_count = logged_in_projects_page.count_of_projects_visible(43)
        logged_in_projects_page.search_project(self.target_project_name)
        logged_in_projects_page.clear_search()
        assert logged_in_projects_page.count_of_projects_visible(43) == initial_count


class TestProjectCards:

    def test_project_card_displays_title(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        card.is_visible()
        assert card.title != ""

    def test_project_card_displays_tests_count(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert "tests" in card.tests_count_text.lower()

    def test_project_card_displays_badge(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert card.badge != ""

    def test_project_card_has_href(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert card.href.startswith("/projects/")

    def test_project_card_displays_member_avatars(self, logged_in_projects_page: ProjectsPage):
        card = logged_in_projects_page.get_project_card(0)
        assert card.get_member_avatars_count() > 0


class TestGlobalSearch:

    def test_open_global_search(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_global_search()
        logged_in_projects_page.header.is_global_search_visible()

    def test_close_global_search_with_escape(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_global_search()
        logged_in_projects_page.header.close_global_search()
        logged_in_projects_page.header.is_global_search_hidden()


class TestProfileMenu:

    def test_open_profile_menu(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_profile_menu()
        expect(logged_in_projects_page.header._profile_menu).to_be_visible()

    def test_profile_menu_contains_account_link(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_profile_menu()
        expect(logged_in_projects_page.header._account_link).to_be_visible()

    def test_profile_menu_contains_sign_out(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_profile_menu()
        expect(logged_in_projects_page.header._sign_out_button).to_be_visible()


class TestHeaderNavigation:

    def test_dashboard_link_is_active(self, logged_in_projects_page: ProjectsPage):
        expect(logged_in_projects_page.header._dashboard_link).to_have_class(re.compile(r"current"))

    def test_companies_link_visible(self, logged_in_projects_page: ProjectsPage):
        expect(logged_in_projects_page.header._companies_link).to_be_visible()

    def test_analytics_dropdown_toggle_visible(self, logged_in_projects_page: ProjectsPage):
        expect(logged_in_projects_page.header._analytics_dropdown_toggle).to_be_visible()

    def test_open_analytics_dropdown(self, logged_in_projects_page: ProjectsPage):
        logged_in_projects_page.header.open_analytics_dropdown()
        expect(logged_in_projects_page.header._analytics_dropdown_menu).to_be_visible()


class TestViewToggle:

    def test_grid_view_is_active_by_default(self, logged_in_projects_page: ProjectsPage):
        expect(logged_in_projects_page._grid_view_button).to_have_class(re.compile(r"active_list_type"))

    def test_projects_grid_is_visible(self, logged_in_projects_page: ProjectsPage):
        expect(logged_in_projects_page._projects_grid).to_be_visible()


class TestCompanySelector:

    def test_company_selector_is_visible(self, logged_in_projects_page: ProjectsPage):
        expect(logged_in_projects_page._company_select).to_be_visible()

    def test_company_selector_has_options(self, logged_in_projects_page: ProjectsPage):
        options = logged_in_projects_page._company_select.locator("option")
        assert options.count() > 0
