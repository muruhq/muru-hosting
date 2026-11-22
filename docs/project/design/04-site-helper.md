# 4. The site helper

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

The site helper is a small Python gRPC service in each site pod of stage
0, hosted by `muructl serve` as a grpcio servicer. It stands in for the
admin listener that Muru's split controller will have (section 12), and
is removed when that arrives.

## 4.1 The admin API proxy

Each call to `muru.admin.v1` is checked for the hub's bearer token and
against an allowlist, then forwarded to the admin socket unchanged,
streams included, and the answer is returned unchanged.

- The allowlist is what the hub may ever do. Which person may do what is
  the hub's check (section 5), not the helper's.

- The proxy is generic over the service's descriptor, so a new Muru call
  needs only an allowlist entry.

- The stubs come from the `.proto` files of the pinned Muru release.

## 4.2 The allowlist

| Kind | Calls |
| --- | --- |
| Reading | GetStatus, Probe, ListProcesses, ListApps, GetApp, GetAppData, ListReleases, GetRelease, WaitRelease, ListRollouts, GetRollout, GetScaleStatus, ApplicationUrls, ListEvents, WatchEvents, ListHosts, ListRoutes, ListUpstreams, DiffConfig, ExportConfig, TailLogs, ListLogs, GetMetrics, ListWebSockets, ListOverlays, PreviewOverlay, ListCommands, ListCommandRuns, GetCommandRun, TailCommandRun, ListConditions |
| Changing | PlanDeploy, Deploy, Rollback, DrainRelease, PromoteRelease, PruneReleases, RemoveRelease, StartRollout, PauseRollout, ResumeRollout, PromoteRollout, AbortRollout, SetScale, SetMaintenance, ControlOverlay, ApplyConfig, RunCommand for declared commands only, StopCommandRun, Debug for status, stacks, tasks and restart only |
| Refused | Shutdown, UpgradeDaemon, ReloadConfig, RemoveApp, DashboardLogin, cache and log file maintenance, the development request records, RunCommand with `argv` (one-off code), Debug inspect and memory, and any call not listed above |

A refused call is answered `PERMISSION_DENIED` with the reason, and never
reaches the daemon. A call a later Muru release adds is refused until it
is listed.

## 4.3 Sources

A service of the helper's own, `muruhosting.site.v1.Sources`, does what
Muru's admin API cannot today: give a release its code from elsewhere
(section 11.2).

- `UploadSource` takes a stream: a header with the directory's name, the
  archive's expected SHA-256 and the commit it came from, then chunks of
  a tar archive. The archive is checked against the digest before any of
  it is unpacked, then unpacked beneath `/srv/site/sources/` into the
  directory named. It refuses absolute paths, `..`, links that lead out
  of the directory, device files and an archive over the size limit, and
  answers with the directory's path.

- The hub names the directory for what it holds, the commit or the
  archive's digest, so uploading the same archive again answers with the
  directory already there, and a job run again does no harm. Another
  archive under a name in use is refused.

- `ListSources` lists the directories, and `RemoveSource` removes one,
  so the hub removes a directory once no release uses it.

The service is removed when Muru can take a release's code through its
own API (muruhq/muru#865).

## 4.4 Health

- `muructl serve`'s own `/livez` and `/readyz` for the helper's process.

- The hub knows the daemon is up by asking the proxied `GetStatus`,
  which answers only while the admin socket does. Muru's edge answers
  the standard gRPC health service for a release itself, serving while
  the release has workers, and a release cannot add to that answer
  (muruhq/muru#864), so the helper has no health service of its own.

## 4.5 Between the hub and the helper

- TLS with a certificate from the cluster's issuer (cert-manager), and
  the token as a bearer credential on every call.

- The helper's own settings are the admin socket's path, the site
  directory and the token (or a file holding it), from the environment.
  Where it listens, and TLS, are Muru's: the listener of `muructl serve`
  in a pod, and `muructl run --port` on a laptop.

- A NetworkPolicy admits the helper's port from the hub's namespace only.

- The hub calls in over the cluster network. A connection from each site
  out to the hub, as muruhq/muru#549 discusses for many instances, is an
  option for later.
