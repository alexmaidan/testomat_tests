import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.helpers import generate_project_name
from tests.fixtures.config import Config


@pytest.mark.smoke
@pytest.mark.web
def test_create_new_project_basic(logged_driver: WebDriver, configs: Config):
    """Test basic project creation flow."""
    wait = WebDriverWait(logged_driver, 15)
    target_project_name = generate_project_name()

    logged_driver.get(f"{configs.app_base_url}/projects/new")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop [action='/projects']")))

    project_title_input = logged_driver.find_element(By.CSS_SELECTOR, "#content-desktop #project_title")
    project_title_input.clear()
    project_title_input.send_keys(target_project_name)

    # Remove form target to prevent opening in a new tab, then submit
    form = logged_driver.find_element(By.CSS_SELECTOR, "#content-desktop [action='/projects']")
    logged_driver.execute_script("arguments[0].removeAttribute('target');", form)
    logged_driver.execute_script("arguments[0].submit();", form)

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sticky-header h2")))

    project_name_el = logged_driver.find_element(By.CSS_SELECTOR, ".sticky-header h2")
    assert project_name_el.text == target_project_name


@pytest.mark.smoke
@pytest.mark.web
def test_new_project_page_is_loaded(logged_driver: WebDriver, configs: Config):
    """Test that the new project page loads with expected elements."""
    wait = WebDriverWait(logged_driver, 10)

    logged_driver.get(f"{configs.app_base_url}/projects/new")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop [action='/projects']")))

    form = logged_driver.find_element(By.CSS_SELECTOR, "#content-desktop [action='/projects']")

    assert form.find_element(By.CSS_SELECTOR, "#classical").is_displayed()
    assert "Classical" in form.find_element(By.CSS_SELECTOR, "#classical").text
    assert form.find_element(By.CSS_SELECTOR, "#bdd").is_displayed()
    assert "BDD" in form.find_element(By.CSS_SELECTOR, "#bdd").text
    assert form.find_element(By.CSS_SELECTOR, "#project_title").is_displayed()
    assert form.find_element(By.CSS_SELECTOR, "#project-create-btn").is_displayed()
