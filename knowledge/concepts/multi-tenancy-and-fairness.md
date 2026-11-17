---
title: Multi-tenancy fairness, quotas and admission control
type: concept
aliases: [fairness, noisy neighbor, per-tenant quotas, admission control, throttling]
sources: [https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/]
---

# Multi-tenancy fairness, quotas and admission control

## Definition
Fairness: each tenant should get an experience close to a single-tenant system even though infrastructure is shared. Achieved by per-tenant quotas, rate limiting, load shedding and layered admission control.

## Why it matters
Sharing lowers cost, ops effort and energy via higher utilization, but couples workloads (e.g. a cron job in one tool slowing another tool on the same database). Load shedding alone is not fair: spikes usually come from one tenant, so shedding would fail innocent tenants.

## How it works
- **Resource allocation resembles bin packing**: placement, continuous monitoring and migration, fleet scaling, bounded stretching (exceed allocation only if spare capacity). Borrowed capacity must be returned almost instantly.
- **Load shedding** (503) protects server and buys time for autoscaling ([[load-shedding-and-overload-handling]]); **rate limiting/quotas** (429, client-side issue; RFC 6585) per tenant or resource (e.g. DynamoDB table). Older services (SQS) still return 503 for compatibility.
- **Quota types**: concurrency (EC2 instances per account) and rate-based (TPS). Defaults per client, raisable on request, visible via usage metrics/alarms. Expensive APIs get lower quotas or debit actual cost after the call (quota can go negative).
- **Flexibility**: Client A limit 1,000 TPS, service capacity 10,000, current 5,000; A spikes to 3,000: strict admits 1,000, flexible admits all while spare capacity exists and sheds over-quota traffic only when others use their quotas. Stacked capacity (borrowable) vs hard allocation (1/3 each). Larger burst at launch (EC2 boot).
- **Layers**: API Gateway, LB/WAF/CloudFront, Shield (DDoS), then in-service.
- **Local admission control**: token bucket (refill rate + burst size); compose low-rate/high-burst with high-rate/low-burst buckets.
- **Distributed admission control**: (1) local limit = global/N servers (needs even round-robin); (2) consistent hashing to rate-tracker fleet (Redis), hot keys mitigated by moving them to local control; (3) async sharing of observed rates (gossip); (4) other algorithms.
- **Reactive rules** on headers/URI/IP, changed dynamically with audit trail and an evaluation (dry-run) mode. High-cardinality dimensions: heavy hitters, top talkers, counting Bloom filters; CloudWatch Contributor Insights.
- **Client behavior**: synchronous callers fail fast (SDK stops retrying when errors frequent, STANDARD mode); async callers back off/backpressure.
- **Accuracy measurement**: log throttle key + limit per request; compute TP/TN/FP/FN per key.
- **Avoid hitting quotas by design**: separate data plane (elastic, slack capacity, autoscaled limits) from control plane; offer change streams (CloudTrail vs polling DescribeInstances), async exports (S3 Inventory), bulk APIs (IoT bulk provisioning), local projections (instance metadata). Quotas as a feature (Lambda concurrency cap for cost control).

## Variants and techniques
[[shuffle-sharding-and-cell-based-architecture]] for isolation; per-tenant queues ([[queue-backlog-management]]); background in [[multitenancy-and-cell-based-architecture]].

## Trade-offs
Quotas can reduce perceived availability even with spare capacity; hard allocation wastes capacity; distributed limiters trade accuracy vs scalability vs simplicity.

## When to use it / when not to
Any shared service/API. Fixed per-tenant limits matter most where tenants are untrusted or bursty.

## Appears in
[[distributed-rate-limiter]]

## See also
[[rate-limiting]], [[hot-keys]], [[consistent-hashing]], [[bloom-filter]], [[gossip-protocol]]

## Interview note (senior/staff)
Say "per-tenant token buckets enforced in layers (edge, then service), 429 vs 503 distinction, burst allowed from unused capacity with owners having priority, quotas visible and raisable, and I'd measure limiter accuracy." Raise the data-plane/control-plane API design point to reduce quota pressure, and mention hot-key handling in distributed counters.
