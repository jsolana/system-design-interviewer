---
title: Constant work pattern
type: concept
aliases: [constant work, anti-fragile systems, periodic full-state refresh]
sources: [https://aws.amazon.com/builders-library/reliability-and-constant-work/]
---

# Constant work pattern

## Definition
Design a system to do the same, predictable amount of work regardless of load, state changes or failures (analogy: a coffee urn is roughly O(1) vs brewing per cup O(N)).

## Why it matters
Variability causes failures: slowdowns lengthen queues, trigger retry storms ("spiral of doom"), and delayed fault response equals downtime. Constant-work systems do not have emergency modes and perform best when needed most.

## How it works
Three properties: (1) work does not scale with load or stress; (2) no modes, same code path always; (3) any variation under stress only reduces work.
- **Route 53 health checks**: fleet of checkers across Regions probes targets every few seconds; results go to aggregators (e.g. unhealthy only if >=3 checks fail); aggregators **push** a fixed-size status table (sized to max capacity, e.g. 10,000 slots with dummies) to DNS servers every few seconds; DNS servers scan all candidate answers even after finding a healthy one. A mass failure (AZ power loss) does not change the work. Rejected alternative: event-driven DNS record updates (an AZ failure could need millions).
- **NLB / Hyperplane configuration via S3**: customer changes are written to a config file in S3; nodes reload the **entire** file every few seconds even if unchanged, with pre-sized file/dummy slots. Losing nodes reduces S3 work.
- **Self-healing**: each cycle starts from clean state; corrupted or missed updates are fixed next pass, no backlog (workflows are edge-triggered and need retry/repair logic).
- Caches are a counter-example: they have modes (cold cache) and can look anti-fragile until over-stressed.

## Variants and techniques
Periodic full-state sync, pushing instead of pulling, fixed-size payloads, cellular architecture with tested per-cell limits.

## Trade-offs
Wasted work (negligible for health checks/config); web fleets are better with elastic scaling (peak capacity always on wastes resources, ~half the servers off-peak). Read O(1) as O(C). Simplicity = ease of understanding, not fewest parts.

## When to use it / when not to
Control planes, config propagation, health aggregation where urgency and scale peak during failures. Not for elastic request-serving fleets where cost matters more.

## Appears in
None yet.

## See also
[[retries-timeouts-and-backoff]], [[avoiding-fallback-in-distributed-systems]], [[shuffle-sharding-and-cell-based-architecture]], [[caching]], [[load-shedding-and-overload-handling]]

## Interview note (senior/staff)
For config/health propagation say: "level-triggered full-state push every N seconds beats event-driven deltas: fixed work, self-healing, no backlog, and failures reduce rather than increase load." Mention fixed-size payloads and call out that caches introduce modes.
