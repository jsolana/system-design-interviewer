---
title: Derived data, dataflow and database unbundling
type: concept
aliases: [system of record, lambda architecture, kappa, dual writes, unbundling the database, materialized views, log-based integration, lambda]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, chs. 11-12 (pp. 487-545), ch. 1, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, chs. 1 and 13 (pp. 10-12, 539-579)]
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

## Additional detail (DDIA 2nd edition, chs. 1, 13)
- *2nd edition*: "Systems of Record and Derived Data" is introduced in ch. 1 (with operational vs analytical systems, ETL and HTAP). Ch. 13 "A Philosophy of Streaming Systems" (formerly 1st-ed ch. 12) keeps the log-based integration thesis: derived views are deterministic functions of the log, which makes restructuring gradual (run old and new views side by side, shift traffic progressively) and recomputation safe. Lambda is criticized again; the unified approach needs replay through the same engine and event-time windowing.
- **Write path vs read path** (new framing): the write path is the precomputed part (eager evaluation), the read path the work done at query time (lazy); indexes, caches and materialized views move work from read to write path; offline-first clients extend the read path to the device.
- **Composing storage**: unbundled databases, federated query engines (Trino, Hoptimator), Kafka's protocol as de facto standard; integration across systems is easier with asynchronous streams than synchronous distributed transactions.
- **Correctness**: *timeliness vs integrity* (ACID couples them; streaming decouples them: integrity via exactly-once, idempotence, deterministic derivation), **loosely interpreted constraints** (overbooking, compensating transactions: apologize later if the business cost is low), **coordination-avoiding** data systems (strong integrity without synchronous coordination; serializability still useful inside derived-state maintenance), end-to-end argument and auditing ("trust, but verify").
- Ch. 14 "Doing the Right Thing" (predictive analytics, bias, privacy, law and society) is an ethics chapter: out of scope for this knowledge base.

## Appears in
[[ad-click-aggregator]], [[fb-news-feed]], [[payment-system]]

## See also
[[change-data-capture]], [[event-sourcing]], [[stream-processing]], [[batch-processing]], [[caching]], [[exactly-once-processing]]
