---
title: Capacity planning
type: concept
aliases: [intent-based capacity planning, N+2 provisioning, headroom, Auxon]
sources: [https://sre.google/sre-book/software-engineering-in-sre/, https://sre.google/sre-book/addressing-cascading-failures/, https://sre.google/sre-book/handling-overload/, https://sre.google/sre-book/monitoring-distributed-systems/]
---

# Capacity planning

## Definition
Forecasting demand and provisioning enough resources, with redundancy, to meet SLOs ([[slos-slis-and-error-budgets]]) through growth, failures and maintenance.

## Why it matters
Under-provisioning causes overload and cascades; over-provisioning wastes money. Traditional planning (collect forecasts, build allocation plan, sign off, deploy) is brittle: one change in efficiency, adoption or a delayed cluster ripples through later quarters.

## How it works
- **Redundancy**: plan N+2 (survive planned maintenance plus an unplanned failure), validate with load tests; this does not fully prevent cascades.
- **Convert demand to resources**: performance metrics from load tests and monitoring map high-level demand (users, requests) to CPU, memory, storage. Provision on CPU primarily; QPS is a poor unit as query cost drifts.
- **Utilization target below 100%**, since latency degrades earlier (saturation signal).
- **Intent-based planning (Auxon)**: encode requirements declaratively (e.g. regional demand with N+2, a dependency within 30 ms latency), feed forecasts, performance data, supply and prices to a solver (linear or mixed-integer program; bin packing is NP-hard so spreadsheets only approximate) and regenerate the allocation plan when inputs change. Output lists unmet requirements and trade-offs explicitly by priority.
- Engineering lessons: start with a simple heuristic solver behind an interface, stay agnostic of forecasting tools, do not chase 100% adoption.
- **Cold start**: new tasks/caches need over-provisioning or warm-up ramps.

## Variants and techniques
Organic growth vs event-driven (launches) forecasting, autoscaling for short-term, reserved capacity for critical traffic, overbooked quotas ([[load-shedding-and-overload-handling]]).

## Trade-offs
Headroom cost vs outage risk; autoscaling lag vs spikes; centralized solver complexity vs spreadsheet fragility.

## When to use it / when not to
Always for stateful or slow-to-provision resources; autoscale stateless tiers but keep a floor and a ceiling.

## Note: what a senior/staff candidate should say
Tie estimates to [[back-of-the-envelope-estimation]], state peak-to-average ratio, headroom (e.g. 30-50%), N+2 across zones, and what you shed if a region is lost.

## Appears in
[[uber]]

## See also
[[back-of-the-envelope-estimation]], [[horizontal-vs-vertical-scaling]], [[cascading-failures]], [[multi-data-center]]
