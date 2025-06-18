.PHONY: install setup-db fetch test lint format type-check

install:
	uv venv && uv sync

setup-db:
	uv run env PYTHONPATH=src python scripts/setup_db.py sqlite:///./gmail_automation.db

fetch:
	uv run env PYTHONPATH=src python scripts/fetch_emails.py --max-results 10

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

type-check:
	uv run mypy src