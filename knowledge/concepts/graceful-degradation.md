---
title: Graceful degradation
type: concept
aliases: [degraded mode, fallbacks, partial availability, feature flags kill switch]
sources: [https://sre.google/sre-book/addressing-cascading-failures/, https://sre.google/sre-book/handling-overload/, https://sre.google/sre-book/embracing-risk/]
---

# Graceful degradation

## Definition
Returning cheaper or lower-quality results, or dropping non-essential features, under load or partial failure instead of failing outright.

## Why it matters
Serving a worse answer to everyone beats timing out for many; it also breaks the feedback loop of [[cascading-failures]].

## How it works
- Reduce work per request: search a cache subset instead of the full corpus, use a cheaper ranking algorithm, skip personalization.
- Trigger it from load signals (CPU, queue length, in-flight count) and shed by criticality ([[load-shedding-and-overload-handling]]).
- Serve stale cached data when the source is down; hide optional components that depend on a failing backend.
- Operational cautions: degraded modes are rarely exercised, so test them regularly, monitor how many servers are in them, keep a fast way to disable complex logic, and make sure the system exits degraded mode on its own.

## Variants and techniques
Stale-while-revalidate, static fallback pages, read-only mode, disabling batch/background work, fail-fast for non-critical dependencies, tiered service for different clients.

## Trade-offs
Added code paths are untested complexity (simplicity principle: every line is liability); quality drop may confuse users; can mask capacity problems if not alerted on.

## When to use it / when not to
Use for features with a meaningful cheaper alternative (feeds, search, recommendations). Not for correctness-critical operations (payments), where you fail or queue instead.

## Note: what a senior/staff candidate should say
Define, per feature, what the degraded version is and who decides (automatic on load, or manual kill switch). Example: a feed serves cached or non-personalized results; checkout stays strict.

## Appears in
[[distributed-rate-limiter]], [[uber]], [[youtube]]

## See also
[[cascading-failures]], [[load-shedding-and-overload-handling]], [[caching]], [[cap-theorem]]
