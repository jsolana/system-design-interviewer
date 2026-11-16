---
title: B-trees
type: concept
aliases: [B-tree, B+ tree, page-oriented storage, copy-on-write B-tree]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 3 (pp. 79-86)]
---

# B-trees

## Definition
The standard index structure of relational DBs: a tree of fixed-size **pages** (typically 4 KB) that keeps keys sorted and is updated by overwriting pages in place.

## Why it matters
Enables efficient point and range reads with little depth: 4 levels, 4 KB pages and a branching factor of 500 store up to ~256 TB.

## How it works
- Each page contains keys and references to child pages (ranges); leaves contain values or references.
- Insertion: if the page fills up it is split and the parent is updated. This multi-page operation is dangerous in the face of a crash -> a **[[write-ahead-log]]** (redo log) is used before modifying pages.
- Concurrency: **latches** (lightweight locks) on the tree.

## Variants and techniques
- Copy-on-write (LMDB): a new version of the page and of its ancestors is written; also useful for snapshot isolation.
- Abbreviated keys in internal nodes (B+ tree) -> higher branching factor.
- Leaves in sequential order and sibling pointers for scans; fractal trees.
- Indexes: clustered (row stored within the index, InnoDB), heap file with indexes pointing to it, covering index (some of the columns in the index), secondary (list of IDs or key+rowid), concatenated multi-column, R-trees for geospatial, fuzzy/in-memory.

## Trade-offs
See the comparison table in [[lsm-trees]]. Each key exists in a single place (an advantage for range locks/transactions), but every write is done at least twice (WAL + page).

## When to use it / when not to
Default in relational OLTP. For very write-intensive ingestion consider LSM.

## Appears in


## See also
[[lsm-trees]], [[database-indexing]], [[write-ahead-log]], [[geospatial-indexing]]
