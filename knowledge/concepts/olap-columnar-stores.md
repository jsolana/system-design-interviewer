---
title: OLAP / columnar stores
type: concept
aliases: [data warehouse, ClickHouse, Druid, Pinot, Redshift, BigQuery, Snowflake]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator, https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k, Designing Data-Intensive Applications (Kleppmann), chs. 3 and 10, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 4 (pp. 134-145)]
---

# OLAP / columnar stores

## Definition
Columnar stores optimized for analytical aggregations over large volumes (Redshift, Snowflake, BigQuery, ClickHouse, Druid, Pinot).

## Why it matters
They allow sub-second multidimensional queries over pre-aggregated metrics, something a transactional database running GROUP BY over raw events cannot achieve at 10k events/s.

## How it works
- Fed with aggregates from a batch job (Spark) or a streaming job (Flink) and queried by AdId/range.
- Nightly rollups (daily/weekly) for long windows: storage is spent in exchange for speed.
- Managed ones scale on their own; self-managed ClickHouse is sharded (e.g. by AdvertiserId).

## Variants and techniques
Druid: rollup at ingestion + compaction; Pinot: star-tree and materialized views; ClickHouse: materialized views (SummingMergeTree/AggregatingMergeTree). TSDB only for simple time-range metrics.

## Trade-offs
Operational fragility at scale (node failures, compaction); TSDBs struggle with high cardinality (InfluxDB/Prometheus with billions of series).

## When to use it / when not to
Read-heavy aggregate analytics; not as a transactional store.

## Additional detail (DDIA, chs. 3 and 10)
- **OLTP vs OLAP**: OLTP = point reads/writes by key, low volume per query; OLAP = scans of millions of rows with aggregations (sum, count, avg) over few columns, typically on a data warehouse fed by ETL.
- **Modeling**: star schema (central fact table with foreign keys to dimensions: date, product, customer) and snowflake (normalized dimensions).
- **Columnar storage**: store each column in separate files to read only the ones needed; better compression (**bitmap encoding** + run-length), vectorized operations; writes use in-memory LSM structures to avoid re-sorting columns. *Materialized views* and data cubes for precomputed aggregates ([[lsm-trees]], [[data-models]]).
- Relation to [[batch-processing]]: the jobs produce the derived data that gets loaded.

## Additional detail (DDIA 2nd edition, ch. 4)
- *2nd edition (new/expanded)*: **cloud data warehouses** (BigQuery, Redshift, Snowflake) decouple compute from storage on object storage ([[cloud-native-architecture]]). Open-source warehouses (Hive, Trino, Spark) unbundled into: **query engine** (Trino, DataFusion, Presto), **storage format** (Parquet, ORC, Lance, Nimble; immutable files), **table format** (Apache Iceberg, Delta: which files form a table, row inserts/deletes, time travel, GC, transactions) and **data catalog** (Polaris, Unity Catalog, Iceberg catalog; REST service).
- **Column storage details**: queries touch ~4-5 of 100+ columns; data split into blocks of thousands/millions of rows (often by timestamp range); Parquet supports nested documents (Dremel). **Bitmap encoding**: one bitmap per distinct value, run-length encoded or *roaring bitmaps*; `IN`/AND/OR become bitwise ops (also usable for graph queries). Wide-column stores (Bigtable, HBase) are row-oriented despite the name.
- **Sort order**: sort whole rows by chosen keys (e.g. date then product); first key compresses best via run-length; never sort columns independently.
- **Writes**: bulk imports; log-structured approach: row-oriented sorted in-memory store merged into new column files; queries merge disk and memory (Snowflake, Vertica, Pinot, Druid).
- **Query execution**: *compilation* (generate and JIT-compile code, LLVM) vs *vectorized processing* (predefined operators over column batches, e.g. equality -> bitmap -> AND); both exploit sequential access, tight loops, SIMD, operating on compressed data. HTAP systems are splitting into separate row and column engines behind one SQL interface.
- **Materialized views / data cubes**: see [[materialized-views]].

## Appears in
[[ad-click-aggregator]], [[food-delivery-time-estimation]], [[metrics-monitoring]]

## See also
[[stream-processing]], [[database-indexing]]
