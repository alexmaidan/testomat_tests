from playwright.sync_api import Page, expect

from tests.config import Config


def test_login_with_invalid_creds(page: Page):
    open_homepage(page)

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    page.locator("#content-desktop #user_email").fill(Config.TEST_USER_EMAIL)
    page.locator("#content-desktop #user_password").fill("pass%^ii")
    page.get_by_role("button", name="Sign in").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page):
    open_login_page(page)
    login_user(page, Config.TEST_USER_EMAIL, Config.TEST_USER_PASSWORD)
    target_project = "A Passage to India"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_visible()


def test_should_be_possible_to_open_free_project(page: Page):
    open_login_page(page)
    login_user(page, Config.TEST_USER_EMAIL, Config.TEST_USER_PASSWORD)
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")
    target_project = "A Passage to India"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


# Helper functions

def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def open_homepage(page: Page):
    page.goto(Config.BASE_URL)


def open_login_page(page: Page):
    page.goto(f"{Config.APP_URL}/users/sign_in")


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()
