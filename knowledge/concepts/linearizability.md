---
title: Linearizability and the CAP theorem
type: concept
aliases: [strong consistency, atomic consistency, CAP theorem, recency guarantee, causal consistency]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 9 (pp. 324-352)]
---

# Linearizability and the CAP theorem

## Definition
**Linearizability**: the system behaves as if there were a single copy of the data and all operations were atomic; once a write completes, any later read sees that value (recency guarantee). It is a consistency model over a single object, distinct from serializability (transaction isolation).

## Why it matters
Needed for locks and leader election, uniqueness constraints (username, account number), coordination across channels (e.g. uploading an image and enqueuing its resize: a fast channel may see stale state).

## How it works
- With a single copy there is no problem; with replication it depends:
  - Single-leader: potentially linearizable if reading from the leader or from synchronous followers (but split brain or failover breaks this).
  - Consensus (ZooKeeper, etcd): linearizable ([[consensus]]).
  - Multi-leader: no. Leaderless with quorum: normally no, even with w+r>n ([[quorum]]).
- Implementing on top of total order broadcast: append a message, wait to see it delivered; compare-and-set as a log.
- **Cost**: the network must be available. Any linearizable DB loses availability under a partition; it is also slow (response time depends on network delay, there is no linearizable algorithm with better performance).

### CAP (reformulated)
- If it is linearizable and there is a network partition -> the disconnected replicas cannot process requests (**CP**). If availability is prioritized under a partition -> not linearizable (**AP**). Better to say "either consistent or available *when there is a partition*". Of little use as a classification; the source calls it misleading/historical.
- Many systems are not linearizable for **performance** reasons (even multicore CPUs with caches), not for partition tolerance.

## Variants and techniques
- **Causal consistency**: preserves causality without a latency/availability penalty; maintained with [[logical-clocks-and-causality]].
- Synchronized clocks (Spanner TrueTime) for global snapshots.

## Trade-offs
Linearizable: easy to reason about, expensive in latency and availability. Causal: weaker but scalable.

## When to use it / when not to
Locks, leader election, uniqueness. Not for data whose reads tolerate staleness (feeds, approximate counters): prefer eventual/causal.

## Appears in


## See also
[[consensus]], [[replication]], [[transactions-and-isolation-levels]], [[serializability]], [[distributed-lock]]
