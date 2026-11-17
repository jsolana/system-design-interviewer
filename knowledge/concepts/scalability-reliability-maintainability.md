---
title: Reliability, scalability and maintainability (load and percentiles)
type: concept
aliases: [load parameters, tail latency, percentiles, SLO, SLA, p99, scaling up/out]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 1 (pp. 3-22), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 2 (pp. 33-56)]
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

## Additional detail (DDIA 2nd edition, ch. 2)
- *2nd edition note*: chapter 1 of the 1st edition became "Defining Nonfunctional Requirements" (ch. 2) and now opens with the **home-timeline case study** (see [[materialized-views]]): 5,800 posts/s avg (150k peak), ~200 followers -> ~1M timeline writes/s vs 400M lookups/s when polling.
- Terminology: **response time** (client view) = **service time** + **queueing delay** + **network latency**; "latency" = any time the request is latent. Jitter = variation of network delay. The mean is useful for estimating throughput limits but not for "typical" time.
- Percentile estimation libraries: HdrHistogram, t-digest, OpenHistogram, DDSketch. Latency impact studies are shown to be unreliable (conflicting numbers); Yahoo: 20-30% more clicks when fast vs slow by >=1.25 s.
- **New**: overload dynamics, retry storms, metastable failures, backoff, circuit breakers, load shedding ([[overload-and-metastable-failures]]).
- Reliability numbers: 2-5% of HDDs fail per year (10,000 disks -> ~1 failure/day); SSDs 0.5-1%/year with ~1 uncorrectable error/year/drive; ~1 in 1,000 machines has a CPU core that occasionally computes wrong results; >1% of machines hit an uncorrectable RAM error per year even with ECC. Hardware faults are weakly independent; software faults are strongly correlated (leap-second bug 2012, SSD firmware dying after 32,768 hours). Availability zones group co-located resources; rolling upgrades.
- **Fault injection / chaos engineering** to exercise fault tolerance ([[distributed-systems-testing]]).
- Scalability: **shared-memory** (vertical, cost grows faster than linear), **shared-disk** (NAS/SAN, limited by locking), **shared-nothing** (horizontal, needs sharding); cloud-native systems separate storage and compute, similar to shared-disk without its problems ([[cloud-native-architecture]]). Linear scalability = 2x resources for 2x load. Plan at most one order of magnitude ahead; manual scaling can have fewer surprises than autoscaling.
- Maintainability is detailed as operability (automation is a double-edged sword), simplicity and evolvability.

## Appears in
[[fb-news-feed]]

## See also
[[fan-out]], [[caching]], [[database-partitioning]], [[replication]]
