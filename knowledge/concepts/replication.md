---
title: Replication
type: concept
aliases: [replication, leader-follower, single-leader, multi-leader, leaderless, failover, replication lag, eventual consistency, database-replication, master-slave, primary-replica]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 5 (pp. 151-197), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 6 (pp. 229-243), System Design Interview Vol. 1 ch. 1, Grokking "Redundancy and Replication"]
---

# Replication

## Definition
Keeping copies of the same data on several nodes in order to: reduce latency (close to the user), increase availability and scale reads. The difficulty lies in handling the *changes* to the data.

## Why it matters
It is the basis of high availability and read scaling, but it introduces lag between replicas (replication lag) and write conflicts.

## How it works
### Single-leader (leader-follower)
- Writes go to the leader, which sends the *replication log* to the followers; reads can go to any of them.
- **Synchronous vs asynchronous**: synchronous guarantees an up-to-date copy but a failed follower blocks writes; a common practice is *semi-synchronous* (1 synchronous follower, the rest asynchronous). With asynchronous, if the leader goes down, committed writes can be lost.
- **Adding a follower**: consistent snapshot of the leader + position in the log (LSN/binlog coordinates) + catch-up.
- **Failover**: detect the failure (timeout), choose a new leader (consensus; best is the most up-to-date replica), reconfigure clients and demote the old leader. Risks: lost/discarded writes (GitHub incident with a reused autoincrement and inconsistency with Redis), *split brain* (fencing/STONITH), poorly calibrated timeout -> unnecessary failovers.
- **Log formats**: statement-based (problems with NOW(), RAND(), autoincrement, side effects), WAL shipping (coupled to the storage engine; prevents upgrades without downtime), **logical (row-based) log** (decoupled, parseable by external systems -> [[change-data-capture]]), trigger-based (flexible, more overhead).

### Problems due to replication lag (reads on asynchronous followers)
- **Read-your-writes (read-after-write)**: read from the leader what the user may have modified; or for 1 min after their last write; or the client remembers the timestamp/LSN of its last write; complicated across devices and datacenters (cross-device).
- **Monotonic reads**: do not see data "go back in time" when reading from different replicas; solution: each user always reads from the same replica (hash of the user id).
- **Consistent prefix reads**: preserve the causality of writes (typical in partitioned databases); causally related writes go to the same partition.
- With eventual consistency, "eventually" has no bound. Transactions are the way to hide these problems from the application.

### Multi-leader
- One leader per datacenter (or per offline device, or collaborative editing). Advantages: local write latency, tolerance of datacenter/inter-DC network failure. Disadvantage: **write conflicts** (see [[conflict-resolution]]) and weak guarantees (autoincrement, triggers, constraints).
- Topologies: circular, star, all-to-all; in the first two a failed node cuts propagation (each write is tagged with node IDs to avoid loops); in all-to-all, writes can arrive out of order (violating causality) -> version vectors.

### Leaderless (Dynamo style: Riak, Cassandra, Voldemort)
- The client (or a coordinator) writes to several replicas and reads from several; see [[quorum]]. There is no failover.
- Catching up nodes that were down: **read repair** (when reading, the new value is rewritten to stale replicas) and **anti-entropy process** (background process that compares and copies differences).
- Concurrency detection with version numbers/**version vectors** ([[logical-clocks-and-causality]]).

## Variants and techniques
| Model | Write | Conflicts | Failover |
|---|---|---|---|
| Single-leader | leader only | none (total order) | yes, delicate |
| Multi-leader | several leaders | yes, must be resolved | per DC |
| Leaderless | quorum | yes, must be resolved | does not exist |

## Trade-offs
- Latency/availability vs consistency: more synchronous replicas = more durability, less availability.
- Read scaling is only realistic with asynchronous replication (with N synchronous followers any failure stops writes).
- Note: DynamoDB (the AWS product) uses single-leader, a different architecture from the Dynamo paper.

## When to use it / when not to
- Single-leader by default; multi-leader if there are several datacenters with local writes or offline use; leaderless if availability is prioritized and eventual consistency is tolerated.

## Additional detail (DDIA 2nd edition, ch. 6)
- *2nd edition (new emphasis)*: **leaderless vs single-leader performance**: single leader limits read throughput, needs failover and is sensitive to a slow leader; leaderless sends requests to several replicas and uses the fastest (**request hedging**), resilient to **gray failures** (degraded but not dead nodes). Costs: hinted-handoff load, bigger quorums raise tail latency (quorums rarely beyond 4 of 7), partitions can prevent quorums; **sloppy quorum** (Dynamo/Riak; Cassandra/ScyllaDB consistency level ANY) trades read guarantees for availability.
- **Multi-region leaderless** (Cassandra/ScyllaDB): coordinator in the local region forwards to all local replicas and one replica per other region; choose consistency level: global quorum, per-region quorum or local quorum (faster, staler). Riak keeps clients local and replicates across clusters asynchronously.
- Concurrency: two writes are concurrent if neither was aware of the other (not about wall-clock time).

## Practical redundancy and failover (System Design Interview Vol. 1 ch. 1; Grokking "Redundancy and Replication")
Merged from the former `database-replication` note.
- **Master/slave in practice**: writes go to the master, reads to slaves (reads far outnumber writes, so more slaves than masters). If a slave fails, its reads move to other slaves (or temporarily to the master); a failed master is replaced by promoting a slave, which may be stale and needs recovery scripts.
- **Redundancy** duplicates critical components to remove SPOFs; **replication** keeps those copies consistent. Failover to an active or passive secondary, automatic or manual, also applies to services (KGS standby, load balancers, index servers), not only databases.
- If primary and secondary fail together, rebuild on a new server. Scanning the whole database filtering by hash is slow, hence an **inverted index server** mapping IDs to servers ([[twitter-search]], [[yelp]]).
- Critical data: several copies on different servers, or erasure coding (Reed-Solomon, mentioned for Messenger).
- Services with in-memory state ([[ticketmaster]]): master-slave and rebuild from the database; anything not persisted (waiting queue) is lost without a replica. Periodic snapshots/checkpoints allow rebuilding ([[typeahead]], [[web-crawler]]).
- Replicating caches: on a miss the server propagates the new entry to replicas. Asynchronous replication across data centers (e.g. Netflix) in [[multi-data-center]].
- Trade-off: a slave may serve slightly stale data; promotion after a master failure may lose unreplicated data.

## Appears in
[[distributed-message-queue]], [[dropbox]], [[gaming-leaderboard]], [[git-repository-hosting]], [[hotel-reservation]], [[key-value-store]], [[proximity-service]], [[s3-object-storage]], [[twitter]], [[twitter-search]], [[typeahead]], [[unique-id-generator]], [[youtube]]

## See also
[[quorum]], [[conflict-resolution]], [[consensus]], [[database-partitioning]], [[change-data-capture]], [[write-ahead-log]], [[distributed-system-faults]]
