from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
TEST_RESULT_DIR = PROJECT_ROOT / "test-result"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add Selenium-specific execution mode flags."""
    group = parser.getgroup("selenium")
    group.addoption(
        "--selenium-headed",
        action="store_true",
        default=False,
        help="Run Selenium tests in headed mode (show browser window).",
    )
    group.addoption(
        "--selenium-headless",
        action="store_true",
        default=False,
        help="Run Selenium tests in headless mode.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest settings and custom markers."""
    if config.option.htmlpath:
        config.option.htmlpath = str(TEST_RESULT_DIR / "report.html")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call) -> None:
    """
    Make test results available to fixtures.
    Used by stop_tracing_on_failure in app fixtures.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.selenium",
    "tests.fixtures.app",
    "tests.fixtures.api",
]
