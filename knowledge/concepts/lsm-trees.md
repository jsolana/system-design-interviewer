---
title: LSM-trees and SSTables
type: concept
aliases: [log-structured merge tree, SSTable, memtable, compaction, LevelDB, RocksDB, Cassandra, HBase]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 3 (pp. 70-86), System Design Interview Vol.1 (Alex Xu), ch. 6 (pp. 105-107)]
---

# LSM-trees and SSTables

## Definition
A *log-structured* storage engine: writes accumulate sorted in memory (memtable) and are flushed to disk as immutable files sorted by key (SSTables), which are merged (compaction) in the background.

## Why it matters
Sequential writes and high write throughput; better compression and less fragmentation than a B-tree. The basis of LevelDB, RocksDB, Cassandra, HBase (Bigtable) and Lucene segments.

## How it works
1. Write -> memtable (balanced tree, e.g. red-black) and appended to an **unsorted on-disk log** (only to recover the memtable after a crash).
2. Memtable exceeds a threshold (a few MB) -> it is written as an SSTable (new, most recent segment); writes continue in a new memtable.
3. Read: memtable, then segments from newest to oldest (sparse in-memory index per segment).
4. Background compaction/merge discards overwritten and deleted values (*tombstones*).
- Identical basis in Lucene: term dictionary in SSTable-like files ([[inverted-index]]).

## Variants and techniques
- **Bloom filters** to avoid reading disk for nonexistent keys ([[bloom-filter]]).
- **Size-tiered** compaction (HBase; Cassandra) vs **leveled** (LevelDB, RocksDB; Cassandra).
- Write amplification: a write is rewritten several times by compaction.

## Trade-offs
| | LSM-tree | B-tree ([[b-trees]]) |
|---|---|---|
| Writes | faster (sequential, generally lower write amp.) | double write (WAL + page) |
| Reads | slower (several structures) | more predictable |
| Space | better compression | fragmentation |
| p99 latency | compaction can interfere | more stable |
| Transactions/range locks | duplicate keys across segments | each key in a single place |
- Risk: if compaction cannot keep up with the write rate, segments pile up and the disk fills; it must be monitored (they usually do not apply back-pressure).

## When to use it / when not to
Write-heavy workloads, metrics/log ingestion, large volumes. Prefer a B-tree if predictable read latency and range locks are required.

## Additional detail (Xu Vol. 1, ch. 6)
Read/write paths of a [[key-value-store]] node (based on Cassandra): **write** = 1) commit log, 2) memory cache (memtable), 3) flush to an SSTable on disk when it fills up or reaches a threshold (SSTable = sorted list of key-value pairs). **Read** = memory; if it misses, the [[bloom-filter]] is consulted to find out which SSTables may contain the key and those are read.

## Appears in
[[digital-wallet]], [[distributed-email-service]], [[key-value-store]], [[whatsapp]]

## See also
[[b-trees]], [[write-ahead-log]], [[database-indexing]], [[bloom-filter]], [[olap-columnar-stores]]
