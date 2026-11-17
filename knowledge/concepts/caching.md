---
title: Caching
type: concept
aliases: [cache-aside, read-through]
sources: [https://aws.amazon.com/builders-library/caching-challenges-and-strategies/, https://www.figma.com/blog/livegraph-real-time-data-at-scale/, https://www.figma.com/blog/figmas-next-generation-data-caching-platform/, Cracking the Coding Interview, ch. 9 pp. 141, 381-384, https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff, https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search, https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k, https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder, https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube, https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox, https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator, System Design Interview Vol.1 (Alex Xu), ch. 1, Grokking the System Design Interview (PDF), "Caching" pp. 176-178, System Design Interview Vol.1 (Alex Xu), ch. 13]
---

# Caching

## Definition
Storing frequent results in memory (Redis, Memcached) to avoid going to the DB.

## Why it matters
Memory ~100 ns vs SSD ~0.1 ms; Redis handles 100k+ ops/s. Absorbs read-heavy loads.

## How it works
- **Cache-aside**: check the cache; on a miss, read the DB and populate it (Bitly).
- **Read-through** with keys like `eventId:eventObject` (Ticketmaster).
- LRU eviction; TTL <= data expiration; long TTL for static data and short TTL for availability.
- Caching search results: key with all the parameters (e.g. TTL 24 h).

## Variants and techniques
Invalidation via DB triggers; Elasticsearch internal caches; CDN ([[cdn-edge-computing]]).

## Trade-offs
Invalidation, warm-up, memory sizing, cache-DB consistency, complexity. Fuzzy results are hard to cache.

## When to use it / when not to
Read-heavy, rarely mutated data (URLs, event details). With real-time availability, use a short TTL or don't cache.

## Additional detail
- [[gopuff]]: Redis in front of partitioned Postgres, TTL ~1 min; the Order Service invalidates when inventory changes.
- [[fb-news-feed]]: post cache replicated N times for hot keys ([[hot-keys]]).
- [[top-k]]: top K cache per window with key `top-k:{window}:{timestamp}`; cron precomputation to avoid stampedes on expiry.
- [[fb-post-search]]: without personalization, the same queries give the same results; cache with TTL < 1 min and CDN with Cache-Control.
- [[tinder]]: precomputed feed in cache + refresh from the index; per-user Bloom filter in cache.

## Additional detail (Xu Vol. 1, ch. 1)
- The book's strategy: **read-through** (the web server checks the cache; on a miss it queries the DB, stores the result and responds). Memcached as an API example.
- Considerations: use a cache when data is read often and modified rarely (memory is volatile; important data goes in persistent storage); define **expiration** neither too short (constant reloads) nor too long (stale data); **consistency** (the DB and cache are not updated in a single transaction; hard across regions, see "Scaling Memcache at Facebook"); **SPOF** (several cache servers in different data centers and over-provision memory by a percentage); **eviction** LRU (most popular), LFU or FIFO.

## Additional detail (Grokking, pp. 176-178)
- Caches exploit **locality of reference**; they can exist at every layer. **Application server cache**: with many nodes and a random LB the miss rate rises -> use global or distributed caches. CDN for static content ([[cdn-edge-computing]]).
- **Write policies / invalidation**: *write-through* (cache + DB at once; full consistency and no loss, but higher write latency); *write-around* (writes to the DB bypassing the cache; avoids flooding it with data that is not re-read, but the first access is a miss); *write-back* (writes only to the cache and persists later; low latency/high throughput for writes, risk of loss if the cache fails; used in the counters of [[distributed-rate-limiter]]).
- **Eviction**: FIFO, LIFO, LRU, MRU, LFU, Random Replacement. In the source's tests LRU (e.g. LinkedHashMap) is the default policy, with the 80-20 rule (cache 20% of the daily read volume) and cache replicas updated on each miss.
- Sizing examples: [[url-shortener]] 170 GB for 20% of daily traffic; [[pastebin]] ~10 GB; [[twitter]] tweets from the last 3 days < 100 GB.

- Autocomplete (Xu Vol. 1, ch. 13): distributed Trie Cache with a weekly snapshot and refill on miss; browser cache with `Cache-Control: private, max-age=3600` ([[typeahead]]).

## Additional detail (Cracking the Coding Interview, ch. 9)
- Cache sits between application and data store; cache either query -> results or a built object (rendered page fragment, recent posts list).
- LRU in O(1): doubly linked list (front = freshest, evict tail) + hash table key -> list node.
- Multi-machine layouts: private cache per machine (fast, low hit rate), full replica per machine (high hit rate, N-fold writes and memory), partitioned cache with owner = hash(key) % N (best space use, one extra hop). See [[search-query-cache]].
- Invalidation: track which cached queries depend on which URL, or periodically sweep; always add a maximum time-to-live so changes that cannot be tracked (new pages) eventually show; TTL can be per topic or per URL (query TTL = min of its URL TTLs). Forwarded hot keys can be re-cached on the requester.
- Immutable data (e.g. pastebin documents) needs no invalidation.

## Additional detail (Figma LiveGraph and FigCache)
- **Invalidation-based read-through cache for real-time queries** (LiveGraph 100x, https://www.figma.com/blog/livegraph-real-time-data-at-scale/): original design was one server tailing the Postgres WAL with an in-memory cache, so every mutation fanned out to every server and every server fanned in all shards; caches fragmented and deploys wiped them (thundering herd). Redesign into three independently scaled services: **edge** (sessions, expands views into queries, re-fetches on invalidation), **read-through cache** (sharded by query hash, hot standbys, deployed separately so edge deploys do not empty it), **invalidator** (sharded like DB shards, tails replication stream, the only topology-aware part).
  - Works because traffic is read-dominated, most updates invalidate few queries, and affected queries can be computed from the row's pre/post image plus query *shapes* (cache key = shape ID + args), so invalidators are stateless and need no global ordering (invalidated queries are re-read from the DB). Only ~11 of ~700 queries have unbounded range filters; they are over-invalidated using a nonce under an "easy" key (`easy-nonce-hard`), plus TTL cleanup.
  - Read/invalidation races: edges subscribe to invalidations before reading; concurrent same-key reads coalesce; an invalidation arriving mid-read marks it stale; a read arriving mid-invalidation does not write to the cache. Validated with chaos tests, sampled cache-vs-DB comparison and convergence checks against the old engine; migrated incrementally over ~1.5 years.
- **Cache proxy tier** (FigCache, https://www.figma.com/blog/figmas-next-generation-data-caching-platform/): Redis became a critical-path dependency with connection-count limits and connection storms. A stateless RESP-speaking proxy in front of ElastiCache multiplexes connections, centralizes routing/guardrails, fans out cross-shard read-only pipelines (cross-shard transactions stay non-atomic), and uses a configurable engine graph (Starlark -> Protobuf). Results: six-nines caching layer, order-of-magnitude fewer Redis connections, incident diagnosis from hours/days to minutes. Cost: extra hop (mitigated by zonal routing) and a new critical tier; built in-house because open-source proxies lacked command-level semantics. See [[proxies]].

## Additional detail (AWS Builders' Library, caching challenges and strategies)
Source: https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
- **Cache as hidden critical dependency / modal behavior**: a service "addicted" to its cache can fail when the cache is cold or down because the source sees a surge. Cache only if data is reusable across requests (unique queries = near-zero hit rate) and staleness is tolerable; typical triggers: dependency latency, throttling, costly scale-out, hot keys.
- **Local (on-box) cache**: fast, simple; but incoherent across servers, downstream load grows with fleet size, cold starts after deploy. **External (Memcached/Redis)**: shared value, load independent of fleet, no cold start on deploy, more storage; but another fleet to operate, often lower availability than the source, must handle failures, needs consistent hashing when nodes change, no conditional puts/transactions.
- **Inline (read/write-through; DAX, Varnish/Nginx, CDN)**: uniform API, no client logic, but a cache outage looks like a dependency outage. **Side (cache-aside)**: app controls, more bug risk.
- **Expiration/eviction**: absolute TTL per object, LRU; size and TTL must be modeled and validated with real hit/miss metrics (arbitrary launch values caused outages).
- **Resilience**: *soft TTL / hard TTL* (refresh after soft, serve stale until hard if source fails; AWS IAM client), backpressure-aware serving from cache, *negative caching* with its own TTL, *request coalescing* (one in-flight fetch per key against thundering herds), load shedding/request caps toward the source, load test with caching disabled.
- **Versioning**: cached data is persistent across mixed deployments; include format versions, read old, guard against poison pills; dropping on version mismatch triggers mass refresh.
- **Security**: encryption in transit/at rest, cache poisoning, timing side channels.
- *Interview note*: always state what happens when the cache is empty (soft/hard TTL, coalescing, shedding) and size the source for cold-cache load or protect it; see [[avoiding-fallback-in-distributed-systems]] and [[constant-work-pattern]].

## Appears in
[[ad-click-aggregator]], [[distributed-cache]], [[distributed-email-service]], [[dropbox]], [[fb-live-comments]], [[fb-news-feed]], [[fb-post-search]], [[gaming-leaderboard]], [[git-repository-hosting]], [[google-maps]], [[google-news]], [[gopuff]], [[hotel-reservation]], [[instagram]], [[leetcode]], [[nearby-friends]], [[pastebin]], [[personal-financial-manager]], [[proximity-service]], [[sales-rank]], [[search-query-cache]], [[social-network-shortest-path]], [[ticketmaster]], [[tinder]], [[top-k]], [[twitter]], [[twitter-search]], [[typeahead]], [[uber]], [[url-shortener]], [[web-crawler]], [[yelp]], [[youtube]]

## See also
[[cdn-edge-computing]], [[database-indexing]]
