---
title: Order book
type: concept
aliases: [limit order book, order book, matching engine]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 13 Stock Exchange, pp. 382-398, 407-408]
---

# Order book

## Definition
List of buy (bids) and sell (asks) orders for an instrument, organized by price level; it is the key structure of an exchange's matching engine.

## Why it matters
Matching must be fast and exact: placing, canceling and executing orders must cost O(1) and it must be possible to query the best bid/ask and iterate over price levels.

## How it works
- Requirements: constant lookup of volume per price level, O(1) add/cancel/execute, fast update (replace), best bid/ask, iterating levels.
- Structure: `OrderBook` with `buyBook` and `sellBook` (each a map price -> `PriceLevel`), pointers to `bestBid`/`bestOffer` and a `Map<OrderID, Order>`. Each `PriceLevel` maintains `totalVolume` and a **doubly linked list** of orders (FIFO): new order = append to the tail O(1); match = remove from the head O(1); cancel = locate via the map and delete without traversing (the double link avoids searching for the previous node, which is O(n) with a singly linked list).
- Example: a buy of 2,700 shares consumes the whole queue of the best ask and part of the next level; the spread widens and the best ask moves up one level.
- Market data levels: **L1** (best bid/ask and quantities), **L2** (more price levels and aggregated quantity), **L3** (queued quantity per level, order by order).
- FIFO matching (the order that arrived first at a price is matched first); variants: FIFO with Lead Market Maker (allocates a portion to an LMM before the queue), dark pools.
- Each match produces two *executions* (fills), one per side. A limit order may be partially matched or not matched at all.

## Variants and techniques
- The market data publisher rebuilds the order book and the **candlesticks** (open/close/high/low/volume per interval: 1 min to 1 month) from the execution stream; candles in preallocated ring buffers and a limited number in memory, the rest on disk.
- Alternative in DeFi: AMM (automatic market making) with no order book.

## Trade-offs
Performance (linked lists + maps) versus complexity; deterministic matching enables replay and high availability (see [[stock-exchange]]).

## When to use it / when not to
Exchanges and supply-demand matching systems by price. Not for simple auctions.

## Appears in
[[stock-exchange]]

## See also
[[stock-exchange]], [[event-sourcing]], [[consensus]]
