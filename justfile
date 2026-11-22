# Common steps. `just` lists them.

default:
    @just --list

# What a development run of the hub has in its environment: Django's debug
# mode, and accounts held by the hub itself in place of GitHub sign-in.
dev := "env HUB_DEBUG=1 HUB_SIGN_IN=local"

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

# The hub's tests, on SQLite unless DATABASE_URL names Postgres
test *args:
    uv run pytest {{args}}

# Run the hub under Muru at http://127.0.0.1:9080/, migrating its database first; arguments go to muructl run, as in `just hub --open`
hub *args: migrate
    {{dev}} uv run muructl run {{args}}

# Run the hub's jobs worker beside `just hub`
worker:
    {{dev}} uv run python manage.py db_worker

# This runs manage.py itself, not the declared command (`muructl command run
# migrate`), which on its own uses another data directory than the run:
# muruhq/muru#859.
#
# Apply the hub's database migrations to the development database
migrate:
    {{dev}} uv run python manage.py migrate --noinput

# A manage.py command with the development settings, such as `just manage createsuperuser`
manage *args:
    {{dev}} uv run python manage.py {{args}}

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
