from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def test_selenium_login_and_search(logged_driver: WebDriver):
    driver = logged_driver
    wait = WebDriverWait(
        driver, 10, poll_frequency=0.1, ignored_exceptions=[StaleElementReferenceException, NoSuchElementException]
    )

    target_project = "Manufacture light"
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #search").send_keys(target_project)
    driver.find_element(By.CSS_SELECTOR, f"#content-desktop [title='{target_project}']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f".breadcrumbs-page [title='{target_project}']")))
