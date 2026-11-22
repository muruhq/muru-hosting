# 13. Open questions

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

When a question is settled, its outcome is written into the section it
concerns, with an ADR for a significant choice, and it is removed from
this list in the same change.

- Whether a site holds one application or several. One keeps the model
  simple and matches "a site"; several fit a site with an API and a front
  end.

- Backups: volume snapshots of `site` and `state` on a schedule set by the
  plan, or a declared command per site for its data.

- Scale to zero for idle sites, such as a student's between terms,
  against the cold start of a preloaded application.

- Secrets for a site's own settings, such as API keys: Muru's secret store
  in the daemon, set through the hub, or Kubernetes Secrets given to the
  daemon's environment.

- Whether the web Deployment reads pod status directly with a read-only
  role, or only through the jobs' records (section 2.5).

- A site whose code is an image rather than a repository, which stage 1
  makes possible.

- Whether Muru's MCP server, which a member runs locally for `muructl
  run`, and the hub's should be one setup for the member's assistant, for
  example one skill covering both: develop locally with one, deploy and
  watch with the other.

- Whether an admin may set a number of custom domains per site, or only
  per account and plan.

- Telemetry for hosted sites (section 14.6): a collector in each site's
  pod or one for the cluster, how one site's telemetry is kept from
  another's, how long it is kept against a plan's size, and whether
  members read it in the hub, through MCP tools, or in a viewer of their
  own reached as the hub's is.
