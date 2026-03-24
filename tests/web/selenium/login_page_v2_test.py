"""Selenium tests for login page functionality using LoginPageV2 (property-based)."""

import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from src.utils.helpers import generate_random_email, generate_random_password
from src.web.constants import Urls
from src.web.selenium.pages.login_page_v2 import LoginPageV2
from tests.fixtures.config import Config


invalid_login_test_data = [
    pytest.param(generate_random_email(), generate_random_password(), id="EC_nonexistent_user"),
    pytest.param(generate_random_email(), "a", id="BVA_password_1_char"),
    pytest.param(generate_random_email(), generate_random_password(100), id="BVA_password_100_chars"),
    pytest.param(generate_random_email(), "<script>alert('XSS')</script>", id="SEC_xss_in_password"),
    pytest.param(generate_random_email(), "' OR '1'='1", id="SEC_sql_injection_password"),
]


@pytest.mark.selenium
def test_login_with_valid_credentials(driver: WebDriver, configs: Config):
    login_page = LoginPageV2(driver)
    login_page.open(configs.app_base_url + Urls.LOGIN)
    login_page.is_loaded()
    login_page.login_user(configs.email, configs.password)
    login_page.has_success_flash()


@pytest.mark.selenium
@pytest.mark.parametrize("email,password", invalid_login_test_data)
def test_login_with_invalid_credentials(driver: WebDriver, configs: Config, email: str, password: str):
    login_page = LoginPageV2(driver)
    login_page.open(configs.app_base_url + Urls.LOGIN)
    login_page.is_loaded()
    login_page.login_user(email, password)
    login_page.has_invalid_login_message()