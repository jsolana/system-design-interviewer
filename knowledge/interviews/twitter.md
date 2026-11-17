---
title: Twitter
type: interview
sources: [Grokking the System Design Interview (PDF), "Designing Twitter" pp. 72-81]
concepts: [database-partitioning, unique-id-generation, consistent-hashing, caching, replication, load-balancer, fan-out, sql-vs-nosql]
difficulty: medium
---

# Twitter

## Prompt
A Twitter-style social network where users post tweets, follow others and mark favorites. Difficulty in the source: Medium.

## Functional requirements
1. Post tweets. 2. Follow users. 3. Mark favorites. 4. Timeline with the top tweets from followed users. 5. Tweets with photos and videos.
- Extended: search, replies, trending topics, mentioning users, notifications, who to follow, Moments.

## Non-functional requirements
- High availability; acceptable latency of 200 ms to generate the timeline.
- Consistency can be sacrificed (if a user takes a while to see a tweet, it does not matter).

## Estimations
- 1,000 M users, 200 M DAU, 100 M tweets/day (~1,150/s), 200 followed on average; 5 favorites/user/day -> 1 B favorites/day.
- Views: 200 M DAU x ((2 + 5) visits x 20 tweets) ≈ 28 B tweet-views/day ≈ 325 K reads/s (peak ~1M/s, peak writes of a few thousand/s). Very read-heavy system.
- Text storage: 100 M x (280 + 30 B of metadata) ≈ 30 GB/day. Media: 1 in 5 tweets with a photo (200 KB), 1 in 10 with a video (2 MB) -> ≈ 24 TB/day.
- Ingress ≈ 290 MB/s; egress ≈ 35 GB/s (93 MB/s text + 13 GB/s photos + 22 GB/s video).

## API
`tweet(api_dev_key, tweet_data, tweet_location, user_location, media_ids)` -> tweet URL or HTTP error (media is uploaded separately).

## Data model
Entities: User, Tweet (ID, content, location, likes, timestamp), UserFollow, FavoriteTweets. SQL vs NoSQL: see [[sql-vs-nosql]] (refers to Instagram). Photos/videos in distributed file storage.

## Architecture (high-level design)
Multiple app servers behind an LB, a DB optimized for many reads, file storage for media, cache and aggregation servers to generate the timeline.

## Deep dives
- **Sharding**:
  - By UserID: hot users and uneven distribution -> spread them or [[consistent-hashing]].
  - By TweetID: solves hot users but the timeline requires querying all partitions (app server -> all DBs -> each sorts by recency -> merge and re-sort).
  - By creation date: fast reads of recent data, but all writes go to one server and the most recent one concentrates the load.
  - **Combined**: TweetID with timestamp: epoch seconds (31 bits for 50 years) + auto-incrementing sequence (17 bits at ~1,150 tweets/s; 2^17 ≈ 130 K/s) = 48 bits (the sequence resets every second). With 64 bits, 100 years and milliseconds are reached. Two key-generating DBs (even/odd) for fault tolerance. See [[unique-id-generation]]. All shards still need to be queried for the timeline, but without a secondary index by date (lower write latency) and with a primary key that already includes the epoch.
- **Cache**: Memcache with LRU; 80-20 rule (cache 20% of daily reads per shard). Alternative: cache the tweets of the last 3 days (< 100 GB, replicated), with a doubly linked list per user (new ones at the head, eviction from the tail).
- **Timeline**: see [[fb-news-feed]] (offline generation and fan-out) and [[instagram]].
- **Replication**: read-only secondary replicas per partition; writes to the primary; failover.
- **LB**: three layers (client-app, app-DB replicas, aggregation-cache), Round Robin initially.
- **Monitoring**: new tweets/day and peak, timeline deliveries, average refresh latency.
- **Extended**: retweet (store the original tweet's ID, no content); trending topics (most frequent hashtags/queries in the last N seconds, refreshed every M; more weight if more people see it); who to follow (friends of followed users, 2-3 levels, prefer celebrities, re-rank with ML); Moments (news from 1-2 h, categorize with supervised ML or clustering); search -> [[twitter-search]].

## Trade-offs and decisions
Shard by UserID (local query, hot users) vs TweetID (distribution, read fan-out) vs combined with a time-based ID; availability > consistency.

## Related concepts
[[database-partitioning]], [[unique-id-generation]], [[consistent-hashing]], [[caching]], [[replication]], [[load-balancer]], [[fan-out]], [[sql-vs-nosql]]

## Follow-up questions
Handling hot users; how to serve feeds (merge/sort by time, pagination, top N, pre-generation).

## Variants
Not covered in the source.
