"""Helper functions for test automation."""

from faker import Faker


def generate_project_name() -> str:
    """Generate a random project name using Faker.

    Returns:
        A random company name as project name
    """
    return Faker().company()


def generate_random_email() -> str:
    """Generate a random email address.

    Returns:
        A random email address
    """
    return Faker().email()


def generate_random_password(length: int = 10) -> str:
    """Generate a random password.

    Args:
        length: Password length (default: 10)

    Returns:
        A random password string
    """
    return Faker().password(length=length)

