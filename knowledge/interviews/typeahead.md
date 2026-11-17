---
title: Typeahead Suggestion (autocomplete)
type: interview
sources: [Grokking the System Design Interview (PDF), "Designing Typeahead Suggestion" pp. 92-99, System Design Interview Vol.1 (Alex Xu) ch. 13]
concepts: [trie, caching, database-partitioning, load-balancer, replication, stream-processing, cdn-edge-computing]
difficulty: medium
---

# Typeahead Suggestion (autocomplete)

## Prompt
Real-time service that recommends terms as the user types in a search box (similar: auto-suggestions, typeahead search). Difficulty in the source: Medium.

## Functional requirements
Given the typed prefix, suggest the 10 most relevant terms that start with it.

## Non-functional requirements
Real-time suggestions: visible in < 200 ms.

## Estimations
- Google scale: 5 B searches/day ≈ 60K QPS.
- ~20 % unique; indexing only the top 50 % -> ~100 M terms.
- Average query: 3 words x 5 characters = 15 characters x 2 B = 30 B -> 100 M x 30 B = 3 GB.
- Growth 2 % daily with 1 year of retention: 3 GB + 0.02 x 3 GB x 365 ≈ 25 GB.

## API
Not covered in the source.

## Data model
In-memory [[trie]] with a search counter per terminal node and a precomputed top-10 per node; snapshot to a file for persistence (level-order traversal: character + number of children).

## Architecture (high-level design)
Client -> (caches of popular terms) -> LB that knows the partitioning scheme -> trie servers (with master-slave replicas) -> aggregator if the query touches several partitions. Offline pipeline: query log (sampled, e.g. 1/1000) -> periodic MapReduce (every hour) -> trie update by offline copy + switch or master-slave.

## Deep dives
- Why a trie and how to get the top-10 quickly (top-N per node, references to terminal nodes, bottom-up construction) and how to update it (EMA, propagate to ancestors, term removal with a filter): see [[trie]].
- **Partitioning**: by range (first letter; unbalanced, e.g. many words start with 'c'), by maximum server capacity (ranges like `A-AABC`, `AABD-BXA`; hotspots remain) or by term hash (random distribution, all servers must be queried and aggregated).
- **Cache** in front of the trie servers with the most frequent searches; possible ML model that predicts engagement to decide what to cache.
- **Fault tolerance**: master-slave; on restart, rebuild from the last snapshot.
- **Client**: wait ~50 ms without typing before requesting; cancel in-flight requests if the user keeps typing; start after a couple of characters; prefetch; local suggestion history; open the connection early; push part of the cache to CDNs/ISPs.
- **Personalization**: per-user history, location, language; stored on server and client; personalized terms go first.
- Ranking beyond count: freshness, location, language, demographics, history.

## Trade-offs and decisions
- Top-N per node: more storage in exchange for minimal latency.
- Offline batch update: suggestions not immediate but the trie serves without interruptions.
- Term hash minimizes hotspots but forces fan-out to all servers.

## Related concepts
[[trie]], [[caching]], [[database-partitioning]], [[load-balancer]], [[replication]], [[stream-processing]]

## Follow-up questions
How to remove terms for legal reasons; alternative ranking; personalization (all answered in deep dives).

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 13, pp. 200-219 ("Design a search autocomplete system", "top k queries")**: offline approach with a trie and a top-k cache per node.
  - Requirements: prefix-only matching, 5 suggestions, ordered by historical frequency, no spell check, lowercase English, 10M DAU; response < 100 ms (Facebook), relevant, sorted, scalable and highly available.
  - Estimations: 10M DAU x 10 searches/day x 20 characters (one request per character; 20 B query = 4 words x 5 characters) / 86,400 s ≈ **24,000 QPS** (peak 48,000); 20% new queries -> 0.4 GB/day of new data.
  - Initial design: *data gathering service* (query-frequency table) + *query service* (SQL sorted by frequency filtering by prefix with LIMIT 5; works with little data, bottleneck with a lot).
  - **[[trie]]** with frequency in the nodes; complexity O(p) + O(c) + O(c log c). Two optimizations: limit the prefix length (p ≈ 50 -> O(1)) and **cache the top-k at each node** (space for time) -> O(1).
  - Data gathering rewritten: analytics logs (append-only) -> aggregators (weekly frequency if real time isn't needed) -> aggregated data -> asynchronous workers build the trie -> **Trie DB** (document store with serialized snapshot, e.g. MongoDB, or KV store mapping each prefix to a key) -> distributed **Trie Cache** (weekly snapshot).
  - Query service: LB -> API servers -> Trie Cache (refilled on a miss). Optimizations: AJAX, **browser cache** (Google: `cache-control: private, max-age=3600`), **data sampling** (log 1 out of every N requests).
  - Operations: create (workers with aggregated data); update (rebuild weekly and replace, or update the node and all its ancestors because they store the top queries); delete (filter layer in front of the Trie Cache for harmful suggestions; asynchronous physical deletion before the next rebuild).
  - Storage scaling: sharding by first letter (a-m / n-z, up to 26 servers and sublevels) with uneven distribution (more words with 'c' than 'x'); mitigate with a **shard map manager** and analysis of the historical distribution (e.g. one shard for 's' and another for 'u'-'z').
  - Follow-ups: multi-language (Unicode in nodes), different tries per country (storable in a CDN), real-time trending (reduce the dataset by sharding, weight recent queries, stream processing: MapReduce, Spark Streaming, Storm, Kafka).
  - Differs from the base (Grokking): Xu explicitly separates the offline path (logs, weekly aggregation, workers) from the query path and quantifies the QPS per keystroke.

See [[top-k]] for ranking of the most frequent elements in streaming.
