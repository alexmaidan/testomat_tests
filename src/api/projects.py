"""API client and data models for Testomat.io Projects endpoints.

Spec: GET /api/projects  (operationId: get_projects)
Auth: JWT Bearer token passed via TESTOMAT_API_TOKEN env variable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import requests


@dataclass
class ProjectAttributes:
    """Attributes of a project resource."""

    title: str | None = None
    description: str | None = None
    slug: str | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> ProjectAttributes:
        """Build from a JSON:API attributes dict.

        Handles both snake_case and kebab-case keys that the API may return.
        """
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            slug=data.get("slug"),
            status=data.get("status"),
            created_at=data.get("created-at") or data.get("created_at"),
            updated_at=data.get("updated-at") or data.get("updated_at"),
        )


@dataclass
class Project:
    """Single project resource following JSON:API structure."""

    id: str
    type: str
    attributes: ProjectAttributes = field(default_factory=ProjectAttributes)

    @classmethod
    def from_dict(cls, data: dict) -> Project:
        """Build from a single JSON:API resource object."""
        return cls(
            id=str(data["id"]),
            type=data.get("type", ""),
            attributes=ProjectAttributes.from_dict(data.get("attributes", {})),
        )


@dataclass
class ProjectsResponse:
    """Response model for GET /api/projects.

    JSON:API top-level document containing a list of project resources.
    """

    data: list[Project] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> ProjectsResponse:
        """Build from the full JSON response body."""
        projects = [Project.from_dict(item) for item in data.get("data", [])]
        return cls(data=projects)

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: int) -> Project:
        return self.data[index]


class ProjectsApi:
    """Client for /api/projects endpoint."""

    def __init__(self, base_url: str, api_token: str):
        """
        Args:
            base_url:  Root URL of the Testomat.io instance, e.g. https://app.testomat.io
            api_token: JWT token obtained from login or directly from account settings.
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def get_projects(self) -> ProjectsResponse:
        """GET /api/projects — Returns all projects for the authenticated user.

        Returns:
            Typed ProjectsResponse with a list of Project objects.

        Raises:
            requests.HTTPError: if the response status is 4xx/5xx.
        """
        url = f"{self.base_url}/api/projects"
        response = self.session.get(url)
        response.raise_for_status()
        return ProjectsResponse.from_dict(response.json())
