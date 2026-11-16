---
title: CQRS
type: concept
aliases: [command-query responsibility segregation, command query separation]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 12 Digital Wallet, pp. 360-361]
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

## Appears in
[[digital-wallet]]

## See also
[[event-sourcing]], [[derived-data-and-dataflow]], [[digital-wallet]]
