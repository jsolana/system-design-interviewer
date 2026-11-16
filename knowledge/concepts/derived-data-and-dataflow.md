---
title: Derived data, dataflow and database unbundling
type: concept
aliases: [system of record, lambda architecture, kappa, dual writes, unbundling the database, materialized views, log-based integration, lambda]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, chs. 11-12 (pp. 487-545), ch. 1]
---

# Derived data, dataflow and unbundling

## Definition
Distinguish the **system of record** (source of truth, normalized, written first) from **derived data** (caches, search indexes, materialized views, data warehouses, ML models) that can be regenerated from the source. The architecture is framed as a flow of data between specialized systems.

## Why it matters
No single system serves all access patterns (OLTP, search, analytics, cache). The key is keeping derived systems in sync without inconsistencies.

## How it works
- **Dual writes** (the application writes to both the DB and the index/cache): dangerous — race conditions (two clients see different orderings in each system) and partial failures without atomicity.
- Solution: **a single write system** and derive the rest from its *ordered log* ([[change-data-capture]], [[event-sourcing]]); consumers in order with offsets; fault tolerant (replay) and applying [[stream-processing]]. This is the principle of state machine replication.
- **Batch vs stream**: the **lambda architecture** runs batch (exact, recomputes) and stream (approximate, low latency) in parallel and merges the results; problems: maintaining two codebases, merging, incremental reprocessing. Alternative: unified engines (same logic for historical and real-time) with log replay.
- **Unbundling the database**: components (secondary indexes, materialized views, replication, full-text) built by separate systems, integrated via a log (loose coupling, fault tolerance, evolvability); trade-off: operational complexity and less transactionality. Strength: denormalized reads ("the write path precomputes, the read path is cheap"). Example: Twitter timeline as a materialized view updated by a stream (join of tweets with followers) and the celebrity exception ([[fan-out]]).
- **Constraints (uniqueness, balances) without distributed transactions**: route conflicting writes to the same log partition and process them sequentially; uniqueness requires consensus/total order ([[consensus]]); writes can be accepted and compensated later (apologies/compensation), thinking in terms of **timeliness** (the user sees the updated state) vs **integrity** (data is not lost/corrupted): integrity is more important, achieved with idempotence and deduplication ([[exactly-once-processing]]).
- Read path: reads can extend all the way to the client (offline-first, pushing changes via WebSockets/SSE to keep client state).
- Verification: auditing and (end-to-end) integrity checking, not blindly trusting the software ("trust, but verify"); event logs make auditing easier.

## Variants and techniques
Kappa-like (everything in stream with reprocessing), CQRS, lambda, batch-only.

## Trade-offs
Strict consistency (distributed transactions) vs eventual consistency with logs; simplicity of a single DB vs flexibility of several systems.

## When to use it / when not to
When several views of the same data are needed (search, cache, analytics). With a small load a single RDBMS is usually enough.

## Appears in
[[ad-click-aggregator]], [[fb-news-feed]], [[payment-system]]

## See also
[[change-data-capture]], [[event-sourcing]], [[stream-processing]], [[batch-processing]], [[caching]], [[exactly-once-processing]]
