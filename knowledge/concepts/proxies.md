---
title: Proxies
type: concept
aliases: [proxy server, reverse proxy, forward proxy]
sources: [Grokking the System Design Interview (PDF), "Proxies" pp. 183-184]
---

# Proxies

## Definition
Intermediate server between client and backend server that acts as an intermediary for requests.

## Why it matters
Allows filtering, logging and transforming requests (adding/removing headers, encrypting/decrypting, compressing) and serving from its cache resources requested by several clients without going to the remote server.

## How it works
- The client connects to the proxy, which requests the resource from other servers.
- **Open proxy**: accessible to any Internet user (variants: anonymous proxy, transparent proxy). A closed proxy serves only users of one network.
- **Reverse proxy**: fetches resources from one or more servers on behalf of the client; the response appears to originate from the proxy itself.

## Variants and techniques
Open/anonymous/transparent, reverse proxy (basis of LBs and edge caches).

## Trade-offs
You gain caching, control and security; you add a hop and a possible SPOF.

## When to use it / when not to
To centralize logging/filtering/caching; to hide backends (reverse proxy).

## Appears in


## See also
[[load-balancer]], [[caching]], [[cdn-edge-computing]]
