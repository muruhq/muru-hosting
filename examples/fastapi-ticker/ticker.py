"""A ticker: a FastAPI application whose page is fed by a stream that stays open."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import time
from collections.abc import AsyncIterator
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

# Change this and deploy again to see a release that differs from the last.

GREETING = "The time, as the server has it"

app = FastAPI(title="fastapi-ticker")
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
log = logging.getLogger("ticker")

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ticker</title>
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ margin: 0; padding: 1rem; font: 16px/1.6 system-ui, sans-serif; }}
    main {{ max-width: 40rem; margin: 3rem auto; }}
    .eyebrow {{ margin: 0; opacity: 0.7; font-size: 0.85rem; }}
    h1 {{ margin: 0.25rem 0 1rem; font-size: 1.8rem; line-height: 1.2; }}
    output {{ display: block; font: 600 clamp(2rem, 12vw, 4rem)/1.1 ui-monospace, monospace; }}
    .state {{ opacity: 0.7; }}
  </style>
</head>
<body>
  <main>
    <p class="eyebrow">fastapi-ticker, release {release}</p>
    <h1>{greeting}</h1>
    <output id="time" aria-live="off">waiting</output>
    <p id="state" class="state" role="status">Connecting.</p>
  </main>
  <script>
    const time = document.getElementById("time");
    const state = document.getElementById("state");
    const ticks = new EventSource("/ticks");

    ticks.onopen = () => {{ state.textContent = "Connected: one tick a second."; }};
    ticks.onmessage = (event) => {{ time.textContent = event.data; }};
    ticks.onerror = () => {{ state.textContent = "The stream closed; connecting again."; }};
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    """Show the page that listens to the ticks."""

    log.info("showing the page")

    return PAGE.format(greeting=GREETING, release=os.environ.get("MURU_RELEASE", "unknown"))


@app.get("/ticks")
async def ticks() -> StreamingResponse:
    """Send the time once a second for as long as the browser listens."""

    async def events() -> AsyncIterator[str]:
        log.info("a listener connected")

        try:
            while True:
                yield f"data: {datetime.now(UTC):%H:%M:%S} UTC\n\n"
                await asyncio.sleep(1)
        finally:
            log.info("a listener went away")

    return StreamingResponse(
        events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"}
    )


@app.get("/api/time")
async def api_time() -> dict[str, str]:
    """Return the time and the release as JSON."""

    return {
        "time": datetime.now(UTC).isoformat(timespec="seconds"),
        "release": os.environ.get("MURU_RELEASE", "unknown"),
    }


@app.get("/slow")
async def slow() -> dict[str, str]:
    """Take three seconds to answer, for trying timeouts and a canary's latency gate."""

    log.info("a slow request began")
    await asyncio.sleep(3)

    return {"took": "three seconds"}


@app.get("/fail")
async def fail() -> dict[str, str]:
    """Raise an error, for trying error pages and a canary's error gate."""

    log.error("a request is about to fail")

    raise RuntimeError("This page fails on purpose.")


def main(arguments: list[str]) -> int:
    """Run the command the project declares."""

    match arguments:
        case ["countdown", start] if start.isdigit():
            for number in range(int(start), 0, -1):
                print(number, flush=True)
                time.sleep(1)

            print("lift-off")
        case _:
            print("usage: python -m ticker countdown NUMBER", file=sys.stderr)

            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
