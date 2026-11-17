---
title: Distributed Cache
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-cache]
concepts: [caching, tail-latency, consistent-hashing, hot-keys, database-partitioning]
difficulty: medium
---

# Distributed Cache

> Note: the article is paywalled after "What is Expected at Each Level?"; only the prompt, requirements, scale and deep dive titles are readable.

## Prompt
In-memory key-value store spread across several machines, partitioned and replicated for high availability and fault tolerance.

## Functional requirements
- Set/get/delete of key-value pairs.
- Configurable expiration per key.
- LRU eviction (confirm the policy with the interviewer; LFU, FIFO... exist).
- Out of scope: configuring the cache size.

## Non-functional requirements
- High availability (eventual consistency acceptable).
- Latency < 10 ms on get/set.
- Scalable.
- Out of scope: durability, strong consistency, complex queries, transactions.

## Estimations
Given assumptions: up to 1 TB of data and peaks of 100k req/s (no detailed calculation).

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source (only three sections: CRUD, expiration, LRU).

## Deep dives
Titles only: high availability and fault tolerance; scalability; uniform key distribution; hot key with many reads; hot key with many writes; performance.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[caching]], [[consistent-hashing]], [[hot-keys]], [[database-partitioning]] (*Note*: indicative, not confirmed by the readable part).

## Follow-up questions
The six deep dive titles.

## Variants
Not covered in the source.
