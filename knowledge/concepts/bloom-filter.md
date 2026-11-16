---
title: Bloom filter
type: concept
aliases: [filtro de bloom]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder, System Design Interview Vol.1 (Alex Xu), ch. 6 and 8, Designing Data-Intensive Applications (Kleppmann), ch. 3]
---

# Bloom filter

## Definition
Probabilistic set-membership structure: no false negatives, with false positives.

## Why it matters
It lets you check "already seen?" with very little memory when the history is huge.

## How it works
One filter is kept per user (in cache) with the seen ids; if it says "not present", it was definitely not seen.

## Variants and techniques
Error rate tunable against memory.

## Trade-offs
False positives hide valid items; it must be kept up to date and rebuilt after a cache loss (expensive at scale).

## When to use it / when not to
Large histories where a false positive is tolerable. For small histories, filtering with the K most recent swipes is enough.

## Additional detail (Xu Vol. 1)
- Ch. 6: in a key-value store's read path, the Bloom filter indicates which SSTables may contain the key, avoiding reading all of them ([[lsm-trees]]).
- Ch. 8: in a URL shortener with "hash + collision resolution", it reduces DB queries to check whether a shortURL already exists ([[url-shortener]]).

## Additional detail (DDIA, ch. 3)
- Use in LSM-trees: avoids reading SSTables on disk for nonexistent keys (looking up an absent key would otherwise have to traverse the memtable and all segments) ([[lsm-trees]]); Cassandra/HBase/LevelDB/RocksDB use it.

## Appears in
[[key-value-store]], [[tinder]], [[url-shortener]], [[web-crawler]]

## See also
[[caching]]
