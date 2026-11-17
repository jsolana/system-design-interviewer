---
title: Shuffle sharding and workload isolation
type: concept
aliases: [shuffle sharding, blast radius reduction, virtual shards, noisy neighbor isolation]
sources: [https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/, https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/, https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/]
---

# Shuffle sharding and workload isolation

## Definition
Assign each customer/resource a small **virtual shard** consisting of a unique-ish combination of workers drawn from the whole fleet. A bad actor or poison request only impacts the workers in its combination; other customers overlap on at most a few workers and still have healthy ones.

## Why it matters
Gives much smaller blast radius than regular sharding, usually at no extra infrastructure cost. Origin: Amazon Route 53 had to host root domains and survive frequent DDoS without buying scrubbing capacity for every domain (tens of millions of dollars).

## How it works
- No sharding: all workers serve everyone; a poison request can take down everything.
- Regular sharding: 8 workers in 4 shards of 2 -> impact ~25% (1/4) but less redundancy per shard.
- Shuffle sharding: shard size 2 from 8 workers = C(8,2) = 28 combinations -> impact ~1/28 (~7x better). More workers and customers improve it; with enough combinations every customer gets a unique shard.
- Requires **fault-tolerant clients** (retry on another worker in the shard).
- Route 53: 2,048 virtual name servers; each domain gets 4; ~730 billion possible shards; no two domains share more than 2 servers. Attacked domain's 4 servers saturate, others survive; attacked customer can be moved to dedicated capacity. Virtual servers are not tied to hosts so they can be moved.
- **Recursive shuffle sharding** isolates a customer's own customers. Open source: Route 53 Infima library.
- **Queues (AWS Lambda async)**: fixed set of queues, hash each customer to a small subset, enqueue to the least-full of them; a noisy customer backs up only its own queues (see [[queue-backlog-management]]).

## Variants and techniques
**Cell-based architecture**: independent full copies (cells) of the service each serving a subset of customers, with a thin routing layer; capacity tested per cell, new cells added before limits. Deployments proceed cell by cell (and AZ/Region waves) to limit blast radius ([[safe-deployments-and-rollbacks]]). Route 53 health checkers are also cellular ([[constant-work-pattern]]). Tenant-sharding background: [[multitenancy-and-cell-based-architecture]].

## Trade-offs
| Aspect | Benefit | Cost |
|---|---|---|
| vs no sharding | tiny blast radius | careful assignment, fault-tolerant clients |
| vs regular sharding | combinatorial reduction (1/28 vs 1/4) | more complex assignment/overlap limits |
| cells | strong isolation, bounded scale-per-cell | routing layer, per-cell overhead, cross-cell operations hard |

## When to use it / when not to
Shared multi-tenant fleets exposed to noisy neighbors, poison requests or DDoS. Not useful if clients cannot retry/fail over or if all requests need all workers.

## Appears in
None yet.

## See also
[[multi-tenancy-and-fairness]], [[database-partitioning]], [[consistent-hashing]], [[static-stability]], [[load-balancer]]

## Interview note (senior/staff)
Offer shuffle sharding when asked "how do you stop one tenant/poison request from taking down everyone": give the combinatorics (8 workers, pairs -> 28 shards, 1/28 of customers affected per bad customer), mention overlap limits and fault-tolerant clients, then pair with cells and per-tenant throttling.
