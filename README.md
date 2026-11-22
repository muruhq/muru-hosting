# muru-hosting

A hosting control plane on Kubernetes for Python web sites served by
[Muru](https://github.com/muruhq/muru): each site in a pod of its own,
deployed from GitHub as Muru releases, managed by the people it belongs
to through a web interface and through their own AI assistant over MCP.

> **This is a proof of concept, not a product.** muru-hosting exists to
> dogfood Muru with a real application, and to test and extend Muru's
> APIs until Muru suits web hosting services for Python applications. It
> is not stable, it may change or stop at any time, and it is not going
> to become a supported project. Do not rely on it to host anything that
> matters, or build on it expecting it to be maintained.

## What it is for

The primary purpose is Muru's, not its users':

- **Dogfooding Muru with a real application.** The control plane is a
  Django application served by `muructl serve`, its helper in each site's
  pod is a gRPC service served by `muructl serve`, and every hosted site
  runs under the Muru daemon. All three ways of running Muru are used
  together, each with its own conventions for settings, data, commands
  and deployment.

- **Validating Muru's APIs.** Everything the control plane does to a site
  goes through Muru's admin API (`muru.admin.v1`). Where that API falls
  short of what a hosting service needs, the gap is filed as an issue
  against Muru and worked around here until Muru closes it.

- **Extending Muru for hosting.** The design runs from what Muru can do
  today to the shape a hosting service needs: Muru's controller and edge
  out of reach of the code they host, per-site isolation, and certificates
  for sites' own domains.

The design covers three ways of using such a control plane, which give it
concrete requirements:

- one person or team managing their own set of deployed applications;

- a small hosting service for other people's sites;

- a university course, where each student hosts an application of their
  own and the course's staff can see every site.

## How it works

- **A site is a pod** in a namespace of its own, running the Muru daemon
  with a helper beside it that the control plane talks to over gRPC.

- **Code comes from GitHub.** A push, a successful CI run or a step in a
  GitHub Actions workflow deploys a commit as a new release, which Muru
  starts beside the running one and switches traffic to by the site's
  policy: at once, as a canary, or after a member approves it.

- **People sign in with GitHub.** An admin decides who may sign in by
  GitHub user, organisation or team, how many sites each account may
  have, and what each person may do on each site.

- **AI assistants manage sites over MCP.** A site member can connect the
  assistant on their own machine to the control plane and have it deploy,
  watch a rollout, read logs and roll back, with the same permissions as
  the web interface.

The [design specification](docs/project/design/index.md) describes it in
full.

## Status

Design only: there is no code yet. The design specification is the
current intended design and changes as the work shows what Muru needs.

## Contributing

This is a personal proof of concept for Muru. Issues about the design, and
about what Muru would need to support hosting, are welcome. See
[CONTRIBUTING.md](CONTRIBUTING.md).

The project is developed with extensive use of AI coding agents, directed
and reviewed by its creator, as Muru is.

## Licence

Apache-2.0. See [LICENSE](LICENSE).
