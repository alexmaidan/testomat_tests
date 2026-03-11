"""API client for Testomat.io Authentication endpoint.

Spec (from description): POST /api/login
Supports two auth methods:
  1. api_token  — pass the TESTOMAT_API_TOKEN directly
  2. email + password — standard credentials
"""

import requests


class AuthApi:
    """Client for POST /api/login endpoint."""

    def __init__(self, base_url: str):
        """
        Args:
            base_url: Root URL of the Testomat.io instance, e.g. https://app.testomat.io
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def login_with_token(self, api_token: str) -> requests.Response:
        """POST /api/login using an API token.

        Args:
            api_token: Testomat.io API token from account settings.

        Returns:
            Raw Response object (caller can inspect status, body, etc.)
        """
        url = f"{self.base_url}/api/login"
        return self.session.post(url, json={"api_token": api_token})

    def login_with_credentials(self, email: str, password: str) -> requests.Response:
        """POST /api/login using email + password.

        Args:
            email:    User email address.
            password: User password.

        Returns:
            Raw Response object.
        """
        url = f"{self.base_url}/api/login"
        return self.session.post(url, json={"email": email, "password": password})
