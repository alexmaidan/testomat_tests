from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from src.web.constants import Urls
from src.web.selenium.components.project_card import ProjectCard
from src.web.selenium.components.projects_page_header import ProjectsPageHeader
from src.web.selenium.core.base_page import BasePage


class ProjectsPage(BasePage):

    URL = Urls.PROJECTS

    _PAGE_TITLE = (By.CSS_SELECTOR, ".common-page-header h2")
    _COMPANY_SELECT = (By.ID, "company_id")
    _PLAN_TOOLTIP = (By.CSS_SELECTOR, ".tooltip-project-plan")
    _SEARCH_INPUT = (By.CSS_SELECTOR, ".common-page-header input#search")
    _CREATE_BUTTON = (By.CSS_SELECTOR, ".common-page-header a.common-btn-primary")
    _GRID_VIEW_BUTTON = (By.ID, "grid-view")
    _PROJECTS_GRID = (By.CSS_SELECTOR, "#grid ul.grid")
    _PROJECT_CARDS = (By.CSS_SELECTOR, "#grid ul.grid > li")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, timeout)
        self.header = ProjectsPageHeader(driver, timeout)

    @property
    def page_title(self) -> WebElement:
        return self.find_visible(self._PAGE_TITLE)

    @property
    def company_select(self) -> WebElement:
        return self.find_visible(self._COMPANY_SELECT)

    @property
    def plan_tooltip(self) -> WebElement:
        return self.find_visible(self._PLAN_TOOLTIP)

    @property
    def search_input(self) -> WebElement:
        return self.find_visible(self._SEARCH_INPUT)

    @property
    def create_button(self) -> WebElement:
        return self.find_visible(self._CREATE_BUTTON)

    @property
    def grid_view_button(self) -> WebElement:
        return self.find_visible(self._GRID_VIEW_BUTTON)

    @property
    def projects_grid(self) -> WebElement:
        return self.find_visible(self._PROJECTS_GRID)

    def is_loaded(self) -> Self:
        assert self.page_title.text == "Projects"
        self.projects_grid
        return self

    def get_selected_company(self) -> str:
        return Select(self.company_select).first_selected_option.text

    def select_company(self, company_name: str) -> Self:
        Select(self.company_select).select_by_visible_text(company_name)
        return self

    def search_project(self, query: str) -> Self:
        inp = self.search_input
        inp.clear()
        inp.send_keys(query)
        return self

    def clear_search(self) -> Self:
        self.search_input.clear()
        return self

    def get_visible_projects_count(self) -> int:
        return sum(1 for c in self.find_all(self._PROJECT_CARDS) if c.is_displayed())

    def wait_for_projects_count(self, expected_count: int) -> int:
        self.wait.until(
            lambda d: sum(1 for c in d.find_elements(*self._PROJECT_CARDS) if c.is_displayed()) == expected_count
        )
        return expected_count

    def get_project_card(self, index: int) -> ProjectCard:
        return ProjectCard(self.find_all(self._PROJECT_CARDS)[index])

    def has_create_button(self) -> Self:
        btn = self.create_button
        assert btn.is_displayed()
        assert btn.text == "Create"
        return self

    def has_plan_badge(self, plan_name: str) -> Self:
        assert plan_name.lower() in self.plan_tooltip.text.lower()
        return self