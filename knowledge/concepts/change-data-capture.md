---
title: Change Data Capture (CDC)
type: concept
aliases: [CDC]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, Designing Data-Intensive Applications (Kleppmann), chs. 5 and 11, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 12 (pp. 500-512), https://shopify.engineering/capturing-every-change-shopify-sharded-monolith]
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

## Additional detail (DDIA 2nd edition, ch. 12)
- *2nd edition (new)*: **CDC and database schemas**: CDC exposes the upstream schema, turning it into a public API (dropping a column breaks consumers, possibly customer-facing services). Mitigation: the **outbox pattern** (a table with its own stable schema written in the same DB transaction as the domain change; CDC reads the outbox). It is a dual write kept inside one system; cost: transformation code and extra writes.
- **CDC vs event sourcing**: CDC extracts low-level changes from a mutable DB (event usually carries the whole new record, so **log compaction** by key keeps only the latest); event sourcing stores intent-level immutable events, later events do not override earlier ones, so the full history is needed (snapshots are only an optimization).
- Quorum databases (Cassandra) cannot give a single change stream; they expose raw per-node log segments the consumer must merge. Kafka Connect integrates CDC tools with Kafka.

## Additional detail (Shopify CDC platform)
Shopify's query-based tool (poll replicas for newer `updated_at`) was at best hourly fresh, missed hard deletes and unreliable `updated_at` changes, lost intermediate states and starved constantly-updated rows. Replacement: log-based CDC with Debezium (about 150 connectors on 12 Kubernetes pods, 100+ MySQL shards) -> Kafka Connect RegexRouter -> Kafka Streams split into one compacted topic per table, partitioned by primary key, Avro + Schema Registry. Large records: compress >1 MB, otherwise offload to GCS and keep a pointer in the header (simpler consumers, but extra dependency and cleanup). Numbers: 400TB+ in Kafka, about 65k records/s average on BFCM 2020 (spikes 100k), p99 under 10 s end to end. Pain points: snapshots lock tables and can block binlog events for hours; tables added later get no snapshot; breaking schema changes ripple; incremental snapshots planned. Source: https://shopify.engineering/capturing-every-change-shopify-sharded-monolith

## Appears in
[[hotel-reservation]], [[ticketmaster]], [[tinder]], [[twitter-search]]

## See also
[[full-text-search]]
