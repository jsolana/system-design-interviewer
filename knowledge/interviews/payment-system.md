---
title: Payment System (Stripe-style)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system, System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 11 Payment System, pp. 315-339, Designing Data-Intensive Applications (Kleppmann), chs. 1 and 12]
concepts: [idempotency, message-queues, exactly-once-processing, double-entry-ledger, reconciliation, two-phase-commit, consensus, derived-data-and-dataflow]
difficulty: high
---

# Payment System

> Note: mostly paywalled page; only the prompt, functional requirements, scale and deep dive titles are readable. Tagged pattern: Multi-step Processes.

## Prompt
A Stripe-style payment processing system: merchants accept payments from customers without building their own infrastructure. The customer enters their details on the merchant's site, which sends them to the system; the system processes the payment and returns the result.

## Functional requirements
- The merchant initiates a payment request (charge an amount).
- The user pays with a credit/debit card.
- The merchant sees status updates (pending, success, failed).
- Out of scope: storing payment methods, refunds, history and reports, other methods, subscriptions, payouts.

## Non-functional requirements
Visible: ~10,000 TPS at peak. The rest is not covered in the source.

## Estimations
Only 10,000 peak TPS.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Titles only: initiate payments, pay with card, payment status.

## Deep dives
Titles only: security; durability and auditability (do not lose data on failures); transactional safety and financial integrity (asynchronous nature of external payment networks); scalability to 10k+ TPS (subsections Servers, Kafka, Database). Bonus: webhook support.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[idempotency]], [[message-queues]] (*Note*: indicative).

## Follow-up questions
Webhooks.

## Variants
- **Designing Data-Intensive Applications (Kleppmann), ch. 12 (transfer between accounts with logs)**: instead of an atomic commit ([[two-phase-commit]]) across the payer's partition, the payee's partition and the request ID table, an idempotent dataflow is used.
  1. The client generates a unique *request ID*; the transfer request is appended as **a single message** to a log partition chosen by request ID (a single-object write = atomic).
  2. A stream processor reads the log and emits two derived messages: debit (account A's partition) and credit (B's partition), both with the request ID.
  3. Downstream processors consume each stream, **deduplicate by request ID** and apply the change to the balance.
  - Differs from the base: eventual consistency with integrity guaranteed by idempotency/dedupe ([[exactly-once-processing]], [[idempotency]]) and no distributed transactions; constraints (non-negative balance) are checked sequentially in each account's partition. See [[derived-data-and-dataflow]].

### Xu & Lam Vol. 2, ch. 11 (pp. 315-339)
Source: System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 11 Payment System, pp. 315-339. It differs in approach: **payment backend for an Amazon-style e-commerce** (pay-in and pay-out), with a third-party PSP (Stripe, Braintree...), credit card only, no card numbers stored, a single currency and **1 M transactions/day = ~10 TPS**: the focus is correctness, not throughput. Requirements: pay-in (receive money from customers on behalf of sellers), pay-out (pay sellers), reliability and fault tolerance, and asynchronous **reconciliation** between internal and external systems.
- **Pay-in**: payment event -> payment service (AML/CFT risk check, normally third-party) -> payment executor (one payment order per PSP; one event can have several orders if there are several sellers) -> PSP (-> card schemes Visa/MasterCard) -> wallet (seller's balance) -> ledger (financial record). **Pay-out**: the same but with an accounts-payable provider (Tipalti) that moves money from the e-commerce account to the seller's account.
- **API**: `POST /v1/payments` (buyer_info, globally unique checkout_id, credit_card_info/token, payment_orders[seller_account, amount, currency ISO 4217, unique payment_order_id]) and `GET /v1/payments/{id}`. `amount` as a **string**, not a double (precision/rounding across protocols and extreme ranges); `payment_order_id` is the idempotency key toward the PSP.
- **Model**: tables `payment_event` (checkout_id PK, buyer_info, seller_info, credit_card_info, is_payment_done) and `payment_order` (payment_order_id PK, buyer_account, amount, currency, checkout_id FK, payment_order_status NOT_STARTED/EXECUTING/SUCCESS/FAILED, ledger_updated, wallet_updated). A relational DB with ACID is preferred over NoSQL/NewSQL for proven stability, tooling and the DBA market. A periodic job alerts on in-flight orders that exceed a threshold.
- **Double-entry ledger**: each transaction is recorded in two accounts (debit and credit, same amount); the sum of all entries is 0; end-to-end traceability (immutable ledger, like Square's Books service).
- PSP **hosted payment page** (iframe/widget/SDK) to avoid touching card data (PCI DSS): the payment service registers the payment with the PSP using a nonce (UUID = payment order id, exactly-once registration), receives a **token**, persists it and uses it to display the hosted page; the customer is redirected to the redirect URL and the PSP notifies the status by **webhook**. Alternative: API integration (the company collects and stores sensitive data) or direct connection to banks/card schemes (giants only).
- **Reconciliation**: last line of defense; every night the PSP/bank sends a *settlement file* that is compared with the ledger (and ledger vs wallet). Mismatches: classifiable and automatable, classifiable but not automatable (queue for finance), unclassifiable (special investigation queue).
- **Payment delays**: manual risk review or 3D Secure; the PSP returns *pending*, the client shows the status and the PSP notifies by webhook (or the payment service polls).
- **Internal communication**: synchronous (HTTP) is simple but has low performance, poor failure isolation, coupling and poor scalability; **asynchronous** with a queue (one receiver) or Kafka (multiple receivers: notifications, reporting, analytics), preferred at this scale.
- **Failed payments**: final payment status in an append-only table; **retry queue** (transient errors) and **dead letter queue** (retry threshold exceeded); non-retryable errors to the DB.
- **Exactly-once = at-least-once (retry) + at-most-once (idempotency)**. Retry strategies: immediate, fixed intervals, incremental, exponential backoff (1 s, 2 s, 4 s...), cancel; `Retry-After` header. Idempotency with an `idempotency-key` (client UUID; in e-commerce, the cart ID) and a DB unique constraint (insert first; if it fails, already seen -> return the previous state; concurrent requests with the same key -> 429). Scenario "PSP processed but the response was lost": the unique nonce/token per order makes the PSP recognize the duplicate.
- **Consistency**: between internal services, exactly-once; with the PSP, idempotency + reconciliation (do not assume the external party is always right); replicas: read and write only on the primary, or replicas synchronized with consensus (Paxos/Raft; YugabyteDB, CockroachDB).
- **Security**: HTTPS, encryption and integrity, SSL with certificate pinning, multi-region replication and snapshots, rate limiting and firewall (DDoS), card **tokenization**, PCI DSS, anti-fraud (AVS, CVV, behavioral analysis).
- Extras: monitoring, alerts, debugging tools, currency exchange, geography, cash payments (Uber/Airbnb), Google/Apple Pay.
