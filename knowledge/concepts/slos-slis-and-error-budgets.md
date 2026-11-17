---
title: SLIs, SLOs, SLAs and error budgets
type: concept
aliases: [SLO, SLI, SLA, error budget, availability nines, service level objectives]
sources: [https://sre.google/workbook/implementing-slos/, https://sre.google/workbook/slo-engineering-case-studies/, https://sre.google/sre-book/embracing-risk/, https://sre.google/sre-book/service-level-objectives/, https://sre.google/sre-book/monitoring-distributed-systems/]
---

# SLIs, SLOs, SLAs and error budgets

## Definition
- **SLI** (indicator): a precisely defined measurement of service quality (latency, error rate, throughput, availability, durability).
- **SLO** (objective): a target for an SLI, e.g. "99.9% of requests succeed" or "median latency < 100 ms".
- **SLA** (agreement): a contract with consequences (often financial) if missed. No consequence means it is really just an SLO.
- **Error budget**: 100% minus the SLO; the amount of unreliability you are allowed to spend on releases, experiments and failures.

## Why it matters
100% reliability is the wrong target: users' own devices and networks are less reliable (a 99% phone cannot tell 99.99% from 99.999%), and each extra nine costs far more engineering and resources. The SLO turns "how reliable?" into an explicit business decision and gives product and SRE teams an objective rule for trading velocity against stability.

## How it works
- **Availability formulas.** Time-based: uptime / total time (99.99% over a year = ~52.56 min downtime; 99.9% = ~9 h/year; 99.99% quarterly = ~13 min). Request-based: successful requests / total requests over a rolling window (preferred at Google, since global services are rarely fully down; 2.5M requests/day at 99.99% allows 250 errors).
- **Budget arithmetic.** A 99.999% SLO leaves a 0.001% budget; an incident failing 0.0002% of requests consumes 20% of it.
- **Policy.** While budget remains, ship. When it is exhausted, slow or freeze releases until reliability recovers. This makes product teams self-policing.
- **Control loop.** Measure SLI, compare to SLO, decide if action is needed, act.
- **Common SLIs by system type.** Serving: availability, latency, throughput. Storage: latency, availability, durability. Pipelines: throughput and end-to-end latency. All: correctness.
- **Percentiles, not averages.** Averages hide the tail (median 50 ms while 5% of requests are ~20x slower). Use 50th/99th/99.9th; a target can be a curve (90% < 1 ms, 99% < 10 ms, 99.9% < 100 ms). Use separate SLOs for interactive vs bulk traffic.
- **Choosing targets.** Start from what users care about; do not derive targets from current performance; keep few and simple; avoid absolute promises; start loose, tighten later. Keep an internal SLO tighter than the published SLA. Avoid overachieving (users start depending on it; Chubby ran planned outages).
- **Window and measurement.** Define aggregation interval, region, request filter and data source; measure client-side when server-side misses problems (slow JS).

## Additional detail (SRE Workbook, ch. 2-3)
Sources: https://sre.google/workbook/implementing-slos/, https://sre.google/workbook/slo-engineering-case-studies/
- **Specification vs implementation:** the spec is the user-centric outcome; implementations (server logs, load balancer metrics, synthetic probers, client instrumentation) trade quality, coverage and cost. Express every SLI as good events / total events (0-100%). Start with the cheapest relevant measurement; keep at most ~5 SLI types.
- **SLI menu:** request-driven = availability, latency (several thresholds, e.g. 90% < 100 ms and 99% < 400 ms), quality (undegraded share); pipelines = freshness, correctness, coverage ([[data-pipeline-reliability]]); storage = durability.
- **Starter SLO recipe:** measure over 7-28 days, round down (two significant digits, 50 ms steps), budget = 100% - SLO. Example: 3,663,253 requests, 97.123% good, p90 432 ms, p99 891 ms -> SLOs 97%, 90% < 450 ms, 99% < 900 ms; 97% leaves 109,897 failures. Budget consumed by an event = event errors / total budget (14,066 errors = ~13%).
- **Windows:** rolling four-week (whole weeks) matches user memory; calendar windows suit business planning (Evernote chose calendar months, 99.95%, counting maintenance as downtime).
- **Error budget policy:** agreed by product, dev and SRE; actions on exhaustion (prioritize reliability bugs, halt features, freeze changes); documented owners, rationale, escalation; reviewed monthly then quarterly. Aspirational SLOs can be tracked without triggering the policy.
- **Iteration:** compare outages and tickets against budget drops; SLO misses real problems -> tighten; flags trivia -> relax; else improve the SLI implementation. Decision matrix: SLO met + low toil + low satisfaction -> tighten; missed + high satisfaction -> loosen.
- **Advanced:** critical user journeys, bucketing by tier or request type, dependencies must be at least as reliable as the journey (shared failure domains break independence), relaxation experiments only with spare budget.
- **Case studies:** Evernote (external prober every minute, second geographic prober confirms, SLO on v3 after ~9 months, cut release windows 5 -> 2 by removing subjective risk calls). Home Depot (VALET: Volume, Availability, Latency, Errors, Tickets; only 5xx count; tiers 99.5/99.9/99.95/99.99%; ~50 to ~800 services in a year via BigQuery automation).
- Burn-rate paging on top of these SLOs: [[slo-burn-rate-alerting]].

## Variants and techniques
- Tiered service levels per client class (Bigtable low-latency vs throughput clusters; the throughput tier can cost 10-50% as much).
- Time-based vs request-based availability; rolling vs calendar windows.

## Trade-offs
- Each additional nine can cost ~100x more than the previous one.
- Worked example: a $1M/quarter service going from 99.9% to 99.99% gains ~$900 of value; spending more than that is not worthwhile.
- Tight SLOs slow feature delivery; loose SLOs risk user trust. Availability targets are both a floor and a ceiling.

## When to use it / when not to
Always define SLOs for user-facing services and storage; use them to drive alerting ([[alerting-strategy]]) and release gating ([[release-engineering-and-canary-deployments]]). Do not copy SLA numbers into SLOs without margin.

## Note: what a senior/staff candidate should say
State the SLO up front (e.g. "99.95% monthly, p99 < 300 ms for reads"), derive the error budget in minutes or requests, tie it to design choices (multi-AZ vs multi-region, sync vs async replication), say that a dependency chain multiplies availabilities (three 99.9% hops = ~99.7%), and mention that exhausting the budget freezes launches.

## Appears in
[[metrics-monitoring]], [[payment-system]], [[youtube]]

## See also
[[observability-and-monitoring]], [[alerting-strategy]], [[capacity-planning]], [[scalability-reliability-maintainability]], [[back-of-the-envelope-estimation]]
