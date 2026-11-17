---
title: Consistent hashing
type: concept
aliases: [hash consistente, hash ring]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp, System Design Interview Vol.1 (Alex Xu), ch. 5, Grokking the System Design Interview (PDF), "Consistent Hashing" pp. 189-192, Designing Data-Intensive Applications (Kleppmann), ch. 6]
---

# Consistent hashing

## Definition
A key -> node assignment scheme that minimizes relocations when nodes are added or removed.

## Why it matters
It allows routing to an "owner" server (e.g. the one holding a user's socket) and keeping related data together (swipe pairs in Redis, [[tinder]]).

## How it works
Each user/key maps to a server; a registry (ZooKeeper or etcd) stores the assignment; servers call each other directly.

## Variants and techniques
Connection draining when scaling to avoid thundering herds; during resharding, events must reach both the old and the new owner.

## Trade-offs
Connection mesh between servers, operational complexity; alternative: [[pub-sub]].

## When to use it / when not to
When state lives on the server and traffic must be routed to it.

## Additional detail (Xu Vol. 1, ch. 5)
**Rehashing problem**: with `serverIndex = hash(key) % N`, if N changes (a server goes down) almost all keys are reassigned, causing a storm of cache misses.
**Consistent hashing** (Karger, MIT): when resizing, only ~`k/n` keys are remapped on average (k keys, n slots).
- **Hash ring**: the hash space (e.g. SHA-1: 0 to 2^160-1) is closed into a ring; servers (by IP or name) and keys are mapped with the same function, with no modulo.
- **Lookup**: from the key's position, go clockwise to the first server.
- **Adding a server**: only the keys between the new server and its predecessor move (counterclockwise until the next server). **Removing**: its keys go to the next server clockwise.
- Two problems with the basic approach: unequal partition sizes and non-uniform key distribution.
- **Virtual nodes (replicas)**: each server appears as several virtual nodes (s0_0, s0_1...). More vnodes = more balanced distribution: the standard deviation is ~10% of the mean with 100 vnodes and ~5% with 200; cost: more memory for metadata (tunable parameter).
- Benefits: minimal redistribution, horizontal scaling with even distribution, mitigates hot keys (celebrity problem).
- Used in: Dynamo, Cassandra, Discord, Akamai CDN, Maglev. Used in [[key-value-store]] for partitioning.

## Additional detail (Grokking, pp. 189-192)
- Context: DHT (`index = hash_function(key)`); with simple modulo it does not scale horizontally (adding a host breaks all mappings) and may be unbalanced with non-uniform data.
- Example ring [0, 256): hash servers and keys onto the ring and advance clockwise to the first server. Adding D only takes keys from its neighbor; if A goes down, its keys go to B.
- To balance, map each cache to **several points on the ring (virtual replicas)**; the more there are, the better the balance.
- Uses in the source: replacing dead hosts and spreading load in video caches ([[youtube]]), [[web-crawler]] servers, rate limiter, server assignment per show in [[ticketmaster]].

## Additional detail (DDIA, ch. 6)
- Nuance: Kleppmann warns that the term "consistent hashing" is used confusingly and that, as defined by Karger et al. (choosing random partition boundaries), it works poorly for databases; in practice a fixed number of partitions or dynamic partitioning is preferred (see [[database-partitioning]]). It has nothing to do with the "consistency" of ACID or of replication.

## Appears in
[[ad-click-aggregator]], [[distributed-cache]], [[distributed-rate-limiter]], [[fb-live-comments]], [[key-value-store]], [[metrics-monitoring]], [[nearby-friends]], [[pastebin]], [[s3-object-storage]], [[search-query-cache]], [[twitter]], [[twitter-search]], [[url-shortener]], [[web-crawler]], [[whatsapp]]

## See also
[[database-partitioning]], [[websockets]]
