# Testomat Tests

Automated test suite for Testomat using Playwright and pytest.

## Project Structure

```
testomat_tests/
├── src/                    # Source code
│   ├── core/               # Base classes
│   ├── utils/              # Helper utilities
│   └── web/                # Web automation
│       ├── components/     # UI components
│       └── pages/          # Page objects
├── tests/                  # Test suites
│   ├── data/               # Test data
│   └── web/                # Web UI tests
└── test-result/            # Test reports
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
uv run pytest -m smoke
uv run pytest -m regression
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

## Environment Variables

| Variable | Description          |
|----------|----------------------|
| EMAIL    | Login email          |
| PASSWORD | Login password       |
| BASE_URL | Base URL for testing |
| APP_URL  | Application URL      |

