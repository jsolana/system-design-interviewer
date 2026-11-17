---
title: Inverted index
type: concept
aliases: [inverted index, reverse index, posting list]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search, Designing Data-Intensive Applications (Kleppmann), ch. 3]
---

# Inverted index

## Definition
A keyword -> list of IDs of the documents containing it map; the basis of text search.

## Why it matters
Avoids scanning the DB with `LIKE '%kw%'`; at petabyte scale, sharding and replication only divide the cost by a constant.

## How it works
- Ingestion: tokenize each post and add its ID to the list of each keyword (10-1,000 writes per post).
- Ordering: two indexes (list by creation, sorted set by likes) to avoid sorting at query time.
- Multi-keyword: list intersection + phrase verification; better by indexing bigrams/shingles.

## Variants and techniques
- Shard by keyword across many Redis instances; ingestion via Kafka.
- Limit each list to ~1k-10k entries; rarely searched keywords go to blob storage (S3/R2) with a fallback.
- Likes: index updated at milestones (powers of 2/10) and re-ranking with fresh counts.

## Trade-offs
Huge lists for common words, index explosion with bigrams (10M -> 100M+ keys), Redis durability (MemoryDB), double storage for two orderings.

## When to use it / when not to
When an existing search engine cannot be used; in practice, [[full-text-search]] with Elasticsearch.

## Additional detail (DDIA, ch. 3)
- Lucene (the basis of Elasticsearch/Solr) stores the term -> postings list mapping in sorted SSTable-like files that are merged in the background, i.e. the same idea as [[lsm-trees]]. In partitioned systems, secondary indexes can be local (per document) or global (per term) ([[database-partitioning]]).

## Appears in
[[distributed-email-service]], [[fb-post-search]], [[linkedin-talent-search]], [[twitter-search]]

## See also
[[full-text-search]], [[redis-sorted-sets]], [[count-min-sketch]]
