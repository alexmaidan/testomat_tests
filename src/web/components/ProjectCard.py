from playwright.sync_api import Locator, expect


class ProjectCard:

    def __init__(self, locator: Locator):
        self._locator = locator

    @property
    def title(self) -> str:
        return self._locator.locator("h3").inner_text()

    @property
    def tests_count_text(self) -> str:
        return self._locator.locator("p.text-gray-500").inner_text()

    @property
    def badge(self) -> str:
        return self._locator.locator(".project-badges .common-badge").first.inner_text()

    @property
    def href(self) -> str:
        return self._locator.locator("a").get_attribute("href")

    def click(self) -> None:
        self._locator.locator("a").click()

    def is_visible(self) -> None:
        expect(self._locator).to_be_visible()

    def has_title(self, title: str) -> None:
        expect(self._locator.locator("h3")).to_have_text(title)

    def has_badge(self, badge: str) -> None:
        expect(self._locator.locator(".project-badges .common-badge").first).to_have_text(badge)

    def get_member_avatars_count(self) -> int:
        return self._locator.locator(".inline-flex img").count()

    def get_additional_members_count(self) -> str | None:
        counter = self._locator.locator(".inline-flex .rounded-full.bg-gray-300")
        if counter.count() > 0:
            return counter.inner_text()
        return None
