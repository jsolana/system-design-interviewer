---
title: Logical clocks and causality (Lamport, version vectors)
type: concept
aliases: [Lamport timestamps, version vectors, happens-before, causal consistency, concurrent writes, sequence numbers]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 5 (pp. 184-193), ch. 9 (pp. 339-352), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 10 (pp. 420-423)]
---

# Logical clocks and causality

## Definition
Mechanisms for ordering events without relying on physical clocks. **Happens-before**: A precedes B if B knows about or depends on A; if neither knows of the other, they are **concurrent**.

## Why it matters
Physical clocks are unreliable ([[distributed-system-faults]]); causality (questions before answers, insert before update) is what must be preserved; it is the strongest consistency model that does not slow down because of network latency.

## How it works
- **Sequence numbers / logical timestamps**: growing counters that give a total order consistent with causality.
- **Lamport timestamp** (counter, nodeID): each node keeps the maximum counter seen; on every request/response it propagates the maximum; ordering: higher counter, ties broken by nodeID. Gives a total order consistent with causality, but is only known after the fact (not useful for deciding in the moment, e.g. "is this username unique?" -> needs total order broadcast, [[consensus]]).
- **Version vectors** (one counter per replica, an extension of the version number in leaderless): allow distinguishing "A overwrites B" from "concurrent" and reading/writing without data loss; the server returns concurrent siblings ([[conflict-resolution]]). *Dotted version vectors* in Riak.
- Concurrency detection on a single record: server with an incrementing version number; the client sends the version it read.

## Variants and techniques
Causal consistency, total order (total order broadcast), vector clocks (a variant for comparing events, not writes).

## Trade-offs
Causality requires no global coordination and does not sacrifice availability, but does not solve constraints that need total order (uniqueness).

## When to use it / when not to
In multi-leader/leaderless replication and in systems that need causal order without consensus; for uniqueness/locks use [[consensus]].

## Additional detail (DDIA 2nd edition, ch. 10)
- *2nd edition*: logical clocks are treated alongside ID generation: Lamport timestamps (counter, node ID), **hybrid logical clocks** (new: physical-time-like, monotonic even if NTP jumps back, consistent with happens-before, no special hardware), vector clocks (detect concurrency, large). Lamport/HLC order is weaker than linearizability: only guarantees greater than timestamps already seen. See [[unique-id-generation]].

## Appears in
[[google-docs]]

## See also
[[replication]], [[quorum]], [[linearizability]], [[unique-id-generation]]
