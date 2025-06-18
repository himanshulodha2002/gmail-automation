.PHONY: help install setup-db fetch process-rules test lint format type-check clean

# Variables (can be overridden: make fetch MAX_RESULTS=20)
DB_DIR ?= data
DB_FILE ?= gmail_automation.db
DB_URL ?= sqlite:///./$(DB_DIR)/$(DB_FILE)
MAX_RESULTS ?= 10

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install         Create venv and install dependencies"
	@echo "  setup-db        Initialize the database"
	@echo "  fetch           Fetch emails from Gmail"
	@echo "  process-rules   Process emails with rules"
	@echo "  test            Run tests"
	@echo "  lint            Run linter"
	@echo "  format          Format code"
	@echo "  type-check      Run type checks"
	@echo "  clean           Remove .venv and database"

install:
	uv venv && uv sync

setup-db:
	mkdir -p $(DB_DIR)
	uv run env PYTHONPATH=src python scripts/setup_db.py $(DB_URL)

fetch:
	uv run env PYTHONPATH=src python scripts/fetch_emails.py --max-results $(MAX_RESULTS)

process-rules:
	uv run env PYTHONPATH=src python scripts/process_rules.py

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

type-check:
	uv run mypy src

clean:
	rm -rf .venv $(DB_DIR) __pycache__ src/**/__pycache__