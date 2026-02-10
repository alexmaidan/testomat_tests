from playwright.sync_api import Page, expect


class LoginPage:
    URL = "/users/sign_in"

    def __init__(self, page: Page):
        self.page = page
        self._email_input = page.locator("#content-desktop #user_email")
        self._password_input = page.locator("#content-desktop #user_password")
        self._remember_me = page.locator("#user_remember_me")
        self._sign_in_button = page.get_by_role("button", name="Sign in")
        self._error_message = page.locator("#content-desktop").get_by_text("Invalid Email or password.")

    def open(self) -> "LoginPage":
        self.page.goto(self.URL)
        return self

    def is_loaded(self) -> "LoginPage":
        expect(self._email_input).to_be_visible()
        return self

    def clear_form(self) -> "LoginPage":
        """Clears email and password inputs for reusing the login form."""
        self._email_input.clear()
        self._password_input.clear()
        return self

    def login_user(self, email: str, password: str, remember_me: bool = False) -> "LoginPage":
        self._email_input.fill(email)
        self._password_input.fill(password)

        if remember_me:
            self._remember_me.check()

        self._sign_in_button.click()
        return self

    def invalid_login_message_visible(self) -> "LoginPage":
        expect(self._error_message).to_be_visible()
        return self
