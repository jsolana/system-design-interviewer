---
title: Metrics Monitoring (Datadog-style)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring, System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 5 pp. 131-157]
concepts: [stream-processing, olap-columnar-stores, time-series-database, message-queues, service-discovery, consistent-hashing, observability-and-monitoring, alerting-strategy, slos-slis-and-error-budgets, slo-burn-rate-alerting]
difficulty: high
---

# Metrics Monitoring

> Note: partially paywalled page; the prompt, requirements, estimations and deep dive questions are readable.

## Prompt
A platform that collects performance metrics (CPU, memory, throughput, latency) from servers and services, stores them as time series, visualizes them in dashboards and fires alerts when thresholds are exceeded (comparable: Datadog, Prometheus/Grafana, CloudWatch).

## Functional requirements
- Ingest metrics (CPU, memory, latency, custom counters).
- Query and visualize in dashboards with filters, aggregations and time ranges.
- Alert rules with thresholds over windows (e.g. p99 > 500 ms for 5 min).
- Notify (email, Slack, PagerDuty).
- Out of scope: logs and full-text search, distributed tracing, ML anomalies.

## Non-functional requirements
- 5M metrics/s from 500k servers.
- Dashboard queries in seconds, even over days/weeks.
- Alert latency < 1 min.
- High availability (dashboards eventually consistent; reliable alert evaluation).
- Late or out-of-order data.
- Out of scope: multi-region, strong consistency.
- *Source note*: alerts usually use moving averages/trends, so going below 1 min is rarely needed.

## Estimations
500k servers x 100 points every 10 s = **5M metrics/s** at peak; 100-200 B per point ≈ **1 GB/s** of ingestion. No storage or retention figures.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Titles only: ingest, query/visualize, define alerts, notify.

## Deep dives
Questions only: low-latency dashboards over weeks of data; alerts in < 1 min; high availability during spikes and failures; cardinality explosion.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[stream-processing]], [[olap-columnar-stores]] (*Note*: indicative).

## Follow-up questions
The four deep dives.

## Variants
### Xu & Lam Vol. 2, ch. 5 (System Design Interview Vol. 2, pp. 131-157)
Source: System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 5 Metrics Monitoring and Alerting System. Difference: an **internal** system (not SaaS) for a large company, operational metrics only (no logs or tracing), with a complete design (the Hello Interview source only provided requirements).
- **Scale**: 100 M DAU, 1,000 server pools x 100 machines x 100 metrics = ~10 M metrics. 1-year retention: 7 days raw, 30 days at 1 min, 1 year at 1 hour. Alerts by email, phone, PagerDuty and webhooks. Non-functional requirements: scalability, low query latency, reliability (do not lose alerts) and flexibility to change technologies.
- **Five components**: collection, transmission, storage, alerting, visualization.
- **Model**: time series (name + labels + timestamped values), write-heavy access with bursty reads -> [[time-series-database]] (InfluxDB/Prometheus), not MySQL or a general NoSQL.
- **Architecture**: metrics source -> metrics collector (autoscalable cluster) -> Kafka -> consumers/Flink/Spark -> TSDB -> query service (+ cache) -> alerting system and visualization system (Grafana).
- **Pull vs push collection**: pull with service discovery (etcd/ZooKeeper) and a collector pool split with consistent hashing to avoid duplicates; push with a local agent (aggregation and buffering) and collectors behind a load balancer. Comparison table: debugging and health check (pull wins), ephemeral jobs and firewall/multi-DC (push wins), authenticity (pull, known-server config), performance (TCP vs UDP, debatable). Large organizations support both.
- **Scaling**: Kafka with partitions by metric name/labels and metric prioritization; alternative without Kafka (Gorilla). Aggregation in the agent, at ingestion (Flink; late events, loss of precision) or at query time.
- **Query service**: decouples the TSDB from clients; optional (Grafana plugins already connect to TSDBs, and a well-chosen TSDB needs no cache of its own). Custom language (Flux) versus complex SQL for moving averages.
- **Storage**: delta/double-delta compression, downsampling by retention rules, cold storage; 85% of queries hit the last 26 h.
- **Alerting**: YAML rules loaded into cache -> alert manager periodically queries the query service -> filters, merges and deduplicates alerts (merge), access control, retries (at-least-once) -> alert store (Cassandra-like KV with inactive/pending/firing/resolved states) -> Kafka -> alert consumers send to email/SMS/PagerDuty/HTTP. Build vs buy: justify building versus off-the-shelf solutions (also for visualization: Grafana).

