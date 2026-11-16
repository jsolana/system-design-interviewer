---
title: Quorum reads and writes
type: concept
aliases: [quorum, w + r > n, sloppy quorum, hinted handoff, strict quorum]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 5 (pp. 179-193) and ch. 9, System Design Interview Vol.1 (Alex Xu), ch. 6 (pp. 95-96, 101)]
---

# Quorum reads and writes

## Definition
In leaderless replication with n replicas, a write must be confirmed by w nodes and a read queries r nodes. If **w + r > n**, the sets overlap in at least one node and the read sees the most recent value (r and w are "minimum votes").

## Why it matters
It makes it possible to tolerate down or slow nodes without failover and to tune the balance between latency, availability and freshness.

## How it works
- Typical config: odd n (3 or 5), w = r = ceil((n+1)/2) (majority). n=3, w=2, r=2 tolerates 1 unavailable node.
- Reads/writes are always sent to all n replicas in parallel; w and r only set how many responses are awaited. If fewer than w/r nodes are available, error.
- Tuning: w=n, r=1 -> fast reads but one down node blocks writes. w+r <= n -> lower latency and higher availability, higher probability of stale reads.
- Versions (number/version) identify the newest value; read repair and anti-entropy ([[replication]]).

## Variants and techniques
- **Sloppy quorum + hinted handoff**: if the n "home" nodes of a key cannot be reached, writes are accepted on other nodes; when the home nodes recover, the writes are forwarded to them. Increases write availability but w+r>n no longer guarantees overlap.
- Quorum in consensus: the decision requires votes from a quorum (majority), see [[consensus]].

## Trade-offs
Cases where stale values are read even with w+r>n: sloppy quorum; concurrent writes (they must be merged; if resolved by timestamp, some are lost due to clock skew); a write concurrent with a read; a failed write that landed on fewer than w replicas and is not rolled back; restoring a node from an old replica. It is not linearizable ([[linearizability]]) in general. Eventual consistency must be assumed.

## When to use it / when not to
Dynamo/Cassandra/Riak-style systems that prioritize availability; not when linearizability is needed (use consensus).

## Additional detail (Xu Vol. 1, ch. 6)
Notation: N (replicas), W (ACKs needed to consider a write successful), R (responses needed for a read). The **coordinator** (proxy between client and nodes) waits for W/R responses; W=1 does not mean writing to a single server, but waiting for a single ACK.
| Config | Effect |
|---|---|
| R=1, W=N | fast reads |
| W=1, R=N | fast writes |
| W+R>N (typical N=3, W=R=2) | strong consistency guaranteed (there is an overlapping node) |
| W+R<=N | no strong consistency guarantee |
W or R > 1 improves consistency but waits for the slowest replica. **Sloppy quorum** in the book: instead of requiring the strict quorum, the first W (write) / R (read) healthy servers on the ring are chosen, ignoring down ones; the substitute server stores the changes and hands them back on recovery (**hinted handoff**). For permanent failures: anti-entropy with [[merkle-tree]]. Failure detection with [[gossip-protocol]]; conflict resolution with [[vector-clocks]].

## Appears in
[[key-value-store]]

## See also
[[replication]], [[consensus]], [[linearizability]], [[logical-clocks-and-causality]]
