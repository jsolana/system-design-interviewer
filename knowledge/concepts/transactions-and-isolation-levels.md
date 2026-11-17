---
title: Transactions, ACID and isolation levels
type: concept
aliases: [ACID, read committed, snapshot isolation, MVCC, repeatable read, lost update, write skew, phantoms, dirty read]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 7 (pp. 221-262), Programming Interviews Exposed 3rd ed. ch. 12 (pp. 182-183)]
---

# Transactions, ACID and isolation levels

## Definition
A transaction groups several reads/writes into a logical unit that either commits or aborts (rollback), allowing safe retries. The guarantees are summarized as **ACID**.

## Why it matters
Simplifies the application's failure model (crashes, partial writes, concurrency). Without them you have to reason by hand about every interleaving.

## How it works
- **ACID**: Atomicity (all or nothing, abortability), Consistency (invariants of the *application*; a property of the app, not of the DB), Isolation (as if executed serially), Durability (committed data is not lost; WAL/replication).
- Single-object: atomicity and isolation per row (log for crash, lock per object), atomic operations (increment), compare-and-set. Multi-object: needed for foreign keys, secondary indexes, denormalization.
- Aborting and retrying is not trivial: the request may have been committed despite a network error (use [[idempotency]]), overload, external effects.

### Isolation levels and anomalies
| Level | Prevents | Mechanism |
|---|---|---|
| Read committed | dirty reads, dirty writes | row locks for writing; reads return the old committed value |
| Snapshot isolation (repeatable read) | additionally non-repeatable reads / read skew | **MVCC**: several versions per row, each transaction sees the snapshot at its start (txid) |
| Serializable | everything (incl. write skew and phantoms) | see [[serializability]] |
- **MVCC**: each row has created_by/deleted_by; a version is visible if it was created by a transaction already committed at snapshot start and not deleted; GC of old versions. Readers never block writers. In B-trees copy-on-write can be used ([[b-trees]]). "Repeatable read" in the SQL standard is ambiguous: Oracle calls it serializable, PostgreSQL/MySQL repeatable read.
- **Lost update** (concurrent read-modify-write): atomic operations, `SELECT ... FOR UPDATE`, automatic detection (PostgreSQL, Oracle, SQL Server under snapshot isolation; MySQL/InnoDB does not), **compare-and-set** ([[optimistic-concurrency-control]]). In multi-leader/leaderless replication: merging siblings/commutative operations ([[conflict-resolution]]).
- **Write skew**: two transactions read the same set, decide and write different objects (two on-call doctors going off call at the same time; room booking; username; double spending). Only serializable avoids it without tricks; alternative: explicitly lock the rows read (`FOR UPDATE`) or materialize conflicts (table of time slots, ugly).
- **Phantom**: a write changes the result of another transaction's earlier search.

## Variants and techniques
Dirty writes are avoided with row-level locks until commit; long reads (backups, analytics) with snapshot isolation.

## Trade-offs
- Interview-book framing (Programming Interviews Exposed ch. 12): the canonical example is a money transfer (debit + credit) wrapped in one transaction so both commit or neither does. Guaranteeing all four ACID properties on every transaction has a significant performance cost, isolation most of all, so most systems let you relax isolation. ACID is not a requirement of relational databases, though most modern ones support it. Referential integrity (primary/foreign keys) is a complementary consistency mechanism.
- The stronger the isolation, the higher the performance cost and aborts. Many NoSQL systems lack multi-object transactions; they pay with anomalies that the application must handle.

## When to use it / when not to
Whenever there are invariants across several objects (payments, reservations, inventory). Choose the level consciously: snapshot isolation is usually enough for reads; critical things (balances, seats) require serializable or explicit locking.

## Appears in
[[hotel-reservation]]

## See also
[[serializability]], [[two-phase-commit]], [[optimistic-concurrency-control]], [[distributed-lock]], [[idempotency]]
