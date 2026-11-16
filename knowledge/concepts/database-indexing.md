---
title: Database indexing
type: concept
aliases: [indexes, indices, B-tree index]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k, https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder, https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff, Designing Data-Intensive Applications (Kleppmann), ch. 3]
---

# Database indexing

## Definition
An auxiliary structure that speeds up lookups by avoiding full table scans.

## Why it matters
Without an index, looking up by key is O(n); with a B-tree it is O(log n).

## How it works
- Using the lookup key as the primary key gives both an index and uniqueness (short_code in [[url-shortener]]).
- Index filter columns (name, date, performer, venue in [[ticketmaster]]); use EXPLAIN, avoid `SELECT *`, use LIMIT, prefer UNION over OR.

## Variants and techniques
B-tree; composite indexes; tsvector + GIN for text (see [[full-text-search]]).

## Trade-offs
More indexes slow down writes; standard indexes perform poorly on partial text matches (`LIKE '%x%'`). An index is not enough for 600k reads/s: [[caching]] is needed.

## When to use it / when not to
Always on frequently queried columns; do not over-index write-heavy tables.

## Additional detail (DDIA, ch. 3)
- **Structures**: [[b-trees]] (4 KB pages, in-place update with WAL) vs [[lsm-trees]] (SSTables + compaction). Rule of thumb: LSM usually writes faster, B-tree reads faster/more predictably.
- **Secondary indexes**: non-unique keys (a list of IDs per key or key + rowid). The value can be the row itself (clustered index, InnoDB: secondary indexes point to the PK), a reference to a **heap file** (avoids duplicating data, but moving rows requires updating indexes) or a **covering index** (stores some columns in the index).
- **Multi-column indexes** (concatenated, e.g. (last name, first name)), R-trees for geospatial data ([[geospatial-indexing]]), full-text/fuzzy search with Lucene's SSTable-like structure ([[inverted-index]]), and in-memory databases.
- In partitioned systems the secondary index can be local or global ([[database-partitioning]]).

## Appears in
[[dropbox]], [[fb-news-feed]], [[gopuff]], [[s3-object-storage]], [[ticketmaster]], [[top-k]], [[url-shortener]], [[whatsapp]], [[yelp]]

## See also
[[full-text-search]], [[caching]]
