---
title: Instagram
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram, Grokking the System Design Interview (PDF), "Designing Instagram" pp. 38-47, Machine Learning Design Interview (Khang Pham, 2022), ch. 3 pp. 136-139]
concepts: [caching, cdn-edge-computing, fan-out, recommendation-system-pipeline, embeddings, exploration-exploitation, approximate-nearest-neighbor-search]
difficulty: medium
---

# Instagram

> Note: mostly paywalled page (Premium). Only the statement, requirements and deep dive titles were readable.

## Prompt
A visual content platform where users share photos and videos with their followers.

## Functional requirements
- Create posts with photos, videos and a caption.
- Follow other users.
- View a chronological feed of the people they follow.
- Out of scope: likes/comments, search, stories, live.

## Non-functional requirements
- Feed with latency < 500 ms; instant rendering of photos (up to 8 MB) and videos (up to 4 GB); 500M DAU. Full list not visible.

## Estimations
500M DAU; 100M posts/day. No further calculations visible.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source (only three flows reflecting the requirements).

## Deep dives
Titles only: low-latency feed; instant photo/video rendering; scale to 500M DAU. The source tags patterns: Scaling Reads, Managing Long Running Tasks, Handling Large Blobs, and mentions overlap with FB News Feed and Dropbox.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[cdn-edge-computing]], [[caching]] (*Note*: indicative). See [[fb-news-feed]] and [[dropbox]].

## Follow-up questions
Not covered in the source.

## Variants
- **Grokking the System Design Interview (PDF), pp. 38-47** (difficulty Medium): simplified version focused on upload, follow, search by title and a News Feed with the best photos from followed users.
  - NFR: high availability, feed latency 200 ms, consistency can be sacrificed, total reliability (photos are never lost).
  - Estimations: 2 M photos/day (23/s) x 200 KB = 400 GB/day -> ~1.425 TB in 10 years; metadata: User 68 B x 500 M = 32 GB, Photo 284 B (0.5 GB/day; 1.88 TB in 10 years), UserFollow 8 B x 500 M x 500 = 1.82 TB; total ~3.7 TB.
  - Storage: photos in HDFS/S3; metadata in a key-value/wide-column store (Cassandra) with replicas (a minimum number of live replicas is maintained; deferred deletion so it can be undone).
  - Separate read and write services because slow uploads exhaust the web server's connections.
  - Sharding by UserID (hot users, uneven distribution, ID = shard + local sequence) vs by PhotoID (dedicated DB generating 64-bit IDs, two even/odd instances behind an LB). **PhotoID = epoch (31 bits for 50 years) + sequence (9 bits, reset every second)**; shard = PhotoID % 10. Many logical partitions mapped to few physical servers with a configuration file to migrate them.
  - Feed: computing on the fly (latest 100 photos from each followed user + ranking) is slow -> pre-generate in a `UserNewsFeed` table with dedicated incremental servers; delivery pull / push (long poll) / hybrid (push for few followers, pull for celebrities). See [[fan-out]].
  - Cache: CDN and geographic photo caches; Memcache for metadata with LRU; 80-20 rule.

- **Machine Learning Design Interview (Khang Pham), ch. 3 pp. 136-139 - recommending content from non-friends (Explore)**: recommend accounts/media outside the user's network based on interests (e.g., a user who likes a van-life magazine); different from pure cold start.
  - Metrics: high recall for candidate generation, CTR for ranking, follow rate of new accounts.
  - Candidate retrieval: identify **seeds** (authors/media with clear interest) and expand them with kNN pipelines giving similar media/authors; similarity by embeddings (user embeddings trained word2vec-style from engagement sessions) and by **co-occurrence** (count pairs of co-engaged media, aggregate, take top N per seed). See [[embeddings]], [[approximate-nearest-neighbor-search]].
  - Data: sessions with positive (like, comment, save) and negative signals ("not interested", "see fewer"); features on engagement, author-viewer interaction, counters/trends, content quality, image/video understanding, content taxonomy.
  - Models: two-tower and gradient boosted trees. Ranking value: `Value(post) = P(like)^w_like * (1 - P(not_interested))^w_see_less`.
  - Cold start: fallback graph exploration (accounts followed by accounts the user liked as seeds, one-hop and two-hop), popular media for brand-new users, adapting as responses arrive ([[exploration-exploitation]]).
  - Differs from the base: ML recommendation, not upload/storage/feed fan-out.
