---
title: Stock Exchange
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 13 Stock Exchange, pp. 379-414]
concepts: [order-book, event-sourcing, consensus, write-ahead-log, rate-limiting, message-queues, multi-data-center, cdn-edge-computing]
difficulty: high
---

# Stock Exchange

## Prompt
Design an electronic stock exchange (like NYSE/Nasdaq at small-to-medium scale) that matches buyers and sellers with ultra-low latency and high reliability.

## Functional requirements
- Stocks only (no options or futures); **limit** orders: place new and cancel (no replace or market orders in the design); regular hours (no after-hours).
- Receive executions (fills) in real time; view the order book in real time.
- At least tens of thousands of concurrent users, 100 symbols and billions of orders per day.
- Simple risk checks (e.g. maximum 1 M Apple shares per day per user) and funds verification with a hold on the funds of pending orders in the wallet.

## Non-functional requirements
- Availability >= 99.99% (8.64 s of downtime per day).
- Fault tolerance and fast recovery.
- Latency: millisecond round-trip, focused on the **99th percentile** (from when an order enters until it comes back executed).
- Security: account management with KYC, DDoS protection for public resources. Extensible to more symbols and users.

## Estimations
- 100 symbols, 1,000 M orders/day; NYSE is open 6.5 h (9:30-16:00): QPS = 10^9 / (6.5 x 3,600) = **~43,000**; peak x5 = **215,000** (more volume at open and close).

## API
REST (institutions use specialized protocols, FIX):
- `POST /v1/order` (symbol, side, price, orderType, quantity) -> id, creationTime, filledQuantity, remainingQuantity, status (new/canceled/filled).
- `GET /v1/execution?symbol&orderId&startTime&endTime` -> executions.
- `GET /v1/marketdata/orderBook/L2?symbol&depth` -> bids and asks.
- `GET /v1/marketdata/candles?symbol&resolution&startTime&endTime` -> open/close/high/low.

## Data model
- **Product** (symbol, lotSize, tickSize, quote/settle currency; stable, cacheable), **Order** (orderID, productID, price, quantity, side, status, type, timeInForce, userID...) and **Execution** (execID, orderID, price, quantity, fees, execStatus...).
- On the critical path, orders and executions do not go to a DB: they are executed in memory and persisted to disk/shared memory via the sequencer (event store), with archiving at close; the reporter writes them to a DB for reporting.
- **Order book** and **candlestick chart** (see [[order-book]]); market data in an in-memory columnar DB (KDB) for real-time analytics and then moved to historical storage.

## Architecture (high-level design)
Business knowledge: brokers (Robinhood, Schwab...), institutional clients (high volume, order splitting; market makers with low latency), limit vs market orders, L1/L2/L3 levels, candlesticks and the FIX protocol.
Three flows:
- **Trading flow (critical path)**: broker -> **client gateway** (validation, rate limiting, authentication, normalization, FIX support; lightweight, with distinct gateways for retail, institutional and colocation) -> **order manager** (risk checks according to the risk manager, funds verification in the wallet; maintains order states, a source of complexity) -> **sequencer** (stamps a sequence on orders and executions, inbound and outbound; acts as a queue and event store; provides fairness, fast recovery and exactly-once) -> **matching engine** (maintains the order book per symbol, matches and emits two fills; must be deterministic) -> executions back to the client.
- **Market data flow**: executions -> market data publisher (builds order books and candlesticks) -> data service -> brokers.
- **Reporting flow**: reporter (combines attributes of orders and executions: client_id, price, quantity, order_type, filled/remaining) -> DB; critical for accuracy and compliance (history, taxes, compliance, settlement), not for latency.

## Deep dives
**Performance**: latency = sum of execution time on the critical path; it is reduced with fewer tasks on the path (not even logging) and less network/disk. A network hop ~500 µs and a disk write tens of ms -> tens of ms end to end, insufficient. Modern design: **everything on a single server** (sometimes a single process) with communication via **mmap** over `/dev/shm` (a message bus with no network or disk, sub-microsecond) -> tens of microseconds.
- **Application loop**: a single-threaded loop that polls tasks, **pinned to a CPU core** (no context switches or locks); trade-off: complexity and the risk of blocking the thread with long tasks.
- **Event sourcing** ([[event-sourcing]]): a single event store (mmap) with a sequence field injected by a **single-writer sequencer** (several sequencers would fight to write); the sequencer pulls events from each component's local ring buffers, assigns them a sequence and writes them; there are backup sequencers. The gateway converts FIX to **SBE** (Simple Binary Encoding); NewOrderEvent -> order manager (reusable library embedded in each component; identical, reproducible states) -> matching -> OrderFilledEvent; the market data processor and reporter subscribe. Without strict latency requirements, Kafka could be used.
- **High availability** (four nines): identify SPOFs; stateless services scale horizontally; stateful ones (order manager, matching engine) with **hot-warm** replicas: the warm one processes the same events without emitting and takes over when the hot one fails (heartbeats to detect); between machines/DCs the whole event store is replicated, e.g. with reliable UDP (Aeron).
- **Fault tolerance**: failover questions (when and how, how to elect a leader, RTO, RPO, degradation). What "down" means (false alarms; the same bug can take down the backup): manual failover at first, automate with experience and chaos engineering. Leader election with **Raft** (cluster of 5; minimum votes n/2+1 = 3; AppendEntries as heartbeat and replication to the followers' mmap event stores; election timeout, candidate, RequestVote, terms, split vote). **RTO** of seconds (automatic failover, prioritized services with a degradation strategy) and **RPO ~ 0** (Raft keeps consistent copies; the new leader works immediately).
- **Matching algorithm**: pseudocode of `handleOrder` (checks sequence, validates, NEW -> match against the opposite book, CANCEL -> remove and mark); FIFO; variants FIFO+LMM, dark pools.
- **Determinism**: functional (same event order = same results; real time does not matter, only the order, which speeds up replay) and **latency** (measured with p99 or p99.99, HdrHistogram; investigate spikes, e.g. safe points/stop-the-world GC in Java).
- **Market data publisher**: per-client levels (retail 5 L2 levels by default, more for a fee); ring buffers (preallocated, no alloc, lock-free, with cache line padding) for 1 min/1 h/1 day candlesticks and a memory limit with persistence.
- **Fairness in distribution**: all receivers must get the data at the same time; do not depend on connection order (assign random order) and use **multicast** with reliable UDP (retransmission by NACK). **Colocation**: brokers' servers in the exchange's data center (latency = cable length); considered a paid VIP service, it does not break fairness.
- **Network security (DDoS)**: isolate public services from private ones, read-only replicas, a cache layer, hardened URLs (`/data/recent` instead of arbitrary query strings, cacheable on a CDN), safelist/blocklist, rate limiting.

## Trade-offs and decisions
- Networked microservices (simple, tens of ms) vs **everything on one server with mmap** (tens of µs).
- Separate sequencer with messaging vs a single event store with a single-writer sequencer.
- Simple hot-warm vs multi-DC Raft cluster (more reliable).
- Automatic vs manual failover at first; cost of CPU pinning and the application loop.
- Kafka (if latency is not critical) vs mmap event store.

## Related concepts
[[order-book]], [[event-sourcing]], [[consensus]], [[write-ahead-log]], [[rate-limiting]], [[message-queues]], [[multi-data-center]], [[cdn-edge-computing]]

## Follow-up questions
- Extend to more symbols/users.
- Options and futures, market/conditional orders, after-hours.
- Failover when the replicas also fail; replication between cities.
- Crypto exchanges in the cloud and AMMs without an order book.

## Variants
Not covered in the source (see [[robinhood]] for the broker side of operations).
