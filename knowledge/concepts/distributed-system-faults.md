---
title: Faults in distributed systems (networks, clocks, pauses)
type: concept
aliases: [partial failure, unreliable network, unreliable clocks, process pauses, fencing token, failure detection, Byzantine faults, system models, TrueTime]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 8 (pp. 273-322)]
---

# Faults in distributed systems

## Definition
Distributed systems suffer **partial failures** that are non-deterministic: parts may fail while others keep working. The network, clocks and process execution are unreliable.

## Why it matters
It forces designing on the assumption that anything that can go wrong, will; it justifies timeouts, quorum, fencing and consensus.

## How it works
### Unreliable networks
- Asynchronous networks (packets, not circuits): no bound on delay; a lost or delayed request, a crashed node, or a lost response are indistinguishable from the outside. The only real detector is the **timeout**.
- Long timeout = slow recovery; short = false positives (and duplicating load when the system is already saturated). Variable delays due to queueing (switch, CPU, TCP).
- Network partitions happen; you must decide what to do.

### Unreliable clocks
- **Time-of-day** (can jump backwards due to NTP) vs **monotonic** (for measuring durations, not comparable across nodes).
- Drift, NTP with limited accuracy; a timestamp is a confidence interval (Spanner's TrueTime returns [earliest, latest]).
- Spanner uses TrueTime intervals for global snapshot isolation: it waits for the clock uncertainty to pass before committing so that timestamps respect causality.
- Danger: ordering events by timestamp (LWW drops writes; see [[conflict-resolution]]). Use **logical clocks** ([[logical-clocks-and-causality]]).

### Process pauses
- GC, suspended VM, swap, SIGSTOP... a node can pause without knowing it and later believe it is still the leader or that its *lease* is still valid.
- **Fencing tokens**: an increasing number on each lock/lease grant; the resource rejects writes with a lower token ([[distributed-lock]]).

### The truth is defined by the majority
- A node cannot trust its own judgment; decisions (leader, lock, declaring a node dead) are made by a **quorum** ([[consensus]]).
- **Byzantine faults** (nodes that lie): ignored in your own datacenters.

### System models
- Timing: synchronous, **partially synchronous** (realistic: sometimes unbounded), asynchronous. Node failures: crash-stop, **crash-recovery**, Byzantine.
- Properties: **safety** (nothing bad ever happens; e.g. uniqueness of fencing tokens) vs **liveness** (something good eventually happens; e.g. availability). Algorithms must always preserve safety and liveness under reasonable assumptions.

## Variants and techniques
Health checks/heartbeats, leases with TTL, quorum, fencing, retries with [[idempotency]], failure simulation / fault injection.

## Trade-offs
Fast detection vs false positives; software-based reliability (more complexity) vs dedicated hardware (atomic clocks/GPS, expensive).

## When to use it / when not to
A permanent mental framework when designing distributed services; does not apply to single-node systems.

## Appears in


## See also
[[consensus]], [[linearizability]], [[replication]], [[distributed-lock]], [[rate-limiting]]
