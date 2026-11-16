---
title: Write-ahead log (WAL)
type: concept
aliases: [WAL, redo log, commit log, replication log]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 4 pp. 91-130, Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 3 (p. 82), ch. 5 (pp. 158-160), ch. 11]
---

# Write-ahead log (WAL)

## Definition
An append-only file where every modification is recorded before it is applied to the main data structures; used to recover after a crash.

## Why it matters
It makes multi-page writes (e.g. [[b-trees]] splits) durable and atomic and is the basis of replication and [[change-data-capture]].

## How it works
- B-tree: every modification is written to the WAL first; after a failure it is replayed to leave the tree consistent.
- LSM: an unsorted log protects the memtable ([[lsm-trees]]).
- Replication: the same log can be shipped to followers (WAL shipping, PostgreSQL/Oracle). It couples replication to the storage engine's physical format (different versions are incompatible); alternative: logical log (MySQL row-based binlog).
- Log as an abstraction: commit log -> total order of events ([[event-sourcing]], [[message-queues]], [[consensus]] / total order broadcast).

## Variants and techniques
Physical vs logical log; log compaction (keep only the latest value per key); copy-on-write as an alternative to the WAL.

## Trade-offs
Double write (log + data) in exchange for simpler recovery.

## When to use it / when not to
Whenever on-disk structures are updated in place or data is to be replicated/derived from a log.

## Additional detail (Xu & Lam Vol. 2, ch. 4)
In a distributed queue each partition is a WAL split into **segments**: only the active segment receives appends (monotonic offset); inactive ones serve reads and are truncated by retention or capacity. Sequential access on spinning disks/RAID (hundreds of MB/s) and the OS page cache make it very efficient. See [[distributed-message-queue]].

## Appears in
[[digital-wallet]], [[distributed-message-queue]], [[s3-object-storage]], [[stock-exchange]]

## See also
[[replication]], [[change-data-capture]], [[lsm-trees]], [[b-trees]]
