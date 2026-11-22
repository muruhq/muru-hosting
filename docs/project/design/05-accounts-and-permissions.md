# 5. Accounts and permissions

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

## 5.1 Signing in

Sign-in is through GitHub only, with the GitHub App's user authorisation
(section 8.1) through django-allauth's GitHub provider. Who may sign in is
an admin setting made of rules, any one of which admits a person:

- a listed GitHub username;

- membership of a GitHub organisation;

- membership of a team within an organisation, which is how a course
  maps: the course's organisation and its student team, as GitHub
  Classroom arranges them.

Membership is checked at each sign-in and refreshed on a schedule, so
someone removed from a team loses access within that period. The first
platform admin is named in the hub's settings; the others are listed
users or members of a named admin team. For development, local accounts
can stand in for GitHub sign-in (section 5.8).

## 5.2 Groups

A group collects sites: a course, a team, a customer. It has leads
(staff, team leads) and optionally a GitHub team it follows, so that its
members are known without listing them.

## 5.3 Owners and entitlements

Every site has one owner, the account it counts against, and may have
other members. An account may own several sites. What an account may
have is its entitlements, set by an admin, with defaults from the hub's
settings, then the group, then the account itself:

| Entitlement | Default | Says |
| --- | --- | --- |
| Sites | 1 | how many sites the account may own |
| Creates its own sites | off | whether the account may create sites itself, up to its number, or only an admin creates them for it |
| Removes its own sites | off | whether the owner may remove a site, or only an admin |
| Plan | the group's | the plan new sites take; an admin may set another per site |
| Custom domains | 0 per site | how many domains of its own each site may have (section 9) |
| MCP access | off | whether the account may use the hub's MCP server, and with which tool sets (section 10) |

- An admin creating a site for an account, or giving an existing site a
  new owner, is refused beyond the owner's number, unless the admin
  raises it.

- Lowering the number below what an account owns keeps its sites and
  refuses new ones.

- A group's bulk creation gives each member of the group's team one site,
  counted the same way.

## 5.4 Roles

| Role | Held by | Can |
| --- | --- | --- |
| Platform admin | listed users, the admin team | everything: create and remove sites and groups, set entitlements, plans and quotas, set owners and members, change domains, recreate a site's pod, upgrade site images, read the audit log |
| Group lead | named in the group | read every site in the group and its audit entries; create sites in the group when an admin allows it, in bulk from the group's GitHub team |
| Site owner | the account a site counts against | what a member can, and set the site's members and viewers; create and remove its own sites only where its entitlements allow |
| Site member | named on the site, or admitted by the site's repository rule (section 5.5) | deploy, promote, roll back, start and control rollouts, restart workers (Muru's rolling restart), run the site's declared commands, set maintenance, read logs, events, metrics and command runs, link the site to a repository, set the deploy trigger and policy, add custom domains within the site's number |
| Site viewer | named on the site | read what members read |

Creating and removing sites, quotas and pod-level actions are admin
operations, except where an owner's entitlements allow it to create or
remove its own sites.

### 5.4.1 What is checked so far

Sites have no members or viewers yet. A site is seen by its owner and by
platform admins, and the same people may act on it. The two questions are
asked separately all the same, by `sites_visible_to` and `may_operate` in
the service layer: a page answers 404 for a site the person may not see
and 403 for an action on one they may only look at, and shows no action
it would refuse.

## 5.5 The repository rule

A site linked to a repository may say that anyone with write access to
the repository is a member. The hub asks GitHub at the moment of each
action, never from a cached answer, and records which rule admitted the
person.

## 5.6 Plans

A plan bounds a site: memory and CPU for the pod, the sizes of its
claims, the releases it retains, whether canaries are allowed, and its
scaling bounds. Kubernetes enforces resources through the namespace's
ResourceQuota and LimitRange; the hub refuses member actions beyond the
plan's Muru bounds.

## 5.7 Audit

Every action records who took it, which rule admitted them, the site,
the Muru call with its arguments (secrets redacted), the way it came (a
page, the Actions API or MCP, with the client's name) and its outcome.
The hub's audit log is the only record of the person, since Muru's
events name the helper's user (section 11.2).

### 5.7.1 What is recorded so far

Each action on a site adds an entry with who took it (nobody, for a
management command run on the hub's machine), whether it came from a page
or a command, the action, what it was taken on, whether it succeeded and
what came of it. A site's page lists its latest entries as its activity.
Which rule admitted the person and the Muru call with its arguments are
not recorded yet.

## 5.8 Local accounts

For development, before a GitHub App exists, the hub can run with
accounts of its own instead of GitHub sign-in.

- **Sign-in is a setting,** `github` by default or `local`. With
  `local`, people sign in with a username and password held by Django's
  own authentication, and GitHub sign-in is not offered. The sign-in
  rules of section 5.1 do not apply.

- **Accounts** are made by an admin, the first with `manage.py
  createsuperuser` and the others through the Django admin site, which is
  on with local sign-in and off by default otherwise. A superuser is a
  platform admin.

- **Everything else is the same:** groups, owners, entitlements, roles,
  plans and the audit log work on local accounts as on GitHub ones, and
  the MCP server's sign-in (section 10.3) goes through the local sign-in
  page.

- **GitHub is separate from sign-in.** Deploys from a repository,
  webhooks and deployment statuses use the GitHub App's own credentials,
  so they work with local sign-in once an App is configured. The
  repository rule (section 5.5) and a group's GitHub team admit nobody,
  since a local account has no GitHub identity.

- **Without a GitHub App,** the parts that need one are not shown, and a
  site is deployed from a directory on the hub's machine with `manage.py
  deploy_site OWNER/NAME PATH`. It archives the directory and goes
  through the same upload and deploy as a commit (section 8), recording
  the commit when the directory is a git checkout with no uncommitted
  changes.

- **It cannot go unnoticed:** with local sign-in, every page's header
  says that the hub uses local accounts.

- **GitHub sign-in without an App** admits nobody: the sign-in page says
  that the hub has no GitHub App configured, and names the setting for
  local accounts.
