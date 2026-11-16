---
title: FB News Feed
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, System Design Interview Vol.1 (Alex Xu) ch. 11, Grokking the System Design Interview (PDF), newsfeed (chapter with truncated title) pp. 128-136, Designing Data-Intensive Applications (Kleppmann), chs. 1 and 12]
concepts: [fan-out, caching, hot-keys, message-queues, database-indexing, cdn-edge-computing, rate-limiting, scalability-reliability-maintainability, derived-data-and-dataflow]
difficulty: medium
---

# FB News Feed

## Prompt
A feed of recent posts from a user's social network. Focus on fan-out and data management. One-directional "follow" relationship; users already authenticated.

## Functional requirements
- Create posts; follow users; view feed (most recent first); paginate it.
- Out of scope: likes/comments, private posts.

## Non-functional requirements
- High availability (takes priority over consistency; ~1 min of staleness tolerated).
- Posting and viewing the feed < 500 ms.
- ~2B users; unlimited follows/followers.

## Estimations
- Post ID ~10 B; 200 posts per user = ~2 KB; 2B users -> ~4 TB of precomputed feeds (reasonable).

## API
- `POST /posts` {content} -> postId.
- `PUT /users/{id}/follow` (idempotent).
- `GET /feed?pageSize&cursor` -> items + nextCursor (cursor = timestamp of the oldest post seen).

## Data model
- **Post** (DynamoDB) with GSI `creatorID` + `createdAt`.
- **Follow**: PK `userFollowing`, SK `userFollowed`; inverse GSI for followers.
- **PrecomputedFeed**: key `userId`, list of up to ~200 postIds in reverse chronological order.

## Architecture (high-level design)
API gateway + LB; stateless Post Service and Following Service; Feed Service. Naive version: followed users -> posts via GSI -> sort (does not scale: many followed users, many posts).

## Deep dives
1. **Many followed users** -> move from fan-out on read to [[fan-out]] on write with precomputed feeds (cap ~200). Anyone paginating beyond that falls back to the naive path. Product lever: a 5,000-friend limit.
2. **Many followers**: bad = the Post Service writes to all feeds (connection limits, latency, uneven load); good = asynchronous workers behind a queue ([[message-queues]], SQS at-least-once; very large tasks must be chunked); great = **hybrid feeds**: accounts with many followers are flagged as not precomputed and merged at read time.
3. **Uneven reads (hot keys)**: good = distributed Redis cache by postId (the hot key repeats on the shard); great = cache replicated N times with an LB ([[hot-keys]]): ~N times more throughput for a viral post, at the cost of more misses and less unique capacity.

## Trade-offs and decisions
- Write amplification vs cheap reads; hybrid adds compute on read (adjustable threshold).
- Separate tables for clarity (AWS recommends single-table in DynamoDB).

## Related concepts
[[fan-out]], [[hot-keys]], [[message-queues]], [[caching]], [[database-indexing]]

## Follow-up questions
No list; expectations: mid = API/data/HLD; senior = >=2 deep dives with fan-out; staff = all of them plus tuning.

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 11, pp. 166-177**: news feed in reverse chronological order, web + mobile, up to 5,000 friends, 10M DAU, with images and videos.
  - API: `POST /v1/me/feed` (content, auth_token) and `GET /v1/me/feed`.
  - Two flows. **Publishing**: web servers (authentication and [[rate-limiting]]) -> Post service (DB + cache) -> Fanout service -> Notification service. **Building**: web server -> Newsfeed service -> Newsfeed cache -> hydrate with user cache and post cache -> JSON; media goes through [[cdn-edge-computing]].
  - **Fanout** ([[fan-out]]): on write (push; precomputed feed, fast read; hot key problem with many friends, waste with inactive users) vs on read (pull; no hot key, slow read). **Hybrid**: push for most and pull for celebrities; consistent hashing to distribute.
  - Fanout service: friend IDs from a graph database, filter with the user's settings (mute, selective sharing) from the user cache, send to a message queue, workers store `<post_id, user_id>` in the news feed cache (IDs only, configurable limit because almost nobody scrolls through thousands of posts).
  - **5-layer cache architecture**: News Feed (IDs), Content (posts; hot cache for popular ones), Social Graph, Action (likes, replies), Counters (likes, replies, followers, following).
  - Wrap-up: DB scaling (vertical/horizontal, SQL/NoSQL, replication, read replicas, consistency, sharding), stateless web tier, multi data center, queues, metrics (peak QPS, refresh latency).
  - Differs from the base: explicit layered cache and graph database; no cursor pagination or hot key detail beyond the hybrid.

See [[instagram]] (similar chronological feed).

- **Grokking the System Design Interview (PDF), pp. 128-136** (difficulty Hard): Facebook newsfeed with friends, pages and groups.
  - Requirements: feed based on what is followed; images/video/text; add new posts for active users; maximum latency 2 s.
  - Estimations: 300 M users, 5 feed loads/day = 1.5 B/day ≈ 17,500 req/s; 500 posts x 1 KB = 500 KB per user x 300 M = 150 TB in memory ≈ 1,500 machines of 100 GB.
  - API `getUserFeed(api_dev_key, user_id, since_id, count, max_id, exclude_replies)`; entities User, Entity (page/group), FeedItem, FeedMedia.
  - Generation: on-the-fly querying is slow (sorting/merging/ranking, backlogs on updates) -> **offline generation** with dedicated servers that keep in memory (hash/LinkedHashMap of FeedItemIDs; about 500 per user, adjustable to 200) since the last generation; only for active users (LRU or login pattern).
  - Publishing: fan-out on load (pull) vs fan-out on write (push, problem with celebrities) vs **hybrid** (no fan-out for celebrities; option: only online friends). Limit on items per request (~20) chosen by the client; notification of new items (avoid on mobile because of data usage).
  - Ranking by features (likes, comments, shares, time, media) and continuous improvement with retention metrics; sharding of posts as in [[twitter]] and of feed by UserID with consistent hashing.

- **Designing Data-Intensive Applications (Kleppmann), ch. 1 (Twitter 2012 case)**: an example of how to describe load and choose fan-out.
  - Load: 4.6k tweets/s on average (peak >12k) and 300k home timeline reads/s; average of ~75 followers per tweet -> ~345k writes/s to timelines; some users with >30M followers (delivery target < 5 s).
  - Approach 1 (pull): tweets in a global table and a join with follows on read (Twitter's first version; it could not keep up with reads). Approach 2 (push): per-user timeline cache updated on posting. Final: **hybrid** (celebrities excluded from fan-out and merged at read time).
  - Differs from the base: no DynamoDB or queue detail; contributes the reasoning with *load parameters* and the view of the timeline as a materialized view maintained by stream processing ([[scalability-reliability-maintainability]], [[derived-data-and-dataflow]], [[fan-out]]).
