---
title: Reliability, scalability and maintainability (load and percentiles)
type: concept
aliases: [load parameters, tail latency, percentiles, SLO, SLA, p99, scaling up/out]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 1 (pp. 3-22)]
---

# Reliability, scalability and maintainability (load and percentiles)

## Definition
DDIA's three design goals for data-intensive applications: **reliability** (continuing to work correctly despite hardware, software and human faults), **scalability** (the ability to cope with more load) and **maintainability** (operability, simplicity, evolvability).

## Why it matters
It provides the vocabulary to reason about non-functional requirements: "scalable" is not a binary label; you have to say *how* the system grows and what options exist to absorb it.

## How it works
- **Load parameters**: a few numbers that describe the load (req/s, read/write ratio, active users, cache hit rate...). Twitter example (2012): 4.6k tweets/s on average (12k peak) vs 300k timeline reads/s; the challenge is *fan-out* (average ~75 followers/tweet -> 345k writes/s to timelines; some users have >30M followers).
- **Performance**: throughput (batch) vs response time (online). Response time = service time + queueing + network; it is a *distribution*, not a single number.
- **Percentiles** instead of the mean: p50 (median), p95, p99, p999. Tail latencies matter: Amazon sets targets at p99.9 because the slowest customers are often the most valuable; optimizing p99.99 was judged too expensive.
- **Tail latency amplification**: if a user request makes N backend calls, the slowest one is enough to slow it down; the probability of seeing a slow call grows with N.
- **Head-of-line blocking**: a few slow requests hold up the ones behind them; measure latency on the client and generate test load without waiting for the previous response.
- Compute percentiles continuously: sliding window; approximations (forward decay, t-digest, HdrHistogram). **Do not average percentiles**: add histograms instead.
- **SLO/SLA**: e.g. median < 200 ms, p99 < 1 s, availability 99.9%.

## Variants and techniques
- Scaling up (vertical) vs scaling out (horizontal, shared-nothing); elastic systems vs manual scaling (simpler, fewer surprises).
- Stateless services are easy to distribute; stateful ones add a lot of complexity, hence the rule of keeping the DB on a single node until cost or HA force otherwise.
- Reliability: tolerate faults (do not confuse *fault* with *failure*), hardware (redundancy), software (correlated systematic errors), humans (sandbox, fast rollback, gradual rollout, monitoring).
- Maintainability: operability, simplicity (abstractions that remove accidental complexity), evolvability.

## Trade-offs
- There is no "magic scaling sauce": the architecture depends on which operations are common and which are rare; 100k req/s of 1 kB is very different from 3 req/min of 2 GB.
- In startups, favor iteration over scaling for a hypothetical load.

## When to use it / when not to
At the start of any interview: define load parameters and latency targets (percentiles) before choosing an architecture.

## Appears in
[[fb-news-feed]]

## See also
[[fan-out]], [[caching]], [[database-partitioning]], [[replication]]
