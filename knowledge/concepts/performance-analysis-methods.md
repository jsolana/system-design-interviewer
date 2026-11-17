---
title: Performance analysis methods (USE method)
type: concept
aliases: [USE method, utilization saturation errors, bottleneck analysis]
sources: [https://www.brendangregg.com/usemethod.html]
---

# Performance analysis methods (USE method)

## Definition
Brendan Gregg's **USE method**: "for every resource, check utilization, saturation and errors". A checklist-style methodology to find resource bottlenecks and errors quickly in any system.

## Why it matters
Gives a systematic way to start a performance investigation instead of guessing; the author estimates it solves about 80% of server issues with about 5% of the effort, and turns unknown-unknowns into known-unknowns.

## How it works
1. List the resources (hardware: CPUs, memory, NICs, storage devices, controllers, interconnects; optionally software: mutexes, thread pools, file descriptor limits; cloud: tenant/cgroup caps).
2. For each resource check three metric types (errors first, they are quick to interpret):

| Metric | Meaning | Examples |
|---|---|---|
| Utilization | average time busy (percent) | CPU busy %, disk busy %, NIC throughput vs max |
| Saturation | work queued that cannot be serviced | CPU run-queue length, disk wait queue, swapping |
| Errors | error event counts | device errors, dropped packets, failed allocations |

3. Investigate findings with other methods (workload characterization, drill-down); iterate.

Interpretation: 100% utilization usually means a bottleneck; above about 70% can already hurt (especially non-preemptible resources like disks); any non-zero saturation can be a problem; non-zero errors deserve a look. Averages hide bursts (CPUs at 100% for seconds while 5-minute averages show 80%).

## Variants and techniques
Complementary: workload characterization, drill-down, latency-based methods (e.g. Method R, finds more but takes longer). The USE method is not latency-based and misses issues outside resources.

## Trade-offs
Fast and cheap but only finds bottlenecks/errors; hardware caches are excluded; one tool in a toolbox.

## When to use it / when not to
Start of any server/service performance triage; also as a model for dashboards (per-resource U/S/E). Not for finding application-level logic latency; use tracing/profiling ([[observability-and-monitoring]]).

## Appears in
None yet.

## See also
[[observability-and-monitoring]], [[tail-latency]], [[overload-and-metastable-failures]], [[network-latency-and-bandwidth]], [[back-of-the-envelope-estimation]]

## Note: what a senior/staff candidate should say
When asked "how would you debug slow requests", walk the resources (CPU, memory, disk, network, pools/locks) with U/S/E, and say saturation (queues) is the leading indicator that utilization alone misses; design dashboards and alerts around it.
