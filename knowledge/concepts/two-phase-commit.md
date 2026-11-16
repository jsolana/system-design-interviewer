---
title: Two-phase commit (2PC) and distributed transactions
type: concept
aliases: [2PC, atomic commit, XA transactions, distributed transactions, in-doubt]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 12 pp. 346-349, Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 9 (pp. 354-364)]
---

# Two-phase commit (2PC)

## Definition
An **atomic commit** algorithm across several nodes: either all commit or all abort. A *coordinator* manages the decision.

## Why it matters
It preserves atomicity in transactions that span several partitions, DBs, or a DB and a message broker, e.g. processing a message exactly once ([[exactly-once-processing]]).

## How it works
1. The application obtains a global transaction ID and executes on each participant.
2. **Phase 1 (prepare)**: the coordinator asks each participant whether it can commit. By saying "yes" the participant promises it will be able to commit (writes everything to disk) and gives up the right to abort unilaterally.
3. If all say yes: the coordinator **writes its decision to its log** (*commit point*) and sends commit (phase 2); otherwise, abort. It retries indefinitely if a participant does not respond.
- If the coordinator crashes after prepare, participants are left **in-doubt**, holding locks until the coordinator comes back (blocking; it is not a non-blocking protocol). It requires recovery using its log; some systems allow "heuristic decisions" (which break atomicity).

## Variants and techniques
- **XA** (standard interface to the transaction manager) for heterogeneous DBs.
- Distributed transactions **internal** to a DB (VoltDB, MySQL Cluster) can be optimized; **heterogeneous** ones are harder.
- Alternative in modern systems: atomic commit backed by fault-tolerant consensus (a replicated coordinator), or avoiding them with logs and idempotent events ([[event-sourcing]], sagas ([[workflow-orchestration]])).

## Trade-offs
- The coordinator is a SPOF if not replicated; held locks amplify failures.
- Complicated to operate; reduced performance (fsync and round trips; distributed MySQL transactions ~10x slower than single-node according to the source).
- Consensus is more general: 2PC does not elect a coordinator and is not tolerant to coordinator failure.

## When to use it / when not to
When strong atomicity is needed across systems with XA support; avoid across heterogeneous services if eventual consistency with idempotence and retries is enough.

## Additional detail (Xu & Lam Vol. 2, ch. 12)
Prepare (the coordinator asks all DBs to prepare and hold locks) and commit/abort. It is a low-level solution (X/Open XA standard) with poor performance: locks are held while waiting for other nodes and the coordinator is a single point of failure. Application-level alternatives: TC/C and [[saga]]. See [[digital-wallet]].

## Appears in
[[digital-wallet]], [[hotel-reservation]], [[payment-system]]

## See also
[[consensus]], [[transactions-and-isolation-levels]], [[idempotency]], [[workflow-orchestration]], [[distributed-lock]]
