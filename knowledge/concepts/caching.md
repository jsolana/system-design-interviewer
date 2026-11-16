---
title: Caching
type: concept
aliases: [cache-aside, read-through]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff, https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search, https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k, https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder, https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube, https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox, https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator, System Design Interview Vol.1 (Alex Xu), ch. 1, Grokking the System Design Interview (PDF), "Caching" pp. 176-178, System Design Interview Vol.1 (Alex Xu), ch. 13]
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

## Appears in
[[ad-click-aggregator]], [[distributed-cache]], [[distributed-email-service]], [[dropbox]], [[fb-live-comments]], [[fb-news-feed]], [[fb-post-search]], [[gaming-leaderboard]], [[google-maps]], [[google-news]], [[gopuff]], [[hotel-reservation]], [[instagram]], [[leetcode]], [[nearby-friends]], [[pastebin]], [[proximity-service]], [[ticketmaster]], [[tinder]], [[top-k]], [[twitter]], [[twitter-search]], [[typeahead]], [[uber]], [[url-shortener]], [[web-crawler]], [[yelp]], [[youtube]]

## See also
[[cdn-edge-computing]], [[database-indexing]]
