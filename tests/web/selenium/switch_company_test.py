import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from tests.fixtures.config import Config


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_driver: WebDriver, configs: Config):
    """Test switching between Enterprise and Free Projects company contexts."""
    wait = WebDriverWait(logged_driver, 10)

    logged_driver.get(configs.app_base_url)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#grid ul.grid")))

    # Verify enterprise plan label is visible
    enterprise_label = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Enterprise')]")))
    assert enterprise_label.is_displayed()

    # Switch to Free Projects company
    company_select = Select(logged_driver.find_element(By.CSS_SELECTOR, "#company_id"))
    company_select.select_by_visible_text("Free Projects")

    # Wait for page content to update after company switch
    # Note: plan label HTML uses lowercase ("free plan"), CSS renders it as "Free Plan"
    long_wait = WebDriverWait(logged_driver, 20)
    long_wait.until(lambda d: "You have not created any projects yet" in d.page_source)
    long_wait.until(lambda d: "free plan" in d.page_source.lower())

    no_projects_els = logged_driver.find_elements(
        By.XPATH, "//*[contains(., 'You have not created any projects yet') and not(*)]"
    )
    assert len(no_projects_els) > 0
    assert any(el.is_displayed() for el in no_projects_els)

    plan_badge = logged_driver.find_element(By.CSS_SELECTOR, ".tooltip-project-plan")
    assert plan_badge.is_displayed()
    assert "free" in plan_badge.text.lower()
