from playwright.sync_api import Page, expect

from src.web.components.ProjectCard import ProjectCard
from src.web.components.ProjectsPageHeader import ProjectsPageHeader


class ProjectsPage:

    URL = "/"

    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectsPageHeader(page)

        self._page_header = page.locator(".common-page-header")
        self._page_title = page.locator(".common-page-header h2")
        self._company_select = page.locator("#company_id")
        self._plan_tooltip = page.locator(".tooltip-project-plan")

        self._search_input = page.locator(".common-page-header input#search")
        self._create_button = page.locator(".common-page-header a.common-btn-primary")
        self._grid_view_button = page.locator("#grid-view")
        self._table_view_button = page.locator("#table-view")

        self._projects_grid = page.locator("#grid ul.grid")
        self._project_cards = page.locator("#grid ul.grid > li")

    def open(self) -> "ProjectsPage":
        self.page.goto(self.URL)
        return self

    def is_loaded(self) -> None:
        expect(self._page_title).to_have_text("Projects")
        expect(self._projects_grid).to_be_visible()


    def select_company(self, company_name: str) -> None:
        self._company_select.select_option(label=company_name)

    def get_selected_company(self) -> str:
        return self._company_select.locator("option:checked").inner_text()

    def search_project(self, query: str) -> None:
        self._search_input.fill(query)

    def clear_search(self) -> None:
        self._search_input.clear()

    def click_create_project(self) -> None:
        self._create_button.click()

    def switch_to_grid_view(self) -> None:
        self._grid_view_button.click()

    def switch_to_table_view(self) -> None:
        self._table_view_button.click()

    def get_visible_projects_count(self) -> int:
        """Returns the current count of visible project cards."""
        return self._project_cards.locator("visible=true").count()

    def wait_for_projects_count(self, expected_count: int) -> int:
        """Waits for a specific number of visible projects and returns the count."""
        visible_cards = self._project_cards.locator("visible=true")
        expect(visible_cards).to_have_count(expected_count)
        return visible_cards.count()

    def count_of_projects_visible(self, expected_count: int) -> int:
        visible_cards = self._project_cards.locator("visible=true")
        expect(visible_cards).to_have_count(expected_count)
        return visible_cards.count()

    def get_project_card(self, index: int) -> ProjectCard:
        return ProjectCard(self._project_cards.nth(index))

    def get_project_card_by_title(self, title: str) -> ProjectCard:
        card_locator = self._project_cards.filter(has=self.page.locator(f"h3:text-is('{title}')"))
        return ProjectCard(card_locator.first)

    def click_project_by_title(self, title: str) -> None:
        self.get_project_card_by_title(title).click()

    def has_project_with_title(self, title: str) -> None:
        expect(self._project_cards.filter(has=self.page.locator(f"h3:text-is('{title}')"))).to_have_count(1)

    def has_projects_count(self, count: int) -> None:
        expect(self._project_cards).to_have_count(count)

    def has_create_button(self) -> None:
        expect(self._create_button).to_be_visible()
        expect(self._create_button).to_have_text("Create")

    def has_plan_badge(self, plan_name: str) -> None:
        expect(self._plan_tooltip).to_contain_text(plan_name)
