---
title: Shard management and load-based rebalancing
type: concept
aliases: [shard manager, shard assignment, load balancing of shards]
sources: [https://www.uber.com/es/en/blog/introducing-shard-manager/, https://www.linkedin.com/blog/engineering/infrastructure/introducing-northguard-and-xinfra]
---

# Shard management and load-based rebalancing

## Definition
A control plane that decides which host owns which shard, and moves shards based on observed load rather than on shard counts.

## Why it matters
Equal shard counts do not mean equal load; clusters get sized for the hottest host and the rest sits idle. Uber's Cadence used a Ringpop hash ring that balanced counts only, had no authoritative assignment record and could only move work by changing membership.

## How it works (Uber Shard Manager, Go + gRPC + etcd)
- **Shard Manager service**: one leader per namespace decides ownership; assignments and leader election live in etcd.
- **Executors** own shards, heartbeat and report per-shard load. **Spectators** cache the shard->owner map and route requests directly; requests never pass through the manager (control plane off the data path).
- **Rebalancing**: smoothed load, an acceptance band (upper/lower thresholds around the average), greedy choice of the move that brings source and destination closest (example: hosts at 160 = 100+60 and 40: move the 60 shard, giving 100/100), plus a movement budget and cooldown to avoid churn. Operators can drain a host or a shard (`smctl`).

## Variants and techniques
- Hash ring by count (Ringpop) vs explicit assignment by load.
- Embedded controller vs dedicated service (clearer ownership, shared foundation, extra component).
- Smaller replication units (LinkedIn Northguard segments instead of partitions) reduce skew so rebalancing is mostly "new segments go to new brokers" with no data movement.

## Trade-offs
- Responsiveness vs churn: Uber chose fewer moves and slower convergence.
- Quality depends on applications reporting load that reflects real work.
- Migrating between ownership systems needs a shared source of truth to avoid stalls.

## When to use it / when not to
Use when shard load is skewed and the fleet is sized for peaks. Plain consistent hashing is enough for uniform, stateless-ish keys.

## Results (production, Cadence Matching)
Hottest-host CPU down 38%; hottest/average ratio about 2.3x -> 1.4x; about 40% fewer hosts for same traffic; within 5% of a constraint solver's optimum in 23 of 24 snapshots (within 1% in 14).

## Appears in
[[distributed-message-queue]]

## See also
[[consistent-hashing]], [[database-partitioning]], [[hot-keys]], [[online-data-migration]], [[service-discovery]]
