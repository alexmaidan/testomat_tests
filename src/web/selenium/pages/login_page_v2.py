from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.web.constants import Urls
from src.web.selenium.core.base_page import BasePage


class LoginPageV2(BasePage):
    """Login page object using @property for lazy element access."""

    URL = Urls.LOGIN

    _EMAIL_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_email")
    _PASSWORD_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_password")
    _REMEMBER_ME = (By.ID, "user_remember_me")
    _SIGN_IN_BUTTON = (By.CSS_SELECTOR, "#content-desktop [value='Sign In']")
    _ERROR_MESSAGE = (By.XPATH, "//*[@id='content-desktop']//*[contains(.,'Invalid email or password.') and not(.//*[contains(.,'Invalid email or password.')])]")
    _SUCCESS_FLASH = (By.CSS_SELECTOR, "#content-desktop .common-flash-success")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, timeout)

    @property
    def email_input(self) -> WebElement:
        return self.find_visible(self._EMAIL_INPUT)

    @property
    def password_input(self) -> WebElement:
        return self.find_visible(self._PASSWORD_INPUT)

    @property
    def remember_me_checkbox(self) -> WebElement:
        return self.find_clickable(self._REMEMBER_ME)

    @property
    def sign_in_button(self) -> WebElement:
        return self.find_clickable(self._SIGN_IN_BUTTON)

    @property
    def error_message(self) -> WebElement:
        return self.find_visible(self._ERROR_MESSAGE)

    @property
    def success_flash(self) -> WebElement:
        return self.find_visible(self._SUCCESS_FLASH)

    def is_loaded(self) -> Self:
        self.email_input
        return self

    def clear_form(self) -> Self:
        self.email_input.clear()
        self.password_input.clear()
        return self

    def login_user(self, email: str, password: str, remember_me: bool = False) -> Self:
        self.email_input.clear()
        self.email_input.send_keys(email)
        self.password_input.clear()
        self.password_input.send_keys(password)

        if remember_me and not self.remember_me_checkbox.is_selected():
            self.remember_me_checkbox.click()

        self.sign_in_button.click()
        return self

    def has_invalid_login_message(self) -> Self:
        self.error_message
        return self

    def has_success_flash(self) -> Self:
        self.success_flash
        return self