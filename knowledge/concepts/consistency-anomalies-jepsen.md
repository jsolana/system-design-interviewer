---
title: Consistency anomalies found by Jepsen
type: concept
aliases: [Jepsen, Elle, isolation anomalies in real databases, consistency model hierarchy]
sources: [https://jepsen.io/analyses, https://jepsen.io/consistency, https://jepsen.io/consistency/models, https://jepsen.io/analyses/postgresql-12.3, https://jepsen.io/analyses/mongodb-4.2.6, https://jepsen.io/analyses/etcd-3.4.3, https://blog.acolyer.org/2020/11/23/elle/]
---

# Consistency anomalies found by Jepsen

## Definition
Jepsen tests real distributed databases under faults (partitions, crashes, pauses, clock skew) and checks histories against consistency models. A consistency model is a safety property defining the set of legal histories; phenomena (G0, G1a, G1b, G1c, G-single, G2-item...) are patterns of dependencies between transactions that models forbid (forbidding cycles in the dependency graph).

## Why it matters
Shows that documented guarantees and marketing ("full ACID", "serializable") often differ from observed behavior, and gives concrete failure examples to cite.

## How it works: model hierarchy (jepsen.io/consistency/models)
- Transactional: strict serializable > serializable > repeatable read and snapshot isolation > ... cursor stability / monotonic atomic view > read committed > read uncommitted.
- Single object: strict serializable > linearizable > sequential > causal > PRAM > monotonic reads, monotonic writes, read your writes.
- Availability in async networks: **not available** under partitions: cursor stability, snapshot isolation, sequential and everything stronger (repeatable read, serializable, strict serializable, linearizable); **sticky available**: read your writes, PRAM, causal; **totally available**: read committed, read uncommitted, monotonic atomic view.

## Findings (case studies)
| System | Finding |
|---|---|
| PostgreSQL 12.3 | `SERIALIZABLE` allowed G2-item (6 cases in a 2-minute run) due to an SSI conflict-detection bug involving fresh inserts with 3 concurrent transactions (presumed present since 2011, fixed in a minor release). `REPEATABLE READ` behaves as snapshot isolation (G2-item about 140/min); no G0/G1a/G1b in read committed. Advice: treat repeatable read as SI; for sensitive transactions use serializable, explicit locks, or tolerate G2. |
| MongoDB 4.2.6 | Transactions ignored DB/collection read/write concern defaults (local, w:1) allowing lost writes and uncommitted reads; `snapshot` needs `majority` writes too, even read-only. Even at strongest settings: read skew (G-single), G1c, duplicated retried effects, internal inconsistency; ~10% of transactions in cycles in one fault-free run (1,461 of 13,914). Cause traced to a retry bug (patch in 4.2.8). Advice: set concerns per transaction; call it snapshot isolated, not "full ACID". |
| etcd 3.4.3 | KV reads/writes/multi-key txns strict serializable under all tested faults (stale reads only with the documented `serializable` flag). **Locks do not give mutual exclusion**: two holders at once, even healthy; with 2 s TTLs and pauses ~18% of acknowledged updates lost; cause: lease not rechecked after waiting. Advice: use locks for performance only, use fencing tokens (e.g. lock key revision) for safety ([[distributed-lock]]). |

Tooling: Elle (Kingsbury and Alvaro, VLDB 2020) infers the dependency graph from histories with unique/appended values (list appends make write order recoverable) and finds cycles in linear time; checks histories of hundreds of thousands of transactions in tens of seconds, where the earlier Knossos handled hundreds. Found anomalies in TiDB, YugaByteDB, Fauna, Dgraph (Acolyer summary). Sound but not complete; tests prove presence of bugs, not absence.
The Jepsen index also lists analyses of MySQL 8.0.34, RDS PostgreSQL 17.4, CockroachDB, Redis-Raft, NATS, Redpanda, TigerBeetle and others (not read here).

## Trade-offs
Stronger models cost availability and latency; weaker models need application-level handling (materialize conflicts as writes, explicit locks).

## When to use it / when not to
Use when choosing an isolation level or datastore for correctness-critical data (money, locks, inventory). Don't trust a label; check the isolation level actually provided.

## Appears in
None yet.

## See also
[[transactions-and-isolation-levels]], [[serializability]], [[linearizability]], [[distributed-lock]], [[eventual-consistency]], [[distributed-systems-testing]], [[consensus]]

## Note: what a senior/staff candidate should say
Name the isolation level you rely on and the anomaly it still allows (e.g. write skew under snapshot isolation), say locks need fencing tokens, and that you would verify claims with fault-injection testing.
