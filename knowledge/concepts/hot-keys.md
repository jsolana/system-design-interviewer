---
title: Hot keys / hot partitions
type: concept
aliases: [hot spots, replicated cache, celebrity problem]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, Designing Data-Intensive Applications (Kleppmann), ch. 6]
---

# Hot keys

## Definition
Keys or partitions that receive a disproportionate fraction of traffic (e.g. a viral post), saturating a node.

## Why it matters
DynamoDB-style DBs perform best with uniform distribution; a cache sharded by key just moves the problem to the cache shard.

## How it works
- Distributed cache (Redis) sharded by id, long TTL and LRU, invalidation on edit: the hot key persists on one shard.
- **Replicated cache**: N instances that serve any key, with an LB in front and no coordination: viral-post load is spread out (~N x throughput).

## Variants and techniques
Cache replication, partitioning with suffixes (not covered in the source).

## Trade-offs
Replicating -> more initial misses (up to ~N DB reads per viral post) and less unique capacity, because popular content is duplicated.

## When to use it / when not to
Content with viral spikes and highly uneven reads.

## Additional detail (DDIA, ch. 6)
- Write technique (DDIA): for a known hot key, add a random suffix (e.g. 2 digits = 100 keys) to spread the writes across partitions; reads must query all N keys and combine them, so it only applies to the few hot keys and requires tracking which ones they are. Hashing the key does not fix a single hot key ([[database-partitioning]]).

## Appears in
[[ad-click-aggregator]], [[distributed-cache]], [[distributed-rate-limiter]], [[fb-news-feed]], [[gaming-leaderboard]]

## See also
[[caching]], [[fan-out]], [[database-partitioning]]
