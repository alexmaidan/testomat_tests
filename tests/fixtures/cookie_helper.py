"""Cookie helper utilities for Playwright tests."""

import json
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Cookie, Page


def get_cookies(context: BrowserContext) -> list[Cookie]:
    """
    Get all cookies from the browser context.

    Args:
        context: BrowserContext to get cookies from

    Returns:
        List of cookies as dictionaries
    """
    return context.cookies()


def get_cookie_by_name(context: BrowserContext, name: str) -> Cookie | None:
    """
    Get a specific cookie by name.

    Args:
        context: BrowserContext to get the cookie from
        name: Name of the cookie to retrieve

    Returns:
        Cookie dictionary if found, None otherwise
    """
    cookies = context.cookies()
    for cookie in cookies:
        if cookie.get("name") == name:
            return cookie
    return None


def set_cookies(context: BrowserContext, cookies: list[dict[str, Any]]) -> None:
    """
    Set cookies in the browser context.

    Args:
        context: BrowserContext to set cookies in
        cookies: List of cookie dictionaries to set
    """
    context.add_cookies(cookies)  # type: ignore[arg-type]


def delete_cookie(context: BrowserContext, name: str, domain: str | None = None) -> None:
    """
    Delete a specific cookie by name.

    Args:
        context: BrowserContext to delete the cookie from
        name: Name of the cookie to delete
        domain: Optional domain to filter by
    """
    cookies = context.cookies()
    filtered_cookies = [
        cookie
        for cookie in cookies
        if not (cookie.get("name") == name and (domain is None or cookie.get("domain") == domain))
    ]
    context.clear_cookies()
    if filtered_cookies:
        context.add_cookies(filtered_cookies)  # type: ignore[arg-type]


def clear_all_cookies(context: BrowserContext) -> None:
    """
    Clear all cookies from the browser context.

    Args:
        context: BrowserContext to clear cookies from
    """
    context.clear_cookies()


def save_cookies_to_file(context: BrowserContext, file_path: str | Path) -> None:
    """
    Save cookies to a JSON file for later use.

    Args:
        context: BrowserContext to get cookies from
        file_path: Path to save the cookies JSON file
    """
    cookies = context.cookies()
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)


def load_cookies_from_file(context: BrowserContext, file_path: str | Path) -> None:
    """
    Load cookies from a JSON file into the browser context.

    Args:
        context: BrowserContext to set cookies in
        file_path: Path to the cookies JSON file
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Cookie file not found: {file_path}")
    with open(file_path, encoding="utf-8") as f:
        cookies = json.load(f)
    context.add_cookies(cookies)


def save_storage_state(context: BrowserContext, file_path: str | Path) -> None:
    """
    Save the full storage state (cookies + localStorage) to a file.

    Args:
        context: BrowserContext to save state from
        file_path: Path to save the storage state JSON file
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(file_path))


def has_cookie(context: BrowserContext, name: str) -> bool:
    """
    Check if a cookie exists in the browser context.

    Args:
        context: BrowserContext to check
        name: Name of the cookie to find

    Returns:
        True if cookie exists, False otherwise
    """
    return get_cookie_by_name(context, name) is not None


def get_session_cookies(page: Page) -> list[Cookie]:
    """
    Get cookies for the current page's URL.

    Args:
        page: Page to get cookies for

    Returns:
        List of cookies for the page's current URL
    """
    return page.context.cookies([page.url])


def is_authenticated(context: BrowserContext, auth_cookie_name: str = "session") -> bool:
    """
    Check if the browser context has an authentication cookie.

    Args:
        context: BrowserContext to check
        auth_cookie_name: Name of the authentication cookie (default: "session")

    Returns:
        True if authenticated, False otherwise
    """
    return has_cookie(context, auth_cookie_name)


class CookieHelper:
    """Helper class for managing cookies in Playwright browser context."""

    def __init__(self, context: BrowserContext) -> None:
        """
        Initialize CookieHelper with a browser context.

        Args:
            context: BrowserContext to manage cookies for
        """
        self._context = context

    def add(self, name: str, value: str, domain: str, path: str = "/") -> None:
        """
        Add a cookie to the browser context.

        Args:
            name: Cookie name
            value: Cookie value
            domain: Cookie domain
            path: Cookie path (default: "/")
        """
        cookie = {
            "name": name,
            "value": value,
            "domain": domain,
            "path": path,
        }
        set_cookies(self._context, [cookie])

    def exists(self, name: str) -> bool:
        """
        Check if a cookie exists.

        Args:
            name: Cookie name to check

        Returns:
            True if cookie exists, False otherwise
        """
        return has_cookie(self._context, name)

    def get_value(self, name: str) -> str | None:
        """
        Get the value of a cookie by name.

        Args:
            name: Cookie name

        Returns:
            Cookie value if found, None otherwise
        """
        cookie = get_cookie_by_name(self._context, name)
        return cookie.get("value") if cookie else None

    def clear(self, name: str | None = None) -> None:
        """
        Clear cookies from the browser context.

        Args:
            name: If provided, clear only this cookie. Otherwise, clear all cookies.
        """
        if name:
            delete_cookie(self._context, name)
        else:
            clear_all_cookies(self._context)

    def get_all(self) -> list[Cookie]:
        """
        Get all cookies from the browser context.

        Returns:
            List of all cookies
        """
        return get_cookies(self._context)
