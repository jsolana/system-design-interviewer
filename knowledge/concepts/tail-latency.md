---
title: Tail latency and percentiles
type: concept
aliases: [percentile latency, p99, coordinated omission, latency SLA]
sources: [https://danluu.com/percentile-latency/, https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html, https://blog.pragmaticengineer.com/resiliency-in-distributed-systems/]
---

# Tail latency and percentiles

## Definition
The slowest slice of requests (p99, p99.9, p99.99) as opposed to the average. Service levels are best expressed on percentiles.

## Why it matters
- Averages hide the worst cases; slow responses cost money because users leave (Dan Luu).
- Dynamo set its SLAs at the 99.9th percentile so that all customers, not just the majority, get good experience (Vogels).
- Timeouts can be derived from a downstream percentile (e.g. its p99.9 to accept a small false-timeout rate; Pragmatic Engineer excerpt).

## How it works / measuring
- **Coordinated omission**: a benchmark that waits for each response before sending the next never records requests that would have queued during a stall. Luu's example: 10,000 requests at 1 ms plus one 10 s stall in a 20 s run reports p99 of 1 ms, but randomly arriving real users would see p75 of at least 5 s. Yahoo's YCSB had this flaw; after correction results differed by more than an order of magnitude. Use open-loop load and HdrHistogram.
- Optimizing only chosen percentile targets can push latency up elsewhere (latency flat below a threshold, sharp rise above it); look at the whole distribution.
- Example targets in the article: p99 < 0.5 ms and p99.99 < 5 ms.

## Variants and techniques
Study the distribution, not a few points; measure from the client; set SLOs on percentiles ([[slos-slis-and-error-budgets]]); hedged requests and bounded retries ([[retries-timeouts-and-backoff]]). (Fan-out amplification is not discussed in these sources.)

## Trade-offs
Tight percentile goals cost capacity (lower utilization, over-provisioning) and complexity; high percentiles need many samples to measure.

## When to use it / when not to
Always use percentiles for user-facing latency requirements; averages only for throughput/capacity math.

## Appears in
[[distributed-cache]]

## See also
[[performance-analysis-methods]], [[network-latency-and-bandwidth]], [[observability-and-monitoring]], [[overload-and-metastable-failures]]

## Note: what a senior/staff candidate should say
State latency requirements as "p99 under X ms at Y QPS", explain that queueing near saturation dominates the tail, and mention measurement pitfalls (coordinated omission) when discussing load tests.
