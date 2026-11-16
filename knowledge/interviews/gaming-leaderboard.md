---
title: Real-time Gaming Leaderboard
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 10 Real-time Gaming Leaderboard, pp. 289-314]
concepts: [redis-sorted-sets, database-partitioning, caching, sql-vs-nosql, database-replication, hot-keys, message-queues]
difficulty: medium
---

# Real-time Gaming Leaderboard

## Prompt
Leaderboard for a mobile game: each month a tournament starts with a new ranking; players earn 1 point per match won.

## Functional requirements
- Show the top 10 players.
- Show the rank of a specific user.
- (Bonus) show the 4 players above and below a user.
- All players enter the ranking; monthly ranking; ties share a rank (tie-breaking optional).

## Non-functional requirements
- Real-time score updates (a batch history is not acceptable).
- Scalability, availability and reliability.

## Estimations
- 5 M DAU, 25 M MAU; 10 matches/player/day.
- 5M / 10^5 = ~50 users/s (peak x5 = 250).
- Scores: 50 x 10 = ~500 QPS; **peak 2,500 QPS**. Top 10: ~50 QPS (once when opening the game).
- Redis storage: 24 B id + 2 B score = 26 B x 25 M = **~650 MB** (x2 for skip list and hash overhead: fits in one Redis).

## API
- `POST /v1/scores` (user_id, points): **internal**, only called by the game servers (200 OK / 400).
- `GET /v1/scores`: top 10 (user_id, user_name, rank, score, total).
- `GET /v1/scores/{user_id}`: the user's rank and score.

## Data model
- Relational DB (simple solution): table `leaderboard(user_id, score)`; `UPDATE score = score + 1`; rank with `ORDER BY score DESC` (or COUNT subquery). With millions of rows the rank computation takes tens of seconds, cannot be cached (data changing continuously) and requires scanning the table; only suitable as batch.
- **Redis sorted set** (`leaderboard_feb_2021`): hash table (user -> score) + **skip list** (score -> user); insertion/search O(log n). Operations: `ZADD`, `ZINCRBY` (O(log n)), `ZRANGE/ZREVRANGE` (O(log n + m)), `ZRANK/ZREVRANK` (O(log n)). Each month a new sorted set; previous ones move to historical storage.
- Supporting MySQL tables: `user` (id, name, profile) and `point` (user_id, score, timestamp of each win; used for history and to rebuild Redis).

## Architecture (high-level design)
- **Game service** validates the win and calls the **Leaderboard service**, which updates the store; clients query the leaderboard service directly.
- Flows: win a point -> `ZINCRBY leaderboard_feb_2021 1 'mary1934'`; top 10 -> `ZREVRANGE leaderboard_feb_2021 0 9 WITHSCORES` (and user details from MySQL or a top-10 profile cache); rank -> `ZREVRANK`; relative -> `ZREVRANGE key 357 365` (rank 361 +/-4).
- Decisions: the **score is set by the server** (if set by the client: man-in-the-middle); in server-authoritative games the game server already knows the end of the match. No message queue is used (not required); if scores feed other consumers (analytics, notifications, turn-based multiplayer) Kafka would be placed between the game service and the leaderboard service.
- Redis persistence: it supports persistence but restarting a large instance is slow; a read replica is used and promoted on failure.

## Deep dives
**Cloud vs self-hosted**: self-managed (API servers + Redis + MySQL + top-10 profile cache) or serverless on AWS: **API Gateway + Lambda** (`LeaderboardFetchTop10`, `LeaderboardFetchPlayerRank`, `LeaderboardUpdateScore`) with Redis and MySQL; automatic scaling, recommended if building from scratch.

**Scaling Redis** (example 500 M DAU = x100: 65 GB and 250,000 QPS):
- *Fixed partition* (by score range, e.g. 10 shards of 100 points): requires uniform distribution (or adjusting ranges), sharding in the application and a secondary cache user_id -> score to know the shard; when moving up a range the user is moved between shards. Top 10 = from the highest shard; rank = local rank + number of players with a higher score in the other shards (`INFO keyspace` O(1)). Chosen.
- *Hash partition* with **Redis Cluster** (16,384 hash slots, CRC16(key) % 16384; add/remove nodes without redistributing everything): top 10 with **scatter-gather** (top 10 from each shard and sort in the app); drawbacks: latency with large k or many partitions (waits for the slowest) and it does not easily give a user's rank.
- *Node sizing*: write-heavy workloads need double the memory (snapshots); use `redis-benchmark`.

**NoSQL alternative (DynamoDB)**: optimized for writes and ordering by score within the partition. Denormalized table (user_id, score, email, profile_pic, leaderboard_name). **Global secondary index** with partition key `game#year-month` and sort key `score`; problem: the whole partition of the hot month -> **write sharding**: `game#year-month#p{user_id % n}`; top 10 with scatter-gather. The number of partitions requires benchmarking (load per partition vs read complexity). Exact rank is hard: approximate with **percentiles** (cron that computes the score distribution per shard and caches it, e.g. "top 10-20%").

**Extras**: Redis Hash to map user_id -> user object (fast read) and for **tie-breaking** (timestamp of the last win; the oldest wins); **failure recovery**: script that walks the `point` table and redoes the `ZINCRBY`s.

## Trade-offs and decisions
- Redis sorted set (O(log n), memory) versus SQL (scan/sort) and NoSQL (write sharding, approximate rank).
- Fixed partition (computable rank, requires even distribution) vs hash/Redis Cluster (automatic distribution, scatter-gather).
- Serverless vs own servers.
- Redis as a derived view that can be rebuilt from MySQL.

## Related concepts
[[redis-sorted-sets]], [[database-partitioning]], [[caching]], [[sql-vs-nosql]], [[database-replication]], [[hot-keys]], [[message-queues]]

## Follow-up questions
- Show 4 players above/below a user.
- Tie-breaking.
- Scale to 100x users.
- Recovery from a massive Redis failure.

## Variants
Not covered in the source (see [[leetcode]] for a leaderboard with Redis sorted sets in another context).
