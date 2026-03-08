import pytest

from src.utils.helpers import generate_project_name
from src.web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_new_project_creation_with_sidebar(logged_app: Application):
    """Test project creation and verify sidebar is displayed.

    Uses logged_app fixture - reuses authorization.
    """
    target_project_name = generate_project_name()
    project_page = (
        logged_app.new_projects_page.open().is_loaded().fill_project_title(target_project_name).click_create()
    )

    project_page.is_loaded().assert_project_name(target_project_name).close_read_me()

    project_page.sidebar.is_loaded().expand().is_tab_active("Tests")
