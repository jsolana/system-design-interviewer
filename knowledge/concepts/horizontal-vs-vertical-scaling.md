---
title: Horizontal vs vertical scaling
type: concept
aliases: [scale up, scale out, vertical scaling, horizontal scaling]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 1 (pp. 9, 28-32)]
---

# Horizontal vs vertical scaling

## Definition
- **Vertical (scale up)**: add CPU/RAM/disk to a machine.
- **Horizontal (scale out)**: add more servers to the pool.

## Why it matters
It sets the growth strategy for each tier. For the web tier horizontal is preferred; for data, horizontal means sharding ([[database-partitioning]]).

## How it works
| | Vertical | Horizontal |
|---|---|---|
| Advantage | simplicity (good at low traffic) | no hard ceiling, redundancy |
| Limit | hardware (RDS has instances with up to 24 TB of RAM) | complexity: LB, sharding, consistency |
| Failure | no failover: one server down takes the system down | tolerates partial outages |
| Cost | powerful servers are much more expensive | cheaper at scale |

## Variants and techniques
Chapter 1 recipe for millions of users: stateless web tier, redundancy at every tier, cache ([[caching]]), multiple data centers ([[multi-data-center]]), assets on [[cdn-edge-computing]], sharding the data tier, splitting into services, monitoring and automation. [[message-queues]] decouple components so they can be scaled separately.

## Trade-offs
Cited example: stackoverflow.com (2013, >10M monthly visitors) ran on 1 master DB: scaling vertically goes a long way, but with SPOF risk and high cost.

## When to use it / when not to
Vertical at the start; horizontal when hardware limits are hit or availability is required.

## Appears in


## See also
[[load-balancer]], [[stateless-architecture]], [[database-replication]], [[sql-vs-nosql]]
