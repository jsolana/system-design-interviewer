---
title: Timeouts, retries, backoff with jitter (and the UNKNOWN outcome)
type: concept
aliases: [retry storm, exponential backoff, jitter, retry budget, hedged requests, retries]
sources: [https://blog.pragmaticengineer.com/resiliency-in-distributed-systems/, https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/, https://aws.amazon.com/builders-library/challenges-with-distributed-systems/, https://sre.google/sre-book/handling-overload/, https://sre.google/sre-book/addressing-cascading-failures/]
---

# Timeouts, retries, backoff with jitter (and the UNKNOWN outcome)

## Definition
The three client-side tools for surviving failed remote calls without turning a small failure rate into an outage: **timeouts** bound how long a call may hold resources, **retries** recover from transient/partial failures, **backoff + jitter** space retries out and de-synchronize clients.

## Why it matters
Remote calls always fail sometimes; every step of a request/reply round trip (post, deliver, validate, update state, reply...) can fail independently because client, network and server do not share fate. A timeout yields **UNKNOWN**: the server may have processed the request, not received it, or failed. Naive retries then amplify load on an already struggling dependency.

## How it works
- **Timeouts**: set on every remote call (even same-host), both connect and request timeout. Too high holds threads/connections/ports; too low causes extra retries and can cascade. Pick an acceptable false-timeout rate (e.g. 0.1%) and use the matching downstream latency percentile (p99.9); add network latency for cross-Region/internet; pad when p99.9 is close to p50. Gotchas: some timeouts exclude DNS/TLS; connection setup counted against a 20 ms timeout caused post-deploy failures (fix: open connections at startup).
- **Retries**: help with partial and short transient failures but are "selfish" (spend server capacity for one caller's odds). Amplification: 5 layers x 3 retries = 3^5 = 243x load on the bottom dependency -> retry at one layer only for cheap operations.
- **Limiting retries**: cap attempts; **local token bucket** (retry while tokens remain, then a fixed slow rate; added to AWS SDK in 2016); circuit breakers stop calls past an error threshold but add hard-to-test modal behavior and can slow recovery. Only retry when the dependency seems healthy; alarm on rising retry rate.
- **Idempotency**: a timeout does not prove no side effect; retry side-effecting calls only if idempotent (e.g. client token on EC2 RunInstances). Retry 5xx, not 4xx (eventual consistency blurs this).
- **Backoff**: exponential, capped (cap makes all clients retry at the same constant rate).
- **Jitter**: randomize waits so clients do not re-synchronize. Also jitter periodic jobs/timers; for scheduled work prefer a stable per-host offset over fresh randomness (reproducible, debuggable). Jittering EBS/Lambda cron-like clients reduced needed server capacity.
- **Hedging / proactive retry**: send in parallel and take the first reply; quorum reads are an always-on form that keeps load constant.
- **Handle every outcome explicitly** in client code: POST_FAILED (definitely not received, safe to retry), RETRYABLE, FATAL, UNKNOWN (timeout; needs idempotency or read-back), SUCCESS (validate reply, tolerate corrupt/incompatible replies).
- **Deadline propagation**: pass remaining time downstream so servers drop work whose client already gave up (see [[load-shedding-and-overload-handling]]).

## Variants and techniques
Full jitter / equal jitter, token-bucket retry budgets, circuit breakers, hedged requests, deadline propagation.

## Trade-offs
- Retries raise success under transient errors but deepen overload; breakers protect but add modes.
- Testing: each call has ~5 outcomes, multiplying test matrices (10 scenarios x 20 permutations = 200 tests in the article's example).
- Failures recur at every level (machine, group, Region), so bugs stay latent for months and spread over the network.

## When to use it / when not to
Retry only idempotent, transient-failure-prone calls, at one layer, with budget and jitter. Do not retry on overload signals (429) in synchronous paths: fail fast.

## Additional detail (Google SRE Book, ch. 21-22)
- **Per-request cap**: at most 3 attempts. **Per-client retry budget**: retry only while retries are below ~10% of requests; worst-case growth falls from ~3x to ~1.1x.
- **Single retry layer**: retry only at the layer directly above the rejecting one; per-layer retries multiply (3 layers x 3 attempts = 27x). Return a distinct "overloaded, do not retry" error upward; backends can emit it when attempt-count histograms show the whole datacenter is overloaded. Do not retry permanent errors.
- **Deadlines**: always set one; check at each stage and drop expired work; propagate the remaining time and cancellations down the RPC tree; fail fast and cap per-client thread share against bimodal latency (a few hung requests exhausting threads).
- Retries act as implicit load balancing to healthier tasks, at the cost of extra load. See [[cascading-failures]], [[load-shedding-and-overload-handling]].

## Additional detail (Pragmatic Engineer / Understanding Distributed Systems excerpt)
Source: https://blog.pragmaticengineer.com/resiliency-in-distributed-systems/. Set a timeout on every network call (many clients default to infinite); choose it from a target false-timeout rate, e.g. the downstream p99.9. Retry only likely-transient errors and check idempotency first; retry at one layer only (multi-layer retries multiply load). Capped exponential backoff plus jitter avoids synchronized retry storms. Retries suit faults that will probably succeed next time; [[circuit-breaker]] suits faults that will probably keep failing. Load shedding: reject excess quickly (HTTP 503), prioritize which to drop; rate limiting uses 429 + Retry-After and shared state.

## Appears in
[[distributed-message-queue]], [[job-scheduler]], [[notification-system]], [[payment-system]]

## See also
[[idempotency]], [[overload-and-metastable-failures]], [[load-shedding-and-overload-handling]], [[avoiding-fallback-in-distributed-systems]], [[distributed-system-faults]], [[rate-limiting]]

## Interview note (senior/staff)
Say: "Every remote call gets a timeout derived from downstream p99.9, retries happen at a single layer with exponential backoff, full jitter and a retry budget, only for idempotent operations (idempotency keys), and deadlines propagate so downstream stops doomed work." Mention the 3^5 amplification example and that a timeout is UNKNOWN, not failure. Call out that retry policy is part of the capacity plan.
