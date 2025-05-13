# Makefile for project pandasAi_to_pandas
# Provides common development commands.

# Default shell for Makefile
SHELL := /bin/bash
# Get project name from directory name
PROJECT_SLUG := $(shell basename $(CURDIR))
# Activate poetry environment for commands
POETRY_RUN := poetry run

.PHONY: help install install-dev test lint format clean run

help:
	@echo "Makefile for pandasAi_to_pandas"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       Install project dependencies (production)"
	@echo "  make install-dev   Install all dependencies including development"
	@echo "  make test          Run tests using pytest"
	@echo "  make lint          Check code style with flake8 and black (check mode)"
	@echo "  make format        Format code with black"
	@echo "  make clean         Remove temporary files (build artifacts, pycache, etc.)"
	@echo "  make run           (Placeholder) Run the main application"
	@echo ""
	@echo "To activate the virtual environment, ensure direnv is setup or run 'poetry shell'."

# Default target when 'make' is run
default: help

install:
	@echo "🛠️ Installing project dependencies (production)..."
	poetry install --no-dev --no-interaction --no-ansi

install-dev:
	@echo "🛠️ Installing all dependencies (including dev)..."
	poetry install --no-interaction --no-ansi

test:
	@echo "🧪 Running tests..."
	$(POETRY_RUN) pytest tests/

lint:
	@echo "🔍 Checking code style with flake8..."
	$(POETRY_RUN) flake8 src/ tests/
	@echo "🔍 Checking code formatting with black (check mode)..."
	$(POETRY_RUN) black --check src/ tests/

format:
	@echo "🎨 Formatting code with black..."
	$(POETRY_RUN) black src/ tests/

clean:
	@echo "🧹 Cleaning up temporary files..."
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info .mypy_cache
	@echo "🧼 Clean complete."

run:
	@echo "🚀 (Placeholder) Running application pandasAi_to_pandas..."
	# Replace with your actual run command, e.g.:
	# $(POETRY_RUN) python src//main.py
	@echo "   Please update 'make run' target in Makefile with your application's entry point."

