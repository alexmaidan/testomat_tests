"""API client fixtures for pytest."""

import pytest

from src.api.auth import AuthApi
from src.api.projects import ProjectsApi
from tests.fixtures.config import Config


@pytest.fixture(scope="module")
def auth_api(configs: Config) -> AuthApi:
    """Module-scoped AuthApi client."""
    return AuthApi(base_url=configs.base_url)


@pytest.fixture(scope="module")
def projects_api(configs: Config) -> ProjectsApi:
    """Module-scoped ProjectsApi client.

    Logs in via TESTOMAT_API_TOKEN to obtain a JWT, then uses that JWT
    as the Bearer token for all project requests.
    """
    assert configs.api_token, "TESTOMAT_API_TOKEN is not set. Add it to your .env file."
    auth = AuthApi(base_url=configs.base_url)
    response = auth.login_with_token(configs.api_token)
    assert response.status_code == 200, f"Login failed with {response.status_code}: {response.text}"
    jwt = response.json()["jwt"]
    return ProjectsApi(base_url=configs.base_url, api_token=jwt)
