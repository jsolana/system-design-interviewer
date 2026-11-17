---
title: Conflict resolution (LWW, merge, CRDTs)
type: concept
aliases: [last write wins, LWW, CRDT, operational transformation, write conflicts, siblings]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 5 (pp. 171-175, 184-193), System Design Interview Vol.1 (Alex Xu), ch. 15, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 6 (pp. 215-229)]
---

# Conflict resolution

## Definition
Strategies so that replicas accepting concurrent writes (multi-leader or leaderless) converge to the same value.

## Why it matters
Without a single write order, each replica may apply a different order and diverge forever. All replication must be **convergent**.

## How it works
- **Avoid conflicts**: all writes for a record go through the same leader (e.g. the user's "home datacenter"). Fails when the leader changes.
- **Last write wins (LWW)**: a unique ID/timestamp per write, and the highest wins. Popular but causes data loss and depends on clocks (see [[distributed-system-faults]]); only safe if keys are written once (e.g. a UUID per write, immutable).
- Per-replica priority (the one with the higher ID wins): also loses data.
- **Merge** of values (e.g. concatenate/union) and keeping **siblings** (concurrent versions) so the application or the user resolves them. Amazon cart example: the union keeps additions but makes deleted items reappear -> *tombstones* are needed.
- Application logic in a *write handler* or *read handler*.
- **Detecting concurrency**: two operations are concurrent if neither knows about the other (happens-before); **version vectors** (one counter per replica) make it possible to distinguish concurrent from causal ([[logical-clocks-and-causality]]).

## Variants and techniques
- **CRDTs** (conflict-free replicated datatypes): counters, sets, maps, lists that merge automatically (Riak 2.0).
- **Mergeable persistent data structures** (explicit history like Git).
- **Operational transformation**: collaborative editing (Etherpad, Google Docs) ([[google-docs]]).
- Some conflicts are semantic (double booking of the same room) and are not resolved by a field merge.

## Trade-offs
Automatic (CRDT/OT): no intervention, but complex and still immature in databases; LWW: simple but loses writes; siblings: loses nothing but pushes work onto the application.

## When to use it / when not to
When writes are accepted on several nodes (offline, multi-DC, collaboration). If constraints are needed (uniqueness, balance) use single-leader or consensus.

## Additional detail (Xu Vol. 1, ch. 15)
Sync conflicts in a drive: the first version processed by the system wins; the second receives a conflict and the user sees their local copy and the latest server one to merge or overwrite. For real-time concurrent editing, the book points to differential synchronization. See [[dropbox]].

## Additional detail (DDIA 2nd edition, ch. 6)
- *2nd edition (new)*: **sync engines / local-first** as multi-leader replication on devices ([[sync-engines-and-local-first]]).
- Conflict avoidance (route a record's writes to one leader; odd/even ID ranges) breaks down when the designated leader changes. LWW is really "one concurrent write is picked at random and others silently dropped"; with wall clocks it is sensitive to clock skew -> use logical clocks.
- Automatic merge by data type: text (track inserted/deleted characters), sets/lists (track deletions to avoid the Amazon cart "removed item reappears" problem), counters (add increments/decrements), maps (merge per key). Cannot enforce constraints like "max 5 items".
- **OT vs CRDT**: OT transforms operation indexes (insert "!" at 3 becomes 4 after "n" inserted at 0); CRDTs use unique element IDs plus the ID of the preceding element, ordering concurrent inserts by ID. OT in Google Docs/ShareDB; CRDTs in Riak, Redis Enterprise, Cosmos DB, Automerge, Yjs.

## Appears in
[[dropbox]]

## See also
[[replication]], [[quorum]], [[optimistic-concurrency-control]]
