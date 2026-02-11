import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBar:
    """Component representing the project sidebar navigation."""

    def __init__(self, page: Page):
        """Initialize SideBar with page locators.

        Args:
            page: Playwright Page instance
        """
        self._page = page
        self._sidebar = page.locator(".mainnav-menu")
        self._sidebar_body = page.locator(".mainnav-menu-body")
        self._sidebar_footer = page.locator(".mainnav-menu-footer")

        self._logo_link = page.get_by_role("link", name="testomat.io")
        self._close_button = page.locator(".btn-close")

        self._tests_link = page.get_by_role("link", name="Tests")
        self._requirements_link = page.get_by_role("link", name="Requirements")
        self._runs_link = page.get_by_role("link", name="Runs")
        self._plans_link = page.get_by_role("link", name="Plans")
        self._steps_link = page.get_by_role("link", name="Steps")
        self._pulse_link = page.get_by_role("link", name="Pulse")
        self._imports_link = page.get_by_role("link", name="Imports")
        self._analytics_link = page.get_by_role("link", name="Analytics")
        self._branches_link = page.get_by_role("link", name="Branches")
        self._settings_link = page.get_by_role("link", name="Settings")

        self._help_link = page.get_by_role("link", name="Help")
        self._projects_link = page.get_by_role("link", name="Projects")

        self._user_avatar = self._sidebar_footer.locator("img.rounded-full")
        self._username_label = self._sidebar_footer.locator(".label-container").last

    def is_loaded(self) -> Self:
        """Assert that the sidebar is loaded.

        Returns:
            Self for method chaining
        """
        expect(self._sidebar).to_be_visible()
        expect(self._sidebar).to_have_class(re.compile(r"mainnav-menu"))
        return self

    def is_visible(self) -> Self:
        """Assert that the sidebar is visible.

        Returns:
            Self for method chaining
        """
        expect(self._sidebar).to_be_visible()
        return self

    def is_expanded(self) -> Self:
        """Assert that the sidebar is expanded.

        Returns:
            Self for method chaining
        """
        expect(self._sidebar).to_have_class(re.compile(r"mainnav-menu-expanded"))
        return self

    def expand(self) -> Self:
        """Expand the sidebar.

        Returns:
            Self for method chaining
        """
        self._sidebar.get_by_role("button").first.click()
        expect(self._sidebar).to_have_class(re.compile(r"mainnav-menu-expanded"))
        return self

    def click_close(self) -> Self:
        """Click the close button.

        Returns:
            Self for method chaining
        """
        self._close_button.click()
        return self

    def click_logo(self) -> Self:
        """Click the logo link.

        Returns:
            Self for method chaining
        """
        self._logo_link.click()
        return self

    def click_tests(self) -> Self:
        """Click the tests link.

        Returns:
            Self for method chaining
        """
        self._tests_link.click()
        return self

    def click_requirements(self) -> Self:
        """Click the requirements link.

        Returns:
            Self for method chaining
        """
        self._requirements_link.click()
        return self

    def click_runs(self) -> Self:
        """Click the runs link.

        Returns:
            Self for method chaining
        """
        self._runs_link.click()
        return self

    def click_plans(self) -> Self:
        """Click the plans link.

        Returns:
            Self for method chaining
        """
        self._plans_link.click()
        return self

    def click_steps(self) -> Self:
        """Click the steps link.

        Returns:
            Self for method chaining
        """
        self._steps_link.click()
        return self

    def click_pulse(self) -> Self:
        """Click the pulse link.

        Returns:
            Self for method chaining
        """
        self._pulse_link.click()
        return self

    def click_imports(self) -> Self:
        """Click the imports link.

        Returns:
            Self for method chaining
        """
        self._imports_link.click()
        return self

    def click_analytics(self) -> Self:
        """Click the analytics link.

        Returns:
            Self for method chaining
        """
        self._analytics_link.click()
        return self

    def click_branches(self) -> Self:
        """Click the branches link.

        Returns:
            Self for method chaining
        """
        self._branches_link.click()
        return self

    def click_settings(self) -> Self:
        """Click the settings link.

        Returns:
            Self for method chaining
        """
        self._settings_link.click()
        return self

    def click_help(self) -> Self:
        """Click the help link.

        Returns:
            Self for method chaining
        """
        self._help_link.click()
        return self

    def click_projects(self) -> Self:
        """Click the projects link.

        Returns:
            Self for method chaining
        """
        self._projects_link.click()
        return self

    def click_user_profile(self) -> Self:
        """Click the user avatar to open profile.

        Returns:
            Self for method chaining
        """
        self._user_avatar.click()
        return self

    def has_active_nav_item(self, name: str) -> Self:
        """Assert that a navigation item is active.

        Args:
            name: Name of the navigation item

        Returns:
            Self for method chaining
        """
        active_link = self._page.get_by_role("link", name=name).locator(".active")
        expect(active_link).to_be_visible()
        return self

    def has_tests_active(self) -> Self:
        """Assert that the tests link is active.

        Returns:
            Self for method chaining
        """
        expect(self._tests_link).to_have_class(re.compile(r"active"))
        return self

    def is_tab_active(self, tab_name: str) -> Self:
        """Check if a tab is active.

        Args:
            tab_name: Name of the tab

        Returns:
            Self for method chaining
        """
        tab_link = self._sidebar.get_by_role("link", name=tab_name)
        expect(tab_link).to_have_class(re.compile(r"\bactive\b"))
        return self

    def has_username(self, username: str) -> Self:
        """Assert that the username matches.

        Args:
            username: Expected username

        Returns:
            Self for method chaining
        """
        expect(self._username_label).to_have_text(username)
        return self

    def get_username(self) -> str:
        """Get the displayed username.

        Returns:
            str: Username text
        """
        return self._username_label.inner_text()

    def is_nav_item_visible(self, name: str) -> Self:
        """Assert that a navigation item is visible.

        Args:
            name: Name of the navigation item

        Returns:
            Self for method chaining
        """
        link = self._page.get_by_role("link", name=name)
        expect(link).to_be_visible()
        return self
