---
title: Transactional outbox
type: concept
aliases: [outbox pattern, transactionally staged job drain, staged jobs, dual-write problem]
sources: [https://microservices.io/patterns/data/transactional-outbox.html, https://brandur.org/job-drain, https://brandur.org/postgres-queues, https://brandur.org/idempotency-keys]
---

# Transactional outbox

## Definition
A way to update a database and publish a message (or enqueue a job) atomically without a distributed transaction: the message is written to an **outbox** table/record in the same local DB transaction as the business data, and a separate **relay** forwards it to the broker afterwards.

## Why it matters
- The dual write "update DB, then send message" is unsafe: sending inside the transaction may fire before commit (consumer cannot find the data) or after a rollback; sending after the commit loses the message if the process crashes in between.
- 2PC across DB and broker is usually not available or not desirable.

## How it works
1. In one local transaction: write business rows + insert the message row into the outbox (relational: a table; NoSQL: a property of the record).
2. A message relay reads the outbox and publishes to the broker. Two implementations named by microservices.io: **polling publisher** and **transaction log tailing** (CDC, see [[change-data-capture]]).
3. After a successful publish the relay deletes/marks the row. A crash between publish and delete causes a re-publish.
- Brandur's version ("transactionally staged job drain"): jobs go in a `staged_jobs` table in the same transaction as their data; a single enqueuer process reads batches, pushes them to the real queue (e.g. Sidekiq/Redis) and deletes them only after the push succeeds. Isolation keeps staged jobs invisible until commit, and rolled-back jobs vanish.

## Variants and techniques
- Event sourcing is the other way to get atomic "state change + event" ([[event-sourcing]]).
- Postgres-as-queue: jobs in the same DB give transactional enqueueing, but Brandur's experiment shows that a long-lived transaction (e.g. analytics on a follower) blocks dead-tuple cleanup; lock scans walk ever more dead index entries, lock time rose from <0.01s to >=0.1s (about 15x), ~100k dead tuples, and the queue ran away once enqueue rate exceeded work rate. Staging in a table and draining to Redis was far more resistant. Safeguards: kill long transactions, `statement_timeout`, do not share the DB across teams.

## Trade-offs
- Guarantees: message sent iff the transaction commits; order preserved as written.
- At-least-once: duplicates are possible, so consumers must be idempotent (track processed message IDs) - see [[idempotency]].
- Error-prone for developers (forgetting to write the outbox row); extra relay process (single instance or lock needed for ordering); extra latency hop.

## When to use it / when not to
Use for reliable events/commands out of a service owning a DB (saga steps, CDC-style integration, background jobs that depend on committed data). Not needed if the DB itself is the queue consumer or when losing a message is acceptable.

## Appears in
[[digital-wallet]], [[payment-system]]

## See also
[[saga]], [[change-data-capture]], [[idempotency]], [[message-queues]], [[exactly-once-processing]], [[microservices-architecture]]

## Note: what a senior/staff candidate should say
Name the dual-write problem explicitly, propose outbox + relay (log tailing for low latency, polling for simplicity), state that delivery is at-least-once so consumers dedupe by ID, and mention operational risks (relay lag monitoring, outbox table growth, long transactions).
