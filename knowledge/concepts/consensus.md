---
title: Consensus (Paxos, Raft, total order broadcast, leader election)
type: concept
aliases: [Paxos, Raft, Zab, Viewstamped Replication, total order broadcast, atomic broadcast, ZooKeeper, etcd, leader election, membership service, state machine replication]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) chs. 9, 12, 13, Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 9 (pp. 364-408)]
---

# Consensus

## Definition
Getting several nodes to agree on a value. Properties: **uniform agreement** (everyone decides the same), **integrity** (a decision is made once), **validity** (the value was proposed by someone) and **termination** (non-crashed nodes eventually decide; this formalizes fault tolerance).

## Why it matters
It is the tool for electing a single leader, avoiding split brain, atomic commit, locks, uniqueness and consistent replication. It is equivalent to linearizable compare-and-set, total order broadcast and atomic commit.

## How it works
- Algorithms: **Paxos** (multi-Paxos), **Raft**, **Zab** (ZooKeeper), **Viewstamped Replication**. Tolerates failures as long as a majority (**quorum**) works; n=3 tolerates 1 failure, n=5 tolerates 2. See [[quorum]].
- Internally: one **leader** per *epoch/term number*; when the leader is in doubt a vote is started with a higher epoch number; to decide, the leader needs the vote of a quorum and must check that there is no other leader with a higher epoch. Two rounds of votes (elect leader; propose).
- **Total order broadcast**: reliable delivery (no message lost) and ordered (same order on all nodes). Equivalent to repeated consensus for each message; it is a **replicated log** (state machine replication) and the basis of replicated DBs, serializable transactions ([[serializability]]), locks with fencing tokens (the zxid/log index) and linearizable reads ([[linearizability]]).
- Difference from [[two-phase-commit]]: in 2PC the coordinator is not elected and its crash is not tolerated; fault-tolerant consensus does tolerate it.

## Variants and techniques
- **ZooKeeper / etcd (Chubby)**: small coordination service (data in memory) with consensus: atomic linearizable operations (compare-and-set), total order with zxid (fencing tokens), **failure detection** with sessions and heartbeats (ephemeral nodes), **change notifications** (watches). Use it for: leader election, assigning partitions to nodes and rebalancing, service discovery and membership.
- Membership service: agreement on which nodes are alive (it can be wrong because of timeouts but is useful).

## Trade-offs
- Requires a majority; without it the system halts (CP).
- Network-sensitive: badly tuned timeouts cause constant elections without progress.
- Fixed number of nodes (changing membership dynamically is hard); limited throughput (each decision is a vote).
- Multi-leader and leaderless do not use global consensus and have conflicts.
- The alternative to consensus in single-leader: wait for the leader, manual failover ("consensus by act of God"), or an automatic algorithm.

## When to use it / when not to
Critical metadata (leader, config, locks) in small clusters. For massive data use replication/partitioning and use consensus only to coordinate.

## Additional detail (Xu & Lam Vol. 2, chs. 9, 12 and 13)
- **Raft** replicating an event list/event store: the leader receives commands, converts them into events and replicates them with *AppendEntries* (which, without content, acts as a heartbeat); it works as long as more than half of the nodes are alive (3 nodes tolerate 1 failure, 5 tolerate 2; minimum votes n/2 + 1). Roles leader/candidate/follower; if a follower receives no heartbeat its election timeout expires, it becomes a candidate and asks for votes (*RequestVote*); *terms* number the periods; a *split vote* triggers a new election. Gives RPO close to 0 and RTO of seconds. See [[digital-wallet]], [[stock-exchange]].
- **Placement service** of an object store: 5 or 7 nodes with Paxos/Raft (with 7 it tolerates 3 failures). See [[s3-object-storage]].

## Appears in
[[digital-wallet]], [[distributed-message-queue]], [[payment-system]], [[s3-object-storage]], [[stock-exchange]]

## See also
[[replication]], [[distributed-lock]], [[linearizability]], [[two-phase-commit]], [[distributed-system-faults]], [[database-partitioning]]
