# Common steps. `just` lists them.

default:
    @just --list

# The development environment and the git hooks
bootstrap:
    uv sync
    uv run pre-commit install
    uv run pre-commit install --hook-type commit-msg

# ruff, mypy and the repository text checks
lint:
    uv run ruff format --check
    uv run ruff check
    uv run mypy
    sh scripts/check-no-em-dashes.sh
    git ls-files '*.py' | xargs uv run python scripts/check-layout.py
    uv run python scripts/check-user-docs.py

# Build the documentation from nothing, with warnings as errors
docs:
    rm -rf docs/_build
    uv run sphinx-build -W --keep-going -b html docs docs/_build/html

# Build the documentation and serve it with live reload on port 8000
docs-serve:
    uv run sphinx-autobuild docs docs/_build/html --port 8000

# Install or update the Muru skill for coding agents from the pinned muructl
skill:
    uv run muructl mcp skill install
