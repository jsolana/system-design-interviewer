---
title: Avoiding fallback in distributed systems (failover vs fallback)
type: concept
aliases: [fallback, failover vs fallback, untested code paths, graceful degradation caveats]
sources: [https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/]
---

# Avoiding fallback in distributed systems

## Definition
**Fallback** = using a *different* mechanism to produce the same result when the primary path fails. Amazon rarely uses it because rarely exercised paths are untested and often make outages worse. Contrast with retry (same call again), hedging (parallel requests, first answer wins) and failover (another copy of the same endpoint).

## Why it matters
Fallbacks are hard to test (multi-machine overload is hard to reproduce), only improve odds, can themselves fail, enlarge blast radius, and hide latent bugs for months or years.

## How it works
Case study (2001 retail outage): shipping-speed feature queried a supply-chain DB; a per-server cache was added with fallback "if cache unhealthy, hit the DB". It worked for months; then caches failed together, all servers hit the DB, it locked up, taking down the whole site and fulfillment centers sharing it. Single-cache failure tests could not reveal this. If the DB could take the fallback load, the cache was not needed.

## Variants and techniques (alternatives)
1. Make the primary path more reliable (e.g. use DynamoDB instead of layering two stores).
2. Return the error and let the caller retry (SDK/CLI retries).
3. **Push data proactively** so no remote fetch is needed (EC2 IAM role credentials are pushed, valid many hours, surviving push outages).
4. **Convert fallback to failover**: run both paths all the time (e.g. randomly choose) so both are exercised.
5. Keep retries/timeouts from becoming a hidden fallback: monitor retry rates; use hedging/quorum for constant load.
Single machine: prefer fail-fast crash, or pre-allocate memory at startup.

## Trade-offs
Less "graceful" behavior in exchange for predictability; requires investing in primary path availability.

## When to use it / when not to
Avoid fallbacks that activate only in chaos. If one is essential, exercise it constantly in production and load-test it.

## Appears in
None yet.

## See also
[[retries-timeouts-and-backoff]], [[constant-work-pattern]], [[static-stability]], [[caching]], [[overload-and-metastable-failures]]

## Interview note (senior/staff)
When asked "what if the cache/service is down?" do not just say "fall back to the DB". Say what load the DB sees when the whole cache fleet is cold, and prefer shedding, stale serving (soft/hard TTL), pushed data, or always-on dual paths; state that untested failure paths are a liability.
