import pytest
from selenium import webdriver

from src.web.constants import Urls
from src.web.selenium.pages.login_page import LoginPage
from tests.fixtures.config import Config


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def _session_logged_driver(configs: Config):
    """Session-scoped driver that logs in once and reuses the session."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.set_window_size(1920, 1080)

    login_page = LoginPage(driver)
    login_page.open(configs.app_base_url + Urls.LOGIN)
    login_page.is_loaded()
    login_page.login_user(configs.email, configs.password)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_driver(_session_logged_driver, configs: Config):
    """Function-scoped fixture that navigates to projects page before each test."""
    _session_logged_driver.get(configs.app_base_url + Urls.PROJECTS)
    yield _session_logged_driver
