"""The hello site: one page saying which site this is and how to deploy to it."""

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
</head>
<body>
  <main>
    <p class="eyebrow">muru-hosting</p>
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
      <li>Deploy the directory from the machine the hub runs on:
<pre>just deploy {site} /path/to/project</pre></li>
    </ol>
    <p>Your first deploy becomes release <code>r2</code>. This page stays as
    <code>r1</code>, so a rollback has somewhere to go.</p>
    {hub}
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
