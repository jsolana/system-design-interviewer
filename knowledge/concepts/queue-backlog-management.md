---
title: Queue backlog management (avoiding insurmountable backlogs)
type: concept
aliases: [queue backlog, message age, sidelining, backpressure in queues, async system recovery]
sources: [https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/]
---

# Queue backlog management

## Definition
Techniques that keep asynchronous (queue-based) systems from entering a **backlog mode** where arrival rate exceeds processing rate and end-to-end latency keeps growing long after the cause is fixed.

## Why it matters
Queues trade latency for durability. Systems are bimodal: fast without backlog, slow with it. After a one-hour outage, draining needs ~2x normal capacity for another hour; a 10x consumer-capacity spike with 30 min until an operator reacts means ~300 min to recover. Synchronous systems drop requests but recover fast; async ones accumulate.

## How it works
- **Measure**: producer-side errors = queue availability; consumer errors overstate failures (retries); DLQ rate is a late signal; **message age** (now minus enqueue time, recorded on dequeue) is the key latency signal. Separate first-attempt age from retry age (AWS IoT `AgeOfFirstAttempt`). Propagate trace IDs; record queue depths.
- **Fairness**: lightweight front API authenticates and tags messages; per-customer rate limits with burst.
- **Topology**: queue per workload isolates but costs polling; shared queue hard to unmix; **shuffle sharding** of customers over a fixed set of queues, enqueue to least-full of the customer's subset (Lambda async) ([[shuffle-sharding-and-cell-based-architecture]]).
- **Sidelining**: move over-rate messages to spillover queues (approximates priority queue); move stale messages (by age on dequeue) to a backlog queue processed after fresh ones (approximates LIFO).
- **TTL drop** where newer data supersedes (anti-entropy sweepers).
- **Limit concurrency per workload** (Little's Law: concurrency = rate x latency; 100 msg/s at 100 ms = 10 threads, at 10 s = 1,000): non-blocking I/O, separate pools, semaphores.
- **Backpressure** upstream: scale inbound throttle inversely with per-workload backlog (SQS lacks per-attribute depth; Amazon MQ finer). Exception: amazon.com orders accept all and prioritize.
- **Delay queues** to defer a slow workload; mind SQS in-flight limits and VisibilityTimeout.
- **SQS FIFO caveat**: polls most recent ~20k unprocessed; big-backlog groups can starve groups with new messages.
- **DLQ** for unprocessable messages; alarm on any DLQ message.
- **Polling buffer**: if every poll returns a message there is no burst headroom.
- **Heartbeat/lease**: processing longer than visibility timeout causes duplicate parallel processing ("fork bomb"); stop or extend lease.

## Variants and techniques
Sidelining, shuffle-sharded queues, backpressure, delay queues, dead-letter queues, LIFO/age-based processing.

## Trade-offs
Dedicated queues = isolation vs cost; FIFO = order vs starvation; reject = protect system vs accept = protect business; retries = durability vs latency.

## When to use it / when not to
Any pipeline with async buffers and multiple tenants/workloads. For pure fire-and-forget low-stakes flows simple TTL drop is enough.

## Appears in
[[distributed-message-queue]], [[job-scheduler]], [[notification-system]]

## See also
[[message-queues]], [[load-shedding-and-overload-handling]], [[multi-tenancy-and-fairness]], [[idempotency]], [[overload-and-metastable-failures]]

## Interview note (senior/staff)
When you put a queue in a design, say how you detect and recover from backlog: alarm on message age, per-tenant isolation (sharded queues), process fresh before stale, bounded concurrency using Little's Law, DLQ, and idempotent consumers; compute drain time from spare capacity (drain rate = capacity minus arrival rate).
