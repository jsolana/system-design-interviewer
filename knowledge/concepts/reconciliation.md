---
title: Reconciliation
type: concept
aliases: [reconciliation, data reconciliation]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 11 Payment System, pp. 326-328; ch. 6 Ad Click Event Aggregation, p. 189]
---

# Reconciliation

## Definition
The practice of periodically comparing the state of related services (or against an external source) to verify that they match and to fix discrepancies; it is usually the **last line of defense** against asynchronous communication failures.

## Why it matters
With asynchronous communication there is no guarantee of delivery or response; reconciliation detects inconsistencies that idempotency and retries did not resolve (and one should not assume the external system is always right).

## How it works
- **Payments**: every night the PSP/bank sends a *settlement file* (balance and transactions of the day); it is compared with the ledger. Ledger vs wallet is also compared internally.
- Discrepancies fall into three categories: (1) classifiable and automatable (fixed by a program); (2) classifiable but not automatable (work queue for the finance team); (3) not classifiable (special queue for manual investigation).
- **Ad clicks**: an end-of-day batch that sorts events by event time and compares with the real-time result (there is no third party to reconcile with); smaller windows (1 h) for more precision; it will not match exactly because of late events.
- In the wallet case, reproducibility (event sourcing) makes it possible to know *how* the difference arose, which reconciliation alone does not explain.

## Variants and techniques
Lambda-style batch reconciliation (correcting the OLAP store from raw data, see [[ad-click-aggregator]]).

## Trade-offs
Detects but neither explains nor prevents; requires manual intervention in non-automatable cases.

## When to use it / when not to
Financial systems and aggregation pipelines where accuracy matters.

## Appears in
[[digital-wallet]], [[payment-system]]

## See also
[[double-entry-ledger]], [[idempotency]], [[exactly-once-processing]], [[payment-system]]
