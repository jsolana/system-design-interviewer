---
title: Gossip protocol
type: concept
aliases: [failure detection, heartbeat, membership list]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 6 (pp. 99-101)]
---

# Gossip protocol

## Definition
A decentralized method for failure detection and cluster membership propagation: nodes periodically exchange information with random nodes.

## Why it matters
In a distributed system it is not enough for one server to say another is down; at least two independent sources are needed. All-to-all multicast is simple but inefficient with many servers.

## How it works
1. Each node maintains a **membership list** (IDs and heartbeat counters).
2. Each node periodically increments its own counter.
3. It sends heartbeats to a set of random nodes, which in turn propagate them.
4. On receiving them, the list is updated.
5. If a counter does not increase for a predefined period, the member is considered offline; other nodes confirm it and it is propagated.

## Variants and techniques
As opposed to all-to-all multicasting (O(n^2) messages).

## Trade-offs
Eventual (not instantaneous) detection in exchange for scalability and no central point.

## When to use it / when not to
Large decentralized clusters (Dynamo, Cassandra). With few nodes or a coordinator (ZooKeeper) it may not be needed.

## Appears in
[[key-value-store]]

## See also
[[quorum]], [[consistent-hashing]]
