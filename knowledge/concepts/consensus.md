---
title: Consensus (Paxos, Raft, total order broadcast, leader election)
type: concept
aliases: [Paxos, Raft, Zab, Viewstamped Replication, total order broadcast, atomic broadcast, ZooKeeper, etcd, leader election, membership service, state machine replication]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) chs. 9, 12, 13, Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 9 (pp. 364-408), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 10 (pp. 425-440), https://sre.google/sre-book/managing-critical-state/, https://blog.cloudflare.com/choosing-quepaxa/]
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

## Additional detail (DDIA 2nd edition, ch. 10)
- *2nd edition (reframed)*: the "many faces of consensus" are equivalent problems: single-value consensus / **CAS register**, **shared log (total order broadcast)**, **atomic fetch-and-add**, **atomic commit**, lock/lease acquisition, uniqueness constraints. In practice most systems expose a **shared log** (Raft, VR and Zab natively; Multi-Paxos for Paxos), enabling state machine replication, event sourcing, serializable transactions via deterministic stored procedures, one-consensus-per-seat (include seat number in entries) and fencing tokens (counter on log entries).
- Algorithms have **epoch numbers** (ballot in Paxos, view in VR, term in Raft): elections use higher epochs and a leader must confirm with a quorum before appending; two quorum rounds (election and proposal) must overlap. Unlike 2PC any node can call an election and only a quorum (not all participants) must answer. Raft only elects a node whose log is at least as up-to-date as a majority; Paxos lets any node lead but requires catching up first.
- **FLP**: no deterministic algorithm guarantees termination in a fully asynchronous model with crashes; timeouts or randomness circumvent it. Byzantine-tolerant variants assume <1/3 faulty (blockchains). Weakening guarantees (Kafka *unclean leader election*) improves availability but leaves theory.
- **Coordination services** (ZooKeeper, etcd): locks, leases, failure detection, change notification. For service discovery, consensus is usually overkill: prefer caches/TTL/DNS; ZooKeeper *observers* serve stale but available reads.

## Additional detail (Google SRE Book, ch. 23)
- Ad hoc leader election, heartbeats and gossip repeatedly caused split-brain and corruption; leader election, membership, locking and reliable queues are all consensus variants, so use a proven system.
- **Quorum sizing**: 2f+1 replicas tolerate f crashes (3f+1 for Byzantine). 3 replicas tolerate 1, 5 tolerate 2 (survive maintenance plus a failure); a 6th replica raises the quorum to 4 and lowers tolerated unavailability to 33% (vs 40% with 5).
- **Performance**: stable leader, batching and pipelining; Multi-Paxos is one round trip; a 10 ms random disk write caps throughput near 100 ops/s; disk logging (1-several ms) dominates latency; RTTs ~1 ms in datacenter, 45 ms within the US, 70 ms New York to London. Beware dueling proposers livelock.
- Locks as renewable leases with timeouts, queues with leases rather than immediate removal, barriers as replicated state machines.
- **Monitor**: healthy replica count, lagging replicas, leader existence, leader-change frequency (flapping), term/view number regressions, proposals seen vs agreed, log-write latency. Keep backups: replication does not cover bugs or human error ([[data-integrity-and-backups]]).
- Source: https://sre.google/sre-book/managing-critical-state/; used by [[distributed-periodic-scheduling]].

## Additional detail (Cloudflare blog, QuePaxa)
Cloudflare's Meerkat KV store (global control plane) chose QuePaxa because leader-based protocols (Raft, Multi-Paxos) stall when the leader is slow or partitioned: a 2020 partial switch failure slowed a consensus-backed dashboard 80x for six hours; fault detectors must guess and Raft timeouts are 5-10x RTT (about 1 s across continents); election storms can become metastable. QuePaxa has an **optional leader** (its proposal gets max priority, so the fast path is one round trip), **no failure detector** (clients/replicas hedge after a short local timeout) and **constructive interference** (proposers adopt the highest-priority proposal seen). Rounds: propose/adopt, spread, check/decide, carry forward. Measured: >95% decisions in one round trip; leader failure dropped decisions to about 65% and recovered in about a minute without halting; slow path at most one third throughput. Costs: more messages (hedging moved to clients), less battle-tested, needs verification/fault-injection. See [[overload-and-metastable-failures]].

## Appears in
[[digital-wallet]], [[distributed-message-queue]], [[git-repository-hosting]], [[payment-system]], [[s3-object-storage]], [[stock-exchange]]

## See also
[[replication]], [[distributed-lock]], [[linearizability]], [[two-phase-commit]], [[distributed-system-faults]], [[database-partitioning]], [[leader-election]]
