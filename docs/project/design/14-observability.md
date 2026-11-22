# 14. Tracing and observability

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

The hub is traced with [wrapture](https://wrapture.readthedocs.io), through
Muru's tracing setting where Muru runs it and through wrapture's own
launcher where it does not, and exports its traces over OTLP. This serves
three ends: visibility while the hub is developed, dogfooding wrapture,
and finding what Muru must add for a trace to run through the edge, the
helper and the daemon (section 14.5).

## 14.1 Tracing the hub's web application

- The hub's committed settings have `tracing` off. A developer turns it on
  for `muructl run` with `tracing` in `muru.local.toml`, and a deployment
  turns it on with a settings file mounted from a ConfigMap, Muru's way of
  changing a container's settings without a new image. Tracing is on only
  where something receives the traces.

- The wrapture configuration is a file of its own, `tracing/wrapture.toml`,
  named by `[tool.muru.tracing] config`:

  - instrumentation for `django`, `sqlite3` and `psycopg` (from
    wrapture-instrumentation-postgresql), `grpc` for the calls to site
    helpers, and the HTTP client the hub uses for GitHub;

  - an `[otel]` table with `service_name = "muru-hosting-hub"` and the
    traces signal, leaving the endpoint to the environment
    (`OTEL_EXPORTER_OTLP_ENDPOINT`), so one file serves every place the
    hub runs.

- Django's instrumentation records each request as the root of its tree
  with its matched route, so `tracing_middleware` stays off for the
  Django entry point. The MCP server's ASGI mount (section 10.1) is not a
  Django view, so its mount has `tracing_middleware = true`.

- lightkube is built on `httpx2`, which the `httpx` instrumentation may
  not cover. The hub's Kubernetes module is the hub's own code, so its
  calls are recorded by section 14.2 whatever the client underneath.

## 14.2 Spans in the hub's own code

For code it owns, wrapture's guidance is to mark the source rather than
configure from outside, so the hub does:

- every action of the service layer (section 10.1) is
  `@wrapture.observed`, with the site, the action and the kind of caller
  (page, Actions API, MCP) as data, so a trace reads in the hub's own
  terms whichever way the action came;

- the functions of the Kubernetes module and of the client for site
  helpers are observed with the category `external`;

- the webhook view marks verification, matching and enqueueing as
  `wrapture.block`s.

Data never includes a secret, a token or a source archive's contents.

## 14.3 Tracing the jobs worker

The jobs worker is Django's `db_worker` command from `django-tasks-db`,
not a Muru entry point, so Muru's tracing does not apply to it. It runs
under wrapture's launcher instead:

```
python -m wrapture --config tracing/wrapture-jobs.toml manage.py db_worker
```

with the same instrumentation and `service_name = "muru-hosting-jobs"`.

A job continues the trace that enqueued it:

- enqueueing records `wrapture.trace_headers()` with the job;

- running it opens `wrapture.block("job:NAME", joins=headers)`, and each
  step of the job is a block beneath it;

- a job resumed after the worker restarts joins the same trace again.

A deploy then reads as one trace: the webhook's request, the job, its
calls to GitHub and to the helper, and the steps between.

## 14.4 Viewing traces

[otel-desktop-viewer](https://github.com/CtrlSpice/otel-desktop-viewer)
receives OTLP and shows traces, metrics and logs in a browser, keeping
them in memory. Nothing is persisted: traces are for visibility during
development and are lost when the viewer stops.

- **Locally:** the viewer's macOS application, receiving on
  `localhost:4318`, with `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`
  for `muructl run` and the jobs worker.

- **In Kubernetes:** an optional Deployment in the hub's namespace, one
  replica of the published image at a pinned release tag
  (`ghcr.io/ctrlspice/otel-desktop-viewer`), with a ClusterIP Service for
  OTLP and the interface. The web Deployment and the jobs worker both
  export to it, so a webhook's trace and the job it starts are seen
  together, which a sidecar in either Deployment could not give. The
  interface is reached with
  `kubectl -n muru-hosting port-forward svc/otel-viewer 8000:8000`, never
  through an Ingress, since it has no sign-in; a NetworkPolicy admits
  OTLP from the hub's namespace only.

- **Bounding its memory:** the viewer deletes its oldest telemetry when
  its store passes `--db-max-size` (512MB by default in memory), checking
  every 30 seconds. It has no limit by age. The Deployment runs it with
  `--host 0.0.0.0 --open-browser=false --db-max-size 128MB` and a memory
  limit of 512Mi, since the size measured is the store's, not the
  process's, and can overshoot between checks.

## 14.5 What a trace needs from Muru

A full trace of a deploy runs from the GitHub webhook through the hub and
the jobs worker to the helper, the daemon and the release it starts.
Today it stops at the helper. Section 11.1 lists the Muru issues:

- the helper's RPCs, served by Muru's own gRPC serving, are not traced as
  requests (muruhq/muru#856);

- the daemon's work for an admin call is in no trace (muruhq/muru#857);

- the edge neither forwards trace context nor exports its own spans, so a
  page's time in the edge and its wait for a worker are missing
  (muruhq/muru#639, muruhq/muru#135);

- Muru's metrics and events are not exported over OTLP (muruhq/muru#136,
  muruhq/muru#137).

## 14.6 Telemetry for hosted sites

A site member debugging their own application wants its traces, metrics
and logs too. That is a later aim, and section 13 holds its questions:
where a site's telemetry is collected, how it is kept apart from other
sites', and whether members see it in the hub, through MCP, or in a
viewer of their own.
