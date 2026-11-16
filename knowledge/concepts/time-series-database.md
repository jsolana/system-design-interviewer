---
title: Time-series database
type: concept
aliases: [TSDB, base de datos de series temporales, metrics storage]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 5 Metrics Monitoring and Alerting System, pp. 131-157]
---

# Time-series database

## Definition
Database optimized for time series: sequences of timestamped values, identified by a metric name and a set of labels (labels/tags). Examples: InfluxDB, Prometheus, OpenTSDB (on HBase), Amazon Timestream, MetricsDB (Twitter), Gorilla (Facebook, in-memory).

## Why it matters
Operational metrics generate a **constant, high write** load with bursty reads (dashboards and alerts). A general relational DB requires expert tuning at that scale, needs an index per label and makes typical queries (moving averages) awkward; a general NoSQL (Cassandra, Bigtable) requires designing custom schemas. A TSDB uses far fewer servers.

## How it works
- **Model**: series = name + labels (key:value) + array of (value, timestamp) pairs; input format "line protocol" (Prometheus, OpenTSDB). E.g.: `cpu.load` with `host:i631,env:prod`.
- **Label indexes** to look up series by labels quickly; labels must be **low cardinality** (few possible values) so as not to overload the DB.
- Based on an in-memory cache + disk storage. Reference: InfluxDB with 8+ cores and 32+ GB handles >250,000 writes/s.
- Own query languages (PromQL, Flux) because SQL is too complex for moving windows/exponential moving average.
- Empirical data point (Gorilla, Facebook): >=85% of queries to the operational data store are over data from the last 26 hours; a TSDB that exploits this performs much better.

## Variants and techniques
- **Compression via delta / double-delta encoding**: store a base timestamp and deltas (e.g. `1610087371, 10, 10, 9, 11`; a 10 s difference fits in ~4 bits instead of 32).
- **Downsampling / rollup**: convert high resolution to low for old data (e.g. 7 days unsampled, 30 days at 1 min, 1 year at 1 h; averages from 10 s to 30 s).
- **Cold storage** for inactive data (cheaper).
- **Aggregation**: in the collection agent (simple, e.g. counter per minute), in the ingestion pipeline (with Flink; reduces writes but complicates late events and loses precision) or at query time (lossless but slower).
- **Collection**: *pull* (Prometheus; `/metrics` endpoint, service discovery with etcd/ZooKeeper; collectors distributed with [[consistent-hashing]]) vs *push* (CloudWatch, Graphite; agent on each server with local aggregation and buffer). Pull makes debugging and health checks easier; push suits ephemeral jobs and serverless or multi-datacenter environments (Pushgateway in pull). Large organizations usually support both.
- Queue (Kafka) in front of the DB so data is not lost if the TSDB goes down; partitioning by metric name and labels. Queue-less alternative: Gorilla, designed to keep accepting writes during partial network failures.

## Trade-offs
- Buy/use a standard TSDB vs build one (the source advises against building or using a general DB).
- Pull vs push; aggregate before writing (less volume) vs after (more flexibility).
- Label cardinality vs query capability.

## When to use it / when not to
Infrastructure metrics, counters and any time-indexed data with continuous writes. Not for logs (ELK) or distributed tracing (other systems).

## Appears in
[[metrics-monitoring]]

## See also
[[metrics-monitoring]], [[stream-processing]], [[message-queues]], [[service-discovery]], [[lsm-trees]], [[olap-columnar-stores]]
