---
title: Replication
type: concept
aliases: [replication, leader-follower, single-leader, multi-leader, leaderless, failover, replication lag, eventual consistency]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 5 (pp. 151-197)]
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

## Appears in
[[distributed-message-queue]], [[key-value-store]], [[s3-object-storage]], [[unique-id-generator]]

## See also
[[quorum]], [[conflict-resolution]], [[consensus]], [[database-partitioning]], [[change-data-capture]], [[write-ahead-log]], [[distributed-system-faults]]
