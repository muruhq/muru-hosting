# 6. Kubernetes

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

## 6.1 Objects for each site

The hub renders a site's objects from templates in one module and
applies them with server-side apply under the field manager
`muru-hosting`, so it owns its fields and leaves others alone:

- the Namespace, labelled with the site, its owner and its group;

- a ResourceQuota and a LimitRange from the site's plan;

- a Secret holding the helper's token, and the helper's certificate;

- a ConfigMap with the daemon's file (section 3.2);

- the `state` and `site` claims (section 3.3);

- the Deployment (section 3.4);

- a Service with two ports: `http` to the edge on 8080 and `helper` to
  the helper's gRPC port;

- an Ingress for the site's hostnames (section 6.3);

- a NetworkPolicy: `http` from the ingress controller's namespace and
  `helper` from the hub's namespace, nothing else in; out, DNS and the
  package index for builds, with the Kubernetes API denied and other
  egress by plan.

Removing a site removes its namespace, after an optional snapshot of its
volumes.

## 6.2 Names

- A site's namespace is `site-OWNER-NAME`, shortened with a hash to fit a
  DNS label's 63 characters.

- Its default hostname is `NAME-OWNER.HOSTING_DOMAIN`.

## 6.3 Certificates

- Every site's default hostname is served with one wildcard certificate
  for `*.HOSTING_DOMAIN`, which cert-manager obtains by DNS-01 and every
  site's Ingress shares. One certificate keeps a course of hundreds of
  sites inside Let's Encrypt's limit of 50 certificates a week for one
  registered domain.

- A custom domain has a certificate of its own (section 9).

## 6.4 The client

The hub uses [lightkube](https://github.com/gtsystem/lightkube) for the
Kubernetes API, through one module of its own, so the choice can change
([ADR 0001](../adr/0001-lightkube-for-the-kubernetes-api.md)).
