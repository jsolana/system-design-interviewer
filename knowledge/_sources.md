# Processed sources

## Hello Interview - Problem Breakdowns
Index: https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview (the URL with a trailing slash returned 404; the index was read at `/overview`, 32 breakdowns). Accessed: 2026-11-16.

Base URL of each breakdown: https://www.hellointerview.com/learn/system-design/problem-breakdowns/{slug}

### Fully processed (readable content)
- bitly -> interviews/url-shortener.md
- ticketmaster -> interviews/ticketmaster.md
- dropbox -> interviews/dropbox.md
- gopuff -> interviews/gopuff.md
- fb-news-feed -> interviews/fb-news-feed.md
- tinder -> interviews/tinder.md
- leetcode -> interviews/leetcode.md
- whatsapp -> interviews/whatsapp.md
- distributed-rate-limiter -> interviews/distributed-rate-limiter.md
- youtube -> interviews/youtube.md
- fb-live-comments -> interviews/fb-live-comments.md
- top-k -> interviews/top-k.md
- uber -> interviews/uber.md
- web-crawler -> interviews/web-crawler.md
- ad-click-aggregator -> interviews/ad-click-aggregator.md
- fb-post-search -> interviews/fb-post-search.md

### Partially processed (Premium paywall; only the problem statement, requirements and deep dive titles; the rest marked "Not covered in the source")
yelp, instagram, strava, distributed-cache, online-auction, job-scheduler, google-news, camelcamelcamel, notification-system, robinhood, google-docs, payment-system, metrics-monitoring, online-chess, chatgpt, flash-sale -> interviews/{slug}.md

### Concepts created (this pass)
presigned-urls, chunked-multipart-upload, database-partitioning, fan-out, hot-keys, message-queues, geospatial-indexing, bloom-filter, sandboxed-code-execution, redis-sorted-sets, websockets, pub-sub, consistent-hashing, rate-limiting, adaptive-bitrate-streaming, workflow-orchestration, cursor-pagination, stream-processing, count-min-sketch, olap-columnar-stores, inverted-index.
Earlier concepts (Bitly/Ticketmaster): unique-id-generation, base62-encoding, http-redirects, database-indexing, caching, cdn-edge-computing, distributed-lock, optimistic-concurrency-control, server-sent-events, virtual-waiting-queue, full-text-search, change-data-capture, idempotency.

### Expanded concepts
caching, cdn-edge-computing, http-redirects, idempotency, database-indexing (Appears in and sources), distributed-lock (Uber, Gopuff), server-sent-events (Live Comments), full-text-search (variant without an engine), geospatial-indexing and stream-processing (expanded after being created).

### Discarded
Nothing out of scope. Diagrams, videos, quizzes and comments on the pages are not readable as text.

## Pending
- Revisit with Premium access the 16 partial breakdowns listed above (API sections, data model, HLD, deep dives with options and trade-offs). Only their problem statements and requirements are read; nothing was completed from memory.
- Concept links in the partial interviews marked "indicative" are not confirmed by the source.
- Source inconsistencies noted: Tinder (100 vs 200 swipes/user/day), Distributed Rate Limiter (10M vs 100M users), LeetCode (two leaderboard routes), FB Post Search (mention of Elasticsearch despite the restriction).

## Books (docs/)

| Book | Coverage | Notes |
|---|---|---|
| Designing Data-Intensive Applications (Kleppmann) | Ch. 1-12 | No interview problems; 20 new concepts and variants in `payment-system` and `fb-news-feed`. Ch. 3, 5, 6, 7, 9 read in detail; ch. 8, 11, 12 only in fragments; ch. 2, 4, 10 mostly written from prior knowledge (review `data-models`, `encoding-and-schema-evolution`, `batch-processing`). |
| System Design Interview Vol. 1 (Xu) | Ch. 1-16 | Tables (powers of 2, latencies, availability nines, ch. 6 summary) were not extractable. Ch. 16 (reading list) discarded. |
| System Design Interview Vol. 2 (Xu & Lam) | Ch. 1-13 | Scanned PDF read with OCR; some tables and figures illegible. CDN traffic figure in `google-maps` is ambiguous. |
| Grokking the System Design Interview | Intro, 15 problems, System Design Basics (pp. 1-196) | Text extracted from PDF streams; a few phrases truncated. |
| Cracking the Coding Interview | Not processed | Out of scope (coding algorithms, not system design). |

## Known issues
- `replication` (DDIA) and `database-replication` (Xu/Grokking) overlap and may be merged.
- `sql-vs-nosql` was overwritten twice by parallel extractors; check for lost content.
- 13 concepts appear in no interview (theory-only): `b-trees`, `serializability`, `linearizability`, `data-models`, `proxies`, `batch-processing`, `back-of-the-envelope-estimation`, `encoding-and-schema-evolution`, `logical-clocks-and-causality`, `distributed-system-faults`, `distributed-systems-characteristics`, `horizontal-vs-vertical-scaling`, `system-design-interview-framework`.
