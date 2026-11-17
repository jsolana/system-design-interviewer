---
title: Observability and monitoring
type: concept
aliases: [monitoring, four golden signals, whitebox monitoring, blackbox monitoring, time-series monitoring, tracing and logging]
sources: [https://sre.google/workbook/monitoring/, https://sre.google/sre-book/monitoring-distributed-systems/, https://sre.google/sre-book/practical-alerting/, https://sre.google/sre-book/effective-troubleshooting/]
---

# Observability and monitoring

## Definition
Collecting, aggregating and displaying real-time quantitative data about a system for dashboards, alerting, trend analysis, capacity planning, experiment comparison and ad hoc debugging.

## Why it matters
You cannot meet an SLO ([[slos-slis-and-error-budgets]]) you do not measure, and during an incident the first question is "what is broken, and why?". See also the monitoring-system design in [[metrics-monitoring]] (interview).

## How it works
- **Whitebox** (internal metrics, logs, handlers) finds imminent problems and failures masked by retries, and is essential for debugging. **Blackbox** (probes acting like a user) shows active, user-visible problems and catches failures that never reach the service (DNS, routing). Use both; probe the global frontend and each datacenter to localize faults.
- **Four golden signals**: latency (track success and error latency separately; a slow error is worse than a fast one), traffic, errors (explicit, implicit such as wrong content with HTTP 200, and policy errors such as too slow), saturation (how full; latency rises before 100% utilization).
- **Symptoms vs causes**: alert on symptoms (users see errors), use causes (CPU, DB refusing connections) for diagnosis.
- **Long tail**: record latency as histograms with roughly exponential buckets (factor ~3). A 100 ms mean at 1,000 rps can hide 1% of requests taking 5 s.
- **Resolution**: sample at high frequency internally, aggregate over longer windows; a 99.9% target rarely needs probes more than once or twice a minute.
- **Time-series model (Borgmon / Prometheus style)**: each series is a (timestamp, value) stream named by labels (var, job, service, zone). Services expose metrics over HTTP, the collector scrapes them. Prefer counters over gauges (no events lost between samples) and sum per-task rates rather than taking the rate of sums (robust to counter resets). Rules derive new series (e.g. per-datacenter request rate over 10 min).
- **Scale numbers**: ~24 bytes per data point; ~1M series at 1-minute resolution for 12 h fits in under 17 GB RAM; recent data in memory (~12 h), older in an external TSDB ([[time-series-database]]).
- **Topology**: per-cluster collectors feed global aggregators that import only filtered series; replicate the global tier across zones.
- **Rules as code**: separate rules from targets, template them, unit-test with synthetic series.
- **Troubleshooting support**: metrics, structured logs with adjustable verbosity and sampling (example: 1 in 1,000 operations, flag those > 10 ms), distributed tracing, and endpoints exposing recent RPC samples and error/latency histograms.

## Additional detail (SRE Workbook, ch. 4)
Source: https://sre.google/workbook/monitoring/
- First check SLI metrics; then recent changes (binary version, flags, config version), direct dependencies, and saturation of every resource including soft ones (file descriptors, thread pools, queue wait, goroutines, heap).
- Metrics are near real time and drive alerts; logs are delayed but exact and serve RCA. For rare events, increment a counter and alert on the metric. Use structured logs. High-cardinality IDs (millions of values) belong in logs, not metric labels.
- Instrument the RPC client library once (size, latency, response code, method, peer) so new dependencies are monitored automatically; label request counters by status code with small label sets.
- Monitoring config is code (review, lint). Components (collection, storage, alert aggregation, visualization) should be loosely coupled; retain months of data for burn-rate windows ([[slo-burn-rate-alerting]]); data staler than 4-5 min slows incident response.
- Suppress noise: one global alert instead of per node, inhibit a service's alerts when its dependency already alerts. Linking alerts to SLOs cut false positives for an ads team running ~50 services.
- Test monitoring: synthetic series with assertions at three tiers (binary exports metrics, rules produce alerts, routing by labels); run a known-metrics exporter for rarely firing alerts.

## Variants and techniques
Logs vs metrics vs traces; push vs pull collection; hierarchical (federated) aggregation; synthetic probers.

## Trade-offs
High resolution costs storage and CPU; more signals mean more noise and maintenance (remove rarely used signals); client-side measurement is costlier but sees more.

## When to use it / when not to
Every production system. Keep it simple and comprehensible; a monitoring system that needs a dedicated team to understand is a liability.

## Note: what a senior/staff candidate should say
Name the golden signals for the system being designed, say what you page on (SLO burn, symptoms) versus put on dashboards (causes), mention percentile histograms rather than averages, blackbox probes plus whitebox metrics, and tracing with request IDs across services.

## Appears in
[[discord-voice-infrastructure]], [[metrics-monitoring]]

## See also
[[alerting-strategy]], [[slos-slis-and-error-budgets]], [[time-series-database]], [[incident-management-and-postmortems]]
