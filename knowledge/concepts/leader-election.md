---
title: Leader election (leases, pitfalls, alternatives)
type: concept
aliases: [leader election, lease, single leader, distributed leader]
sources: [https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/]
---

# Leader election

## Definition
Giving one component (process, host, thread, even a human) special powers such as assigning work, modifying data or serving all requests, with a mechanism to replace it on failure.

## Why it matters
Simplifies concurrency, partial failure modes, logging; a leader can offer strong consistency, one consistent cache, and notify rather than reach consensus. But it is a single point of failure/trust, limits scale, and complicates partial deployments (one-box, blue/green, rollback).

## How it works
- First consider alternatives: Step Functions for workflows, idempotent APIs, optimistic locking.
- **Leases** are Amazon's most used mechanism: a database records the leader; leader sends periodic heartbeats; if they stop, another candidate takes over. Alternatives: Paxos, ZooKeeper, custom hardware.
- **Time**: do not rely on synchronized wall clocks; use local elapsed durations; beware timer jumps, drift under CPU load, leap seconds.
- **Pitfalls**: leader believing it holds the lease longer than it does (slow/lossy network, GC pause between check and action). Check lease frequently, assume early expiry, avoid background heartbeat threads (work thread may be dead/unaware), keep audit log and visibility of leadership changes, track leader capacity, model with TLA+.
- Failure handling: persist before announcing; idempotent work so new leader can redrive; zero or two leaders may exist briefly; idempotent workloads tolerate two leaders; "at most one" systems need consistent election plus a downstream guard (the DB prevents two lease holders from interfering).
- Use tested libraries (DynamoDB lock client, ZooKeeper clients) rather than custom code.

## Variants and techniques
Shard the leader (one leader per data item/shard: DynamoDB, EBS, EFS); KCL leases give each Kinesis shard one owner; RDBMS primary with manual or automated failover.

## Trade-offs
Simplicity and consistency vs availability, scale ceiling, blast radius, deployment safety.

## When to use it / when not to
Use when single-writer ordering is needed; limit scope via sharding; avoid when idempotency/optimistic locking suffice.

## Appears in
[[job-scheduler]]

## See also
[[consensus]], [[distributed-lock]], [[replication]], [[optimistic-concurrency-control]], [[idempotency]], [[logical-clocks-and-causality]]

## Interview note (senior/staff)
Say: "Leases with local-duration timers, fencing so a stale leader cannot write, idempotent work for redrive, leader per shard to bound blast radius," and state you can't guarantee exactly one leader, only design for zero or two. Prefer avoiding a leader if idempotency plus optimistic locking works.
