---
title: Distributed Key-Value Store
type: interview
sources: [System Design Interview Vol.1 (Alex Xu), ch. 6, pp. 87-109]
concepts: [cap-theorem, eventual-consistency, consistent-hashing, quorum, replication, vector-clocks, gossip-protocol, merkle-tree, lsm-trees, bloom-filter, sql-vs-nosql, multi-data-center]
difficulty: high
---

# Distributed Key-Value Store

## Prompt
Design a key-value store (distributed hash table) with `put(key, value)` and `get(key)`. Design based on Dynamo, Cassandra and BigTable.

## Functional requirements
- `put(key, value)` and `get(key)`.
- Small key-value pair size (< 10 KB); able to store big data.

## Non-functional requirements
- High availability (responds quickly even with failures).
- High scalability and **auto scaling** (add/remove servers based on traffic).
- Tunable consistency.
- Low latency.

## Estimations
Not covered in the source.

## API
`put(key, value)`, `get(key)`. Keys can be plain text or hash (shorter is better); the value is opaque (strings, lists, objects).

## Data model
Key-value pairs; each modification is an immutable version with [[vector-clocks]]. Per-node storage: commit log + memory cache + SSTables ([[lsm-trees]]).

## Architecture (high-level design)
- **Single server**: in-memory hash table; optimizations: compression and keeping only hot data in memory. It falls short: a distributed system is needed.
- **CAP** ([[cap-theorem]]): choose CP or AP depending on the case (banking = CP, the book recommends AP/eventual).
- **Partitioning**: [[consistent-hashing]] (even distribution, minimal redistribution, auto scaling, heterogeneity: more virtual nodes for more powerful servers).
- **Replication**: asynchronous to N servers (N configurable): from the key's position, the first N *unique* servers clockwise (with virtual nodes, physical duplicates must be skipped). Replicas in different data centers connected by fast networks ([[multi-data-center]]).
- **Consistency**: [[quorum]] with N, W, R. W+R>N = strong consistency (N=3, W=R=2). Models: strong, weak, eventual (recommended, as in Dynamo/Cassandra).
- **Inconsistency resolution**: versioning with [[vector-clocks]]; the client reconciles.
- **Decentralized architecture**: the client talks to a *coordinator* (proxy); nodes are on a ring; all have the same responsibilities, so there is no SPOF; adding/moving nodes is automatic. Each node: API, coordinator, failure detection, replication, storage engine, conflict resolution.
- **Write path** (Cassandra): commit log -> memory cache -> flush to SSTable.
- **Read path**: memory -> if not found, [[bloom-filter]] to choose SSTables -> return result.

## Deep dives
1. **Failure detection**: at least 2 independent sources are needed; all-to-all multicast is inefficient; use [[gossip-protocol]] (heartbeats, membership list).
2. **Temporary failures**: sloppy quorum (first W/R healthy servers on the ring) + hinted handoff (the stand-in returns the data when the original comes back).
3. **Permanent failures**: anti-entropy with [[merkle-tree]] (synchronizes only differing buckets; e.g. 1M buckets/1000M keys).
4. **Data center outage**: replicate across several data centers.

## Trade-offs and decisions
- W/R: latency vs consistency (R=1,W=N fast read; W=1,R=N fast write).
- Eventual consistency (availability) vs strong (blocks operations).
- Vector clocks: resolve conflicts but complicate the client and grow (they are truncated).
- Sloppy quorum: availability at the expense of the overlap guarantee.
- *Book summary*: big data -> consistent hashing; high availability for reads -> replication and multi-DC; writes -> hinted handoff/sloppy quorum; partitioned data -> consistent hashing; tunable consistency -> quorum; conflicts -> vector clocks; failures -> gossip, merkle trees, multi-DC replication.

## Related concepts
[[cap-theorem]], [[consistent-hashing]], [[quorum]], [[replication]], [[vector-clocks]], [[gossip-protocol]], [[merkle-tree]], [[lsm-trees]], [[bloom-filter]], [[sql-vs-nosql]], [[multi-data-center]]

## Follow-up questions
Not covered in the source (the chapter ends with a summary of techniques by feature).

## Variants
Not covered in the source.
