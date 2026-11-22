# Contributing to muru-hosting

muru-hosting is a proof of concept whose purpose is to dogfood Muru with a
real application and to test and extend Muru's APIs for hosting services.
It is not a product, and it is not going to become a supported project,
so contributions are about that purpose.

## How contributions work

Like Muru, muru-hosting takes contributions as requirements, not as code.
Pull requests are limited to collaborators. Everyone else contributes by
describing what they need:

1. Search the existing issues here and in
   [muruhq/muru](https://github.com/muruhq/muru/issues) first.

2. Open an issue describing the problem, the use case and the desired
   behaviour. A requirement that a hosting service puts on Muru is the
   most useful thing to send, and may belong in Muru's tracker rather
   than this one.

3. The maintainer discusses it in the issue and decides whether and how
   it fits the design.

Questions go to [Muru's discussions](https://github.com/muruhq/muru/discussions).
Security problems are described in [SECURITY.md](SECURITY.md).

## Building

| Tool | macOS | Linux (Debian or Ubuntu) |
| --- | --- | --- |
| git | `xcode-select --install` | `apt install git` |
| uv | `brew install uv` | the installer at astral.sh/uv |
| just | `brew install just` | `apt install just` |

Then:

```
just bootstrap    # the development environment and the git hooks
just lint         # ruff, mypy and the repository text checks
just docs         # the documentation, with warnings as errors
```

## Design specification and decision records

The design specification lives in
[docs/project/design](docs/project/design/index.md) and is the source of
truth for intended design. Architecture decision records live in
[docs/project/adr](docs/project/adr/index.md). When implementation needs
to differ from the specification, add an ADR and update the specification
in the same change.

## Conventions

The rules for writing, code, commits and branches are in
[AGENTS.md](AGENTS.md). They apply to people as much as to AI coding
agents.
