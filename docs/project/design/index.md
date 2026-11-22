# Design specification

muru-hosting is a proof of concept hosting control plane on Kubernetes
for Python web sites served by Muru, built to dogfood Muru and to test and
extend its APIs for hosting services.

## How the specification is maintained

- This copy is the source of truth for intended design. It changes
  through pull requests like code, and its history is the git history.

- When implementation shows that the specification needs to change, the
  change is made in the same pull request, with a new
  [architecture decision record](../adr/index.md) for a significant
  choice. Nobody deviates from the specification silently.

- Section numbers are kept stable so that issues, pull requests and
  decision records can refer to them. New material is added as new
  subsections rather than by renumbering.

- Cross references of the form "section 4.2" refer to the numbered
  sections below. A reference of the form muruhq/muru#146 is an issue in
  Muru's tracker.

## Sections

```{toctree}
:maxdepth: 1

01-overview.md
02-hub.md
03-site-pod.md
04-site-helper.md
05-accounts-and-permissions.md
06-kubernetes.md
07-site-lifecycle.md
08-deploying.md
09-custom-domains.md
10-mcp.md
11-needs-from-muru.md
12-split-controller.md
13-open-questions.md
14-observability.md
15-development.md
```
