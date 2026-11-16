---
title: Batch processing (Unix, MapReduce, dataflow)
type: concept
aliases: [MapReduce, Hadoop, HDFS, Spark, Flink, sort-merge join, broadcast hash join, offline systems, dataflow engines, data lake]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 10 (pp. 411-460)]
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

## Appears in


## See also
[[stream-processing]], [[derived-data-and-dataflow]], [[olap-columnar-stores]], [[database-partitioning]]
