"""Tests demonstrating cookie-based session optimization.

These tests showcase how to use cookies for:
1. Fast authentication via cached session state
2. Session validation without full login
3. Cookie manipulation for testing different scenarios
"""

import pytest

from src.web.application import Application
from tests.fixtures.app import STORAGE_STATE_PATH, is_session_valid
from tests.fixtures.cookie_helper import CookieHelper


@pytest.mark.smoke
@pytest.mark.web
class TestCookieBasedAuthentication:
    """Tests for cookie-based authentication optimization."""

    def test_session_restored_from_cookies(self, logged_app: Application):
        """
        Verify session is properly restored from cached cookies.

        The logged_app fixture automatically tries to restore session
        from storage_state.json before performing a full login.
        """
        # Navigate to a protected page
        logged_app.projects_page.open()
        logged_app.projects_page.is_loaded()

        # Verify we're authenticated (not redirected to login)
        assert is_session_valid(logged_app.page), "Session should be valid"
        assert "/login" not in logged_app.page.url
        assert "/sign_in" not in logged_app.page.url

    def test_storage_state_file_created(self, logged_app: Application):
        """
        Verify storage state file is created after login.

        This file contains cookies and localStorage that can be
        reused to skip login in subsequent test runs.
        """
        # The logged_app fixture should have created the storage state
        assert STORAGE_STATE_PATH.exists(), f"Storage state file should exist at {STORAGE_STATE_PATH}"

    def test_session_cookies_are_valid(self, cookies: CookieHelper):
        """
        Verify session cookies exist and are valid.
        """
        # Check that we have valid session cookies
        assert cookies.is_session_valid(), "Should have valid session cookies"

        # Should have authentication-related cookies
        auth_cookies = cookies.get_auth_cookies()
        assert len(auth_cookies) > 0, "Should have at least one auth cookie"


@pytest.mark.web
class TestCookieManipulation:
    """Tests for cookie manipulation scenarios."""

    def test_can_add_custom_cookie(self, logged_app: Application, cookies: CookieHelper):
        """Test adding a custom cookie for feature flags."""
        cookies.add("test_feature", "enabled", "app.testomat.io")

        assert cookies.exists("test_feature")
        assert cookies.get_value("test_feature") == "enabled"

        # Cleanup
        cookies.clear(name="test_feature")

    def test_cookie_persists_after_navigation(self, logged_app: Application, cookies: CookieHelper):
        """Test that cookies persist across page navigation."""
        cookies.add("persistent_test", "value123", "app.testomat.io")

        # Navigate to different page
        logged_app.projects_page.open()

        # Cookie should still exist
        assert cookies.exists("persistent_test")
        assert cookies.get_value("persistent_test") == "value123"

        # Cleanup
        cookies.clear(name="persistent_test")

    def test_get_all_cookies(self, logged_app: Application, cookies: CookieHelper):
        """Test retrieving all cookies from context."""
        all_cookies = cookies.get_all()

        # Should have at least some cookies (session cookies)
        assert len(all_cookies) > 0, "Should have cookies in context"

        # Each cookie should have required fields
        for cookie in all_cookies:
            assert "name" in cookie
            assert "value" in cookie


@pytest.mark.web
class TestSessionValidation:
    """Tests for session validation utilities."""

    def test_is_session_valid_on_protected_page(self, logged_app: Application):
        """Test session validation on protected pages."""
        logged_app.projects_page.open()

        assert is_session_valid(logged_app.page), "Session should be valid on projects page"

    def test_session_cookie_validation(self, cookies: CookieHelper):
        """Test session cookie validation with custom cookie names."""
        # Test with default session cookie names
        is_valid = cookies.is_session_valid()
        assert is_valid, "Should have valid session with default cookie names"

        # Test with specific cookie names (may or may not exist)
        custom_names = ["_testomat_session", "remember_token"]
        cookies.is_session_valid(session_cookie_names=custom_names)
