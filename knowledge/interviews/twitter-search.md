---
title: Twitter Search
type: interview
sources: [Grokking the System Design Interview (PDF), "Designing Twitter Search" pp. 113-118]
concepts: [inverted-index, database-partitioning, consistent-hashing, caching, load-balancer, database-replication, unique-id-generation]
difficulty: medium
---

# Twitter Search

## Prompt
Design a service that stores tweets and allows searching them. Difficulty in the source: Medium.

## Functional requirements
Search across all tweets with multi-word queries combined with AND/OR; sort by most recent (default), best match or most likes; pagination.

## Non-functional requirements
Not explicit beyond the low latency and fault tolerance addressed in the design.

## Estimations
- 400 M tweets/day x 300 B = 120 GB/day (~1.38 MB/s).
- 5 years: 120 GB x 365 x 5 ≈ 200 TB; with 80% maximum occupancy and replication ≈ 500 TB; 4 TB servers -> ~125 servers.
- 730 B tweets in 5 years -> TweetID of ~5 bytes.
- Index: ~500 K words (300 K English + 200 K proper nouns) x 5 characters = 2.5 MB. Indexing 2 years (292 B tweets) x 5 B = 1460 GB; ~15 indexable words per tweet -> ≈ 21 TB; with servers of 144 GB RAM ≈ 152 servers.

## API
`search(api_dev_key, search_terms, maximum_results_to_return, sort, page_token)` -> JSON with user ID/name, text, tweet ID, date, likes...

## Data model
- Tweets table (TweetID, content) in a DB, partitioned by hash of the TweetID (system-wide unique ID, see [[twitter]]).
- [[inverted-index]] word -> list of TweetIDs, in memory.

## Architecture (high-level design)
Tweet DB + index servers; app servers query the indexes and an aggregator server combines results; LB between client-app and app-backend; cache (Memcached) in front of the DB for hot tweets.

## Deep dives
- **Index sharding**:
  - By word (hash of the word): a query touches only that word's server; problems: hot words and uneven distribution of TweetIDs per word (solution: redistribution or [[consistent-hashing]]).
  - By tweet (hash of the TweetID, all its words are indexed on that server): all servers must be queried and the results aggregated.
- **Fault tolerance**: secondary replica per server; if both fail, rebuild. Brute force (scanning the DB filtering by hash) is slow and unavailable during rebuild; better an **Index-Builder server** with a hash set of TweetIDs per index server (with its own replica).
- **Ranking**: popularity score (likes, retweets, follows...) stored with the tweet; each partition sorts by it, the aggregator merges and returns the top.
- LRU cache and Round Robin LB (with the load-aware LB variant).

## Trade-offs and decisions
Shard by word (cheap queries, hotspots) vs shard by tweet (uniform distribution, fan-out to all servers).

## Related concepts
[[inverted-index]], [[database-partitioning]], [[consistent-hashing]], [[caching]], [[load-balancer]], [[database-replication]], [[unique-id-generation]]

## Follow-up questions
Ranking by social graph distance, popularity or relevance.

## Variants
See [[fb-post-search]] for post search with a different approach (another source).
