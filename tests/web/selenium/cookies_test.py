import pytest
from selenium.webdriver.chrome.webdriver import WebDriver


@pytest.mark.smoke
@pytest.mark.web
def test_add_feature_flag_cookie(logged_driver: WebDriver):
    logged_driver.add_cookie({"name": "feature_flag", "value": "dark_mode_enabled"})

    cookie = logged_driver.get_cookie("feature_flag")
    assert cookie is not None
    assert cookie["value"] == "dark_mode_enabled"

    logged_driver.refresh()


@pytest.mark.web
def test_clear_feature_flag_cookie(logged_driver: WebDriver):
    """Verify that a feature flag cookie can be cleared."""
    logged_driver.add_cookie({"name": "feature_flag", "value": "beta_feature"})
    assert logged_driver.get_cookie("feature_flag") is not None

    logged_driver.delete_cookie("feature_flag")
    assert logged_driver.get_cookie("feature_flag") is None


@pytest.mark.web
def test_add_multiple_feature_flags(logged_driver: WebDriver):
    """Verify that multiple feature flag cookies can be added."""
    logged_driver.add_cookie({"name": "feature_dark_mode", "value": "enabled"})
    logged_driver.add_cookie({"name": "feature_new_ui", "value": "disabled"})

    assert logged_driver.get_cookie("feature_dark_mode")["value"] == "enabled"
    assert logged_driver.get_cookie("feature_new_ui")["value"] == "disabled"
