---
title: Data pipeline reliability
type: concept
aliases: [pipeline SLOs, freshness SLI, pipeline failure modes, idempotent pipelines]
sources: [https://sre.google/workbook/data-processing/, https://sre.google/workbook/implementing-slos/]
---

# Data pipeline reliability

## Definition
Operating batch and streaming data pipelines to explicit SLOs (freshness, correctness, completeness) and designing them to tolerate delay, corruption, hotspots and regional failure.

## Why it matters
Users care about the end-to-end result, not per-stage health. Pipelines fail silently (stale or wrong data) unlike request-driven services that fail loudly.

## How it works
**SLIs**
- Freshness: X% of data processed within Y (e.g. 99% of actions reflected within 30 min; new products in recommendations within 12 h); oldest-record age; job completed in time.
- Correctness: compare against golden data from test accounts; backward-looking targets (<= 0.1% wrong invoices per quarter).
- Completeness/coverage: share of published events delivered (audit daily); count expected vs processed.
- Skewness: max share of data in the wrong time bucket.
- Measure freshness with a watermark close to the user, not periodic queries.

**Design patterns**
- Streaming (e.g. Dataflow) starts downstream work early, lower latency than batch stages that wait for predecessors. Starting with batch behind an interchangeable API eases later migration.
- Gate jobs on their inputs finishing; split big pipelines into smaller independently released ones.
- **Idempotent mutations** so reruns do not duplicate; **two-phase mutation** (stage proposed changes, validate, then apply).
- **Checkpointing** to resume after failure/preemption and to reprocess selectively.
- Holistic view: per-stage checks miss a stage silently dropping a field.

**Failure modes and responses**
- Delayed data: stall rather than process incomplete input; stale is almost always better than incorrect.
- Corrupt data: stop the bleeding, then restore known-good version or reprocess.
- Hotspots (hot tablet, lock contention, oversized work unit): block bad fine-grained data, split work dynamically, restructure access.
- Overload: many workers on one serving task; cap autoscaler (Spotify capped instances after runaway scaling); size to ~50% CPU at peak.
- Regional failure: automatic failover or practiced manual failover (needs spare capacity elsewhere); failed failover can extend the outage.
- Canary pipeline changes with ramp 1% -> 10% -> 50% -> 100%, canary at least one work unit long.

## Variants and techniques
Periodic batch, continuous streaming, staged event delivery (Spotify: hourly buckets, 3-step ETL, tiered timeliness priorities, clients buffer events up to 30 days).

## Trade-offs
Streaming latency vs complexity; strict gating (delay) vs freshness; full reprocessing cost vs correctness.

## When to use it / when not to
Any ETL, ML feature, analytics or billing pipeline. For one-off jobs, SLOs may be overkill.

## Note: what a senior/staff candidate should say
Define freshness, correctness and completeness SLOs, make stages idempotent and checkpointed, prefer stalling over propagating bad data, and plan replay/backfill and regional failover. Links: [[batch-processing]], [[stream-processing]], [[exactly-once-processing]].

## Appears in
[[ad-click-aggregator]]

## See also
[[batch-processing]], [[stream-processing]], [[exactly-once-processing]], [[slos-slis-and-error-budgets]], [[workflow-orchestration]]
