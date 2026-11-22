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
| Reading | GetStatus, ListProcesses, ListApps, GetApp, GetAppData, ListReleases, GetRelease, WaitRelease, ListRollouts, GetRollout, GetScaleStatus, ApplicationUrls, ListEvents, WatchEvents, ListHosts, ListRoutes, ListUpstreams, DiffConfig, ExportConfig, TailLogs, ListLogs, GetMetrics, ListWebSockets, ListOverlays, PreviewOverlay, ListCommands, ListCommandRuns, GetCommandRun, TailCommandRun, ListConditions |
| Changing | PlanDeploy, Deploy, Rollback, DrainRelease, PromoteRelease, PruneReleases, RemoveRelease, StartRollout, PauseRollout, ResumeRollout, PromoteRollout, AbortRollout, SetScale, SetMaintenance, ControlOverlay, ApplyConfig, RunCommand for declared commands only, Debug for status, stacks, tasks and restart only |
| Refused | Shutdown, UpgradeDaemon, ReloadConfig, RemoveApp, DashboardLogin, cache and log file maintenance, RunCommand with `argv` (one-off code), Debug inspect and memory |

## 4.3 Sources

A service of the helper's own, `muruhosting.site.v1.Sources`, does what
Muru's admin API cannot today: give a release its code from elsewhere
(section 11.2).

- `UploadSource` takes a stream of chunks of a tar archive, with its
  expected SHA-256 and the commit it came from, and unpacks it beneath
  `/srv/site/sources/` into a directory named for the commit. It refuses
  absolute paths, `..`, links that lead out of the directory and device
  files, and answers with the directory's path.

- `ListSources` lists the directories, and `RemoveSource` removes one,
  so the hub removes a directory once no release uses it.

The service is removed when Muru can take a release's code through its
own API.

## 4.4 Health

- `muructl serve`'s own `/livez` and `/readyz` for the helper's process.

- A gRPC health service that reports serving only while the admin socket
  answers GetStatus, so the hub knows the daemon is up.

## 4.5 Between the hub and the helper

- TLS with a certificate from the cluster's issuer (cert-manager), and
  the token as a bearer credential on every call.

- A NetworkPolicy admits the helper's port from the hub's namespace only.

- The hub calls in over the cluster network. A connection from each site
  out to the hub, as muruhq/muru#549 discusses for many instances, is an
  option for later.
