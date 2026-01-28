import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBar:

    def __init__(self, page: Page):
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

    def is_loaded(self) -> SideBar:
        expect(self._sidebar).to_be_visible()
        expect(self._sidebar).to_have_class(re.compile(r"mainnav-menu"))
        return self

    def is_visible(self) -> None:
        expect(self._sidebar).to_be_visible()

    def is_expanded(self) -> Self:
        expect(self._sidebar).to_have_class(re.compile(r"mainnav-menu-expanded"))
        return self

    def expand(self) -> Self:
        self._sidebar.get_by_role("button").first.click()
        expect(self._sidebar).to_have_class(re.compile(r"mainnav-menu-expanded"))
        return self

    def click_close(self) -> None:
        self._close_button.click()

    def click_logo(self) -> None:
        self._logo_link.click()

    def click_tests(self) -> None:
        self._tests_link.click()

    def click_requirements(self) -> None:
        self._requirements_link.click()

    def click_runs(self) -> None:
        self._runs_link.click()

    def click_plans(self) -> None:
        self._plans_link.click()

    def click_steps(self) -> None:
        self._steps_link.click()

    def click_pulse(self) -> None:
        self._pulse_link.click()

    def click_imports(self) -> None:
        self._imports_link.click()

    def click_analytics(self) -> None:
        self._analytics_link.click()

    def click_branches(self) -> None:
        self._branches_link.click()

    def click_settings(self) -> None:
        self._settings_link.click()

    def click_help(self) -> None:
        self._help_link.click()

    def click_projects(self) -> None:
        self._projects_link.click()

    def click_user_profile(self) -> None:
        self._user_avatar.click()

    def has_active_nav_item(self, name: str) -> None:
        active_link = self._page.get_by_role("link", name=name).locator(".active")
        expect(active_link).to_be_visible()

    def has_tests_active(self) -> Self:
        expect(self._tests_link).to_have_class(re.compile(r"active"))
        return self

    def is_tab_active(self, tab_name: str) -> Self:
        tab_link = self._sidebar.get_by_role("link", name=tab_name)
        expect(tab_link).to_have_class(re.compile(r"\bactive\b"))
        return self

    def has_username(self, username: str) -> None:
        expect(self._username_label).to_have_text(username)

    def get_username(self) -> str:
        return self._username_label.inner_text()

    def is_nav_item_visible(self, name: str) -> None:
        link = self._page.get_by_role("link", name=name)
        expect(link).to_be_visible()
