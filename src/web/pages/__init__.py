"""Page objects package for web pages."""

from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.new_projects_page import NewProjectsPage
from src.web.pages.project_page import ProjectPage
from src.web.pages.projects_page import ProjectsPage

__all__ = [
    "HomePage",
    "LoginPage",
    "ProjectsPage",
    "ProjectPage",
    "NewProjectsPage",
]
