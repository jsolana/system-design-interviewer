---
title: Database replication
type: concept
aliases: [master-slave, primary-replica]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 1 (pp. 12-14), Grokking the System Design Interview (PDF), "Redundancy and Replication" pp. 184-185]
---

# Database replication

## Definition
Keeping copies of a database on several servers. Master/slave model: the master accepts writes (insert, update, delete) and the slaves receive copies and serve reads only.

## Why it matters
- **Performance**: reads are spread across slaves (most apps have far more reads than writes, so there are more slaves than masters).
- **Reliability**: data survives the loss of a server or a location.
- **High availability**: the site stays up if a database goes down.

## How it works
- Writes go to the master; reads go to slaves.
- A slave goes down: its reads go to other slaves (or temporarily to the master if it is the only one) and it is replaced.
- The master goes down: a slave is promoted. In production this is more complex because the slave may be out of date; data must be recovered with recovery scripts.

## Redundancy and failover (Grokking the System Design Interview, pp. 184-185 and fault tolerance per problem)
- **Redundancy** = duplicating critical components to eliminate SPOFs; **replication** = keeping those copies consistent (master propagates, slaves acknowledge receipt).
- Failover to a secondary replica (active or passive), automatic or manual. Also applies to services (KGS standby, LB, index servers) and not only to databases.
- If primary and secondary fail at the same time: rebuild on a new server; scanning the whole database filtering by hash is slow, which is why an **inverted index server** (Index-Builder / QuadTree Index server) mapping IDs -> server is used ([[twitter-search]], [[yelp]]).
- For critical data: several copies on different servers or erasure coding (Reed-Solomon, mentioned in Messenger).
- Services with in-memory state ([[ticketmaster]]): master-slave and rebuild from the database; anything not persisted (waiting queue) is lost without a replica.
- Periodic snapshots/checkpoints allow rebuilding (trie in [[typeahead]], crawler in [[web-crawler]]).
- Replicating caches: on a cache miss the server propagates the new entry to the replicas.

## Variants and techniques
Multi-master and circular replication (more complex; out of the book's scope). Asynchronous replication between data centers (e.g. Netflix) in [[multi-data-center]].

## Trade-offs
A slave may serve slightly stale data; promotion after a master failure may lose unreplicated data.

## When to use it / when not to
Always for redundancy and read-heavy workloads. To grow in writes/volume, [[database-partitioning]] (sharding) is needed.

## Appears in
[[dropbox]], [[gaming-leaderboard]], [[hotel-reservation]], [[proximity-service]], [[twitter]], [[twitter-search]], [[typeahead]], [[youtube]]

## See also
[[load-balancer]], [[database-partitioning]], [[caching]]
