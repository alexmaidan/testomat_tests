"""API tests for:
  - POST /api/login  (authentication)
  - GET  /api/projects  (operationId: get_projects)

Authentication: TESTOMAT_API_TOKEN environment variable (JWT Bearer token).
Fixtures: defined in tests/fixtures/api.py
"""

from src.api.auth import AuthApi
from src.api.projects import Project, ProjectAttributes, ProjectsApi, ProjectsResponse
from tests.fixtures.config import Config


class TestLogin:
    """Tests for POST /api/login."""

    def test_login_with_token_returns_200(self, auth_api: AuthApi, configs: Config):
        """Login via API token returns HTTP 200."""
        response = auth_api.login_with_token(configs.api_token)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

    def test_login_with_token_returns_jwt(self, auth_api: AuthApi, configs: Config):
        """Login via API token response body contains a 'jwt' field."""
        response = auth_api.login_with_token(configs.api_token)
        body = response.json()
        assert "jwt" in body, f"'jwt' key missing from login response: {body}"
        assert body["jwt"], "JWT token value is empty"

    def test_login_with_credentials_returns_200(self, auth_api: AuthApi, configs: Config):
        """Login via email + password returns HTTP 200."""
        response = auth_api.login_with_credentials(configs.email, configs.password)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

    def test_login_with_credentials_returns_jwt(self, auth_api: AuthApi, configs: Config):
        """Login via email + password response body contains a 'jwt' field."""
        response = auth_api.login_with_credentials(configs.email, configs.password)
        body = response.json()
        assert "jwt" in body, f"'jwt' key missing from login response: {body}"
        assert body["jwt"], "JWT token value is empty"

    def test_login_with_invalid_token_returns_401(self, auth_api: AuthApi):
        """Login with a wrong API token returns HTTP 401."""
        response = auth_api.login_with_token("invalid_token")
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    def test_login_with_invalid_credentials_returns_401(self, auth_api: AuthApi):
        """Login with wrong email/password returns HTTP 401."""
        response = auth_api.login_with_credentials("wrong@example.com", "wrongpassword")
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"


class TestGetProjects:
    """Tests for GET /api/projects — get_projects."""

    def test_get_projects_returns_response(self, projects_api: ProjectsApi):
        """Request succeeds and returns a ProjectsResponse."""
        response = projects_api.get_projects()
        assert isinstance(response, ProjectsResponse)

    def test_get_projects_list_not_empty(self, projects_api: ProjectsApi):
        """Authenticated user has at least one project."""
        response = projects_api.get_projects()
        assert len(response) > 0, "No projects returned for this user"

    def test_get_projects_items_are_project_instances(self, projects_api: ProjectsApi):
        """Each item in the response is a Project dataclass."""
        response = projects_api.get_projects()
        for project in response:
            assert isinstance(project, Project)

    def test_get_projects_items_have_id_and_type(self, projects_api: ProjectsApi):
        """Each project has a non-empty id and type."""
        response = projects_api.get_projects()
        for project in response:
            assert project.id, f"Project has empty id: {project}"
            assert project.type, f"Project has empty type: {project}"

    def test_get_projects_items_have_attributes(self, projects_api: ProjectsApi):
        """Each project has a ProjectAttributes instance."""
        response = projects_api.get_projects()
        for project in response:
            assert isinstance(project.attributes, ProjectAttributes)

    def test_get_projects_items_have_title(self, projects_api: ProjectsApi):
        """Each project has a non-empty title in attributes."""
        response = projects_api.get_projects()
        for project in response:
            assert project.attributes.title, f"Project {project.id} has empty title"
