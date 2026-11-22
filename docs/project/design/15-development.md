# 15. Development

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

## 15.1 Order of work

Stage 0 is built in three phases, so that each part is developed where it
is quickest to work on, and the hub never has to reach into a cluster
from outside it.

1. **Sites on a laptop.** Each site is a Muru daemon of its own on the
   developer's machine, macOS or Linux, with the helper beside it under
   `muructl run` (section 15.3). This phase builds the helper's API, the
   hub's accounts, sites, deploys from GitHub, live views, MCP server and
   tracing, all against a real daemon, with no Kubernetes.

2. **Sites in Kind.** The hub, still on the laptop, creates and removes
   sites in a local Kind cluster: the namespace, the Deployment, the
   claims, the Service, the Ingress and the policies (section 15.4). Only
   the Kubernetes API is reached from outside the cluster, through the
   kubeconfig.

3. **The hub in Kind.** The hub is built and deployed into the same
   cluster as its web and jobs Deployments (section 15.5), and from there
   reaches each site's helper as a deployment does. The code of phase 1
   that talks to helpers is used unchanged: only the helper's address
   differs.

Where a site runs is a property of the site in the hub, `local` or
`kubernetes`. The `local` kind stays after phase 3, as the quick way to
work on the helper and the hub.

## 15.2 The hub on a laptop

- The hub runs with `muructl run` from the checkout, and the jobs worker
  beside it as `manage.py db_worker`, under wrapture's launcher when
  tracing (section 14.3).

- **SQLite by default.** With no `DATABASE_URL` in the environment, the
  hub uses SQLite in `MURU_DATA_DIR`, which `muructl run` gives every
  project, so a checkout needs no database server. `DATABASE_URL` names
  Postgres, as a deployment does. `django-tasks-db` works on both,
  making its transactions exclusive on SQLite.

- **The data directory is in the checkout.** The hub's run table sets
  `data_dir` to the ignored `.muru-hosting/hub/`, and the settings fall
  back to the same directory when `MURU_DATA_DIR` is unset, so
  `manage.py` and the jobs worker, which do not run under Muru, open the
  database the run serves.

- **Settings come from the environment:** `HUB_DEBUG`, `HUB_SECRET_KEY`
  (required unless `HUB_DEBUG` is on), `HUB_ALLOWED_HOSTS`, `HUB_SIGN_IN`
  and `DATABASE_URL`. The `just` recipes give a development run
  `HUB_DEBUG=1` and `HUB_SIGN_IN=local`.

- **Code runs on both.** Models and queries use what Django offers on
  both databases. Something only Postgres has is used only with a SQLite
  path beside it, and a test that needs Postgres says so with a marker and
  runs in CI's Postgres job.

- **Tests** run against SQLite, with wrapture's pytest support for
  observing and standing in for collaborators (AGENTS.md).

- **No GitHub needed to start:** with local sign-in and no GitHub App
  (section 5.8), the hub runs from a fresh checkout after `manage.py
  createsuperuser`, and sites are deployed from local directories with
  `manage.py deploy_site`. Configuring an App adds deploys from GitHub
  without changing how people sign in.

- **Webhooks** reach a laptop through `gh webhook forward` (the gh
  extension cli/gh-webhook), which forwards a repository's deliveries to
  the local hub's webhook path.

## 15.3 Sites on a laptop

A local site has the parts of a site pod (section 3) as processes and
directories on the developer's machine, run as the developer's own user.

- **The daemon:** a user daemon of the site's own, started with
  `muructl daemon start` and its own `--state-dir`, `--run-dir`,
  `--log-dir` and `--config`, so it never touches the developer's own
  daemon or another site's. Its configuration file is written from the
  same template as a pod's ConfigMap (section 3.2), with a listener on a
  port of the site's own on 127.0.0.1 and the site's data directory
  beneath the site directory below.

- **The site directory:** a directory per site in the checkout's
  ignored `.muru-hosting/sites/OWNER-NAME/`, standing in for the `site`
  claim, with the daemon's state and logs beside it. The run directory,
  which holds the admin socket, is under `/tmp`, since a Unix socket path
  is limited to 104 bytes on macOS.

- **The helper:** the helper's project under `muructl run`, with the
  admin socket's path, the site directory, its listening address and its
  token in its settings, all of which a pod gives it too. It listens on
  127.0.0.1 without TLS, which is a setting; the token is still required.

- **Starting and registering:** `just site-up OWNER/NAME` starts a site's
  daemon and helper (`scripts/local-site.py`) and registers the site
  with the hub through `manage.py register_site`, which records the
  helper's address and token, the site's directory and its address on a
  site of the `local` kind. `just site-down OWNER/NAME` forgets the site,
  stops both and removes the directories. The hub's job for creating a
  `local` site starts nothing: it deploys the hello site through the
  helper, as for any site (section 7.1). Removing one forgets it.

- **Ports:** the daemon and the helper each take a free port on
  127.0.0.1 when the site is first started, kept with the helper's pid in
  the site's directory, so a site keeps its address across restarts.

- **The jobs worker** carries out the deploy, so `just worker` runs
  beside `just hub` for a new site to get its hello site.

- **Deploys** go through the helper's `Sources` service and the admin
  API exactly as in a pod, since the helper and the daemon share the
  site directory and the user.

- **Tracing:** the hub, the jobs worker and each helper export to the
  viewer on the laptop (section 14.4), so one viewer shows a webhook, its
  job and the helper's calls together, once muruhq/muru#856 gives the
  helper's RPCs spans.

The same arrangement runs on Linux, which lets CI test the helper
against a real daemon with no cluster: the test suite starts a daemon
and the helper under `muructl run`, calls the helper as the hub does,
and takes a site from registration through the hello site to a deploy of
a directory.

### 15.3.1 The packages

One uv workspace holds the hub at the root and the packages it shares
with the helper: `packages/stubs` for the generated gRPC stubs and
`helper` for the site helper, so one environment runs the hub, the
helper and the tests. The hello site in `hello/` is not a member: it is a
project of its own, as a site's code is, with its own `uv.lock`.

The stubs are generated with their modules beneath
`muruhosting_stubs`, so that `muru.admin.v1` never meets Muru's own
`muru` package in a worker. The `.proto` file of the pinned release is
kept beside them, so an upgrade of Muru shows what changed in the API.

## 15.4 Sites in Kind

The hub on a laptop manages sites in a local Kind cluster that already
has an ingress controller installed, mapped to the host's ports as Kind's
ingress guide describes.

- **The cluster:** the hub uses the kubeconfig's current context, or the
  context its settings name, so it never acts on a cluster by accident; a
  context that is not a Kind cluster's is refused unless the settings say
  otherwise.

- **Images:** the site runtime and helper images are built locally and
  loaded with `kind load docker-image`, with `imagePullPolicy:
  IfNotPresent`.

- **Hostnames:** `HOSTING_DOMAIN` is a wildcard name that resolves to the
  host, such as `127-0-0-1.nip.io`, so a site answers at
  `NAME-OWNER.127-0-0-1.nip.io` through the ingress controller. Sites are
  served over HTTP in development; with cert-manager in the cluster and a
  self-signed issuer named in the settings, over HTTPS.

- **Storage:** the access mode of the claims is a setting.
  ReadWriteOncePod needs a CSI driver, which Kind's default storage class
  may not be, so development uses ReadWriteOnce.

- **Network policies** are applied as in a deployment, and enforced only
  if the cluster's network plugin enforces them.

- **Ingress class:** the class of the cluster's ingress controller is a
  setting, so the hub works with whichever controller is installed.

- **What this phase checks:** that a site's objects are applied, updated
  and removed as section 6 describes, that its pod becomes ready with the
  helper healthy, and that its hostname reaches the daemon through the
  ingress, which answers 503 until a release serves.

- **The helper is not reached.** A hub outside the cluster cannot reach
  a helper's Service, and the hub has no code for doing so. In this
  phase a development setting ends the creating job once the pod is
  ready, before the hello site's deploy, which phase 3 checks.

## 15.5 The hub in Kind

- **Image:** the hub built with `muructl build --deployment` and loaded
  with `kind load docker-image`, deployed as section 2.4 describes, with
  its migration Job.

- **Database:** a single Postgres pod in the hub's namespace, from the
  development manifests, without a backup.

- **Address:** the hub answers at `hub.127-0-0-1.nip.io` through the
  ingress controller, which is also the GitHub App's callback address
  for development.

- **Webhooks:** `gh webhook forward` sends deliveries to the hub's
  address in the cluster.

- **Tracing:** the viewer Deployment of section 14.4, reached with
  `kubectl port-forward`.

## 15.6 Development commands

The commands for running the hub, the worker, local sites, the viewer
and the Kind images are recipes in the `justfile`, added as the code
they run is.
