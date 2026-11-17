---
title: LSM-trees and SSTables
type: concept
aliases: [log-structured merge tree, SSTable, memtable, compaction, LevelDB, RocksDB, Cassandra, HBase]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 3 (pp. 70-86), System Design Interview Vol.1 (Alex Xu), ch. 6 (pp. 105-107), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 4 (pp. 129-134)]
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

## Additional detail (DDIA 2nd edition, ch. 4)
- *2nd edition*: rule of thumb stays: LSM better for writes, B-trees for reads, but benchmark your workload; engines can blend both.
- **Read path**: B-tree = one page per level (predictable); LSM checks several SSTables (Bloom filters help point reads, not range queries, which must merge all segments).
- **Latency spikes**: when the memtable fills faster than compaction can flush, engines like RocksDB apply backpressure (stall reads/writes).
- **Sequential vs random writes**: even on SSDs, flash is written by 4 KiB page but erased by ~512 KiB block, so scattered writes cause more garbage collection and wear; NVMe parallelism requires careful design.
- **Write amplification** = bytes written to disk / bytes of the logical write. LSM: log + memtable flush + every compaction (WiscKey-style key/value separation reduces it). B-tree: WAL + page write (whole page even for few changed bytes). LSM typically lower for common workloads.
- **Space**: B-trees fragment (need vacuum/defrag); LSM compresses blocks and has little fragmentation, but overwritten/deleted data lingers until compaction (leveled compaction has low overhead, size-tiered more). Delayed physical deletion matters for regulations; immutable SSTables make snapshots/backups cheap.
- **Secondary indexes**: value is a list of row IDs or key + row ID. **Clustered index** (row in index, InnoDB primary key) vs **heap file** (Postgres; updates larger than old value need moves/forwarding pointers) vs **covering index** (included columns). **In-memory DBs** (VoltDB, SingleStore, Redis, RAMCloud) are faster because they skip encoding structures for disk, not because they avoid disk reads.
- Multicolumn: concatenated index vs multidimensional (R-tree, Bkd-tree, space-filling curve).

## Appears in
[[digital-wallet]], [[distributed-email-service]], [[key-value-store]], [[whatsapp]]

## See also
[[b-trees]], [[write-ahead-log]], [[database-indexing]], [[bloom-filter]], [[olap-columnar-stores]]
