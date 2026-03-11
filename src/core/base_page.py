"""Base page class with common functionality for all page objects."""

from typing import Self

from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects providing common functionality."""

    URL: str = ""

    def __init__(self, page: Page):
        """Initialize the page with a Playwright Page instance.

        Args:
            page: Playwright Page instance
        """
        self.page = page

    def open(self) -> Self:
        """Navigate to the page URL.

        Returns:
            Self for method chaining
        """
        self.page.goto(self.URL)
        return self

    def wait_for_timeout(self, timeout: int) -> Self:
        """Wait for a specified timeout in milliseconds.

        Args:
            timeout: Time to wait in milliseconds

        Returns:
            Self for method chaining
        """
        self.page.wait_for_timeout(timeout)
        return self

    def get_current_url(self) -> str:
        """Get the current page URL.

        Returns:
            Current URL string
        """
        return self.page.url

    def reload(self) -> Self:
        """Reload the current page.

        Returns:
            Self for method chaining
        """
        self.page.reload()
        return self

