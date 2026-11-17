---
title: Autoscaling and load management
type: concept
aliases: [autoscaling pitfalls, load shedding with autoscaling, global load balancing, anycast, retry jitter]
sources: [https://sre.google/workbook/managing-load/]
---

# Autoscaling and load management

## Definition
Combining global load balancing, autoscaling and load shedding so a service absorbs demand spikes without feedback loops that turn partial failure into an outage.

## Why it matters
Each mechanism is sound alone but destructive when composed without coordination.

## How it works
**Global load balancing (GCLB example):** anycast single VIP routes users to nearest frontend (no DNS geolocation, longer TTLs); Maglev packet-level balancer (ECMP, consistent hashing, connection tracking, N+1 redundancy); a global scheduler matches demand to cluster capacity and drains failed clusters; frontends terminate TLS, route by header/path, health-check, and use lame-duck mode for graceful removal. See [[load-balancer]].

**Autoscaling pitfalls**
- Unhealthy/slow-starting instances skew average metrics: use cool-downs, autohealing, LB-observed capacity.
- Stateful or sticky traffic: more instances do not help; use consistent-hash routing.
- Scale-up aggressive, scale-down conservative.
- Runaway scaling from CPU-bound bugs or stuck dependencies until quota is exhausted.
- Scaling the frontend overloads databases and dependencies: analyze dependency capacity first.
- Shared quota lets one service starve others; use per-service quotas, regional instance groups for zone balance.
- Set min/max matching quota, stay well below bottlenecks, keep a documented kill switch and manual override.

**Load shedding:** set thresholds so autoscaling triggers first; put deadlines on RPCs so servers stop work abandoned by clients.

**Feedback loops:** a case study where shedding returned cheap errors, making the balancer believe region A was most efficient; it got 400 RPS vs 40 for the others and mostly failed with 503. Fix: count errors as high (about 120%) CPU utilization so load spreads.

**Pokemon GO lessons:** load-tested to 5x the optimistic estimate, real load reached about 50x; SYN flood and proxy limits forced migration to a global LB; backend timeouts caused LB retries, cutting frontend capacity ~50%; clients with immediate retries and constant backoff synchronized into spikes ~20x the prior peak. Fixes: isolate and expand a frontend pool, admin rate limits, client jitter plus truncated exponential backoff.

## Variants and techniques
Rate limiting ([[rate-limiting]]), backoff with jitter, retry budgets and circuit breakers ([[overload-and-metastable-failures]]), pre-planned mitigation flags.

## Trade-offs
Headroom (cost) vs resilience; fast scale-up vs flapping; shedding protects servers but can mislead balancers.

## When to use it / when not to
Any elastic service. Do not rely on autoscaling for sudden spikes (instance startup latency); pre-provision for known events.

## Note: what a senior/staff candidate should say
"Autoscaling is slow, so I keep headroom, shed load beyond it, bound retries with jitter and exponential backoff, and check downstream capacity before scaling the frontend." Mention load-testing well above forecast and kill switches.

## Appears in
[[distributed-rate-limiter]]

## See also
[[load-balancer]], [[rate-limiting]], [[overload-and-metastable-failures]], [[horizontal-vs-vertical-scaling]], [[slos-slis-and-error-budgets]]
