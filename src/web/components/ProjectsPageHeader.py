from playwright.sync_api import Page, expect


class ProjectsPageHeader:

    def __init__(self, page: Page):
        self._page = page
        self._header_nav = page.locator(".auth-header-nav")

        self._dashboard_link = page.locator(".auth-header-nav-left-items a[href='/']")
        self._companies_link = page.locator(".auth-header-nav-left-items a[href='/companies']")
        self._analytics_dropdown_toggle = page.locator("#analytics-dropdown-toggle")
        self._analytics_dropdown_menu = page.locator("#analytics-dropdown-menu")
        self._analytics_link = page.locator("#analytics-dropdown-menu a[href='/analytics']")
        self._dashboards_link = page.locator("#analytics-dropdown-menu a[href='/analytics/dashboards']")
        self._docs_link = page.locator(".auth-header-nav-left-items a[href='https://docs.testomat.io']")
        self._changelog_link = page.locator(".auth-header-nav-left-items a[href='https://changelog.testomat.io']")
        self._public_api_link = page.locator(".auth-header-nav-left-items a[href='/docs/openapi']")

        self._new_project_button = page.locator("a.auth-header-nav-right-icon-button[href='/projects/new']")
        self._global_search_button = page.locator("#showGlobalSearchBtn")
        self._profile_menu_toggle = page.locator("#toggle-profile-menu")
        self._profile_menu = page.locator("#profile-menu")
        self._user_avatar = page.locator("#user-menu-button img")

        self._my_companies_link = page.locator("#profile-menu a[href='/companies']")
        self._account_link = page.locator("#profile-menu a[href='/account']")
        self._downloads_link = page.locator("#profile-menu a[href='/account/files']")
        self._request_trial_link = page.locator("#profile-menu a[href='/trials']")
        self._sign_out_button = page.locator("#profile-menu button[type='submit']")

        self._global_search_modal = page.locator(".global-search")
        self._global_search_input = page.locator("#global_search_text")

    def is_visible(self) -> None:
        expect(self._header_nav).to_be_visible()

    def click_dashboard(self) -> None:
        self._dashboard_link.click()

    def click_companies(self) -> None:
        self._companies_link.click()

    def open_analytics_dropdown(self) -> None:
        self._analytics_dropdown_toggle.click()

    def click_analytics(self) -> None:
        self.open_analytics_dropdown()
        self._analytics_link.click()

    def click_dashboards(self) -> None:
        self.open_analytics_dropdown()
        self._dashboards_link.click()

    def click_docs(self) -> None:
        self._docs_link.click()

    def click_changelog(self) -> None:
        """Click Changelog link."""
        self._changelog_link.click()

    def click_public_api(self) -> None:
        self._public_api_link.click()

    def click_new_project(self) -> None:
        self._new_project_button.click()

    def open_global_search(self) -> None:
        self._global_search_button.click()
        expect(self._global_search_modal).to_be_visible()

    def search_globally(self, query: str) -> None:
        self.open_global_search()
        self._global_search_input.fill(query)
        self._global_search_input.press("Enter")

    def close_global_search(self) -> None:
        self._page.keyboard.press("Escape")

    def is_global_search_visible(self) -> None:
        expect(self._global_search_modal).to_be_visible()

    def is_global_search_hidden(self) -> None:
        expect(self._global_search_modal).to_be_hidden()

    def open_profile_menu(self) -> None:
        self._profile_menu_toggle.click()
        expect(self._profile_menu).to_be_visible()

    def click_my_companies(self) -> None:
        self.open_profile_menu()
        self._my_companies_link.click()

    def click_account(self) -> None:
        self.open_profile_menu()
        self._account_link.click()

    def click_downloads(self) -> None:
        self.open_profile_menu()
        self._downloads_link.click()

    def click_request_trial(self) -> None:
        self.open_profile_menu()
        self._request_trial_link.click()

    def sign_out(self) -> None:
        self.open_profile_menu()
        self._sign_out_button.click()

    def has_dashboard_active(self) -> None:
        expect(self._dashboard_link).to_have_class("current")

    def has_companies_active(self) -> None:
        expect(self._companies_link).to_have_class("current")
