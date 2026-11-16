---
title: Digital Wallet
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 12 Digital Wallet, pp. 341-377]
concepts: [event-sourcing, cqrs, two-phase-commit, saga, consensus, database-partitioning, service-discovery, lsm-trees, write-ahead-log, idempotency, reconciliation]
difficulty: high
---

# Digital Wallet

## Prompt
Backend of a digital wallet (PayPal-style) that supports **balance transfer between two wallets** on the same platform (faster and with no extra fee compared to a bank transfer).

## Functional requirements
- Transfer balance between two wallets (other features and currencies out of scope).

## Non-functional requirements
- **1 M TPS**.
- Reliability >= 99.99%.
- Transactional guarantees.
- **Reproducibility**: be able to rebuild the historical balance by replaying the data from the beginning (reconciliation only shows discrepancies, not how they were generated).

## Estimations
- A typical relational node supports about 1,000 TPS -> 1 M TPS = 1,000 nodes; but each transfer is 2 operations (debit and credit) -> 2 M TPS = **2,000 nodes**. With 20,000 TPS/node, 100 would suffice (source table: 1,000/2,000 nodes at 1,000 TPS; 100/200 at 10,000-20,000 TPS). Design goal: increase TPS per node.

## API
`POST /v1/wallet/balance_transfer`: from_account, to_account, amount (string, not double; see [[payment-system]]), currency (ISO 4217), transaction_id (UUID for deduplication). Response: status and transaction_id.

## Data model
- State = `account -> balance` map (key-value; a relational DB can be seen as KV with a PK).
- **Phase status** table (in the source account's DB): ID and content of the distributed transaction, state of the Try phase per DB (not sent/sent/response received), name of the second phase (Confirm/Cancel), its status and an out-of-order flag.
- In event sourcing: command list, event list, state (RocksDB/SQLite) and snapshots.

## Architecture (high-level design)
Three evolving designs:
1. **In-memory Redis with sharding**: partition `hash(accountID) % n`, number of partitions and addresses in ZooKeeper; stateless wallet service that validates and updates two Redis nodes. Correctness fails: if the service crashes between the two updates the transfer is left incomplete, and the data is not durable.
2. **Sharded transactional DB + distributed transactions**: each Redis node is replaced by a relational DB; two updates in different DBs must be made atomic (2PC, TC/C or Saga).
3. **Event sourcing** with reproducibility (final design).

## Deep dives
**Distributed transactions**
- **2PC** (low-level solution, XA): prepare phase and commit/abort; holds locks for a long time and the coordinator (wallet service) is a SPOF; poor performance ([[two-phase-commit]]).
- **Try-Confirm/Cancel (TC/C)**: compensation in the business layer, each phase is an independent local transaction. Try: A -$1 (in C, NOP); Confirm: C +$1; Cancel: A +$1 (undo; in C NOP). Difference from 2PC: in 2PC the local transactions are still unfinished when the second phase starts; in TC/C they are already completed and the second phase applies the inverse. DB-independent (it only needs transactions), but the complexity moves to the application.
  - *Unbalanced state*: after Try $1 is missing (A + C = 0 temporarily); the application sees the intermediate state.
  - *Valid Try order*: the only valid option is to subtract from A and NOP in C (subtracting from C first, or doing it in parallel, is invalid because of the risk that someone moves the money or partial failures).
  - *Out-of-order execution*: a Cancel can arrive before its Try; the Cancel leaves a flag and the Try always checks it and fails if it exists.
- **[[saga]]**: de facto in microservices; linear operations, each a transaction in its own DB; on a failure rollback happens in reverse order with compensating transactions (n operations + n compensations). Coordination: **choreography** (decentralized via events; each service with its own state machine, hard with many services) or **orchestration** (single coordinator; preferred in wallets). Debit first and then credit.
- **TC/C vs Saga**: TC/C allows parallel execution (better latency with many services), Saga is linear; with few services or no latency requirement, either works (Saga by trend).

**Event sourcing** ([[event-sourcing]]): answers the audit questions (balance at any point in time, historical and current correctness, correctness after code changes). Terms: **command** (external intent, in a FIFO queue, may contain randomness/I/O and may be invalid), **event** (validated, immutable fact, in the past tense, deterministic; a command generates zero or more events; event order follows command order), **state** (balances) and **state machine** (validates commands -> events and applies events to state; must be deterministic). Example: command A->$1->C generates events A:-1 and C:+1. **Reproducibility**: replaying from the beginning always gives the same state; code versions can be run over the same events and compared.
- **[[cqrs]]**: one write state machine and several read-only ones that rebuild views from the published events (eventually consistent).

**High-performance event sourcing**: command and event list in append-only **local files** (fast sequential writes; `mmap` to cache in memory), state in SQLite/RocksDB (LSM, write-optimized, with cache), and periodic **snapshots** (e.g. at 00:00 for finance) in object storage/HDFS to avoid reprocessing from the start.

**Reliability**: state and snapshots are regenerated from the events; commands are not enough because event generation may not be deterministic; **only the event list needs high reliability** -> replication with **Raft consensus** (leader, candidates, followers; works as long as more than half are alive: 3 nodes tolerate 1 failure, 5 tolerate 2). The leader receives commands, converts them into events and Raft replicates them; all nodes apply events and obtain the same state. If the leader fails, another is elected; the client resends the command if there was no response; follower failures are retried indefinitely.

**Distributed event sourcing**: (1) pull with polling is not real time and adds load; improved with a **reverse proxy** that forwards the command and receives the state by **push** from the read-only state machine; (2) a Raft group has limited capacity -> partition accounts (key hash) into Raft groups and coordinate with **TC/C or Saga** (final design). Flow with Saga (15 steps): the coordinator creates a record in phase status, sends A:-$1 to partition 1 (command -> validate -> event -> Raft -> apply -> CQRS -> push to the coordinator), records success and then sends C:+$1 to partition 2 with the same cycle, and responds to the caller.

## Trade-offs and decisions
- Redis (fast, neither durable nor atomic) -> transactional DB + 2PC/TC/C/Saga (atomic, hard to audit) -> event sourcing (reproducible and auditable).
- Local files (performance) versus remote Kafka/DB, compensated by Raft replication.
- 2PC (blocking) vs TC/C (business-level compensation, parallel) vs Saga (linear, orchestrated).
- Eventual consistency of the read path vs reverse proxy with push.

## Related concepts
[[event-sourcing]], [[cqrs]], [[two-phase-commit]], [[saga]], [[consensus]], [[database-partitioning]], [[service-discovery]], [[lsm-trees]], [[write-ahead-log]], [[idempotency]], [[reconciliation]]

## Follow-up questions
- How to audit and find the root cause of erroneous operations (event sourcing).
- How to make a system that processes one event at a time faster.
- Reliability of a server with data on local disk; scaling to 1 M TPS.

## Variants
Not covered in the source (compare with [[payment-system]], ch. 11, for the payment flow with a PSP).
