from typing import Self

from playwright.sync_api import Page, expect

from src.core.base_page import BasePage
from src.web.components.side_bar import SideBar


class ProjectPage(BasePage):
    """Project page object for viewing and managing a single project."""

    def __init__(self, page: Page):
        """Initialize ProjectPage with page locators.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self.sidebar = SideBar(page)
        self._sticky_header = page.locator(".sticky-header")
        self._main_nav = page.locator(".mainnav-menu")
        self._first_suite_placeholder = page.locator("[placeholder='First Suite']")
        self._suite_button = page.get_by_role("button", name="Suite")
        self._project_name = page.locator(".sticky-header h2")
        self._close_readme_button = page.locator(".back .third-btn")

    def is_loaded(self) -> Self:
        """Assert that the project page is fully loaded.

        Returns:
            Self for method chaining
        """
        expect(self._sticky_header).to_be_visible()
        expect(self._main_nav).to_be_visible()
        expect(self._first_suite_placeholder).to_be_visible()
        expect(self._suite_button).to_be_visible()
        return self

    def assert_project_name(self, expected_project_name: str) -> Self:
        """Assert that the project name matches the expected value.

        Args:
            expected_project_name: Expected project name

        Returns:
            Self for method chaining
        """
        expect(self._project_name).to_have_text(expected_project_name)
        return self

    # Keep old method name for backward compatibility
    def empty_project_name_is(self, expected_project_name: str) -> Self:
        """Deprecated: Use assert_project_name() instead."""
        return self.assert_project_name(expected_project_name)

    def close_read_me(self) -> Self:
        """Close the README panel.

        Returns:
            Self for method chaining
        """
        self._close_readme_button.click()
        return self

