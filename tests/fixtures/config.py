"""Configuration fixtures for pytest."""

import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    app_base_url: str
    email: str
    password: str
    api_token: str


@pytest.fixture(scope="session")
def configs():
    """Session-scoped configuration loaded from environment variables."""
    return Config(
        base_url=os.getenv("BASE_URL"),
        app_base_url=os.getenv("APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        api_token=os.getenv("TESTOMAT_API_TOKEN"),
    )
