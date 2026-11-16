---
title: Double-entry ledger
type: concept
aliases: [contabilidad de partida doble, ledger]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 11 Payment System, p. 322]
---

# Double-entry ledger

## Definition
Accounting principle whereby every transaction is recorded in **two accounts** with the same amount: one is debited and the other credited. The sum of all entries must be 0.

## Why it matters
Gives end-to-end traceability and consistency across the payment lifecycle; "a cent lost by someone is a cent gained by someone else". Key for later analysis (total revenue, forecasting).

## How it works
- Example: the user pays $1 to the seller -> $1 debit to the buyer and $1 credit to the seller.
- The ledger is append-only and immutable (see Square's Books service); the payment service updates it after the wallet and sets `ledger_updated`.
- It is reconciled with the settlement files from PSPs/banks ([[reconciliation]]).

## Variants and techniques
Event sourcing to rebuild balances by replaying the events ([[event-sourcing]]); in [[payment-system]] and [[digital-wallet]].

## Trade-offs
More writes and storage in exchange for auditability and integrity.

## When to use it / when not to
Any system that moves money. Not needed for counters with no financial value.

## Appears in
[[payment-system]]

## See also
[[reconciliation]], [[event-sourcing]], [[idempotency]]
