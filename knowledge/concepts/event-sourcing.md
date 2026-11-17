---
title: Event sourcing and CQRS
type: concept
aliases: [event log, CQRS, immutable events, materialized views, command vs event, append-only log]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 12 pp. 355-374, Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 11 (pp. 495-512), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 3 (pp. 101-105), ch. 12 (pp. 508-512)]
---

# Event sourcing and CQRS

## Definition
Store all state changes as an **immutable sequence of events** (append-only); the current state is a **derived view** obtained by applying the events (CQRS: separate the write model from the read model).

## Why it matters
Auditability and traceability, recomputing and creating new views (by reprocessing the log), debugging, avoiding corruption from bugs (the log is not lost), aligning with the accounting model (ledger of entries; corrected with a compensating entry, not by deleting).

## How it works
- Distinction: in CDC the log is *derived* from low-level changes of a mutable DB; in event sourcing the **event** (business intent) is written first and the state is derived, deterministic (same input -> same state).
- Command vs event: a *command* can be rejected; once validated it becomes a done event (e.g. "reservation requested" -> "reservation confirmed"). Seat reservations: tentative event + confirmation.
- Reconstruction: log replay, with periodic snapshots; **log compaction** doesn't apply the same way (events must be kept).
- Several optimized read views (denormalized, indexes, caches, search) fed from the same log; changing schema = build a new view in parallel and migrate gradually.

## Variants and techniques
- **CQRS**: write model (log) and read models (views).
- Concurrency: a single writer per log partition serializes and avoids locks.
- Limitation: real deletion (privacy, legislation) and event schema changes; reads may lag (eventual consistency; read-your-writes with synchrony or transactions over the log).

## Trade-offs
Advantages: auditability, flexibility, recovery. Disadvantages: eventual consistency of views, more storage, hard deletion, learning curve.

## When to use it / when not to
Domains with auditing and multiple consumers (finance, carts, reservations). Not for simple CRUD.

## Additional detail (Xu & Lam Vol. 2, ch. 12)
- Terms: **command** (intent, FIFO, may be invalid or involve I/O), **event** (validated fact, immutable, deterministic, in the past; a command generates zero or more), **state**, deterministic **state machine** (validates and applies).
- Main benefit: **reproducibility/auditability** (balance at any instant, verify historical correctness, compare code versions over the same events). Read views via [[cqrs]].
- High performance: command/event list in local append-only files with `mmap`, state in RocksDB/SQLite, periodic snapshots in object storage; reliability by replicating only the event list with **Raft** (commands are not enough because event generation may be non-deterministic); scaling with partitions and TC/C or Saga. See [[digital-wallet]].

## Additional detail (DDIA 2nd edition, chs. 3 and 12)
- *2nd edition*: event sourcing/CQRS moved into the data-models chapter (ch. 3, pp. 101-105). Added advantages: events record **intent** ("booking canceled" vs row mutations); views are reproducible (delete and recompute after a view bug); several views in any data model, even in-memory only; mistakes fixed by compensating/deletion events; audit log; logs absorb write bursts.
- Added downsides: **determinism with external data** (include the exchange rate in the event or query it by event timestamp); **immutability vs GDPR** (per-user logs can be deleted; otherwise keep personal data outside the event or use **crypto-shredding**); replaying must not repeat side effects (re-sending emails). Name events in the past tense; all views must consume events in the same order. Tools: EventStoreDB, MartenDB, Axon, Kafka + stream processors.
- Distinction from CDC: see [[change-data-capture]].

## Appears in
[[digital-wallet]], [[stock-exchange]]

## See also
[[change-data-capture]], [[stream-processing]], [[derived-data-and-dataflow]], [[write-ahead-log]], [[message-queues]]
