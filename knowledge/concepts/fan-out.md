---
title: Fan-out (on read / on write / hybrid)
type: concept
aliases: [fan-out on write, fan-out on read, precomputed feeds, push vs pull]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, System Design Interview Vol.1 (Alex Xu), ch. 11, Designing Data-Intensive Applications (Kleppmann), ch. 1]
---

# Fan-out

## Definition
How an event (a post) is distributed to many recipients (followers' feeds): at read time (pull) or at write time (push).

## Why it matters
Determines read latency, write cost and storage in feeds, notifications and similar systems.

## How it works
- **Fan-out on read**: when the feed is requested, the followed accounts and their posts are queried and sorted. Slow with many followed accounts.
- **Fan-out on write**: on publishing, the post is prepended to precomputed feeds (table `userId -> list of postIds`, cap ~200).
- For accounts with millions of followers: asynchronous workers behind a queue, with chunked tasks.

## Variants and techniques
**Hybrid**: highly followed accounts are not precomputed and are merged at read time with the precomputed feed; adjustable threshold. Fallback to the naive path for deep pagination. Product limits (friend cap).

## Trade-offs
Push: fast reads, amplified writes and extra storage (~4 TB for 2B users x 200 posts). Pull: simple but slow. Hybrid: more complexity and compute at read time.

## When to use it / when not to
Push for read-heavy with bounded followers; pull/hybrid for celebrities.

## Additional detail (Xu Vol. 1, ch. 11)
Fanout on write (push: precomputed feed, fast read, but a hot key with many friends and waste with inactive users) vs fanout on read (pull: no hot key, slow read). Hybrid: push for the majority and pull for celebrities/users with many followers; consistent hashing helps distribute load. Pipeline: friend IDs (graph DB) -> filter by settings (mute) -> queue -> workers -> news feed cache of `<post_id, user_id>` (IDs only, with a configurable limit). See [[fb-news-feed]].

## Additional detail (DDIA, ch. 1)
- **Twitter case (2012)**: 4.6k tweets/s (peak 12k) vs 300k timeline reads/s. A tweet reaches ~75 followers on average (345k writes/s to the timeline caches), but there are accounts with >30M followers (30M writes per tweet; delivery target < 5 s). They moved from a pull approach (SQL join of tweets/follows) to push (per-user timeline cache) and finally to a **hybrid**: push for the majority; celebrities are excluded from the fan-out and merged at read time. Idea: the distribution of followers is the key *load parameter* ([[scalability-reliability-maintainability]]).
- Dataflow view: the timeline is a **materialized view** maintained by a stream processor (join of tweet and follow events) ([[derived-data-and-dataflow]]).

## Appears in
[[fb-news-feed]], [[instagram]], [[twitter]]

## See also
[[message-queues]], [[hot-keys]], [[caching]]
