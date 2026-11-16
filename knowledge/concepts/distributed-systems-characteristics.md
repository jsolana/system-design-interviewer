---
title: Key characteristics of distributed systems
type: concept
aliases: [scalability, reliability, availability, efficiency, serviceability]
sources: [Grokking the System Design Interview (PDF), "Key Characteristics of Distributed Systems" pp. 169-172]
---

# Key characteristics of distributed systems

## Definition
Five properties for evaluating a design: scalability, reliability, availability, efficiency and serviceability/manageability.

## Why it matters
They are the common vocabulary for stating non-functional requirements and justifying decisions.

## How it works
- **Scalability**: the ability to grow under more data or work without losing performance; performance usually degrades with size due to management/network costs, and some tasks are not distributable (atomic). Horizontal scaling (more servers; e.g. Cassandra, MongoDB) vs vertical (more CPU/RAM; e.g. MySQL, with a limit and downtime). See [[horizontal-vs-vertical-scaling]].
- **Reliability**: the probability that the system keeps providing service despite component failures; achieved with software and data redundancy (the shopping cart is not lost if the server goes down). It has a cost.
- **Availability**: percentage of time operational. Reliable implies available, but not the other way around (you can have high availability with an unreliable product if it is repaired quickly; e.g. 99.99% with no security testing that collapses later).
- **Efficiency**: latency (delay until the first item) and throughput (items per unit of time); costs: number of messages and message size.
- **Serviceability/manageability**: ease and speed of repairing/maintaining/upgrading; if repair time grows, availability drops. Early failure detection.

## Variants and techniques
Redundancy ([[database-replication]]), [[load-balancer]], [[cap-theorem]].

## Trade-offs
Redundancy increases reliability and cost; scaling without losing efficiency requires balancing load across nodes.

## When to use it / when not to
At the start of the design to set priorities (e.g. availability > consistency in social networks).

## Appears in


## See also
[[cap-theorem]], [[horizontal-vs-vertical-scaling]], [[database-replication]]
