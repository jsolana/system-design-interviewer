---
title: OLAP / columnar stores
type: concept
aliases: [data warehouse, ClickHouse, Druid, Pinot, Redshift, BigQuery, Snowflake]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator, https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k, Designing Data-Intensive Applications (Kleppmann), chs. 3 and 10]
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

## Appears in
[[ad-click-aggregator]], [[metrics-monitoring]]

## See also
[[stream-processing]], [[database-indexing]]
