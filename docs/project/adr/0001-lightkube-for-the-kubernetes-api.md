---
status: accepted
date: 2026-11-22
---

# ADR 0001: lightkube for the Kubernetes API

## Context and problem statement

The hub creates and changes every site's Kubernetes objects (section 6.1)
and watches its pod come up (section 7.1). It renders a site's objects
from templates and applies them again whenever the site changes, so
server-side apply is its central operation. Which Python client does it
use?

## Decision drivers

- Server-side apply with a field manager, so the hub owns the fields it
  sets and leaves others alone.

- Watching resources, from asyncio code as well as synchronous code,
  since the jobs worker mostly waits.

- Typed objects that mypy in strict mode can check.

- An active project with recent releases, and use beyond its authors.

## Considered options

Compared on 2026-11-22 from PyPI, GitHub and each package's source:

| | lightkube | kr8s | pykube-ng | kubernetes (official) |
| --- | --- | --- | --- | --- |
| Latest release | 1.0.2, 2026-10-31 (1.0.0 in 2026-08) | 0.20.15, 2026-01-16 | 23.6.0, 2023-06-16 | 37.0.3, 2026-11-18 |
| Activity | commits in 2026-10, 23 contributors, 4 open issues | commits in 2026-10, 28 contributors, 51 open issues | last commit 2023-06 | active, generated from the API's schema |
| Used by | about 600 code results in Canonical's organisation alone (its Juju charms) | about 300 code results, Dask's Kubernetes operator | | widely |
| Server-side apply | yes, `apply()` with a field manager | no: merge and JSON patches only, declarative apply an open request | no | yes, awkwardly |
| Watch | sync and async | sync and async | sync only | yes |
| Types | typed models per Kubernetes version, `py.typed` | dictionaries through `python-box`, `py.typed` | untyped | generated models |
| Licence | MIT | BSD-3-Clause | Apache-2.0 | Apache-2.0 |

## Decision outcome

Chosen option: lightkube, because it is the only one of the four with
server-side apply, typed models and both sync and async clients, and it
has reached 1.0 with steady releases. kr8s reads more like `kubectl` and
suits scripts, but lacks apply. pykube-ng has had no release since June
2023. The official client is ruled out on ergonomics.

### Consequences

- Good: a site's objects are applied the same way on creation and on
  every change, and mypy checks them.

- Good: the jobs worker can watch pods from asyncio code.

- Bad: a smaller community than the official client's, with one main
  maintainer. All Kubernetes access goes through one module of the hub,
  so changing client touches only that module.

## More information

- Section 6 of the specification.

- lightkube: https://github.com/gtsystem/lightkube

- kr8s's request for declarative apply:
  https://github.com/kr8s-org/kr8s/issues/443
