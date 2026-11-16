---
title: Stateless web tier
type: concept
aliases: [stateless architecture, stateful vs stateless, session externalization]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 1 (pp. 20-22)]
---

# Stateless web tier

## Definition
Web servers do not keep client state between requests (e.g. session); the state lives in a shared data store (relational, Memcached/Redis, NoSQL).

## Why it matters
A stateful server requires all of a client's requests to reach it (sticky sessions). A stateless system is simpler, more robust and more scalable, and allows autoscaling of the web tier.

## How it works
- Move sessions/profile out of the web servers into a shared store (the book picks NoSQL for its ease of scaling).
- Any server handles any request by reading the state from the store.
- Autoscaling: add/remove servers based on load, with no loss of state.

## Variants and techniques
Stateful + sticky sessions at the [[load-balancer]] (a less scalable alternative).

## Trade-offs
The shared store becomes a critical dependency (needs [[database-replication]]/redundancy) and adds a network hop per request.

## When to use it / when not to
The default for the web tier. Local state only if it is disposable or recoverable.

## Appears in
[[dropbox]], [[nearby-friends]], [[notification-system]], [[url-shortener]], [[web-crawler]], [[youtube]]

## See also
[[load-balancer]], [[horizontal-vs-vertical-scaling]]
