---
title: Full-text search
type: concept
aliases: [Elasticsearch, inverted index]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster]
---

# Full-text search

## Definition
Searching over text with specialized indexes instead of `LIKE '%term%'` (full scan).

## Why it matters
Meets latencies such as < 500 ms and tolerates typos.

## How it works
- Ladder of options: indexes + query optimization -> PostgreSQL FTS (tsvector + GIN) -> Elasticsearch.
- Elasticsearch: inverted index, fuzzy matching ("Tayler" ~ "Taylor"), filter and request caches per shard.

## Variants and techniques
Synchronization with the primary DB via [[change-data-capture]].

## Trade-offs
- Postgres FTS: faster than LIKE, more storage, maintenance, not Lucene-based.
- Elasticsearch: better search; cluster cost and sync reliability.

## When to use it / when not to
Elasticsearch when search is a core feature; Postgres FTS for moderate scale.

## Appears in
[[distributed-email-service]], [[fb-post-search]], [[linkedin-talent-search]], [[ticketmaster]], [[tinder]], [[yelp]]

## See also
[[database-indexing]], [[change-data-capture]], [[caching]]
