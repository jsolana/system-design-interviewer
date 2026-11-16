---
title: Top K (YouTube Top K Videos)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k]
concepts: [stream-processing, count-min-sketch, caching, redis-sorted-sets, database-partitioning, database-indexing]
difficulty: high
---

# Top K (YouTube Top K Videos)

## Prompt
Ingest a firehose of view events (VideoIDs) and accurately answer "top K most viewed videos" for the last hour, day, month and all-time.

## Functional requirements
- Top K all-time (max K 1k) and over tumbling windows of 1 h, 1 day, 1 month and all-time.
- Out of scope: arbitrary ranges and arbitrary start/end points.
- Tumbling windows (not sliding) for simplicity, agreed with the interviewer; K capped at 1k so results are not unbounded.

## Non-functional requirements
- Maximum delay of 1 min between a view and its being counted.
- Accurate results (approximation comes in as a deep dive).
- Responses in tens of ms (precomputation and cache).
- Huge volume of views/s and of videos.

## Estimations
- Shorts: 70B views/day / 100k s ≈ **700k writes/s**.
- ~1 h of content uploaded per second; ~6 min/video -> ~1M videos/day; 10 years ≈ 3.6B (~4B).
- Naive table: 4B x (8 B id + 8 B counter) ≈ **64 GB**.

## API
`GET /views/top-k?window={WINDOW}&k={K}` -> `[{videoId, views}]` (no pagination because of the K cap).

## Data model
- **VideoViews** (videoId, views, timestamp by hour), with an index on views and timestamp.
- **VideoViewsLastHour/LastDay/LastMonth**: per-window aggregates indexed by views (deep dive 3).
- Sorted list/heap of top-1000 per window (deep dive 5). Entities: Video, View, Time Window.

## Architecture (high-level design)
- All-time: events in Kafka topic `ViewEvent` (partitioned by videoId) -> consumer increments counter in Postgres -> top-K service behind LB with `ORDER BY views DESC LIMIT k` over an index (O(k) cost on read; each write updates the index).
- Windows: hourly timestamp column, one row per video and active hour; `SUM(views) GROUP BY videoId` with a time filter (writes proportional to views, reads with scans).

## Deep dives
1. **Reduce DB queries**: good = top K cache per window (`top-k:{window}:{truncated timestamp}`, TTL of hours; on expiry, a stampede hits the DB, request coalescing does not fix latency); great = cron that precomputes and warms the cache before it expires, keeping old entries in case the job is delayed.
2. **Massive writes** ([[stream-processing]]): shard by videoId (top K = merge of each shard's top K, globally correct; 70 shards for 700k TPS is too many); batching with Flink (1 h tumbling windows, BoundedOutOfOrderness watermarks ~30 s, checkpoints and Kafka offset rewind; reduces volume 2-100x -> ~5-10 shards).
3. **Optimize queries with windows**: good = coarser granularity (hourly and daily, summing days for the month; more staleness); great = aggregate tables per window indexed by views (4 writes instead of 1; mitigate with unlogged tables, deferred fsync, batch tuning); great with caveats = in-memory aggregation in Flink (RocksDB, rolling aggregator + top-K heap, write to Redis sorted sets every minute; requires deep Flink knowledge).
4. **Sliding windows**: increment with the latest minute and decrement the one from 60 min ago (all-time never decrements); requires minute-level data for a month. Alternatives: sliding only for the last hour and tumbling for day/month; or a second consumer group that decrements with lag (a month+ of Kafka retention). Native Flink sliding with a 1 min slide multiplies memory by 43,200.
5. **Approximation** ([[count-min-sketch]]): hundreds of MB versus ~100 GB. Good = Redis (CMS.INCRBY/QUERY + ZADD to a sorted set trimmed to 1000; durability and divergence risk); great = state in Flink with checkpoints and replay from Kafka. CMS only allows decrementing what was added.
6. **Specialized DBs**: bad = InfluxDB/Prometheus (cardinality of billions of series); good = TimescaleDB (hypertables, continuous aggregates; still needs cache and sharding); good = real-time OLAP (Druid, Pinot, ClickHouse with ingestion-time pre-aggregation; operational fragility). High cardinality is the central challenge.

## Trade-offs and decisions
- Accuracy vs memory (CMS); freshness vs cost (Flink batching, cron).
- More writes in exchange for O(k) reads.
- Master simple primitives before specialized tools.

## Related concepts
[[stream-processing]], [[count-min-sketch]], [[caching]], [[redis-sorted-sets]], [[database-partitioning]], [[database-indexing]]

## Follow-up questions
Billions of videos; late events beyond the minute; sliding windows; approximation and CMS durability; cron failure or cold cache; shard and merge of top K; replacing with a TSDB/OLAP.

## Variants
Not covered in the source.
