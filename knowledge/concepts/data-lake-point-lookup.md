---
title: Point lookups on a data lake (Random Access Parquet)
type: concept
aliases: [RAP, external index over Parquet, key lookup on object storage]
sources: [https://engineering.atspotify.com/2026/7/indexing-the-data-lake-for-online-point-queries]
---

# Point lookups on a data lake (Random Access Parquet)

## Definition
Serving low-latency key lookups straight from columnar files in object storage by adding an external index that maps each key to file + row locations, instead of copying data into a KV store or running a distributed SQL engine.

## Why it matters
Object storage latency is now 30-100 ms (single-digit ms on newer tiers), but Trino/BigQuery add seconds of planning even for one row; KV stores are too costly for huge datasets. Example: a year of listening history = about 90 daily partitions x 1,000 files = ~90,000 Parquet files.

## How it works
- Index is a multimap: key -> (dictionary-encoded file ordinal, row numbers, optional value count). Terabytes of data -> gigabytes of index.
- Reader resolves rows to pages using cached file metadata and issues parallel ranged reads of only needed bytes.
- Baseline pruning: key-based partitioning (90,000 -> 90 files) and Bloom filters (-> ~12).

## Variants and techniques
- **Concentrate keys**: sort/hash-bucket by key, co-group rows per key into nested columns, use coarser partitions (weekly = 52 files/key/year vs 365).
- **Fewer bytes**: one page per key, ZSTD frame resets per key (files still valid Parquet), alignment padding to 4KB/16KB blocks.
- **Fewer reads**: store point-access fields as one blob/variant column, interleave columns per key, covering indexes (small values or precomputed aggregates in the index).
- **Secondary indexes** (hash, sorted, space-filling curves) are serving-layer changes only.

## Trade-offs
- One-page-per-key and frame resets lose delta/RLE encodings and slightly hurt compression; blobs lose column pruning for batch; interleaving makes single-column scans read dead space; covering indexes grow the index.
- Core lesson: dependent round trips dominate cost; a definitive external index beats probabilistic filters.

## When to use it / when not to
Large datasets needing occasional online key access and where duplicating into a KV store is too costly. Not for high-QPS ultra-low-latency paths.

## Appears in
None yet.

## See also
[[bloom-filter]], [[olap-columnar-stores]], [[object-storage]], [[database-indexing]]
