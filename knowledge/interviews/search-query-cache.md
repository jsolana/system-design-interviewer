---
title: Search Query Result Cache (100 machines)
type: interview
sources: [Cracking the Coding Interview, 6th ed. (G. Laakmann McDowell), ch. 9 pp. 137-145 and solutions pp. 372-395 (problem 9.5)]
concepts: [caching, consistent-hashing, load-balancer, database-partitioning]
difficulty: medium
---

# Search Query Result Cache (100 machines)

## Prompt
A simplified search engine has 100 machines answering queries; the machine for a query is chosen at random. Each calls an expensive processSearch(query) on another cluster. Design a cache for the most recent queries and explain how to update it when data changes.

## Functional requirements
- Efficient lookup by query.
- Expire old data; refresh when underlying results change.

## Non-functional requirements
Assumptions stated: query handling occurs on the initial machine except processSearch; millions of queries cached; machine-to-machine calls are fast; a result is an ordered list of URLs, each with a 50-char title and 200-char summary; the most popular queries are extremely popular.

## Estimations
Not covered beyond the assumptions above.

## API
getResults(query) / insertResults(query, results).

## Data model
Single-machine LRU: doubly linked list (most recent at front, evict from tail) plus hash table query -> list node, giving O(1) lookup and O(1) freshness update.

## Architecture (high-level design)
Three ways to spread the cache across machines:
| Option | Pro | Con |
|---|---|---|
| Each machine has its own cache | Fast, no cross-machine calls | Repeat queries on another machine miss; low hit rate |
| Full copy on every machine | Hot queries nearly always hit | Every update goes to N machines; N-fold space, so fewer entries |
| Each machine holds a segment (owner = hash(query) % N) | Best use of space | Extra hop to the owner machine j; owner either returns cached value or calls processSearch itself |
Owner-calls-processSearch is preferred over "owner returns null, requester computes and forwards" (more calls, no gain).

## Deep dives
- Invalidation: results change when (1) page content changes/removed, (2) ranking changes, (3) new pages appear. For 1-2, keep a URL -> cached queries table (large) or periodically crawl the caches; for 3 (hard) use an automatic timeout so nothing stays more than x minutes.
- Enhancement: hot query can be cached also on the requesting machine after one forward.
- Enhancement: route queries by hash instead of randomly (with its own trade-offs).
- Per-topic or per-URL timeouts: query timeout = min of timeouts of its URLs (news refreshed faster than historical stock prices).

## Trade-offs and decisions
Hit rate vs update cost vs memory (the three options); freshness vs load (timeouts).

## Related concepts
[[caching]], [[consistent-hashing]], [[load-balancer]], [[database-partitioning]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.
