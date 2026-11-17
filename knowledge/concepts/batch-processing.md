---
title: Batch processing (Unix, MapReduce, dataflow)
type: concept
aliases: [MapReduce, Hadoop, HDFS, Spark, Flink, sort-merge join, broadcast hash join, offline systems, dataflow engines, data lake]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 10 (pp. 411-460), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 11 (pp. 451-481)]
---

# Batch processing

## Definition
Processing a **bounded, known** input set (offline) to produce derived datasets (indexes, models, reports). It is measured in throughput, not latency.

## Why it matters
It allows recomputing derived views from the source of truth ("human fault tolerance": if the code has a bug, fix it and rerun), with immutable input and fresh output.

## How it works
- **Unix philosophy**: programs that do one thing, immutable inputs, composition with pipes, uniformity (files).
- **MapReduce**: mapper (extracts key/value) -> **shuffle** (partitions by key hash and sorts) -> reducer (processes per key). Input lives in a distributed filesystem (**HDFS**, replicated); output goes to new files; failed tasks are retried (determinism required).
- **Joins**:
  - *Reduce-side*: **sort-merge join** (mappers emit by join key, reducers bring them together; secondary sort).
  - *Map-side*: **broadcast hash join** (small table in memory), **partitioned hash join**, **map-side merge join** (both sorted/partitioned the same way).
  - **Skew**: hot keys (celebrities) -> *skewed join* (spread the hot key across reducers), sharded join.
- **Output**: build search indexes and key-value databases (Voldemort) by loading immutable files and swapping, instead of writing row by row.
- Multi-job workflows: schedulers (Airflow, Oozie), materialized intermediate files.

## Variants and techniques
- **Dataflow engines** (Spark, Tez, Flink): avoid materializing intermediate state, flexible operators, recomputation via lineage; better than chained MapReduce.
- Graph processing (Pregel/BSP), higher-level APIs (Hive, Pig, SQL).
- Hadoop vs MPP: the "data lake" (dump raw data, schema on read) vs data warehouse (upfront modeling).

## Trade-offs
Latency of hours, but easy to reason about and fault tolerant; compared with [[stream-processing]], which gives low latency. Unified architectures ([[derived-data-and-dataflow]]) combine both.

## When to use it / when not to
ETL, training, indexing, periodic reports; not for cases that need results in seconds.

## Additional detail (DDIA 2nd edition, ch. 11)
*Verification against the 2nd edition (ch. 11 "Batch Processing", pp. 451-481):* the core of the 1st-edition entry (Unix philosophy, MapReduce shuffle, sort-merge join with secondary sort, dataflow engines, Pregel graph processing, human fault tolerance) is confirmed. Differences:
- The 2nd edition no longer details **broadcast hash joins, partitioned hash joins, map-side merge joins, skew handling and the Voldemort/search-index-building example**; those 1st-edition items are not in this text (do not rely on them as DDIA 2nd-ed content). The Hadoop-vs-MPP "data lake vs warehouse" framing is replaced by the **data lakehouse** (object storage + open table formats + query engines; see [[olap-columnar-stores]]).
- **Unix tools example** (new): access-log top-5 pages with `awk | sort | uniq -c | sort -n | head`; sort-based approach spills to disk (mergesort, sequential I/O) vs in-memory hash table whose working set is the number of distinct keys.
- **Storage layer**: distributed filesystems (HDFS 128 MB blocks, NameNode metadata, DataNodes, replication or erasure coding, shared-nothing, tasks scheduled near replicas) vs **object stores** (S3, GCS, Azure Blob; bucket + key, immutable objects, prefix listing not directories, non-atomic rename = copy+delete, no locks; storage and compute separated and scaled independently). Batch storage is shifting from HDFS to object stores; the S3 API is a de facto protocol (MinIO, R2, B2).
- **Job orchestration** (new): scheduler allocates cores/memory; problems of gang allocation (two 100-core jobs), idle reservations/deadlock, **preemption** of low-priority tasks, so task failures are routine; workflow schedulers (Airflow; Oozie/Azkaban replaced) wait for all upstream jobs; jobs pass data via files in a DFS/object store.
- **Models**: MapReduce (mapper/shuffle/reducer, per-reducer sorted files) and **dataflow engines** (Spark keeps intermediate data in memory and recomputes lost data from lineage; Flink checkpoints; operators start as soon as input is ready, no needless sorting). SQL/query engines with cost-based optimizers (Hive, Trino, Spark SQL) and **DataFrame APIs** that compile to optimized query plans.
- **Use cases**: ETL, analytics, **machine learning** (feature prep, LLM data preparation: tokenizing, embeddings), reconciliation, and **serving derived data**: do not write record-by-record from a job into a live DB (load, contention, partial output); bulk-load files and atomically swap dataset versions (TiDB Lightning, Pinot bulk import).
- Rollback by switching a directory/table version is easy on object stores and table formats ("minimizing irreversibility").

## Appears in
[[duplicate-url-detection]], [[linkedin-course-recommendation]], [[personal-financial-manager]], [[sales-rank]]

## See also
[[stream-processing]], [[derived-data-and-dataflow]], [[olap-columnar-stores]], [[database-partitioning]]
