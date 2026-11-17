---
title: Circuit breaker
type: concept
aliases: [circuit breaking, Hystrix pattern]
sources: [https://martinfowler.com/bliki/CircuitBreaker.html, https://microservices.io/patterns/reliability/circuit-breaker.html, https://blog.pragmaticengineer.com/resiliency-in-distributed-systems/]
---

# Circuit breaker

## Definition
A proxy/wrapper around a remote (or risky) call that counts failures and, past a threshold, fails calls immediately instead of invoking the unhealthy dependency, so callers do not pile up on it and the failure does not cascade.

## Why it matters
A synchronous caller of a slow or dead service can exhaust its threads/connections and fail too ([[cascading-failures]]). Failing fast frees resources and gives the dependency room to recover.

## How it works
Three states:
- **Closed**: calls pass; failures counted, a success resets the count.
- **Open**: after N failures, calls return an error without touching the supplier for a reset timeout.
- **Half-open**: after the timeout a limited trial call is allowed; success closes the breaker, failure re-opens it (timer restarts).
Parameters (Fowler's toy example): invocation timeout (slow = failure), failure threshold (5), reset timeout (0.1 s); real ones are workload-specific. Microservices.io example: Hystrix with an 800 ms timeout.

## Variants and techniques
- Trip on failure **rate** (e.g. 50%) rather than count; different thresholds per error type; not every error (business outcomes) should count.
- Async systems: trip when the request queue is full or a thread pool is exhausted.
- Operability: log and alert on state changes, expose state, allow manual trip/reset.
- Client behaviour when open: fail the operation, queue for later (e.g. card authorization), or serve stale data ([[graceful-degradation]]).
- Pragmatic Engineer (Understanding Distributed Systems excerpt): retries suit faults likely to succeed next time, circuit breakers suit faults likely to keep failing.

## Trade-offs
- Timeout/threshold tuning is hard: too aggressive gives false positives, too lenient adds latency (microservices.io).
- Adds modal behaviour that is hard to test and can slow recovery (see [[retries-timeouts-and-backoff]]).

## When to use it / when not to
Service-to-service synchronous calls, API gateways, discovery routers. Pair with timeouts, bounded retries with jitter and fallbacks; unnecessary for calls with a single in-process failure domain.

## Appears in
None yet.

## See also
[[retries-timeouts-and-backoff]], [[cascading-failures]], [[overload-and-metastable-failures]], [[load-shedding-and-overload-handling]], [[api-gateway]], [[microservices-architecture]]

## Note: what a senior/staff candidate should say
Frame it as one layer of defence: timeouts first, retries with budget and jitter, then a breaker plus a defined fallback; explain who is protected (caller resources and callee recovery) and how you would monitor trips.
