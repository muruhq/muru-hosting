# Instructions for AI coding agents

These rules are written in the imperative for AI coding agents and apply
equally to people. They follow the rules of the Muru repository, so that
work moves between the two without a change of habits, with what differs
for a proof of concept that uses Muru rather than being it.

## Start here

1. Run `just bootstrap`. It creates the development environment with uv
   and installs the git hooks.

2. Read the relevant pages of the design specification in
   [docs/project/design](docs/project/design/index.md) before working on a
   part of the system. The specification is the source of truth for
   intended design.

3. Read the architecture decision records in
   [docs/project/adr](docs/project/adr/index.md) that touch the area you
   are working on.

4. Use [scratch/](scratch/) for temporary working files: reference
   material you are given, plans you are asked to write, intermediate
   outputs. The directory exists in the repository but its contents are
   not part of it (`scratch/.gitignore` ignores everything except
   itself). Never reference files in `scratch/` by name from code or
   documentation that will be committed, because they come and go. It is
   not where pending work is tracked: that is GitHub issues (see Project
   process).

## What this repository is

- A proof of concept whose purpose is Muru's: to dogfood Muru with a real
  application, and to test and extend Muru's APIs until Muru suits Python
  web hosting services. It is not a product, makes no promise of
  stability, and is not going to become a supported project. Say so where
  a reader could take it for one, and never write as if it were.

- It is a client of Muru, never a part of it. It uses released versions
  of Muru from PyPI, pinned in `pyproject.toml`, and nothing from Muru's
  source tree.

## Working with Muru

- Control goes through Muru's admin API, `muru.admin.v1`, and nothing
  else. Never run `muructl` from application code to change something,
  parse its output, read Muru's state store or scrape its dashboard. A
  need the admin API does not meet is a gap in Muru (below), not a reason
  to go around it.

- The admin API's Python stubs are generated from the `.proto` files of
  the pinned Muru release, never edited by hand. Muru is in alpha with no
  compatibility promise between releases, so upgrading Muru is a change
  of its own: bump the pin, regenerate the stubs (`just stubs`, then
  `just skill`), fix what breaks and note in the commit what changed. A
  test fails while the stubs are not those of the pinned release.

- When the work shows Muru lacks something muru-hosting needs, open an
  issue in [muruhq/muru](https://github.com/muruhq/muru/issues) in the
  same step, with the use case from here, and link it from the
  muru-hosting issue that needs it. Section 11 of the specification lists
  what the design needs from Muru; keep it current.

- A workaround is never recorded in a code comment alone. In the same
  step as the upstream issue, open an issue in this repository with the
  `workaround` label, saying which upstream issue it waits on, where the
  workaround is and what to change when the upstream issue closes, and
  put it on the project board. The comment beside the code names both
  issues. This holds for any upstream project, not only Muru: wrapture,
  unwrapt, Django and the rest.

- A bug in Muru found here is an issue in muruhq/muru, with the smallest
  reproduction that does not need muru-hosting.

## Writing style, for every file in the repository

- Do not use em dashes in any file. Rephrase with commas, parentheses,
  colons or separate sentences. CI rejects the em dash character (U+2014)
  in tracked text files.

- In bulleted lists where items run to more than one line, put a blank
  line between the bullets, in docstrings, Markdown files, code comments
  and any other prose. This is about the raw file being readable. Be
  consistent within a list: if one item needs the spacing, space every
  item in it.

- Text users see (pages, messages, errors, MCP tool descriptions) never
  names a section of the specification or an ADR, which are internal and
  go stale. Say what the thing is instead. Code comments and docstrings
  may cite them.

- The user documentation (the home page, tutorials, how-to guides,
  reference and explanation) describes what muru-hosting does and how to
  use it, as a user guide would. It carries no status notes and no
  promises of what is still to come: that lives in GitHub issues. A limit
  a user would hit is stated as it is, where it applies.
  `scripts/check-user-docs.py` rejects status notes and future-tense
  phrases in those pages. The proof of concept notice on the home page is
  a statement of what the project is, not a status note.

- User pages state what muru-hosting does. They do not compare it with
  other hosting services or argue for its design; the reasoning belongs
  in the specification and the ADRs.

## Python code

- Always use type hints: on all function and method parameters and
  return types, and on attributes and variables where the type is not
  obvious from the assignment. mypy runs in strict mode.

- Every function, method or property in the public API of a module has a
  docstring saying what it does, except trivially obvious cases such as
  an accessor property named for the attribute it returns, and dunder
  methods implementing standard protocols.

- Put a blank line between a function or method docstring and the first
  line of code.

- Format and lint with ruff (`just lint` runs it). Do not hand-format.

- Mark the hub's key operations for tracing in the source, with
  `@wrapture.observed` on each service-layer action and on the functions
  that call Kubernetes, GitHub and site helpers, and `wrapture.block` for
  the steps of a job or a view. Section 14 of the specification says what
  is traced and how; a new action or job step is traced in the same
  change that adds it. Never put a secret, a token or file contents in a
  span's data. Use `hub.tracing.observed` for the decorator, which keeps
  the function's signature for mypy until GrahamDumpleton/wrapture#6 is
  fixed.

## Tests

- Tests are pytest, and run against SQLite unless a test is marked as
  needing Postgres.

- Use [wrapture](https://wrapture.readthedocs.io) for observing and
  standing in for collaborators, never `unittest.mock`: `bound()` and
  `binding()` to intervene in real calls, `stub()` for a callable,
  `mock(Spec)` for a collaborator, and its events to assert on what
  happened, with its pytest plugin. wrapture's "Coming from
  unittest.mock" page translates each mock idiom. A case wrapture cannot
  express is a wrapture issue, raised before working around it.

## Code layout

Code is read far more often than it is written, so function bodies are
laid out as paragraphs with vertical space between the steps, never as
one dense block. The rules below are mechanical on purpose, so that a
checker can enforce them; when in doubt the blank line goes in.

- A compound statement (`if`, `for`, `while`, `try`, `with`, `match`)
  that spans more than two lines has a blank line before it, unless it is
  the first statement of its enclosing block or sits directly below a
  block comment.

- The first statement after such a block ends (after the dedent) has a
  blank line before it. `else`, `elif`, `except`, `finally`, a closing
  bracket and a continued method chain are not statements for this
  purpose.

- A short guard of one or two lines (`if x is None: return`) is exempt
  from both rules, so a run of simple statements and guards may stay
  together. Do not put a blank line between every statement.

- Setup for a loop or a conditional is a paragraph of its own. The line
  that computes a deadline, a buffer or a lock goes above a blank line,
  and the loop below it; a block comment above the pair ties them
  together.

- Where it helps, start a paragraph with a short comment saying what the
  step does or why it is needed. Prefer one comment per logical block
  over line-by-line commentary, and omit it when the code already says it
  plainly. A block comment has a blank line below it and, unless it opens
  a block, a blank line above it.

- Docstrings are followed by a blank line before the first line of code.

This is what the rules produce:

```python
    def wait_until_ready(self, site: Site, timeout: float) -> Release:
        """Wait for the site's newest release to serve, or fail."""

        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            release = self.admin.newest_release(site)

            if release.state == "failed":
                raise DeployFailed(release.message)

            if release.serving:
                return release

            time.sleep(1)

        # Out of time: say where the release got to.

        raise DeployTimedOut(site, release.state)
```

Code produced through scripts, heredocs or patches is held to the same
rules; reread every new or changed body as a reader before reporting it.
`scripts/check-layout.py` enforces the rules, runs from `just lint` and
the pre-commit hook, and inserts the missing blank lines with `--fix`.

## Git and review

- Commit messages never include a co-authored-by trailer or any other
  agent attribution, and pull request descriptions carry none either. A
  commit message hook, installed by `just bootstrap`, rejects them.

- Never commit on your own initiative. Finish the piece of work,
  summarise it and wait to be told to commit. Permission to commit covers
  only the work it was given for and does not carry forward to later
  steps of a multi-step plan. Uncommitted changes are how review happens,
  so committing early makes review harder.

- `main` is the default branch, and while the project is a proof of
  concept the only long-lived one. Work happens on feature branches
  merged into `main` through a pull request. A change is not treated as
  landed until the GitHub Actions run for the pushed merge has passed.

- Pull requests are merged with a merge commit (`gh pr merge --merge`),
  never squashed or rebased, so each commit on a branch survives with the
  issue it names. A branch carries one commit per issue rather than
  fix-up commits. Never rebase or force-push a branch that has been
  pushed.

## Project process

- Run `just lint` and the relevant tests before reporting work as
  complete, and `just docs` when the documentation changed. Say which
  ran and whether they passed.

- The specification is the current intended design, never a frozen
  document. When the implementation needs to differ from it, propose an
  ADR (copy `docs/project/adr/template.md`) and update the specification
  page in the same change instead of deviating silently. Add new material
  as new subsections so section numbers stay stable.

- ADRs are append-only. Never edit the decision in an existing record;
  add a new one that supersedes it and set the old record's status to
  superseded.

- Track pending work as GitHub issues in this repository, never in
  files, and Muru's part of it as issues in muruhq/muru (above). When
  work is found or deferred, open an issue in the same step. Write it with
  the headings and label of the matching issue form, or a plain structure
  for work no form fits, and do not hard-wrap its text, since GitHub
  shows every line break. A pull request that finishes an issue says
  `Closes #N`.

- Open an issue for every problem found along the way, not only for the
  work in hand: a bug, something clumsy to use, a mismatch between the
  code, the specification and the documentation, a step that could not be
  tested. A problem that is only mentioned in a report is lost, so file
  it when it is found and say in the report which issues were opened.

- Keep the project board true to the work: every open issue is on it,
  with its fields set, since it is how the maintainer decides what comes
  next. The maintainer moves issues to Next; take the Next issue with the
  lowest Order.

## Commands

| Command | Does |
| --- | --- |
| `just bootstrap` | Create the development environment and install the git hooks |
| `just lint` | ruff, mypy and the repository text checks |
| `just test` | The hub's tests, on SQLite unless `DATABASE_URL` names Postgres |
| `just hub ARGS` | Run the hub under Muru at http://127.0.0.1:9080/ with local sign-in, migrating its database first; arguments go to `muructl run`, as in `just hub --open` |
| `just dev ARGS` | Run the hub and its jobs worker together, which a deploy from a site's page needs; arguments go to `muructl run` |
| `just worker` | Run the hub's jobs worker beside `just hub` |
| `just manage ARGS` | A `manage.py` command with the development settings, such as `just manage createsuperuser` |
| `just site-up OWNER/NAME` | Start a site on this machine (its own Muru daemon and the site helper) and register it with the hub, which deploys the hello site to it once `just worker` runs |
| `just site-down OWNER/NAME` | Forget a site on this machine, stop its daemon and helper and remove its directories |
| `just deploy OWNER/NAME PATH` | Deploy a directory to a site |
| `just viewer` | Run otel-desktop-viewer, which receives the hub's traces at localhost:4318 and shows them at http://localhost:8000/ |
| `just stubs` | Regenerate the gRPC stubs from the pinned Muru release's `admin.proto` |
| `just docs` | Build the documentation from nothing, with warnings as errors |
| `just docs-serve` | Build the documentation and serve it with live reload |
| `just skill` | Install or update the Muru skill for coding agents from the pinned `muructl` |

## Coding agents and Muru

`.mcp.json` lists Muru's MCP server, `muructl mcp serve` from the pinned
`muructl`, so an agent can run what it builds under Muru, read what Muru
observes and roll back. `.claude/skills/muru/` holds the skill that
`muructl` writes to teach the development loop; `just skill` updates it
after Muru is upgraded, and it is never edited by hand. Notes for agents
about this project belong in this file, not in that skill.

## Where things are

| Path | Holds |
| --- | --- |
| `hub/` | The hub's Django project: `accounts/` for who signs in, `hosting/` for sites, with `manage.py` and its `[tool.muru]` settings at the root |
| `helper/` | The site helper, a gRPC service Muru serves beside each site's daemon: the allowlisted proxy of `muru.admin.v1` and the Sources service |
| `hello/` | The hello site, the project every new site is given as its first release |
| `packages/stubs/` | The gRPC stubs the hub and the helper share: `admin.proto` of the pinned Muru release, the helper's own `.proto`, and the code `just stubs` generates from them |
| `deploy/site/` | The configuration of a site's Muru daemon, for a pod and for a site on a laptop |
| `tests/` | The tests of the hub and the helper, some against a real daemon |
| `tracing/` | wrapture's configuration for the hub, used when tracing is on |
| `docs/` | Sphinx documentation: the design specification and ADRs under `docs/project/`, user documentation beside them |
| `scripts/` | The repository's checks |
| `scratch/` | Temporary working files, ignored by git |
