---
title: Serializability (serial execution, 2PL, SSI)
type: concept
aliases: [serializable isolation, two-phase locking, 2PL, SSI, serializable snapshot isolation, actual serial execution, predicate locks, index-range locks]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 7 (pp. 251-262)]
---

# Serializability

## Definition
The strongest isolation level: the result of running concurrent transactions is equivalent to running them one after another in some order, even with write skew and phantoms.

## Why it matters
It completely eliminates the class of race conditions that weak levels leave to the application and that are hard to test.

## How it works (three implementations)
1. **Actual serial execution**: a single thread runs transactions in order (VoltDB, Redis, Datomic). Viable because RAM is cheap (data in memory) and OLTP transactions are short. Requires *stored procedures* (no user interaction inside the transaction), general-purpose languages (Java/Lua). Scaling: partition so each transaction touches a single partition; multi-partition ones are orders of magnitude slower; throughput limited to one CPU per partition.
2. **Two-phase locking (2PL)**: readers and writers block each other. Shared (read) and exclusive (write) locks held until commit/abort (phase 1: acquire; phase 2: release at the end). Deadlocks are detected and one transaction is aborted. For phantoms: **predicate locks** (on a search condition, even nonexistent rows) or their efficient approximation **index-range locks (next-key locking)**; if there is no suitable index the whole table is locked. Drawback: worse performance and very high tail latencies; one slow transaction can block the others.
3. **Serializable Snapshot Isolation (SSI)**: optimistic. On top of snapshot isolation, it detects when a decision was based on an outdated premise (read of a version that has since been overwritten / write that affects a previous read) and aborts at commit. Readers don't block writers. Advantage: good performance with low contention; cost in aborts with high contention and long read-write transactions. (PostgreSQL ≥ 9.1 and FoundationDB.)

## Variants and techniques
Pessimistic (2PL) vs optimistic (SSI) vs serial. Detection of an outdated premise in SSI: MVCC reads ignored by another write / writes that affect previous reads.

## Trade-offs
- Serial: maximum simplicity, single-core throughput.
- 2PL: simple semantics, a lot of contention and deadlocks.
- SSI: scales better on reads, aborts under contention.
- Note: don't confuse with linearizability ([[linearizability]]): serializability is about transactions (multi-object); linearizability is about recency of a single object. "Strict serializability" combines both.

## When to use it / when not to
When there are invariants across concurrent objects (reservations, balances). Avoid if the workload has a lot of contention on a few rows and waiting/aborts are not tolerated.

## Appears in


## See also
[[transactions-and-isolation-levels]], [[two-phase-commit]], [[optimistic-concurrency-control]], [[distributed-lock]]
