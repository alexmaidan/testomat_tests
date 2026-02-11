from typing import Self

from playwright.sync_api import Locator, expect

from src.core.base_component import BaseComponent


class ProjectCard(BaseComponent):
    """Component representing a project card in the projects grid."""

    def __init__(self, locator: Locator):
        """Initialize ProjectCard with a locator.

        Args:
            locator: Playwright Locator for the project card element
        """
        super().__init__(locator)

    @property
    def title(self) -> str:
        """Get the project card title.

        Returns:
            Project title text
        """
        return self._locator.locator("h3").inner_text()

    @property
    def tests_count_text(self) -> str:
        """Get the tests count text.

        Returns:
            Tests count text
        """
        return self._locator.locator("p.text-gray-500").inner_text()

    @property
    def badge(self) -> str:
        """Get the project badge text.

        Returns:
            Badge text
        """
        return self._locator.locator(".project-badges .common-badge").first.inner_text()

    @property
    def href(self) -> str:
        """Get the project link href.

        Returns:
            Link href attribute
        """
        return self._locator.locator("a").get_attribute("href")

    def click(self) -> None:
        """Click the project card link."""
        self._locator.locator("a").click()

    def has_title(self, title: str) -> Self:
        """Assert that the card has the expected title.

        Args:
            title: Expected title text

        Returns:
            Self for method chaining
        """
        expect(self._locator.locator("h3")).to_have_text(title)
        return self

    def has_badge(self, badge: str) -> Self:
        """Assert that the card has the expected badge.

        Args:
            badge: Expected badge text

        Returns:
            Self for method chaining
        """
        expect(self._locator.locator(".project-badges .common-badge").first).to_have_text(badge)
        return self

    def get_member_avatars_count(self) -> int:
        """Get the count of member avatar images.

        Returns:
            Number of member avatars
        """
        return self._locator.locator(".inline-flex img").count()

    def get_additional_members_count(self) -> str | None:
        """Get the additional members count text if present.

        Returns:
            Additional members count text or None
        """
        counter = self._locator.locator(".inline-flex .rounded-full.bg-gray-300")
        if counter.count() > 0:
            return counter.inner_text()
        return None
