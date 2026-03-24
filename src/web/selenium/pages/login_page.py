from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.constants import Urls
from src.web.selenium.core.base_page import BasePage


class LoginPage(BasePage):
    """Login page object for user authentication via Selenium."""

    URL = Urls.LOGIN

    _EMAIL_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_email")
    _PASSWORD_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_password")
    _REMEMBER_ME = (By.ID, "user_remember_me")
    _SIGN_IN_BUTTON = (By.CSS_SELECTOR, "#content-desktop [value='Sign In']")
    _ERROR_MESSAGE = (By.XPATH, "//*[@id='content-desktop']//*[contains(.,'Invalid email or password.') and not(.//*[contains(.,'Invalid email or password.')])]")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, timeout)

    def is_loaded(self) -> Self:
        self.find_visible(self._EMAIL_INPUT)
        return self

    def clear_form(self) -> Self:
        self.find_visible(self._EMAIL_INPUT).clear()
        self.find_visible(self._PASSWORD_INPUT).clear()
        return self

    def login_user(self, email: str, password: str, remember_me: bool = False) -> Self:
        self.type_text(self._EMAIL_INPUT, email)
        self.type_text(self._PASSWORD_INPUT, password)

        if remember_me:
            checkbox = self.find_clickable(self._REMEMBER_ME)
            if not checkbox.is_selected():
                checkbox.click()

        self.click(self._SIGN_IN_BUTTON)
        return self

    def has_invalid_login_message(self) -> Self:
        self.find_visible(self._ERROR_MESSAGE)
        return self