# 9. Custom domains

```{admonition} Design specification
:class: note

This page is part of the muru-hosting design specification and describes
intended design. See the [specification index](index.md) for how it is
maintained.
```

## 9.1 Adding a domain

A member adds a domain of their own to a site, up to the site's number of
custom domains (section 5.3):

1. The hub shows the records to create: a CNAME from the domain to the
   site's default hostname (or, for an apex domain, A and AAAA records to
   the ingress's addresses), and a TXT record `_muru-hosting.DOMAIN`
   holding a token for this site.

2. The hub checks both from public resolvers, when asked and then on a
   schedule, and shows what it found. The TXT record proves the domain is
   the member's, so no one can claim a domain that points at the service
   but belongs to someone else.

3. Once both hold, a job adds the domain to the site's Ingress, a
   cert-manager Certificate for it by HTTP-01 through the ingress, and the
   host to the site's daemon with `ApplyConfig`. The site's page shows the
   certificate's state, its expiry and its renewals.

4. A domain whose records stop holding is shown as failing and, after a
   grace period, removed, so a lapsed domain does not keep a certificate
   being renewed.

Removing a domain reverses step 3. A domain belongs to one site at a time.

## 9.2 Where Let's Encrypt lives

In stage 0, and in stage 1 as section 12 describes it, TLS ends at the
ingress, so cert-manager does all of it and nothing is needed from Muru.

Muru's own ACME (muruhq/muru#133, HTTP-01 and TLS-ALPN-01 in the edge)
matters when TLS moves into the site's pod: an SNI router, or the ingress
passing TLS through to the edge, so that the certificate's key is held
only by the site's edge and the site serves HTTP/2 itself. That is an
option for stage 1, with the edge in a container of its own holding the
keys out of the site's code's reach. The hub then adds hosts with ACME
settings through `ApplyConfig` instead of Certificates.
