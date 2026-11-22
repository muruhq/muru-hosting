# 10. MCP for AI assistants

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

The hub serves the Model Context Protocol, so a site member can set up
the assistant on their own machine (Claude Code, Claude Desktop, any MCP
client) to manage their sites: deploy a commit, watch the rollout, read
the logs and events of a failing release, roll back.

## 10.1 The server

- Streamable HTTP at `https://HUB/mcp`, built with the Python MCP SDK as
  an ASGI application and served at that path by a Muru mount beside the
  Django WSGI application.

- The tools call the same service layer as the hub's pages: one function
  per action, which checks the person's role and entitlements, carries it
  out and writes the audit entry. A tool can do nothing a page cannot,
  and the audit records that the action came through MCP, with the
  client's name.

- Streams become bounded snapshots, as in Muru's own MCP server: events
  after a sequence number, the last lines of a log, a command run's
  output so far, a deploy's state when asked again.

- Every tool carries the protocol's annotations (read-only, destructive,
  idempotent), and the hub enforces what they say rather than trusting a
  client to.

- The initialize response's instructions carry a short model of the
  hub's objects (site, release, rollout, the deploy triggers, what each
  operation does to traffic), and the hub serves a skill a member can
  install, teaching the loop: push, deploy, watch, check, roll back.

## 10.2 Tool sets

| Set | Tools | For |
| --- | --- | --- |
| Member | list sites, site status, releases with their commits, deploy a commit, deploy status, promote, roll back, rollout control, restart workers, maintenance, list and run declared commands, command output, logs, events, a metrics summary, custom domain status | site owners and members |
| Viewer | the member set's reading tools | viewers, and any token made read-only |
| Group lead | list the group's sites, their status, releases, logs and events | group leads |
| Admin | create a site, set entitlements and members, recreate a pod, read the audit log | platform admins |

The lead and admin sets are off for the whole hub unless its settings
turn them on, and then off for each account unless an admin turns them on
for it. Removing a site, removing a group and changing another admin's
rights are never offered over MCP, whatever is turned on.

## 10.3 Access

Three checks, each of which can only narrow what the one before it
allows:

1. **The account's entitlement:** MCP access off, or on with the sets an
   admin allows it.

2. **The token's scope:** the sets and sites the person chose when making
   it, and whether it is read-only.

3. **The person's role on each site at the moment of the call,** as for
   any page.

Signing in follows the protocol's authorisation for remote servers. The
hub is the authorisation server for its MCP endpoint, publishes its
protected resource metadata, and runs OAuth 2.1 with PKCE, the person
signing in as for the pages, through GitHub or with a local account
(section 5.8), and choosing the token's scope on the consent page.

For clients that cannot do that, a member makes a personal token on their
account page, with a scope and an expiry. Every token is listed on the
account page and can be revoked there. An admin can revoke any token, or
switch an account's MCP access off, which ends its tokens at once.
