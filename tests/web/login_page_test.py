import pytest
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config

fake = Faker()

# =============================================================================
# TEST DESIGN TECHNIQUES:
# 1. Equivalence Class Partitioning (ECP) - divides input into valid/invalid classes
# 2. Boundary Value Analysis (BVA) - tests at the edges of input ranges
# =============================================================================
# EMAIL CLASSES: empty, no @, no domain, no local part, invalid chars, spaces
# PASSWORD CLASSES: empty, only spaces, valid format but wrong
# BVA EMAIL: min length, max length (255), exceeds max
# BVA PASSWORD: 1 char, 5-9 chars (around typical 8 char minimum), 100+, 255 chars
# =============================================================================

invalid_login_test_data = [
    # --- Equivalence Class Partitioning: Email ---
    pytest.param("", fake.password(length=10), id="EC_empty_email"),
    pytest.param("userwithoutat.com", fake.password(length=10), id="EC_email_no_at"),
    pytest.param("user@", fake.password(length=10), id="EC_email_no_domain"),
    pytest.param("@domain.com", fake.password(length=10), id="EC_email_no_local"),
    pytest.param("user<>@domain.com", fake.password(length=10), id="EC_email_invalid_chars"),
    pytest.param("user name@domain.com", fake.password(length=10), id="EC_email_with_space"),
    pytest.param(" user@domain.com", fake.password(length=10), id="EC_email_leading_space"),
    pytest.param("user@domain.com ", fake.password(length=10), id="EC_email_trailing_space"),

    # --- Equivalence Class Partitioning: Password ---
    pytest.param(fake.email(), "", id="EC_empty_password"),
    pytest.param(fake.email(), "        ", id="EC_password_only_spaces"),

    # --- Boundary Value Analysis: Email ---
    pytest.param("a@b.co", fake.password(length=10), id="BVA_email_min_length"),
    pytest.param(f"{'a' * 64}@{'b' * 185}.com", fake.password(length=10), id="BVA_email_max_255"),
    pytest.param(f"{'a' * 100}@{'b' * 200}.com", fake.password(length=10), id="BVA_email_exceeds_max"),

    # --- Boundary Value Analysis: Password ---
    pytest.param(fake.email(), "a", id="BVA_password_1_char"),
    pytest.param(fake.email(), "abc45", id="BVA_password_5_chars"),
    pytest.param(fake.email(), "abcde6", id="BVA_password_6_chars"),
    pytest.param(fake.email(), "abcdef7", id="BVA_password_7_chars"),
    pytest.param(fake.email(), "abcdefg8", id="BVA_password_8_chars"),
    pytest.param(fake.email(), "abcdefgh9", id="BVA_password_9_chars"),
    pytest.param(fake.email(), fake.password(length=100), id="BVA_password_100_chars"),
    pytest.param(fake.email(), fake.password(length=255), id="BVA_password_255_chars"),

    # --- Wrong credentials (valid format, non-existent user) ---
    pytest.param(fake.email(), fake.password(length=10), id="EC_nonexistent_user"),

    # --- Security: XSS and SQL Injection ---
    pytest.param(fake.email(), "<script>alert('XSS')</script>", id="SEC_xss_in_password"),
    pytest.param(fake.email(), "' OR '1'='1", id="SEC_sql_injection_password"),
]


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("email,password", invalid_login_test_data)
def test_login_invalid(persistent_login_app: Application, email: str, password: str):
    """
    Uses persistent_login_app fixture - same page for all parametrized tests.
    Login page is opened once, form is cleared between tests.
    """
    persistent_login_app.login_page.clear_form()
    persistent_login_app.login_page.login_user(email, password)
    persistent_login_app.login_page.invalid_login_message_visible()
    persistent_login_app.login_page.wait_for_timeout(2000)  # Wait briefly to ensure no navigation occurs



@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(app: Application, configs: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)

    app.projects_page.is_loaded()
