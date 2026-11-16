---
title: Change Data Capture (CDC)
type: concept
aliases: [CDC]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, Designing Data-Intensive Applications (Kleppmann), chs. 5 and 11]
---

# Change Data Capture (CDC)

## Definition
Capturing the changes of a DB in order to propagate them to other systems.

## Why it matters
It keeps a secondary index (Elasticsearch) in sync with the source of truth (PostgreSQL).

## How it works
Changes in Postgres are emitted and applied to the search index.

## Variants and techniques
Not detailed in the source.

## Trade-offs
Reliability of the synchronization and eventual consistency of the index.

## When to use it / when not to
When maintaining derived replicas (search, cache) of a primary DB.

## Additional detail (DDIA, chs. 5 and 11)
- **What it is**: observing all the changes written to a DB (the *system of record*) and exposing them as a stream in the same order, to feed search indexes, caches, a data warehouse. It is implemented by reading the logical replication log (MySQL row-based binlog, decoded WAL in Postgres; Debezium, Maxwell) or with triggers (more fragile).
- **Why**: it avoids *dual writes* (the application writes to the DB and to another system: ordering races and partial failures that leave inconsistencies); see [[derived-data-and-dataflow]].
- **Initial snapshot**: to create a new consumer you must copy a consistent snapshot tied to an exact log position/offset and then apply the changes; alternative: **log compaction** (keep only the latest value per key, tombstones for deletes), which allows rebuilding from the log without a snapshot (Kafka).
- Asynchronous consumption -> derived data is eventually consistent (lag, read-your-writes) ([[replication]]).
- Related variant: [[event-sourcing]] (the event is the primary data).

## Appears in
[[hotel-reservation]], [[ticketmaster]], [[tinder]]

## See also
[[full-text-search]]
