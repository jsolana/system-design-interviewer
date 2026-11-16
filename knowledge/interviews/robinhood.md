---
title: Robinhood
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood]
concepts: [server-sent-events, pub-sub]
difficulty: high
---

# Robinhood

> Note: the page is mostly paywalled; the prompt, terms, functional requirements and deep dive titles are readable. Tagged pattern: Real-time Updates.

## Prompt
A commission-free trading platform with real-time market data and basic order management. It is a **broker**, not an exchange: it routes customer orders to external exchanges.

Terms: symbol (ticker), order (market: executes at the current price, only number of shares; limit: shares + target price, may remain pending until executed or canceled).
Assumed exchange interface: synchronous request/response API to place/cancel orders and a push feed per symbol (symbol, price per share, number of shares, orderId). It is worth clarifying this early with the interviewer.

## Functional requirements
- View live stock prices.
- Manage orders (create and cancel market/limit).
- Out of scope: after-hours, ETFs/options/crypto, real-time order book.

## Non-functional requirements
Not covered in the source (paywalled).

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source (two blocks: live prices and order management).

## Deep dives
Titles only: scaling live price updates; tracking order updates; order consistency.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[server-sent-events]], [[pub-sub]] (*Note*: indicative).

## Follow-up questions
The three deep dives.

## Variants
Not covered in the source.
