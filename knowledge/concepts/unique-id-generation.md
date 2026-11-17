---
title: Unique ID generation (hash vs counter)
type: concept
aliases: [unique short code, counter-based ids, id generation]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, System Design Interview Vol.1 (Alex Xu), ch. 7 and 8, Grokking the System Design Interview (PDF), "Designing Instagram" pp. 44-47 and "Designing Twitter" pp. 77-78, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 10 (pp. 417-425)]
---

# Unique ID generation (hash vs counter)

## Definition
Techniques for producing unique, short identifiers (e.g. short codes) without collisions.

## Why it matters
Uniqueness is the central requirement of a URL shortener: one code = one single destination.

## How it works
- **Hash**: canonicalize the input, hash (SHA-256), [[base62-encoding]], truncate (8 chars = 62^8 ≈ 218T). Deterministic, allows dedup.
- **Counter**: atomic counter (Redis INCR) encoded in base62. No collisions, decodable.

## Variants and techniques
- Hash: UNIQUE constraint + bounded retries (3-5) with a random salt; HMAC/secret salt against guessing.
- Counter: **batching** (each instance reserves a block, e.g. 1000, with a single increment); Redis Sentinel/Cluster for failover; **disjoint ranges per region** to avoid cross-region coordination; XOR with a secret key to avoid enumeration.
- Losing unreplicated counter values is acceptable: only uniqueness matters. The DB UNIQUE constraint is the final safety net.

## Trade-offs
| | Hash | Counter |
|---|---|---|
| Collisions | Grow as it fills up | None |
| Coordination | None | Distributed counter |
| Security | Guessable without salt | Sequential/enumerable |
| Length | Fixed | Grows over time |

## When to use it / when not to
Counter when guaranteed uniqueness and scale are needed; hash when deterministic dedup without shared state is wanted.

## Additional detail (Xu Vol. 1, chs. 7 and 8)
64-bit numeric IDs sortable by time in distributed environments (see [[unique-id-generator]]): multi-master auto_increment with step k, 128-bit UUID, ticket server (Flickr) and **Snowflake** (1 sign bit + 41 timestamp ms + 5 datacenter + 5 machine + 12 sequence; ~69 years, 4096 IDs/ms/machine, requires clock synchronization/NTP). In the URL shortener, an alternative to the counter is "hash (CRC32/MD5/SHA-1) truncated to 7 characters + collision resolution" ([[url-shortener]]).

## Additional detail (Grokking: time-sortable IDs)
- **PhotoID/TweetID = epoch in seconds + auto-incrementing sequence**, so that the ID encodes the date, serves as a primary key sortable by recency and allows deriving the shard (e.g. `PhotoID % 10`).
- Sizes: 86,400 x 365 x 50 ≈ 1.6 B seconds -> 31 bits for 50 years. [[instagram]] (23 photos/s): 9 bits of sequence (512/s) = 40 bits; [[twitter]] (1,150 tweets/s): 17 bits (~130K/s) = 48 bits. The sequence resets every second. With 64 bits, 100 years fit in milliseconds.
- Generation: a dedicated DB with a table holding only a 64-bit ID (auto-increment); two instances (even/odd using the auto_increment step) behind an LB to avoid a SPOF; they can get out of sync without a problem. Alternative on shards: local auto-increment + shard prefix. For short keys offline: [[key-generation-service]].

## Additional detail (DDIA 2nd edition, ch. 10)
- *2nd edition (new section "ID Generators and Logical Clocks")*: a single-node autoincrement counter is a linearizable fetch-and-add, but it is a SPOF, slow across regions and a bottleneck. Alternatives and what they lose: odd/even or shard-number bits (lose ordering), **blocks of IDs** (lose ordering), **UUID v4** (128 bits, random order), **timestamp + shard + sequence/random** (UUIDv7, Snowflake, ULID, Hazelcast Flake, MongoDB ObjectID; only as ordered as the NTP-synced clocks).
- **Logical clocks**: Lamport (counter, nodeID) is consistent with causality but not linearizable and unrelated to wall time; **hybrid logical clocks** (physical time that moves forward to the max seen, always incrementing; near wall-clock semantics, only roughly synced clocks needed; good for MVCC transaction IDs); **vector clocks** detect concurrency but cost one counter per node. None gives linearizable IDs: example of a private-account setting changed on one device and a photo uploaded later from another, stored in separate databases with their own logical clocks, can be exposed.
- **Linearizable ID generators**: need consensus or TrueTime-style clock uncertainty waits (Spanner).
- See also [[logical-clocks-and-causality]], [[consensus]].

## Appears in
[[hotel-reservation]], [[twitter]], [[twitter-search]], [[unique-id-generator]], [[url-shortener]], [[whatsapp]]

## See also
[[base62-encoding]], [[database-indexing]]
