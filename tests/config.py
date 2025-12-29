import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Test configuration from environment variables"""

    # User credentials
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "")

    # URLs
    BASE_URL = os.getenv("TEST_BASE_URL", "https://testomat.io")
    APP_URL = os.getenv("TEST_APP_URL", "https://app.testomat.io")

    @classmethod
    def validate(cls):
        """Validate that required config is present"""
        if not cls.TEST_USER_EMAIL or not cls.TEST_USER_PASSWORD:
            raise ValueError(
                "Missing credentials! Please set TEST_USER_EMAIL and TEST_USER_PASSWORD "
                "in your .env file or environment variables."
            )


# Validate config on import
Config.validate()
