from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.side_bar import SideBar


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.sidebar = SideBar(page)
        self._sticky_header = page.locator(".sticky-header")
        self._main_nav = page.locator(".mainnav-menu")
        self._first_suite_placeholder = page.locator("[placeholder='First Suite']")
        self._suite_button = page.get_by_role("button", name="Suite")
        self._project_name = page.locator(".sticky-header h2")
        self._close_readme_button = page.locator(".back .third-btn")

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

    def is_loaded(self) -> Self:
        expect(self._sticky_header).to_be_visible()
        expect(self._main_nav).to_be_visible()
        expect(self._first_suite_placeholder).to_be_visible()
        expect(self._suite_button).to_be_visible()
        return self

    def assert_project_name(self, expected_project_name: str) -> Self:
        expect(self._project_name).to_have_text(expected_project_name)
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        return self.assert_project_name(expected_project_name)

    def close_read_me(self) -> Self:
        self._close_readme_button.click()
        return self

    def create_test_via_popup(self):
        self.page.locator(".sticky-header").get_by_role("button", name="Test  ", exact=True).click()
        return self

    def create_test_suite_via_popup(self):
        self.page.locator(".md-icon-chevron-down").click()
        self.page.get_by_text("Collection of test cases").click()

    def create_first_suite(self, target_suite_name: str):
        self.page.locator("[placeholder='First Suite']").fill(target_suite_name)
        suite_button = self.page.get_by_role("button", name="Suite")
        suite_button.click()
        expect(suite_button).to_be_hidden()
        return self

    def suite_with_name_is_visible(self, test_suite_name: str):
        expect(self.page.locator(".suites-list-content").get_by_text(test_suite_name)).to_be_visible()
