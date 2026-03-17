import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.fixtures.config import Config


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def module_driver():
    """Module-scoped Chrome driver - reused across all tests in a module."""
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_driver(driver, configs: Config):
    """Function-scoped driver already logged in to the application."""
    _do_login(driver, configs)
    yield driver


def _do_login(driver, configs: Config) -> None:
    """Perform login with the given driver using credentials from configs."""
    wait = WebDriverWait(
        driver, 10, poll_frequency=0.1,
        ignored_exceptions=[StaleElementReferenceException, NoSuchElementException],
    )
    driver.get(configs.app_base_url)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop #user_email")))
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email").send_keys(configs.email)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password").send_keys(configs.password)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop [value='Sign In']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop .common-flash-success")))
