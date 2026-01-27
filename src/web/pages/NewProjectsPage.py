from playwright.sync_api import Page, expect


class NewProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.__form_container = page.locator("#content-desktop [action='/projects']")

    def open(self):
        self.page.goto("/projects/new")

    def is_loaded(self):
        expect(self.__form_container).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_contain_text("Classical")
        expect(self.__form_container.locator("#bdd")).to_be_visible()
        expect(self.__form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self.__form_container.locator("#project_title")).to_be_visible()
        expect(self.__form_container.locator("#demo-btn")).to_be_visible()
        expect(self.__form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.page.get_by_text("How to Start?")).to_be_visible()
        expect(self.page.get_by_text("New Project")).to_be_visible()

    def fill_project_title(self, target_project_name: str):
        self.__form_container.locator("#project_title").fill(target_project_name)

    def click_create(self):
        self.__form_container.locator("#project-create-btn input").click()
        expect(self.__form_container.locator("#project-create-btn input")).to_be_hidden(timeout=10_000)
