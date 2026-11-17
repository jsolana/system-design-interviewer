---
title: Overload, retry storms and metastable failures
type: concept
aliases: [metastable failure, retry storm, exponential backoff, circuit breaker, load shedding, backpressure, cascading failure]
sources: [https://sre.google/workbook/managing-load/, Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 2 (pp. 38-47), https://sre.google/sre-book/handling-overload/]
---

# Overload, retry storms and metastable failures

## Definition
*2nd edition (new).* Near capacity, response time rises sharply because of queueing. A system can then fall into a vicious cycle (clients time out and resend, raising load) and stay overloaded even after the original load drops until it is reset: a **metastable failure**.

## Why it matters
It explains many real outages and why retries, timeouts and queue limits must be designed, not defaulted.

## How it works
- Throughput near the hardware maximum -> queueing delay explodes -> timeouts -> retries -> more load (**retry storm**).
- Client-side mitigations: **exponential backoff with jitter** (randomized), **circuit breaker** (stop sending to a service that recently errored/timed out), **token bucket** for retries.
- Server-side: **load shedding** (reject proactively when approaching overload), **backpressure** (tell clients to slow down), good queueing/load-balancing algorithms.
- Related software-fault patterns: cascading failures, runaway processes that exhaust shared resources, avoiding feedback loops.

## Variants and techniques
Measure response time on the client (queueing is not in service time); fault injection / chaos engineering to exercise error handling ([[distributed-systems-testing]]).

## Additional detail (SRE Workbook, ch. 11 Managing Load)
Source: https://sre.google/workbook/managing-load/. Real-world retry storm: Pokemon GO clients with immediate retries and constant backoff synchronized into spikes ~20x the previous global peak, and load balancer retries after backend timeouts halved frontend capacity; fix was jitter plus truncated exponential backoff and admin rate limits. Load shedding combined with load balancing can mislead the balancer (cheap error responses look "efficient"; count errors as high CPU). Set shedding thresholds above the autoscaling trigger and put deadlines on RPCs. More in [[autoscaling-and-load-management]].

## Trade-offs
Shedding load loses requests but protects the rest; aggressive retries improve success on transient errors but amplify overload.

## When to use it / when not to
Always for services with retries/fan-out; backoff and breakers matter most for internal service-to-service calls.

## Appears in
None yet.

## See also
Google SRE Book treatment in dedicated files: [[load-shedding-and-overload-handling]], [[cascading-failures]], [[retries-timeouts-and-backoff]], [[graceful-degradation]].

[[retries-timeouts-and-backoff]], [[load-shedding-and-overload-handling]], [[constant-work-pattern]], [[rate-limiting]], [[idempotency]], [[scalability-reliability-maintainability]], [[distributed-system-faults]]
