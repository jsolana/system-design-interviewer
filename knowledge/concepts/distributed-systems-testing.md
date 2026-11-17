---
title: Testing and verifying distributed systems (formal methods, fault injection, DST)
type: concept
aliases: [deterministic simulation testing, DST, Jepsen, chaos engineering, fault injection, model checking, TLA+]
sources: [Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 2 (p. 44) and ch. 9 (pp. 384-388), https://sre.google/sre-book/testing-reliability/]
---

# Testing and verifying distributed systems

## Definition
*2nd edition (new section).* Techniques to gain confidence that algorithms and implementations hold their safety/liveness properties despite concurrency, partial failures and delays.

## Why it matters
The state space is huge; unit tests miss rare interleavings and failure combinations.

## How it works
- **Formal verification / proofs**: prove the algorithm in the system model; does not guarantee the implementation.
- **Model checkers** (TLA+, Gallina, FizzBee): explore states of a simplified model against invariants; bounded, risk of spec/code drift. Used by CockroachDB, TiDB, Kafka; found data-loss ambiguity in viewstamped replication.
- **Fault injection**: kill/pause processes, unmount disks, break networks; **chaos engineering** is production fault injection (Netflix Chaos Monkey); **Jepsen** automates it and has found critical bugs in many databases.
- **Deterministic simulation testing (DST)**: runs the real code with network, I/O and clocks mocked so a simulator controls ordering and failures; failures are replayable. Needs all nondeterminism controllable (built in as FoundationDB's Flow or TigerBeetle, or via deterministic runtimes). Also property-based testing and fuzzing.

## Variants and techniques
Combination is recommended (AWS, FoundationDB, TigerBeetle).

## Trade-offs
Model checking: cheap but not the real code. Fault injection: real code but non-reproducible failures. DST: reproducible but requires architectural support.

## When to use it / when not to
Any consensus, replication or storage component; overkill for simple stateless services.

## Appears in
None yet.

## See also
Production-testing view (canaries, probers, stress and configuration tests, MTTR/MTBF argument) in [[release-engineering-and-canary-deployments]]; sizing note from the SRE Book (ch. 17): ~21,000 tests compared before and after a patch means each test must pass 99.9999%+ to accept 99 of 100 good patches.

[[distributed-system-faults]], [[consensus]], [[overload-and-metastable-failures]]
