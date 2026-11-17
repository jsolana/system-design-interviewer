---
title: Distributed periodic scheduling (distributed cron)
type: concept
aliases: [distributed cron, cron service, periodic job scheduling]
sources: [https://sre.google/sre-book/distributed-periodic-scheduling/]
---

# Distributed periodic scheduling (distributed cron)

## Definition
A fault-tolerant service that launches jobs at configured times, replacing a single-machine cron daemon whose failure domain is one machine.

## Why it matters
Single-machine cron loses launches when the host dies; at fleet scale, losing one machine out of 1,000 must not take cron down. Related interview: [[job-scheduler]].

## How it works
- Run replicas (default 3) coordinated by Paxos ([[consensus]]); only the leader launches jobs and mutates state, and must stop talking to the datacenter scheduler (Borg) the moment it loses leadership.
- Record the start and completion of each launch synchronously via quorum, before and after the launch. Followers mirror state; the new leader finishes open launches.
- **Idempotency**: some jobs are safe to repeat (GC), others not (payroll, newsletters). Google prefers skipping a launch to a double launch (fail closed). For partial failures across multiple RPCs, make operations idempotent or look up their state; job names embed the scheduled launch time so the new leader can detect missing or duplicate launches ([[idempotency]]).
- **State**: Paxos log on local disk plus periodic snapshots (the critical artifact) backed up to a distributed filesystem; losing the log only rolls back to the last snapshot. State is kept in the service, not a distributed filesystem, since small writes are expensive there.
- **Thundering herd**: a "?" in the schedule lets the system choose a time by hashing the job configuration over the allowed range; some spikiness remains for jobs pinned to exact times.
- Numbers: smallest interval 1 minute; failover must be under 1 minute (1-2 minutes delay is too long for 5-minute jobs).

## Variants and techniques
Lease-based leader instead of full Paxos log; store state in an external DB; at-least-once vs at-most-once launch semantics.

## Trade-offs
Skip vs duplicate launches (at-most-once vs at-least-once); in-service state is fast but must be snapshotted and backed up.

## When to use it / when not to
For periodic jobs needing high availability; for workflows with dependencies see [[workflow-orchestration]].

## Note: what a senior/staff candidate should say
State the launch semantics explicitly, use leader election with fencing, record intent before launching, make jobs idempotent, and jitter schedules.

## Appears in
[[job-scheduler]]

## See also
[[job-scheduler]], [[consensus]], [[idempotency]], [[distributed-lock]]
