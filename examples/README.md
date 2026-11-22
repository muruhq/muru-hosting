# Example projects

Small applications to deploy to a site while working on muru-hosting. Each
is a project of its own, with a `[tool.muru]` table and a `uv.lock`, so a
site's daemon builds its environment and serves it as it would anyone's
code. They are not part of the hub and nothing imports them.

| Directory | Interface | Shows |
| --- | --- | --- |
| `flask-guestbook/` | WSGI | A page backed by SQLite in the site's data directory, static files, and declared commands with inputs |
| `fastapi-ticker/` | ASGI | A page fed by a stream that stays open, a JSON endpoint, and a declared command |

Deploy one from a site's page in the hub, giving its directory, or from
the command line:

```
just deploy OWNER/NAME examples/flask-guestbook
```

Both log a line for each thing they do, so a site's log has something in
it, and both show the release that is serving, so a new release can be
told from the last. Each has a `/fail` page that raises an error and a
`/slow` page that takes a few seconds, for trying a canary's gates.

To make a release that differs, change `GREETING` in the application's
module and deploy again.
