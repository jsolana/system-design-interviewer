---
title: Eventual consistency
type: concept
aliases: [weak consistency, session consistency, read-your-writes, monotonic reads, inconsistency window]
sources: [https://www.allthingsdistributed.com/2008/12/eventually_consistent.html, https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html]
---

# Eventual consistency

## Definition
A weak consistency form: if no new updates arrive, all reads eventually return the last written value. The time until then is the **inconsistency window**. Vogels' example: DNS.

## Why it matters
At large scale partitions are unavoidable, so consistency must be traded against availability (see [[cap-theorem]]); inconsistency is tolerated for performance under concurrency and availability in partitions.

## How it works
Client-side variants (Vogels):
- **Causal**: a process informed of an update sees it; unrelated processes follow normal eventual rules.
- **Read-your-writes**: writer always sees own updates (special case of causal).
- **Session**: read-your-writes inside a session, lost after it ends.
- **Monotonic reads**: never see an older value after seeing a newer one.
- **Monotonic writes**: writes of one process are serialized.
Monotonic reads + read-your-writes are the most useful for developers and can be combined (sticky sessions or client-side version tracking).

Server-side: N replicas, W write acks, R replicas read.
- W+R > N: read and write sets overlap, strong consistency.
- W+R <= N: reads may miss recent writes (eventual).
- Common configs: N=3, W=R=2 (fault tolerance); R=1 with many replicas (read scaling); W=1 (fast writes, lazy propagation). Dynamo's common (N,R,W) = (3,2,2).
- Primary-backup RDBMS: reading from an async backup is eventually consistent; window depends on log shipping.

## Variants and techniques
Dynamo (Vogels, 2007): "always writeable", conflicts resolved on read by the application (merge shopping carts) or last-write-wins; vector clocks, sloppy quorum + hinted handoff, Merkle-tree anti-entropy, gossip membership, consistent hashing with virtual nodes; get/put on objects < 1 MB; SLAs at p99.9. See [[quorum]], [[vector-clocks]], [[conflict-resolution]].

## Trade-offs
Majority quorums make the minority side unavailable in a partition; eventual designs stay writable but push conflict handling to the application. For websites, keep the inconsistency window shorter than the time to the user's next page load.

## When to use it / when not to
Carts, feeds, counters, caches, DNS-like data. Not for balances, inventory or locks that need [[linearizability]].

## Appears in
[[key-value-store]]

## See also
[[replication]], [[quorum]], [[cap-theorem]], [[consistency-anomalies-jepsen]], [[key-value-store]]

## Note: what a senior/staff candidate should say
Say which user-visible guarantee you need (usually read-your-writes plus monotonic reads), pick N/R/W from it, and where you need stronger consistency, route just those operations to a strongly consistent path.
