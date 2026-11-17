---
title: Saga
type: concept
aliases: [saga pattern, compensating transactions]
sources: [https://microservices.io/patterns/data/saga.html, System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 12 pp. 349-355, System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 7 Hotel Reservation System, pp. 219-221]
---

# Saga

## Definition
Sequence of local transactions (one per service/database) in which each step commits its change and publishes a message that triggers the next; if a step fails, **compensating transactions** are run that undo the changes of the previous steps.

## Why it matters
In a microservices architecture with one DB per service, a logically atomic operation spans several DBs and doesn't fit in a single ACID transaction; there is a single happy path but many possible failures that produce inconsistencies.

## How it works
- Local steps chained by messages/events; **eventual** consistency.
- Each step has a compensating action (e.g. release the reservation if the payment fails).
- Contrast: 2PC gives a single atomic commit (ACID) but is blocking (a failed node halts progress) and low-performing; the saga relies on eventual consistency.

## Additional detail (Xu & Lam Vol. 2, ch. 12)
- **Linear** operations; with n steps you must prepare 2n operations (n normal and n compensations executed in reverse order). In a transfer the debit goes first and then the credit.
- **Choreography** (decentralized: each service reacts to events from others and maintains its state machine; hard to manage with many services) vs **orchestration** (a coordinator orders the steps; preferred in wallets).
- Compared with **TC/C (Try-Confirm/Cancel)**: both are application-level distributed transactions with compensation; TC/C compensates in the Cancel phase, allows parallel execution and requires an out-of-order flag (a Cancel may arrive before its Try); Saga compensates in the rollback and is sequential. With critical latency and many services, TC/C; otherwise, Saga. Progress state in a *phase status table*. See [[digital-wallet]].

## Additional detail (microservices.io)
- Source: https://microservices.io/patterns/data/saga.html. Example: an order must not exceed a customer's credit limit with Orders and Customers in separate DBs.
- **Choreography**: each local transaction publishes domain events that trigger the next steps (no coordinator). **Orchestration**: a central orchestrator tells participants which local transaction to run and processes replies.
- **No isolation (the "I" of ACID)**: concurrent sagas can read/write inconsistent data, so *countermeasures* are required (analysis-heavy; detailed in Richardson's book, not on the page).
- No automatic rollback: compensations must be written by hand.
- A service must update its DB and publish atomically: use [[transactional-outbox]] or [[event-sourcing]].
- A client that starts a saga synchronously needs the outcome: reply when the saga completes, or return an ID and let the client poll, or push a notification (WebSocket/webhook).
- Note: a senior answer names the missing isolation and the chosen countermeasure, plus idempotent steps and compensations.

## Variants and techniques
- Pragmatic alternative (hotel reservation): avoid the problem by storing inventory and reservations in the same relational DB (hybrid service) and leveraging ACID.
- See also orchestration in [[workflow-orchestration]].

## Trade-offs
Large increase in complexity (compensations, intermediate states, idempotency); decide whether it is worth it compared with a monolithic design at the service boundary.

## When to use it / when not to
When an operation crosses services with their own DBs and cannot be consolidated. Not when a single relational DB can cover the operation.

## Appears in
[[digital-wallet]], [[hotel-reservation]]

## See also
[[two-phase-commit]], [[workflow-orchestration]], [[idempotency]], [[transactions-and-isolation-levels]], [[event-sourcing]]
