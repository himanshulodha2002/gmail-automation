.PHONY: install test lint format clean run

install:
    uv sync

test:
    uv run pytest tests/

test-unit:
    uv run pytest tests/unit/

test-integration:
    uv run pytest tests/integration/

lint:
    uv run ruff check src/ tests/

format:
    uv run ruff format src/ tests/

type-check:
    uv run mypy src/

clean:
    find . -type d -name __pycache__ -delete
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache
    rm -rf htmlcov
    rm -rf .coverage

run:
    uv run python -m gmail_automation.main

setup-db:
    uv run python scripts/setup_db.py sqlite:///./gmail_automation.db

fetch:
    uv run gmail-automation fetch --count 10