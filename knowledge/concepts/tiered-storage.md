---
title: Tiered storage
type: concept
aliases: [hot/cold storage separation, storage disaggregation]
sources: [https://www.confluent.io/blog/10x-apache-kafka-elasticity/]
---

# Tiered storage

## Definition
Keeping only recent ("hot") data on fast local disks or memory and offloading the bulk of older data to cheap object storage, while presenting a single logical view (same offsets/addresses) to clients.

## Why it matters
When a node's local data is small, adding, replacing or failing over a node moves little data, so scaling and recovery become fast and compute and storage scale separately.

## How it works
- Example (Kafka as run by Confluent Cloud): brokers keep about one day of data locally and the rest (~1:30 ratio in the post's example) in object storage; historical reads go through a separate network path so they do not block real-time reads/writes; offsets are unchanged and clients read through brokers.
- Smaller local footprint allows higher-performance disks.
- Modeled effect: new-broker data copy drops from ~194 TB (~43 h at 10 Gbit) to ~6.5 TB (~1.4 h). Source reports a 69% average reduction in expansion time on Azure clusters after rollout (vendor figure).

## Variants and techniques
Memory cache -> local disk -> object storage hierarchy; online self-balancing so partitions serve as soon as they catch up.

## Trade-offs
- Cost/performance balancing across tiers is a major engineering effort.
- Historical reads depend on object storage latency/availability (isolated from the real-time path).
- Numbers in the source are vendor-supplied and partly illustrative.

## When to use it / when not to
Large retention with mostly-recent reads (logs, streams); not when most reads touch old data at low latency.

## Appears in
[[distributed-message-queue]]

## See also
[[message-queues]], [[object-storage]], [[replication]]
