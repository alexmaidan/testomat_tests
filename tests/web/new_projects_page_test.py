from faker import Faker

from src.web.Application import Application


def test_new_project_creation(logged_app: Application):
    """Uses logged_app fixture - reuses authorization."""
    target_project_name = Faker().company()
    (logged_app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (logged_app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())
