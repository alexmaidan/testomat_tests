from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.waits import Wait


class ProjectsPageHeader:

    _DASHBOARD_LINK = (By.CSS_SELECTOR, ".auth-header-nav-left-items a[href='/']")
    _COMPANIES_LINK = (By.CSS_SELECTOR, ".auth-header-nav-left-items a[href='/companies']")
    _ANALYTICS_DROPDOWN_TOGGLE = (By.ID, "analytics-dropdown-toggle")
    _ANALYTICS_DROPDOWN_MENU = (By.ID, "analytics-dropdown-menu")
    _PROFILE_MENU_TOGGLE = (By.ID, "toggle-profile-menu")
    _PROFILE_MENU = (By.ID, "profile-menu")
    _ACCOUNT_LINK = (By.CSS_SELECTOR, "#profile-menu a[href='/account']")
    _SIGN_OUT_BUTTON = (By.CSS_SELECTOR, "#profile-menu button[type='submit']")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = Wait(driver, timeout)

    @property
    def dashboard_link(self) -> WebElement:
        return self.wait.for_visible(self._DASHBOARD_LINK)

    @property
    def companies_link(self) -> WebElement:
        return self.wait.for_visible(self._COMPANIES_LINK)

    @property
    def analytics_dropdown_toggle(self) -> WebElement:
        return self.wait.for_visible(self._ANALYTICS_DROPDOWN_TOGGLE)

    @property
    def analytics_dropdown_menu(self) -> WebElement:
        return self.wait.for_visible(self._ANALYTICS_DROPDOWN_MENU)

    @property
    def profile_menu(self) -> WebElement:
        return self.wait.for_visible(self._PROFILE_MENU)

    @property
    def account_link(self) -> WebElement:
        return self.wait.for_visible(self._ACCOUNT_LINK)

    @property
    def sign_out_button(self) -> WebElement:
        return self.wait.for_visible(self._SIGN_OUT_BUTTON)

    def open_profile_menu(self) -> Self:
        self.wait.for_clickable(self._PROFILE_MENU_TOGGLE).click()
        self.wait.for_visible(self._PROFILE_MENU)
        return self

    def open_analytics_dropdown(self) -> Self:
        self.wait.for_clickable(self._ANALYTICS_DROPDOWN_TOGGLE).click()
        self.wait.for_visible(self._ANALYTICS_DROPDOWN_MENU)
        return self