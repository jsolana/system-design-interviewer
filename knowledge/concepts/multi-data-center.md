---
title: Multi data center
type: concept
aliases: [geoDNS, multi-region, geo-routing]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 1 (pp. 23-24), ch. 4 (p. 67)]
---

# Multi data center

## Definition
Deploying the system across several data centers/regions; geoDNS resolves the domain to the IP of the data center closest to the user (e.g. x% US-East, (100-x)% US-West).

## Why it matters
Better availability and lower latency for international users; on an outage, all traffic is redirected to the healthy data center.

## How it works
Technical challenges:
- **Traffic redirection**: geoDNS or other tools.
- **Data synchronization**: replicate data between data centers (typically asynchronous, like Netflix) so failover finds the data.
- **Testing and deployment**: test in every location and automate deployments to maintain consistency.

## Variants and techniques
Edge servers (Cloudflare had 194 in 2020) route to the nearest one; the rate limiter synchronizes with eventual consistency ([[rate-limiting]]).

## Trade-offs
Eventual consistency between regions versus latency and availability.

## When to use it / when not to
With a global user base or DR requirements. Excessive for a single small market.

## Appears in
[[distributed-email-service]], [[distributed-rate-limiter]], [[key-value-store]], [[proximity-service]], [[s3-object-storage]], [[stock-exchange]], [[unique-id-generator]]

## See also
[[cdn-edge-computing]], [[database-replication]]
