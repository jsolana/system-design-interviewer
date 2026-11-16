---
title: Count-Min Sketch
type: concept
aliases: [CMS, sketch, approximate counting]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k]
---

# Count-Min Sketch

## Definition
A probabilistic data structure that estimates element frequencies using a 2D array of counters and several hash functions.

## Why it matters
Hundreds of MB of memory versus ~100 GB of exact counters for billions of videos.

## How it works
Each element increments one counter per row (a different hash each); the estimate is the minimum. It is combined with a sorted list or heap of the top 1000 to obtain top K (skip ZADD if the count is below the minimum).

## Variants and techniques
- Redis: CMS.INCRBY, CMS.QUERY + ZADD to a trimmed sorted set; risk of durability loss and sketch/sorted set divergence.
- Flink: sketch and list kept in state with checkpoints, recovery by Kafka replay.
- Decrement is allowed only for what was already added (sliding windows).

## Trade-offs
Approximate results (overestimates) in exchange for memory; complex to operate.

## When to use it / when not to
When exact accuracy is not mandatory and cardinality is huge.

## Appears in
[[fb-post-search]], [[top-k]]

## See also
[[stream-processing]], [[redis-sorted-sets]], [[bloom-filter]]
