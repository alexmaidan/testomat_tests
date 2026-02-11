"""Tests for new project page functionality."""

from src.utils.helpers import generate_project_name
from src.web.application import Application


def test_create_new_project_basic(logged_app: Application):
    """Test basic project creation flow.

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
