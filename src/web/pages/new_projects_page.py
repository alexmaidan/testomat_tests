from typing import Self

from playwright.sync_api import Page, expect

from src.core.base_page import BasePage
from src.web.constants import Urls
from src.web.pages.project_page import ProjectPage


class NewProjectsPage(BasePage):
    """New project creation page object."""

    URL = Urls.NEW_PROJECT

    def __init__(self, page: Page):
        """Initialize NewProjectsPage with page locators.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self._form_container = page.locator("#content-desktop [action='/projects']")

    def is_loaded(self) -> Self:
        """Assert that the new projects page is fully loaded.

        Returns:
            Self for method chaining
        """
        expect(self._form_container).to_be_visible()
        expect(self._form_container.locator("#classical")).to_be_visible()
        expect(self._form_container.locator("#classical")).to_contain_text("Classical")
        expect(self._form_container.locator("#bdd")).to_be_visible()
        expect(self._form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self._form_container.locator("#project_title")).to_be_visible()
        expect(self._form_container.locator("#demo-btn")).to_be_visible()
        expect(self._form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.page.get_by_text("How to Start?")).to_be_visible()
        expect(self.page.get_by_text("New Project")).to_be_visible()
        return self

    def fill_project_title(self, target_project_name: str) -> Self:
        """Fill in the project title field.

        Args:
            target_project_name: Name for the new project

        Returns:
            Self for method chaining
        """
        self._form_container.locator("#project_title").fill(target_project_name)
        return self

    def click_create(self) -> ProjectPage:
        """Click the create button and return the project page.

        Returns:
            ProjectPage instance for the newly created project
        """
        self._form_container.locator("#project-create-btn input").click()
        expect(self._form_container.locator("#project-create-btn input")).to_be_hidden(timeout=10_000)
        return ProjectPage(self.page)
