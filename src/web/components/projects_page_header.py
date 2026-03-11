from typing import Self

from playwright.sync_api import Page, expect


class ProjectsPageHeader:
    """Component representing the header navigation on the projects page."""

    def __init__(self, page: Page):
        """Initialize ProjectsPageHeader with page locators.

        Args:
            page: Playwright Page instance
        """
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

    def is_visible(self) -> Self:
        """Assert that the header is visible.

        Returns:
            Self for method chaining
        """
        expect(self._header_nav).to_be_visible()
        return self

    def click_dashboard(self) -> Self:
        """Click the dashboard link.

        Returns:
            Self for method chaining
        """
        self._dashboard_link.click()
        return self

    def click_companies(self) -> Self:
        """Click the companies link.

        Returns:
            Self for method chaining
        """
        self._companies_link.click()
        return self

    def open_analytics_dropdown(self) -> Self:
        """Open the analytics dropdown menu.

        Returns:
            Self for method chaining
        """
        self._analytics_dropdown_toggle.click()
        return self

    def click_analytics(self) -> Self:
        """Click the analytics link.

        Returns:
            Self for method chaining
        """
        self.open_analytics_dropdown()
        self._analytics_link.click()
        return self

    def click_dashboards(self) -> Self:
        """Click the dashboards link.

        Returns:
            Self for method chaining
        """
        self.open_analytics_dropdown()
        self._dashboards_link.click()
        return self

    def click_docs(self) -> Self:
        """Click the docs link.

        Returns:
            Self for method chaining
        """
        self._docs_link.click()
        return self

    def click_changelog(self) -> Self:
        """Click the changelog link.

        Returns:
            Self for method chaining
        """
        self._changelog_link.click()
        return self

    def click_public_api(self) -> Self:
        """Click the public API link.

        Returns:
            Self for method chaining
        """
        self._public_api_link.click()
        return self

    def click_new_project(self) -> Self:
        """Click the new project button.

        Returns:
            Self for method chaining
        """
        self._new_project_button.click()
        return self

    def open_global_search(self) -> Self:
        """Open the global search modal.

        Returns:
            Self for method chaining
        """
        self._global_search_button.click()
        expect(self._global_search_modal).to_be_visible()
        return self

    def search_globally(self, query: str) -> Self:
        """Perform a global search.

        Args:
            query: Search query string

        Returns:
            Self for method chaining
        """
        self.open_global_search()
        self._global_search_input.fill(query)
        self._global_search_input.press("Enter")
        return self

    def close_global_search(self) -> Self:
        """Close the global search modal.

        Returns:
            Self for method chaining
        """
        self._page.keyboard.press("Escape")
        return self

    def is_global_search_visible(self) -> Self:
        """Assert that the global search modal is visible.

        Returns:
            Self for method chaining
        """
        expect(self._global_search_modal).to_be_visible()
        return self

    def is_global_search_hidden(self) -> Self:
        """Assert that the global search modal is hidden.

        Returns:
            Self for method chaining
        """
        expect(self._global_search_modal).to_be_hidden()
        return self

    def open_profile_menu(self) -> Self:
        """Open the profile menu dropdown.

        Returns:
            Self for method chaining
        """
        self._profile_menu_toggle.click()
        expect(self._profile_menu).to_be_visible()
        return self

    def click_my_companies(self) -> Self:
        """Click the my companies link in profile menu.

        Returns:
            Self for method chaining
        """
        self.open_profile_menu()
        self._my_companies_link.click()
        return self

    def click_account(self) -> Self:
        """Click the account link in profile menu.

        Returns:
            Self for method chaining
        """
        self.open_profile_menu()
        self._account_link.click()
        return self

    def click_downloads(self) -> Self:
        """Click the downloads link in profile menu.

        Returns:
            Self for method chaining
        """
        self.open_profile_menu()
        self._downloads_link.click()
        return self

    def click_request_trial(self) -> Self:
        """Click the request trial link in profile menu.

        Returns:
            Self for method chaining
        """
        self.open_profile_menu()
        self._request_trial_link.click()
        return self

    def sign_out(self) -> Self:
        """Sign out the current user.

        Returns:
            Self for method chaining
        """
        self.open_profile_menu()
        self._sign_out_button.click()
        return self

    def has_dashboard_active(self) -> Self:
        """Assert that the dashboard link is active.

        Returns:
            Self for method chaining
        """
        expect(self._dashboard_link).to_have_class("current")
        return self

    def has_companies_active(self) -> Self:
        """Assert that the companies link is active.

        Returns:
            Self for method chaining
        """
        expect(self._companies_link).to_have_class("current")
        return self
