# Testomat Tests

Automated test suite for Testomat using Playwright and pytest.

## Project Structure

```
testomat_tests/
├── src/                    # Source code
│   ├── core/               # Base classes (BasePage, BaseComponent)
│   ├── utils/              # Helper utilities (Faker-based generators)
│   └── web/                # Web automation
│       ├── components/     # UI components (ProjectCard, SideBar, etc.)
│       └── pages/          # Page objects (HomePage, LoginPage, etc.)
├── tests/                  # Test suites
│   ├── data/               # Test data
│   └── web/                # Web UI tests
├── test-result/            # Test reports (HTML reports, traces)
└── videos/                 # Video recordings of test runs
```

## Setup

### Prerequisites

- Python 3.14+
- [UV](https://docs.astral.sh/uv/) package manager

### Installation

1. Clone the repository
2. Install dependencies:

```bash
uv sync
```

3. Install Playwright browsers:

```bash
uv run playwright install
```

4. Create `.env` file from `example.env` and configure your credentials.

## Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/web/login_page_test.py

# Run tests with markers
uv run pytest -m smoke       # Quick smoke tests
uv run pytest -m regression  # Full regression suite
uv run pytest -m web         # Web UI tests
uv run pytest -m slow        # Tests that take longer to execute

# Run in headless mode (override default)
uv run pytest --headless
```

## Development

### Linting

```bash
uv run ruff check .
uv run ruff format .
```

## Configuration

- `pyproject.toml` - Project configuration, dependencies, pytest and ruff settings
- `example.env` - Environment variables template

## Features

- **Page Object Pattern** - Clean separation between test logic and UI interactions
- **Playwright Integration** - Modern browser automation with pytest-playwright
- **Video Recording** - Automatic video capture of test runs (saved to `videos/`)
- **Tracing** - Playwright traces retained on failures for debugging
- **HTML Reports** - Self-contained test reports generated in `test-result/`
- **Screenshots** - Automatic screenshots on test failures
- **Faker Integration** - Random test data generation for dynamic testing

## Environment Variables

| Variable | Description          |
|----------|----------------------|
| EMAIL    | Login email          |
| PASSWORD | Login password       |
| BASE_URL | Base URL for testing |
| APP_URL  | Application URL      |

