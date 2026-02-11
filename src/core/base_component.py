"""Base component class with common functionality for all UI components."""

from playwright.sync_api import Locator, expect


class BaseComponent:
    """Base class for all UI components providing common functionality."""

    def __init__(self, locator: Locator):
        """Initialize the component with a Playwright Locator.

        Args:
            locator: Playwright Locator for the component root element
        """
        self._locator = locator

    def is_visible(self) -> None:
        """Assert that the component is visible."""
        expect(self._locator).to_be_visible()

    def is_hidden(self) -> None:
        """Assert that the component is hidden."""
        expect(self._locator).to_be_hidden()

    def click(self) -> None:
        """Click the component."""
        self._locator.click()

    def get_text(self) -> str:
        """Get the inner text of the component.

        Returns:
            Inner text content
        """
        return self._locator.inner_text()

