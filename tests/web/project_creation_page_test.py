"""Tests for project creation page with sidebar verification."""

from src.utils.helpers import generate_project_name
from src.web.application import Application


def test_new_project_creation_with_sidebar(logged_app: Application):
    """Test project creation and verify sidebar is displayed.

    Uses logged_app fixture - reuses authorization.
    """
    target_project_name = generate_project_name()
    (logged_app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (logged_app.project_page
     .is_loaded()
     .assert_project_name(target_project_name)
     .close_read_me())

    (logged_app.project_page.sidebar
     .is_loaded()
     .expand()
     .is_tab_active("Tests"))
