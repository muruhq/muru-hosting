# 11. What the design needs from Muru

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

This section is the list of what the design takes from Muru, and of what
Muru lacks. It is kept current: a gap found in the work is added here and
filed in Muru's tracker in the same change, and an entry is updated when
Muru closes it.

## 11.1 Muru issues the design builds on

| Muru issue | What it gives | Used in |
| --- | --- | --- |
| [muruhq/muru#146](https://github.com/muruhq/muru/issues/146) | the admin API over TCP with tokens and roles | stage 1: replaces the helper's proxy |
| [muruhq/muru#148](https://github.com/muruhq/muru/issues/148) | the controller split from where the processes run | stage 1: the supervisor in the site's container |
| [muruhq/muru#187](https://github.com/muruhq/muru/issues/187) | an admin API client and access model for applications | the shared access model, and a published client in place of this repository's stubs |
| [muruhq/muru#549](https://github.com/muruhq/muru/issues/549) | a separate admin UI for production systems | this repository is one, for hosting |
| [muruhq/muru#90](https://github.com/muruhq/muru/issues/90) | the audit log | the principal behind each change, beside the hub's own log |
| [muruhq/muru#321](https://github.com/muruhq/muru/issues/321) | rollouts whose capacity follows traffic | canaries inside a site's memory limit |
| [muruhq/muru#133](https://github.com/muruhq/muru/issues/133) | ACME certificates in the edge | custom domains with TLS in the pod (section 9.2) |
| [muruhq/muru#856](https://github.com/muruhq/muru/issues/856) | gRPC entry points traced, joining the caller's trace | the helper's RPCs in the hub's traces (section 14.5) |
| [muruhq/muru#857](https://github.com/muruhq/muru/issues/857) | admin API calls joining the caller's trace, with the controller's work as spans | a deploy's trace through the daemon (section 14.5) |
| [muruhq/muru#639](https://github.com/muruhq/muru/issues/639) | the edge forwarding W3C trace context | a page's trace starting at the edge |
| [muruhq/muru#135](https://github.com/muruhq/muru/issues/135) | edge spans, deploys and rollouts exported over OTLP | the edge's and the controller's time in a trace |
| [muruhq/muru#136](https://github.com/muruhq/muru/issues/136), [muruhq/muru#137](https://github.com/muruhq/muru/issues/137) | Muru's metrics and events over OTLP | metrics and events beside the traces, and for hosted sites (section 14.6) |

## 11.2 Gaps found so far

Each is filed in Muru's tracker when the work reaches it.

1. **Deploying from an uploaded archive through the admin API.** `Deploy`
   takes a directory on the node, so a remote caller has no way to give a
   release its code. The helper's `Sources` service stands in (section
   4.3).

2. **Release metadata.** `DeployRequest` and `Release` carry no commit,
   branch, author or link, so Muru's own views show only `rN` for a
   release the hub knows came from a commit. The hub keeps them.

3. **The admin socket's path is not given to releases.** The helper is
   told it in its settings.

4. **No idempotency keys on changing calls,** which Muru's own design
   calls for. A hub job that times out on a promote or a rollback cannot
   safely retry it.

5. **No principal on whose behalf a call is made,** for Muru's events and
   audit log. muruhq/muru#90 and muruhq/muru#187 have an application as
   the principal, not a person behind it.

6. **No guide for the daemon in a Kubernetes pod:** probes for the
   daemon's container, the shutdown budget against the grace period,
   volumes and a non-root daemon. Muru's Kubernetes guide covers `muructl
   serve` alone.

## 11.3 Needed for stage 1

Beyond muruhq/muru#146 and muruhq/muru#148, stage 1 (section 12) needs of
Muru:

- the state directory split into a part the controller alone holds and a
  part shared with the site's container;

- relays writing log files in the controller's container from pipes
  passed across from the site's container;

- the worker protocol hardened as an input from workers the site
  controls, with fuzzing, since the edge reads it in a trusted container;

- environment builds run through the supervisor, never in the
  controller's container, since a build backend runs the site's code;

- pruning of releases, environments and caches by policy, since a hosted
  site cannot be pruned by hand;

- a guide and manifests for a site of this shape, and its Compose
  equivalent for development.
