import time

import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.helpers import generate_random_email, generate_random_password
from tests.fixtures.config import Config

# =============================================================================
# TEST DESIGN TECHNIQUES:
# 1. Equivalence Class Partitioning (ECP) - divides input into valid/invalid classes
# 2. Boundary Value Analysis (BVA) - tests at the edges of input ranges
# =============================================================================
# EMAIL CLASSES: empty, no @, no domain, no local part, invalid chars, spaces
# PASSWORD CLASSES: empty, only spaces, valid format but wrong
# BVA EMAIL: min length, max length (255), exceeds max
# BVA PASSWORD: 1 char, 5-9 chars (around typical 8 char minimum), 100+, 255 chars
# =============================================================================

invalid_login_test_data = [
    # --- Equivalence Class Partitioning: Email ---
    pytest.param("", generate_random_password(), id="EC_empty_email"),
    pytest.param("userwithoutat.com", generate_random_password(), id="EC_email_no_at"),
    pytest.param("user@", generate_random_password(), id="EC_email_no_domain"),
    pytest.param("@domain.com", generate_random_password(), id="EC_email_no_local"),
    pytest.param("user<>@domain.com", generate_random_password(), id="EC_email_invalid_chars"),
    pytest.param("user name@domain.com", generate_random_password(), id="EC_email_with_space"),
    pytest.param(" user@domain.com", generate_random_password(), id="EC_email_leading_space"),
    pytest.param("user@domain.com ", generate_random_password(), id="EC_email_trailing_space"),
    # --- Equivalence Class Partitioning: Password ---
    pytest.param(generate_random_email(), "", id="EC_empty_password"),
    pytest.param(generate_random_email(), "        ", id="EC_password_only_spaces"),
    # --- Boundary Value Analysis: Email ---
    pytest.param("a@b.co", generate_random_password(), id="BVA_email_min_length"),
    pytest.param(f"{'a' * 64}@{'b' * 185}.com", generate_random_password(), id="BVA_email_max_255"),
    pytest.param(f"{'a' * 100}@{'b' * 200}.com", generate_random_password(), id="BVA_email_exceeds_max"),
    # --- Boundary Value Analysis: Password ---
    pytest.param(generate_random_email(), "a", id="BVA_password_1_char"),
    pytest.param(generate_random_email(), "abc45", id="BVA_password_5_chars"),
    pytest.param(generate_random_email(), "abcde6", id="BVA_password_6_chars"),
    pytest.param(generate_random_email(), "abcdef7", id="BVA_password_7_chars"),
    pytest.param(generate_random_email(), "abcdefg8", id="BVA_password_8_chars"),
    pytest.param(generate_random_email(), "abcdefgh9", id="BVA_password_9_chars"),
    pytest.param(generate_random_email(), generate_random_password(100), id="BVA_password_100_chars"),
    pytest.param(generate_random_email(), generate_random_password(255), id="BVA_password_255_chars"),
    # --- Wrong credentials (valid format, non-existent user) ---
    pytest.param(generate_random_email(), generate_random_password(), id="EC_nonexistent_user"),
    # --- Security: XSS and SQL Injection ---
    pytest.param(generate_random_email(), "<script>alert('XSS')</script>", id="SEC_xss_in_password"),
    pytest.param(generate_random_email(), "' OR '1'='1", id="SEC_sql_injection_password"),
]


@pytest.fixture(scope="function")
def persistent_login_driver(driver: WebDriver, configs: Config):
    """Fresh browser per test to avoid state pollution.
    Small delay prevents server-side rate limiting from rapid consecutive attempts."""
    time.sleep(2)
    driver.get(configs.app_base_url)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop #user_email")))
    return driver


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("email,password", invalid_login_test_data)
def test_login_invalid(persistent_login_driver: WebDriver, email: str, password: str):
    """
    Test invalid login scenarios.
    Each test gets a fresh browser to avoid state pollution between tests.
    Uses form.submit() via JS to bypass ALL browser-side HTML5 validation
    so every input value reaches the server and gets the server-side error.
    """
    wait = WebDriverWait(persistent_login_driver, 15)

    email_input = persistent_login_driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email")
    password_input = persistent_login_driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password")

    email_input.send_keys(email)
    password_input.send_keys(password)

    # form.submit() bypasses HTML5 email/required validation entirely
    form = persistent_login_driver.find_element(By.CSS_SELECTOR, "#content-desktop form")
    persistent_login_driver.execute_script("arguments[0].submit();", form)

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='content-desktop']//*[contains(text(), 'Invalid Email or password.')]")
        )
    )


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(driver: WebDriver, configs: Config):
    """Test successful login with valid credentials."""
    wait = WebDriverWait(driver, 10)

    driver.get(configs.app_base_url)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop #user_email")))
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email").send_keys(configs.email)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password").send_keys(configs.password)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop [value='Sign In']").click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".common-page-header h2")))
    assert driver.find_element(By.CSS_SELECTOR, ".common-page-header h2").text == "Projects"
