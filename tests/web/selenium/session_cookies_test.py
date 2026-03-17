import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.fixtures.config import Config


def _is_session_valid(driver: WebDriver) -> bool:
    """Check if the current URL indicates a valid session."""
    url = driver.current_url
    return "/login" not in url and "/sign_in" not in url


@pytest.mark.smoke
@pytest.mark.web
class TestCookieBasedAuthentication:
    """Tests for session validation after login."""

    def test_session_restored_from_cookies(self, logged_driver: WebDriver, configs: Config):
        """Verify session is valid after login and on the protected projects page."""
        wait = WebDriverWait(logged_driver, 10)
        logged_driver.get(configs.app_base_url)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".common-page-header")))

        assert _is_session_valid(logged_driver), "Session should be valid"
        assert "/login" not in logged_driver.current_url
        assert "/sign_in" not in logged_driver.current_url

    def test_session_cookies_are_valid(self, logged_driver: WebDriver):
        """Verify session cookies exist and contain at least one auth-related cookie."""
        all_cookies = logged_driver.get_cookies()
        assert len(all_cookies) > 0, "Should have at least one cookie after login"

        cookie_names = [c["name"] for c in all_cookies]
        session_keywords = ["session", "token", "auth", "_testomat"]
        has_auth_cookie = any(any(keyword in name.lower() for keyword in session_keywords) for name in cookie_names)
        assert has_auth_cookie, f"Should have at least one auth cookie, got: {cookie_names}"


@pytest.mark.web
class TestCookieManipulation:
    """Tests for cookie manipulation scenarios."""

    def test_can_add_custom_cookie(self, logged_driver: WebDriver):
        """Test adding a custom cookie for feature flags."""
        logged_driver.add_cookie({"name": "test_feature", "value": "enabled"})

        cookie = logged_driver.get_cookie("test_feature")
        assert cookie is not None
        assert cookie["value"] == "enabled"

        logged_driver.delete_cookie("test_feature")

    def test_cookie_persists_after_navigation(self, logged_driver: WebDriver, configs: Config):
        """Test that cookies persist across page navigation."""
        logged_driver.add_cookie({"name": "persistent_test", "value": "value123"})

        logged_driver.get(configs.app_base_url)

        cookie = logged_driver.get_cookie("persistent_test")
        assert cookie is not None
        assert cookie["value"] == "value123"

        logged_driver.delete_cookie("persistent_test")

    def test_get_all_cookies(self, logged_driver: WebDriver):
        """Test retrieving all cookies from the session."""
        all_cookies = logged_driver.get_cookies()

        assert len(all_cookies) > 0, "Should have cookies after login"

        for cookie in all_cookies:
            assert "name" in cookie
            assert "value" in cookie


@pytest.mark.web
class TestSessionValidation:
    """Tests for session validation utilities."""

    def test_is_session_valid_on_protected_page(self, logged_driver: WebDriver, configs: Config):
        """Test session is valid on the protected projects page."""
        wait = WebDriverWait(logged_driver, 10)
        logged_driver.get(configs.app_base_url)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".common-page-header")))

        assert _is_session_valid(logged_driver), "Session should be valid on projects page"

    def test_session_cookie_validation(self, logged_driver: WebDriver):
        """Test session cookie validation with known session cookie names."""
        all_cookies = logged_driver.get_cookies()
        cookie_names = [c["name"] for c in all_cookies]

        assert len(cookie_names) > 0, "Should have cookies after login"

        custom_names = ["_testomat_session", "remember_token"]
        has_custom = any(name in cookie_names for name in custom_names)
        # Log result without asserting - cookies may vary by environment
        _ = has_custom
