from typing import Self

from playwright.sync_api import Page, expect

from src.core.base_page import BasePage
from src.web.constants import Urls


class LoginPage(BasePage):
    """Login page object for user authentication."""

    URL = Urls.LOGIN

    def __init__(self, page: Page):
        """Initialize LoginPage with page locators.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self._email_input = page.locator("#content-desktop #user_email")
        self._password_input = page.locator("#content-desktop #user_password")
        self._remember_me = page.locator("#user_remember_me")
        self._sign_in_button = page.get_by_role("button", name="Sign in")
        self._error_message = page.locator("#content-desktop").get_by_text("Invalid Email or password.")

    def is_loaded(self) -> Self:
        """Assert that the login page is fully loaded.

        Returns:
            Self for method chaining
        """
        expect(self._email_input).to_be_visible()
        return self

    def clear_form(self) -> Self:
        """Clear email and password inputs for reusing the login form.

        Returns:
            Self for method chaining
        """
        self._email_input.clear()
        self._password_input.clear()
        return self

    def login_user(self, email: str, password: str, remember_me: bool = False) -> Self:
        """Fill in login credentials and submit the form.

        Args:
            email: User email address
            password: User password
            remember_me: Whether to check the remember me checkbox

        Returns:
            Self for method chaining
        """
        self._email_input.fill(email)
        self._password_input.fill(password)

        if remember_me:
            self._remember_me.check()

        self._sign_in_button.click()
        return self

    def has_invalid_login_message(self) -> Self:
        """Assert that the invalid login error message is visible.

        Returns:
            Self for method chaining
        """
        expect(self._error_message).to_be_visible()
        return self

    # Keep old method name for backward compatibility
    def invalid_login_message_visible(self) -> Self:
        """Deprecated: Use has_invalid_login_message() instead."""
        return self.has_invalid_login_message()

