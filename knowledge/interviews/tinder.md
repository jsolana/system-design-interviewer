---
title: Tinder
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder]
concepts: [geospatial-indexing, bloom-filter, caching, change-data-capture, full-text-search, database-partitioning]
difficulty: medium
---

# Tinder

## Prompt
Mobile dating app: swipe right (like) / left (pass), suggestions by location and filters, notification of a mutual match. Focus on the feed and swipes.

## Functional requirements
- Profile with preferences (age range, interests, maximum distance).
- View a stack of candidates matching preferences/distance.
- Swipe yes/no one by one.
- Match notification when there is a mutual "yes".
- Out of scope: photos, DMs, premium.

## Non-functional requirements
- Strong consistency on swipes (if both say yes, the match must be detected).
- 20M DAU, ~100 swipes/user/day.
- Feed < 300 ms.
- Do not repeat profiles already seen.
- Out of scope: fake profiles, monitoring.

## Estimations
20M x 100 x 100 B ≈ 200 GB/day of swipes (~2B swipes/day). *Note*: the source also cites 4B/day (200 swipes/user), inconsistent with the rest.

## API
- `POST /profile` (age_min, age_max, distance, interestedIn).
- `GET /feed?lat&long&distance` -> User[] (no pagination; the client re-requests when the stack runs out).
- `POST /swipe/{userId}` {decision}. Identity comes from the token/JWT.

## Data model
- Profile/User (age range, interestedIn, distance, lat/long, interests).
- **Swipe** in Cassandra; HLD partitioned by `swiping_user_id`; in the deep dive, partition key = ordered pair `smaller:larger` with from_user, to_user, direction, created_at.
- Match: not detailed.

## Architecture (high-level design)
Client -> API Gateway -> Profile Service (+ Profile DB) and Swipe Service (+ Swipe DB Cassandra) + external push (APNS/FCM). Initial feed: SQL by age/interests/bounding box (inefficient; requires a geospatial index). Swipe: write and check for the reverse swipe; the second swiper sees the match in the app and the first receives a push. Swipe and Profile are separated because of the large difference in write volume.

## Deep dives
1. **Consistent and fast swipes** (race: A and B both say yes at the same time and each check does not see the other). Bad = DB polling; good = transactions (Cassandra LWT/Paxos only within a partition, slow); great = Cassandra with pair partitioning and batch; great = Redis with hash by ordered pair (`swipes:a:b`) and an atomic Lua script, consistent hashing, Cassandra as the durable store (losing Redis only loses recent detection). Alternative: eventual reconciliation (but the last swiper needs immediate notice).
2. **Low-latency feed** ([[geospatial-indexing]]): indexed DB or search engine (Elasticsearch/OpenSearch) synchronized via [[change-data-capture]] with batched writes; or precomputation + [[caching]]; optimal = combine: serve precomputed and refresh from the index when few profiles remain. Freshness: TTL < 1 h, recompute only for active users, refresh on filter/location change.
3. **Avoid repeats**: bad = query swipes and filter (lagging replicas, large history); great = the client stores the K most recent swipes + cache/query; great = per-user [[bloom-filter]] in cache (no false negatives; false positives hide valid profiles; costly rebuild after a crash).

## Trade-offs and decisions
- Strong consistency on swipes vs Redis complexity (failover, rebalancing).
- Cassandra partitions grow and get hot -> archiving.
- Feed freshness vs precomputation cost.

## Related concepts
[[geospatial-indexing]], [[bloom-filter]], [[caching]], [[change-data-capture]], [[database-partitioning]], [[full-text-search]]

## Follow-up questions
Consistency vs availability (reconciliation), partition growth/archiving, Redis failover, index sync, Bloom filter size, feed TTL.

## Variants
Not covered in the source.
