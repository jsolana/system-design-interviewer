---
title: Distributed lock
type: concept
aliases: [distributed lock, Redis lock]
sources: [https://jepsen.io/analyses/etcd-3.4.3, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, Designing Data-Intensive Applications (Kleppmann), ch. 8]
---

# Distributed lock

## Definition
Mutual exclusion between different processes, normally with a shared store (Redis) and a TTL.

## Why it matters
Allows temporarily reserving a resource (seat) during a long flow (checkout) without keeping DB locks open.

## How it works
- Redis `SET key value NX EX <ttl>`: key = ticketId, value = userId, TTL 10 min. Atomic acquisition and automatic expiration.
- Multi-resource: acquire one by one and release all if one fails; Lua script to make it atomic if the keys are on the same node.
- Reading reserved items: sorted set by expiration (`ZADD`, count future scores, `ZREMRANGEBYSCORE`) to avoid ghost entries.

## Variants and techniques
Alternatives: `SELECT FOR UPDATE` (bad for long checkouts), state + expiration with cron, implicit state (reserved with expiration in the row).

## Trade-offs
- If Redis goes down: errors at payment, but [[optimistic-concurrency-control]] / row locks in the DB prevent double selling.
- If the TTL expires during payment: one write wins and the other is refunded; mitigate with a generous TTL or by extending it when payment starts.

## When to use it / when not to
Temporary reservations with a timeout. Keep the DB as the final source of truth.

## Additional variants (Uber, Gopuff)
- [[uber]]: Redis lock on driverId with a 10 s TTL (= acceptance window) so a driver is not assigned to two rides; accepting releases the lock and updates the DB; expiration returns the driver to available. Worse: locks in the application (no coordination, left hanging if the instance goes down) or state in the DB with an in-memory timeout + cron.
- [[gopuff]]: a lock across two stores (orders and inventory) leaves risks of overselling and deadlock; a SERIALIZABLE transaction in a single DB is preferable.

## Additional detail (DDIA, ch. 8)
- **Fencing tokens**: a lock/lease with a TTL is not safe by itself: a client can pause (GC, VM) and keep believing it is the owner after its lease expires. Solution: each grant returns an increasing token (in ZooKeeper the zxid or the cversion) and the protected resource rejects writes with a token lower than the one already seen ([[distributed-system-faults]]).
- A reliable lock/lease service relies on [[consensus]] (ZooKeeper/etcd: linearizable compare-and-set + sessions with heartbeats), not on local clocks ([[linearizability]]).

## Additional detail (Jepsen etcd 3.4.3)
Source: https://jepsen.io/analyses/etcd-3.4.3. etcd locks did not provide mutual exclusion: two clients held the same lock simultaneously even in healthy clusters (lease not rechecked after waiting); with 1-3 s lease TTLs and pauses/partitions ~18% of acknowledged updates to a lock-protected set were lost. Use such locks for efficiency only; for safety use **fencing tokens** (e.g. lock key revision) and have the protected resource reject lower tokens. See [[consistency-anomalies-jepsen]].

## Appears in
[[flash-sale]], [[gopuff]], [[ticketmaster]], [[uber]], [[web-crawler]]

## See also
[[optimistic-concurrency-control]], [[idempotency]]
