---
title: FB Post Search
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search]
concepts: [inverted-index, caching, cdn-edge-computing, count-min-sketch, message-queues, database-partitioning, redis-sorted-sets, full-text-search]
difficulty: high
---

# FB Post Search

## Prompt
Keyword search over Facebook posts. The interviewer forbids ready-made search engines and full-text indexes (Elasticsearch, Postgres full-text): the index must be designed from scratch.

## Functional requirements
- Create and like posts; search by keyword; sort by recency or by likes.
- Out of scope: fuzzy/semantic search, personalization, privacy, advanced ranking, media, live updating of the search page.

## Non-functional requirements
- Median latency < 500 ms; high request volume.
- New posts searchable in ~1 min.
- Old/unpopular posts remain discoverable (more latency tolerated).
- High availability.

## Estimations
Assumptions: 1B users, 100k s/day.
- Posts: ~10k/s; likes: ~100k/s; searches: ~10k/s (bursts 10x+).
- Storage: 1B posts/day x 365 x 10 years ≈ 3.6T posts x 1 KB ≈ 3.6 PB.
- Conclusion: a write-heavy system with storage that must be bounded.

## API
Endpoints for create post, like and search (could be consumed from Kafka). No schemas in the source.

## Data model
No schema; entities User, Post, Like (as a counter). The design is expressed in Redis structures.

## Architecture (high-level design)
- Write: existing Post Service and Like Service; an Ingestion Service writes to the DB.
- Search: API gateway -> scaled Search Service -> index. `LIKE '%kw%'` without an index (bad: sharding/replication only divide by a constant). **[[inverted-index]]** keyword -> postIds in Redis (excellent); challenges: huge lists for common words, 10-1,000 writes per post, durability (MemoryDB).
- Sorting: at query time (bad: hundreds of MB and millions of lookups); **two indexes** (excellent): a Redis list by creation (read from the end) and [[redis-sorted-sets]] by likes; cost: double storage and many score updates.

## Deep dives
1. **High request volume** ([[caching]]): without personalization, the same queries = the same results and 1 min of staleness is acceptable. Good = distributed cache with TTL < 1 min; excellent = CDN with `Cache-Control` ([[cdn-edge-computing]]).
2. **Multi-keyword and phrases**: good = intersection + exact-phrase filter (expensive, hard within 500 ms); excellent = index **bigrams/shingles** (from ~10M keys to 100M+); mitigate by indexing only likely bigrams, falling back to intersection, and using [[count-min-sketch]] for frequencies.
3. **High write volume**: posts -> Kafka to partition/absorb bursts ([[message-queues]]), indexes sharded by keyword across many Redis instances ([[database-partitioning]]). Likes: good = batching per post (~30 s; helps viral posts, little for the rest); excellent = **two stages**: update the index only at milestones (powers of 2 or 10; ~10 writes instead of 1,000), an approximate/stale index and, at query time, fetch the top 2N candidates, ask the Like Service for fresh counts and re-sort (rename the field, e.g. "approxLikes"). *Note*: the source text mentions Elasticsearch here, contradicting the constraint.
4. **Storage**: limit each inverted index to ~1k-10k entries; a batch job driven by search analytics that moves rarely searched keywords from Redis to blob storage (S3/R2) with a fallback and somewhat more latency.

## Trade-offs and decisions
- Redis is fast but expensive and has a durability challenge; cold storage for the long tail.
- Approximate likes: fewer writes in exchange for re-sorting with fresh data and more complexity.
- Bigrams: fast phrase reads versus index explosion.

## Related concepts
[[inverted-index]], [[full-text-search]], [[caching]], [[cdn-edge-computing]], [[count-min-sketch]], [[message-queues]], [[database-partitioning]], [[redis-sorted-sets]]

## Follow-up questions
Eviction policy and TTL vs the 1 min SLA; Redis durability and failover; hot keywords; huge lists; bigram growth and selection; accuracy of approximate likes; cold-to-hot promotion; visibility of new posts within 1 min.

## Variants
Not covered in the source.
