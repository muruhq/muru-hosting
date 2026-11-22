"""The hello site: one page saying which site this is and how to deploy to it, with a game."""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable
from html import escape
from typing import Any

StartResponse = Callable[[str, list[tuple[str, str]]], Any]

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{site} · muru-hosting</title>
  <link rel="stylesheet" href="/static/hello.css">
  <script src="/static/hello.js" defer></script>
</head>
<body>
  <main>
    <p class="eyebrow"><button type="button" id="logo" class="logo">muru-hosting</button></p>
    <h1>{site} is up</h1>
    <p class="lead">This is the page a new site serves. It is release
    <code>{release}</code> of the site, answering at <code>{host}</code>.</p>

    <h2>Deploy your own code</h2>
    <ol>
      <li>Give your project a <code>[tool.muru]</code> table in its
      <code>pyproject.toml</code>, naming its WSGI or ASGI application:
<pre>[tool.muru]
entrypoint = "myproject.wsgi:application"</pre></li>
      <li>Commit a <code>uv.lock</code>, so the site builds the project's
      environment itself.</li>
      <li>Deploy the directory from this site's page in the hub, or from the
      machine the hub runs on:
<pre>just deploy {site} /path/to/project</pre></li>
    </ol>
    <p>Your first deploy becomes release <code>r2</code>. This page stays as
    <code>r1</code>, so a rollback has somewhere to go.</p>
    {hub}

    <section id="game-section" hidden>
      <h2>Keep the site serving</h2>
      <p>Requests arrive at the edge and wait in its queue. Send each one to
      a worker that is free, before the queue overflows. When a green
      release starts, switch traffic to it once its workers are ready.</p>
      <canvas id="game" role="img"
        aria-label="The edge's queue on the left, and each release's workers on the right"></canvas>
      <p class="game-bar">
        <button type="button" id="game-start" class="button">Play</button>
        <span id="game-controls" hidden>
          <button type="button" class="button" data-worker="0">Worker 1</button>
          <button type="button" class="button" data-worker="1">Worker 2</button>
          <button type="button" class="button" data-worker="2">Worker 3</button>
          <button type="button" class="button" id="game-switch" hidden>Switch traffic</button>
        </span>
      </p>
      <p id="game-status" role="status">Use the buttons, the keys 1 to 3 and S,
      or tap a worker.</p>
    </section>
  </main>
  <footer>A proof of concept that dogfoods
  <a href="https://github.com/muruhq/muru">Muru</a>. Host nothing here that matters.</footer>
</body>
</html>
"""


def application(environ: dict[str, Any], start_response: StartResponse) -> Iterable[bytes]:
    """Answer every path with the hello page."""

    site = os.environ.get("HELLO_SITE", "This site")
    hub_url = os.environ.get("HELLO_HUB_URL", "")
    hub = (
        f'<p><a class="button" href="{escape(hub_url)}">Manage this site</a></p>' if hub_url else ""
    )

    body = PAGE.format(
        site=escape(site),
        release=escape(os.environ.get("MURU_RELEASE", "unknown")),
        host=escape(environ.get("HTTP_HOST", "")),
        hub=hub,
    ).encode()

    start_response(
        "200 OK",
        [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))],
    )

    return [body]
