# 2. The hub

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

The hub is a Django project in its own namespace, served by `muructl
serve` from an image built with `muructl build --deployment`.

## 2.1 Web

- Pages for members, group leads and admins, the GitHub webhook
  endpoint, a small JSON API for GitHub Actions (section 8.2) and the MCP
  server (section 10).

- Live views (events, logs, a rollout's progress, a command's output) are
  streamed to the browser from the helper's gRPC streams. A WSGI view
  hands the request to an ASGI application on the worker's loop (Muru's
  handoff), which serves it as Server-Sent Events or a WebSocket, so a
  long stream holds no WSGI thread.

## 2.2 Data

- **Database:** Postgres in a deployment. The hub serves many people,
  the migration Job of section 2.4 needs a database a second pod can
  reach, and Postgres gives the job queue `SKIP LOCKED`. On a laptop the
  hub uses SQLite (section 15.2).

- **Data directory:** `muructl serve --data-dir` on a volume, for source
  archives fetched from GitHub before they are sent to a site, and the
  hello site's built archive (section 7.2).

## 2.3 Jobs

Django's tasks framework (`django.tasks`) with the database backend from
the `django-tasks-db` package, its `db_worker` command in a second
Deployment of the same image, traced as section 14.3 describes.

- Creating a site, deploying a commit, adding a domain and removing a
  site are jobs.

- Each job records its steps, so a worker restarted in the middle resumes
  from the last finished one. The slow parts (builds, starts, gates)
  happen in the site's daemon, so a job mostly calls and waits.

- Jobs for one site run one at a time.

## 2.4 Running the hub

- **Image:** the hub's project built with `muructl build --deployment`.

- **Migrations:** a declared `migrate` command, run by a Job from the new
  image before the Deployment moves to it, as Muru's Kubernetes guide
  describes.

- **Secrets:** the GitHub App's private key and webhook secret, the
  Django secret key and the database password, from Kubernetes Secrets
  given as environment variables.

- **Replicas:** the web Deployment can run several replicas, since its
  state is in Postgres; the jobs worker runs one.

## 2.5 Kubernetes rights

- The jobs worker's ServiceAccount is the only one in the system with
  cluster rights: namespaces and, within site namespaces, Deployments,
  Services, Ingresses, PersistentVolumeClaims, NetworkPolicies,
  ResourceQuotas, LimitRanges, Secrets, ConfigMaps and cert-manager
  Certificates.

- The web Deployment's ServiceAccount has none. It shows pod status from
  the jobs' records, or through a read-only role if that proves too slow
  (section 13).
