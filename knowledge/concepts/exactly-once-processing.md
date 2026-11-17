---
title: Exactly-once processing (effectively-once)
type: concept
aliases: [exactly-once semantics, at-least-once, at-most-once, end-to-end argument, deduplication, request ID, atomic commit of messages]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 4 pp. 91-130, Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 11 (fault tolerance en streams), ch. 12 (end-to-end argument, pp. 515-545), ch. 9 (p. 360), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 8 (pp. 334-335)]
---

# Exactly-once processing

## Definition
Guarantee that the **visible effect** of processing each message is as if it had been processed only once, even though there are internal retries. More descriptively: *effectively-once*.

## Why it matters
Retries after failures (at-least-once) duplicate effects (charges, emails, counters). Disabling retries (at-most-once) loses data.

## How it works
- **Batch**: tasks are retryable because the input is immutable and the output is only published when the task finishes ([[batch-processing]]).
- **Stream**: you cannot wait for the end; solutions: **microbatching** (Spark Streaming, ~1 s, implicit window by processing time) or periodic state **checkpoints** with barriers (Flink) and discarding output after the last checkpoint.
- This holds *within* the framework; when the output goes out to a DB, broker or email, a retry repeats the external effect.
- For external effects: **atomic commit** between processing and output ([[two-phase-commit]], XA, internal transactions in Kafka/Flink) or, better, **idempotent** operations: compare-and-set/version, storing the message offset together with the state, or an **operation ID** ([[idempotency]]).
- **End-to-end argument** (Saltzer et al.): TCP, DB transactions or stream processors are not enough; deduplication must be done end to end, e.g. the client generates a unique request/operation ID (UUID, or hash of form fields) that is propagated to the DB and checked in a table with a uniqueness constraint.
- Also, a node that failed and came back may be a "zombie": use fencing ([[distributed-system-faults]]).

## Variants and techniques
- Uniqueness/balance constraints without a distributed transaction: partition the log by the unique value and process sequentially (single-thread per partition) with a processor that emits success/rejection ([[derived-data-and-dataflow]]).
- Transfer A->B: request with request ID in a log (atomic, a single message), a processor emits debit (partition of A) and credit (partition of B) with that ID, and downstream processors deduplicate by ID; avoids atomic commit across partitions.

## Trade-offs
Coordination cost vs duplicates. Idempotence is cheaper and more robust than 2PC; it requires stable IDs and storage of seen IDs.

## When to use it / when not to
Payments, inventory, counters, notifications. If the effect is naturally idempotent (upsert), at-least-once is enough.

## Additional detail (Xu & Lam Vol. 2, ch. 4)
Semantics in a queue: at-most-once (ACK=0, offset commit before processing), at-least-once (ACK=1/all with retries, commit after processing; duplicates can be deduplicated with a unique key) and exactly-once (high cost; payments, trading, accounting when the destination is not idempotent). See [[distributed-message-queue]].

## Additional detail (DDIA 2nd edition, ch. 8)
- *2nd edition (explicit recipe)*: exactly-once does not need a distributed transaction across broker and DB. Keep a table of processed message IDs in the DB: in one local transaction check/insert the ID (unique constraint), do the processing writes, commit; then ack the broker; later delete the ID in a separate transaction. Crash before commit -> retry; crash after commit before ack -> retry sees ID and drops. Same idea in Kafka Streams. Internal distributed transactions still help when IDs and data live on different shards.

## Appears in
[[ad-click-aggregator]], [[distributed-message-queue]], [[payment-system]]

## See also
[[idempotency]], [[stream-processing]], [[message-queues]], [[two-phase-commit]], [[payment-system]]
