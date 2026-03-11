import pytest
from faker import Faker

from src.api.projects import ProjectsApi
from src.utils.helpers import generate_project_name
from src.web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_new_project_creation_and_test_popup(logged_app: Application):
    target_project_name = generate_project_name()
    project_page = (
        logged_app.new_projects_page.open().is_loaded().fill_project_title(target_project_name).click_create()
    )

    project_page.is_loaded().assert_project_name(target_project_name).close_read_me()

    project_page.sidebar.is_loaded().expand().is_tab_active("Tests")

    target_suite_name = Faker().company()
    project_page.create_first_suite(target_suite_name)
    project_page.create_test_via_popup()
    logged_app.test_for_suite_popup.is_loaded().select_first_suite()

    test_name = Faker().sentence()
    logged_app.test_modal.is_loaded("test").set_title(test_name).save()
    logged_app.test_modal.edit_is_visible("test")


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_test_from_sidebar(logged_app: Application, projects_api: ProjectsApi):
    all_projects = projects_api.get_projects()
    target_project_id = all_projects[0].id

    logged_app.project_page.open_by_id(target_project_id).sidebar.is_loaded()
    logged_app.project_page.create_test_via_popup()
    logged_app.test_for_suite_popup.is_loaded().select_first_suite()

    test_name = Faker().sentence()
    logged_app.test_modal.is_loaded("test").set_title(test_name).save()
    logged_app.test_modal.edit_is_visible("test")
