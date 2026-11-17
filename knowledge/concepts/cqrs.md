---
title: CQRS
type: concept
aliases: [command-query responsibility segregation, command query separation]
sources: [https://martinfowler.com/bliki/CQRS.html, https://microservices.io/patterns/data/cqrs.html, System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 12 Digital Wallet, pp. 360-361]
---

# CQRS

## Definition
A pattern that separates the write path (commands -> events -> state) from the read path: one state machine writes the state, and one or more read-only state machines build views from the published event stream.

## Why it matters
In event sourcing the external client does not see the state (balances). Instead of publishing the state, the **events** are published and each consumer rebuilds the view it needs; this enables custom views (balances, auditing of duplicate charges, state over a period).

## How it works
- Write path: command queue -> state machine (validates and generates events) -> event queue -> applies to state.
- Read path: read-only state machines read the event queue and rebuild historical state/views; a query service serves them.
- Eventually consistent: read views lag somewhat but always catch up.
- To give the user a near-immediate response, a **reverse proxy** is added that forwards the command and receives the state by *push* from the read state machine (instead of the client polling periodically).

## Variants and techniques
Pull (polling, not real time and adds overhead) vs push via reverse proxy; used in [[digital-wallet]].

## Trade-offs
Auditability and read flexibility at the cost of eventual consistency and greater complexity.

## When to use it / when not to
Systems with event sourcing and multiple read views (wallets, finance). Not for simple CRUD.

## Additional detail (Fowler, microservices.io)
- Fowler (credits Greg Young): a separate model to update than to read; they may share a DB, use separate DBs or processes. Benefits: independent modeling/optimization, separate read/write scaling, different access techniques, fits task-based UIs, events, event sourcing.
- Use in complex domains, large read/write skew, specific bounded contexts (not the whole system). Fowler warns it adds "risky complexity" to most systems; many attempts caused difficulty; if only a few queries hurt, a reporting database may be enough. Keeping two models consistent pushes toward eventual consistency.
- Microservices.io: with database-per-service, cross-service queries are hard, so build a read-only **view database** per query (often NoSQL) kept current by subscribing to domain events; drawbacks: complexity, duplicated code, replication lag. Alternative: API composition.
- Note: a senior answer mentions CQRS only where read patterns justify it and states the staleness window to the product owner.

## Appears in
[[digital-wallet]]

## See also
[[event-sourcing]], [[derived-data-and-dataflow]], [[digital-wallet]]
