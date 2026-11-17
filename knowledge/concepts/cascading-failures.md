---
title: Cascading failures
type: concept
aliases: [cascade, retry storm, GC death spiral, crash loop, queries of death]
sources: [https://sre.google/sre-book/addressing-cascading-failures/, https://sre.google/sre-book/handling-overload/]
---

# Cascading failures

## Definition
A failure that grows by positive feedback: one component failing raises the failure probability of the others (typically by shifting its load onto them).

## Why it matters
It turns a partial failure (one cluster) into a global outage, and recovery is hard because restarted servers are hit by the full backlog of load.

## How it works
Common causes:
- **Server overload**: the most common trigger; a failed cluster's traffic lands on the rest.
- **Resource exhaustion**: CPU (slower requests, more concurrency, queues, missed deadlines, colder caches); memory (more in-flight requests, tasks killed, Java GC death spiral, smaller caches); threads (starvation, failed health checks); file descriptors (no new connections).
- **Unavailability**: crashes push load to survivors, leading to crash-looping; restarted tasks get slammed and die again.
- **Slow startup and cold caches**: new tasks or flushed caches cannot take full load; a cache needed for capacity is a hard dependency.
- **Retry storms** and unbounded queues ([[retries-timeouts-and-backoff]]).

Prevention checklist: load test to failure (find which resource exhausts first); serve degraded results ([[graceful-degradation]]); reject early ([[load-shedding-and-overload-handling]]); rate-limit at proxies/balancers; N+2 capacity planning ([[capacity-planning]]); short queues; deadlines and cancellation propagation; avoid same-layer cross-calls; warm-up ramps.

Immediate mitigation: add capacity if available; disable health-check-driven restarts that make things worse (separate process health from service health); restart only after finding the cause and roll out slowly; drop traffic aggressively then ramp up gradually so caches warm; enter degraded modes; pause batch jobs; block queries of death.

Testing: stress each component gradually and with spikes, verify it leaves degraded mode by itself, find how far load must fall for a crashed fleet to stabilize, test hung (not failed) non-critical backends and popular clients' backoff.

## Variants and techniques
Bimodal latency (a few hung requests exhaust threads: fail fast, cap per-client share), cross-layer cascades, cache-miss stampedes, metastable states ([[overload-and-metastable-failures]]).

## Trade-offs
Changes meant to improve normal operation (retries, caches, aggressive health checks) increase cascade risk. Allowing some errors beats trying to serve everything.

## When to use it / when not to
Think about it in every design with fan-out, shared dependencies or multi-cluster failover.

## Note: what a senior/staff candidate should say
When proposing failover, ask "does the surviving capacity absorb the failed region's load?" (N+1 vs N+2), then name the breakers: load shedding, jittered backoff with retry budgets, deadlines, circuit breaking, cell isolation ([[multitenancy-and-cell-based-architecture]]).

## Appears in
[[uber]]

## See also
[[load-shedding-and-overload-handling]], [[graceful-degradation]], [[retries-timeouts-and-backoff]], [[multi-data-center]]
