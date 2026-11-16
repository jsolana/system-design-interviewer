---
title: Optimistic Concurrency Control (OCC)
type: concept
aliases: [OCC, optimistic locking, conditional update]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 7 pp. 205-221, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, Designing Data-Intensive Applications (Kleppmann), ch. 7]
---

# Optimistic Concurrency Control (OCC)

## Definition
Concurrency control without blocking: writes are conditional and, if someone else changed the data, the write fails.

## Why it matters
Guarantees a single winner (no double booking) without long-held locks.

## How it works
Short transaction with a conditional update. "Implicit state" example: if the ticket is AVAILABLE, or RESERVED with an expired reservation, set it to RESERVED with expiration = now + 10 min; commit.

## Variants and techniques
Can be combined with [[distributed-lock]] as a safety net; materialized views or composite indexes for the double read condition.

## Trade-offs
Retries/failures for the loser (e.g. refund via Stripe); reads with a double condition.

## When to use it / when not to
Moderate contention and short transactions; not for holding resources for minutes.

## Additional detail (DDIA, ch. 7)
- It is the way to avoid **lost updates** without locks: *compare-and-set* (`UPDATE ... WHERE value = <what was read>`; check affected rows and retry) or a version column. It is not safe if the WHERE clause reads from an old snapshot. Alternatives: atomic operations (`counter = counter + 1`), `SELECT ... FOR UPDATE`, automatic detection under snapshot isolation (PostgreSQL, Oracle) ([[transactions-and-isolation-levels]]).
- **SSI** (serializable snapshot isolation) is the optimistic version at the database level: it detects stale premises and aborts at commit ([[serializability]]).
- In multi-leader/leaderless replication, the equivalent is version vectors and sibling merging ([[conflict-resolution]]).

## Additional detail (Xu & Lam Vol. 2, ch. 7)
Three options for the "last room" race ([[hotel-reservation]]): **pessimistic locking** (`SELECT ... FOR UPDATE`; serializes, useful with high contention, but deadlocks and poor scalability), **optimistic locking** with a `version` column (better than timestamp because of inaccurate clocks; the update only succeeds if the version is the expected one +1; no locks but many retries under high contention) and **database constraints** (`CHECK(total_inventory - total_reserved >= 0)`; simple, but not versionable as code and not portable across DBs). With low contention (few reservations/s) the last two are adequate.

## Appears in
[[flash-sale]], [[hotel-reservation]], [[online-auction]], [[ticketmaster]]

## See also
[[distributed-lock]], [[idempotency]]
