from typing import Self

from playwright.sync_api import Page, expect

from src.core.base_page import BasePage
from src.web.constants import Urls


class HomePage(BasePage):
    """Home page object for the main testomat.io website."""

    URL = Urls.HOME

    def __init__(self, page: Page):
        """Initialize HomePage with page locators.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self._header_wrapper = page.locator("#headerMenuWrapper")
        self._login_item = page.locator(".side-menu .login-item")
        self._start_item = page.locator(".side-menu .start-item")

    def is_loaded(self) -> Self:
        """Assert that the home page is fully loaded.

        Returns:
            Self for method chaining
        """
        expect(self._header_wrapper).to_be_visible()
        expect(self._login_item).to_have_text("Log in")
        expect(self._start_item).to_have_text("Start for free")
        return self

    def click_login(self) -> Self:
        """Click the login button.

        Returns:
            Self for method chaining
        """
        self.page.get_by_text("Log in", exact=True).click()
        return self
