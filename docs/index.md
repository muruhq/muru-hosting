# muru-hosting

muru-hosting is a hosting control plane on Kubernetes for Python web sites
served by [Muru](https://github.com/muruhq/muru). Each site runs in a pod
of its own, is deployed from GitHub as Muru releases, and is managed by
the people it belongs to through a web interface and through their own AI
assistant over MCP.

```{admonition} A proof of concept
:class: warning

muru-hosting exists to dogfood Muru with a real application, and to test
and extend Muru's APIs until Muru suits web hosting services for Python
applications. It is not a product and not a supported project: nothing
about it is stable, and nothing should be hosted on it that matters.
```

## Project

```{toctree}
:maxdepth: 1

project/about
project/design/index
project/adr/index
```
