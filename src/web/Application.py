from playwright.sync_api import Page

from src.web.components.test_for_suite_popup import TestForSuitePopup
from src.web.components.test_modal import TestModal
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.new_projects_page import NewProjectsPage
from src.web.pages.project_page import ProjectPage
from src.web.pages.projects_page import ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.new_projects_page = NewProjectsPage(page)
        self.project_page = ProjectPage(page)
        self.projects_page = ProjectsPage(page)
        self.test_for_suite_popup = TestForSuitePopup(page)
        self.test_modal = TestModal(page)
