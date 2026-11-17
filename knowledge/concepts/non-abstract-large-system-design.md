---
title: Non-abstract large system design (NALSD)
type: concept
aliases: [NALSD, capacity-driven design, iterative design with resource estimation]
sources: [https://sre.google/workbook/non-abstract-design/]
---

# Non-abstract large system design (NALSD)

## Definition
An iterative method: start from SLO-style requirements, sketch a design, compute concrete resources (machines, disks, IOPS, bandwidth), find the next bottleneck, and refine until the design is possible, feasible and resilient.

## Why it matters
Hand-wavy boxes hide the constraint that really shapes the design (often IOPS or RAM, not capacity). It is the core of a senior-level estimation-driven answer.

## How it works
At each iteration ask: Is it possible? Can we do better? Is it feasible? Is it resilient?

Worked example (ad click-through-rate reporting):
- Requirements: 99.9% of dashboard queries < 1 s; 99.9% of the time data < 5 min old; 500k queries/s, 10k clicks/s.
- Estimates: 2 KB/query log -> ~86.4 TB/day (~100 TB); clicks ~2% of queries (2% CTR); unbatched writes need ~2,500 HDDs at 200 IOPS (IOPS-bound); 100 TB in RAM at 64 GB/machine = ~1,563 machines; consensus (Paxos ~25 ms/op) allows ~40 sequential ops/s per process.
- Iterations: (1) one machine: rejected (SPOFs, storage/IOPS/RAM); (2) MapReduce batch: scales but batch boundaries split queries from clicks and miss the 5-min freshness; (3) a log joiner with query store and click/query maps joining on demand, single site; (4) shard by hashing query_id (log sharder) and ad_id for the maps, replicas on different machines; (5) multi-datacenter with 3 or 5 consensus replicas to survive a datacenter loss.
- Principles: reasonable assumptions are fine; separate components by growth rate; each iteration exposes new constraints.

## Variants and techniques
See [[back-of-the-envelope-estimation]] for the arithmetic, [[database-partitioning]] and [[consensus]] for sharding and replication steps.

## Trade-offs
Depth of estimation vs time in an interview; resilience (replicas, multi-DC) multiplies resources and latency.

## When to use it / when not to
Large-scale design interviews requiring capacity reasoning. Skip precise numbers for small systems.

## Note: what a senior/staff candidate should say
Anchor on the bottleneck resource (IOPS vs RAM vs bandwidth), show the numbers, reject simpler designs with a stated reason, then add sharding and multi-region replication, and finish by checking each requirement.

## Appears in
None yet.

## See also
[[back-of-the-envelope-estimation]], [[system-design-interview-framework]], [[database-partitioning]], [[consensus]], [[stream-processing]]
