---
title: Redis sorted sets
type: concept
aliases: [zset, leaderboard, ranking]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 10 pp. 289-314, https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode]
---

# Redis sorted sets

## Definition
Redis structure that keeps members ordered by score; ideal for rankings.

## Why it matters
Avoids expensive DB queries and sorts for read-heavy leaderboards.

## How it works
`ZADD` when processing each submission/event; range reads in reverse order with scores (`ZRANGE ... REV WITHSCORES`; `ZREVRANGE` has been deprecated since Redis 6.2). Clients read the top ~1,000 and paginate.

## Variants and techniques
Alternatives: polling the DB (bad), cache refreshed every 30 s (stale). Refresh via 5 s polling instead of WebSockets; progressive polling near the end.

## Trade-offs
The source of truth remains the DB; Redis is a derived view.

## When to use it / when not to
Live rankings with refresh in seconds.

## Additional detail (Xu & Lam Vol. 2, ch. 10)
- Internal implementation: **hash table** (member -> score) + **skip list** (sorted base list with multi-level indexes that skip every other node; search ~ O(log n)). Commands: `ZADD`, `ZINCRBY` (O(log n)), `ZRANGE/ZREVRANGE` (O(log n + m)), `ZRANK/ZREVRANK` (O(log n)); a user's neighbors with `ZREVRANGE key rank-4 rank+4`.
- One sorted set per period (e.g. `leaderboard_feb_2021`); 25M entries of 26 B ~ 650 MB. Scaling to 100x: *fixed partition* by score range (rank = local + players with higher score in other shards) or Redis Cluster (16,384 slots, scatter-gather for the top k).
- Compared with SQL: computing the rank with `COUNT(*)` or sorting scans millions of rows (tens of seconds). See [[gaming-leaderboard]].

## Appears in
[[distributed-rate-limiter]], [[fb-post-search]], [[gaming-leaderboard]], [[leetcode]], [[online-chess]], [[strava]], [[top-k]]

## See also
[[caching]]
