"""Selenium tests for login page functionality."""

import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.helpers import generate_random_email, generate_random_password
from src.web.constants import Urls
from src.web.selenium.pages.login_page import LoginPage
from tests.fixtures.config import Config


# Only cases where credentials reach the server (valid email format).
# Cases blocked by browser input validation (empty/malformed email) belong in Playwright tests.
invalid_login_test_data = [
    pytest.param(generate_random_email(), generate_random_password(), id="EC_nonexistent_user"),
    pytest.param(generate_random_email(), "a", id="BVA_password_1_char"),
    pytest.param(generate_random_email(), generate_random_password(100), id="BVA_password_100_chars"),
    pytest.param(generate_random_email(), "<script>alert('XSS')</script>", id="SEC_xss_in_password"),
    pytest.param(generate_random_email(), "' OR '1'='1", id="SEC_sql_injection_password"),
]


@pytest.mark.selenium
def test_login_with_valid_credentials(driver: WebDriver, configs: Config):
    login_page = LoginPage(driver)
    login_page.open(configs.app_base_url + Urls.LOGIN)
    login_page.is_loaded()
    login_page.login_user(configs.email, configs.password)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop .common-flash-success"))
    )


@pytest.mark.selenium
@pytest.mark.parametrize("email,password", invalid_login_test_data)
def test_login_with_invalid_credentials(driver: WebDriver, configs: Config, email: str, password: str):
    login_page = LoginPage(driver)
    login_page.open(configs.app_base_url + Urls.LOGIN)
    login_page.is_loaded()
    login_page.login_user(email, password)
    login_page.has_invalid_login_message()
