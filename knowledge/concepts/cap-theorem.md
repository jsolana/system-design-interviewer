---
title: CAP theorem
type: concept
aliases: [CAP theorem, consistency availability partition tolerance]
sources: [Grokking the System Design Interview (PDF), "CAP Theorem" pp. 188-189, System Design Interview Vol.1 (Alex Xu), ch. 6 (pp. 90-92)]
---

# CAP theorem

## Definition
A distributed system cannot simultaneously guarantee more than two of: **Consistency** (all nodes see the same data at the same time), **Availability** (every request receives a response, success or failure) and **Partition tolerance** (the system keeps working despite message loss or partial network failures).

## Why it matters
It is the first thing to consider when designing a distributed system: it forces you to choose what to sacrifice during a partition.

## How it works
- To be consistent, all nodes must see the same updates in the same order. With a partition, a read on the lagging side would return stale data; the only way to avoid that is to stop serving from that side (availability is lost).
- Availability is achieved by replicating data across servers ([[database-replication]]).

## Variants and techniques
Practical choice in the source's exercises: social content systems (Instagram, Twitter, YouTube) -> availability over consistency (acceptable for a photo/tweet to take a while to appear); messaging (Messenger) -> high consistency of history across devices even at the cost of availability.

## Trade-offs
CP: consistent but may reject requests; AP: always responds but may return stale data (eventual consistency).

## When to use it / when not to
Reasoning framework to justify asynchronous replication, caches and database choice ([[sql-vs-nosql]]).

## Additional detail (Xu Vol. 1, ch. 6)
- Classification of stores: **CP** (sacrifices availability), **AP** (sacrifices consistency), **CA** (does not exist in practice because network partitions are unavoidable).
- Example with 3 replicas n1, n2, n3: without a partition there is consistency and availability. If n3 is isolated: **CP** blocks writes on n1/n2 so they don't diverge (typical of banking: an error is returned until resolved); **AP** keeps accepting reads (possibly stale) and writes on n1/n2 and syncs n3 when the partition heals.
- Consistency models: strong (a read sees the latest write; requires blocking replicas until all agree), weak and eventual (given enough time all converge). Dynamo and Cassandra use eventual; see [[key-value-store]].

## Appears in
[[distributed-email-service]], [[google-maps]], [[key-value-store]]

## See also
[[database-replication]], [[distributed-systems-characteristics]]
