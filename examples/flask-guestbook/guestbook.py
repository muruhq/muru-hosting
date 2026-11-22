"""A guestbook: a Flask application that keeps its entries in the site's data directory."""

from __future__ import annotations

import logging
import os
import sqlite3
import sys
import time
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, url_for
from werkzeug.wrappers import Response

# Change this and deploy again to see a release that differs from the last.

GREETING = "Sign the guestbook"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
log = logging.getLogger("guestbook")

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Guestbook</title>
  <link rel="stylesheet" href="/static/guestbook.css">
</head>
<body>
  <main>
    <p class="eyebrow">flask-guestbook, release {{ release }}</p>
    <h1>{{ greeting }}</h1>
    <form method="post" action="{{ url_for('sign') }}">
      <label for="name">Your name</label>
      <input id="name" name="name" required maxlength="60" autocomplete="name">
      <label for="message">A message</label>
      <input id="message" name="message" required maxlength="200">
      <button type="submit">Sign</button>
    </form>
    <h2>{{ entries|length }} {{ "entry" if entries|length == 1 else "entries" }}</h2>
    {% if entries %}
    <ul>
      {% for entry in entries %}
      <li><strong>{{ entry["name"] }}</strong> {{ entry["message"] }}
      <span class="when">{{ entry["signed_at"] }} UTC</span></li>
      {% endfor %}
    </ul>
    {% else %}
    <p class="empty">Nobody has signed yet.</p>
    {% endif %}
  </main>
</body>
</html>
"""


def database() -> sqlite3.Connection:
    """Open the guestbook, in the data directory Muru gives the application."""

    directory = Path(os.environ.get("MURU_DATA_DIR", "."))
    directory.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(directory / "guestbook.sqlite3")
    connection.row_factory = sqlite3.Row
    connection.execute(
        "CREATE TABLE IF NOT EXISTS entries ("
        "id INTEGER PRIMARY KEY, name TEXT NOT NULL, message TEXT NOT NULL, "
        "signed_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M', 'now')))"
    )

    return connection


def add_entry(name: str, message: str) -> None:
    """Add an entry to the guestbook."""

    with database() as connection:
        connection.execute("INSERT INTO entries (name, message) VALUES (?, ?)", (name, message))

    log.info("%s signed the guestbook", name)


@app.get("/")
def index() -> str:
    """Show the guestbook, newest entry first."""

    with database() as connection:
        entries = connection.execute("SELECT * FROM entries ORDER BY id DESC LIMIT 50").fetchall()

    log.info("showing %d entries", len(entries))

    return render_template_string(
        PAGE,
        entries=entries,
        greeting=GREETING,
        release=os.environ.get("MURU_RELEASE", "unknown"),
    )


@app.post("/sign")
def sign() -> Response:
    """Add the entry the form carries."""

    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()

    if name and message:
        add_entry(name[:60], message[:200])

    return redirect(url_for("index"))


@app.get("/slow")
def slow() -> str:
    """Take three seconds to answer, for trying timeouts and a canary's latency gate."""

    log.info("a slow request began")
    time.sleep(3)

    return "That took three seconds.\n"


@app.get("/fail")
def fail() -> str:
    """Raise an error, for trying error pages and a canary's error gate."""

    log.error("a request is about to fail")

    raise RuntimeError("This page fails on purpose.")


def main(arguments: list[str]) -> int:
    """Run one of the commands the project declares."""

    match arguments:
        case ["sign", name, message]:
            add_entry(name, message)
            print(f"{name} signed the guestbook")
        case ["count"]:
            with database() as connection:
                names = [row["name"] for row in connection.execute("SELECT name FROM entries")]

            for number, name in enumerate(names, start=1):
                print(f"{number}: {name}", flush=True)
                time.sleep(0.5)

            print(f"{len(names)} entries in all")
        case ["clear"]:
            with database() as connection:
                removed = connection.execute("DELETE FROM entries").rowcount

            print(f"removed {removed} entries")
        case _:
            print("usage: python -m guestbook sign NAME MESSAGE | count | clear", file=sys.stderr)

            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
